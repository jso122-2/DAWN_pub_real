# /schema/rebloom_summary.py

import os
import csv
from datetime import datetime

LOG_PATH = "logs/rebloom_summary_log.csv"
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

# Write headers once
if not os.path.exists(LOG_PATH):
    with open(LOG_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["tick_id", "seed_id", "source", "reason", "ancestry_tag", "reinforcement_count"])

def log_rebloom_trigger(tick_id, bloom, source="broadcast", reason="reinforcement"):
    ancestry = getattr(bloom, "rebloom_tag", "untagged")
    reinforce = getattr(bloom, "reinforcement_count", 0)

    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            tick_id, bloom.seed_id, source, reason, ancestry, reinforce
        ])
