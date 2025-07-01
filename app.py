from flask import Flask, render_template, request
from ia import responder_con_ia

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    respuesta_ia = ""
    modelo_usado = ""
    fragmentos = []
    pregunta = ""
    mostrar_fragmentos = False

    if request.method == "POST":
        pregunta = request.form["consulta"]
        mostrar_fragmentos = "ver_fragmento" in request.form
        respuesta_ia, modelo_usado, fragmentos = responder_con_ia(pregunta)

    return render_template(
        "index.html",
        respuesta=respuesta_ia,
        pregunta=pregunta,
        modelo=modelo_usado,
        fragmentos=fragmentos,
        mostrar_fragmentos=mostrar_fragmentos
    )
