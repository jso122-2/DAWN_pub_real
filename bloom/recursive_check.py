
def is_recursive_eligible(bloom):
    return "synthesis-" in bloom.get("seed_id", "") and bloom.get("lineage_depth", 0) < 8
