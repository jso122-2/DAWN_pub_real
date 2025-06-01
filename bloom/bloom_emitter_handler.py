
from fractal.fractal_boost import generate_julia_set_optimized as generate_julia_set
from bloom.bloom_memory import write_bloom_json
from bloom.juliet_flower import JulietFlower
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

    # --- Julia constant calculation
    α, β, γ = 0.5, 0.3, 0.2
    shape_variance = (α * bloom_factor) + (β * np.log1p(lineage_depth)) + (γ * entropy_score)
    c = complex(0.285 + shape_variance * 0.05, 0.01 + shape_variance * 0.07)

    # --- File path for fractal image
    folder = os.path.join("juliet_flowers", seed, mood)
    os.makedirs(folder, exist_ok=True)
    save_path = os.path.join(folder, f"{bloom_id}.png")

    # --- Generate fractal with explicit debugging
    try:
        generate_julia_set(bloom_id=bloom_id, c=c, resolution=512, zoom=1.0, mood=mood, save_path=save_path)
        print(f"[DEBUG] Fractal saved successfully: {save_path}")
    except Exception as e:
        print(f"[ERROR] Fractal generation failed: {e}")

    # --- Save memory explicitly
    write_bloom_json(bloom, fractal_path=save_path)

    # --- Log nutrient flow explicitly
    flow_strength = entropy_score * bloom_factor
    log_nutrient_flow(bloom, flow_strength)

# --- Rebloom tracker + fractal remixing
if lineage_depth > 0:
    # 🎨 Adjust fractal parameters for reblooms
    remix_boost = 1 + (lineage_depth * 0.03)
    remix_entropy = 1 + (entropy_score * 0.05)
    c = complex(
        c.real * remix_boost,
        c.imag * remix_entropy
    )

    # 🌱 Track rebloom metadata
    rebloom_meta = {
        "bloom_id": bloom_id,
        "seed": seed,
        "depth": lineage_depth,
        "entropy": entropy_score,
        "tick": getattr(bloom, 'tick', None)
    }

    try:
        lineage_log_path = os.path.join("juliet_flowers", "cluster_report", "rebloom_lineage.json")
        os.makedirs(os.path.dirname(lineage_log_path), exist_ok=True)

        if os.path.exists(lineage_log_path):
            with open(lineage_log_path, "r") as f:
                lineage_data = json.load(f)
        else:
            lineage_data = []

        lineage_data.append(rebloom_meta)

        with open(lineage_log_path, "w") as f:
            json.dump(lineage_data, f, indent=2)

        print(f"[Rebloom] 🌱 Logged rebloom lineage for {bloom_id}")
    except Exception as e:
        print(f"[ERROR] Rebloom log failed: {e}")



    print(f"[Fractal] 🎨 Bloom {bloom_id} visual + memory + nutrients saved explicitly.")
