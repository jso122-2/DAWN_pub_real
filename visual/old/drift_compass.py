# drift_compass.py
import csv
import matplotlib.pyplot as plt
import numpy as np

def polar_to_xy(angle_rad, magnitude):
    return magnitude * np.cos(angle_rad), magnitude * np.sin(angle_rad)

def draw_drift_compass(csv_path="juliet_flowers/cluster_report/drift_compass_log.csv"):
    ticks, angles, mags = [], [], []
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.reader(f):
            tick, angle, mag = int(row[0]), float(row[1]), float(row[2])
            ticks.append(tick)
            angles.append(angle)
            mags.append(mag)

    X = np.array(ticks)
    Y = np.zeros_like(X)
    U, V = [], []

    for a, m in zip(angles, mags):
        dx, dy = polar_to_xy(a, m)
        U.append(dx)
        V.append(dy)

    plt.figure(figsize=(12, 4))
    plt.quiver(X, Y, U, V, angles, scale=1, scale_units='xy', angles='xy', cmap="hsv")
    plt.yticks([])
    plt.xlabel("Tick")
    plt.title("🧭 Semantic Drift Compass")
    plt.tight_layout()
    plt.savefig("juliet_flowers/cluster_report/drift_compass.png")
    print("📍 Saved: drift_compass.png")

if __name__ == "__main__":
    draw_drift_compass()
