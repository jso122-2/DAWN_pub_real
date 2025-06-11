import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("juliet_flowers/cluster_report/zone_overlay_log.csv", names=["tick", "zone", "pulse"])
colors = {"🟢 calm": "green", "🟡 active": "gold", "🔴 surge": "red"}
df["color"] = df["zone"].map(colors)

plt.figure(figsize=(12, 3))
plt.scatter(df["tick"], df["pulse"], c=df["color"], s=80, marker='|')
plt.title("Pulse Zones Over Time")
plt.xlabel("Tick")
plt.ylabel("Pulse")
plt.tight_layout()
plt.savefig("juliet_flowers/cluster_report/pulse_zone_overlay.png")
