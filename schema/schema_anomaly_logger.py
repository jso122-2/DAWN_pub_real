# /core/schema_anomaly_logger.py

import os
from datetime import datetime

LOG_PATH = "logs/schema_anomalies.log"

def log_anomaly(label, message):
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] [{label}] {message}\n"
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(log_entry)
    print(f"[SCHEMA] ⚠️ {message}")
