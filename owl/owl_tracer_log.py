import json
import os
from datetime import datetime

LOG_PATH = "owl/owl_log.json"

def owl_log(message: str):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "message": message
    }

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(entry)

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)

    print(f"[OwlLog] {message}")
