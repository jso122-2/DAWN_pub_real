# bloom_writer.py
import os
import json
from datetime import datetime
from fractal.encode_script_as_fractal import encode_script_as_fractal

# Write Bloom JSON with integrated Multibrot fractal encoding
def write_bloom_json(bloom, output_dir=None, multibrot_exponent=3, resolution=512):
    """
    Saves bloom metadata as JSON and generates a Multibrot fractal key visualization.
    """
    # Determine output folder
    seed = bloom.get('agent') or bloom.seed
    mood = bloom.get('mood') or bloom.mood
    tick = bloom.get('tick') or bloom.tick
    base_folder = output_dir or f"juliet_flowers/{seed}/{mood}/{tick}"
    os.makedirs(base_folder, exist_ok=True)

    # Fractal encoding: include exponent in seed generation
    # Use entire JSON string as source text for maximum structural embedding
    text_block = json.dumps(bloom, indent=2)
    fractal_filename = f"{bloom.get('id', bloom.id)}_exp{multibrot_exponent}.png"
    fractal_path = os.path.join(base_folder, fractal_filename)

    # Encode script/text as multibrot fractal (Julia generalization)
    c, fig = encode_script_as_fractal(
        text=text_block,
        save_path=fractal_path,
        resolution=resolution
    )

    # Attach fractal info to metadata
    bloom['fractal_signature'] = {
        'seed_complex': str(c),
        'exponent': multibrot_exponent,
        'resolution': resolution,
        'fractal_path': fractal_path
    }

    # Save metadata JSON
    metadata_path = os.path.join(base_folder, f"{bloom['id']}.json")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(bloom, f, indent=2)

    print(f"[Bloom] 🌸 Saved bloom and Multibrot fractal → {metadata_path}")
    return metadata_path, fractal_path
