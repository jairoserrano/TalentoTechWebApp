from flask import Flask
from flask import render_template, request, redirect, url_for
import json, os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database/database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Nombre,Apellidos,Correo,Telefono,Ciudad
class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)

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

    # Guardar en archivo json.
    with open(f"database/{telefono}.json", "w") as file:
        file.write(json.dumps(request.form.to_dict()))

    # Guardar en base de datos.
    contacto = Contacto(nombre=nombre, apellidos=apellidos, email=email, telefono=telefono, ciudad=ciudad)
    db.session.add(contacto)
    db.session.commit()

    # Redireccionar a la página de contacto.
    return redirect(url_for("contacto", mensaje="Contacto guardado."))


@app.route("/setup")
def setup():
    with app.app_context():
        db.create_all()
    return "Base de datos creada correctamente."


@app.route("/database/contactos")
def database_contactos():
    contactos = Contacto.query.all()
    return render_template("admin/contactos.html", contactos=contactos)


@app.route("/database/contactos/editar/<int:id>", methods=["GET","POST"])
def editar_contacto(id):
    if request.method == "POST":
        contacto = Contacto.query.get(id)
        contacto.nombre = request.form.get("nombre")
        contacto.apellidos = request.form.get("apellidos")
        contacto.email = request.form.get("email")
        contacto.telefono = request.form.get("telefono")
        contacto.ciudad = request.form.get("ciudad")
        db.session.commit()
        return redirect(url_for("database_contactos"))
    else:
        contacto = Contacto.query.get(id)
        return render_template("admin/editar_contacto.html", contacto=contacto)


"""
Ruta para mostrar los contactos guardados.
"""
@app.route("/admin/contactos")
def admin_contactos():
    contactos = []
    # lectura del archivo, teniendo en cuenta la codificación utf-8.
    with open("database/contactos.txt", "r", encoding="utf-8") as file:
        for linea in file:
            # separar los datos por comas.
            datos = linea.strip().split(",")
            # Crear un diccionario con los datos.
            contacto = {
                "nombre": datos[0],
                "apellidos": datos[1],
                "email": datos[2],
                "telefono": datos[3],
                "ciudad": datos[4]
            }
            # Agregar el contacto a la lista de contactos.
            contactos.append(contacto)

    return render_template("admin/contactos.html", contactos=contactos)

if __name__ == "__main__":
    app.run(debug=True)
