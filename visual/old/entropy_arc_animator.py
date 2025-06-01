
import os
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation

BLOOM_DIR = "juliet_flowers/bloom_metadata"
OUTPUT = "juliet_flowers/cluster_report/entropy_arc.gif"

def load_entropy_blooms():
    entries = []
    for fname in sorted(os.listdir(BLOOM_DIR)):
        if fname.endswith(".json") and fname.startswith(("synthesis-", "cornerfusion-", "recursive-")):
            with open(os.path.join(BLOOM_DIR, fname), "r") as f:
                bloom = json.load(f)
                entries.append((bloom["seed_id"], bloom.get("entropy_score", 0.0)))
    return entries

def animate_entropy_arc():
    data = load_entropy_blooms()
    if not data:
        print("[EntropyArc] ❌ No fusion/synthesis blooms found.")
        return

    fig, ax = plt.subplots(figsize=(10, 4))
    x = []
    y = []

    def update(frame):
        ax.clear()
        x.append(frame)
        y.append(data[frame][1])
        ax.plot(x, y, marker='o', color='crimson')
        ax.set_xticks(x)
        ax.set_xticklabels([data[i][0] for i in range(len(x))], rotation=45, ha="right", fontsize=8)
        ax.set_title("📈 Entropy Arc (Fusion Lineage)")
        ax.set_ylabel("Entropy Score")
        ax.set_ylim(0, 1)
        ax.grid(True)
        plt.tight_layout()

    ani = animation.FuncAnimation(fig, update, frames=len(data), interval=800, repeat=False)
    ani.save(OUTPUT, writer="pillow")
    print(f"[EntropyArc] 📈 Saved → {OUTPUT}")

if __name__ == "__main__":
    animate_entropy_arc()
