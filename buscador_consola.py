from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Leer el texto desde el archivo extraído
with open("texto_extraido.txt", "texto_extraidoaereas", "r", encoding="utf-8") as f:
    contenido = f.read()

# Divide el texto por secciones 
secciones = contenido.split("=== Página")

# Crea una lista indexada de secciones
paginas = [("Página" + s[:5], s) for s in secciones if len(s.strip()) > 30]

def buscar(query):
    mejores = process.extract(query, [texto for _, texto in paginas], limit=5)
    for score, resultado in mejores:
        print(f"\n🔎 Coincidencia con {score}% de similitud:\n")
        print(resultado[:500])  #muestra los primeros 500 caracteres 
        print("\n" + "="*50)

while True:
    pregunta = input("\nEscribe lo que deseas buscar (o 'salir' para cerrar): ").strip()
    if pregunta.lower() == "salir":
        break
    buscar(pregunta)
