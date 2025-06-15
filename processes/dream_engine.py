#!/usr/bin/env python3
import json
import time
import random
import math
import logging
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque

logger = logging.getLogger(__name__)

@dataclass
class DreamState:
    """Current state of the dream system"""
    is_dreaming: bool = False
    dream_depth: float = 0.0  # 0-1 scale
    dream_coherence: float = 0.0  # 0-1 scale
    dream_charge: float = 0.0  # 0-1 scale
    dream_momentum: float = 0.0
    dream_history: List[Dict] = field(default_factory=list)
    last_dream_time: float = field(default_factory=time.time)
    dream_entities: Set[str] = field(default_factory=set)
    dream_connections: Dict[str, List[str]] = field(default_factory=dict)
    dream_metrics: Dict[str, float] = field(default_factory=lambda: {
        'vividness': 0.0,
        'stability': 0.0,
        'novelty': 0.0,
        'emotional_intensity': 0.0,
        'dream_state': 12.1,  # From metrics
        'rem_activity': 8.3,  # From metrics
        'lucidity': 22.7      # From metrics
    })

class DreamEngine:
    """
    Manages dream states and processing.
    Handles dream generation, evolution, and analysis.
    """
    
    def __init__(self):
        """Initialize dream engine"""
        self.state = DreamState()
        self.config = {
            'dream_threshold': 0.3,
            'dream_decay': 0.95,
            'dream_momentum_factor': 0.1,
            'max_dream_depth': 1.0,
            'min_dream_coherence': 0.2,
            'dream_entity_limit': 100,
            'metric_update_interval': 0.5  # 500ms
        }
        self.last_metric_update = time.time()
        logger.info("Initialized DreamEngine")
    
    def start_dream(self, initial_depth: float = 0.5) -> None:
        """
        Start a new dream state
        
        Args:
            initial_depth: Initial dream depth (0-1)
        """
        if self.state.is_dreaming:
            logger.warning("Already dreaming")
            return
        
        self.state.is_dreaming = True
        self.state.dream_depth = min(initial_depth, self.config['max_dream_depth'])
        self.state.dream_coherence = self.config['min_dream_coherence']
        self.state.dream_charge = 0.0
        self.state.dream_momentum = 0.0
        self.state.dream_entities.clear()
        self.state.dream_connections.clear()
        self.state.last_dream_time = time.time()
        
        logger.info(f"Started dream with depth {initial_depth}")
    
    def end_dream(self) -> Dict:
        """
        End current dream and return dream summary
        
        Returns:
            Dream summary dictionary
        """
        if not self.state.is_dreaming:
            logger.warning("Not currently dreaming")
            return {}
        
        # Create dream summary
        dream_summary = {
            'duration': time.time() - self.state.last_dream_time,
            'max_depth': self.state.dream_depth,
            'final_coherence': self.state.dream_coherence,
            'entity_count': len(self.state.dream_entities),
            'metrics': self.state.dream_metrics.copy(),
            'timestamp': datetime.now().isoformat()
        }
        
        # Record dream in history
        self.state.dream_history.append(dream_summary)
        if len(self.state.dream_history) > 100:
            self.state.dream_history = self.state.dream_history[-100:]
        
        # Reset dream state
        self.state.is_dreaming = False
        self.state.dream_depth = 0.0
        self.state.dream_coherence = 0.0
        self.state.dream_charge = 0.0
        self.state.dream_momentum = 0.0
        self.state.dream_entities.clear()
        self.state.dream_connections.clear()
        
        logger.info("Ended dream")
        return dream_summary
    
    def update_dream(self, delta_time: float) -> None:
        """
        Update dream state
        
        Args:
            delta_time: Time since last update
        """
        if not self.state.is_dreaming:
            return
        
        # Update dream charge with momentum
        self.state.dream_momentum *= self.config['dream_decay']
        self.state.dream_charge = min(
            1.0,
            self.state.dream_charge + self.state.dream_momentum * delta_time
        )
        
        # Update dream depth based on charge
        target_depth = self.state.dream_charge * self.config['max_dream_depth']
        self.state.dream_depth += (target_depth - self.state.dream_depth) * 0.1
        
        # Update dream coherence
        base_coherence = self.config['min_dream_coherence']
        charge_factor = self.state.dream_charge * 0.5
        stability_factor = self.state.dream_metrics['stability'] * 0.3
        self.state.dream_coherence = min(
            1.0,
            base_coherence + charge_factor + stability_factor
        )
        
        # Update dream metrics
        self._update_dream_metrics(delta_time)
        
        # Check for dream termination
        if (self.state.dream_coherence < self.config['min_dream_coherence'] or
            self.state.dream_charge < self.config['dream_threshold']):
            self.end_dream()
    
    def _update_dream_metrics(self, delta_time: float) -> None:
        """
        Update dream metrics
        
        Args:
            delta_time: Time since last update
        """
        current_time = time.time()
        
        # Update base metrics
        self.state.dream_metrics['vividness'] = (
            self.state.dream_charge * 0.6 +
            self.state.dream_depth * 0.4
        )
        
        # Update stability based on coherence and entity count
        entity_factor = min(1.0, len(self.state.dream_entities) / self.config['dream_entity_limit'])
        self.state.dream_metrics['stability'] = (
            self.state.dream_coherence * 0.7 +
            (1.0 - entity_factor) * 0.3
        )
        
        # Update novelty based on new entities and connections
        new_entities = len(self.state.dream_entities) / self.config['dream_entity_limit']
        new_connections = sum(len(conns) for conns in self.state.dream_connections.values())
        connection_factor = min(1.0, new_connections / (self.config['dream_entity_limit'] * 2))
        self.state.dream_metrics['novelty'] = (
            new_entities * 0.5 +
            connection_factor * 0.5
        )
        
        # Update emotional intensity based on charge and momentum
        self.state.dream_metrics['emotional_intensity'] = (
            self.state.dream_charge * 0.6 +
            abs(self.state.dream_momentum) * 0.4
        )
        
        # Update periodic metrics
        if current_time - self.last_metric_update >= self.config['metric_update_interval']:
            # Update dream state metric
            base_value = self.state.dream_metrics['dream_state']
            variation = math.sin(current_time * 0.1) * 10 + random.uniform(-2, 2)
            self.state.dream_metrics['dream_state'] = max(0, min(100, base_value + variation))
            
            # Update REM activity metric
            base_value = self.state.dream_metrics['rem_activity']
            variation = math.sin(current_time * 0.1) * 10 + random.uniform(-2, 2)
            self.state.dream_metrics['rem_activity'] = max(0, min(100, base_value + variation))
            
            # Update lucidity metric
            base_value = self.state.dream_metrics['lucidity']
            variation = math.sin(current_time * 0.1) * 10 + random.uniform(-2, 2)
            self.state.dream_metrics['lucidity'] = max(0, min(100, base_value + variation))
            
            self.last_metric_update = current_time
    
    def add_dream_entity(self, entity_id: str, connections: Optional[List[str]] = None) -> None:
        """
        Add entity to current dream
        
        Args:
            entity_id: Entity identifier
            connections: List of connected entity IDs
        """
        if not self.state.is_dreaming:
            return
        
        if len(self.state.dream_entities) >= self.config['dream_entity_limit']:
            # Remove oldest entity if at limit
            oldest = next(iter(self.state.dream_entities))
            self.state.dream_entities.remove(oldest)
            if oldest in self.state.dream_connections:
                del self.state.dream_connections[oldest]
        
        self.state.dream_entities.add(entity_id)
        if connections:
            self.state.dream_connections[entity_id] = connections
    
    def get_dream_state(self) -> Dict:
        """Get current dream state"""
        return {
            'is_dreaming': self.state.is_dreaming,
            'dream_depth': self.state.dream_depth,
            'dream_coherence': self.state.dream_coherence,
            'dream_charge': self.state.dream_charge,
            'dream_momentum': self.state.dream_momentum,
            'entity_count': len(self.state.dream_entities),
            'metrics': self.state.dream_metrics.copy(),
            'dream_duration': time.time() - self.state.last_dream_time if self.state.is_dreaming else 0.0
        }
    
    def get_dream_history(self) -> List[Dict]:
        """Get dream history"""
        return self.state.dream_history.copy()
    
    def get_metrics_json(self) -> str:
        """Get current metrics as JSON string"""
        return json.dumps({
            "type": "metrics",
            "subprocess_id": "dream_engine",
            "metrics": {
                "dream_state": self.state.dream_metrics['dream_state'],
                "rem_activity": self.state.dream_metrics['rem_activity'],
                "lucidity": self.state.dream_metrics['lucidity']
            },
            "timestamp": time.time()
        })

# Global instance
_dream_engine = None

def get_dream_engine() -> DreamEngine:
    """Get or create the global dream engine instance"""
    global _dream_engine
    if _dream_engine is None:
        _dream_engine = DreamEngine()
    return _dream_engine

__all__ = ['DreamEngine', 'get_dream_engine']

def main():
    """Dummy subprocess for Dream Engine"""
    engine = get_dream_engine()
    
    while True:
        # Update dream state
        engine.update_dream(0.5)  # 500ms delta
        
        # Output metrics
        print(engine.get_metrics_json())
        
        time.sleep(0.5)  # Update every 500ms

if __name__ == "__main__":
    main()
