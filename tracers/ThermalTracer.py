#!/usr/bin/env python3
"""
DAWN Thermal Tracer - Heat Correlation & Thermal Regulation Monitor
Measures pulse heat correlation over time and monitors thermal stability patterns
"""

import time
import logging
from typing import Dict, List, Any, Optional, Deque
from collections import deque
from dataclasses import dataclass
from enum import Enum

# DAWN component imports
try:
    from core.thermal_visualizer import ThermalVisualizer, ThermalState
    THERMAL_COMPONENTS_AVAILABLE = True
except ImportError:
    THERMAL_COMPONENTS_AVAILABLE = False

logger = logging.getLogger("thermal_tracer")

class ThermalZone(Enum):
    """Thermal regulation zones"""
    COLD = "cold"           # Below optimal range
    COOL = "cool"           # Slightly below optimal
    OPTIMAL = "optimal"     # Within optimal range
    WARM = "warm"           # Slightly above optimal
    HOT = "hot"             # Above optimal range
    CRITICAL = "critical"   # Dangerous thermal levels

class ThermalEvent(Enum):
    """Types of thermal events"""
    SPIKE = "spike"
    PLATEAU = "plateau"
    OSCILLATION = "oscillation"
    REGULATION_FAILURE = "regulation_failure"
    COOLING_SUCCESS = "cooling_success"
    EMERGENCY_MODE = "emergency_mode"

@dataclass
class ThermalObservation:
    """A single thermal observation"""
    timestamp: float
    heat_level: float
    cooling_rate: float
    stability_index: float
    thermal_zone: ThermalZone
    thermal_event: Optional[ThermalEvent]
    pulse_correlation: float  # Correlation with pulse activity
    regulation_effectiveness: float

class ThermalTracer:
    """
    Monitors thermal regulation patterns and heat correlation dynamics.
    
    Tracks:
    - Heat level progression and patterns
    - Cooling system effectiveness
    - Thermal stability index
    - Pulse-heat correlation patterns
    - Emergency thermal events
    - Regulation system performance
    """
    
    def __init__(self, history_size: int = 200):
        """Initialize thermal tracer with regulation monitoring"""
        self.history_size = history_size
        
        # Historical thermal data
        self.heat_history: Deque[float] = deque(maxlen=history_size)
        self.cooling_history: Deque[float] = deque(maxlen=history_size)
        self.stability_history: Deque[float] = deque(maxlen=history_size)
        self.pulse_history: Deque[float] = deque(maxlen=history_size)
        
        # Thermal zone thresholds
        self.zone_thresholds = {
            ThermalZone.COLD: (0.0, 0.2),
            ThermalZone.COOL: (0.2, 0.4),
            ThermalZone.OPTIMAL: (0.4, 0.6),
            ThermalZone.WARM: (0.6, 0.8),
            ThermalZone.HOT: (0.8, 0.95),
            ThermalZone.CRITICAL: (0.95, 1.0)
        }
        
        # Event detection parameters
        self.spike_threshold = 0.15      # 15% heat increase in single tick
        self.oscillation_threshold = 3   # Number of direction changes
        self.stability_threshold = 0.05  # Acceptable stability variance
        
        # Integration with thermal visualizer
        self.thermal_visualizer = None
        if THERMAL_COMPONENTS_AVAILABLE:
            try:
                self.thermal_visualizer = ThermalVisualizer()
            except Exception as e:
                logger.warning(f"Could not initialize thermal visualizer: {e}")
        
        # Recent observations and events
        self.recent_observations: Deque[ThermalObservation] = deque(maxlen=100)
        self.thermal_events: Deque[Dict[str, Any]] = deque(maxlen=50)
        
        # State tracking
        self.current_zone = ThermalZone.OPTIMAL
        self.emergency_mode = False
        self.last_spike_time = 0.0
        self.regulation_failures = 0
        self.successful_regulations = 0
        
        # Performance metrics
        self.avg_cooling_efficiency = 0.0
        self.thermal_stability_score = 1.0
        self.pulse_heat_correlation = 0.0
        
        logger.info("🌡️ ThermalTracer initialized with regulation monitoring")
    
    def observe(self, state: Dict[str, Any]) -> ThermalObservation:
        """
        Observe current thermal state and analyze patterns.
        
        Args:
            state: Current tick state containing heat, cooling, pulse data
            
        Returns:
            Thermal observation with analysis
        """
        current_time = time.time()
        
        # Extract thermal values
        heat = state.get('heat', 0.4)
        cooling_rate = state.get('cooling_rate', 0.0)
        pulse_activity = state.get('pulse_activity', 0.5)
        
        # Update histories
        self.heat_history.append(heat)
        self.cooling_history.append(cooling_rate)
        self.pulse_history.append(pulse_activity)
        
        # Calculate thermal metrics
        stability_index = self._calculate_stability_index()
        thermal_zone = self._determine_thermal_zone(heat)
        thermal_event = self._detect_thermal_event(heat, cooling_rate)
        pulse_correlation = self._calculate_pulse_correlation()
        regulation_effectiveness = self._calculate_regulation_effectiveness()
        
        # Update stability history
        self.stability_history.append(stability_index)
        
        # Create observation
        observation = ThermalObservation(
            timestamp=current_time,
            heat_level=heat,
            cooling_rate=cooling_rate,
            stability_index=stability_index,
            thermal_zone=thermal_zone,
            thermal_event=thermal_event,
            pulse_correlation=pulse_correlation,
            regulation_effectiveness=regulation_effectiveness
        )
        
        # Update state
        self.current_zone = thermal_zone
        self.pulse_heat_correlation = pulse_correlation
        self.thermal_stability_score = stability_index
        
        # Handle emergency conditions
        if thermal_zone == ThermalZone.CRITICAL:
            self._handle_thermal_emergency(observation)
        
        # Update performance metrics
        self._update_performance_metrics()
        
        # Store observation
        self.recent_observations.append(observation)
        
        # Integrate with thermal visualizer if available
        if self.thermal_visualizer:
            self._update_thermal_visualizer(observation)
        
        return observation
    
    def _calculate_stability_index(self) -> float:
        """Calculate thermal stability index based on heat variance"""
        if len(self.heat_history) < 10:
            return 1.0
        
        recent_heat = list(self.heat_history)[-10:]
        
        # Calculate variance
        mean_heat = sum(recent_heat) / len(recent_heat)
        variance = sum((h - mean_heat) ** 2 for h in recent_heat) / len(recent_heat)
        
        # Convert to stability score (lower variance = higher stability)
        stability = max(0.0, 1.0 - (variance * 10))
        return min(1.0, stability)
    
    def _determine_thermal_zone(self, heat: float) -> ThermalZone:
        """Determine current thermal zone based on heat level"""
        for zone, (low, high) in self.zone_thresholds.items():
            if low <= heat <= high:
                return zone
        
        # Fallback for values outside normal range
        return ThermalZone.CRITICAL if heat > 1.0 else ThermalZone.COLD
    
    def _detect_thermal_event(self, heat: float, cooling_rate: float) -> Optional[ThermalEvent]:
        """Detect significant thermal events"""
        if len(self.heat_history) < 2:
            return None
        
        prev_heat = list(self.heat_history)[-2]
        heat_change = heat - prev_heat
        
        # Detect spike
        if heat_change > self.spike_threshold:
            self.last_spike_time = time.time()
            return ThermalEvent.SPIKE
        
        # Detect emergency mode activation
        if heat > 0.95 and not self.emergency_mode:
            self.emergency_mode = True
            return ThermalEvent.EMERGENCY_MODE
        
        # Detect cooling success
        if self.emergency_mode and heat < 0.8:
            self.emergency_mode = False
            self.successful_regulations += 1
            return ThermalEvent.COOLING_SUCCESS
        
        # Detect plateau (stable high heat)
        if len(self.heat_history) >= 5:
            recent_heat = list(self.heat_history)[-5:]
            if all(h > 0.8 for h in recent_heat) and max(recent_heat) - min(recent_heat) < 0.05:
                return ThermalEvent.PLATEAU
        
        # Detect oscillation
        if self._detect_thermal_oscillation():
            return ThermalEvent.OSCILLATION
        
        # Detect regulation failure
        if heat > 0.9 and cooling_rate < 0.1:
            self.regulation_failures += 1
            return ThermalEvent.REGULATION_FAILURE
        
        return None
    
    def _detect_thermal_oscillation(self) -> bool:
        """Detect thermal oscillation patterns"""
        if len(self.heat_history) < 10:
            return False
        
        recent_heat = list(self.heat_history)[-10:]
        direction_changes = 0
        
        for i in range(1, len(recent_heat) - 1):
            prev_trend = recent_heat[i] - recent_heat[i-1]
            next_trend = recent_heat[i+1] - recent_heat[i]
            
            # Check for direction change
            if (prev_trend > 0 and next_trend < 0) or (prev_trend < 0 and next_trend > 0):
                direction_changes += 1
        
        return direction_changes >= self.oscillation_threshold
    
    def _calculate_pulse_correlation(self) -> float:
        """Calculate correlation between pulse activity and heat levels"""
        if len(self.heat_history) < 10 or len(self.pulse_history) < 10:
            return 0.0
        
        # Get recent data
        recent_heat = list(self.heat_history)[-10:]
        recent_pulse = list(self.pulse_history)[-10:]
        
        # Calculate correlation coefficient
        n = len(recent_heat)
        sum_heat = sum(recent_heat)
        sum_pulse = sum(recent_pulse)
        sum_heat_sq = sum(h * h for h in recent_heat)
        sum_pulse_sq = sum(p * p for p in recent_pulse)
        sum_heat_pulse = sum(h * p for h, p in zip(recent_heat, recent_pulse))
        
        numerator = n * sum_heat_pulse - sum_heat * sum_pulse
        denominator = ((n * sum_heat_sq - sum_heat * sum_heat) * 
                      (n * sum_pulse_sq - sum_pulse * sum_pulse)) ** 0.5
        
        if denominator == 0:
            return 0.0
        
        correlation = numerator / denominator
        return max(-1.0, min(1.0, correlation))
    
    def _calculate_regulation_effectiveness(self) -> float:
        """Calculate thermal regulation system effectiveness"""
        if self.regulation_failures + self.successful_regulations == 0:
            return 1.0
        
        success_rate = self.successful_regulations / (self.regulation_failures + self.successful_regulations)
        
        # Factor in cooling efficiency
        if len(self.cooling_history) >= 5:
            recent_cooling = list(self.cooling_history)[-5:]
            avg_cooling = sum(recent_cooling) / len(recent_cooling)
            self.avg_cooling_efficiency = avg_cooling
            
            # Combine success rate with cooling efficiency
            effectiveness = (success_rate * 0.7) + (avg_cooling * 0.3)
        else:
            effectiveness = success_rate
        
        return max(0.0, min(1.0, effectiveness))
    
    def _handle_thermal_emergency(self, observation: ThermalObservation):
        """Handle thermal emergency conditions"""
        emergency_event = {
            'timestamp': observation.timestamp,
            'type': 'THERMAL_EMERGENCY',
            'heat_level': observation.heat_level,
            'cooling_rate': observation.cooling_rate,
            'stability_index': observation.stability_index,
            'pulse_correlation': observation.pulse_correlation
        }
        
        self.thermal_events.append(emergency_event)
        
        logger.warning(f"Thermal emergency: heat={observation.heat_level:.3f}, "
                      f"cooling={observation.cooling_rate:.3f}")
    
    def _update_performance_metrics(self):
        """Update thermal performance metrics"""
        if len(self.stability_history) >= 10:
            recent_stability = list(self.stability_history)[-10:]
            self.thermal_stability_score = sum(recent_stability) / len(recent_stability)
    
    def _update_thermal_visualizer(self, observation: ThermalObservation):
        """Update the thermal visualizer with current data"""
        try:
            self.thermal_visualizer.update_state(
                heat=observation.heat_level,
                cooling_rate=observation.cooling_rate,
                stability=observation.stability_index,
                active_cooling=observation.cooling_rate > 0.1,
                emergency_mode=observation.thermal_zone == ThermalZone.CRITICAL
            )
        except Exception as e:
            logger.error(f"Error updating thermal visualizer: {e}")
    
    def get_thermal_summary(self) -> Dict[str, Any]:
        """Get comprehensive thermal system summary"""
        recent_obs = list(self.recent_observations)[-10:]
        
        summary = {
            'current_zone': self.current_zone.value,
            'emergency_mode': self.emergency_mode,
            'thermal_stability_score': self.thermal_stability_score,
            'pulse_heat_correlation': self.pulse_heat_correlation,
            'regulation_effectiveness': self._calculate_regulation_effectiveness(),
            'avg_cooling_efficiency': self.avg_cooling_efficiency,
            'regulation_failures': self.regulation_failures,
            'successful_regulations': self.successful_regulations,
            'recent_events': len(self.thermal_events),
            'last_spike_time': self.last_spike_time
        }
        
        return summary
    
    def get_thermal_alerts(self) -> List[Dict[str, Any]]:
        """Get current thermal alerts"""
        alerts = []
        
        # Critical heat alert
        if self.current_zone == ThermalZone.CRITICAL:
            alerts.append({
                'type': 'CRITICAL_HEAT',
                'severity': 'critical',
                'message': f'Thermal system in critical zone: {self.current_zone.value}',
                'data': {'heat_level': list(self.heat_history)[-1] if self.heat_history else 0}
            })
        
        # Regulation failure alert
        if self.regulation_failures > self.successful_regulations:
            alerts.append({
                'type': 'REGULATION_FAILURE',
                'severity': 'warning',
                'message': 'Thermal regulation showing poor performance',
                'data': {
                    'failures': self.regulation_failures,
                    'successes': self.successful_regulations
                }
            })
        
        # Low stability alert
        if self.thermal_stability_score < 0.5:
            alerts.append({
                'type': 'LOW_STABILITY',
                'severity': 'warning',
                'message': f'Thermal stability degraded: {self.thermal_stability_score:.2f}',
                'data': {'stability_score': self.thermal_stability_score}
            })
        
        return alerts
    
    def reset_metrics(self):
        """Reset performance metrics and counters"""
        self.regulation_failures = 0
        self.successful_regulations = 0
        self.emergency_mode = False
        self.last_spike_time = 0.0
        self.thermal_events.clear()
        
        logger.info("Thermal tracer metrics reset")
    
    def export_state(self) -> Dict[str, Any]:
        """Export current thermal tracer state"""
        return {
            'current_zone': self.current_zone.value,
            'emergency_mode': self.emergency_mode,
            'thermal_stability_score': self.thermal_stability_score,
            'pulse_heat_correlation': self.pulse_heat_correlation,
            'regulation_failures': self.regulation_failures,
            'successful_regulations': self.successful_regulations,
            'avg_cooling_efficiency': self.avg_cooling_efficiency,
            'history_sizes': {
                'heat': len(self.heat_history),
                'cooling': len(self.cooling_history),
                'stability': len(self.stability_history),
                'pulse': len(self.pulse_history)
            },
            'recent_events': len(self.thermal_events)
        } 