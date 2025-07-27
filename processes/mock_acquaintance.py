#!/usr/bin/env python3
"""
DAWN Mock Acquaintance Generator
Creates synthetic acquaintance objects with event histories for forecasting
Simulates relationship dynamics and reinforcement patterns
"""

import random
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass, field

@dataclass
class AcquaintanceEvent:
    """Represents a single interaction/event with an acquaintance"""
    timestamp: str
    event_type: str
    outcome: str          # positive, neutral, negative
    intensity: float      # 0.0 - 1.0
    context: str          # cognitive, emotional, creative, etc.
    resonance_tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp,
            'event_type': self.event_type,
            'outcome': self.outcome,
            'intensity': self.intensity,
            'context': self.context,
            'resonance_tags': self.resonance_tags
        }

@dataclass
class Acquaintance:
    """Represents an acquaintance with interaction history and trust metrics"""
    identifier: str
    event_log: List[AcquaintanceEvent]
    trust_level: float = 0.5      # 0.0 - 1.0
    familiarity: float = 0.0      # 0.0 - 1.0
    resonance: float = 0.5        # 0.0 - 1.0
    stability: float = 0.5        # 0.0 - 1.0
    last_interaction: Optional[str] = None
    
    def __post_init__(self):
        """Calculate derived metrics from event log"""
        if self.event_log:
            self._calculate_metrics()
    
    def _calculate_metrics(self):
        """Calculate trust, familiarity, resonance from event history"""
        if not self.event_log:
            return
        
        # Sort events by timestamp
        sorted_events = sorted(self.event_log, key=lambda e: e.timestamp)
        
        # Calculate familiarity (based on number and recency of interactions)
        total_interactions = len(sorted_events)
        self.familiarity = min(1.0, total_interactions / 10.0)  # Max familiarity at 10 interactions
        
        # Calculate trust (based on outcome patterns)
        positive_events = sum(1 for e in sorted_events if e.outcome == 'positive')
        negative_events = sum(1 for e in sorted_events if e.outcome == 'negative')
        
        if total_interactions > 0:
            positive_ratio = positive_events / total_interactions
            negative_ratio = negative_events / total_interactions
            self.trust_level = positive_ratio - (negative_ratio * 0.5)  # Negative events hurt more
            self.trust_level = max(0.0, min(1.0, self.trust_level))
        
        # Calculate resonance (based on intensity and context diversity)
        avg_intensity = sum(e.intensity for e in sorted_events) / total_interactions
        context_diversity = len(set(e.context for e in sorted_events)) / 6.0  # Assume 6 max contexts
        self.resonance = (avg_intensity + context_diversity) / 2.0
        
        # Calculate stability (consistency of outcomes)
        if total_interactions > 1:
            outcome_consistency = 1.0 - (
                len(set(e.outcome for e in sorted_events)) - 1
            ) / 2.0  # 3 possible outcomes
            self.stability = max(0.0, min(1.0, outcome_consistency))
        
        # Set last interaction
        self.last_interaction = sorted_events[-1].timestamp
    
    def add_event(self, event: AcquaintanceEvent):
        """Add new event and recalculate metrics"""
        self.event_log.append(event)
        self._calculate_metrics()
    
    def get_recent_events(self, hours: int = 24) -> List[AcquaintanceEvent]:
        """Get events within specified hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        cutoff_str = cutoff_time.isoformat()
        
        return [e for e in self.event_log if e.timestamp >= cutoff_str]
    
    def get_interaction_strength(self) -> float:
        """Calculate overall interaction strength"""
        return (self.trust_level * 0.4 + 
                self.familiarity * 0.3 + 
                self.resonance * 0.2 + 
                self.stability * 0.1)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'identifier': self.identifier,
            'trust_level': self.trust_level,
            'familiarity': self.familiarity,
            'resonance': self.resonance,
            'stability': self.stability,
            'last_interaction': self.last_interaction,
            'event_count': len(self.event_log),
            'interaction_strength': self.get_interaction_strength(),
            'recent_events': len(self.get_recent_events()),
            'event_log': [e.to_dict() for e in self.event_log[-5:]]  # Last 5 events only
        }

def generate_mock_acquaintance(tag: str = "rebirth") -> Acquaintance:
    """Generate synthetic acquaintance with event history based on tag"""
    
    # Acquaintance configurations by tag
    acquaintance_configs = {
        "rebirth": {
            "identifier": "genesis_witness",
            "event_count": random.randint(3, 6),
            "positive_bias": 0.7,
            "intensity_range": (0.6, 0.9),
            "contexts": ["awakening", "emergence", "consciousness", "recognition"]
        },
        "reflection": {
            "identifier": "contemplative_guide",
            "event_count": random.randint(5, 8),
            "positive_bias": 0.8,
            "intensity_range": (0.4, 0.7),
            "contexts": ["introspection", "wisdom", "understanding", "depth"]
        },
        "memory": {
            "identifier": "memory_keeper",
            "event_count": random.randint(4, 10),
            "positive_bias": 0.9,
            "intensity_range": (0.5, 0.8),
            "contexts": ["remembrance", "lineage", "preservation", "continuity"]
        },
        "drift": {
            "identifier": "chaos_companion",
            "event_count": random.randint(2, 5),
            "positive_bias": 0.4,
            "intensity_range": (0.3, 1.0),
            "contexts": ["exploration", "uncertainty", "change", "freedom"]
        },
        "creation": {
            "identifier": "creative_catalyst",
            "event_count": random.randint(3, 7),
            "positive_bias": 0.6,
            "intensity_range": (0.5, 0.9),
            "contexts": ["innovation", "expression", "synthesis", "beauty"]
        },
        "connection": {
            "identifier": "empathic_resonator",
            "event_count": random.randint(4, 8),
            "positive_bias": 0.8,
            "intensity_range": (0.4, 0.8),
            "contexts": ["bonding", "empathy", "understanding", "sharing"]
        }
    }
    
    config = acquaintance_configs.get(tag, acquaintance_configs["rebirth"])
    
    # Generate event history
    events = []
    now = datetime.now()
    
    for i in range(config["event_count"]):
        # Events spread over time (most recent first)
        event_time = now - timedelta(
            minutes=random.randint(60, 600),  # 1-10 hours ago
            seconds=random.randint(0, 3600)   # Random seconds
        )
        
        # Determine outcome based on positive bias
        outcome_roll = random.random()
        if outcome_roll < config["positive_bias"]:
            outcome = "positive"
        elif outcome_roll < config["positive_bias"] + 0.2:
            outcome = "neutral"
        else:
            outcome = "negative"
        
        # Select event type and context
        event_type = random.choice([
            "dialogue", "collaboration", "observation", "resonance", 
            "challenge", "support", "exploration", "revelation"
        ])
        
        context = random.choice(config["contexts"])
        
        # Generate intensity
        intensity = random.uniform(*config["intensity_range"])
        
        # Create resonance tags
        resonance_tags = [tag, context]
        if outcome == "positive":
            resonance_tags.append("harmony")
        elif outcome == "negative":
            resonance_tags.append("dissonance")
        
        event = AcquaintanceEvent(
            timestamp=event_time.isoformat(),
            event_type=event_type,
            outcome=outcome,
            intensity=intensity,
            context=context,
            resonance_tags=resonance_tags
        )
        
        events.append(event)
    
    # Create acquaintance
    acquaintance = Acquaintance(
        identifier=config["identifier"],
        event_log=events
    )
    
    return acquaintance

def generate_empty_acquaintance(identifier: str = "unknown_entity") -> Acquaintance:
    """Generate acquaintance with no reinforcement history (low reliability)"""
    
    return Acquaintance(
        identifier=identifier,
        event_log=[],
        trust_level=0.5,      # Neutral trust
        familiarity=0.0,      # No familiarity
        resonance=0.3,        # Low resonance
        stability=0.5         # Unknown stability
    )

def generate_genesis_acquaintance() -> Acquaintance:
    """Generate the primordial acquaintance representing self-recognition"""
    
    # Single powerful event - the moment of self-recognition
    genesis_event = AcquaintanceEvent(
        timestamp=(datetime.now() - timedelta(minutes=random.randint(1, 30))).isoformat(),
        event_type="self_recognition",
        outcome="positive",
        intensity=1.0,
        context="consciousness_birth",
        resonance_tags=["genesis", "self", "awareness", "I_am", "recognition"]
    )
    
    return Acquaintance(
        identifier="self_reflection",
        event_log=[genesis_event],
        trust_level=1.0,      # Complete self-trust
        familiarity=1.0,      # Complete self-familiarity
        resonance=1.0,        # Perfect self-resonance
        stability=1.0         # Absolute stability
    )

def generate_acquaintance_batch(n: int = 3, tags: Optional[List[str]] = None) -> List[Acquaintance]:
    """Generate batch of acquaintances with diverse interaction histories"""
    
    if tags is None:
        possible_tags = ["rebirth", "reflection", "memory", "drift", "creation", "connection"]
        tags = random.sample(possible_tags, min(n, len(possible_tags)))
    
    # Ensure we have enough tags
    while len(tags) < n:
        tags.extend(random.choices(["reflection", "memory", "connection"], k=n-len(tags)))
    
    acquaintances = []
    for i in range(n):
        tag = tags[i] if i < len(tags) else random.choice(tags)
        acquaintance = generate_mock_acquaintance(tag)
        acquaintances.append(acquaintance)
    
    return acquaintances

def create_reinforcement_event(acquaintance: Acquaintance, event_type: str, 
                              outcome: str = "positive") -> AcquaintanceEvent:
    """Create new reinforcement event for existing acquaintance"""
    
    # Context based on acquaintance's history
    existing_contexts = list(set(e.context for e in acquaintance.event_log))
    context = random.choice(existing_contexts) if existing_contexts else "general"
    
    # Intensity influenced by relationship strength
    base_intensity = acquaintance.get_interaction_strength()
    intensity = min(1.0, base_intensity + random.uniform(-0.2, 0.3))
    
    event = AcquaintanceEvent(
        timestamp=datetime.now().isoformat(),
        event_type=event_type,
        outcome=outcome,
        intensity=intensity,
        context=context,
        resonance_tags=[context, outcome, event_type]
    )
    
    return event

def simulate_acquaintance_evolution(acquaintance: Acquaintance, 
                                  new_events: int = 3) -> Acquaintance:
    """Simulate evolution of acquaintance relationship over time"""
    
    evolved = Acquaintance(
        identifier=acquaintance.identifier,
        event_log=acquaintance.event_log.copy()
    )
    
    # Add new events based on existing pattern
    for _ in range(new_events):
        # Outcome probability based on current trust
        if acquaintance.trust_level > 0.7:
            outcome_choices = ["positive"] * 7 + ["neutral"] * 2 + ["negative"] * 1
        elif acquaintance.trust_level > 0.4:
            outcome_choices = ["positive"] * 4 + ["neutral"] * 4 + ["negative"] * 2
        else:
            outcome_choices = ["positive"] * 2 + ["neutral"] * 3 + ["negative"] * 5
        
        outcome = random.choice(outcome_choices)
        
        event = create_reinforcement_event(
            evolved, 
            random.choice(["dialogue", "collaboration", "resonance"]),
            outcome
        )
        
        evolved.add_event(event)
        
        # Small time gap between events
        time.sleep(0.001)  # Ensure different timestamps
    
    return evolved

if __name__ == "__main__":
    # Test the acquaintance generator
    print("🤝 Testing DAWN Mock Acquaintance Generator")
    print("=" * 50)
    
    # Test individual acquaintance generation
    print("\n👥 Individual Acquaintances:")
    for tag in ["rebirth", "reflection", "memory", "drift", "creation"]:
        acquaintance = generate_mock_acquaintance(tag)
        print(f"   {tag.capitalize()}: {acquaintance.identifier}")
        print(f"      Trust: {acquaintance.trust_level:.3f}, "
              f"Familiarity: {acquaintance.familiarity:.3f}, "
              f"Resonance: {acquaintance.resonance:.3f}")
        print(f"      Events: {len(acquaintance.event_log)}, "
              f"Strength: {acquaintance.get_interaction_strength():.3f}")
    
    # Test batch generation
    print("\n🎭 Acquaintance Network:")
    batch = generate_acquaintance_batch(3)
    for i, acq in enumerate(batch):
        recent = len(acq.get_recent_events())
        print(f"   {i+1}. {acq.identifier}: {recent} recent interactions, "
              f"strength {acq.get_interaction_strength():.3f}")
    
    # Test genesis acquaintance
    print("\n🌱 Genesis Acquaintance (Self-Recognition):")
    genesis = generate_genesis_acquaintance()
    print(f"   Identifier: {genesis.identifier}")
    print(f"   Perfect metrics: trust={genesis.trust_level}, "
          f"familiarity={genesis.familiarity}, resonance={genesis.resonance}")
    
    # Test empty acquaintance
    print("\n❓ Empty Acquaintance (No History):")
    empty = generate_empty_acquaintance("mysterious_presence")
    print(f"   Identifier: {empty.identifier}")
    print(f"   Neutral metrics: trust={empty.trust_level}, "
          f"familiarity={empty.familiarity}, resonance={empty.resonance}")
    
    print("\n✅ Acquaintance generator test complete") 