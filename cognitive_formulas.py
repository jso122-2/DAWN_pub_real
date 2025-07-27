#!/usr/bin/env python3
"""
DAWN Cognitive Formula Engine - P = B×σ² Implementation
======================================================

Implements the core cognitive pressure formula:
P = B × σ² (Bloom mass × Sigil velocity squared)

Plus supporting formulas:
- Bloom Mass (B): Active memory + rebloom queue + reflection backlog
- Sigil Velocity (σ): Recent sigils + thought rate + entropy delta + mutation rate  
- Pressure Relief: Dynamic threshold-based interventions
- System Modulation: Pressure-based performance adjustments

The engine provides real-time cognitive pressure monitoring and 
automated intervention recommendations for DAWN's consciousness system.
"""

import time
import math
import logging
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple, Callable, Set
from datetime import datetime, timezone
from collections import deque
from enum import Enum
from pathlib import Path
import json

logger = logging.getLogger("cognitive_formulas")

class PressureLevel(Enum):
    """Cognitive pressure level classifications"""
    LOW = "low"           # < 20: Normal operation
    MODERATE = "moderate" # 20-50: Monitor closely  
    HIGH = "high"         # 50-100: Reduce load
    CRITICAL = "critical" # > 100: Emergency protocols

class BloomMassComponent(Enum):
    """Components that contribute to bloom mass"""
    ACTIVE_MEMORY = "active_memory"
    REBLOOM_QUEUE = "rebloom_queue"
    REFLECTION_BACKLOG = "reflection_backlog"
    PROCESSING_LOAD = "processing_load"
    SIGIL_MUTATIONS = "sigil_mutations"

class SigilVelocityComponent(Enum):
    """Components that contribute to sigil velocity"""
    RECENT_SIGILS = "recent_sigils"
    THOUGHT_RATE = "thought_rate"
    ENTROPY_DELTA = "entropy_delta"
    MUTATION_RATE = "mutation_rate"
    FEEDBACK_LOOPS = "feedback_loops"

@dataclass
class CognitivePressureReading:
    """Single cognitive pressure measurement"""
    timestamp: float
    bloom_mass: float           # B component
    sigil_velocity: float       # σ component  
    pressure_value: float       # P = B × σ²
    pressure_level: PressureLevel
    pressure_trend: float       # Rate of change
    component_breakdown: Dict[str, float] = field(default_factory=dict)
    relief_actions: List[str] = field(default_factory=list)
    system_recommendations: List[str] = field(default_factory=list)

@dataclass
class FormulaEngineState:
    """Current state of the formula engine"""
    readings_history: deque = field(default_factory=lambda: deque(maxlen=50))
    last_reading: Optional[CognitivePressureReading] = None
    calculations_count: int = 0
    interventions_triggered: int = 0
    mr_wolf_activations: int = 0
    average_pressure: float = 0.0
    peak_pressure: float = 0.0
    pressure_stability: float = 1.0

class DAWNFormulaEngine:
    """
    DAWN Cognitive Formula Engine
    
    Implements the cognitive pressure formula P = B × σ² and provides
    real-time monitoring, intervention recommendations, and system
    modulation based on cognitive load analysis.
    """
    
    def __init__(self):
        """Initialize the DAWN Formula Engine"""
        
        # Core formula parameters
        self.PRESSURE_THRESHOLDS = {
            PressureLevel.LOW: 0.0,
            PressureLevel.MODERATE: 20.0,
            PressureLevel.HIGH: 50.0,
            PressureLevel.CRITICAL: 100.0
        }
        
        # Bloom mass component weights
        self.BLOOM_MASS_WEIGHTS = {
            BloomMassComponent.ACTIVE_MEMORY: 1.0,
            BloomMassComponent.REBLOOM_QUEUE: 1.5,      # Higher impact
            BloomMassComponent.REFLECTION_BACKLOG: 2.0,  # Highest impact
            BloomMassComponent.PROCESSING_LOAD: 1.2,
            BloomMassComponent.SIGIL_MUTATIONS: 0.8
        }
        
        # Sigil velocity component factors
        self.SIGIL_VELOCITY_FACTORS = {
            SigilVelocityComponent.RECENT_SIGILS: 1.0,
            SigilVelocityComponent.THOUGHT_RATE: 0.8,
            SigilVelocityComponent.ENTROPY_DELTA: 1.5,   # High impact
            SigilVelocityComponent.MUTATION_RATE: 1.3,
            SigilVelocityComponent.FEEDBACK_LOOPS: 1.1
        }
        
        # Engine configuration
        self.pressure_sensitivity = 1.0
        self.velocity_damping = 0.9      # Prevents velocity spikes
        self.mass_scaling = 1.0          # Adjusts bloom mass impact
        self.intervention_cooldown = 10.0 # Seconds between interventions
        
        # State tracking
        self.state = FormulaEngineState()
        self.last_intervention_time = 0.0
        self.active_interventions: Set[str] = set()
        
        # Callback system for interventions
        self.intervention_callbacks: List[Callable] = []
        self.mr_wolf_callback: Optional[Callable] = None
        
        logger.info("🧠 [FORMULA] DAWN Cognitive Formula Engine initialized")
        logger.info(f"🧠 [FORMULA] Pressure thresholds: {[f'{level.value}={thresh}' for level, thresh in self.PRESSURE_THRESHOLDS.items()]}")
    
    def calculate_pressure(self, state: Dict[str, Any]) -> CognitivePressureReading:
        """
        Calculate cognitive pressure using P = B × σ²
        
        Args:
            state: DAWN cognitive state containing metrics
            
        Returns:
            CognitivePressureReading with full analysis
        """
        calculation_start = time.time()
        
        try:
            current_time = time.time()
            
            # Calculate Bloom Mass (B)
            bloom_mass, bloom_breakdown = self.calculate_bloom_mass(state)
            
            # Calculate Sigil Velocity (σ) 
            sigil_velocity, velocity_breakdown = self.calculate_sigil_velocity(state)
            
            # Apply core formula: P = B × σ²
            raw_pressure = bloom_mass * (sigil_velocity ** 2)
            
            # Apply scaling and sensitivity
            scaled_pressure = raw_pressure * self.pressure_sensitivity * self.mass_scaling
            
            # Apply velocity damping to prevent spikes
            if self.state.last_reading:
                prev_pressure = self.state.last_reading.pressure_value
                damped_pressure = scaled_pressure * (1 - self.velocity_damping) + prev_pressure * self.velocity_damping
            else:
                damped_pressure = scaled_pressure
            
            pressure_value = max(0.0, damped_pressure)
            
            # Classify pressure level
            pressure_level = self._classify_pressure_level(pressure_value)
            
            # Calculate pressure trend
            pressure_trend = self._calculate_pressure_trend(pressure_value)
            
            # Generate interventions and recommendations
            relief_actions = self._generate_relief_actions(pressure_value, pressure_level, state)
            system_recommendations = self._generate_system_recommendations(pressure_value, pressure_level, state)
            
            # Create comprehensive reading
            reading = CognitivePressureReading(
                timestamp=current_time,
                bloom_mass=bloom_mass,
                sigil_velocity=sigil_velocity,
                pressure_value=pressure_value,
                pressure_level=pressure_level,
                pressure_trend=pressure_trend,
                component_breakdown={
                    **{f"bloom_{k}": v for k, v in bloom_breakdown.items()},
                    **{f"velocity_{k}": v for k, v in velocity_breakdown.items()},
                    "raw_pressure": raw_pressure,
                    "scaled_pressure": scaled_pressure,
                    "damped_pressure": damped_pressure
                },
                relief_actions=relief_actions,
                system_recommendations=system_recommendations
            )
            
            # Update state
            self.state.readings_history.append(reading)
            self.state.last_reading = reading
            self.state.calculations_count += 1
            self._update_state_metrics()
            
            # Execute interventions if needed
            self._execute_interventions(reading, state)
            
            calculation_time = time.time() - calculation_start
            logger.debug(f"🧠 [FORMULA] P={pressure_value:.1f} (B={bloom_mass:.1f}, σ={sigil_velocity:.2f}) - {pressure_level.value} [{calculation_time*1000:.1f}ms]")
            
            return reading
            
        except Exception as e:
            logger.error(f"🧠 [FORMULA] Pressure calculation error: {e}")
            # Return safe fallback reading
            return CognitivePressureReading(
                timestamp=time.time(),
                bloom_mass=0.0,
                sigil_velocity=0.0,
                pressure_value=0.0,
                pressure_level=PressureLevel.LOW,
                pressure_trend=0.0,
                relief_actions=["Error in pressure calculation"],
                system_recommendations=["Check formula engine health"]
            )
    
    def calculate_bloom_mass(self, state: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
        """
        Calculate bloom mass (B) from cognitive state components
        
        Returns:
            Tuple of (total_bloom_mass, component_breakdown)
        """
        components = {}
        
        # Extract and weight each component
        components[BloomMassComponent.ACTIVE_MEMORY.value] = (
            state.get('active_memory_count', 0) * self.BLOOM_MASS_WEIGHTS[BloomMassComponent.ACTIVE_MEMORY]
        )
        
        components[BloomMassComponent.REBLOOM_QUEUE.value] = (
            state.get('rebloom_queue_size', 0) * self.BLOOM_MASS_WEIGHTS[BloomMassComponent.REBLOOM_QUEUE]
        )
        
        components[BloomMassComponent.REFLECTION_BACKLOG.value] = (
            state.get('reflection_backlog', 0) * self.BLOOM_MASS_WEIGHTS[BloomMassComponent.REFLECTION_BACKLOG]
        )
        
        components[BloomMassComponent.PROCESSING_LOAD.value] = (
            state.get('processing_load', 0) * self.BLOOM_MASS_WEIGHTS[BloomMassComponent.PROCESSING_LOAD]
        )
        
        components[BloomMassComponent.SIGIL_MUTATIONS.value] = (
            state.get('sigil_mutation_backlog', 0) * self.BLOOM_MASS_WEIGHTS[BloomMassComponent.SIGIL_MUTATIONS]
        )
        
        # Calculate total bloom mass
        total_mass = sum(components.values())
        
        logger.debug(f"🧠 [BLOOM] Mass={total_mass:.1f} (memory={components['active_memory']:.1f}, rebloom={components['rebloom_queue']:.1f}, reflection={components['reflection_backlog']:.1f})")
        
        return total_mass, components
    
    def calculate_sigil_velocity(self, state: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
        """
        Calculate sigil velocity (σ) from cognitive dynamics
        
        Returns:
            Tuple of (total_velocity, component_breakdown) 
        """
        components = {}
        
        # Extract and factor each component
        components[SigilVelocityComponent.RECENT_SIGILS.value] = (
            state.get('recent_sigil_count', 0) * self.SIGIL_VELOCITY_FACTORS[SigilVelocityComponent.RECENT_SIGILS]
        )
        
        components[SigilVelocityComponent.THOUGHT_RATE.value] = (
            state.get('thought_rate', 0) * self.SIGIL_VELOCITY_FACTORS[SigilVelocityComponent.THOUGHT_RATE]
        )
        
        components[SigilVelocityComponent.ENTROPY_DELTA.value] = (
            abs(state.get('entropy_delta', 0)) * self.SIGIL_VELOCITY_FACTORS[SigilVelocityComponent.ENTROPY_DELTA]
        )
        
        components[SigilVelocityComponent.MUTATION_RATE.value] = (
            state.get('sigil_mutation_rate', 0) * self.SIGIL_VELOCITY_FACTORS[SigilVelocityComponent.MUTATION_RATE]
        )
        
        components[SigilVelocityComponent.FEEDBACK_LOOPS.value] = (
            state.get('feedback_loop_intensity', 0) * self.SIGIL_VELOCITY_FACTORS[SigilVelocityComponent.FEEDBACK_LOOPS]
        )
        
        # Calculate total velocity
        total_velocity = sum(components.values())
        
        logger.debug(f"🧠 [VELOCITY] σ={total_velocity:.2f} (sigils={components['recent_sigils']:.1f}, thoughts={components['thought_rate']:.1f}, entropy={components['entropy_delta']:.2f})")
        
        return total_velocity, components
    
    def _classify_pressure_level(self, pressure_value: float) -> PressureLevel:
        """Classify pressure level based on thresholds"""
        
        if pressure_value >= self.PRESSURE_THRESHOLDS[PressureLevel.CRITICAL]:
            return PressureLevel.CRITICAL
        elif pressure_value >= self.PRESSURE_THRESHOLDS[PressureLevel.HIGH]:
            return PressureLevel.HIGH
        elif pressure_value >= self.PRESSURE_THRESHOLDS[PressureLevel.MODERATE]:
            return PressureLevel.MODERATE
        else:
            return PressureLevel.LOW
    
    def _calculate_pressure_trend(self, current_pressure: float) -> float:
        """Calculate rate of pressure change"""
        
        if len(self.state.readings_history) < 2:
            return 0.0
        
        recent_readings = list(self.state.readings_history)[-5:]  # Last 5 readings
        pressures = [r.pressure_value for r in recent_readings] + [current_pressure]
        
        # Simple linear trend
        if len(pressures) >= 3:
            # Calculate slope of recent pressure changes
            x = list(range(len(pressures)))
            y = pressures
            n = len(x)
            
            x_mean = sum(x) / n
            y_mean = sum(y) / n
            
            numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
            denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
            
            if denominator > 0:
                return numerator / denominator
        
        return 0.0
    
    def _generate_relief_actions(self, pressure_value: float, pressure_level: PressureLevel, state: Dict[str, Any]) -> List[str]:
        """Generate pressure relief action recommendations"""
        
        actions = []
        
        if pressure_level == PressureLevel.CRITICAL:
            actions.extend([
                "🚨 EMERGENCY: Halt non-essential processing",
                "🐺 Trigger Mr. Wolf stabilization protocol", 
                "⏸️ Suspend rebloom queue processing",
                "🔄 Reduce reflection depth to minimum",
                "🧹 Clear sigil mutation backlog",
                "💾 Force memory consolidation",
                "🛑 Disable new sigil generation"
            ])
        elif pressure_level == PressureLevel.HIGH:
            actions.extend([
                "⚠️ Reduce processing load by 40%",
                "⏸️ Pause rebloom operations", 
                "🐌 Decrease thought generation rate",
                "📦 Consolidate active memories",
                "🔄 Limit reflection cycles",
                "⚡ Boost entropy damping"
            ])
        elif pressure_level == PressureLevel.MODERATE:
            actions.extend([
                "👁️ Monitor processing carefully",
                "🔧 Optimize memory usage", 
                "🤔 Consider reflection consolidation",
                "📊 Analyze bloom mass sources",
                "⚖️ Balance sigil generation rate"
            ])
        elif pressure_level == PressureLevel.LOW:
            actions.extend([
                "✅ Normal operation maintained",
                "🚀 Consider enabling enhanced processing",
                "🧠 Increase reflection depth if needed"
            ])
        
        # Add specific actions based on component analysis
        if state.get('rebloom_queue_size', 0) > 10:
            actions.append("📝 Prioritize rebloom queue processing")
        
        if state.get('reflection_backlog', 0) > 5:
            actions.append("🤔 Address reflection backlog immediately")
        
        if state.get('sigil_mutation_rate', 0) > 0.8:
            actions.append("🧬 Throttle sigil mutation rate")
        
        return actions
    
    def _generate_system_recommendations(self, pressure_value: float, pressure_level: PressureLevel, state: Dict[str, Any]) -> List[str]:
        """Generate system-level recommendations"""
        
        recommendations = []
        
        # Performance tuning recommendations
        if pressure_level in [PressureLevel.HIGH, PressureLevel.CRITICAL]:
            recommendations.extend([
                "Increase tick interval to reduce frequency",
                "Activate conservative processing mode",
                "Enable aggressive memory garbage collection",
                "Reduce GUI update frequency"
            ])
        
        # Capacity recommendations
        if pressure_value > self.state.peak_pressure * 0.8:
            recommendations.append("Consider increasing system capacity")
        
        # Stability recommendations  
        if self.state.pressure_stability < 0.5:
            recommendations.extend([
                "Investigate pressure oscillation causes",
                "Adjust velocity damping parameters",
                "Review bloom mass accumulation patterns"
            ])
        
        return recommendations
    
    def _update_state_metrics(self):
        """Update aggregate state metrics"""
        
        if not self.state.readings_history:
            return
        
        recent_readings = list(self.state.readings_history)
        pressures = [r.pressure_value for r in recent_readings]
        
        # Update average pressure
        self.state.average_pressure = sum(pressures) / len(pressures)
        
        # Update peak pressure
        self.state.peak_pressure = max(self.state.peak_pressure, pressures[-1])
        
        # Calculate pressure stability (inverse of variance)
        if len(pressures) > 1:
            variance = np.var(pressures)
            self.state.pressure_stability = 1.0 / (1.0 + variance)
        else:
            self.state.pressure_stability = 1.0
    
    def _execute_interventions(self, reading: CognitivePressureReading, state: Dict[str, Any]):
        """Execute automatic interventions based on pressure level"""
        
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_intervention_time < self.intervention_cooldown:
            return
        
        interventions_executed = []
        
        # Critical pressure interventions
        if reading.pressure_level == PressureLevel.CRITICAL:
            if "mr_wolf" not in self.active_interventions:
                self._trigger_mr_wolf(reading, state)
                interventions_executed.append("mr_wolf")
                self.state.mr_wolf_activations += 1
            
            if "emergency_halt" not in self.active_interventions:
                self._trigger_emergency_halt(reading, state)
                interventions_executed.append("emergency_halt")
        
        # High pressure interventions
        elif reading.pressure_level == PressureLevel.HIGH:
            if "load_reduction" not in self.active_interventions:
                self._trigger_load_reduction(reading, state)
                interventions_executed.append("load_reduction")
        
        # Update intervention tracking
        if interventions_executed:
            self.active_interventions.update(interventions_executed)
            self.state.interventions_triggered += len(interventions_executed)
            self.last_intervention_time = current_time
            
            # Execute callbacks
            for callback in self.intervention_callbacks:
                try:
                    callback(reading, interventions_executed)
                except Exception as e:
                    logger.warning(f"🧠 [FORMULA] Intervention callback failed: {e}")
    
    def _trigger_mr_wolf(self, reading: CognitivePressureReading, state: Dict[str, Any]):
        """Trigger Mr. Wolf stabilization protocol"""
        
        logger.warning(f"🐺 [MR_WOLF] Activating stabilization protocol - Pressure: {reading.pressure_value:.1f}")
        
        if self.mr_wolf_callback:
            try:
                self.mr_wolf_callback(reading, state)
            except Exception as e:
                logger.error(f"🐺 [MR_WOLF] Callback execution failed: {e}")
        
        # Log the activation
        self._log_intervention("mr_wolf_activation", reading, {
            "trigger_pressure": reading.pressure_value,
            "bloom_mass": reading.bloom_mass,
            "sigil_velocity": reading.sigil_velocity
        })
    
    def _trigger_emergency_halt(self, reading: CognitivePressureReading, state: Dict[str, Any]):
        """Trigger emergency processing halt"""
        
        logger.critical(f"🛑 [EMERGENCY] Halting non-essential processing - Pressure: {reading.pressure_value:.1f}")
        
        # This would integrate with the actual system halt mechanisms
        self._log_intervention("emergency_halt", reading, {
            "halted_subsystems": ["rebloom", "mutation", "deep_reflection"],
            "pressure_threshold": self.PRESSURE_THRESHOLDS[PressureLevel.CRITICAL]
        })
    
    def _trigger_load_reduction(self, reading: CognitivePressureReading, state: Dict[str, Any]):
        """Trigger load reduction measures"""
        
        logger.warning(f"⚡ [LOAD_REDUCTION] Reducing system load - Pressure: {reading.pressure_value:.1f}")
        
        self._log_intervention("load_reduction", reading, {
            "reduction_level": 0.4,  # 40% reduction
            "affected_components": ["processing_load", "rebloom_queue", "thought_rate"]
        })
    
    def _log_intervention(self, intervention_type: str, reading: CognitivePressureReading, details: Dict[str, Any]):
        """Log intervention to file system"""
        
        log_entry = {
            "timestamp": reading.timestamp,
            "intervention_type": intervention_type,
            "pressure_state": {
                "pressure_value": reading.pressure_value,
                "pressure_level": reading.pressure_level.value,
                "bloom_mass": reading.bloom_mass,
                "sigil_velocity": reading.sigil_velocity,
                "pressure_trend": reading.pressure_trend
            },
            "details": details
        }
        
        # Write to intervention log
        try:
            log_path = Path("runtime/logs/pressure_interventions.log")
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(log_path, "a") as f:
                f.write(f"{json.dumps(log_entry)}\n")
                
        except Exception as e:
            logger.error(f"🧠 [FORMULA] Failed to log intervention: {e}")
    
    # Public interface methods
    
    def register_intervention_callback(self, callback: Callable):
        """Register callback for intervention notifications"""
        self.intervention_callbacks.append(callback)
        logger.info(f"🧠 [FORMULA] Registered intervention callback: {callback.__name__ if hasattr(callback, '__name__') else 'anonymous'}")
    
    def register_mr_wolf_callback(self, callback: Callable):
        """Register Mr. Wolf activation callback"""
        self.mr_wolf_callback = callback
        logger.info("🐺 [FORMULA] Registered Mr. Wolf callback")
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current formula engine state"""
        
        return {
            "current_reading": {
                "pressure_value": self.state.last_reading.pressure_value if self.state.last_reading else 0.0,
                "pressure_level": self.state.last_reading.pressure_level.value if self.state.last_reading else "low",
                "bloom_mass": self.state.last_reading.bloom_mass if self.state.last_reading else 0.0,
                "sigil_velocity": self.state.last_reading.sigil_velocity if self.state.last_reading else 0.0,
                "pressure_trend": self.state.last_reading.pressure_trend if self.state.last_reading else 0.0
            } if self.state.last_reading else None,
            "metrics": {
                "calculations_count": self.state.calculations_count,
                "interventions_triggered": self.state.interventions_triggered,
                "mr_wolf_activations": self.state.mr_wolf_activations,
                "average_pressure": self.state.average_pressure,
                "peak_pressure": self.state.peak_pressure,
                "pressure_stability": self.state.pressure_stability
            },
            "active_interventions": list(self.active_interventions),
            "readings_history_length": len(self.state.readings_history)
        }
    
    def get_pressure_modulation(self) -> Dict[str, float]:
        """Get pressure-based modulation factors for other systems"""
        
        if not self.state.last_reading:
            return {
                "processing_multiplier": 1.0,
                "reflection_depth_limit": 1.0,
                "mutation_rate_limit": 1.0,
                "memory_consolidation_urgency": 0.0
            }
        
        reading = self.state.last_reading
        
        # Calculate modulation based on pressure level
        if reading.pressure_level == PressureLevel.CRITICAL:
            processing_multiplier = 0.2  # Severely reduce processing
            reflection_depth_limit = 0.1
            mutation_rate_limit = 0.0
            memory_consolidation_urgency = 1.0
        elif reading.pressure_level == PressureLevel.HIGH:
            processing_multiplier = 0.6
            reflection_depth_limit = 0.5
            mutation_rate_limit = 0.3
            memory_consolidation_urgency = 0.8
        elif reading.pressure_level == PressureLevel.MODERATE:
            processing_multiplier = 0.8
            reflection_depth_limit = 0.8
            mutation_rate_limit = 0.7
            memory_consolidation_urgency = 0.4
        else:  # LOW
            processing_multiplier = 1.0
            reflection_depth_limit = 1.0
            mutation_rate_limit = 1.0
            memory_consolidation_urgency = 0.1
        
        return {
            "processing_multiplier": processing_multiplier,
            "reflection_depth_limit": reflection_depth_limit,
            "mutation_rate_limit": mutation_rate_limit,
            "memory_consolidation_urgency": memory_consolidation_urgency,
            "pressure_relief_priority": reading.pressure_value / 100.0  # Normalized priority
        }

# Global formula engine instance
_global_formula_engine: Optional[DAWNFormulaEngine] = None

def get_dawn_formula_engine() -> DAWNFormulaEngine:
    """Get global DAWN formula engine instance"""
    global _global_formula_engine
    if _global_formula_engine is None:
        _global_formula_engine = DAWNFormulaEngine()
    return _global_formula_engine

def calculate_cognitive_pressure(state: Dict[str, Any]) -> CognitivePressureReading:
    """Convenience function to calculate cognitive pressure"""
    engine = get_dawn_formula_engine()
    return engine.calculate_pressure(state)

def get_pressure_modulation() -> Dict[str, float]:
    """Convenience function to get pressure-based modulation"""
    engine = get_dawn_formula_engine()
    return engine.get_pressure_modulation()

# Export key classes and functions
__all__ = [
    'DAWNFormulaEngine',
    'CognitivePressureReading', 
    'PressureLevel',
    'BloomMassComponent',
    'SigilVelocityComponent',
    'get_dawn_formula_engine',
    'calculate_cognitive_pressure',
    'get_pressure_modulation'
] 