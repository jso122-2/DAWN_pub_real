# /owl/owl_commentary.py

import os
from datetime import datetime

COMMENTARY_DIR = "owl/commentary"
os.makedirs(COMMENTARY_DIR, exist_ok=True)


def log_reflection(seed_id, content, mood="reflective"):
    """
    Save a timestamped reflection for a given seed bloom.
    """
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"owl_reflection_{seed_id}_{timestamp}.txt"
    filepath = os.path.join(COMMENTARY_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"[Reflection] 🧠 Mood: {mood}\n")
        f.write(f"[Seed] 🌱 {seed_id}\n")
        f.write("\n---\n")
        f.write(content.strip())
        f.write("\n")

    print(f"[OwlCommentary] 📄 Saved reflection → {filepath}")
    return filepath
