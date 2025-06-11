"""
Sigil Memory - Manages system sigil storage and recall
"""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SigilState:
    """Current state of sigil memory"""
    active_sigils: List[Dict] = None
    entropy: float = 0.5
    
    def __post_init__(self):
        if self.active_sigils is None:
            self.active_sigils = []

class SigilMemory:
    """Manages system sigil storage and recall"""
    
    def __init__(self):
        """Initialize sigil memory"""
        self._state = SigilState()
        logger.info("Initialized SigilMemory")
        
    def get_entropy(self) -> float:
        """Get current sigil entropy"""
        return self._state.entropy
        
    def add_sigil(self, sigil: Dict[str, Any]) -> None:
        """Add a new sigil to memory"""
        self._state.active_sigils.append(sigil)
        self._update_entropy()
        
    def remove_sigil(self, sigil_id: str) -> None:
        """Remove a sigil from memory"""
        self._state.active_sigils = [
            s for s in self._state.active_sigils 
            if s.get('id') != sigil_id
        ]
        self._update_entropy()
        
    def get_active_sigils(self) -> List[Dict]:
        """Get all active sigils"""
        return self._state.active_sigils.copy()
        
    def _update_entropy(self) -> None:
        """Update sigil entropy based on number of active sigils"""
        # Simple entropy calculation based on number of sigils
        num_sigils = len(self._state.active_sigils)
        self._state.entropy = min(1.0, num_sigils / 10.0)  # Cap at 1.0 