# rebloom_lineage.py

import os
import json

BASE_DIR = "juliet_flowers/"
OUTPUT_JSON = "juliet_flowers/cluster_report/rebloom_lineage.json"

def collect_all_blooms():
    all_blooms = {}
    for seed in os.listdir(BASE_DIR):
        seed_path = os.path.join(BASE_DIR, seed)
        if not os.path.isdir(seed_path):
            continue

        for mood in os.listdir(seed_path):
            mood_path = os.path.join(seed_path, mood)
            if not os.path.isdir(mood_path):
                continue

            for tick in os.listdir(mood_path):
                tick_path = os.path.join(mood_path, tick)
                if not os.path.isdir(tick_path):
                    continue

                for fname in os.listdir(tick_path):
                    if fname.endswith(".json") or fname.endswith(".txt"):
                        fpath = os.path.join(tick_path, fname)
                        with open(fpath, "r", encoding="utf-8") as f:
                            try:
                                data = json.load(f)
                                bloom_id = data.get("id")
                                if bloom_id:
                                    all_blooms[bloom_id] = data
                            except Exception as e:
                                print(f"[WARN] Skipping {fpath}: {e}")
    return all_blooms

def compute_lineages(all_blooms):
    lineage_map = {}

    def trace_lineage(bloom_id):
        chain = []
        current = bloom_id
        while current:
            bloom = all_blooms.get(current)
            if not bloom:
                break
            chain.append(current)
            current = bloom.get("ancestor_id")
        return list(reversed(chain))

    for bloom_id in all_blooms:
        chain = trace_lineage(bloom_id)
        lineage_map[bloom_id] = {
            "generation_depth": len(chain) - 1,
            "rebloom_chain": chain
        }

    return lineage_map

def main():
    print("🔍 Gathering blooms...")
    blooms = collect_all_blooms()
    print(f"🌸 Total blooms found: {len(blooms)}")

    print("🔗 Computing rebloom lineages...")
    lineage_data = compute_lineages(blooms)

    os.makedirs("juliet_flowers/cluster_report", exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(lineage_data, f, indent=2)

    print(f"✅ Lineage map saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
