
import os
import json
from datetime import datetime
from bloom.spawn_bloom import spawn_bloom
from owl.owl_rebloom_log import owl_log_rebloom
from owl.owl_synthesis_analysis import owl_analyze_synthesis
from mood.blend import blend_moods

def fuse_all_corners():
    bloom_dir = "juliet_flowers/bloom_metadata"
    ids = ["00", "02", "20", "22"]
    blooms = []

    for f in os.listdir(bloom_dir):
        for idtag in ids:
            if idtag in f and f.endswith(".json"):
                with open(os.path.join(bloom_dir, f), "r") as fp:
                    blooms.append(json.load(fp))
                break

    if len(blooms) < 4:
        print("[CornerFusion] ⚠️ Not all corner blooms found.")
        return

    fused = {
        "seed_id": f"cornerfusion-{datetime.now().strftime('%H%M%S')}",
        "lineage_depth": max(b["lineage_depth"] for b in blooms) + 1,
        "entropy_score": sum(b["entropy_score"] for b in blooms) / len(blooms),
        "bloom_factor": sum(b["bloom_factor"] for b in blooms) / len(blooms),
        "mood": blend_moods(blooms)
    }

    print(f"[CornerFusion] 🧠 Fusing all corner seeds → {fused['seed_id']}")
    spawn_bloom(fused)
    owl_log_rebloom(fused)
    owl_analyze_synthesis(blooms, fused)
