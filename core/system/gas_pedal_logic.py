"""
A mind that never changes speed cannot respond. And a mind that never slows down never remembers.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple


class GasPedalLogic:
    """Dynamic tick rate controller for DAWN's recursive thinking systems."""
    
    def __init__(self):
        self.min_tick_rate = 0.5
        self.max_tick_rate = 10.0
        self.log_path = Path("logs/recursive/tick_modulation_log.json")
        self._ensure_log_directory()
        
        # Modulation thresholds
        self.thresholds = {
            "high_entropy": 0.7,
            "low_entropy": 0.4,
            "positive_mood": 0.5,
            "coherence_critical": 0.4,
            "coherence_stable": 0.8,
            "drift_critical": 0.8,
            "drift_moderate": 0.5
        }
    
    def _ensure_log_directory(self):
        """Create log directory if it doesn't exist."""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self.log_path.write_text("[]")
    
    def adjust_tick_rate(self, state_dict: Dict) -> Dict:
        """
        Adjust the recursive tick rate based on system state.
        
        Args:
            state_dict: Dictionary containing:
                - current_tick_rate: float (ticks per second)
                - coherence_score: float
                - mood_valence: float
                - entropy: float
                - pressure_zone: str ("calm", "active", "surge")
                - drift_magnitude: float (semantic instability metric)
        
        Returns:
            Dictionary with new_tick_rate, modulation_reason, and clamped flag
        """
        current_rate = state_dict['current_tick_rate']
        coherence = state_dict['coherence_score']
        mood = state_dict['mood_valence']
        entropy = state_dict['entropy']
        pressure = state_dict['pressure_zone']
        drift_magnitude = state_dict.get('drift_magnitude', 0.0)
        
        # Calculate base adjustment factor using the enhanced formula
        # Drift represents semantic instability/emotional pull - distinct from entropy
        adjustment_factor = (1 - coherence) + (entropy * 0.5) + (drift_magnitude * 0.75)
        
        # Determine modulation direction and reason
        modulation_reason, direction_multiplier = self._determine_modulation(
            coherence, mood, entropy, pressure, drift_magnitude
        )
        
        # Apply directional adjustment
        if direction_multiplier < 0:
            # For slowdown, reduce the adjustment factor
            adjustment_factor *= -0.5
        
        # Calculate new tick rate
        new_tick_rate = current_rate * (1 + adjustment_factor)
        
        # Clamp to valid range
        original_rate = new_tick_rate
        new_tick_rate = max(self.min_tick_rate, min(self.max_tick_rate, new_tick_rate))
        clamped = (new_tick_rate != original_rate)
        
        # Create output
        output = {
            "new_tick_rate": round(new_tick_rate, 3),
            "modulation_reason": modulation_reason,
            "clamped": clamped,
            "adjustment_factor": round(adjustment_factor, 3),
            "previous_rate": current_rate
        }
        
        # Log the adjustment
        self._log_adjustment(state_dict, output)
        
        return output
    
    def _determine_modulation(self, coherence: float, mood: float, 
                            entropy: float, pressure: str, drift_magnitude: float) -> Tuple[str, float]:
        """
        Determine the reason for modulation and direction.
        
        Returns:
            Tuple of (reason_string, direction_multiplier)
            direction_multiplier: 1.0 for increase, -1.0 for decrease
        """
        # Priority 1: Surge conditions always increase
        if pressure == "surge":
            return "SURGE_MODE: Maximum response required", 1.0
        
        # Priority 2: High drift magnitude (semantic fragmentation)
        if drift_magnitude > self.thresholds["drift_critical"]:
            return "SEMANTIC_FRAGMENTATION: High drift detected, stabilization critical", 1.0
        
        # Priority 3: High entropy conditions
        if entropy > self.thresholds["high_entropy"]:
            if coherence < self.thresholds["coherence_critical"]:
                return "CRITICAL: High entropy + low coherence detected", 1.0
            else:
                return "HIGH_ENTROPY: Increased processing needed", 1.0
        
        # Priority 4: Coherence drop with drift
        if coherence < self.thresholds["coherence_critical"]:
            if drift_magnitude > self.thresholds["drift_moderate"]:
                return "COHERENCE_DRIFT: Meaning fragmentation in progress", 1.0
            return "COHERENCE_DROP: Stabilization required", 1.0
        
        # Priority 4: Calm conditions - check for slowdown
        if pressure == "calm":
            if mood > self.thresholds["positive_mood"] and entropy < self.thresholds["low_entropy"]:
                return "CALM_POSITIVE: Reducing to conservation mode", -1.0
            else:
                return "CALM_ZONE: Maintaining steady state", -1.0
        
        # Priority 5: Stable positive state
        if (mood > self.thresholds["positive_mood"] and 
            entropy < self.thresholds["low_entropy"] and
            coherence > self.thresholds["coherence_stable"]):
            return "STABLE_POSITIVE: System in optimal state, reducing rate", -1.0
        
        # Default: Active monitoring
        return "ACTIVE_MONITORING: Standard adjustment", 1.0
    
    def _log_adjustment(self, state: Dict, result: Dict):
        """Log the tick rate adjustment event."""
        # Read existing log
        try:
            with open(self.log_path, 'r') as f:
                log_data = json.load(f)
        except:
            log_data = []
        
        # Create log entry
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "input_state": {
                "current_tick_rate": state['current_tick_rate'],
                "coherence_score": round(state['coherence_score'], 3),
                "mood_valence": round(state['mood_valence'], 3),
                "entropy": round(state['entropy'], 3),
                "pressure_zone": state['pressure_zone'],
                "drift_magnitude": round(state.get('drift_magnitude', 0.0), 3)
            },
            "output": result,
            "rate_change": round(result['new_tick_rate'] - state['current_tick_rate'], 3)
        }
        
        # Append and save
        log_data.append(entry)
        
        # Keep only last 1000 entries to prevent unbounded growth
        if len(log_data) > 1000:
            log_data = log_data[-1000:]
        
        with open(self.log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
    
    def get_tick_statistics(self) -> Dict:
        """Analyze historical tick rate adjustments."""
        try:
            with open(self.log_path, 'r') as f:
                log_data = json.load(f)
        except:
            return {"error": "No log data available"}
        
        if not log_data:
            return {"error": "Empty log"}
        
        # Calculate statistics
        rates = [entry['output']['new_tick_rate'] for entry in log_data]
        changes = [entry['rate_change'] for entry in log_data]
        reasons = {}
        
        for entry in log_data:
            reason = entry['output']['modulation_reason'].split(':')[0]
            reasons[reason] = reasons.get(reason, 0) + 1
        
        return {
            "total_adjustments": len(log_data),
            "average_tick_rate": round(sum(rates) / len(rates), 3),
            "min_rate_seen": min(rates),
            "max_rate_seen": max(rates),
            "average_change": round(sum(changes) / len(changes), 3),
            "clamped_count": sum(1 for e in log_data if e['output']['clamped']),
            "reason_distribution": reasons
        }


# Example usage
if __name__ == "__main__":
    gas_pedal = GasPedalLogic()
    
    # Test scenarios
    test_states = [
        {
            "current_tick_rate": 2.0,
            "coherence_score": 0.3,
            "mood_valence": -0.2,
            "entropy": 0.85,
            "pressure_zone": "active",
            "drift_magnitude": 0.6
        },
        {
            "current_tick_rate": 5.0,
            "coherence_score": 0.9,
            "mood_valence": 0.7,
            "entropy": 0.3,
            "pressure_zone": "calm",
            "drift_magnitude": 0.1
        },
        {
            "current_tick_rate": 3.0,
            "coherence_score": 0.5,
            "mood_valence": 0.0,
            "entropy": 0.6,
            "pressure_zone": "surge",
            "drift_magnitude": 0.9
        }
    ]
    
    for i, state in enumerate(test_states):
        print(f"\nTest {i+1}:")
        print(f"Input: {state}")
        result = gas_pedal.adjust_tick_rate(state)
        print(f"Output: {result}")
    
    # Show statistics
    print("\nTick Rate Statistics:")
    stats = gas_pedal.get_tick_statistics()
    print(json.dumps(stats, indent=2))