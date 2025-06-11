import os
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

LOG_PATH = "owl/logs/crow_stall_log.json"
HISTORY_PATH = "owl/logs/crow_stall_history.json"
OUT = "juliet_flowers/cluster_report/stall_density_over_time.gif"

def load_stall_history():
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "r") as f:
            return json.load(f)
    return []

def save_stall_snapshot():
    if not os.path.exists(LOG_PATH):
        return
    with open(LOG_PATH, "r") as f:
        current = json.load(f)
    history = load_stall_history()
    history.append({"timestamp": datetime.now().isoformat(), "stalls": current})
    with open(HISTORY_PATH, "w") as f:
        json.dump(history[-100:], f, indent=2)  # keep last 100

def animate_history():
    history = load_stall_history()
    if not history:
        print("❌ No stall history to animate.")
        return

    fig, ax = plt.subplots(figsize=(6, 6))

    def to_coords(zone):
        return ord(zone[0]) - ord("A"), int(zone[1])

    def update(i):
        ax.clear()
        snap = history[i]["stalls"]
        xs, ys, sizes = [], [], []
        for zone, count in snap.items():
            x, y = to_coords(zone)
            xs.append(x)
            ys.append(y)
            sizes.append(count * 40)

        ax.scatter(xs, ys, s=sizes, color="red", alpha=0.7)
        ax.set_xticks(range(5))
        ax.set_yticks(range(5))
        ax.grid(True)
        ax.set_title(f"🎥 Stall Density — {history[i]['timestamp'][:19]}")
        ax.set_xlim(-0.5, 4.5)
        ax.set_ylim(-0.5, 4.5)

    ani = FuncAnimation(fig, update, frames=len(history), interval=400)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    ani.save(OUT, writer="pillow")
    plt.close()
    print(f"✅ Animated stall density saved → {OUT}")

if __name__ == "__main__":
    animate_history()
