import json
import os

def predict_rebirth_candidates(lineage_path, scup_threshold=1.0, trust_threshold=0.75):
    with open(lineage_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    trust_map = data.get("seed_trust", {})
    rebirth_candidates = []

    for seed, trust in trust_map.items():
        if trust >= trust_threshold:
            scup_sim = 1.0 + (trust * 0.2)
            if scup_sim >= scup_threshold:
                rebirth_candidates.append(seed)

    data["rebirth_candidates"] = rebirth_candidates

    with open(lineage_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[Rebirth] Candidates predicted: {rebirth_candidates}")
