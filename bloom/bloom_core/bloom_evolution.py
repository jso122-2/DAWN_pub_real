# /bloom_core/bloom_evolution.py

import math

def evolve_bloom_shape(bloom):
    """
    Recursively evolve bloom shape based on:
    - bloom_factor
    - lineage_depth
    - entropy_score
    """
    try:
        factor = getattr(bloom, "bloom_factor", 1.0)
        depth = getattr(bloom, "lineage_depth", 0)
        entropy = getattr(bloom, "entropy_score", 0.0)
        base_shape = getattr(bloom, "shape_signature", [1.0, 1.0])

        if factor <= 0 or math.isnan(factor):
            factor = 1.0
            log(bloom, f"⚠️ Invalid bloom_factor, defaulting to 1.0")

        # Recursive modulation logic
        mod = (factor * 0.7) + (depth * 0.1) - (entropy * 0.6)
        mod = max(0.1, min(mod, 2.5))
        evolved = [round(s * mod, 4) for s in base_shape]

        if any(math.isnan(v) or v < 0 for v in evolved):
            log(bloom, "❌ Shape evolution anomaly. Reverting to base.")
            return base_shape

        bloom.shape_signature = evolved
        bloom.evolution_mod = round(mod, 4)
        log(bloom, f"🌸 Shape evolved → {evolved} (mod={mod:.3f})")
        return evolved

    except Exception as e:
        log(bloom, f"🔥 Shape evolution failed: {str(e)}")
        return getattr(bloom, "shape_signature", [1.0, 1.0])

def lock_bloom_evolution(bloom):
    """
    Finalizes and locks bloom evolution if stable.
    Uses a composite stability index to assign shape_state.
    """
    try:
        factor = getattr(bloom, "bloom_factor", 1.0)
        depth = getattr(bloom, "lineage_depth", 0)
        entropy = getattr(bloom, "entropy_score", 0.5)

        stability = (factor * 0.6) + ((1 / (1 + depth)) * 0.3) + ((1 - entropy) * 0.1)
        bloom.stability_index = round(stability, 3)

        if stability > 0.85:
            bloom.shape_state = "crystal"
        elif stability > 0.6:
            bloom.shape_state = "spiral"
        elif stability > 0.4:
            bloom.shape_state = "wave"
        else:
            bloom.shape_state = "unstable"

        bloom.evolution_locked = True
        log(bloom, f"🔒 Bloom evolution locked as '{bloom.shape_state}' (stability={bloom.stability_index})")
        return bloom.shape_state

    except Exception as e:
        bloom.shape_state = "undefined"
        bloom.evolution_locked = False
        log(bloom, f"⚠️ Failed to evolve bloom shape: {str(e)}")
        return "error"

def log(bloom, message):
    """Appends to activity log regardless of bloom type."""
    if hasattr(bloom, "activity_log"):
        bloom.activity_log.append(message)
    elif isinstance(bloom, dict):
        bloom.setdefault("activity_log", []).append(message)
