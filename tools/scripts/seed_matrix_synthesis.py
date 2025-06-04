
import os
import json
from datetime import datetime
from bloom.spawn_bloom import spawn_bloom
from owl.owl_rebloom_log import owl_log_rebloom

MOODS = ["joyful", "focused", "reflective", "anxious", "sad"]

def seed_matrix_synthesis(rows=3, cols=3):
    print(f"💠 Beginning seed matrix synthesis: {rows}x{cols}")
    for r in range(rows):
        for c in range(cols):
            mood = MOODS[(r * cols + c) % len(MOODS)]
            bloom = {
                "seed_id": f"matrix-{r}{c}",
                "lineage_depth": r,
                "entropy_score": 0.2 + (c * 0.1),
                "bloom_factor": 1.0 + (r * 0.2),
                "mood": mood
            }

            print(f"🌱 Synthesizing matrix bloom [{r},{c}] → Mood: {mood}, Entropy: {bloom['entropy_score']}")
            spawn_bloom(bloom)
            owl_log_rebloom(bloom)

    print("✅ Matrix synthesis complete.")

if __name__ == "__main__":
    seed_matrix_synthesis()
