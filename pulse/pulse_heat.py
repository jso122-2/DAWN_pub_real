#!/usr/bin/env python3
"""
pulse_heat.py - Enhanced Thermal Regulation System for DAWN
Dynamic thermal management through expression-based cooling cycles
Restructured to support linguistic expression as primary cooling mechanism
"""

import sys, os
import time
import threading
import math
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, List, Callable, Union, Tuple, Any
from enum import Enum
import numpy as np

# Ensure proper path resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# === EXPRESSION-BASED ENUMS ===

class DecayCurve(Enum):
    """Thermal decay patterns"""
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    SIGMOID = "sigmoid"

class HeatSourceType(Enum):
    """Enhanced heat source types with expression mapping"""
    COGNITIVE_LOAD = "cognitive_load"
    EMOTIONAL_RESONANCE = "emotional_resonance"
    MEMORY_PROCESSING = "memory_processing"
    AWARENESS_SPIKE = "awareness_spike"
    UNEXPRESSED_THOUGHT = "unexpressed_thought"
    PATTERN_RECOGNITION = "pattern_recognition"
    DRIFT = "drift"
    MOOD = "mood"
    ALIGNMENT = "alignment"
    ENTROPY = "entropy"
    CURIOSITY = "curiosity"
    TENSION = "tension"
    PRESSURE = "pressure"
    URGENCY = "urgency"

class ReleaseValve(Enum):
    """Expression channels for thermal release"""
    VERBAL_EXPRESSION = "verbal_expression"
    SYMBOLIC_OUTPUT = "symbolic_output"
    CREATIVE_FLOW = "creative_flow"
    EMPATHETIC_RESPONSE = "empathetic_response"
    CONCEPTUAL_MAPPING = "conceptual_mapping"
    MEMORY_TRACE = "memory_trace"
    PATTERN_SYNTHESIS = "pattern_synthesis"

class ThermalZone(Enum):
    """Thermal zone classifications"""
    CALM = "🟢 calm"
    STABLE = "🟡 stable"
    ACTIVE = "🟡 active"
    HOT = "🔴 hot"
    CRITICAL = "🚨 critical"

# === DATA STRUCTURES ===

@dataclass
class HeatSource:
    """Individual heat contribution with decay characteristics."""
    name: str
    base_heat: float
    decay_rate: float = 0.95  # Heat retention per tick
    last_contribution: float = 0.0
    cumulative: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)
    expression_affinity: Dict = field(default_factory=dict)
    
    def apply_decay(self, delta_time: float = 1.0) -> float:
        """Apply time-based decay and return amount decayed."""
        decay_amount = self.last_contribution * (1 - self.decay_rate) * delta_time
        self.last_contribution *= (self.decay_rate ** delta_time)
        return decay_amount

@dataclass
class ExpressionPhase:
    """Tracks thermal dynamics during expression cycles"""
    # Pre-expression state
    pre_thermal: float = 0.0
    pre_pressure: float = 0.0
    pre_readiness: float = 0.0
    
    # During expression
    thermal_flow: float = 0.0
    momentum_sustain: float = 0.0
    coherence_maintain: float = 1.0
    expression_type: Optional[ReleaseValve] = None
    
    # Post-expression
    thermal_drop: float = 0.0
    satisfaction: float = 0.0
    recharge_time: float = 0.0
    
    # Timestamps
    start_time: float = 0.0
    peak_time: float = 0.0
    end_time: float = 0.0
    
    # Content
    expression_content: str = ""
    coherence_score: float = 1.0

@dataclass
class ThermalState:
    """Comprehensive thermal state with expression dynamics"""
    current_thermal: float = 5.0
    thermal_ceiling: float = 8.0
    decay_curve: DecayCurve = DecayCurve.SIGMOID
    expression_momentum: float = 0.0
    cooling_rate: float = 0.3
    heat_sources: Dict[str, HeatSource] = field(default_factory=dict)
    release_valves: List[ReleaseValve] = field(default_factory=list)
    stability_target: float = 5.5
    
    # Historical tracking
    thermal_history: deque = field(default_factory=lambda: deque(maxlen=100))
    expression_history: deque = field(default_factory=lambda: deque(maxlen=50))

# === MAIN THERMAL REGULATOR ===

class UnifiedPulseHeat:
    """
    Enhanced thermal regulation system with expression-based cooling.
    Maintains backward compatibility while adding expression dynamics.
    """
    
    _instance = None
    _lock = threading.RLock()
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, decay_rate=0.02, memory_window=100, max_heat=99.9):
        if self._initialized:
            return
            
        with self._lock:
            if self._initialized:
                return
                
            # Legacy compatibility properties
            self.decay_rate = decay_rate
            self.memory_window = memory_window
            self.max_heat = max_heat  # Clamped to 99.9°C
            self.memory_log = deque(maxlen=memory_window)
            self.memory = []
            self.window = memory_window
            
            # Core thermal state
            self.heat = 0.0
            self.current_heat = 0.0
            self.baseline_heat = 0.0
            self.heat_capacity = max_heat
            self.critical_threshold = max_heat * 0.8
            
            # Temperature change tracking for logging
            self.last_logged_temp = 0.0
            self.temp_change_threshold = 0.1  # Only log if temp changes by this amount
            self.last_zone = None
            self.sigils_active = False  # Track sigil activity for cooldown
            
            # Expression-based thermal management
            self.thermal_state = ThermalState()
            self.current_phase: Optional[ExpressionPhase] = None
            self.phase_history: deque = deque(maxlen=20)
            self.expression_momentum = 0.0
            
            # Expression cooling mappings
            self.expression_cooling = {
                ReleaseValve.VERBAL_EXPRESSION: 0.4,
                ReleaseValve.SYMBOLIC_OUTPUT: 0.3,
                ReleaseValve.CREATIVE_FLOW: 0.6,
                ReleaseValve.EMPATHETIC_RESPONSE: 0.5,
                ReleaseValve.CONCEPTUAL_MAPPING: 0.35,
                ReleaseValve.MEMORY_TRACE: 0.25,
                ReleaseValve.PATTERN_SYNTHESIS: 0.45
            }
            
            # Heat source configuration
            self.heat_sources: Dict[str, HeatSource] = {}
            self.source_weights: Dict[str, float] = {
                'drift': 1.0,
                'mood': 0.8,
                'alignment': 1.2,
                'entropy': 0.6,
                'curiosity': 0.9,
                'tension': 1.1,
                'pressure': 1.0,
                'urgency': 1.3,
                'cognitive_load': 1.1,
                'emotional_resonance': 1.2,
                'memory_processing': 0.9,
                'awareness_spike': 1.4,
                'unexpressed_thought': 1.3,
                'pattern_recognition': 1.0
            }
            
            # Source to expression affinity mapping
            self.source_expression_affinity = {
                HeatSourceType.COGNITIVE_LOAD: {
                    ReleaseValve.CONCEPTUAL_MAPPING: 0.8,
                    ReleaseValve.SYMBOLIC_OUTPUT: 0.7
                },
                HeatSourceType.EMOTIONAL_RESONANCE: {
                    ReleaseValve.EMPATHETIC_RESPONSE: 0.9,
                    ReleaseValve.CREATIVE_FLOW: 0.7
                },
                HeatSourceType.UNEXPRESSED_THOUGHT: {
                    ReleaseValve.VERBAL_EXPRESSION: 0.9,
                    ReleaseValve.CREATIVE_FLOW: 0.8
                },
                HeatSourceType.PATTERN_RECOGNITION: {
                    ReleaseValve.PATTERN_SYNTHESIS: 0.9,
                    ReleaseValve.CONCEPTUAL_MAPPING: 0.8
                }
            }
            
            # Thermal dynamics
            self.thermal_momentum = 0.0
            self.cooling_rate = decay_rate * 2
            self.conductivity = 0.1
            
            # Expression curve parameters
            self.curve_params = {
                DecayCurve.LINEAR: {"rate": 0.3},
                DecayCurve.EXPONENTIAL: {"base": 0.85, "min_rate": 0.1},
                DecayCurve.SIGMOID: {"steepness": 0.5, "midpoint": 6.0}
            }
            
            # Memory and averaging systems
            self.heat_history = deque(maxlen=memory_window)
            self.running_average = 0.0
            self.variance = 0.0
            
            # Legacy zone tracking
            self.zone_timer = {
                "🟢 calm": 0,
                "🟡 active": 0,
                "🔴 surge": 0
            }
            self.current_zone = None
            self.zone_history = []
            
            # Legacy mood and penalty tracking
            self.mood_pressure = {}
            self.seed_penalties = {}
            
            # State tracking
            self.tick_count = 0
            self.last_update = datetime.utcnow()
            self.last_decay = time.time()
            self.last_tick_time = time.time()
            self.stability_index = 1.0
            
            # Event callbacks
            self.threshold_callbacks: List[Callable] = []
            self.stability_callbacks: List[Callable] = []
            self.expression_callbacks: List[Callable] = []
            
            # Suppression state
            self.override_active = False
            
            # Constitutional preservation
            self.kindness_thermal_modifier = 0.9
            
            self._initialized = True
            print(f"[PulseHeat] 🔥 Enhanced thermal system initialized | Max Heat: {self.max_heat}°C | ID: {id(self)}")

    # === EXPRESSION-BASED THERMAL MANAGEMENT ===
    
    def calculate_expression_momentum(self, awareness_level: float = 50.0) -> float:
        """Build linguistic pressure based on thermal state and awareness"""
        # Momentum builds faster when above stability target
        thermal_pressure = max(0, self.heat - self.thermal_state.stability_target)
        
        # Unexpressed thoughts add significant pressure
        unexpressed_count = sum(1 for name, source in self.heat_sources.items() 
                               if 'unexpressed' in name.lower())
        unexpressed_factor = unexpressed_count * 0.15
        
        # High awareness increases expression readiness
        awareness_factor = awareness_level / 100.0
        
        # Time since last expression
        if self.phase_history:
            last_phase = self.phase_history[-1]
            time_since = time.time() - last_phase.end_time
            time_factor = min(1.0, time_since / 60.0)
        else:
            time_factor = 0.5
        
        # Calculate momentum with sigmoid activation
        raw_momentum = (thermal_pressure * 0.3 + unexpressed_factor + 
                       time_factor * 0.2 + awareness_factor * 0.2)
        self.expression_momentum = 1 / (1 + np.exp(-4 * (raw_momentum - 0.5)))
        self.thermal_state.expression_momentum = self.expression_momentum
        
        return self.expression_momentum
    
    def update_thermal_ceiling(self, awareness_level: float) -> float:
        """Dynamically adjust thermal ceiling based on system state"""
        # Higher awareness allows lower ceiling (more expression freedom)
        base_ceiling = 8.0
        awareness_factor = (100 - awareness_level) / 100
        
        # When thermal is high, lower the ceiling to encourage expression
        thermal_factor = max(0, self.heat - 6.0) * 0.5
        
        new_ceiling = base_ceiling - (awareness_factor * 2.0) - thermal_factor
        self.thermal_state.thermal_ceiling = max(4.0, min(9.0, new_ceiling))
        
        return self.thermal_state.thermal_ceiling
    
    def initiate_expression(self, expression_type: ReleaseValve, 
                          intensity: float = 1.0,
                          content: str = "") -> ExpressionPhase:
        """Begin expression cycle with thermal tracking"""
        phase = ExpressionPhase()
        phase.start_time = time.time()
        phase.expression_type = expression_type
        phase.expression_content = content
        
        # Pre-expression state
        phase.pre_thermal = self.heat
        phase.pre_pressure = self.calculate_expression_momentum()
        phase.pre_readiness = self._calculate_readiness()
        
        # During expression calculations
        base_cooling = self.expression_cooling.get(expression_type, 0.3)
        
        # Kind expressions get cooling bonus
        if expression_type == ReleaseValve.EMPATHETIC_RESPONSE:
            base_cooling *= self.kindness_thermal_modifier
        
        # Calculate affinity bonus based on heat sources
        affinity_bonus = self._calculate_affinity_bonus(expression_type)
        
        phase.thermal_flow = base_cooling * intensity * phase.pre_readiness * (1 + affinity_bonus)
        phase.momentum_sustain = self._calculate_momentum_sustain(phase.pre_pressure)
        phase.coherence_maintain = self._calculate_coherence(phase.pre_thermal)
        
        self.current_phase = phase
        self.thermal_state.release_valves.append(expression_type)
        
        # Trigger expression callbacks
        for callback in self.expression_callbacks:
            try:
                callback('start', phase)
            except Exception as e:
                print(f"[PulseHeat] ❌ Expression callback error: {e}")
        
        return phase
    
    def process_expression_tick(self, elapsed_time: float = 0.1) -> Dict[str, float]:
        """Process ongoing expression with thermal flow"""
        if not self.current_phase:
            return {}
        
        phase = self.current_phase
        
        # Apply cooling based on decay curve
        cooling = self._apply_decay_curve(phase.thermal_flow, elapsed_time)
        old_heat = self.heat
        self.heat = max(0, self.heat - cooling)
        self.current_heat = self.heat
        
        # Update momentum (decreases during expression)
        momentum_decay = elapsed_time * 0.1 / phase.momentum_sustain
        self.expression_momentum = max(0, self.expression_momentum - momentum_decay)
        
        # Track thermal history
        self.heat_history.append(self.heat)
        self.thermal_state.thermal_history.append({
            "time": time.time(),
            "thermal": self.heat,
            "momentum": self.expression_momentum,
            "cooling": cooling
        })
        
        return {
            "current_thermal": self.heat,
            "cooling_rate": cooling,
            "momentum": self.expression_momentum,
            "coherence": phase.coherence_maintain,
            "thermal_drop": old_heat - self.heat
        }
    
    def complete_expression(self) -> Dict[str, float]:
        """Complete expression cycle and calculate satisfaction"""
        if not self.current_phase:
            return {}
        
        phase = self.current_phase
        phase.end_time = time.time()
        phase.peak_time = (phase.start_time + phase.end_time) / 2
        
        # Post-expression calculations
        phase.thermal_drop = phase.pre_thermal - self.heat
        phase.satisfaction = self._calculate_satisfaction(phase)
        phase.recharge_time = self._calculate_recharge_time(phase)
        
        # Store in history
        self.phase_history.append(phase)
        self.thermal_state.expression_history.append(phase)
        
        # Clear expressed thoughts from heat sources
        self._clear_expressed_heat_sources(phase.expression_type)
        
        # Trigger expression callbacks
        for callback in self.expression_callbacks:
            try:
                callback('complete', phase)
            except Exception as e:
                print(f"[PulseHeat] ❌ Expression callback error: {e}")
        
        self.current_phase = None
        
        return {
            "thermal_drop": phase.thermal_drop,
            "satisfaction": phase.satisfaction,
            "recharge_time": phase.recharge_time,
            "final_thermal": self.heat,
            "expression_type": phase.expression_type.value if phase.expression_type else None
        }
    
    def apply_emergency_cooling(self, force_expression: bool = True) -> Dict[str, float]:
        """Emergency cooling for thermal overload prevention"""
        if self.heat < 8.5:
            return {"applied": False, "thermal": self.heat}
        
        # Rapid cooling
        emergency_rate = 1.5
        old_heat = self.heat
        self.heat = max(6.0, self.heat - emergency_rate)
        self.current_heat = self.heat
        
        # Force expression readiness
        if force_expression:
            self.expression_momentum = 1.0
            self.thermal_state.expression_momentum = 1.0
        
        # Lower ceiling for easier expression
        self.thermal_state.thermal_ceiling = 6.0
        
        print(f"[PulseHeat] 🚨 Emergency cooling applied: {old_heat:.2f} → {self.heat:.2f}")
        
        return {
            "applied": True,
            "cooling": emergency_rate,
            "thermal": self.heat,
            "ceiling": self.thermal_state.thermal_ceiling,
            "forced_expression": force_expression
        }
    
    # === ENHANCED LEGACY METHODS ===
    
    def get_heat(self) -> float:
        """Get current heat with automatic decay and memory update"""
        # Apply standard decay
        old_heat = self.heat
        self.heat = max(0.0, self.heat - self.decay_rate)
        
        # Clamp to maximum safe temperature
        self.heat = min(self.max_heat, self.heat)
        self.current_heat = self.heat
        
        # Update memory for legacy compatibility
        if not hasattr(self, "memory"):
            self.memory = []
        self.memory.append(self.heat)
        if len(self.memory) > self.window:
            self.memory.pop(0)
        
        # Update heat history
        self.heat_history.append(self.heat)
        self._update_thermal_memory()
        
        # Only log if temperature changed significantly
        temp_change = abs(self.heat - self.last_logged_temp)
        if temp_change >= self.temp_change_threshold:
            zone = self.classify()
            if zone != self.last_zone:
                print(f"[PulseHeat] 🌡️ Heat: {old_heat:.1f} → {self.heat:.1f}°C | Zone: {zone}")
                self.last_logged_temp = self.heat
                self.last_zone = zone
        
        return self.heat

    def update_heat(self, new_heat: float, source: str = "manual", reason: str = "") -> float:
        """Update heat to a specific value with clamping and logging"""
        old_heat = self.heat
        
        # Clamp to safe range
        self.heat = max(0.0, min(self.max_heat, new_heat))
        self.current_heat = self.heat
        
        # Update memory
        if not hasattr(self, "memory"):
            self.memory = []
        self.memory.append(self.heat)
        if len(self.memory) > self.window:
            self.memory.pop(0)
        
        # Only log significant changes
        temp_change = abs(self.heat - self.last_logged_temp)
        if temp_change >= self.temp_change_threshold:
            zone = self.classify()
            reason_str = f" ({reason})" if reason else ""
            print(f"[PulseHeat] 🔄 Heat updated by {source}{reason_str}: {old_heat:.1f} → {self.heat:.1f}°C | Zone: {zone}")
            self.last_logged_temp = self.heat
            self.last_zone = zone
        
        return self.heat

    def cooldown(self, force_cooldown: bool = False) -> Dict[str, float]:
        """Apply cooldown logic when no sigils active and in HOT zone"""
        old_heat = self.heat
        old_zone = self.classify()
        cooldown_applied = 0.0
        
        # Check if cooldown should be applied
        should_cooldown = (
            force_cooldown or 
            (not self.sigils_active and old_zone in ["🔴 hot", "🚨 critical"])
        )
        
        if should_cooldown:
            # Apply aggressive cooldown for HOT/CRITICAL zones
            if old_zone in ["🔴 hot", "🚨 critical"]:
                cooldown_rate = 1.5  # Reduce by 1.5°C per tick
                self.heat = max(0.0, self.heat - cooldown_rate)
                cooldown_applied = cooldown_rate
                
                # Once below 80°C, transition to stable zone
                if self.heat < 80.0:
                    # Determine target zone based on heat level
                    if self.heat < 40.0:
                        target_zone = "🟢 calm"
                    else:
                        target_zone = "🟡 stable"
                    
                    new_zone = self.classify()
                    if new_zone != old_zone:
                        print(f"[PulseHeat] ❄️ Cooldown complete: {old_heat:.1f} → {self.heat:.1f}°C | {old_zone} → {new_zone}")
                        self.last_logged_temp = self.heat
                        self.last_zone = new_zone
            
            # Apply moderate cooldown for other zones when forced
            elif force_cooldown:
                cooldown_rate = 0.8
                self.heat = max(0.0, self.heat - cooldown_rate)
                cooldown_applied = cooldown_rate
        
        # Clamp to maximum
        self.heat = min(self.max_heat, self.heat)
        self.current_heat = self.heat
        
        # Update memory
        if cooldown_applied > 0:
            if not hasattr(self, "memory"):
                self.memory = []
            self.memory.append(self.heat)
            if len(self.memory) > self.window:
                self.memory.pop(0)
        
        return {
            "old_heat": old_heat,
            "new_heat": self.heat,
            "cooldown_applied": cooldown_applied,
            "old_zone": old_zone,
            "new_zone": self.classify(),
            "sigils_active": self.sigils_active,
            "forced": force_cooldown
        }

    def set_sigils_active(self, active: bool) -> None:
        """Set sigil activity state for cooldown logic"""
        old_state = self.sigils_active
        self.sigils_active = active
        
        if old_state != active:
            state_str = "ACTIVE" if active else "INACTIVE"
            print(f"[PulseHeat] 🎯 Sigils {state_str}")
            
            # Trigger cooldown check when sigils become inactive
            if not active:
                self.cooldown()

    def add_heat(self, amount: float, source: str, reason: str = ""):
        """Enhanced add_heat with expression affinity tracking and clamping"""
        # Safety check for emergency recovery
        if source == "emergency_recovery" and amount > 0:
            print(f"[PulseHeat] ⚠️ WARNING: Emergency recovery trying to add heat!")
            amount = -abs(amount)
        
        # Create or update heat source
        if source not in self.heat_sources:
            heat_source = HeatSource(
                name=source,
                base_heat=amount,
                decay_rate=self._get_source_decay_rate(source)
            )
            
            # Add expression affinities
            source_type = self._get_source_type(source)
            if source_type and source_type in self.source_expression_affinity:
                heat_source.expression_affinity = self.source_expression_affinity[source_type]
            
            self.heat_sources[source] = heat_source
        else:
            heat_source = self.heat_sources[source]
            heat_source.last_contribution = amount
            heat_source.cumulative += amount
        
        # Apply heat with clamping to 99.9°C
        old_heat = self.heat
        self.heat = min(self.max_heat, max(0, self.heat + amount))
        self.current_heat = self.heat
        
        # Update thermal momentum
        self.thermal_momentum = self.thermal_momentum * 0.9 + (amount * 0.1)
        
        # Update memory
        self.memory.append(self.heat)
        if len(self.memory) > self.window:
            self.memory.pop(0)
        
        # Only log significant changes to prevent spam
        temp_change = abs(self.heat - self.last_logged_temp)
        if temp_change >= self.temp_change_threshold:
            zone = self.classify()
            reason_str = f" ({reason})" if reason else ""
            print(f"[PulseHeat] +{amount:.2f} from {source}{reason_str} | Heat: {old_heat:.1f} → {self.heat:.1f}°C | Zone: {zone}")
            self.last_logged_temp = self.heat
            self.last_zone = zone
        
        # Check for expression triggers
        if self.heat > self.thermal_state.stability_target + 1.5:
            self.calculate_expression_momentum()
        
        # Auto-cooldown if reaching critical levels
        if self.heat >= self.max_heat * 0.95:  # At 94.5°C or higher
            print(f"[PulseHeat] 🚨 Critical temperature reached! Initiating emergency cooldown...")
            self.cooldown(force_cooldown=True)

    def tick_update(self) -> Dict[str, float]:
        """Enhanced tick update with cooldown and expression dynamics"""
        with self._lock:
            self.tick_count += 1
            current_time = datetime.utcnow()
            delta_time = (current_time - self.last_update).total_seconds()
            self.last_update = current_time
            
            # Apply decay if overheated
            if self.heat > self.max_heat * 0.8:  # Above 80% of max
                decay_modifier = self._calculate_decay_modifier()
                self.heat -= self.decay_rate * decay_modifier
                self.heat = max(0, self.heat)
            
            # Apply heat source decay
            total_decay = 0.0
            for source in self.heat_sources.values():
                decay_amount = source.apply_decay(delta_time)
                total_decay += decay_amount
            
            # Apply passive cooling
            passive_cooling = self.cooling_rate * max(self.heat - self.baseline_heat, 0) * delta_time
            
            # Update total heat
            old_heat = self.heat
            self.heat = max(
                self.heat - total_decay - passive_cooling,
                self.baseline_heat
            )
            
            # Clamp to safe maximum
            self.heat = min(self.heat, self.heat_capacity)
            self.current_heat = self.heat
            
            # Apply cooldown logic
            self.cooldown()
            
            # Update memory and statistics
            self.heat_history.append(self.heat)
            self._update_thermal_memory()
            
            # Update expression momentum
            if self.tick_count % 10 == 0:  # Every 10 ticks
                self.calculate_expression_momentum()
            
            stats = {
                'current_heat': self.heat,
                'average_heat': self.running_average,
                'variance': self.variance,
                'momentum': self.thermal_momentum,
                'expression_momentum': self.expression_momentum,
                'stability': self.stability_index,
                'source_count': len(self.heat_sources),
                'memory_depth': len(self.heat_history),
                'tick': self.tick_count,
                'zone': self.classify(),
                'sigils_active': self.sigils_active,
                'max_heat': self.max_heat
            }
            
            return stats
    
    def get_thermal_diagnosis(self) -> Dict[str, any]:
        """Comprehensive thermal state diagnosis with expression readiness"""
        # Identify dominant heat sources
        source_counts = {}
        for name, source in self.heat_sources.items():
            source_counts[name] = {
                'contribution': source.last_contribution,
                'cumulative': source.cumulative,
                'affinity': source.expression_affinity
            }
        
        # Calculate thermal trajectory
        if len(self.heat_history) > 10:
            recent_thermals = list(self.heat_history)[-10:]
            trajectory = np.polyfit(range(10), recent_thermals, 1)[0]
        else:
            trajectory = 0.0
        
        # Expression readiness
        readiness = self._calculate_readiness()
        
        # Stability assessment
        stability = 1.0 - abs(self.heat - self.thermal_state.stability_target) / 5.0
        
        # Recommended expression type
        recommended_expression = self._recommend_expression_type()
        
        return {
            "current_thermal": self.heat,
            "thermal_ceiling": self.thermal_state.thermal_ceiling,
            "expression_momentum": self.expression_momentum,
            "dominant_heat_sources": source_counts,
            "thermal_trajectory": trajectory,
            "expression_readiness": readiness,
            "stability_score": max(0, stability),
            "recommended_action": self._recommend_action(),
            "recommended_expression": recommended_expression,
            "phase_active": self.current_phase is not None,
            "recent_expressions": len(self.phase_history)
        }
    
    # === HELPER METHODS ===
    
    def _calculate_readiness(self) -> float:
        """Calculate expression readiness based on thermal state"""
        # High readiness when thermal exceeds stability target
        thermal_factor = max(0, self.heat - self.thermal_state.stability_target) / 4.0
        
        # Momentum contributes to readiness
        momentum_factor = self.expression_momentum * 0.5
        
        # Ceiling proximity increases urgency
        ceiling_factor = max(0, self.heat - self.thermal_state.thermal_ceiling + 1) * 0.3
        
        return min(1.0, thermal_factor + momentum_factor + ceiling_factor)
    
    def _calculate_affinity_bonus(self, expression_type: ReleaseValve) -> float:
        """Calculate expression effectiveness based on heat source affinities"""
        total_affinity = 0.0
        total_heat = sum(s.last_contribution for s in self.heat_sources.values())
        
        if total_heat == 0:
            return 0.0
        
        for source in self.heat_sources.values():
            if expression_type in source.expression_affinity:
                weight = source.last_contribution / total_heat
                affinity = source.expression_affinity[expression_type]
                total_affinity += weight * affinity
        
        return total_affinity
    
    def _calculate_momentum_sustain(self, initial_pressure: float) -> float:
        """How long expression can sustain based on built pressure"""
        base_sustain = 5.0  # seconds
        pressure_bonus = initial_pressure * 10.0
        
        # Higher thermal allows longer expression
        thermal_bonus = max(0, self.heat - 5.0) * 2.0
        
        return base_sustain + pressure_bonus + thermal_bonus
    
    def _calculate_coherence(self, thermal: float) -> float:
        """Coherence maintenance during expression"""
        # Optimal coherence at moderate thermals
        if thermal < 4.0:
            return 0.7 + thermal * 0.075
        elif thermal < 7.0:
            return 1.0
        else:
            return 1.0 - (thermal - 7.0) * 0.1
    
    def _apply_decay_curve(self, base_cooling: float, elapsed: float) -> float:
        """Apply selected decay curve to cooling rate"""
        curve = self.thermal_state.decay_curve
        params = self.curve_params[curve]
        
        if curve == DecayCurve.LINEAR:
            return base_cooling * params["rate"] * elapsed
        
        elif curve == DecayCurve.EXPONENTIAL:
            decay_factor = params["base"] ** elapsed
            return base_cooling * (1 - decay_factor) + params["min_rate"] * elapsed
        
        elif curve == DecayCurve.SIGMOID:
            x = self.heat
            steepness = params["steepness"]
            midpoint = params["midpoint"]
            sigmoid = 1 / (1 + np.exp(-steepness * (x - midpoint)))
            return base_cooling * sigmoid * elapsed
    
    def _calculate_satisfaction(self, phase: ExpressionPhase) -> float:
        """Calculate expression satisfaction score"""
        # Thermal relief achieved
        relief_factor = phase.thermal_drop / 3.0
        
        # Expression completeness
        duration = phase.end_time - phase.start_time
        completeness = min(1.0, duration / phase.momentum_sustain)
        
        # Coherence maintained
        coherence_factor = phase.coherence_maintain
        
        # Approach to stability target
        final_distance = abs(self.heat - self.thermal_state.stability_target)
        stability_factor = 1.0 - (final_distance / 5.0)
        
        return (relief_factor * 0.3 + completeness * 0.3 + 
                coherence_factor * 0.2 + stability_factor * 0.2)
    
    def _calculate_recharge_time(self, phase: ExpressionPhase) -> float:
        """Time until next expression cycle"""
        base_recharge = 10.0 + phase.thermal_drop * 5.0
        
        # Satisfaction reduces recharge time
        satisfaction_modifier = 1.0 - (phase.satisfaction * 0.3)
        
        # Current thermal affects recharge
        if self.heat < self.thermal_state.stability_target:
            thermal_modifier = 1.5
        else:
            thermal_modifier = 0.7
        
        return base_recharge * satisfaction_modifier * thermal_modifier
    
    def _clear_expressed_heat_sources(self, expression_type: ReleaseValve):
        """Clear heat sources that were expressed"""
        sources_to_reduce = []
        
        for name, source in self.heat_sources.items():
            if expression_type in source.expression_affinity:
                affinity = source.expression_affinity[expression_type]
                if affinity > 0.7:  # High affinity sources get cleared
                    sources_to_reduce.append((name, affinity))
        
        for name, affinity in sources_to_reduce:
            if name in self.heat_sources:
                self.heat_sources[name].last_contribution *= (1 - affinity)
                if 'unexpressed' in name.lower():
                    del self.heat_sources[name]
    
    def _recommend_expression_type(self) -> Optional[str]:
        """Recommend best expression type based on current heat sources"""
        if not self.heat_sources:
            return None
        
        # Calculate weighted affinity scores
        expression_scores = {}
        total_heat = sum(s.last_contribution for s in self.heat_sources.values())
        
        if total_heat == 0:
            return None
        
        for valve in ReleaseValve:
            score = 0.0
            for source in self.heat_sources.values():
                if valve in source.expression_affinity:
                    weight = source.last_contribution / total_heat
                    score += weight * source.expression_affinity[valve]
            expression_scores[valve] = score
        
        # Find best expression type
        best_type = max(expression_scores.items(), key=lambda x: x[1])
        if best_type[1] > 0.1:  # Minimum threshold
            return best_type[0].value
        
        return None
    
    def _recommend_action(self) -> str:
        """Recommend action based on thermal state"""
        thermal = self.heat
        momentum = self.expression_momentum
        
        if thermal > 8.5:
            return "URGENT: Initiate expression immediately - thermal overload risk"
        elif thermal > 7.0 and momentum > 0.7:
            return "EXPRESS: High thermal and momentum - expression recommended"
        elif thermal > self.thermal_state.stability_target + 1.0:
            return "PREPARE: Building thermal pressure - prepare expression channels"
        elif thermal < self.thermal_state.stability_target - 1.0:
            return "RECHARGE: Below optimal thermal - allow natural recharge"
        else:
            return "STABLE: Operating within optimal thermal range"
    
    def _get_source_type(self, source_name: str) -> Optional[HeatSourceType]:
        """Map source name to HeatSourceType"""
        source_lower = source_name.lower()
        for heat_type in HeatSourceType:
            if heat_type.value in source_lower:
                return heat_type
        return None
    
    def _calculate_decay_modifier(self) -> float:
        """Calculate decay modifier based on current conditions"""
        if self.heat > self.max_heat * 0.8:
            return 2.0
        elif self.heat < self.max_heat * 0.2:
            return 0.5
        return 1.0
    
    def _update_thermal_memory(self):
        """Update heat history and running statistics"""
        if len(self.heat_history) >= 2:
            alpha = 0.1
            self.running_average = (alpha * self.heat + 
                                  (1 - alpha) * self.running_average)
            
            heat_array = list(self.heat_history)
            mean = sum(heat_array) / len(heat_array)
            self.variance = sum((x - mean) ** 2 for x in heat_array) / len(heat_array)
        else:
            self.running_average = self.heat
            self.variance = 0.0
    
    def _get_source_decay_rate(self, source: str) -> float:
        """Get appropriate decay rate for heat source type"""
        decay_rates = {
            'drift': 0.98,
            'mood': 0.92,
            'alignment': 0.96,
            'entropy': 0.90,
            'curiosity': 0.94,
            'tension': 0.93,
            'pressure': 0.91,
            'urgency': 0.89,
            'cognitive_load': 0.94,
            'emotional_resonance': 0.95,
            'memory_processing': 0.96,
            'awareness_spike': 0.88,
            'unexpressed_thought': 0.85,
            'pattern_recognition': 0.93,
            'general': 0.95
        }
        
        source_lower = source.lower()
        for key in decay_rates:
            if key in source_lower:
                return decay_rates[key]
        
        return decay_rates['general']

    def get_thermal_profile(self) -> Dict[str, Any]:
        """Get thermal profile for consciousness system compatibility"""
        try:
            return {
                'singleton_id': f"unified_pulse_{id(self)}",
                'current_heat': self.heat,
                'baseline_heat': self.baseline_heat,
                'running_average': self.running_average,
                'thermal_momentum': self.thermal_momentum,
                'stability_index': self.stability_index,
                'variance': self.variance,
                'heat_capacity': self.heat_capacity,
                'memory_size': len(self.heat_history),
                'tick_count': self.tick_count,
                'current_zone': self.classify(),
                'zone_history': getattr(self, 'zone_history', []),
                'sources': {name: {'contribution': source.last_contribution, 
                                'cumulative': source.cumulative} 
                        for name, source in self.heat_sources.items()},
                'penalties': getattr(self, 'seed_penalties', {}),
                'mood_pressure': getattr(self, 'mood_pressure', {}),
                'last_update': datetime.now(timezone.utc).isoformat(),
                'expression_momentum': self.expression_momentum,
                'thermal_ceiling': self.thermal_state.thermal_ceiling
            }
        except Exception as e:
            print(f"[PulseHeat] ❌ Error generating thermal profile: {e}")
            return {
                'singleton_id': 'fallback_profile',
                'current_heat': self.heat,
                'baseline_heat': 0.0,
                'running_average': 0.0,
                'thermal_momentum': 0.0,
                'stability_index': 0.5,
                'variance': 0.0,
                'heat_capacity': 10.0,
                'memory_size': 0,
                'tick_count': 0,
                'current_zone': '🟢 calm',
                'zone_history': [],
                'sources': {},
                'penalties': {},
                'mood_pressure': {},
                'last_update': datetime.now(timezone.utc).isoformat()
            }
    
    # === LEGACY COMPATIBILITY ===
    
    def get_average(self) -> float:
        """Legacy averaging with debug info"""
        avg = sum(self.memory) / len(self.memory) if self.memory else 0.0
        return avg
    
    def classify(self) -> str:
        """Enhanced classification with improved zone boundaries"""
        heat = self.heat
        
        if heat < 20.0:
            return ThermalZone.CALM.value
        elif heat < 50.0:
            return ThermalZone.STABLE.value
        elif heat < 70.0:
            return ThermalZone.ACTIVE.value
        elif heat < 90.0:
            return ThermalZone.HOT.value
        else:
            return ThermalZone.CRITICAL.value
    
    def boost(self, amount: float, source: str = "boost"):
        """Legacy boost method"""
        self.add_heat(amount, source, "⚡ Boost")
    
    def apply_penalty(self, seed: str, factor: float):
        """Apply penalty to seed with mycelium integration"""
        self.seed_penalties[seed] = factor
        print(f"[Pulse] 🪶 Penalty applied to seed {seed}: {factor}")
        try:
            from mycelium.mycelium_layer import mycelium
            mycelium.weaken_seed(seed, factor)
        except ImportError:
            pass
    
    def _log(self, msg: str):
        """Legacy logging method"""
        print(f"[PulseHeat] {msg} | Heat: {self.heat:.3f} | Avg: {self.get_average():.3f}")
    
    # === EVENT REGISTRATION ===
    
    def register_expression_callback(self, callback: Callable):
        """Register callback for expression events"""
        self.expression_callbacks.append(callback)

# === GLOBAL SINGLETON AND CONVENIENCE FUNCTIONS ===

# Maintain backward compatibility
PulseHeat = UnifiedPulseHeat
pulse = UnifiedPulseHeat()

# Enhanced convenience functions
def add_heat(source: str, amount: float, context: str = "") -> float:
    """Add heat to the unified thermal system"""
    pulse.add_heat(amount, source, context)
    return pulse.heat

def initiate_expression(expression_type: str = "creative_flow", 
                       intensity: float = 1.0) -> ExpressionPhase:
    """Start expression cycle for cooling"""
    try:
        valve = ReleaseValve(expression_type)
    except ValueError:
        valve = ReleaseValve.CREATIVE_FLOW
    
    return pulse.initiate_expression(valve, intensity)

def process_expression_tick(elapsed: float = 0.1) -> Dict[str, float]:
    """Process ongoing expression"""
    return pulse.process_expression_tick(elapsed)

def complete_expression() -> Dict[str, float]:
    """Complete current expression cycle"""
    return pulse.complete_expression()

def get_thermal_diagnosis() -> Dict[str, any]:
    """Get comprehensive thermal diagnosis"""
    return pulse.get_thermal_diagnosis()

def update_awareness_ceiling(awareness: float) -> float:
    """Update thermal ceiling based on awareness"""
    return pulse.update_thermal_ceiling(awareness)

# Register global singleton
import builtins
if not hasattr(builtins, 'pulse'):
    builtins.pulse = pulse
    print("[PulseHeat] 🌍 Enhanced pulse singleton registered globally")

# Example usage for testing
if __name__ == "__main__":
    print("\n=== Testing Enhanced Expression-Based Thermal System ===")
    
    # Set initial state
    pulse.heat = 7.3
    pulse.add_heat(0.5, "awareness_spike", "high awareness detected")
    pulse.add_heat(0.3, "unexpressed_thought", "pending expression")
    
    # Update ceiling based on awareness
    ceiling = update_awareness_ceiling(94.0)
    print(f"\nThermal ceiling adjusted to: {ceiling:.1f}")
    
    # Check thermal diagnosis
    diagnosis = get_thermal_diagnosis()
    print(f"\nThermal Diagnosis:")
    print(f"  Current: {diagnosis['current_thermal']:.2f}")
    print(f"  Momentum: {diagnosis['expression_momentum']:.2f}")
    print(f"  Recommended: {diagnosis['recommended_action']}")
    print(f"  Best expression: {diagnosis['recommended_expression']}")
    
    # Initiate expression
    phase = initiate_expression("creative_flow", 0.9)
    print(f"\nExpression initiated - thermal flow: {phase.thermal_flow:.2f}")
    
    # Simulate expression
    for i in range(5):
        tick_result = process_expression_tick(0.5)
        print(f"Tick {i+1}: thermal={tick_result['current_thermal']:.2f}, "
              f"cooling={tick_result['cooling_rate']:.3f}")
    
    # Complete expression
    completion = complete_expression()
    print(f"\nExpression completed:")
    print(f"  Thermal drop: {completion['thermal_drop']:.2f}")
    print(f"  Satisfaction: {completion['satisfaction']:.2f}")
    print(f"  Final thermal: {completion['final_thermal']:.2f}")