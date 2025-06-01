import os
import json
from collections import defaultdict

JULIET_DIR = "juliet_flowers"

def summarize_fields():
    summary = {}

    for folder in os.listdir(JULIET_DIR):
        path = os.path.join(JULIET_DIR, folder)
        if not os.path.isdir(path) or folder == "cluster_report":
            continue

        moods = set()
        agents = set()
        bloom_factors = []
        flower_ids = []

        for fname in os.listdir(path):
            if not fname.endswith(".json"):
                continue
            try:
                with open(os.path.join(path, fname), "r") as f:
                    flower = json.load(f)
                    agents.add(flower["agent"])
                    moods.add(flower["mood"])
                    bloom_factors.append(flower["fractal_signature"]["bloom_factor"])
                    flower_ids.append(flower["id"])
            except Exception as e:
                print(f"[Summary] ⚠️ Skipped {fname} in {folder}: {e}")

        if bloom_factors:
            summary[folder] = {
                "total": len(bloom_factors),
                "agents": sorted(agents),
                "moods": sorted(moods),
                "avg_bloom_factor": round(sum(bloom_factors) / len(bloom_factors), 3),
                "flowers": flower_ids
            }

    return summary
