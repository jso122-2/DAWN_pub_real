# /fractal/fractal_generator.py

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
import hashlib
import random
from mycelium.nutrient_utils import get_nutrient_heat

IMG_SIZE = (512, 512)
SAVE_DIR = "juliet_flowers/fractal_signatures"
os.makedirs(SAVE_DIR, exist_ok=True)

PLATONIC_PIGMENTS = {
    "resilient": (44, 122, 255),
    "anxious": (255, 44, 122),
    "reflective": (153, 102, 255),
    "focused": (50, 205, 50),
    "joyful": (255, 215, 0),
    "sorrowful": (120, 120, 120),
    "furious": (255, 0, 0),
    "neutral": (200, 200, 200)
}


def evolve_fractal_signature(seed_id, entropy, lineage_depth, bloom_factor):
    """
    Generate complex number `c` for Julia fractal based on semantic variables.
    """
    real = np.cos(entropy * np.pi) * 0.7885 + (bloom_factor - 1.0) * 0.1
    imag = np.sin(lineage_depth) * 0.3 + random.uniform(-0.05, 0.05)

    seed_hash = int(hashlib.md5(seed_id.encode()).hexdigest(), 16)
    offset = ((seed_hash % 1000) / 1000.0 - 0.5) * 0.2

    return complex(real + offset, imag)


def apply_heat_blend(img, heat, mood):
    base = img.convert("RGB")
    tint = PLATONIC_PIGMENTS.get(mood, (180, 180, 180))
    overlay = Image.new("RGB", base.size, tint)

    # New: Modulate alpha by SCUP / Sigil Intensity
    from codex.sigil_memory_ring import get_sigil_energy_index
    sigil_intensity = get_sigil_energy_index()  # Returns value 0.0–1.0

    alpha = min(0.6 + (sigil_intensity * 0.3), 0.95)
    return Image.blend(base, overlay, alpha=alpha)




def overlay_signature(img, seed_id, lineage_depth, mood, entropy, heat, bloom_factor):
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()

    lines = [
        f"Seed: {seed_id}",
        f"Depth: {lineage_depth}",
        f"Heat: {heat:.2f}",
        f"Mood: {mood}",
        f"Entropy: {entropy:.2f}",
        f"Bloom Factor: {bloom_factor:.2f}"
    ]

    for i, line in enumerate(lines):
        draw.text((10, 10 + i * 16), line, font=font, fill=(255, 255, 255))

    return img


def generate_julia_image(seed_id, lineage_depth, bloom_factor, entropy_score, mood="reflective", is_synthesis=False):
    """
    Full rendering pipeline for a bloom's Julia-set visual.
    Dynamically varies zoom, iterations, and offset by seed + semantic input.
    """
    width, height = IMG_SIZE
    zoom_factor = 1.5 - (bloom_factor * 0.2)
    entropy_shift = (entropy_score - 0.5) * 1.2

    # Dynamic viewport offset based on seed
    seed_hash = int(hashlib.sha256(seed_id.encode()).hexdigest(), 16)
    offset_x = ((seed_hash % 1000) / 1000 - 0.5) * 1.2
    offset_y = (((seed_hash // 1000) % 1000) / 1000 - 0.5) * 1.2

    # Generate meshgrid with offset
    x = np.linspace(-zoom_factor + offset_x, zoom_factor + offset_x, width)
    y = np.linspace(-zoom_factor + offset_y, zoom_factor + offset_y, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y


    # More dynamic iterations
    iter_base = 240 + int((bloom_factor + entropy_score) * 40)
    iterations = iter_base + (lineage_depth * 5)
    if is_synthesis:
        iterations += 80  # Super-blooms go deeper

    # Get complex constant for fractal generation
    c = evolve_fractal_signature(seed_id, entropy_score, lineage_depth, bloom_factor)

    output = np.zeros(Z.shape, dtype=int)
    mask = np.full(Z.shape, True, dtype=bool)

    for i in range(iterations):
        Z[mask] = Z[mask] ** 2 + c
        mask, old_mask = abs(Z) < 4, mask
        output += mask & old_mask


    max_val = output.max()
    if max_val == 0:
        max_val = 1  # prevent division by zero
    output_normalized = np.uint8(255 * output / max_val)

    img = Image.fromarray(output_normalized).convert("L").resize(IMG_SIZE)

    # Add mood + pressure tint
    heat = get_nutrient_heat(seed_id)
    img_colored = apply_heat_blend(img, heat, mood)

    # Add visual signature overlay
    final = overlay_signature(img_colored, seed_id, lineage_depth, mood, entropy_score, heat, bloom_factor)

    # Save
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"{seed_id}_{timestamp}.png"
    final_path = os.path.join(SAVE_DIR, filename)
    final.save(final_path)
    print(f"[Fractal] 🌸 Rendered {filename} | Mood: {mood} | Entropy: {entropy_score:.2f} | Heat: {heat:.2f}")

    return final_path


    output_normalized = np.uint8(255 * output / output.max())
    img = Image.fromarray(output_normalized).convert("L").resize(IMG_SIZE)
