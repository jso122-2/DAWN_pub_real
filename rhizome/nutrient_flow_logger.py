import os
import csv
from datetime import datetime
from collections import defaultdict

# === Paths & Constants ===
BASE_LOG_DIR = "logs/mycelium_logs"
DEFAULT_LOG_PATH = os.path.join(BASE_LOG_DIR, "nutrient_flow_log.csv")

os.makedirs(BASE_LOG_DIR, exist_ok=True)

HEADERS = ["tick_id", "from_node", "to_node", "nutrient_type", "amount"]

# === Global Session Counters ===
NUTRIENT_COUNTER = defaultdict(float)

# === Internal: Ensure header once ===
def _ensure_header(path):
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)

# === Core Logger ===
def log_nutrient_transfer(tick_id, from_node, to_node, nutrient_type, amount, path=DEFAULT_LOG_PATH, flush=False):
    """
    Log a nutrient flow event.
    Supports optional flushing and path override.
    """
    _ensure_header(path)
    rounded = round(amount, 4)

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([tick_id, from_node, to_node, nutrient_type, rounded])

    NUTRIENT_COUNTER[nutrient_type] += rounded

    if flush:
        f.flush()

    print(f"[NutrientLog] 🌱 Tick {tick_id} | {from_node} → {to_node} | {nutrient_type} = {rounded:.4f}")

# === Utility: Save session summary ===
def save_nutrient_summary(path=os.path.join(BASE_LOG_DIR, "nutrient_session_summary.csv")):
    """
    Dump a summary of nutrient totals after a run.
    """
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nutrient_type", "total_transferred"])
        for nutrient, total in NUTRIENT_COUNTER.items():
            writer.writerow([nutrient, round(total, 4)])

    print(f"[NutrientLog] 🧾 Saved session summary to {path}")

# === Optional: Timestamped session log path ===
def get_timestamped_log_path():
    stamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    return os.path.join(BASE_LOG_DIR, f"nutrient_log_{stamp}.csv")
