"""
Mood Tracker - Manages system mood metrics
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MoodState:
    """Current state of mood tracking"""
    valence: float = 0.5
    arousal: float = 0.5
    tag: str = 'neutral'
    mood_entropy: float = 0.5

class MoodTracker:
    """Tracks system mood metrics"""
    
    def __init__(self):
        """Initialize mood tracker"""
        self._state = MoodState()
        logger.info("Initialized MoodTracker")
        
    def get_mood(self) -> Dict[str, Any]:
        """Get current mood state"""
        return {
            'valence': self._state.valence,
            'arousal': self._state.arousal,
            'tag': self._state.tag,
            'entropy': self._state.mood_entropy
        }
        
    def get_mood_entropy(self) -> float:
        """Get current mood entropy"""
        return self._state.mood_entropy
        
    def update_mood(self, valence: float = None, arousal: float = None, tag: str = None) -> None:
        """Update mood state"""
        if valence is not None:
            if not 0.0 <= valence <= 1.0:
                logger.warning(f"Valence value {valence} out of range [0.0, 1.0]")
                valence = max(0.0, min(1.0, valence))
            self._state.valence = valence
            
        if arousal is not None:
            if not 0.0 <= arousal <= 1.0:
                logger.warning(f"Arousal value {arousal} out of range [0.0, 1.0]")
                arousal = max(0.0, min(1.0, arousal))
            self._state.arousal = arousal
            
        if tag is not None:
            self._state.tag = tag
            
        # Update mood entropy based on valence/arousal distance from neutral
        valence_dist = abs(self._state.valence - 0.5)
        arousal_dist = abs(self._state.arousal - 0.5)
        self._state.mood_entropy = (valence_dist + arousal_dist) / 2 