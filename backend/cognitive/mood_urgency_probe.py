from typing import Dict, Any, Optional
from datetime import datetime
import numpy as np

class MoodUrgencyProbe:
    def __init__(self):
        self.mood_state = {
            "urgency": 0.0,
            "intensity": 0.0,
            "valence": 0.0,
            "activation": 0.0
        }
        self.last_update = datetime.now()
        self._active = True
    
    def is_active(self) -> bool:
        return self._active
    
    def get_metrics(self) -> Dict[str, Any]:
        return {
            "mood_state": self.mood_state,
            "last_update": self.last_update.isoformat(),
            "active": self._active
        }
    
    def configure(self, config: Dict[str, Any]) -> None:
        if "active" in config:
            self._active = config["active"]
        if "mood_state" in config:
            self.mood_state.update(config["mood_state"])
        self.last_update = datetime.now()
    
    def update(self, new_state: Dict[str, Any]) -> None:
        self.mood_state.update(new_state)
        self.last_update = datetime.now()
    
    def get_urgency(self) -> float:
        return self.mood_state["urgency"]
    
    def get_intensity(self) -> float:
        return self.mood_state["intensity"]
    
    def get_valence(self) -> float:
        return self.mood_state["valence"]
    
    def get_activation(self) -> float:
        return self.mood_state["activation"]

# Singleton instance
_mood_probe = None

def get_mood_probe() -> MoodUrgencyProbe:
    global _mood_probe
    if _mood_probe is None:
        _mood_probe = MoodUrgencyProbe()
    return _mood_probe 