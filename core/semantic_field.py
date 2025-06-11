"""
Semantic Field - Core semantic topology and alignment management
"""

import logging
import json
import os
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SemanticState:
    """Current state of semantic field"""
    alignment: float = 0.5
    coherence: float = 0.5
    entropy: float = 0.5
    node_count: int = 0
    connection_count: int = 0
    last_update: float = 0.0
    semantic_status: str = "stable"

class SemanticField:
    """
    Core semantic field management system.
    Handles semantic topology, alignment, and coherence.
    """
    
    def __init__(self):
        """Initialize semantic field with default state"""
        self.state = SemanticState()
        self.log_dir = "logs"
        logger.info("Initialized SemanticField")
        
    def update_state(self,
                    alignment: Optional[float] = None,
                    coherence: Optional[float] = None,
                    entropy: Optional[float] = None,
                    node_count: Optional[int] = None,
                    connection_count: Optional[int] = None) -> None:
        """Update semantic field state"""
        if alignment is not None:
            self.state.alignment = alignment
        if coherence is not None:
            self.state.coherence = coherence
        if entropy is not None:
            self.state.entropy = entropy
        if node_count is not None:
            self.state.node_count = node_count
        if connection_count is not None:
            self.state.connection_count = connection_count
            
        # Update semantic status based on metrics
        if (self.state.coherence < 0.3 or 
            self.state.alignment < 0.3 or 
            self.state.entropy > 0.7):
            self.state.semantic_status = "unstable"
        elif (self.state.coherence < 0.6 or 
              self.state.alignment < 0.6 or 
              self.state.entropy > 0.4):
            self.state.semantic_status = "warning"
        else:
            self.state.semantic_status = "stable"
            
        self.state.last_update = datetime.now().timestamp()
        logger.info(f"Updated semantic state: {self.state.semantic_status}")
        
    def get_current_alignment(self) -> float:
        """Get current semantic alignment value"""
        return self.state.alignment
        
    def get_state(self) -> Dict:
        """Get current semantic field state"""
        return asdict(self.state)
        
    def log_semantic_event(self, event_type: str, details: Dict) -> None:
        """Log a semantic-related event"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "details": details,
            "state": asdict(self.state)
        }
        
        # Ensure log directory exists
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Write to log file
        log_file = os.path.join(self.log_dir, "semantic_events.log")
        with open(log_file, "a") as f:
            f.write(json.dumps(event) + "\n")
            
        logger.info(f"Logged semantic event: {event_type}")
        
    def export_state(self) -> Dict:
        """Export current semantic field state"""
        return {
            "timestamp": datetime.now().isoformat(),
            "state": asdict(self.state)
        }

# Global instance
semantic_field = SemanticField()

# Export key functions
__all__ = [
    'semantic_field',
    'get_current_alignment'
]

def get_current_alignment() -> float:
    """Get current semantic alignment value"""
    return semantic_field.get_current_alignment() 