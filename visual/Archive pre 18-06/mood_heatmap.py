#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

OUT = "visual/outputs/mood_heatmap/mood_heatmap.png"

# Generate synthetic mood data

def generate_synthetic_mood():
    np.random.seed(42)
    mood = np.random.rand(10, 10)
    return mood

def plot_mood_heatmap():
    mood = generate_synthetic_mood()
    fig, ax = plt.subplots(figsize=(6, 6))
    cax = ax.imshow(mood, cmap="coolwarm", interpolation="nearest")
    ax.set_title("Mood Heatmap")
    fig.colorbar(cax, ax=ax, label="Mood Intensity")
    output_dir = os.path.dirname(OUT)
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(OUT)
    plt.close()
    print(f"✅ Mood heatmap saved → {OUT}")
    return OUT

def main(*args, **kwargs):
    output_path = plot_mood_heatmap()
    print(f"✅ Saved mood heatmap to {output_path}")

if __name__ == "__main__":
    main()
