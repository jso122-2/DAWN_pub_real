"""
SCUP Tracker - Manages Semantic Coherence Under Pressure values
"""

import logging
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SCUPState:
    """Current state of SCUP tracking"""
    scup: float = 0.0
    last_update: float = 0.0
    update_count: int = 0

class SCUPTracker:
    """Tracks SCUP (Semantic Coherence Under Pressure) values"""
    
    def __init__(self, threshold=0.5, cooldown=300.0):
        """Initialize SCUP tracker with threshold and cooldown parameters"""
        self.scup = 0.0
        self._min_scup = 0.0
        self._max_scup = 1.0
        self.threshold = threshold
        self.cooldown = cooldown
        self._last_cooldown = time.time()
        logger.info("Initialized SCUPTracker")
        
    def update(self, delta: float) -> None:
        """Update SCUP value by delta, bounded between 0 and 1"""
        try:
            # Check cooldown
            if time.time() - self._last_cooldown < self.cooldown:
                logger.debug("SCUP update skipped due to cooldown")
                return
                
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
            
    def is_above_threshold(self) -> bool:
        """Check if current SCUP value is above threshold"""
        return self.scup >= self.threshold
        
    def reset_cooldown(self) -> None:
        """Reset the cooldown timer"""
        self._last_cooldown = time.time()

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

# Export key functions for helix_import
__all__ = [
    'SCUPTracker',
    'FallbackSCUPTracker',
    'get_scup_tracker',
    'update_scup',
    'get_scup',
    'set_scup',
    'get_tracker'
] 