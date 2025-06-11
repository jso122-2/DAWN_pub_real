# /core/entropy_tracker.py

"""
Tracks and aggregates entropy per bloom and per lineage depth.
Exports entropy summary as CSV for analytical use.
"""

import os
import json
import csv
from collections import defaultdict

BLOOM_DIR = "juliet_flowers/bloom_metadata"
OUT_CSV = "juliet_flowers/cluster_report/entropy_summary.csv"

def aggregate_entropy_per_lineage():
    """
    Scans bloom metadata and aggregates entropy scores per lineage depth.
    Returns both lineage-level and bloom-level summaries.
    """
    lineage_agg = defaultdict(list)
    bloom_summaries = []

    bloom_files = [f for f in os.listdir(BLOOM_DIR) if f.endswith(".json")]

    for file in bloom_files:
        path = os.path.join(BLOOM_DIR, file)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        seed = data.get("seed_id", "unknown")
        depth = data.get("lineage_depth", 0)
        entropy = data.get("entropy_score", 0.0)

        lineage_agg[depth].append(entropy)
        bloom_summaries.append({
            "seed_id": seed,
            "lineage_depth": depth,
            "entropy_score": entropy
        })

    return lineage_agg, bloom_summaries

def export_entropy_summary(csv_path=OUT_CSV):
    """
    Exports a CSV with one row per bloom:
    seed_id, lineage_depth, entropy_score
    """
    _, bloom_summaries = aggregate_entropy_per_lineage()

    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["seed_id", "lineage_depth", "entropy_score"])
        writer.writeheader()
        for row in bloom_summaries:
            writer.writerow(row)

    print(f"[EntropyTracker] 📄 Exported bloom entropy summary → {csv_path}")

def print_lineage_entropy_stats():
    """
    Print stats for each lineage level: avg, min, max, stddev.
    """
    import statistics

    lineage_agg, _ = aggregate_entropy_per_lineage()

    print("🧬 Lineage Entropy Stats:")
    for depth in sorted(lineage_agg.keys()):
        scores = lineage_agg[depth]
        avg = round(statistics.mean(scores), 4)
        std = round(statistics.stdev(scores), 4) if len(scores) > 1 else 0.0
        print(f" - Depth {depth:2d}: avg={avg} | std={std} | min={min(scores):.2f} | max={max(scores):.2f}")

if __name__ == "__main__":
    export_entropy_summary()
    print_lineage_entropy_stats()
