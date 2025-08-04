from typing import Dict, Any, List
from dataclasses import dataclass
from ...base import EvaluationLayer, ReflexState, RebloomMode

@dataclass
class SemanticSignal:
    """Represents a semantic signal that may trigger rebloom"""
    name: str
    value: float
    threshold: float
    weight: float
    triggered: bool

class RebloomEvaluator(EvaluationLayer):
    """Core evaluation logic for determining rebloom necessity"""
    
    def __init__(self):
        self.signals: Dict[str, SemanticSignal] = {
            "emotional_overload": SemanticSignal(
                name="emotional_overload",
                value=0.0,
                threshold=0.8,
                weight=1.2,
                triggered=False
            ),
            "conceptual_instability": SemanticSignal(
                name="conceptual_instability",
                value=0.0,
                threshold=0.6,
                weight=1.0,
                triggered=False
            ),
            "schema_breakdown": SemanticSignal(
                name="schema_breakdown",
                value=0.0,
                threshold=0.7,
                weight=1.5,
                triggered=False
            )
        }
    
    def _calculate_signals(self, state: ReflexState) -> None:
        """Calculate all semantic signals from state"""
        # Emotional overload = mood heat * drift
        self.signals["emotional_overload"].value = state.heat * state.drift_score
        
        # Conceptual instability = drift * entropy
        self.signals["conceptual_instability"].value = state.drift_score * state.entropy
        
        # Schema breakdown = (1 - alignment) * drift
        if hasattr(state.audit_result, "alignment_score"):
            alignment = state.audit_result.alignment_score
            self.signals["schema_breakdown"].value = (1 - alignment) * state.drift_score
    
    def _evaluate_signals(self) -> tuple[bool, RebloomMode, List[str]]:
        """Evaluate signals and determine rebloom mode"""
        should_rebloom = False
        flags = []
        mode = RebloomMode.CLARIFY
        
        # Check each signal
        for signal in self.signals.values():
            signal.triggered = signal.value > signal.threshold
            if signal.triggered:
                should_rebloom = True
                flags.append(f"{signal.name}={signal.value:.2f}")
                
                # Determine mode based on triggered signals
                if signal.name == "emotional_overload":
                    mode = RebloomMode.REPHRASE
                elif signal.name == "schema_breakdown":
                    mode = RebloomMode.REGENERATE
        
        return should_rebloom, mode, flags
    
    def process(self, state: ReflexState) -> ReflexState:
        """Process state through evaluation logic"""
        self._calculate_signals(state)
        should_rebloom, mode, flags = self._evaluate_signals()
        
        # Update state metadata with evaluation results
        state.metadata.update({
            "should_rebloom": should_rebloom,
            "mode": mode,
            "flags": flags,
            "signals": {name: signal.value for name, signal in self.signals.items()}
        })
        
        return state
    
    def validate(self, state: ReflexState) -> bool:
        """Validate evaluation results"""
        required_keys = ["should_rebloom", "mode", "flags", "signals"]
        return all(key in state.metadata for key in required_keys) 