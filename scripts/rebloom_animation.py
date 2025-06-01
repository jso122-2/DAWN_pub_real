import os
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation

DATA_DIR = "juliet_flowers/bloom_metadata"

def load_bloom_data():
    blooms = []
    for f in os.listdir(DATA_DIR):
        if f.endswith(".json"):
            with open(os.path.join(DATA_DIR, f), "r") as file:
                data = json.load(file)
                if data.get("seed_id", "").startswith("rebloom") or data.get("mood") == "rebloom":
                    blooms.append(data)
    return sorted(blooms, key=lambda b: b.get("timestamp", "0"))

def color_by_depth(depth):
    # RGB spectrum: early gen → blue, late gen → red
    scale = min(depth / 10, 1.0)
    return (scale, 0, 1.0 - scale)  # Red → Blue

def animate_rebloom_trails():
    blooms = load_bloom_data()
    fig, ax = plt.subplots(figsize=(10, 6))

    def update(i):
        ax.clear()
        current = blooms[:i + 1]
        for bloom in current:
            x = bloom.get("lineage_depth", 0)
            y = bloom.get("entropy_score", 0.0)
            color = color_by_depth(x)
            ax.scatter(x, y, s=60, color=color, alpha=0.7)
            ax.text(x, y + 0.05, bloom["seed_id"], fontsize=6)

        ax.set_xlim(0, 15)
        ax.set_ylim(0, 1)
        ax.set_title(f"🌱 Rebloom Trail Map – Frame {i+1}")
        ax.set_xlabel("Lineage Depth")
        ax.set_ylabel("Entropy")

    ani = animation.FuncAnimation(fig, update, frames=len(blooms), interval=500, repeat=False)
    os.makedirs("visuals", exist_ok=True)
    ani.save("visuals/rebloom_trail_animation.gif", writer="pillow")
    plt.close()

if __name__ == "__main__":
    animate_rebloom_trails()
