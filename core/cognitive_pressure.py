#!/usr/bin/env python3
"""
DAWN Cognitive Pressure Engine
P = Bσ² Cognitive Pressure Calculation and Integration System

Calculates cognitive pressure using bloom mass (B) and sigil velocity (σ²) where:
- bloom_mass (B) = active cognitive load from Sigil Engine + Entropy Analyzer activity  
- sigil_velocity (σ) = processing speed from recent sigil executions + entropy change rate
- cognitive_pressure (P) = B * σ²

Integrates with existing DAWN components:
- Pulse Controller: Pressure-thermal coupling and zone influence
- Sigil Engine: Cognitive load tracking and processing speed metrics
- Entropy Analyzer: Chaos activity and entropy change rate monitoring
- GUI Interface: Real-time pressure visualization
"""

import time
import math
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from collections import deque

# DAWN Core Integration
try:
    from ...pulse_controller import PulseController
    PULSE_CONTROLLER_AVAILABLE = True
except ImportError:
    PULSE_CONTROLLER_AVAILABLE = False
    PulseController = None

try:
    from ...sigil_engine import SigilEngine
    SIGIL_ENGINE_AVAILABLE = True
except ImportError:
    SIGIL_ENGINE_AVAILABLE = False
    SigilEngine = None

try:
    from ...dawn_entropy_analyzer import EnhancedEntropyAnalyzer
    ENTROPY_ANALYZER_AVAILABLE = True
except ImportError:
    ENTROPY_ANALYZER_AVAILABLE = False
    EnhancedEntropyAnalyzer = None

# Configure logging
logger = logging.getLogger(__name__)


class PressureLevel(Enum):
    """Cognitive pressure level classifications"""
    MINIMAL = "minimal"      # P < 10
    LOW = "low"             # 10 ≤ P < 25
    MODERATE = "moderate"   # 25 ≤ P < 50
    HIGH = "high"           # 50 ≤ P < 100
    CRITICAL = "critical"   # P ≥ 100
    OVERFLOW = "overflow"   # P ≥ 200


class PressureAlert(Enum):
    """Pressure alert types"""
    PRESSURE_SPIKE = "pressure_spike"
    SUSTAINED_HIGH = "sustained_high"
    CRITICAL_OVERLOAD = "critical_overload"
    BLOOM_MASS_BUILDUP = "bloom_mass_buildup"
    VELOCITY_SURGE = "velocity_surge"
    THERMAL_PRESSURE_COUPLING = "thermal_pressure_coupling"


@dataclass
class BloomMassComponents:
    """Components of bloom mass (B) calculation"""
    sigil_queue_size: float = 0.0          # Active sigils in queue
    sigil_execution_load: float = 0.0      # Current execution overhead
    entropy_activity: float = 0.0          # Entropy analyzer workload
    thermal_contribution: float = 0.0      # Thermal system pressure
    memory_load: float = 0.0               # Active memory operations
    total_bloom_mass: float = 0.0          # B = sum of all components


@dataclass
class SigilVelocityComponents:
    """Components of sigil velocity (σ) calculation"""
    recent_executions: float = 0.0         # Recent sigil execution rate
    processing_speed: float = 0.0          # Average processing speed
    entropy_change_rate: float = 0.0       # Rate of entropy change
    thermal_momentum: float = 0.0          # Thermal system momentum
    cognitive_acceleration: float = 0.0    # Rate of cognitive change
    total_sigil_velocity: float = 0.0      # σ = combined velocity metrics


@dataclass
class CognitivePressureSnapshot:
    """Complete cognitive pressure analysis snapshot"""
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Core P = Bσ² calculation
    bloom_mass: BloomMassComponents = field(default_factory=BloomMassComponents)
    sigil_velocity: SigilVelocityComponents = field(default_factory=SigilVelocityComponents)
    cognitive_pressure: float = 0.0        # P = B * σ²
    pressure_level: PressureLevel = PressureLevel.MINIMAL
    
    # System integration
    thermal_coupling: float = 0.0          # Pressure-thermal interaction
    pulse_zone_influence: str = "none"     # Influence on pulse zones
    entropy_feedback: float = 0.0          # Entropy system feedback
    
    # Alerts and recommendations
    active_alerts: List[PressureAlert] = field(default_factory=list)
    relief_recommendations: List[str] = field(default_factory=list)
    system_health: str = "normal"


class CognitivePressureEngine:
    """
    DAWN Cognitive Pressure Engine
    
    Calculates and monitors cognitive pressure (P = Bσ²) by integrating data from:
    - Sigil Engine: Provides cognitive load and processing metrics
    - Entropy Analyzer: Provides chaos activity and change rates  
    - Pulse Controller: Provides thermal context and pressure-thermal coupling
    """
    
    def __init__(self, 
                 pulse_controller: Optional[PulseController] = None,
                 sigil_engine: Optional[SigilEngine] = None,
                 entropy_analyzer: Optional[EnhancedEntropyAnalyzer] = None,
                 history_size: int = 100):
        """
        Initialize the cognitive pressure engine
        
        Args:
            pulse_controller: DAWN pulse controller for thermal integration
            sigil_engine: DAWN sigil engine for cognitive load tracking  
            entropy_analyzer: DAWN entropy analyzer for chaos monitoring
            history_size: Number of pressure snapshots to maintain in history
        """
        # Component integration
        self.pulse_controller = pulse_controller
        self.sigil_engine = sigil_engine  
        self.entropy_analyzer = entropy_analyzer
        
        # Core pressure state
        self.current_pressure = 0.0
        self.current_level = PressureLevel.MINIMAL
        self.pressure_history: deque = deque(maxlen=history_size)
        self.last_update = time.time()
        
        # Component weight configuration
        self.bloom_mass_weights = {
            'sigil_queue_size': 1.2,        # Queued sigils create pressure
            'sigil_execution_load': 1.5,    # Active execution creates high pressure  
            'entropy_activity': 1.0,        # Entropy analysis workload
            'thermal_contribution': 0.8,    # Thermal system pressure
            'memory_load': 1.1               # Memory operations
        }
        
        self.sigil_velocity_weights = {
            'recent_executions': 1.3,        # Recent execution rate
            'processing_speed': 1.0,         # Average processing speed
            'entropy_change_rate': 1.4,      # Entropy change velocity
            'thermal_momentum': 0.9,         # Thermal momentum
            'cognitive_acceleration': 1.2    # Cognitive change rate
        }
        
        # Pressure thresholds
        self.pressure_thresholds = {
            PressureLevel.MINIMAL: 0.0,
            PressureLevel.LOW: 10.0,
            PressureLevel.MODERATE: 25.0,
            PressureLevel.HIGH: 50.0,
            PressureLevel.CRITICAL: 100.0,
            PressureLevel.OVERFLOW: 200.0
        }
        
        # Alert thresholds
        self.alert_thresholds = {
            'pressure_spike': 30.0,          # Rapid pressure increase
            'sustained_high': 75.0,          # Sustained high pressure
            'critical_overload': 150.0,      # Critical system overload
            'velocity_surge': 20.0,          # Rapid velocity increase
            'bloom_mass_buildup': 40.0       # Excessive bloom mass
        }
        
        # Performance tracking
        self.calculation_count = 0
        self.total_calculation_time = 0.0
        self.alert_count = 0
        self.last_alert_time = 0.0
        
        # Integration flags
        self.thermal_coupling_enabled = True
        self.entropy_feedback_enabled = True
        self.alert_system_enabled = True
        
        logger.info(f"🧠 Cognitive Pressure Engine initialized")
        logger.info(f"   Pulse Controller: {'✅' if pulse_controller else '❌'}")
        logger.info(f"   Sigil Engine: {'✅' if sigil_engine else '❌'}")
        logger.info(f"   Entropy Analyzer: {'✅' if entropy_analyzer else '❌'}")

    def calculate_bloom_mass(self) -> BloomMassComponents:
        """
        Calculate bloom mass (B) from integrated DAWN components
        
        Returns:
            BloomMassComponents with detailed breakdown
        """
        components = BloomMassComponents()
        
        # Sigil Engine contribution
        if self.sigil_engine:
            try:
                # Get sigil queue information
                queue_size = getattr(self.sigil_engine, 'pending_count', 0)
                components.sigil_queue_size = queue_size * self.bloom_mass_weights['sigil_queue_size']
                
                # Get execution load
                execution_load = getattr(self.sigil_engine, 'current_heat', 0) / 10.0  # Normalize thermal to load
                components.sigil_execution_load = execution_load * self.bloom_mass_weights['sigil_execution_load']
                
                # Memory operations (if available)
                memory_ops = getattr(self.sigil_engine, 'active_operations', 0)
                components.memory_load = memory_ops * self.bloom_mass_weights['memory_load']
                
            except Exception as e:
                logger.warning(f"Error extracting sigil engine data: {e}")
        
        # Entropy Analyzer contribution  
        if self.entropy_analyzer:
            try:
                # Get entropy analysis activity
                analysis_count = getattr(self.entropy_analyzer, 'analysis_count', 0)
                activity_factor = min(10.0, analysis_count / 10.0)  # Normalize activity
                components.entropy_activity = activity_factor * self.bloom_mass_weights['entropy_activity']
                
            except Exception as e:
                logger.warning(f"Error extracting entropy analyzer data: {e}")
        
        # Pulse Controller thermal contribution
        if self.pulse_controller and self.thermal_coupling_enabled:
            try:
                # High thermal contributes to cognitive pressure
                thermal_heat = getattr(self.pulse_controller, 'current_heat', 0)
                thermal_factor = max(0, (thermal_heat - 50) / 10.0)  # Only above 50° contributes
                components.thermal_contribution = thermal_factor * self.bloom_mass_weights['thermal_contribution']
                
            except Exception as e:
                logger.warning(f"Error extracting pulse controller data: {e}")
        
        # Calculate total bloom mass (B)
        components.total_bloom_mass = (
            components.sigil_queue_size +
            components.sigil_execution_load +
            components.entropy_activity +
            components.thermal_contribution +
            components.memory_load
        )
        
        return components

    def calculate_sigil_velocity(self) -> SigilVelocityComponents:
        """
        Calculate sigil velocity (σ) from integrated DAWN components
        
        Returns:
            SigilVelocityComponents with detailed breakdown
        """
        components = SigilVelocityComponents()
        
        # Sigil Engine velocity metrics
        if self.sigil_engine:
            try:
                # Recent execution rate
                execution_rate = getattr(self.sigil_engine, 'executions_per_second', 0)
                components.recent_executions = execution_rate * self.sigil_velocity_weights['recent_executions']
                
                # Processing speed (inverse of average execution time)
                avg_execution_time = getattr(self.sigil_engine, 'average_execution_time', 1.0)
                processing_speed = 1.0 / max(0.1, avg_execution_time)  # Prevent division by zero
                components.processing_speed = processing_speed * self.sigil_velocity_weights['processing_speed']
                
                # Cognitive acceleration (rate of change in processing)
                acceleration = getattr(self.sigil_engine, 'processing_acceleration', 0)
                components.cognitive_acceleration = acceleration * self.sigil_velocity_weights['cognitive_acceleration']
                
            except Exception as e:
                logger.warning(f"Error extracting sigil engine velocity: {e}")
        
        # Entropy Analyzer change rate
        if self.entropy_analyzer:
            try:
                # Get most recent entropy delta
                if hasattr(self.entropy_analyzer, 'previous_entropy') and self.entropy_analyzer.previous_entropy:
                    # Calculate entropy change rate
                    entropy_delta = abs(getattr(self.entropy_analyzer, 'last_delta', 0))
                    change_rate = entropy_delta * 10.0  # Scale up for velocity calculation
                    components.entropy_change_rate = change_rate * self.sigil_velocity_weights['entropy_change_rate']
                
            except Exception as e:
                logger.warning(f"Error extracting entropy change rate: {e}")
        
        # Pulse Controller thermal momentum
        if self.pulse_controller:
            try:
                # Thermal momentum (rate of heat change)
                current_heat = getattr(self.pulse_controller, 'current_heat', 0)
                if hasattr(self.pulse_controller, 'heat_history') and self.pulse_controller.heat_history:
                    # Calculate heat change rate from history
                    if len(self.pulse_controller.heat_history) > 1:
                        recent_heat = self.pulse_controller.heat_history[-1][1]
                        prev_heat = self.pulse_controller.heat_history[-2][1] 
                        heat_momentum = abs(recent_heat - prev_heat)
                        components.thermal_momentum = heat_momentum * self.sigil_velocity_weights['thermal_momentum']
                
            except Exception as e:
                logger.warning(f"Error extracting thermal momentum: {e}")
        
        # Calculate total sigil velocity (σ)
        components.total_sigil_velocity = (
            components.recent_executions +
            components.processing_speed +
            components.entropy_change_rate +
            components.thermal_momentum +
            components.cognitive_acceleration
        )
        
        return components

    def calculate_cognitive_pressure(self) -> CognitivePressureSnapshot:
        """
        Calculate complete cognitive pressure (P = Bσ²) with full system integration
        
        Returns:
            CognitivePressureSnapshot with comprehensive analysis
        """
        start_time = time.time()
        
        try:
            # Calculate bloom mass (B) and sigil velocity (σ)
            bloom_mass = self.calculate_bloom_mass()
            sigil_velocity = self.calculate_sigil_velocity()
            
            # Apply cognitive pressure formula: P = B * σ²
            cognitive_pressure = bloom_mass.total_bloom_mass * (sigil_velocity.total_sigil_velocity ** 2)
            
            # Classify pressure level
            pressure_level = self._classify_pressure_level(cognitive_pressure)
            
            # Calculate system integration metrics
            thermal_coupling = self._calculate_thermal_coupling(cognitive_pressure)
            pulse_zone_influence = self._calculate_pulse_zone_influence(cognitive_pressure)
            entropy_feedback = self._calculate_entropy_feedback(cognitive_pressure)
            
            # Generate alerts and recommendations
            active_alerts = self._generate_alerts(cognitive_pressure, bloom_mass, sigil_velocity)
            relief_recommendations = self._generate_relief_recommendations(pressure_level, active_alerts)
            system_health = self._assess_system_health(cognitive_pressure, active_alerts)
            
            # Create comprehensive snapshot
            snapshot = CognitivePressureSnapshot(
                bloom_mass=bloom_mass,
                sigil_velocity=sigil_velocity,
                cognitive_pressure=cognitive_pressure,
                pressure_level=pressure_level,
                thermal_coupling=thermal_coupling,
                pulse_zone_influence=pulse_zone_influence,
                entropy_feedback=entropy_feedback,
                active_alerts=active_alerts,
                relief_recommendations=relief_recommendations,
                system_health=system_health
            )
            
            # Update engine state
            self.current_pressure = cognitive_pressure
            self.current_level = pressure_level
            self.pressure_history.append(snapshot)
            self.last_update = time.time()
            
            # Performance tracking
            calculation_time = time.time() - start_time
            self.calculation_count += 1
            self.total_calculation_time += calculation_time
            
            logger.debug(f"🧠 Cognitive pressure calculated: P={cognitive_pressure:.2f} ({pressure_level.value})")
            
            return snapshot
            
        except Exception as e:
            logger.error(f"🧠 Error calculating cognitive pressure: {e}")
            # Return minimal safe snapshot
            return CognitivePressureSnapshot()

    def _classify_pressure_level(self, pressure: float) -> PressureLevel:
        """Classify pressure level based on thresholds"""
        for level in reversed(list(PressureLevel)):
            if pressure >= self.pressure_thresholds[level]:
                return level
        return PressureLevel.MINIMAL

    def _calculate_thermal_coupling(self, pressure: float) -> float:
        """Calculate pressure-thermal coupling strength"""
        if not self.pulse_controller or not self.thermal_coupling_enabled:
            return 0.0
        
        try:
            current_heat = getattr(self.pulse_controller, 'current_heat', 0)
            # Coupling strength increases with both pressure and heat
            coupling = (pressure / 100.0) * (current_heat / 100.0)
            return min(1.0, coupling)
        except Exception:
            return 0.0

    def _calculate_pulse_zone_influence(self, pressure: float) -> str:
        """Calculate how pressure influences pulse zones"""
        if pressure < 25:
            return "none"
        elif pressure < 50:
            return "minor"
        elif pressure < 100:
            return "moderate"
        else:
            return "major"

    def _calculate_entropy_feedback(self, pressure: float) -> float:
        """Calculate entropy system feedback from pressure"""
        if not self.entropy_analyzer or not self.entropy_feedback_enabled:
            return 0.0
        
        # High pressure creates entropy feedback
        return min(1.0, pressure / 150.0)

    def _generate_alerts(self, pressure: float, bloom_mass: BloomMassComponents, 
                        sigil_velocity: SigilVelocityComponents) -> List[PressureAlert]:
        """Generate pressure alerts based on current state"""
        alerts = []
        
        if not self.alert_system_enabled:
            return alerts
        
        # Pressure spike detection
        if len(self.pressure_history) > 1:
            prev_pressure = self.pressure_history[-1].cognitive_pressure
            pressure_delta = pressure - prev_pressure
            if pressure_delta > self.alert_thresholds['pressure_spike']:
                alerts.append(PressureAlert.PRESSURE_SPIKE)
        
        # Sustained high pressure
        if pressure > self.alert_thresholds['sustained_high']:
            alerts.append(PressureAlert.SUSTAINED_HIGH)
        
        # Critical overload
        if pressure > self.alert_thresholds['critical_overload']:
            alerts.append(PressureAlert.CRITICAL_OVERLOAD)
        
        # Bloom mass buildup
        if bloom_mass.total_bloom_mass > self.alert_thresholds['bloom_mass_buildup']:
            alerts.append(PressureAlert.BLOOM_MASS_BUILDUP)
        
        # Velocity surge
        if sigil_velocity.total_sigil_velocity > self.alert_thresholds['velocity_surge']:
            alerts.append(PressureAlert.VELOCITY_SURGE)
        
        # Thermal-pressure coupling alert
        thermal_coupling = self._calculate_thermal_coupling(pressure)
        if thermal_coupling > 0.7:
            alerts.append(PressureAlert.THERMAL_PRESSURE_COUPLING)
        
        if alerts:
            self.alert_count += len(alerts)
            self.last_alert_time = time.time()
        
        return alerts

    def _generate_relief_recommendations(self, level: PressureLevel, alerts: List[PressureAlert]) -> List[str]:
        """Generate pressure relief recommendations"""
        recommendations = []
        
        if level == PressureLevel.CRITICAL or level == PressureLevel.OVERFLOW:
            recommendations.extend([
                "🚨 CRITICAL: Reduce sigil execution load immediately",
                "🔥 Activate thermal cooling protocols",
                "⏸️ Pause non-essential cognitive operations",
                "🔄 Redistribute processing load"
            ])
        elif level == PressureLevel.HIGH:
            recommendations.extend([
                "⚠️ Reduce active sigil queue size",
                "🌡️ Monitor thermal coupling",
                "📊 Optimize entropy analysis frequency"
            ])
        elif level == PressureLevel.MODERATE:
            recommendations.extend([
                "📈 Monitor pressure trends",
                "⚡ Consider load balancing",
                "🧠 Optimize cognitive processing"
            ])
        
        # Alert-specific recommendations
        if PressureAlert.BLOOM_MASS_BUILDUP in alerts:
            recommendations.append("🌸 Reduce bloom mass through memory consolidation")
        
        if PressureAlert.VELOCITY_SURGE in alerts:
            recommendations.append("🏃 Stabilize sigil velocity through pacing")
        
        if PressureAlert.THERMAL_PRESSURE_COUPLING in alerts:
            recommendations.append("🔗 Decouple thermal-pressure feedback loop")
        
        return recommendations

    def _assess_system_health(self, pressure: float, alerts: List[PressureAlert]) -> str:
        """Assess overall system health based on pressure and alerts"""
        if pressure > 150 or PressureAlert.CRITICAL_OVERLOAD in alerts:
            return "critical"
        elif pressure > 75 or len(alerts) > 2:
            return "warning"
        elif pressure > 50 or len(alerts) > 0:
            return "caution"
        else:
            return "normal"

    def get_current_state(self) -> Dict[str, Any]:
        """Get current cognitive pressure engine state"""
        return {
            "cognitive_pressure": self.current_pressure,
            "pressure_level": self.current_level.value,
            "last_update": self.last_update,
            "history_length": len(self.pressure_history),
            "calculation_count": self.calculation_count,
            "alert_count": self.alert_count,
            "average_calculation_time": (
                self.total_calculation_time / max(1, self.calculation_count)
            ),
            "component_status": {
                "pulse_controller": self.pulse_controller is not None,
                "sigil_engine": self.sigil_engine is not None,
                "entropy_analyzer": self.entropy_analyzer is not None
            },
            "integration_flags": {
                "thermal_coupling": self.thermal_coupling_enabled,
                "entropy_feedback": self.entropy_feedback_enabled,
                "alert_system": self.alert_system_enabled
            }
        }

    def get_pressure_breakdown(self) -> Dict[str, Any]:
        """Get detailed breakdown of current pressure calculation"""
        if not self.pressure_history:
            return {"error": "No pressure data available"}
        
        latest = self.pressure_history[-1]
        
        return {
            "timestamp": latest.timestamp.isoformat(),
            "bloom_mass_breakdown": {
                "sigil_queue_size": latest.bloom_mass.sigil_queue_size,
                "sigil_execution_load": latest.bloom_mass.sigil_execution_load,
                "entropy_activity": latest.bloom_mass.entropy_activity,
                "thermal_contribution": latest.bloom_mass.thermal_contribution,
                "memory_load": latest.bloom_mass.memory_load,
                "total": latest.bloom_mass.total_bloom_mass
            },
            "sigil_velocity_breakdown": {
                "recent_executions": latest.sigil_velocity.recent_executions,
                "processing_speed": latest.sigil_velocity.processing_speed,
                "entropy_change_rate": latest.sigil_velocity.entropy_change_rate,
                "thermal_momentum": latest.sigil_velocity.thermal_momentum,
                "cognitive_acceleration": latest.sigil_velocity.cognitive_acceleration,
                "total": latest.sigil_velocity.total_sigil_velocity
            },
            "pressure_calculation": {
                "bloom_mass_B": latest.bloom_mass.total_bloom_mass,
                "sigil_velocity_sigma": latest.sigil_velocity.total_sigil_velocity,
                "velocity_squared": latest.sigil_velocity.total_sigil_velocity ** 2,
                "cognitive_pressure_P": latest.cognitive_pressure,
                "pressure_level": latest.pressure_level.value
            },
            "system_integration": {
                "thermal_coupling": latest.thermal_coupling,
                "pulse_zone_influence": latest.pulse_zone_influence,
                "entropy_feedback": latest.entropy_feedback,
                "system_health": latest.system_health
            },
            "alerts": [alert.value for alert in latest.active_alerts],
            "recommendations": latest.relief_recommendations
        }

    def enable_thermal_coupling(self, enabled: bool = True):
        """Enable/disable thermal-pressure coupling"""
        self.thermal_coupling_enabled = enabled
        logger.info(f"🔗 Thermal coupling {'enabled' if enabled else 'disabled'}")

    def enable_entropy_feedback(self, enabled: bool = True):
        """Enable/disable entropy feedback"""
        self.entropy_feedback_enabled = enabled
        logger.info(f"📊 Entropy feedback {'enabled' if enabled else 'disabled'}")

    def enable_alert_system(self, enabled: bool = True):
        """Enable/disable alert system"""
        self.alert_system_enabled = enabled
        logger.info(f"🚨 Alert system {'enabled' if enabled else 'disabled'}")


# Global cognitive pressure engine instance
_global_pressure_engine: Optional[CognitivePressureEngine] = None


def get_cognitive_pressure_engine() -> CognitivePressureEngine:
    """Get global cognitive pressure engine instance"""
    global _global_pressure_engine
    if _global_pressure_engine is None:
        _global_pressure_engine = CognitivePressureEngine()
    return _global_pressure_engine


def initialize_pressure_engine(pulse_controller=None, sigil_engine=None, entropy_analyzer=None):
    """Initialize global pressure engine with DAWN components"""
    global _global_pressure_engine
    _global_pressure_engine = CognitivePressureEngine(
        pulse_controller=pulse_controller,
        sigil_engine=sigil_engine,
        entropy_analyzer=entropy_analyzer
    )
    return _global_pressure_engine


# Convenience functions for integration
def calculate_pressure() -> float:
    """Calculate current cognitive pressure"""
    engine = get_cognitive_pressure_engine()
    snapshot = engine.calculate_cognitive_pressure()
    return snapshot.cognitive_pressure


def get_pressure_level() -> str:
    """Get current pressure level"""
    engine = get_cognitive_pressure_engine()
    return engine.current_level.value


def get_pressure_breakdown() -> Dict[str, Any]:
    """Get detailed pressure breakdown"""
    engine = get_cognitive_pressure_engine()
    return engine.get_pressure_breakdown()


def get_pressure_alerts() -> List[str]:
    """Get current pressure alerts"""
    engine = get_cognitive_pressure_engine()
    if engine.pressure_history:
        latest = engine.pressure_history[-1]
        return [alert.value for alert in latest.active_alerts]
    return [] 