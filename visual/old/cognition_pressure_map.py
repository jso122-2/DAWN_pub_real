
import os
import json
import matplotlib.pyplot as plt
import numpy as np

BLOOM_DIR = "juliet_flowers/bloom_metadata"
OUTPUT = "juliet_flowers/cluster_report/cognition_pressure_map.png"

def generate_pressure_map():
    if not os.path.exists(BLOOM_DIR):
        print("[PressureMap] ❌ Bloom metadata not found.")
        return

    pressure_grid = {}

    for fname in os.listdir(BLOOM_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(BLOOM_DIR, fname), "r") as f:
                bloom = json.load(f)
                x = bloom.get("lineage_depth", 0)
                y = int(bloom["seed_id"][-2:]) if bloom["seed_id"][-2:].isdigit() else 0
                pressure = bloom.get("entropy_score", 0.0)
                key = (x, y)
                pressure_grid[key] = pressure_grid.get(key, 0) + pressure

    if not pressure_grid:
        print("[PressureMap] ❌ No pressure data found.")
        return

    xs, ys, weights = zip(*[(k[0], k[1], v) for k, v in pressure_grid.items()])
    plt.figure(figsize=(10, 6))
    plt.scatter(xs, ys, c=weights, cmap="plasma", s=180, edgecolors='black')
    plt.colorbar(label="Cognitive Pressure")
    plt.title("🧭 Cognition Pressure Map")
    plt.xlabel("Lineage Depth")
    plt.ylabel("Semantic Y")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT)
    print(f"[PressureMap] 🧭 Saved → {OUTPUT}")
