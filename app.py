import os
import uuid
import json
import base64
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'campet_secret_key_escuela_2026')

# Configuración de carpetas y formatos permitidos
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # Máximo 10 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Verifica si la extensión del archivo es válida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def encode_image_to_base64(image_path):
    """Convierte una imagen a Base64 para enviar a la API de Inteligencia Artificial."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_with_gemini(image_path):
    """
    Analiza la imagen utilizando la API de Google Gemini (gemini-2.5-flash).
    Devuelve un diccionario estructurado con las observaciones corporales.
    """
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key or api_key == 'tu_api_key_de_gemini_aqui':
        return None, "NO_API_KEY"

    try:
        from google import genai
        from google.genai import types
        from PIL import Image

        client = genai.Client(api_key=api_key)
        img = Image.open(image_path)

        prompt = """
        Eres un asistente especializado en etología canina y lenguaje corporal de perros.
        Analiza la fotografía adjunta siguiendo estrictamente estas reglas:

        REGLAS FUNDAMENTALES:
        1. Analiza ÚNICAMENTE las características corporales que sean verdaderamente VISIBLES en la foto.
        2. Si una parte del cuerpo (orejas, cola, postura, mirada, etc.) no es visible claramente o está fuera de encuadre, debes responder "No visible". NUNCA inventes o supongas rasgos no visibles.
        3. NUNCA afirmes con certeza absoluta el estado emocional ni realices diagnósticos médicos o veterinarios. Usa SIEMPRE lenguaje orientativo como: "podría indicar", "señales compatibles con", "posiblemente".
        4. Responde EXCLUSIVAMENTE en formato JSON válido con las siguientes llaves exactas:
        {
          "state": "Nombre corto del posible estado (ej: Alerta, Relajación, Curiosidad, Juego, Incomodidad, Miedo)",
          "confidence": "Bajo" | "Moderado" | "Alto",
          "signals": {
            "ears": "Descripción visible de las orejas (o 'No visible')",
            "tail": "Descripción visible de la cola (o 'No visible')",
            "posture": "Descripción visible de la postura corporal (o 'No visible')",
            "head": "Posición de la cabeza (o 'No visible')",
            "gaze": "Dirección o tipo de mirada (o 'No visible')",
            "expression": "Expresión facial u ocular (o 'No visible')"
          },
          "interpretation": "Explicación detallada orientativa de por qué las señales indican ese estado.",
          "vet_recommendation": false o true (true solo si se observan signos de dolor evidente, fatiga extrema o malestar que requiera veterinario)
        }
        """

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[img, prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )

        result_data = json.loads(response.text)
        result_data['is_demo'] = False
        return result_data, None

    except Exception as e:
        print(f"Error al comunicar con la API de Gemini: {e}")
        return None, str(e)

def get_demo_analysis(filename):
    """
    Modo DEMO simulado cuando no hay API Key configurada.
    Genera un análisis realista para demostraciones de clase o pruebas.
    """
    # Determinamos algunas variantes simuladas según el nombre del archivo o aleatorio inteligente
    if "sample1" in filename or "alert" in filename:
        return {
            "state": "Alerta y Atención",
            "confidence": "Alto",
            "signals": {
                "ears": "Orejas erguidas y orientadas hacia adelante.",
                "tail": "No visible",
                "posture": "Postura erguida, peso distribuido sobre las cuatro patas en posición de apoyo firme.",
                "head": "Cabeza elevada y alineada con la mirada.",
                "gaze": "Mirada fija y directa hacia un punto específico del entorno.",
                "expression": "Expresión facial concentrada sin signos de rigidez muscular facial extrema."
            },
            "interpretation": "Las señales visibles (orejas erguidas, cabeza alta y postura firme) son compatibles con un estado de alerta o interés activo hacia un estímulo del entorno.",
            "vet_recommendation": False,
            "is_demo": True
        }
    elif "sample2" in filename or "relaxed" in filename:
        return {
            "state": "Relajación",
            "confidence": "Alto",
            "signals": {
                "ears": "Orejas en posición relajada y natural sin tensión.",
                "tail": "Cola reposando suavemente en el suelo.",
                "posture": "Cuerpo recostado de forma relajada sobre la superficie.",
                "head": "Cabeza apoyada o ligeramente baja con musculatura suelta.",
                "gaze": "Mirada tranquila con parpadeo suave.",
                "expression": "Expresión facial descansada sin ceño ni tensión."
            },
            "interpretation": "Las señales corporales descritas (postura recostada, orejas flojas y boca suelta) podrían indicar un estado de tranquilidad, calma y confort ambiental.",
            "vet_recommendation": False,
            "is_demo": True
        }
    else:
        return {
            "state": "Curiosidad e Interés",
            "confidence": "Moderado",
            "signals": {
                "ears": "Orejas ligeramente ladeadas o dirigidas hacia una fuente de sonido.",
                "tail": "No visible",
                "posture": "Postura en ligera inclinación hacia adelante.",
                "head": "Cabeza levemente inclinada en ángulo de exploración.",
                "gaze": "Mirada atenta hacia la cámara o el objeto de interés.",
                "expression": "Expresión despierta e inquisitiva."
            },
            "interpretation": "Las observaciones corporales visibles sugieren un estado compatible con la curiosidad, exploración o expectativa frente a algo llamativo.",
            "vet_recommendation": False,
            "is_demo": True
        }

# --- RUTAS DE LA APLICACIÓN ---

@app.route('/')
def index():
    """Pantalla principal / Inicio"""
    return render_template('index.html')

@app.route('/analyze')
def analyze_page():
    """Pantalla para subir/tomar la fotografía"""
    return render_template('analyze.html')

@app.route('/how-it-works')
def how_it_works():
    """Pantalla explicativa ¿Cómo funciona?"""
    return render_template('how_it_works.html')

@app.route('/history')
def history():
    """Pantalla de historial 'Mis análisis'"""
    return render_template('history.html')

@app.route('/api/analyze', methods=['POST'])
def process_analysis():
    """Endpoint que recibe la fotografía y ejecuta el análisis por IA o DEMO"""
    image_url = None
    file_path = None
    filename_saved = None

    # Comprobar si se envió un archivo cargado o una foto de muestra
    if 'photo' in request.files and request.files['photo'].filename != '':
        file = request.files['photo']
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Formato de imagen no permitido. Usa JPG, JPEG, PNG o WEBP.'}), 400
        
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename_saved = f"dog_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}.{ext}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename_saved)
        file.save(file_path)
        image_url = url_for('static', filename=f'uploads/{filename_saved}')

    elif 'sample_name' in request.form:
        sample_name = request.form['sample_name']
        filename_saved = f"{sample_name}.jpg"
        file_path = os.path.join(app.root_path, 'static', 'images', filename_saved)
        image_url = url_for('static', filename=f'images/{filename_saved}')
    
    else:
        return jsonify({'success': False, 'error': 'No se recibió ninguna imagen válida.'}), 400

    # Intentar análisis con Gemini o usar Modo DEMO
    analysis_result, error_code = analyze_with_gemini(file_path)
    
    if analysis_result is None:
        # Fallback automático a Modo DEMO si la API Key no está configurada o falla
        analysis_result = get_demo_analysis(filename_saved)

    analysis_id = uuid.uuid4().hex[:10]
    timestamp = datetime.now().strftime('%d/%m/%Y - %H:%M')

    response_data = {
        'id': analysis_id,
        'image_url': image_url,
        'timestamp': timestamp,
        'state': analysis_result.get('state', 'Observación general'),
        'confidence': analysis_result.get('confidence', 'Moderado'),
        'signals': analysis_result.get('signals', {}),
        'interpretation': analysis_result.get('interpretation', 'Se observan señales compatibles con atención o indagación.'),
        'vet_recommendation': analysis_result.get('vet_recommendation', False),
        'is_demo': analysis_result.get('is_demo', True),
        'disclaimer': "Esta herramienta ofrece una interpretación orientativa basada únicamente en señales visibles de la fotografía. No constituye un diagnóstico veterinario ni permite determinar con certeza el estado emocional o de salud del perro."
    }

    return jsonify({'success': True, 'data': response_data})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
