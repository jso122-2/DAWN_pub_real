"""
Schema subsystem for DAWN tick engine
"""

import logging
import random
import math
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SchemaSubsystem:
    """Schema subsystem for managing schema coherence and mood states"""
    
    def __init__(self):
        self.initialized = False
        self.coherence_pressure = 0.5  # SCUP
        self.active_mood = "neutral"
        self.mood_stability = 1.0
        self.schema_entropy = 0.0
        self.schema_state = "ready"
        
        self.moods = [
            "neutral", "contemplative", "curious", 
            "anticipatory", "focused", "creative",
            "reflective", "energetic"
        ]
        
    async def initialize(self):
        """Initialize schema subsystem"""
        self.initialized = True
        logger.info("🧠 Schema subsystem initialized")
        
    async def tick(self, delta: float, ctx: Any = None) -> Dict[str, Any]:
        """Execute a single tick of the schema subsystem"""
        # Get pulse influence
        pulse_state = getattr(ctx, 'pulse_state', {})
        pulse_heat = pulse_state.get('heat', 0.5)
        
        # Update SCUP based on various factors
        scup_delta = random.gauss(0, 0.02)
        self.coherence_pressure += scup_delta
        
        # Add pulse influence
        if pulse_heat > 0.7:
            self.coherence_pressure += 0.01
        
        # Bound SCUP
        self.coherence_pressure = max(0, min(1, self.coherence_pressure))
        
        # Update mood based on SCUP and stability
        if random.random() < (1 - self.mood_stability) * 0.1:
            self.active_mood = random.choice(self.moods)
            
        # Special moods for high SCUP
        if self.coherence_pressure > 0.8:
            if self.active_mood == "neutral":
                self.active_mood = "anticipatory"
        
        # Calculate entropy
        self.schema_entropy = (1 - self.mood_stability) * 0.5 + random.gauss(0, 0.05)
        self.schema_entropy = max(0, min(1, self.schema_entropy))
        
        # Update mood stability
        if self.coherence_pressure > 0.9:
            self.mood_stability *= 0.95
        else:
            self.mood_stability = min(1, self.mood_stability + 0.01)
        
        # Update context with our values
        if ctx:
            ctx.scup = self.coherence_pressure
            ctx.mood = self.active_mood
        
        return {
            "status": "ok",
            "schema_state": self.schema_state,
            "coherence_pressure": self.coherence_pressure,
            "active_mood": self.active_mood,
            "mood_stability": self.mood_stability,
            "entropy": self.schema_entropy,
            "delta": delta
        }
    
    def get_state(self) -> Dict[str, Any]:
        """Get current schema state"""
        return {
            "status": "active" if self.initialized else "inactive",
            "schema_state": self.schema_state,
            "coherence_pressure": self.coherence_pressure,
            "active_mood": self.active_mood,
            "mood_stability": self.mood_stability,
            "entropy": self.schema_entropy
        } 