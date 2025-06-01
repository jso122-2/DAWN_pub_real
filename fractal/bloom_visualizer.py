import os
import json
import matplotlib.pyplot as plt
import numpy as np

CLUSTER_DIR = os.path.join("juliet_flowers", "cluster_report")
os.makedirs(CLUSTER_DIR, exist_ok=True)

MOOD_COLORMAPS = {
    "calm": "Blues",
    "curious": "Greens",
    "reflective": "Purples",
    "anxious": "Oranges",
    "overload": "Reds",
    "neutral": "gray"
}


def julia(x, y, c, iterations=100):
    z = complex(x, y)
    for i in range(iterations):
        z = z*z + c
        if abs(z) > 2.0:
            return i
    return iterations

def plot_julia(c: complex, filename: str, mood: str = "neutral", scale: float = 1.0):

    width, height = 300, 300
    x_range = y_range = scale
    img = np.zeros((height, width))

    for x in range(width):
        for y in range(height):
            zx = 2.0 * (x - width / 2) / (width / 2) * x_range
            zy = 2.0 * (y - height / 2) / (height / 2) * y_range
            img[y, x] = julia(zx, zy, c)

    colormap = MOOD_COLORMAPS.get(mood, "gray")
    plt.imshow(img, cmap=colormap)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(CLUSTER_DIR, filename), dpi=150)
    plt.close()
