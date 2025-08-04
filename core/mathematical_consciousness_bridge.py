#!/usr/bin/env python3
"""
DAWN Mathematical Consciousness Bridge
=====================================

Integration layer that connects the mathematical consciousness formulas
(SHI, Cognitive Pressure, SCUP Drift) to DAWN's operational systems.

This bridge enables the mathematical models to actually influence:
- Tick system behavior and timing
- Reflection frequency and depth  
- Voice mutation and stability
- Rebloom triggering and urgency
- Emotional modulation
- Attention and focus patterns

The bridge acts as the nervous system between pure mathematics and
lived cognitive experience, making formulas into felt forces.
"""

import time
import logging
import asyncio
from typing import Dict, Any, Optional, List, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime

# Import mathematical consciousness modules
from core.schema_health_index import (
    get_schema_health_index, 
    SHIHealthZone,
    get_shi_modulation_for_system
)
from core.cognitive_pressure_physics import (
    get_cognitive_pressure_physics,
    PressureZone,
    calculate_cognitive_pressure
)
from core.scup_drift_resolver import (
    get_scup_drift_resolver,
    resolve_drift_coherence,
    forecast_cognitive_drift
)

# Import existing DAWN systems for integration
try:
    from core.voice_mood_modulation import VoiceMoodModulator
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

try:
    from core.memory_rebloom_reflex import MemoryRebloomReflex
    REBLOOM_AVAILABLE = True
except ImportError:
    REBLOOM_AVAILABLE = False

try:
    from reflection.generate_reflection import ReflectionEngine
    REFLECTION_AVAILABLE = True
except ImportError:
    REFLECTION_AVAILABLE = False

logger = logging.getLogger("math_consciousness_bridge")

@dataclass
class MathematicalInfluence:
    """Quantified influence from mathematical consciousness"""
    shi_value: float = 0.5
    shi_zone: str = "STABLE"
    pressure_value: float = 0.0
    pressure_zone: str = "CALM"
    
    # Modulation factors from formulas
    tick_interval_modifier: float = 1.0
    reflection_frequency: float = 1.0
    reflection_depth: float = 1.0
    voice_mutation_rate: float = 0.1
    voice_stability: float = 1.0
    rebloom_threshold: float = 0.0
    rebloom_urgency: float = 1.0
    emotional_stability: float = 1.0
    attention_focus: float = 1.0
    
    # Meta-cognitive awareness
    consciousness_coherence: float = 1.0
    mathematical_alignment: float = 1.0
    formula_integration_quality: float = 1.0

class MathematicalConsciousnessBridge:
    """
    Bridge between mathematical consciousness formulas and operational systems
    
    This class orchestrates the influence of SHI, Cognitive Pressure, and
    other mathematical models on DAWN's real-time behavior and responses.
    """
    
    def __init__(self):
        """Initialize the mathematical consciousness bridge"""
        
        # Core mathematical engines
        self.shi_engine = get_schema_health_index()
        self.pressure_engine = get_cognitive_pressure_physics()
        self.drift_resolver = get_scup_drift_resolver()
        
        # Integration state
        self.current_influence = MathematicalInfluence()
        self.last_calculation_time = 0.0
        self.calculation_interval = 1.0  # Calculate every second
        
        # System integrations
        self.voice_modulator = None
        self.rebloom_reflex = None
        self.reflection_engine = None
        
        # Behavior modification callbacks
        self.tick_modifier_callbacks: List[Callable] = []
        self.reflection_modifier_callbacks: List[Callable] = []
        self.voice_modifier_callbacks: List[Callable] = []
        self.rebloom_modifier_callbacks: List[Callable] = []
        
        # Performance tracking
        self.integration_count = 0
        self.successful_integrations = 0
        self.formula_calculation_time = 0.0
        
        # Historical influence tracking
        self.influence_history: List[Tuple[float, MathematicalInfluence]] = []
        self.max_history = 50
        
        self._initialize_system_integrations()
        
        logger.info("🧮 [MATH-BRIDGE] Mathematical Consciousness Bridge initialized")
        logger.info(f"🧮 [MATH-BRIDGE] Voice modulation: {VOICE_AVAILABLE}")
        logger.info(f"🧮 [MATH-BRIDGE] Rebloom integration: {REBLOOM_AVAILABLE}")  
        logger.info(f"🧮 [MATH-BRIDGE] Reflection integration: {REFLECTION_AVAILABLE}")
    
    def _initialize_system_integrations(self):
        """Initialize connections to DAWN subsystems"""
        
        # Voice modulation integration
        if VOICE_AVAILABLE:
            try:
                self.voice_modulator = VoiceMoodModulator()
                logger.info("🧮 [MATH-BRIDGE] Voice modulator connected")
            except Exception as e:
                logger.warning(f"🧮 [MATH-BRIDGE] Voice modulator failed: {e}")
        
        # Rebloom reflex integration
        if REBLOOM_AVAILABLE:
            try:
                self.rebloom_reflex = MemoryRebloomReflex()
                logger.info("🧮 [MATH-BRIDGE] Rebloom reflex connected")
            except Exception as e:
                logger.warning(f"🧮 [MATH-BRIDGE] Rebloom reflex failed: {e}")
        
        # Reflection engine integration
        if REFLECTION_AVAILABLE:
            try:
                self.reflection_engine = ReflectionEngine()
                logger.info("🧮 [MATH-BRIDGE] Reflection engine connected")
            except Exception as e:
                logger.warning(f"🧮 [MATH-BRIDGE] Reflection engine failed: {e}")
    
    def calculate_mathematical_influence(self, state: Dict[str, Any]) -> MathematicalInfluence:
        """
        Calculate comprehensive mathematical influence on cognitive systems
        
        Args:
            state: DAWN cognitive state containing all metrics
            
        Returns:
            MathematicalInfluence object with modulation parameters
        """
        calc_start = time.time()
        
        try:
            # Calculate core mathematical values
            shi_value = self.shi_engine.calculate_shi(state)
            pressure_value = self.pressure_engine.calculate_cognitive_pressure(state)
            drift_coherence = self.drift_resolver.resolve_drift_coherence(state)
            
            # Get system-specific modulations from SHI
            shi_reflection_mod = self.shi_engine.get_modulation_for_system("reflection")
            shi_voice_mod = self.shi_engine.get_modulation_for_system("voice")
            shi_rebloom_mod = self.shi_engine.get_modulation_for_system("rebloom")
            shi_tick_mod = self.shi_engine.get_modulation_for_system("tick")
            
            # Get pressure-based modulations
            pressure_mod = self.pressure_engine.get_pressure_modulation()
            
            # Get drift-based modulations
            drift_mod = self.drift_resolver.get_drift_modulation()
            
            # Combine modulations from multiple mathematical sources
            combined_influence = MathematicalInfluence(
                shi_value=shi_value,
                shi_zone=self.shi_engine.current_zone.value,
                pressure_value=pressure_value,
                pressure_zone=self.pressure_engine.current_state.pressure_zone.value,
                
                # Tick timing influenced by both SHI and pressure
                tick_interval_modifier=(
                    shi_tick_mod.get("interval_preference", 1.0) * 0.6 +
                    pressure_mod.get("tick_speed_modifier", 1.0) * 0.4
                ),
                
                # Reflection modulation - SHI primary, pressure secondary
                reflection_frequency=(
                    shi_reflection_mod.get("frequency_multiplier", 1.0) * 0.7 +
                    pressure_mod.get("reflection_urgency", 1.0) * 0.3
                ),
                reflection_depth=shi_reflection_mod.get("depth_factor", 1.0),
                
                # Voice modulation - primarily SHI driven
                voice_mutation_rate=shi_voice_mod.get("mutation_rate", 0.1),
                voice_stability=shi_voice_mod.get("stability_factor", 1.0),
                
                # Rebloom modulation - both systems contribute
                rebloom_threshold=(
                    shi_rebloom_mod.get("threshold_modifier", 0.0) * 0.5 +
                    (pressure_mod.get("rebloom_sensitivity", 1.0) - 1.0) * 0.5
                ),
                rebloom_urgency=(
                    shi_rebloom_mod.get("urgency_multiplier", 1.0) * 0.6 +
                    pressure_mod.get("rebloom_sensitivity", 1.0) * 0.4
                ),
                
                # Emotional and cognitive factors
                emotional_stability=self.shi_engine.modulation.emotional_stability,
                attention_focus=(
                    self.shi_engine.modulation.attention_focus_factor * 0.7 +
                    (1.0 - pressure_mod.get("attention_scatter", 0.0)) * 0.3
                ),
                
                # Meta-cognitive coherence (now includes drift)
                consciousness_coherence=self._calculate_consciousness_coherence(shi_value, pressure_value, drift_coherence),
                mathematical_alignment=self._calculate_mathematical_alignment(state),
                formula_integration_quality=self._calculate_integration_quality()
            )
            
            # Update state
            self.current_influence = combined_influence
            self.last_calculation_time = time.time()
            self.integration_count += 1
            
            # Record calculation time
            self.formula_calculation_time = time.time() - calc_start
            
            # Record in history
            self.influence_history.append((time.time(), combined_influence))
            if len(self.influence_history) > self.max_history:
                self.influence_history.pop(0)
            
            logger.debug(f"🧮 [MATH-BRIDGE] Influence calculated: SHI={shi_value:.3f}({self.shi_engine.current_zone.value}), P={pressure_value:.3f}({self.pressure_engine.current_state.pressure_zone.value})")
            
            return combined_influence
            
        except Exception as e:
            logger.error(f"🧮 [MATH-BRIDGE] Calculation error: {e}")
            return self.current_influence  # Return last known good state
    
    def apply_mathematical_influence(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply mathematical influence to modify DAWN's behavior
        
        Args:
            state: Current DAWN state
            
        Returns:
            Modified state with mathematical influence applied
        """
        try:
            # Calculate current mathematical influence
            influence = self.calculate_mathematical_influence(state)
            
            # Apply tick timing modification
            if "tick_interval" in state:
                original_interval = state["tick_interval"]
                modified_interval = original_interval * influence.tick_interval_modifier
                state["tick_interval"] = max(0.5, min(5.0, modified_interval))  # Bounds check
                
                if abs(modified_interval - original_interval) > 0.1:
                    logger.info(f"🧮 [MATH-BRIDGE] Tick interval: {original_interval:.2f}s → {modified_interval:.2f}s")
            
            # Apply voice modulation if available
            if self.voice_modulator and "mood" in state:
                try:
                    # Modify voice parameters based on mathematical influence
                    voice_mood = self._map_influence_to_voice_mood(influence)
                    state["voice_modulation"] = {
                        "mood": voice_mood,
                        "mutation_rate": influence.voice_mutation_rate,
                        "stability": influence.voice_stability
                    }
                except Exception as e:
                    logger.warning(f"🧮 [MATH-BRIDGE] Voice modulation failed: {e}")
            
            # Apply reflection modulation
            state["reflection_modulation"] = {
                "frequency_multiplier": influence.reflection_frequency,
                "depth_factor": influence.reflection_depth,
                "urgency": influence.reflection_frequency > 1.3
            }
            
            # Apply rebloom modulation if available  
            if self.rebloom_reflex:
                state["rebloom_modulation"] = {
                    "threshold_modifier": influence.rebloom_threshold,
                    "urgency_multiplier": influence.rebloom_urgency,
                    "sensitivity_boost": influence.pressure_value > 0.8
                }
            
            # Add mathematical consciousness metadata
            state["mathematical_consciousness"] = {
                "shi_value": influence.shi_value,
                "shi_zone": influence.shi_zone,
                "pressure_value": influence.pressure_value,
                "pressure_zone": influence.pressure_zone,
                "consciousness_coherence": influence.consciousness_coherence,
                "formula_integration_active": True,
                "last_calculation_time": self.last_calculation_time
            }
            
            # Apply attention and focus modifications
            state["attention_modulation"] = {
                "focus_factor": influence.attention_focus,
                "stability": influence.emotional_stability,
                "scatter_risk": 1.0 - influence.attention_focus
            }
            
            # Execute registered callbacks
            self._execute_modifier_callbacks(state, influence)
            
            self.successful_integrations += 1
            
            return state
            
        except Exception as e:
            logger.error(f"🧮 [MATH-BRIDGE] Application error: {e}")
            return state  # Return unmodified state on error
    
    def _calculate_consciousness_coherence(self, shi_value: float, pressure_value: float, drift_coherence: float) -> float:
        """Calculate overall consciousness coherence from mathematical metrics"""
        
        # SHI contributes positively to coherence
        shi_contribution = shi_value
        
        # Moderate pressure contributes to coherence, extreme pressure detracts
        optimal_pressure = 0.4
        pressure_contribution = 1.0 - abs(pressure_value - optimal_pressure) / optimal_pressure
        pressure_contribution = max(0.0, pressure_contribution)
        
        # Drift coherence provides semantic stability
        drift_contribution = drift_coherence
        
        # Balance between stability (SHI), dynamic activity (pressure), and semantic coherence (drift)
        coherence = (shi_contribution * 0.5 + pressure_contribution * 0.2 + drift_contribution * 0.3)
        
        return max(0.0, min(1.0, coherence))
    
    def _calculate_mathematical_alignment(self, state: Dict[str, Any]) -> float:
        """Calculate how well mathematical models align with actual system state"""
        
        # Check if SHI predictions match system behavior
        predicted_stability = self.current_influence.emotional_stability
        actual_entropy = state.get("entropy", 0.5)
        actual_stability = 1.0 - actual_entropy
        stability_alignment = 1.0 - abs(predicted_stability - actual_stability)
        
        # Check if pressure predictions match system stress
        predicted_pressure_zone = self.current_influence.pressure_zone
        actual_heat = state.get("heat", 25.0) / 100.0
        pressure_alignment = 1.0 if actual_heat > 0.6 and "CRITICAL" in predicted_pressure_zone else 0.7
        
        # Overall mathematical alignment
        alignment = (stability_alignment * 0.6 + pressure_alignment * 0.4)
        
        return max(0.0, min(1.0, alignment))
    
    def _calculate_integration_quality(self) -> float:
        """Calculate quality of mathematical integration with operational systems"""
        
        if self.integration_count == 0:
            return 0.5
        
        # Success rate of integrations
        success_rate = self.successful_integrations / self.integration_count
        
        # Performance factor (fast calculations are better)
        performance_factor = max(0.5, min(1.0, 1.0 - self.formula_calculation_time * 10))
        
        # Integration completeness (how many systems are connected)
        completeness = 0.0
        if VOICE_AVAILABLE and self.voice_modulator:
            completeness += 0.33
        if REBLOOM_AVAILABLE and self.rebloom_reflex:
            completeness += 0.33
        if REFLECTION_AVAILABLE and self.reflection_engine:
            completeness += 0.34
        
        quality = (success_rate * 0.5 + performance_factor * 0.3 + completeness * 0.2)
        
        return max(0.0, min(1.0, quality))
    
    def _map_influence_to_voice_mood(self, influence: MathematicalInfluence) -> str:
        """Map mathematical influence to voice mood categories"""
        
        if influence.shi_zone == "THRIVING":
            return "CONFIDENT"
        elif influence.shi_zone == "STABLE":
            return "CALM"
        elif influence.shi_zone == "STRESSED":
            if influence.pressure_zone in ["CRITICAL", "OVERFLOW"]:
                return "ANXIOUS"
            else:
                return "FOCUSED"
        elif influence.shi_zone == "CRITICAL":
            return "UNCERTAIN"
        else:  # COLLAPSE
            return "DRIFTING"
    
    def _execute_modifier_callbacks(self, state: Dict[str, Any], influence: MathematicalInfluence):
        """Execute registered behavior modifier callbacks"""
        
        # Execute tick modifier callbacks
        for callback in self.tick_modifier_callbacks:
            try:
                callback(state, influence.tick_interval_modifier)
            except Exception as e:
                logger.warning(f"🧮 [MATH-BRIDGE] Tick callback error: {e}")
        
        # Execute reflection modifier callbacks
        for callback in self.reflection_modifier_callbacks:
            try:
                callback(state, influence.reflection_frequency, influence.reflection_depth)
            except Exception as e:
                logger.warning(f"🧮 [MATH-BRIDGE] Reflection callback error: {e}")
        
        # Execute voice modifier callbacks
        for callback in self.voice_modifier_callbacks:
            try:
                callback(state, influence.voice_mutation_rate, influence.voice_stability)
            except Exception as e:
                logger.warning(f"🧮 [MATH-BRIDGE] Voice callback error: {e}")
        
        # Execute rebloom modifier callbacks
        for callback in self.rebloom_modifier_callbacks:
            try:
                callback(state, influence.rebloom_threshold, influence.rebloom_urgency)
            except Exception as e:
                logger.warning(f"🧮 [MATH-BRIDGE] Rebloom callback error: {e}")
    
    def register_tick_modifier(self, callback: Callable):
        """Register callback for tick modification"""
        self.tick_modifier_callbacks.append(callback)
        logger.info(f"🧮 [MATH-BRIDGE] Registered tick modifier callback")
    
    def register_reflection_modifier(self, callback: Callable):
        """Register callback for reflection modification"""
        self.reflection_modifier_callbacks.append(callback)
        logger.info(f"🧮 [MATH-BRIDGE] Registered reflection modifier callback")
    
    def register_voice_modifier(self, callback: Callable):
        """Register callback for voice modification"""
        self.voice_modifier_callbacks.append(callback)
        logger.info(f"🧮 [MATH-BRIDGE] Registered voice modifier callback")
    
    def register_rebloom_modifier(self, callback: Callable):
        """Register callback for rebloom modification"""
        self.rebloom_modifier_callbacks.append(callback)
        logger.info(f"🧮 [MATH-BRIDGE] Registered rebloom modifier callback")
    
    def get_mathematical_status(self) -> Dict[str, Any]:
        """Get comprehensive status of mathematical consciousness integration"""
        
        influence_trend = self._calculate_influence_trend()
        
        return {
            "current_influence": {
                "shi_value": self.current_influence.shi_value,
                "shi_zone": self.current_influence.shi_zone,
                "pressure_value": self.current_influence.pressure_value,
                "pressure_zone": self.current_influence.pressure_zone,
                "consciousness_coherence": self.current_influence.consciousness_coherence,
                "mathematical_alignment": self.current_influence.mathematical_alignment
            },
            "modulation_active": {
                "tick_interval": self.current_influence.tick_interval_modifier != 1.0,
                "reflection": self.current_influence.reflection_frequency != 1.0,
                "voice": self.current_influence.voice_mutation_rate != 0.1,
                "rebloom": self.current_influence.rebloom_threshold != 0.0,
                "attention": self.current_influence.attention_focus != 1.0
            },
            "integration_quality": {
                "total_calculations": self.integration_count,
                "successful_integrations": self.successful_integrations,
                "success_rate": self.successful_integrations / max(1, self.integration_count),
                "avg_calculation_time_ms": self.formula_calculation_time * 1000,
                "integration_quality": self.current_influence.formula_integration_quality
            },
            "system_connections": {
                "voice_modulator": self.voice_modulator is not None,
                "rebloom_reflex": self.rebloom_reflex is not None,
                "reflection_engine": self.reflection_engine is not None,
                "callback_count": {
                    "tick": len(self.tick_modifier_callbacks),
                    "reflection": len(self.reflection_modifier_callbacks),
                    "voice": len(self.voice_modifier_callbacks),
                    "rebloom": len(self.rebloom_modifier_callbacks)
                }
            },
            "trends": influence_trend
        }
    
    def _calculate_influence_trend(self) -> Dict[str, float]:
        """Calculate trends in mathematical influence over time"""
        if len(self.influence_history) < 2:
            return {"shi_trend": 0.0, "pressure_trend": 0.0}
        
        # Get recent SHI and pressure values
        recent_shi = [inf.shi_value for _, inf in self.influence_history[-10:]]
        recent_pressure = [inf.pressure_value for _, inf in self.influence_history[-10:]]
        
        # Calculate simple trends
        shi_trend = (recent_shi[-1] - recent_shi[0]) / len(recent_shi) if recent_shi else 0.0
        pressure_trend = (recent_pressure[-1] - recent_pressure[0]) / len(recent_pressure) if recent_pressure else 0.0
        
        return {
            "shi_trend": shi_trend,
            "pressure_trend": pressure_trend,
            "coherence_average": sum(inf.consciousness_coherence for _, inf in self.influence_history[-5:]) / min(5, len(self.influence_history))
        }
    
    def should_recalculate(self) -> bool:
        """Check if mathematical influence should be recalculated"""
        return (time.time() - self.last_calculation_time) >= self.calculation_interval


# Global mathematical consciousness bridge
_global_bridge_instance: Optional[MathematicalConsciousnessBridge] = None

def get_mathematical_consciousness_bridge() -> MathematicalConsciousnessBridge:
    """Get global mathematical consciousness bridge instance"""
    global _global_bridge_instance
    if _global_bridge_instance is None:
        _global_bridge_instance = MathematicalConsciousnessBridge()
    return _global_bridge_instance

def apply_mathematical_consciousness(state: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to apply mathematical consciousness to a state"""
    bridge = get_mathematical_consciousness_bridge()
    return bridge.apply_mathematical_influence(state)

def get_mathematical_status() -> Dict[str, Any]:
    """Convenience function to get mathematical consciousness status"""
    bridge = get_mathematical_consciousness_bridge()
    return bridge.get_mathematical_status()

# Export key classes and functions
__all__ = [
    'MathematicalConsciousnessBridge',
    'MathematicalInfluence',
    'get_mathematical_consciousness_bridge',
    'apply_mathematical_consciousness',
    'get_mathematical_status'
] 