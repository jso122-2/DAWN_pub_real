
import os
import json
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch

BLOOM_DIR = "juliet_flowers/bloom_metadata"
OUTPUT = "juliet_flowers/cluster_report/drift_lattice.png"

def generate_lattice():
    plt.figure(figsize=(10, 6))
    for fname in os.listdir(BLOOM_DIR):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(BLOOM_DIR, fname), "r") as f:
            bloom = json.load(f)
            x = bloom.get("lineage_depth", 0)
            y = int(bloom["seed_id"][-2:]) if bloom["seed_id"][-2:].isdigit() else 0
            entropy = bloom.get("entropy_score", 0.0)
            plt.scatter(x, y, s=150, c=[[1-entropy, 0.2, entropy]], edgecolors='black')
            plt.text(x + 0.1, y, bloom["seed_id"], fontsize=7)

    plt.title("🕸️ Semantic Drift Lattice")
    plt.xlabel("Lineage Depth")
    plt.ylabel("Semantic Y")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT)
    print(f"[Lattice] 🕸️ Drift lattice saved → {OUTPUT}")

if __name__ == "__main__":
    generate_lattice()
