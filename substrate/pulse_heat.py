"""
Pulse Heat System - Manages thermal dynamics of DAWN's pulse system
"""

import time
import logging
from typing import Dict, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class PulseHeatState:
    """Current state of the pulse heat system"""
    heat_level: float = 0.0
    momentum: float = 0.0
    stability: float = 1.0
    last_update: float = field(default_factory=time.time)
    thermal_history: Dict[str, float] = field(default_factory=dict)

class PulseHeatSystem:
    """Manages the thermal dynamics of DAWN's pulse system"""
    
    def __init__(self):
        """Initialize the pulse heat system"""
        self.state = PulseHeatState()
        self.config = {
            'heat_decay_rate': 0.95,
            'momentum_decay_rate': 0.98,
            'stability_recovery_rate': 0.01,
            'max_heat': 1.0,
            'min_heat': 0.0
        }
        logger.info("Initialized PulseHeatSystem")
    
    def update(self, delta_time: float) -> None:
        """Update the pulse heat system state"""
        # Update heat level
        self.state.heat_level *= self.config['heat_decay_rate']
        
        # Update momentum
        self.state.momentum *= self.config['momentum_decay_rate']
        
        # Update stability
        if self.state.heat_level > 0.8:
            self.state.stability *= 0.95
        else:
            self.state.stability = min(1.0, 
                self.state.stability + self.config['stability_recovery_rate'])
        
        # Record thermal history
        self.state.thermal_history[time.time()] = self.state.heat_level
        
        # Update timestamp
        self.state.last_update = time.time()
    
    def add_heat(self, amount: float) -> None:
        """Add heat to the system"""
        self.state.heat_level = min(
            self.config['max_heat'],
            self.state.heat_level + amount
        )
        self.state.momentum += amount * 0.1
    
    def get_state(self) -> Dict:
        """Get current system state"""
        return {
            'heat_level': self.state.heat_level,
            'momentum': self.state.momentum,
            'stability': self.state.stability,
            'last_update': self.state.last_update
        }

# Global instance
_pulse_heat_system = None

def pulse_heat() -> PulseHeatSystem:
    """Get or create the global pulse heat system instance"""
    global _pulse_heat_system
    if _pulse_heat_system is None:
        _pulse_heat_system = PulseHeatSystem()
    return _pulse_heat_system

__all__ = ['pulse_heat', 'PulseHeatSystem'] 