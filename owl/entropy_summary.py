import os
import json

def summarize_entropy(log_dir="juliet_flowers/cluster_report", lineage_path="juliet_flowers/index/lineage_map.json"):
    drift_map = {}
    for fname in os.listdir(log_dir):
        if fname.startswith("vector_drift_") and fname.endswith(".log"):
            bloom_id = fname.replace("vector_drift_", "").replace(".log", "")
            seed = bloom_id.split("_")[0]
            with open(os.path.join(log_dir, fname), encoding="utf-8") as f:
                for line in f:
                    if "Drift Score" in line:
                        drift = float(line.strip().split(": ")[-1])
                        drift_map.setdefault(seed, []).append(drift)

    avg_drift_per_seed = {seed: sum(scores)/len(scores) for seed, scores in drift_map.items() if scores}

    if os.path.exists(lineage_path):
        with open(lineage_path, "r", encoding="utf-8") as f:
            lineage = json.load(f)
    else:
        lineage = {}

    lineage["drift_entropy_summary"] = avg_drift_per_seed

    with open(lineage_path, "w", encoding="utf-8") as f:
        json.dump(lineage, f, indent=2)

    print(f"[Entropy Summary] Drift scores updated in {lineage_path}")
