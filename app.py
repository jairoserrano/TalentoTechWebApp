from flask import Flask
from flask import session
from config import Config
from models import db, Contacto, Usuario, Galleta
from flask import render_template, request, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = "sdhjaskdhlasd%#&%tchajksfhjkS"
app.config.from_object(Config)
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("user")
        password = request.form.get("password")
        usuario = Usuario.query.filter_by(user=user).first()
        #return usuario.get_password("admin")
        if usuario is not None and usuario.validar_password(password):
            session["user"] = user
            if usuario.admin:
                session["admin"] = True
                return redirect(url_for("database_contactos"))
            session["admin"] = False
            return redirect(url_for("index"))
        else:
            return "Usuario o contraseña incorrectos."
    else:
        return render_template("login/login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/galletas")
def galletas():
    galletas = Galleta.query.all()
    return render_template("galletas.html", galletas=galletas)

@app.route("/galletas/nueva", methods=["GET", "POST"])
def nueva_galleta():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")
        descripcion = request.form.get("descripcion")

        galleta = Galleta(
            nombre=nombre,
            precio=precio,
            descripcion=descripcion,
        )
        db.session.add(galleta)
        db.session.commit()
        
        request.files["imagen"].save(f"static/img/galletas/{galleta.id}.webp")
        
        return redirect(url_for("galletas"))
    
    return render_template("admin/nueva_galleta.html")

@app.route("/galletas/<int:id>")
def galleta(id):
    galleta = Galleta.query.get(id)
    return render_template("galleta.html", galleta=galleta)


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
    contacto = Contacto(
        nombre=nombre,
        apellidos=apellidos,
        email=email,
        telefono=telefono,
        ciudad=ciudad,
    )
    db.session.add(contacto)
    db.session.commit()

    # Redireccionar a la página de contacto.
    return redirect(url_for("contacto", mensaje="Contacto guardado."))


@app.route("/setup")
def setup():
    with app.app_context():
        db.create_all()
    return "Base de datos creada correctamente."


@app.route("/perfil", methods=["GET", "POST"])
def perfil():
    if request.method == "POST":
        usuario = Usuario().query.filter_by(user=session["user"]).first()
        usuario.set_password(request.form.get("password"))
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("perfil.html")


@app.route("/database/contactos")
def database_contactos():
    # contactos = Contacto.query.all()
    contactos = Contacto.query.filter_by(borrado=False).all()
    return render_template("admin/contactos.html", contactos=contactos)


@app.route("/database/contactos/papelera")
def database_contactos_papelera():
    # contactos = Contacto.query.all()
    contactos = Contacto.query.filter_by(borrado=True).all()
    return render_template("admin/contactos.html", contactos=contactos, papelera=True)


@app.route("/database/contactos/restaurar/<int:id>", methods=["GET"])
def restaurar_contacto(id):
    contacto = Contacto.query.get(id)
    contacto.borrado = False
    db.session.commit()
    return redirect(url_for("database_contactos"))


@app.route("/database/contactos/editar/<int:id>", methods=["GET", "POST"])
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


@app.route("/database/contactos/eliminar/<int:id>", methods=["GET"])
def eliminar_contacto(id):
    contacto = Contacto.query.get(id)
    contacto.borrado = True
    db.session.commit()
    # db.session.delete(contacto)
    # db.session.commit()
    return redirect(url_for("database_contactos"))


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
                "ciudad": datos[4],
            }
            # Agregar el contacto a la lista de contactos.
            contactos.append(contacto)

    return render_template("admin/contactos.html", contactos=contactos)


if __name__ == "__main__":
    app.run(debug=True)
