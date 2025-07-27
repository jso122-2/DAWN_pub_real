"""
Pulse System - Core thermal regulation and state management
"""

import yaml
import logging
import time
from typing import Dict, Optional
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PulseState:
    """Current state of pulse system"""
    heat: float = 0.0
    stability_index: float = 0.5
    thermal_momentum: float = 0.0
    tick_count: int = 0
    last_update: float = 0.0

class PulseSystem:
    """
    Core thermal regulation and state management system.
    Provides thermal profile, tick updates, and zone classification.
    """
    
    def __init__(self, config_path: str = "config/pulse_config.yaml"):
        """Initialize pulse system with configuration"""
        self.state = PulseState()
        self.config = self._load_config(config_path)
        self.heat_capacity = self.config.get('heat_capacity', 100.0)
        self.stability_threshold = self.config.get('stability_threshold', 0.7)
        self.momentum_decay = self.config.get('momentum_decay', 0.95)
        self.zone_thresholds = self.config.get('zone_thresholds', {
            'calm': 0.3,
            'active': 0.6,
            'surge': 0.8
        })
        logger.info("Initialized PulseSystem")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load pulse configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading pulse config: {e}")
            return {}
    
    def get_thermal_profile(self) -> Dict:
        """Get current thermal profile"""
        return {
            'current_heat': self.state.heat,
            'stability_index': self.state.stability_index,
            'thermal_momentum': self.state.thermal_momentum,
            'heat_capacity': self.heat_capacity
        }
    
    def tick_update(self) -> Dict:
        """Update pulse state for current tick"""
        self.state.tick_count += 1
        current_time = time.time()
        
        # Calculate time delta
        delta = current_time - self.state.last_update
        self.state.last_update = current_time
        
        # Update thermal momentum
        self.state.thermal_momentum *= self.momentum_decay
        
        # Update stability index
        if self.state.heat < self.heat_capacity * 0.3:
            self.state.stability_index = min(1.0, self.state.stability_index + 0.01)
        elif self.state.heat > self.heat_capacity * 0.7:
            self.state.stability_index = max(0.0, self.state.stability_index - 0.01)
        
        return {
            'tick_count': self.state.tick_count,
            'delta': delta,
            'heat': self.state.heat,
            'stability': self.state.stability_index,
            'momentum': self.state.thermal_momentum
        }
    
    def tick_thermal_update(self, delta: float) -> Dict:
        """Update thermal state for current tick"""
        # Calculate heat change based on delta
        heat_change = delta * self.state.thermal_momentum
        
        # Update heat level
        self.state.heat = max(0.0, min(self.heat_capacity, 
                                     self.state.heat + heat_change))
        
        return {
            'heat': self.state.heat,
            'heat_change': heat_change,
            'stability': self.state.stability_index
        }
    
    def classify(self) -> str:
        """Classify current zone based on heat level"""
        heat_ratio = self.state.heat / self.heat_capacity
        
        if heat_ratio <= self.zone_thresholds['calm']:
            return "🟢 calm"
        elif heat_ratio <= self.zone_thresholds['active']:
            return "🟡 active"
        else:
            return "🔴 surge"
    
    def apply_heat(self, amount: float) -> None:
        """Apply heat to the system"""
        self.state.heat = min(self.heat_capacity, self.state.heat + amount)
        self.state.thermal_momentum = min(1.0, self.state.thermal_momentum + 0.1)
    
    def remove_heat(self, amount: float) -> None:
        """Remove heat from the system"""
        self.state.heat = max(0.0, self.state.heat - amount)
        self.state.thermal_momentum = max(-1.0, self.state.thermal_momentum - 0.1)
    
    def get_state(self) -> Dict:
        """Get current pulse system state"""
        return {
            'heat': self.state.heat,
            'stability_index': self.state.stability_index,
            'thermal_momentum': self.state.thermal_momentum,
            'tick_count': self.state.tick_count,
            'current_zone': self.classify()
        }

# Global instance
pulse = PulseSystem()

# Export key functions
__all__ = ['pulse'] 