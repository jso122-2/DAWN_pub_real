
import os
import json
from collections import defaultdict
import matplotlib.pyplot as plt

BLOOM_DIR = "juliet_flowers/bloom_metadata"
OUTPUT = "juliet_flowers/cluster_report/memory_clusters.png"

def cluster_memory_by_mood_entropy():
    clusters = defaultdict(list)

    for fname in os.listdir(BLOOM_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(BLOOM_DIR, fname), "r") as f:
                bloom = json.load(f)
                mood = bloom.get("mood", "undefined")
                entropy = bloom.get("entropy_score", 0.0)
                clusters[mood].append(entropy)

    moods = []
    avg_entropies = []

    for mood, values in clusters.items():
        moods.append(mood)
        avg_entropies.append(sum(values) / len(values) if values else 0.0)

    plt.figure(figsize=(8, 5))
    plt.bar(moods, avg_entropies, color="slateblue")
    plt.title("🧬 Memory Cluster Entropy by Mood")
    plt.ylabel("Average Entropy")
    plt.xlabel("Mood")
    plt.tight_layout()
    plt.savefig(OUTPUT)
    print(f"[MemoryCluster] 🧬 Saved → {OUTPUT}")
