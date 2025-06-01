# /mycelium/mycelium_animation.py

"""
Dual animations for mycelium behavior:

1. animate_nutrient_map:
   - Visualizes nutrient accumulation by lineage depth.
   - Uses mycelium_logs/nutrient_log.json

2. animate_root_density_over_time:
   - Visualizes root density changes per seed over time.
   - Uses logs/mycelium_logs/nutrient_flow.csv
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import defaultdict

# --- CONFIG ---
JSON_LOG = "mycelium_logs/nutrient_log.json"
CSV_LOG = "logs/mycelium_logs/nutrient_flow.csv"
OUT_NUTRIENT = "juliet_flowers/cluster_report/nutrient_growth.gif"
OUT_DENSITY = "visuals/root_density_over_time.gif"

# --- A. Nutrient Accumulation over Lineage Depth ---
def animate_nutrient_map():
    if not os.path.exists(JSON_LOG):
        print("[Mycelium] ❌ No nutrient_log.json found.")
        return

    with open(JSON_LOG, "r") as f:
        raw = json.load(f)

    depths = sorted(int(k) for k in raw.keys())
    values = [raw[str(k)] for k in depths]

    fig, ax = plt.subplots(figsize=(10, 6))
    bar = ax.bar(depths, [0] * len(depths), color="seagreen")
    ax.set_ylim(0, max(values) + 2)
    ax.set_xlabel("Lineage Depth")
    ax.set_ylabel("Bloom Count")
    ax.set_title("🌱 Nutrient Accumulation Over Lineage")

    def update(frame):
        for i, b in enumerate(bar):
            if i <= frame:
                b.set_height(values[i])
        ax.set_title(f"🌱 Nutrient Accumulation – Depth ≤ {depths[frame]}")

    ani = animation.FuncAnimation(fig, update, frames=len(depths), interval=1000, repeat=False)

    os.makedirs(os.path.dirname(OUT_NUTRIENT), exist_ok=True)
    ani.save(OUT_NUTRIENT, writer="pillow")
    print(f"[Mycelium] 🌿 Nutrient map saved → {OUT_NUTRIENT}")

# --- B. Root Density Evolution over Time ---
def animate_root_density_over_time():
    if not os.path.exists(CSV_LOG):
        print("[Mycelium] ❌ nutrient_flow.csv not found.")
        return

    df = pd.read_csv(CSV_LOG)
    if "tick" not in df or "seed" not in df:
        print("[Mycelium] ❌ Missing required 'tick' or 'seed' columns.")
        return

    ticks = sorted(df["tick"].unique())
    seeds = sorted(df["seed"].unique())

    # Build tick → seed → count map
    density = defaultdict(lambda: {seed: 0 for seed in seeds})
    for _, row in df.iterrows():
        density[row["tick"]][row["seed"]] += 1

    fig, ax = plt.subplots(figsize=(12, 6))
    bar = ax.bar(seeds, [0] * len(seeds), color="seagreen")
    ax.set_ylim(0, max(max(seed_map.values()) for seed_map in density.values()) + 1)
    ax.set_title("🌱 Root Density Over Time")
    ax.set_xlabel("Seed")
    ax.set_ylabel("Density (Nutrient Hits)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    def update(frame_idx):
        tick = ticks[frame_idx]
        current = density[tick]
        for bar_rect, seed in zip(bar, seeds):
            bar_rect.set_height(current[seed])
        ax.set_title(f"🌱 Root Density – Tick {tick}")

    ani = animation.FuncAnimation(fig, update, frames=len(ticks), interval=500, repeat=False)

    os.makedirs(os.path.dirname(OUT_DENSITY), exist_ok=True)
    ani.save(OUT_DENSITY, writer="pillow")
    print(f"[Mycelium] ✅ Root density animation saved → {OUT_DENSITY}")

# --- CLI Trigger ---
if __name__ == "__main__":
    animate_nutrient_map()
    animate_root_density_over_time()
