"""
Memory subsystem for DAWN tick engine
"""

import logging
import random
from typing import Dict, Any
from collections import deque

logger = logging.getLogger(__name__)

class MemorySubsystem:
    """Memory subsystem for managing memory traces and recall patterns"""
    
    def __init__(self):
        self.initialized = False
        self.memory_count = 0
        self.recent_memories = deque(maxlen=100)
        self.recall_rate = 0.0
        self.consolidation_pressure = 0.0
        self.memory_state = "ready"
        
    async def initialize(self):
        """Initialize memory subsystem"""
        self.initialized = True
        logger.info("🧩 Memory subsystem initialized")
        
    async def tick(self, delta: float, ctx: Any = None) -> Dict[str, Any]:
        """Execute a single tick of the memory subsystem"""
        # Simulate memory formation based on SCUP
        scup = getattr(ctx, 'scup', 0.5)
        
        if random.random() < scup * 0.1:
            # Form new memory
            self.memory_count += 1
            memory = {
                "tick": getattr(ctx, 'tick_id', 0),
                "mood": getattr(ctx, 'mood', 'neutral'),
                "strength": scup
            }
            self.recent_memories.append(memory)
        
        # Calculate recall rate
        if self.recent_memories:
            recent_strengths = [m["strength"] for m in list(self.recent_memories)[-10:]]
            self.recall_rate = sum(recent_strengths) / len(recent_strengths)
        
        # Update consolidation pressure
        self.consolidation_pressure = len(self.recent_memories) / 100.0
        
        return {
            "status": "ok",
            "memory_state": self.memory_state,
            "count": self.memory_count,
            "recent_count": len(self.recent_memories),
            "recall_rate": self.recall_rate,
            "consolidation_pressure": self.consolidation_pressure,
            "entropy": self.consolidation_pressure * 0.2,
            "delta": delta
        }
    
    def get_state(self) -> Dict[str, Any]:
        """Get current memory state"""
        return {
            "status": "active" if self.initialized else "inactive",
            "memory_state": self.memory_state,
            "count": self.memory_count,
            "recent_count": len(self.recent_memories),
            "recall_rate": self.recall_rate,
            "consolidation_pressure": self.consolidation_pressure
        } 