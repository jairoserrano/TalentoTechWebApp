from flask import Flask
from flask import render_template, request, redirect, url_for


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/galletas")
def galletas():
    return render_template("galletas.html")

@app.route("/galletas/<string:galleta>")
def galleta(galleta):
    return render_template("galleta.html", tipo=galleta)

@app.route("/contacto", methods=["GET"])
def contacto():
    mensaje = request.args.get("mensaje")
    return render_template("contacto.html", mensaje=mensaje)

"""
Recepción de contactos para venta de productos.
"""
@app.route("/contacto", methods=["POST"])
def guardar_contacto():
    nombre = request.form.get("nombre")
    apellidos = request.form.get("apellidos")
    email = request.form.get("email")
    telefono = request.form.get("telefono")
    ciudad = request.form.get("ciudad")
    # Guardar en archivo de texto plano con formato csv, separado por comas.
    with open("database/contactos.txt", "a") as file:
        file.write(f"{nombre},{apellidos},{email},{telefono},{ciudad}\n")

    # Redireccionar a la página de contacto.
    return redirect(url_for("contacto", mensaje="Contacto guardado."))

if __name__ == "__main__":
    app.run(debug=True)
