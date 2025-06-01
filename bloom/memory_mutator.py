import random
from owl.owl_tracer_log import owl_log

def mutate_suppressed_bloom(bloom, entropy_cutoff=0.5):
    """
    Extracts lower-entropy sentences from a suppressed bloom and mutates them into a new seed.
    Also adapts mood and bloom_factor to encourage recovery.
    """
    if not getattr(bloom, "suppressed", False):
        return None  # Only mutate suppressed blooms

    original_sentences = getattr(bloom, "sentences", [])
    entropy_scores = getattr(bloom, "entropy_map", {})  # sentence → entropy score

    # Filter retained sentences
    retained = [
        s for s in original_sentences
        if entropy_scores.get(s, 1.0) <= entropy_cutoff
    ]

    if not retained:
        owl_log(f"[Mutation Failed] ❌ No viable sentences found in {bloom.seed_id}")
        return None

    random.shuffle(retained)

    # New mood and factor adjustments
    adjusted_factor = round(getattr(bloom, "bloom_factor", 1.0) * 0.95, 3)
    new_mood = "curious"

    mutant_seed = {
        "seed_id": f"{bloom.seed_id}::mutant",
        "sentences": retained,
        "origin": bloom.seed_id,
        "mutation_tag": "suppression_salvage",
        "lineage_depth": getattr(bloom, "lineage_depth", 0) + 1,
        "entropy_score": round(
            sum(entropy_scores.get(s, 0.5) for s in retained) / len(retained), 3
        ),
        "bloom_factor": adjusted_factor,
        "mood": new_mood,
        "belief_resonance": getattr(bloom, "belief_resonance", {}),
    }

    owl_log(f"[Mutation] 🧬 {bloom.seed_id} salvaged → mutant ({len(retained)} sentences, mood={new_mood}, factor={adjusted_factor})")
    return mutant_seed
