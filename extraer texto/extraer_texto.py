import pdfplumber

# Cambia este nombre por el de tu archivo PDF
archivo_pdf = "norma_electrica.pdf"

# Variable para almacenar todo el texto extraído
texto_completo = ""

# Abrimos el PDF y extraemos el texto de cada página
with pdfplumber.open("DCCIAMBT Aereas1.pdf") as pdf:
    for i, pagina in enumerate(pdf.pages, start=1):
        texto = pagina.extract_text()
        if texto:
            texto_completo += f"\n\n=== Página {i} ===\n\n"
            texto_completo += texto
        else:
            texto_completo += f"\n\n=== Página {i}: (sin texto visible) ===\n\n"

# Guardamos todo en un archivo de texto
archivo_salida = "texto_extraidoaereas.txt"
with open(archivo_salida, "w", encoding="utf-8") as f:
    f.write(texto_completo)

print(f"✅ Listo. El texto fue extraído y guardado en '{archivo_salida}'")

