# Media Extractors

Aplicación web local para analizar, convertir y descargar contenido multimedia desde enlaces compatibles.

<div align="center">

  <p><strong>Flask</strong> · <strong>yt-dlp</strong> · <strong>FFmpeg</strong> · <strong>Python</strong></p>

</div>

## ✨ Descripción

Media Extractors es una herramienta local diseñada para ayudar a descargar contenido multimedia de forma sencilla desde una interfaz web. Permite analizar enlaces, elegir el formato deseado y guardar los archivos directamente en tu equipo.

## 🚀 Funcionalidades

- Análisis previo de enlaces compatibles.
- Descarga en formato MP4 o MP3.
- Selección de calidad de video.
- Elección de carpeta de destino.
- Vista previa de información como título, autor, duración y miniatura.
- Compatibilidad con cookies del navegador para algunos sitios restringidos.

## 🛠️ Tecnologías

- Python
- Flask
- Jinja2
- yt-dlp
- FFmpeg
- HTML, CSS y JavaScript
- Tkinter para el selector de carpetas

## ✅ Requisitos

Antes de iniciar, asegúrate de tener:

- Windows 10 o 11
- Python 3.10 o superior
- pip
- FFmpeg instalado y agregado al PATH
- Conexión a Internet

## 📦 Instalación

1. Clona el repositorio:

```bash
git clone <url-del-repositorio>
cd Media-estractors
```

2. Crea y activa un entorno virtual:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. Instala las dependencias:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4. Verifica que FFmpeg esté disponible:

```bash
ffmpeg -version
```

## ▶️ Uso

1. Ejecuta la aplicación:

```bash
python app.py
```

2. Abre la siguiente URL en tu navegador:

```text
http://127.0.0.1:5000
```

3. Pega un enlace compatible, selecciona el formato y la calidad, elige la carpeta de destino y pulsa Descargar.

## 📁 Estructura del proyecto

```text
Media-estractors/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── downloads/
├── tests/
└── README.md
```

## ⚠️ Notas importantes

- La compatibilidad depende de yt-dlp y de las reglas de cada plataforma.
- Algunos sitios pueden requerir iniciar sesión o usar cookies del navegador.
- Los archivos descargados se guardan localmente en la carpeta seleccionada.

## 🔧 Solución de problemas

- Si la app no inicia, revisa que Python y FFmpeg estén correctamente instalados.
- Si FFmpeg no funciona, vuelve a agregarlo al PATH.
- Si un enlace falla, intenta actualizar yt-dlp:

```bash
python -m pip install --upgrade yt-dlp
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar el proyecto, puedes abrir un issue o enviar un pull request.

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.
