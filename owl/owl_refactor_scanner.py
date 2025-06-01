def suggest_refactors(blooms, entropy_cutoff=0.5, shape_set={"unstable", "wave"}):
    """
    Returns list of bloom IDs recommended for refactor.
    Criteria:
    - Not sealed
    - Shape is semi-coherent but not locked
    - Moderate entropy (not chaotic, not crystal)
    """
    candidates = []
    for bloom in blooms:
        shape = getattr(bloom, "shape_state", "unknown")
        entropy = getattr(bloom, "entropy_score", 0.5)
        locked = getattr(bloom, "evolution_locked", False)
        if not locked and shape in shape_set and entropy < entropy_cutoff:
            candidates.append((bloom.seed_id, round(entropy, 3), shape))

    print("[Owl] 🔁 Refactor Candidates:")
    for sid, ent, shp in candidates:
        print(f"  • {sid} | entropy={ent}, shape={shp}")
    return candidates
