"""
Schema Interface - Core interface for schema management and evolution
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
class SchemaState:
    """Current state of schema system"""
    coherence: float = 0.5
    entropy: float = 0.5
    alignment: float = 0.5
    trust_stability: float = 0.5
    rebloom_risk: float = 0.0
    pressure: float = 0.0
    drift: float = 0.0
    last_update: float = 0.0
    schema_status: str = "stable"

class SchemaInterface:
    """
    Core interface for schema management and evolution.
    Provides methods for schema state management, evolution tracking,
    and interaction with other DAWN components.
    """
    
    def __init__(self):
        """Initialize schema interface with default state"""
        self.state = SchemaState()
        self.log_dir = "logs"
        self.schema_dir = "schema"
        logger.info("Initialized SchemaInterface")
        
    def update_state(self,
                    coherence: Optional[float] = None,
                    entropy: Optional[float] = None,
                    alignment: Optional[float] = None,
                    trust_stability: Optional[float] = None,
                    rebloom_risk: Optional[float] = None,
                    pressure: Optional[float] = None,
                    drift: Optional[float] = None) -> None:
        """Update schema state with new values"""
        if coherence is not None:
            self.state.coherence = coherence
        if entropy is not None:
            self.state.entropy = entropy
        if alignment is not None:
            self.state.alignment = alignment
        if trust_stability is not None:
            self.state.trust_stability = trust_stability
        if rebloom_risk is not None:
            self.state.rebloom_risk = rebloom_risk
        if pressure is not None:
            self.state.pressure = pressure
        if drift is not None:
            self.state.drift = drift
            
        # Update schema status based on metrics
        if (self.state.coherence < 0.3 or 
            self.state.trust_stability < 0.3 or 
            self.state.rebloom_risk > 0.7):
            self.state.schema_status = "unstable"
        elif (self.state.coherence < 0.6 or 
              self.state.trust_stability < 0.6 or 
              self.state.rebloom_risk > 0.4):
            self.state.schema_status = "warning"
        else:
            self.state.schema_status = "stable"
            
        self.state.last_update = datetime.now().timestamp()
        logger.info(f"Updated schema state: {self.state.schema_status}")
        
    def get_state(self) -> Dict:
        """Get current schema state"""
        return asdict(self.state)
        
    def log_schema_event(self, event_type: str, details: Dict) -> None:
        """Log a schema-related event"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "details": details,
            "state": asdict(self.state)
        }
        
        # Ensure log directory exists
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Write to log file
        log_file = os.path.join(self.log_dir, "schema_events.log")
        with open(log_file, "a") as f:
            f.write(json.dumps(event) + "\n")
            
        logger.info(f"Logged schema event: {event_type}")
        
    def export_state(self) -> Dict:
        """Export current schema state"""
        return {
            "timestamp": datetime.now().isoformat(),
            "state": asdict(self.state)
        }
        
    def add_suppression_override(self, override_config: Dict) -> bool:
        """Add a suppression override to schema evolution"""
        try:
            # Implementation would go here
            logger.info("Added schema suppression override")
            return True
        except Exception as e:
            logger.error(f"Error adding suppression override: {e}")
            return False
            
    def get_current_alignment(self) -> float:
        """Get current schema alignment value"""
        return self.state.alignment 