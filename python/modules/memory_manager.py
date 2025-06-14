import asyncio
import numpy as np
from typing import Dict, Any, List, Optional
from collections import deque
import logging

logger = logging.getLogger(__name__)


class MemoryCell:
    """Individual memory storage unit"""
    def __init__(self, content: Any, importance: float = 0.5, timestamp: int = 0):
        self.content = content
        self.importance = importance
        self.timestamp = timestamp
        self.access_count = 0
        self.last_accessed = timestamp
        self.decay_rate = 0.01


class MemoryManager:
    """
    Manages memory storage, retrieval, and pressure for DAWN consciousness
    """
    
    def __init__(self, capacity: int = 1000, decay_rate: float = 0.001):
        self.capacity = capacity
        self.decay_rate = decay_rate
        
        # Memory storage
        self.short_term = deque(maxlen=capacity // 10)
        self.long_term = {}
        self.working_memory = []
        
        # Memory metrics
        self.pressure = 0.0
        self.fragmentation = 0.0
        self.consolidation_rate = 0.0
        
        logger.info(f"MemoryManager initialized with capacity {capacity}")
    
    async def get_state(self, tick_number: int) -> Dict[str, Any]:
        """Get current memory state"""
        # Update memory pressure
        self.pressure = min(
            (len(self.short_term) + len(self.long_term)) / self.capacity,
            1.0
        )
        
        # Add some variation
        self.pressure = np.clip(
            self.pressure + np.random.normal(0, 0.05),
            0.1, 0.9
        )
        
        state = {
            'pressure': self.pressure,
            'fragmentation': self.fragmentation,
            'consolidation_rate': self.consolidation_rate,
            'short_term_usage': len(self.short_term) / 100,
            'long_term_count': len(self.long_term),
            'working_memory_load': len(self.working_memory),
            'total_capacity': self.capacity
        }
        
        return state 