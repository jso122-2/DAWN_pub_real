#!/usr/bin/env python3
"""
DAWN Cognitive Pressure Physics - P = Bσ²
==========================================

Implements the fundamental cognitive pressure equation: P = Bσ²

Where:
- P = Cognitive Pressure (instability detection, cascade trigger)
- B = Bloom Mass (accumulated memory weight, depth, complexity)
- σ = Sigil Velocity (rate of sigil activation, symbolic processing speed)

This formula captures how cognitive instability builds up when heavy memory
processing (bloom mass) combines with rapid symbolic thinking (sigil velocity).
High pressure triggers cascades, reblooms, and emergency interventions.

The physics model treats consciousness as a dynamic system where:
- Bloom Mass represents the "weight" of active memories and associations
- Sigil Velocity represents the "speed" of symbolic processing
- Pressure accumulation leads to state transitions and cognitive events

This is used for:
- Instability detection and early warning
- Rebloom cascade triggering  
- Emergency cognitive intervention
- Adaptive tick rate adjustment
- System stability monitoring
"""

import time
import math
import logging
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone
from enum import Enum

logger = logging.getLogger("cognitive_pressure")

class PressureZone(Enum):
    """Cognitive pressure operational zones"""
    CALM = "CALM"           # P < 0.2 - Low pressure, stable state
    BUILDING = "BUILDING"   # P 0.2-0.5 - Pressure accumulating
    ACTIVE = "ACTIVE"       # P 0.5-0.8 - High activity, watch carefully
    CRITICAL = "CRITICAL"   # P 0.8-1.2 - Critical pressure, intervention needed
    OVERFLOW = "OVERFLOW"   # P > 1.2 - Overflow state, emergency action

@dataclass 
class BloomMassMetrics:
    """Bloom mass calculation components"""
    memory_depth: float = 0.0      # Depth of active memories
    association_weight: float = 0.0 # Weight of associations
    rebloom_accumulation: float = 0.0 # Rebloomed memory load
    semantic_density: float = 0.0   # Density of semantic content
    total_mass: float = 0.0         # Computed bloom mass B

@dataclass
class SigilVelocityMetrics:
    """Sigil velocity calculation components"""
    activation_rate: float = 0.0    # Sigils activated per time unit
    processing_speed: float = 0.0   # Speed of sigil processing
    symbolic_intensity: float = 0.0 # Intensity of symbolic thinking
    cascade_velocity: float = 0.0   # Speed of sigil cascades
    total_velocity: float = 0.0     # Computed sigil velocity σ

@dataclass
class CognitivePressureState:
    """Complete cognitive pressure state"""
    bloom_mass: BloomMassMetrics = field(default_factory=BloomMassMetrics)
    sigil_velocity: SigilVelocityMetrics = field(default_factory=SigilVelocityMetrics)
    pressure_value: float = 0.0     # P = Bσ²
    pressure_zone: PressureZone = PressureZone.CALM
    instability_risk: float = 0.0   # Risk of cascade/breakdown
    intervention_needed: bool = False
    timestamp: float = 0.0

class CognitivePressurePhysics:
    """
    Cognitive Pressure Physics Engine
    
    Implements P = Bσ² calculations and provides pressure-based
    insights for cognitive stability and intervention systems.
    """
    
    def __init__(self):
        """Initialize the cognitive pressure physics engine"""
        self.current_state = CognitivePressureState()
        self.pressure_history: List[Tuple[float, float]] = []  # (timestamp, pressure)
        self.max_history = 50
        
        # Physics constants
        self.MASS_SCALING_FACTOR = 1.0
        self.VELOCITY_SCALING_FACTOR = 1.0
        self.PRESSURE_CAP = 2.0  # Maximum theoretical pressure
        
        # Pressure zone thresholds
        self.CALM_THRESHOLD = 0.2
        self.BUILDING_THRESHOLD = 0.5
        self.ACTIVE_THRESHOLD = 0.8
        self.CRITICAL_THRESHOLD = 1.2
        
        # Tracking metrics
        self.calculation_count = 0
        self.peak_pressure = 0.0
        self.pressure_spikes = 0
        self.cascade_triggers = 0
        
        logger.info("⚡ [PRESSURE] Cognitive Pressure Physics initialized")
        logger.info(f"⚡ [PRESSURE] Zones: CALM<{self.CALM_THRESHOLD}, BUILDING<{self.BUILDING_THRESHOLD}, ACTIVE<{self.ACTIVE_THRESHOLD}, CRITICAL<{self.CRITICAL_THRESHOLD}")
    
    def calculate_cognitive_pressure(self, state: Dict[str, Any]) -> float:
        """
        Calculate cognitive pressure using P = Bσ²
        
        Args:
            state: DAWN cognitive state containing:
                - bloom_data: dict with depth, complexity, reblooms
                - sigil_data: list of active sigils
                - memory_state: dict with access patterns
                - entropy: float (disorder level)
                - heat: float (thermal energy)
                - tick_interval: float (timing data)
        
        Returns:
            Cognitive pressure value P
        """
        try:
            # Step 1: Calculate Bloom Mass (B)
            bloom_mass = self._calculate_bloom_mass(state)
            
            # Step 2: Calculate Sigil Velocity (σ)
            sigil_velocity = self._calculate_sigil_velocity(state)
            
            # Step 3: Apply core physics formula P = Bσ²
            raw_pressure = bloom_mass.total_mass * (sigil_velocity.total_velocity ** 2)
            
            # Step 4: Apply scaling and bounds
            pressure = min(self.PRESSURE_CAP, raw_pressure * self.MASS_SCALING_FACTOR)
            
            # Step 5: Calculate derived metrics
            pressure_zone = self._classify_pressure_zone(pressure)
            instability_risk = self._calculate_instability_risk(pressure, bloom_mass, sigil_velocity)
            intervention_needed = pressure_zone in [PressureZone.CRITICAL, PressureZone.OVERFLOW]
            
            # Step 6: Update state
            self.current_state = CognitivePressureState(
                bloom_mass=bloom_mass,
                sigil_velocity=sigil_velocity,
                pressure_value=pressure,
                pressure_zone=pressure_zone,
                instability_risk=instability_risk,
                intervention_needed=intervention_needed,
                timestamp=time.time()
            )
            
            # Step 7: Track metrics and history
            self._update_tracking_metrics(pressure)
            self._record_pressure_history(pressure)
            
            logger.debug(f"⚡ [PRESSURE] P={pressure:.3f} (B={bloom_mass.total_mass:.2f}, σ={sigil_velocity.total_velocity:.2f}) → {pressure_zone.value}")
            
            return pressure
            
        except Exception as e:
            logger.error(f"⚡ [PRESSURE] Calculation error: {e}")
            return self.current_state.pressure_value  # Return last known value
    
    def _calculate_bloom_mass(self, state: Dict[str, Any]) -> BloomMassMetrics:
        """Calculate bloom mass B from memory and association data"""
        
        # Extract bloom-related data
        bloom_data = state.get('bloom_data', {})
        memory_state = state.get('memory_state', {})
        rebloom_events = state.get('rebloom_events', [])
        
        # Memory depth component
        memory_depth = bloom_data.get('depth', 0) / 10.0  # Normalize depth scale
        memory_depth = max(0.0, min(1.0, memory_depth))
        
        # Association weight from coherence and connections
        coherence = state.get('coherence', 0.5)
        connections = memory_state.get('active_connections', 0)
        association_weight = coherence * min(1.0, connections / 10.0)
        
        # Rebloom accumulation - recent reblooms add mass
        recent_reblooms = len([r for r in rebloom_events if isinstance(r, dict) and 
                             time.time() - r.get('timestamp', 0) < 30])  # Last 30 seconds
        rebloom_accumulation = min(0.8, recent_reblooms / 5.0)
        
        # Semantic density from bloom complexity
        bloom_complexity = bloom_data.get('complexity', 0.0)
        semantic_drift = abs(bloom_data.get('semantic_drift', 0.0))
        semantic_density = (bloom_complexity + semantic_drift) / 2.0
        semantic_density = max(0.0, min(1.0, semantic_density))
        
        # Total bloom mass with weighted components
        total_mass = (
            memory_depth * 0.3 +
            association_weight * 0.25 +
            rebloom_accumulation * 0.25 +
            semantic_density * 0.2
        )
        
        return BloomMassMetrics(
            memory_depth=memory_depth,
            association_weight=association_weight,
            rebloom_accumulation=rebloom_accumulation,
            semantic_density=semantic_density,
            total_mass=total_mass
        )
    
    def _calculate_sigil_velocity(self, state: Dict[str, Any]) -> SigilVelocityMetrics:
        """Calculate sigil velocity σ from symbolic processing data"""
        
        # Extract sigil-related data
        sigil_data = state.get('sigil_data', [])
        if isinstance(sigil_data, dict):
            sigil_data = sigil_data.get('active_sigils', [])
        
        tick_interval = state.get('tick_interval', 2.0)
        
        # Activation rate - sigils per time unit
        active_sigil_count = len(sigil_data) if isinstance(sigil_data, list) else 0
        activation_rate = active_sigil_count / max(tick_interval, 0.1)  # Sigils per second
        activation_rate = min(5.0, activation_rate)  # Cap at 5 sigils/sec
        
        # Processing speed from sigil intensity and system heat
        heat = state.get('heat', 25.0) / 100.0  # Normalize heat
        entropy = state.get('entropy', 0.5)
        processing_speed = heat * (1.0 + entropy)  # Heat + entropy boost speed
        processing_speed = max(0.1, min(2.0, processing_speed))
        
        # Symbolic intensity from sigil categories and pressure
        symbolic_intensity = 0.0
        if isinstance(sigil_data, list):
            # Analyze sigil types for intensity
            intensity_categories = ['critical', 'meta', 'action', 'integration']
            for sigil in sigil_data:
                if isinstance(sigil, dict):
                    category = sigil.get('category', 'unknown')
                    if category in intensity_categories:
                        symbolic_intensity += sigil.get('intensity', 0.5)
        
        symbolic_intensity = min(2.0, symbolic_intensity)
        
        # Cascade velocity - how fast sigils trigger each other
        sigil_pressure = state.get('sigil_pressure', 0.0)
        cascade_velocity = sigil_pressure * processing_speed
        cascade_velocity = max(0.0, min(1.5, cascade_velocity))
        
        # Total velocity with weighted components
        total_velocity = (
            activation_rate * 0.4 +
            processing_speed * 0.3 +
            symbolic_intensity * 0.2 +
            cascade_velocity * 0.1
        )
        
        # Normalize to reasonable range [0, 2]
        total_velocity = max(0.0, min(2.0, total_velocity))
        
        return SigilVelocityMetrics(
            activation_rate=activation_rate,
            processing_speed=processing_speed,
            symbolic_intensity=symbolic_intensity,
            cascade_velocity=cascade_velocity,
            total_velocity=total_velocity
        )
    
    def _classify_pressure_zone(self, pressure: float) -> PressureZone:
        """Classify pressure value into operational zones"""
        if pressure < self.CALM_THRESHOLD:
            return PressureZone.CALM
        elif pressure < self.BUILDING_THRESHOLD:
            return PressureZone.BUILDING
        elif pressure < self.ACTIVE_THRESHOLD:
            return PressureZone.ACTIVE
        elif pressure < self.CRITICAL_THRESHOLD:
            return PressureZone.CRITICAL
        else:
            return PressureZone.OVERFLOW
    
    def _calculate_instability_risk(self, pressure: float, 
                                  bloom_mass: BloomMassMetrics, 
                                  sigil_velocity: SigilVelocityMetrics) -> float:
        """Calculate risk of cognitive instability based on pressure components"""
        
        # Base risk from pressure level
        pressure_risk = min(1.0, pressure / self.CRITICAL_THRESHOLD)
        
        # Mass-velocity imbalance risk
        mass_velocity_ratio = (bloom_mass.total_mass / max(0.1, sigil_velocity.total_velocity))
        imbalance_risk = abs(mass_velocity_ratio - 1.0)  # Risk when ratio far from 1:1
        imbalance_risk = min(0.5, imbalance_risk)
        
        # Velocity spike risk
        velocity_spike_risk = 0.0
        if sigil_velocity.total_velocity > 1.5:
            velocity_spike_risk = (sigil_velocity.total_velocity - 1.5) * 0.4
        
        # Mass accumulation risk
        mass_accumulation_risk = 0.0
        if bloom_mass.rebloom_accumulation > 0.6:
            mass_accumulation_risk = (bloom_mass.rebloom_accumulation - 0.6) * 0.5
        
        # Combined instability risk
        total_risk = min(1.0, 
            pressure_risk * 0.5 +
            imbalance_risk * 0.2 +
            velocity_spike_risk * 0.15 +
            mass_accumulation_risk * 0.15
        )
        
        return total_risk
    
    def _update_tracking_metrics(self, pressure: float):
        """Update tracking metrics for analysis"""
        self.calculation_count += 1
        
        # Track peak pressure
        if pressure > self.peak_pressure:
            self.peak_pressure = pressure
        
        # Count pressure spikes
        if pressure > self.ACTIVE_THRESHOLD:
            self.pressure_spikes += 1
        
        # Count cascade triggers
        if pressure > self.CRITICAL_THRESHOLD:
            self.cascade_triggers += 1
    
    def _record_pressure_history(self, pressure: float):
        """Record pressure in history for temporal analysis"""
        current_time = time.time()
        self.pressure_history.append((current_time, pressure))
        
        # Maintain history size
        if len(self.pressure_history) > self.max_history:
            self.pressure_history.pop(0)
    
    def get_pressure_trend(self, time_window: float = 10.0) -> Dict[str, float]:
        """Analyze pressure trend over time window"""
        if len(self.pressure_history) < 2:
            return {"trend": 0.0, "volatility": 0.0, "average": 0.0}
        
        current_time = time.time()
        recent_history = [(t, p) for t, p in self.pressure_history 
                         if current_time - t <= time_window]
        
        if len(recent_history) < 2:
            return {"trend": 0.0, "volatility": 0.0, "average": self.current_state.pressure_value}
        
        # Calculate trend (slope)
        times = [t for t, p in recent_history]
        pressures = [p for t, p in recent_history]
        
        # Simple linear regression for trend
        n = len(times)
        sum_t = sum(times)
        sum_p = sum(pressures)
        sum_tp = sum(t * p for t, p in recent_history)
        sum_t2 = sum(t * t for t in times)
        
        trend = (n * sum_tp - sum_t * sum_p) / (n * sum_t2 - sum_t * sum_t)
        
        # Calculate volatility (standard deviation)
        avg_pressure = sum_p / n
        volatility = math.sqrt(sum((p - avg_pressure) ** 2 for p in pressures) / n)
        
        return {
            "trend": trend,
            "volatility": volatility,
            "average": avg_pressure
        }
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current pressure state for external systems"""
        trend_data = self.get_pressure_trend()
        
        return {
            "pressure": self.current_state.pressure_value,
            "pressure_zone": self.current_state.pressure_zone.value,
            "instability_risk": self.current_state.instability_risk,
            "intervention_needed": self.current_state.intervention_needed,
            "bloom_mass": {
                "total": self.current_state.bloom_mass.total_mass,
                "memory_depth": self.current_state.bloom_mass.memory_depth,
                "association_weight": self.current_state.bloom_mass.association_weight,
                "rebloom_accumulation": self.current_state.bloom_mass.rebloom_accumulation,
                "semantic_density": self.current_state.bloom_mass.semantic_density
            },
            "sigil_velocity": {
                "total": self.current_state.sigil_velocity.total_velocity,
                "activation_rate": self.current_state.sigil_velocity.activation_rate,
                "processing_speed": self.current_state.sigil_velocity.processing_speed,
                "symbolic_intensity": self.current_state.sigil_velocity.symbolic_intensity,
                "cascade_velocity": self.current_state.sigil_velocity.cascade_velocity
            },
            "trends": trend_data,
            "statistics": {
                "calculation_count": self.calculation_count,
                "peak_pressure": self.peak_pressure,
                "pressure_spikes": self.pressure_spikes,
                "cascade_triggers": self.cascade_triggers
            }
        }
    
    def should_trigger_intervention(self) -> bool:
        """Check if intervention should be triggered based on pressure"""
        return self.current_state.intervention_needed
    
    def should_trigger_cascade(self) -> bool:
        """Check if cascade should be triggered based on pressure"""
        return self.current_state.pressure_zone in [PressureZone.CRITICAL, PressureZone.OVERFLOW]
    
    def get_pressure_modulation(self) -> Dict[str, float]:
        """Get pressure-based modulation parameters for other systems"""
        pressure = self.current_state.pressure_value
        zone = self.current_state.pressure_zone
        
        if zone == PressureZone.CALM:
            return {
                "tick_speed_modifier": 0.9,    # Slower ticks when calm
                "rebloom_sensitivity": 0.8,    # Less sensitive to reblooms
                "reflection_urgency": 0.7,     # Less urgent reflection
                "attention_scatter": 0.1       # Focused attention
            }
        elif zone == PressureZone.BUILDING:
            return {
                "tick_speed_modifier": 1.0,    # Normal tick speed
                "rebloom_sensitivity": 1.0,    # Normal sensitivity
                "reflection_urgency": 1.0,     # Normal reflection
                "attention_scatter": 0.2       # Normal attention
            }
        elif zone == PressureZone.ACTIVE:
            return {
                "tick_speed_modifier": 1.1,    # Slightly faster ticks
                "rebloom_sensitivity": 1.2,    # More sensitive
                "reflection_urgency": 1.3,     # More urgent reflection
                "attention_scatter": 0.4       # Some attention scatter
            }
        elif zone == PressureZone.CRITICAL:
            return {
                "tick_speed_modifier": 1.3,    # Much faster ticks
                "rebloom_sensitivity": 1.5,    # Very sensitive
                "reflection_urgency": 1.8,     # Very urgent reflection
                "attention_scatter": 0.7       # High attention scatter
            }
        else:  # OVERFLOW
            return {
                "tick_speed_modifier": 1.5,    # Emergency fast ticks
                "rebloom_sensitivity": 2.0,    # Hypersensitive
                "reflection_urgency": 2.5,     # Emergency reflection
                "attention_scatter": 1.0       # Complete attention scatter
            }


# Global pressure physics instance
_global_pressure_instance: Optional[CognitivePressurePhysics] = None

def get_cognitive_pressure_physics() -> CognitivePressurePhysics:
    """Get global cognitive pressure physics instance"""
    global _global_pressure_instance
    if _global_pressure_instance is None:
        _global_pressure_instance = CognitivePressurePhysics()
    return _global_pressure_instance

def calculate_cognitive_pressure(state: Dict[str, Any]) -> float:
    """Convenience function to calculate cognitive pressure for a state"""
    physics = get_cognitive_pressure_physics()
    return physics.calculate_cognitive_pressure(state)

def get_pressure_state() -> Dict[str, Any]:
    """Convenience function to get current pressure state"""
    physics = get_cognitive_pressure_physics()
    return physics.get_current_state()

# Export key classes and functions
__all__ = [
    'CognitivePressurePhysics',
    'CognitivePressureState',
    'BloomMassMetrics',
    'SigilVelocityMetrics', 
    'PressureZone',
    'get_cognitive_pressure_physics',
    'calculate_cognitive_pressure',
    'get_pressure_state'
] 