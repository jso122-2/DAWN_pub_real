
def stable_mood_transition(prev_mood, target_mood):
    transitions = {
        'calm': ['reflective', 'curious'],
        'reflective': ['curious', 'calm'],
        'curious': ['reflective', 'anxious', 'calm'],
        'anxious': ['curious', 'calm']
    }
    if target_mood in transitions.get(prev_mood, []):
        return target_mood
    return prev_mood  # Explicitly remain stable if invalid transition

print("[MoodStability] ✅ Mood stability tuning initialized.")
