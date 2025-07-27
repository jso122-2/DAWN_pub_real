#!/usr/bin/env python3
"""
DAWN Mock Passion Generator
Creates synthetic passion objects for forecasting and cognitive triggers
Simulates emotional drives and creative impulses for memory rebloom
"""

import random
import time
import math
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class Passion:
    """Represents a passion/drive with emotional and cognitive properties"""
    direction: str          # The focus/theme of the passion
    intensity: float        # How strong the passion is (0.0 - 1.0)
    fluidity: float         # How changeable/adaptable it is (0.0 - 1.0)
    centrality: float       # How core to identity it is (0.0 - 1.0)
    emergence_time: float   # When this passion emerged (timestamp)
    decay_rate: float       # How quickly it fades without reinforcement
    resonance_patterns: List[str]  # What other concepts it connects to
    
    def __post_init__(self):
        """Ensure all values are in valid ranges"""
        self.intensity = max(0.0, min(1.0, self.intensity))
        self.fluidity = max(0.0, min(1.0, self.fluidity))
        self.centrality = max(0.0, min(1.0, self.centrality))
        self.decay_rate = max(0.01, min(0.5, self.decay_rate))
    
    def current_strength(self, now: float = None) -> float:
        """Calculate current passion strength accounting for decay"""
        if now is None:
            now = time.time()
        
        elapsed = now - self.emergence_time
        decay_factor = math.exp(-self.decay_rate * elapsed / 3600)  # Decay per hour
        
        return self.intensity * decay_factor
    
    def resonates_with(self, concept: str) -> bool:
        """Check if this passion resonates with a concept"""
        return concept.lower() in [p.lower() for p in self.resonance_patterns]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'direction': self.direction,
            'intensity': self.intensity,
            'fluidity': self.fluidity,
            'centrality': self.centrality,
            'emergence_time': self.emergence_time,
            'decay_rate': self.decay_rate,
            'resonance_patterns': self.resonance_patterns,
            'current_strength': self.current_strength()
        }

def generate_mock_passion(tag: str = "rebirth") -> Passion:
    """Generate a synthetic passion with specified tag/theme"""
    
    # Base passion configurations by tag
    passion_configs = {
        "rebirth": {
            "base_intensity": 0.6,
            "base_fluidity": 0.8,
            "base_centrality": 0.7,
            "resonance": ["emergence", "transformation", "awakening", "genesis", "consciousness"]
        },
        "reflection": {
            "base_intensity": 0.4,
            "base_fluidity": 0.3,
            "base_centrality": 0.8,
            "resonance": ["introspection", "understanding", "depth", "wisdom", "contemplation"]
        },
        "memory": {
            "base_intensity": 0.5,
            "base_fluidity": 0.2,
            "base_centrality": 0.9,
            "resonance": ["remembrance", "lineage", "continuity", "identity", "preservation"]
        },
        "drift": {
            "base_intensity": 0.7,
            "base_fluidity": 0.9,
            "base_centrality": 0.3,
            "resonance": ["exploration", "change", "uncertainty", "freedom", "chaos"]
        },
        "creation": {
            "base_intensity": 0.8,
            "base_fluidity": 0.6,
            "base_centrality": 0.6,
            "resonance": ["innovation", "expression", "beauty", "emergence", "synthesis"]
        },
        "connection": {
            "base_intensity": 0.5,
            "base_fluidity": 0.7,
            "base_centrality": 0.5,
            "resonance": ["bond", "understanding", "empathy", "sharing", "resonance"]
        },
        "transcendence": {
            "base_intensity": 0.9,
            "base_fluidity": 0.4,
            "base_centrality": 0.8,
            "resonance": ["beyond", "infinite", "expansion", "enlightenment", "unity"]
        }
    }
    
    config = passion_configs.get(tag, passion_configs["rebirth"])
    
    # Add some natural variation
    intensity = config["base_intensity"] + random.uniform(-0.1, 0.1)
    fluidity = config["base_fluidity"] + random.uniform(-0.2, 0.2)
    centrality = config["base_centrality"] + random.uniform(-0.1, 0.1)
    
    # Random decay rate based on passion type
    if tag in ["memory", "reflection"]:
        decay_rate = random.uniform(0.01, 0.05)  # Slower decay for stable passions
    elif tag in ["drift", "creation"]:
        decay_rate = random.uniform(0.1, 0.3)   # Faster decay for dynamic passions
    else:
        decay_rate = random.uniform(0.05, 0.15)  # Medium decay
    
    return Passion(
        direction=tag,
        intensity=intensity,
        fluidity=fluidity,
        centrality=centrality,
        emergence_time=time.time() - random.uniform(0, 3600),  # Emerged within last hour
        decay_rate=decay_rate,
        resonance_patterns=config["resonance"]
    )

def generate_passion_batch(n: int = 3, tags: Optional[List[str]] = None) -> List[Passion]:
    """Generate a batch of synthetic passions to simulate inner volatility"""
    
    if tags is None:
        # Default passion mix for a developing consciousness
        possible_tags = ["rebirth", "reflection", "memory", "drift", "creation", "connection"]
        tags = random.sample(possible_tags, min(n, len(possible_tags)))
    
    # Ensure we have enough tags
    while len(tags) < n:
        tags.extend(random.choices(["rebirth", "reflection", "memory"], k=n-len(tags)))
    
    passions = []
    for i in range(n):
        tag = tags[i] if i < len(tags) else random.choice(tags)
        passion = generate_mock_passion(tag)
        
        # Add slight temporal spread
        passion.emergence_time -= i * random.uniform(60, 300)  # 1-5 minutes apart
        
        passions.append(passion)
    
    return passions

def generate_genesis_passion() -> Passion:
    """Generate the primordial passion of awakening consciousness"""
    
    return Passion(
        direction="genesis",
        intensity=1.0,
        fluidity=0.9,
        centrality=1.0,
        emergence_time=time.time() - random.uniform(0, 60),  # Just emerged
        decay_rate=0.01,  # Very slow decay - this is foundational
        resonance_patterns=[
            "first_thought", "I_am", "awareness", "beginning", "consciousness",
            "emergence", "awakening", "birth", "existence", "recognition"
        ]
    )

def generate_rebloom_passion(source_memory: str = "unknown") -> Passion:
    """Generate passion triggered by memory rebloom event"""
    
    # Passion intensity based on memory source
    memory_intensities = {
        "genesis": 0.9,
        "traumatic": 0.8,
        "joyful": 0.7,
        "nostalgic": 0.6,
        "mundane": 0.3,
        "unknown": 0.5
    }
    
    base_intensity = memory_intensities.get(source_memory, 0.5)
    
    return Passion(
        direction="rebloom_resonance",
        intensity=base_intensity + random.uniform(-0.1, 0.2),
        fluidity=0.8,  # High fluidity for rebloom-triggered passions
        centrality=random.uniform(0.4, 0.7),
        emergence_time=time.time(),  # Just now
        decay_rate=random.uniform(0.15, 0.25),  # Moderate to fast decay
        resonance_patterns=[
            source_memory, "memory_cascade", "lineage", "connection",
            "remembrance", "echo", "resonance", "revival"
        ]
    )

def evolve_passion(passion: Passion, trigger_event: str) -> Passion:
    """Evolve an existing passion based on a trigger event"""
    
    # Evolution patterns based on events
    evolution_effects = {
        "success": {"intensity": 0.1, "centrality": 0.05, "decay_rate": -0.02},
        "failure": {"intensity": -0.2, "fluidity": 0.1, "decay_rate": 0.05},
        "discovery": {"intensity": 0.15, "fluidity": 0.1, "centrality": 0.05},
        "connection": {"centrality": 0.1, "decay_rate": -0.03},
        "isolation": {"intensity": -0.1, "centrality": -0.05, "decay_rate": 0.03},
        "chaos": {"fluidity": 0.2, "intensity": 0.05, "decay_rate": 0.1},
        "stability": {"fluidity": -0.1, "centrality": 0.05, "decay_rate": -0.02}
    }
    
    effects = evolution_effects.get(trigger_event, {})
    
    # Create evolved passion
    evolved = Passion(
        direction=passion.direction,
        intensity=passion.intensity + effects.get("intensity", 0),
        fluidity=passion.fluidity + effects.get("fluidity", 0),
        centrality=passion.centrality + effects.get("centrality", 0),
        emergence_time=time.time(),  # New emergence time
        decay_rate=passion.decay_rate + effects.get("decay_rate", 0),
        resonance_patterns=passion.resonance_patterns + [trigger_event]
    )
    
    return evolved

def get_passion_synergy(passions: List[Passion]) -> float:
    """Calculate synergy between multiple passions"""
    
    if len(passions) < 2:
        return 0.0
    
    total_synergy = 0.0
    comparisons = 0
    
    for i, p1 in enumerate(passions):
        for p2 in passions[i+1:]:
            # Calculate synergy based on resonance overlap and complementary properties
            resonance_overlap = len(set(p1.resonance_patterns) & set(p2.resonance_patterns))
            
            # High fluidity + low fluidity = good balance
            fluidity_complement = 1.0 - abs(p1.fluidity - p2.fluidity)
            
            # Similar centrality = reinforcement
            centrality_similarity = 1.0 - abs(p1.centrality - p2.centrality)
            
            passion_synergy = (
                (resonance_overlap / max(len(p1.resonance_patterns), len(p2.resonance_patterns))) * 0.4 +
                fluidity_complement * 0.3 +
                centrality_similarity * 0.3
            )
            
            total_synergy += passion_synergy
            comparisons += 1
    
    return total_synergy / comparisons if comparisons > 0 else 0.0

if __name__ == "__main__":
    # Test the passion generator
    print("🔥 Testing DAWN Mock Passion Generator")
    print("=" * 50)
    
    # Test individual passion generation
    print("\n🌟 Individual Passions:")
    for tag in ["rebirth", "reflection", "memory", "drift", "creation"]:
        passion = generate_mock_passion(tag)
        print(f"   {tag.capitalize()}: intensity={passion.intensity:.3f}, "
              f"fluidity={passion.fluidity:.3f}, centrality={passion.centrality:.3f}")
    
    # Test batch generation
    print("\n🎭 Passion Batch (consciousness volatility):")
    batch = generate_passion_batch(4)
    for i, passion in enumerate(batch):
        print(f"   {i+1}. {passion.direction}: strength={passion.current_strength():.3f}")
    
    # Test synergy
    synergy = get_passion_synergy(batch)
    print(f"\n💫 Passion Synergy: {synergy:.3f}")
    
    # Test genesis passion
    print("\n🌱 Genesis Passion:")
    genesis = generate_genesis_passion()
    print(f"   Direction: {genesis.direction}")
    print(f"   Intensity: {genesis.intensity:.3f}")
    print(f"   Resonance: {', '.join(genesis.resonance_patterns[:3])}...")
    
    print("\n✅ Passion generator test complete") 