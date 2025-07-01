import os
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from dotenv import load_dotenv

# Cargar variables desde .env (útil en desarrollo local)
load_dotenv()

# Configurar la API Key desde variable de entorno
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ No se encontró la variable de entorno GEMINI_API_KEY.")
genai.configure(api_key=api_key)

# Modelos disponibles
MODELO_PREFERIDO = "models/gemini-1.5-pro-latest"
MODELO_ALTERNATIVO = "models/gemini-1.5-flash-latest"

# Cargar contenido normativo desde archivo
try:
    with open("fragmentos.txt", "r", encoding="utf-8") as f:
        todos_los_fragmentos = f.read()
except Exception as e:
    raise RuntimeError(f"❌ Error al cargar fragmentos.txt: {e}")


# Función para generar respuesta con un modelo específico
def generar_respuesta_con_modelo(modelo_id, prompt):
    modelo = genai.GenerativeModel(modelo_id)
    respuesta = modelo.generate_content(prompt)
    return respuesta.text.strip()

# Función principal que responde usando IA
def responder_con_ia(pregunta):
    try:
        prompt = f"""..."""  # tu prompt aquí
        respuesta = generar_respuesta_con_modelo(MODELO_PREFERIDO, prompt)
        return respuesta, MODELO_PREFERIDO, []
    except Exception as e:
        print(f"❌ Error interno: {e}")
        return f"❌ Error: {e}", "Error", []

Eres un asistente técnico experto en normas eléctricas. A continuación hay contenido normativo y una consulta.
Responde solamente con base en el contenido proporcionado, de forma clara y profesional.

CONTENIDO:
{todos_los_fragmentos}

PREGUNTA: {pregunta}

RESPUESTA:
"""
    try:
        respuesta = generar_respuesta_con_modelo(MODELO_PREFERIDO, prompt)
        return respuesta, MODELO_PREFERIDO, []
    except ResourceExhausted:
        respuesta = generar_respuesta_con_modelo(MODELO_ALTERNATIVO, prompt)
        return respuesta, MODELO_ALTERNATIVO, []
    except Exception as e:
        return f"❌ Error: {e}", "Error", []
