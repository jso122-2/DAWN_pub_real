# drift_logger.py

import os
import csv
from datetime import datetime

log_dir = "logs/drift_logs"
os.makedirs(log_dir, exist_ok=True)

def log_drift(seed_id, delta_vector, tick):
    """
    Logs semantic drift per bloom over time.
    """
    log_path = os.path.join(log_dir, f"{seed_id}_drift.csv")
    exists = os.path.isfile(log_path)

    with open(log_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["tick", "timestamp", "delta_vector"])
        writer.writerow([tick, datetime.now().isoformat(), delta_vector])

    print(f"[DriftLog] 🌀 Logged drift for {seed_id}: Δ={delta_vector:.3f}")
