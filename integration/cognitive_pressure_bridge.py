#!/usr/bin/env python3
"""
DAWN Cognitive Pressure Bridge - Formula Integration
===================================================

Integrates cognitive pressure formulas (P = Bσ²) into the conversation system's
consciousness state management. This bridge connects the existing cognitive pressure
physics with the conversation response generation system.

Features:
- Real-time cognitive pressure calculation during conversations
- Pressure-based response strategy modulation
- Integration with existing consciousness state management
- Schema Health Index (SHI) calculation and monitoring
- Pressure relief recommendations for conversation flow
"""

import time
import logging
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

# Import existing cognitive pressure systems
try:
    from core.cognitive_formulas import get_dawn_formula_engine, CognitivePressureReading
    from core.cognitive_pressure_physics import CognitivePressurePhysics, PressureZone
    from core.scup_drift_resolver import get_scup_drift_resolver
    FORMULA_SYSTEMS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Cognitive pressure systems not available: {e}")
    FORMULA_SYSTEMS_AVAILABLE = False

logger = logging.getLogger("cognitive_pressure_bridge")

@dataclass
class EnhancedConsciousnessState:
    """Enhanced consciousness state with cognitive pressure integration"""
    
    # Core consciousness metrics
    scup: float = 50.0  # System Consciousness Unity Percentage
    entropy: float = 0.5  # Chaos level (0-1)
    mood: str = "CONTEMPLATIVE"
    thermal_zone: str = "CALM"
    
    # Cognitive pressure integration
    cognitive_pressure: float = 0.0  # P = Bσ² value
    pressure_zone: str = "CALM"  # Pressure zone classification
    shi_score: float = 0.5  # Schema Health Index
    instability_risk: float = 0.0  # Risk of cognitive cascade
    
    # Bloom mass components (B in P = Bσ²)
    bloom_mass: float = 0.0
    active_memory_count: int = 0
    rebloom_queue_size: int = 0
    reflection_backlog: int = 0
    processing_load: float = 0.0
    
    # Sigil velocity components (σ in P = Bσ²)
    sigil_velocity: float = 0.0
    recent_sigil_count: int = 0
    thought_rate: float = 0.0
    entropy_delta: float = 0.0
    mutation_rate: float = 0.0
    
    # Timestamp and tracking
    timestamp: float = field(default_factory=time.time)
    pressure_history: list = field(default_factory=list)
    
    def update_with_formulas(self, state_data: Dict[str, Any]) -> None:
        """Update consciousness state with cognitive pressure formulas"""
        if not FORMULA_SYSTEMS_AVAILABLE:
            logger.warning("Cognitive pressure formulas not available")
            return
        
        try:
            # Update core metrics
            self.scup = state_data.get('scup', self.scup)
            self.entropy = state_data.get('entropy', self.entropy)
            self.mood = state_data.get('mood', self.mood)
            self.thermal_zone = state_data.get('thermal_zone', self.thermal_zone)
            
            # Calculate cognitive pressure using existing formula engine
            formula_engine = get_dawn_formula_engine()
            pressure_reading = formula_engine.calculate_pressure(state_data)
            
            # Update pressure-related metrics
            self.cognitive_pressure = pressure_reading.pressure_value
            self.pressure_zone = pressure_reading.pressure_level.value
            
            # Extract bloom mass and sigil velocity components
            if hasattr(pressure_reading, 'bloom_mass_breakdown'):
                self.bloom_mass = pressure_reading.bloom_mass_breakdown.get('total_bloom_mass', 0.0)
                self.active_memory_count = state_data.get('active_memory_count', 0)
                self.rebloom_queue_size = state_data.get('rebloom_queue_size', 0)
                self.reflection_backlog = state_data.get('reflection_backlog', 0)
                self.processing_load = state_data.get('processing_load', 0.0)
            
            if hasattr(pressure_reading, 'sigil_velocity_breakdown'):
                self.sigil_velocity = pressure_reading.sigil_velocity_breakdown.get('total_sigil_velocity', 0.0)
                self.recent_sigil_count = state_data.get('recent_sigil_count', 0)
                self.thought_rate = state_data.get('thought_rate', 0.0)
                self.entropy_delta = abs(state_data.get('entropy_delta', 0.0))
                self.mutation_rate = state_data.get('sigil_mutation_rate', 0.0)
            
            # Calculate Schema Health Index (SHI)
            self.shi_score = self._calculate_shi_score(state_data)
            
            # Calculate instability risk
            self.instability_risk = self._calculate_instability_risk()
            
            # Update timestamp and history
            self.timestamp = time.time()
            self._update_pressure_history()
            
            logger.debug(f"🧠 [PRESSURE] P={self.cognitive_pressure:.3f} (B={self.bloom_mass:.2f}, σ={self.sigil_velocity:.2f}) → {self.pressure_zone}")
            
        except Exception as e:
            logger.error(f"Error updating consciousness state with formulas: {e}")
    
    def _calculate_shi_score(self, state_data: Dict[str, Any]) -> float:
        """Calculate Schema Health Index (SHI)"""
        try:
            # SHI components based on system stability
            unity_score = min(1.0, self.scup / 100.0)
            thermal_stability = 1.0 - abs(state_data.get('thermal_heat', 0.5) - 0.5)
            entropy_balance = 1.0 - abs(self.entropy - 0.5)
            pressure_stability = max(0.0, 1.0 - (self.cognitive_pressure / 100.0))
            
            # Weighted combination
            shi = (
                unity_score * 0.3 +
                thermal_stability * 0.25 +
                entropy_balance * 0.25 +
                pressure_stability * 0.2
            )
            
            return max(0.0, min(1.0, shi))
            
        except Exception as e:
            logger.error(f"Error calculating SHI: {e}")
            return 0.5
    
    def _calculate_instability_risk(self) -> float:
        """Calculate risk of cognitive instability/cascade"""
        try:
            # Risk factors
            high_pressure_risk = min(1.0, self.cognitive_pressure / 50.0)
            low_shi_risk = 1.0 - self.shi_score
            entropy_risk = self.entropy if self.entropy > 0.7 else 0.0
            pressure_spike_risk = self._detect_pressure_spike()
            
            # Combined risk score
            risk = (
                high_pressure_risk * 0.4 +
                low_shi_risk * 0.3 +
                entropy_risk * 0.2 +
                pressure_spike_risk * 0.1
            )
            
            return max(0.0, min(1.0, risk))
            
        except Exception as e:
            logger.error(f"Error calculating instability risk: {e}")
            return 0.0
    
    def _detect_pressure_spike(self) -> float:
        """Detect recent pressure spikes in history"""
        if len(self.pressure_history) < 3:
            return 0.0
        
        recent_pressures = [entry['pressure'] for entry in self.pressure_history[-3:]]
        if len(recent_pressures) < 3:
            return 0.0
        
        # Calculate rate of change
        pressure_change = recent_pressures[-1] - recent_pressures[0]
        return max(0.0, pressure_change / 10.0)  # Normalize to 0-1
    
    def _update_pressure_history(self) -> None:
        """Update pressure history for trend analysis"""
        history_entry = {
            'timestamp': self.timestamp,
            'pressure': self.cognitive_pressure,
            'zone': self.pressure_zone,
            'shi': self.shi_score
        }
        
        self.pressure_history.append(history_entry)
        
        # Keep only last 50 entries
        if len(self.pressure_history) > 50:
            self.pressure_history = self.pressure_history[-50:]
    
    def get_pressure_relief_recommendations(self) -> list:
        """Get recommendations for pressure relief based on current state"""
        recommendations = []
        
        if self.cognitive_pressure > 80:
            recommendations.append("CRITICAL: Reduce cognitive load immediately")
            recommendations.append("Consider pausing conversation for system stabilization")
        
        elif self.cognitive_pressure > 50:
            recommendations.append("HIGH: Simplify conversation topics")
            recommendations.append("Focus on single-threaded responses")
        
        elif self.cognitive_pressure > 20:
            recommendations.append("MODERATE: Monitor pressure levels")
            recommendations.append("Maintain current conversation pace")
        
        if self.shi_score < 0.3:
            recommendations.append("LOW SHI: System coherence compromised")
            recommendations.append("Consider restarting conversation context")
        
        if self.instability_risk > 0.7:
            recommendations.append("HIGH RISK: Cognitive instability detected")
            recommendations.append("Implement emergency stabilization protocols")
        
        return recommendations

class CognitivePressureBridge:
    """
    Bridge between cognitive pressure formulas and conversation system
    """
    
    def __init__(self):
        """Initialize the cognitive pressure bridge"""
        self.consciousness_state = EnhancedConsciousnessState()
        self.formula_engine = None
        self.scup_resolver = None
        
        if FORMULA_SYSTEMS_AVAILABLE:
            try:
                self.formula_engine = get_dawn_formula_engine()
                self.scup_resolver = get_scup_drift_resolver()
                logger.info("🧠 [BRIDGE] Cognitive pressure bridge initialized with formula systems")
            except Exception as e:
                logger.warning(f"🧠 [BRIDGE] Formula systems initialization failed: {e}")
        else:
            logger.warning("🧠 [BRIDGE] Running without cognitive pressure formulas")
    
    def update_consciousness_state(self, conversation_context: Dict[str, Any]) -> EnhancedConsciousnessState:
        """
        Update consciousness state with cognitive pressure integration
        
        Args:
            conversation_context: Current conversation context and metrics
            
        Returns:
            Updated consciousness state with pressure calculations
        """
        try:
            # Prepare state data for formula calculation
            state_data = self._prepare_state_data(conversation_context)
            
            # Update consciousness state with formulas
            self.consciousness_state.update_with_formulas(state_data)
            
            return self.consciousness_state
            
        except Exception as e:
            logger.error(f"Error updating consciousness state: {e}")
            return self.consciousness_state
    
    def _prepare_state_data(self, conversation_context: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare state data for cognitive pressure calculation"""
        
        # Extract metrics from conversation context
        metrics = conversation_context.get('metrics', {})
        consciousness_state = conversation_context.get('consciousness_state', {})
        
        # Build comprehensive state data
        state_data = {
            # Core consciousness metrics
            'scup': consciousness_state.get('scup', 50.0),
            'entropy': consciousness_state.get('entropy', 0.5),
            'mood': consciousness_state.get('mood', 'CONTEMPLATIVE'),
            'thermal_zone': consciousness_state.get('thermal_zone', 'CALM'),
            
            # Bloom mass components (B in P = Bσ²)
            'active_memory_count': metrics.get('active_memory_count', 0),
            'rebloom_queue_size': metrics.get('rebloom_queue_size', 0),
            'reflection_backlog': metrics.get('reflection_backlog', 0),
            'processing_load': metrics.get('processing_load', 0.0),
            'sigil_mutations': metrics.get('sigil_mutations', 0),
            
            # Sigil velocity components (σ in P = Bσ²)
            'recent_sigil_count': metrics.get('recent_sigil_count', 0),
            'thought_rate': metrics.get('thought_rate', 0.0),
            'entropy_delta': metrics.get('entropy_delta', 0.0),
            'sigil_mutation_rate': metrics.get('sigil_mutation_rate', 0.0),
            'feedback_loop_intensity': metrics.get('feedback_loop_intensity', 0.0),
            
            # Additional context
            'conversation_turns': conversation_context.get('conversation_turns', 0),
            'topic_depth': conversation_context.get('topic_depth', 0),
            'response_complexity': conversation_context.get('response_complexity', 0.0),
            'user_energy': conversation_context.get('user_energy', 0.5)
        }
        
        return state_data
    
    def get_pressure_modulated_response_strategy(self, base_strategy: str) -> str:
        """
        Modify response strategy based on cognitive pressure
        
        Args:
            base_strategy: Original response strategy
            
        Returns:
            Pressure-modulated response strategy
        """
        pressure = self.consciousness_state.cognitive_pressure
        shi = self.consciousness_state.shi_score
        
        # High pressure modifications
        if pressure > 80:
            if base_strategy == "DIRECT_ANSWER":
                return "INTROSPECTIVE_REFLECTION"
            elif base_strategy == "PHILOSOPHICAL_EXPLORATION":
                return "SIMPLE_CLARIFICATION"
            elif base_strategy == "TECHNICAL_ANALYSIS":
                return "BASIC_EXPLANATION"
        
        # Low SHI modifications
        elif shi < 0.3:
            if base_strategy in ["COMPLEX_ANALYSIS", "DEEP_EXPLORATION"]:
                return "STABILIZATION_RESPONSE"
        
        # Normal pressure - use base strategy
        return base_strategy
    
    def get_system_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive system health summary"""
        return {
            'consciousness_state': {
                'scup': self.consciousness_state.scup,
                'entropy': self.consciousness_state.entropy,
                'mood': self.consciousness_state.mood,
                'thermal_zone': self.consciousness_state.thermal_zone
            },
            'cognitive_pressure': {
                'pressure_value': self.consciousness_state.cognitive_pressure,
                'pressure_zone': self.consciousness_state.pressure_zone,
                'bloom_mass': self.consciousness_state.bloom_mass,
                'sigil_velocity': self.consciousness_state.sigil_velocity
            },
            'system_health': {
                'shi_score': self.consciousness_state.shi_score,
                'instability_risk': self.consciousness_state.instability_risk,
                'recommendations': self.consciousness_state.get_pressure_relief_recommendations()
            },
            'timestamp': self.consciousness_state.timestamp
        }

# Global instance for easy access
_cognitive_pressure_bridge = None

def get_cognitive_pressure_bridge() -> CognitivePressureBridge:
    """Get global cognitive pressure bridge instance"""
    global _cognitive_pressure_bridge
    if _cognitive_pressure_bridge is None:
        _cognitive_pressure_bridge = CognitivePressureBridge()
    return _cognitive_pressure_bridge 