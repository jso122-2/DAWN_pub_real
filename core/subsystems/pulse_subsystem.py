"""
Pulse subsystem for DAWN tick engine
"""

import logging
import random
import math
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PulseSubsystem:
    """Pulse subsystem for managing rhythmic pulses and heat zones"""
    
    def __init__(self):
        self.initialized = False
        self.start_time = time.time()
        self.beat_count = 0
        self.current_zone = "calm"
        self.heat = 0.0
        self.pulse_state = "ready"
        
    async def initialize(self):
        """Initialize pulse subsystem"""
        self.initialized = True
        self.start_time = time.time()
        logger.info("💓 Pulse subsystem initialized")
        
    async def tick(self, delta: float, ctx: Any = None) -> Dict[str, Any]:
        """Execute a single tick of the pulse subsystem"""
        self.beat_count += 1
        
        # Simulate rhythmic heat oscillation
        phase = (time.time() - self.start_time) * 0.1
        base_heat = (math.sin(phase) + 1) / 2  # 0-1 oscillation
        
        # Add some noise
        noise = random.gauss(0, 0.05)
        self.heat = max(0, min(1, base_heat + noise))
        
        # Determine zone based on heat
        if self.heat < 0.3:
            self.current_zone = "calm"
        elif self.heat < 0.6:
            self.current_zone = "active"
        elif self.heat < 0.8:
            self.current_zone = "warm"
        else:
            self.current_zone = "hot"
        
        return {
            "status": "ok",
            "pulse_state": self.pulse_state,
            "zone": self.current_zone,
            "heat": self.heat,
            "beat": self.beat_count,
            "entropy": self.heat * 0.3,
            "delta": delta
        }
    
    def get_state(self) -> Dict[str, Any]:
        """Get current pulse state"""
        return {
            "status": "active" if self.initialized else "inactive",
            "pulse_state": self.pulse_state,
            "zone": self.current_zone,
            "heat": self.heat,
            "beat_count": self.beat_count
        } 