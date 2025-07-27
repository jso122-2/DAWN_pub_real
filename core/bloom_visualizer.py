"""
Bloom Visualizer - Visualizes DAWN's bloom state and rebloom dynamics
"""

import logging
import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BloomState:
    """Current state of bloom visualization"""
    active_blooms: int = 0
    sealed_blooms: int = 0
    rebloom_stability: float = 1.0
    rebloom_queue_size: int = 0
    last_update: float = 0.0
    bloom_status: str = "stable"

class BloomVisualizer:
    """
    Visualizes DAWN's bloom state and rebloom dynamics.
    Tracks active blooms, sealed blooms, and rebloom readiness.
    """
    
    def __init__(self):
        """Initialize bloom visualizer with default state"""
        self.state = BloomState()
        self.log_dir = "logs"
        logger.info("Initialized BloomVisualizer")
        
    def update_state(self, 
                    active_blooms: Optional[int] = None,
                    sealed_blooms: Optional[int] = None,
                    rebloom_stability: Optional[float] = None,
                    rebloom_queue_size: Optional[int] = None) -> None:
        """Update bloom visualization state"""
        if active_blooms is not None:
            self.state.active_blooms = active_blooms
        if sealed_blooms is not None:
            self.state.sealed_blooms = sealed_blooms
        if rebloom_stability is not None:
            self.state.rebloom_stability = rebloom_stability
        if rebloom_queue_size is not None:
            self.state.rebloom_queue_size = rebloom_queue_size
            
        # Update bloom status based on metrics
        if self.state.rebloom_stability < 0.5 or self.state.rebloom_queue_size > 10:
            self.state.bloom_status = "unstable"
        elif self.state.rebloom_stability < 0.8 or self.state.rebloom_queue_size > 5:
            self.state.bloom_status = "warning"
        else:
            self.state.bloom_status = "stable"
            
        self.state.last_update = datetime.now().timestamp()
        logger.info(f"Updated bloom state: {self.state.bloom_status}")
        
    def get_visualization(self) -> Dict:
        """Get current bloom visualization state"""
        return asdict(self.state)
        
    def log_bloom_event(self, event_type: str, details: Dict) -> None:
        """Log a bloom-related event"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "details": details,
            "state": asdict(self.state)
        }
        
        # Ensure log directory exists
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Write to log file
        log_file = os.path.join(self.log_dir, "bloom_events.log")
        with open(log_file, "a") as f:
            f.write(json.dumps(event) + "\n")
            
        logger.info(f"Logged bloom event: {event_type}")
        
    def export_state(self) -> Dict:
        """Export current bloom state"""
        return {
            "timestamp": datetime.now().isoformat(),
            "state": asdict(self.state)
        } 