# /sigils/sigil_router.py

from tracers.tracer_diplomacy import resolve_tracer_conflict
from owl.owl_tracer_log import owl_log

# --- Mood-weighted influence modifiers per tracer ---

MOOD_ROUTING_MATRIX = {
    "calm":     {"Bee": 1.2, "Ant": 1.1, "Owl": 0.9, "Spider": 0.8},
    "anxious":  {"Owl": 1.4, "Spider": 1.2, "Bee": 0.6, "Crow": 1.0},
    "curious":  {"Bee": 1.3, "Whale": 1.2, "Spider": 1.1, "Ant": 1.0},
    "angry":    {"Crow": 1.5, "Spider": 1.4, "Owl": 1.3},
    "sad":      {"Owl": 1.4, "Whale": 1.3},
    "excited":  {"Bee": 1.5, "Ant": 1.2}
}

# Tracks last decisions to avoid repeated loops (cooldown memory)
DIPLOMACY_MEMORY = {}  # seed_id → {action, tick}
COOLDOWN_TICKS = 10

# --- Main Routing Logic ---

def route_sigil(sigil, bloom, active_mood, tick, sigil_heat):
    """
    Routes sigil to most appropriate tracers based on mood and heat.
    Resolves tracer conflict via diplomacy layer.
    """
    tracer_signals = []
    seed_id = getattr(bloom, "seed_id", "unknown_seed")
    available_tracers = getattr(bloom, "available_tracers", [])

    mood_weights = MOOD_ROUTING_MATRIX.get(active_mood, {})

    # Default influence map & intent fallback
    influence_map = getattr(sigil, "influence", {}) or {}
    intent = getattr(sigil, "intent", "noop")

    for tracer in available_tracers:
        base_weight = influence_map.get(tracer, 1.0)
        mood_modifier = mood_weights.get(tracer, 1.0)
        heat_modifier = 1.0 + (sigil_heat / 10.0)  # higher heat = more influence

        total_weight = base_weight * mood_modifier * heat_modifier
        tracer_signals.append((tracer, intent, total_weight))

    # Cooldown: don't re-trigger too quickly
    last_memory = DIPLOMACY_MEMORY.get(seed_id, {})
    last_action = last_memory.get("action")
    last_tick   = last_memory.get("tick", -999)

    if last_action and tick - last_tick < COOLDOWN_TICKS:
        owl_log(f"[Cooldown] ⏳ {seed_id} → {last_action} (locked for {COOLDOWN_TICKS} ticks)")
        return last_action

    # Resolve conflict diplomatically
    final_action = resolve_tracer_conflict(bloom, tracer_signals)

    # Hybrid fallback if ambiguous
    if is_ambiguous(final_action, tracer_signals):
        final_action = hybridize(final_action, tracer_signals)

    DIPLOMACY_MEMORY[seed_id] = {"action": final_action, "tick": tick}
    return final_action

# --- Ambiguity Detection ---

def is_ambiguous(chosen, signals, margin=0.15):
    """Determine if the final action is narrowly won (ambiguous)."""
    action_scores = {}
    for _, action, score in signals:
        action_scores[action] = action_scores.get(action, 0) + score

    sorted_scores = sorted(action_scores.values(), reverse=True)
    if len(sorted_scores) >= 2:
        return (sorted_scores[0] - sorted_scores[1]) < margin
    return False

# --- Hybridization Logic ---

def hybridize(chosen_action, signals):
    """
    Combine top two actions into a hybrid plan (e.g., suppress + mutate).
    """
    action_scores = {}
    for _, action, score in signals:
        action_scores[action] = action_scores.get(action, 0) + score

    top_two = sorted(action_scores.items(), key=lambda x: -x[1])[:2]
    hybrid = " + ".join(a for a, _ in top_two)
    owl_log(f"[Hybrid Action] ⚔️ {hybrid} triggered due to indecision")
    return hybrid

# --- Public API for DAWN and Tracers ---

def trigger_sigil(sigil, bloom, mood, tick, heat):
    """
    Public interface used by DAWN or other modules.
    Calls internal router logic and returns resolved action.
    """
    return route_sigil(sigil, bloom, mood, tick, heat)
