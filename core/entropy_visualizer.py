"""
Entropy Visualizer - Visualizes DAWN's entropy state and dynamics
"""

import logging
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EntropyState:
    """Current state of entropy visualization"""
    total_entropy: float = 0.0
    mood_entropy: float = 0.0
    sigil_entropy: float = 0.0
    bloom_entropy: float = 0.0
    last_update: float = 0.0
    entropy_trend: str = "stable"

class EntropyVisualizer:
    """
    Visualizes DAWN's entropy state and dynamics.
    Provides real-time visualization of various entropy components.
    """
    
    def __init__(self):
        """Initialize entropy visualizer with default state"""
        self.state = EntropyState()
        self.log_dir = "logs"
        logger.info("Initialized EntropyVisualizer")
        
    def update_state(self, total_entropy: float, mood_entropy: float, 
                    sigil_entropy: float, bloom_entropy: float) -> None:
        """Update entropy visualization state"""
        self.state.total_entropy = total_entropy
        self.state.mood_entropy = mood_entropy
        self.state.sigil_entropy = sigil_entropy
        self.state.bloom_entropy = bloom_entropy
        self.state.last_update = datetime.now().timestamp()
        
        # Update entropy trend
        if total_entropy > 0.7:
            self.state.entropy_trend = "increasing"
        elif total_entropy < 0.3:
            self.state.entropy_trend = "decreasing"
        else:
            self.state.entropy_trend = "stable"
        
    def get_visualization(self) -> Dict:
        """Get current entropy visualization state"""
        return {
            "total_entropy": self.state.total_entropy,
            "mood_entropy": self.state.mood_entropy,
            "sigil_entropy": self.state.sigil_entropy,
            "bloom_entropy": self.state.bloom_entropy,
            "entropy_trend": self.state.entropy_trend,
            "last_update": self.state.last_update
        }
        
    def log_entropy_event(self, event_type: str, details: Dict) -> None:
        """Log entropy events for analysis"""
        event = {
            "timestamp": datetime.now().timestamp(),
            "type": event_type,
            "details": details,
            "state": self.get_visualization()
        }
        logger.info(f"Entropy event: {event_type} - {details}")
        
    def export_state(self) -> Dict:
        """Export current entropy state for persistence"""
        return {
            "total_entropy": self.state.total_entropy,
            "mood_entropy": self.state.mood_entropy,
            "sigil_entropy": self.state.sigil_entropy,
            "bloom_entropy": self.state.bloom_entropy,
            "entropy_trend": self.state.entropy_trend,
            "last_update": self.state.last_update
        } 