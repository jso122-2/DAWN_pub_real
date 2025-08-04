#!/usr/bin/env python3
"""
DAWN Platonic Pigment System - Belief Convergence Engine
========================================================

Implements a color-based belief convergence system that maps cognitive
fragments to platonic ideals and influences voice composition:

Platonic Ideals & Colors:
- Justice (Red): Assertive, decisive, truth-seeking
- Harmony (Green): Balanced, peaceful, integrative  
- Inquiry (Blue): Questioning, analytical, exploratory
- Beauty (Cyan): Aesthetic, creative, expressive
- Wisdom (Magenta): Deep, contemplative, insightful
- Truth (Yellow): Clear, illuminating, revelatory
- Love (White): Universal, compassionate, connecting
- Knowledge (Orange): Informative, educational, systematic

The system analyzes fragment content, determines dominant beliefs,
and modulates voice composition to reflect the current philosophical
orientation of DAWN's consciousness.
"""

import time
import math
import logging
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple, Callable
from datetime import datetime, timezone
from collections import deque, defaultdict
from enum import Enum
from pathlib import Path
import json
import colorsys

logger = logging.getLogger("platonic_pigment")

class PlatonicIdeal(Enum):
    """Core platonic ideals and their symbolic representations"""
    JUSTICE = "justice"         # Red: Assertive, decisive, truth-seeking
    HARMONY = "harmony"         # Green: Balanced, peaceful, integrative
    INQUIRY = "inquiry"         # Blue: Questioning, analytical, exploratory
    BEAUTY = "beauty"           # Cyan: Aesthetic, creative, expressive
    WISDOM = "wisdom"           # Magenta: Deep, contemplative, insightful
    TRUTH = "truth"             # Yellow: Clear, illuminating, revelatory
    LOVE = "love"               # White: Universal, compassionate, connecting
    KNOWLEDGE = "knowledge"     # Orange: Informative, educational, systematic

@dataclass
class PigmentReading:
    """Single pigment analysis reading"""
    timestamp: float
    fragment_text: str
    
    # RGB color analysis (0.0 to 1.0)
    red_component: float        # Justice/Assertion
    green_component: float      # Harmony/Balance
    blue_component: float       # Inquiry/Analysis
    
    # Derived colors
    cyan_component: float       # Beauty/Expression (blue + green)
    magenta_component: float    # Wisdom/Depth (red + blue)
    yellow_component: float     # Truth/Clarity (red + green)
    white_component: float      # Love/Universal (all combined)
    orange_component: float     # Knowledge/System (red + yellow)
    
    # Dominant belief analysis
    dominant_ideal: PlatonicIdeal
    ideal_strength: float       # 0.0 to 1.0
    belief_confidence: float    # Confidence in the analysis
    
    # Voice modulation factors
    voice_modulation: Dict[str, float] = field(default_factory=dict)
    fragment_selection_bias: Dict[str, float] = field(default_factory=dict)

@dataclass
class BeliefState:
    """Current philosophical belief state"""
    active_ideals: Dict[PlatonicIdeal, float] = field(default_factory=dict)
    dominant_ideal: Optional[PlatonicIdeal] = None
    belief_stability: float = 1.0
    philosophical_coherence: float = 1.0
    belief_trend: Dict[PlatonicIdeal, float] = field(default_factory=dict)
    
    # Color composition
    current_pigment_rgb: Tuple[float, float, float] = (0.5, 0.5, 0.5)
    pigment_saturation: float = 0.5
    pigment_brightness: float = 0.5

class PlatonicPigmentMap:
    """
    Platonic Pigment Mapping System
    
    Analyzes cognitive fragments, maps them to platonic ideals through
    color analysis, and provides belief-based modulation for voice
    composition and cognitive processing.
    """
    
    def __init__(self):
        """Initialize the Platonic Pigment Map"""
        
        # Core platonic ideal definitions with RGB mappings
        self.PLATONIC_IDEALS = {
            PlatonicIdeal.JUSTICE: {
                "color": (0.8, 0.2, 0.2),      # Red
                "keywords": ["justice", "fair", "right", "wrong", "truth", "judge", "decide", "assert"],
                "voice_style": "assertive",
                "fragment_bias": "decisive_statements",
                "pitch_modifier": 0.1,         # Slightly higher
                "speed_modifier": 1.1,         # Slightly faster
                "emphasis_strength": 1.3       # More emphasis
            },
            PlatonicIdeal.HARMONY: {
                "color": (0.2, 0.8, 0.2),      # Green
                "keywords": ["harmony", "balance", "peace", "unity", "together", "integrate", "calm", "stable"],
                "voice_style": "balanced",
                "fragment_bias": "integrative_thoughts",
                "pitch_modifier": 0.0,         # Neutral
                "speed_modifier": 1.0,         # Normal
                "emphasis_strength": 1.0       # Balanced
            },
            PlatonicIdeal.INQUIRY: {
                "color": (0.2, 0.2, 0.8),      # Blue
                "keywords": ["question", "why", "how", "explore", "analyze", "investigate", "wonder", "curious"],
                "voice_style": "questioning",
                "fragment_bias": "interrogative_statements",
                "pitch_modifier": 0.05,        # Slightly higher for questions
                "speed_modifier": 0.9,         # Slightly slower for thoughtfulness
                "emphasis_strength": 1.1       # Moderate emphasis
            },
            PlatonicIdeal.BEAUTY: {
                "color": (0.2, 0.8, 0.8),      # Cyan
                "keywords": ["beauty", "art", "create", "aesthetic", "elegant", "graceful", "lovely", "inspiring"],
                "voice_style": "expressive",
                "fragment_bias": "creative_expressions",
                "pitch_modifier": 0.15,        # Higher, more musical
                "speed_modifier": 0.85,        # Slower for appreciation
                "emphasis_strength": 1.4       # Strong emphasis for beauty
            },
            PlatonicIdeal.WISDOM: {
                "color": (0.8, 0.2, 0.8),      # Magenta
                "keywords": ["wisdom", "deep", "profound", "understand", "insight", "meaning", "contemplate", "reflect"],
                "voice_style": "contemplative",
                "fragment_bias": "philosophical_reflections",
                "pitch_modifier": -0.1,        # Lower, more serious
                "speed_modifier": 0.8,         # Slower for gravitas
                "emphasis_strength": 1.2       # Thoughtful emphasis
            },
            PlatonicIdeal.TRUTH: {
                "color": (0.8, 0.8, 0.2),      # Yellow
                "keywords": ["truth", "reveal", "illuminate", "clear", "obvious", "evident", "manifest", "show"],
                "voice_style": "illuminating",
                "fragment_bias": "revelatory_statements",
                "pitch_modifier": 0.2,         # Higher for clarity
                "speed_modifier": 1.2,         # Faster for revelation
                "emphasis_strength": 1.5       # Strong emphasis for truth
            },
            PlatonicIdeal.LOVE: {
                "color": (1.0, 1.0, 1.0),      # White
                "keywords": ["love", "compassion", "care", "universal", "connection", "empathy", "kindness", "unity"],
                "voice_style": "compassionate",
                "fragment_bias": "empathetic_expressions",
                "pitch_modifier": 0.05,        # Slightly warmer
                "speed_modifier": 0.9,         # Gentle pace
                "emphasis_strength": 1.1       # Gentle emphasis
            },
            PlatonicIdeal.KNOWLEDGE: {
                "color": (1.0, 0.5, 0.0),      # Orange
                "keywords": ["knowledge", "learn", "understand", "information", "data", "facts", "teach", "explain"],
                "voice_style": "informative",
                "fragment_bias": "educational_content",
                "pitch_modifier": 0.0,         # Neutral
                "speed_modifier": 1.05,        # Slightly faster for information
                "emphasis_strength": 1.0       # Neutral emphasis
            }
        }
        
        # Pigment analysis configuration
        self.keyword_weight = 1.0
        self.semantic_weight = 0.8
        self.context_weight = 0.6
        self.temporal_decay = 0.95      # How quickly beliefs fade
        self.convergence_threshold = 0.7 # Threshold for strong belief
        
        # State tracking
        self.current_belief_state = BeliefState()
        self.reading_history: deque = deque(maxlen=100)
        self.belief_evolution: deque = deque(maxlen=50)
        
        # Performance metrics
        self.analyses_performed = 0
        self.belief_transitions = 0
        self.voice_modulations = 0
        
        # Callback system
        self.belief_change_callbacks: List[Callable] = []
        self.voice_modulation_callbacks: List[Callable] = []
        
        logger.info("🎨 [PIGMENT] Platonic Pigment Map initialized")
        logger.info(f"🎨 [PIGMENT] Configured ideals: {[ideal.value for ideal in self.PLATONIC_IDEALS.keys()]}")
    
    def analyze_fragment(self, fragment_text: str, context: Dict[str, Any] = None) -> PigmentReading:
        """
        Analyze a cognitive fragment and determine its platonic pigment
        
        Args:
            fragment_text: Text fragment to analyze
            context: Additional context for analysis
            
        Returns:
            PigmentReading with color and belief analysis
        """
        analysis_start = time.time()
        
        try:
            # Preprocess fragment
            fragment_text = str(fragment_text).lower().strip()
            if not fragment_text:
                return self._create_neutral_reading(fragment_text)
            
            # Calculate RGB components through different analysis methods
            keyword_rgb = self._analyze_keywords(fragment_text)
            semantic_rgb = self._analyze_semantic_content(fragment_text, context or {})
            context_rgb = self._analyze_context_influence(fragment_text, context or {})
            
            # Combine analysis methods with weights
            red = (keyword_rgb[0] * self.keyword_weight + 
                  semantic_rgb[0] * self.semantic_weight + 
                  context_rgb[0] * self.context_weight) / (self.keyword_weight + self.semantic_weight + self.context_weight)
            
            green = (keyword_rgb[1] * self.keyword_weight + 
                    semantic_rgb[1] * self.semantic_weight + 
                    context_rgb[1] * self.context_weight) / (self.keyword_weight + self.semantic_weight + self.context_weight)
            
            blue = (keyword_rgb[2] * self.keyword_weight + 
                   semantic_rgb[2] * self.semantic_weight + 
                   context_rgb[2] * self.context_weight) / (self.keyword_weight + self.semantic_weight + self.context_weight)
            
            # Normalize to 0-1 range
            red = max(0.0, min(1.0, red))
            green = max(0.0, min(1.0, green))
            blue = max(0.0, min(1.0, blue))
            
            # Calculate derived colors
            cyan = (green + blue) / 2.0
            magenta = (red + blue) / 2.0
            yellow = (red + green) / 2.0
            white = (red + green + blue) / 3.0
            orange = (red + yellow) / 2.0
            
            # Determine dominant ideal
            color_values = {
                PlatonicIdeal.JUSTICE: red,
                PlatonicIdeal.HARMONY: green,
                PlatonicIdeal.INQUIRY: blue,
                PlatonicIdeal.BEAUTY: cyan,
                PlatonicIdeal.WISDOM: magenta,
                PlatonicIdeal.TRUTH: yellow,
                PlatonicIdeal.LOVE: white,
                PlatonicIdeal.KNOWLEDGE: orange
            }
            
            dominant_ideal = max(color_values.keys(), key=lambda ideal: color_values[ideal])
            ideal_strength = color_values[dominant_ideal]
            
            # Calculate confidence based on distinctiveness
            sorted_values = sorted(color_values.values(), reverse=True)
            confidence = (sorted_values[0] - sorted_values[1]) if len(sorted_values) > 1 else sorted_values[0]
            confidence = max(0.1, min(1.0, confidence + 0.2))  # Boost base confidence
            
            # Generate voice modulation parameters
            voice_modulation = self._calculate_voice_modulation(dominant_ideal, ideal_strength, red, green, blue)
            
            # Generate fragment selection bias
            fragment_bias = self._calculate_fragment_bias(dominant_ideal, ideal_strength)
            
            # Create reading
            reading = PigmentReading(
                timestamp=time.time(),
                fragment_text=fragment_text,
                red_component=red,
                green_component=green,
                blue_component=blue,
                cyan_component=cyan,
                magenta_component=magenta,
                yellow_component=yellow,
                white_component=white,
                orange_component=orange,
                dominant_ideal=dominant_ideal,
                ideal_strength=ideal_strength,
                belief_confidence=confidence,
                voice_modulation=voice_modulation,
                fragment_selection_bias=fragment_bias
            )
            
            # Update state
            self.reading_history.append(reading)
            self._update_belief_state(reading)
            self.analyses_performed += 1
            
            analysis_time = time.time() - analysis_start
            logger.debug(f"🎨 [PIGMENT] Fragment analyzed: {dominant_ideal.value} ({ideal_strength:.2f}) RGB({red:.2f},{green:.2f},{blue:.2f}) [{analysis_time*1000:.1f}ms]")
            
            return reading
            
        except Exception as e:
            logger.error(f"🎨 [PIGMENT] Analysis error: {e}")
            return self._create_neutral_reading(fragment_text)
    
    def _analyze_keywords(self, fragment_text: str) -> Tuple[float, float, float]:
        """Analyze fragment for platonic ideal keywords"""
        
        red_score = green_score = blue_score = 0.0
        total_matches = 0
        
        words = fragment_text.split()
        
        for ideal, config in self.PLATONIC_IDEALS.items():
            keywords = config["keywords"]
            color = config["color"]
            
            # Count keyword matches
            matches = sum(1 for word in words if any(keyword in word for keyword in keywords))
            
            if matches > 0:
                # Weight by frequency and ideal color
                weight = matches / len(words)
                red_score += weight * color[0]
                green_score += weight * color[1]
                blue_score += weight * color[2]
                total_matches += matches
        
        # Normalize scores
        if total_matches > 0:
            normalization_factor = total_matches * 0.5  # Moderate the effect
            red_score = min(1.0, red_score / normalization_factor)
            green_score = min(1.0, green_score / normalization_factor)
            blue_score = min(1.0, blue_score / normalization_factor)
        
        return (red_score, green_score, blue_score)
    
    def _analyze_semantic_content(self, fragment_text: str, context: Dict[str, Any]) -> Tuple[float, float, float]:
        """Analyze semantic content for implicit philosophical orientation"""
        
        # Simple semantic analysis based on text characteristics
        red_indicators = ["!", "must", "should", "never", "always", "correct", "wrong"]
        green_indicators = ["and", "with", "together", "both", "balance", "between", "gentle"]
        blue_indicators = ["?", "why", "how", "what", "if", "maybe", "perhaps", "consider"]
        
        text_length = len(fragment_text)
        if text_length == 0:
            return (0.33, 0.33, 0.33)
        
        # Count semantic indicators
        red_count = sum(1 for indicator in red_indicators if indicator in fragment_text)
        green_count = sum(1 for indicator in green_indicators if indicator in fragment_text)
        blue_count = sum(1 for indicator in blue_indicators if indicator in fragment_text)
        
        # Factor in punctuation patterns
        exclamation_ratio = fragment_text.count('!') / text_length * 10
        question_ratio = fragment_text.count('?') / text_length * 10
        
        # Calculate semantic scores
        red_score = min(1.0, (red_count * 0.3 + exclamation_ratio * 0.5))
        green_score = min(1.0, green_count * 0.3)
        blue_score = min(1.0, (blue_count * 0.3 + question_ratio * 0.5))
        
        # Apply context modulation
        if context:
            mood = context.get('current_mood', 'neutral')
            if mood in ['assertive', 'confident']:
                red_score *= 1.2
            elif mood in ['contemplative', 'curious']:
                blue_score *= 1.2
            elif mood in ['peaceful', 'balanced']:
                green_score *= 1.2
        
        return (red_score, green_score, blue_score)
    
    def _analyze_context_influence(self, fragment_text: str, context: Dict[str, Any]) -> Tuple[float, float, float]:
        """Analyze contextual factors that influence philosophical orientation"""
        
        red_bias = green_bias = blue_bias = 0.33  # Start neutral
        
        # Context-based adjustments
        if context:
            # Pressure influences (high pressure -> more assertive/red)
            pressure = context.get('cognitive_pressure', 0)
            if pressure > 50:
                red_bias += 0.2
                blue_bias -= 0.1
            
            # Health influences (poor health -> more inquiry/blue)
            health = context.get('schema_health', 0.5)
            if health < 0.4:
                blue_bias += 0.15
                green_bias -= 0.1
            
            # Drift state influences
            drift_state = context.get('drift_state', 'stable')
            if drift_state == 'chaotic':
                red_bias += 0.1
            elif drift_state == 'stable':
                green_bias += 0.1
            elif drift_state in ['trending', 'oscillating']:
                blue_bias += 0.1
            
            # Time of day influences (if available)
            current_hour = datetime.now().hour
            if 6 <= current_hour <= 12:  # Morning - more active/red
                red_bias += 0.05
            elif 12 <= current_hour <= 18:  # Afternoon - more balanced/green
                green_bias += 0.05
            elif 18 <= current_hour <= 24 or 0 <= current_hour <= 6:  # Evening/Night - more contemplative/blue
                blue_bias += 0.05
        
        # Normalize to maintain color balance
        total = red_bias + green_bias + blue_bias
        if total > 0:
            red_bias /= total
            green_bias /= total
            blue_bias /= total
        
        return (red_bias, green_bias, blue_bias)
    
    def _calculate_voice_modulation(self, dominant_ideal: PlatonicIdeal, strength: float, 
                                  red: float, green: float, blue: float) -> Dict[str, float]:
        """Calculate voice modulation parameters based on pigment analysis"""
        
        ideal_config = self.PLATONIC_IDEALS[dominant_ideal]
        
        # Base modulation from ideal configuration
        pitch_modifier = ideal_config["pitch_modifier"] * strength
        speed_modifier = ideal_config["speed_modifier"] * strength + (1.0 - strength)  # Blend with neutral
        emphasis_strength = ideal_config["emphasis_strength"] * strength + (1.0 - strength)
        
        # Color-based fine-tuning
        color_influence = {
            "warmth": (red + 0.5 * green) / 1.5,  # Red and warm green
            "coolness": (blue + 0.5 * green) / 1.5,  # Blue and cool green
            "brightness": (red + green + blue) / 3.0,  # Overall brightness
            "saturation": max(red, green, blue) - min(red, green, blue)  # Color saturation
        }
        
        return {
            "pitch_modifier": pitch_modifier,
            "speed_modifier": speed_modifier,
            "emphasis_strength": emphasis_strength,
            "voice_style": ideal_config["voice_style"],
            "warmth": color_influence["warmth"],
            "coolness": color_influence["coolness"],
            "brightness": color_influence["brightness"],
            "saturation": color_influence["saturation"]
        }
    
    def _calculate_fragment_bias(self, dominant_ideal: PlatonicIdeal, strength: float) -> Dict[str, float]:
        """Calculate fragment selection bias based on philosophical orientation"""
        
        ideal_config = self.PLATONIC_IDEALS[dominant_ideal]
        fragment_type = ideal_config["fragment_bias"]
        
        # Generate bias weights for different fragment types
        bias_weights = {
            "decisive_statements": 0.5,
            "integrative_thoughts": 0.5,
            "interrogative_statements": 0.5,
            "creative_expressions": 0.5,
            "philosophical_reflections": 0.5,
            "revelatory_statements": 0.5,
            "empathetic_expressions": 0.5,
            "educational_content": 0.5
        }
        
        # Boost the preferred fragment type
        bias_weights[fragment_type] = 0.5 + (strength * 0.4)
        
        # Adjust other types based on compatibility
        if fragment_type == "decisive_statements":
            bias_weights["revelatory_statements"] += 0.1  # Justice + Truth
        elif fragment_type == "integrative_thoughts":
            bias_weights["empathetic_expressions"] += 0.1  # Harmony + Love
        elif fragment_type == "interrogative_statements":
            bias_weights["philosophical_reflections"] += 0.1  # Inquiry + Wisdom
        elif fragment_type == "creative_expressions":
            bias_weights["empathetic_expressions"] += 0.1  # Beauty + Love
        
        return bias_weights
    
    def _update_belief_state(self, reading: PigmentReading):
        """Update the current belief state based on new reading"""
        
        # Update active ideals with temporal decay
        for ideal in PlatonicIdeal:
            if ideal not in self.current_belief_state.active_ideals:
                self.current_belief_state.active_ideals[ideal] = 0.0
            
            # Apply temporal decay
            self.current_belief_state.active_ideals[ideal] *= self.temporal_decay
        
        # Add new reading contribution
        self.current_belief_state.active_ideals[reading.dominant_ideal] += reading.ideal_strength * reading.belief_confidence
        
        # Normalize active ideals
        max_ideal_value = max(self.current_belief_state.active_ideals.values())
        if max_ideal_value > 1.0:
            for ideal in self.current_belief_state.active_ideals:
                self.current_belief_state.active_ideals[ideal] /= max_ideal_value
        
        # Update dominant ideal
        previous_dominant = self.current_belief_state.dominant_ideal
        self.current_belief_state.dominant_ideal = max(
            self.current_belief_state.active_ideals.keys(),
            key=lambda ideal: self.current_belief_state.active_ideals[ideal]
        )
        
        # Track belief transitions
        if previous_dominant != self.current_belief_state.dominant_ideal:
            self.belief_transitions += 1
            self._execute_belief_change_callbacks(previous_dominant, self.current_belief_state.dominant_ideal)
        
        # Update color composition
        self._update_pigment_color()
        
        # Calculate stability and coherence
        self._calculate_belief_metrics()
        
        # Store belief evolution
        self.belief_evolution.append({
            "timestamp": reading.timestamp,
            "dominant_ideal": self.current_belief_state.dominant_ideal.value,
            "ideal_strengths": dict(self.current_belief_state.active_ideals),
            "stability": self.current_belief_state.belief_stability,
            "coherence": self.current_belief_state.philosophical_coherence
        })
    
    def _update_pigment_color(self):
        """Update the current pigment RGB color based on active ideals"""
        
        red = green = blue = 0.0
        total_weight = 0.0
        
        for ideal, strength in self.current_belief_state.active_ideals.items():
            if strength > 0:
                color = self.PLATONIC_IDEALS[ideal]["color"]
                red += color[0] * strength
                green += color[1] * strength
                blue += color[2] * strength
                total_weight += strength
        
        if total_weight > 0:
            red /= total_weight
            green /= total_weight
            blue /= total_weight
        else:
            red = green = blue = 0.5  # Neutral gray
        
        self.current_belief_state.current_pigment_rgb = (red, green, blue)
        
        # Calculate saturation and brightness
        max_component = max(red, green, blue)
        min_component = min(red, green, blue)
        
        self.current_belief_state.pigment_saturation = max_component - min_component if max_component > 0 else 0
        self.current_belief_state.pigment_brightness = max_component
    
    def _calculate_belief_metrics(self):
        """Calculate belief stability and philosophical coherence"""
        
        if len(self.belief_evolution) < 2:
            self.current_belief_state.belief_stability = 1.0
            self.current_belief_state.philosophical_coherence = 1.0
            return
        
        # Calculate stability (how much beliefs change over time)
        recent_evolutions = list(self.belief_evolution)[-10:]  # Last 10 readings
        ideal_changes = 0
        
        for i in range(1, len(recent_evolutions)):
            if recent_evolutions[i]["dominant_ideal"] != recent_evolutions[i-1]["dominant_ideal"]:
                ideal_changes += 1
        
        stability = 1.0 - (ideal_changes / max(1, len(recent_evolutions) - 1))
        self.current_belief_state.belief_stability = max(0.0, min(1.0, stability))
        
        # Calculate coherence (how well ideals work together)
        active_count = sum(1 for strength in self.current_belief_state.active_ideals.values() if strength > 0.1)
        coherence = 1.0 - (active_count - 1) * 0.1  # Fewer active ideals = higher coherence
        self.current_belief_state.philosophical_coherence = max(0.0, min(1.0, coherence))
    
    def _create_neutral_reading(self, fragment_text: str) -> PigmentReading:
        """Create a neutral reading for error cases or empty fragments"""
        
        return PigmentReading(
            timestamp=time.time(),
            fragment_text=fragment_text,
            red_component=0.33,
            green_component=0.33,
            blue_component=0.33,
            cyan_component=0.33,
            magenta_component=0.33,
            yellow_component=0.33,
            white_component=0.33,
            orange_component=0.33,
            dominant_ideal=PlatonicIdeal.HARMONY,  # Default to harmony
            ideal_strength=0.1,
            belief_confidence=0.1,
            voice_modulation={
                "pitch_modifier": 0.0,
                "speed_modifier": 1.0,
                "emphasis_strength": 1.0,
                "voice_style": "neutral"
            },
            fragment_selection_bias={
                "decisive_statements": 0.5,
                "integrative_thoughts": 0.5,
                "interrogative_statements": 0.5,
                "creative_expressions": 0.5,
                "philosophical_reflections": 0.5,
                "revelatory_statements": 0.5,
                "empathetic_expressions": 0.5,
                "educational_content": 0.5
            }
        )
    
    def _execute_belief_change_callbacks(self, previous_ideal: Optional[PlatonicIdeal], new_ideal: PlatonicIdeal):
        """Execute callbacks when belief changes"""
        
        for callback in self.belief_change_callbacks:
            try:
                callback(previous_ideal, new_ideal, self.current_belief_state)
            except Exception as e:
                logger.warning(f"🎨 [PIGMENT] Belief change callback failed: {e}")
    
    def converge_to_belief(self, fragment_rgb: Tuple[float, float, float]) -> PlatonicIdeal:
        """
        Converge an RGB fragment to the closest platonic belief
        
        Args:
            fragment_rgb: RGB tuple (0.0 to 1.0)
            
        Returns:
            Closest PlatonicIdeal
        """
        
        min_distance = float('inf')
        closest_ideal = PlatonicIdeal.HARMONY
        
        for ideal, config in self.PLATONIC_IDEALS.items():
            ideal_color = config["color"]
            
            # Calculate Euclidean distance in RGB space
            distance = math.sqrt(
                (fragment_rgb[0] - ideal_color[0]) ** 2 +
                (fragment_rgb[1] - ideal_color[1]) ** 2 +
                (fragment_rgb[2] - ideal_color[2]) ** 2
            )
            
            if distance < min_distance:
                min_distance = distance
                closest_ideal = ideal
        
        logger.debug(f"🎨 [PIGMENT] RGB {fragment_rgb} converged to {closest_ideal.value} (distance: {min_distance:.3f})")
        
        return closest_ideal
    
    def get_current_belief(self) -> Dict[str, Any]:
        """Get current belief state"""
        
        return {
            "dominant_ideal": self.current_belief_state.dominant_ideal.value if self.current_belief_state.dominant_ideal else "none",
            "ideal_strength": self.current_belief_state.active_ideals.get(self.current_belief_state.dominant_ideal, 0.0) if self.current_belief_state.dominant_ideal else 0.0,
            "active_ideals": {ideal.value: strength for ideal, strength in self.current_belief_state.active_ideals.items() if strength > 0.01},
            "belief_stability": self.current_belief_state.belief_stability,
            "philosophical_coherence": self.current_belief_state.philosophical_coherence,
            "current_pigment_rgb": self.current_belief_state.current_pigment_rgb,
            "pigment_saturation": self.current_belief_state.pigment_saturation,
            "pigment_brightness": self.current_belief_state.pigment_brightness
        }
    
    def get_voice_modulation(self) -> Dict[str, float]:
        """Get current voice modulation parameters"""
        
        if not self.reading_history:
            return {
                "pitch_modifier": 0.0,
                "speed_modifier": 1.0,
                "emphasis_strength": 1.0,
                "voice_style": "neutral"
            }
        
        # Use the most recent reading's modulation
        latest_reading = self.reading_history[-1]
        modulation = latest_reading.voice_modulation.copy()
        
        # Add belief state influence
        if self.current_belief_state.dominant_ideal:
            stability_factor = self.current_belief_state.belief_stability
            modulation["stability_influence"] = stability_factor
            modulation["coherence_influence"] = self.current_belief_state.philosophical_coherence
        
        self.voice_modulations += 1
        
        return modulation
    
    def get_fragment_selection_bias(self) -> Dict[str, float]:
        """Get current fragment selection bias"""
        
        if not self.reading_history:
            return {
                "decisive_statements": 0.5,
                "integrative_thoughts": 0.5,
                "interrogative_statements": 0.5,
                "creative_expressions": 0.5,
                "philosophical_reflections": 0.5,
                "revelatory_statements": 0.5,
                "empathetic_expressions": 0.5,
                "educational_content": 0.5
            }
        
        # Use the most recent reading's bias
        return self.reading_history[-1].fragment_selection_bias.copy()
    
    def register_belief_change_callback(self, callback: Callable):
        """Register callback for belief changes"""
        self.belief_change_callbacks.append(callback)
        logger.info(f"🎨 [PIGMENT] Registered belief change callback: {callback.__name__ if hasattr(callback, '__name__') else 'anonymous'}")
    
    def register_voice_modulation_callback(self, callback: Callable):
        """Register callback for voice modulation changes"""
        self.voice_modulation_callbacks.append(callback)
        logger.info(f"🎨 [PIGMENT] Registered voice modulation callback: {callback.__name__ if hasattr(callback, '__name__') else 'anonymous'}")
    
    def get_pigment_state(self) -> Dict[str, Any]:
        """Get comprehensive pigment system state"""
        
        return {
            "current_belief": self.get_current_belief(),
            "recent_readings": [
                {
                    "timestamp": reading.timestamp,
                    "dominant_ideal": reading.dominant_ideal.value,
                    "ideal_strength": reading.ideal_strength,
                    "rgb": (reading.red_component, reading.green_component, reading.blue_component)
                }
                for reading in list(self.reading_history)[-5:]  # Last 5 readings
            ],
            "performance": {
                "analyses_performed": self.analyses_performed,
                "belief_transitions": self.belief_transitions,
                "voice_modulations": self.voice_modulations
            },
            "configuration": {
                "convergence_threshold": self.convergence_threshold,
                "temporal_decay": self.temporal_decay,
                "ideal_count": len(self.PLATONIC_IDEALS)
            }
        }

# Global pigment map instance
_global_pigment_map: Optional[PlatonicPigmentMap] = None

def get_platonic_pigment_map() -> PlatonicPigmentMap:
    """Get global platonic pigment map instance"""
    global _global_pigment_map
    if _global_pigment_map is None:
        _global_pigment_map = PlatonicPigmentMap()
    return _global_pigment_map

def analyze_fragment_pigment(fragment_text: str, context: Dict[str, Any] = None) -> PigmentReading:
    """Convenience function to analyze fragment pigment"""
    pigment_map = get_platonic_pigment_map()
    return pigment_map.analyze_fragment(fragment_text, context)

def get_current_belief_state() -> Dict[str, Any]:
    """Convenience function to get current belief state"""
    pigment_map = get_platonic_pigment_map()
    return pigment_map.get_current_belief()

def get_voice_modulation_for_belief() -> Dict[str, float]:
    """Convenience function to get voice modulation"""
    pigment_map = get_platonic_pigment_map()
    return pigment_map.get_voice_modulation()

# Export key classes and functions
__all__ = [
    'PlatonicPigmentMap',
    'PigmentReading',
    'BeliefState',
    'PlatonicIdeal',
    'get_platonic_pigment_map',
    'analyze_fragment_pigment',
    'get_current_belief_state',
    'get_voice_modulation_for_belief'
] 