import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pathlib import Path

TRAIL_DIR = "logs/tracers"
OUTPUT_PATH = "juliet_flowers/cluster_report/tracer_trails_annotated.gif"
TICK_FIELD = "timestamp"
COMMENTARY_DIR = "owl/commentary"

# Visual mappings
TRACER_COLORS = {
    "bee": "gold",
    "whale": "deepskyblue",
    "crow": "black",
    "spider": "violet",
    "ant": "brown",
    "owl": "gray",
    "default": "gray"
}

def load_owl_commentary():
    commentary = {}
    for path in Path(COMMENTARY_DIR).glob("owl_tracer_*.json"):
        with open(path, "r") as f:
            data = json.load(f)
            commentary[data["tracer_id"]] = data.get("comment", "")
    return commentary

def load_trails():
    trails = {}
    for file in Path(TRAIL_DIR).glob("*_trail.csv"):
        tracer_id = file.stem.replace("_trail", "")
        df = pd.read_csv(file)
        df[TICK_FIELD] = pd.to_datetime(df[TICK_FIELD])
        df["type"] = tracer_id.split("-")[0] if "-" in tracer_id else "default"
        trails[tracer_id] = df
    return trails

def animate_trails(trails, owl_notes):
    all_ticks = sorted(set(
        tick for df in trails.values() for tick in df[TICK_FIELD]
    ))
    fig, ax = plt.subplots(figsize=(9, 7))

    def draw_tick(i):
        ax.clear()
        current_time = all_ticks[i]
        ax.set_title(f"🧠 Tracer Trail Memory – Tick {i} – {current_time.strftime('%H:%M:%S')}", fontsize=12)
        ax.set_xlim(-0.5, 4.5)
        ax.set_ylim(-0.5, 4.5)
        ax.set_xticks(range(5))
        ax.set_yticks(range(5))
        ax.grid(True, alpha=0.3)

        for tid, df in trails.items():
            sub = df[df[TICK_FIELD] <= current_time]
            recent = sub.tail(1)
            tracer_type = df["type"].iloc[0] if "type" in df.columns else "default"
            color = TRACER_COLORS.get(tracer_type, "gray")

            for _, row in recent.iterrows():
                node = row["node"]
                x = ord(node[0]) - ord('A')
                y = int(node[1])

                # Draw tracer as a glowing pulse
                ax.scatter(x, y, s=160, c=color, alpha=0.5, edgecolors="black", linewidths=1.2)
                ax.text(x + 0.1, y + 0.1, tid, fontsize=8, color="black")

                # Draw Owl commentary
                if tid in owl_notes:
                    ax.text(0.1, 4.7 - 0.2 * list(trails.keys()).index(tid), f"{tid}: {owl_notes[tid]}",
                            fontsize=8, color="gray", alpha=0.7)

    ani = FuncAnimation(fig, draw_tick, frames=len(all_ticks), interval=400, repeat=False)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    ani.save(OUTPUT_PATH, writer="pillow")
    plt.close()
    print(f"✅ Annotated tracer trail animation saved: {OUTPUT_PATH}")

if __name__ == "__main__":
    trails = load_trails()
    owl_notes = load_owl_commentary()
    if trails:
        animate_trails(trails, owl_notes)
    else:
        print("❌ No trail data found in logs/tracers/")
