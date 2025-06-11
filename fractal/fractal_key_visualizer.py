# fractal_key_visualizer.py
# Renders a Julia set fractal for a given complex seed.

import numpy as np
import matplotlib.pyplot as plt

def render_julia(c: complex, resolution: int = 512, iterations: int = 300):
    """
    Generates and returns a matplotlib Figure of the Julia set for constant c.
    """
    x = np.linspace(-1.5, 1.5, resolution)
    y = np.linspace(-1.5, 1.5, resolution)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    M = np.zeros(Z.shape, dtype=int)
    mask = np.ones(Z.shape, bool)

    for i in range(iterations):
        Z[mask] = Z[mask]**2 + c
        mask = np.abs(Z) < 2
        M[mask] = i

    fig, ax = plt.subplots()
    ax.imshow(M, extent=[-1.5, 1.5, -1.5, 1.5], origin='lower')
    ax.axis('off')
    return fig
