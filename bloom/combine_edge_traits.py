
import os
import json
from datetime import datetime
from bloom.spawn_bloom import spawn_bloom
from mood.blend import blend_moods
from owl.owl_rebloom_log import owl_log_rebloom
from owl.owl_synthesis_analysis import owl_analyze_synthesis

def combine_edge_traits():
    bloom_dir = "juliet_flowers/bloom_metadata"
    files = sorted([
        f for f in os.listdir(bloom_dir)
        if f.endswith(".json")
    ])

    if not files:
        print("[EdgeFusion] ❌ No blooms to fuse.")
        return

    left = None
    right = None
    for f in files:
        if "00" in f:
            with open(os.path.join(bloom_dir, f), "r") as fp:
                left = json.load(fp)
        elif "22" in f:
            with open(os.path.join(bloom_dir, f), "r") as fp:
                right = json.load(fp)

    if not left or not right:
        print("[EdgeFusion] ⚠️ Could not find matrix corners.")
        return

    fused = {
        "seed_id": f"edgefusion-{datetime.now().strftime('%H%M%S')}",
        "lineage_depth": max(left["lineage_depth"], right["lineage_depth"]) + 1,
        "entropy_score": (left["entropy_score"] + right["entropy_score"]) / 2,
        "bloom_factor": (left["bloom_factor"] + right["bloom_factor"]) / 2,
        "mood": blend_moods([left, right])
    }

    print(f"[EdgeFusion] 🌐 Fusion complete: {fused}")
    spawn_bloom(fused)
    owl_log_rebloom(fused)
    owl_analyze_synthesis([left, right], fused)
