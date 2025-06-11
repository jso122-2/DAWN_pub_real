"""
Alignment Probe - Monitors system alignment metrics
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AlignmentState:
    """Current state of alignment tracking"""
    current_alignment: float = 0.5
    alignment_drift: float = 0.0
    alignment_history: list = None
    
    def __post_init__(self):
        if self.alignment_history is None:
            self.alignment_history = []

class AlignmentProbe:
    """Monitors system alignment metrics"""
    
    def __init__(self):
        """Initialize alignment probe"""
        self._state = AlignmentState()
        logger.info("Initialized AlignmentProbe")
        
    def get_current_alignment(self) -> float:
        """Get current alignment value"""
        return self._state.current_alignment
        
    def get_alignment_drift(self) -> float:
        """Get current alignment drift"""
        return self._state.alignment_drift
        
    def update_alignment(self, value: float) -> None:
        """Update alignment value"""
        if not 0.0 <= value <= 1.0:
            logger.warning(f"Alignment value {value} out of range [0.0, 1.0]")
            value = max(0.0, min(1.0, value))
            
        # Calculate drift
        old_alignment = self._state.current_alignment
        self._state.current_alignment = value
        self._state.alignment_drift = value - old_alignment
        
        # Update history
        self._state.alignment_history.append(value)
        if len(self._state.alignment_history) > 100:
            self._state.alignment_history = self._state.alignment_history[-100:]
            
    def get_alignment_history(self) -> list:
        """Get alignment history"""
        return self._state.alignment_history.copy() 