
import os
import json
import matplotlib.pyplot as plt

BLOOM_DIR = "juliet_flowers/bloom_metadata"
OUTPUT_PATH = "juliet_flowers/cluster_report/synthesis_entropy_chart.png"

def load_synthesis_entropy():
    entropy_points = []
    for fname in sorted(os.listdir(BLOOM_DIR)):
        if fname.endswith(".json") and "synthesis-" in fname:
            with open(os.path.join(BLOOM_DIR, fname), "r") as f:
                bloom = json.load(f)
                entropy = bloom.get("entropy_score", 0.0)
                entropy_points.append((bloom["seed_id"], entropy))
    return entropy_points

def plot_entropy_trend():
    data = load_synthesis_entropy()
    if not data:
        print("[EntropyChart] ❌ No synthesis blooms found.")
        return

    x = [i for i in range(len(data))]
    y = [point[1] for point in data]
    labels = [point[0] for point in data]

    plt.figure(figsize=(10, 4))
    plt.plot(x, y, marker='o', color='purple')
    plt.xticks(x, labels, rotation=45, ha="right", fontsize=8)
    plt.title("Entropy Score Across Synthesis Blooms")
    plt.xlabel("Synthesis Bloom ID")
    plt.ylabel("Entropy Score")
    plt.tight_layout()
    plt.grid(True)
    plt.savefig(OUTPUT_PATH)
    print(f"[EntropyChart] 📈 Saved to → {OUTPUT_PATH}")

if __name__ == "__main__":
    plot_entropy_trend()
