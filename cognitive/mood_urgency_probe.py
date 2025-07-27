# /schema/mood_urgency_probe.py

import math
from typing import Dict, Optional, Tuple, List
import logging
import time
from dataclasses import dataclass, field
from core.schema_anomaly_logger import log_anomaly

logger = logging.getLogger(__name__)

@dataclass
class MoodState:
    """Current mood state of the system"""
    valence: float = 0.0  # Positive/negative (-1 to 1)
    arousal: float = 0.0  # Energy level (0 to 1)
    dominance: float = 0.5  # Control level (0 to 1)
    urgency: float = 0.0  # Urgency level (0 to 1)
    last_update: float = field(default_factory=time.time)
    history: List[Dict] = field(default_factory=list)

class MoodUrgencyProbe:
    """Probes and analyzes mood states and urgency levels"""
    
    def __init__(self):
        """Initialize the mood urgency probe"""
        self.state = MoodState()
        self.config = {
            'history_size': 100,
            'decay_rate': 0.95,
            'urgency_threshold': 0.7,
            'mood_update_interval': 1.0
        }
        logger.info("Initialized MoodUrgencyProbe")
    
    def update_mood(self, 
                   valence: Optional[float] = None,
                   arousal: Optional[float] = None,
                   dominance: Optional[float] = None) -> None:
        """
        Update the current mood state
        
        Args:
            valence: New valence value (-1 to 1)
            arousal: New arousal value (0 to 1)
            dominance: New dominance value (0 to 1)
        """
        # Update values if provided
        if valence is not None:
            self.state.valence = max(-1.0, min(1.0, valence))
        if arousal is not None:
            self.state.arousal = max(0.0, min(1.0, arousal))
        if dominance is not None:
            self.state.dominance = max(0.0, min(1.0, dominance))
        
        # Calculate urgency
        self._update_urgency()
        
        # Record history
        self._record_history()
        
        # Update timestamp
        self.state.last_update = time.time()
        
        # Check for anomalies
        self._check_anomalies()
    
    def _update_urgency(self) -> None:
        """Update the urgency level based on current mood state"""
        # Urgency increases with high arousal and negative valence
        arousal_factor = self.state.arousal
        valence_factor = (1.0 - self.state.valence) / 2.0  # Convert -1,1 to 0,1
        dominance_factor = 1.0 - self.state.dominance  # Lower dominance = higher urgency
        
        # Calculate urgency as weighted combination
        self.state.urgency = (
            0.4 * arousal_factor +
            0.4 * valence_factor +
            0.2 * dominance_factor
        )
    
    def _record_history(self) -> None:
        """Record current state in history"""
        state_record = {
            'timestamp': time.time(),
            'valence': self.state.valence,
            'arousal': self.state.arousal,
            'dominance': self.state.dominance,
            'urgency': self.state.urgency
        }
        
        self.state.history.append(state_record)
        
        # Trim history if too long
        if len(self.state.history) > self.config['history_size']:
            self.state.history = self.state.history[-self.config['history_size']:]
    
    def _check_anomalies(self) -> None:
        """Check for anomalous mood states"""
        # Check for extreme urgency
        if self.state.urgency > self.config['urgency_threshold']:
            log_anomaly(
                'high_urgency',
                {
                    'urgency': self.state.urgency,
                    'valence': self.state.valence,
                    'arousal': self.state.arousal,
                    'dominance': self.state.dominance
                },
                severity='warning'
            )
        
        # Check for mood instability
        if len(self.state.history) >= 2:
            last_state = self.state.history[-2]
            current_state = self.state.history[-1]
            
            # Calculate mood change
            valence_change = abs(current_state['valence'] - last_state['valence'])
            arousal_change = abs(current_state['arousal'] - last_state['arousal'])
            
            if valence_change > 0.5 or arousal_change > 0.5:
                log_anomaly(
                    'mood_instability',
                    {
                        'valence_change': valence_change,
                        'arousal_change': arousal_change,
                        'current_state': current_state,
                        'previous_state': last_state
                    },
                    severity='warning'
                )
    
    def get_state(self) -> Dict:
        """Get current mood state"""
        return {
            'valence': self.state.valence,
            'arousal': self.state.arousal,
            'dominance': self.state.dominance,
            'urgency': self.state.urgency,
            'last_update': self.state.last_update
        }
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get mood history"""
        if limit is None:
            return self.state.history
        return self.state.history[-limit:]

# Global instance
_mood_probe = None

def get_mood_probe() -> MoodUrgencyProbe:
    """Get or create the global mood probe instance"""
    global _mood_probe
    if _mood_probe is None:
        _mood_probe = MoodUrgencyProbe()
    return _mood_probe

__all__ = ['MoodUrgencyProbe', 'get_mood_probe']
