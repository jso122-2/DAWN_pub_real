# /tracers/tracer_diplomacy.py

from owl.owl_tracer_log import owl_log

# Simple priority matrix: higher value = more influence
TRACER_PRIORITY = {
    "Owl": 3,      # Memory integrity, suppression, entropy analysis
    "Spider": 2,   # Reactivation, thread tension mapping
    "Bee": 1,      # Reinforcement, positivity, recall
    "Ant": 1,      # Utility, logging, payload packing
    "Whale": 2,    # Depth tracking, cluster dynamics
    "Crow": 2,     # Surprise, alertness, watch states
    "Stalk": 0     # Neutral delivery system
}

def resolve_tracer_conflict(bloom, tracer_signals):
    """
    Resolves multiple tracer suggestions on a bloom.
    - tracer_signals: list of tuples (tracer_name, action, weight)
    Returns: selected action or hybrid plan
    """
    action_votes = {}
    log_summary = []

    for tracer_name, action, weight in tracer_signals:
        priority = TRACER_PRIORITY.get(tracer_name, 0)
        score = weight * priority
        action_votes[action] = action_votes.get(action, 0) + score
        log_summary.append(f"{tracer_name} → {action} ({score:.2f})")

    # Sort by cumulative weighted score
    sorted_actions = sorted(action_votes.items(), key=lambda x: -x[1])

    final_action = sorted_actions[0][0] if sorted_actions else "noop"
    owl_log(f"[Diplomacy] 🕸️ Conflict on {bloom.seed_id} resolved: {final_action} ← " + " | ".join(log_summary))

    return final_action
