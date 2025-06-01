
import os
import json
import matplotlib.pyplot as plt

BLOOM_DIR = "juliet_flowers/bloom_metadata"
OUTPUT = "juliet_flowers/cluster_report/entropy_clusters.png"

def cluster_entropy():
    clusters = {"low": [], "medium": [], "high": []}

    for fname in os.listdir(BLOOM_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(BLOOM_DIR, fname), "r") as f:
                bloom = json.load(f)
                e = bloom.get("entropy_score", 0.0)
                if e < 0.3:
                    clusters["low"].append(bloom)
                elif e < 0.7:
                    clusters["medium"].append(bloom)
                else:
                    clusters["high"].append(bloom)

    counts = [len(clusters["low"]), len(clusters["medium"]), len(clusters["high"])]
    labels = ["Low (0–0.3)", "Medium (0.3–0.7)", "High (0.7–1.0)"]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, counts, color=["blue", "orange", "red"])
    plt.title("🔬 Entropy Clustering by Variance")
    plt.ylabel("Bloom Count")
    plt.tight_layout()
    plt.savefig(OUTPUT)
    print(f"[Clusters] 🔬 Saved → {OUTPUT}")
