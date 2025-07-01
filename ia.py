import os
import google.generativeai as genai
import google.generativeai as genai
genai.configure(api_key="AIzaSyCh9dXMJXAqDKA2qzjnYKomZ8N8hD9B2dA")

from google.api_core.exceptions import ResourceExhausted
from dotenv import load_dotenv

load_dotenv()  # Cargar variables desde .env

# Configura la API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODELO_PREFERIDO = "models/gemini-1.5-pro-latest"
MODELO_ALTERNATIVO = "models/gemini-1.5-flash-latest"

# Cargar todos los fragmentos como texto (sin FAISS)
with open("fragmentos.txt", "r", encoding="utf-8") as f:
    todos_los_fragmentos = f.read()

# Función para generar respuesta
def generar_respuesta_con_modelo(modelo_id, prompt):
    modelo = genai.GenerativeModel(modelo_id)
    respuesta = modelo.generate_content(prompt)
    return respuesta.text.strip()

def responder_con_ia(pregunta):
    prompt = f"""
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
