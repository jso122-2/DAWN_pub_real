# animate_field_map.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize
from bloom.juliet_utils import load_bloom_metadata
from mood_drift import compute_mood_drift

SEED_PATH = "juliet_flowers/"
OUTPUT_PATH = "juliet_flowers/cluster_report/field_evolution.gif"
FIELD_SIZE = (100, 100)
TICKS = 50  # Adjust based on log data or max known ticks

def build_field_at_tick(tick):
    field = np.zeros(FIELD_SIZE)
    for seed in os.listdir(SEED_PATH):
        seed_path = os.path.join(SEED_PATH, seed)
        if not os.path.isdir(seed_path):
            continue

        for mood in os.listdir(seed_path):
            mood_path = os.path.join(seed_path, mood)
            if not os.path.isdir(mood_path):
                continue

            for t in os.listdir(mood_path):
                tick_path = os.path.join(mood_path, t)
                if t.isdigit() and os.path.isdir(tick_path) and int(t) == tick:
                    bloom_meta = load_bloom_metadata(tick_path)
                    for bloom in bloom_meta:
                        x, y = bloom.get("seed_coord", [0, 0])
                        pressure = bloom.get("semantic_pressure", 0.0)
                        drift = compute_mood_drift(bloom.get("mood"), bloom.get("mood_prev"))
                        field[x, y] += pressure * drift
    return field

def animate_field():
    fig, ax = plt.subplots(figsize=(10, 10))
    frame = ax.imshow(np.zeros(FIELD_SIZE), origin="lower", cmap="hot", norm=Normalize())
    plt.title("🔥 Field Pressure Evolution")
    plt.xlabel("Seed Space X")
    plt.ylabel("Seed Space Y")
    plt.tight_layout()

    print("\n[DEBUG] Scanning tick folders...")
    for seed in os.listdir(SEED_PATH):
        seed_path = os.path.join(SEED_PATH, seed)
        if not os.path.isdir(seed_path):
            continue

        for mood in os.listdir(seed_path):
            mood_path = os.path.join(seed_path, mood)
            if not os.path.isdir(mood_path):
                continue

            for t in os.listdir(mood_path):
                tick_path = os.path.join(mood_path, t)
                if t.isdigit() and os.path.isdir(tick_path):
                    print(f"✅ Found tick folder: {tick_path}")

    valid_ticks = []

    print("\n[DEBUG] Scanning tick folders...")
    for seed in os.listdir(SEED_PATH):
        seed_path = os.path.join(SEED_PATH, seed)
        if not os.path.isdir(seed_path):
            continue

        for mood in os.listdir(seed_path):
            mood_path = os.path.join(seed_path, mood)
            if not os.path.isdir(mood_path):
                continue

            for t in os.listdir(mood_path):
                tick_path = os.path.join(mood_path, t)
                if t.isdigit() and os.path.isdir(tick_path):
                    valid_ticks.append(int(t))
                    print(f"✅ Found tick folder: {tick_path}")

    TICKS = max(valid_ticks) + 1 if valid_ticks else 1
    print(f"[INFO] Animating {TICKS} ticks.")




    def update(tick):
        field = build_field_at_tick(tick)
        frame.set_data(field)
        ax.set_title(f"🔥 Tick {tick}")
        return [frame]

    ani = FuncAnimation(fig, update, frames=range(TICKS), interval=300, blit=True)
    ani.save(OUTPUT_PATH, writer="pillow", fps=2)
    print(f"[FieldMapAnimation] 🎞️ Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    animate_field()
