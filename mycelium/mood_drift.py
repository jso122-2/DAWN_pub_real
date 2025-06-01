import matplotlib.pyplot as plt
import json
import os
from math import sqrt
from datetime import datetime

# --- Mood Position Map (semantic 2D embedding) ---
MOOD_COORDS = {
    "happy": (1, 1),
    "neutral": (0, 0),
    "sad": (-1, -1),
    "angry": (-1, 1),
    "anxious": (0, -1),
    "calm": (1, 0),
    "excited": (1, 2),
    "tired": (-1, 0),
    "curious": (0.5, 1),
    "reflective": (0.2, -0.2),
    "none": (0, 0)  # fallback
}

DRIFT_LOG_PATH = "juliet_flowers/cluster_report/mood_drift_log.json"

# --- Core Math ---
def mood_distance(m1, m2):
    p1 = MOOD_COORDS.get(m1, MOOD_COORDS["none"])
    p2 = MOOD_COORDS.get(m2, MOOD_COORDS["none"])
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def normalize_dist(d, max_dist=3.0):
    return min(d / max_dist, 1.0)

def compute_mood_drift(current_mood, previous_mood):
    dist = mood_distance(current_mood, previous_mood)
    drift = normalize_dist(dist)
    log_mood_drift(previous_mood, current_mood, drift)
    return drift

# --- Logging for visual + reflex hooks ---
def log_mood_drift(prev, curr, drift):
    os.makedirs(os.path.dirname(DRIFT_LOG_PATH), exist_ok=True)
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "from": prev,
        "to": curr,
        "drift": round(drift, 3)
    }
    try:
        if os.path.exists(DRIFT_LOG_PATH):
            with open(DRIFT_LOG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
        data.append(entry)
        with open(DRIFT_LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(data[-100:], f, indent=2)
    except Exception as e:
        print(f"[MoodDrift] ⚠️ Failed to log drift: {e}")

# --- Reflex Visualization ---
def render_mood_drift_map():
    """
    Render the mood drift vector field from recent logs.
    """
    try:
        with open(DRIFT_LOG_PATH, "r", encoding="utf-8") as f:
            entries = json.load(f)
    except Exception as e:
        print(f"[MoodDrift] ❌ No drift log found: {e}")
        return

    plt.figure(figsize=(8, 6))
    for entry in entries:
        f, t = entry["from"], entry["to"]
        p1 = MOOD_COORDS.get(f, (0, 0))
        p2 = MOOD_COORDS.get(t, (0, 0))
        plt.arrow(p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1],
                  head_width=0.05, length_includes_head=True,
                  alpha=0.6, color="blue")

    # Mood labels
    for mood, (x, y) in MOOD_COORDS.items():
        plt.text(x + 0.05, y + 0.05, mood, fontsize=9, alpha=0.7)

    plt.title("🌀 Mood Drift Vector Field")
    plt.grid(True)
    plt.axis("equal")
    os.makedirs("juliet_flowers/cluster_report", exist_ok=True)
    out = "juliet_flowers/cluster_report/mood_drift_map.png"
    plt.savefig(out)
    print(f"[MoodDrift] ✅ Saved mood drift field → {out}")
    plt.close()
