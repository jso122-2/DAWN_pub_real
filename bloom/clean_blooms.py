# clean_blooms.py

import os
import shutil

BLOOM_DIR = "juliet_flowers/"
REGISTRY = "bloom_registry.json"

def clean_bloom_logs():
    print("🧹 Cleaning juliet_flowers/...")

    for seed in os.listdir(BLOOM_DIR):
        path = os.path.join(BLOOM_DIR, seed)
        if os.path.isdir(path):
            shutil.rmtree(path)
            print(f"❌ Removed: {path}")

    os.makedirs(BLOOM_DIR, exist_ok=True)
    print("✅ Bloom directory reset.")

    if os.path.exists(REGISTRY):
        os.remove(REGISTRY)
        print(f"🗑️ Removed bloom registry: {REGISTRY}")

if __name__ == "__main__":
    clean_bloom_logs()
