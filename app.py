from flask import Flask
from flask import render_template


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

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")


if __name__ == "__main__":
    app.run(debug=True)
