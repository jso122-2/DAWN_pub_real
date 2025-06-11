import numpy as np
import matplotlib.pyplot as plt
import os

def generate_julia_set(c, resolution=512, zoom=1.0, max_iter=256, mood="neutral", save_path=None):
    print(f"[DEBUG] Generating fractal: c={c}, mood={mood}, save_path={save_path}")

    try:
        x = np.linspace(-1.5/zoom, 1.5/zoom, resolution)
        y = np.linspace(-1.5/zoom, 1.5/zoom, resolution)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        iteration = np.zeros(Z.shape, dtype=int)
        mask = np.full(Z.shape, True, dtype=bool)

        for i in range(max_iter):
            Z[mask] = Z[mask] ** 2 + c
            diverged = np.abs(Z) > 2
            iteration[diverged & mask] = i
            mask &= ~diverged

        norm = iteration / max_iter
        cmap = {
            "neutral": "bone",
            "anxious": "magma",
            "reflective": "viridis",
            "joyful": "plasma",
            "melancholy": "cividis",
            "angry": "inferno",
            "calm": "twilight"
        }.get(mood, "bone")

        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.figure(figsize=(5, 5), dpi=100)
            plt.axis("off")
            plt.imshow(norm, cmap=cmap, extent=[-1.5, 1.5, -1.5, 1.5])
            plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
            plt.close()
            print(f"[DEBUG SUCCESS] Fractal explicitly saved at: {save_path}")

    except Exception as e:
        print(f"[DEBUG ERROR] Fractal generation explicitly failed: {e}")
