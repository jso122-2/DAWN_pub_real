
import os
import json
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
import matplotlib.animation as animation

BLOOM_DIR = "juliet_flowers/bloom_metadata"
OUTPUT = "juliet_flowers/cluster_report/recursive_bloom_tree.gif"

def load_blooms():
    blooms = []
    for fname in sorted(os.listdir(BLOOM_DIR)):
        if fname.endswith(".json"):
            with open(os.path.join(BLOOM_DIR, fname), "r") as f:
                bloom = json.load(f)
                blooms.append(bloom)
    return blooms

def animate_bloom_tree():
    blooms = load_blooms()
    fig, ax = plt.subplots(figsize=(10, 6))
    plotted = []

    def update(frame):
        ax.clear()
        current = blooms[:frame+1]
        for b in current:
            x = b.get("lineage_depth", 0)
            y = int(b["seed_id"][-2:]) if b["seed_id"][-2:].isdigit() else 0
            entropy = b.get("entropy_score", 0.0)
            ax.scatter(x, y, s=140, c=[[1-entropy, 0.3, entropy]], edgecolors='black')
            ax.text(x + 0.1, y, b["seed_id"], fontsize=6)
        ax.set_title("🌿 Recursive Bloom Tree")
        ax.set_xlabel("Lineage Depth")
        ax.set_ylabel("Semantic Y")
        ax.grid(True)
        plt.tight_layout()

    ani = animation.FuncAnimation(fig, update, frames=len(blooms), interval=700, repeat=False)
    ani.save(OUTPUT, writer="pillow")
    print(f"[Tree] 🌿 Saved → {OUTPUT}")

if __name__ == "__main__":
    animate_bloom_tree()
