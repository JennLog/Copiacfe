import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# 🔐 Clave de API directamente en el código (solo para uso personal)
import os
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
  

# Modelos disponibles
MODELO_PREFERIDO = "models/gemini-1.5-pro-latest"
MODELO_ALTERNATIVO = "models/gemini-1.5-flash-latest"

# Cargar modelo de embeddings
modelo_embeddings = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("indice_faiss.index")

# Cargar fragmentos
with open("fragmentos.txt", "r", encoding="utf-8") as f:
    fragmentos = f.read().split("\n===\n")

# Buscar fragmentos similares
def buscar_fragmentos_similares(pregunta, k=3):
    emb = modelo_embeddings.encode([pregunta])[0].reshape(1, -1)
    distancias, indices = index.search(emb, k)
    return [fragmentos[i] for i in indices[0]]

# Generar respuesta con un modelo específico
def generar_respuesta_con_modelo(modelo_id, prompt):
    modelo = genai.GenerativeModel(modelo_id)
    respuesta = modelo.generate_content(prompt)
    return respuesta.text.strip()

# Función principal para responder con IA
def responder_con_ia(pregunta):
    fragmentos_usados = buscar_fragmentos_similares(pregunta)
    contexto = "\n\n".join(fragmentos_usados)
    prompt = f"""
Eres un asistente técnico experto en normas eléctricas. A continuación hay un fragmento de norma y una consulta.
Usa solo el contenido proporcionado para responder de forma clara, precisa y profesional.

CONTEXTO:
{contexto}

PREGUNTA: {pregunta}

RESPUESTA:
"""
    try:
        respuesta = generar_respuesta_con_modelo(MODELO_PREFERIDO, prompt)
        return respuesta, MODELO_PREFERIDO, fragmentos_usados
    except ResourceExhausted:
        print("⚠️ Cuota del modelo pro agotada. Usando modelo flash.")
        respuesta = generar_respuesta_con_modelo(MODELO_ALTERNATIVO, prompt)
        return respuesta, MODELO_ALTERNATIVO, fragmentos_usados
    except Exception as e:
        return f"❌ Error al generar respuesta: {e}", "Error", []

