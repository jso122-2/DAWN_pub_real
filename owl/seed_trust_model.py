import json
import os

def compute_seed_trust(drift_log_dir, lineage_path):
    drift_map = {}
    for fname in os.listdir(drift_log_dir):
        if fname.startswith("vector_drift_") and fname.endswith(".log"):
            seed = fname.split("_")[2]  # assumes seed is third token
            with open(os.path.join(drift_log_dir, fname), encoding="utf-8") as f:
                for line in f:
                    if "Drift Score" in line:
                        score = float(line.strip().split(": ")[-1])
                        drift_map.setdefault(seed, []).append(score)

    trust_scores = {}
    for seed, scores in drift_map.items():
        if scores:
            avg_drift = sum(scores) / len(scores)
            trust = max(0.0, 1.0 - avg_drift)
            trust_scores[seed] = round(trust, 4)

    with open(lineage_path, "r", encoding="utf-8") as f:
        lineage = json.load(f)

    lineage["seed_trust"] = trust_scores

    with open(lineage_path, "w", encoding="utf-8") as f:
        json.dump(lineage, f, indent=2)

    print(f"[Trust Model] Seed trust values injected into lineage_map.json.")
