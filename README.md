# 🐾 Campet - Análisis de Lenguaje Corporal Canino con IA

**Campet** es una aplicación web responsive con experiencia mobile-first diseñada para interpretar las señales visibles del lenguaje corporal en perros y cachorros utilizando inteligencia artificial con visión computacional (Google Gemini 2.5 Flash / Modo DEMO).

---

## 🌟 Características Principales

1. **Pantalla de Inicio Moderna:**
   - Presentación de la marca Campet con el logo oficial.
   - Acceso rápido a análisis y guía explicativa.
   - Demostración visual de características futuras (*Análisis de Vídeo — Próximamente*).

2. **Carga y Captura de Fotografía:**
   - Soporte para selección desde dispositivo y captura directa con la cámara del celular.
   - Compatibilidad con formatos **JPG, JPEG, PNG y WEBP**.
   - Vista previa con opciones para cambiar o eliminar la fotografía antes de analizar.
   - Botón de imágenes de muestra para pruebas rápidas instantáneas.

3. **Análisis con Visión Artificial (IA):**
   - Evalúa estrictamente características visibles: **Orejas, Cola, Postura Corporal, Cabeza, Mirada y Expresión**.
   - Si una característica no es apreciable en la foto, se indica formalmente como **"No visible"**.
   - Genera respuestas orientativas utilizando expresiones cautelosas como *"podría indicar"*, *"posiblemente"* o *"señales compatibles con"*.
   - **Modo DEMO Automático:** Funciona perfectamente incluso sin clave API de IA, ofreciendo simulaciones completas para demostración.

4. **Resultados e Interpretación:**
   - Fotografía analizada.
   - Posible estado del perro (ej: Alerta, Relajación, Curiosidad, Juego).
   - Nivel de confianza (*Bajo, Moderado, Alto*).
   - Desglose detallado de señales observadas y explicación etológica prudente.
   - Nota legal/descargo aclarando que no constituye diagnóstico veterinario.

5. **Historial ("Mis análisis"):**
   - Almacenamiento local mediante `localStorage` para consultar los análisis realizados durante la sesión.
   - Detalle emergente de cada consulta e historia acumulada.

---

## 📁 Estructura del Proyecto

```text
Campet/
├── app.py                  # Servidor principal Flask y lógica de IA / DEMO
├── requirements.txt        # Dependencias de Python (Flask, Gunicorn, google-genai, Pillow)
├── Procfile                # Configuración de inicio para despliegue en Render/Heroku
├── .env.example            # Plantilla de variables de entorno
├── .gitignore              # Archivos excluidos del control de versiones
├── README.md               # Documentación y guía del proyecto
├── static/
│   ├── css/
│   │   └── style.css       # Sistema de diseño responsive Mobile-First
│   ├── js/
│   │   └── main.js         # Lógica auxiliar de interfaz y almacenamiento
│   ├── images/
│   │   ├── logo.png        # Logo oficial de la aplicación Campet
│   │   ├── sample1.jpg     # Foto de muestra (Perro Alerta)
│   │   └── sample2.jpg     # Foto de muestra (Perro Relajado)
│   └── uploads/            # Carpeta para almacenamiento de imágenes subidas
└── templates/
    ├── base.html           # Shell principal con navegación mobile
    ├── index.html          # Pantalla principal (Inicio)
    ├── analyze.html        # Pantalla de carga, vista previa y análisis
    ├── result.html         # Plantilla secundaria de resultados
    ├── history.html        # Pantalla de historial "Mis Análisis"
    └── how_it_works.html   # Explicación paso a paso de funcionamiento
```

---

## 🚀 Instalación y Ejecución Local

### 1. Requisitos Previos
- Python 3.9 o superior instalado en el equipo.

### 2. Clonar / Descargar el Proyecto
```bash
cd Campet
```

### 3. Crear Entorno Virtual (Opcional pero recomendado)
```bash
# En Windows:
python -m venv venv
venv\Scripts\activate

# En Mac/Linux:
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar Variables de Entorno (Opcional para modo IA Real)
Copia el archivo `.env.example` a `.env`:
```bash
cp .env.example .env
```
Abre `.env` e ingresa tu clave API de Google Gemini en `GEMINI_API_KEY`:
```env
GEMINI_API_KEY=tu_clave_api_gemini_aqui
```
*Si dejas la clave en blanco o no creas el archivo `.env`, la aplicación funcionará automáticamente en **Modo DEMO**.*

### 6. Ejecutar la Aplicación
```bash
python app.py
```
Abre tu navegador e ingresa a: **`http://localhost:5000`**

---

## ☁️ Despliegue en Render / GitHub

1. **Subir a GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Campet app"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/Campet.git
   git push -u origin main
   ```

2. **Desplegar en Render:**
   - Crea un nuevo **Web Service** en [Render.com](https://render.com/).
   - Conecta tu repositorio de GitHub.
   - Configura el comando de inicio (Start Command):
     ```bash
     gunicorn app:app
     ```
   - En la sección **Environment Variables**, añade opcionalmente `GEMINI_API_KEY`.
   - Haz clic en **Deploy**.

---

## 🎓 Guía para Presentación Escolar

Al presentar este proyecto ante tus profesores y compañeros, puedes destacar:

1. **Propósito ético:** El sistema nunca emite diagnósticos médicos ni verdades absolutas, promoviendo la tenencia responsable de mascotas y sugiriendo la opinión de veterinarios en caso de duda.
2. **Arquitectura limpia:** El backend en Python + Flask gestiona la API y las peticiones, mientras que el frontend en HTML5, CSS3 y JavaScript ofrece una experiencia tipo app nativa móvil.
3. **Visión por IA y Resiliencia (Modo DEMO):** Puedes mostrar el análisis real con Gemini API o demostrar cómo la app entra en **Modo DEMO** de resiliencia si no hay internet o credenciales.
