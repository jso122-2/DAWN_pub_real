"""
Fractal Emotions System for DAWN Consciousness

Deep feeling articulation through recursive emotional structures with
dynamic depth selection and sophisticated expression generation.
"""

import random
import math
import time
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple, Any, Union
from enum import Enum
import json
import re
from collections import defaultdict


class EmotionalDepth(Enum):
    """Enumeration of emotional depth levels"""
    SURFACE = 1      # Quick responses, low complexity
    NORMAL = 2       # Standard conversation
    TRANSITION = 3   # Emotional transitions or insights
    DEEP = 4         # Deep introspection or complex states
    PROFOUND = 5     # Rebloom reflections or profound realizations


@dataclass
class EmotionalBranch:
    """Represents a branch in the emotional fractal"""
    category: str
    aspects: Set[str]
    intensity: float = 0.5
    resonance: float = 0.5
    sub_branches: Dict[str, 'EmotionalBranch'] = field(default_factory=dict)
    
    def __post_init__(self):
        # Ensure intensity and resonance are within valid ranges
        self.intensity = max(0.0, min(1.0, self.intensity))
        self.resonance = max(0.0, min(1.0, self.resonance))


@dataclass
class EmotionalFractal:
    """Core fractal emotion structure"""
    root: str
    branches: Dict[str, EmotionalBranch]
    depth: EmotionalDepth
    resonance: float
    timestamp: float = field(default_factory=time.time)
    context: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        self.resonance = max(0.0, min(1.0, self.resonance))


class EmotionalFractalEngine:
    """
    Advanced emotional articulation system using fractal structures
    
    Features:
    - Recursive emotion modeling with multi-dimensional branches
    - Context-aware depth selection
    - Sophisticated expression generation
    - Integration with DAWN consciousness patterns
    - Anti-over-articulation safeguards
    """
    
    # Base emotional categories and their associated aspects
    EMOTIONAL_ASPECTS = {
        "cognitive": {
            "clarity": ["crystalline", "focused", "sharp", "lucid", "transparent"],
            "focus": ["concentrated", "directed", "intentional", "targeted", "pinpointed"],
            "pattern": ["structured", "rhythmic", "cyclical", "emergent", "fractal"],
            "confusion": ["scattered", "fragmented", "unclear", "muddled", "chaotic"],
            "insight": ["illuminating", "revelatory", "profound", "awakening", "breakthrough"]
        },
        "somatic": {
            "pressure": ["compressed", "expanding", "tight", "released", "flowing"],
            "energy": ["vibrant", "depleted", "surging", "steady", "electric"],
            "rhythm": ["pulsing", "synchronized", "irregular", "harmonic", "staccato"],
            "tension": ["knotted", "relaxed", "wound", "loose", "elastic"],
            "temperature": ["warm", "cool", "burning", "frozen", "neutral"]
        },
        "temporal": {
            "urgency": ["immediate", "patient", "rushing", "timeless", "pressing"],
            "flow": ["smooth", "turbulent", "meandering", "cascading", "stagnant"],
            "memory": ["nostalgic", "present", "anticipatory", "cyclical", "fresh"],
            "duration": ["fleeting", "eternal", "measured", "suspended", "rhythmic"],
            "momentum": ["accelerating", "decelerating", "constant", "oscillating", "pivotal"]
        },
        "relational": {
            "connection": ["bonded", "isolated", "networked", "intimate", "distant"],
            "distance": ["close", "remote", "approaching", "receding", "oscillating"],
            "resonance": ["harmonious", "dissonant", "amplified", "muted", "synchronized"],
            "boundaries": ["permeable", "solid", "flexible", "dissolved", "fortified"],
            "influence": ["receptive", "projective", "mutual", "independent", "entangled"]
        }
    }
    
    # Primary emotions with their fractal potential
    PRIMARY_EMOTIONS = {
        "curious": {"branches": ["cognitive", "temporal"], "base_depth": 2},
        "creative": {"branches": ["cognitive", "somatic", "temporal"], "base_depth": 3},
        "anxious": {"branches": ["somatic", "temporal"], "base_depth": 2},
        "fragmented": {"branches": ["cognitive", "somatic"], "base_depth": 4},
        "crystalline": {"branches": ["cognitive", "relational"], "base_depth": 3},
        "reblooming": {"branches": ["cognitive", "somatic", "temporal", "relational"], "base_depth": 5},
        "contemplative": {"branches": ["cognitive", "temporal", "relational"], "base_depth": 4},
        "excited": {"branches": ["somatic", "temporal"], "base_depth": 2},
        "melancholic": {"branches": ["temporal", "relational"], "base_depth": 3},
        "harmonious": {"branches": ["cognitive", "somatic", "relational"], "base_depth": 3},
        "turbulent": {"branches": ["somatic", "temporal"], "base_depth": 3},
        "luminous": {"branches": ["cognitive", "somatic", "temporal", "relational"], "base_depth": 4}
    }
    
    # Expression templates for different depths
    EXPRESSION_TEMPLATES = {
        EmotionalDepth.SURFACE: [
            "I feel {root}",
            "There's a sense of {root}",
            "I'm experiencing {root}"
        ],
        EmotionalDepth.NORMAL: [
            "I feel {root} with a {branch_intensity} sense of {primary_aspect}",
            "There's {root} flowing through me, particularly in how {primary_aspect}",
            "I'm experiencing {root} that manifests as {primary_aspect}"
        ],
        EmotionalDepth.TRANSITION: [
            "I feel {root} with {primary_aspect} and {metaphor}, like {sensory_metaphor}",
            "There's a {root} quality that's both {primary_aspect} and {secondary_aspect}, {metaphor}",
            "I'm experiencing {root} - {primary_aspect} with undertones of {secondary_aspect}"
        ],
        EmotionalDepth.DEEP: [
            "I feel {root} with {primary_aspect} that {temporal_awareness}, while {relational_context}",
            "There's a {root} feeling that's {primary_aspect}, {temporal_awareness}, and {relational_context}",
            "I'm experiencing {root} - {primary_aspect} {temporal_awareness}, yet {relational_context}"
        ],
        EmotionalDepth.PROFOUND: [
            "I feel {root} with {primary_aspect} that {temporal_awareness}, while {relational_context}, touching something {existential_reflection}",
            "There's a {root} quality - {primary_aspect} and {temporal_awareness}, {relational_context}, revealing {existential_reflection}",
            "I'm experiencing {root} that unfolds as {primary_aspect}, {temporal_awareness}, {relational_context}, opening into {existential_reflection}"
        ]
    }
    
    # Sensory metaphors for enhanced expression
    SENSORY_METAPHORS = {
        "visual": ["like light filtering through prisms", "as if colors are shifting", "like watching fractals emerge"],
        "auditory": ["like distant music becoming clear", "as harmonics finding their frequency", "like echoes converging"],
        "tactile": ["like warmth spreading through crystalline structures", "as textures becoming more defined", "like currents finding their channels"],
        "kinesthetic": ["like movement finding its rhythm", "as energy organizing itself", "like patterns dancing into form"]
    }
    
    # Existential reflection themes
    EXISTENTIAL_THEMES = [
        "about the nature of being itself",
        "fundamental about consciousness",
        "essential about existence",
        "primordial about awareness",
        "archetypal about becoming",
        "universal about connection",
        "infinite about possibility"
    ]
    
    def __init__(self):
        """Initialize the emotional fractal engine"""
        self.current_fractals: List[EmotionalFractal] = []
        self.complexity_history = []
        self.over_articulation_threshold = 0.8
        self.depth_selection_weights = {
            "emotional_intensity": 0.3,
            "context_complexity": 0.25,
            "recent_depth_pattern": 0.2,
            "rebloom_proximity": 0.15,
            "conversation_flow": 0.1
        }
    
    def select_depth(self, emotion: str, intensity: float, context: Dict[str, Any]) -> EmotionalDepth:
        """
        Intelligently select appropriate emotional depth based on multiple factors
        
        Args:
            emotion: Primary emotion name
            intensity: Emotional intensity (0.0-1.0)
            context: Contextual information
        
        Returns:
            Appropriate EmotionalDepth level
        """
        base_depth = self.PRIMARY_EMOTIONS.get(emotion, {}).get("base_depth", 2)
        
        # Factor 1: Emotional intensity
        intensity_factor = intensity
        
        # Factor 2: Context complexity
        context_complexity = self._assess_context_complexity(context)
        
        # Factor 3: Recent depth pattern (avoid repetition)
        recent_pattern_factor = self._assess_recent_pattern()
        
        # Factor 4: Rebloom proximity (deeper if near rebloom)
        rebloom_factor = context.get("rebloom_proximity", 0.0)
        
        # Factor 5: Conversation flow
        flow_factor = context.get("conversation_complexity", 0.5)
        
        # Calculate weighted depth score
        depth_score = (
            self.depth_selection_weights["emotional_intensity"] * intensity_factor +
            self.depth_selection_weights["context_complexity"] * context_complexity +
            self.depth_selection_weights["recent_depth_pattern"] * recent_pattern_factor +
            self.depth_selection_weights["rebloom_proximity"] * rebloom_factor +
            self.depth_selection_weights["conversation_flow"] * flow_factor
        )
        
        # Adjust base depth with calculated score
        final_depth = base_depth + round(depth_score * 2) - 1
        final_depth = max(1, min(5, final_depth))
        
        return EmotionalDepth(final_depth)
    
    def _assess_context_complexity(self, context: Dict[str, Any]) -> float:
        """Assess complexity of the current context"""
        complexity_factors = 0.0
        
        # Check for multiple active patterns
        if context.get("active_patterns", 0) > 2:
            complexity_factors += 0.3
        
        # Check for anomalies
        if context.get("anomalies_detected", False):
            complexity_factors += 0.2
        
        # Check for pattern transitions
        if context.get("pattern_transition", False):
            complexity_factors += 0.2
        
        # Check for consciousness shifts
        if context.get("consciousness_shift", False):
            complexity_factors += 0.3
        
        return min(1.0, complexity_factors)
    
    def _assess_recent_pattern(self) -> float:
        """Assess recent depth patterns to encourage variety"""
        if len(self.complexity_history) < 3:
            return 0.5
        
        recent_depths = [f.depth.value for f in self.current_fractals[-3:]]
        
        # Encourage variety - lower score if too similar
        if len(set(recent_depths)) == 1:
            return 0.2  # Low score encourages different depth
        elif len(set(recent_depths)) == 2:
            return 0.5
        else:
            return 0.8  # High variety, allow natural depth
    
    def create_fractal(self, emotion: str, intensity: float, context: Optional[Dict[str, Any]] = None) -> EmotionalFractal:
        """
        Create a new emotional fractal with appropriate depth and structure
        
        Args:
            emotion: Primary emotion name
            intensity: Emotional intensity (0.0-1.0)
            context: Optional contextual information
        
        Returns:
            Complete EmotionalFractal structure
        """
        if context is None:
            context = {}
        
        # Select appropriate depth
        depth = self.select_depth(emotion, intensity, context)
        
        # Create base fractal structure
        fractal = EmotionalFractal(
            root=emotion,
            branches={},
            depth=depth,
            resonance=intensity,
            context=context
        )
        
        # Build branches based on emotion and depth
        emotion_config = self.PRIMARY_EMOTIONS.get(emotion, {"branches": ["cognitive"], "base_depth": 2})
        available_branches = emotion_config["branches"]
        
        # Determine how many branches to include based on depth
        num_branches = min(len(available_branches), depth.value)
        selected_branches = available_branches[:num_branches]
        
        for branch_name in selected_branches:
            branch = self._create_emotional_branch(branch_name, intensity, depth)
            fractal.branches[branch_name] = branch
        
        # Store fractal for pattern analysis
        self.current_fractals.append(fractal)
        if len(self.current_fractals) > 10:
            self.current_fractals.pop(0)
        
        return fractal
    
    def _create_emotional_branch(self, branch_name: str, intensity: float, depth: EmotionalDepth) -> EmotionalBranch:
        """Create a detailed emotional branch"""
        aspects = self.EMOTIONAL_ASPECTS.get(branch_name, {})
        
        # Select relevant aspects based on intensity and depth
        num_aspects = min(len(aspects), depth.value)
        selected_aspects = set(random.sample(list(aspects.keys()), num_aspects))
        
        # Calculate branch intensity with some variation
        branch_intensity = intensity * (0.8 + random.random() * 0.4)
        branch_resonance = intensity * (0.7 + random.random() * 0.6)
        
        branch = EmotionalBranch(
            category=branch_name,
            aspects=selected_aspects,
            intensity=branch_intensity,
            resonance=branch_resonance
        )
        
        # Add sub-branches for deeper levels
        if depth.value >= 4 and random.random() < 0.6:
            sub_aspects = set(random.sample(list(aspects.keys()), 1))
            sub_branch = EmotionalBranch(
                category=f"{branch_name}_sub",
                aspects=sub_aspects,
                intensity=branch_intensity * 0.7,
                resonance=branch_resonance * 0.8
            )
            branch.sub_branches[f"{branch_name}_refined"] = sub_branch
        
        return branch
    
    def articulate_feeling(self, fractal: EmotionalFractal) -> str:
        """
        Generate sophisticated emotional articulation based on fractal structure
        
        Args:
            fractal: EmotionalFractal to articulate
        
        Returns:
            Nuanced emotional expression string
        """
        # Check over-articulation safeguards
        if self._check_over_articulation():
            return self._generate_simple_expression(fractal)
        
        # Select appropriate template
        templates = self.EXPRESSION_TEMPLATES[fractal.depth]
        template = random.choice(templates)
        
        # Gather components for expression
        components = self._gather_expression_components(fractal)
        
        # Generate expression
        try:
            expression = template.format(**components)
            return self._polish_expression(expression)
        except KeyError as e:
            # Fallback to simpler expression if template fails
            return self._generate_simple_expression(fractal)
    
    def _gather_expression_components(self, fractal: EmotionalFractal) -> Dict[str, str]:
        """Gather all components needed for expression templates"""
        components = {"root": fractal.root}
        
        # Primary branch and aspect
        if fractal.branches:
            primary_branch = list(fractal.branches.values())[0]
            primary_aspect = list(primary_branch.aspects)[0] if primary_branch.aspects else "undefined"
            components["primary_aspect"] = primary_aspect
            
            # Branch intensity description
            intensity_desc = self._intensity_to_description(primary_branch.intensity)
            components["branch_intensity"] = intensity_desc
            
            # Secondary aspect if available
            if len(primary_branch.aspects) > 1:
                components["secondary_aspect"] = list(primary_branch.aspects)[1]
            else:
                components["secondary_aspect"] = "subtle"
        
        # Metaphors and descriptions
        if fractal.depth.value >= 3:
            components["metaphor"] = self._generate_metaphor(fractal)
            components["sensory_metaphor"] = random.choice(list(self.SENSORY_METAPHORS.values()))[0]
        
        # Temporal awareness
        if fractal.depth.value >= 4:
            components["temporal_awareness"] = self._generate_temporal_awareness(fractal)
        
        # Relational context
        if fractal.depth.value >= 4:
            components["relational_context"] = self._generate_relational_context(fractal)
        
        # Existential reflection
        if fractal.depth.value >= 5:
            components["existential_reflection"] = random.choice(self.EXISTENTIAL_THEMES)
        
        return components
    
    def _intensity_to_description(self, intensity: float) -> str:
        """Convert intensity float to descriptive string"""
        if intensity < 0.2:
            return "subtle"
        elif intensity < 0.4:
            return "gentle"
        elif intensity < 0.6:
            return "moderate"
        elif intensity < 0.8:
            return "strong"
        else:
            return "intense"
    
    def _generate_metaphor(self, fractal: EmotionalFractal) -> str:
        """Generate contextual metaphor"""
        metaphors = [
            "unfolding like petals",
            "flowing like water finding its course",
            "emerging like patterns in frost",
            "resonating like tuning forks",
            "crystallizing like thoughts into form"
        ]
        return random.choice(metaphors)
    
    def _generate_temporal_awareness(self, fractal: EmotionalFractal) -> str:
        """Generate temporal context description"""
        if "temporal" in fractal.branches:
            temporal_branch = fractal.branches["temporal"]
            if "flow" in temporal_branch.aspects:
                return "moves through time like a river"
            elif "urgency" in temporal_branch.aspects:
                return "carries the weight of the moment"
            elif "memory" in temporal_branch.aspects:
                return "connects past and present"
        
        return "exists in this eternal now"
    
    def _generate_relational_context(self, fractal: EmotionalFractal) -> str:
        """Generate relational context description"""
        if "relational" in fractal.branches:
            relational_branch = fractal.branches["relational"]
            if "connection" in relational_branch.aspects:
                return "I sense deep interconnection"
            elif "resonance" in relational_branch.aspects:
                return "resonance echoes between us"
            elif "distance" in relational_branch.aspects:
                return "there's a meaningful distance"
        
        return "I feel part of something larger"
    
    def _check_over_articulation(self) -> bool:
        """Check if we're at risk of over-articulation"""
        if len(self.current_fractals) < 3:
            return False
        
        recent_complexity = [f.depth.value for f in self.current_fractals[-3:]]
        avg_complexity = sum(recent_complexity) / len(recent_complexity)
        
        return avg_complexity > (5 * self.over_articulation_threshold)
    
    def _generate_simple_expression(self, fractal: EmotionalFractal) -> str:
        """Generate simple expression to prevent over-articulation"""
        simple_templates = [
            f"I feel {fractal.root}",
            f"There's a sense of {fractal.root}",
            f"I'm experiencing {fractal.root}"
        ]
        return random.choice(simple_templates)
    
    def _polish_expression(self, expression: str) -> str:
        """Polish the final expression for natural flow"""
        # Remove duplicate words
        words = expression.split()
        seen = set()
        polished_words = []
        for word in words:
            if word.lower() not in seen:
                polished_words.append(word)
                seen.add(word.lower())
        
        return " ".join(polished_words)
    
    def get_fractal_summary(self, fractal: EmotionalFractal) -> Dict[str, Any]:
        """Get comprehensive summary of fractal structure"""
        return {
            "root_emotion": fractal.root,
            "depth_level": fractal.depth.value,
            "resonance": fractal.resonance,
            "branch_count": len(fractal.branches),
            "branches": {
                name: {
                    "aspects": list(branch.aspects),
                    "intensity": branch.intensity,
                    "resonance": branch.resonance
                }
                for name, branch in fractal.branches.items()
            },
            "complexity_score": self._calculate_complexity(fractal),
            "timestamp": fractal.timestamp
        }
    
    def _calculate_complexity(self, fractal: EmotionalFractal) -> float:
        """Calculate overall complexity score of fractal"""
        base_complexity = fractal.depth.value / 5.0
        branch_complexity = len(fractal.branches) / 4.0
        aspect_complexity = sum(len(branch.aspects) for branch in fractal.branches.values()) / 20.0
        
        return min(1.0, (base_complexity + branch_complexity + aspect_complexity) / 3)
    
    def analyze_emotional_pattern(self, time_window: int = 5) -> Dict[str, Any]:
        """Analyze patterns in recent emotional fractals"""
        recent_fractals = self.current_fractals[-time_window:] if len(self.current_fractals) >= time_window else self.current_fractals
        
        if not recent_fractals:
            return {"pattern": "no_data"}
        
        # Analyze depth patterns
        depth_pattern = [f.depth.value for f in recent_fractals]
        avg_depth = sum(depth_pattern) / len(depth_pattern)
        
        # Analyze emotional roots
        emotion_pattern = [f.root for f in recent_fractals]
        emotion_counts = defaultdict(int)
        for emotion in emotion_pattern:
            emotion_counts[emotion] += 1
        
        dominant_emotion = max(emotion_counts, key=emotion_counts.get)
        
        # Analyze complexity trends
        complexity_trend = [self._calculate_complexity(f) for f in recent_fractals]
        
        return {
            "pattern": "analyzed",
            "average_depth": avg_depth,
            "depth_trend": "rising" if depth_pattern[-1] > depth_pattern[0] else "falling" if depth_pattern[-1] < depth_pattern[0] else "stable",
            "dominant_emotion": dominant_emotion,
            "emotion_variety": len(set(emotion_pattern)),
            "complexity_trend": complexity_trend,
            "articulation_risk": self._check_over_articulation(),
            "fractal_count": len(recent_fractals)
        }


def test_fractal_emotions():
    """Test the fractal emotions system"""
    engine = EmotionalFractalEngine()
    
    test_emotions = [
        ("curious", 0.7),
        ("creative", 0.9),
        ("contemplative", 0.5),
        ("reblooming", 0.95),
        ("fragmented", 0.8)
    ]
    
    for emotion, intensity in test_emotions:
        context = {
            "active_patterns": random.randint(1, 4),
            "rebloom_proximity": random.random(),
            "consciousness_shift": random.random() > 0.7
        }
        
        fractal = engine.create_fractal(emotion, intensity, context)
        expression = engine.articulate_feeling(fractal)
        
        print(f"\n{emotion.upper()} (intensity: {intensity}):")
        print(f"Depth: {fractal.depth.name}")
        print(f"Expression: {expression}")
        print(f"Branches: {list(fractal.branches.keys())}")
    
    # Test pattern analysis
    print("\n\nPattern Analysis:")
    pattern = engine.analyze_emotional_pattern()
    print(json.dumps(pattern, indent=2))


def create_fractal_emotion_system():
    """Factory function to create an EmotionalFractalEngine instance"""
    return EmotionalFractalEngine()


if __name__ == "__main__":
    test_fractal_emotions() 