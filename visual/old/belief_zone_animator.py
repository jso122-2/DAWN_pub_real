import os
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

BLOOM_DIR = "juliet_flowers/bloom_metadata"
OUT = "juliet_flowers/cluster_report/belief_zone_emergence.gif"

def load_bloom_frames():
    frames = []
    for file in sorted(os.listdir(BLOOM_DIR)):
        if not file.endswith(".json"):
            continue
        with open(os.path.join(BLOOM_DIR, file)) as f:
            bloom = json.load(f)
            belief = bloom.get("belief_resonance", {}).get("belief", "unknown")
            depth = bloom.get("lineage_depth", 0)
            frames.append((depth, belief))
    return frames

def animate_belief_zones():
    frames = load_bloom_frames()
    if not frames:
        print("❌ No belief resonance data found.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    all_beliefs = sorted(set(b for _, b in frames))
    belief_to_y = {b: i for i, b in enumerate(all_beliefs)}

    x_data, y_data = [], []

    def update(frame_idx):
        ax.clear()
        current = frames[:frame_idx+1]
        x_data = [depth for depth, _ in current]
        y_data = [belief_to_y[belief] for _, belief in current]

        ax.scatter(x_data, y_data, c="black", s=80)
        ax.set_yticks(range(len(all_beliefs)))
        ax.set_yticklabels(all_beliefs)
        ax.set_xlabel("Lineage Depth")
        ax.set_title(f"🎥 Belief Zone Emergence – {frame_idx+1}/{len(frames)}")
        ax.grid(True)

    ani = FuncAnimation(fig, update, frames=len(frames), interval=400, repeat=False)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    ani.save(OUT, writer="pillow")
    plt.close()
    print(f"✅ Saved animation → {OUT}")

if __name__ == "__main__":
    animate_belief_zones()
