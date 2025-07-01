import google.generativeai as genai

API_KEY = "AIzaSyCh9dXMJXAqDKA2qzjnYKomZ8N8hD9B2dA"
genai.configure(api_key=API_KEY)

modelo = genai.GenerativeModel("models/gemini-1.5-pro-latest")
respuesta = modelo.generate_content("¿Qué es una norma eléctrica y para qué sirve?")
print(respuesta.text.strip())
