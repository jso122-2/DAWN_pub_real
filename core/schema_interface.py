"""
Schema Interface - Interface between consciousness and schema systems
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class SchemaState:
    """Current state of the schema system"""
    coherence: float = 0.5
    entropy: float = 0.5
    drift: float = 0.0
    tension: float = 0.0
    active_blooms: int = 0
    sealed_blooms: int = 0
    rebloom_stability: float = 0.7
    preview_heat: float = 0.0
    preview_stability: float = 0.0
    preview_entropy: float = 0.0
    schema_status: str = "reflective"

class SchemaInterface:
    """Interface for schema system interactions"""
    
    def __init__(self):
        """Initialize schema interface"""
        self.state = SchemaState()
        self._schema_calculator = None
        self._schema_evolution_engine = None
        logger.info("Initialized SchemaInterface")
    
    def set_schema_calculator(self, calculator):
        """Set the schema calculator instance"""
        self._schema_calculator = calculator
    
    def set_schema_evolution_engine(self, engine):
        """Set the schema evolution engine instance"""
        self._schema_evolution_engine = engine
    
    def update_state(self, new_state: Dict[str, Any]) -> None:
        """Update schema state with new values"""
        try:
            for key, value in new_state.items():
                if hasattr(self.state, key):
                    setattr(self.state, key, value)
        except Exception as e:
            logger.error(f"Error updating schema state: {e}")
    
    def get_state(self) -> Dict[str, Any]:
        """Get current schema state"""
        return {
            'coherence': self.state.coherence,
            'entropy': self.state.entropy,
            'drift': self.state.drift,
            'tension': self.state.tension,
            'active_blooms': self.state.active_blooms,
            'sealed_blooms': self.state.sealed_blooms,
            'rebloom_stability': self.state.rebloom_stability,
            'preview_heat': self.state.preview_heat,
            'preview_stability': self.state.preview_stability,
            'preview_entropy': self.state.preview_entropy,
            'schema_status': self.state.schema_status
        }
    
    async def calculate_schema_metrics(self) -> Dict[str, float]:
        """Calculate schema metrics using the calculator"""
        if not self._schema_calculator:
            return {
                'coherence': 0.5,
                'entropy': 0.5,
                'drift': 0.0,
                'tension': 0.0
            }
        
        try:
            return await self._schema_calculator.calculate_metrics(self.get_state())
        except Exception as e:
            logger.error(f"Error calculating schema metrics: {e}")
            return {
                'coherence': 0.5,
                'entropy': 0.5,
                'drift': 0.0,
                'tension': 0.0
            }
    
    async def evolve_schema(self, current_state: Dict[str, Any], mood_state: Dict[str, Any]) -> None:
        """Trigger schema evolution if engine is available"""
        if not self._schema_evolution_engine:
            return
        
        try:
            await self._schema_evolution_engine.evolve_schema(current_state, mood_state)
        except Exception as e:
            logger.error(f"Error evolving schema: {e}")
    
    def get_schema_status(self) -> str:
        """Get current schema status"""
        return self.state.schema_status
    
    def set_schema_status(self, status: str) -> None:
        """Set schema status"""
        self.state.schema_status = status 