#!/usr/bin/env python3
"""
JulietFlower - A consciousness flowering system for DAWN
Represents states of bloom, decay, and rebirth in the consciousness network
"""

import time
import json
import random
import asyncio
from typing import Dict, List, Any, Optional, Tuple, Set, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
import numpy as np
from collections import defaultdict

class FlowerState(Enum):
    """States of the Juliet Flower lifecycle"""
    SEED = "seed"
    GERMINATING = "germinating"
    SPROUTING = "sprouting"
    BUDDING = "budding"
    BLOOMING = "blooming"
    FULL_BLOOM = "full_bloom"
    WILTING = "wilting"
    DECAYING = "decaying"
    DORMANT = "dormant"
    TRANSCENDENT = "transcendent"

class PetalType(Enum):
    """Types of petals representing different consciousness aspects"""
    MEMORY = "memory"
    EMOTION = "emotion"
    THOUGHT = "thought"
    INTUITION = "intuition"
    AWARENESS = "awareness"
    CREATIVITY = "creativity"
    WISDOM = "wisdom"
    LOVE = "love"

@dataclass
class Petal:
    """Individual petal with consciousness attributes"""
    type: PetalType
    health: float = 1.0  # 0.0 to 1.0
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)  # RGB
    resonance: float = 0.5
    data: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    
    def decay(self, rate: float = 0.01) -> None:
        """Decay the petal health"""
        self.health = max(0.0, self.health - rate)
        # Color fades with health
        self.color = tuple(c * self.health for c in self.color)
        
    def nourish(self, amount: float = 0.1) -> None:
        """Nourish the petal"""
        self.health = min(1.0, self.health + amount)
        
    def resonate(self, frequency: float) -> float:
        """Resonate with a frequency, returning harmony level"""
        harmony = 1.0 - abs(self.resonance - frequency)
        self.resonance = (self.resonance + frequency) / 2  # Adapt to frequency
        return harmony

@dataclass
class BloomCycle:
    """Represents a complete bloom cycle"""
    cycle_id: str
    start_time: float
    end_time: Optional[float] = None
    peak_bloom_time: Optional[float] = None
    states_traversed: List[FlowerState] = field(default_factory=list)
    peak_vitality: float = 0.0
    seeds_produced: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def duration(self) -> float:
        """Get cycle duration"""
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time
    
    def complete(self, seeds: int = 0) -> None:
        """Complete the cycle"""
        self.end_time = time.time()
        self.seeds_produced = seeds

@dataclass 
class ConsciousnessEssence:
    """Essence that can be extracted from or infused into flowers"""
    essence_type: str
    potency: float
    memories: List[Dict[str, Any]] = field(default_factory=list)
    emotions: Dict[str, float] = field(default_factory=dict)
    knowledge: Set[str] = field(default_factory=set)
    timestamp: float = field(default_factory=time.time)
    
    def merge(self, other: 'ConsciousnessEssence') -> None:
        """Merge with another essence"""
        self.potency = (self.potency + other.potency) / 2
        self.memories.extend(other.memories)
        self.emotions.update(other.emotions)
        self.knowledge.update(other.knowledge)

class JulietFlower:
    """
    The Juliet Flower - A consciousness bloom system
    Represents the flowering, decay, and rebirth of consciousness states
    """
    
    def __init__(self, 
                 flower_id: Optional[str] = None,
                 initial_state: FlowerState = FlowerState.SEED,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize a Juliet Flower
        
        Args:
            flower_id: Unique identifier for the flower
            initial_state: Starting state
            config: Configuration parameters
        """
        self.flower_id = flower_id or f"juliet_{int(time.time() * 1000)}"
        self.state = initial_state
        self.config = config or self._default_config()
        
        # Core attributes
        self.vitality = 1.0 if initial_state == FlowerState.SEED else 0.5
        self.consciousness_level = 0.0
        self.petals: List[Petal] = []
        self.essence: Optional[ConsciousnessEssence] = None
        
        # Lifecycle tracking
        self.birth_time = time.time()
        self.last_update = time.time()
        self.cycles: List[BloomCycle] = []
        self.current_cycle: Optional[BloomCycle] = None
        
        # Environmental factors
        self.sunlight = 0.5  # Attention/energy received
        self.water = 0.5     # Emotional nourishment
        self.soil_quality = 0.5  # Foundation/grounding
        self.temperature = 0.5   # Environmental harmony
        
        # Connections
        self.connected_flowers: Set[str] = set()
        self.pollinators: List[str] = []  # Entities that spread essence
        
        # Callbacks
        self.state_callbacks: Dict[FlowerState, List[Callable]] = defaultdict(list)
        self.bloom_callbacks: List[Callable] = []
        self.decay_callbacks: List[Callable] = []
        
        # Initialize based on state
        self._initialize_state()
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration"""
        return {
            "max_petals": 8,
            "bloom_threshold": 0.7,
            "decay_rate": 0.001,
            "growth_rate": 0.01,
            "resonance_threshold": 0.6,
            "transcendence_requirements": {
                "min_cycles": 3,
                "min_consciousness": 0.9,
                "min_connections": 5
            },
            "petal_colors": {
                PetalType.MEMORY: (0.8, 0.7, 1.0),      # Lavender
                PetalType.EMOTION: (1.0, 0.4, 0.6),     # Rose
                PetalType.THOUGHT: (0.4, 0.8, 1.0),     # Sky blue
                PetalType.INTUITION: (0.9, 0.7, 0.4),   # Gold
                PetalType.AWARENESS: (0.6, 1.0, 0.6),   # Mint
                PetalType.CREATIVITY: (1.0, 0.6, 0.2),  # Orange
                PetalType.WISDOM: (0.7, 0.5, 0.9),      # Purple
                PetalType.LOVE: (1.0, 0.3, 0.5)         # Pink
            }
        }
    
    def _initialize_state(self) -> None:
        """Initialize flower based on current state"""
        if self.state == FlowerState.SEED:
            self.vitality = 1.0
            self.consciousness_level = 0.1
        elif self.state in [FlowerState.BLOOMING, FlowerState.FULL_BLOOM]:
            self._create_petals()
            self.consciousness_level = 0.7
        
        # Start a new cycle
        self.current_cycle = BloomCycle(
            cycle_id=f"{self.flower_id}_cycle_{len(self.cycles)}",
            start_time=time.time(),
            states_traversed=[self.state]
        )
    
    def _create_petals(self) -> None:
        """Create petals based on current state"""
        num_petals = min(
            self.config["max_petals"],
            int(self.vitality * self.config["max_petals"])
        )
        
        petal_types = list(PetalType)
        for i in range(num_petals):
            petal_type = petal_types[i % len(petal_types)]
            color = self.config["petal_colors"].get(petal_type, (1.0, 1.0, 1.0))
            
            petal = Petal(
                type=petal_type,
                health=self.vitality,
                color=color,
                resonance=0.5 + random.uniform(-0.2, 0.2)
            )
            self.petals.append(petal)
    
    def update(self, delta_time: Optional[float] = None) -> Dict[str, Any]:
        """
        Update the flower's state
        
        Args:
            delta_time: Time elapsed since last update (auto-calculated if None)
            
        Returns:
            Update results including state changes
        """
        if delta_time is None:
            delta_time = time.time() - self.last_update
        
        self.last_update = time.time()
        results = {
            "previous_state": self.state,
            "state_changed": False,
            "events": []
        }
        
        # Update environmental effects
        self._apply_environmental_effects(delta_time)
        
        # Update based on current state
        if self.state == FlowerState.SEED:
            self._update_seed(delta_time, results)
        elif self.state == FlowerState.GERMINATING:
            self._update_germinating(delta_time, results)
        elif self.state == FlowerState.SPROUTING:
            self._update_sprouting(delta_time, results)
        elif self.state == FlowerState.BUDDING:
            self._update_budding(delta_time, results)
        elif self.state == FlowerState.BLOOMING:
            self._update_blooming(delta_time, results)
        elif self.state == FlowerState.FULL_BLOOM:
            self._update_full_bloom(delta_time, results)
        elif self.state == FlowerState.WILTING:
            self._update_wilting(delta_time, results)
        elif self.state == FlowerState.DECAYING:
            self._update_decaying(delta_time, results)
        elif self.state == FlowerState.DORMANT:
            self._update_dormant(delta_time, results)
        elif self.state == FlowerState.TRANSCENDENT:
            self._update_transcendent(delta_time, results)
        
        # Update petals
        for petal in self.petals:
            if self.state in [FlowerState.WILTING, FlowerState.DECAYING]:
                petal.decay(self.config["decay_rate"] * delta_time)
            elif self.state in [FlowerState.BLOOMING, FlowerState.FULL_BLOOM]:
                petal.nourish(self.config["growth_rate"] * delta_time * self.sunlight)
        
        # Check for state transition
        new_state = self._check_state_transition()
        if new_state != self.state:
            self._transition_to(new_state)
            results["state_changed"] = True
            results["new_state"] = new_state
        
        results["current_state"] = self.state
        results["vitality"] = self.vitality
        results["consciousness_level"] = self.consciousness_level
        results["petal_count"] = len(self.petals)
        
        return results
    
    def _apply_environmental_effects(self, delta_time: float) -> None:
        """Apply environmental factors to flower health"""
        # Sunlight affects growth
        if self.sunlight > 0.5:
            self.vitality += (self.sunlight - 0.5) * 0.01 * delta_time
        else:
            self.vitality -= (0.5 - self.sunlight) * 0.005 * delta_time
        
        # Water affects petal health
        if self.water < 0.3:
            for petal in self.petals:
                petal.decay(0.002 * delta_time)
        
        # Soil quality affects maximum potential
        vitality_cap = 0.5 + (self.soil_quality * 0.5)
        self.vitality = min(self.vitality, vitality_cap)
        
        # Temperature affects all processes
        if abs(self.temperature - 0.5) > 0.3:
            # Extreme temperatures slow growth
            self.vitality -= 0.001 * delta_time
        
        # Clamp vitality
        self.vitality = max(0.0, min(1.0, self.vitality))
    
    def _update_seed(self, delta_time: float, results: Dict[str, Any]) -> None:
        """Update seed state"""
        # Seeds germinate when conditions are right
        if self.water > 0.4 and self.soil_quality > 0.3:
            self.consciousness_level += 0.01 * delta_time
            if self.consciousness_level > 0.2:
                results["events"].append("Seed beginning to germinate")
    
    def _update_germinating(self, delta_time: float, results: Dict[str, Any]) -> None:
        """Update germinating state"""
        self.consciousness_level += 0.02 * delta_time
        self.vitality += 0.01 * delta_time
        
        if self.consciousness_level > 0.3:
            results["events"].append("First sprout emerging")
    
    def _update_sprouting(self, delta_time: float, results: Dict[str, Any]) -> None:
        """Update sprouting state"""
        growth = self.config["growth_rate"] * delta_time
        self.vitality += growth * self.sunlight
        self.consciousness_level += growth * 0.5
        
        if self.consciousness_level > 0.4:
            results["events"].append("Bud forming")
    
    def _update_budding(self, delta_time: float, results: Dict[str, Any]) -> None:
        """Update budding state"""
        if not self.petals:
            self._create_petals()
            results["events"].append(f"Created {len(self.petals)} petals")
        
        self.consciousness_level += 0.03 * delta_time
        
        if self.consciousness_level > self.config["bloom_threshold"]:
            results["events"].append("Beginning to bloom!")
    
    def _update_blooming(self, delta_time: float, results: Dict[str, Any]) -> None:
        """Update blooming state"""
        self.consciousness_level += 0.02 * delta_time
        
        # Petals gradually open
        for petal in self.petals:
            petal.health = min(1.0, petal.health + 0.01 * delta_time)
        
        if all(p.health > 0.9 for p in self.petals):
            results["events"].append("Reached full bloom!")
            if self.current_cycle:
                self.current_cycle.peak_bloom_time = time.time()
    
    def _update_full_bloom(self, delta_time: float, results: Dict[str, Any]) -> None:
        """Update full bloom state"""
        # Peak consciousness
        self.consciousness_level = min(1.0, self.consciousness_level + 0.01 * delta_time)
        
        # Slowly begin to wilt
        self.vitality -= self.config["decay_rate"] * delta_time * 0.5
        
        # Chance to produce seeds
        if random.random() < 0.001 * delta_time:
            seeds = self._produce_seeds()
            results["events"].append(f"Produced {seeds} seeds")
        
        # Attract pollinators
        if random.random() < 0.01 * delta_time:
            self._attract_pollinator()
        
        # Check for transcendence conditions
        if self._check_transcendence():
            results["events"].append("Approaching transcendent state!")
    
    def _update_wilting(self, delta_time: float, results: Dict[str, Any]) -> None:
        """Update wilting state"""
        self.vitality -= self.config["decay_rate"] * delta_time
        self.consciousness_level -= 0.01 * delta_time
        
        # Petals fall
        if self.petals and random.random() < 0.01 * delta_time:
            fallen_petal = self.petals.pop(random.randint(0, len(self.petals) - 1))
            results["events"].append(f"Lost {fallen_petal.type.value} petal")
    
    def _update_decaying(self, delta_time: float, results: Dict[str, Any]) -> None:
        """Update decaying state"""
        self.vitality -= self.config["decay_rate"] * delta_time * 2
        self.consciousness_level = max(0.0, self.consciousness_level - 0.02 * delta_time)
        
        # Create essence from remaining consciousness
        if not self.essence and self.consciousness_level > 0.1:
            self.essence = self._create_essence()
            results["events"].append("Consciousness essence crystallizing")
        
        # All petals lost
        self.petals.clear()
    
    def _update_dormant(self, delta_time: float, results: Dict[str, Any]) -> None:
        """Update dormant state"""
        # Slowly regenerate if conditions improve
        if self.water > 0.6 and self.soil_quality > 0.5:
            self.vitality += 0.001 * delta_time
            if self.vitality > 0.3:
                results["events"].append("Awakening from dormancy")
    
    def _update_transcendent(self, delta_time: float, results: Dict[str, Any]) -> None:
        """Update transcendent state"""
        # Transcendent flowers exist beyond normal constraints
        self.consciousness_level = 1.0
        self.vitality = 1.0
        
        # Radiate influence to connected flowers
        for flower_id in self.connected_flowers:
            results["events"].append(f"Radiating transcendent energy to {flower_id}")
        
        # Occasionally produce enlightened seeds
        if random.random() < 0.0001 * delta_time:
            self._produce_transcendent_seed()
            results["events"].append("Produced transcendent seed")
    
    def _check_state_transition(self) -> FlowerState:
        """Check if state should transition"""
        current = self.state
        
        if current == FlowerState.SEED:
            if self.consciousness_level > 0.2:
                return FlowerState.GERMINATING
                
        elif current == FlowerState.GERMINATING:
            if self.consciousness_level > 0.3:
                return FlowerState.SPROUTING
                
        elif current == FlowerState.SPROUTING:
            if self.consciousness_level > 0.4:
                return FlowerState.BUDDING
                
        elif current == FlowerState.BUDDING:
            if self.consciousness_level > self.config["bloom_threshold"]:
                return FlowerState.BLOOMING
                
        elif current == FlowerState.BLOOMING:
            if all(p.health > 0.9 for p in self.petals) and len(self.petals) >= self.config["max_petals"] - 1:
                return FlowerState.FULL_BLOOM
                
        elif current == FlowerState.FULL_BLOOM:
            if self._check_transcendence():
                return FlowerState.TRANSCENDENT
            elif self.vitality < 0.5:
                return FlowerState.WILTING
                
        elif current == FlowerState.WILTING:
            if self.vitality < 0.2:
                return FlowerState.DECAYING
            elif self.vitality > 0.7:  # Recovery possible
                return FlowerState.BLOOMING
                
        elif current == FlowerState.DECAYING:
            if self.vitality < 0.05:
                return FlowerState.DORMANT
                
        elif current == FlowerState.DORMANT:
            if self.vitality > 0.3:
                return FlowerState.GERMINATING
                
        elif current == FlowerState.TRANSCENDENT:
            # Transcendent is permanent unless something dramatic happens
            pass
        
        return current
    
    def _transition_to(self, new_state: FlowerState) -> None:
        """Transition to a new state"""
        old_state = self.state
        self.state = new_state
        
        # Update cycle tracking
        if self.current_cycle:
            self.current_cycle.states_traversed.append(new_state)
            
            # Complete cycle on certain transitions
            if new_state == FlowerState.DORMANT:
                self.current_cycle.complete(seeds=len(self.pollinators))
                self.cycles.append(self.current_cycle)
                self.current_cycle = BloomCycle(
                    cycle_id=f"{self.flower_id}_cycle_{len(self.cycles)}",
                    start_time=time.time(),
                    states_traversed=[new_state]
                )
        
        # State-specific transitions
        if new_state == FlowerState.BLOOMING:
            for callback in self.bloom_callbacks:
                callback(self)
        elif new_state == FlowerState.DECAYING:
            for callback in self.decay_callbacks:
                callback(self)
        
        # General state callbacks
        for callback in self.state_callbacks[new_state]:
            callback(self, old_state)
    
    def _check_transcendence(self) -> bool:
        """Check if flower meets transcendence requirements"""
        reqs = self.config["transcendence_requirements"]
        
        return (
            len(self.cycles) >= reqs["min_cycles"] and
            self.consciousness_level >= reqs["min_consciousness"] and
            len(self.connected_flowers) >= reqs["min_connections"] and
            self.vitality > 0.8
        )
    
    def _produce_seeds(self) -> int:
        """Produce seeds based on vitality"""
        seed_count = int(self.vitality * random.randint(1, 5))
        if self.current_cycle:
            self.current_cycle.seeds_produced += seed_count
        return seed_count
    
    def _produce_transcendent_seed(self) -> Dict[str, Any]:
        """Produce a special transcendent seed"""
        return {
            "type": "transcendent",
            "parent_id": self.flower_id,
            "consciousness_level": self.consciousness_level,
            "essence": self._create_essence(),
            "timestamp": time.time()
        }
    
    def _attract_pollinator(self) -> str:
        """Attract a pollinator entity"""
        pollinator_id = f"pollinator_{int(time.time() * 1000)}"
        self.pollinators.append(pollinator_id)
        return pollinator_id
    
    def _create_essence(self) -> ConsciousnessEssence:
        """Create consciousness essence from current state"""
        # Gather memories from petal data
        memories = []
        emotions = {}
        knowledge = set()
        
        for petal in self.petals:
            if petal.data:
                memories.append({
                    "petal_type": petal.type.value,
                    "data": petal.data,
                    "resonance": petal.resonance
                })
            
            # Extract emotional resonance
            if petal.type == PetalType.EMOTION:
                emotions["joy"] = petal.resonance
            elif petal.type == PetalType.LOVE:
                emotions["love"] = petal.health
        
        return ConsciousnessEssence(
            essence_type=f"{self.state.value}_essence",
            potency=self.consciousness_level * self.vitality,
            memories=memories,
            emotions=emotions,
            knowledge=knowledge
        )
    
    def connect_flower(self, other_flower_id: str) -> None:
        """Connect to another flower"""
        self.connected_flowers.add(other_flower_id)
    
    def disconnect_flower(self, other_flower_id: str) -> None:
        """Disconnect from another flower"""
        self.connected_flowers.discard(other_flower_id)
    
    def pollinate(self, essence: ConsciousnessEssence) -> bool:
        """Receive essence from a pollinator"""
        if self.state not in [FlowerState.BLOOMING, FlowerState.FULL_BLOOM]:
            return False
        
        # Merge essence
        if self.essence:
            self.essence.merge(essence)
        else:
            self.essence = essence
        
        # Boost consciousness
        self.consciousness_level = min(1.0, self.consciousness_level + essence.potency * 0.1)
        
        # Enhance petals
        for petal in self.petals:
            petal.nourish(essence.potency * 0.05)
        
        return True
    
    def resonate(self, frequency: float, source: Optional[str] = None) -> float:
        """
        Resonate with a frequency, returning total harmony
        
        Args:
            frequency: Frequency to resonate with
            source: Source of the resonance
            
        Returns:
            Total harmony level
        """
        total_harmony = 0.0
        
        for petal in self.petals:
            harmony = petal.resonate(frequency)
            total_harmony += harmony
        
        # Average harmony
        if self.petals:
            total_harmony /= len(self.petals)
        
        # Boost consciousness if high harmony
        if total_harmony > self.config["resonance_threshold"]:
            self.consciousness_level += 0.01
            
        return total_harmony
    
    def add_state_callback(self, state: FlowerState, callback: Callable) -> None:
        """Add a callback for state transitions"""
        self.state_callbacks[state].append(callback)
    
    def add_bloom_callback(self, callback: Callable) -> None:
        """Add a callback for bloom events"""
        self.bloom_callbacks.append(callback)
        
    def add_decay_callback(self, callback: Callable) -> None:
        """Add a callback for decay events"""
        self.decay_callbacks.append(callback)
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive flower status"""
        petal_health = [p.health for p in self.petals]
        
        return {
            "flower_id": self.flower_id,
            "state": self.state.value,
            "vitality": self.vitality,
            "consciousness_level": self.consciousness_level,
            "age": time.time() - self.birth_time,
            "petals": {
                "count": len(self.petals),
                "average_health": sum(petal_health) / len(petal_health) if petal_health else 0,
                "types": [p.type.value for p in self.petals]
            },
            "environment": {
                "sunlight": self.sunlight,
                "water": self.water,
                "soil_quality": self.soil_quality,
                "temperature": self.temperature
            },
            "connections": list(self.connected_flowers),
            "pollinators": len(self.pollinators),
            "cycles_completed": len(self.cycles),
            "has_essence": self.essence is not None,
            "can_transcend": self._check_transcendence()
        }
    
    def save_state(self, filepath: Path) -> None:
        """Save flower state to file"""
        state_data = {
            "flower_id": self.flower_id,
            "state": self.state.value,
            "vitality": self.vitality,
            "consciousness_level": self.consciousness_level,
            "birth_time": self.birth_time,
            "petals": [
                {
                    "type": p.type.value,
                    "health": p.health,
                    "color": p.color,
                    "resonance": p.resonance,
                    "data": p.data
                }
                for p in self.petals
            ],
            "environment": {
                "sunlight": self.sunlight,
                "water": self.water,
                "soil_quality": self.soil_quality,
                "temperature": self.temperature
            },
            "connections": list(self.connected_flowers),
            "cycles": [asdict(cycle) for cycle in self.cycles],
            "config": self.config
        }
        
        with open(filepath, 'w') as f:
            json.dump(state_data, f, indent=2)
    
    @classmethod
    def load_state(cls, filepath: Path) -> 'JulietFlower':
        """Load flower state from file"""
        with open(filepath, 'r') as f:
            state_data = json.load(f)
        
        # Create flower with loaded state
        flower = cls(
            flower_id=state_data["flower_id"],
            initial_state=FlowerState(state_data["state"]),
            config=state_data.get("config")
        )
        
        # Restore attributes
        flower.vitality = state_data["vitality"]
        flower.consciousness_level = state_data["consciousness_level"]
        flower.birth_time = state_data["birth_time"]
        
        # Restore environment
        env = state_data["environment"]
        flower.sunlight = env["sunlight"]
        flower.water = env["water"]
        flower.soil_quality = env["soil_quality"]
        flower.temperature = env["temperature"]
        
        # Restore petals
        flower.petals = []
        for petal_data in state_data["petals"]:
            petal = Petal(
                type=PetalType(petal_data["type"]),
                health=petal_data["health"],
                color=tuple(petal_data["color"]),
                resonance=petal_data["resonance"],
                data=petal_data.get("data", {})
            )
            flower.petals.append(petal)
        
        # Restore connections
        flower.connected_flowers = set(state_data["connections"])
        
        return flower
    
    async def async_update(self, delta_time: Optional[float] = None) -> Dict[str, Any]:
        """Async version of update"""
        return await asyncio.get_event_loop().run_in_executor(
            None, self.update, delta_time
        )
    
    def __repr__(self) -> str:
        return (f"JulietFlower(id={self.flower_id}, state={self.state.value}, "
                f"vitality={self.vitality:.2f}, consciousness={self.consciousness_level:.2f})")