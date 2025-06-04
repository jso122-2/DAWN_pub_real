import os
from datetime import datetime

def log_nutrient_path(seed_id: str, mood: str, signal_type: str, pressure: float):
    now = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    log_dir = f"mycelium_logs/daily/{datetime.now().strftime('%Y-%m-%d')}"
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, f"{seed_id}_{now}.log")
    with open(log_path, "w") as f:
        f.write(f"[NutrientPath]\n")
        f.write(f"Seed: {seed_id}\nMood: {mood}\nSignal: {signal_type}\nPressure: {pressure:.2f}\n")
        f.write(f"Timestamp: {now}\n")

    print(f"[Mycelium] 🌱 Nutrient path logged: {log_path}")
