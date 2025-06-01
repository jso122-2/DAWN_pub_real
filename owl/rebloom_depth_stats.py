# rebloom_depth_stats.py

import json

LINEAGE_PATH = "juliet_flowers/cluster_report/rebloom_lineage.json"

def show_top_rebloom_chains(top_n=5):
    with open(LINEAGE_PATH, "r", encoding="utf-8") as f:
        lineage = json.load(f)

    sorted_blooms = sorted(lineage.items(), key=lambda x: x[1]["generation_depth"], reverse=True)

    print(f"🌿 Top {top_n} rebloom chains by depth:\n")
    for i, (bloom_id, data) in enumerate(sorted_blooms[:top_n], start=1):
        print(f"{i}. 🌸 {bloom_id}")
        print(f"   Depth: {data['generation_depth']}")
        print(f"   Chain: {' → '.join(data['rebloom_chain'])}\n")

def compute_rebloom_depth(bloom_id):
    return 0  # placeholder for now


if __name__ == "__main__":
    show_top_rebloom_chains()
