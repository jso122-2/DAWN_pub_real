
import json
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

LOG_PATH = "mycelium_logs/nutrient_log.json"
OUTPUT = "juliet_flowers/cluster_report/nutrient_trails.gif"

def animate_nutrient_trails():
    if not os.path.exists(LOG_PATH):
        print("[NutrientTrails] ❌ No nutrient log found.")
        return

    with open(LOG_PATH, "r") as f:
        raw = json.load(f)

    depths = sorted(int(k) for k in raw.keys())
    max_count = max(raw[str(k)] for k in depths)
    counts = [raw[str(k)] for k in depths]

    fig, ax = plt.subplots()
    bars = ax.bar(depths, [0]*len(depths), color="limegreen")

    def update(frame):
        for i, b in enumerate(bars):
            if i <= frame:
                b.set_height(counts[i])
                b.set_color((1 - counts[i]/max_count, 0.5, counts[i]/max_count))
        ax.set_title("🕸️ Nutrient Trails by Depth")
        ax.set_xlabel("Lineage Depth")
        ax.set_ylabel("Bloom Count")
        ax.set_ylim(0, max(counts) + 1)
        plt.tight_layout()

    ani = animation.FuncAnimation(fig, update, frames=len(depths), interval=1000, repeat=False)
    ani.save(OUTPUT, writer="pillow")
    print(f"[NutrientTrails] 🕸️ Saved → {OUTPUT}")
