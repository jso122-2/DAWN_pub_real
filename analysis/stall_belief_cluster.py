import os
import json
from tracers.whale import nearest_belief, PIGMENTS

BLOOM_DIR = "juliet_flowers/bloom_metadata"
STALL_LOG = "owl/logs/crow_stall_log.json"
OUT = "juliet_flowers/cluster_report/stall_belief_clusters.json"

def cluster_by_belief():
    if not os.path.exists(STALL_LOG):
        print("❌ No stall log.")
        return

    with open(STALL_LOG, "r") as f:
        stalls = json.load(f)

    mood_colors = {
        "joyful": (255, 215, 0),
        "anxious": (255, 69, 0),
        "reflective": (70, 130, 180),
        "focused": (34, 139, 34),
        "sad": (105, 105, 105),
        "curious": (255, 140, 0),
        "overload": (255, 0, 255)
    }

    clusters = {}

    for file in os.listdir(BLOOM_DIR):
        if not file.endswith(".json"):
            continue
        with open(os.path.join(BLOOM_DIR, file)) as f:
            data = json.load(f)
            zone = data.get("seed_context", ["?"])[-1]
            if zone not in stalls:
                continue

            mood = data.get("mood", "reflective")
            rgb = mood_colors.get(mood, (180, 180, 180))
            belief = nearest_belief(rgb)
            clusters.setdefault(belief, []).append(zone)

    with open(OUT, "w") as f:
        json.dump(clusters, f, indent=2)

    print(f"✅ Belief cluster map saved: {OUT}")

if __name__ == "__main__":
    cluster_by_belief()
