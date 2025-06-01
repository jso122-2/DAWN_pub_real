# /field_map.py

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Assume these are populated externally
from mycelium.mycelium_layer import get_root_density_frame
from bloom.rebloom_tracker import get_rebloom_trail_frame
from owl.owl_heatmap import get_semantic_pressure_overlay

def animate_hybrid_field(tick_range, seed_field_shape, save_path="juliet_flowers/cluster_report/hybrid_field.gif"):
    """
    Animate hybrid semantic field:
    - Root density (Mycelium)
    - Rebloom trails
    - Semantic pressure heatmap (Owl)
    """

    fig, ax = plt.subplots(figsize=(8, 8))
    frames = []

    for tick in tick_range:
        # Layers
        root_density = get_root_density_frame(tick, seed_field_shape)
        rebloom_overlay = get_rebloom_trail_frame(tick, seed_field_shape)
        pressure_heatmap = get_semantic_pressure_overlay(tick, seed_field_shape)

        # Combine visual data
        combined = np.clip(
            0.5 * root_density +
            0.3 * rebloom_overlay +
            0.7 * pressure_heatmap,
            0, 1
        )

        frame = ax.imshow(combined, cmap='inferno', animated=True)
        title = ax.text(0.5, 1.01, f"Hybrid Field – Tick {tick}", transform=ax.transAxes,
                        ha="center", va="bottom", fontsize=12, color='white')
        frames.append([frame, title])

    ani = animation.ArtistAnimation(fig, frames, interval=500, blit=True)
    ani.save(save_path, writer="pillow")

    print(f"✅ Hybrid field animation saved to {save_path}")
