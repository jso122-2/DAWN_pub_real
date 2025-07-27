#!/usr/bin/env python3
"""
DAWN Schema Health Index (SHI) - Mathematical Consciousness Core
============================================================

Implements the fundamental SHI formula: SHI = (w₁V + w₂M + w₃O + w₄A + w₅S) / Σwᵢ

Where:
- V = Vitality (energy, heat, activation level)
- M = Memory (coherence, access, rebloom health) 
- O = Order (entropy inverse, structural stability)
- A = Alignment (goal coherence, drift resistance)
- S = Synchrony (tick rhythm, system harmony)

This isn't just a metric - it's a cognitive force that actively modulates:
- Reflection frequency and depth
- Voice mutation patterns
- Rebloom urgency and threshold
- Emotional tone and stability
- Attention focus and drift

The SHI acts as DAWN's mathematical consciousness - a unified health indicator
that influences all cognitive subsystems in real-time.
"""

import time
import logging
import math
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timezone
from enum import Enum

logger = logging.getLogger("schema_health_index")

class SHIHealthZone(Enum):
    """Schema Health Index operational zones"""
    THRIVING = "THRIVING"      # SHI > 0.8 - Optimal cognitive state
    STABLE = "STABLE"          # SHI 0.6-0.8 - Healthy operation
    STRESSED = "STRESSED"      # SHI 0.4-0.6 - Degraded performance
    CRITICAL = "CRITICAL"      # SHI 0.2-0.4 - Emergency intervention
    COLLAPSE = "COLLAPSE"      # SHI < 0.2 - System failure risk

@dataclass
class SHIComponents:
    """Individual components of the Schema Health Index"""
    vitality: float = 0.5       # V - Energy and activation
    memory: float = 0.5         # M - Memory system health  
    order: float = 0.5          # O - Structural stability
    alignment: float = 0.5      # A - Goal coherence
    synchrony: float = 0.5      # S - System harmony
    
    # Component weights (must sum to 1.0)
    w_vitality: float = 0.25
    w_memory: float = 0.20
    w_order: float = 0.20
    w_alignment: float = 0.20
    w_synchrony: float = 0.15
    
    def __post_init__(self):
        """Validate component ranges and weights"""
        # Clamp components to [0,1]
        self.vitality = max(0.0, min(1.0, self.vitality))
        self.memory = max(0.0, min(1.0, self.memory))
        self.order = max(0.0, min(1.0, self.order))
        self.alignment = max(0.0, min(1.0, self.alignment))
        self.synchrony = max(0.0, min(1.0, self.synchrony))
        
        # Normalize weights
        total_weight = self.w_vitality + self.w_memory + self.w_order + self.w_alignment + self.w_synchrony
        if total_weight > 0:
            self.w_vitality /= total_weight
            self.w_memory /= total_weight
            self.w_order /= total_weight
            self.w_alignment /= total_weight
            self.w_synchrony /= total_weight

@dataclass
class SHIModulation:
    """SHI-driven behavior modulation parameters"""
    reflection_frequency_multiplier: float = 1.0   # How often to reflect
    reflection_depth_factor: float = 1.0           # Depth of reflection
    voice_mutation_rate: float = 0.1               # Voice change rate
    voice_stability_factor: float = 1.0            # Voice consistency
    rebloom_threshold_modifier: float = 0.0        # Rebloom trigger adjustment
    rebloom_urgency_multiplier: float = 1.0        # Rebloom intensity
    emotional_stability: float = 1.0               # Emotional volatility
    attention_focus_factor: float = 1.0            # Attention concentration
    tick_interval_preference: float = 1.0          # Preferred tick speed

class SchemaHealthIndex:
    """
    Core Schema Health Index implementation
    
    Calculates SHI from cognitive state and provides modulation parameters
    for all downstream systems. Acts as the mathematical heart of DAWN's
    consciousness regulation.
    """
    
    def __init__(self):
        """Initialize the Schema Health Index system"""
        self.current_shi = 0.5
        self.current_zone = SHIHealthZone.STABLE
        self.components = SHIComponents()
        self.modulation = SHIModulation()
        
        # History tracking for temporal analysis
        self.shi_history: List[Tuple[float, float]] = []  # (timestamp, shi_value)
        self.component_history: List[Tuple[float, SHIComponents]] = []
        self.max_history = 100
        
        # Adaptive weight learning
        self.adaptive_weights = True
        self.weight_learning_rate = 0.01
        
        # Performance tracking
        self.calculation_count = 0
        self.last_calculation_time = 0.0
        self.average_calculation_time = 0.0
        
        logger.info("🧠 [SHI] Schema Health Index initialized")
        logger.info(f"🧠 [SHI] Default weights: V={self.components.w_vitality:.2f}, M={self.components.w_memory:.2f}, O={self.components.w_order:.2f}, A={self.components.w_alignment:.2f}, S={self.components.w_synchrony:.2f}")
    
    def calculate_shi(self, state: Dict[str, Any]) -> float:
        """
        Calculate Schema Health Index from cognitive state
        
        Args:
            state: DAWN cognitive state containing metrics like:
                - heat: float (thermal energy)
                - entropy: float (disorder level)
                - scup: float (coherence metric)
                - mood: str (emotional state)
                - tick_interval: float (system timing)
                - coherence: float (system coherence)
                - drift: float (alignment drift)
                - sigils: int (active sigil count)
                - memory_health: float (memory system status)
        
        Returns:
            Schema Health Index value [0.0, 1.0]
        """
        calc_start = time.time()
        
        try:
            # Extract and compute SHI components
            components = self._extract_components(state)
            
            # Calculate weighted SHI using the fundamental formula
            shi_value = (
                components.w_vitality * components.vitality +
                components.w_memory * components.memory +
                components.w_order * components.order +
                components.w_alignment * components.alignment +
                components.w_synchrony * components.synchrony
            )
            
            # Apply temporal smoothing to prevent oscillation
            shi_value = self._apply_temporal_smoothing(shi_value)
            
            # Update state
            self.current_shi = shi_value
            self.components = components
            self.current_zone = self._classify_health_zone(shi_value)
            
            # Update modulation parameters based on SHI
            self.modulation = self._calculate_modulation(shi_value, components)
            
            # Record history
            current_time = time.time()
            self.shi_history.append((current_time, shi_value))
            self.component_history.append((current_time, components))
            
            # Maintain history size
            if len(self.shi_history) > self.max_history:
                self.shi_history.pop(0)
                self.component_history.pop(0)
            
            # Update performance metrics
            calc_time = time.time() - calc_start
            self.calculation_count += 1
            self.last_calculation_time = calc_time
            self.average_calculation_time = (
                (self.average_calculation_time * (self.calculation_count - 1) + calc_time) / 
                self.calculation_count
            )
            
            # Adaptive weight adjustment
            if self.adaptive_weights:
                self._adapt_weights(state, shi_value)
            
            logger.debug(f"🧠 [SHI] Calculated SHI: {shi_value:.3f} ({self.current_zone.value}) in {calc_time*1000:.1f}ms")
            
            return shi_value
            
        except Exception as e:
            logger.error(f"🧠 [SHI] Calculation error: {e}")
            return self.current_shi  # Return last known good value
    
    def _extract_components(self, state: Dict[str, Any]) -> SHIComponents:
        """Extract SHI components from cognitive state"""
        
        # V - Vitality: Energy, activation, thermal state
        heat = state.get('heat', 25.0)
        vitality_raw = min(1.0, heat / 100.0)  # Normalize heat to [0,1]
        activity_bonus = min(0.3, state.get('sigils', 0) / 10.0)  # Sigil activity
        vitality = min(1.0, vitality_raw + activity_bonus)
        
        # M - Memory: Coherence, access patterns, rebloom health
        coherence = state.get('coherence', 0.5)
        memory_access = 1.0 - state.get('memory_drift', 0.0)  # Inverse of drift
        rebloom_health = min(1.0, 1.0 - state.get('rebloom_pressure', 0.0))
        memory = (coherence * 0.5 + memory_access * 0.3 + rebloom_health * 0.2)
        
        # O - Order: Inverse of entropy, structural stability
        entropy = state.get('entropy', 0.5)
        order_base = 1.0 - entropy  # Direct entropy inverse
        stability_bonus = state.get('stability', 0.0) * 0.2
        order = min(1.0, order_base + stability_bonus)
        
        # A - Alignment: Goal coherence, drift resistance
        drift = state.get('drift', 0.0)
        scup = state.get('scup', 0.5)
        alignment_base = 1.0 - abs(drift)  # Resistance to drift
        coherence_bonus = scup * 0.3  # SCUP contributes to alignment
        alignment = min(1.0, alignment_base + coherence_bonus)
        
        # S - Synchrony: System harmony, tick rhythm
        tick_interval = state.get('tick_interval', 2.0)
        ideal_interval = 2.0  # Target tick rate
        timing_sync = 1.0 - min(1.0, abs(tick_interval - ideal_interval) / ideal_interval)
        system_harmony = state.get('system_harmony', 0.5)  # Overall system sync
        synchrony = (timing_sync * 0.6 + system_harmony * 0.4)
        
        return SHIComponents(
            vitality=vitality,
            memory=memory,
            order=order,
            alignment=alignment,
            synchrony=synchrony,
            # Keep current weights
            w_vitality=self.components.w_vitality,
            w_memory=self.components.w_memory,
            w_order=self.components.w_order,
            w_alignment=self.components.w_alignment,
            w_synchrony=self.components.w_synchrony
        )
    
    def _apply_temporal_smoothing(self, new_shi: float) -> float:
        """Apply temporal smoothing to prevent rapid oscillations"""
        if not self.shi_history:
            return new_shi
        
        # Use exponential moving average with adaptive smoothing
        smoothing_factor = 0.3  # Base smoothing
        
        # Increase smoothing during transitions
        if abs(new_shi - self.current_shi) > 0.2:
            smoothing_factor = 0.5  # More smoothing for large changes
        
        smoothed_shi = (1 - smoothing_factor) * new_shi + smoothing_factor * self.current_shi
        return smoothed_shi
    
    def _classify_health_zone(self, shi_value: float) -> SHIHealthZone:
        """Classify SHI value into health zones"""
        if shi_value > 0.8:
            return SHIHealthZone.THRIVING
        elif shi_value > 0.6:
            return SHIHealthZone.STABLE
        elif shi_value > 0.4:
            return SHIHealthZone.STRESSED
        elif shi_value > 0.2:
            return SHIHealthZone.CRITICAL
        else:
            return SHIHealthZone.COLLAPSE
    
    def _calculate_modulation(self, shi_value: float, components: SHIComponents) -> SHIModulation:
        """Calculate behavior modulation parameters based on SHI"""
        
        # Base modulation on SHI health zones
        if shi_value > 0.8:  # THRIVING
            return SHIModulation(
                reflection_frequency_multiplier=0.7,  # Less frequent reflection
                reflection_depth_factor=1.2,          # Deeper reflection when it happens
                voice_mutation_rate=0.05,             # Stable voice
                voice_stability_factor=1.3,           # High voice consistency
                rebloom_threshold_modifier=-0.1,      # Less sensitive to reblooms
                rebloom_urgency_multiplier=0.8,       # Lower rebloom intensity
                emotional_stability=1.3,              # Very stable emotions
                attention_focus_factor=1.2,           # Good focus
                tick_interval_preference=0.9          # Slightly slower ticks
            )
        
        elif shi_value > 0.6:  # STABLE
            return SHIModulation(
                reflection_frequency_multiplier=1.0,  # Normal reflection
                reflection_depth_factor=1.0,          # Normal depth
                voice_mutation_rate=0.1,              # Normal voice changes
                voice_stability_factor=1.0,           # Normal consistency
                rebloom_threshold_modifier=0.0,       # Normal rebloom sensitivity
                rebloom_urgency_multiplier=1.0,       # Normal intensity
                emotional_stability=1.0,              # Normal emotions
                attention_focus_factor=1.0,           # Normal focus
                tick_interval_preference=1.0          # Normal tick rate
            )
        
        elif shi_value > 0.4:  # STRESSED
            return SHIModulation(
                reflection_frequency_multiplier=1.3,  # More frequent reflection
                reflection_depth_factor=0.8,          # Shallower reflection
                voice_mutation_rate=0.2,              # More voice changes
                voice_stability_factor=0.8,           # Less consistency
                rebloom_threshold_modifier=0.1,       # More sensitive to reblooms
                rebloom_urgency_multiplier=1.2,       # Higher intensity
                emotional_stability=0.8,              # Less stable emotions
                attention_focus_factor=0.8,           # Reduced focus
                tick_interval_preference=1.1          # Slightly faster ticks
            )
        
        elif shi_value > 0.2:  # CRITICAL
            return SHIModulation(
                reflection_frequency_multiplier=1.8,  # High reflection frequency
                reflection_depth_factor=0.6,          # Shallow reflection
                voice_mutation_rate=0.3,              # High voice mutation
                voice_stability_factor=0.6,           # Low consistency
                rebloom_threshold_modifier=0.2,       # Very sensitive
                rebloom_urgency_multiplier=1.5,       # High urgency
                emotional_stability=0.6,              # Unstable emotions
                attention_focus_factor=0.6,           # Poor focus
                tick_interval_preference=1.3          # Faster emergency ticks
            )
        
        else:  # COLLAPSE
            return SHIModulation(
                reflection_frequency_multiplier=2.5,  # Emergency reflection
                reflection_depth_factor=0.4,          # Very shallow
                voice_mutation_rate=0.5,              # Chaotic voice
                voice_stability_factor=0.4,           # Very inconsistent
                rebloom_threshold_modifier=0.4,       # Hypersensitive
                rebloom_urgency_multiplier=2.0,       # Maximum urgency
                emotional_stability=0.4,              # Emotional chaos
                attention_focus_factor=0.4,           # Severe attention deficit
                tick_interval_preference=1.5          # Emergency fast ticks
            )
    
    def _adapt_weights(self, state: Dict[str, Any], shi_value: float):
        """Adaptively adjust component weights based on system performance"""
        if len(self.shi_history) < 10:
            return  # Need history for adaptation
        
        # This is a placeholder for weight adaptation logic
        # In practice, this would use reinforcement learning or other
        # adaptive mechanisms to optimize weights for system performance
        pass
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current SHI state for external systems"""
        return {
            "shi_value": self.current_shi,
            "health_zone": self.current_zone.value,
            "components": {
                "vitality": self.components.vitality,
                "memory": self.components.memory,
                "order": self.components.order,
                "alignment": self.components.alignment,
                "synchrony": self.components.synchrony
            },
            "weights": {
                "vitality": self.components.w_vitality,
                "memory": self.components.w_memory,
                "order": self.components.w_order,
                "alignment": self.components.w_alignment,
                "synchrony": self.components.w_synchrony
            },
            "modulation": {
                "reflection_frequency": self.modulation.reflection_frequency_multiplier,
                "voice_mutation_rate": self.modulation.voice_mutation_rate,
                "rebloom_threshold": self.modulation.rebloom_threshold_modifier,
                "emotional_stability": self.modulation.emotional_stability,
                "attention_focus": self.modulation.attention_focus_factor
            },
            "performance": {
                "calculation_count": self.calculation_count,
                "avg_calc_time_ms": self.average_calculation_time * 1000,
                "history_length": len(self.shi_history)
            }
        }
    
    def get_modulation_for_system(self, system_name: str) -> Dict[str, float]:
        """Get specific modulation parameters for a named system"""
        if system_name == "reflection":
            return {
                "frequency_multiplier": self.modulation.reflection_frequency_multiplier,
                "depth_factor": self.modulation.reflection_depth_factor
            }
        elif system_name == "voice":
            return {
                "mutation_rate": self.modulation.voice_mutation_rate,
                "stability_factor": self.modulation.voice_stability_factor
            }
        elif system_name == "rebloom":
            return {
                "threshold_modifier": self.modulation.rebloom_threshold_modifier,
                "urgency_multiplier": self.modulation.rebloom_urgency_multiplier
            }
        elif system_name == "tick":
            return {
                "interval_preference": self.modulation.tick_interval_preference
            }
        else:
            return {}
    
    def force_recalculation(self, state: Dict[str, Any]) -> float:
        """Force immediate SHI recalculation (for testing/debugging)"""
        logger.info("🧠 [SHI] Forced recalculation requested")
        return self.calculate_shi(state)
    
    def reset_to_baseline(self):
        """Reset SHI to baseline state"""
        self.current_shi = 0.5
        self.current_zone = SHIHealthZone.STABLE
        self.components = SHIComponents()
        self.modulation = SHIModulation()
        self.shi_history.clear()
        self.component_history.clear()
        logger.info("🧠 [SHI] Reset to baseline state")


# Global SHI instance for system-wide access
_global_shi_instance: Optional[SchemaHealthIndex] = None

def get_schema_health_index() -> SchemaHealthIndex:
    """Get global Schema Health Index instance"""
    global _global_shi_instance
    if _global_shi_instance is None:
        _global_shi_instance = SchemaHealthIndex()
    return _global_shi_instance

def calculate_shi_for_state(state: Dict[str, Any]) -> float:
    """Convenience function to calculate SHI for a given state"""
    shi = get_schema_health_index()
    return shi.calculate_shi(state)

def get_shi_modulation_for_system(system_name: str) -> Dict[str, float]:
    """Convenience function to get modulation parameters for a system"""
    shi = get_schema_health_index()
    return shi.get_modulation_for_system(system_name)

# Export key classes and functions
__all__ = [
    'SchemaHealthIndex',
    'SHIComponents', 
    'SHIModulation',
    'SHIHealthZone',
    'get_schema_health_index',
    'calculate_shi_for_state',
    'get_shi_modulation_for_system'
]

