"""
Alignment Visualizer - Visualizes DAWN's alignment state and drift
"""

import logging
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AlignmentState:
    """Current state of alignment visualization"""
    current_alignment: float = 0.5
    alignment_drift: float = 0.0
    trust_stability: float = 0.0
    last_update: float = 0.0
    alignment_status: str = "stable"

class AlignmentVisualizer:
    """
    Visualizes DAWN's alignment state and drift.
    Provides real-time visualization of system alignment metrics.
    """
    
    def __init__(self):
        """Initialize alignment visualizer with default state"""
        self.state = AlignmentState()
        self.log_dir = "logs"
        logger.info("Initialized AlignmentVisualizer")
        
    def update_state(self, current_alignment: float, alignment_drift: float, 
                    trust_stability: float) -> None:
        """Update alignment visualization state"""
        self.state.current_alignment = current_alignment
        self.state.alignment_drift = alignment_drift
        self.state.trust_stability = trust_stability
        self.state.last_update = datetime.now().timestamp()
        
        # Update alignment status
        if alignment_drift > 0.7:
            self.state.alignment_status = "drifting"
        elif trust_stability < 0.3:
            self.state.alignment_status = "unstable"
        else:
            self.state.alignment_status = "stable"
        
    def get_visualization(self) -> Dict:
        """Get current alignment visualization state"""
        return {
            "current_alignment": self.state.current_alignment,
            "alignment_drift": self.state.alignment_drift,
            "trust_stability": self.state.trust_stability,
            "alignment_status": self.state.alignment_status,
            "last_update": self.state.last_update
        }
        
    def log_alignment_event(self, event_type: str, details: Dict) -> None:
        """Log alignment events for analysis"""
        event = {
            "timestamp": datetime.now().timestamp(),
            "type": event_type,
            "details": details,
            "state": self.get_visualization()
        }
        logger.info(f"Alignment event: {event_type} - {details}")
        
    def export_state(self) -> Dict:
        """Export current alignment state for persistence"""
        return {
            "current_alignment": self.state.current_alignment,
            "alignment_drift": self.state.alignment_drift,
            "trust_stability": self.state.trust_stability,
            "alignment_status": self.state.alignment_status,
            "last_update": self.state.last_update
        } 