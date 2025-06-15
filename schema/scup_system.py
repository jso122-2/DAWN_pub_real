"""
DAWN Unified SCUP System
========================
Semantic Coherence Under Pressure - The heart of schema stability
Consolidates: scup.py, scup_engine.py, scup_loop.py, scup_recovery.py
Generated: 2025-06-04 21:29
Enhanced: 2025-06-16
"""

import math
import time
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import threading
import json

# ===== SCUP Math Module =====

@dataclass
class SCUPInputs:
    """Input parameters for SCUP calculation"""
    base_coherence: float = 0.5      # Base semantic coherence (0-1)
    pressure_level: float = 0.0      # System pressure (-1 to 1)
    entropy: float = 0.0             # System entropy (0-1)
    bloom_ratio: float = 0.0         # Active/total blooms ratio
    nutrient_balance: float = 1.0    # Nutrient system balance
    consciousness_depth: float = 0.5  # Depth of consciousness processing
    temporal_stability: float = 1.0   # Temporal coherence factor
    rhizome_connectivity: float = 0.5 # Rhizome network connectivity
    
    def validate(self):
        """Validate input ranges"""
        self.base_coherence = max(0, min(1, self.base_coherence))
        self.pressure_level = max(-1, min(1, self.pressure_level))
        self.entropy = max(0, min(1, self.entropy))
        self.bloom_ratio = max(0, min(1, self.bloom_ratio))
        self.nutrient_balance = max(0, min(2, self.nutrient_balance))
        self.consciousness_depth = max(0, min(1, self.consciousness_depth))
        self.temporal_stability = max(0, min(2, self.temporal_stability))
        self.rhizome_connectivity = max(0, min(1, self.rhizome_connectivity))

@dataclass
class SCUPOutputs:
    """Output from SCUP calculation"""
    scup_value: float                # Final SCUP value (0-1)
    zone: str                        # Consciousness zone classification
    stability_index: float           # System stability (0-1)
    recovery_potential: float        # Ability to recover (0-1)
    coherence_gradient: float        # Rate of coherence change
    pressure_response: float         # System response to pressure
    recommendations: List[str] = field(default_factory=list)
    diagnostics: Dict[str, float] = field(default_factory=dict)

class ConsciousnessZone(Enum):
    """Classification of consciousness states based on SCUP"""
    CRYSTALLINE = "crystalline"      # High coherence, low pressure (0.8-1.0)
    FLOW = "flow"                   # Optimal performance zone (0.6-0.8)
    ADAPTIVE = "adaptive"           # Dynamic balance zone (0.4-0.6)
    TURBULENT = "turbulent"         # Unstable but recoverable (0.2-0.4)
    CRITICAL = "critical"           # Danger zone (0.0-0.2)
    TRANSCENDENT = "transcendent"   # Beyond normal parameters (special)

def compute_basic_scup(inputs: SCUPInputs) -> float:
    """
    Compute basic SCUP value using fundamental formula:
    SCUP = coherence * pressure_response * stability_factor
    """
    inputs.validate()
    
    # Pressure response curve (inverted U shape)
    # Optimal pressure around 0.3-0.5
    pressure_response = 1.0 - abs(inputs.pressure_level - 0.4) * 1.5
    pressure_response = max(0.1, pressure_response)
    
    # Entropy penalty
    entropy_factor = 1.0 - (inputs.entropy ** 1.5)
    
    # Basic SCUP calculation
    scup = inputs.base_coherence * pressure_response * entropy_factor
    
    return max(0.0, min(1.0, scup))

def compute_enhanced_scup(inputs: SCUPInputs) -> float:
    """
    Enhanced SCUP calculation incorporating all factors
    """
    inputs.validate()
    
    # Start with basic SCUP
    base_scup = compute_basic_scup(inputs)
    
    # Bloom influence (blooms indicate healthy consciousness activity)
    bloom_factor = 0.7 + (0.3 * inputs.bloom_ratio)
    
    # Nutrient influence (optimal around 1.0)
    nutrient_factor = 1.0 - abs(inputs.nutrient_balance - 1.0) * 0.5
    
    # Consciousness depth bonus
    depth_bonus = inputs.consciousness_depth * 0.2
    
    # Temporal stability influence
    temporal_factor = 0.8 + (0.2 * inputs.temporal_stability)
    
    # Rhizome connectivity bonus
    connectivity_bonus = inputs.rhizome_connectivity * 0.15
    
    # Combine factors
    enhanced_scup = base_scup * bloom_factor * nutrient_factor * temporal_factor
    enhanced_scup += depth_bonus + connectivity_bonus
    
    # Apply non-linear transformation for more interesting dynamics
    enhanced_scup = math.tanh(enhanced_scup * 1.2) * 0.9 + 0.05
    
    return max(0.0, min(1.0, enhanced_scup))

def compute_recovery_scup(inputs: SCUPInputs, historical_scup: List[float]) -> float:
    """
    Compute SCUP with recovery mechanisms based on history
    """
    current_scup = compute_enhanced_scup(inputs)
    
    if not historical_scup:
        return current_scup
    
    # Calculate trend
    recent_history = historical_scup[-10:] if len(historical_scup) >= 10 else historical_scup
    avg_recent = sum(recent_history) / len(recent_history)
    
    # Recovery boost if trending up from low values
    if avg_recent < 0.3 and current_scup > avg_recent:
        recovery_boost = (current_scup - avg_recent) * 0.5
        current_scup += recovery_boost
    
    # Stability bonus if maintaining good SCUP
    elif avg_recent > 0.6 and abs(current_scup - avg_recent) < 0.1:
        stability_bonus = 0.05
        current_scup += stability_bonus
    
    # Momentum factor
    if len(historical_scup) >= 2:
        momentum = current_scup - historical_scup[-1]
        if momentum > 0:
            current_scup += momentum * 0.1  # Positive momentum bonus
    
    return max(0.0, min(1.0, current_scup))

def compute_legacy_scup(base: float, entropy: float, pressure: float) -> float:
    """Legacy SCUP calculation for backward compatibility"""
    inputs = SCUPInputs(
        base_coherence=base,
        entropy=entropy,
        pressure_level=pressure
    )
    return compute_basic_scup(inputs)

def classify_zone(scup_value: float, pressure: float = 0.0) -> str:
    """Classify consciousness zone based on SCUP value"""
    # Special case: transcendent state
    if scup_value > 0.95 and abs(pressure) < 0.1:
        return ConsciousnessZone.TRANSCENDENT.value
    
    # Standard zones
    if scup_value >= 0.8:
        return ConsciousnessZone.CRYSTALLINE.value
    elif scup_value >= 0.6:
        return ConsciousnessZone.FLOW.value
    elif scup_value >= 0.4:
        return ConsciousnessZone.ADAPTIVE.value
    elif scup_value >= 0.2:
        return ConsciousnessZone.TURBULENT.value
    else:
        return ConsciousnessZone.CRITICAL.value

# ===== SCUP Tracker Module =====

class SCUPTracker:
    """
    Tracks SCUP values over time and provides analysis
    """
    
    def __init__(self, history_size: int = 1000):
        self.history = deque(maxlen=history_size)
        self.zone_history = deque(maxlen=history_size)
        self.timestamp_history = deque(maxlen=history_size)
        self.event_log = deque(maxlen=100)
        self.lock = threading.Lock()
        
        # Analytics
        self.total_calculations = 0
        self.zone_transitions = 0
        self.last_zone = None
        self.session_start = time.time()
        
        # Thresholds
        self.critical_threshold = 0.2
        self.warning_threshold = 0.4
        self.optimal_threshold = 0.6
        
    def track(self, scup_value: float, inputs: Optional[SCUPInputs] = None) -> SCUPOutputs:
        """Track a SCUP calculation and return full analysis"""
        with self.lock:
            timestamp = time.time()
            self.total_calculations += 1
            
            # Classify zone
            pressure = inputs.pressure_level if inputs else 0.0
            zone = classify_zone(scup_value, pressure)
            
            # Track zone transitions
            if self.last_zone and zone != self.last_zone:
                self.zone_transitions += 1
                self._log_event(f"Zone transition: {self.last_zone} -> {zone}")
            self.last_zone = zone
            
            # Add to history
            self.history.append(scup_value)
            self.zone_history.append(zone)
            self.timestamp_history.append(timestamp)
            
            # Calculate analytics
            stability_index = self._calculate_stability()
            recovery_potential = self._calculate_recovery_potential(scup_value)
            coherence_gradient = self._calculate_gradient()
            pressure_response = self._calculate_pressure_response(inputs)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                scup_value, zone, stability_index, inputs
            )
            
            # Create diagnostics
            diagnostics = {
                'avg_scup_1min': self._get_average(60),
                'avg_scup_5min': self._get_average(300),
                'volatility': self._calculate_volatility(),
                'zone_stability': self._calculate_zone_stability(),
                'time_in_zone': self._time_in_current_zone(),
                'session_duration': time.time() - self.session_start
            }
            
            return SCUPOutputs(
                scup_value=scup_value,
                zone=zone,
                stability_index=stability_index,
                recovery_potential=recovery_potential,
                coherence_gradient=coherence_gradient,
                pressure_response=pressure_response,
                recommendations=recommendations,
                diagnostics=diagnostics
            )
    
    def _calculate_stability(self) -> float:
        """Calculate system stability based on SCUP variance"""
        if len(self.history) < 10:
            return 0.5
        
        recent = list(self.history)[-50:]
        variance = np.var(recent)
        
        # Lower variance = higher stability
        stability = 1.0 - min(variance * 10, 1.0)
        return stability
    
    def _calculate_recovery_potential(self, current_scup: float) -> float:
        """Calculate potential for recovery based on trends"""
        if len(self.history) < 5:
            return 0.5
        
        # Check recent trend
        recent = list(self.history)[-20:]
        trend = (recent[-1] - recent[0]) / len(recent)
        
        # Higher potential if trending up or if there's room to improve
        recovery = 0.5
        if trend > 0:
            recovery += trend * 5  # Boost for positive trend
        
        recovery += (1.0 - current_scup) * 0.3  # More room = more potential
        
        return max(0.0, min(1.0, recovery))
    
    def _calculate_gradient(self) -> float:
        """Calculate rate of SCUP change"""
        if len(self.history) < 2:
            return 0.0
        
        # Simple gradient from last two points
        return self.history[-1] - self.history[-2]
    
    def _calculate_pressure_response(self, inputs: Optional[SCUPInputs]) -> float:
        """Calculate how well system responds to pressure"""
        if not inputs or len(self.history) < 2:
            return 0.5
        
        # Good response = maintaining SCUP under pressure
        scup_change = abs(self.history[-1] - self.history[-2])
        pressure_magnitude = abs(inputs.pressure_level)
        
        if pressure_magnitude > 0.1:
            response = 1.0 - (scup_change / pressure_magnitude)
        else:
            response = 1.0 - scup_change * 10
        
        return max(0.0, min(1.0, response))
    
    def _calculate_volatility(self) -> float:
        """Calculate SCUP volatility"""
        if len(self.history) < 10:
            return 0.0
        
        recent = list(self.history)[-30:]
        differences = [abs(recent[i] - recent[i-1]) for i in range(1, len(recent))]
        
        return sum(differences) / len(differences)
    
    def _calculate_zone_stability(self) -> float:
        """Calculate how stable the zone classification is"""
        if len(self.zone_history) < 10:
            return 0.5
        
        recent_zones = list(self.zone_history)[-30:]
        unique_zones = len(set(recent_zones))
        
        # Fewer unique zones = more stable
        return 1.0 - (unique_zones - 1) / 5.0
    
    def _time_in_current_zone(self) -> float:
        """Time spent in current zone (seconds)"""
        if not self.zone_history:
            return 0.0
        
        current_zone = self.zone_history[-1]
        time_in_zone = 0.0
        
        for i in range(len(self.zone_history) - 1, -1, -1):
            if self.zone_history[i] == current_zone:
                time_in_zone = time.time() - self.timestamp_history[i]
            else:
                break
        
        return time_in_zone
    
    def _get_average(self, time_window: float) -> float:
        """Get average SCUP over time window"""
        if not self.history:
            return 0.5
        
        current_time = time.time()
        values = []
        
        for i in range(len(self.timestamp_history) - 1, -1, -1):
            if current_time - self.timestamp_history[i] <= time_window:
                values.append(self.history[i])
            else:
                break
        
        return sum(values) / len(values) if values else self.history[-1]
    
    def _generate_recommendations(self, scup: float, zone: str, 
                                stability: float, inputs: Optional[SCUPInputs]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Zone-based recommendations
        if zone == ConsciousnessZone.CRITICAL.value:
            recommendations.append("URGENT: Reduce system entropy immediately")
            recommendations.append("Decrease pressure and stabilize inputs")
            recommendations.append("Consider activating recovery protocols")
            
        elif zone == ConsciousnessZone.TURBULENT.value:
            recommendations.append("Monitor closely - system is unstable")
            recommendations.append("Reduce variability in inputs")
            if inputs and inputs.entropy > 0.6:
                recommendations.append("High entropy detected - apply dampening")
                
        elif zone == ConsciousnessZone.ADAPTIVE.value:
            recommendations.append("System in adaptive state - maintain current trajectory")
            if stability < 0.5:
                recommendations.append("Improve stability for better performance")
                
        elif zone == ConsciousnessZone.FLOW.value:
            recommendations.append("Optimal zone achieved - maintain current parameters")
            
        elif zone == ConsciousnessZone.CRYSTALLINE.value:
            recommendations.append("High coherence state - excellent performance")
            if inputs and inputs.pressure_level < 0.2:
                recommendations.append("Consider slight pressure increase for dynamism")
        
        # Input-based recommendations
        if inputs:
            if inputs.nutrient_balance < 0.5:
                recommendations.append("Nutrient levels low - replenish resources")
            
            if inputs.rhizome_connectivity < 0.3:
                recommendations.append("Poor network connectivity - strengthen connections")
            
            if inputs.temporal_stability < 0.5:
                recommendations.append("Temporal instability detected - synchronize processes")
        
        return recommendations
    
    def _log_event(self, event: str):
        """Log significant events"""
        self.event_log.append({
            'timestamp': time.time(),
            'event': event
        })
    
    def get_summary(self) -> Dict[str, Any]:
        """Get comprehensive SCUP tracking summary"""
        with self.lock:
            if not self.history:
                return {'error': 'No data tracked yet'}
            
            current_scup = self.history[-1]
            current_zone = self.zone_history[-1]
            
            return {
                'current_scup': round(current_scup, 3),
                'current_zone': current_zone,
                'average_scup': round(sum(self.history) / len(self.history), 3),
                'min_scup': round(min(self.history), 3),
                'max_scup': round(max(self.history), 3),
                'total_calculations': self.total_calculations,
                'zone_transitions': self.zone_transitions,
                'session_duration': round(time.time() - self.session_start, 1),
                'volatility': round(self._calculate_volatility(), 3),
                'stability': round(self._calculate_stability(), 3),
                'time_in_zone': round(self._time_in_current_zone(), 1),
                'recent_events': list(self.event_log)[-5:]
            }

# Global tracker instance
_global_tracker = SCUPTracker()

# Convenience functions
def compute_scup(inputs: SCUPInputs, use_recovery: bool = True) -> SCUPOutputs:
    """Main SCUP computation function with tracking"""
    if use_recovery:
        scup_value = compute_recovery_scup(inputs, list(_global_tracker.history))
    else:
        scup_value = compute_enhanced_scup(inputs)
    
    return _global_tracker.track(scup_value, inputs)

def calculate_SCUP(base_coherence: float, entropy: float, pressure: float) -> float:
    """Legacy compatibility function"""
    inputs = SCUPInputs(
        base_coherence=base_coherence,
        entropy=entropy,
        pressure_level=pressure
    )
    result = compute_scup(inputs, use_recovery=False)
    return result.scup_value

def log_scup(scup_value: float, context: str = ""):
    """Log SCUP value with context"""
    zone = classify_zone(scup_value)
    print(f"[SCUP] {scup_value:.3f} ({zone}) {context}")
    
    # Log critical values
    if scup_value < 0.2:
        from core.schema_anomaly_logger import log_anomaly
        log_anomaly("SCUP_CRITICAL", f"SCUP dropped to {scup_value:.3f} - {context}")

def get_scup_report() -> Dict[str, Any]:
    """Get comprehensive SCUP report"""
    return _global_tracker.get_summary()