# Media Extractor DKTService — Rama web

Esta es la rama dedicada a la presentación pública del proyecto. Aquí encontrarás una landing page estática, moderna y adaptable, diseñada para mostrar qué es Media Extractor DKTService y cómo acceder a su aplicación local.

## 🌐 Página web

- 🌍 Ver la landing page pública: https://media-extractor-dktservice.vercel.app
- 📦 Descargar la rama principal: https://github.com/tore234/media-extractor-dktservice/archive/refs/heads/main.zip
- 🧠 Repositorio: https://github.com/tore234/media-extractor-dktservice


## ¿Qué encontrarás aquí?

- Una interfaz profesional y responsive.
- Información clara sobre el proyecto y sus funciones.
- Secciones para plataformas compatibles, requisitos e instalación.
- Enlaces directos al repositorio y al ZIP de la rama principal.
- Un diseño listo para desplegar en Vercel.

## Objetivo de esta rama

La rama `web` solo contiene la página pública del proyecto. No incluye la aplicación funcional ni procesos de descarga multimedia. La versión completa y operativa de la herramienta sigue en la rama `main`.

## Estructura del proyecto

```text
/
├── index.html
├── styles.css
├── script.js
├── vercel.json
├── README.md
└── assets/
    ├── logo.png
    └── banner.png
```

## Probar la página localmente

Puedes ver la landing page abriendo el archivo `index.html` directamente en tu navegador o sirviéndola con un servidor estático.

### Opción 1: abrir directamente

Haz doble clic en `index.html`.

### Opción 2: servidor local

```bash
python -m http.server 8000
```

Luego abre:

```text
http://127.0.0.1:8000
```

## Desplegar en Vercel

1. Conecta este repositorio a Vercel.
2. Selecciona la rama `web` como fuente de despliegue.
3. Vercel detectará el sitio estático automáticamente.
4. El archivo `vercel.json` ya está preparado para URLs limpias.

## Enlaces útiles

- Repositorio: https://github.com/tore234/media-extractor-dktservice
- Descarga ZIP de la rama main: https://github.com/tore234/media-extractor-dktservice/archive/refs/heads/main.zip

## Nota importante

Esta rama está pensada exclusivamente para mostrar el proyecto al público. La descarga multimedia real y la ejecución funcional de la aplicación deben realizarse desde la rama `main` en un entorno local.
