# interval_animation.py
import csv
import matplotlib.pyplot as plt

def animate_tick_dynamics(csv_path="juliet_flowers/cluster_report/rebloom_tick_log.csv"):
    ticks, bloom_ct, heat_vals, zones = [], [], [], []
    
    ticks, bloom_ct, heat_vals, zones, scup_vals = [], [], [], [], []

    with open(csv_path, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            ticks.append(int(row[0]))
            bloom_ct.append(int(row[1]))
            heat_vals.append(float(row[2]))
            zones.append(row[3])
            scup_vals.append(float(row[4]))


    fig, ax1 = plt.subplots(figsize=(12, 6))
    zone_colors = {"🟢 calm": "green", "🟡 active": "gold", "🔴 surge": "red"}
    zone_plot = [zone_colors.get(z, "gray") for z in zones]

    scatter = ax1.scatter(ticks, heat_vals, c=zone_plot, label="Pulse Heat", s=50)
    ax1.plot(ticks, heat_vals, alpha=0.3, linewidth=1)
    ax1.set_xlabel("Tick")
    ax1.set_ylabel("Pulse Heat")
    ax1.grid(True)

    # SCUP on twin y-axis
    ax2 = ax1.twinx()
    ax2.plot(ticks, scup_vals, color="blue", linewidth=2, linestyle="--", label="SCUP")
    ax2.set_ylabel("SCUP", color="blue")
    ax2.tick_params(axis='y', labelcolor="blue")

    plt.title("🎞️ Pulse Heat & SCUP Overlay Over Time")
    fig.tight_layout()
    plt.savefig("juliet_flowers/cluster_report/tick_heat_scup_overlay.png")
    print("📈 Saved: tick_heat_scup_overlay.png")

if __name__ == "__main__":
    animate_tick_dynamics()
