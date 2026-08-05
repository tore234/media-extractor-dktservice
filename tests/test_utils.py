from pathlib import Path

from app import app, build_download_options, is_instagram_url, resolve_destination_folder, validate_url


def test_validate_url_accepts_http_links():
    assert validate_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ") is True
    assert validate_url("https://www.instagram.com/p/abc123/") is True
    assert validate_url("not-a-url") is False


def test_is_instagram_url_detects_instagram_links():
    assert is_instagram_url("https://www.instagram.com/p/abc123/") is True
    assert is_instagram_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ") is False


def test_build_download_options_uses_audio_preset_for_mp3():
    options = build_download_options("mp3", ffmpeg_available=False)
    assert options["format"] == "bestaudio/best"


def test_build_download_options_falls_back_for_mp4_without_ffmpeg():
    options = build_download_options("mp4", ffmpeg_available=False)
    assert options["format"] == "best[ext=mp4]/best"


def test_build_download_options_uses_requested_quality():
    options = build_download_options("mp4", ffmpeg_available=False, quality="low")
    assert options["format"] == "18/18"


def test_resolve_destination_folder_uses_desktop_when_selected():
    home = str(Path.home())
    assert resolve_destination_folder("desktop") == str(Path(home) / "Desktop")


def test_choose_folder_route_returns_selected_path(monkeypatch):
    class FakeTk:
        def withdraw(self):
            return None

        def attributes(self, *_args, **_kwargs):
            return None

        def destroy(self):
            return None

    monkeypatch.setattr("app.tk.Tk", lambda: FakeTk())
    monkeypatch.setattr("app.filedialog.askdirectory", lambda title=None: r"C:\\Users\\demo\\Desktop")

    client = app.test_client()
    response = client.get('/choose-folder')

    assert response.status_code == 200
    assert response.get_json()['folder'] == r"C:\Users\demo\Desktop"


def test_analyze_route_returns_metadata(monkeypatch):
    class FakeYDL:
        def __init__(self, options):
            self.options = options

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def extract_info(self, url, download=False):
            return {
                "title": "Demo title",
                "uploader": "Demo uploader",
                "duration": 93,
                "thumbnail": "https://example.com/thumb.jpg",
            }

    monkeypatch.setattr("app.yt_dlp.YoutubeDL", FakeYDL)

    client = app.test_client()
    response = client.post(
        "/analyze",
        data={
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "format": "mp4",
            "quality": "best",
            "download_folder": "",
        },
    )

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Enlace analizado correctamente" in html
    assert "Demo title" in html
