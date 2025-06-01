# compute_mood_drift.py

from math import sqrt

# Define 2D mood space positions
MOOD_COORDS = {
    "happy": (1, 1),
    "neutral": (0, 0),
    "sad": (-1, -1),
    "angry": (-1, 1),
    "anxious": (0, -1),
    "calm": (1, 0),
    "excited": (1, 2),
    "tired": (-1, 0),
    "none": (0, 0)  # fallback
}

def mood_distance(m1, m2):
    p1 = MOOD_COORDS.get(m1, MOOD_COORDS["none"])
    p2 = MOOD_COORDS.get(m2, MOOD_COORDS["none"])
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def normalize_dist(d, max_dist=3.0):
    return min(d / max_dist, 1.0)  # caps at 1.0

def compute_mood_drift(current_mood, previous_mood):
    dist = mood_distance(current_mood, previous_mood)
    drift = normalize_dist(dist)
    return drift
