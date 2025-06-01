import os
import json
from datetime import datetime
from bloom.spawn_bloom import spawn_bloom
from owl.owl_rebloom_log import owl_log_rebloom
from owl.owl_synthesis_analysis import owl_analyze_synthesis
from mood.blend import blend_moods
from bloom.recursive_check import is_recursive_eligible

# Example of tracked blocked lineages
blocked_ancestries = {"∆stuck-ghostlineage", "∆orphan-branchA"}

def unblock_lineage(bloom):
    lineage_tag = bloom.get("lineage_tag", "")
    if lineage_tag in blocked_ancestries:
        blocked_ancestries.remove(lineage_tag)
        print(f"[UNBLOCK] 🔓 Releasing blocked lineage: {lineage_tag}")
        return True
    return False

def recursive_synthesis(n=3):
    bloom_dir = "juliet_flowers/bloom_metadata"
    files = sorted([
        f for f in os.listdir(bloom_dir)
        if f.endswith(".json") and "synthesis-" in f
    ], reverse=True)

    eligible = []
    for fname in files:
        with open(os.path.join(bloom_dir, fname), "r") as f:
            bloom = json.load(f)

            if unblock_lineage(bloom):
                print(f"[Queue] 🌀 Bloom {bloom.get('seed_id')} unblocked for synthesis.")

            if is_recursive_eligible(bloom):
                eligible.append(bloom)
            if len(eligible) >= n:
                break

    if len(eligible) < n:
        print("[Recursive] ⚠️ Not enough eligible synthesis blooms.")
        return

    lineage = max(b["lineage_depth"] for b in eligible) + 1
    entropy = sum(b["entropy_score"] for b in eligible) / n
    bloom_factor = sum(b["bloom_factor"] for b in eligible) / n
    mood = blend_moods(eligible)

    new_bloom = {
        "seed_id": f"recursive-{datetime.now().strftime('%H%M%S')}",
        "lineage_depth": lineage,
        "entropy_score": entropy,
        "bloom_factor": bloom_factor,
        "mood": mood
    }

    print(f"[Recursive] 🌺 Evolving next-gen bloom from {n} synthesis nodes...")
    print(f"🧬 → Lineage: {lineage}, Entropy: {entropy:.2f}, Mood: {mood}")

    spawn_bloom(new_bloom)
    owl_log_rebloom(new_bloom)
    owl_analyze_synthesis(eligible, new_bloom)
