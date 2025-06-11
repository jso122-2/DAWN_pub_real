import os
import json
import csv

BLOOM_DIR = "juliet_flowers/bloom_metadata"
OUT = "juliet_flowers/cluster_report/resonance_matrix.csv"

def archive_resonance_matrix():
    with open(OUT, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["seed_id", "lineage_depth", "mood", "belief", "resonance_distance", "rgb_r", "rgb_g", "rgb_b"])

        for file in os.listdir(BLOOM_DIR):
            if not file.endswith(".json"):
                continue
            with open(os.path.join(BLOOM_DIR, file)) as j:
                data = json.load(j)
                belief = data.get("belief_resonance", {})
                rgb = belief.get("rgb", (0, 0, 0))
                writer.writerow([
                    data.get("seed_id", "unknown"),
                    data.get("lineage_depth", 0),
                    data.get("mood", "neutral"),
                    belief.get("belief", "unknown"),
                    belief.get("distance", 0.0),
                    rgb[0], rgb[1], rgb[2]
                ])
    print(f"✅ Resonance matrix archived to: {OUT}")

if __name__ == "__main__":
    archive_resonance_matrix()
