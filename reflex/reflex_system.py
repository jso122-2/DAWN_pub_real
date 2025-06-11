from typing import Dict, Any, Optional
from .layers.base import ReflexState
from .layers.input_layer import InputLayerManager
from .layers.evaluation_layer import RebloomEvaluator
from .layers.decision_layer import RebloomDecisionMaker
from .layers.logging_layer import RebloomLogger
from .layers.actuation_layer import RebloomController

class ReflexSystem:
    """
    Main orchestrator for the layered reflex architecture.
    Coordinates the flow of state through all layers and manages the rebloom process.
    """
    
    def __init__(self, log_dir: str = "logs/rebloom"):
        self.input_layer = InputLayerManager()
        self.evaluation_layer = RebloomEvaluator()
        self.decision_layer = RebloomDecisionMaker()
        self.logging_layer = RebloomLogger(log_dir)
        self.actuation_layer = RebloomController()
    
    def process_state(self, state: ReflexState) -> ReflexState:
        """
        Process state through all layers in sequence.
        
        Args:
            state: Initial reflex state to process
            
        Returns:
            Updated state after processing through all layers
        """
        # Process through each layer
        state = self.input_layer.process(state)
        if not self.input_layer.validate(state):
            raise ValueError("Input layer validation failed")
        
        state = self.evaluation_layer.process(state)
        if not self.evaluation_layer.validate(state):
            raise ValueError("Evaluation layer validation failed")
        
        state = self.decision_layer.process(state)
        if not self.decision_layer.validate(state):
            raise ValueError("Decision layer validation failed")
        
        state = self.logging_layer.process(state)
        if not self.logging_layer.validate(state):
            raise ValueError("Logging layer validation failed")
        
        state = self.actuation_layer.process(state)
        if not self.actuation_layer.validate(state):
            raise ValueError("Actuation layer validation failed")
        
        return state
    
    def create_initial_state(
        self,
        mood: str,
        drift_score: float,
        heat: float,
        entropy: float,
        sigil: str,
        task_id: str,
        task_router: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ReflexState:
        """
        Create initial reflex state with required fields.
        
        Args:
            mood: Current emotional tone
            drift_score: Current drift score
            heat: Current emotional heat
            entropy: Current entropy level
            sigil: Current sigil
            task_id: Current task ID
            task_router: Task router instance
            metadata: Additional metadata
            
        Returns:
            Initialized reflex state
        """
        return ReflexState(
            mood=mood,
            drift_score=drift_score,
            heat=heat,
            entropy=entropy,
            sigil=sigil,
            audit_result=None,
            metadata={
                "task_id": task_id,
                "task_router": task_router,
                **(metadata or {})
            }
        ) 