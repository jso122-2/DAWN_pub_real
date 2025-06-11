# folder_normalizer.py

import os
import shutil

BASE_DIR = "juliet_flowers/"
DEFAULT_TICK = "0"

def normalize_bloom_folders():
    moved = 0
    for seed in os.listdir(BASE_DIR):
        seed_path = os.path.join(BASE_DIR, seed)
        if not os.path.isdir(seed_path):
            continue

        for mood in os.listdir(seed_path):
            mood_path = os.path.join(seed_path, mood)
            if not os.path.isdir(mood_path):
                continue

            for item in os.listdir(mood_path):
                item_path = os.path.join(mood_path, item)

                # If it's already a folder (i.e. tick folder), skip
                if os.path.isdir(item_path):
                    continue

                # If it's a stray bloom JSON/TXT file, move it into tick folder
                if item.endswith(".json") or item.endswith(".txt"):
                    tick_path = os.path.join(mood_path, DEFAULT_TICK)
                    os.makedirs(tick_path, exist_ok=True)

                    dest_path = os.path.join(tick_path, item)
                    shutil.move(item_path, dest_path)
                    moved += 1
                    print(f"[NORMALIZED] Moved {item} → {tick_path}/")

    print(f"\n✅ Normalization complete. {moved} files relocated into tick folder '{DEFAULT_TICK}'.")

if __name__ == "__main__":
    normalize_bloom_folders()
