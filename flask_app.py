
import os
import json
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route("/")
def index():
    fractals = sorted(os.listdir("juliet_flowers/fractal_signatures"))[-5:]
    commentary_files = sorted(os.listdir("owl/commentary"))[-5:]

    return render_template("index.html", fractals=fractals, commentary_files=commentary_files)

@app.route("/fractals/<filename>")
def get_fractal(filename):
    return send_from_directory("juliet_flowers/fractal_signatures", filename)

@app.route("/commentary/<filename>")
def get_commentary(filename):
    with open(os.path.join("owl/commentary", filename), "r", encoding="utf-8") as f:
        content = f.read()
    return f"<pre>{content}</pre>"

if __name__ == "__main__":
    app.run(debug=True)
