from flask import Flask, render_template, url_for, request
from flask_material import Material

app = Flask(__name__)
Material(app)

@app.route('/')
def index():
    return render_template("index.html")
