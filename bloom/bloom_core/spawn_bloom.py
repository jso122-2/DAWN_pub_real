# /bloom_core/spawn_bloom.py

import os
import json
from datetime import datetime

def spawn_bloom(bloom_data, pulse=None):
    """
    Save a bloom to disk with lineage and synthesis info.
    """
    seed_id = bloom_data.get("seed_id", "unknown")
    timestamp = datetime.utcnow().isoformat()
    bloom_data["timestamp"] = timestamp
    path = f"juliet_flowers/bloom_metadata/{seed_id}_{timestamp}.json"

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(bloom_data, f, indent=2)

    print(f"[Bloom] 🌸 Bloom spawned: {seed_id} | Depth: {bloom_data.get('lineage_depth')} | Mood: {bloom_data.get('mood')}")
