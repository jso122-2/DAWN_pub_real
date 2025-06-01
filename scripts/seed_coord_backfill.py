import os
import json
import random

ROOT = "juliet_flowers/"
FIELD_SIZE = 100

def backfill_seed_coords():
    count = 0
    for root, _, files in os.walk(ROOT):
        for fname in files:
            if fname.endswith(".json"):
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    coord = data.get("seed_coord", [None, None])
                    if not coord or not isinstance(coord, list) or len(coord) != 2:
                        data["seed_coord"] = [random.randint(0, FIELD_SIZE-1), random.randint(0, FIELD_SIZE-1)]
                        with open(fpath, "w", encoding="utf-8") as f:
                            json.dump(data, f, indent=2)
                        count += 1
                except Exception as e:
                    print(f"[WARN] Skipped {fpath}: {e}")

    print(f"✅ Backfilled seed_coord in {count} files.")

if __name__ == "__main__":
    backfill_seed_coords()
