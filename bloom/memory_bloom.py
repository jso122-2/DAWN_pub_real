import os
import json
from datetime import datetime

def write_bloom_json(bloom, fractal_path):
    # Create dir path
    mood = bloom.mood
    seed = bloom.seed
    bloom_id = bloom.bloom_id
    folder = f"juliet_flowers/{seed}/{mood}"
    os.makedirs(folder, exist_ok=True)

    # Prepare memory dict
    memory = {
        "bloom_id": bloom_id,
        "lineage_depth": bloom.lineage_depth,
        "entropy_score": bloom.entropy_score,
        "mood": mood,
        "bloom_factor": bloom.bloom_factor,
        "timestamp": datetime.now().isoformat(),
        "fractal_path": fractal_path
    }

    # Write JSON
    path = os.path.join(folder, f"{bloom_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

    print(f"📝 Memory saved to {path}")
