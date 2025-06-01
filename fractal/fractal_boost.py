from pathlib import Path
import numpy as np
from numba import njit, prange
from PIL import Image
import os

# Mood → base RGB color (used for gradient mapping)
MOOD_RGB = {
    "neutral": (180, 180, 180),
    "anxious": (100, 0, 150),
    "reflective": (30, 144, 255),
    "joyful": (255, 140, 0),
    "melancholy": (70, 70, 120),
    "angry": (255, 50, 50),
    "calm": (120, 220, 160)
}

@njit(parallel=True)
def julia_optimized(width, height, zoom, max_iter, c_real, c_imag):
    result = np.zeros((height, width), dtype=np.uint16)
    for y in prange(height):
        for x in prange(width):
            zx = 1.5 * (x - width / 2) / (0.5 * zoom * width)
            zy = 1.5 * (y - height / 2) / (0.5 * zoom * height)
            z = complex(zx, zy)
            c = complex(c_real, c_imag)
            iter_count = 0
            while abs(z) < 10 and iter_count < max_iter:
                z = z*z + c
                iter_count += 1
            result[y, x] = iter_count
    return result

def apply_color_map(iter_array, max_iter, base_color):
    h, w = iter_array.shape
    img = np.zeros((h, w, 3), dtype=np.uint8)
    r_base, g_base, b_base = base_color
    norm = iter_array / max_iter
    for y in range(h):
        for x in range(w):
            scale = norm[y, x]
            img[y, x] = (
                int(scale * r_base),
                int(scale * g_base),
                int(scale * b_base)
            )
    return img

def generate_julia_set_optimized(bloom_id, c, mood="neutral", resolution=512, zoom=1.0, max_iter=256, save_path=None):
    width = height = resolution
    fractal = julia_optimized(width, height, zoom, max_iter, c.real, c.imag)
    base_color = MOOD_RGB.get(mood, (180, 180, 180))
    rgb_array = apply_color_map(fractal, max_iter, base_color)

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        img = Image.fromarray(rgb_array)
        img.save(save_path)
        print(f"⚡ Optimized Julia saved → {save_path}")

    return rgb_array

boost_path = Path("/mnt/data/Tick_engine/fractal/fractal_boost.py")
