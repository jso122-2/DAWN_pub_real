import os
import json
import matplotlib.pyplot as plt
from datetime import datetime

LOG_PATH = "juliet_flowers/cluster_report/sigil_emission_log.json"
OUT = "juliet_flowers/cluster_report/sigil_timeline.png"

def load_log():
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH) as f:
        return json.load(f)

def plot_timeline():
    data = load_log()
    if not data:
        print("❌ No sigil emission data found.")
        return

    timestamps = [datetime.fromisoformat(e["timestamp"]) for e in data]
    sigils = [e["sigil"] for e in data]

    plt.figure(figsize=(10, 5))
    plt.scatter(timestamps, sigils, marker="|", color="purple", s=300)
    plt.title("📈 Sigil Emissions Over Time")
    plt.ylabel("Sigil")
    plt.xlabel("Timestamp")
    plt.xticks(rotation=45)
    plt.grid(True, axis="y")
    plt.tight_layout()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    plt.savefig(OUT)
    plt.close()
    print(f"✅ Sigil timeline saved → {OUT}")

if __name__ == "__main__":
    plot_timeline()
