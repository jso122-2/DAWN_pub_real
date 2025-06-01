import os
import json
import matplotlib.pyplot as plt

BLOOM_DIR = "juliet_flowers/bloom_metadata"
OUT_PATH = "juliet_flowers/cluster_report/belief_resonance_scatter.png"

def visualize_resonance():
    x = []  # lineage_depth
    y = []  # resonance
    colors = []
    labels = []

    for file in os.listdir(BLOOM_DIR):
        if not file.endswith(".json"):
            continue
        with open(os.path.join(BLOOM_DIR, file)) as f:
            data = json.load(f)
            belief_data = data.get("belief_resonance", {})
            if not belief_data:
                continue
            x.append(data.get("lineage_depth", 0))
            y.append(belief_data.get("distance", 0.0))
            colors.append(belief_data.get("rgb", (128, 128, 128)))
            labels.append(belief_data.get("belief", "unknown"))

    plt.figure(figsize=(10, 6))
    for i in range(len(x)):
        plt.scatter(x[i], y[i], color=[c/255 for c in colors[i]], label=labels[i] if labels[i] not in labels[:i] else "", s=80)

    plt.xlabel("Lineage Depth")
    plt.ylabel("Belief Resonance (RGB Distance)")
    plt.title("📊 Bloom Belief Resonance Scatter")
    plt.grid(True)
    plt.legend(loc="upper right")
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    plt.savefig(OUT_PATH)
    plt.close()
    print(f"✅ Resonance scatter saved to: {OUT_PATH}")

if __name__ == "__main__":
    visualize_resonance()
