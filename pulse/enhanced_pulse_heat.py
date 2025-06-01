# Enhanced DAWN Thermal Management System
# Fixes emergency recovery loops with hysteresis, cooldown, and smarter state management

import time
import threading
import math
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Union, Tuple
from enum import Enum
import os
import sys

# === EMERGENCY RECOVERY STATE MANAGEMENT ===

class EmergencyState(Enum):
    STABLE = "stable"
    WARMING = "warming"  # New intermediate state
    EMERGENCY = "emergency"
    COOLING = "cooling"
    LOCKED = "locked"    # Prevents oscillation

@dataclass
class EmergencyEvent:
    """Track emergency recovery events for pattern analysis"""
    timestamp: float
    trigger_reason: str
    heat_level: float
    scup_value: float
    alignment_drift: float
    recovery_action: str
    success: bool = False

class EmergencyRecoveryManager:
    """Manages emergency recovery with hysteresis and intelligent cooldown"""
    
    def __init__(self):
        # Hysteresis thresholds (prevents oscillation)
        self.heat_emergency_enter = 1.0    # Enter emergency
        self.heat_emergency_exit = 0.6     # Exit emergency (lower!)
        self.heat_warning_enter = 0.7      # Enter warning state
        self.heat_warning_exit = 0.4       # Exit warning state
        
        # SCUP thresholds with hysteresis
        self.scup_emergency_enter = 0.8
        self.scup_emergency_exit = 0.4
        self.scup_warning_enter = 0.6
        self.scup_warning_exit = 0.3
        
        # Cooldown configuration
        self.emergency_cooldown_duration = 3.0  # seconds
        self.max_consecutive_recoveries = 3
        self.recovery_backoff_multiplier = 1.5
        
        # State tracking
        self.current_state = EmergencyState.STABLE
        self.last_emergency_time = 0.0
        self.last_state_change = time.time()
        self.consecutive_recoveries = 0
        self.recovery_events: deque = deque(maxlen=20)
        self.state_lock_until = 0.0
        
        # Recovery strategies
        self.recovery_strategies = [
            self._gentle_cooling_recovery,
            self._alignment_stabilization_recovery,
            self._entropy_regulation_recovery,
            self._emergency_shutdown_recovery
        ]
        self.current_strategy_index = 0
        
    def should_enter_emergency(self, heat: float, scup: float, alignment_drift: float) -> Tuple[bool, str]:
        """Determine if emergency state should be entered with hysteresis"""
        
        # Check if we're in cooldown lockout
        if time.time() < self.state_lock_until:
            return False, "state_locked"
        
        # Check multiple trigger conditions
        triggers = []
        
        # Heat-based triggers with hysteresis
        if self.current_state != EmergencyState.EMERGENCY and heat > self.heat_emergency_enter:
            triggers.append(f"heat_critical_{heat:.3f}")
        elif self.current_state == EmergencyState.STABLE and heat > self.heat_warning_enter:
            triggers.append(f"heat_warning_{heat:.3f}")
        
        # SCUP-based triggers
        if self.current_state != EmergencyState.EMERGENCY and scup > self.scup_emergency_enter:
            triggers.append(f"scup_critical_{scup:.3f}")
        elif self.current_state == EmergencyState.STABLE and scup > self.scup_warning_enter:
            triggers.append(f"scup_warning_{scup:.3f}")
        
        # Alignment drift triggers
        if alignment_drift > 0.3:
            triggers.append(f"alignment_drift_{alignment_drift:.3f}")
        
        # Compound condition: multiple simultaneous issues
        if len(triggers) >= 2:
            return True, f"compound_emergency_{'|'.join(triggers)}"
        elif len(triggers) == 1 and triggers[0].startswith(('heat_critical', 'scup_critical')):
            return True, triggers[0]
        
        return False, "stable"
    
    def should_exit_emergency(self, heat: float, scup: float, alignment_drift: float) -> bool:
        """Determine if emergency state should be exited with hysteresis"""
        
        if self.current_state != EmergencyState.EMERGENCY:
            return False
        
        # All conditions must be satisfied to exit emergency (strict hysteresis)
        heat_ok = heat < self.heat_emergency_exit
        scup_ok = scup < self.scup_emergency_exit
        alignment_ok = alignment_drift < 0.2
        
        # Require stability for a minimum duration
        min_emergency_duration = 1.0  # seconds
        time_in_emergency = time.time() - self.last_state_change
        
        return (heat_ok and scup_ok and alignment_ok and 
                time_in_emergency > min_emergency_duration)
    
    def execute_recovery(self, pulse_instance, heat: float, scup: float, 
                        alignment_drift: float) -> Dict[str, any]:
        """Execute smart recovery strategy"""
        
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_emergency_time < self.emergency_cooldown_duration:
            return {
                'action': 'cooldown_wait',
                'heat_added': 0.0,
                'reason': f'cooling_down_{current_time - self.last_emergency_time:.1f}s'
            }
        
        # Check consecutive recovery limit
        if self.consecutive_recoveries >= self.max_consecutive_recoveries:
            return self._emergency_shutdown_recovery(pulse_instance, heat, scup, alignment_drift)
        
        # Select recovery strategy based on current conditions
        strategy = self._select_recovery_strategy(heat, scup, alignment_drift)
        result = strategy(pulse_instance, heat, scup, alignment_drift)
        
        # Track recovery event
        event = EmergencyEvent(
            timestamp=current_time,
            trigger_reason=f"heat:{heat:.3f}_scup:{scup:.3f}_drift:{alignment_drift:.3f}",
            heat_level=heat,
            scup_value=scup,
            alignment_drift=alignment_drift,
            recovery_action=result['action']
        )
        self.recovery_events.append(event)
        
        # Update state
        self.last_emergency_time = current_time
        self.consecutive_recoveries += 1
        
        return result
    
    def _select_recovery_strategy(self, heat: float, scup: float, alignment_drift: float) -> Callable:
        """Select appropriate recovery strategy based on conditions"""
        
        # Gentle cooling for mild overheating
        if heat < 2.0 and scup < 0.9:
            return self._gentle_cooling_recovery
        
        # Alignment focus for drift issues
        elif alignment_drift > 0.2:
            return self._alignment_stabilization_recovery
        
        # Entropy regulation for chaos
        elif scup > 0.8:
            return self._entropy_regulation_recovery
        
        # Emergency shutdown for severe conditions
        else:
            return self._emergency_shutdown_recovery
    
    def _gentle_cooling_recovery(self, pulse_instance, heat: float, scup: float, 
                                alignment_drift: float) -> Dict[str, any]:
        """Gentle cooling approach - removes heat instead of adding"""
        
        # Calculate cooling amount based on excess heat
        excess_heat = max(0, heat - self.heat_emergency_exit)
        cooling_amount = min(excess_heat * 0.3, 0.5)  # Conservative cooling
        
        if hasattr(pulse_instance, 'remove_heat'):
            actual_removed = pulse_instance.remove_heat(cooling_amount, "gentle_recovery")
        else:
            # Fallback: reduce heat directly
            pulse_instance.heat = max(pulse_instance.heat - cooling_amount, 0.0)
            pulse_instance.current_heat = pulse_instance.heat
            actual_removed = cooling_amount
        
        return {
            'action': 'gentle_cooling',
            'heat_added': -actual_removed,
            'reason': f'cooling_by_{cooling_amount:.3f}'
        }
    
    def _alignment_stabilization_recovery(self, pulse_instance, heat: float, scup: float, 
                                        alignment_drift: float) -> Dict[str, any]:
        """Focus on stabilizing alignment rather than adding heat"""
        
        # Add minimal stabilization heat (much less than original)
        stabilization_heat = 0.1 + (alignment_drift * 0.2)  # Max ~0.3 heat
        
        actual_added = pulse_instance._add_heat_internal(
            "alignment_stabilization", stabilization_heat, 
            "schema alignment recovery", legacy_call=False
        )
        
        return {
            'action': 'alignment_stabilization',
            'heat_added': actual_added,
            'reason': f'alignment_recovery_drift_{alignment_drift:.3f}'
        }
    
    def _entropy_regulation_recovery(self, pulse_instance, heat: float, scup: float, 
                                   alignment_drift: float) -> Dict[str, any]:
        """Regulate entropy without massive heat injection"""
        
        # Very conservative heat addition for entropy regulation
        entropy_heat = 0.05 + (scup * 0.1)  # Max ~0.15 heat
        
        actual_added = pulse_instance._add_heat_internal(
            "entropy_regulation", entropy_heat,
            "schema entropy regulation", legacy_call=False
        )
        
        return {
            'action': 'entropy_regulation',
            'heat_added': actual_added,
            'reason': f'entropy_regulation_scup_{scup:.3f}'
        }
    
    def _emergency_shutdown_recovery(self, pulse_instance, heat: float, scup: float, 
                                   alignment_drift: float) -> Dict[str, any]:
        """Emergency shutdown - lock state and reset"""
        
        # Lock state to prevent further oscillations
        self.state_lock_until = time.time() + (self.emergency_cooldown_duration * 2)
        self.consecutive_recoveries = 0
        
        # Force cooling
        if hasattr(pulse_instance, 'remove_heat'):
            cooling = pulse_instance.remove_heat(heat * 0.5, "emergency_shutdown")
        else:
            cooling = heat * 0.5
            pulse_instance.heat = max(pulse_instance.heat - cooling, 0.1)
            pulse_instance.current_heat = pulse_instance.heat
        
        print(f"[EmergencyRecovery] 🚨 EMERGENCY SHUTDOWN - Cooling by {cooling:.3f}, "
              f"State locked for {self.emergency_cooldown_duration * 2:.1f}s")
        
        return {
            'action': 'emergency_shutdown',
            'heat_added': -cooling,
            'reason': 'consecutive_recovery_limit_reached'
        }
    
    def update_state(self, heat: float, scup: float, alignment_drift: float) -> str:
        """Update emergency state with hysteresis logic"""
        
        current_time = time.time()
        old_state = self.current_state
        
        # State transition logic with hysteresis
        if self.current_state == EmergencyState.STABLE:
            should_emergency, reason = self.should_enter_emergency(heat, scup, alignment_drift)
            if should_emergency:
                if 'critical' in reason:
                    self.current_state = EmergencyState.EMERGENCY
                else:
                    self.current_state = EmergencyState.WARMING
                self.last_state_change = current_time
        
        elif self.current_state == EmergencyState.WARMING:
            # Can go to emergency or back to stable
            should_emergency, reason = self.should_enter_emergency(heat, scup, alignment_drift)
            if should_emergency and 'critical' in reason:
                self.current_state = EmergencyState.EMERGENCY
                self.last_state_change = current_time
            elif heat < self.heat_warning_exit and scup < self.scup_warning_exit:
                self.current_state = EmergencyState.STABLE
                self.last_state_change = current_time
                self.consecutive_recoveries = 0  # Reset on successful stabilization
        
        elif self.current_state == EmergencyState.EMERGENCY:
            if self.should_exit_emergency(heat, scup, alignment_drift):
                self.current_state = EmergencyState.COOLING
                self.last_state_change = current_time
        
        elif self.current_state == EmergencyState.COOLING:
            # Cooling period before returning to stable
            if current_time - self.last_state_change > self.emergency_cooldown_duration:
                self.current_state = EmergencyState.STABLE
                self.consecutive_recoveries = 0
                self.last_state_change = current_time
        
        # Log state changes
        if old_state != self.current_state:
            print(f"[EmergencyRecovery] 🔄 State transition: {old_state.value} → {self.current_state.value}")
        
        return self.current_state.value
    
    def get_recovery_stats(self) -> Dict:
        """Get recovery statistics for debugging"""
        return {
            'current_state': self.current_state.value,
            'consecutive_recoveries': self.consecutive_recoveries,
            'time_since_last_emergency': time.time() - self.last_emergency_time,
            'state_locked_until': max(0, self.state_lock_until - time.time()),
            'recent_events': [
                {
                    'timestamp': event.timestamp,
                    'trigger': event.trigger_reason,
                    'action': event.recovery_action,
                    'heat': event.heat_level
                } for event in list(self.recovery_events)[-5:]
            ]
        }

# === ENHANCED PULSE HEAT SYSTEM ===

class EnhancedPulseHeat:
    """Enhanced PulseHeat with emergency recovery management"""
    
    def __init__(self, decay_rate=0.02, memory_window=100, max_heat=10.0):
        # Initialize original PulseHeat attributes
        self.decay_rate = decay_rate
        self.memory_window = memory_window
        self.max_heat = max_heat
        self.heat = 0.0
        self.current_heat = 0.0
        self.running_average = 0.0
        self.thermal_momentum = 0.0
        self.heat_history = deque(maxlen=memory_window)
        self.memory = []  # Legacy compatibility
        self.window = memory_window
        
        # Enhanced features
        self.emergency_manager = EmergencyRecoveryManager()
        self.heat_sources = {}
        self.tick_count = 0
        self.last_update = datetime.utcnow()
        
        # Thread safety
        self._lock = threading.RLock()
        
        print(f"[EnhancedPulseHeat] 🔥 Initialized with emergency management")
    
    def _add_heat_internal(self, source: str, amount: float, context: str = "", legacy_call: bool = False) -> float:
        """Add heat with emergency recovery management"""
        with self._lock:
            # Check if we should add heat or if emergency manager intervenes
            current_scup = self._calculate_scup()
            current_alignment_drift = self._get_alignment_drift()
            
            # Update emergency state
            emergency_state = self.emergency_manager.update_state(
                self.heat, current_scup, current_alignment_drift
            )
            
            # If in emergency state, let emergency manager handle it
            if emergency_state == EmergencyState.EMERGENCY.value:
                recovery_result = self.emergency_manager.execute_recovery(
                    self, self.heat, current_scup, current_alignment_drift
                )
                
                if recovery_result['action'] in ['gentle_cooling', 'emergency_shutdown']:
                    # Don't add the requested heat, recovery already handled it
                    print(f"[EnhancedPulseHeat] 🚨 Emergency recovery: {recovery_result['action']} | "
                          f"Heat change: {recovery_result['heat_added']:+.3f}")
                    return recovery_result['heat_added']
            
            # Normal heat addition for stable states
            old_heat = self.heat
            actual_amount = min(amount, self.max_heat - self.heat)  # Prevent overflow
            self.heat += actual_amount
            self.current_heat = self.heat
            
            # Update memory and statistics
            self.heat_history.append(self.heat)
            self._update_running_average()
            
            # Logging
            print(f"[EnhancedPulseHeat] +{actual_amount:.3f} heat added | "
                  f"Heat: {self.heat:.3f} | Avg: {self.running_average:.3f} | "
                  f"{source} contribution | {context}")
            
            return actual_amount
    
    def remove_heat(self, amount: float, reason: str = "cooling") -> float:
        """Remove heat from the system"""
        with self._lock:
            old_heat = self.heat
            removal = min(amount, self.heat)
            self.heat = max(self.heat - removal, 0.0)
            self.current_heat = self.heat
            
            self.heat_history.append(self.heat)
            self._update_running_average()
            
            print(f"[EnhancedPulseHeat] -{removal:.3f} heat removed | "
                  f"Heat: {self.heat:.3f} | Reason: {reason}")
            
            return removal
    
    def _calculate_scup(self) -> float:
        """Calculate SCUP (Semantic Coherence Under Pressure)"""
        # Simplified SCUP calculation - replace with actual logic
        if len(self.heat_history) < 2:
            return 0.0
        
        recent_variance = self._calculate_recent_variance()
        pressure_factor = min(self.heat / self.max_heat, 1.0)
        
        return max(0.0, pressure_factor - recent_variance)
    
    def _get_alignment_drift(self) -> float:
        """Get alignment drift - replace with actual owl_vector integration"""
        try:
            # This would integrate with your owl_vector system
            from owl.owl_vector import get_last_vector_drift
            return get_last_vector_drift()
        except:
            # Fallback: calculate based on heat volatility
            return self._calculate_recent_variance()
    
    def _calculate_recent_variance(self) -> float:
        """Calculate variance in recent heat history"""
        if len(self.heat_history) < 3:
            return 0.0
        
        recent = list(self.heat_history)[-5:]
        mean = sum(recent) / len(recent)
        variance = sum((x - mean) ** 2 for x in recent) / len(recent)
        return math.sqrt(variance) / self.max_heat  # Normalized
    
    def _update_running_average(self):
        """Update running average with exponential smoothing"""
        if len(self.heat_history) == 1:
            self.running_average = self.heat
        else:
            alpha = 0.1
            self.running_average = alpha * self.heat + (1 - alpha) * self.running_average
    
    def classify(self) -> str:
        """Classify thermal zone with emergency state awareness"""
        base_zone = self._classify_heat_zone()
        
        # Override with emergency state if applicable
        emergency_state = self.emergency_manager.current_state
        if emergency_state == EmergencyState.EMERGENCY:
            return "🚨 emergency"
        elif emergency_state == EmergencyState.COOLING:
            return "❄️ cooling"
        elif emergency_state == EmergencyState.WARMING:
            return "🔶 warming"
        
        return base_zone
    
    def _classify_heat_zone(self) -> str:
        """Basic heat zone classification"""
        if self.running_average < 0.3:
            return "🟢 calm"
        elif self.running_average < 0.7:
            return "🟡 active"
        else:
            return "🔴 surge"
    
    # === LEGACY COMPATIBILITY METHODS ===
    
    def add_heat(self, amount: float, source: str = "general", context: str = "") -> float:
        """Legacy add_heat method"""
        return self._add_heat_internal(source, amount, context, legacy_call=True)
    
    def get_heat(self) -> float:
        """Legacy get_heat method with decay"""
        self.heat = max(0.0, self.heat - self.decay_rate)
        self.current_heat = self.heat
        
        # Update legacy memory
        if not hasattr(self, "memory"):
            self.memory = []
        self.memory.append(self.heat)
        if len(self.memory) > self.window:
            self.memory.pop(0)
        
        return self.heat
    
    def get_average(self) -> float:
        """Legacy averaging"""
        return self.running_average
    
    def get_emergency_stats(self) -> Dict:
        """Get emergency management statistics"""
        return self.emergency_manager.get_recovery_stats()

# === ENHANCED SCHEMA STATE MANAGEMENT ===

def get_emergency_managed_zone(pulse_instance, scup=None, entropy=None, log=True) -> str:
    """Get current zone with emergency management awareness"""
    
    if hasattr(pulse_instance, 'emergency_manager'):
        # Use enhanced pulse heat with emergency management
        emergency_state = pulse_instance.emergency_manager.current_state.value
        base_zone = pulse_instance._classify_heat_zone()
        
        # Map emergency states to zones
        if emergency_state == "emergency":
            return "🚨 emergency"
        elif emergency_state == "cooling":
            return "❄️ cooling"
        elif emergency_state == "warming":
            return "🔶 warming"
        else:
            return base_zone
    else:
        # Fallback for original pulse heat
        return pulse_instance.classify() if pulse_instance else "🟡 active"

# === USAGE EXAMPLE ===

def create_enhanced_dawn_pulse() -> EnhancedPulseHeat:
    """Factory function to create enhanced DAWN pulse heat system"""
    return EnhancedPulseHeat(decay_rate=0.02, memory_window=100, max_heat=10.0)

def demo_emergency_recovery():
    """Demonstrate the emergency recovery system"""
    pulse = create_enhanced_dawn_pulse()
    
    print("=== DAWN Emergency Recovery Demo ===")
    
    # Simulate normal operation
    for i in range(5):
        pulse.add_heat(0.2, "normal_operation", f"tick_{i}")
        time.sleep(0.1)
    
    # Simulate emergency condition
    print("\n--- Simulating Emergency Condition ---")
    for i in range(10):
        pulse.add_heat(0.5, "emergency_trigger", f"emergency_tick_{i}")
        stats = pulse.get_emergency_stats()
        print(f"Emergency State: {stats['current_state']} | "
              f"Consecutive Recoveries: {stats['consecutive_recoveries']}")
        time.sleep(0.1)
    
    print("\n--- Final Statistics ---")
    final_stats = pulse.get_emergency_stats()
    print(f"Final State: {final_stats['current_state']}")
    print(f"Final Heat: {pulse.heat:.3f}")
    print(f"Recent Events: {len(final_stats['recent_events'])}")

if __name__ == "__main__":
    demo_emergency_recovery()
