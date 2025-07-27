import os
import json
from datetime import datetime
from collections import Counter
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

def calculate_mood_entropy_adjustment(eligible_blooms):
    """Calculate entropy adjustment based on parent bloom moods"""
    mood_counts = Counter(bloom["mood"] for bloom in eligible_blooms)
    dominant_mood = mood_counts.most_common(1)[0][0]
    dominant_count = mood_counts[dominant_mood]
    total_count = len(eligible_blooms)
    
    # Define mood-based entropy adjustments
    mood_adjustments = {
        "submerged": 0.10,    # +10% entropy for submerged dominance
        "anxious": 0.08,      # +8% entropy for anxious dominance
        "overload": 0.15,     # +15% entropy for overload dominance
        "reflective": -0.05,  # -5% entropy for reflective dominance
        "focused": -0.03,     # -3% entropy for focused dominance
        "joyful": 0.05        # +5% entropy for joyful dominance
    }
    
    # Calculate adjustment based on dominance ratio
    dominance_ratio = dominant_count / total_count
    base_adjustment = mood_adjustments.get(dominant_mood, 0.0)
    
    # Scale adjustment by dominance ratio
    return base_adjustment * dominance_ratio

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
    base_entropy = sum(b["entropy_score"] for b in eligible) / n
    bloom_factor = sum(b["bloom_factor"] for b in eligible) / n
    mood = blend_moods(eligible)
    
    # Calculate mood-based entropy adjustment
    entropy_adjustment = calculate_mood_entropy_adjustment(eligible)
    adjusted_entropy = min(1.0, base_entropy * (1 + entropy_adjustment))

    new_bloom = {
        "seed_id": f"recursive-{datetime.now().strftime('%H%M%S')}",
        "lineage_depth": lineage,
        "entropy_score": adjusted_entropy,
        "bloom_factor": bloom_factor,
        "mood": mood
    }

    print(f"[Recursive] 🌺 Evolving next-gen bloom from {n} synthesis nodes...")
    print(f"🧬 → Lineage: {lineage}, Base Entropy: {base_entropy:.2f}, Mood Adjustment: {entropy_adjustment:.2%}")
    print(f"🧬 → Final Entropy: {adjusted_entropy:.2f}, Mood: {mood}")

    spawn_bloom(new_bloom)
    owl_log_rebloom(new_bloom)
    owl_analyze_synthesis(eligible, new_bloom) 