#!/usr/bin/env python3
"""
pulse_state_tracker.py

Manages persistent pulse state for DAWN cognitive system
Provides queryable interface for urgency, pressure, and state-of-mind

Integration:
    Primary: dawn.pulse.state.pulse_state_tracker
    Dependencies: pulse_engine.py, unified_pulse_heat.py
    Output: pulse_state.json
"""

import json
import time
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
import logging

# Core DAWN components
try:
    from core.tick_engine import get_current_tick
    from pulse.pulse_engine import PulseEngine
    from pulse.unified_pulse_heat import UnifiedPulseHeat
except ImportError:
    def get_current_tick():
        return int(time.time() * 1000)

logger = logging.getLogger(__name__)

class PulseStateTracker:
    """Manages persistent pulse state for DAWN"""
    
    def __init__(self, state_file: str = "pulse/pulse_state.json"):
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()
        self.pulse_engine = None
        self.pulse_heat = None
        
    def _load_state(self) -> Dict[str, Any]:
        """Load state from JSON file"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading pulse state: {e}")
                return self._get_default_state()
        return self._get_default_state()
    
    def _get_default_state(self) -> Dict[str, Any]:
        """Get default state structure"""
        return {
            "current_tick": 0,
            "system_pressure": 0.35,
            "mood": "stable",
            "pulse_temperature": "cool",
            "last_claude_signal": "schema drift",
            "thermal_state": {
                "current_heat": 0.0,
                "baseline_heat": 0.0,
                "thermal_momentum": 0.0,
                "stability_index": 1.0,
                "heat_capacity": 10.0,
                "current_zone": "🟢 calm"
            },
            "pressure_components": {
                "entropy_level": 0.0,
                "mood_valence": 0.0,
                "drift_pressure": 0.0,
                "pulse_temp": 0.0
            },
            "last_update": "",
            "zone_history": [],
            "heat_sources": {},
            "mood_pressure": {}
        }
    
    def save_state(self):
        """Save current state to JSON file"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving pulse state: {e}")
    
    def wire(self, pulse_engine: Optional[PulseEngine] = None, 
             pulse_heat: Optional[UnifiedPulseHeat] = None):
        """Wire into pulse engine and heat system"""
        self.pulse_engine = pulse_engine
        self.pulse_heat = pulse_heat
        logger.info("Pulse state tracker wired")
    
    def update(self):
        """Update state from pulse systems"""
        if not self.pulse_engine or not self.pulse_heat:
            return
            
        # Get current tick
        self.state["current_tick"] = get_current_tick()
        
        # Get thermal profile
        thermal_profile = self.pulse_heat.get_thermal_profile()
        self.state["thermal_state"].update({
            "current_heat": thermal_profile["current_heat"],
            "baseline_heat": thermal_profile["baseline_heat"],
            "thermal_momentum": thermal_profile["thermal_momentum"],
            "stability_index": thermal_profile["stability_index"],
            "heat_capacity": thermal_profile["heat_capacity"],
            "current_zone": thermal_profile["current_zone"]
        })
        
        # Update pressure components
        self.state["pressure_components"].update({
            "entropy_level": thermal_profile.get("entropy_level", 0.0),
            "mood_valence": thermal_profile.get("mood_valence", 0.0),
            "drift_pressure": thermal_profile.get("drift_pressure", 0.0),
            "pulse_temp": thermal_profile["current_heat"]
        })
        
        # Update system pressure
        self.state["system_pressure"] = thermal_profile["current_heat"]
        
        # Update zone history
        if thermal_profile.get("zone_history"):
            self.state["zone_history"] = thermal_profile["zone_history"]
            
        # Update heat sources
        self.state["heat_sources"] = thermal_profile.get("sources", {})
        
        # Update mood pressure
        self.state["mood_pressure"] = thermal_profile.get("mood_pressure", {})
        
        # Update timestamp
        self.state["last_update"] = datetime.utcnow().isoformat()
        
        # Save state
        self.save_state()
    
    def get_urgency(self) -> float:
        """Get current system urgency level"""
        return self.state["system_pressure"]
    
    def get_mood(self) -> str:
        """Get current system mood"""
        return self.state["mood"]
    
    def get_temperature(self) -> str:
        """Get current pulse temperature state"""
        return self.state["pulse_temperature"]
    
    def get_thermal_state(self) -> Dict[str, Any]:
        """Get current thermal state"""
        return self.state["thermal_state"]
    
    def get_pressure_components(self) -> Dict[str, float]:
        """Get current pressure components"""
        return self.state["pressure_components"]
    
    def get_zone_history(self) -> list:
        """Get zone transition history"""
        return self.state["zone_history"]
    
    def get_heat_sources(self) -> Dict[str, Any]:
        """Get current heat sources"""
        return self.state["heat_sources"]
    
    def get_mood_pressure(self) -> Dict[str, float]:
        """Get current mood pressure"""
        return self.state["mood_pressure"]
    
    def set_claude_signal(self, signal: str):
        """Set last Claude signal"""
        self.state["last_claude_signal"] = signal
        self.save_state()
    
    def set_mood(self, mood: str):
        """Set system mood"""
        self.state["mood"] = mood
        self.save_state()
    
    def set_temperature(self, temp: str):
        """Set pulse temperature state"""
        self.state["pulse_temperature"] = temp
        self.save_state()

# Example usage
if __name__ == "__main__":
    tracker = PulseStateTracker()
    print("Pulse State Tracker initialized")
    print(f"Current urgency: {tracker.get_urgency()}")
    print(f"Current mood: {tracker.get_mood()}")
    print(f"Current temperature: {tracker.get_temperature()}") 