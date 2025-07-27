from typing import Dict, Any, List, Optional
import numpy as np
from datetime import datetime

class ConsciousnessModule:
    def __init__(self):
        self.consciousness_state = {
            "scup": 0.0,
            "entropy": 0.0,
            "coherence": 0.0,
            "temperature": 0.0,
            "mood": 0.0,
            "bloom_state": np.zeros((10, 10)),
            "neural_activity": np.zeros((10, 10)),
            "alignment_matrix": np.zeros((10, 10))
        }
        self.history = {
            "scup": [],
            "entropy": [],
            "coherence": [],
            "temperature": [],
            "mood": []
        }
        self.max_history_length = 1000
    
    def update_state(self, new_state: Dict[str, Any]) -> None:
        """Update consciousness state with new values"""
        self.consciousness_state.update(new_state)
        
        # Update history
        for key in self.history:
            if key in new_state:
                self.history[key].append(new_state[key])
                if len(self.history[key]) > self.max_history_length:
                    self.history[key].pop(0)
    
    def get_state(self) -> Dict[str, Any]:
        """Get current consciousness state"""
        return self.consciousness_state
    
    def get_history(self, metric: str, length: int = 100) -> List[float]:
        """Get historical data for a specific metric"""
        if metric not in self.history:
            return []
        return self.history[metric][-length:]
    
    def get_scup(self) -> float:
        """Get current SCUP value"""
        return self.consciousness_state["scup"]
    
    def get_entropy(self) -> float:
        """Get current entropy value"""
        return self.consciousness_state["entropy"]
    
    def get_coherence(self) -> float:
        """Get current coherence value"""
        return self.consciousness_state["coherence"]
    
    def get_temperature(self) -> float:
        """Get current temperature value"""
        return self.consciousness_state["temperature"]
    
    def get_mood(self) -> float:
        """Get current mood value"""
        return self.consciousness_state["mood"]
    
    def get_bloom_state(self) -> np.ndarray:
        """Get current bloom state matrix"""
        return self.consciousness_state["bloom_state"]
    
    def get_neural_activity(self) -> np.ndarray:
        """Get current neural activity matrix"""
        return self.consciousness_state["neural_activity"]
    
    def get_alignment_matrix(self) -> np.ndarray:
        """Get current alignment matrix"""
        return self.consciousness_state["alignment_matrix"]
    
    def get_metrics(self) -> Dict[str, float]:
        """Get all scalar metrics"""
        return {
            "scup": self.get_scup(),
            "entropy": self.get_entropy(),
            "coherence": self.get_coherence(),
            "temperature": self.get_temperature(),
            "mood": self.get_mood()
        }
    
    def get_matrices(self) -> Dict[str, np.ndarray]:
        """Get all matrix metrics"""
        return {
            "bloom_state": self.get_bloom_state(),
            "neural_activity": self.get_neural_activity(),
            "alignment_matrix": self.get_alignment_matrix()
        }
    
    def get_full_state(self) -> Dict[str, Any]:
        """Get complete state including all metrics and matrices"""
        return {
            **self.get_metrics(),
            **self.get_matrices(),
            "timestamp": datetime.now().isoformat()
        } 