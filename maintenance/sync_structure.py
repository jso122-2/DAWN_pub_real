import os
import json

def sync_juliet_structure():
    base_dir = "juliet_flowers"
    index = {}

    for seed in os.listdir(base_dir):
        seed_path = os.path.join(base_dir, seed)
        if os.path.isdir(seed_path):  # ✅ Prevent file crash
            index[seed] = {}
            for mood in os.listdir(seed_path):
                mood_path = os.path.join(seed_path, mood)
                if os.path.isdir(mood_path):  # ✅ Handle nested file errors
                    blooms = os.listdir(mood_path)
                    index[seed][mood] = blooms

    os.makedirs(os.path.join(base_dir, "index"), exist_ok=True)
    with open(os.path.join(base_dir, "index", "lineage_map.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    print("[Structure] 📂 Juliet memory structure synchronized.")
