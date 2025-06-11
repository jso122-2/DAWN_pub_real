# /bloom_core/synthesis_logic.py

from rhizome.rhizome_pathfinder import find_path
from .spawn_bloom import spawn_bloom

SYNTHESIS_THRESHOLD = 2.5
REINFORCEMENT_TRACKER = {}

def check_synthesis_trigger(seed_a, seed_b, signal_strength, pulse=None):
    path_key = f"{seed_a}→{seed_b}"
    REINFORCEMENT_TRACKER[path_key] = REINFORCEMENT_TRACKER.get(path_key, 0.0) + signal_strength

    if REINFORCEMENT_TRACKER[path_key] >= SYNTHESIS_THRESHOLD:
        print(f"[🌸 Trigger] Synthesis Bloom on path: {path_key}")
        path = find_path(seed_a, seed_b)
        if path:
            bloom_data = {
                "seed_id": seed_b,
                "lineage_depth": len(path),
                "bloom_factor": round(signal_strength, 3),
                "entropy_score": round(0.2 + 0.1 * len(path), 3),
                "mood": "synthesis",
                "path_history": path
            }
            spawn_bloom(bloom_data, pulse or {})
        REINFORCEMENT_TRACKER[path_key] = 0.0
