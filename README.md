blioteca
/
README_MAIN_PRO.md


🩸 Media Extractor DKTService
<div align="center">

<img src="app/templates/logo/banner.png" alt="Banner de Media Extractor DKTService" width="100%">

<br>

Aplicación web local para analizar y descargar contenido multimedia desde enlaces compatibles usando Flask, yt-dlp y FFmpeg.

## Descripción

Media Extractors permite:

- Analizar un enlace antes de descargarlo.
- Elegir entre formato MP4 o MP3.
- Definir la calidad de descarga.
- Seleccionar una carpeta de destino.
- Descargar el archivo de forma local en el equipo.

La interfaz se abre en el navegador y el procesamiento se realiza de forma local.

## Requisitos

- Windows 10 o 11
- Python 3.10 o superior
- pip
- FFmpeg instalado y agregado al PATH
- Conexión a Internet

## Instalación

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

4. Asegúrate de tener FFmpeg disponible:
   ```bash
   ffmpeg -version
   ```

## Uso

1. Ejecuta la aplicación:
   ```bash
   python app.py
   ```

http://127.0.0.1:5000
⚡ Instalación automática en Windows
Cuando el repositorio incluya los scripts preparados, el usuario podrá ejecutar:

instalar.bat
Después:

iniciar.bat
Para actualizar Flask y yt-dlp:

actualizar.bat
📦 requirements.txt
Contenido recomendado:

Flask>=3.1,<4
Werkzeug>=3.1,<4
yt-dlp
FFmpeg se instala de forma independiente y no mediante pip.

🎯 Uso
Ejecuta iniciar.bat o python app.py.

Abre http://127.0.0.1:5000.

Pega un enlace compatible.

Selecciona MP4 o MP3.

Elige la calidad.

Selecciona la carpeta de destino.

Presiona Analizar enlace para revisar la información.

Presiona Descargar ahora.

Espera el mensaje de confirmación.

Abre el archivo desde la interfaz o desde la carpeta seleccionada.

🍪 Instagram y Facebook
Algunos enlaces pueden solicitar una sesión válida.

La aplicación puede intentar leer las cookies del navegador configurado:

COOKIE_BROWSER = "chrome"
También puedes establecerlo mediante una variable de entorno:

$env:MEDIA_EXTRACTOR_BROWSER="edge"
python app.py
Valores comunes:

chrome
edge
firefox
brave
opera
chromium
Recomendaciones
Inicia sesión en la plataforma desde el navegador elegido.

Cierra completamente el navegador antes de probar.

No publiques archivos cookies.txt.

No compartas cookies ni sesiones personales.

Utiliza únicamente contenido para el que tengas autorización.

🔄 Actualizar yt-dlp
Las plataformas cambian frecuentemente. Actualiza yt-dlp cuando una descarga deje de funcionar:

python -m pip install --upgrade yt-dlp
Para actualizar todas las dependencias principales:

python -m pip install --upgrade Flask Werkzeug yt-dlp
🛠️ Solución de problemas
La página no abre
Ejecuta:

python app.py
Debes ver:

Running on http://127.0.0.1:5000
FFmpeg no está disponible
Comprueba:

ffmpeg -version
Si no se reconoce el comando, instala FFmpeg y agrégalo al PATH.

PowerShell bloquea el entorno virtual
Ejecuta:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
Después:

.venv\Scripts\Activate.ps1
Instagram solicita iniciar sesión
Inicia sesión en Chrome, Edge o Firefox.

Cierra completamente el navegador.

Actualiza yt-dlp.

Prueba otra vez.

Confirma que el contenido sea público o accesible con tu cuenta.

El puerto 5000 está ocupado
Comprueba:

netstat -ano | findstr :5000
También puedes cambiar el puerto en app.py:

app.run(
    host="127.0.0.1",
    port=5001,
    debug=True,
    threaded=False,
)
🔐 Seguridad y privacidad
Media Extractor está pensado para ejecutarse localmente.

Los enlaces se procesan en la computadora del usuario.

Los archivos se guardan en la carpeta seleccionada.

No se requiere almacenamiento permanente en la nube.

Las cookies y sesiones deben permanecer fuera del repositorio.

La aplicación no debe exponerse públicamente con debug=True.

No ejecutes archivos descargados que no sean de confianza.

El .gitignore debe incluir:

.venv/
__pycache__/
app/downloads/*
!app/downloads/.gitkeep
cookies.txt
*.cookies.txt
.env
.env.*
build/
dist/
*.spec
⚖️ Uso responsable
Esta herramienta debe utilizarse únicamente para:

Contenido propio.

Material de dominio público.

Recursos con licencia compatible.

Contenido para el que exista autorización.

Copias permitidas por la legislación y los términos aplicables.

El usuario es responsable de comprobar que tiene derecho a descargar, convertir o reutilizar cada contenido.

🌿 Ramas del proyecto
main
└── Aplicación local estable

web
└── Página pública y documentación para Vercel

develop
└── Desarrollo y pruebas futuras
Cambiar a la aplicación local:

git switch main
Cambiar a la página web:

git switch web
🗺️ Roadmap
Interfaz web local.

Descarga MP4.

Conversión MP3.

Selección de calidad.

Selector de carpeta.

Análisis previo.

Soporte inicial para redes sociales.

Barra de progreso en tiempo real.

Cancelación de descargas.

Historial local.

Descarga por lotes.

Lista de reproducción opcional.

Empaquetado como .exe.

Instalador de Windows.

Actualizador interno.

Pruebas automatizadas.

Publicación de versiones mediante GitHub Releases.

Página pública de descarga en Vercel.

🤝 Contribuciones
Haz un fork del repositorio.

Crea una rama:

git switch -c feature/nueva-funcion
Guarda tus cambios:

git add .
git commit -m "Agrega nueva función"
Sube la rama:

git push -u origin feature/nueva-funcion
Abre un Pull Request hacia main.

📝 Convención de commits
Ejemplos:

feat: agrega barra de progreso
fix: corrige selección de carpeta
docs: actualiza guía de instalación
style: mejora diseño de la interfaz
refactor: reorganiza opciones de yt-dlp
chore: actualiza dependencias
📜 Licencia
Este proyecto puede distribuirse bajo la licencia MIT, siempre que se conserve el aviso correspondiente.

Consulta el archivo:

LICENSE
👤 Autor
DKTService

Proyecto orientado a facilitar el análisis, conversión y descarga local de contenido multimedia mediante herramientas de código abierto.

<div align="center">

🩸 MEDIA EXTRACTOR DKTService
Analiza. Convierte. Descarga.

Desarrollado con Python, Flask, yt-dlp y FFmpeg.

</div>