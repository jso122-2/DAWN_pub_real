import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict

PRESSURE_DIR = "juliet_flowers/cluster_report"
BLOOM_DIR = "juliet_flowers/bloom_metadata"
NUTRIENT = "attention"
OUT = f"{PRESSURE_DIR}/nutrient_belief_overlay_{NUTRIENT}.png"

def load_belief_map():
    belief_map = {}
    for f in os.listdir(BLOOM_DIR):
        if not f.endswith(".json"):
            continue
        with open(os.path.join(BLOOM_DIR, f)) as fp:
            data = json.load(fp)
            belief = data.get("belief_resonance", {}).get("belief", "unknown")
            seed_id = data.get("seed_id")
            if seed_id:
                belief_map[seed_id] = belief
    return belief_map

def load_latest_pressure():
    files = [f for f in os.listdir(PRESSURE_DIR) if f.startswith("nutrient_pressure_tick") and f.endswith(".json")]
    if not files:
        print("❌ No pressure snapshots found.")
        return {}
    latest = sorted(files)[-1]
    with open(os.path.join(PRESSURE_DIR, latest)) as f:
        return json.load(f), latest

def generate_overlay():
    belief_map = load_belief_map()
    pressure_data, timestamp = load_latest_pressure()
    if not pressure_data:
        return

    aggregate = defaultdict(list)
    for seed, nutrients in pressure_data.items():
        belief = belief_map.get(seed, "unknown")
        val = nutrients.get(NUTRIENT)
        if val is not None:
            aggregate[belief].append(val)

    beliefs, averages = [], []
    for belief, values in aggregate.items():
        beliefs.append(belief)
        averages.append(round(sum(values) / len(values), 3))

    plt.figure(figsize=(10, 5))
    plt.bar(beliefs, averages, color="teal")
    plt.title(f"🧬 {NUTRIENT.title()} Level by Belief Zone – {timestamp}")
    plt.ylabel(f"{NUTRIENT} level (avg)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    plt.savefig(OUT)
    plt.close()
    print(f"✅ Belief-nutrient overlay saved → {OUT}")

if __name__ == "__main__":
    generate_overlay()
