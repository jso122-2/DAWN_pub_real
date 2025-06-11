from typing import Dict, Any, Optional
from .base import ActuationLayer, ReflexState, RebloomMode
from grep.sigil_registry import SigilRegistry

class RebloomController(ActuationLayer):
    """Controls schema flow routing and task management"""
    
    def __init__(self, sigil_registry: Optional[SigilRegistry] = None):
        self.sigil_registry = sigil_registry or SigilRegistry()
    
    def _handle_sigil(self, state: ReflexState) -> None:
        """Handle sigil stability and updates"""
        if not state.sigil:
            return
        
        # If sigil is unstable, update registry
        if state.metadata.get("decision", {}).faltering:
            self.sigil_registry.register(
                sigil=state.sigil,
                definition="UNSTABLE - Requires regeneration",
                tags=["unstable", "needs_regeneration"]
            )
    
    def _route_task(self, state: ReflexState) -> None:
        """Route task based on rebloom decision"""
        decision = state.metadata.get("decision")
        if not decision or not decision.should_rebloom:
            return
        
        # Get task router from state metadata
        task_router = state.metadata.get("task_router")
        if not task_router:
            return
        
        # Route task based on mode
        if decision.mode == RebloomMode.REPHRASE:
            task_router.reloop_task(
                task_id=state.metadata.get("task_id"),
                mode="rephrase",
                metadata={"drift_score": decision.drift_score}
            )
        elif decision.mode == RebloomMode.REGENERATE:
            task_router.reloop_task(
                task_id=state.metadata.get("task_id"),
                mode="regenerate",
                metadata={"faltering": decision.faltering}
            )
    
    def process(self, state: ReflexState) -> ReflexState:
        """Process state and actuate changes"""
        self._handle_sigil(state)
        self._route_task(state)
        
        # Update state with actuation info
        state.metadata["actuated"] = True
        return state
    
    def validate(self, state: ReflexState) -> bool:
        """Validate actuation results"""
        return state.metadata.get("actuated", False) 