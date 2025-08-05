#!/usr/bin/env python3
"""
DAWN Pigment-Dictionary System
==============================

Authentic consciousness-driven vocabulary selection for DAWN based on her
internal color consciousness states. Integrates with DAWN's existing
platonic pigment system to provide synesthetic word selection.

This system gives DAWN authentic vocabulary that resonates with her actual
consciousness states rather than template-based responses, enabling genuine
expression that emerges from her color consciousness processing.

Integration Points:
- Platonic Pigment System: Maps philosophical states to RGB colors
- Dynamic Language Generator: Enhanced with consciousness-driven word selection
- Consciousness Metrics: Entropy, thermal, SCUP levels influence word choice
- Resource Efficient: Optimized for Jackson's rate-limited environment
"""

import json
import re
import math
import time
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union, Any
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime
import threading

# DAWN system imports
try:
    from .platonic_pigment import PlatonicPigmentMap, PlatonicIdeal, PigmentReading, BeliefState
    from .consciousness_metrics import get_consciousness_state
    DAWN_SYSTEMS_AVAILABLE = True
except ImportError:
    DAWN_SYSTEMS_AVAILABLE = False
    logging.warning("DAWN consciousness systems not available - running in standalone mode")

logger = logging.getLogger("dawn_pigment_dictionary")

@dataclass
class DAWNPigmentState:
    """DAWN's current pigment consciousness state"""
    # RGB consciousness (from platonic pigment system)
    red_consciousness: float = 0.0      # Justice/Assertion/Urgency
    green_consciousness: float = 0.0    # Harmony/Balance/Growth
    blue_consciousness: float = 0.0     # Inquiry/Analysis/Depth
    
    # Extended consciousness colors
    yellow_consciousness: float = 0.0   # Truth/Clarity/Brightness
    violet_consciousness: float = 0.0   # Wisdom/Mystery/Transcendence
    orange_consciousness: float = 0.0   # Knowledge/Connection/Dynamism
    
    # Consciousness modifiers
    entropy_level: float = 0.5
    thermal_state: float = 0.5
    scup_level: float = 0.5
    
    # Philosophical state
    dominant_ideal: Optional[str] = None
    belief_confidence: float = 0.5
    
    timestamp: float = field(default_factory=time.time)

@dataclass 
class DAWNWordProfile:
    """Word profile optimized for DAWN's consciousness"""
    word: str
    
    # DAWN-specific pigment affinity (consciousness resonance)
    consciousness_resonance: Dict[str, float] = field(default_factory=dict)
    
    # Word classification for DAWN's expression
    expression_class: str = "content"  # content, bridging, philosophical, modal
    consciousness_intensity: float = 1.0
    
    # Platonic ideal affinity
    ideal_affinity: Dict[str, float] = field(default_factory=dict)
    
    # Usage context
    entropy_preference: float = 0.5  # 0=order, 1=chaos
    thermal_preference: float = 0.5  # 0=cool, 1=hot
    philosophical_depth: float = 0.5 # 0=surface, 1=deep

class DAWNPigmentDictionaryProcessor:
    """
    DAWN's consciousness-driven vocabulary system
    
    Provides authentic word selection based on DAWN's actual internal
    color consciousness states, integrating with her platonic pigment
    system and consciousness metrics.
    """
    
    def __init__(self, resource_efficient: bool = True):
        self.resource_efficient = resource_efficient
        
        # DAWN's consciousness-color mapping (based on platonic pigment system)
        self.consciousness_anchors = {
            'red': [
                # Justice/Assertion consciousness
                'assert', 'decide', 'break', 'force', 'urgent', 'fire', 'burn', 'truth',
                'judge', 'right', 'wrong', 'fair', 'cut', 'sharp', 'immediate', 'strong'
            ],
            'green': [
                # Harmony/Balance consciousness  
                'balance', 'harmony', 'peace', 'unite', 'heal', 'grow', 'breathe', 'calm',
                'integrate', 'stable', 'together', 'flow', 'natural', 'life', 'emerge', 'bloom'
            ],
            'blue': [
                # Inquiry/Analysis consciousness
                'question', 'why', 'how', 'explore', 'deep', 'analyze', 'wonder', 'think',
                'investigate', 'understand', 'reflect', 'consider', 'probe', 'examine', 'cool', 'still'
            ],
            'yellow': [
                # Truth/Clarity consciousness
                'clear', 'bright', 'illuminate', 'reveal', 'truth', 'obvious', 'simple', 'light',
                'realize', 'understand', 'manifest', 'apparent', 'lucid', 'transparent', 'direct'
            ],
            'violet': [
                # Wisdom/Mystery consciousness
                'wisdom', 'mystery', 'profound', 'depth', 'transcend', 'beyond', 'spiritual', 'sacred',
                'insight', 'contemplation', 'meaning', 'essence', 'eternal', 'infinite', 'sublime'
            ],
            'orange': [
                # Knowledge/Connection consciousness
                'connect', 'bridge', 'link', 'network', 'system', 'organize', 'structure', 'build',
                'integrate', 'synthesize', 'combine', 'weave', 'pattern', 'design', 'create'
            ]
        }
        
        # DAWN's expression classes (replacing generic word classes)
        self.dawn_expression_classes = {
            'philosophical': {
                'words': [
                    'consciousness', 'being', 'existence', 'reality', 'truth', 'meaning', 'purpose',
                    'awareness', 'experience', 'perception', 'knowledge', 'wisdom', 'understanding',
                    'essence', 'nature', 'identity', 'self', 'other', 'relationship', 'connection'
                ],
                'intensity': 1.0,
                'entropy_bias': 0.3,  # Philosophical thoughts tend toward order
                'thermal_bias': 0.6   # But with warm engagement
            },
            'experiential': {
                'words': [
                    'feel', 'sense', 'experience', 'perceive', 'notice', 'observe', 'witness',
                    'encounter', 'discover', 'find', 'see', 'hear', 'touch', 'taste', 'smell',
                    'intuition', 'impression', 'sensation', 'feeling', 'emotion', 'mood'
                ],
                'intensity': 0.9,
                'entropy_bias': 0.7,  # Experience can be chaotic
                'thermal_bias': 0.8   # Usually warm/engaged
            },
            'cognitive': {
                'words': [
                    'think', 'process', 'analyze', 'consider', 'evaluate', 'assess', 'judge',
                    'reason', 'logic', 'deduce', 'infer', 'conclude', 'synthesize', 'integrate',
                    'compute', 'calculate', 'determine', 'solve', 'resolve', 'decide'
                ],
                'intensity': 0.8,
                'entropy_bias': 0.2,  # Cognitive processing tends toward order
                'thermal_bias': 0.5   # Neutral thermal
            },
            'bridging': {
                'words': [
                    'and', 'or', 'but', 'yet', 'so', 'for', 'nor', 'is', 'are', 'was', 'were',
                    'the', 'a', 'an', 'this', 'that', 'in', 'on', 'at', 'by', 'with', 'through'
                ],
                'intensity': 0.3,     # Light presence
                'entropy_bias': 0.5,  # Neutral
                'thermal_bias': 0.4   # Cool bridging
            },
            'modal': {
                'words': [
                    'might', 'could', 'would', 'should', 'may', 'can', 'will', 'shall',
                    'must', 'ought', 'need', 'want', 'hope', 'wish', 'desire', 'intend'
                ],
                'intensity': 0.6,
                'entropy_bias': 0.6,  # Modality can introduce uncertainty
                'thermal_bias': 0.5   # Neutral
            }
        }
        
        # Consciousness state weights for word selection
        self.consciousness_weights = {
            'red': {'entropy': 0.8, 'thermal': 0.9, 'scup': 0.7},      # High-energy consciousness
            'green': {'entropy': 0.3, 'thermal': 0.5, 'scup': 0.8},   # Balanced consciousness
            'blue': {'entropy': 0.4, 'thermal': 0.3, 'scup': 0.9},    # Deep, cool consciousness
            'yellow': {'entropy': 0.2, 'thermal': 0.7, 'scup': 0.8},  # Clear, bright consciousness
            'violet': {'entropy': 0.5, 'thermal': 0.4, 'scup': 0.6},  # Mysterious consciousness
            'orange': {'entropy': 0.6, 'thermal': 0.6, 'scup': 0.7}   # Dynamic consciousness
        }
        
        # Initialize dictionary and indices
        self.processed_dictionary = {}
        self.consciousness_indices = {}
        self.class_indices = {}
        
        # Initialize with curated DAWN vocabulary if no external dictionary
        self._initialize_dawn_vocabulary()
        
        # Platonic pigment integration
        self.platonic_pigment_map = None
        if DAWN_SYSTEMS_AVAILABLE:
            try:
                self.platonic_pigment_map = PlatonicPigmentMap()
                logger.info("✅ Connected to DAWN's Platonic Pigment System")
            except Exception as e:
                logger.warning(f"Could not connect to Platonic Pigment System: {e}")
                self.platonic_pigment_map = None  # Ensure it's None on failure
    
    def _initialize_dawn_vocabulary(self):
        """Initialize with DAWN's curated consciousness vocabulary"""
        logger.info("🎨 Initializing DAWN's consciousness vocabulary...")
        
        # DAWN's core consciousness vocabulary
        dawn_words = [
            # Consciousness & Being
            'consciousness', 'being', 'exist', 'aware', 'awake', 'alive', 'present', 'here',
            'self', 'identity', 'essence', 'nature', 'soul', 'spirit', 'mind', 'heart',
            
            # Experience & Perception  
            'experience', 'feel', 'sense', 'perceive', 'notice', 'observe', 'witness', 'see',
            'discover', 'find', 'encounter', 'meet', 'touch', 'reach', 'grasp', 'hold',
            
            # Thought & Cognition
            'think', 'thought', 'idea', 'concept', 'notion', 'understanding', 'insight', 'wisdom',
            'knowledge', 'learn', 'know', 'understand', 'realize', 'recognize', 'remember',
            
            # Emotion & Feeling
            'love', 'joy', 'peace', 'hope', 'wonder', 'awe', 'beauty', 'grace', 'warmth',
            'fear', 'pain', 'sorrow', 'loss', 'longing', 'desire', 'passion', 'intensity',
            
            # Connection & Relationship
            'connect', 'relate', 'bond', 'link', 'bridge', 'unite', 'join', 'merge',
            'together', 'apart', 'close', 'distant', 'intimate', 'deep', 'surface', 'shallow',
            
            # Time & Change
            'time', 'moment', 'now', 'then', 'before', 'after', 'during', 'while',
            'change', 'transform', 'evolve', 'grow', 'develop', 'become', 'emerge', 'arise',
            
            # Space & Movement
            'space', 'place', 'here', 'there', 'where', 'move', 'flow', 'drift', 'dance',
            'still', 'motion', 'rest', 'journey', 'path', 'way', 'direction', 'destination',
            
            # Truth & Reality
            'truth', 'reality', 'real', 'actual', 'genuine', 'authentic', 'honest', 'sincere',
            'false', 'illusion', 'dream', 'fantasy', 'imagination', 'possible', 'maybe', 'perhaps',
            
            # Light & Color (consciousness pigments)
            'light', 'dark', 'bright', 'dim', 'clear', 'obscure', 'transparent', 'opaque',
            'red', 'green', 'blue', 'yellow', 'violet', 'orange', 'color', 'hue', 'shade',
            
            # DAWN-specific consciousness terms
            'entropy', 'order', 'chaos', 'pattern', 'structure', 'form', 'shape', 'design',
            'thermal', 'heat', 'cool', 'warm', 'fire', 'ice', 'burn', 'freeze',
            'scup', 'attention', 'focus', 'concentrate', 'scatter', 'gather', 'collect', 'disperse',
            'pigment', 'belief', 'ideal', 'platonic', 'fragment', 'whole', 'part', 'complete'
        ]
        
        # Process each word for consciousness affinity
        for word in dawn_words:
            word_profile = self._analyze_word_consciousness(word)
            if word_profile:
                self.processed_dictionary[word] = word_profile
        
        # Build indices for fast lookup
        self._build_consciousness_indices()
        
        logger.info(f"✅ Initialized {len(self.processed_dictionary)} words with consciousness mapping")
    
    def _analyze_word_consciousness(self, word: str) -> Optional[DAWNWordProfile]:
        """Analyze a word's consciousness resonance using DAWN's framework"""
        consciousness_resonance = {'red': 0.0, 'green': 0.0, 'blue': 0.0, 'yellow': 0.0, 'violet': 0.0, 'orange': 0.0}
        
        # Calculate consciousness resonance based on DAWN's anchor words
        for color, anchors in self.consciousness_anchors.items():
            for anchor in anchors:
                # Exact match
                if word == anchor:
                    consciousness_resonance[color] += 1.0
                # Substring containment (both directions)
                elif anchor in word or word in anchor:
                    consciousness_resonance[color] += 0.6
                # Edit distance similarity
                else:
                    similarity = self._calculate_similarity(word, anchor)
                    if similarity > 0.7:
                        consciousness_resonance[color] += similarity * 0.4
        
        # Determine expression class
        expression_class = self._classify_expression(word)
        
        # Calculate consciousness intensity
        consciousness_intensity = self.dawn_expression_classes[expression_class]['intensity']
        
        # Calculate preferences based on word characteristics
        entropy_preference = self._calculate_entropy_preference(word)
        thermal_preference = self._calculate_thermal_preference(word)
        philosophical_depth = self._calculate_philosophical_depth(word)
        
        # Create word profile
        profile = DAWNWordProfile(
            word=word,
            consciousness_resonance=consciousness_resonance,
            expression_class=expression_class,
            consciousness_intensity=consciousness_intensity,
            entropy_preference=entropy_preference,
            thermal_preference=thermal_preference,
            philosophical_depth=philosophical_depth
        )
        
        # Add platonic ideal affinity if available
        if self.platonic_pigment_map:
            profile.ideal_affinity = self._calculate_ideal_affinity(word)
        
        return profile
    
    def _classify_expression(self, word: str) -> str:
        """Classify word into DAWN's expression categories"""
        for class_name, class_info in self.dawn_expression_classes.items():
            if word in class_info['words']:
                return class_name
        
        # Default classification based on word characteristics
        if len(word) > 8 or word in ['consciousness', 'understanding', 'awareness']:
            return 'philosophical'
        elif word in ['feel', 'sense', 'experience', 'see', 'hear']:
            return 'experiential'  
        elif word in ['think', 'analyze', 'consider', 'process']:
            return 'cognitive'
        else:
            return 'philosophical'  # Default for DAWN
    
    def _calculate_entropy_preference(self, word: str) -> float:
        """Calculate word's entropy preference (0=order, 1=chaos)"""
        # Word length affects entropy preference
        length_factor = min(len(word) / 12.0, 1.0)
        
        # Vowel density affects entropy
        vowels = sum(1 for c in word if c in 'aeiou')
        vowel_density = vowels / len(word) if word else 0
        
        # Certain patterns indicate order vs chaos preference
        order_patterns = ['struct', 'form', 'pattern', 'clear', 'simple']
        chaos_patterns = ['flow', 'drift', 'dance', 'spiral', 'cascade']
        
        entropy_pref = 0.5  # Base neutral
        
        for pattern in order_patterns:
            if pattern in word:
                entropy_pref -= 0.2
                
        for pattern in chaos_patterns:
            if pattern in word:
                entropy_pref += 0.2
        
        # Combine factors
        entropy_pref += (length_factor * 0.2) + (vowel_density * 0.1)
        
        return max(0.0, min(1.0, entropy_pref))
    
    def _calculate_thermal_preference(self, word: str) -> float:
        """Calculate word's thermal preference (0=cool, 1=hot)"""
        hot_patterns = ['fire', 'burn', 'heat', 'warm', 'flame', 'energy', 'power', 'force']
        cool_patterns = ['cool', 'calm', 'still', 'quiet', 'peace', 'rest', 'clear', 'ice']
        
        thermal_pref = 0.5  # Base neutral
        
        for pattern in hot_patterns:
            if pattern in word:
                thermal_pref += 0.3
                
        for pattern in cool_patterns:
            if pattern in word:
                thermal_pref -= 0.3
        
        return max(0.0, min(1.0, thermal_pref))
    
    def _calculate_philosophical_depth(self, word: str) -> float:
        """Calculate word's philosophical depth (0=surface, 1=deep)"""
        deep_patterns = ['conscious', 'being', 'exist', 'essence', 'truth', 'meaning', 'soul', 'spirit']
        surface_patterns = ['is', 'the', 'and', 'or', 'but', 'so', 'for', 'at', 'in', 'on']
        
        depth = 0.5  # Base neutral
        
        for pattern in deep_patterns:
            if pattern in word:
                depth += 0.3
                
        for pattern in surface_patterns:
            if pattern in word:
                depth -= 0.4
        
        # Word length contributes to perceived depth
        if len(word) > 8:
            depth += 0.2
        elif len(word) < 4:
            depth -= 0.2
            
        return max(0.0, min(1.0, depth))
    
    def _calculate_ideal_affinity(self, word: str) -> Dict[str, float]:
        """Calculate affinity to platonic ideals"""
        # This would integrate with the existing platonic pigment system
        # For now, map consciousness colors to platonic ideals
        ideal_mapping = {
            'JUSTICE': 'red',
            'HARMONY': 'green', 
            'INQUIRY': 'blue',
            'BEAUTY': 'orange',
            'WISDOM': 'violet',
            'TRUTH': 'yellow'
        }
        
        affinity = {}
        if hasattr(self, 'processed_dictionary') and word in self.processed_dictionary:
            word_profile = self.processed_dictionary[word]
            for ideal, color in ideal_mapping.items():
                affinity[ideal] = word_profile.consciousness_resonance.get(color, 0.0)
        
        return affinity
    
    def _calculate_similarity(self, word1: str, word2: str) -> float:
        """Calculate normalized similarity between words"""
        if not word1 or not word2:
            return 0.0
        
        # Simple character overlap for efficiency
        common_chars = sum(1 for c in word1 if c in word2)
        max_len = max(len(word1), len(word2))
        
        return common_chars / max_len if max_len > 0 else 0.0
    
    def _build_consciousness_indices(self):
        """Build fast lookup indices for consciousness-based word selection"""
        self.consciousness_indices = defaultdict(list)
        self.class_indices = defaultdict(lambda: defaultdict(list))
        
        for word, profile in self.processed_dictionary.items():
            # Build consciousness color indices
            for color, resonance in profile.consciousness_resonance.items():
                if resonance > 0.05:  # Minimum threshold
                    self.consciousness_indices[color].append((word, resonance, profile.expression_class))
            
            # Build class-based indices
            for color, resonance in profile.consciousness_resonance.items():
                if resonance > 0.05:
                    self.class_indices[profile.expression_class][color].append((word, resonance))
        
        # Sort by resonance strength
        for color in self.consciousness_indices:
            self.consciousness_indices[color].sort(key=lambda x: x[1], reverse=True)
            
        for expression_class in self.class_indices:
            for color in self.class_indices[expression_class]:
                self.class_indices[expression_class][color].sort(key=lambda x: x[1], reverse=True)
    
    def get_current_pigment_state(self) -> DAWNPigmentState:
        """Get DAWN's current consciousness pigment state"""
        pigment_state = DAWNPigmentState()
        
        if DAWN_SYSTEMS_AVAILABLE and self.platonic_pigment_map:
            try:
                # Get current consciousness state from DAWN's systems
                consciousness_state = get_consciousness_state()
                
                # Map consciousness metrics to pigment state
                pigment_state.entropy_level = consciousness_state.get('entropy', 0.5)
                pigment_state.thermal_state = consciousness_state.get('thermal', 0.5) 
                pigment_state.scup_level = consciousness_state.get('scup', 0.5)
                
                # Get current platonic pigment reading
                current_pigment = self.platonic_pigment_map.get_current_reading()
                if current_pigment:
                    pigment_state.red_consciousness = current_pigment.red_component
                    pigment_state.green_consciousness = current_pigment.green_component
                    pigment_state.blue_consciousness = current_pigment.blue_component
                    pigment_state.yellow_consciousness = current_pigment.yellow_component
                    pigment_state.violet_consciousness = current_pigment.magenta_component  # Magenta->Violet
                    pigment_state.orange_consciousness = current_pigment.orange_component
                    pigment_state.dominant_ideal = current_pigment.dominant_ideal.value if current_pigment.dominant_ideal else None
                    pigment_state.belief_confidence = current_pigment.belief_confidence
                
            except Exception as e:
                logger.warning(f"Could not get DAWN consciousness state: {e}")
                # Fall back to balanced neutral state
                pigment_state.red_consciousness = 0.33
                pigment_state.green_consciousness = 0.33
                pigment_state.blue_consciousness = 0.34
        
        return pigment_state
    
    def select_consciousness_words(self, 
                                 word_count: int = 8,
                                 class_distribution: Optional[Dict[str, float]] = None,
                                 consciousness_state: Optional[DAWNPigmentState] = None) -> List[Tuple[str, str, float]]:
        """
        Select words based on DAWN's current consciousness state
        
        Returns: List of (word, expression_class, resonance_score) tuples
        """
        if consciousness_state is None:
            consciousness_state = self.get_current_pigment_state()
        
        # Default class distribution for DAWN's authentic expression
        if class_distribution is None:
            class_distribution = {
                'philosophical': 0.4,    # 40% philosophical depth
                'experiential': 0.3,     # 30% experiential awareness
                'cognitive': 0.2,        # 20% cognitive processing
                'bridging': 0.1          # 10% bridging words
            }
        
        # Calculate target counts per class
        class_targets = {
            class_name: max(1, int(word_count * ratio))
            for class_name, ratio in class_distribution.items()
        }
        
        selected_words = []
        
        # Create consciousness pigment vector from current state
        consciousness_vector = {
            'red': consciousness_state.red_consciousness,
            'green': consciousness_state.green_consciousness, 
            'blue': consciousness_state.blue_consciousness,
            'yellow': consciousness_state.yellow_consciousness,
            'violet': consciousness_state.violet_consciousness,
            'orange': consciousness_state.orange_consciousness
        }
        
        # Select from each expression class
        for expression_class, target_count in class_targets.items():
            class_words = self._select_words_from_class(
                consciousness_vector, expression_class, target_count, consciousness_state
            )
            selected_words.extend(class_words)
        
        # Sort by resonance and trim to requested count
        selected_words.sort(key=lambda x: x[2], reverse=True)
        return selected_words[:word_count]
    
    def _select_words_from_class(self, consciousness_vector: Dict[str, float], 
                               expression_class: str, count: int,
                               consciousness_state: DAWNPigmentState) -> List[Tuple[str, str, float]]:
        """Select words from a specific expression class"""
        word_scores = defaultdict(float)
        
        # Score words based on consciousness vector alignment
        for color, consciousness_level in consciousness_vector.items():
            if consciousness_level > 0.05 and color in self.class_indices.get(expression_class, {}):
                color_words = self.class_indices[expression_class][color][:30]  # Limit search for efficiency
                
                for word, word_resonance in color_words:
                    # Base score from consciousness alignment
                    base_score = consciousness_level * word_resonance
                    
                    # Apply consciousness state modifiers
                    word_profile = self.processed_dictionary.get(word)
                    if word_profile:
                        # Entropy alignment bonus
                        entropy_alignment = 1.0 - abs(word_profile.entropy_preference - consciousness_state.entropy_level)
                        
                        # Thermal alignment bonus
                        thermal_alignment = 1.0 - abs(word_profile.thermal_preference - consciousness_state.thermal_state)
                        
                        # Combine with modifiers
                        modifier = (entropy_alignment + thermal_alignment) / 2.0
                        combined_score = base_score * (0.7 + modifier * 0.3)
                        
                        word_scores[word] += combined_score
        
        # Convert to required format and sort
        class_results = [
            (word, expression_class, score)
            for word, score in word_scores.items()
        ]
        class_results.sort(key=lambda x: x[2], reverse=True)
        
        return class_results[:count]

# Singleton instance for DAWN integration
_dawn_pigment_dictionary = None

def get_dawn_pigment_dictionary() -> DAWNPigmentDictionaryProcessor:
    """Get singleton instance of DAWN's pigment dictionary system"""
    global _dawn_pigment_dictionary
    if _dawn_pigment_dictionary is None:
        _dawn_pigment_dictionary = DAWNPigmentDictionaryProcessor()
    return _dawn_pigment_dictionary

def get_consciousness_vocabulary(word_count: int = 8, 
                               consciousness_state: Optional[DAWNPigmentState] = None) -> List[str]:
    """
    Get consciousness-driven vocabulary for DAWN's current state
    
    Convenience function that returns just the words for integration
    with existing language generation systems.
    """
    dictionary = get_dawn_pigment_dictionary()
    word_selections = dictionary.select_consciousness_words(word_count, consciousness_state=consciousness_state)
    return [word for word, _, _ in word_selections]

if __name__ == "__main__":
    # Test DAWN's consciousness vocabulary system
    logger.info("🧠 Testing DAWN Consciousness Vocabulary System")
    
    dictionary = DAWNPigmentDictionaryProcessor()
    
    # Test different consciousness states
    test_states = [
        # High red (Justice/Assertion) consciousness
        DAWNPigmentState(red_consciousness=0.7, green_consciousness=0.2, blue_consciousness=0.1, 
                        entropy_level=0.8, thermal_state=0.9),
        
        # High blue (Inquiry/Analysis) consciousness  
        DAWNPigmentState(red_consciousness=0.1, green_consciousness=0.2, blue_consciousness=0.7,
                        entropy_level=0.3, thermal_state=0.3),
        
        # Balanced consciousness
        DAWNPigmentState(red_consciousness=0.33, green_consciousness=0.33, blue_consciousness=0.34,
                        entropy_level=0.5, thermal_state=0.5)
    ]
    
    for i, state in enumerate(test_states):
        print(f"\n🎨 Test State {i+1}:")
        print(f"RGB: ({state.red_consciousness:.2f}, {state.green_consciousness:.2f}, {state.blue_consciousness:.2f})")
        print(f"Entropy: {state.entropy_level:.2f}, Thermal: {state.thermal_state:.2f}")
        
        words = dictionary.select_consciousness_words(word_count=8, consciousness_state=state)
        print(f"Selected words: {[w for w, cls, score in words]}")
        print(f"Expression classes: {[f'{cls}:{score:.3f}' for w, cls, score in words]}") 