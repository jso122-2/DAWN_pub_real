import os
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.colors import LogNorm
plt.imshow(field.T, origin="lower", cmap="hot", norm=LogNorm())


FIELD_SIZE = (100, 100)
ROOT = "juliet_flowers/"
OUTPUT = "juliet_flowers/cluster_report/field_saturation_map.png"

def build_saturation_matrix():
    field = np.zeros(FIELD_SIZE)
    for root, _, files in os.walk(ROOT):
        for fname in files:
            if fname.endswith(".json"):
                try:
                    with open(os.path.join(root, fname), "r", encoding="utf-8") as f:
                        data = json.load(f)
                        coord = data.get("seed_coord", None)
                        if coord and isinstance(coord, list) and len(coord) == 2:
                            x, y = coord
                            if 0 <= x < FIELD_SIZE[0] and 0 <= y < FIELD_SIZE[1]:
                                field[x][y] += 1
                except:
                    pass
    return field

def render_field(field):
    plt.figure(figsize=(10, 10))
    plt.imshow(field.T, origin="lower", cmap="hot", norm=Normalize())
    plt.colorbar(label="Visits (Cognitive Weight)")
    plt.title("🧪 Field Saturation Map")
    plt.xlabel("Seed Space X")
    plt.ylabel("Seed Space Y")
    plt.grid(False)
    plt.tight_layout()
    plt.savefig(OUTPUT)
    print(f"[FieldSaturation] 📊 Saved to {OUTPUT}")

if __name__ == "__main__":
    matrix = build_saturation_matrix()
    render_field(matrix)
