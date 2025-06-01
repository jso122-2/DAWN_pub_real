import os
import json
import matplotlib.pyplot as plt
import numpy as np

ROOT = "juliet_flowers/"
ENTROPY_JSON = "juliet_flowers/cluster_report/owl_entropy_report.json"
OUTPUT = "juliet_flowers/cluster_report/drift_entropy_overlay.png"

def load_entropy():
    with open(ENTROPY_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def load_bloom_sequence():
    sequences = {}
    for seed in os.listdir(ROOT):
        seed_path = os.path.join(ROOT, seed)
        if not os.path.isdir(seed_path):
            continue
        bloom_list = []
        for mood in os.listdir(seed_path):
            mood_path = os.path.join(seed_path, mood)
            if not os.path.isdir(mood_path):
                continue
            for tick in os.listdir(mood_path):
                tick_path = os.path.join(mood_path, tick)
                if not os.path.isdir(tick_path):
                    continue
                for fname in os.listdir(tick_path):
                    if fname.endswith(".json") and "flower" in fname:
                        with open(os.path.join(tick_path, fname), "r", encoding="utf-8") as f:
                            bloom = json.load(f)
                            bloom_id = bloom["id"]
                            coord = bloom.get("seed_coord")
                            factor = bloom.get("fractal_signature", {}).get("bloom_factor", 1.0)
                            if coord:
                                bloom_list.append((int(tick), coord, bloom_id, factor))
        if bloom_list:
            bloom_list.sort()
            sequences[seed] = bloom_list
    return sequences

def plot_entropy_drifts(sequences, entropy_scores):
    plt.figure(figsize=(10, 10))
    ax = plt.gca()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_title("🧠🌀 Drift-Entropy Hybrid Field")
    ax.set_xlabel("Seed Space X")
    ax.set_ylabel("Seed Space Y")

    for agent, path in sequences.items():
        for i in range(1, len(path)):
            _, (x0, y0), id0, f0 = path[i - 1]
            _, (x1, y1), id1, f1 = path[i]

            dx = x1 - x0
            dy = y1 - y0

            entropy1 = entropy_scores.get(id1, {}).get("delta_entropy", 0.0)
            color = "red" if entropy1 > 2.0 else "blue"
            alpha = min(0.9, 0.4 + 0.2 * entropy1)
            width = 1.0 + 0.5 * abs(f1 - f0)

            ax.arrow(x0, y0, dx, dy, head_width=1.5, color=color,
                     length_includes_head=True, alpha=alpha, linewidth=width)

    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT)
    print(f"[DriftEntropy] 🧠🌀 Merged map saved to {OUTPUT}")

if __name__ == "__main__":
    entropy = load_entropy()
    data = load_bloom_sequence()
    plot_entropy_drifts(data, entropy)
