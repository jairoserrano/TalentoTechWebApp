from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/galletas')
def galletas():
    return "Aquí mis galletas."


@app.route('/contacto')
def contacto():
    return "Aquí mi contacto."


if __name__ == '__main__':
    app.run(debug=True)