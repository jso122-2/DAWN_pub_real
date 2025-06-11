"""
Tension Tracker - Manages system tension metrics
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TensionState:
    """Current state of tension tracking"""
    current_tension: float = 0.0
    peak_tension: float = 0.0
    tension_history: list = None
    
    def __post_init__(self):
        if self.tension_history is None:
            self.tension_history = []

class TensionTracker:
    """Tracks system tension metrics"""
    
    def __init__(self):
        """Initialize tension tracker"""
        self._state = TensionState()
        logger.info("Initialized TensionTracker")
        
    def get_current_tension(self) -> float:
        """Get current tension value"""
        return self._state.current_tension
        
    def get_peak_tension(self) -> float:
        """Get peak tension value"""
        return self._state.peak_tension
        
    def update_tension(self, value: float) -> None:
        """Update tension value"""
        if not 0.0 <= value <= 1.0:
            logger.warning(f"Tension value {value} out of range [0.0, 1.0]")
            value = max(0.0, min(1.0, value))
            
        self._state.current_tension = value
        self._state.peak_tension = max(self._state.peak_tension, value)
        self._state.tension_history.append(value)
        
        # Keep history manageable
        if len(self._state.tension_history) > 100:
            self._state.tension_history = self._state.tension_history[-100:]
            
    def get_tension_history(self) -> list:
        """Get tension history"""
        return self._state.tension_history.copy() 