"""
🧠 Parmenides — Thread Gatekeeper and Reflective Sentinel

- Controls thought admission via parmenides_gate()
- Supports bulk thread handling (parmenides_gate_all)
- Tracks gate rationale (gate_rationale_log.json)
- Allows resurfacing of gated threads
- Can visualize the emotional weight of blocked thought using avatar rendering
"""

import json
import os
from datetime import datetime

GATE_LOG = "juliet_flowers/cluster_report/gate_rationale_log.json"
GATED_QUEUE = []

# -- CORE SINGLE BLOOM EVALUATION --

def parmenides_gate(bloom, current_zone, schema_state=None, verbose=True):
    mood = getattr(bloom, "mood", "neutral")
    entropy = getattr(bloom, "entropy_score", 0.5)
    depth = getattr(bloom, "lineage_depth", 0)
    urgency = getattr(bloom, "bloom_factor", 1.0)
    seed = getattr(bloom, "seed_id", "unknown")

    sensitive = mood in ["vulnerable", "exposed", "anxious"]
    volatile = entropy >= 0.7
    emergent = depth >= 6
    overactive = urgency >= 2.0

    held = False
    reasons = []

    if current_zone == "🔴 surge" and (sensitive or volatile or emergent):
        held, reasons = True, ["schema surge"]
    elif current_zone == "🟡 active" and (sensitive or volatile):
        held, reasons = True, ["mood-volatility conflict"]
    elif current_zone != "🟢 calm" and overactive:
        held, reasons = True, ["overactive urgency"]

    if held:
        bloom.thread_status = "held"
        rationale = f"Held by Parmenides due to {', '.join(reasons)}"
        bloom.activity_log.append(f"🛑 {rationale}")
        GATED_QUEUE.append(bloom)
        log_rationale(seed, current_zone, mood, entropy, depth, urgency, reasons)
        if verbose: print(f"[Parmenides] 🛑 {seed} held → {reasons}")
        return False

    bloom.thread_status = "admitted"
    bloom.activity_log.append(f"✅ Passed Parmenides (zone={current_zone})")
    if verbose: print(f"[Parmenides] ✅ {seed} admitted")
    return True

# -- BULK EVALUATION --

def parmenides_gate_all(blooms, current_zone, verbose=True):
    """
    Process a list of blooms. Returns [admitted], leaves held in GATED_QUEUE.
    """
    admitted = []
    for bloom in blooms:
        if parmenides_gate(bloom, current_zone, verbose=verbose):
            admitted.append(bloom)
    return admitted

# -- GATE REASON LOGGING --

def log_rationale(seed_id, zone, mood, entropy, depth, urgency, reasons):
    log_entry = {
        "seed_id": seed_id,
        "zone": zone,
        "mood": mood,
        "entropy_score": entropy,
        "lineage_depth": depth,
        "bloom_factor": urgency,
        "reason": reasons,
        "timestamp": datetime.now().isoformat()
    }

    if os.path.exists(GATE_LOG):
        with open(GATE_LOG, "r", encoding="utf-8") as f:
            log_data = json.load(f)
    else:
        log_data = []

    log_data.append(log_entry)

    with open(GATE_LOG, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)

# -- RESURFACE HELD THREADS --

def resurface_gated_threads(current_zone, verbose=True):
    """
    Try to re-admit held threads once schema calms.
    """
    global GATED_QUEUE
    released = []
    remaining = []

    for bloom in GATED_QUEUE:
        if parmenides_gate(bloom, current_zone, verbose=verbose):
            released.append(bloom)
        else:
            remaining.append(bloom)

    GATED_QUEUE = remaining
    if verbose:
        print(f"[Parmenides] 🔁 Resurfaced {len(released)} threads.")
    return released

# -- AVATAR RENDER (TEXT) --

def parmenides_avatar():
    """
    Returns a symbolic snapshot of the gate's emotional state.
    """
    total = len(GATED_QUEUE)
    if total == 0:
        return "🧘 Parmenides is calm. All thoughts flowing freely."

    sample = GATED_QUEUE[-1]
    return f"""
    🧠 Parmenides Avatar
    --------------------------
    Held Thoughts     : {total}
    Last Blocked      : {sample.seed_id}
    Mood              : {sample.mood}
    Entropy           : {sample.entropy_score:.2f}
    Depth             : {sample.lineage_depth}
    Urgency           : {sample.bloom_factor:.2f}
    --------------------------
    Reflection continues until calm returns.
    """

# -- TEST CLI --

if __name__ == "__main__":
    print(parmenides_avatar())
