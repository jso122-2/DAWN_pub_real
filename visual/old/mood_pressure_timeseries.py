import json
import matplotlib.pyplot as plt
from datetime import datetime
import os

LOG_PATH = "juliet_flowers/bloom_log.csv"

def plot_mood_pressure_series():
    mood_totals = {}
    mood_times = {}

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()[1:]  # skip header
        for line in lines:
            timestamp, _, _, mood, entropy, bloom_factor, _ = line.strip().split(",")
            mood_totals.setdefault(mood, []).append(float(entropy) * float(bloom_factor))
            mood_times.setdefault(mood, []).append(datetime.fromisoformat(timestamp))

    for mood in mood_totals:
        plt.plot(mood_times[mood], mood_totals[mood], label=mood)

    plt.legend()
    plt.title("📈 Mood Pressure Over Time (from Bloom Events)")
    plt.xlabel("Time")
    plt.ylabel("Mood Pressure (entropy × factor)")
    plt.tight_layout()
    path = "juliet_flowers/cluster_report/mood_pressure_timeseries.png"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.savefig(path)
    print(f"✅ Saved → {path}")
    plt.close()

if __name__ == "__main__":
    plot_mood_pressure_series()
