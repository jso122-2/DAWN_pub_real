# /visual/persephone_decay_map.py

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os

def render_soft_edge_decay_map(soft_edge_history, output="juliet_flowers/cluster_report/persephone_decay_map.png"):
    """
    Render a heatmap-style scatterplot of soft-edged bloom activity over time.
    X-axis: Tick
    Y-axis: Bloom index
    Color: Occurrence
    """
    if not soft_edge_history:
        print("[PersephoneViz] ❌ No decay data to visualize.")
        return

    ticks = []
    bloom_ids = []

    for tick, blooms in soft_edge_history.items():
        for b in blooms:
            ticks.append(tick)
            bloom_ids.append(b)

    bloom_to_idx = {b: i for i, b in enumerate(sorted(set(bloom_ids)))}
    y = [bloom_to_idx[b] for b in bloom_ids]

    plt.figure(figsize=(12, 6))
    plt.scatter(ticks, y, c=y, cmap="inferno", s=50, alpha=0.8)
    plt.xlabel("Tick")
    plt.ylabel("Bloom")
    plt.title("🌒 Persephone Soft Edge Map")
    plt.yticks(range(len(bloom_to_idx)), list(bloom_to_idx.keys()), fontsize=7)
    plt.grid(alpha=0.3)
    plt.tight_layout()

    os.makedirs(os.path.dirname(output), exist_ok=True)
    plt.savefig(output)
    print(f"[PersephoneViz] 🖼️ Soft edge decay map saved → {output}")
