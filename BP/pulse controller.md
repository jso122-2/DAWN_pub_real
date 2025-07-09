#!/usr/bin/env python3
"""
DAWN Pulse Controller
Cognitive heat regulation and pulse zone management system

Manages heat-based pulse zones, tick intervals, and cognitive load regulation
for the DAWN recursive symbolic engine.
"""

import time
import math
from typing import List, Dict, Any, Optional, Tuple


class ZoneTransition:
    """Represents a transition between pulse zones"""
    
    def __init__(self, from_zone: str, to_zone: str, heat_value: float):
        self.from_zone = from_zone
        self.to_zone = to_zone
        self.heat_value = heat_value
        self.timestamp = time.time()
        self.duration = 0.0  # Will be set when transition completes
        
    def complete_transition(self):
        """Mark transition as complete and calculate duration"""
        self.duration = time.time() - self.timestamp


class PulseController:
    """Main pulse and heat regulation controller for DAWN"""
    
    def __init__(self, initial_heat: float = 25.0):
        # Core heat state
        self.current_heat = max(0.0, min(100.0, float(initial_heat)))
        self.target_heat = self.current_heat
        self.heat_history: List[Tuple[float, float]] = []  # (timestamp, heat_value)
        
        # Zone management
        self.current_zone = self._calculate_zone(self.current_heat)
        self.previous_zone = self.current_zone
        self.zone_entry_time = time.time()
        self.zone_transitions: List[ZoneTransition] = []
        
        # Surge tracking
        self.last_surge_time: Optional[float] = None
        self.surge_count = 0
        self.total_surge_duration = 0.0
        self.current_surge_start: Optional[float] = None
        
        # Heat regulation parameters
        self.heat_dampening = 0.85  # Heat decay factor per update
        self.max_heat_change_per_update = 15.0  # Prevents heat spikes
        self.heat_smoothing = 0.2  # Smoothing factor for gradual changes
        
        # Tick interval parameters
        self.base_tick_interval = 1.0  # 1 second base interval
        self.min_tick_interval = 0.1   # 100ms minimum (max speed)
        self.max_tick_interval = 5.0   # 5 second maximum (min speed)
        
        # Grace period parameters
        self.base_grace_period = 30.0  # 30 seconds base cooldown
        self.grace_multiplier = 1.5    # Multiplier for repeated surges
        self.max_grace_period = 300.0  # 5 minute maximum grace
        
        # Performance tracking
        self.total_updates = 0
        self.start_time = time.time()
        
    def update_heat(self, new_heat_value: float) -> Dict[str, Any]:
        """
        Update the current heat value with validation and smoothing
        
        Args:
            new_heat_value: New heat level (0-100)
            
        Returns:
            Dictionary with update results and zone information
        """
        try:
            # Validate input
            new_heat_value = max(0.0, min(100.0, float(new_heat_value)))
            
            # Apply heat change limits to prevent spikes
            heat_delta = new_heat_value - self.current_heat
            if abs(heat_delta) > self.max_heat_change_per_update:
                # Limit the change rate
                if heat_delta > 0:
                    new_heat_value = self.current_heat + self.max_heat_change_per_update
                else:
                    new_heat_value = self.current_heat - self.max_heat_change_per_update
            
            # Apply smoothing for gradual transitions
            smoothed_heat = (self.heat_smoothing * new_heat_value + 
                           (1.0 - self.heat_smoothing) * self.current_heat)
            
            # Store previous values
            previous_heat = self.current_heat
            previous_zone = self.current_zone
            
            # Update heat
            self.current_heat = smoothed_heat
            self.target_heat = new_heat_value
            
            # Record in history
            current_time = time.time()
            self.heat_history.append((current_time, self.current_heat))
            
            # Limit history size
            if len(self.heat_history) > 1000:
                self.heat_history = self.heat_history[-500:]  # Keep last 500 entries
            
            # Update zone
            new_zone = self._calculate_zone(self.current_heat)
            zone_changed = self._update_zone(new_zone)
            
            # Track surge state
            surge_info = self._update_surge_tracking()
            
            # Increment update counter
            self.total_updates += 1
            
            # Return update summary
            return {
                'previous_heat': previous_heat,
                'current_heat': self.current_heat,
                'target_heat': self.target_heat,
                'heat_delta': self.current_heat - previous_heat,
                'previous_zone': previous_zone,
                'current_zone': self.current_zone,
                'zone_changed': zone_changed,
                'time_in_zone': current_time - self.zone_entry_time,
                'surge_active': surge_info['surge_active'],
                'tick_interval': self.get_tick_interval(),
                'grace_period': self.apply_grace_period(),
                'update_count': self.total_updates
            }
            
        except Exception as e:
            print(f"❌ Error updating heat: {e}")
            return {
                'error': str(e),
                'current_heat': self.current_heat,
                'current_zone': self.current_zone
            }
    
    def get_pulse_zone(self) -> str:
        """
        Get current pulse zone based on heat thresholds
        
        Returns:
            Zone string: "CALM", "ACTIVE", or "SURGE"
        """
        return self.current_zone
    
    def get_tick_interval(self) -> float:
        """
        Calculate tick interval using inverse function of heat
        Higher heat = faster processing = shorter intervals
        
        Returns:
            Tick interval in seconds
        """
        try:
            # Inverse relationship: higher heat = shorter intervals
            # Use exponential decay for smooth curve
            heat_factor = self.current_heat / 100.0  # Normalize to 0-1
            
            # Calculate interval using exponential inverse
            # At heat=0: interval = max_tick_interval
            # At heat=100: interval = min_tick_interval
            interval = (self.max_tick_interval * math.exp(-4 * heat_factor) + 
                       self.min_tick_interval)
            
            # Ensure bounds
            interval = max(self.min_tick_interval, min(self.max_tick_interval, interval))
            
            # Apply zone-specific modifiers
            if self.current_zone == "SURGE":
                interval *= 0.8  # 20% faster in surge
            elif self.current_zone == "CALM":
                interval *= 1.2  # 20% slower in calm
            
            return round(interval, 3)
            
        except Exception as e:
            print(f"❌ Error calculating tick interval: {e}")
            return self.base_tick_interval
    
    def apply_grace_period(self) -> float:
        """
        Calculate cooldown period based on last surge
        
        Returns:
            Grace period duration in seconds
        """
        try:
            if self.last_surge_time is None:
                return 0.0
            
            # Time since last surge
            time_since_surge = time.time() - self.last_surge_time
            
            # Calculate base grace period
            grace_period = self.base_grace_period
            
            # Apply multiplier for repeated surges (cooling gets longer)
            if self.surge_count > 1:
                repeated_surge_multiplier = min(self.grace_multiplier ** (self.surge_count - 1), 4.0)
                grace_period *= repeated_surge_multiplier
            
            # Apply intensity modifier based on how long the surge lasted
            if hasattr(self, 'last_surge_duration'):
                intensity_modifier = 1.0 + (self.last_surge_duration / 60.0)  # +1 per minute of surge
                grace_period *= min(intensity_modifier, 3.0)  # Cap at 3x
            
            # Cap maximum grace period
            grace_period = min(grace_period, self.max_grace_period)
            
            # Calculate remaining grace period
            remaining_grace = max(0.0, grace_period - time_since_surge)
            
            return round(remaining_grace, 1)
            
        except Exception as e:
            print(f"❌ Error calculating grace period: {e}")
            return 0.0
    
    def _calculate_zone(self, heat_value: float) -> str:
        """Calculate zone based on heat thresholds"""
        if heat_value < 40:
            return "CALM"
        elif heat_value < 60:
            return "ACTIVE"
        else:
            return "SURGE"
    
    def _update_zone(self, new_zone: str) -> bool:
        """Update zone and track transitions"""
        if new_zone != self.current_zone:
            # Record transition
            transition = ZoneTransition(self.current_zone, new_zone, self.current_heat)
            
            # Complete previous transition if exists
            if self.zone_transitions:
                self.zone_transitions[-1].complete_transition()
            
            self.zone_transitions.append(transition)
            
            # Update zone state
            self.previous_zone = self.current_zone
            self.current_zone = new_zone
            self.zone_entry_time = time.time()
            
            print(f"🌡️ Zone transition: {self.previous_zone} → {self.current_zone} | Heat: {self.current_heat:.1f}")
            
            return True
        
        return False
    
    def _update_surge_tracking(self) -> Dict[str, Any]:
        """Update surge state tracking"""
        current_time = time.time()
        surge_active = self.current_zone == "SURGE"
        
        if surge_active and self.current_surge_start is None:
            # Surge starting
            self.current_surge_start = current_time
            print(f"🔥 SURGE initiated | Heat: {self.current_heat:.1f}")
            
        elif not surge_active and self.current_surge_start is not None:
            # Surge ending
            surge_duration = current_time - self.current_surge_start
            self.total_surge_duration += surge_duration
            self.last_surge_time = current_time
            self.last_surge_duration = surge_duration
            self.surge_count += 1
            self.current_surge_start = None
            
            print(f"❄️ Surge ended | Duration: {surge_duration:.1f}s | Total surges: {self.surge_count}")
        
        return {
            'surge_active': surge_active,
            'surge_duration': (current_time - self.current_surge_start) if self.current_surge_start else 0.0,
            'total_surges': self.surge_count,
            'time_since_last_surge': (current_time - self.last_surge_time) if self.last_surge_time else 0.0
        }
    
    def apply_heat_decay(self, decay_rate: float = None) -> float:
        """
        Apply natural heat decay over time
        
        Args:
            decay_rate: Optional custom decay rate (0.0-1.0)
            
        Returns:
            New heat value after decay
        """
        if decay_rate is None:
            decay_rate = self.heat_dampening
        
        # Apply decay
        decayed_heat = self.current_heat * decay_rate
        
        # Update heat through normal channels
        result = self.update_heat(decayed_heat)
        
        return result.get('current_heat', self.current_heat)
    
    def regulate_heat(self, target_heat: float, regulation_speed: float = 0.1) -> Dict[str, Any]:
        """
        Gradually regulate heat toward target value
        
        Args:
            target_heat: Target heat level (0-100)
            regulation_speed: Speed of regulation (0.0-1.0)
            
        Returns:
            Regulation result dictionary
        """
        try:
            target_heat = max(0.0, min(100.0, float(target_heat)))
            regulation_speed = max(0.01, min(1.0, float(regulation_speed)))
            
            # Calculate heat adjustment
            heat_difference = target_heat - self.current_heat
            heat_adjustment = heat_difference * regulation_speed
            
            # Apply adjustment
            new_heat = self.current_heat + heat_adjustment
            result = self.update_heat(new_heat)
            
            # Add regulation info
            result['regulation_target'] = target_heat
            result['regulation_speed'] = regulation_speed
            result['heat_adjustment'] = heat_adjustment
            result['distance_to_target'] = abs(target_heat - self.current_heat)
            
            return result
            
        except Exception as e:
            print(f"❌ Error in heat regulation: {e}")
            return {'error': str(e)}
    
    def get_heat_statistics(self) -> Dict[str, Any]:
        """Get comprehensive heat and performance statistics"""
        try:
            current_time = time.time()
            uptime = current_time - self.start_time
            
            # Heat statistics
            if self.heat_history:
                heat_values = [h[1] for h in self.heat_history]
                avg_heat = sum(heat_values) / len(heat_values)
                min_heat = min(heat_values)
                max_heat = max(heat_values)
                heat_variance = sum((h - avg_heat) ** 2 for h in heat_values) / len(heat_values)
            else:
                avg_heat = min_heat = max_heat = heat_variance = self.current_heat
            
            # Zone statistics
            zone_distribution = {}
            zone_durations = {}
            
            for transition in self.zone_transitions:
                from_zone = transition.from_zone
                zone_distribution[from_zone] = zone_distribution.get(from_zone, 0) + 1
                if transition.duration > 0:
                    zone_durations[from_zone] = zone_durations.get(from_zone, [])
                    zone_durations[from_zone].append(transition.duration)
            
            # Current zone time
            time_in_current_zone = current_time - self.zone_entry_time
            
            return {
                # Heat metrics
                'current_heat': self.current_heat,
                'target_heat': self.target_heat,
                'average_heat': round(avg_heat, 2),
                'min_heat': round(min_heat, 2),
                'max_heat': round(max_heat, 2),
                'heat_variance': round(heat_variance, 2),
                'heat_history_size': len(self.heat_history),
                
                # Zone metrics
                'current_zone': self.current_zone,
                'time_in_current_zone': round(time_in_current_zone, 1),
                'zone_transitions': len(self.zone_transitions),
                'zone_distribution': zone_distribution,
                
                # Surge metrics
                'total_surges': self.surge_count,
                'total_surge_duration': round(self.total_surge_duration, 1),
                'average_surge_duration': (round(self.total_surge_duration / self.surge_count, 1) 
                                         if self.surge_count > 0 else 0.0),
                'time_since_last_surge': (round(current_time - self.last_surge_time, 1) 
                                        if self.last_surge_time else None),
                'current_grace_period': self.apply_grace_period(),
                
                # Performance metrics
                'uptime': round(uptime, 1),
                'total_updates': self.total_updates,
                'updates_per_second': round(self.total_updates / uptime, 2) if uptime > 0 else 0.0,
                'current_tick_interval': self.get_tick_interval()
            }
            
        except Exception as e:
            print(f"❌ Error generating statistics: {e}")
            return {'error': str(e)}
    
    def reset_surge_tracking(self) -> None:
        """Reset surge tracking statistics"""
        self.last_surge_time = None
        self.surge_count = 0
        self.total_surge_duration = 0.0
        self.current_surge_start = None
        print("🔄 Surge tracking reset")
    
    def emergency_cooldown(self, cooldown_target: float = 25.0) -> Dict[str, Any]:
        """
        Emergency heat reduction to prevent system overload
        
        Args:
            cooldown_target: Target heat level for emergency cooldown
            
        Returns:
            Cooldown result dictionary
        """
        print(f"🚨 Emergency cooldown initiated | Current heat: {self.current_heat:.1f}")
        
        # Rapid heat reduction
        result = self.update_heat(cooldown_target)
        
        # Reset surge tracking to prevent grace period penalties
        self.reset_surge_tracking()
        
        result['emergency_cooldown'] = True
        result['cooldown_target'] = cooldown_target
        
        print(f"❄️ Emergency cooldown complete | New heat: {self.current_heat:.1f}")
        
        return result


# Test and demonstration functions
def _test_pulse_controller():
    """Test the pulse controller with various scenarios"""
    print("🔥 Testing DAWN Pulse Controller")
    print("=" * 40)
    
    # Create controller
    controller = PulseController(initial_heat=30.0)
    
    print(f"Initial state: Zone={controller.get_pulse_zone()}, Heat={controller.current_heat:.1f}")
    print(f"Initial tick interval: {controller.get_tick_interval():.3f}s")
    
    # Test heat updates and zone transitions
    test_heat_values = [45, 55, 65, 75, 85, 70, 50, 30, 20]
    
    print(f"\n📈 Testing heat progression...")
    for heat in test_heat_values:
        result = controller.update_heat(heat)
        zone = result['current_zone']
        interval = controller.get_tick_interval()
        grace = controller.apply_grace_period()
        
        print(f"Heat: {result['current_heat']:5.1f} | Zone: {zone:6s} | "
              f"Interval: {interval:.3f}s | Grace: {grace:5.1f}s")
        
        # Simulate some time passing
        time.sleep(0.1)
    
    # Test surge tracking
    print(f"\n🔥 Testing surge scenario...")
    surge_sequence = [70, 75, 80, 85, 90, 85, 75, 65, 45, 30]
    
    for heat in surge_sequence:
        result = controller.update_heat(heat)
        if result.get('zone_changed'):
            print(f"Zone change: {result['previous_zone']} → {result['current_zone']}")
        time.sleep(0.2)  # Simulate longer surge
    
    # Show final statistics
    print(f"\n📊 Final Statistics:")
    stats = controller.get_heat_statistics()
    print(f"Total surges: {stats['total_surges']}")
    print(f"Average heat: {stats['average_heat']:.1f}")
    print(f"Zone transitions: {stats['zone_transitions']}")
    print(f"Current grace period: {stats['current_grace_period']:.1f}s")
    
    # Test emergency cooldown
    print(f"\n🚨 Testing emergency cooldown...")
    controller.update_heat(95)  # Create emergency situation
    emergency_result = controller.emergency_cooldown(20)
    print(f"Cooldown result: {emergency_result['current_heat']:.1f}")


if __name__ == "__main__":
    _test_pulse_controller()