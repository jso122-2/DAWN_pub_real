from fractal.fractal_generator import generate_julia_set
from bloom.bloom_memory import write_bloom_json
from mycelium.nutrient_logger import log_nutrient_flow
import numpy as np
import os

def handle_bloom_emitted(bloom):
    # --- Extract bloom attributes
    bloom_factor = bloom.bloom_factor
    lineage_depth = bloom.lineage_depth
    entropy_score = bloom.entropy_score
    mood = bloom.mood
    bloom_id = bloom.bloom_id
    seed = bloom.seed

    # --- Julia constant
    α, β, γ = 0.5, 0.3, 0.2
    shape_variance = (α * bloom_factor) + (β * np.log1p(lineage_depth)) + (γ * entropy_score)
    c = complex(0.285 + shape_variance * 0.05, 0.01 + shape_variance * 0.07)

    # --- File path
    folder = os.path.join("juliet_flowers", seed, mood)
    os.makedirs(folder, exist_ok=True)
    save_path = os.path.join(folder, f"{bloom_id}.png")

    # --- Generate Fractal & Save Memory
    generate_julia_set(c=c, resolution=512, zoom=1.0, mood=mood, save_path=save_path)
    write_bloom_json(bloom, fractal_path=save_path)

    # --- 💧 Log Nutrient Flow
    flow_strength = entropy_score * bloom_factor
    log_nutrient_flow(bloom, flow_strength)

    print(f"[Fractal] 🎨 Bloom {bloom_id} visual + memory + nutrients saved.")
