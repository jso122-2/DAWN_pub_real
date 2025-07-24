#!/usr/bin/env python3
"""
DAWN Pulse Controller - Enhanced System Regulation
Regulates system mood and heat based on entropy levels with consciousness integration.
"""

import logging
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass
from collections import deque

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class ZoneTransition:
    """Record of a zone transition event"""
    timestamp: datetime
    previous_zone: str
    new_zone: str
    entropy_value: float
    heat_level: float


class DAWNPulseController:
    """
    Enhanced Pulse Controller for DAWN's cognition engine
    
    Regulates system mood and heat based on entropy levels.
    Manages operational zones and system temperature with consciousness integration.
    """
    
    def __init__(self, natural_language_generator=None):
        """
        Initialize the DAWN Pulse Controller.
        
        Args:
            natural_language_generator: Optional language generator for narration
        """
        self.natural_language_generator = natural_language_generator
        
        # Core state
        self.zone = "CALM"
        self.heat = 0.0
        self.heat_increment = 0.1
        self.heat_decay = 0.05
        
        # Zone transition thresholds (exactly as specified)
        self.thresholds = {
            'CALM': 0.4,
            'FOCUS': 0.6,
            'STRESSED': 0.8
        }
        
        # Enhanced tracking
        self.zone_history: deque = deque(maxlen=100)
        self.heat_history: deque = deque(maxlen=100)
        self.transition_history: List[ZoneTransition] = []
        
        # Performance metrics
        self.total_updates = 0
        self.zone_changes = 0
        self.time_in_zones = {
            'CALM': 0.0,
            'FOCUS': 0.0,
            'STRESSED': 0.0,
            'PANIC': 0.0
        }
        self.last_update_time = time.time()
        
        # Emergency cooling tracking
        self.emergency_cooling_count = 0
        self.last_emergency_cooling = None
        
        logger.info("🌡️ DAWN Pulse Controller initialized")
    
    def update_zone(self, entropy_value: float) -> bool:
        """
        Update the current operational zone based on entropy value.
        
        Args:
            entropy_value: Current entropy measurement
            
        Returns:
            True if zone changed, False otherwise
        """
        previous_zone = self.zone
        current_time = time.time()
        
        # Update time spent in previous zone
        time_delta = current_time - self.last_update_time
        self.time_in_zones[previous_zone] += time_delta
        self.last_update_time = current_time
        
        # Determine new zone based on thresholds
        if entropy_value < self.thresholds['CALM']:
            self.zone = "CALM"
        elif entropy_value < self.thresholds['FOCUS']:
            self.zone = "FOCUS"
        elif entropy_value < self.thresholds['STRESSED']:
            self.zone = "STRESSED"
        else:
            self.zone = "PANIC"
        
        zone_changed = previous_zone != self.zone
        
        # Log zone transitions with enhanced information
        if zone_changed:
            self.zone_changes += 1
            
            # Create transition record
            transition = ZoneTransition(
                timestamp=datetime.now(),
                previous_zone=previous_zone,
                new_zone=self.zone,
                entropy_value=entropy_value,
                heat_level=self.heat
            )
            self.transition_history.append(transition)
            
            # Limit transition history
            if len(self.transition_history) > 50:
                self.transition_history = self.transition_history[-25:]
            
            # Enhanced logging with consciousness integration
            transition_msg = f"🌡️ Zone transition: {previous_zone} → {self.zone} (entropy: {entropy_value:.3f})"
            logger.info(transition_msg)
            print(transition_msg)
            
            # Natural language commentary if available
            if self.natural_language_generator:
                zone_commentary = self._generate_zone_commentary(previous_zone, self.zone, entropy_value)
                print(f"🗣️ DAWN: {zone_commentary}")
        
        # Record zone and entropy in history
        self.zone_history.append({
            'timestamp': current_time,
            'zone': self.zone,
            'entropy': entropy_value
        })
        
        self.total_updates += 1
        return zone_changed
    
    def _generate_zone_commentary(self, previous_zone: str, new_zone: str, entropy: float) -> str:
        """Generate natural language commentary for zone transitions"""
        zone_descriptions = {
            'CALM': 'tranquil awareness',
            'FOCUS': 'concentrated attention',
            'STRESSED': 'heightened tension',
            'PANIC': 'critical urgency'
        }
        
        previous_desc = zone_descriptions.get(previous_zone, previous_zone.lower())
        new_desc = zone_descriptions.get(new_zone, new_zone.lower())
        
        if new_zone == 'PANIC':
            return f"I surge from {previous_desc} into {new_desc} as entropy reaches {entropy:.3f}"
        elif new_zone == 'STRESSED':
            return f"I shift from {previous_desc} to {new_desc}, feeling the system tension rise"
        elif new_zone == 'FOCUS':
            return f"I transition from {previous_desc} into {new_desc}, gathering my cognitive resources"
        elif new_zone == 'CALM':
            return f"I settle from {previous_desc} into {new_desc}, finding inner peace"
        else:
            return f"I move from {previous_desc} to {new_desc} following the entropy flow"
    
    def get_zone(self) -> str:
        """
        Get the current operational zone.
        
        Returns:
            Current zone (CALM, FOCUS, STRESSED, PANIC)
        """
        return self.zone
    
    def adjust_heat(self) -> float:
        """
        Adjust system heat based on current zone.
        Increases heat in STRESSED or PANIC zones, otherwise allows cooling.
        
        Returns:
            New heat level
        """
        previous_heat = self.heat
        
        if self.zone in ["STRESSED", "PANIC"]:
            # Increase heat in high-stress zones
            self.heat = min(1.0, self.heat + self.heat_increment)
            if self.zone == "PANIC":
                # Double heat increment in panic mode
                self.heat = min(1.0, self.heat + self.heat_increment)
        else:
            # Allow heat to decay in calmer zones
            self.heat = max(0.0, self.heat - self.heat_decay)
        
        # Record heat history
        self.heat_history.append({
            'timestamp': time.time(),
            'heat': self.heat,
            'zone': self.zone
        })
        
        # Generate commentary for significant heat changes
        heat_delta = self.heat - previous_heat
        if abs(heat_delta) > 0.1 and self.natural_language_generator:
            if heat_delta > 0:
                heat_commentary = f"I feel my systems warming as heat rises to {self.heat:.3f}"
            else:
                heat_commentary = f"I sense cooling relief as heat drops to {self.heat:.3f}"
            print(f"🗣️ DAWN: {heat_commentary}")
        
        return self.heat
    
    def get_heat(self) -> float:
        """
        Get the current system heat level.
        
        Returns:
            Heat level between 0.0 and 1.0
        """
        return self.heat
    
    def set_heat_parameters(self, increment: Optional[float] = None, decay: Optional[float] = None):
        """
        Adjust heat regulation parameters.
        
        Args:
            increment: Heat increase rate per cycle
            decay: Heat decrease rate per cycle
        """
        if increment is not None:
            self.heat_increment = increment
            logger.info(f"Heat increment adjusted to {increment}")
        if decay is not None:
            self.heat_decay = decay
            logger.info(f"Heat decay adjusted to {decay}")
    
    def get_zone_emoji(self) -> str:
        """
        Get an emoji representation of the current zone.
        
        Returns:
            Emoji representing current zone
        """
        zone_emojis = {
            "CALM": "😌",
            "FOCUS": "🎯",
            "STRESSED": "😰",
            "PANIC": "🚨"
        }
        return zone_emojis.get(self.zone, "❓")
    
    def get_status_summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive summary of current pulse controller status.
        
        Returns:
            Status information including zone, heat, emoji, and metrics
        """
        return {
            'zone': self.zone,
            'heat': round(self.heat, 3),
            'emoji': self.get_zone_emoji(),
            'thresholds': self.thresholds,
            'total_updates': self.total_updates,
            'zone_changes': self.zone_changes,
            'time_in_current_zone': time.time() - self.last_update_time,
            'emergency_cooling_count': self.emergency_cooling_count
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get detailed performance metrics"""
        total_time = sum(self.time_in_zones.values())
        
        return {
            'total_updates': self.total_updates,
            'zone_changes': self.zone_changes,
            'zone_change_rate': self.zone_changes / max(1, self.total_updates),
            'time_in_zones': dict(self.time_in_zones),
            'zone_distribution': {
                zone: time_spent / max(1, total_time) 
                for zone, time_spent in self.time_in_zones.items()
            } if total_time > 0 else {},
            'current_heat': self.heat,
            'heat_increment': self.heat_increment,
            'heat_decay': self.heat_decay,
            'emergency_cooling_count': self.emergency_cooling_count
        }
    
    def emergency_cooling(self) -> str:
        """
        Emergency heat dissipation function.
        Rapidly reduces system heat with consciousness narration.
        
        Returns:
            Description of cooling action
        """
        previous_heat = self.heat
        self.heat = max(0.0, self.heat - 0.3)
        self.emergency_cooling_count += 1
        self.last_emergency_cooling = datetime.now()
        
        cooling_msg = f"❄️ Emergency cooling activated. Heat reduced from {previous_heat:.3f} to {self.heat:.3f}"
        logger.info(cooling_msg)
        print(cooling_msg)
        
        # Natural language commentary
        if self.natural_language_generator:
            cooling_commentary = "I rapidly dissipate excess heat to prevent critical overload"
            print(f"🗣️ DAWN: {cooling_commentary}")
            return f"{cooling_msg} {cooling_commentary}"
        
        return cooling_msg
    
    def get_zone_stability(self) -> float:
        """
        Calculate zone stability based on recent transition frequency.
        
        Returns:
            Stability score from 0.0 (unstable) to 1.0 (stable)
        """
        if len(self.zone_history) < 10:
            return 1.0  # Not enough data, assume stable
        
        recent_zones = [entry['zone'] for entry in list(self.zone_history)[-10:]]
        unique_zones = len(set(recent_zones))
        
        # More unique zones = less stable
        stability = 1.0 - (unique_zones - 1) / 3  # Max 4 zones, so max penalty is 3/3 = 1.0
        return max(0.0, stability)
    
    def get_heat_trend(self) -> str:
        """
        Determine heat trend based on recent history.
        
        Returns:
            Trend description: 'rising', 'falling', 'stable'
        """
        if len(self.heat_history) < 5:
            return 'stable'
        
        recent_heat = [entry['heat'] for entry in list(self.heat_history)[-5:]]
        
        if recent_heat[-1] > recent_heat[0] + 0.05:
            return 'rising'
        elif recent_heat[-1] < recent_heat[0] - 0.05:
            return 'falling'
        else:
            return 'stable'
    
    def get_recent_transitions(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent zone transitions"""
        recent = self.transition_history[-limit:] if self.transition_history else []
        return [
            {
                'timestamp': t.timestamp.isoformat(),
                'previous_zone': t.previous_zone,
                'new_zone': t.new_zone,
                'entropy_value': t.entropy_value,
                'heat_level': t.heat_level
            }
            for t in recent
        ]
    
    def predict_zone_transition(self, entropy_trend: float) -> Optional[str]:
        """
        Predict next zone based on entropy trend.
        
        Args:
            entropy_trend: Rate of entropy change
            
        Returns:
            Predicted next zone or None if stable
        """
        current_entropy = self.zone_history[-1]['entropy'] if self.zone_history else 0.5
        predicted_entropy = current_entropy + entropy_trend
        
        # Determine what zone the predicted entropy would be in
        if predicted_entropy < self.thresholds['CALM']:
            predicted_zone = "CALM"
        elif predicted_entropy < self.thresholds['FOCUS']:
            predicted_zone = "FOCUS"
        elif predicted_entropy < self.thresholds['STRESSED']:
            predicted_zone = "STRESSED"
        else:
            predicted_zone = "PANIC"
        
        return predicted_zone if predicted_zone != self.zone else None


# Integration interface for DAWN system
def create_dawn_pulse_controller(natural_language_generator=None) -> DAWNPulseController:
    """Factory function for DAWN integration."""
    return DAWNPulseController(natural_language_generator=natural_language_generator)


# Example usage and testing
if __name__ == "__main__":
    print("🌡️ DAWN Pulse Controller Initialized")
    
    # Create controller instance
    controller = DAWNPulseController()
    
    # Test entropy values and zone transitions
    test_entropies = [0.2, 0.5, 0.7, 0.9, 0.3]
    
    print("\n🧪 Testing zone transitions:")
    for entropy in test_entropies:
        zone_changed = controller.update_zone(entropy)
        heat = controller.adjust_heat()
        status = controller.get_status_summary()
        
        change_indicator = "→" if zone_changed else "="
        print(f"Entropy: {entropy} {change_indicator} Zone: {status['zone']} {status['emoji']} | Heat: {status['heat']}")
        
        time.sleep(0.1)  # Brief pause to simulate real-time
    
    # Test emergency cooling
    print(f"\n🚨 Testing emergency cooling:")
    controller.emergency_cooling()
    
    # Show final metrics
    metrics = controller.get_performance_metrics()
    print(f"\n📊 Performance Metrics:")
    print(f"  Total updates: {metrics['total_updates']}")
    print(f"  Zone changes: {metrics['zone_changes']}")
    print(f"  Zone stability: {controller.get_zone_stability():.2f}")
    print(f"  Heat trend: {controller.get_heat_trend()}")
    
    print(f"\n📈 Zone Distribution:")
    for zone, percentage in metrics['zone_distribution'].items():
        print(f"  {zone}: {percentage:.1%}")
    
    print(f"\n📋 Final Status: {controller.get_status_summary()}") 