"""
Entropy Tracker - Manages system entropy metrics
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EntropyState:
    """Current state of entropy tracking"""
    entropy_index: float = 0.5
    mood_entropy: float = 0.5
    sigil_entropy: float = 0.5
    bloom_entropy: float = 0.5
    total_entropy: float = 0.5

class EntropyTracker:
    """Tracks system entropy and stability metrics"""
    
    def __init__(self):
        """Initialize the entropy tracker"""
        self.entropy = 0.5  # Start at neutral entropy
        self.stability = 1.0
        self.last_update = datetime.now(timezone.utc)
        self.history = []
        logger.info("Initialized EntropyTracker")
        
    def update(self, scup: float, tension: float) -> None:
        """Update entropy based on SCUP and tension"""
        try:
            current_time = datetime.now(timezone.utc)
            time_delta = (current_time - self.last_update).total_seconds()
            self.last_update = current_time
            
            # Calculate entropy change based on SCUP and tension
            scup_contribution = abs(scup - 0.5) * 0.3
            tension_contribution = tension * 0.7
            entropy_change = (scup_contribution + tension_contribution) * time_delta
            
            # Update entropy with damping
            self.entropy = max(0.0, min(1.0, self.entropy + entropy_change))
            
            # Update stability
            self.stability = 1.0 - abs(self.entropy - 0.5) * 2
            
            # Store in history
            self.history.append({
                "timestamp": current_time.isoformat(),
                "entropy": self.entropy,
                "stability": self.stability,
                "scup": scup,
                "tension": tension
            })
            
            # Keep history manageable
            if len(self.history) > 100:
                self.history.pop(0)
                
            logger.debug(f"Updated entropy: {self.entropy:.2f}, stability: {self.stability:.2f}")
            
        except Exception as e:
            logger.error(f"Error updating entropy: {e}")
            
    def get_entropy(self) -> float:
        """Get current entropy value"""
        return self.entropy
        
    def get_stability(self) -> float:
        """Get current stability value"""
        return self.stability
        
    def update_health(self, entropy: float, tension: float) -> None:
        """Update health metrics based on entropy and tension"""
        try:
            self.update(entropy, tension)
            if self.stability < 0.3:
                logger.warning("Low system stability detected")
        except Exception as e:
            logger.error(f"Error updating health: {e}")
            
    def get_state(self) -> Dict[str, Any]:
        """Get current state"""
        return {
            "entropy": self.entropy,
            "stability": self.stability,
            "last_update": self.last_update.isoformat(),
            "history_length": len(self.history)
        }

    def get_entropy_index(self) -> float:
        """Get current entropy index"""
        return self._state.entropy_index
        
    def get_mood_entropy(self) -> float:
        """Get current mood entropy"""
        return self._state.mood_entropy
        
    def get_sigil_entropy(self) -> float:
        """Get current sigil entropy"""
        return self._state.sigil_entropy
        
    def get_bloom_entropy(self) -> float:
        """Get current bloom entropy"""
        return self._state.bloom_entropy
        
    def get_total_entropy(self) -> float:
        """Get total system entropy"""
        return self._state.total_entropy
        
    def update_entropy(self, entropy_type: str, value: float) -> None:
        """Update specific entropy value"""
        if not 0.0 <= value <= 1.0:
            logger.warning(f"Entropy value {value} out of range [0.0, 1.0]")
            value = max(0.0, min(1.0, value))
            
        if entropy_type == 'mood':
            self._state.mood_entropy = value
        elif entropy_type == 'sigil':
            self._state.sigil_entropy = value
        elif entropy_type == 'bloom':
            self._state.bloom_entropy = value
        else:
            logger.warning(f"Unknown entropy type: {entropy_type}")
            return
            
        # Update total entropy
        self._state.total_entropy = (
            self._state.mood_entropy * 0.3 +
            self._state.sigil_entropy * 0.3 +
            self._state.bloom_entropy * 0.4
        )
        
        # Update entropy index
        self._state.entropy_index = self._state.total_entropy 