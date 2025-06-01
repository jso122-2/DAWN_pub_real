import json

MoodWeight = {
    "anxious": 0.85,
    "curious": 1.10,
    "reflective": 1.00,
    "excited": 1.25,
    "calm": 0.90
}

def adjust_weight_by_emotion(weight_map, mood_map):
    adjusted = {}
    for seed, weight in weight_map.items():
        mood = mood_map.get(seed, "reflective")
        multiplier = MoodWeight.get(mood, 1.0)
        adjusted[seed] = round(weight * multiplier, 4)
    return adjusted

def run_emotional_weight():
    with open("juliet_flowers/index/weight_map.json", "r", encoding="utf-8") as f:
        weights = json.load(f)
    with open("juliet_flowers/index/mood_charge.json", "r", encoding="utf-8") as f:
        moods = json.load(f)

    adjusted = adjust_weight_by_emotion(weights, moods)
    with open("juliet_flowers/index/emotion_weight_map.json", "w", encoding="utf-8") as f:
        json.dump(adjusted, f, indent=2)

    print("[Emotion] 🎭 Emotional weight adjustment complete.")

if __name__ == "__main__":
    run_emotional_weight()
