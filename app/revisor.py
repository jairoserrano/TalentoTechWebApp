import requests
import json

url = "http://127.0.0.1:5000/api/galletas?page=1"

response = requests.get(url)
if response.status_code == 200:
    galletas = response.json()
    for galleta in galletas:
        print(f"ID: {galleta['id']}, Nombre: {galleta['nombre']}, Precio: {galleta['precio']}, Descripcion: {galleta['descripcion']}")
else:
    print(f"Error: {response.status_code}")