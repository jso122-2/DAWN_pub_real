"""
Schema Decay Handler - Manages schema decay and evolution
"""

import logging
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class DecayState:
    """Current state of schema decay"""
    decay_rate: float = 0.1
    stability: float = 1.0
    last_update: float = field(default_factory=time.time)
    metrics: Dict[str, float] = field(default_factory=lambda: {
        'decay_rate': 0.1,
        'stability': 1.0,
        'evolution_rate': 0.0
    })

class SchemaDecayHandler:
    """
    Handles schema decay and evolution.
    Manages the rate at which schemas decay and evolve over time.
    """
    
    def __init__(self):
        """Initialize schema decay handler"""
        self.state = DecayState()
        self.config = {
            'update_interval': 1.0,  # 1 second
            'min_decay_rate': 0.01,
            'max_decay_rate': 0.5,
            'stability_threshold': 0.8
        }
        logger.info("Initialized SchemaDecayHandler")
    
    def update_metrics(self, delta_time: float) -> None:
        """Update decay metrics"""
        # Calculate decay rate based on stability
        self.state.decay_rate = max(
            self.config['min_decay_rate'],
            min(
                self.config['max_decay_rate'],
                (1.0 - self.state.stability) * self.config['max_decay_rate']
            )
        )
        
        # Update stability
        self.state.stability = max(
            0.0,
            min(1.0, self.state.stability - self.state.decay_rate * delta_time)
        )
        
        # Update metrics
        self.state.metrics.update({
            'decay_rate': self.state.decay_rate,
            'stability': self.state.stability,
            'evolution_rate': 1.0 - self.state.stability
        })
        
        self.state.last_update = time.time()
    
    def get_decay_rate(self) -> float:
        """Get current decay rate"""
        return self.state.decay_rate
    
    def get_stability(self) -> float:
        """Get current stability"""
        return self.state.stability
    
    def get_metrics(self) -> Dict[str, float]:
        """Get current metrics"""
        return self.state.metrics.copy()
    
    def get_metrics_json(self) -> str:
        """Get current metrics as JSON string"""
        import json
        return json.dumps({
            "type": "metrics",
            "subprocess_id": "schema_decay",
            "metrics": self.state.metrics,
            "timestamp": time.time()
        })

# Global instance
_decay_handler = None

def get_decay_system() -> SchemaDecayHandler:
    """Get or create the global schema decay handler instance"""
    global _decay_handler
    if _decay_handler is None:
        _decay_handler = SchemaDecayHandler()
    return _decay_handler

__all__ = ['SchemaDecayHandler', 'get_decay_system'] 