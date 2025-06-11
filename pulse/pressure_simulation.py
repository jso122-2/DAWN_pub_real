import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image

PRESSURE_LOG_PATH = "juliet_flowers/cluster_report/nutrient_pressure.json"
COORDS_PATH = "juliet_flowers/cluster_report/seed_coords.json"
SNAPSHOT_DIR = "visuals/pressure_snapshots"
GIF_PATH = "visuals/pressure_animation.gif"
ANNOTATION_SOURCE = "juliet_flowers/active_events.json"  # Optional

def load_seed_coordinates():
    with open(COORDS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_hotspots(threshold=2.0):
    if not os.path.exists(ANNOTATION_SOURCE):
        return {}
    with open(ANNOTATION_SOURCE, "r") as f:
        return json.load(f)  # {"whale-001": "🧠", ...}

def save_pressure_snapshot(tick):
    if tick % 10 != 0:
        return

    if not os.path.exists(PRESSURE_LOG_PATH) or not os.path.exists(COORDS_PATH):
        print("[PressureSim] ❌ Missing pressure or coordinate files.")
        return

    with open(PRESSURE_LOG_PATH, "r") as f:
        pressure_data = json.load(f)

    coords = load_seed_coordinates()
    events = get_hotspots()

    x_vals, y_vals, intensities, labels = [], [], [], []

    for seed, types in pressure_data.items():
        total_pressure = sum(types.values())
        if seed in coords:
            x, y = coords[seed]
            x_vals.append(x)
            y_vals.append(y)
            intensities.append(total_pressure)
            labels.append(events.get(seed, ""))

    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(x_vals, y_vals, c=intensities, cmap="YlOrRd", s=80, edgecolors="k")
    plt.colorbar(scatter, ax=ax, label="Nutrient Pressure")
    plt.title(f"🧭 Semantic Pressure – Tick {tick}")
    plt.xlabel("Semantic X")
    plt.ylabel("Semantic Y")

    for x, y, label in zip(x_vals, y_vals, labels):
        if label:
            ax.text(x + 0.4, y + 0.2, label, fontsize=10)

    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    out_path = os.path.join(SNAPSHOT_DIR, f"pressure_tick_{tick:04d}.png")
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"[PressureSim] 📸 Snapshot saved → {out_path}")

def generate_gif():
    print("[PressureSim] 🎞️ Generating GIF...")
    images = []
    for fname in sorted(os.listdir(SNAPSHOT_DIR)):
        if fname.endswith(".png"):
            path = os.path.join(SNAPSHOT_DIR, fname)
            images.append(Image.open(path))

    if not images:
        print("[PressureSim] ❌ No images to animate.")
        return

    images[0].save(GIF_PATH,
                   save_all=True,
                   append_images=images[1:],
                   duration=400,
                   loop=0)
    print(f"[PressureSim] ✅ GIF saved → {GIF_PATH}")
