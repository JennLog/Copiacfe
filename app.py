from flask import Flask, render_template, request
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

genai.configure(api_key=os.getenv("API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    respuesta_ia = ""
    pregunta = ""
    if request.method == "POST":
        pregunta = request.form["consulta"]
        respuesta_ia = responder_con_ia(pregunta)
    return render_template("index.html", respuesta=respuesta_ia, pregunta=pregunta)

def responder_con_ia(pregunta):
    model = genai.GenerativeModel("gemini-pro")
    respuesta = model.generate_content(pregunta)
    return respuesta.text

if __name__ == "__main__":
    app.run(debug=True)
