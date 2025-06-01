import os
import json
import pandas as pd
from datetime import datetime

TICK_FILE = "tick_state.json"
ZONE_OVERLAY_FILE = "juliet_flowers/cluster_report/zone_overlay_log.csv"

# 🧠 Unified tick record
TICK_STATE = {
    "tick": 0,
    "timestamp": None,
    "zone": None,
    "pulse": None
}

# 🔄 Load latest tick from file
def load_tick():
    if not os.path.exists(TICK_FILE):
        return 0
    with open(TICK_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("tick", 0)

# 💾 Save tick metadata
def save_tick(tick, zone=None, pulse=None):
    TICK_STATE["tick"] = tick
    TICK_STATE["timestamp"] = datetime.utcnow().isoformat()
    TICK_STATE["zone"] = zone
    TICK_STATE["pulse"] = pulse

    from semantic.sigil_ring import get_total_drift_entropy
    drift = round(get_total_drift_entropy(), 4)

    with open(ZONE_OVERLAY_FILE, "a", encoding="utf-8") as log:
        log.write(f"{tick},{zone},{pulse},{drift}\n")


# ⏱️ Emit next tick and persist
def emit_tick(zone=None, pulse=None):
    tick = load_tick() + 1
    save_tick(tick, zone=zone, pulse=pulse)
    print(f"⏱️ Tick emitted | Tick: {tick} | Zone: {zone} | Pulse: {pulse}")
    return tick

# 📈 Access current tick value
def current_tick():
    return TICK_STATE.get("tick", 0)

# 📊 Load full overlay log
def load_zone_overlay():
    try:
        df = pd.read_csv(ZONE_OVERLAY_FILE, names=["tick", "zone", "pulse"], encoding="utf-8")
        return df
    except Exception as e:
        print(f"[Pulse] ❌ Failed to load overlay log: {e}")
        return pd.DataFrame()

# 🔁 Return last N zone pulses
def get_recent_zone_window(window=10):
    df = load_zone_overlay()
    if df.empty:
        return []
    return df.tail(window).to_dict("records")
