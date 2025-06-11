import os
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation

BLOOM_DIR = "juliet_flowers/bloom_metadata"

def animate_synthesis_blooms():
    blooms = []
    for file in sorted(os.listdir(BLOOM_DIR)):
        if not file.endswith(".json"):
            continue
        with open(os.path.join(BLOOM_DIR, file), "r") as f:
            data = json.load(f)
            if data.get("mood") == "synthesis":
                blooms.append({
                    "tick": data.get("timestamp", file[:16]),
                    "id": data["seed_id"],
                    "depth": data.get("lineage_depth", 0),
                    "factor": data.get("bloom_factor", 1.0)
                })

    fig, ax = plt.subplots(figsize=(8, 8))
    ticks = [b["tick"] for b in blooms]

    def update(i):
        ax.clear()
        subset = blooms[:i + 1]
        for bloom in subset:
            ax.scatter(
                bloom["depth"],
                bloom["factor"],
                s=bloom["factor"] * 80,
                alpha=0.6,
                label=bloom["id"]
            )
        ax.set_title(f"🌸 Bloom Emergence – Tick {ticks[i]}")
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 5)
        ax.set_xlabel("Lineage Depth")
        ax.set_ylabel("Bloom Factor")

    ani = animation.FuncAnimation(fig, update, frames=len(blooms), interval=700, repeat=False)
    ani.save("visuals/synthesis_bloom_animation.gif", writer="pillow")
    plt.close()

if __name__ == "__main__":
    animate_synthesis_blooms()
