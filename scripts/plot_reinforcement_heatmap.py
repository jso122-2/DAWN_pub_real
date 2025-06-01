import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def plot_reinforcement_heatmap(path="logs/reinforcement_log.json"):
    if not os.path.exists(path):
        print("No reinforcement log found.")
        return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Build DataFrame from snapshots
    rows = []
    for snapshot in data:
        tick = snapshot["timestamp"]
        for path_key, value in snapshot["reinforcement_tracker"].items():
            source, target = path_key.split("→")
            rows.append({"tick": tick, "from": source, "to": target, "reinforcement": value})

    df = pd.DataFrame(rows)
    pivot = df.pivot_table(index="from", columns="to", values="reinforcement", aggfunc="max", fill_value=0)

    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot, cmap="YlGnBu", linewidths=0.3, linecolor="gray", annot=True, fmt=".1f")
    plt.title("🧬 Reinforcement Heatmap (Paths)")
    plt.tight_layout()
    plt.savefig("visuals/reinforcement_heatmap.png")
    plt.show()

if __name__ == "__main__":
    plot_reinforcement_heatmap()
