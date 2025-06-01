# drift_entropy_overlay.py
import csv
import matplotlib.pyplot as plt
import numpy as np

def polar_to_xy(angle_rad, magnitude):
    return magnitude * np.cos(angle_rad), magnitude * np.sin(angle_rad)

def plot_drift_and_entropy(csv_path="juliet_flowers/cluster_report/drift_compass_log.csv"):
    ticks, angles, mags, entropy_vals = [], [], [], []
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.reader(f):
            tick, angle, mag, entropy = int(row[0]), float(row[1]), float(row[2]), float(row[3])
            ticks.append(tick)
            angles.append(angle)
            mags.append(mag)
            entropy_vals.append(entropy)

    X = np.array(ticks)
    Y = np.zeros_like(X)
    U, V = [], []

    for a, m in zip(angles, mags):
        dx, dy = polar_to_xy(a, m)
        U.append(dx)
        V.append(dy)

    fig, ax1 = plt.subplots(figsize=(14, 5))

    # 🧭 Drift Vectors
    quiv = ax1.quiver(X, Y, U, V, angles, scale=1, scale_units='xy', angles='xy', cmap="twilight_shifted")
    ax1.set_ylabel("Drift Direction (vector)")
    ax1.set_yticks([])
    ax1.set_xlabel("Tick")
    ax1.set_title("🌪️ Drift & Entropy Stormmap")

    # 🧬 Entropy Overlay
    ax2 = ax1.twinx()
    ax2.plot(ticks, entropy_vals, color="black", alpha=0.5, linewidth=2, linestyle="--", label="Entropy")
    ax2.set_ylabel("Entropy", color="black")
    ax2.tick_params(axis='y', labelcolor="black")

    plt.grid(True, axis='x')
    plt.tight_layout()
    plt.savefig("juliet_flowers/cluster_report/drift_entropy_stormmap.png")
    print("🌪️ Saved: drift_entropy_stormmap.png")

if __name__ == "__main__":
    plot_drift_and_entropy()
