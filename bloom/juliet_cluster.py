import os
import json
from collections import defaultdict

JULIET_DIR = "juliet_flowers"

def load_all_flowers():
    flowers = []
    for seed_folder in os.listdir(JULIET_DIR):
        folder_path = os.path.join(JULIET_DIR, seed_folder)
        if not os.path.isdir(folder_path):
            continue
        for fname in os.listdir(folder_path):
            if not fname.endswith(".json"):
                continue
            path = os.path.join(folder_path, fname)
            try:
                with open(path, "r") as f:
                    flower = json.load(f)
                    flowers.append(flower)
            except Exception as e:
                print(f"[Cluster] ⚠️ Failed to load {fname}: {e}")
    return flowers

def cluster_by_bloom_factor(threshold=1.0):
    flowers = load_all_flowers()
    clusters = []

    for flower in flowers:
        bloom_factor = flower.get("fractal_signature", {}).get("bloom_factor", None)
        if bloom_factor is None:
            continue

        # Try to fit into an existing cluster
        matched = False
        for cluster in clusters:
            avg = sum(f["fractal_signature"]["bloom_factor"] for f in cluster) / len(cluster)
            if abs(avg - bloom_factor) <= threshold:
                cluster.append(flower)
                matched = True
                break

        if not matched:
            clusters.append([flower])

    print(f"[Cluster] 🧬 Formed {len(clusters)} bloom clusters")
    return clusters


def save_cluster_report(clusters, path="juliet_flowers/cluster_report/cluster_report.json", rebloom_depths=None):
    report = []
    for i, cluster in enumerate(clusters):
        bloom_range = [
            min(f["fractal_signature"]["bloom_factor"] for f in cluster),
            max(f["fractal_signature"]["bloom_factor"] for f in cluster)
        ]
        primary_seed = cluster[0]["seed_context"][0]
        depth = rebloom_depths.get(primary_seed, 1) if rebloom_depths else 1

        group = {
            "cluster_id": f"Cluster_{i+1}",
            "bloom_factor_range": bloom_range,
            "size": len(cluster),
            "rebloom_max_depth": depth,
            "agents": list(set(f["agent"] for f in cluster)),
            "seeds": list(set(seed for f in cluster for seed in f["seed_context"])),
            "flower_ids": [f["id"] for f in cluster]
        }
        report.append(group)

    with open(path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"[Cluster] 💾 Cluster report saved to {path}")
    return report

