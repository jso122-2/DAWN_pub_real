#!/usr/bin/env python3
import json
import time
import random
import math
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class AwarenessState:
    """Current state of the awareness system"""
    focus_level: float = 0.0
    clarity: float = 0.0
    presence: float = 0.0
    last_update: float = field(default_factory=time.time)
    awareness_history: List[Dict] = field(default_factory=list)

class AwarenessEngine:
    """Manages DAWN's awareness and consciousness processes"""
    
    def __init__(self):
        """Initialize the awareness engine"""
        self.state = AwarenessState()
        self.config = {
            'history_size': 100,
            'decay_rate': 0.95,
            'clarity_threshold': 0.7,
            'update_interval': 1.0
        }
        logger.info("Initialized AwarenessEngine")
    
    def update_awareness(self, 
                        focus_level: Optional[float] = None,
                        clarity: Optional[float] = None,
                        presence: Optional[float] = None) -> None:
        """
        Update the current awareness state
        
        Args:
            focus_level: New focus level (0 to 1)
            clarity: New clarity level (0 to 1)
            presence: New presence level (0 to 1)
        """
        # Update values if provided
        if focus_level is not None:
            self.state.focus_level = max(0.0, min(1.0, focus_level))
        if clarity is not None:
            self.state.clarity = max(0.0, min(1.0, clarity))
        if presence is not None:
            self.state.presence = max(0.0, min(1.0, presence))
        
        # Record state
        self._record_state()
        
        # Update timestamp
        self.state.last_update = time.time()
        
        # Check for anomalies
        self._check_anomalies()
    
    def _record_state(self) -> None:
        """Record current state in history"""
        state_record = {
            'timestamp': time.time(),
            'focus_level': self.state.focus_level,
            'clarity': self.state.clarity,
            'presence': self.state.presence
        }
        
        self.state.awareness_history.append(state_record)
        
        # Trim history if too long
        if len(self.state.awareness_history) > self.config['history_size']:
            self.state.awareness_history = self.state.awareness_history[-self.config['history_size']:]
    
    def _check_anomalies(self) -> None:
        """Check for anomalous awareness states"""
        # Check for extreme clarity
        if self.state.clarity > self.config['clarity_threshold']:
            logger.warning(f"High clarity state detected: {self.state.clarity}")
        
        # Check for awareness instability
        if len(self.state.awareness_history) >= 2:
            last_state = self.state.awareness_history[-2]
            current_state = self.state.awareness_history[-1]
            
            # Calculate state change
            focus_change = abs(current_state['focus_level'] - last_state['focus_level'])
            clarity_change = abs(current_state['clarity'] - last_state['clarity'])
            
            if focus_change > 0.5 or clarity_change > 0.5:
                logger.warning(f"Awareness instability detected: focus={focus_change}, clarity={clarity_change}")
    
    def get_state(self) -> Dict:
        """Get current awareness state"""
        return {
            'focus_level': self.state.focus_level,
            'clarity': self.state.clarity,
            'presence': self.state.presence,
            'last_update': self.state.last_update
        }
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get awareness history"""
        if limit is None:
            return self.state.awareness_history
        return self.state.awareness_history[-limit:]
    
    def process_consciousness(self, consciousness_data: Dict[str, Any]) -> None:
        """
        Process consciousness data and update awareness state
        
        Args:
            consciousness_data: Dictionary containing consciousness metrics
        """
        # Extract relevant metrics
        focus = consciousness_data.get('focus', 0.0)
        clarity = consciousness_data.get('clarity', 0.0)
        presence = consciousness_data.get('presence', 0.0)
        
        # Update awareness state
        self.update_awareness(focus, clarity, presence)
        
        # Log significant changes
        if focus > 0.8 or clarity > 0.8:
            logger.info(f"Significant consciousness state: focus={focus:.2f}, clarity={clarity:.2f}, presence={presence:.2f}")

# Global instance
_awareness_engine = None

def get_awareness_engine() -> AwarenessEngine:
    """Get or create the global awareness engine instance"""
    global _awareness_engine
    if _awareness_engine is None:
        _awareness_engine = AwarenessEngine()
    return _awareness_engine

__all__ = ['AwarenessEngine', 'get_awareness_engine']

def main():
    """Dummy subprocess for Awareness Engine"""
    metrics = {
        "awareness_level": {
                "value": 88.8,
                "unit": "%"
        },
        "focus": {
                "value": 92.1,
                "unit": "%"
        },
        "attention_span": {
                "value": 8.5,
                "unit": "s"
        }
}
    
    t = 0
    while True:
        # Update metrics with some variation
        current_metrics = {}
        
        for metric_name, metric_info in metrics.items():
            base_value = metric_info["value"]
            unit = metric_info["unit"]
            
            if unit == "%":
                # Oscillate between bounds
                variation = math.sin(t * 0.1) * 10 + random.uniform(-2, 2)
                value = max(0, min(100, base_value + variation))
            else:
                # Random walk
                variation = random.uniform(-0.1, 0.1) * base_value
                value = max(0, base_value + variation)
            
            current_metrics[metric_name] = value
        
        # Output metrics as JSON
        print(json.dumps({
            "type": "metrics",
            "subprocess_id": "awareness_engine",
            "metrics": current_metrics,
            "timestamp": time.time()
        }))
        
        time.sleep(0.5)  # Update every 500ms
        t += 0.5

if __name__ == "__main__":
    main()
