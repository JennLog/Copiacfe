import os
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ No se encontró la variable de entorno GEMINI_API_KEY.")
genai.configure(api_key=api_key)

# Modelos
MODELO_PREFERIDO = "models/gemini-1.5-pro-latest"
MODELO_ALTERNATIVO = "models/gemini-1.5-flash-latest"

# Cargar fragmentos como lista
with open("fragmentos.txt", "r", encoding="utf-8") as f:
    todos_los_fragmentos = f.read().split("\n\n")  # separa por doble salto de línea


import difflib

def buscar_fragmentos_relevantes(pregunta, fragmentos, max_resultados=3):
    # Calcular similitud entre la pregunta y cada fragmento
    puntuaciones = [(frag, difflib.SequenceMatcher(None, pregunta.lower(), frag.lower()).ratio()) for frag in fragmentos]
    # Ordenar por similitud descendente
    puntuaciones.sort(key=lambda x: x[1], reverse=True)
    # Devolver los fragmentos más similares
    return [frag for frag, _ in puntuaciones[:max_resultados]]


# Generar respuesta con modelo
def generar_respuesta_con_modelo(modelo_id, prompt):
    modelo = genai.GenerativeModel(modelo_id)
    respuesta = modelo.generate_content(prompt)
    return respuesta.text.strip()

# Función principal
def responder_con_ia(pregunta):
    fragmentos_relevantes = buscar_fragmentos_relevantes(pregunta, todos_los_fragmentos)
    contenido_util = "\n\n".join(fragmentos_relevantes)

   prompt = f"""
Eres un asistente técnico experto en normas eléctricas. A continuación hay contenido normativo y una consulta.
Responde solamente con base en el contenido proporcionado, de forma clara y profesional.

CONTENIDO:
{contenido_util}

PREGUNTA: {pregunta}

RESPUESTA:
"""
    try:
        respuesta = generar_respuesta_con_modelo(MODELO_PREFERIDO, prompt)
        return respuesta, MODELO_PREFERIDO, fragmentos_relevantes
    except ResourceExhausted:
        return (
            "⚠️ Has superado el límite gratuito de tokens por minuto. Intenta de nuevo en unos segundos o considera reducir el tamaño del contenido.",
            "Límite alcanzado",
            fragmentos_relevantes,
        )
    except Exception as e:
        return f"❌ Error: {e}", "Error", fragmentos_relevantes
