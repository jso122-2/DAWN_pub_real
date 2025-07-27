"""
Schema Evolution Engine - Core schema evolution and adaptation system
"""

import logging
import json
import os
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EvolutionState:
    """Current state of schema evolution"""
    evolution_rate: float = 0.1
    adaptation_threshold: float = 0.5
    suppression_active: bool = False
    last_evolution: float = 0.0
    evolution_status: str = "stable"

class SchemaEvolutionEngine:
    """
    Core schema evolution and adaptation system.
    Manages schema evolution, suppression, and adaptation.
    """
    
    def __init__(self):
        """Initialize schema evolution engine with default state"""
        self.state = EvolutionState()
        self.log_dir = "logs"
        self.suppression_overrides = {}
        self.evolution_state = "stable"
        self.scup = 0.5
        self.entropy = 0.5
        self.mood = "neutral"
        logger.info("Initialized SchemaEvolutionEngine")
        
    def update_state(self,
                    evolution_rate: Optional[float] = None,
                    adaptation_threshold: Optional[float] = None,
                    suppression_active: Optional[bool] = None) -> None:
        """Update evolution engine state"""
        if evolution_rate is not None:
            self.state.evolution_rate = evolution_rate
        if adaptation_threshold is not None:
            self.state.adaptation_threshold = adaptation_threshold
        if suppression_active is not None:
            self.state.suppression_active = suppression_active
            
        # Update evolution status based on metrics
        if self.state.evolution_rate > 0.8 or self.state.suppression_active:
            self.state.evolution_status = "unstable"
        elif self.state.evolution_rate > 0.5:
            self.state.evolution_status = "warning"
        else:
            self.state.evolution_status = "stable"
            
        self.state.last_evolution = datetime.now(timezone.utc).timestamp()
        logger.info(f"Updated evolution state: {self.state.evolution_status}")
        
    def add_suppression_override(self, override_config: Dict) -> bool:
        """Add a suppression override to schema evolution"""
        try:
            override_id = override_config.get('id', str(len(self.suppression_overrides)))
            self.suppression_overrides[override_id] = {
                'config': override_config,
                'timestamp': datetime.now(timezone.utc).timestamp()
            }
            self.state.suppression_active = True
            logger.info(f"Added suppression override: {override_id}")
            return True
        except Exception as e:
            logger.error(f"Error adding suppression override: {e}")
            return False
            
    def remove_suppression_override(self, override_id: str) -> bool:
        """Remove a suppression override"""
        try:
            if override_id in self.suppression_overrides:
                del self.suppression_overrides[override_id]
                if not self.suppression_overrides:
                    self.state.suppression_active = False
                logger.info(f"Removed suppression override: {override_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error removing suppression override: {e}")
            return False
            
    def get_state(self) -> Dict:
        """Get current evolution engine state"""
        return asdict(self.state)
        
    def log_evolution_event(self, event_type: str, details: Dict) -> None:
        """Log an evolution-related event"""
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": event_type,
            "details": details,
            "state": asdict(self.state)
        }
        
        # Ensure log directory exists
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Write to log file
        log_file = os.path.join(self.log_dir, "evolution_events.log")
        with open(log_file, "a") as f:
            f.write(json.dumps(event) + "\n")
            
        logger.info(f"Logged evolution event: {event_type}")
        
    def export_state(self) -> Dict:
        """Export current evolution engine state"""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "state": asdict(self.state),
            "suppression_overrides": self.suppression_overrides
        }

    def get_scup(self) -> float:
        """Get current SCUP value"""
        return self.scup
        
    def get_entropy(self) -> float:
        """Get current entropy value"""
        return self.entropy
        
    def get_mood(self) -> str:
        """Get current mood state"""
        return self.mood
        
    def update_state(self, scup: float, entropy: float, mood: str):
        """Update evolution state"""
        self.scup = scup
        self.entropy = entropy
        self.mood = mood
        
        # Update evolution state based on values
        if abs(scup - 0.5) > 0.3 or entropy > 0.7:
            self.evolution_state = "unstable"
        else:
            self.evolution_state = "stable"
            
        logger.info(f"Updated evolution state: {self.evolution_state}")
        
    def evolve_schema(self, schema_state: dict, mood_state: dict):
        """Evolve schema based on current state"""
        # Schema evolution logic here
        pass
        
    async def update(self) -> None:
        """Update schema evolution engine state"""
        try:
            # Update evolution state
            self.update_state(
                evolution_rate=self.state.evolution_rate,
                adaptation_threshold=self.state.adaptation_threshold,
                suppression_active=self.state.suppression_active
            )
            
            # Log evolution event if state changed
            if self.state.evolution_status != self.evolution_state:
                self.log_evolution_event(
                    "state_change",
                    {
                        "old_state": self.evolution_state,
                        "new_state": self.state.evolution_status
                    }
                )
                self.evolution_state = self.state.evolution_status
                
            logger.debug("Updated schema evolution engine")
            
        except Exception as e:
            logger.error(f"Error updating schema evolution engine: {e}")

# Global instance
schema_evolution_engine = SchemaEvolutionEngine()

# Export key functions
__all__ = [
    'schema_evolution_engine',
    'add_suppression_override'
]

def add_suppression_override(override_config: Dict) -> bool:
    """Add a suppression override to schema evolution"""
    return schema_evolution_engine.add_suppression_override(override_config) 