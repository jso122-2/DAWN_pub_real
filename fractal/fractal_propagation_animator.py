import os
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

ROOT = "juliet_flowers/"
FRACTAL_DIR = "juliet_flowers/fractal_signatures/"
OUTPUT = "juliet_flowers/cluster_report/fractal_growth.gif"
FIELD_SIZE = (100, 100)
FPS = 2

# Build frames by tick index
def load_blooms_by_tick():
    tick_map = {}
    for seed in os.listdir(ROOT):
        seed_path = os.path.join(ROOT, seed)
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
                try:
                    tick_idx = int(tick)
                except:
                    continue
                for fname in os.listdir(tick_path):
                    if fname.endswith(".json") and "flower" in fname:
                        full_path = os.path.join(tick_path, fname)
                        with open(full_path, "r", encoding="utf-8") as f:
                            bloom = json.load(f)
                            bloom_id = bloom["id"]
                            coord = bloom.get("seed_coord", None)
                            if coord:
                                tick_map.setdefault(tick_idx, []).append((coord, bloom_id))
    return tick_map

def animate_blooms(tick_blooms):
    ticks = sorted(tick_blooms.keys())
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, FIELD_SIZE[0])
    ax.set_ylim(0, FIELD_SIZE[1])
    ax.set_title("🌸 Fractal Bloom Growth")
    ax.set_xlabel("Seed Space X")
    ax.set_ylabel("Seed Space Y")

    def update(frame):
        ax.clear()
        ax.set_xlim(0, FIELD_SIZE[0])
        ax.set_ylim(0, FIELD_SIZE[1])
        ax.set_title(f"🌸 Fractal Growth — Tick {ticks[frame]}")
        ax.set_xlabel("Seed Space X")
        ax.set_ylabel("Seed Space Y")

        for f in ticks[:frame + 1]:
            for (x, y), bloom_id in tick_blooms[f]:
                path = os.path.join(FRACTAL_DIR, f"{bloom_id}.png")
                if os.path.exists(path):
                    try:
                        img = Image.open(path)
                        img.thumbnail((22, 22))
                        imagebox = OffsetImage(img, zoom=0.4)
                        ab = AnnotationBbox(imagebox, (x, y), frameon=False)
                        ax.add_artist(ab)
                    except:
                        pass

    ani = FuncAnimation(fig, update, frames=len(ticks), interval=1000 // FPS)
    ani.save(OUTPUT, writer="pillow", fps=FPS)
    print(f"[FractalGrowth] 🎞️ Saved to {OUTPUT}")

if __name__ == "__main__":
    bloom_map = load_blooms_by_tick()
    animate_blooms(bloom_map)
