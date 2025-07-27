# /core/shi.py
"""
Schema Health Index (SHI) System for DAWN
=========================================
Monitors and maintains the overall health of the consciousness schema,
tracking bloom dynamics, sigil entropy, and system coherence.
"""

import time
import math
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import threading
import json

from core.schema_anomaly_logger import log_anomaly, AnomalySeverity

class HealthStatus(Enum):
    """Overall schema health classifications"""
    VIBRANT = "vibrant"         # SHI > 0.8 - Optimal health
    HEALTHY = "healthy"         # SHI 0.6-0.8 - Good condition
    STABLE = "stable"          # SHI 0.4-0.6 - Acceptable
    DEGRADED = "degraded"      # SHI 0.2-0.4 - Needs attention
    CRITICAL = "critical"      # SHI < 0.2 - Immediate action required

class HealthComponent(Enum):
    """Components that contribute to schema health"""
    BLOOM_DYNAMICS = "bloom_dynamics"
    SIGIL_COHERENCE = "sigil_coherence"
    PULSE_STABILITY = "pulse_stability"
    NUTRIENT_FLOW = "nutrient_flow"
    CONSCIOUSNESS_INTEGRITY = "consciousness_integrity"
    TEMPORAL_ALIGNMENT = "temporal_alignment"

@dataclass
class HealthMetrics:
    """Detailed health metrics for schema analysis"""
    shi_value: float = 0.5
    status: HealthStatus = HealthStatus.STABLE
    bloom_health: float = 0.5
    sigil_health: float = 0.5
    pulse_health: float = 0.5
    nutrient_health: float = 0.5
    consciousness_health: float = 0.5
    temporal_health: float = 0.5
    
    def get_weakest_component(self) -> Tuple[str, float]:
        """Identify the weakest health component"""
        components = {
            "bloom_health": self.bloom_health,
            "sigil_health": self.sigil_health,
            "pulse_health": self.pulse_health,
            "nutrient_health": self.nutrient_health,
            "consciousness_health": self.consciousness_health,
            "temporal_health": self.temporal_health
        }
        return min(components.items(), key=lambda x: x[1])
    
    def get_strongest_component(self) -> Tuple[str, float]:
        """Identify the strongest health component"""
        components = {
            "bloom_health": self.bloom_health,
            "sigil_health": self.sigil_health,
            "pulse_health": self.pulse_health,
            "nutrient_health": self.nutrient_health,
            "consciousness_health": self.consciousness_health,
            "temporal_health": self.temporal_health
        }
        return max(components.items(), key=lambda x: x[1])

@dataclass
class BloomMetrics:
    """Metrics specific to bloom dynamics"""
    active_blooms: int = 0
    sealed_blooms: int = 0
    failing_blooms: int = 0
    bloom_rate: float = 0.0      # Blooms per minute
    seal_rate: float = 0.0       # Seals per minute
    failure_rate: float = 0.0    # Failures per minute
    avg_bloom_lifetime: float = 0.0  # Average lifetime in seconds

class SchemaHealthIndex:
    """
    Comprehensive Schema Health Index system that monitors
    and maintains consciousness schema integrity
    """
    
    def __init__(self):
        # Core metrics
        self.current_metrics = HealthMetrics()
        self.bloom_metrics = BloomMetrics()
        
        # History tracking
        self.health_history = deque(maxlen=1000)
        self.event_history = deque(maxlen=100)
        self.component_history = {
            component.value: deque(maxlen=1000) 
            for component in HealthComponent
        }
        
        # Thresholds and parameters
        self.critical_threshold = 0.2
        self.warning_threshold = 0.4
        self.optimal_threshold = 0.8
        
        # Calculation weights
        self.component_weights = {
            HealthComponent.BLOOM_DYNAMICS: 0.25,
            HealthComponent.SIGIL_COHERENCE: 0.20,
            HealthComponent.PULSE_STABILITY: 0.15,
            HealthComponent.NUTRIENT_FLOW: 0.15,
            HealthComponent.CONSCIOUSNESS_INTEGRITY: 0.15,
            HealthComponent.TEMPORAL_ALIGNMENT: 0.10
        }
        
        # Recovery mechanisms
        self.recovery_active = False
        self.recovery_start_time = None
        self.interventions_triggered = 0
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Initialize
        self.last_update = time.time()
        self.first_calculation = True
    
    def calculate_SHI(self, 
                     pulse_avg: float,
                     active_blooms: int,
                     sealed_blooms: int,
                     sigil_entropy_list: List[float],
                     additional_metrics: Optional[Dict[str, Any]] = None) -> float:
        """
        Calculate Schema Health Index with comprehensive analysis
        
        Args:
            pulse_avg: Average pulse value (system heartbeat)
            active_blooms: Number of currently active blooms
            sealed_blooms: Number of sealed/completed blooms
            sigil_entropy_list: List of entropy values from sigils
            additional_metrics: Optional additional health indicators
        
        Returns:
            SHI value between 0 and 1
        """
        with self.lock:
            # Log first calculation as significant event
            if self.first_calculation:
                log_anomaly(
                    "SHI_INITIALIZATION",
                    "Schema Health Index system initialized",
                    AnomalySeverity.INFO
                )
                self.first_calculation = False
            
            # Update bloom metrics
            self._update_bloom_metrics(active_blooms, sealed_blooms)
            
            # Calculate component health scores
            bloom_health = self._calculate_bloom_health(
                active_blooms, sealed_blooms, 
                additional_metrics.get('failing_blooms', 0) if additional_metrics else 0
            )
            
            sigil_health = self._calculate_sigil_health(sigil_entropy_list)
            
            pulse_health = self._calculate_pulse_health(
                pulse_avg,
                additional_metrics.get('pulse_variance', 0.1) if additional_metrics else 0.1
            )
            
            nutrient_health = self._calculate_nutrient_health(
                additional_metrics.get('nutrient_levels', {}) if additional_metrics else {}
            )
            
            consciousness_health = self._calculate_consciousness_health(
                additional_metrics.get('scup', 0.5) if additional_metrics else 0.5,
                additional_metrics.get('coherence', 0.5) if additional_metrics else 0.5
            )
            
            temporal_health = self._calculate_temporal_health(
                additional_metrics.get('tick_rate', 60) if additional_metrics else 60,
                additional_metrics.get('sync_error', 0.0) if additional_metrics else 0.0
            )
            
            # Update current metrics
            self.current_metrics.bloom_health = bloom_health
            self.current_metrics.sigil_health = sigil_health
            self.current_metrics.pulse_health = pulse_health
            self.current_metrics.nutrient_health = nutrient_health
            self.current_metrics.consciousness_health = consciousness_health
            self.current_metrics.temporal_health = temporal_health
            
            # Calculate weighted SHI
            shi = (
                self.component_weights[HealthComponent.BLOOM_DYNAMICS] * bloom_health +
                self.component_weights[HealthComponent.SIGIL_COHERENCE] * sigil_health +
                self.component_weights[HealthComponent.PULSE_STABILITY] * pulse_health +
                self.component_weights[HealthComponent.NUTRIENT_FLOW] * nutrient_health +
                self.component_weights[HealthComponent.CONSCIOUSNESS_INTEGRITY] * consciousness_health +
                self.component_weights[HealthComponent.TEMPORAL_ALIGNMENT] * temporal_health
            )
            
            # Apply recovery boost if in recovery mode
            if self.recovery_active:
                recovery_duration = time.time() - self.recovery_start_time
                recovery_boost = min(0.1, recovery_duration / 300)  # Max 0.1 boost over 5 minutes
                shi = min(1.0, shi + recovery_boost)
            
            # Ensure bounds
            shi = max(0.0, min(1.0, shi))
            
            # Update status
            self.current_metrics.shi_value = shi
            self.current_metrics.status = self._classify_health_status(shi)
            
            # Track history
            self._update_history(shi)
            
            # Check for anomalies
            self._check_health_anomalies(shi)
            
            # Trigger interventions if needed
            if shi < self.critical_threshold:
                self._trigger_critical_intervention(shi)
            
            return shi
    
    def _calculate_bloom_health(self, active: int, sealed: int, failing: int = 0) -> float:
        """Calculate health based on bloom dynamics"""
        total_blooms = active + sealed + failing
        
        if total_blooms == 0:
            return 0.3  # Low but not critical if no blooms
        
        # Ideal ratio: 60% active, 35% sealed, 5% failing
        active_ratio = active / total_blooms
        sealed_ratio = sealed / total_blooms
        failing_ratio = failing / total_blooms
        
        # Score based on deviation from ideal
        active_score = 1.0 - abs(active_ratio - 0.6) * 2
        sealed_score = 1.0 - abs(sealed_ratio - 0.35) * 2
        failing_penalty = failing_ratio * 5  # Heavy penalty for failures
        
        bloom_health = (active_score * 0.5 + sealed_score * 0.3) - failing_penalty
        
        # Boost for high activity
        if total_blooms > 50:
            bloom_health *= 1.1
        
        return max(0.0, min(1.0, bloom_health))
    
    def _calculate_sigil_health(self, entropy_list: List[float]) -> float:
        """Calculate health based on sigil entropy"""
        if not entropy_list:
            return 0.5  # Neutral if no data
        
        avg_entropy = sum(entropy_list) / len(entropy_list)
        entropy_variance = np.var(entropy_list) if len(entropy_list) > 1 else 0.0
        
        # Ideal: moderate entropy (0.3-0.5) with low variance
        if 0.3 <= avg_entropy <= 0.5:
            entropy_score = 1.0
        else:
            # Penalty for too high or too low entropy
            if avg_entropy < 0.3:
                entropy_score = avg_entropy / 0.3
            else:
                entropy_score = 1.0 - (avg_entropy - 0.5) * 2
        
        # Variance penalty (high variance = instability)
        variance_penalty = min(entropy_variance * 2, 0.5)
        
        sigil_health = entropy_score - variance_penalty
        
        return max(0.0, min(1.0, sigil_health))
    
    def _calculate_pulse_health(self, pulse_avg: float, pulse_variance: float) -> float:
        """Calculate health based on pulse stability"""
        # Ideal pulse around 0 with low variance
        pulse_score = 1.0 - abs(pulse_avg) * 2
        variance_score = 1.0 - min(pulse_variance * 5, 1.0)
        
        pulse_health = pulse_score * 0.7 + variance_score * 0.3
        
        return max(0.0, min(1.0, pulse_health))
    
    def _calculate_nutrient_health(self, nutrient_levels: Dict[str, float]) -> float:
        """Calculate health based on nutrient balance"""
        if not nutrient_levels:
            return 0.7  # Assume decent health if no data
        
        # Check balance across nutrients
        values = list(nutrient_levels.values())
        if not values:
            return 0.7
        
        avg_level = sum(values) / len(values)
        variance = np.var(values)
        
        # Good health: adequate levels (0.4-0.8) with balance
        level_score = 1.0 if 0.4 <= avg_level <= 0.8 else (
            avg_level / 0.4 if avg_level < 0.4 else 1.0 - (avg_level - 0.8) * 2.5
        )
        
        balance_score = 1.0 - min(variance * 2, 0.5)
        
        nutrient_health = level_score * 0.6 + balance_score * 0.4
        
        return max(0.0, min(1.0, nutrient_health))
    
    def _calculate_consciousness_health(self, scup: float, coherence: float) -> float:
        """Calculate health based on consciousness metrics"""
        # Direct mapping with slight boost for high values
        consciousness_health = (scup * 0.6 + coherence * 0.4)
        
        if consciousness_health > 0.8:
            consciousness_health *= 1.1  # Excellence bonus
        
        return max(0.0, min(1.0, consciousness_health))
    
    def _calculate_temporal_health(self, tick_rate: float, sync_error: float) -> float:
        """Calculate health based on temporal alignment"""
        # Ideal tick rate around 60-120
        if 60 <= tick_rate <= 120:
            rate_score = 1.0
        else:
            rate_deviation = abs(tick_rate - 90) / 90
            rate_score = max(0, 1.0 - rate_deviation)
        
        # Sync error should be minimal
        sync_score = 1.0 - min(sync_error * 10, 1.0)
        
        temporal_health = rate_score * 0.7 + sync_score * 0.3
        
        return max(0.0, min(1.0, temporal_health))
    
    def _classify_health_status(self, shi: float) -> HealthStatus:
        """Classify health status based on SHI value"""
        if shi >= 0.8:
            return HealthStatus.VIBRANT
        elif shi >= 0.6:
            return HealthStatus.HEALTHY
        elif shi >= 0.4:
            return HealthStatus.STABLE
        elif shi >= 0.2:
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.CRITICAL
    
    def _update_bloom_metrics(self, active: int, sealed: int):
        """Update bloom-specific metrics"""
        current_time = time.time()
        
        if hasattr(self, '_last_bloom_update'):
            time_delta = current_time - self._last_bloom_update
            
            # Calculate rates (per minute)
            if time_delta > 0:
                active_delta = active - self.bloom_metrics.active_blooms
                sealed_delta = sealed - self.bloom_metrics.sealed_blooms
                
                self.bloom_metrics.bloom_rate = (active_delta / time_delta) * 60
                self.bloom_metrics.seal_rate = (sealed_delta / time_delta) * 60
        
        self.bloom_metrics.active_blooms = active
        self.bloom_metrics.sealed_blooms = sealed
        self._last_bloom_update = current_time
    
    def _update_history(self, shi: float):
        """Update historical tracking"""
        self.health_history.append({
            'timestamp': time.time(),
            'shi': shi,
            'status': self.current_metrics.status.value
        })
        
        # Track component history
        for component in HealthComponent:
            value = getattr(self.current_metrics, f"{component.value.split('_')[0]}_health", 0.5)
            self.component_history[component.value].append(value)
    
    def _check_health_anomalies(self, shi: float):
        """Check for health-related anomalies"""
        # Sudden drops
        if len(self.health_history) > 1:
            prev_shi = self.health_history[-2]['shi']
            drop = prev_shi - shi
            
            if drop > 0.2:
                log_anomaly(
                    "SHI_SUDDEN_DROP",
                    f"SHI dropped by {drop:.3f} in one update",
                    AnomalySeverity.ERROR,
                    {"previous": prev_shi, "current": shi}
                )
            
        # Component imbalance
        weakest_comp, weakest_val = self.current_metrics.get_weakest_component()
        strongest_comp, strongest_val = self.current_metrics.get_strongest_component()
        
        if strongest_val - weakest_val > 0.6:
            log_anomaly(
                "SHI_COMPONENT_IMBALANCE",
                f"Large health imbalance: {weakest_comp}={weakest_val:.3f}, {strongest_comp}={strongest_val:.3f}",
                AnomalySeverity.WARNING,
                {"weakest": weakest_comp, "strongest": strongest_comp}
            )
    
    def _trigger_critical_intervention(self, shi: float):
        """Trigger intervention for critical health"""
        if not self.recovery_active:
            self.recovery_active = True
            self.recovery_start_time = time.time()
            self.interventions_triggered += 1
            
            log_anomaly(
                "SHI_CRITICAL_INTERVENTION",
                f"Critical SHI ({shi:.3f}) - Recovery mode activated",
                AnomalySeverity.CRITICAL,
                {
                    "shi": shi,
                    "weakest_component": self.current_metrics.get_weakest_component(),
                    "intervention_count": self.interventions_triggered
                }
            )
            
            # Log event
            self.event_history.append({
                'timestamp': time.time(),
                'event': 'critical_intervention',
                'shi': shi,
                'details': 'Recovery mode activated'
            })
    
    def update_schema_health(self, shi: float):
        """Update schema health and trigger appropriate responses"""
        with self.lock:
            status = self._classify_health_status(shi)
            
            # Log status changes
            if hasattr(self, '_last_status') and self._last_status != status:
                log_anomaly(
                    "SHI_STATUS_CHANGE",
                    f"Schema health status changed: {self._last_status.value} -> {status.value}",
                    AnomalySeverity.INFO,
                    {"old_status": self._last_status.value, "new_status": status.value, "shi": shi}
                )
                
                self.event_history.append({
                    'timestamp': time.time(),
                    'event': 'status_change',
                    'old_status': self._last_status.value,
                    'new_status': status.value,
                    'shi': shi
                })
            
            self._last_status = status
            
            # Check if we can exit recovery mode
            if self.recovery_active and shi > self.warning_threshold:
                recovery_duration = time.time() - self.recovery_start_time
                self.recovery_active = False
                
                log_anomaly(
                    "SHI_RECOVERY_COMPLETE",
                    f"Schema health recovered to {shi:.3f} after {recovery_duration:.1f}s",
                    AnomalySeverity.INFO,
                    {"shi": shi, "recovery_duration": recovery_duration}
                )
    
    def get_health_report(self) -> Dict[str, Any]:
        """Get comprehensive health report"""
        with self.lock:
            recent_history = list(self.health_history)[-100:]
            avg_recent_shi = sum(h['shi'] for h in recent_history) / len(recent_history) if recent_history else 0.5
            
            # Calculate trends
            if len(self.health_history) >= 10:
                old_avg = sum(h['shi'] for h in list(self.health_history)[:10]) / 10
                new_avg = sum(h['shi'] for h in list(self.health_history)[-10:]) / 10
                trend = "improving" if new_avg > old_avg else "declining" if new_avg < old_avg else "stable"
            else:
                trend = "insufficient_data"
            
            return {
                'current_shi': round(self.current_metrics.shi_value, 3),
                'status': self.current_metrics.status.value,
                'average_shi': round(avg_recent_shi, 3),
                'trend': trend,
                'components': {
                    'bloom_health': round(self.current_metrics.bloom_health, 3),
                    'sigil_health': round(self.current_metrics.sigil_health, 3),
                    'pulse_health': round(self.current_metrics.pulse_health, 3),
                    'nutrient_health': round(self.current_metrics.nutrient_health, 3),
                    'consciousness_health': round(self.current_metrics.consciousness_health, 3),
                    'temporal_health': round(self.current_metrics.temporal_health, 3)
                },
                'weakest_component': self.current_metrics.get_weakest_component(),
                'strongest_component': self.current_metrics.get_strongest_component(),
                'bloom_metrics': {
                    'active': self.bloom_metrics.active_blooms,
                    'sealed': self.bloom_metrics.sealed_blooms,
                    'bloom_rate': round(self.bloom_metrics.bloom_rate, 2),
                    'seal_rate': round(self.bloom_metrics.seal_rate, 2)
                },
                'recovery_active': self.recovery_active,
                'interventions_triggered': self.interventions_triggered,
                'recent_events': list(self.event_history)[-5:],
                'recommendations': self._generate_recommendations()
            }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate health improvement recommendations"""
        recommendations = []
        
        # Component-specific recommendations
        if self.current_metrics.bloom_health < 0.5:
            recommendations.append("Increase bloom generation rate or reduce bloom failures")
        
        if self.current_metrics.sigil_health < 0.5:
            recommendations.append("Stabilize sigil entropy - reduce variance")
        
        if self.current_metrics.pulse_health < 0.5:
            recommendations.append("Stabilize pulse patterns - check for external disturbances")
        
        if self.current_metrics.nutrient_health < 0.5:
            recommendations.append("Balance nutrient levels across all types")
        
        if self.current_metrics.consciousness_health < 0.5:
            recommendations.append("Improve SCUP and coherence values")
        
        if self.current_metrics.temporal_health < 0.5:
            recommendations.append("Synchronize tick rate and reduce temporal drift")
        
        # Overall recommendations
        if self.current_metrics.shi_value < self.warning_threshold:
            recommendations.insert(0, "PRIORITY: Schema health is degraded - immediate attention required")
        
        if self.recovery_active:
            recommendations.append("Recovery mode active - maintain stable conditions")
        
        return recommendations

# Global SHI instance
_shi_system = SchemaHealthIndex()

# Legacy compatibility functions
def calculate_SHI(pulse_avg: float, active_blooms: int, sealed_blooms: int, sigil_entropy_list: List[float]) -> float:
    """Legacy function for SHI calculation"""
    return _shi_system.calculate_SHI(pulse_avg, active_blooms, sealed_blooms, sigil_entropy_list)

def update_schema_health(shi: float):
    """Legacy function for health updates"""
    _shi_system.update_schema_health(shi)

# Extended API
def get_health_report() -> Dict[str, Any]:
    """Get comprehensive health report"""
    return _shi_system.get_health_report()

def calculate_enhanced_SHI(pulse_avg: float, active_blooms: int, sealed_blooms: int, 
                          sigil_entropy_list: List[float], **kwargs) -> float:
    """Enhanced SHI calculation with additional metrics"""
    return _shi_system.calculate_SHI(pulse_avg, active_blooms, sealed_blooms, sigil_entropy_list, kwargs)