import json
import os
from itertools import combinations
from collections import defaultdict

CLUSTER_REPORT = os.path.join("juliet_flowers", "cluster_report", "cluster_report.json")

def load_clusters():
    with open(CLUSTER_REPORT, "r") as f:
        return json.load(f)

def link_clusters(clusters, seed_overlap_weight=1.0, mood_overlap_weight=1.0, bloom_diff_weight=1.0):
    links = []

    for c1, c2 in combinations(clusters, 2):
        shared_seeds = set(c1["seeds"]) & set(c2["seeds"])
        shared_moods = set(c1["agents"]) & set(c2["agents"])

        bloom1 = sum(c1["bloom_factor_range"]) / 2
        bloom2 = sum(c2["bloom_factor_range"]) / 2
        bloom_diff = abs(bloom1 - bloom2)

        score = (
            len(shared_seeds) * seed_overlap_weight +
            len(shared_moods) * mood_overlap_weight -
            bloom_diff * bloom_diff_weight
        )

        if score > 0:
            links.append({
                "from": c1["cluster_id"],
                "to": c2["cluster_id"],
                "score": round(score, 2),
                "shared_seeds": list(shared_seeds),
                "shared_agents": list(shared_moods),
                "bloom_diff": round(bloom_diff, 2)
            })

    return sorted(links, key=lambda x: -x["score"])
