
import os
import time
from collections import defaultdict

LOG_PATH = "juliet_flowers/cluster_report/tracer_log.txt"

def log_tracer_activation(name, sigil, score, label):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    timestamp = time.time()
    line = f"[{timestamp:.2f}] [TRACER] {name} — responded to {sigil} with priority {score:.2f} ({label.upper()})\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())

def compute_tracer_urgency():
    if not os.path.exists(LOG_PATH):
        return 0.0

    urgency_scores = []
    now = time.time()
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                ts = float(line.split(']')[0].strip('['))
                if now - ts < 300:  # last 5 min
                    score_str = line.split("priority ")[1].split(" ")[0]
                    urgency_scores.append(float(score_str))
            except:
                continue

    if not urgency_scores:
        return 0.0
    return round(sum(urgency_scores) / len(urgency_scores), 3)
