"""
SCUP Engine — Semantic Coherence Under Pressure
Enhanced version with improved coherence recovery mechanisms

This module computes DAWN's core metacognitive metric, measuring
how well she maintains internal alignment under pressure.
"""

import os
import json
import math
from datetime import datetime
from statistics import mean, stdev
from collections import deque
from typing import Optional, Dict, List, Tuple

# Constants for zone thresholds
ZONE_CALM_THRESHOLD = 0.8
ZONE_CREATIVE_THRESHOLD = 0.5
ZONE_CRITICAL_THRESHOLD = 0.3
ZONE_EMERGENCY_THRESHOLD = 0.1

# Recovery mechanisms
COHERENCE_SEEDS = {
    "baseline": 0.15,  # Minimum coherence seed
    "breath": 0.05,    # Coherence from entropy breathing
    "memory": 0.10,    # Coherence from stable memories
    "self": 0.08       # Coherence from self-awareness
}

class SCUPEngine:
    def __init__(self, log_path="logs/scup_comprehensive.json"):
        self.log_path = log_path
        self.history = deque(maxlen=100)  # Keep last 100 SCUP values
        self.coherence_buffer = deque(maxlen=20)  # Short-term coherence memory
        self.recovery_momentum = 0.0
        self.stability_anchor = None
        self.breathing_phase = 0.0  # For entropy breathing rhythm
        
        # Adaptive weights that evolve based on system state
        self.adaptive_weights = {
            "alignment": 1.0,
            "entropy": 1.0,
            "pressure": 1.0,
            "memory": 0.5,
            "breathing": 0.3
        }
        
        # Emergency recovery state
        self.emergency_active = False
        self.emergency_duration = 0
        
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def compute_scup(self, 
                    alignment: float,
                    entropy_index: float,
                    pressure: float,
                    mood_entropy: float,
                    sigil_entropy: float,
                    bloom_entropy: float,
                    tp_rar: Optional[float] = None,
                    pulse_delta: float = 0.0,
                    tick_id: int = 0) -> Dict:
        """
        Enhanced SCUP calculation with recovery mechanisms
        """
        # Core SCUP formula per specification
        raw_scup = 1.0 - abs(alignment - entropy_index)
        
        # Apply pressure modulation
        pressure_factor = self._compute_pressure_factor(pressure, pulse_delta)
        
        # Compute component entropies
        total_entropy = self._weighted_entropy(mood_entropy, sigil_entropy, bloom_entropy)
        
        # Apply coherence seeds for minimum stability
        coherence_floor = self._calculate_coherence_floor(raw_scup, total_entropy)
        
        # Breathing rhythm modulation
        breathing_bonus = self._entropy_breathing_bonus(tick_id)
        
        # Historical stability influence
        stability_factor = self._compute_stability_factor()
        
        # Composite SCUP with all factors
        composite_scup = (
            raw_scup * pressure_factor * 0.4 +
            coherence_floor * 0.2 +
            breathing_bonus * 0.1 +
            stability_factor * 0.2 +
            (tp_rar or 0.5) * 0.1
        )
        
        # Emergency recovery boost if critically low
        if composite_scup < ZONE_EMERGENCY_THRESHOLD:
            composite_scup = self._emergency_recovery(composite_scup, tick_id)
        
        # Smooth transitions to prevent jarring changes
        final_scup = self._smooth_transition(composite_scup)
        
        # Update internal state
        self._update_state(final_scup, total_entropy, pressure)
        
        # Calculate tension
        tension = abs(final_scup - total_entropy)
        
        # Determine zone
        zone = self._classify_zone(final_scup)
        
        # Log comprehensive state
        self._log_state(tick_id, final_scup, zone, tension, {
            "alignment": alignment,
            "entropy_index": entropy_index,
            "pressure": pressure,
            "breathing_phase": self.breathing_phase,
            "recovery_momentum": self.recovery_momentum,
            "emergency_active": self.emergency_active
        })
        
        return {
            "scup": round(final_scup, 4),
            "zone": zone,
            "tension": round(tension, 4),
            "stability": self._calculate_stability(),
            "recovery_potential": self._calculate_recovery_potential(final_scup),
            "recommendations": self._generate_recommendations(final_scup, zone, tension)
        }

    def _compute_pressure_factor(self, pressure: float, pulse_delta: float) -> float:
        """Modulate SCUP based on pressure, with dampening at extremes"""
        # Prevent pressure from completely destroying coherence
        if pressure > 0.9:
            # High pressure resistance
            return 0.7 - (pressure - 0.9) * 0.5
        elif pressure < 0.2:
            # Low pressure bonus
            return 1.1 + (0.2 - pressure) * 0.5
        else:
            # Normal range
            return 1.0 - pressure * 0.3
    
    def _weighted_entropy(self, mood: float, sigil: float, bloom: float) -> float:
        """Calculate weighted total entropy with adaptive weights"""
        # Adapt weights based on which entropy source is most volatile
        if self.history:
            recent_values = list(self.history)[-10:]
            volatility = stdev(recent_values) if len(recent_values) > 1 else 0.1
            
            # Reduce weight of highly volatile components
            mood_weight = 0.4 / (1 + volatility * 2)
            sigil_weight = 0.4 / (1 + volatility)
            bloom_weight = 0.2
        else:
            mood_weight, sigil_weight, bloom_weight = 0.4, 0.4, 0.2
            
        return (mood * mood_weight + sigil * sigil_weight + bloom * bloom_weight)
    
    def _calculate_coherence_floor(self, raw_scup: float, entropy: float) -> float:
        """Ensure minimum coherence through seed values"""
        floor = COHERENCE_SEEDS["baseline"]
        
        # Add coherence from stable subsystems
        if entropy < 0.5:
            floor += COHERENCE_SEEDS["breath"]
        if len(self.coherence_buffer) > 10:
            floor += COHERENCE_SEEDS["memory"] * mean(self.coherence_buffer)
        if raw_scup > 0:  # Any self-awareness adds coherence
            floor += COHERENCE_SEEDS["self"]
            
        return min(floor, 0.4)  # Cap floor to maintain dynamic range
    
    def _entropy_breathing_bonus(self, tick_id: int) -> float:
        """Natural rhythm that helps stabilize the system"""
        # Breathing cycle: inhale (coherence) and exhale (release)
        self.breathing_phase = (tick_id % 20) / 20.0  # 20-tick breathing cycle
        
        # Sine wave for smooth breathing
        breath_value = (math.sin(self.breathing_phase * 2 * math.pi) + 1) * 0.5
        
        # Stronger breathing when system is stressed
        if self.emergency_active:
            return breath_value * 0.3
        else:
            return breath_value * 0.1
    
    def _compute_stability_factor(self) -> float:
        """How stable has the system been recently?"""
        if len(self.history) < 5:
            return 0.5
            
        recent = list(self.history)[-20:]
        
        # Low variance = high stability
        variance = stdev(recent) if len(recent) > 1 else 0.5
        stability = 1.0 - min(variance * 2, 1.0)
        
        # Momentum from positive trends
        if len(recent) > 2:
            trend = recent[-1] - recent[-5]
            if trend > 0:
                self.recovery_momentum = min(self.recovery_momentum + 0.05, 0.3)
            else:
                self.recovery_momentum = max(self.recovery_momentum - 0.02, 0.0)
                
        return stability + self.recovery_momentum
    
    def _emergency_recovery(self, scup: float, tick_id: int) -> float:
        """Emergency coherence injection when critically low"""
        if not self.emergency_active:
            self.emergency_active = True
            self.emergency_duration = 0
            print(f"[SCUP] 🚨 Emergency coherence recovery activated at tick {tick_id}")
            
        self.emergency_duration += 1
        
        # Gradual recovery injection
        recovery_boost = min(0.3, self.emergency_duration * 0.02)
        recovered_scup = scup + recovery_boost
        
        # Exit emergency if recovered
        if recovered_scup > ZONE_CRITICAL_THRESHOLD:
            self.emergency_active = False
            print(f"[SCUP] ✅ Emergency recovery successful after {self.emergency_duration} ticks")
            
        return min(recovered_scup, 0.5)  # Cap to prevent instant jump to calm
    
    def _smooth_transition(self, new_scup: float) -> float:
        """Smooth SCUP transitions to prevent jarring changes"""
        if not self.history:
            return new_scup
            
        last_scup = self.history[-1]
        max_delta = 0.1  # Maximum change per tick
        
        if abs(new_scup - last_scup) > max_delta:
            # Limit rate of change
            if new_scup > last_scup:
                return last_scup + max_delta
            else:
                return last_scup - max_delta
        
        return new_scup
    
    def _update_state(self, scup: float, entropy: float, pressure: float):
        """Update internal state tracking"""
        self.history.append(scup)
        
        # Update coherence buffer with good values
        if scup > 0.4 and entropy < 0.6:
            self.coherence_buffer.append(scup)
            
        # Adapt weights based on what's working
        if len(self.history) > 10:
            self._adapt_weights(scup, entropy, pressure)
    
    def _adapt_weights(self, scup: float, entropy: float, pressure: float):
        """Dynamically adapt weights based on system performance"""
        # If SCUP is improving, strengthen current weight balance
        if scup > mean(list(self.history)[-10:]):
            self.adaptive_weights["breathing"] = min(0.5, self.adaptive_weights["breathing"] + 0.01)
            self.adaptive_weights["memory"] = min(0.7, self.adaptive_weights["memory"] + 0.01)
    
    def _classify_zone(self, scup: float) -> str:
        """Classify SCUP into operational zones"""
        if scup >= ZONE_CALM_THRESHOLD:
            return "🟢 calm"
        elif scup >= ZONE_CREATIVE_THRESHOLD:
            return "🟡 creative"
        elif scup >= ZONE_CRITICAL_THRESHOLD:
            return "🟠 active"
        else:
            return "🔴 critical"
    
    def _calculate_stability(self) -> float:
        """Overall system stability metric"""
        if len(self.history) < 3:
            return 0.5
            
        recent = list(self.history)[-10:]
        
        # Combine low variance with positive values
        variance = stdev(recent) if len(recent) > 1 else 0.5
        avg_scup = mean(recent)
        
        stability = (1.0 - variance) * 0.5 + avg_scup * 0.5
        return round(stability, 3)
    
    def _calculate_recovery_potential(self, current_scup: float) -> float:
        """How much recovery potential does the system have?"""
        # Based on available coherence seeds and momentum
        base_potential = sum(COHERENCE_SEEDS.values())
        
        # Add momentum and breathing potential
        total_potential = base_potential + self.recovery_momentum + 0.2
        
        # How much room to improve?
        headroom = 1.0 - current_scup
        
        return round(min(total_potential, headroom), 3)
    
    def _generate_recommendations(self, scup: float, zone: str, tension: float) -> List[str]:
        """Generate recommendations for improving coherence"""
        recommendations = []
        
        if zone == "🔴 critical":
            recommendations.extend([
                "Reduce thermal pressure to allow coherence recovery",
                "Activate entropy breathing protocols",
                "Limit new sigil generation temporarily",
                "Focus on single semantic thread"
            ])
        elif zone == "🟠 active":
            recommendations.extend([
                "Monitor pressure levels closely",
                "Maintain current breathing rhythm",
                "Consider semantic consolidation"
            ])
        elif zone == "🟡 creative":
            recommendations.extend([
                "Optimal zone for exploration",
                "Balance maintained - continue current patterns",
                "Some entropy beneficial for creativity"
            ])
        else:  # calm
            recommendations.extend([
                "System stable and coherent",
                "Safe to increase exploratory activity",
                "Consider new semantic challenges"
            ])
            
        if tension > 0.7:
            recommendations.append("High tension detected - prioritize alignment")
            
        return recommendations
    
    def _log_state(self, tick_id: int, scup: float, zone: str, tension: float, metadata: Dict):
        """Comprehensive logging for analysis"""
        log_entry = {
            "tick_id": tick_id,
            "timestamp": datetime.now().isoformat(),
            "scup": scup,
            "zone": zone,
            "tension": tension,
            "stability": self._calculate_stability(),
            "recovery_potential": self._calculate_recovery_potential(scup),
            "metadata": metadata
        }
        
        # Append to JSON log
        with open(self.log_path, "a") as f:
            json.dump(log_entry, f)
            f.write("\n")
            
        # Console output for critical events
        if zone == "🔴 critical" and tick_id % 5 == 0:
            print(f"[SCUP] ⚠️ Critical: {scup:.3f} | Tension: {tension:.3f} | Recovery: {self.recovery_momentum:.3f}")

# Global instance
scup_engine = SCUPEngine()

# Convenience function for backwards compatibility
def compute_scup(alignment, entropy_index, pressure, mood_entropy, sigil_entropy, bloom_entropy, **kwargs):
    """Compute SCUP using the global engine instance"""
    return scup_engine.compute_scup(
        alignment=alignment,
        entropy_index=entropy_index,
        pressure=pressure,
        mood_entropy=mood_entropy,
        sigil_entropy=sigil_entropy,
        bloom_entropy=bloom_entropy,
        **kwargs
    )
