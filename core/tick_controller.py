#!/usr/bin/env python3
"""
tick_controller.py

Manages DAWN's tick timing and safety controls:
- Tracks current tick number
- Enforces cooldown periods between ticks
- Monitors system health metrics (SCUP, entropy)
- Prevents infinite loops and system overload

Author: DAWN Development Team
Epoch: epoch_0601
"""

import json
import time
from datetime import datetime
from typing import Dict, Optional, Tuple
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class TickController:
    """Supervises DAWN's tick timing and safety controls"""
    
    def __init__(self, config_path: str = "tick_engine_config.json"):
        self.config = self._load_config(config_path)
        self.tick_state_path = Path("tick_state.json")
        self.current_tick = 0
        self.last_tick_time = 0
        self.cooldown_period = self.config.get("cooldown_ticks", 1000)  # ms
        self.scup_threshold = self.config.get("scup_threshold", 0.95)
        self.entropy_threshold = self.config.get("entropy_threshold", 0.8)
        
    def _load_config(self, config_path: str) -> Dict:
        """Load tick engine configuration"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return {}
            
    def _load_tick_state(self) -> Dict:
        """Load current tick state from file"""
        try:
            with open(self.tick_state_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"tick": 0, "timestamp": None, "zone": None, "pulse": None}
            
    def _save_tick_state(self, state: Dict):
        """Save current tick state to file"""
        with open(self.tick_state_path, 'w') as f:
            json.dump(state, f, indent=2)
            
    def can_proceed(self, current_scup: float, current_entropy: float) -> Tuple[bool, str]:
        """
        Check if system can proceed with next tick
        
        Args:
            current_scup: Current SCUP value (0-1)
            current_entropy: Current entropy value (0-1)
            
        Returns:
            Tuple of (can_proceed, reason)
        """
        # Check cooldown
        current_time = int(time.time() * 1000)
        if current_time - self.last_tick_time < self.cooldown_period:
            return False, "Cooldown period not elapsed"
            
        # Check SCUP threshold
        if current_scup > self.scup_threshold:
            return False, f"SCUP threshold exceeded: {current_scup:.2f}"
            
        # Check entropy threshold
        if current_entropy > self.entropy_threshold:
            return False, f"Entropy threshold exceeded: {current_entropy:.2f}"
            
        return True, "OK"
        
    def advance_tick(self, zone: Optional[str] = None, pulse: Optional[str] = None) -> int:
        """
        Advance to next tick if conditions allow
        
        Args:
            zone: Current zone identifier
            pulse: Current pulse identifier
            
        Returns:
            New tick number
        """
        # Load current state
        state = self._load_tick_state()
        self.current_tick = state.get("tick", 0)
        
        # Update state
        self.current_tick += 1
        self.last_tick_time = int(time.time() * 1000)
        
        new_state = {
            "tick": self.current_tick,
            "timestamp": datetime.now().isoformat(),
            "zone": zone,
            "pulse": pulse
        }
        
        # Save updated state
        self._save_tick_state(new_state)
        logger.info(f"Advanced to tick {self.current_tick}")
        
        return self.current_tick
        
    def get_current_tick(self) -> int:
        """Get current tick number"""
        state = self._load_tick_state()
        return state.get("tick", 0)
        
    def reset(self):
        """Reset tick counter and state"""
        self.current_tick = 0
        self.last_tick_time = 0
        self._save_tick_state({
            "tick": 0,
            "timestamp": datetime.now().isoformat(),
            "zone": None,
            "pulse": None
        })
        logger.info("Tick controller reset")

# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Create controller
    controller = TickController()
    
    # Simulate tick advancement
    for i in range(3):
        # Simulate system metrics
        scup = 0.5 + (i * 0.1)  # Gradually increasing SCUP
        entropy = 0.3 + (i * 0.1)  # Gradually increasing entropy
        
        # Check if we can proceed
        can_proceed, reason = controller.can_proceed(scup, entropy)
        
        if can_proceed:
            tick = controller.advance_tick(zone="test_zone", pulse="test_pulse")
            print(f"Advanced to tick {tick}")
        else:
            print(f"Cannot proceed: {reason}")
            
        # Small delay to simulate work
        time.sleep(0.1) 