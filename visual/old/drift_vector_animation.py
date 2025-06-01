
import os
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

BLOOM_DIR = "juliet_flowers/bloom_metadata"
OUTPUT = "juliet_flowers/cluster_report/drift_vector_animation.gif"

def load_blooms():
    blooms = []
    for fname in sorted(os.listdir(BLOOM_DIR)):
        if fname.endswith(".json"):
            with open(os.path.join(BLOOM_DIR, fname), "r") as f:
                bloom = json.load(f)
                blooms.append(bloom)
    return blooms

def extract_drift_coords(blooms):
    coords = []
    for bloom in blooms:
        x = bloom.get("lineage_depth", 0)
        y = int(bloom["seed_id"][-2:]) if bloom["seed_id"][-2:].isdigit() else np.random.randint(0, 20)
        entropy = bloom.get("entropy_score", 0.0)
        coords.append((x, y, entropy, bloom["seed_id"]))
    return coords

def animate_drift():
    blooms = load_blooms()
    coords = extract_drift_coords(blooms)

    fig, ax = plt.subplots(figsize=(10, 6))
    scat = ax.scatter([], [], s=100, edgecolors='black')
    txt = ax.text(0.5, 1.05, "", ha="center", transform=ax.transAxes, fontsize=12)

    def update(frame):
        ax.clear()
        for i in range(min(len(coords), frame + 1)):
            x, y, entropy, seed_id = coords[i]
            ax.scatter(x, y, s=100, c=[[1 - entropy, 0.3, entropy]], edgecolors='black')
            ax.text(x + 0.1, y, seed_id, fontsize=6)
        ax.set_title("Drift Vector Animation")
        ax.set_xlabel("Lineage Depth")
        ax.set_ylabel("Semantic Drift (Y)")
        ax.grid(True)
        txt.set_text(f"Tick {frame + 1}")
        return scat,

    ani = animation.FuncAnimation(fig, update, frames=len(coords), interval=700, repeat=False)
    ani.save(OUTPUT, writer="pillow")
    print(f"[DriftVector] 🧲 Animation saved → {OUTPUT}")

if __name__ == "__main__":
    animate_drift()
