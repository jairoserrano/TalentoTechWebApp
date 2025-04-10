from flask import Flask
from flask import session, jsonify, send_file
from config import Config
from models import db, Contacto, Usuario, Galleta
from flask import render_template, request, redirect, url_for
from io import BytesIO
import json
import pandas as pd

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
        # return usuario.get_password("admin")
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


@app.route("/galletas/xls")
def xls_galletas():

    galletas = Galleta.query.all()
    datos = [galleta.to_dict() for galleta in galletas]
    df = pd.DataFrame(datos)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="galletas.xlsx")


@app.route("/galletas")
def galletas():
    galletas = Galleta.query.all()
    return render_template("galletas.html", galletas=galletas)


@app.route("/galletas_con_api")
def galletas_con_api():
    return render_template("galletas_con_api.html")


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


@app.route("/contactos/limpiar")
def pandas_contactos():
    datos = pd.read_csv('database/contactos.txt', sep=",", dtype={
        "Nombre": "string",
        "Apellido": "string",
        "Correo": "string",
        "Telefono": "string",
        "Ciudad": "string"
    })
    datos = datos.drop_duplicates(subset="Correo", keep="first")
    datos = datos.drop_duplicates(subset="Telefono", keep="first")
    datos.to_csv('database/contactos_limpio.txt', sep=",", index=False)
    return "limpieza del dataset realizada correctamente"


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


'''
Rutas para APIs REST.
'''
@app.route("/api/galletas")
def api_galletas():
    '''
    Endpoint para obtener todas las galletas.
    '''
    galletas = Galleta.query.paginate(per_page=10, page=request.args.get("page", 1, type=int))
    return jsonify([galleta.to_dict() for galleta in galletas])


@app.route("/api/galletas/<int:id>")
def api_galleta(id):
    ''''
    Endpoint para obtener una galleta por su id.'
    '''
    galleta = Galleta.query.get(id)
    if galleta:
        return jsonify(galleta.to_dict())
    else:
        return jsonify({"error": "Galleta no encontrada"}), 404

@app.route("/api/galletas/<int:id>", methods=["DELETE"])
def api_delete_galleta(id):
    '''
    Endpoint para eliminar una galleta por su id.
    '''
    galleta = Galleta.query.get(id)
    if galleta:
        db.session.delete(galleta)
        db.session.commit()
        return jsonify({"message": "Galleta eliminada"}), 200
    else:
        return jsonify({"error": "Galleta no encontrada"}), 404

@app.route("/api/galletas", methods=["POST"])
def api_create_galleta():
    '''
    Endpoint para crear una galleta.
    '''
    data = request.get_json()
    galleta = Galleta(
        nombre=data["nombre"],
        precio=data["precio"],
        descripcion=data["descripcion"],
    )
    db.session.add(galleta)
    db.session.commit()
    return jsonify(galleta.to_dict()), 201

@app.route("/api/galletas/<int:id>", methods=["PUT"])
def api_update_galleta(id):
    '''
    Endpoint para actualizar una galleta por su id.
    '''
    data = request.get_json()
    galleta = Galleta.query.get(id)
    if galleta:
        galleta.nombre = data["nombre"]
        galleta.precio = data["precio"]
        galleta.descripcion = data["descripcion"]
        db.session.commit()
        return jsonify(galleta.to_dict()), 200
    else:
        return jsonify({"error": "Galleta no encontrada"}), 404


@app.route("/api/contactos")
def api_contactos():
    contactos = Contacto.query.all()
    return jsonify([contacto.to_dict() for contacto in contactos])


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
