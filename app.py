import os
import re
import shutil
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import tkinter as tk
from tkinter import filedialog
import yt_dlp


app = Flask(__name__)

DEFAULT_DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")
app.config["DOWNLOAD_FOLDER"] = DEFAULT_DOWNLOAD_FOLDER
os.makedirs(DEFAULT_DOWNLOAD_FOLDER, exist_ok=True)

# Navegador usado para intentar leer cookies en contenido que requiere sesión.
# Puedes cambiarlo por: chrome, firefox, edge, brave, opera o chromium.
COOKIE_BROWSER = os.getenv("MEDIA_EXTRACTOR_BROWSER", "chrome").strip().lower()

SUPPORTED_PLATFORM_NAMES = {
    "youtube": "YouTube",
    "instagram": "Instagram",
    "tiktok": "TikTok",
    "facebook": "Facebook",
    "generic": "Sitio compatible",
}


def resolve_download_folder(folder_value: str | None) -> str:
    """Normaliza y crea la carpeta de descarga."""
    base_folder = (folder_value or "").strip()

    if not base_folder:
        return DEFAULT_DOWNLOAD_FOLDER

    expanded = os.path.expanduser(os.path.expandvars(base_folder))

    if not os.path.isabs(expanded):
        expanded = os.path.abspath(expanded)

    os.makedirs(expanded, exist_ok=True)
    return expanded


def resolve_destination_folder(folder_value: str | None) -> str:
    """Resuelve carpetas predefinidas o una ruta personalizada."""
    presets = {
        "downloads": DEFAULT_DOWNLOAD_FOLDER,
        "desktop": str(Path.home() / "Desktop"),
        "documents": str(Path.home() / "Documents"),
        "videos": str(Path.home() / "Videos"),
        "music": str(Path.home() / "Music"),
    }

    if not folder_value:
        return DEFAULT_DOWNLOAD_FOLDER

    if folder_value in presets:
        target = presets[folder_value]
        os.makedirs(target, exist_ok=True)
        return target

    return resolve_download_folder(folder_value)


def get_selected_folder() -> tuple[str, str, str]:
    """Obtiene y resuelve la carpeta seleccionada en el formulario."""
    selected_folder = request.form.get("download_folder", "downloads")
    custom_folder = request.form.get("custom_folder", "").strip()

    if selected_folder == "custom":
        resolved_folder = (
            resolve_destination_folder(custom_folder)
            if custom_folder
            else DEFAULT_DOWNLOAD_FOLDER
        )
    else:
        resolved_folder = resolve_destination_folder(selected_folder)

    return resolved_folder, selected_folder, custom_folder


def validate_url(url: str) -> bool:
    """Valida de forma básica que la entrada sea una URL HTTP o HTTPS."""
    return bool(re.match(r"^https?://\S+$", url.strip(), re.IGNORECASE))


def detect_platform(url: str) -> str:
    """Identifica la plataforma a partir del dominio."""
    clean_url = url.strip().lower()

    patterns = {
        "youtube": (
            r"^https?://(?:www\.)?(?:youtube\.com|youtu\.be)/"
        ),
        "instagram": (
            r"^https?://(?:www\.)?(?:instagram\.com|instagr\.am)/"
        ),
        "tiktok": (
            r"^https?://(?:www\.|m\.|vm\.)?"
            r"(?:tiktok\.com|tiktokv\.com)/"
        ),
        "facebook": (
            r"^https?://(?:www\.|m\.|web\.)?"
            r"(?:facebook\.com|fb\.watch|fb\.com)/"
        ),
    }

    for platform, pattern in patterns.items():
        if re.search(pattern, clean_url, re.IGNORECASE):
            return platform

    return "generic"


def has_ffmpeg() -> bool:
    """Comprueba que FFmpeg y FFprobe estén disponibles en el PATH."""
    ffmpeg = shutil.which("ffmpeg") or shutil.which("ffmpeg.exe")
    ffprobe = shutil.which("ffprobe") or shutil.which("ffprobe.exe")
    return bool(ffmpeg and ffprobe)


def platform_display_name(platform: str) -> str:
    return SUPPORTED_PLATFORM_NAMES.get(platform, "Sitio compatible")


QUALITY_ALIASES = {
    "maximum": "best",
    "max": "best",
    "best": "best",
    "2160p": "best",
    "4k": "best",
    "high": "1080",
    "1080": "1080",
    "1080p": "1080",
    "medium": "720",
    "720": "720",
    "720p": "720",
    "low": "360",
    "360": "360",
    "360p": "360",
    "lowest": "lowest",
    "worst": "lowest",
}


def normalize_quality(quality: str | None) -> str:
    """Normaliza los valores enviados por el formulario."""
    clean_quality = (quality or "best").strip().lower()
    return QUALITY_ALIASES.get(clean_quality, "best")


def base_ydl_options() -> dict[str, Any]:
    """Opciones generales compartidas por análisis y descarga."""
    return {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "socket_timeout": 45,
        "retries": 10,
        "fragment_retries": 10,
        "extractor_retries": 5,
        "file_access_retries": 5,
        "continuedl": True,
        "concurrent_fragment_downloads": 4,
        "check_formats": "selected",
        "extract_flat": False,
        "windowsfilenames": True,
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
        },
    }


def apply_platform_options(
    options: dict[str, Any],
    url: str,
    *,
    use_browser_cookies: bool = True,
) -> str:
    """
    Agrega opciones específicas para Instagram, TikTok y Facebook.

    Instagram y Facebook suelen requerir cookies para contenido privado,
    restringido por edad o visible solo al iniciar sesión.
    """
    platform = detect_platform(url)

    if (
        use_browser_cookies
        and COOKIE_BROWSER
        and platform in {"instagram", "facebook"}
    ):
        options["cookiesfrombrowser"] = (COOKIE_BROWSER,)

    # No se fija manualmente un host de API para TikTok. yt-dlp elige
    # automáticamente el cliente y el endpoint compatibles con su versión.

    return platform


def build_download_options(
    format_type: str,
    ffmpeg_available: bool | None = None,
    download_folder: str | None = None,
    quality: str = "best",
) -> dict[str, Any]:
    """Construye las opciones respetando la calidad elegida por el usuario.

    La selección no limita primero por extensión. Esto evita perder la máxima
    resolución cuando el mejor video solo existe como WebM, VP9 o AV1.
    FFmpeg combina el mejor video con el mejor audio sin recodificarlos.
    """
    ffmpeg_available = (
        has_ffmpeg()
        if ffmpeg_available is None
        else ffmpeg_available
    )
    normalized_quality = normalize_quality(quality)

    target_folder = resolve_download_folder(download_folder)
    output_template = os.path.join(
        target_folder,
        "%(title).180B [%(id)s].%(ext)s",
    )

    common_options: dict[str, Any] = {
        **base_ydl_options(),
        "outtmpl": output_template,
        "overwrites": False,
    }

    if format_type == "mp3":
        return {
            **common_options,
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "0",
                }
            ],
        }

    if ffmpeg_available:
        # El selector oficial de yt-dlp para la mejor calidad disponible.
        # Descarga video y audio separados cuando es necesario y los combina.
        video_options: dict[str, Any] = {
            **common_options,
            "format": "bv*+ba/b",
            # MP4 cuando los codecs lo permiten; MKV como respaldo para no
            # recodificar ni perder calidad con AV1, VP9 u Opus.
            "merge_output_format": "mp4/mkv",
        }

        if normalized_quality == "1080":
            video_options["format_sort"] = [
                "res:1080",
                "fps",
                "hdr:12",
                "vcodec",
                "channels",
                "acodec",
                "br",
            ]
        elif normalized_quality == "720":
            video_options["format_sort"] = [
                "res:720",
                "fps",
                "hdr:12",
                "vcodec",
                "channels",
                "acodec",
                "br",
            ]
        elif normalized_quality == "360":
            video_options["format_sort"] = [
                "res:360",
                "fps",
                "vcodec",
                "channels",
                "acodec",
                "br",
            ]
        elif normalized_quality == "lowest":
            video_options["format_sort"] = [
                "+res",
                "+fps",
                "+br",
            ]

        # Para "best" no se agrega límite: yt-dlp elige la resolución, FPS,
        # HDR, video y audio de mayor calidad ofrecidos por la plataforma.
        return video_options

    # Sin FFmpeg solo se pueden usar formatos que ya traen audio y video.
    # Esto evita descargar un archivo de video sin sonido, pero no garantiza
    # la máxima calidad de YouTube, que normalmente viene en pistas separadas.
    combined_options: dict[str, Any] = {
        **common_options,
        "format": "b[ext=mp4]/b",
    }

    if normalized_quality == "1080":
        combined_options["format_sort"] = ["res:1080", "fps", "br"]
    elif normalized_quality == "720":
        combined_options["format_sort"] = ["res:720", "fps", "br"]
    elif normalized_quality == "360":
        combined_options["format_sort"] = ["res:360", "fps", "br"]
    elif normalized_quality == "lowest":
        combined_options["format_sort"] = ["+res", "+fps", "+br"]

    return combined_options


def find_downloaded_file(
    title: str,
    download_folder: str | None = None,
) -> str | None:
    """Busca el archivo descargado más reciente relacionado con el título."""
    folder = Path(resolve_download_folder(download_folder))

    if not folder.exists():
        return None

    candidates = sorted(
        (path for path in folder.iterdir() if path.is_file()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    normalized_title = secure_filename(title).lower()

    for path in candidates:
        normalized_name = secure_filename(path.stem).lower()

        if normalized_title and normalized_title in normalized_name:
            return path.name

    return candidates[0].name if candidates else None


def should_retry_without_cookies(error: Exception) -> bool:
    """Detecta errores frecuentes al leer cookies del navegador."""
    message = str(error).lower()

    cookie_markers = (
        "could not copy chrome cookie database",
        "could not copy edge cookie database",
        "could not copy firefox cookie database",
        "permission denied",
        "cookiesfrombrowser",
        "cookie database",
        "failed to decrypt",
    )

    return any(marker in message for marker in cookie_markers)


def extract_media_info(
    url: str,
    options: dict[str, Any],
    *,
    download: bool,
) -> tuple[dict[str, Any], str, bool]:
    """
    Ejecuta yt-dlp.

    Si Instagram o Facebook fallan únicamente por la lectura de cookies,
    vuelve a intentar sin cookies para contenido público.
    """
    platform = apply_platform_options(options, url, use_browser_cookies=True)

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=download)

        return info, platform, False

    except Exception as exc:
        if "cookiesfrombrowser" in options and should_retry_without_cookies(exc):
            retry_options = dict(options)
            retry_options.pop("cookiesfrombrowser", None)

            with yt_dlp.YoutubeDL(retry_options) as ydl:
                info = ydl.extract_info(url, download=download)

            return info, platform, True

        raise


def humanize_error(error: Exception, platform: str) -> str:
    """Transforma errores técnicos frecuentes en mensajes claros."""
    message = str(error)
    message_lower = message.lower()
    platform_name = platform_display_name(platform)

    if "unsupported url" in message_lower:
        return (
            f"El enlace de {platform_name} no es compatible o no apunta "
            "directamente a una publicación, reel o video."
        )

    if any(
        marker in message_lower
        for marker in (
            "login required",
            "sign in",
            "private",
            "not available",
            "cookies",
            "checkpoint",
        )
    ):
        return (
            f"{platform_name} solicita iniciar sesión o el contenido es "
            f"privado/restringido. Inicia sesión en {COOKIE_BROWSER.title()} "
            "y vuelve a intentarlo."
        )

    if "requested format is not available" in message_lower:
        return (
            "La plataforma no ofreció un formato compatible con la selección. "
            "Actualiza yt-dlp y verifica que FFmpeg y FFprobe estén instalados. "
            "La opción de máxima calidad necesita combinar video y audio."
        )

    if "ffmpeg" in message_lower or "ffprobe" in message_lower:
        return (
            "FFmpeg o FFprobe no están disponibles o no están configurados "
            "correctamente en el PATH."
        )

    if any(
        marker in message_lower
        for marker in ("403", "forbidden", "429", "too many requests")
    ):
        return (
            f"{platform_name} bloqueó temporalmente la solicitud. "
            "Actualiza yt-dlp y vuelve a intentarlo más tarde."
        )

    return f"No se pudo procesar el enlace: {message}"


@app.route("/logo/<path:filename>")
def logo_file(filename):
    logo_dir = os.path.join(app.root_path, "templates", "logo")
    return send_from_directory(logo_dir, filename)


@app.route("/choose-folder")
def choose_folder():
    root = None

    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        selected = filedialog.askdirectory(
            title="Selecciona una carpeta de destino"
        )

        return jsonify({"folder": selected or ""})

    except Exception as exc:
        return jsonify(
            {
                "folder": "",
                "error": f"No se pudo abrir el selector: {exc}",
            }
        ), 500

    finally:
        if root is not None:
            try:
                root.destroy()
            except tk.TclError:
                pass


@app.route("/")
def index():
    return render_template(
        "index.html",
        selected_folder="downloads",
        download_folder=DEFAULT_DOWNLOAD_FOLDER,
        format_type="mp4",
        quality="best",
        supported_platforms="YouTube, TikTok, Instagram y Facebook",
    )


@app.route("/analyze", methods=["POST"])
def analyze():
    url = request.form.get("url", "").strip()
    format_type = request.form.get("format", "mp4")
    quality = request.form.get("quality", "best")

    resolved_folder, selected_folder, custom_folder = get_selected_folder()
    platform = detect_platform(url)

    common_template_data = {
        "download_folder": resolved_folder,
        "format_type": format_type,
        "quality": quality,
        "selected_folder": selected_folder,
        "custom_folder": custom_folder,
        "supported_platforms": "YouTube, TikTok, Instagram y Facebook",
        "detected_platform": platform_display_name(platform),
    }

    if not validate_url(url):
        return render_template(
            "index.html",
            error="Ingresa un enlace HTTP o HTTPS válido.",
            **common_template_data,
        )

    options = {
        **base_ydl_options(),
        "skip_download": True,
    }

    try:
        info, platform, cookies_skipped = extract_media_info(
            url,
            options,
            download=False,
        )

        title = info.get("title") or "media"
        uploader = info.get("uploader") or info.get("channel") or "Desconocido"
        duration = info.get("duration")

        duration_text = None

        if duration is not None:
            minutes, seconds = divmod(int(duration), 60)
            hours, minutes = divmod(minutes, 60)

            parts = []

            if hours:
                parts.append(f"{hours}h")

            if minutes or hours:
                parts.append(f"{minutes}m")

            parts.append(f"{seconds}s")
            duration_text = " ".join(parts)

        cookie_notice = None

        if cookies_skipped:
            cookie_notice = (
                "No se pudieron leer las cookies del navegador, "
                "pero el contenido público sí pudo analizarse."
            )

        return render_template(
            "index.html",
            analyze_success=(
                f"Enlace de {platform_display_name(platform)} "
                f"analizado correctamente."
            ),
            analyze_title=title,
            analyze_uploader=uploader,
            analyze_duration=duration_text,
            analyze_thumbnail=info.get("thumbnail"),
            cookie_notice=cookie_notice,
            **common_template_data,
        )

    except Exception as exc:
        return render_template(
            "index.html",
            error=humanize_error(exc, platform),
            **common_template_data,
        )


@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url", "").strip()
    format_type = request.form.get("format", "mp4")
    quality = request.form.get("quality", "best")
    normalized_quality = normalize_quality(quality)

    resolved_folder, selected_folder, custom_folder = get_selected_folder()
    platform = detect_platform(url)

    common_template_data = {
        "download_folder": resolved_folder,
        "format_type": format_type,
        "quality": quality,
        "selected_folder": selected_folder,
        "custom_folder": custom_folder,
        "supported_platforms": "YouTube, TikTok, Instagram y Facebook",
        "detected_platform": platform_display_name(platform),
    }

    if not validate_url(url):
        return render_template(
            "index.html",
            error="Ingresa un enlace HTTP o HTTPS válido.",
            **common_template_data,
        )

    ffmpeg_available = has_ffmpeg()

    if format_type == "mp3" and not ffmpeg_available:
        return render_template(
            "index.html",
            error=(
                "Para convertir a MP3 necesitas FFmpeg y FFprobe instalados "
                "y agregados al PATH."
            ),
            **common_template_data,
        )

    if (
        format_type != "mp3"
        and platform == "youtube"
        and normalized_quality == "best"
        and not ffmpeg_available
    ):
        return render_template(
            "index.html",
            error=(
                "Para descargar la máxima calidad de YouTube necesitas "
                "FFmpeg y FFprobe. YouTube suele entregar el video y el "
                "audio por separado; sin FFmpeg solo sería posible descargar "
                "una versión combinada de menor calidad."
            ),
            **common_template_data,
        )

    options = build_download_options(
        format_type=format_type,
        ffmpeg_available=ffmpeg_available,
        download_folder=resolved_folder,
        quality=normalized_quality,
    )

    try:
        info, platform, cookies_skipped = extract_media_info(
            url,
            options,
            download=True,
        )

        title = info.get("title") or "media"
        downloaded_file = find_downloaded_file(title, resolved_folder)

        if downloaded_file is None:
            extension = ".mp3" if format_type == "mp3" else ".mp4"
            downloaded_file = secure_filename(title) + extension

        cookie_notice = None

        if cookies_skipped:
            cookie_notice = (
                "La descarga pública se completó sin usar cookies "
                "del navegador."
            )

        return render_template(
            "index.html",
            success=(
                f"Descarga de {platform_display_name(platform)} "
                f"completada: {title}"
            ),
            file_name=downloaded_file,
            cookie_notice=cookie_notice,
            **common_template_data,
        )

    except Exception as exc:
        return render_template(
            "index.html",
            error=humanize_error(exc, platform),
            **common_template_data,
        )


@app.route("/files/<path:filename>")
def files(filename):
    folder = resolve_download_folder(
        request.args.get("folder", DEFAULT_DOWNLOAD_FOLDER)
    )

    return send_from_directory(
        folder,
        filename,
        as_attachment=True,
    )


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000,
        threaded=False,
    )