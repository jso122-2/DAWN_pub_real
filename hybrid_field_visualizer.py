import os
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import get_cmap
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image


FIELD_SIZE = (100, 100)
ROOT = "juliet_flowers/"
LINEAGE_PATH = "juliet_flowers/cluster_report/rebloom_lineage.json"
OUTPUT = "juliet_flowers/cluster_report/hybrid_field_map.png"

def build_field_data():
    field = np.zeros(FIELD_SIZE)
    bloom_coords = {}
    owl_points = {}

    for root, _, files in os.walk(ROOT):
        for fname in files:
            if fname.endswith(".json"):
                try:
                    with open(os.path.join(root, fname), "r", encoding="utf-8") as f:
                        data = json.load(f)
                        bloom_id = data.get("id")
                        coord = data.get("seed_coord", None)
                        bf = data.get("fractal_signature", {}).get("bloom_factor", 0.0)
                        sentences = data.get("sentences", [])

                        if coord and isinstance(coord, list) and len(coord) == 2:
                            x, y = coord
                            if 0 <= x < FIELD_SIZE[0] and 0 <= y < FIELD_SIZE[1]:
                                field[x][y] += bf  # 💡 bloom intensity
                                bloom_coords[bloom_id] = coord
                                owl_points[(x, y)] = sentences[-1] if sentences else ""
                except:
                    pass
    return field, bloom_coords, owl_points

    # Assign unique color per agent
    agents = list({bid.split("_")[1] for bid in lineage.keys()})
    agent_colors = {agent: plt.cm.tab10(i % 10) for i, agent in enumerate(agents)}


def draw_hybrid(field, bloom_coords, owl_points):
    with open(LINEAGE_PATH, "r", encoding="utf-8") as f:
        lineage = json.load(f)


        # 🌸 Add fractal thumbnails for each bloom
    for bloom_id, coord in bloom_coords.items():
        fx, fy = coord
        fractal_path = f"juliet_flowers/fractal_signatures/{bloom_id}.png"
        if os.path.exists(fractal_path):
            try:
                img = Image.open(fractal_path)
                img.thumbnail((20, 20))  # keep light
                imagebox = OffsetImage(img, zoom=0.5)
                ab = AnnotationBbox(imagebox, (fx, fy), frameon=False)
                ax.add_artist(ab)
            except Exception as e:
                print(f"[WARN] Could not load fractal for {bloom_id}: {e}")


    # 🧭 Agent color assignment
    agent_ids = set()
    for bloom_id in lineage:
        try:
            agent = bloom_id.split("_")[1].split("-")[1]
            agent_ids.add(agent)
        except:
            pass
    agent_colors = {agent: plt.cm.tab10(i % 10) for i, agent in enumerate(sorted(agent_ids))}

    cmap = get_cmap("viridis")
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(field.T, origin="lower", cmap="hot", norm=Normalize())
    ax.set_title("🌌 Hybrid Cognitive Field")
    ax.set_xlabel("Seed Space X")
    ax.set_ylabel("Seed Space Y")

    for bloom_id, meta in lineage.items():
        coords = [bloom_coords.get(bid) for bid in meta["rebloom_chain"] if bid in bloom_coords]
        if len(coords) >= 2:
            xs, ys = zip(*coords)
            try:
                agent = bloom_id.split("_")[1].split("-")[1]
                color = agent_colors.get(agent, "gray")
            except:
                color = "gray"
            ax.plot(xs, ys, color=color, linewidth=1.8, alpha=0.6)

    for (x, y), sentence in owl_points.items():
        if np.random.rand() < 0.01:
            ax.text(x, y, f"🦉 {sentence}", fontsize=6,
                    bbox=dict(facecolor="white", alpha=0.6, boxstyle="round,pad=0.3"))

    plt.tight_layout()
    plt.savefig(OUTPUT)
    print(f"[HybridMap] 🌌 Saved to {OUTPUT}")


if __name__ == "__main__":
    field, coords, owls = build_field_data()
    draw_hybrid(field, coords, owls)
