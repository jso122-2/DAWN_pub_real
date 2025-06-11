import json
import os
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def compute_charge(weight, urgency_factor=1.0, mood_multiplier=1.0):
    raw = weight * urgency_factor * mood_multiplier
    return round(sigmoid(raw), 4)

def load_weights(path="juliet_flowers/index/weight_map.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_mood_modifiers(path="juliet_flowers/index/mood_charge.json"):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_charge_map(charge_map, path="juliet_flowers/index/charge_map.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(charge_map, f, indent=2)

def run_charge_engine():
    weights = load_weights()
    mood_mod = load_mood_modifiers()
    urgency_factor = 1.0

    charge_map = {}
    for seed, weight in weights.items():
        mood_mult = mood_mod.get(seed, 1.0)
        charge_map[seed] = compute_charge(weight, urgency_factor, mood_mult)

    save_charge_map(charge_map)
    print("[ChargeEngine] ⚡ Semantic charge map saved to charge_map.json")

if __name__ == "__main__":
    run_charge_engine()
