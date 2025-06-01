from owl.owl_tracer_log import owl_log

def suppress_bloom_if_unstable(bloom):
    """
    Suppress bloom if unstable traits are detected.
    This includes high entropy, low trust, poor conversion feedback,
    and mood/lineage red flags.
    """

    suppression_reasons = []

    # Unified accessor: fallback if passed bloom is a dict
    def get(key, default=None):
        return getattr(bloom, key, None) if hasattr(bloom, key) else bloom.get(key, default)

    seed = get("seed_id", "unknown")
    entropy = get("entropy_score", 1.0)
    suppressions = get("suppressions", 0)
    trust = get("trust_score", 1.0)
    feedback_flags = get("feedback_flags", {})
    mood = get("mood", "undefined")
    depth = get("lineage_depth", 0)

    # 🚨 High entropy
    if entropy > 0.75:
        suppression_reasons.append("entropy_spike")

    # 🔁 Repeated suppressions
    if suppressions > 2:
        suppression_reasons.append("repeat_flagged")

    # ⚠️ Low trust zone
    if trust < 0.3:
        suppression_reasons.append("low_trust")

    # 📉 Explicit conversion failure
    if feedback_flags.get("poor_conversion"):
        suppression_reasons.append("conversion_failure")

    # 🧬 Excessive lineage depth (possible drift or staleness)
    if depth >= 12:
        suppression_reasons.append("drift_depth")

    # 😖 Mood filters (optional: we can auto-mute certain unstable mood pairings)
    if mood in ["anxious", "fatalistic"] and entropy > 0.7:
        suppression_reasons.append("mood_instability")

    # 📦 Log and suppress if any flags triggered
    if suppression_reasons:
        # Apply suppression metadata back onto the bloom (works for dict or object)
        if isinstance(bloom, dict):
            bloom["suppressed"] = True
            bloom["suppression_reason"] = suppression_reasons
        else:
            bloom.suppressed = True
            bloom.suppression_reason = suppression_reasons

        owl_log(f"[Suppressed] 🚫 {seed} blocked ({', '.join(suppression_reasons)})")
        return True

    return False
