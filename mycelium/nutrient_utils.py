import json
import os

def get_nutrient_heat(depth: int, normalize_by: int = 10, fallback: float = 0.0):
    path = "logs/mycelium_logs/nutrient_log.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            nutrient_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"[Mycelium] ⚠️ Missing or invalid nutrient log at {path}")
        return fallback

    count = nutrient_data.get(str(depth), 0)
    return min(1.0, count / normalize_by)
