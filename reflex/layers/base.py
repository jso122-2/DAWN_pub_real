from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional
from enum import Enum

class RebloomMode(Enum):
    CLARIFY = "clarify"
    REPHRASE = "rephrase"
    REGENERATE = "regenerate"
    SUPPRESS = "suppress"

@dataclass
class ReflexState:
    """Base state container for reflex system layers"""
    mood: str
    drift_score: float
    heat: float
    entropy: float
    sigil: str
    audit_result: Any
    metadata: Dict[str, Any]

@dataclass
class RebloomDecision:
    """Standardized output from the reflex system"""
    should_rebloom: bool
    mode: RebloomMode
    flags: list[str]
    faltering: bool
    drift_score: float
    metadata: Dict[str, Any]

class ReflexLayer(ABC):
    """Base class for all reflex system layers"""
    
    @abstractmethod
    def process(self, state: ReflexState) -> ReflexState:
        """Process the current state and return updated state"""
        pass

    @abstractmethod
    def validate(self, state: ReflexState) -> bool:
        """Validate the current state"""
        pass

class InputLayer(ReflexLayer):
    """Layer 1: Symbolic State Reading"""
    pass

class EvaluationLayer(ReflexLayer):
    """Layer 2: Semantic Reflex Core"""
    pass

class DecisionLayer(ReflexLayer):
    """Layer 3: Standardized Semantic Output"""
    pass

class LoggingLayer(ReflexLayer):
    """Layer 4: Symbolic Audit Memory"""
    pass

class ActuationLayer(ReflexLayer):
    """Layer 5: Schema Flow Routing"""
    pass 