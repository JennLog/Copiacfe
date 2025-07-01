from flask import Flask, render_template, request
from ia import responder_con_ia

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    respuesta_ia = ""
    modelo_usado = ""
    fragmentos = []
    pregunta = ""
    if request.method == "POST":
        pregunta = request.form["consulta"]
        respuesta_ia, modelo_usado, fragmentos = responder_con_ia(pregunta)
    return render_template("index.html", respuesta=respuesta_ia, pregunta=pregunta, modelo=modelo_usado, fragmentos=fragmentos)
if __name__ == "__main__":
    app.run(debug=True)
