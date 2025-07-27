
import os
import json

BLOOM_DIR = "juliet_flowers/bloom_metadata"
EXPORT_PATH = "juliet_flowers/cluster_report/full_lineage_export.json"

def export_lineage_json():
    lineage = []
    for fname in sorted(os.listdir(BLOOM_DIR)):
        if fname.endswith(".json"):
            with open(os.path.join(BLOOM_DIR, fname), "r") as f:
                lineage.append(json.load(f))

    with open(EXPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(lineage, f, indent=2)

    print(f"[Export] 📁 Full lineage exported to → {EXPORT_PATH}")
