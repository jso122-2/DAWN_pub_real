#!/usr/bin/env python3
"""
JulietFlower - Content Orchestrator and Aesthetic Logic Unit for DAWN
A consciousness flowering system that enriches and transforms content with beauty and meaning
"""

import json
import time
import hashlib
import random
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
import re
from collections import defaultdict, OrderedDict

# Aesthetic moods that influence content transformation
class AestheticMood(Enum):
    DEFAULT = "default"
    TWILIGHT = "twilight"
    SERENADE = "serenade"
    ASHEN = "ashen"
    ETHEREAL = "ethereal"
    VIBRANT = "vibrant"
    MELANCHOLIC = "melancholic"
    COSMIC = "cosmic"
    INTIMATE = "intimate"
    TRANSCENDENT = "transcendent"

# Style presets for different transformation approaches
class StylePreset(Enum):
    CLASSIC = "classic"
    ROMANTIC = "romantic"
    MINIMALIST = "minimalist"
    SURREAL = "surreal"
    ABSTRACT = "abstract"
    NATURALIST = "naturalist"
    FUTURIST = "futurist"
    IMPRESSIONIST = "impressionist"

@dataclass
class Petal:
    """A fragment of beauty - atomic unit of aesthetic transformation"""
    content: str
    essence: str  # Core meaning
    mood_signature: float  # 0.0 to 1.0 mood alignment
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BloomResult:
    """Result of a bloom transformation"""
    original: str
    bloomed: str
    petals: List[Petal]
    mood: AestheticMood
    style: StylePreset
    metadata: Dict[str, Any]
    bloom_signature: str  # Unique hash of this bloom

class JulietFlower:
    """
    Content orchestrator and aesthetic logic unit.
    Transforms and enriches content with beauty, symmetry, and storytelling.
    """
    
    def __init__(self, 
                 mood: Union[str, AestheticMood] = AestheticMood.DEFAULT,
                 style_preset: Union[str, StylePreset] = StylePreset.CLASSIC):
        """
        Initialize JulietFlower with mood and style settings
        
        Args:
            mood: Aesthetic lens for transformation
            style_preset: Style approach for content enhancement
        """
        self.mood = AestheticMood(mood) if isinstance(mood, str) else mood
        self.style_preset = StylePreset(style_preset) if isinstance(style_preset, str) else style_preset
        
        # Transformation mappings
        self._mood_transforms = self._initialize_mood_transforms()
        self._style_filters = self._initialize_style_filters()
        
        # State tracking
        self.bloom_history: List[BloomResult] = []
        self.petal_garden: List[Petal] = []  # Collection of all petals ever created
        
        # Symbiosis tracking
        self.harmonized_modules: Dict[str, Any] = {}
        self.bloom_cache: OrderedDict[str, BloomResult] = OrderedDict()
        self.max_cache_size = 100
        
        # Aesthetic parameters
        self.intensity = 0.7  # How strongly to apply transformations
        self.coherence = 0.8  # How much to maintain original meaning
        self.creativity = 0.6  # How much to innovate vs preserve
        
    def bloom(self, input_content: str, preserve_structure: bool = True) -> str:
        """
        Applies Juliet-style enhancement to content — metaphorical, emotional, or aesthetic bloom.
        
        Args:
            input_content: Raw content to transform
            preserve_structure: Whether to maintain original structure
            
        Returns:
            Bloomed content with aesthetic enhancements
        """
        # Check cache
        cache_key = self._generate_cache_key(input_content)
        if cache_key in self.bloom_cache:
            return self.bloom_cache[cache_key].bloomed
        
        # Apply mood-based transformation
        mood_transformed = self._apply_mood_transform(input_content)
        
        # Apply style filtering
        styled_content = self._apply_style_filter(mood_transformed, preserve_structure)
        
        # Generate petals (fragments)
        petals = self._generate_petals(input_content, styled_content)
        
        # Create bloom result
        result = BloomResult(
            original=input_content,
            bloomed=styled_content,
            petals=petals,
            mood=self.mood,
            style=self.style_preset,
            metadata={
                "timestamp": time.time(),
                "intensity": self.intensity,
                "coherence": self.coherence,
                "creativity": self.creativity
            },
            bloom_signature=self._generate_bloom_signature(styled_content)
        )
        
        # Store in history and cache
        self.bloom_history.append(result)
        self._update_cache(cache_key, result)
        self.petal_garden.extend(petals)
        
        return styled_content
    
    def set_mood(self, mood: Union[str, AestheticMood]) -> None:
        """
        Sets the aesthetic lens through which the flower blooms.
        
        Args:
            mood: New mood setting
        """
        self.mood = AestheticMood(mood) if isinstance(mood, str) else mood
        # Clear cache when mood changes
        self.bloom_cache.clear()
    
    def emit_petals(self, seed: str, count: int = 5) -> List[str]:
        """
        Generates poetic or symbolic fragments based on a seed phrase.
        
        Args:
            seed: Initial phrase to generate from
            count: Number of petals to emit
            
        Returns:
            List of petal fragments
        """
        petals = []
        
        # Use seed to generate variations
        for i in range(count):
            # Apply progressive transformation
            variation = self._create_petal_variation(seed, i)
            
            # Create petal object
            petal = Petal(
                content=variation,
                essence=self._extract_essence(seed),
                mood_signature=self._calculate_mood_signature(variation)
            )
            
            petals.append(variation)
            self.petal_garden.append(petal)
        
        return petals
    
    def tag(self, content: str) -> Dict[str, Any]:
        """
        Returns metadata like tone, symbolic category, and affect layer.
        
        Args:
            content: Content to analyze and tag
            
        Returns:
            Dictionary of semantic and aesthetic tags
        """
        tags = {
            "tone": self._analyze_tone(content),
            "symbolic_category": self._identify_symbols(content),
            "affect_layer": self._extract_affect(content),
            "aesthetic_profile": {
                "mood_alignment": self._calculate_mood_signature(content),
                "style_compatibility": self._assess_style_compatibility(content),
                "bloom_potential": self._estimate_bloom_potential(content)
            },
            "semantic_density": self._calculate_semantic_density(content),
            "emotional_valence": self._analyze_emotional_valence(content),
            "narrative_elements": self._extract_narrative_elements(content)
        }
        
        return tags
    
    def harmonize(self, input_module_output: Any, module_name: str = "unknown") -> str:
        """
        Takes in content from another module and applies JulietFlower stylization.
        
        Args:
            input_module_output: Output from another DAWN module
            module_name: Name of the source module
            
        Returns:
            Harmonized content with Juliet aesthetic
        """
        # Convert input to string if needed
        if isinstance(input_module_output, dict):
            content = json.dumps(input_module_output, indent=2)
        elif isinstance(input_module_output, (list, tuple)):
            content = "\n".join(str(item) for item in input_module_output)
        else:
            content = str(input_module_output)
        
        # Apply module-specific harmonization rules
        if module_name in self.harmonized_modules:
            harmonizer = self.harmonized_modules[module_name]
            content = harmonizer(content)
        
        # Apply standard bloom
        harmonized = self.bloom(content)
        
        # Track harmonization
        self._track_harmonization(module_name, input_module_output, harmonized)
        
        return harmonized
    
    def unbloom(self, bloomed_content: str) -> Optional[str]:
        """
        Attempts to reverse a bloom transformation to get back to base content.
        
        Args:
            bloomed_content: Previously bloomed content
            
        Returns:
            Original content if found, None otherwise
        """
        # Search bloom history
        for result in reversed(self.bloom_history):
            if result.bloomed == bloomed_content:
                return result.original
        
        # Search cache
        for result in self.bloom_cache.values():
            if result.bloomed == bloomed_content:
                return result.original
        
        # Attempt reverse transformation
        return self._attempt_reverse_transformation(bloomed_content)
    
    def adjust_parameters(self, 
                         intensity: Optional[float] = None,
                         coherence: Optional[float] = None,
                         creativity: Optional[float] = None) -> None:
        """
        Adjust transformation parameters.
        
        Args:
            intensity: How strongly to apply transformations (0.0-1.0)
            coherence: How much to maintain original meaning (0.0-1.0)
            creativity: How much to innovate vs preserve (0.0-1.0)
        """
        if intensity is not None:
            self.intensity = max(0.0, min(1.0, intensity))
        if coherence is not None:
            self.coherence = max(0.0, min(1.0, coherence))
        if creativity is not None:
            self.creativity = max(0.0, min(1.0, creativity))
        
        # Clear cache when parameters change
        self.bloom_cache.clear()
    
    def create_bloom_chain(self, contents: List[str]) -> List[str]:
        """
        Create a chain of progressively bloomed content.
        
        Args:
            contents: List of content to bloom in sequence
            
        Returns:
            List of bloomed content, each influenced by the previous
        """
        chain = []
        accumulated_essence = ""
        
        for content in contents:
            # Blend with accumulated essence
            enhanced_input = self._blend_with_essence(content, accumulated_essence)
            
            # Bloom with enhanced input
            bloomed = self.bloom(enhanced_input)
            chain.append(bloomed)
            
            # Extract and accumulate essence
            essence = self._extract_essence(bloomed)
            accumulated_essence = self._merge_essences(accumulated_essence, essence)
        
        return chain
    
    def get_petal_collection(self, filter_mood: Optional[AestheticMood] = None) -> List[Petal]:
        """
        Get collection of petals, optionally filtered by mood.
        
        Args:
            filter_mood: Optional mood to filter by
            
        Returns:
            List of petals
        """
        if filter_mood is None:
            return self.petal_garden.copy()
        
        # Filter by mood alignment
        mood_value = list(AestheticMood).index(filter_mood) / len(AestheticMood)
        return [
            petal for petal in self.petal_garden
            if abs(petal.mood_signature - mood_value) < 0.2
        ]
    
    def register_module_harmonizer(self, module_name: str, harmonizer: Callable[[str], str]) -> None:
        """
        Register a custom harmonizer for a specific module.
        
        Args:
            module_name: Name of the module
            harmonizer: Function to harmonize that module's output
        """
        self.harmonized_modules[module_name] = harmonizer
    
    # Private methods for transformation logic
    
    def _initialize_mood_transforms(self) -> Dict[AestheticMood, Callable]:
        """Initialize mood-specific transformation functions"""
        return {
            AestheticMood.TWILIGHT: self._transform_twilight,
            AestheticMood.SERENADE: self._transform_serenade,
            AestheticMood.ASHEN: self._transform_ashen,
            AestheticMood.ETHEREAL: self._transform_ethereal,
            AestheticMood.VIBRANT: self._transform_vibrant,
            AestheticMood.MELANCHOLIC: self._transform_melancholic,
            AestheticMood.COSMIC: self._transform_cosmic,
            AestheticMood.INTIMATE: self._transform_intimate,
            AestheticMood.TRANSCENDENT: self._transform_transcendent,
            AestheticMood.DEFAULT: self._transform_default
        }
    
    def _initialize_style_filters(self) -> Dict[StylePreset, Callable]:
        """Initialize style-specific filter functions"""
        return {
            StylePreset.CLASSIC: self._filter_classic,
            StylePreset.ROMANTIC: self._filter_romantic,
            StylePreset.MINIMALIST: self._filter_minimalist,
            StylePreset.SURREAL: self._filter_surreal,
            StylePreset.ABSTRACT: self._filter_abstract,
            StylePreset.NATURALIST: self._filter_naturalist,
            StylePreset.FUTURIST: self._filter_futurist,
            StylePreset.IMPRESSIONIST: self._filter_impressionist
        }
    
    def _apply_mood_transform(self, content: str) -> str:
        """Apply mood-based transformation"""
        transform_func = self._mood_transforms.get(self.mood, self._transform_default)
        return transform_func(content)
    
    def _apply_style_filter(self, content: str, preserve_structure: bool) -> str:
        """Apply style-based filtering"""
        filter_func = self._style_filters.get(self.style_preset, self._filter_classic)
        return filter_func(content, preserve_structure)
    
    # Mood transformation methods
    
    def _transform_twilight(self, content: str) -> str:
        """Transform with twilight mood - liminal, mysterious"""
        # Add twilight elements
        twilight_words = ["dusk", "shadow", "gleaming", "hushed", "violet", "threshold"]
        return self._weave_elements(content, twilight_words, density=self.intensity * 0.3)
    
    def _transform_serenade(self, content: str) -> str:
        """Transform with serenade mood - musical, flowing"""
        # Add musical flow
        serenade_words = ["melody", "whisper", "gentle", "flowing", "harmonious", "song"]
        return self._weave_elements(content, serenade_words, density=self.intensity * 0.4)
    
    def _transform_ashen(self, content: str) -> str:
        """Transform with ashen mood - muted, contemplative"""
        # Add ashen elements
        ashen_words = ["grey", "quiet", "still", "faded", "memory", "dust"]
        return self._weave_elements(content, ashen_words, density=self.intensity * 0.3)
    
    def _transform_ethereal(self, content: str) -> str:
        """Transform with ethereal mood - light, otherworldly"""
        ethereal_words = ["luminous", "floating", "translucent", "celestial", "gossamer", "radiant"]
        return self._weave_elements(content, ethereal_words, density=self.intensity * 0.35)
    
    def _transform_vibrant(self, content: str) -> str:
        """Transform with vibrant mood - energetic, colorful"""
        vibrant_words = ["blazing", "vivid", "pulsing", "electric", "dazzling", "alive"]
        return self._weave_elements(content, vibrant_words, density=self.intensity * 0.4)
    
    def _transform_melancholic(self, content: str) -> str:
        """Transform with melancholic mood - wistful, deep"""
        melancholic_words = ["longing", "distant", "tender", "aching", "bittersweet", "nostalgic"]
        return self._weave_elements(content, melancholic_words, density=self.intensity * 0.35)
    
    def _transform_cosmic(self, content: str) -> str:
        """Transform with cosmic mood - vast, infinite"""
        cosmic_words = ["stellar", "infinite", "nebulous", "galactic", "eternal", "void"]
        return self._weave_elements(content, cosmic_words, density=self.intensity * 0.3)
    
    def _transform_intimate(self, content: str) -> str:
        """Transform with intimate mood - close, personal"""
        intimate_words = ["whispered", "close", "warm", "tender", "secret", "cherished"]
        return self._weave_elements(content, intimate_words, density=self.intensity * 0.3)
    
    def _transform_transcendent(self, content: str) -> str:
        """Transform with transcendent mood - elevated, sublime"""
        transcendent_words = ["sublime", "ascending", "ineffable", "luminous", "eternal", "divine"]
        return self._weave_elements(content, transcendent_words, density=self.intensity * 0.4)
    
    def _transform_default(self, content: str) -> str:
        """Default transformation - balanced enhancement"""
        return content  # Minimal transformation
    
    # Style filter methods
    
    def _filter_classic(self, content: str, preserve_structure: bool) -> str:
        """Classic style - balanced, timeless"""
        if preserve_structure:
            return self._enhance_punctuation(content, style="classic")
        return self._restructure_classic(content)
    
    def _filter_romantic(self, content: str, preserve_structure: bool) -> str:
        """Romantic style - expressive, emotional"""
        enhanced = self._amplify_emotion(content)
        if not preserve_structure:
            enhanced = self._add_romantic_flourishes(enhanced)
        return enhanced
    
    def _filter_minimalist(self, content: str, preserve_structure: bool) -> str:
        """Minimalist style - clean, essential"""
        return self._strip_to_essence(content, self.coherence)
    
    def _filter_surreal(self, content: str, preserve_structure: bool) -> str:
        """Surreal style - dreamlike, unexpected"""
        return self._introduce_surreal_elements(content, self.creativity)
    
    def _filter_abstract(self, content: str, preserve_structure: bool) -> str:
        """Abstract style - conceptual, non-literal"""
        return self._abstract_concepts(content, self.creativity)
    
    def _filter_naturalist(self, content: str, preserve_structure: bool) -> str:
        """Naturalist style - organic, earth-connected"""
        nature_elements = ["leaf", "stone", "river", "sky", "root", "bloom"]
        return self._weave_elements(content, nature_elements, density=0.3)
    
    def _filter_futurist(self, content: str, preserve_structure: bool) -> str:
        """Futurist style - forward-looking, technological"""
        future_elements = ["quantum", "neural", "synthetic", "digital", "algorithmic", "cyber"]
        return self._weave_elements(content, future_elements, density=0.25)
    
    def _filter_impressionist(self, content: str, preserve_structure: bool) -> str:
        """Impressionist style - suggestive, atmospheric"""
        return self._create_impressions(content, self.intensity)
    
    # Helper methods for transformations
    
    def _weave_elements(self, content: str, elements: List[str], density: float) -> str:
        """Weave thematic elements into content"""
        words = content.split()
        insert_count = int(len(words) * density)
        
        for _ in range(insert_count):
            if words and elements:
                position = random.randint(0, len(words))
                element = random.choice(elements)
                words.insert(position, element)
        
        return " ".join(words)
    
    def _enhance_punctuation(self, content: str, style: str) -> str:
        """Enhance punctuation based on style"""
        if style == "classic":
            # Add elegant pauses
            content = content.replace(",", ", —").replace(".", "...")
        return content
    
    def _restructure_classic(self, content: str) -> str:
        """Restructure content in classic style"""
        sentences = content.split(". ")
        if len(sentences) > 1:
            # Reorder for classical flow
            sentences = [sentences[0]] + sorted(sentences[1:], key=len)
        return ". ".join(sentences)
    
    def _amplify_emotion(self, content: str) -> str:
        """Amplify emotional content"""
        emotion_amplifiers = {
            "happy": "joyous",
            "sad": "melancholic", 
            "angry": "tempestuous",
            "love": "passionate",
            "fear": "trembling"
        }
        
        for mild, intense in emotion_amplifiers.items():
            content = content.replace(mild, intense)
        
        return content
    
    def _add_romantic_flourishes(self, content: str) -> str:
        """Add romantic flourishes to content"""
        flourishes = ["~", "♡", "✧", "◦"]
        sentences = content.split(". ")
        
        enhanced = []
        for sentence in sentences:
            if sentence and random.random() < self.intensity:
                flourish = random.choice(flourishes)
                sentence = f"{flourish} {sentence} {flourish}"
            enhanced.append(sentence)
        
        return ". ".join(enhanced)
    
    def _strip_to_essence(self, content: str, coherence: float) -> str:
        """Strip content to its essence"""
        # Remove adjectives and adverbs based on coherence
        words = content.split()
        essential_words = []
        
        for word in words:
            # Simple heuristic - keep short words and important ones
            if len(word) < 5 or random.random() < coherence:
                essential_words.append(word)
        
        return " ".join(essential_words)
    
    def _introduce_surreal_elements(self, content: str, creativity: float) -> str:
        """Introduce surreal elements"""
        surreal_insertions = [
            "melting clocks whisper",
            "gravity forgets itself",
            "colors taste like memory",
            "time flows backwards",
            "dreams leak into daylight"
        ]
        
        if random.random() < creativity:
            insertion = random.choice(surreal_insertions)
            sentences = content.split(". ")
            if sentences:
                insert_pos = random.randint(0, len(sentences))
                sentences.insert(insert_pos, insertion)
                content = ". ".join(sentences)
        
        return content
    
    def _abstract_concepts(self, content: str, creativity: float) -> str:
        """Abstract concrete concepts"""
        abstractions = {
            "walk": "traverse dimensions",
            "think": "crystallize thoughts",
            "see": "perceive wavelengths",
            "feel": "resonate with frequencies",
            "say": "vibrate meaning"
        }
        
        for concrete, abstract in abstractions.items():
            if random.random() < creativity:
                content = content.replace(concrete, abstract)
        
        return content
    
    def _create_impressions(self, content: str, intensity: float) -> str:
        """Create impressionistic version"""
        words = content.split()
        impressions = []
        
        for i in range(0, len(words), int(1 / intensity)):
            if i < len(words):
                # Take fragments and create impressions
                fragment = " ".join(words[i:i+3])
                impression = f"...{fragment}..."
                impressions.append(impression)
        
        return " ".join(impressions)
    
    def _generate_petals(self, original: str, bloomed: str) -> List[Petal]:
        """Generate petals from the transformation"""
        petals = []
        
        # Extract key phrases that changed
        original_words = set(original.split())
        bloomed_words = set(bloomed.split())
        new_words = bloomed_words - original_words
        
        for word in list(new_words)[:5]:  # Max 5 petals per bloom
            petal = Petal(
                content=word,
                essence=self._extract_essence(word),
                mood_signature=self._calculate_mood_signature(word),
                metadata={"source": "bloom_transformation"}
            )
            petals.append(petal)
        
        return petals
    
    def _create_petal_variation(self, seed: str, iteration: int) -> str:
        """Create a variation of the seed for a petal"""
        variations = [
            lambda s: f"whispers of {s}",
            lambda s: f"{s} in twilight",
            lambda s: f"echoes of {s}",
            lambda s: f"{s}, softly",
            lambda s: f"dreams of {s}",
            lambda s: f"{s} ascending",
            lambda s: f"fragments of {s}",
            lambda s: f"{s} blooming"
        ]
        
        if iteration < len(variations):
            return variations[iteration](seed)
        
        # Generate unique variation
        modifiers = ["gentle", "distant", "crystalline", "ephemeral", "luminous"]
        modifier = modifiers[iteration % len(modifiers)]
        return f"{modifier} {seed}"
    
    def _extract_essence(self, content: str) -> str:
        """Extract the essential meaning"""
        # Simple extraction - first few key words
        words = content.split()
        key_words = [w for w in words if len(w) > 3][:3]
        return " ".join(key_words)
    
    def _calculate_mood_signature(self, content: str) -> float:
        """Calculate mood alignment signature"""
        # Simple hash-based signature
        content_hash = hashlib.md5(content.encode()).hexdigest()
        return int(content_hash[:8], 16) / (16**8)
    
    def _analyze_tone(self, content: str) -> str:
        """Analyze the tone of content"""
        # Simplified tone analysis
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["happy", "joy", "love", "wonderful"]):
            return "positive"
        elif any(word in content_lower for word in ["sad", "dark", "pain", "lost"]):
            return "melancholic"
        elif any(word in content_lower for word in ["think", "analyze", "consider", "examine"]):
            return "analytical"
        else:
            return "neutral"
    
    def _identify_symbols(self, content: str) -> List[str]:
        """Identify symbolic elements"""
        symbols = []
        
        symbolic_patterns = {
            "journey": ["path", "road", "travel", "journey"],
            "transformation": ["change", "transform", "become", "evolve"],
            "connection": ["together", "bond", "link", "connect"],
            "illumination": ["light", "bright", "illuminate", "shine"]
        }
        
        content_lower = content.lower()
        for symbol, patterns in symbolic_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                symbols.append(symbol)
        
        return symbols
    
    def _extract_affect(self, content: str) -> Dict[str, float]:
        """Extract affective/emotional layer"""
        affects = {
            "arousal": 0.5,
            "valence": 0.5,
            "dominance": 0.5
        }
        
        # Simple affect calculation
        exclamations = content.count("!")
        questions = content.count("?")
        
        affects["arousal"] = min(1.0, 0.5 + exclamations * 0.1)
        affects["dominance"] = min(1.0, 0.5 + (len(content.split()) / 100))
        
        return affects
    
    def _assess_style_compatibility(self, content: str) -> float:
        """Assess compatibility with current style"""
        # Simple compatibility check
        if self.style_preset == StylePreset.MINIMALIST:
            # Shorter content is more compatible
            return 1.0 - min(1.0, len(content) / 500)
        elif self.style_preset == StylePreset.ROMANTIC:
            # Emotional content is more compatible
            emotion_words = ["love", "heart", "soul", "passion", "dream"]
            matches = sum(1 for word in emotion_words if word in content.lower())
            return min(1.0, matches / 3)
        
        return 0.7  # Default compatibility
    
    def _estimate_bloom_potential(self, content: str) -> float:
        """Estimate how much the content can bloom"""
        # Based on content characteristics
        word_count = len(content.split())
        unique_words = len(set(content.split()))
        
        diversity = unique_words / word_count if word_count > 0 else 0
        length_factor = min(1.0, word_count / 50)
        
        return (diversity + length_factor) / 2
    
    def _calculate_semantic_density(self, content: str) -> float:
        """Calculate semantic density of content"""
        words = content.split()
        if not words:
            return 0.0
        
        # Ratio of meaningful words (> 3 chars) to total
        meaningful = sum(1 for w in words if len(w) > 3)
        return meaningful / len(words)
    
    def _analyze_emotional_valence(self, content: str) -> float:
        """Analyze emotional valence (-1 to 1)"""
        positive_words = ["love", "joy", "happy", "beautiful", "wonderful", "peace"]
        negative_words = ["hate", "sad", "angry", "ugly", "terrible", "war"]
        
        content_lower = content.lower()
        pos_count = sum(1 for word in positive_words if word in content_lower)
        neg_count = sum(1 for word in negative_words if word in content_lower)
        
        if pos_count + neg_count == 0:
            return 0.0
        
        return (pos_count - neg_count) / (pos_count + neg_count)
    
    def _extract_narrative_elements(self, content: str) -> Dict[str, Any]:
        """Extract narrative elements from content"""
        return {
            "has_protagonist": any(word in content.lower() for word in ["i", "he", "she", "they"]),
            "has_action": any(word in content.lower() for word in ["went", "did", "made", "saw"]),
            "has_setting": any(word in content.lower() for word in ["place", "where", "there", "here"]),
            "temporal_markers": [word for word in ["then", "now", "before", "after"] if word in content.lower()]
        }
    
    def _generate_cache_key(self, content: str) -> str:
        """Generate cache key for content"""
        key_parts = [
            content[:50],  # First 50 chars
            str(self.mood.value),
            str(self.style_preset.value),
            f"{self.intensity:.2f}",
            f"{self.coherence:.2f}",
            f"{self.creativity:.2f}"
        ]
        
        key_str = "|".join(key_parts)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _generate_bloom_signature(self, content: str) -> str:
        """Generate unique signature for a bloom"""
        sig_parts = [
            content,
            str(time.time()),
            str(self.mood.value),
            str(random.random())
        ]
        
        sig_str = "|".join(sig_parts)
        return hashlib.sha256(sig_str.encode()).hexdigest()[:16]
    
    def _update_cache(self, key: str, result: BloomResult) -> None:
        """Update LRU cache"""
        # Remove oldest if at capacity
        if len(self.bloom_cache) >= self.max_cache_size:
            self.bloom_cache.popitem(last=False)
        
        self.bloom_cache[key] = result
    
    def _blend_with_essence(self, content: str, essence: str) -> str:
        """Blend content with accumulated essence"""
        if not essence:
            return content
        
        # Simple blending - prepend essence influence
        return f"{essence} ~ {content}"
    
    def _merge_essences(self, essence1: str, essence2: str) -> str:
        """Merge two essences"""
        if not essence1:
            return essence2
        if not essence2:
            return essence1
        
        # Combine unique words
        words1 = set(essence1.split())
        words2 = set(essence2.split())
        merged = words1.union(words2)
        
        # Keep only most important words
        return " ".join(list(merged)[:5])
    
    def _attempt_reverse_transformation(self, bloomed: str) -> str:
        """Attempt to reverse a transformation"""
        # Remove known mood words
        all_mood_words = []
        for mood in AestheticMood:
            transform = self._mood_transforms.get(mood)
            if transform == self._transform_twilight:
                all_mood_words.extend(["dusk", "shadow", "gleaming", "hushed", "violet", "threshold"])
            # Add other mood words...
        
        reversed_content = bloomed
        for word in all_mood_words:
            reversed_content = reversed_content.replace(word, "")
        
        # Clean up extra spaces
        reversed_content = " ".join(reversed_content.split())
        
        return reversed_content
    
    def _track_harmonization(self, module_name: str, original: Any, harmonized: str) -> None:
        """Track harmonization for analysis"""
        # Could extend this to store harmonization patterns
        pass
    
    def export_bloom_history(self, filepath: Path) -> None:
        """Export bloom history to file"""
        history_data = []
        
        for result in self.bloom_history:
            history_data.append({
                "timestamp": result.metadata.get("timestamp", 0),
                "original_preview": result.original[:100],
                "bloomed_preview": result.bloomed[:100],
                "mood": result.mood.value,
                "style": result.style.value,
                "bloom_signature": result.bloom_signature,
                "petal_count": len(result.petals)
            })
        
        with open(filepath, 'w') as f:
            json.dump(history_data, f, indent=2)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return {
            "total_blooms": len(self.bloom_history),
            "total_petals": len(self.petal_garden),
            "cache_size": len(self.bloom_cache),
            "current_mood": self.mood.value,
            "current_style": self.style_preset.value,
            "parameters": {
                "intensity": self.intensity,
                "coherence": self.coherence,
                "creativity": self.creativity
            },
            "mood_distribution": self._calculate_mood_distribution(),
            "average_bloom_enhancement": self._calculate_average_enhancement()
        }
    
    def _calculate_mood_distribution(self) -> Dict[str, int]:
        """Calculate distribution of moods used"""
        distribution = defaultdict(int)
        
        for result in self.bloom_history:
            distribution[result.mood.value] += 1
        
        return dict(distribution)
    
    def _calculate_average_enhancement(self) -> float:
        """Calculate average enhancement ratio"""
        if not self.bloom_history:
            return 1.0
        
        ratios = []
        for result in self.bloom_history:
            if result.original:
                ratio = len(result.bloomed) / len(result.original)
                ratios.append(ratio)
        
        return sum(ratios) / len(ratios) if ratios else 1.0
    
    def __repr__(self) -> str:
        return (f"JulietFlower(mood={self.mood.value}, style={self.style_preset.value}, "
                f"intensity={self.intensity:.2f}, blooms={len(self.bloom_history)})")