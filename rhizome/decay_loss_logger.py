# /rhizome/decay_loss_logger.py

import os
import csv

LOG_PATH = "logs/decay_loss_log.csv"
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

# Header setup
if not os.path.exists(LOG_PATH):
    with open(LOG_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "tick_id", "from", "to", "nutrient_type",
            "initial_strength", "final_strength", "total_decay"
        ])

def log_decay_loss(tick_id, from_seed, to_seed, nutrient_type, initial, final):
    decay = round(initial - final, 4)
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            tick_id, from_seed, to_seed, nutrient_type,
            round(initial, 4), round(final, 4), decay
        ])
