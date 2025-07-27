import random
import time
from typing import Dict, List, Any

class NeuralMetricsService:
    def __init__(self):
        self.last_update = time.time()
        self.entropy_history: List[float] = []
        self.max_history_size = 100

    def generate_metrics(self) -> Dict[str, Any]:
        """Generate neural metrics data"""
        current_time = time.time()
        delta_time = current_time - self.last_update
        self.last_update = current_time

        # Generate base metrics
        metrics = {
            "neural_activity": self._generate_neural_activity(),
            "quantum_coherence": self._generate_quantum_coherence(),
            "chaos_factor": self._generate_chaos_factor(),
            "memory_utilization": self._generate_memory_utilization(),
            "pattern_recognition": self._generate_pattern_recognition(),
            "tick_number": int(current_time * 10)  # Simulate tick number
        }

        # Update entropy distribution
        entropy = self._calculate_entropy(metrics)
        self.entropy_history.append(entropy)
        if len(self.entropy_history) > self.max_history_size:
            self.entropy_history.pop(0)
        
        metrics["entropy_distribution"] = self.entropy_history.copy()

        return metrics

    def _generate_neural_activity(self) -> float:
        """Generate neural activity metric (0-1)"""
        return min(1.0, max(0.0, random.normalvariate(0.7, 0.1)))

    def _generate_quantum_coherence(self) -> float:
        """Generate quantum coherence metric (0-1)"""
        return min(1.0, max(0.0, random.normalvariate(0.6, 0.15)))

    def _generate_chaos_factor(self) -> float:
        """Generate chaos factor metric (0-1)"""
        return min(1.0, max(0.0, random.normalvariate(0.4, 0.2)))

    def _generate_memory_utilization(self) -> float:
        """Generate memory utilization metric (0-1)"""
        return min(1.0, max(0.0, random.normalvariate(0.8, 0.1)))

    def _generate_pattern_recognition(self) -> float:
        """Generate pattern recognition metric (0-1)"""
        return min(1.0, max(0.0, random.normalvariate(0.75, 0.12)))

    def _calculate_entropy(self, metrics: Dict[str, Any]) -> float:
        """Calculate entropy based on metrics"""
        # Simple entropy calculation based on metric variance
        values = [
            metrics["neural_activity"],
            metrics["quantum_coherence"],
            metrics["chaos_factor"],
            metrics["memory_utilization"],
            metrics["pattern_recognition"]
        ]
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return min(1.0, max(0.0, variance * 2))  # Scale variance to 0-1 range 