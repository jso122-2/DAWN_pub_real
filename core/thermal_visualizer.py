"""
Thermal Visualizer - Visualizes DAWN's thermal state and regulation
"""

import logging
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ThermalState:
    """Current state of thermal visualization"""
    current_heat: float = 0.0
    cooling_rate: float = 0.0
    stability: float = 0.0
    last_update: float = 0.0
    active_cooling: bool = False
    emergency_mode: bool = False

class ThermalVisualizer:
    """
    Visualizes DAWN's thermal state and regulation.
    Provides real-time visualization of heat levels, cooling rates, and stability.
    """
    
    def __init__(self):
        """Initialize thermal visualizer with default state"""
        self.state = ThermalState()
        self.log_dir = "logs"
        logger.info("Initialized ThermalVisualizer")
        
    def update_state(self, heat: float, cooling_rate: float, stability: float, 
                    active_cooling: bool = False, emergency_mode: bool = False) -> None:
        """Update thermal visualization state"""
        self.state.current_heat = heat
        self.state.cooling_rate = cooling_rate
        self.state.stability = stability
        self.state.active_cooling = active_cooling
        self.state.emergency_mode = emergency_mode
        self.state.last_update = datetime.now().timestamp()
        
    def get_visualization(self) -> Dict:
        """Get current thermal visualization state"""
        return {
            "heat_level": self.state.current_heat,
            "cooling_rate": self.state.cooling_rate,
            "stability": self.state.stability,
            "active_cooling": self.state.active_cooling,
            "emergency_mode": self.state.emergency_mode,
            "last_update": self.state.last_update
        }
        
    def log_thermal_event(self, event_type: str, details: Dict) -> None:
        """Log thermal events for analysis"""
        event = {
            "timestamp": datetime.now().timestamp(),
            "type": event_type,
            "details": details,
            "state": self.get_visualization()
        }
        logger.info(f"Thermal event: {event_type} - {details}")
        
    def export_state(self) -> Dict:
        """Export current thermal state for persistence"""
        return {
            "current_heat": self.state.current_heat,
            "cooling_rate": self.state.cooling_rate,
            "stability": self.state.stability,
            "active_cooling": self.state.active_cooling,
            "emergency_mode": self.state.emergency_mode,
            "last_update": self.state.last_update
        } 