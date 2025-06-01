
import os
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image

BLOOM_DIR = "juliet_flowers/bloom_metadata"
FRACTAL_DIR = "juliet_flowers/fractal_signatures"
OUTPUT = "juliet_flowers/cluster_report/semantic_timeline.gif"

def render_semantic_timeline():
    files = sorted(f for f in os.listdir(BLOOM_DIR) if f.endswith(".json"))
    frames = []

    for f in files:
        with open(os.path.join(BLOOM_DIR, f), "r") as meta_file:
            bloom = json.load(meta_file)

        sid = bloom["seed_id"]
        fractals = [img for img in os.listdir(FRACTAL_DIR) if sid in img]
        if not fractals:
            continue

        img_path = os.path.join(FRACTAL_DIR, sorted(fractals)[-1])
        img = Image.open(img_path).convert("RGB")

        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, 260, 20], fill=(0, 0, 0))
        draw.text((5, 5), f"{sid} | Mood: {bloom['mood']} | Entropy: {bloom['entropy_score']:.2f}", fill=(255, 255, 255))

        frames.append(img)

    if frames:
        frames[0].save(
            OUTPUT,
            save_all=True,
            append_images=frames[1:],
            duration=800,
            loop=0
        )
        print(f"[Timeline] 🎞️ Semantic timeline saved → {OUTPUT}")
    else:
        print("[Timeline] ❌ No frames generated.")
