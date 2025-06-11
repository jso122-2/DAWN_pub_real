import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

SCUP_LOG = "juliet_flowers/scup_bloom_correlation.csv"
ZONE_LOG = "juliet_flowers/cluster_report/zone_overlay_log.csv"
OUT = "juliet_flowers/cluster_report/scup_zone_overlay.gif"

def map_zone_to_level(z):
    return {"🟢 calm": 0, "🟡 active": 1, "🔴 surge": 2}.get(z, 1)

def animate_scup_zone():
    if not os.path.exists(SCUP_LOG) or not os.path.exists(ZONE_LOG):
        print("❌ Missing SCUP or Zone log.")
        return

    scup_df = pd.read_csv(SCUP_LOG, parse_dates=["timestamp"])
    zone_df = pd.read_csv(ZONE_LOG, names=["tick", "zone", "heat"])
    zone_df["level"] = zone_df["zone"].apply(map_zone_to_level)

    fig, ax = plt.subplots(figsize=(10, 5))

    def update(i):
        ax.clear()
        scup_slice = scup_df.iloc[:i+1]
        zone_slice = zone_df.iloc[:i+1]

        ax.plot(scup_slice["timestamp"], scup_slice["scup"], color="black", linewidth=2, label="SCUP")
        ax.fill_between(scup_slice["timestamp"],
                        0,
                        1.5,
                        color=zone_color(zone_slice["zone"].iloc[-1]),
                        alpha=0.2,
                        label=zone_slice["zone"].iloc[-1])

        ax.set_ylim(0, 1.2)
        ax.set_title(f"🎥 SCUP + Zone Overlay – Frame {i+1}")
        ax.set_ylabel("SCUP")
        ax.legend()

    def zone_color(zone):
        return {
            "🟢 calm": "green",
            "🟡 active": "gold",
            "🔴 surge": "red"
        }.get(zone, "gray")

    ani = FuncAnimation(fig, update, frames=min(len(scup_df), len(zone_df)), interval=400, repeat=False)
    ani.save(OUT, writer="pillow")
    plt.close()
    print(f"✅ SCUP + Zone animation saved → {OUT}")

if __name__ == "__main__":
    animate_scup_zone()
