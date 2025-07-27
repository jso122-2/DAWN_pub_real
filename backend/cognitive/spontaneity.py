from typing import Dict, Any, Optional, List
from datetime import datetime
import numpy as np

class SpontaneityModule:
    def __init__(self):
        self.spontaneity_state = {
            "level": 0.0,
            "threshold": 0.5,
            "bursts": [],
            "patterns": [],
            "energy": 0.0
        }
        self.last_update = datetime.now()
        self._active = True
    
    def is_active(self) -> bool:
        return self._active
    
    def get_metrics(self) -> Dict[str, Any]:
        return {
            "spontaneity_state": self.spontaneity_state,
            "last_update": self.last_update.isoformat(),
            "active": self._active
        }
    
    def configure(self, config: Dict[str, Any]) -> None:
        if "active" in config:
            self._active = config["active"]
        if "spontaneity_state" in config:
            self.spontaneity_state.update(config["spontaneity_state"])
        self.last_update = datetime.now()
    
    def update(self, new_state: Dict[str, Any]) -> None:
        self.spontaneity_state.update(new_state)
        self.last_update = datetime.now()
    
    def get_level(self) -> float:
        return self.spontaneity_state["level"]
    
    def get_threshold(self) -> float:
        return self.spontaneity_state["threshold"]
    
    def get_bursts(self) -> List[Dict[str, Any]]:
        return self.spontaneity_state["bursts"]
    
    def get_patterns(self) -> List[Dict[str, Any]]:
        return self.spontaneity_state["patterns"]
    
    def get_energy(self) -> float:
        return self.spontaneity_state["energy"]
    
    def add_burst(self, burst: Dict[str, Any]) -> None:
        self.spontaneity_state["bursts"].append({
            **burst,
            "timestamp": datetime.now().isoformat()
        })
        if len(self.spontaneity_state["bursts"]) > 100:  # Keep last 100 bursts
            self.spontaneity_state["bursts"].pop(0)
    
    def add_pattern(self, pattern: Dict[str, Any]) -> None:
        self.spontaneity_state["patterns"].append({
            **pattern,
            "timestamp": datetime.now().isoformat()
        })
        if len(self.spontaneity_state["patterns"]) > 100:  # Keep last 100 patterns
            self.spontaneity_state["patterns"].pop(0)
    
    def clear_bursts(self) -> None:
        self.spontaneity_state["bursts"] = []
    
    def clear_patterns(self) -> None:
        self.spontaneity_state["patterns"] = []
    
    def set_threshold(self, threshold: float) -> None:
        self.spontaneity_state["threshold"] = max(0.0, min(1.0, threshold))
    
    def set_energy(self, energy: float) -> None:
        self.spontaneity_state["energy"] = max(0.0, min(1.0, energy)) 