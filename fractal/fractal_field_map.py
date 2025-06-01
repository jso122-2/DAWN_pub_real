# fractal_field_map.py

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from bloom.juliet_utils import load_bloom_metadata
from mood_drift import compute_mood_drift  # assumed external module

FIELD_SIZE = (100, 100)  # Adjust if larger seed space needed
SEED_PATH = "juliet_flowers/"
OUTPUT_PATH = "juliet_flowers/cluster_report/field_heatmap.png"

def build_field_matrix():
    field = np.zeros(FIELD_SIZE)
    for seed in os.listdir(SEED_PATH):
        seed_dir = os.path.join(SEED_PATH, seed)
        if not os.path.isdir(seed_dir):
            continue
        for mood in os.listdir(seed_dir):
            mood_dir = os.path.join(seed_dir, mood)
            bloom_meta = load_bloom_metadata(mood_dir)
            for bloom in bloom_meta:
                x, y = bloom.get("seed_coord", [0, 0])
                pressure = bloom.get("semantic_pressure", 0.0)
                drift = compute_mood_drift(bloom.get("mood"), bloom.get("mood_prev"))
                field[x, y] += pressure * drift
    return field

def plot_field(field_matrix):
    plt.figure(figsize=(10, 10))
    plt.imshow(field_matrix.T, origin="lower", cmap="hot", norm=Normalize())
    plt.title("🌡️ Semantic Pressure Field Map")
    plt.xlabel("Seed Space X")
    plt.ylabel("Seed Space Y")
    plt.colorbar(label="Field Intensity")
    plt.grid(False)
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH)
    print(f"[FieldMap] 📊 Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    field = build_field_matrix()
    plot_field(field)
