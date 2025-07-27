#!/usr/bin/env python3
"""
DAWN Drift Tracer - Cognitive Drift Detection & Analysis
Monitors deviation from entropy/mood baselines and semantic coherence shifts
"""

import time
import logging
from typing import Dict, List, Any, Optional, Deque
from collections import deque
from dataclasses import dataclass
from enum import Enum

# DAWN component imports
try:
    from core.enhanced_drift_reflex import EnhancedDriftReflex, ReflexZone, ReflexTrigger
    from semantic.drift_calculator import calculate_pressure_delta
    DRIFT_COMPONENTS_AVAILABLE = True
except ImportError:
    DRIFT_COMPONENTS_AVAILABLE = False

logger = logging.getLogger("drift_tracer")

class DriftType(Enum):
    """Types of drift detected"""
    SEMANTIC = "semantic"
    ENTROPY = "entropy"
    COHERENCE = "coherence"
    THERMAL = "thermal"
    MOOD = "mood"

@dataclass
class DriftObservation:
    """A single drift observation"""
    timestamp: float
    drift_type: DriftType
    magnitude: float
    baseline_deviation: float
    current_value: float
    baseline_value: float
    trend_direction: str  # "rising", "falling", "stable"

class DriftTracer:
    """
    Monitors cognitive drift patterns and deviations from baseline states.
    
    Detects:
    - Semantic field pressure shifts
    - Entropy baseline deviations
    - Coherence degradation
    - Thermal regulation anomalies
    - Mood state instability
    """
    
    def __init__(self, history_size: int = 100):
        """Initialize drift tracer with baseline tracking"""
        self.history_size = history_size
        
        # Historical data for baseline calculation
        self.entropy_history: Deque[float] = deque(maxlen=history_size)
        self.scup_history: Deque[float] = deque(maxlen=history_size)
        self.heat_history: Deque[float] = deque(maxlen=history_size)
        self.pressure_history: Deque[float] = deque(maxlen=history_size)
        
        # Baseline states
        self.baselines = {
            'entropy': 0.5,
            'scup': 0.7,
            'heat': 0.4,
            'pressure': 10.0
        }
        
        # Drift detection thresholds
        self.drift_thresholds = {
            'minor': 0.15,    # 15% deviation
            'moderate': 0.30,  # 30% deviation
            'major': 0.50,     # 50% deviation
            'critical': 0.75   # 75% deviation
        }
        
        # Integration with enhanced drift reflex
        self.drift_reflex = None
        if DRIFT_COMPONENTS_AVAILABLE:
            try:
                self.drift_reflex = EnhancedDriftReflex()
            except Exception as e:
                logger.warning(f"Could not initialize drift reflex: {e}")
        
        # Recent observations
        self.recent_observations: Deque[DriftObservation] = deque(maxlen=50)
        
        # State tracking
        self.current_zone = "stable"
        self.last_major_drift = None
        self.drift_event_count = 0
        
        logger.info("🌊 DriftTracer initialized with baseline monitoring")
    
    def observe(self, state: Dict[str, Any]) -> List[DriftObservation]:
        """
        Observe current state and detect drift patterns.
        
        Args:
            state: Current tick state containing entropy, scup, heat, etc.
            
        Returns:
            List of drift observations
        """
        current_time = time.time()
        observations = []
        
        # Extract values from state
        entropy = state.get('entropy', 0.5)
        scup = state.get('scup', 0.7)
        heat = state.get('heat', 0.4)
        
        # Calculate semantic pressure if available
        pressure = 0.0
        if DRIFT_COMPONENTS_AVAILABLE:
            try:
                pressure = calculate_pressure_delta(state)
            except Exception:
                pressure = 0.0
        
        # Update histories
        self.entropy_history.append(entropy)
        self.scup_history.append(scup)
        self.heat_history.append(heat)
        self.pressure_history.append(pressure)
        
        # Update baselines (moving average)
        self._update_baselines()
        
        # Detect entropy drift
        entropy_obs = self._detect_drift(
            DriftType.ENTROPY, 
            entropy, 
            self.baselines['entropy'],
            current_time
        )
        if entropy_obs:
            observations.append(entropy_obs)
        
        # Detect coherence drift (via SCUP)
        coherence_obs = self._detect_drift(
            DriftType.COHERENCE,
            scup,
            self.baselines['scup'], 
            current_time
        )
        if coherence_obs:
            observations.append(coherence_obs)
        
        # Detect thermal drift
        thermal_obs = self._detect_drift(
            DriftType.THERMAL,
            heat,
            self.baselines['heat'],
            current_time
        )
        if thermal_obs:
            observations.append(thermal_obs)
        
        # Detect semantic pressure drift
        if pressure > 0:
            pressure_obs = self._detect_drift(
                DriftType.SEMANTIC,
                pressure,
                self.baselines['pressure'],
                current_time
            )
            if pressure_obs:
                observations.append(pressure_obs)
        
        # Update zone based on observations
        self._update_drift_zone(observations)
        
        # Store observations
        for obs in observations:
            self.recent_observations.append(obs)
        
        # Integrate with drift reflex if available
        if self.drift_reflex and observations:
            self._integrate_with_reflex(observations, state)
        
        return observations
    
    def _detect_drift(self, drift_type: DriftType, current: float, 
                     baseline: float, timestamp: float) -> Optional[DriftObservation]:
        """Detect drift for a specific metric"""
        if baseline == 0:
            return None
        
        # Calculate deviation
        deviation = abs(current - baseline) / baseline
        
        # Only report significant drift
        if deviation < self.drift_thresholds['minor']:
            return None
        
        # Determine trend direction
        trend = "stable"
        if drift_type == DriftType.ENTROPY and len(self.entropy_history) > 1:
            trend = "rising" if current > list(self.entropy_history)[-2] else "falling"
        elif drift_type == DriftType.COHERENCE and len(self.scup_history) > 1:
            trend = "falling" if current < list(self.scup_history)[-2] else "rising"
        elif drift_type == DriftType.THERMAL and len(self.heat_history) > 1:
            trend = "rising" if current > list(self.heat_history)[-2] else "falling"
        
        observation = DriftObservation(
            timestamp=timestamp,
            drift_type=drift_type,
            magnitude=deviation,
            baseline_deviation=deviation,
            current_value=current,
            baseline_value=baseline,
            trend_direction=trend
        )
        
        # Track major drift events
        if deviation >= self.drift_thresholds['major']:
            self.last_major_drift = observation
            self.drift_event_count += 1
        
        return observation
    
    def _update_baselines(self):
        """Update baseline values using moving averages"""
        if len(self.entropy_history) >= 10:
            self.baselines['entropy'] = sum(list(self.entropy_history)[-10:]) / 10
        
        if len(self.scup_history) >= 10:
            self.baselines['scup'] = sum(list(self.scup_history)[-10:]) / 10
        
        if len(self.heat_history) >= 10:
            self.baselines['heat'] = sum(list(self.heat_history)[-10:]) / 10
        
        if len(self.pressure_history) >= 10:
            self.baselines['pressure'] = sum(list(self.pressure_history)[-10:]) / 10
    
    def _update_drift_zone(self, observations: List[DriftObservation]):
        """Update current drift zone based on observations"""
        if not observations:
            self.current_zone = "stable"
            return
        
        max_magnitude = max(obs.magnitude for obs in observations)
        
        if max_magnitude >= self.drift_thresholds['critical']:
            self.current_zone = "critical"
        elif max_magnitude >= self.drift_thresholds['major']:
            self.current_zone = "major"
        elif max_magnitude >= self.drift_thresholds['moderate']:
            self.current_zone = "moderate"
        else:
            self.current_zone = "minor"
    
    def _integrate_with_reflex(self, observations: List[DriftObservation], state: Dict[str, Any]):
        """Integrate observations with the enhanced drift reflex system"""
        if not self.drift_reflex:
            return
        
        for obs in observations:
            # Map drift observations to reflex triggers
            if obs.drift_type == DriftType.ENTROPY and obs.magnitude > self.drift_thresholds['moderate']:
                # Trigger entropy reflex
                if hasattr(self.drift_reflex, 'trigger_count'):
                    self.drift_reflex.trigger_count += 1
            
            elif obs.drift_type == DriftType.SEMANTIC and obs.magnitude > self.drift_thresholds['moderate']:
                # Trigger semantic pressure reflex
                if hasattr(self.drift_reflex, 'current_zone'):
                    self.drift_reflex.current_zone = ReflexZone.YELLOW if obs.magnitude < 0.5 else ReflexZone.RED
    
    def get_drift_summary(self) -> Dict[str, Any]:
        """Get summary of current drift state"""
        recent_obs = list(self.recent_observations)[-10:]
        
        summary = {
            'current_zone': self.current_zone,
            'total_drift_events': self.drift_event_count,
            'baselines': self.baselines.copy(),
            'recent_drift_count': len(recent_obs),
            'drift_types_active': list(set(obs.drift_type.value for obs in recent_obs)),
            'max_recent_magnitude': max((obs.magnitude for obs in recent_obs), default=0),
            'last_major_drift': self.last_major_drift.drift_type.value if self.last_major_drift else None
        }
        
        return summary
    
    def get_trend_analysis(self) -> Dict[str, str]:
        """Analyze trends across different metrics"""
        trends = {}
        
        # Entropy trend
        if len(self.entropy_history) >= 5:
            recent = list(self.entropy_history)[-5:]
            if recent[-1] > recent[0] * 1.1:
                trends['entropy'] = 'rising'
            elif recent[-1] < recent[0] * 0.9:
                trends['entropy'] = 'falling'
            else:
                trends['entropy'] = 'stable'
        
        # Coherence trend (SCUP)
        if len(self.scup_history) >= 5:
            recent = list(self.scup_history)[-5:]
            if recent[-1] > recent[0] * 1.1:
                trends['coherence'] = 'improving'
            elif recent[-1] < recent[0] * 0.9:
                trends['coherence'] = 'degrading'
            else:
                trends['coherence'] = 'stable'
        
        # Thermal trend
        if len(self.heat_history) >= 5:
            recent = list(self.heat_history)[-5:]
            if recent[-1] > recent[0] * 1.1:
                trends['thermal'] = 'heating'
            elif recent[-1] < recent[0] * 0.9:
                trends['thermal'] = 'cooling'
            else:
                trends['thermal'] = 'stable'
        
        return trends
    
    def reset_baselines(self):
        """Reset baseline calculations"""
        self.baselines = {
            'entropy': 0.5,
            'scup': 0.7,
            'heat': 0.4,
            'pressure': 10.0
        }
        logger.info("Drift baselines reset to defaults")
    
    def export_state(self) -> Dict[str, Any]:
        """Export current tracer state"""
        return {
            'current_zone': self.current_zone,
            'baselines': self.baselines,
            'drift_event_count': self.drift_event_count,
            'last_major_drift': self.last_major_drift.__dict__ if self.last_major_drift else None,
            'history_sizes': {
                'entropy': len(self.entropy_history),
                'scup': len(self.scup_history),
                'heat': len(self.heat_history),
                'pressure': len(self.pressure_history)
            }
        } 