from typing import Dict, Any, Optional
from datetime import datetime
import numpy as np

class EntropyFluctuation:
    def __init__(self):
        self.entropy_state = {
            "current": 0.0,
            "target": 0.5,
            "fluctuation": 0.0,
            "stability": 0.0
        }
        self.last_update = datetime.now()
        self._active = True
    
    def is_active(self) -> bool:
        return self._active
    
    def get_metrics(self) -> Dict[str, Any]:
        return {
            "entropy_state": self.entropy_state,
            "last_update": self.last_update.isoformat(),
            "active": self._active
        }
    
    def configure(self, config: Dict[str, Any]) -> None:
        if "active" in config:
            self._active = config["active"]
        if "entropy_state" in config:
            self.entropy_state.update(config["entropy_state"])
        self.last_update = datetime.now()
    
    def update(self, new_state: Dict[str, Any]) -> None:
        self.entropy_state.update(new_state)
        self.last_update = datetime.now()
    
    def get_current_entropy(self) -> float:
        return self.entropy_state["current"]
    
    def get_target_entropy(self) -> float:
        return self.entropy_state["target"]
    
    def get_fluctuation(self) -> float:
        return self.entropy_state["fluctuation"]
    
    def get_stability(self) -> float:
        return self.entropy_state["stability"]

# Singleton instance
_entropy_fluctuation = None

def get_entropy_fluctuation() -> EntropyFluctuation:
    global _entropy_fluctuation
    if _entropy_fluctuation is None:
        _entropy_fluctuation = EntropyFluctuation()
    return _entropy_fluctuation 