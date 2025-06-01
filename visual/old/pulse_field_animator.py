# /visuals/pulse_field_animator.py

"""
Pulse Field Animator:
🌐 Animates entropy and zone transitions across ticks.
Reads from: juliet_flowers/cluster_report/zone_overlay_log.csv
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Config ---
LOG_PATH = "juliet_flowers/cluster_report/zone_overlay_log.csv"
OUT_PATH = "visuals/pulse_field_animation.gif"

ZONE_COLORS = {
    "🟢 calm": "green",
    "🟡 active": "gold",
    "🔴 surge": "red"
}

def animate_pulse_field():
    if not os.path.exists(LOG_PATH):
        print("[PulseField] ❌ zone_overlay_log.csv not found.")
        return

    df = pd.read_csv(LOG_PATH, names=["tick", "zone", "pulse"])

    ticks = df["tick"].values
    entropy = df["pulse"].values  # using 'pulse' as proxy for entropy curve here
    zones = df["zone"].values

    fig, ax = plt.subplots(figsize=(10, 6))
    entropy_line, = ax.plot([], [], lw=2, color="purple", label="Entropy (Pulse)")
    zone_marker = ax.scatter([], [], s=200, c=[], marker='o', label="Zone")

    ax.set_xlim(min(ticks), max(ticks))
    ax.set_ylim(0, max(entropy) + 0.5)
    ax.set_title("🌐 Pulse Field Evolution")
    ax.set_xlabel("Tick")
    ax.set_ylabel("Entropy / Pulse")
    ax.legend()

    def update(i):
        current_ticks = ticks[:i + 1]
        current_entropy = entropy[:i + 1]
        current_zone = zones[i]

        entropy_line.set_data(current_ticks, current_entropy)
        zone_marker.set_offsets([[ticks[i], entropy[i]]])
        zone_marker.set_color(ZONE_COLORS.get(current_zone, "gray"))
        ax.set_title(f"🌐 Tick {ticks[i]} | Zone: {current_zone}")

        return entropy_line, zone_marker

    ani = animation.FuncAnimation(fig, update, frames=len(ticks), interval=500, repeat=False)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    ani.save(OUT_PATH, writer="pillow")
    print(f"[PulseField] ✅ Pulse field animation saved → {OUT_PATH}")

# CLI trigger
if __name__ == "__main__":
    animate_pulse_field()
