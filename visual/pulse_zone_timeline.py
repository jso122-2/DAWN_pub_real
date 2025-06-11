import matplotlib.pyplot as plt
import pandas as pd
import os

LOG_PATH = "juliet_flowers/cluster_report/zone_overlay_log.csv"
OUT = "juliet_flowers/cluster_report/pulse_zone_timeline.png"

def map_zone_to_level(zone):
    return {"🟢 calm": 0, "🟡 active": 1, "🔴 surge": 2}.get(zone, 1)

def visualize_zone_timeline():
    if not os.path.exists(LOG_PATH):
        print("❌ Zone overlay log not found.")
        return

    df = pd.read_csv(LOG_PATH, names=["tick", "zone", "heat"])
    df["level"] = df["zone"].apply(map_zone_to_level)

    plt.figure(figsize=(12, 4))
    plt.plot(df["tick"], df["level"], drawstyle="steps-post", color="purple", linewidth=2)
    plt.yticks([0, 1, 2], ["🟢 calm", "🟡 active", "🔴 surge"])
    plt.xlabel("Tick")
    plt.title("📈 Pulse Zone Sequence Over Time")
    plt.grid(True, axis="y")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    plt.savefig(OUT)
    plt.close()
    print(f"✅ Pulse zone timeline saved → {OUT}")

if __name__ == "__main__":
    visualize_zone_timeline()
