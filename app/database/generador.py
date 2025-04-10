import csv
import random

nombres = ["Sofía", "Pedro", "María", "Luis", "Ana", "Carlos", "Laura", "Andrés", "Camila", "Daniela"]
apellidos = ["Ruiz", "Rodríguez", "Torres", "Fernández", "Gómez", "Martínez", "López", "Pérez", "Sánchez", "Ramírez"]
ciudades = ["Medellín", "Cúcuta", "Cartagena", "Barranquilla", "Pereira", "Bogotá", "Cali", "Bucaramanga", "Manizales", "Santa Marta"]
dominios = ["gmail.com", "yahoo.com", "hotmail.com", "utb.edu.co"]

def generar_email(nombre, apellido):
    return f"{nombre.lower()}.{apellido.lower()}@{random.choice(dominios)}"

def generar_telefono():
    return str(random.randint(3000000000, 3199999999))

with open("contactos.txt", mode="a", newline="", encoding="utf-8") as archivo:
    writer = csv.writer(archivo)
    for _ in range(10000):
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        email = generar_email(nombre, apellido)
        telefono = generar_telefono()
        ciudad = random.choice(ciudades)
        writer.writerow([nombre, apellido, email, telefono, ciudad])
