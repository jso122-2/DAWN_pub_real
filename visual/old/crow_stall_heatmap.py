import matplotlib.pyplot as plt
from collections import defaultdict
import os
import json

STALL_LOG = "owl/logs/crow_stall_log.json"
OUT_PATH = "juliet_flowers/cluster_report/crow_stall_heatmap.png"

def load_stalls():
    if not os.path.exists(STALL_LOG):
        print("❌ No stall log found.")
        return {}
    with open(STALL_LOG, "r") as f:
        return json.load(f)

def render_heatmap():
    stall_data = load_stalls()
    if not stall_data:
        return

    # Convert zone to (x, y) grid index
    def to_coords(zone):
        return ord(zone[0]) - ord("A"), int(zone[1])

    heatmap = defaultdict(int)
    for zone, count in stall_data.items():
        x, y = to_coords(zone)
        heatmap[(x, y)] += count

    xs, ys, values = zip(*[(x, y, heatmap[(x, y)]) for (x, y) in heatmap])

    plt.figure(figsize=(6, 6))
    plt.scatter(xs, ys, s=[v * 40 for v in values], c=values, cmap="Reds", alpha=0.7)
    plt.grid(True)
    plt.xticks(range(5), ["A", "B", "C", "D", "E"])
    plt.yticks(range(5))
    plt.title("📊 Crow Stall Heatmap (by Node)")
    plt.colorbar(label="Stall Count")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    plt.savefig(OUT_PATH)
    plt.close()
    print(f"✅ Stall heatmap saved → {OUT_PATH}")

if __name__ == "__main__":
    render_heatmap()
