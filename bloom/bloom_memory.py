
import os
import json
from datetime import datetime

def write_bloom_json(bloom, fractal_path):
    """
    Save bloom memory metadata as JSON file.
    """
    mood = bloom.mood
    seed = bloom.seed
    bloom_id = bloom.bloom_id
    folder = os.path.join("juliet_flowers", seed, mood)
    os.makedirs(folder, exist_ok=True)

    memory = {
        "bloom_id": bloom_id,
        "lineage_depth": bloom.lineage_depth,
        "entropy_score": bloom.entropy_score,
        "mood": mood,
        "bloom_factor": bloom.bloom_factor,
        "timestamp": datetime.now().isoformat(),
        "fractal_path": fractal_path
    }

    file_path = os.path.join(folder, f"{bloom_id}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

    print(f"📝 Bloom memory saved: {file_path}")
