#!/usr/bin/env python3
"""
wire_pulse_state.py

Wires pulse state tracker into DAWN system
"""

import logging
from pulse.pulse_state_tracker import PulseStateTracker
from pulse.pulse_engine import PulseEngine
from pulse.unified_pulse_heat import UnifiedPulseHeat

logger = logging.getLogger(__name__)

def wire_pulse_state():
    """Wire pulse state tracker into system"""
    try:
        # Initialize components
        pulse_engine = PulseEngine()
        pulse_heat = UnifiedPulseHeat()
        state_tracker = PulseStateTracker()
        
        # Wire components
        pulse_engine.wire(None)  # Wire engine first
        state_tracker.wire(pulse_engine, pulse_heat)
        
        # Initial state update
        state_tracker.update()
        
        logger.info("Pulse state tracker wired successfully")
        return state_tracker
        
    except Exception as e:
        logger.error(f"Error wiring pulse state: {e}")
        return None

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Wire system
    tracker = wire_pulse_state()
    
    if tracker:
        print("\nPulse State Tracker Status:")
        print(f"Current urgency: {tracker.get_urgency()}")
        print(f"Current mood: {tracker.get_mood()}")
        print(f"Current temperature: {tracker.get_temperature()}")
        print("\nThermal State:")
        thermal = tracker.get_thermal_state()
        for key, value in thermal.items():
            print(f"  {key}: {value}") 