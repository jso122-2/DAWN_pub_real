def recommend_rebloom_candidates(blooms):
    """
    Return top candidates based on:
    - high sentiment alignment
    - low entropy
    - mid-to-deep lineage (stable but still generative)
    """
    ranked = []

    for bloom in blooms:
        mood = getattr(bloom, "mood", "neutral")
        entropy = getattr(bloom, "entropy_score", 0.5)
        depth = getattr(bloom, "lineage_depth", 0)

        if mood in ["curious", "reflective"] and entropy < 0.3 and 1 <= depth <= 4:
            score = (1 - entropy) + (0.3 * depth)
            ranked.append((bloom.seed_id, round(score, 3)))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked[:5]
