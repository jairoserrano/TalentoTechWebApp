from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    borrado = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "email": self.email,
            "telefono": self.telefono,
            "ciudad": self.ciudad
        }

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    def get_password(self, password):
        return bcrypt.generate_password_hash(password, 10)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password, 10)

    def validar_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
class Galleta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    borrado = db.Column(db.Boolean, default=False)

    def get_nombre_archivo(self):
        return f"{self.id}.webp"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "descripcion": self.descripcion
        }