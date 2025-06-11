import os
import json
import pandas as pd
from datetime import datetime

TICK_FILE = "tick_state.json"
ZONE_OVERLAY_FILE = "juliet_flowers/cluster_report/zone_overlay_log.csv"

class TickEmitter:
    """Core tick emission system for DAWN"""
    
    def __init__(self):
        self.tick_state = {
            "tick": 0,
            "timestamp": None,
            "zone": None,
            "pulse": None
        }
        self._load_initial_state()
        
    def _load_initial_state(self):
        """Load the initial tick state"""
        if os.path.exists(TICK_FILE):
            with open(TICK_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tick_state.update(data)
    
    def emit_tick(self, zone=None, pulse=None):
        """Emit the next tick and persist state"""
        self.tick_state["tick"] += 1
        self.tick_state["timestamp"] = datetime.utcnow().isoformat()
        self.tick_state["zone"] = zone
        self.tick_state["pulse"] = pulse
        
        # Save state
        with open(TICK_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tick_state, f, indent=2)
            
        # Log to overlay
        try:
            from semantic.sigil_ring import get_total_drift_entropy
            drift = round(get_total_drift_entropy(), 4)
            
            with open(ZONE_OVERLAY_FILE, "a", encoding="utf-8") as log:
                log.write(f"{self.tick_state['tick']},{zone},{pulse},{drift}\n")
        except Exception as e:
            print(f"[Pulse] ❌ Failed to log overlay: {e}")
            
        print(f"⏱️ Tick emitted | Tick: {self.tick_state['tick']} | Zone: {zone} | Pulse: {pulse}")
        return self.tick_state["tick"]
    
    def current_tick(self):
        """Get current tick value"""
        return self.tick_state["tick"]
    
    def load_zone_overlay(self):
        """Load the full zone overlay log"""
        try:
            df = pd.read_csv(ZONE_OVERLAY_FILE, names=["tick", "zone", "pulse"], encoding="utf-8")
            return df
        except Exception as e:
            print(f"[Pulse] ❌ Failed to load overlay log: {e}")
            return pd.DataFrame()
    
    def get_recent_zone_window(self, window=10):
        """Get the last N zone pulses"""
        df = self.load_zone_overlay()
        if df.empty:
            return []
        return df.tail(window).to_dict("records")

# For backward compatibility
TICK_STATE = {
    "tick": 0,
    "timestamp": None,
    "zone": None,
    "pulse": None
}

def load_tick():
    if not os.path.exists(TICK_FILE):
        return 0
    with open(TICK_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("tick", 0)

def save_tick(tick, zone=None, pulse=None):
    TICK_STATE["tick"] = tick
    TICK_STATE["timestamp"] = datetime.utcnow().isoformat()
    TICK_STATE["zone"] = zone
    TICK_STATE["pulse"] = pulse

    from semantic.sigil_ring import get_total_drift_entropy
    drift = round(get_total_drift_entropy(), 4)

    with open(ZONE_OVERLAY_FILE, "a", encoding="utf-8") as log:
        log.write(f"{tick},{zone},{pulse},{drift}\n")

def emit_tick(zone=None, pulse=None):
    tick = load_tick() + 1
    save_tick(tick, zone=zone, pulse=pulse)
    print(f"⏱️ Tick emitted | Tick: {tick} | Zone: {zone} | Pulse: {pulse}")
    return tick

def current_tick():
    return TICK_STATE.get("tick", 0)

def load_zone_overlay():
    try:
        df = pd.read_csv(ZONE_OVERLAY_FILE, names=["tick", "zone", "pulse"], encoding="utf-8")
        return df
    except Exception as e:
        print(f"[Pulse] ❌ Failed to load overlay log: {e}")
        return pd.DataFrame()

def get_recent_zone_window(window=10):
    df = load_zone_overlay()
    if df.empty:
        return []
    return df.tail(window).to_dict("records")
