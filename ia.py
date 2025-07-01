import os
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ No se encontró la variable de entorno GEMINI_API_KEY.")
genai.configure(api_key=api_key)

MODELO_PREFERIDO = "models/gemini-1.5-pro-latest"
MODELO_ALTERNATIVO = "models/gemini-1.5-flash-latest"

with open("fragmentos.txt", "r", encoding="utf-8") as f:
    contenido_completo = f.read()

MAX_TOKENS = 3000
contenido_truncado = contenido_completo[:MAX_TOKENS * 4]

def generar_respuesta_con_modelo(modelo_id, prompt):
    modelo = genai.GenerativeModel(modelo_id)
    respuesta = modelo.generate_content(prompt)
    return respuesta.text.strip()

def responder_con_ia(pregunta):
    prompt = f"""
Eres un asistente técnico experto en normas eléctricas. A continuación se presenta el contenido completo de las normas y una consulta.
Responde únicamente usando el contenido proporcionado. Si la respuesta no está explícita, di que no se encontró.

CONTENIDO:
{contenido_truncado}

PREGUNTA: {pregunta}

RESPUESTA:
"""
    try:
        respuesta = generar_respuesta_con_modelo(MODELO_PREFERIDO, prompt)
        return respuesta, MODELO_PREFERIDO, [contenido_truncado]
    except ResourceExhausted:
        respuesta = generar_respuesta_con_modelo(MODELO_ALTERNATIVO, prompt)
        return respuesta, MODELO_ALTERNATIVO, [contenido_truncado]
    except Exception as e:
        return f"❌ Error: {e}", "Error", [contenido_truncado]

