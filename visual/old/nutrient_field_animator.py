import os
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

INPUT_DIR = "juliet_flowers/cluster_report"
NUTRIENT = "attention"
OUT = f"{INPUT_DIR}/animated_{NUTRIENT}_field.gif"

def load_snapshots():
    frames = []
    for f in sorted(os.listdir(INPUT_DIR)):
        if f.startswith("nutrient_pressure_tick") and f.endswith(".json"):
            with open(os.path.join(INPUT_DIR, f)) as file:
                data = json.load(file)
                frames.append((f, data))
    return frames

def animate():
    frames = load_snapshots()
    if not frames:
        print("❌ No nutrient snapshots found.")
        return

    fig, ax = plt.subplots(figsize=(6, 6))

    def to_coords(seed):
        return ord(seed[0]) - ord("A"), int(seed[1])

    def update(i):
        ax.clear()
        fname, snapshot = frames[i]
        xs, ys, vals = [], [], []
        for seed, nutrients in snapshot.items():
            if NUTRIENT in nutrients:
                x, y = to_coords(seed)
                xs.append(x)
                ys.append(y)
                vals.append(nutrients[NUTRIENT])
        scatter = ax.scatter(xs, ys, c=vals, cmap="YlGnBu", s=180, edgecolors="black")
        ax.set_title(f"🎥 {NUTRIENT.title()} Field – {fname}")
        ax.set_xticks(range(5))
        ax.set_yticks(range(5))
        ax.grid(True)

    ani = FuncAnimation(fig, update, frames=len(frames), interval=500, repeat=False)
    ani.save(OUT, writer="pillow")
    plt.close()
    print(f"✅ Animated nutrient field saved → {OUT}")

if __name__ == "__main__":
    animate()
