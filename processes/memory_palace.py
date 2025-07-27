"""
Memory Palace - Manages memory processing, consolidation, and visualization
"""

import json
import time
import random
import math
import logging
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
import numpy as np

logger = logging.getLogger(__name__)

@dataclass
class MemoryState:
    """Current state of the memory system"""
    short_term: float = 89.3  # Base value from metrics
    long_term: float = 76.4   # Base value from metrics
    working_memory: float = 91.2  # Base value from metrics
    last_update: float = field(default_factory=time.time)
    memory_history: List[Dict] = field(default_factory=list)
    active_memories: Dict[str, Dict] = field(default_factory=dict)
    consolidation_threshold: float = 0.7
    metrics: Dict[str, float] = field(default_factory=lambda: {
        'short_term': 89.3,
        'long_term': 76.4,
        'working_memory': 91.2
    })

class MemoryPalace:
    """
    Manages memory processing and visualization.
    Handles memory consolidation, pattern detection, and spatial organization.
    """
    
    def __init__(self):
        """Initialize memory palace"""
        self.state = MemoryState()
        self.config = {
            'update_interval': 0.5,  # 500ms
            'consolidation_threshold': 0.7,
            'memory_timeout': 300.0,  # 5 minutes
            'history_limit': 100,
            'spatial': {
                'sector_radius': 100,
                'layer_height': 50,
                'cluster_threshold': 0.7,
                'connection_distance': 50,
                'repulsion_force': 0.1,
                'attraction_force': 0.05
            },
            'memory': {
                'decay_threshold': 0.1,
                'base_decay_rate': 0.001,
                'crystallization_threshold': 0.9,
                'consolidation_interval': 1000,  # ms
                'max_memories': 10000,
                'max_associations': 20
            }
        }
        logger.info("Initialized MemoryPalace")
    
    def update_metrics(self, delta_time: float) -> None:
        """
        Update memory metrics
        
        Args:
            delta_time: Time since last update
        """
        current_time = time.time()
        
        # Update short-term memory
        base_value = self.state.metrics['short_term']
        variation = math.sin(current_time * 0.1) * 10 + random.uniform(-2, 2)
        self.state.metrics['short_term'] = max(0, min(100, base_value + variation))
        
        # Update long-term memory
        base_value = self.state.metrics['long_term']
        variation = math.sin(current_time * 0.1) * 10 + random.uniform(-2, 2)
        self.state.metrics['long_term'] = max(0, min(100, base_value + variation))
        
        # Update working memory
        base_value = self.state.metrics['working_memory']
        variation = math.sin(current_time * 0.1) * 10 + random.uniform(-2, 2)
        self.state.metrics['working_memory'] = max(0, min(100, base_value + variation))
        
        # Record metrics in history
        self._record_metrics()
        
        # Clean up old memories
        self._cleanup_memories()
    
    def _record_metrics(self) -> None:
        """Record current metrics in history"""
        metrics_record = {
            'timestamp': datetime.now().isoformat(),
            'metrics': self.state.metrics.copy()
        }
        
        self.state.memory_history.append(metrics_record)
        if len(self.state.memory_history) > self.config['history_limit']:
            self.state.memory_history = self.state.memory_history[-self.config['history_limit']:]
    
    def _cleanup_memories(self) -> None:
        """Clean up expired memories"""
        current_time = time.time()
        expired = [
            mem_id for mem_id, mem in self.state.active_memories.items()
            if current_time - mem['timestamp'] > self.config['memory_timeout']
        ]
        
        for mem_id in expired:
            del self.state.active_memories[mem_id]
    
    def create_memory(self, content: str, details: Dict[str, Any], system_state: Dict[str, Any]) -> str:
        """
        Create a new memory
        
        Args:
            content: Memory content
            details: Additional memory details
            system_state: Current system state
            
        Returns:
            Memory ID
        """
        if not content:
            logger.warning("Attempted to create memory with empty content")
            return None
        
        memory_id = f"mem_{int(time.time() * 1000)}"
        self.state.active_memories[memory_id] = {
            'content': content,
            'details': details,
            'system_state': system_state,
            'timestamp': time.time(),
            'strength': self._calculate_initial_strength(content, details),
            'consolidation': 0,
            'associations': [],
            'spatial_position': self._calculate_spatial_position(content, system_state),
            'metadata': {
                'importance': self._calculate_importance(content, details),
                'uniqueness': self._calculate_uniqueness(content),
                'unity': system_state.get('unity', 0.7),
                'abstraction_level': self._determine_abstraction_level(content),
                'crystallized': False,
                'tags': self._extract_tags(content, details)
            }
        }
        
        logger.info(f"Created memory {memory_id} with strength {self.state.active_memories[memory_id]['strength']}")
        return memory_id
    
    def _calculate_initial_strength(self, content: str, details: Dict[str, Any]) -> float:
        """Calculate initial memory strength"""
        return random.uniform(0.3, 0.8)
    
    def _calculate_spatial_position(self, content: str, system_state: Dict[str, Any]) -> Dict[str, float]:
        """Calculate spatial position for memory"""
        # Use content hash to determine position
        content_hash = hash(content)
        return {
            'x': ((content_hash % 1000) / 1000 - 0.5) * 200,
            'y': (((content_hash >> 10) % 1000) / 1000 - 0.5) * 200,
            'z': (((content_hash >> 20) % 1000) / 1000 - 0.5) * 200
        }
    
    def _calculate_importance(self, content: str, details: Dict[str, Any]) -> float:
        """Calculate memory importance"""
        importance = 0.5
        
        if 'critical' in content.lower() or 'important' in content.lower():
            importance += 0.3
        if len(content) > 100:
            importance += 0.1
        if details.get('priority') == 'high':
            importance += 0.2
        
        return min(importance, 1.0)
    
    def _calculate_uniqueness(self, content: str) -> float:
        """Calculate memory uniqueness"""
        similar = [
            mem for mem in self.state.active_memories.values()
            if self._calculate_similarity(content, mem['content']) > 0.7
        ]
        
        return max(0.1, 1 - (len(similar) * 0.1))
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0
    
    def _determine_abstraction_level(self, content: str) -> float:
        """Determine abstraction level of content"""
        if 'concept' in content.lower() or 'principle' in content.lower():
            return 0.9
        if 'pattern' in content.lower() or 'relationship' in content.lower():
            return 0.7
        return 0.3
    
    def _extract_tags(self, content: str, details: Dict[str, Any]) -> List[str]:
        """Extract tags from content and details"""
        tags = list(details.get('tags', []))
        
        content_lower = content.lower()
        if 'pattern' in content_lower:
            tags.append('pattern')
        if 'insight' in content_lower:
            tags.append('insight')
        if 'important' in content_lower:
            tags.append('significant')
        
        return tags
    
    def get_memory_state(self) -> Dict:
        """Get current memory state"""
        return {
            'metrics': self.state.metrics.copy(),
            'active_memories': len(self.state.active_memories),
            'history_size': len(self.state.memory_history)
        }
    
    def get_metrics_json(self) -> str:
        """Get current metrics as JSON string"""
        return json.dumps({
            "type": "metrics",
            "subprocess_id": "memory_palace",
            "metrics": {
                "short_term": self.state.metrics['short_term'],
                "long_term": self.state.metrics['long_term'],
                "working_memory": self.state.metrics['working_memory']
            },
            "timestamp": time.time()
        })

# Global instance
_memory_palace = None

def get_memory_palace() -> MemoryPalace:
    """Get or create the global memory palace instance"""
    global _memory_palace
    if _memory_palace is None:
        _memory_palace = MemoryPalace()
    return _memory_palace

__all__ = ['MemoryPalace', 'get_memory_palace']

def main():
    """Dummy subprocess for Memory Palace"""
    palace = get_memory_palace()
    
    while True:
        # Update metrics
        palace.update_metrics(0.5)  # 500ms delta
        
        # Output metrics
        print(palace.get_metrics_json())
        
        time.sleep(0.5)  # Update every 500ms

if __name__ == "__main__":
    main()
