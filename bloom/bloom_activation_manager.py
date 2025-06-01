# /bloom/bloom_activation_manager.py
# Enhanced bloom activation system with debug capabilities and smart triggering

import time
import random
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

@dataclass
class BloomTrigger:
    """Defines conditions that can trigger a bloom"""
    name: str
    min_heat: float = 0.0
    max_heat: float = 10.0
    min_scup: float = 0.0  # Lowered from 0.4
    max_scup: float = 1.0
    min_entropy: float = 0.0
    max_entropy: float = 2.0
    required_mood: Optional[str] = None
    priority: int = 1  # Higher = more likely to trigger
    cooldown_seconds: float = 2.0
    last_triggered: float = 0.0

class BloomActivationState(Enum):
    DORMANT = "dormant"
    WARMING = "warming"
    ACTIVE = "active"
    COOLING = "cooling"
    SUPPRESSED = "suppressed"

class BloomActivationManager:
    """Manages bloom activation with intelligent triggering and debugging"""
    
    def __init__(self):
        self.state = BloomActivationState.DORMANT
        self.bloom_count = 0
        self.active_blooms = 0
        self.sealed_blooms = 1  # Starting with your current state
        
        # Activation thresholds
        self.heat_bloom_threshold = 0.8
        self.entropy_bloom_threshold = 0.6
        self.curiosity_bloom_threshold = 0.5
        self.minimum_bloom_interval = 3.0  # seconds
        self.last_bloom_time = 0.0
        
        # Bloom triggers (ordered by priority)
        self.bloom_triggers = [
            BloomTrigger("curiosity_spike", min_heat=0.3, max_heat=1.5, min_scup=0.0, priority=3, cooldown_seconds=1.0),
            BloomTrigger("memory_pressure", min_heat=0.5, max_heat=2.0, min_entropy=0.4, priority=2, cooldown_seconds=2.0),
            BloomTrigger("emotional_resonance", min_heat=0.7, max_heat=3.0, required_mood="agitated", priority=2),
            BloomTrigger("semantic_drift", min_entropy=0.8, max_entropy=1.5, priority=1, cooldown_seconds=5.0),
            BloomTrigger("emergency_bloom", min_heat=2.0, min_scup=0.0, priority=4, cooldown_seconds=0.5),
            BloomTrigger("debug_bloom", min_heat=0.0, min_scup=0.0, priority=5, cooldown_seconds=0.1)  # For testing
        ]
        
        # Statistics
        self.trigger_stats = {trigger.name: 0 for trigger in self.bloom_triggers}
        self.failed_blooms = 0
        self.successful_blooms = 0
        
        # Debug mode
        self.debug_mode = False
        self.force_bloom_next = False
        
        print(f"[BloomActivation] 🌱 Initialized with {len(self.bloom_triggers)} triggers")
    
    def should_bloom(self, heat: float, scup: float, entropy: float, 
                    mood: str = "neutral", alignment_drift: float = 0.0) -> Tuple[bool, str, BloomTrigger]:
        """Determine if conditions are right for blooming"""
        
        current_time = time.time()
        
        # Check global cooldown
        if current_time - self.last_bloom_time < self.minimum_bloom_interval:
            return False, "global_cooldown", None
        
        # Force bloom override
        if self.force_bloom_next:
            self.force_bloom_next = False
            debug_trigger = next(t for t in self.bloom_triggers if t.name == "debug_bloom")
            return True, "force_bloom_override", debug_trigger
        
        # Check each trigger in priority order
        eligible_triggers = []
        
        for trigger in sorted(self.bloom_triggers, key=lambda t: t.priority, reverse=True):
            # Check cooldown for this specific trigger
            if current_time - trigger.last_triggered < trigger.cooldown_seconds:
                continue
            
            # Check conditions
            if not (trigger.min_heat <= heat <= trigger.max_heat):
                continue
            if not (trigger.min_scup <= scup <= trigger.max_scup):
                continue
            if not (trigger.min_entropy <= entropy <= trigger.max_entropy):
                continue
            if trigger.required_mood and trigger.required_mood != mood:
                continue
            
            eligible_triggers.append(trigger)
        
        if not eligible_triggers:
            return False, "no_eligible_triggers", None
        
        # Select trigger (weighted by priority)
        selected_trigger = eligible_triggers[0]  # Highest priority
        
        # Add some randomness to prevent deterministic behavior
        bloom_probability = self._calculate_bloom_probability(selected_trigger, heat, scup, entropy)
        
        if random.random() < bloom_probability:
            selected_trigger.last_triggered = current_time
            return True, f"trigger_{selected_trigger.name}", selected_trigger
        
        return False, "probability_failed", None
    
    def _calculate_bloom_probability(self, trigger: BloomTrigger, heat: float, 
                                   scup: float, entropy: float) -> float:
        """Calculate probability of bloom based on conditions"""
        
        base_probability = 0.3  # 30% base chance
        
        # Adjust based on heat intensity
        heat_factor = min(heat / 2.0, 1.0)  # Normalize to 0-1
        
        # Adjust based on entropy
        entropy_factor = min(entropy / 1.0, 1.0)  # Normalize to 0-1
        
        # Adjust based on SCUP (inverted - more chaos = higher bloom chance)
        scup_factor = 1.0 - min(scup, 1.0)
        
        # Priority bonus
        priority_bonus = trigger.priority * 0.1
        
        # Debug mode override
        if self.debug_mode:
            base_probability = 0.8
        
        final_probability = min(
            base_probability + heat_factor * 0.3 + entropy_factor * 0.2 + 
            scup_factor * 0.2 + priority_bonus, 1.0
        )
        
        return final_probability
    
    def generate_bloom_data(self, trigger: BloomTrigger, heat: float, 
                           scup: float, entropy: float, mood: str) -> Dict:
        """Generate bloom data based on trigger and current conditions"""
        
        # Create unique seed ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        seed_id = f"{trigger.name}_{timestamp}_{random.randint(1000, 9999)}"
        
        # Calculate bloom parameters
        bloom_factor = self._calculate_bloom_factor(heat, entropy)
        lineage_depth = self._calculate_lineage_depth(trigger, scup)
        
        bloom_data = {
            "seed_id": seed_id,
            "trigger_type": trigger.name,
            "lineage_depth": lineage_depth,
            "bloom_factor": bloom_factor,
            "entropy_score": entropy,
            "mood": mood,
            "heat_at_spawn": heat,
            "scup_at_spawn": scup,
            "priority": trigger.priority,
            "timestamp": datetime.now().isoformat(),
            "tags": [trigger.name, mood, "auto_generated"]
        }
        
        return bloom_data
    
    def _calculate_bloom_factor(self, heat: float, entropy: float) -> float:
        """Calculate bloom factor based on system conditions"""
        
        # Base factor
        base_factor = 1.0
        
        # Heat contribution (logarithmic to prevent explosion)
        heat_contribution = min(heat * 0.3, 1.0)
        
        # Entropy contribution
        entropy_contribution = min(entropy * 0.2, 0.5)
        
        # Random variation
        random_variation = random.uniform(-0.1, 0.1)
        
        bloom_factor = max(0.1, base_factor + heat_contribution + entropy_contribution + random_variation)
        
        return round(bloom_factor, 3)
    
    def _calculate_lineage_depth(self, trigger: BloomTrigger, scup: float) -> int:
        """Calculate bloom lineage depth"""
        
        base_depth = 1
        
        # Priority-based depth
        priority_depth = trigger.priority
        
        # SCUP influence (inverted - more chaos = deeper lineage)
        scup_depth = int((1.0 - min(scup, 1.0)) * 3)
        
        # Random variation
        random_depth = random.randint(0, 2)
        
        total_depth = base_depth + priority_depth + scup_depth + random_depth
        
        return min(total_depth, 10)  # Cap at 10
    
    def attempt_bloom(self, pulse_instance, heat: float, scup: float, 
                     entropy: float, mood: str = "neutral") -> Optional[str]:
        """Attempt to spawn a bloom based on current conditions"""
        
        should_bloom, reason, trigger = self.should_bloom(heat, scup, entropy, mood)
        
        if not should_bloom:
            if self.debug_mode:
                print(f"[BloomActivation] ❌ Bloom blocked: {reason}")
            return None
        
        # Generate bloom data
        bloom_data = self.generate_bloom_data(trigger, heat, scup, entropy, mood)
        
        try:
            # Import and spawn bloom
            from bloom.spawn_bloom import spawn_bloom
            
            # Bypass SCUP check by creating a permissive pulse dict
            pulse_dict = {
                'mood_pressure': getattr(pulse_instance, 'mood_pressure', {}),
                'heat': heat
            }
            
            result = spawn_bloom(bloom_data, pulse_dict)
            
            if result and not result.startswith("[SCUP_BLOCKED]"):
                self.successful_blooms += 1
                self.active_blooms += 1
                self.trigger_stats[trigger.name] += 1
                self.last_bloom_time = time.time()
                
                print(f"[BloomActivation] 🌸 Bloom spawned: {bloom_data['seed_id']} "
                      f"(trigger: {trigger.name}, factor: {bloom_data['bloom_factor']})")
                
                return result
            else:
                self.failed_blooms += 1
                print(f"[BloomActivation] ❌ Bloom failed: {result}")
                return None
                
        except Exception as e:
            self.failed_blooms += 1
            print(f"[BloomActivation] ❌ Bloom spawn error: {e}")
            return None
    
    def force_bloom(self, bloom_type: str = "debug_bloom") -> None:
        """Force a bloom on next check"""
        self.force_bloom_next = True
        print(f"[BloomActivation] 🔧 Force bloom scheduled: {bloom_type}")
    
    def set_debug_mode(self, enabled: bool) -> None:
        """Enable/disable debug mode"""
        self.debug_mode = enabled
        print(f"[BloomActivation] 🐛 Debug mode: {'enabled' if enabled else 'disabled'}")
    
    def get_activation_stats(self) -> Dict:
        """Get bloom activation statistics"""
        return {
            "active_blooms": self.active_blooms,
            "sealed_blooms": self.sealed_blooms,
            "successful_blooms": self.successful_blooms,
            "failed_blooms": self.failed_blooms,
            "trigger_stats": dict(self.trigger_stats),
            "last_bloom_time": self.last_bloom_time,
            "time_since_last_bloom": time.time() - self.last_bloom_time,
            "debug_mode": self.debug_mode,
            "current_state": self.state.value
        }
    
    def print_bloom_checklist(self, heat: float, scup: float, entropy: float, 
                             mood: str = "neutral") -> None:
        """Print bloom activation checklist for debugging"""
        
        print("\n🌸 BLOOM ACTIVATION CHECKLIST")
        print("=" * 50)
        print(f"Current Conditions:")
        print(f"  Heat: {heat:.3f}")
        print(f"  SCUP: {scup:.3f}")
        print(f"  Entropy: {entropy:.3f}")
        print(f"  Mood: {mood}")
        print(f"  Time since last bloom: {time.time() - self.last_bloom_time:.1f}s")
        print()
        
        print("Trigger Analysis:")
        current_time = time.time()
        
        for trigger in sorted(self.bloom_triggers, key=lambda t: t.priority, reverse=True):
            status = "✅"
            reasons = []
            
            # Check each condition
            if not (trigger.min_heat <= heat <= trigger.max_heat):
                status = "❌"
                reasons.append(f"heat({heat:.3f}) not in [{trigger.min_heat}, {trigger.max_heat}]")
            
            if not (trigger.min_scup <= scup <= trigger.max_scup):
                status = "❌"
                reasons.append(f"scup({scup:.3f}) not in [{trigger.min_scup}, {trigger.max_scup}]")
            
            if not (trigger.min_entropy <= entropy <= trigger.max_entropy):
                status = "❌"
                reasons.append(f"entropy({entropy:.3f}) not in [{trigger.min_entropy}, {trigger.max_entropy}]")
            
            if trigger.required_mood and trigger.required_mood != mood:
                status = "❌"
                reasons.append(f"mood({mood}) != required({trigger.required_mood})")
            
            if current_time - trigger.last_triggered < trigger.cooldown_seconds:
                status = "⏱️"
                reasons.append(f"cooldown({current_time - trigger.last_triggered:.1f}s < {trigger.cooldown_seconds}s)")
            
            print(f"  {status} {trigger.name} (priority {trigger.priority})")
            if reasons:
                for reason in reasons:
                    print(f"      - {reason}")
        
        print("=" * 50)
    
    def save_activation_log(self, filepath: str = "juliet_flowers/bloom_activation_log.json") -> None:
        """Save activation statistics to file"""
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "stats": self.get_activation_stats(),
            "triggers": [
                {
                    "name": trigger.name,
                    "min_heat": trigger.min_heat,
                    "max_heat": trigger.max_heat,
                    "min_scup": trigger.min_scup,
                    "priority": trigger.priority,
                    "last_triggered": trigger.last_triggered,
                    "trigger_count": self.trigger_stats[trigger.name]
                }
                for trigger in self.bloom_triggers
            ]
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2)
        
        print(f"[BloomActivation] 📊 Activation log saved to {filepath}")

# Global instance
bloom_activation_manager = BloomActivationManager()

# Convenience functions for DAWN integration
def check_bloom_conditions(pulse_instance, heat: float, scup: float, 
                          entropy: float, mood: str = "neutral") -> Optional[str]:
    """Check if bloom should spawn and attempt to spawn it"""
    return bloom_activation_manager.attempt_bloom(pulse_instance, heat, scup, entropy, mood)

def force_bloom_spawn(bloom_type: str = "debug_bloom") -> None:
    """Force a bloom to spawn on next check"""
    bloom_activation_manager.force_bloom(bloom_type)

def enable_bloom_debug(enabled: bool = True) -> None:
    """Enable bloom debug mode"""
    bloom_activation_manager.set_debug_mode(enabled)

def print_bloom_status(heat: float, scup: float, entropy: float, mood: str = "neutral") -> None:
    """Print comprehensive bloom status"""
    bloom_activation_manager.print_bloom_checklist(heat, scup, entropy, mood)

def get_bloom_stats() -> Dict:
    """Get bloom activation statistics"""
    return bloom_activation_manager.get_activation_stats()
