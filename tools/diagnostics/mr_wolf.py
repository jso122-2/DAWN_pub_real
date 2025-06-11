
import os
import json
import time
from datetime import datetime

WOLF_LOG_PATH = "diagnostics/wolf_log.json"
SCUP_HISTORY = []

def log_wolf_event(state, metrics):
    os.makedirs(os.path.dirname(WOLF_LOG_PATH), exist_ok=True)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "state": state,
        "metrics": metrics
    }
    with open(WOLF_LOG_PATH, "a", encoding="utf-8") as f:
        json.dump(log_entry, f)
        f.write("\n")
    print(f"[Mr Wolf] 🔍 {state.upper()} — logged at {log_entry['timestamp']}")

def monitor_scup(scup_value, shi=1.0, tracer_divergence=0.0, tick=None):
    SCUP_HISTORY.append(scup_value)
    if len(SCUP_HISTORY) > 10:
        SCUP_HISTORY.pop(0)

    avg_scup = sum(SCUP_HISTORY) / len(SCUP_HISTORY)
    mode = "observe"

    if scup_value < 0.25 and avg_scup < 0.3:
        mode = "predictive"

    if scup_value < 0.15 and shi < 0.6 and tracer_divergence > 0.3:
        mode = "lockdown"

    metrics = {
        "tick": tick,
        "scup": scup_value,
        "avg_scup": round(avg_scup, 3),
        "shi": shi,
        "tracer_divergence": tracer_divergence,
        "history": SCUP_HISTORY
    }

    log_wolf_event(mode, metrics)

    if mode == "lockdown":
        from codex.sigils import invoke_sigil
        invoke_sigil("/X-")

    return mode
