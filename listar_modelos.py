import google.generativeai as genai


API_KEY = "AIzaSyCh9dXMJXAqDKA2qzjnYKomZ8N8hD9B2dA"

genai.configure(api_key=API_KEY)

# Listar modelos disponibles
modelos = genai.list_models()
for modelo in modelos:
    print(modelo.name)
