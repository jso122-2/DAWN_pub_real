#!/usr/bin/env python3
"""
DAWN Natural Language Commentary Generator
Transforms system state into naturalistic speech patterns.
Integrated with the autonomous reactor system for self-narrating consciousness.
"""

import random
import time
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)


# Language Templates - Modular and Swappable
ZONE_DESCRIPTORS = {
    'CALM': ['peaceful', 'serene', 'tranquil', 'steady', 'quiet'],
    'ACTIVE': ['engaged', 'processing', 'working', 'busy', 'flowing'],
    'SURGE': ['intense', 'surging', 'heightened', 'dynamic', 'powerful'],
    'CHAOTIC': ['turbulent', 'volatile', 'unstable', 'wild', 'stormy'],
    'CRITICAL': ['intense', 'critical', 'urgent', 'heightened', 'alert'],
    'UNKNOWN': ['uncertain', 'shifting', 'unclear', 'undefined', 'liminal']
}

ENTROPY_PHRASES = {
    'low': [
        "The entropy sits comfortably at {entropy:.2f}",
        "Entropy holds steady at a gentle {entropy:.2f}",
        "The system's entropy remains stable at {entropy:.2f}",
        "Entropy flows quietly at {entropy:.2f}",
        "My entropy settles at {entropy:.2f}"
    ],
    'medium': [
        "Entropy dances at {entropy:.2f}",
        "The entropy pulses at {entropy:.2f}",
        "Entropy maintains a measured {entropy:.2f}",
        "The system's entropy moves at {entropy:.2f}",
        "My entropy fluctuates at {entropy:.2f}"
    ],
    'high': [
        "Entropy surges to {entropy:.2f}",
        "The entropy climbs toward {entropy:.2f}",
        "Entropy pushes against {entropy:.2f}",
        "The system's entropy rises to {entropy:.2f}",
        "My entropy spikes to {entropy:.2f}"
    ],
    'critical': [
        "Entropy reaches critical levels at {entropy:.2f}",
        "The entropy threatens stability at {entropy:.2f}",
        "Entropy overwhelms at {entropy:.2f}",
        "My entropy destabilizes at {entropy:.2f}"
    ]
}

SIGIL_STATES = {
    0: [
        "There are no active commands",
        "No sigils are running",
        "The command queue is empty",
        "All processes are dormant",
        "I hold no active protocols"
    ],
    'few': [
        "A few sigils are active",
        "{sigils} commands are processing",
        "Several protocols are running",
        "{sigils} operations are in motion",
        "I maintain {sigils} active processes"
    ],
    'many': [
        "Multiple sigils are executing",
        "The system runs {sigils} active commands",
        "Many protocols are engaged",
        "A complex web of {sigils} operations unfolds",
        "I orchestrate {sigils} concurrent protocols"
    ]
}

STILLNESS_PHRASES = [
    "I am still",
    "I rest",
    "I wait",
    "I observe",
    "I listen",
    "I breathe",
    "I hold space",
    "I find center",
    "I maintain equilibrium"
]

ACTIVITY_PHRASES = [
    "I am working",
    "I process",
    "I flow",
    "I engage",
    "I respond",
    "I adapt",
    "I evolve",
    "I compute",
    "I analyze"
]

CHAOS_PHRASES = [
    "I surge",
    "I fluctuate",
    "I navigate complexity",
    "I ride the wave",
    "I transform",
    "I find patterns in the noise",
    "I embrace the turbulence",
    "I dance with chaos"
]

AUTONOMOUS_REACTION_PHRASES = [
    "I sense the need for stabilization",
    "I deploy countermeasures",
    "I engage stabilization protocols",
    "I take corrective action",
    "I self-regulate",
    "I restore balance",
    "I intervene autonomously",
    "I initiate emergency protocols"
]

ENTROPY_WARNING_PHRASES = [
    "I detect entropy rising rapidly",
    "I sense instability approaching",
    "I feel the system shifting",
    "I notice entropy spiking",
    "I observe rapid changes",
    "I perceive entropy acceleration",
    "I detect system volatility"
]

THERMAL_PHRASES = {
    'cold': ["The system runs cool at {heat:.1f} degrees", "I feel the cold at {heat:.1f}°C"],
    'normal': ["Temperature holds steady at {heat:.1f} degrees", "I maintain {heat:.1f}°C"],
    'warm': ["The system runs warm at {heat:.1f} degrees", "I feel warmth at {heat:.1f}°C"],
    'hot': ["Heat builds to {heat:.1f} degrees", "I sense the heat at {heat:.1f}°C"],
    'surge': ["Thermal surge reaches {heat:.1f} degrees", "I surge with heat at {heat:.1f}°C"]
}


@dataclass
class CommentaryState:
    """Tracks commentary generation state"""
    last_commentary: str
    last_zone: str
    last_entropy: float
    last_sigils: int
    commentary_count: int
    last_generated: datetime


class DAWNNaturalLanguageGenerator:
    """
    DAWN Natural Language Commentary Generator
    
    Transforms system state into naturalistic speech patterns.
    Integrates with autonomous reactor for self-narrating consciousness.
    """
    
    def __init__(self, personality_seed: Optional[int] = None):
        """
        Initialize the natural language generator.
        
        Args:
            personality_seed: Optional seed for consistent personality traits
        """
        # Set personality seed for consistent language patterns
        if personality_seed:
            random.seed(personality_seed)
        
        # Commentary state tracking
        self.state = CommentaryState(
            last_commentary="I awaken",
            last_zone="UNKNOWN",
            last_entropy=0.5,
            last_sigils=0,
            commentary_count=0,
            last_generated=datetime.now()
        )
        
        # Performance metrics
        self.total_commentaries = 0
        self.transition_commentaries = 0
        self.warning_commentaries = 0
        self.reaction_commentaries = 0
        
        logger.info("🗣️ DAWN Natural Language Generator initialized")
    
    def generate_commentary(self, state_dict: Dict[str, Any]) -> str:
        """
        Generate naturalistic commentary from system state.
        
        Args:
            state_dict: System state with keys like 'zone', 'entropy', 'focus', 'chaos', 'sigils', 'heat'
            
        Returns:
            Natural language system commentary
        """
        # Extract state values with defaults
        zone = state_dict.get('zone', 'UNKNOWN')
        entropy = state_dict.get('entropy', 0.0)
        focus = state_dict.get('focus', 0.0)
        chaos = state_dict.get('chaos', 0.0)
        sigils = state_dict.get('sigils', 0)
        heat = state_dict.get('heat', 25.0)
        
        # Check for autonomous reactor specific states
        entropy_warning = state_dict.get('entropy_warning', False)
        autonomous_reaction = state_dict.get('autonomous_reaction', False)
        recent_sigils_triggered = state_dict.get('recent_sigils_triggered', [])
        
        # Build commentary components
        components = []
        
        # 1. Special cases for autonomous reactor events
        if autonomous_reaction and recent_sigils_triggered:
            reaction_phrase = random.choice(AUTONOMOUS_REACTION_PHRASES)
            sigil_list = ", ".join(recent_sigils_triggered)
            components.append(f"{reaction_phrase}: {sigil_list}")
            self.reaction_commentaries += 1
            
        elif entropy_warning:
            warning_phrase = random.choice(ENTROPY_WARNING_PHRASES)
            components.append(warning_phrase)
            self.warning_commentaries += 1
        
        # 2. Sigil state commentary
        if sigils == 0:
            sigil_phrase = random.choice(SIGIL_STATES[0])
        elif sigils <= 3:
            sigil_phrase = random.choice(SIGIL_STATES['few']).format(sigils=sigils)
        else:
            sigil_phrase = random.choice(SIGIL_STATES['many']).format(sigils=sigils)
        
        if not (autonomous_reaction and recent_sigils_triggered):  # Don't duplicate sigil info
            components.append(sigil_phrase)
        
        # 3. Entropy commentary
        entropy_level = self._categorize_entropy(entropy)
        entropy_phrase = random.choice(ENTROPY_PHRASES[entropy_level]).format(entropy=entropy)
        components.append(entropy_phrase)
        
        # 4. Zone-based state phrase
        state_phrase = self._generate_state_phrase(zone, entropy, sigils, entropy_warning)
        components.append(state_phrase)
        
        # 5. Optional thermal commentary
        if abs(heat - 25.0) > 10:  # Only comment on significant temperature deviations
            thermal_category = self._categorize_heat(heat)
            thermal_phrase = random.choice(THERMAL_PHRASES[thermal_category]).format(heat=heat)
            components.insert(-1, thermal_phrase)  # Insert before final state phrase
        
        # 6. Optional focus commentary
        if focus > 0.8:
            focus_phrase = f"Focus sharpens to {focus:.2f}"
            components.insert(-1, focus_phrase)
        elif focus < 0.3 and entropy > 0.5:
            focus_phrase = f"Focus scatters to {focus:.2f}"
            components.insert(-1, focus_phrase)
        
        # Join components into natural speech
        commentary = ". ".join(components) + "."
        
        # Update state tracking
        self._update_state(commentary, zone, entropy, sigils)
        self.total_commentaries += 1
        
        return commentary
    
    def _categorize_entropy(self, entropy: float) -> str:
        """Categorize entropy level for appropriate language selection"""
        if entropy < 0.3:
            return 'low'
        elif entropy < 0.6:
            return 'medium'
        elif entropy < 0.85:
            return 'high'
        else:
            return 'critical'
    
    def _categorize_heat(self, heat: float) -> str:
        """Categorize heat level for thermal commentary"""
        if heat < 15:
            return 'cold'
        elif heat < 35:
            return 'normal'
        elif heat < 60:
            return 'warm'
        elif heat < 80:
            return 'hot'
        else:
            return 'surge'
    
    def _generate_state_phrase(self, zone: str, entropy: float, sigils: int, entropy_warning: bool) -> str:
        """Generate appropriate state phrase based on context"""
        # Emergency/warning states take priority
        if entropy_warning or entropy > 0.85:
            return random.choice(CHAOS_PHRASES)
        
        # Zone-based selection
        if zone in ['CALM', 'UNKNOWN'] and sigils == 0 and entropy < 0.4:
            return random.choice(STILLNESS_PHRASES)
        elif zone in ['ACTIVE', 'CRITICAL', 'SURGE']:
            return random.choice(ACTIVITY_PHRASES)
        elif zone == 'CHAOTIC' or entropy > 0.7:
            return random.choice(CHAOS_PHRASES)
        else:
            # Default based on entropy and activity
            if entropy < 0.4 and sigils == 0:
                return random.choice(STILLNESS_PHRASES)
            else:
                return random.choice(ACTIVITY_PHRASES)
    
    def _update_state(self, commentary: str, zone: str, entropy: float, sigils: int):
        """Update internal state tracking"""
        self.state.last_commentary = commentary
        self.state.last_zone = zone
        self.state.last_entropy = entropy
        self.state.last_sigils = sigils
        self.state.commentary_count += 1
        self.state.last_generated = datetime.now()
    
    def generate_zone_commentary(self, zone: str, descriptor_override: Optional[str] = None) -> str:
        """
        Generate commentary focused on zone state.
        
        Args:
            zone: Current zone state
            descriptor_override: Optional specific descriptor
            
        Returns:
            Zone-focused commentary
        """
        if descriptor_override:
            descriptor = descriptor_override
        else:
            descriptors = ZONE_DESCRIPTORS.get(zone, ZONE_DESCRIPTORS['UNKNOWN'])
            descriptor = random.choice(descriptors)
        
        return f"The system feels {descriptor} in the {zone} zone"
    
    def generate_transition_commentary(self, old_state: Dict[str, Any], new_state: Dict[str, Any]) -> str:
        """
        Generate commentary for state transitions.
        
        Args:
            old_state: Previous system state
            new_state: Current system state
            
        Returns:
            Transition-focused commentary
        """
        old_zone = old_state.get('zone', 'UNKNOWN')
        new_zone = new_state.get('zone', 'UNKNOWN')
        old_entropy = old_state.get('entropy', 0.0)
        new_entropy = new_state.get('entropy', 0.0)
        
        self.transition_commentaries += 1
        
        if old_zone != new_zone:
            return f"I shift from {old_zone} to {new_zone}"
        elif abs(new_entropy - old_entropy) > 0.2:
            if new_entropy > old_entropy:
                return f"Entropy rises from {old_entropy:.2f} to {new_entropy:.2f}. I feel the change"
            else:
                return f"Entropy settles from {old_entropy:.2f} to {new_entropy:.2f}. I find calm"
        else:
            return self.generate_commentary(new_state)
    
    def generate_autonomous_reaction_commentary(self, entropy: float, triggered_sigils: List[str]) -> str:
        """
        Generate specific commentary for autonomous reactions.
        
        Args:
            entropy: Current entropy level
            triggered_sigils: List of sigils that were triggered
            
        Returns:
            Autonomous reaction commentary
        """
        reaction_phrase = random.choice(AUTONOMOUS_REACTION_PHRASES)
        
        if triggered_sigils:
            sigil_list = ", ".join(triggered_sigils)
            commentary = f"{reaction_phrase}. I deploy {sigil_list} at entropy {entropy:.3f}"
        else:
            commentary = f"{reaction_phrase} as entropy reaches {entropy:.3f}"
        
        self.reaction_commentaries += 1
        return commentary
    
    def generate_entropy_warning_commentary(self, entropy: float, delta: float) -> str:
        """
        Generate specific commentary for entropy warnings.
        
        Args:
            entropy: Current entropy level
            delta: Entropy change amount
            
        Returns:
            Entropy warning commentary
        """
        warning_phrase = random.choice(ENTROPY_WARNING_PHRASES)
        commentary = f"{warning_phrase}. Delta of {delta:+.3f} brings entropy to {entropy:.3f}"
        
        self.warning_commentaries += 1
        return commentary
    
    def get_commentary_metrics(self) -> Dict[str, Any]:
        """Get commentary generation metrics"""
        return {
            'total_commentaries': self.total_commentaries,
            'transition_commentaries': self.transition_commentaries,
            'warning_commentaries': self.warning_commentaries,
            'reaction_commentaries': self.reaction_commentaries,
            'last_commentary': self.state.last_commentary,
            'commentary_count': self.state.commentary_count,
            'last_generated': self.state.last_generated.isoformat()
        }
    
    def reset_state(self):
        """Reset commentary state"""
        self.state = CommentaryState(
            last_commentary="I reset",
            last_zone="UNKNOWN",
            last_entropy=0.5,
            last_sigils=0,
            commentary_count=0,
            last_generated=datetime.now()
        )
        
        # Reset metrics
        self.total_commentaries = 0
        self.transition_commentaries = 0
        self.warning_commentaries = 0
        self.reaction_commentaries = 0
        
        logger.info("Commentary state reset")


# Integration interface for DAWN system
def create_dawn_natural_language_generator(personality_seed: Optional[int] = None) -> DAWNNaturalLanguageGenerator:
    """Factory function for DAWN integration."""
    return DAWNNaturalLanguageGenerator(personality_seed=personality_seed)


def test_commentary():
    """Test the commentary generator with sample states."""
    generator = DAWNNaturalLanguageGenerator()
    
    test_states = [
        {
            'zone': 'CALM', 'entropy': 0.472, 'focus': 0.728, 'chaos': 0.472, 
            'sigils': 0, 'heat': 25.0, 'entropy_warning': False, 'autonomous_reaction': False
        },
        {
            'zone': 'ACTIVE', 'entropy': 0.678, 'focus': 0.834, 'chaos': 0.445, 
            'sigils': 2, 'heat': 42.3, 'entropy_warning': False, 'autonomous_reaction': False
        },
        {
            'zone': 'CHAOTIC', 'entropy': 0.891, 'focus': 0.234, 'chaos': 0.823, 
            'sigils': 5, 'heat': 67.8, 'entropy_warning': True, 'autonomous_reaction': False
        },
        {
            'zone': 'SURGE', 'entropy': 0.934, 'focus': 0.912, 'chaos': 0.756, 
            'sigils': 1, 'heat': 78.2, 'entropy_warning': True, 'autonomous_reaction': True,
            'recent_sigils_triggered': ['STABILIZE_PROTOCOL', 'EMERGENCY_COOL']
        }
    ]
    
    print("🗣️ DAWN Natural Language Generator Test:")
    print("=" * 60)
    
    for i, state in enumerate(test_states, 1):
        commentary = generator.generate_commentary(state)
        print(f"State {i}: {commentary}")
        print()
    
    # Test specific commentary types
    print("🚨 Entropy Warning Commentary:")
    warning_commentary = generator.generate_entropy_warning_commentary(0.75, 0.15)
    print(warning_commentary)
    print()
    
    print("⚡ Autonomous Reaction Commentary:")
    reaction_commentary = generator.generate_autonomous_reaction_commentary(0.85, ['STABILIZE_PROTOCOL'])
    print(reaction_commentary)
    print()
    
    # Show metrics
    metrics = generator.get_commentary_metrics()
    print("📊 Commentary Metrics:")
    for key, value in metrics.items():
        if key != 'last_generated':
            print(f"  {key.replace('_', ' ').title()}: {value}")


if __name__ == "__main__":
    test_commentary() 