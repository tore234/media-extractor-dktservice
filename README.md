🩸 Media Extractor DKTService
<div align="center">

<img src="app/templates/logo/banner.png" alt="Banner de Media Extractor DKTService" width="100%">

<br>

Aplicación local para analizar, convertir y descargar contenido multimedia
Convierte contenido compatible a MP4 o MP3 mediante una interfaz web local construida con Flask, yt-dlp y FFmpeg.

<br>








</div>

📌 Descripción
Media Extractor DKTService es una aplicación local que permite analizar enlaces multimedia, elegir el formato y la calidad, seleccionar una carpeta de destino y guardar el resultado directamente en el equipo del usuario.

Aunque la interfaz se abre en el navegador, el procesamiento se ejecuta localmente en la computadora mediante Flask, yt-dlp y FFmpeg.

Navegador local
      ↓
Flask en 127.0.0.1
      ↓
yt-dlp + FFmpeg
      ↓
Archivo guardado en el equipo
✨ Funciones principales
🎬 Descarga de contenido compatible en formato MP4.

🎧 Extracción y conversión de audio a MP3.

🔎 Análisis previo del enlace.

🖼️ Vista previa con título, autor, duración y miniatura.

🎚️ Selección de calidad:

Máxima.

Alta, hasta 1080p.

Media, hasta 720p.

Baja, hasta 360p.

Mínima.

📁 Selección de carpeta de destino.

🖥️ Interfaz local adaptable a PC y dispositivos móviles dentro de la red.

🍪 Compatibilidad opcional con cookies del navegador para contenido que exige sesión.

⚠️ Mensajes claros de error y confirmación.

🩸 Diseño visual negro, rojo oscuro y carmesí de DKTService.

🌐 Plataformas contempladas
La aplicación utiliza los extractores disponibles en yt-dlp y está preparada para trabajar con enlaces compatibles de:

Plataforma	Contenido público	Contenido con sesión
YouTube	✅	Según disponibilidad
TikTok	✅	Limitado
Instagram	✅	Puede requerir cookies
Facebook	✅	Puede requerir cookies
La compatibilidad puede cambiar cuando las plataformas modifican sus sistemas. Mantén yt-dlp actualizado.

🧰 Tecnologías
Tecnología	Función
Python	Lógica principal
Flask	Servidor web local
Jinja2	Renderizado de la interfaz
yt-dlp	Análisis y descarga multimedia
FFmpeg	Conversión, extracción y unión de audio/video
HTML5	Estructura de la interfaz
CSS3	Diseño visual
JavaScript	Interacciones del formulario
Tkinter	Selector local de carpetas
📂 Estructura del repositorio
media-extractor-dktservice/
│
├── app/
│   ├── app.py
│   ├── requirements.txt
│   ├── instalar.bat
│   ├── iniciar.bat
│   ├── actualizar.bat
│   │
│   ├── templates/
│   │   ├── index.html
│   │   └── logo/
│   │       ├── logo.png
│   │       └── banner.png
│   │
│   └── downloads/
│       └── .gitkeep
│
├── docs/
│   ├── instalacion.md
│   ├── ffmpeg.md
│   └── problemas-frecuentes.md
│
├── .gitignore
├── LICENSE
└── README.md
Ajusta esta estructura si tu proyecto todavía tiene los archivos directamente en la raíz.

✅ Requisitos
Antes de ejecutar la aplicación necesitas:

Windows 10 o Windows 11.

Python 3.10 o superior.

pip.

FFmpeg agregado al PATH.

Navegador moderno.

Conexión a Internet.

Comprueba Python:

python --version
Comprueba pip:

python -m pip --version
Comprueba FFmpeg:

ffmpeg -version
🚀 Instalación rápida
1. Clonar el repositorio
git clone https://github.com/TU-USUARIO/media-extractor-dktservice.git
cd media-extractor-dktservice
2. Entrar a la aplicación
cd app
3. Crear el entorno virtual
python -m venv .venv
4. Activarlo
En PowerShell:

.venv\Scripts\Activate.ps1
En CMD:

.venv\Scripts\activate.bat
5. Instalar dependencias
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
6. Ejecutar
python app.py
Abre en el navegador:

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
