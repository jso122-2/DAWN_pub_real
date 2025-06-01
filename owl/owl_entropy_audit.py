import os
import numpy as np
from PIL import Image
import json
from scipy.stats import entropy

LINEAGE_PATH = "juliet_flowers/cluster_report/rebloom_lineage.json"
FRACTAL_DIR = "juliet_flowers/fractal_signatures/"
OUTPUT_JSON = "juliet_flowers/cluster_report/owl_entropy_report.json"

def image_entropy(image_path):
    try:
        with Image.open(image_path) as img:
            grayscale = img.convert("L")
            hist = grayscale.histogram()
            hist = np.array(hist) / sum(hist)
            return entropy(hist)
    except Exception as e:
        print(f"[Owl] 🧪 Could not read {image_path}: {e}")
        return None

def analyze_entropy():
    with open(LINEAGE_PATH, "r", encoding="utf-8") as f:
        lineage = json.load(f)

    audit = {}

    for bloom_id, meta in lineage.items():
        chain = meta["rebloom_chain"]
        scores = []
        for bid in chain:
            path = os.path.join(FRACTAL_DIR, f"{bid}.png")
            score = image_entropy(path)
            if score is not None:
                scores.append(score)

        if scores:
            delta = max(scores) - min(scores)
            audit[bloom_id] = {
                "avg_entropy": round(np.mean(scores), 4),
                "delta_entropy": round(delta, 4),
                "status": "stable" if delta < 0.2 else "chaotic"
            }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2)
    print(f"[Owl] 🧠 Entropy audit saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    analyze_entropy()
