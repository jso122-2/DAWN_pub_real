
import os
import json
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route("/")
def index():
    try:
        fractals = sorted(os.listdir("juliet_flowers/fractal_signatures"))[-10:]
        commentary = sorted(os.listdir("owl/commentary"))[-10:]
    except:
        fractals, commentary = [], []

    return render_template(
        "dashboard.html",
        fractals=fractals,
        commentary=commentary,
        moodmap="mood_heatmap.png",
        entropyarc="entropy_arc.gif",
        fieldmap="recursive_fieldmap.png",
        trailmap="nutrient_trails.gif",
        pressuremap="cognition_pressure_map.png",
        clusters="memory_clusters.png",
        timeline="semantic_timeline.gif"
    )

@app.route("/fractals/<filename>")
def fractal(filename):
    return send_from_directory("juliet_flowers/fractal_signatures", filename)

@app.route("/commentary/<filename>")
def owl(filename):
    return send_from_directory("owl/commentary", filename)

@app.route("/cluster_report/<filename>")
def report_assets(filename):
    return send_from_directory("juliet_flowers/cluster_report", filename)

if __name__ == "__main__":
    app.run(debug=True)
