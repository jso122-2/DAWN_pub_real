
import os
import json
import hashlib

BLOOM_DIR = "juliet_flowers/bloom_metadata"
EXPORT = "juliet_flowers/cluster_report/compressed_bloom_genome.json"

def compress_bloom(bloom):
    trait_hash = hashlib.sha1(json.dumps(bloom, sort_keys=True).encode()).hexdigest()
    compressed = {
        "id": bloom.get("seed_id"),
        "depth": bloom.get("lineage_depth", 0),
        "entropy": bloom.get("entropy_score", 0.0),
        "bloom_factor": bloom.get("bloom_factor", 1.0),
        "mood": bloom.get("mood", "undefined"),
        "sig": trait_hash[:12]
    }
    return compressed

def export_compressed_genome():
    compressed = []
    for fname in os.listdir(BLOOM_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(BLOOM_DIR, fname), "r") as f:
                bloom = json.load(f)
                compressed.append(compress_bloom(bloom))

    with open(EXPORT, "w") as f:
        json.dump(compressed, f, indent=2)
    print(f"[Genome] 📦 Compressed genome saved → {EXPORT}")
