import os
import csv
from datetime import datetime

LOG_PATH = "juliet_flowers/field_logs/field_snapshot.csv"
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

FIELD_HEADERS = [
    "tick_id",
    "timestamp",
    "zone",
    "pulse_heat",
    "scup_score",
    "entropy_score",
    "bloom_count",
    "interval",
    "mood_pressure"
]


def init_field_log():
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(FIELD_HEADERS)
        print("[FieldLogger] 🆕 Initialized pulse field log.")


def log_field_snapshot(tick_id, zone, pulse_heat, scup_score, entropy_score, bloom_count, interval, mood_pressure):
    timestamp = datetime.utcnow().isoformat()

    row = [
        tick_id,
        timestamp,
        zone,
        round(pulse_heat, 3),
        round(scup_score, 3),
        round(entropy_score, 3),
        bloom_count,
        round(interval, 3),
        round(mood_pressure, 3)
    ]

    with open(LOG_PATH, mode="a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(row)

    print(f"[FieldLogger] ✅ Logged tick {tick_id} → zone: {zone}, SCUP: {scup_score:.3f}, pulse: {pulse_heat:.2f}")
