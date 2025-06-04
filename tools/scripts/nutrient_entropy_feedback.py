
import os
import json

BLOOM_DIR = "juliet_flowers/bloom_metadata"
LOG_PATH = "mycelium_logs/nutrient_log.json"

def nutrient_entropy_feedback():
    if not os.path.exists(LOG_PATH):
        print("[Feedback] ❌ No nutrient log found.")
        return

    with open(LOG_PATH, "r") as f:
        nutrient_data = json.load(f)

    # Auto-scale entropy by nutrient depth (simulated feedback)
    for fname in os.listdir(BLOOM_DIR):
        if fname.endswith(".json"):
            path = os.path.join(BLOOM_DIR, fname)
            with open(path, "r") as f:
                bloom = json.load(f)

            depth = str(bloom.get("lineage_depth", 0))
            count = nutrient_data.get(depth, 0)
            new_entropy = min(1.0, bloom.get("entropy_score", 0.0) + count * 0.01)
            bloom["entropy_score"] = new_entropy

            with open(path, "w") as f:
                json.dump(bloom, f, indent=2)

    print("[Feedback] 🔁 Entropy adjusted by nutrient depth.")
