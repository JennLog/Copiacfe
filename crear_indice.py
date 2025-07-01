from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Cargar modelo local
modelo = SentenceTransformer("all-MiniLM-L6-v2")

# Leer fragmentos
with open("texto_extraido.txt", "r", encoding="utf-8") as f:
    texto = f.read()

fragmentos = [s.strip() for s in texto.split("=== Página") if len(s.strip()) > 30]

# Generar embeddings
print("Generando embeddings...")
embeddings = modelo.encode(fragmentos, convert_to_numpy=True)

# Crear índice FAISS
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

# Guardar índice y fragmentos
faiss.write_index(index, "indice_faiss.index")
with open("fragmentos.txt", "w", encoding="utf-8") as f:
    for frag in fragmentos:
        f.write(frag + "\n===\n")

print("✅ Índice creado con éxito.")
