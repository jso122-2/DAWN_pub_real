# /visual/visual_bloom_state.py

"""
Visualizes bloom shape states across all saved bloom records.
Each bloom is positioned semantically (e.g., via coordinates or lineage).
Color and symbol represent shape type and stability.
"""

import os
import json
import matplotlib.pyplot as plt

# Config
BLOOM_DIR = "juliet_flowers/bloom_metadata"
COORDS_PATH = "juliet_flowers/cluster_report/seed_coords.json"  # Optional
OUT_PATH = "visuals/bloom_shape_state_map.png"

SHAPE_MARKERS = {
    "crystal": ("o", "skyblue"),
    "spiral": ("^", "violet"),
    "wave": ("s", "gold"),
    "unstable": ("X", "tomato"),
    "undefined": ("?", "gray")
}

def visualize_bloom_shapes():
    bloom_files = [f for f in os.listdir(BLOOM_DIR) if f.endswith(".json")]
    coords = load_coords()

    fig, ax = plt.subplots(figsize=(10, 8))

    for file in bloom_files:
        path = os.path.join(BLOOM_DIR, file)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        seed = data.get("seed_id", "unknown")
        shape = data.get("shape_state", "undefined")
        stability = data.get("stability_index", 0.0)
        x, y = coords.get(seed, (0, 0))

        marker, color = SHAPE_MARKERS.get(shape, ("?", "black"))
        ax.scatter(x, y, s=120, c=color, marker=marker, edgecolors="black")
        ax.text(x + 0.2, y + 0.2, f"{shape[:2]} ({stability:.2f})", fontsize=8)

    ax.set_title("🌸 Bloom Shape States by Semantic Position")
    ax.set_xlabel("Semantic X")
    ax.set_ylabel("Semantic Y")
    ax.grid(True)
    plt.tight_layout()

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    plt.savefig(OUT_PATH)
    print(f"[Visual] ✅ Bloom shape map saved to → {OUT_PATH}")

def load_coords():
    if not os.path.exists(COORDS_PATH):
        return {}
    with open(COORDS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    visualize_bloom_shapes()
