from flask import Flask, render_template, request
from ia import responder_con_ia

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    respuesta_ia = ""
    pregunta = ""
    modelo = ""
    fragmentos = []
    
    if request.method == "POST":
        pregunta = request.form.get("consulta", "")
        respuesta_ia, modelo, fragmentos = responder_con_ia(pregunta)
        
    return render_template("index.html", respuesta=respuesta_ia, pregunta=pregunta, modelo=modelo, fragmentos=fragmentos)

if __name__ == "__main__":
    app.run(debug=False)
