import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import numpy as np

SCUP_LOG = "visual/outputs/scup_zone_animator/scup_bloom_correlation.csv"
ZONE_LOG = "visual/outputs/scup_zone_animator/zone_overlay_log.csv"
OUT = "visual/outputs/scup_zone_animator/scup_zone_overlay.gif"

ZONE_LABELS = {"calm": "green", "active": "gold", "surge": "red"}
ZONE_NAMES = ["calm", "active", "surge"]

# Generate synthetic logs with ASCII zone names

def generate_synthetic_logs():
    timestamps = pd.date_range(start="2025-06-01", periods=50, freq="min")
    scup = np.clip(np.cumsum(np.random.randn(50) * 0.05 + 0.5), 0, 1)
    scup_df = pd.DataFrame({"timestamp": timestamps, "scup": scup})
    scup_df.to_csv(SCUP_LOG, index=False)
    zones = np.random.choice(ZONE_NAMES, size=50, p=[0.6, 0.3, 0.1])
    heat = np.clip(np.random.rand(50), 0, 1)
    zone_df = pd.DataFrame({"tick": range(50), "zone": zones, "heat": heat})
    zone_df.to_csv(ZONE_LOG, index=False, header=False)

def map_zone_to_level(z):
    return {"calm": 0, "active": 1, "surge": 2}.get(z, 1)

def animate_scup_zone():
    if not os.path.exists(SCUP_LOG) or not os.path.exists(ZONE_LOG):
        print("⚠️ Missing SCUP or Zone log, generating synthetic data...")
        generate_synthetic_logs()
    scup_df = pd.read_csv(SCUP_LOG, parse_dates=["timestamp"])
    zone_df = pd.read_csv(ZONE_LOG, names=["tick", "zone", "heat"])
    zone_df["level"] = zone_df["zone"].apply(map_zone_to_level)
    fig, ax = plt.subplots(figsize=(10, 5))
    def update(i):
        ax.clear()
        scup_slice = scup_df.iloc[:i+1]
        zone_slice = zone_df.iloc[:i+1]
        ax.plot(scup_slice["timestamp"], scup_slice["scup"], color="black", linewidth=2, label="SCUP")
        zone = zone_slice["zone"].iloc[-1]
        ax.fill_between(scup_slice["timestamp"], 0, 1.5, color=ZONE_LABELS.get(zone, "gray"), alpha=0.2, label=zone)
        ax.set_ylim(0, 1.2)
        ax.set_title(f"SCUP + Zone Overlay – Frame {i+1} [{zone.upper()}]")
        ax.set_ylabel("SCUP")
        ax.legend()
    ani = FuncAnimation(fig, update, frames=min(len(scup_df), len(zone_df)), interval=400, repeat=False)
    ani.save(OUT, writer="pillow")
    plt.close()
    print(f"✅ SCUP + Zone animation saved → {OUT}")
    return OUT

def main(*args, **kwargs):
    output_dir = "visual/outputs/scup_zone_animator"
    os.makedirs(output_dir, exist_ok=True)
    output_path = animate_scup_zone()
    print(f"✅ Saved SCUP zone animation to {output_path}")

if __name__ == "__main__":
    main()
