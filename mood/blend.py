
from collections import Counter

# Mood blend priority table (can be expanded)
MOOD_HIERARCHY = [
    "joyful", "focused", "reflective", "anxious", "sad"
]

def blend_moods(source_blooms):
    moods = [bloom.get("mood", "undefined") for bloom in source_blooms]
    mood_counts = Counter(moods)

    if not mood_counts:
        return "undefined"

    # Find highest priority mood by presence in source set
    for mood in MOOD_HIERARCHY:
        if mood in mood_counts:
            return mood

    return moods[0]  # fallback
