"""
Bloom Manager - Manages system bloom states
"""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BloomState:
    """Current state of bloom management"""
    active_blooms: List[Dict] = None
    sealed_blooms: List[Dict] = None
    rebloom_queue: List[Dict] = None
    rebloom_stability: float = 0.7
    
    def __post_init__(self):
        if self.active_blooms is None:
            self.active_blooms = []
        if self.sealed_blooms is None:
            self.sealed_blooms = []
        if self.rebloom_queue is None:
            self.rebloom_queue = []

class BloomManager:
    """Manages system bloom states"""
    
    def __init__(self):
        """Initialize bloom manager"""
        self._state = BloomState()
        logger.info("Initialized BloomManager")
        
    def get_rebloom_stability(self) -> float:
        """Get current rebloom stability"""
        return self._state.rebloom_stability
        
    def add_active_bloom(self, bloom: Dict[str, Any]) -> None:
        """Add a new active bloom"""
        self._state.active_blooms.append(bloom)
        
    def seal_bloom(self, bloom_id: str) -> None:
        """Seal an active bloom"""
        bloom = next(
            (b for b in self._state.active_blooms if b.get('id') == bloom_id),
            None
        )
        if bloom:
            self._state.active_blooms.remove(bloom)
            self._state.sealed_blooms.append(bloom)
            
    def queue_rebloom(self, bloom: Dict[str, Any]) -> None:
        """Queue a bloom for reblooming"""
        self._state.rebloom_queue.append(bloom)
        
    def preview_rebloom_queue(self) -> Dict[str, Any]:
        """Get preview of next rebloom"""
        if not self._state.rebloom_queue:
            return {
                'heat': 0.0,
                'stability': 0.0,
                'entropy': 0.0
            }
            
        next_bloom = self._state.rebloom_queue[0]
        return {
            'heat': next_bloom.get('heat', 0.0),
            'stability': next_bloom.get('stability', 0.0),
            'entropy': next_bloom.get('entropy', 0.0)
        } 