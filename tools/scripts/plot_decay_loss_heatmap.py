# /scripts/plot_decay_loss_heatmap.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_decay_loss_heatmap(log_path="logs/decay_loss_log.csv"):
    if not os.path.exists(log_path):
        print("No decay log found.")
        return

    df = pd.read_csv(log_path)
    df["tick_id"] = df["tick_id"].astype(str)

    pivot = df.pivot_table(
        index="to",
        columns="tick_id",
        values="total_decay",
        aggfunc="sum",
        fill_value=0
    )

    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot, cmap="YlOrRd", linewidths=0.1, linecolor="black")
    plt.title("🔥 Total Decay Loss Heatmap (to-node vs. tick)")
    plt.xlabel("Tick ID")
    plt.ylabel("To Node")
    plt.tight_layout()
    plt.savefig("visuals/decay_loss_heatmap.png")
    plt.show()

if __name__ == "__main__":
    plot_decay_loss_heatmap()
