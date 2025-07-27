"""
DAWN Tension Engine
Calculates semantic tension from SCUP vs entropy deltas and provides adaptive responses.
"""

import sys, os
import math
import time
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass, field
from collections import deque
from datetime import datetime
from enum import Enum

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class TensionZone(Enum):
    """Tension zones based on SCUP-entropy dynamics."""
    HARMONIC = "harmonic"        # Low tension, balanced state
    CREATIVE = "creative"        # Moderate tension, productive
    TURBULENT = "turbulent"      # High tension, unstable
    CRITICAL = "critical"        # Extreme tension, requires intervention

@dataclass
class TensionReading:
    """A single tension measurement with context."""
    timestamp: datetime
    scup_score: float
    entropy_level: float
    tension_magnitude: float
    tension_direction: float  # Radians
    zone: TensionZone
    recommended_interval: float
    heat_scaling: float
    action_threshold: float
    
    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp.isoformat(),
            'scup_score': self.scup_score,
            'entropy_level': self.entropy_level,
            'tension_magnitude': self.tension_magnitude,
            'tension_direction': self.tension_direction,
            'zone': self.zone.value,
            'recommended_interval': self.recommended_interval,
            'heat_scaling': self.heat_scaling,
            'action_threshold': self.action_threshold
        }

class TensionEngine:
    """
    Calculates semantic tension from SCUP vs entropy dynamics.
    
    Tension emerges from the relationship between coherence (SCUP) and 
    information entropy. This drives adaptive responses in tick intervals,
    heat scaling, and action thresholds.
    """
    
    def __init__(self, memory_window: int = 100):
        self.memory_window = memory_window
        
        # Tension history and trends
        self.tension_history = deque(maxlen=memory_window)
        self.scup_history = deque(maxlen=memory_window)
        self.entropy_history = deque(maxlen=memory_window)
        
        # Zone classification thresholds
        self.zone_thresholds = {
            TensionZone.HARMONIC: (0.0, 0.3),      # Low tension
            TensionZone.CREATIVE: (0.3, 0.6),      # Moderate tension
            TensionZone.TURBULENT: (0.6, 0.8),     # High tension
            TensionZone.CRITICAL: (0.8, 1.0)       # Extreme tension
        }
        
        # Response parameters
        self.base_interval = 1.0
        self.interval_range = (0.1, 5.0)  # Min/max tick intervals
        self.heat_scale_range = (0.5, 2.0)  # Heat scaling multipliers
        self.action_thresholds = {
            TensionZone.HARMONIC: 0.2,
            TensionZone.CREATIVE: 0.4,
            TensionZone.TURBULENT: 0.6,
            TensionZone.CRITICAL: 0.8
        }
        
        # Adaptive parameters
        self.tension_sensitivity = 1.0
        self.momentum_decay = 0.9
        self.current_momentum = 0.0
        
        # State tracking
        self.current_zone = TensionZone.HARMONIC
        self.zone_transition_history = deque(maxlen=50)
        self.last_calculation = None
        
        print("[TensionEngine] ⚡ Semantic tension engine initialized")
    
    def calculate_tension(self, scup_score: float, entropy_level: float,
                         pulse_heat: float = None, context: Dict = None) -> TensionReading:
        """
        Calculate current semantic tension from SCUP and entropy.
        
        Args:
            scup_score: Current SCUP (Semantic Coherence Under Pressure)
            entropy_level: Current entropy level
            pulse_heat: Optional pulse heat for additional context
            context: Optional additional context
            
        Returns:
            TensionReading with comprehensive tension analysis
        """
        try:
            # Record inputs
            self.scup_history.append(scup_score)
            self.entropy_history.append(entropy_level)
            
            # Calculate base tension magnitude
            tension_magnitude = self._calculate_base_tension(scup_score, entropy_level)
            
            # Apply momentum and temporal factors
            tension_magnitude = self._apply_momentum(tension_magnitude)
            
            # Calculate tension direction (phase relationship)
            tension_direction = self._calculate_tension_direction(scup_score, entropy_level)
            
            # Classify tension zone
            zone = self._classify_tension_zone(tension_magnitude)
            
            # Calculate adaptive responses
            recommended_interval = self._calculate_recommended_interval(tension_magnitude, zone)
            heat_scaling = self._calculate_heat_scaling(tension_magnitude, zone)
            action_threshold = self.action_thresholds[zone]
            
            # Create tension reading
            reading = TensionReading(
                timestamp=datetime.utcnow(),
                scup_score=scup_score,
                entropy_level=entropy_level,
                tension_magnitude=tension_magnitude,
                tension_direction=tension_direction,
                zone=zone,
                recommended_interval=recommended_interval,
                heat_scaling=heat_scaling,
                action_threshold=action_threshold
            )
            
            # Update state
            self.tension_history.append(reading)
            self._update_zone_tracking(zone)
            self.last_calculation = datetime.utcnow()
            
            return reading
            
        except Exception as e:
            print(f"[TensionEngine] ❌ Tension calculation error: {e}")
            # Return safe default
            return self._create_default_reading(scup_score, entropy_level)
    
    def _calculate_base_tension(self, scup: float, entropy: float) -> float:
        """Calculate base tension magnitude from SCUP-entropy relationship."""
        # Tension emerges from imbalance between order (SCUP) and chaos (entropy)
        
        # Ideal state: moderate SCUP (0.6-0.8) with moderate entropy (0.4-0.6)
        ideal_scup = 0.7
        ideal_entropy = 0.5
        
        # Calculate deviations from ideal
        scup_deviation = abs(scup - ideal_scup) / ideal_scup
        entropy_deviation = abs(entropy - ideal_entropy) / ideal_entropy
        
        # Tension from individual deviations
        base_tension = (scup_deviation + entropy_deviation) / 2
        
        # Additional tension from imbalance (high entropy + low SCUP = high tension)
        imbalance_factor = 0.0
        if scup < 0.4 and entropy > 0.6:  # Chaotic state
            imbalance_factor = (0.6 - entropy) + (0.4 - scup)
        elif scup > 0.8 and entropy < 0.3:  # Over-rigid state
            imbalance_factor = (scup - 0.8) + (0.3 - entropy)
        
        # Combine factors
        total_tension = base_tension + abs(imbalance_factor) * 0.5
        
        # Apply sensitivity scaling
        scaled_tension = total_tension * self.tension_sensitivity
        
        return min(1.0, max(0.0, scaled_tension))
    
    def _apply_momentum(self, base_tension: float) -> float:
        """Apply momentum to tension calculation for temporal smoothing."""
        if not self.tension_history:
            self.current_momentum = 0.0
            return base_tension
        
        # Calculate momentum from recent tension changes
        recent_tensions = [r.tension_magnitude for r in list(self.tension_history)[-5:]]
        if len(recent_tensions) >= 2:
            recent_change = recent_tensions[-1] - recent_tensions[0]
            self.current_momentum = (self.current_momentum * self.momentum_decay + 
                                   recent_change * (1 - self.momentum_decay))
        
        # Apply momentum influence
        momentum_influence = self.current_momentum * 0.2  # 20% influence
        adjusted_tension = base_tension + momentum_influence
        
        return min(1.0, max(0.0, adjusted_tension))
    
    def _calculate_tension_direction(self, scup: float, entropy: float) -> float:
        """Calculate tension direction in radians (phase relationship)."""
        # Map SCUP and entropy to unit circle
        # High SCUP, low entropy -> 0 radians (positive x-axis)
        # Low SCUP, high entropy -> π radians (negative x-axis)
        
        x = (scup - 0.5) * 2      # Range [-1, 1]
        y = (entropy - 0.5) * 2   # Range [-1, 1]
        
        return math.atan2(y, x)
    
    def _classify_tension_zone(self, tension_magnitude: float) -> TensionZone:
        """Classify tension magnitude into zones."""
        for zone, (min_thresh, max_thresh) in self.zone_thresholds.items():
            if min_thresh <= tension_magnitude < max_thresh:
                return zone
        
        # Default to critical if above all thresholds
        return TensionZone.CRITICAL
    
    def _calculate_recommended_interval(self, tension: float, zone: TensionZone) -> float:
        """Calculate recommended tick interval based on tension."""
        # Higher tension = faster ticks (lower interval)
        # Lower tension = slower ticks (higher interval)
        
        min_interval, max_interval = self.interval_range
        
        # Base calculation: inverse relationship with tension
        if tension == 0:
            base_interval = max_interval
        else:
            # Exponential curve for more dramatic response at high tension
            tension_factor = math.pow(tension, 1.5)
            base_interval = max_interval - (max_interval - min_interval) * tension_factor
        
        # Zone-specific adjustments
        zone_multipliers = {
            TensionZone.HARMONIC: 1.2,      # Slower in harmonic state
            TensionZone.CREATIVE: 1.0,      # Normal in creative state
            TensionZone.TURBULENT: 0.7,     # Faster in turbulent state
            TensionZone.CRITICAL: 0.4       # Much faster in critical state
        }
        
        adjusted_interval = base_interval * zone_multipliers[zone]
        
        return max(min_interval, min(adjusted_interval, max_interval))
    
    def _calculate_heat_scaling(self, tension: float, zone: TensionZone) -> float:
        """Calculate heat scaling multiplier based on tension."""
        min_scale, max_scale = self.heat_scale_range
        
        # Linear scaling with tension
        base_scaling = min_scale + (max_scale - min_scale) * tension
        
        # Zone-specific adjustments
        zone_adjustments = {
            TensionZone.HARMONIC: 0.9,      # Slightly reduce heat in harmony
            TensionZone.CREATIVE: 1.1,      # Boost heat in creative tension
            TensionZone.TURBULENT: 1.3,     # Increase heat in turbulence
            TensionZone.CRITICAL: 1.5       # Maximum heat in critical state
        }
        
        adjusted_scaling = base_scaling * zone_adjustments[zone]
        
        return max(min_scale, min(adjusted_scaling, max_scale))
    
    def _update_zone_tracking(self, new_zone: TensionZone):
        """Update zone transition tracking."""
        if new_zone != self.current_zone:
            transition = {
                'timestamp': datetime.utcnow(),
                'from_zone': self.current_zone.value,
                'to_zone': new_zone.value,
                'tension_magnitude': self.tension_history[-1].tension_magnitude if self.tension_history else 0.0
            }
            
            self.zone_transition_history.append(transition)
            self.current_zone = new_zone
            
            print(f"[TensionEngine] 🔄 Zone transition: {transition['from_zone']} → {transition['to_zone']}")
    
    def _create_default_reading(self, scup: float, entropy: float) -> TensionReading:
        """Create safe default tension reading."""
        return TensionReading(
            timestamp=datetime.utcnow(),
            scup_score=scup,
            entropy_level=entropy,
            tension_magnitude=0.3,
            tension_direction=0.0,
            zone=TensionZone.CREATIVE,
            recommended_interval=1.0,
            heat_scaling=1.0,
            action_threshold=0.4
        )
    
    def get_current_tension_state(self) -> Dict:
        """Get comprehensive current tension state."""
        if not self.tension_history:
            return {'status': 'no_data'}
        
        latest = self.tension_history[-1]
        
        # Calculate trends
        trend_data = self._calculate_trends()
        
        return {
            'current_tension': latest.tension_magnitude,
            'current_zone': latest.zone.value,
            'scup_score': latest.scup_score,
            'entropy_level': latest.entropy_level,
            'recommended_interval': latest.recommended_interval,
            'heat_scaling': latest.heat_scaling,
            'action_threshold': latest.action_threshold,
            'momentum': self.current_momentum,
            'trends': trend_data,
            'zone_stability': self._calculate_zone_stability()
        }
    
    def _calculate_trends(self) -> Dict:
        """Calculate tension and component trends."""
        if len(self.tension_history) < 5:
            return {'status': 'insufficient_data'}
        
        recent_tensions = [r.tension_magnitude for r in list(self.tension_history)[-10:]]
        recent_scup = list(self.scup_history)[-10:]
        recent_entropy = list(self.entropy_history)[-10:]
        
        # Simple trend calculation (could be enhanced with linear regression)
        tension_trend = recent_tensions[-1] - recent_tensions[0]
        scup_trend = recent_scup[-1] - recent_scup[0] if recent_scup else 0
        entropy_trend = recent_entropy[-1] - recent_entropy[0] if recent_entropy else 0
        
        return {
            'tension_trend': tension_trend,
            'scup_trend': scup_trend,
            'entropy_trend': entropy_trend,
            'trend_strength': abs(tension_trend),
            'trend_direction': 'increasing' if tension_trend > 0.05 else 'decreasing' if tension_trend < -0.05 else 'stable'
        }
    
    def _calculate_zone_stability(self) -> Dict:
        """Calculate how stable the current zone is."""
        if len(self.zone_transition_history) < 2:
            return {'stability': 'unknown', 'transitions_recent': 0}
        
        # Count recent transitions (last 5 minutes)
        recent_transitions = []
        cutoff_time = datetime.utcnow() - timedelta(minutes=5)
        
        for transition in self.zone_transition_history:
            if isinstance(transition, dict) and 'timestamp' in transition:
                if transition['timestamp'] > cutoff_time:
                    recent_transitions.append(transition)
        
        transition_count = len(recent_transitions)
        
        if transition_count == 0:
            stability = 'stable'
        elif transition_count <= 2:
            stability = 'moderate'
        else:
            stability = 'unstable'
        
        return {
            'stability': stability,
            'transitions_recent': transition_count,
            'current_zone_duration': self._get_current_zone_duration()
        }
    
    def _get_current_zone_duration(self) -> float:
        """Get duration in current zone (seconds)."""
        if not self.zone_transition_history:
            return 0.0
        
        last_transition = self.zone_transition_history[-1]
        if isinstance(last_transition, dict) and 'timestamp' in last_transition:
            return (datetime.utcnow() - last_transition['timestamp']).total_seconds()
        
        return 0.0
    
    def predict_tension_trajectory(self, steps_ahead: int = 5) -> List[Dict]:
        """Predict tension trajectory based on current trends."""
        if len(self.tension_history) < 10:
            return []
        
        # Simple linear extrapolation (could be enhanced with ML models)
        recent_tensions = [r.tension_magnitude for r in list(self.tension_history)[-10:]]
        recent_scup = list(self.scup_history)[-10:]
        recent_entropy = list(self.entropy_history)[-10:]
        
        # Calculate average rates of change
        tension_rate = (recent_tensions[-1] - recent_tensions[0]) / len(recent_tensions)
        scup_rate = (recent_scup[-1] - recent_scup[0]) / len(recent_scup) if recent_scup else 0
        entropy_rate = (recent_entropy[-1] - recent_entropy[0]) / len(recent_entropy) if recent_entropy else 0
        
        predictions = []
        current_tension = recent_tensions[-1]
        current_scup = recent_scup[-1] if recent_scup else 0.7
        current_entropy = recent_entropy[-1] if recent_entropy else 0.5
        
        for step in range(1, steps_ahead + 1):
            # Project forward
            pred_tension = max(0.0, min(1.0, current_tension + tension_rate * step))
            pred_scup = max(0.0, min(1.0, current_scup + scup_rate * step))
            pred_entropy = max(0.0, min(1.0, current_entropy + entropy_rate * step))
            
            # Classify predicted zone
            pred_zone = self._classify_tension_zone(pred_tension)
            
            predictions.append({
                'step': step,
                'predicted_tension': pred_tension,
                'predicted_scup': pred_scup,
                'predicted_entropy': pred_entropy,
                'predicted_zone': pred_zone.value,
                'confidence': max(0.1, 1.0 - step * 0.15)  # Decreasing confidence
            })
        
        return predictions
    
    def get_tension_recommendations(self) -> Dict[str, Any]:
        """Get actionable recommendations based on current tension state."""
        if not self.tension_history:
            return {'status': 'no_data'}
        
        latest = self.tension_history[-1]
        zone = latest.zone
        tension = latest.tension_magnitude
        
        recommendations = {
            'zone': zone.value,
            'tension_level': tension,
            'immediate_actions': [],
            'system_adjustments': {},
            'monitoring_focus': []
        }
        
        # Zone-specific recommendations
        if zone == TensionZone.HARMONIC:
            recommendations['immediate_actions'].extend([
                'Consider increasing creative challenges',
                'System is stable - good time for optimization',
                'Monitor for stagnation'
            ])
            recommendations['system_adjustments']['tick_interval'] = 'can_increase'
            recommendations['monitoring_focus'].extend(['entropy_levels', 'creative_output'])
        
        elif zone == TensionZone.CREATIVE:
            recommendations['immediate_actions'].extend([
                'Maintain current balance',
                'Good state for complex problem solving',
                'Monitor for transitions'
            ])
            recommendations['system_adjustments']['heat_scaling'] = 'optimal'
            recommendations['monitoring_focus'].extend(['balance_maintenance', 'output_quality'])
        
        elif zone == TensionZone.TURBULENT:
            recommendations['immediate_actions'].extend([
                'Increase stabilization efforts',
                'Reduce system complexity temporarily',
                'Focus on core functions'
            ])
            recommendations['system_adjustments']['tick_interval'] = 'decrease'
            recommendations['system_adjustments']['heat_scaling'] = 'reduce'
            recommendations['monitoring_focus'].extend(['stability_metrics', 'error_rates'])
        
        elif zone == TensionZone.CRITICAL:
            recommendations['immediate_actions'].extend([
                'IMMEDIATE: Stabilization required',
                'Reduce entropy sources',
                'Increase coherence mechanisms',
                'Consider emergency protocols'
            ])
            recommendations['system_adjustments']['tick_interval'] = 'minimize'
            recommendations['system_adjustments']['heat_scaling'] = 'emergency_mode'
            recommendations['monitoring_focus'].extend(['critical_metrics', 'system_health'])
        
        # Add trend-based recommendations
        trends = self._calculate_trends()
        if trends.get('trend_direction') == 'increasing' and tension > 0.6:
            recommendations['immediate_actions'].append('Tension rising - prepare stabilization')
        elif trends.get('trend_direction') == 'decreasing' and tension < 0.3:
            recommendations['immediate_actions'].append('Tension falling - consider activation')
        
        return recommendations
    
    def calibrate_sensitivity(self, new_sensitivity: float):
        """Calibrate tension sensitivity."""
        old_sensitivity = self.tension_sensitivity
        self.tension_sensitivity = max(0.1, min(3.0, new_sensitivity))
        
        print(f"[TensionEngine] ⚖️ Sensitivity calibrated: {old_sensitivity:.2f} → {self.tension_sensitivity:.2f}")
    
    def get_zone_statistics(self) -> Dict[str, Any]:
        """Get statistics about zone transitions and time spent."""
        if not self.tension_history:
            return {'status': 'no_data'}
        
        # Count time in each zone
        zone_times = {zone.value: 0.0 for zone in TensionZone}
        zone_counts = {zone.value: 0 for zone in TensionZone}
        
        for reading in self.tension_history:
            zone_counts[reading.zone.value] += 1
        
        total_readings = len(self.tension_history)
        zone_percentages = {
            zone: (count / total_readings) * 100 
            for zone, count in zone_counts.items()
        }
        
        # Transition statistics
        transition_count = len(self.zone_transition_history)
        avg_zone_duration = self._calculate_average_zone_duration()
        
        return {
            'total_readings': total_readings,
            'zone_percentages': zone_percentages,
            'zone_counts': zone_counts,
            'transition_count': transition_count,
            'average_zone_duration_seconds': avg_zone_duration,
            'current_zone': self.current_zone.value,
            'current_zone_duration': self._get_current_zone_duration()
        }
    
    def _calculate_average_zone_duration(self) -> float:
        """Calculate average duration spent in each zone."""
        if len(self.zone_transition_history) < 2:
            return 0.0
        
        durations = []
        for i in range(1, len(self.zone_transition_history)):
            prev_transition = self.zone_transition_history[i-1]
            curr_transition = self.zone_transition_history[i]
            
            if (isinstance(prev_transition, dict) and isinstance(curr_transition, dict) and
                'timestamp' in prev_transition and 'timestamp' in curr_transition):
                duration = (curr_transition['timestamp'] - prev_transition['timestamp']).total_seconds()
                durations.append(duration)
        
        return sum(durations) / len(durations) if durations else 0.0

# Global tension engine instance
tension_engine = TensionEngine()

# Convenience functions for external systems
def calculate_semantic_tension(scup_score: float, entropy_level: float, 
                             pulse_heat: float = None) -> TensionReading:
    """Calculate current semantic tension."""
    return tension_engine.calculate_tension(scup_score, entropy_level, pulse_heat)

def get_tension_state() -> Dict:
    """Get current tension state."""
    return tension_engine.get_current_tension_state()

def get_tension_recommendations() -> Dict:
    """Get tension-based recommendations."""
    return tension_engine.get_tension_recommendations()

def predict_tension(steps_ahead: int = 5) -> List[Dict]:
    """Predict tension trajectory."""
    return tension_engine.predict_tension_trajectory(steps_ahead)

def get_zone_stats() -> Dict:
    """Get zone statistics."""
    return tension_engine.get_zone_statistics()

def calibrate_tension_sensitivity(sensitivity: float):
    """Calibrate tension engine sensitivity."""
    tension_engine.calibrate_sensitivity(sensitivity)

# Integration with other systems
def get_recommended_tick_interval(scup: float, entropy: float) -> float:
    """Get recommended tick interval based on tension analysis."""
    reading = calculate_semantic_tension(scup, entropy)
    return reading.recommended_interval

def get_heat_scaling_factor(scup: float, entropy: float) -> float:
    """Get heat scaling factor based on tension analysis."""
    reading = calculate_semantic_tension(scup, entropy)
    return reading.heat_scaling

def get_action_threshold(scup: float, entropy: float) -> float:
    """Get action threshold based on tension analysis."""
    reading = calculate_semantic_tension(scup, entropy)
    return reading.action_threshold

def should_trigger_stabilization() -> bool:
    """Check if stabilization should be triggered based on tension."""
    state = get_tension_state()
    if 'current_zone' not in state:
        return False
    
    return (state['current_zone'] in ['turbulent', 'critical'] or
            state.get('current_tension', 0) > 0.7)

def should_increase_activity() -> bool:
    """Check if activity should be increased based on low tension."""
    state = get_tension_state()
    if 'current_zone' not in state:
        return False
    
    return (state['current_zone'] == 'harmonic' and
            state.get('current_tension', 0) < 0.2)

# Schema phase tagging
__schema_phase__ = "Liminal-Agency-Transition"
__dawn_signature__ = "🧠 DAWN Tension-Aware"

print("[TensionEngine] ⚡ DAWN semantic tension engine initialized")
print("[TensionEngine] 🌊 Ready to monitor SCUP-entropy dynamics")
