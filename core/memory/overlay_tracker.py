# /core/overlay_tracker.py

import os
from datetime import datetime

LOG_PATH = "logs/overlay_events.log"

def log_overlay_event(bloom_id, overlay_symbol, source, reason, tracer=None):
    """
    Logs any visual overlay applied to a bloom (e.g. ❌, 💧, 🔥).
    
    bloom_id   → ID of the bloom receiving the overlay
    overlay_symbol → Emoji or string applied (e.g. ❌, 🔥)
    source     → Who applied it ("Owl", "Crow", "user", "DAWN", etc.)
    reason     → Short string explanation (e.g. "SCUP < 0.3", "contradiction loop")
    tracer     → Optional: name of tracer or module responsible
    """
    timestamp = datetime.now().isoformat()
    log_entry = (
        f"[{timestamp}] {overlay_symbol} applied to {bloom_id} "
        f"by {source} ({'via ' + tracer if tracer else 'direct'}) | reason: {reason}\n"
    )
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(log_entry)
    print(log_entry.strip())  # Optional live echo
