from typing import Dict, Any, Optional, List
from datetime import datetime
import numpy as np

class QualiaKernel:
    def __init__(self):
        self.qualia_state = {
            "intensity": 0.0,
            "coherence": 0.0,
            "novelty": 0.0,
            "valence": 0.0,
            "patterns": []
        }
        self.last_update = datetime.now()
        self._active = True
    
    def is_active(self) -> bool:
        return self._active
    
    def get_metrics(self) -> Dict[str, Any]:
        return {
            "qualia_state": self.qualia_state,
            "last_update": self.last_update.isoformat(),
            "active": self._active
        }
    
    def configure(self, config: Dict[str, Any]) -> None:
        if "active" in config:
            self._active = config["active"]
        if "qualia_state" in config:
            self.qualia_state.update(config["qualia_state"])
        self.last_update = datetime.now()
    
    def update(self, new_state: Dict[str, Any]) -> None:
        self.qualia_state.update(new_state)
        self.last_update = datetime.now()
    
    def get_intensity(self) -> float:
        return self.qualia_state["intensity"]
    
    def get_coherence(self) -> float:
        return self.qualia_state["coherence"]
    
    def get_novelty(self) -> float:
        return self.qualia_state["novelty"]
    
    def get_valence(self) -> float:
        return self.qualia_state["valence"]
    
    def get_patterns(self) -> List[Dict[str, Any]]:
        return self.qualia_state["patterns"]
    
    def add_pattern(self, pattern: Dict[str, Any]) -> None:
        self.qualia_state["patterns"].append(pattern)
        if len(self.qualia_state["patterns"]) > 100:  # Keep last 100 patterns
            self.qualia_state["patterns"].pop(0)

# Singleton instance
_qualia_kernel = None

def get_qualia_kernel() -> QualiaKernel:
    global _qualia_kernel
    if _qualia_kernel is None:
        _qualia_kernel = QualiaKernel()
    return _qualia_kernel 