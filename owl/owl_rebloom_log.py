
import os
import json
from datetime import datetime

COMMENTARY_DIR = "owl/commentary"
os.makedirs(COMMENTARY_DIR, exist_ok=True)

def owl_log_rebloom(bloom_data):
    seed_id = bloom_data.get("seed_id", "unknown")
    mood = bloom_data.get("mood", "undefined")
    lineage_depth = bloom_data.get("lineage_depth", 0)
    entropy_score = bloom_data.get("entropy_score", 0.0)

    commentary = f"🦉 {datetime.now().isoformat()} | REBLOOM: {seed_id}\n"
    commentary += f"    Mood: {mood}\n"
    commentary += f"    Lineage Depth: {lineage_depth}\n"
    commentary += f"    Entropy Score: {entropy_score:.2f}\n"

    filename = f"owl_rebloom_{seed_id}_{datetime.now().isoformat(timespec='seconds').replace(':','-')}.txt"
    filepath = os.path.join(COMMENTARY_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(commentary)

    print(f"[Owl] 🪶 Commentary saved → {filepath}")
