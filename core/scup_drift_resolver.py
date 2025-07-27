#!/usr/bin/env python3
"""
DAWN SCUP Drift Resolver - Coherence Tracking Mathematics
=========================================================

Implements the SCUP drift resolution equation: SCUP_i × Δd_i / Entropy_i

Enhanced with:
- Cognitive Pressure Engine: P = B * σ² (Bloom mass × Sigil velocity squared)
- Schema Health Index (SHI) monitoring
- Tracer ecosystem integration
- Advanced drift state management

Where:
- SCUP_i = Semantic Coherence Under Pressure value at time i
- Δd_i = Drift delta (change in semantic drift) at time i  
- Entropy_i = System entropy at time i
- P = Cognitive Pressure (B * σ²)
- SHI = Schema Health Index (vitality, memory, orbit, ash, soft_edge)

This formula provides drift-weighted coherence tracking that:
- Emphasizes coherence during high drift periods
- Accounts for entropy's destabilizing influence
- Monitors cognitive pressure and schema health
- Enables predictive drift forecasting
- Powers internal prioritization systems
- Stabilizes semantic consistency over time

The drift resolver acts as DAWN's semantic compass, helping maintain
conceptual coherence even during turbulent cognitive states.
"""

import time
import math
import logging
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple, Callable
from datetime import datetime, timezone
from collections import deque
from enum import Enum

# Integration with existing SCUP system
try:
    from schema.scup_math import compute_basic_scup, SCUPInputs
    from schema.scup_tracker import SCUPTracker
    SCUP_SYSTEM_AVAILABLE = True
except ImportError:
    SCUP_SYSTEM_AVAILABLE = False

logger = logging.getLogger("scup_drift_resolver")

class DriftState(Enum):
    """Semantic drift states"""
    STABLE = "STABLE"           # Low drift, high coherence
    OSCILLATING = "OSCILLATING" # Moderate drift, variable coherence
    TRENDING = "TRENDING"       # Consistent drift direction
    CHAOTIC = "CHAOTIC"         # High drift, low predictability
    CONVERGING = "CONVERGING"   # Drift reducing, stabilizing
    PRESSURIZED = "PRESSURIZED" # High cognitive pressure state
    UNHEALTHY = "UNHEALTHY"     # Low schema health

@dataclass
class CognitivePressureState:
    """Cognitive pressure state tracking"""
    bloom_mass: float           # B in P = B * σ²
    sigil_velocity: float       # σ in P = B * σ²
    pressure_value: float       # P = B * σ²
    pressure_level: str         # "low", "moderate", "high", "critical"
    pressure_trend: float       # Rate of pressure change
    relief_actions: List[str] = field(default_factory=list)

@dataclass
class SchemaHealthState:
    """Schema Health Index (SHI) state"""
    vitality: float             # v: System vitality
    memory_health: float        # m: Memory system health
    orbit_load: float          # o: Processing orbit load
    ash_availability: float     # a: Available cognitive ash
    soft_edge_response: float   # s: Soft edge responsiveness
    shi_value: float           # Combined health index
    health_level: str          # "poor", "fair", "good", "excellent"
    recommendations: List[str] = field(default_factory=list)

@dataclass
class DriftMeasurement:
    """Single drift measurement point - enhanced with pressure and health"""
    timestamp: float
    scup_value: float
    drift_delta: float  # Δd_i
    entropy_value: float
    resolved_coherence: float  # SCUP_i × Δd_i / Entropy_i
    drift_direction: str  # "increasing", "decreasing", "stable"
    confidence: float = 1.0
    
    # Enhanced measurements
    cognitive_pressure: Optional[CognitivePressureState] = None
    schema_health: Optional[SchemaHealthState] = None
    tracer_alerts: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class DriftForecast:
    """Predictive drift forecast - enhanced with pressure and health projections"""
    predicted_drift: float
    predicted_scup: float
    predicted_coherence: float
    predicted_pressure: float
    predicted_shi: float
    forecast_horizon: float  # Time horizon in seconds
    confidence: float
    risk_level: str  # "low", "moderate", "high", "critical"
    recommended_actions: List[str] = field(default_factory=list)
    pressure_interventions: List[str] = field(default_factory=list)
    health_interventions: List[str] = field(default_factory=list)

class SCUPDriftResolver:
    """
    SCUP Drift Resolver - Enhanced Semantic Coherence Mathematics
    
    Implements drift-weighted coherence tracking using the equation
    SCUP_i × Δd_i / Entropy_i enhanced with cognitive pressure engine
    P = B * σ² and Schema Health Index monitoring.
    """
    
    def __init__(self, history_size: int = 50):
        """Initialize the enhanced SCUP drift resolver"""
        
        self.history_size = history_size
        self.drift_history: deque = deque(maxlen=history_size)
        self.pressure_history: deque = deque(maxlen=history_size)
        self.health_history: deque = deque(maxlen=history_size)
        self.last_measurement: Optional[DriftMeasurement] = None
        
        # Integration with existing SCUP system
        self.scup_tracker = None
        if SCUP_SYSTEM_AVAILABLE:
            try:
                self.scup_tracker = SCUPTracker()
                logger.info("🧭 [DRIFT] Connected to existing SCUP tracker")
            except Exception as e:
                logger.warning(f"🧭 [DRIFT] SCUP tracker connection failed: {e}")
        
        # Drift resolution parameters
        self.ENTROPY_FLOOR = 0.01  # Prevent division by zero
        self.DRIFT_THRESHOLD = 0.1  # Minimum significant drift
        self.STABILITY_WINDOW = 5   # Measurements for stability assessment
        self.FORECAST_HORIZON = 10.0  # Default forecast time (seconds)
        
        # Cognitive Pressure Engine parameters
        self.PRESSURE_THRESHOLDS = {
            "low": 20.0,
            "moderate": 50.0,
            "high": 100.0,
            "critical": 200.0
        }
        self.BLOOM_MASS_WEIGHTS = {
            "active_memory": 1.0,
            "rebloom_queue": 1.5,
            "reflection_backlog": 2.0,
            "processing_load": 1.2
        }
        self.SIGIL_VELOCITY_FACTORS = {
            "recent_sigils": 1.0,
            "thought_rate": 0.8,
            "entropy_delta": 1.5,
            "mutation_rate": 1.3
        }
        
        # Schema Health Index (SHI) parameters
        self.SHI_WEIGHTS = {
            "vitality": 0.25,
            "memory_health": 0.25,
            "orbit_load": 0.20,
            "ash_availability": 0.15,
            "soft_edge_response": 0.15
        }
        self.SHI_THRESHOLDS = {
            "poor": 0.3,
            "fair": 0.5,
            "good": 0.7,
            "excellent": 0.85
        }
        
        # Adaptive learning parameters
        self.drift_sensitivity = 1.0
        self.coherence_weight = 1.0
        self.entropy_damping = 0.8
        self.pressure_sensitivity = 1.0
        self.health_weight = 0.3
        
        # Performance tracking
        self.resolution_count = 0
        self.forecast_count = 0
        self.pressure_calculations = 0
        self.health_assessments = 0
        self.prediction_accuracy = 0.0
        self.last_resolution_time = 0.0
        
        # Enhanced state tracking
        self.current_drift_state = DriftState.STABLE
        self.current_pressure_state: Optional[CognitivePressureState] = None
        self.current_health_state: Optional[SchemaHealthState] = None
        self.coherence_trend = 0.0
        self.drift_velocity = 0.0
        self.stability_score = 1.0
        
        # Tracer integration hooks
        self.tracer_callbacks: List[Callable] = []
        self.tracer_state: Dict[str, Any] = {}
        
        logger.info("🧭 [DRIFT] Enhanced SCUP Drift Resolver initialized")
        logger.info(f"🧭 [DRIFT] History size: {history_size}, SCUP integration: {SCUP_SYSTEM_AVAILABLE}")
        logger.info("🧭 [DRIFT] Cognitive Pressure Engine: ACTIVE")
        logger.info("🧭 [DRIFT] Schema Health Index: ACTIVE")
    
    def calculate_cognitive_pressure(self, state: Dict[str, Any]) -> CognitivePressureState:
        """
        Calculate cognitive pressure using P = B * σ²
        
        Args:
            state: DAWN cognitive state containing bloom and sigil metrics
            
        Returns:
            CognitivePressureState with pressure calculations
        """
        try:
            # Calculate Bloom Mass (B)
            active_memory = state.get('active_memory_count', 0) * self.BLOOM_MASS_WEIGHTS["active_memory"]
            rebloom_queue = state.get('rebloom_queue_size', 0) * self.BLOOM_MASS_WEIGHTS["rebloom_queue"]
            reflection_backlog = state.get('reflection_backlog', 0) * self.BLOOM_MASS_WEIGHTS["reflection_backlog"]
            processing_load = state.get('processing_load', 0) * self.BLOOM_MASS_WEIGHTS["processing_load"]
            
            bloom_mass = active_memory + rebloom_queue + reflection_backlog + processing_load
            
            # Calculate Sigil Velocity (σ)
            recent_sigils = state.get('recent_sigil_count', 0) * self.SIGIL_VELOCITY_FACTORS["recent_sigils"]
            thought_rate = state.get('thought_rate', 0) * self.SIGIL_VELOCITY_FACTORS["thought_rate"]
            entropy_delta = abs(state.get('entropy_delta', 0)) * self.SIGIL_VELOCITY_FACTORS["entropy_delta"]
            mutation_rate = state.get('sigil_mutation_rate', 0) * self.SIGIL_VELOCITY_FACTORS["mutation_rate"]
            
            sigil_velocity = recent_sigils + thought_rate + entropy_delta + mutation_rate
            
            # Apply cognitive pressure formula: P = B * σ²
            pressure_value = bloom_mass * (sigil_velocity ** 2) * self.pressure_sensitivity
            
            # Classify pressure level
            pressure_level = "low"
            for level, threshold in self.PRESSURE_THRESHOLDS.items():
                if pressure_value >= threshold:
                    pressure_level = level
            
            # Calculate pressure trend
            pressure_trend = 0.0
            if self.pressure_history:
                prev_pressure = self.pressure_history[-1].pressure_value
                pressure_trend = pressure_value - prev_pressure
            
            # Generate relief actions based on pressure level
            relief_actions = self._generate_pressure_relief_actions(pressure_value, pressure_level)
            
            pressure_state = CognitivePressureState(
                bloom_mass=bloom_mass,
                sigil_velocity=sigil_velocity,
                pressure_value=pressure_value,
                pressure_level=pressure_level,
                pressure_trend=pressure_trend,
                relief_actions=relief_actions
            )
            
            self.pressure_history.append(pressure_state)
            self.current_pressure_state = pressure_state
            self.pressure_calculations += 1
            
            logger.debug(f"🧭 [PRESSURE] P={pressure_value:.1f} (B={bloom_mass:.1f}, σ={sigil_velocity:.2f}) - {pressure_level}")
            
            return pressure_state
            
        except Exception as e:
            logger.error(f"🧭 [PRESSURE] Calculation error: {e}")
            return CognitivePressureState(0, 0, 0, "error", 0)
    
    def calculate_schema_health_index(self, state: Dict[str, Any]) -> SchemaHealthState:
        """
        Calculate Schema Health Index (SHI) from system vitals
        
        Args:
            state: DAWN cognitive state containing health metrics
            
        Returns:
            SchemaHealthState with health assessment
        """
        try:
            # Extract health components (0.0 to 1.0 scale)
            vitality = max(0.0, min(1.0, state.get('system_vitality', 0.5)))
            memory_health = max(0.0, min(1.0, state.get('memory_coherence', 0.5)))
            orbit_load = 1.0 - max(0.0, min(1.0, state.get('processing_orbit_load', 0.5)))  # Inverted - lower load = better
            ash_availability = max(0.0, min(1.0, state.get('cognitive_ash_level', 0.5)))
            soft_edge_response = max(0.0, min(1.0, state.get('soft_edge_responsiveness', 0.5)))
            
            # Calculate weighted SHI
            shi_value = (
                vitality * self.SHI_WEIGHTS["vitality"] +
                memory_health * self.SHI_WEIGHTS["memory_health"] +
                orbit_load * self.SHI_WEIGHTS["orbit_load"] +
                ash_availability * self.SHI_WEIGHTS["ash_availability"] +
                soft_edge_response * self.SHI_WEIGHTS["soft_edge_response"]
            )
            
            # Classify health level
            health_level = "poor"
            for level, threshold in self.SHI_THRESHOLDS.items():
                if shi_value >= threshold:
                    health_level = level
            
            # Generate health recommendations
            recommendations = self._generate_health_recommendations(
                vitality, memory_health, orbit_load, ash_availability, soft_edge_response, health_level
            )
            
            health_state = SchemaHealthState(
                vitality=vitality,
                memory_health=memory_health,
                orbit_load=orbit_load,
                ash_availability=ash_availability,
                soft_edge_response=soft_edge_response,
                shi_value=shi_value,
                health_level=health_level,
                recommendations=recommendations
            )
            
            self.health_history.append(health_state)
            self.current_health_state = health_state
            self.health_assessments += 1
            
            logger.debug(f"🧭 [HEALTH] SHI={shi_value:.3f} ({health_level}) - V:{vitality:.2f} M:{memory_health:.2f} O:{orbit_load:.2f}")
            
            return health_state
            
        except Exception as e:
            logger.error(f"🧭 [HEALTH] Assessment error: {e}")
            return SchemaHealthState(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, "error")
    
    def _generate_pressure_relief_actions(self, pressure_value: float, pressure_level: str) -> List[str]:
        """Generate pressure relief recommendations"""
        actions = []
        
        if pressure_level == "critical":
            actions.extend([
                "EMERGENCY: Halt non-essential processing",
                "Trigger Mr. Wolf stabilization protocol",
                "Suspend rebloom queue processing",
                "Reduce reflection depth",
                "Clear sigil mutation backlog"
            ])
        elif pressure_level == "high":
            actions.extend([
                "Reduce processing load",
                "Pause rebloom operations",
                "Decrease thought generation rate",
                "Consolidate active memories"
            ])
        elif pressure_level == "moderate":
            actions.extend([
                "Monitor processing carefully",
                "Optimize memory usage",
                "Consider reflection consolidation"
            ])
        
        return actions
    
    def _generate_health_recommendations(self, vitality: float, memory_health: float, 
                                       orbit_load: float, ash_availability: float, 
                                       soft_edge_response: float, health_level: str) -> List[str]:
        """Generate schema health improvement recommendations"""
        recommendations = []
        
        if health_level == "poor":
            recommendations.append("CRITICAL: Schema health intervention required")
            
        if vitality < 0.4:
            recommendations.append("Boost system vitality - reduce cognitive load")
        if memory_health < 0.4:
            recommendations.append("Memory consolidation needed - strengthen coherence")
        if orbit_load < 0.4:  # Remember orbit_load is inverted
            recommendations.append("Reduce processing orbit load - defer non-critical tasks")
        if ash_availability < 0.3:
            recommendations.append("Cognitive ash depletion - restore processing resources")
        if soft_edge_response < 0.4:
            recommendations.append("Improve soft edge responsiveness - enhance adaptability")
            
        if health_level in ["good", "excellent"]:
            recommendations.append("Enable expressive processing modes")
            recommendations.append("Consider increased mutation rates")
            
        return recommendations
    
    def resolve_drift_coherence(self, state: Dict[str, Any]) -> float:
        """
        Enhanced drift coherence resolution with pressure and health integration
        
        Args:
            state: DAWN cognitive state containing all metrics
        
        Returns:
            Resolved coherence value (enhanced with pressure/health modulation)
        """
        resolution_start = time.time()
        
        try:
            # Extract core SCUP values
            current_scup = state.get('scup', 0.5)
            current_entropy = max(self.ENTROPY_FLOOR, state.get('entropy', 0.5))
            current_drift = state.get('drift', 0.0)
            current_time = time.time()
            
            # Calculate drift delta (Δd_i)
            drift_delta = self._calculate_drift_delta(current_drift, current_time)
            
            # Calculate enhanced metrics
            pressure_state = self.calculate_cognitive_pressure(state)
            health_state = self.calculate_schema_health_index(state)
            
            # Apply core drift resolution formula: SCUP_i × Δd_i / Entropy_i
            if abs(drift_delta) < self.DRIFT_THRESHOLD:
                # Minimal drift - use direct SCUP coherence
                base_coherence = current_scup
            else:
                # Significant drift - apply full formula
                raw_resolution = (current_scup * abs(drift_delta)) / current_entropy
                scaled_resolution = raw_resolution * self.drift_sensitivity
                baseline_coherence = current_scup * self.coherence_weight
                base_coherence = (scaled_resolution * 0.7 + baseline_coherence * 0.3)
            
            # Apply pressure modulation
            pressure_factor = self._calculate_pressure_modulation(pressure_state)
            pressure_modulated_coherence = base_coherence * pressure_factor
            
            # Apply health modulation
            health_factor = self._calculate_health_modulation(health_state)
            final_coherence = pressure_modulated_coherence * health_factor
            
            # Bound the result
            resolved_coherence = max(0.0, min(1.0, final_coherence))
            
            # Determine drift direction
            drift_direction = self._classify_drift_direction(drift_delta)
            
            # Collect tracer alerts
            tracer_alerts = self._collect_tracer_alerts(state, pressure_state, health_state)
            
            # Create enhanced measurement record
            measurement = DriftMeasurement(
                timestamp=current_time,
                scup_value=current_scup,
                drift_delta=drift_delta,
                entropy_value=current_entropy,
                resolved_coherence=resolved_coherence,
                drift_direction=drift_direction,
                confidence=self._calculate_measurement_confidence(state),
                cognitive_pressure=pressure_state,
                schema_health=health_state,
                tracer_alerts=tracer_alerts
            )
            
            # Update history and state
            self.drift_history.append(measurement)
            self.last_measurement = measurement
            self._update_enhanced_drift_state()
            
            # Update performance metrics
            self.resolution_count += 1
            self.last_resolution_time = time.time() - resolution_start
            
            # Integration with existing SCUP system
            if self.scup_tracker:
                self._integrate_with_scup_tracker(measurement, state)
            
            # Execute tracer callbacks
            self._execute_tracer_callbacks(measurement)
            
            logger.debug(f"🧭 [DRIFT] Enhanced coherence: {resolved_coherence:.3f} (base={base_coherence:.2f}, P-mod={pressure_factor:.2f}, H-mod={health_factor:.2f})")
            
            return resolved_coherence
            
        except Exception as e:
            logger.error(f"🧭 [DRIFT] Enhanced resolution error: {e}")
            return state.get('scup', 0.5)  # Fallback to raw SCUP
    
    def _calculate_pressure_modulation(self, pressure_state: CognitivePressureState) -> float:
        """Calculate coherence modulation based on cognitive pressure"""
        if pressure_state.pressure_level == "critical":
            return 0.5  # Severely reduce coherence under critical pressure
        elif pressure_state.pressure_level == "high":
            return 0.7  # Moderate reduction
        elif pressure_state.pressure_level == "moderate":
            return 0.9  # Slight reduction
        else:
            return 1.0  # No reduction for low pressure
    
    def _calculate_health_modulation(self, health_state: SchemaHealthState) -> float:
        """Calculate coherence modulation based on schema health"""
        # Use SHI directly as a coherence modulation factor
        # Healthy schemas support better coherence
        base_factor = 0.7 + (health_state.shi_value * 0.3)  # Range: 0.7-1.0
        return max(0.5, min(1.0, base_factor))
    
    def _collect_tracer_alerts(self, state: Dict[str, Any], pressure_state: CognitivePressureState, 
                              health_state: SchemaHealthState) -> List[Dict[str, Any]]:
        """Collect alerts from tracer ecosystem"""
        alerts = []
        
        # Pressure-based tracer alerts
        if pressure_state.pressure_level in ["high", "critical"]:
            alerts.append({
                "tracer": "pressure_monitor",
                "type": "pressure_alert",
                "level": pressure_state.pressure_level,
                "message": f"Cognitive pressure {pressure_state.pressure_level}: {pressure_state.pressure_value:.1f}",
                "actions": pressure_state.relief_actions
            })
        
        # Health-based tracer alerts
        if health_state.health_level in ["poor", "fair"]:
            alerts.append({
                "tracer": "health_monitor",
                "type": "health_alert",
                "level": health_state.health_level,
                "message": f"Schema health {health_state.health_level}: SHI={health_state.shi_value:.3f}",
                "recommendations": health_state.recommendations
            })
        
        # Drift-based alerts
        if self.current_drift_state in [DriftState.CHAOTIC, DriftState.PRESSURIZED, DriftState.UNHEALTHY]:
            alerts.append({
                "tracer": "drift_monitor",
                "type": "drift_alert",
                "level": "warning",
                "message": f"Drift state: {self.current_drift_state.value}",
                "stability_score": self.stability_score
            })
        
        return alerts
    
    def _update_enhanced_drift_state(self):
        """Update drift state classification with pressure and health considerations"""
        
        if len(self.drift_history) < 3:
            self.current_drift_state = DriftState.STABLE
            return
        
        # Analyze recent patterns
        recent_measurements = list(self.drift_history)[-5:]
        drift_values = [m.drift_delta for m in recent_measurements]
        coherence_values = [m.resolved_coherence for m in recent_measurements]
        
        # Calculate basic drift statistics
        drift_variance = np.var(drift_values) if len(drift_values) > 1 else 0.0
        coherence_trend = self._calculate_trend(coherence_values)
        drift_magnitude = np.mean([abs(d) for d in drift_values])
        
        # Update instance variables
        self.coherence_trend = coherence_trend
        self.drift_velocity = drift_magnitude
        self.stability_score = 1.0 - drift_variance
        
        # Enhanced state classification with pressure and health
        pressure_critical = (self.current_pressure_state and 
                           self.current_pressure_state.pressure_level in ["high", "critical"])
        health_poor = (self.current_health_state and 
                      self.current_health_state.health_level in ["poor", "fair"])
        
        # Priority state classifications
        if pressure_critical:
            self.current_drift_state = DriftState.PRESSURIZED
        elif health_poor:
            self.current_drift_state = DriftState.UNHEALTHY
        elif drift_variance > 0.05:
            self.current_drift_state = DriftState.CHAOTIC
        elif drift_variance < 0.01 and drift_magnitude < 0.05:
            self.current_drift_state = DriftState.STABLE
        elif abs(coherence_trend) > 0.1:
            if coherence_trend > 0:
                self.current_drift_state = DriftState.CONVERGING
            else:
                self.current_drift_state = DriftState.TRENDING
        else:
            self.current_drift_state = DriftState.OSCILLATING
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend (slope) of a series of values"""
        
        if len(values) < 2:
            return 0.0
        
        n = len(values)
        x = list(range(n))
        y = values
        
        # Simple linear regression
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def _calculate_trend_consistency(self, measurements: List[DriftMeasurement]) -> float:
        """Calculate how consistent the trend has been (higher = more predictable)"""
        
        if len(measurements) < 3:
            return 0.5
        
        # Calculate trend segments
        segment_trends = []
        for i in range(2, len(measurements)):
            segment_values = [m.resolved_coherence for m in measurements[i-2:i+1]]
            segment_trend = self._calculate_trend(segment_values)
            segment_trends.append(segment_trend)
        
        # Measure consistency (low variance = high consistency)
        if len(segment_trends) > 1:
            trend_variance = np.var(segment_trends)
            consistency = 1.0 / (1.0 + trend_variance * 10)  # Normalized inverse variance
        else:
            consistency = 0.5
        
        return max(0.0, min(1.0, consistency))
    
    def _assess_forecast_risk(self, predicted_drift: float, predicted_scup: float, 
                                         predicted_coherence: float, risk_level: str) -> List[str]:
        """Generate actionable recommendations based on forecast"""
        
        recommendations = []
        
        if risk_level in ["high", "critical"]:
            recommendations.append("Increase reflection frequency")
            recommendations.append("Trigger stabilization protocols")
        
        if abs(predicted_drift) > 0.2:
            recommendations.append("Monitor semantic consistency")
            recommendations.append("Consider drift intervention")
        
        if predicted_scup < 0.4:
            recommendations.append("Reduce cognitive pressure")
            recommendations.append("Enhance coherence support")
        
        if predicted_coherence < 0.5:
            recommendations.append("Strengthen memory coherence")
            recommendations.append("Activate coherence recovery")
        
        if not recommendations:
            recommendations.append("Continue normal operation")
        
        return recommendations
    
    def register_tracer_callback(self, callback: Callable[[DriftMeasurement], None]):
        """Register a callback function for tracer integration"""
        self.tracer_callbacks.append(callback)
        logger.info(f"🧭 [TRACER] Registered callback: {callback.__name__ if hasattr(callback, '__name__') else 'anonymous'}")
    
    def _execute_tracer_callbacks(self, measurement: DriftMeasurement):
        """Execute all registered tracer callbacks"""
        for callback in self.tracer_callbacks:
            try:
                callback(measurement)
            except Exception as e:
                logger.warning(f"🧭 [TRACER] Callback execution failed: {e}")

    def _calculate_drift_delta(self, current_drift: float, current_time: float) -> float:
        """Calculate drift delta (Δd_i) from previous measurement"""
        
        if not self.drift_history:
            return 0.0  # No previous measurement for comparison
        
        # Get most recent measurement
        prev_measurement = self.drift_history[-1]
        time_delta = current_time - prev_measurement.timestamp
        
        if time_delta <= 0:
            return 0.0
        
        # Calculate drift change rate
        drift_change = current_drift - prev_measurement.drift_delta
        drift_delta = drift_change / time_delta
        
        # Apply temporal smoothing to reduce noise
        if len(self.drift_history) >= 2:
            prev_delta = prev_measurement.drift_delta
            smoothed_delta = drift_delta * 0.7 + prev_delta * 0.3
            return smoothed_delta
        
        return drift_delta
    
    def _classify_drift_direction(self, drift_delta: float) -> str:
        """Classify drift direction based on delta value"""
        
        if abs(drift_delta) < self.DRIFT_THRESHOLD:
            return "stable"
        elif drift_delta > 0:
            return "increasing"
        else:
            return "decreasing"
    
    def _calculate_measurement_confidence(self, state: Dict[str, Any]) -> float:
        """Calculate confidence in the measurement based on system state"""
        
        # Base confidence
        confidence = 1.0
        
        # Reduce confidence during high entropy
        entropy = state.get('entropy', 0.5)
        entropy_penalty = entropy * 0.3
        confidence -= entropy_penalty
        
        # Reduce confidence if SCUP is very low (unreliable measurements)
        scup = state.get('scup', 0.5)
        if scup < 0.3:
            confidence -= (0.3 - scup) * 0.5
        
        # Increase confidence with more history
        history_bonus = min(0.2, len(self.drift_history) / self.history_size * 0.2)
        confidence += history_bonus
        
        return max(0.1, min(1.0, confidence))
    
    def _integrate_with_scup_tracker(self, measurement: DriftMeasurement, state: Dict[str, Any]):
        """Integrate drift resolution with existing SCUP tracking system"""
        
        try:
            # Update SCUP tracker with drift-resolved coherence
            if hasattr(self.scup_tracker, 'update_coherence'):
                self.scup_tracker.update_coherence(measurement.resolved_coherence)
            
            # Provide enhanced drift information to SCUP system
            if hasattr(self.scup_tracker, 'update_drift_info'):
                drift_info = {
                    "drift_delta": measurement.drift_delta,
                    "drift_direction": measurement.drift_direction,
                    "drift_state": self.current_drift_state.value,
                    "stability_score": self.stability_score,
                    # Enhanced integration data
                    "cognitive_pressure": {
                        "pressure_value": measurement.cognitive_pressure.pressure_value if measurement.cognitive_pressure else 0,
                        "pressure_level": measurement.cognitive_pressure.pressure_level if measurement.cognitive_pressure else "unknown"
                    },
                    "schema_health": {
                        "shi_value": measurement.schema_health.shi_value if measurement.schema_health else 0.5,
                        "health_level": measurement.schema_health.health_level if measurement.schema_health else "unknown"
                    }
                }
                self.scup_tracker.update_drift_info(drift_info)
                
        except Exception as e:
            logger.warning(f"🧭 [DRIFT] SCUP integration failed: {e}")

    def _generate_forecast_recommendations(self, predicted_drift: float, predicted_scup: float, 
                                         predicted_coherence: float, risk_level: str) -> List[str]:
        """Generate actionable recommendations based on forecast"""
        
        recommendations = []
        
        if risk_level in ["high", "critical"]:
            recommendations.append("Increase reflection frequency")
            recommendations.append("Trigger stabilization protocols")
        
        if abs(predicted_drift) > 0.2:
            recommendations.append("Monitor semantic consistency")
            recommendations.append("Consider drift intervention")
        
        if predicted_scup < 0.4:
            recommendations.append("Reduce cognitive pressure")
            recommendations.append("Enhance coherence support")
        
        if predicted_coherence < 0.5:
            recommendations.append("Strengthen memory coherence")
            recommendations.append("Activate coherence recovery")
        
        if not recommendations:
            recommendations.append("Continue normal operation")
        
        return recommendations
    
    def forecast_drift(self, horizon: float = None) -> DriftForecast:
        """
        Enhanced predictive drift forecast with pressure and health projections
        
        Args:
            horizon: Forecast time horizon in seconds (default: self.FORECAST_HORIZON)
            
        Returns:
            Enhanced DriftForecast with pressure and health predictions
        """
        
        if horizon is None:
            horizon = self.FORECAST_HORIZON
        
        try:
            if len(self.drift_history) < 3:
                # Insufficient data for meaningful forecast
                return DriftForecast(
                    predicted_drift=0.0,
                    predicted_scup=0.5,
                    predicted_coherence=0.5,
                    predicted_pressure=0.0,
                    predicted_shi=0.5,
                    forecast_horizon=horizon,
                    confidence=0.1,
                    risk_level="unknown",
                    recommended_actions=["Collect more drift data"],
                    pressure_interventions=[],
                    health_interventions=[]
                )
            
            # Extract historical trends
            recent_measurements = list(self.drift_history)[-10:]
            drift_deltas = [m.drift_delta for m in recent_measurements]
            scup_values = [m.scup_value for m in recent_measurements]
            coherence_values = [m.resolved_coherence for m in recent_measurements]
            
            # Extract pressure and health trends
            pressure_values = [m.cognitive_pressure.pressure_value for m in recent_measurements 
                             if m.cognitive_pressure]
            shi_values = [m.schema_health.shi_value for m in recent_measurements 
                         if m.schema_health]
            
            # Calculate trend projections
            drift_trend = self._calculate_trend(drift_deltas)
            scup_trend = self._calculate_trend(scup_values)
            coherence_trend = self._calculate_trend(coherence_values)
            pressure_trend = self._calculate_trend(pressure_values) if pressure_values else 0.0
            shi_trend = self._calculate_trend(shi_values) if shi_values else 0.0
            
            # Project forward
            current_drift = drift_deltas[-1] if drift_deltas else 0.0
            current_scup = scup_values[-1] if scup_values else 0.5
            current_coherence = coherence_values[-1] if coherence_values else 0.5
            current_pressure = pressure_values[-1] if pressure_values else 0.0
            current_shi = shi_values[-1] if shi_values else 0.5
            
            # Enhanced projections
            predicted_drift = current_drift + (drift_trend * horizon)
            predicted_scup = max(0.0, min(1.0, current_scup + (scup_trend * horizon)))
            predicted_coherence = max(0.0, min(1.0, current_coherence + (coherence_trend * horizon)))
            predicted_pressure = max(0.0, current_pressure + (pressure_trend * horizon))
            predicted_shi = max(0.0, min(1.0, current_shi + (shi_trend * horizon)))
            
            # Calculate enhanced forecast confidence
            trend_consistency = self._calculate_trend_consistency(recent_measurements)
            forecast_confidence = min(1.0, trend_consistency * 0.8 + 0.2)
            
            # Enhanced risk assessment
            risk_level = self._assess_enhanced_forecast_risk(
                predicted_drift, predicted_scup, predicted_coherence, 
                predicted_pressure, predicted_shi
            )
            
            # Generate enhanced recommendations
            recommended_actions = self._generate_forecast_recommendations(
                predicted_drift, predicted_scup, predicted_coherence, risk_level
            )
            
            pressure_interventions = self._generate_pressure_interventions(predicted_pressure)
            health_interventions = self._generate_health_interventions(predicted_shi)
            
            forecast = DriftForecast(
                predicted_drift=predicted_drift,
                predicted_scup=predicted_scup,
                predicted_coherence=predicted_coherence,
                predicted_pressure=predicted_pressure,
                predicted_shi=predicted_shi,
                forecast_horizon=horizon,
                confidence=forecast_confidence,
                risk_level=risk_level,
                recommended_actions=recommended_actions,
                pressure_interventions=pressure_interventions,
                health_interventions=health_interventions
            )
            
            self.forecast_count += 1
            
            logger.debug(f"🧭 [FORECAST] Enhanced: drift={predicted_drift:.3f}, P={predicted_pressure:.1f}, SHI={predicted_shi:.3f}, risk={risk_level}")
            
            return forecast
            
        except Exception as e:
            logger.error(f"🧭 [FORECAST] Enhanced forecast error: {e}")
            return DriftForecast(
                predicted_drift=0.0,
                predicted_scup=0.5,
                predicted_coherence=0.5,
                predicted_pressure=0.0,
                predicted_shi=0.5,
                forecast_horizon=horizon,
                confidence=0.1,
                risk_level="error",
                recommended_actions=[],
                pressure_interventions=[],
                health_interventions=[]
            )
    
    def _assess_enhanced_forecast_risk(self, predicted_drift: float, predicted_scup: float, 
                                     predicted_coherence: float, predicted_pressure: float, 
                                     predicted_shi: float) -> str:
        """Enhanced risk assessment including pressure and health factors"""
        
        risk_factors = 0
        
        # Existing drift/SCUP/coherence risk factors
        if abs(predicted_drift) > 0.3:
            risk_factors += 2
        elif abs(predicted_drift) > 0.1:
            risk_factors += 1
        
        if predicted_scup < 0.3:
            risk_factors += 2
        elif predicted_scup < 0.5:
            risk_factors += 1
        
        if predicted_coherence < 0.4:
            risk_factors += 2
        elif predicted_coherence < 0.6:
            risk_factors += 1
        
        # Enhanced pressure risk factors
        if predicted_pressure > self.PRESSURE_THRESHOLDS["critical"]:
            risk_factors += 3
        elif predicted_pressure > self.PRESSURE_THRESHOLDS["high"]:
            risk_factors += 2
        elif predicted_pressure > self.PRESSURE_THRESHOLDS["moderate"]:
            risk_factors += 1
        
        # Enhanced health risk factors
        if predicted_shi < 0.3:
            risk_factors += 2
        elif predicted_shi < 0.5:
            risk_factors += 1
        
        # Classify enhanced risk level
        if risk_factors >= 7:
            return "critical"
        elif risk_factors >= 5:
            return "high"
        elif risk_factors >= 2:
            return "moderate"
        else:
            return "low"
    
    def _generate_pressure_interventions(self, predicted_pressure: float) -> List[str]:
        """Generate pressure-specific interventions for forecast"""
        interventions = []
        
        if predicted_pressure > self.PRESSURE_THRESHOLDS["critical"]:
            interventions.extend([
                "Prepare emergency pressure relief protocols",
                "Schedule Mr. Wolf activation",
                "Pre-emptively reduce processing load"
            ])
        elif predicted_pressure > self.PRESSURE_THRESHOLDS["high"]:
            interventions.extend([
                "Implement pressure monitoring",
                "Prepare load reduction strategies",
                "Monitor bloom mass accumulation"
            ])
        elif predicted_pressure > self.PRESSURE_THRESHOLDS["moderate"]:
            interventions.append("Monitor pressure trends closely")
        
        return interventions
    
    def _generate_health_interventions(self, predicted_shi: float) -> List[str]:
        """Generate health-specific interventions for forecast"""
        interventions = []
        
        if predicted_shi < 0.3:
            interventions.extend([
                "Critical schema health intervention required",
                "Boost system vitality",
                "Emergency memory consolidation",
                "Restore cognitive ash reserves"
            ])
        elif predicted_shi < 0.5:
            interventions.extend([
                "Schema health improvement needed",
                "Monitor memory coherence",
                "Optimize processing orbits"
            ])
        elif predicted_shi < 0.7:
            interventions.append("Maintain current health protocols")
        
        return interventions
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get enhanced current drift resolver state"""
        
        latest_measurement = self.last_measurement
        
        return {
            "drift_state": self.current_drift_state.value,
            "stability_score": self.stability_score,
            "coherence_trend": self.coherence_trend,
            "drift_velocity": self.drift_velocity,
            
            # Enhanced state information
            "cognitive_pressure": {
                "current_pressure": self.current_pressure_state.pressure_value if self.current_pressure_state else 0,
                "pressure_level": self.current_pressure_state.pressure_level if self.current_pressure_state else "unknown",
                "bloom_mass": self.current_pressure_state.bloom_mass if self.current_pressure_state else 0,
                "sigil_velocity": self.current_pressure_state.sigil_velocity if self.current_pressure_state else 0
            } if self.current_pressure_state else None,
            
            "schema_health": {
                "shi_value": self.current_health_state.shi_value if self.current_health_state else 0.5,
                "health_level": self.current_health_state.health_level if self.current_health_state else "unknown",
                "vitality": self.current_health_state.vitality if self.current_health_state else 0.5,
                "memory_health": self.current_health_state.memory_health if self.current_health_state else 0.5
            } if self.current_health_state else None,
            
            "latest_measurement": {
                "timestamp": latest_measurement.timestamp if latest_measurement else 0,
                "scup_value": latest_measurement.scup_value if latest_measurement else 0,
                "drift_delta": latest_measurement.drift_delta if latest_measurement else 0,
                "entropy_value": latest_measurement.entropy_value if latest_measurement else 0,
                "resolved_coherence": latest_measurement.resolved_coherence if latest_measurement else 0,
                "confidence": latest_measurement.confidence if latest_measurement else 0,
                "tracer_alerts": latest_measurement.tracer_alerts if latest_measurement else []
            } if latest_measurement else None,
            
            "history_length": len(self.drift_history),
            "performance": {
                "resolution_count": self.resolution_count,
                "forecast_count": self.forecast_count,
                "pressure_calculations": self.pressure_calculations,
                "health_assessments": self.health_assessments,
                "last_resolution_time_ms": self.last_resolution_time * 1000,
                "scup_integration_active": self.scup_tracker is not None,
                "tracer_callbacks_registered": len(self.tracer_callbacks)
            }
        }
    
    def get_drift_modulation(self) -> Dict[str, float]:
        """Get enhanced drift-based modulation parameters for other systems"""
        
        if not self.last_measurement:
            return {
                "coherence_boost": 1.0, 
                "stability_factor": 1.0, 
                "drift_compensation": 0.0,
                "pressure_modulation": 1.0,
                "health_modulation": 1.0
            }
        
        drift_magnitude = abs(self.last_measurement.drift_delta)
        coherence = self.last_measurement.resolved_coherence
        
        # Base modulation factors
        coherence_boost = 1.0 + (1.0 - coherence) * 0.5
        stability_factor = self.stability_score
        drift_compensation = min(0.5, drift_magnitude * 2.0)
        
        # Enhanced pressure modulation
        pressure_modulation = 1.0
        if self.current_pressure_state:
            if self.current_pressure_state.pressure_level == "critical":
                pressure_modulation = 0.3
            elif self.current_pressure_state.pressure_level == "high":
                pressure_modulation = 0.6
            elif self.current_pressure_state.pressure_level == "moderate":
                pressure_modulation = 0.8
        
        # Enhanced health modulation
        health_modulation = 1.0
        if self.current_health_state:
            health_modulation = 0.5 + (self.current_health_state.shi_value * 0.5)
        
        return {
            "coherence_boost": coherence_boost,
            "stability_factor": stability_factor,
            "drift_compensation": drift_compensation,
            "coherence_priority": 1.0 - coherence,
            "pressure_modulation": pressure_modulation,
            "health_modulation": health_modulation,
            "system_readiness": min(pressure_modulation, health_modulation)  # Overall system readiness
        }


# Global drift resolver instance
_global_drift_resolver: Optional[SCUPDriftResolver] = None

def get_scup_drift_resolver() -> SCUPDriftResolver:
    """Get global SCUP drift resolver instance"""
    global _global_drift_resolver
    if _global_drift_resolver is None:
        _global_drift_resolver = SCUPDriftResolver()
    return _global_drift_resolver

def resolve_drift_coherence(state: Dict[str, Any]) -> float:
    """Convenience function to resolve drift coherence for a state"""
    resolver = get_scup_drift_resolver()
    return resolver.resolve_drift_coherence(state)

def forecast_cognitive_drift(horizon: float = 10.0) -> DriftForecast:
    """Convenience function to generate drift forecast"""
    resolver = get_scup_drift_resolver()
    return resolver.forecast_drift(horizon)

# Export key classes and functions
__all__ = [
    'SCUPDriftResolver',
    'DriftMeasurement',
    'DriftForecast',
    'DriftState',
    'get_scup_drift_resolver',
    'resolve_drift_coherence',
    'forecast_cognitive_drift'
] 