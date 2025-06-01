# /rhizome/trail_tracker.py

def validate_path(bloom):
    """
    Placeholder: checks for logical semantic continuity.
    Later use embedding path diff + rebloom tree delta.
    """
    lineage = bloom.get_lineage()
    if not lineage:
        return {"valid": False, "reason": "No ancestry"}
    if bloom.seed_id in [a.seed_id for a in lineage]:
        return {"valid": False, "reason": "Loop detected", "loop": True}
    return {"valid": True}


def is_dead_end(bloom):
    """
    If bloom has no children, low entropy, and no rebloom pattern — it's a dead end.
    """
    return bloom.lineage_depth > 3 and bloom.entropy_score < 0.3


def reinforce_path(bloom):
    """
    Log reinforcement — later apply reinforcement weight for prioritization.
    """
    if not hasattr(bloom, "reinforcement_log"):
        bloom.reinforcement_log = []
    bloom.reinforcement_log.append("Path validated and reinforced by Ant")
