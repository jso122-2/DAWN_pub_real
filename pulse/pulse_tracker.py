"""
Pulse Tracker - Manages pulse-related state tracking
"""

import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PulseState:
    """Current state of the pulse system"""
    scup: float = 0.0
    heat: float = 0.0
    alignment: float = 0.0
    tick_id: int = 0

class SCUPTracker:
    """Tracks SCUP (Semantic Coherence Under Pressure) values"""
    
    def __init__(self, initial_scup: float = 0.0):
        self.scup = initial_scup
        self._min_scup = 0.0
        self._max_scup = 1.0
        logger.info(f"Initialized SCUPTracker with SCUP={initial_scup}")
        
    def update(self, delta: float) -> None:
        """Update SCUP value by delta, bounded between 0 and 1"""
        try:
            new_scup = self.scup + delta
            self.scup = max(self._min_scup, min(self._max_scup, new_scup))
            logger.debug(f"Updated SCUP: {self.scup} (delta: {delta})")
        except Exception as e:
            logger.error(f"Error updating SCUP: {e}")
            # Maintain current value on error
            
    def get(self) -> float:
        """Get current SCUP value"""
        return self.scup
        
    def set(self, value: float) -> None:
        """Set SCUP value directly, bounded between 0 and 1"""
        try:
            self.scup = max(self._min_scup, min(self._max_scup, value))
            logger.debug(f"Set SCUP to: {self.scup}")
        except Exception as e:
            logger.error(f"Error setting SCUP: {e}")
            # Maintain current value on error

# Global instance
_scup_tracker = SCUPTracker()

def get_scup_tracker() -> SCUPTracker:
    """Get the global SCUP tracker instance"""
    return _scup_tracker

def update_scup(delta: float) -> None:
    """Update SCUP value on global tracker"""
    _scup_tracker.update(delta)
    
def get_scup() -> float:
    """Get current SCUP value from global tracker"""
    return _scup_tracker.get()
    
def set_scup(value: float) -> None:
    """Set SCUP value on global tracker"""
    _scup_tracker.set(value)

# Fallback class for when SCUPTracker is not available
class FallbackSCUPTracker:
    """Fallback SCUP tracker that always returns 0.5"""
    
    def __init__(self):
        self.scup = 0.5
        logger.warning("Using FallbackSCUPTracker")
        
    def update(self, delta: float) -> None:
        """No-op update"""
        pass
        
    def get(self) -> float:
        """Always return 0.5"""
        return 0.5
        
    def set(self, value: float) -> None:
        """No-op set"""
        pass

def get_tracker() -> Any:
    """Get SCUP tracker with fallback"""
    try:
        return get_scup_tracker()
    except Exception as e:
        logger.error(f"Error getting SCUP tracker, using fallback: {e}")
        return FallbackSCUPTracker() 