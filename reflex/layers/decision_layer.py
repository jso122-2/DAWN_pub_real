from typing import Dict, Any, List
from ...base import DecisionLayer, ReflexState, RebloomDecision, RebloomMode

class RebloomDecisionMaker(DecisionLayer):
    """Standardizes semantic output for the memory system"""
    
    def _detect_faltering(self, state: ReflexState) -> bool:
        """Detect if the system is showing signs of persistent decline"""
        # Check for multiple high-drift signals
        high_drift_signals = sum(
            1 for signal in state.metadata.get("signals", {}).values()
            if signal > 0.7
        )
        return high_drift_signals >= 2
    
    def _format_flags(self, state: ReflexState) -> List[str]:
        """Format decision flags for clarity"""
        flags = state.metadata.get("flags", [])
        
        # Add drift score flag
        flags.append(f"drift={state.drift_score:.2f}")
        
        # Add entropy flag if high
        if state.entropy > 0.7:
            flags.append(f"entropy={state.entropy:.2f} exceeds threshold")
        
        # Add mood flag if drifting
        if state.mood == "drift":
            flags.append("mood=drift")
        
        return flags
    
    def process(self, state: ReflexState) -> ReflexState:
        """Process state into standardized decision"""
        should_rebloom = state.metadata.get("should_rebloom", False)
        mode = state.metadata.get("mode", RebloomMode.CLARIFY)
        flags = self._format_flags(state)
        faltering = self._detect_faltering(state)
        
        decision = RebloomDecision(
            should_rebloom=should_rebloom,
            mode=mode,
            flags=flags,
            faltering=faltering,
            drift_score=state.drift_score,
            metadata=state.metadata
        )
        
        # Update state with decision
        state.metadata["decision"] = decision
        return state
    
    def validate(self, state: ReflexState) -> bool:
        """Validate decision output"""
        if "decision" not in state.metadata:
            return False
        
        decision = state.metadata["decision"]
        return isinstance(decision, RebloomDecision) and all([
            isinstance(decision.should_rebloom, bool),
            isinstance(decision.mode, RebloomMode),
            isinstance(decision.flags, list),
            isinstance(decision.faltering, bool),
            isinstance(decision.drift_score, float)
        ]) 