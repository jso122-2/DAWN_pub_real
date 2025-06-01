# /owl/owl_entropy_plot.py

import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def render_entropy_chart(
    log_path="logs/owl_entropy_log.csv",
    output_path="juliet_flowers/cluster_report/entropy_chart.png",
    title="🧠 Owl Entropy Drift Timeline",
    show=True
):
    """
    Reads logged entropy deltas from Owl and renders a drift-over-time chart.
    """
    if not os.path.exists(log_path):
        print(f"[OwlPlot] ❌ Entropy log not found at {log_path}")
        return None

    try:
        df = pd.read_csv(log_path)
        if df.empty:
            print("[OwlPlot] ⚠️ Entropy log is empty.")
            return None

        ticks = df["tick"] if "tick" in df.columns else range(len(df))
        entropy = df["delta"] if "delta" in df.columns else df.iloc[:, -1]

        plt.figure(figsize=(12, 5))
        plt.plot(ticks, entropy, color="purple", linewidth=2)
        plt.title(title)
        plt.xlabel("Tick")
        plt.ylabel("Entropy Drift ∆")
        plt.grid(alpha=0.3)
        plt.axhline(0.6, color="red", linestyle="--", label="Drift Alert Threshold")
        plt.legend()
        plt.tight_layout()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        if show:
            plt.show()
        plt.close()

        print(f"[OwlPlot] ✅ Entropy chart saved → {output_path}")
        return output_path

    except Exception as e:
        print(f"[OwlPlot] ❌ Failed to render chart: {e}")
        return None
