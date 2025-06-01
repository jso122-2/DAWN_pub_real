# /core/mood.py

def calculate_mood_urgency(mood_state):
    """Weighted urgency by mood proportion."""
    weights = {"stressed": 0.9, "reflective": 0.6, "resilient": 0.3}
    return sum(weights.get(m, 0.5) * v for m, v in mood_state.items())
