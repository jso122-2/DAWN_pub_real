# drift_entropy_animator.py
import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def polar_to_xy(angle_rad, magnitude):
    return magnitude * np.cos(angle_rad), magnitude * np.sin(angle_rad)

def load_data(path):
    ticks, angles, mags, entropy_vals = [], [], [], []
    with open(path, encoding="utf-8") as f:
        for row in csv.reader(f):
            tick, angle, mag, entropy = int(row[0]), float(row[1]), float(row[2]), float(row[3])
            ticks.append(tick)
            angles.append(angle)
            mags.append(mag)
            entropy_vals.append(entropy)
    return ticks, angles, mags, entropy_vals

def animate_stormmap(csv_path="juliet_flowers/cluster_report/drift_compass_log.csv"):
    ticks, angles, mags, entropy = load_data(csv_path)
    U, V = [], []
    for a, m in zip(angles, mags):
        dx, dy = polar_to_xy(a, m)
        U.append(dx)
        V.append(dy)

    fig, ax = plt.subplots(figsize=(12, 5))
    quiv = ax.quiver([], [], [], [], angles, scale=1, angles='xy', cmap="twilight_shifted")
    entropy_line, = ax.plot([], [], 'k--', alpha=0.4, lw=2)

    def init():
        ax.set_xlim(0, max(ticks) + 1)
        ax.set_ylim(-max(mags)*1.2, max(mags)*1.2)
        ax.set_title("🌪️ Drift-Entropy Stormmap Animation")
        return quiv, entropy_line

    def update(frame):
        ax.clear()
        ax.set_xlim(0, max(ticks))
        ax.set_ylim(-max(mags)*1.2, max(mags)*1.2)
        ax.set_xlabel("Tick")
        ax.set_yticks([])
        ax.set_title("🌪️ Drift-Entropy Stormmap Animation")

        sub_x = np.array(ticks[:frame])
        sub_U = np.array(U[:frame])
        sub_V = np.array(V[:frame])
        sub_C = np.array(angles[:frame])
        sub_entropy = entropy[:frame]

        ax.quiver(sub_x, np.zeros_like(sub_x), sub_U, sub_V, sub_C, scale=1, cmap="twilight_shifted")
        ax.plot(sub_x, sub_entropy, 'k--', alpha=0.6, lw=2)

        return ax,

    ani = FuncAnimation(fig, update, frames=len(ticks), init_func=init, blit=False, repeat=False)
    ani.save("juliet_flowers/cluster_report/stormmap.gif", writer="pillow", fps=3)
    print("🎥 Saved: stormmap.gif")

if __name__ == "__main__":
    animate_stormmap()
