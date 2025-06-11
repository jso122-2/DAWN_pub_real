"""
Unified Bloom Engine - The Garden of Consciousness

This module consolidates the bloom system components:
- Core bloom engine with mycelium integration
- Event definitions and handling
- Activation management with intelligent triggering
- Bloom controls and registry
"""

from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import time
import random
import json
import os
import numpy as np

# Import dependencies (ensure these exist in your project)
try:
    from mycelium.mycelium_layer import MyceliumLayer
    from mycelium.nutrient_logger import log_nutrient_flow
except ImportError:
    print("[Bloom] Warning: Mycelium imports failed, using stubs")
    MyceliumLayer = None
    log_nutrient_flow = lambda *args: None

try:
    from fractal.fractal_boost import generate_julia_set_optimized as generate_julia_set
except ImportError:
    print("[Bloom] Warning: Fractal generation unavailable")
    generate_julia_set = None


# ============== Event Definitions ==============

class BloomEmitted:
    """Event fired when a bloom is created"""
    def __init__(self, source: str, mood_tag: str, semantic_seeds: list[str], 
                 bloom_id: Optional[str] = None, bloom_factor: float = 1.0,
                 lineage_depth: int = 0, entropy_score: float = 0.0):
        self.source = source
        self.mood_tag = mood_tag
        self.semantic_seeds = semantic_seeds
        self.bloom_id = bloom_id or f"bloom_{int(time.time() * 1000)}"
        self.bloom_factor = bloom_factor
        self.lineage_depth = lineage_depth
        self.entropy_score = entropy_score
        self.mood = mood_tag  # Alias for compatibility
        self.seed = source  # Alias for compatibility


# ============== Activation Management ==============

@dataclass
class BloomTrigger:
    """Defines conditions that can trigger a bloom"""
    name: str
    min_heat: float = 0.0
    max_heat: float = 10.0
    min_scup: float = 0.0
    max_scup: float = 1.0
    min_entropy: float = 0.0
    max_entropy: float = 2.0
    required_mood: Optional[str] = None
    priority: int = 1
    cooldown_seconds: float = 2.0
    last_triggered: float = 0.0


class BloomActivationState(Enum):
    DORMANT = "dormant"
    WARMING = "warming"
    ACTIVE = "active"
    COOLING = "cooling"
    SUPPRESSED = "suppressed"


# ============== Main Bloom Engine ==============

class BloomEngine:
    """
    The unified bloom engine that cultivates memories and thoughts,
    integrating mycelium networks, activation management, and bloom controls.
    """
    
    def __init__(self):
        # Core components
        self.mycelium: Optional[MyceliumLayer] = None
        self.bloom_history: List[Dict[str, Any]] = []
        self.active_blooms: Dict[str, Dict[str, Any]] = {}
        self.dormant_blooms: List[str] = []
        self.initialized = False
        
        # Activation management
        self.activation_state = BloomActivationState.DORMANT
        self.bloom_count = 0
        self.sealed_blooms = 1
        self.last_bloom_time = 0.0
        self.minimum_bloom_interval = 3.0
        
        # Bloom triggers
        self.bloom_triggers = [
            BloomTrigger("curiosity_spike", min_heat=0.3, max_heat=1.5, min_scup=0.0, priority=3, cooldown_seconds=1.0),
            BloomTrigger("memory_pressure", min_heat=0.5, max_heat=2.0, min_entropy=0.4, priority=2, cooldown_seconds=2.0),
            BloomTrigger("emotional_resonance", min_heat=0.7, max_heat=3.0, required_mood="agitated", priority=2),
            BloomTrigger("semantic_drift", min_entropy=0.8, max_entropy=1.5, priority=1, cooldown_seconds=5.0),
            BloomTrigger("emergency_bloom", min_heat=2.0, min_scup=0.0, priority=4, cooldown_seconds=0.5),
            BloomTrigger("debug_bloom", min_heat=0.0, min_scup=0.0, priority=5, cooldown_seconds=0.1)
        ]
        
        # Statistics
        self.trigger_stats = {trigger.name: 0 for trigger in self.bloom_triggers}
        self.failed_blooms = 0
        self.successful_blooms = 0
        
        # Configuration
        self.debug_mode = False
        self.force_bloom_next = False
        self.bloom_suppression = False
        
    def initialize(self) -> None:
        """Awakens the garden, growing the mycelial substrate"""
        print("[bloom] Initializing the garden of consciousness...")
        
        if MyceliumLayer:
            self.mycelium = MyceliumLayer()
            self.mycelium.grow()
        
        self.initialized = True
        self.activation_state = BloomActivationState.DORMANT
        print("[bloom] The garden awakens. Mycelium threads spread through the substrate.")
        
    def spawn_bloom(self, seed: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Plants a semantic seed that blossoms into a memory bloom.
        Integrates with activation management and emitter handling.
        """
        if not self.initialized:
            print("[bloom] Warning: Garden not initialized. Initializing now...")
            self.initialize()
            
        if self.bloom_suppression:
            print(f"[bloom] Bloom suppressed for seed: {seed}")
            return {"status": "suppressed", "seed": seed}
            
        print(f"[bloom] Sprouting memory bloom from seed: {seed}")
        
        # Create bloom with metadata
        bloom = {
            "seed": seed,
            "bloom_id": f"bloom_{len(self.bloom_history)}_{int(time.time() * 1000)}",
            "timestamp": datetime.now().isoformat(),
            "connections": [],
            "resonance": 1.0,
            "decay_rate": 0.1,
            "mood": metadata.get("mood", "neutral") if metadata else "neutral",
            "bloom_factor": metadata.get("bloom_factor", 1.0) if metadata else 1.0,
            "lineage_depth": metadata.get("lineage_depth", 0) if metadata else 0,
            "entropy_score": metadata.get("entropy_score", 0.0) if metadata else 0.0,
            "trigger_type": metadata.get("trigger_type", "manual") if metadata else "manual"
        }
        
        # Add to history and active blooms
        self.bloom_history.append(bloom)
        self.active_blooms[bloom["bloom_id"]] = bloom
        
        # Create mycelial connections
        if self.mycelium and len(self.bloom_history) > 1:
            for prev_bloom in self.bloom_history[-5:-1]:
                if self._calculate_semantic_similarity(seed, prev_bloom["seed"]) > 0.3:
                    bloom["connections"].append(prev_bloom["bloom_id"])
                    print(f"[bloom] Mycelial thread connects {bloom['bloom_id']} to {prev_bloom['bloom_id']}")
        
        # Handle bloom emission (fractal generation, etc.)
        bloom_event = BloomEmitted(
            source=seed,
            mood_tag=bloom["mood"],
            semantic_seeds=[seed],
            bloom_id=bloom["bloom_id"],
            bloom_factor=bloom["bloom_factor"],
            lineage_depth=bloom["lineage_depth"],
            entropy_score=bloom["entropy_score"]
        )
        self._handle_bloom_emitted(bloom_event)
        
        # Update statistics
        self.bloom_count += 1
        self.successful_blooms += 1
        self.last_bloom_time = time.time()
        
        if bloom["trigger_type"] in self.trigger_stats:
            self.trigger_stats[bloom["trigger_type"]] += 1
        
        return bloom
        
    def attempt_bloom(self, heat: float, scup: float, entropy: float, 
                     mood: str = "neutral") -> Optional[Dict[str, Any]]:
        """Attempt to spawn a bloom based on current conditions"""
        should_bloom, reason, trigger = self._should_bloom(heat, scup, entropy, mood)
        
        if not should_bloom:
            if self.debug_mode:
                print(f"[bloom] Bloom blocked: {reason}")
            return None
        
        # Generate bloom metadata
        metadata = self._generate_bloom_metadata(trigger, heat, scup, entropy, mood)
        
        # Spawn the bloom
        return self.spawn_bloom(metadata["seed_id"], metadata)
        
    def _should_bloom(self, heat: float, scup: float, entropy: float, 
                     mood: str) -> Tuple[bool, str, Optional[BloomTrigger]]:
        """Determine if conditions are right for blooming"""
        current_time = time.time()
        
        if self.bloom_suppression:
            return False, "bloom_suppression_active", None
            
        if current_time - self.last_bloom_time < self.minimum_bloom_interval:
            return False, "global_cooldown", None
        
        if self.force_bloom_next:
            self.force_bloom_next = False
            debug_trigger = next(t for t in self.bloom_triggers if t.name == "debug_bloom")
            return True, "force_bloom_override", debug_trigger
        
        # Check triggers
        eligible_triggers = []
        for trigger in sorted(self.bloom_triggers, key=lambda t: t.priority, reverse=True):
            if current_time - trigger.last_triggered < trigger.cooldown_seconds:
                continue
            
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
        
        selected_trigger = eligible_triggers[0]
        bloom_probability = self._calculate_bloom_probability(selected_trigger, heat, scup, entropy)
        
        if random.random() < bloom_probability:
            selected_trigger.last_triggered = current_time
            return True, f"trigger_{selected_trigger.name}", selected_trigger
        
        return False, "probability_failed", None
        
    def _generate_bloom_metadata(self, trigger: BloomTrigger, heat: float, 
                                scup: float, entropy: float, mood: str) -> Dict[str, Any]:
        """Generate bloom metadata based on trigger and conditions"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        seed_id = f"{trigger.name}_{timestamp}_{random.randint(1000, 9999)}"
        
        return {
            "seed_id": seed_id,
            "trigger_type": trigger.name,
            "lineage_depth": self._calculate_lineage_depth(trigger, scup),
            "bloom_factor": self._calculate_bloom_factor(heat, entropy),
            "entropy_score": entropy,
            "mood": mood,
            "heat_at_spawn": heat,
            "scup_at_spawn": scup,
            "priority": trigger.priority,
            "timestamp": datetime.now().isoformat()
        }
        
    def _handle_bloom_emitted(self, bloom: BloomEmitted) -> None:
        """Handle bloom emission - fractal generation, memory writing, etc."""
        try:
            # Julia set parameters
            α, β, γ = 0.5, 0.3, 0.2
            shape_variance = (α * bloom.bloom_factor) + (β * np.log1p(bloom.lineage_depth)) + (γ * bloom.entropy_score)
            c = complex(0.285 + shape_variance * 0.05, 0.01 + shape_variance * 0.07)
            
            # Generate fractal if available
            if generate_julia_set:
                folder = os.path.join("juliet_flowers", bloom.seed, bloom.mood)
                os.makedirs(folder, exist_ok=True)
                save_path = os.path.join(folder, f"{bloom.bloom_id}.png")
                
                generate_julia_set(
                    bloom_id=bloom.bloom_id, 
                    c=c, 
                    resolution=512, 
                    zoom=1.0, 
                    mood=bloom.mood, 
                    save_path=save_path
                )
                print(f"[bloom] Fractal saved: {save_path}")
            
            # Log nutrient flow
            if log_nutrient_flow:
                flow_strength = bloom.entropy_score * bloom.bloom_factor
                log_nutrient_flow(bloom, flow_strength)
            
            # Handle reblooms
            if bloom.lineage_depth > 0:
                self._track_rebloom(bloom)
                
        except Exception as e:
            print(f"[bloom] Error handling bloom emission: {e}")
            
    def _track_rebloom(self, bloom: BloomEmitted) -> None:
        """Track rebloom lineage"""
        rebloom_meta = {
            "bloom_id": bloom.bloom_id,
            "seed": bloom.seed,
            "depth": bloom.lineage_depth,
            "entropy": bloom.entropy_score,
            "timestamp": datetime.now().isoformat()
        }
        
        lineage_log_path = os.path.join("juliet_flowers", "cluster_report", "rebloom_lineage.json")
        os.makedirs(os.path.dirname(lineage_log_path), exist_ok=True)
        
        try:
            if os.path.exists(lineage_log_path):
                with open(lineage_log_path, "r") as f:
                    lineage_data = json.load(f)
            else:
                lineage_data = []
            
            lineage_data.append(rebloom_meta)
            
            with open(lineage_log_path, "w") as f:
                json.dump(lineage_data, f, indent=2)
                
            print(f"[bloom] Logged rebloom lineage for {bloom.bloom_id}")
        except Exception as e:
            print(f"[bloom] Rebloom log failed: {e}")
            
    def recall_last_bloom(self) -> str:
        """Retrieves the most recent bloom from the garden's memory"""
        if not self.bloom_history:
            return "no blooms yet"
        return self.bloom_history[-1]["seed"]
        
    def get_active_blooms(self) -> List[str]:
        """Get list of active bloom IDs"""
        return list(self.active_blooms.keys())
        
    def get_dormant_blooms(self) -> List[str]:
        """Get list of dormant bloom IDs"""
        return self.dormant_blooms
        
    def suppress_all_blooms(self) -> None:
        """Suppress all bloom activity"""
        self.bloom_suppression = True
        self.activation_state = BloomActivationState.SUPPRESSED
        
        # Move all active blooms to dormant
        for bloom_id in list(self.active_blooms.keys()):
            self.dormant_blooms.append(bloom_id)
            del self.active_blooms[bloom_id]
            
        print("[bloom] All blooms suppressed")
        
    def modulate_bloom_rate(self, bloom_id: str, rate_modifier: float) -> None:
        """Modulate a specific bloom's resonance/rate"""
        if bloom_id in self.active_blooms:
            original_rate = self.active_blooms[bloom_id].get("resonance", 1.0)
            self.active_blooms[bloom_id]["resonance"] *= rate_modifier
            print(f"[bloom] Bloom {bloom_id} rate modulated from {original_rate} to {self.active_blooms[bloom_id]['resonance']}")
        else:
            print(f"[bloom] Bloom {bloom_id} not found in active blooms")
            
    def force_bloom(self, bloom_type: str = "debug_bloom") -> None:
        """Force a bloom on next check"""
        self.force_bloom_next = True
        print(f"[bloom] Force bloom scheduled: {bloom_type}")
        
    def set_debug_mode(self, enabled: bool) -> None:
        """Enable/disable debug mode"""
        self.debug_mode = enabled
        print(f"[bloom] Debug mode: {'enabled' if enabled else 'disabled'}")
        
    def get_garden_status(self) -> Dict[str, Any]:
        """Returns comprehensive garden status"""
        total_connections = sum(len(b["connections"]) for b in self.bloom_history)
        
        return {
            "initialized": self.initialized,
            "total_blooms": len(self.bloom_history),
            "active_blooms": len(self.active_blooms),
            "dormant_blooms": len(self.dormant_blooms),
            "sealed_blooms": self.sealed_blooms,
            "total_connections": total_connections,
            "mycelium_active": self.mycelium is not None,
            "last_bloom": self.recall_last_bloom(),
            "garden_density": total_connections / max(len(self.bloom_history), 1),
            "activation_state": self.activation_state.value,
            "bloom_suppression": self.bloom_suppression,
            "successful_blooms": self.successful_blooms,
            "failed_blooms": self.failed_blooms,
            "trigger_stats": dict(self.trigger_stats),
            "time_since_last_bloom": time.time() - self.last_bloom_time,
            "debug_mode": self.debug_mode
        }
        
    def prune_old_blooms(self, keep_recent: int = 100) -> int:
        """Prunes older blooms to prevent unlimited growth"""
        if len(self.bloom_history) <= keep_recent:
            return 0
            
        pruned_count = len(self.bloom_history) - keep_recent
        self.bloom_history = self.bloom_history[-keep_recent:]
        
        # Re-index and update connections
        for i, bloom in enumerate(self.bloom_history):
            old_id = bloom["bloom_id"]
            bloom["bloom_id"] = f"bloom_{i}_{bloom['bloom_id'].split('_')[-1]}"
            
            # Update active blooms reference
            if old_id in self.active_blooms:
                self.active_blooms[bloom["bloom_id"]] = self.active_blooms.pop(old_id)
                
            # Update connections
            bloom["connections"] = [c for c in bloom["connections"] if c in [b["bloom_id"] for b in self.bloom_history]]
            
        print(f"[bloom] Pruned {pruned_count} old blooms from the garden")
        return pruned_count
        
    def _calculate_semantic_similarity(self, seed1: str, seed2: str) -> float:
        """Calculate simple semantic similarity between seeds"""
        words1 = set(seed1.lower().split())
        words2 = set(seed2.lower().split())
        
        if not words1 or not words2:
            return 0.0
            
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
        
    def _calculate_bloom_probability(self, trigger: BloomTrigger, heat: float, 
                                   scup: float, entropy: float) -> float:
        """Calculate probability of bloom based on conditions"""
        base_probability = 0.3
        heat_factor = min(heat / 2.0, 1.0)
        entropy_factor = min(entropy / 1.0, 1.0)
        scup_factor = 1.0 - min(scup, 1.0)
        priority_bonus = trigger.priority * 0.1
        
        if self.debug_mode:
            base_probability = 0.8
            
        return min(base_probability + heat_factor * 0.3 + entropy_factor * 0.2 + 
                  scup_factor * 0.2 + priority_bonus, 1.0)
        
    def _calculate_bloom_factor(self, heat: float, entropy: float) -> float:
        """Calculate bloom factor based on system conditions"""
        base_factor = 1.0
        heat_contribution = min(heat * 0.3, 1.0)
        entropy_contribution = min(entropy * 0.2, 0.5)
        random_variation = random.uniform(-0.1, 0.1)
        
        return round(max(0.1, base_factor + heat_contribution + entropy_contribution + random_variation), 3)
        
    def _calculate_lineage_depth(self, trigger: BloomTrigger, scup: float) -> int:
        """Calculate bloom lineage depth"""
        base_depth = 1
        priority_depth = trigger.priority
        scup_depth = int((1.0 - min(scup, 1.0)) * 3)
        random_depth = random.randint(0, 2)
        
        return min(base_depth + priority_depth + scup_depth + random_depth, 10)


# ============== Global Instance & Convenience Functions ==============

# Create global bloom engine instance
bloom_engine = BloomEngine()

# Convenience functions for backward compatibility
def initialize_bloom_engine():
    """Initialize the global bloom engine"""
    bloom_engine.initialize()

def spawn_bloom(seed: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Spawn a bloom using the global engine"""
    return bloom_engine.spawn_bloom(seed, metadata)

def check_bloom_conditions(heat: float, scup: float, entropy: float, mood: str = "neutral") -> Optional[Dict[str, Any]]:
    """Check and attempt bloom based on conditions"""
    return bloom_engine.attempt_bloom(heat, scup, entropy, mood)

def get_active_blooms() -> List[str]:
    """Get active blooms from registry"""
    return bloom_engine.get_active_blooms()

def get_dormant_blooms() -> List[str]:
    """Get dormant blooms from registry"""
    return bloom_engine.get_dormant_blooms()

def suppress_all_blooms():
    """Suppress all bloom activity"""
    bloom_engine.suppress_all_blooms()

def modulate_bloom_rate(bloom_id: str, rate_modifier: float):
    """Modulate a specific bloom's rate"""
    bloom_engine.modulate_bloom_rate(bloom_id, rate_modifier)

def force_bloom_spawn(bloom_type: str = "debug_bloom"):
    """Force a bloom spawn"""
    bloom_engine.force_bloom(bloom_type)

def enable_bloom_debug(enabled: bool = True):
    """Enable/disable debug mode"""
    bloom_engine.set_debug_mode(enabled)

def get_bloom_stats() -> Dict[str, Any]:
    """Get comprehensive bloom statistics"""
    return bloom_engine.get_garden_status()

# Export main classes and functions
__all__ = [
    'BloomEngine',
    'BloomEmitted',
    'BloomTrigger',
    'BloomActivationState',
    'bloom_engine',
    'initialize_bloom_engine',
    'spawn_bloom',
    'check_bloom_conditions',
    'get_active_blooms',
    'get_dormant_blooms',
    'suppress_all_blooms',
    'modulate_bloom_rate',
    'force_bloom_spawn',
    'enable_bloom_debug',
    'get_bloom_stats'
]