"""
Pulse Layer - Unified interface for pulse and SCUP tracking
"""

import logging
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
import time
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PulseState:
    """Current state of the pulse system"""
    tick_id: int = 0
    last_tick_time: float = 0.0
    heat: float = 0.0
    alignment: float = 0.0
    scup: float = 0.5
    urgency: float = 0.0

class PulseLayer:
    """Unified pulse layer combining SCUP and pulse tracking"""
    
    def __init__(self):
        self._state = PulseState()
        self._scup_tracker = None
        self._pulse_tracker = None
        self._initialize()
        logger.info("Initialized PulseLayer")
        
    def _initialize(self) -> None:
        """Initialize trackers"""
        try:
            from pulse.scup_tracker import get_tracker as get_scup_tracker
            from pulse.pulse_tracker import get_tracker as get_pulse_tracker
            
            self._scup_tracker = get_scup_tracker()
            self._pulse_tracker = get_pulse_tracker()
            
            # Initialize with non-zero values
            self._state.scup = self._scup_tracker.get()
            self._state.heat = 0.1  # Start with minimal heat
            self._state.alignment = 0.5  # Start with neutral alignment
            
        except Exception as e:
            logger.error(f"Error initializing trackers: {e}")
            # Use fallback values
            self._state.scup = 0.5
            self._state.heat = 0.1
            self._state.alignment = 0.5
            
    def get_state(self) -> PulseState:
        """Get current pulse state"""
        return self._state
        
    def run_tick(self) -> None:
        """Execute a single tick, updating both SCUP and pulse values"""
        try:
            # Update tick counter and timestamp
            self._state.tick_id += 1
            self._state.last_tick_time = time.time()
            
            # Update SCUP
            if self._scup_tracker:
                self._state.scup = self._scup_tracker.get()
                
            # Update pulse heat with decay
            self._state.heat = max(0.0, self._state.heat * 0.95)
            
            # Update alignment based on SCUP and heat
            self._state.alignment = (self._state.scup + (1.0 - self._state.heat)) / 2.0
            
            # Update urgency based on heat and SCUP
            self._state.urgency = (self._state.heat + (1.0 - self._state.scup)) / 2.0
            
            logger.debug(f"Tick {self._state.tick_id}: SCUP={self._state.scup:.3f}, Heat={self._state.heat:.3f}")
            
        except Exception as e:
            logger.error(f"Error in run_tick: {e}")
            
    async def process_tick(self) -> None:
        """Async version of run_tick for compatibility with tick engine"""
        self.run_tick()
            
    def add_heat(self, amount: float) -> None:
        """Add heat to the system"""
        try:
            self._state.heat = min(1.0, self._state.heat + amount)
            logger.debug(f"Added heat: {amount:.3f}, new heat: {self._state.heat:.3f}")
        except Exception as e:
            logger.error(f"Error adding heat: {e}")
            
    def update_scup(self, delta: float) -> None:
        """Update SCUP value"""
        try:
            if self._scup_tracker:
                self._scup_tracker.update(delta)
                self._state.scup = self._scup_tracker.get()
            logger.debug(f"Updated SCUP: {self._state.scup:.3f}")
        except Exception as e:
            logger.error(f"Error updating SCUP: {e}")

class UnifiedPulseHeat:
    """Unified pulse heat system that manages thermal state"""
    
    def __init__(self):
        """Initialize the pulse heat system"""
        self.heat = 0.0
        self.last_tick_time = datetime.now(timezone.utc)
        self.thermal_state = "stable"
        self.tension = 0.0
        logger.info("Initialized UnifiedPulseHeat")
        
    async def update(self) -> None:
        """Update thermal state based on SCUP value"""
        try:
            current_time = datetime.now(timezone.utc)
            time_delta = (current_time - self.last_tick_time).total_seconds()
            self.last_tick_time = current_time
            
            # Update heat based on time delta
            heat_change = -0.1 * time_delta  # Natural cooling
            self.heat = max(0.0, min(1.0, self.heat + heat_change))
            
            # Update thermal state
            if self.heat > 0.8:
                self.thermal_state = "overheated"
            elif self.heat < 0.2:
                self.thermal_state = "cooling"
            else:
                self.thermal_state = "stable"
                
            logger.debug(f"Updated heat: {self.heat:.2f}, state: {self.thermal_state}")
            
        except Exception as e:
            logger.error(f"Error updating thermal state: {e}")
            
    def get_heat(self) -> float:
        """Get current heat value"""
        return self.heat
        
    def get_tension(self) -> float:
        """Get current tension value"""
        return self.tension
        
    def update_health(self, scup: float, entropy: float) -> None:
        """Update health metrics based on SCUP and entropy"""
        try:
            # Calculate tension based on SCUP and entropy
            self.tension = abs(scup - 0.5) * (1.0 - entropy)
            logger.debug(f"Updated tension: {self.tension:.2f}")
        except Exception as e:
            logger.error(f"Error updating health: {e}")
            
    def get_thermal_state(self) -> Dict[str, Any]:
        """Get current thermal state"""
        return {
            "heat": self.heat,
            "tension": self.tension,
            "state": self.thermal_state,
            "last_tick": self.last_tick_time.isoformat()
        }

# Global instance
_pulse_layer = PulseLayer()

def get_pulse_layer() -> PulseLayer:
    """Get the global pulse layer instance"""
    return _pulse_layer

def run_tick() -> None:
    """Run a single tick on the global pulse layer"""
    _pulse_layer.run_tick()
    
def get_state() -> PulseState:
    """Get current state from global pulse layer"""
    return _pulse_layer.get_state()
    
def add_heat(amount: float) -> None:
    """Add heat to the global pulse layer"""
    _pulse_layer.add_heat(amount)
    
def update_scup(delta: float) -> None:
    """Update SCUP on the global pulse layer"""
    _pulse_layer.update_scup(delta)

# Export key functions
__all__ = [
    'PulseLayer',
    'PulseState',
    'get_pulse_layer',
    'run_tick',
    'get_state',
    'add_heat',
    'update_scup'
] 