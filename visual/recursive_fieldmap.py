
import os
import json
import matplotlib.pyplot as plt
import numpy as np

BLOOM_DIR = "juliet_flowers/bloom_metadata"
OUTPUT = "juliet_flowers/cluster_report/recursive_fieldmap.png"

def load_blooms():
    blooms = []
    for fname in os.listdir(BLOOM_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(BLOOM_DIR, fname), "r") as f:
                bloom = json.load(f)
                blooms.append(bloom)
    return blooms

def render_fieldmap():
    blooms = load_blooms()
    if not blooms:
        print("[FieldMap] ❌ No blooms found.")
        return

    # Assign coordinates via synthetic lineage mapping
    coords = []
    for bloom in blooms:
        x = bloom.get("lineage_depth", 0)
        y = int(bloom["seed_id"][-2:]) if bloom["seed_id"][-2:].isdigit() else np.random.randint(0, 20)
        entropy = bloom.get("entropy_score", 0.0)
        mood = bloom.get("mood", "unknown")
        coords.append((x, y, entropy, mood, bloom["seed_id"]))

    plt.figure(figsize=(10, 6))
    for x, y, entropy, mood, seed_id in coords:
        plt.scatter(x, y, s=100, c=[[1-entropy, 0.3, entropy]], label=mood, edgecolors='black')
        plt.text(x + 0.1, y, seed_id, fontsize=6)

    plt.title("Recursive Field Map")
    plt.xlabel("Lineage Depth")
    plt.ylabel("Semantic Drift Position (Y)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT)
    print(f"[FieldMap] 🌌 Saved → {OUTPUT}")

if __name__ == "__main__":
    render_fieldmap()
