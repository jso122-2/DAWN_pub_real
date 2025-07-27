"""
Visual subsystem for DAWN tick engine
"""

import logging
import random
from typing import Dict, Any

logger = logging.getLogger(__name__)

class VisualSubsystem:
    """Visual subsystem for managing system visualization and display"""
    
    def __init__(self):
        self.initialized = False
        self.pattern_count = 0
        self.active_pattern = "none"
        self.visual_entropy = 0.0
        self.visual_state = "ready"
        
        self.patterns = [
            "spiral", "wave", "pulse", "fractal",
            "grid", "flow", "constellation", "aurora"
        ]
        
    async def initialize(self):
        """Initialize visual subsystem"""
        self.initialized = True
        logger.info("👁️  Visual subsystem initialized")
        
    async def tick(self, delta: float, ctx: Any = None) -> Dict[str, Any]:
        """Execute a single tick of the visual subsystem"""
        # Update pattern based on mood
        mood = getattr(ctx, 'mood', 'neutral')
        
        if mood == "contemplative":
            self.active_pattern = "spiral"
        elif mood == "energetic":
            self.active_pattern = "pulse"
        elif mood == "creative":
            self.active_pattern = "fractal"
        elif random.random() < 0.1:
            # Random pattern change
            self.active_pattern = random.choice(self.patterns)
            self.pattern_count += 1
        
        # Calculate visual entropy
        pulse_state = getattr(ctx, 'pulse_state', {})
        pulse_heat = pulse_state.get('heat', 0.5)
        self.visual_entropy = pulse_heat * 0.4 + random.gauss(0, 0.1)
        self.visual_entropy = max(0, min(1, self.visual_entropy))
        
        return {
            "status": "ok",
            "visual_state": self.visual_state,
            "active_pattern": self.active_pattern,
            "pattern_count": self.pattern_count,
            "entropy": self.visual_entropy,
            "delta": delta
        }
    
    def get_state(self) -> Dict[str, Any]:
        """Get current visual state"""
        return {
            "status": "active" if self.initialized else "inactive",
            "visual_state": self.visual_state,
            "active_pattern": self.active_pattern,
            "pattern_count": self.pattern_count,
            "entropy": self.visual_entropy
        } 