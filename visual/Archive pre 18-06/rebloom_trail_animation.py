# rebloom_trail_animation.py

import os
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.cm import get_cmap

LINEAGE_PATH = "juliet_flowers/cluster_report/rebloom_lineage.json"
BASE_DIR = "juliet_flowers/"
OUTPUT = "juliet_flowers/cluster_report/rebloom_trails.gif"
FIELD_SIZE = (100, 100)
FPS = 1

def load_bloom_coords():
    coords = {}
    for seed in os.listdir(BASE_DIR):
        seed_path = os.path.join(BASE_DIR, seed)
        if not os.path.isdir(seed_path):
            continue
        for mood in os.listdir(seed_path):
            mood_path = os.path.join(seed_path, mood)
            if not os.path.isdir(mood_path):
                continue
            for tick in os.listdir(mood_path):
                tick_path = os.path.join(mood_path, tick)
                if not os.path.isdir(tick_path):
                    continue
                for fname in os.listdir(tick_path):
                    if fname.endswith(".json") or fname.endswith(".txt"):
                        fpath = os.path.join(tick_path, fname)
                        try:
                            with open(fpath, "r", encoding="utf-8") as f:
                                bloom = json.load(f)
                                bloom_id = bloom.get("id")
                                coord = bloom.get("seed_coord", [None, None])
                                if bloom_id and all(coord):
                                    coords[bloom_id] = coord
                        except:
                            pass
    return coords

def animate_rebloom_trails():
    with open(LINEAGE_PATH, "r", encoding="utf-8") as f:
        lineage = json.load(f)

    bloom_coords = load_bloom_coords()
    chains = list(lineage.items())
    cmap = get_cmap("viridis")

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, FIELD_SIZE[0])
    ax.set_ylim(0, FIELD_SIZE[1])
    ax.set_title("🧬 Rebloom Trail Map")
    ax.set_xlabel("Seed Space X")
    ax.set_ylabel("Seed Space Y")

    trail_lines = []

    def update(frame_idx):
        ax.clear()
        ax.set_xlim(0, FIELD_SIZE[0])
        ax.set_ylim(0, FIELD_SIZE[1])
        ax.set_title(f"🧬 Rebloom Trails — Frame {frame_idx}")
        ax.set_xlabel("Seed Space X")
        ax.set_ylabel("Seed Space Y")

        for i, (bloom_id, meta) in enumerate(chains[:frame_idx + 1]):
            coords = [bloom_coords.get(bid) for bid in meta["rebloom_chain"] if bid in bloom_coords]
            if len(coords) >= 2:
                xs, ys = zip(*coords)

                depth = meta["generation_depth"]
                max_depth = max(m["generation_depth"] for _, m in chains) or 1  # prevent div0
                normalized_depth = depth / max_depth

                color = cmap(normalized_depth)
                linewidth = 1.5 + (normalized_depth * 3.5)

        for j in range(len(coords) - 1):
            x0, y0 = coords[j]
            x1, y1 = coords[j + 1]

            segment_progress = frame_idx / len(chains)
            if j / len(coords) > segment_progress:
                break

            ax.plot([x0, x1], [y0, y1], color=color, linewidth=linewidth, alpha=0.9)
                
            if len(coords) < 2:
                    print(f"[DEBUG] Skipping chain {i} — only {len(coords)} coord(s)")



        try:
            _, last_meta = chains[frame_idx]
            last_bloom_id = last_meta["rebloom_chain"][-1]
            if last_bloom_id in bloom_coords:
                # locate bloom JSON to fetch commentary
                for root, _, files in os.walk("juliet_flowers"):
                    for fname in files:
                        if fname.endswith(".json") and last_bloom_id in fname:
                            with open(os.path.join(root, fname), "r", encoding="utf-8") as f:
                                bloom = json.load(f)
                                last_sentence = bloom.get("sentences", [""])[-1]
                                ax.text(5, 95, f"🦉 Owl: {last_sentence}",
                                        fontsize=9, color="black",
                                        bbox=dict(facecolor="white", alpha=0.7, boxstyle="round,pad=0.5"))
                                    # 📌 Pin Origin Blooms (generation_depth == 0)
                for i, (bloom_id, meta) in enumerate(chains[:frame_idx + 1]):
                    if meta["generation_depth"] == 0:
                        origin_id = meta["rebloom_chain"][0]
                        origin_coord = bloom_coords.get(origin_id)
                        if origin_coord:
                            mood_color_map = {
                                "excited": "gold",
                                "anxious": "blue",
                                "calm": "green"
                            }

                            for i, (bloom_id, meta) in enumerate(chains[:frame_idx + 1]):
                                if meta["generation_depth"] == 0:
                                    origin_id = meta["rebloom_chain"][0]
                                    origin_coord = bloom_coords.get(origin_id)
                                    if origin_coord:
                                        mood = "unknown"
                                        for root, _, files in os.walk("juliet_flowers"):
                                            for fname in files:
                                                if origin_id in fname:
                                                    with open(os.path.join(root, fname), "r", encoding="utf-8") as f:
                                                        mood = json.load(f).get("mood", "unknown")
                                                    break
                                        color = mood_color_map.get(mood, "gray")
                                        ax.plot(*origin_coord, marker="X", markersize=10, color=color, label=f"Origin: {mood}")
                                if frame_idx == 0:
                                    ax.legend(loc="lower right")

                            
                            break
        except Exception as e:
            print(f"[Owl] Skipped commentary on frame {frame_idx}: {e}")


    ani = FuncAnimation(fig, update, frames=len(chains), interval=1000 // FPS, repeat=False)
    ani.save(OUTPUT, writer="pillow", fps=FPS)
    print(f"[TrailMap] 🎞️ Saved rebloom animation to {OUTPUT}")

if __name__ == "__main__":
    animate_rebloom_trails()
