import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.animation import FuncAnimation

PRESSURE_DIR = "juliet_flowers/cluster_report"
BLOOM_DIR = "juliet_flowers/bloom_metadata"
NUTRIENT = "attention"
OUT = f"{PRESSURE_DIR}/nutrient_belief_{NUTRIENT}_animated.gif"

def load_belief_map():
    belief_map = {}
    for f in os.listdir(BLOOM_DIR):
        if f.endswith(".json"):
            with open(os.path.join(BLOOM_DIR, f)) as fp:
                data = json.load(fp)
                belief = data.get("belief_resonance", {}).get("belief", "unknown")
                seed_id = data.get("seed_id")
                if seed_id:
                    belief_map[seed_id] = belief
    return belief_map

def load_pressure_snapshots():
    frames = []
    for f in sorted(os.listdir(PRESSURE_DIR)):
        if f.startswith("nutrient_pressure_tick") and f.endswith(".json"):
            with open(os.path.join(PRESSURE_DIR, f)) as fp:
                data = json.load(fp)
                frames.append((f, data))
    return frames

def animate_overlay():
    belief_map = load_belief_map()
    frames = load_pressure_snapshots()
    if not frames:
        print("❌ No pressure snapshots.")
        return

    fig, ax = plt.subplots(figsize=(10, 5))

    def update(i):
        ax.clear()
        fname, pressure = frames[i]
        aggregate = defaultdict(list)
        for seed, nutrients in pressure.items():
            belief = belief_map.get(seed, "unknown")
            val = nutrients.get(NUTRIENT)
            if val is not None:
                aggregate[belief].append(val)

        beliefs, averages = [], []
        for belief, vals in aggregate.items():
            beliefs.append(belief)
            averages.append(sum(vals) / len(vals))

        ax.bar(beliefs, averages, color="teal")
        ax.set_title(f"🧬 {NUTRIENT.title()} by Belief – {fname}")
        ax.set_ylabel("Avg Pressure")
        ax.set_xticks(range(len(beliefs)))
        ax.set_xticklabels(beliefs, rotation=45)
        ax.set_ylim(0, 1.0)

    ani = FuncAnimation(fig, update, frames=len(frames), interval=500, repeat=False)
    ani.save(OUT, writer="pillow")
    plt.close()
    print(f"✅ Animated nutrient-belief overlay saved → {OUT}")

if __name__ == "__main__":
    animate_overlay()
