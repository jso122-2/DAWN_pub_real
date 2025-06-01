# juliet_utils.py

import os
import json
import random

def load_bloom_metadata(mood_dir):
    blooms = []
    for fname in os.listdir(mood_dir):
        if fname.endswith(".json") or fname.endswith(".txt"):
            fpath = os.path.join(mood_dir, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    seed_coord = data.get("seed_coord")
                    if not seed_coord:
                        seed_coord = [random.randint(0, 99), random.randint(0, 99)]


                    pressure = data.get("semantic_pressure")
                    if pressure is None:
                        fs = data.get("fractal_signature", {})
                        pressure = max(0.1, fs.get("bloom_factor", 1.0) / 10.0)  # ensure minimum heat


                    blooms.append({
                        "seed_coord": seed_coord,
                        "semantic_pressure": pressure,
                        "mood": data.get("mood", ""),
                        "mood_prev": data.get("mood_prev", data.get("mood", "none"))
                    })
            except Exception as e:
                print(f"[WARN] Skipping {fpath}: {e}")
    return blooms

