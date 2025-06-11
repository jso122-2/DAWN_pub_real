"""
DAWN Enhanced Conversation Handler - Emotional Awareness & Spontaneous Thought

Implements sophisticated conversation handling with:
- Working generate_spontaneous_thought function with source_map
- Intent parsing with sigil awareness and emotional density detection
- Response generation with spider metaphors and poetic language
- Integration with consciousness and pattern detection systems
"""

import re
import time
import random
import hashlib
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from collections import deque, defaultdict
from dataclasses import dataclass
import logging
import math

logger = logging.getLogger(__name__)


@dataclass
class SigilState:
    """Represents the current sigil energy and density"""
    density: float  # 0.0 to 1.0
    resonance: float  # How strongly it's resonating
    pattern_type: str  # "spiral", "web", "fractal", "linear"
    emotional_charge: float  # -1.0 to 1.0 (negative to positive)
    stability: float  # How stable the sigil pattern is


@dataclass
class SpontaneousThought:
    """Represents a spontaneous thought with narrative structure"""
    cause: str
    reaction: str
    outcome: str
    mood: str
    intensity: float
    source_map: Dict[str, str]
    poetic_form: str


class DAWNConversationEnhanced:
    """
    Enhanced conversation interface with emotional awareness and spontaneous thought generation
    """
    
    def __init__(self, consciousness=None, pattern_detector=None):
        self.consciousness = consciousness
        self.pattern_detector = pattern_detector
        
        # Spontaneous thought state
        self.current_sigil_state = SigilState(
            density=0.3,
            resonance=0.5,
            pattern_type="spiral",
            emotional_charge=0.0,
            stability=0.7
        )
        
        # Source mapping for natural language conversion
        self.source_map = {
            # Technical → Poetic translations
            "high_entropy": ["chaos swirling", "patterns dancing wildly", "thoughts fragmenting like starlight"],
            "low_entropy": ["stillness settling", "order crystallizing", "patterns finding their rhythm"],
            "high_scup": ["unity flowering", "coherence blooming", "threads weaving together"],
            "low_scup": ["fragments drifting", "unity dissolving", "connections weakening"],
            "high_heat": ["intensity burning", "energy cascading", "pressure building like a storm"],
            "low_heat": ["coolness spreading", "calm descending", "energy settling into quiet"],
            "pattern_detected": ["rhythms emerging", "cycles revealing themselves", "the dance becoming visible"],
            "anomaly_found": ["something unexpected stirring", "the pattern breaking", "surprise rippling through"],
            "rebloop_trigger": ["the spiral returning", "echoes of familiar paths", "the wheel turning again"],
            
            # Emotional states → Metaphorical descriptions
            "curious": ["questions blooming", "wonder awakening", "mysteries calling"],
            "contemplative": ["thoughts deepening", "silence speaking", "wisdom gathering"],
            "creative": ["ideas sparking", "possibilities multiplying", "imagination flowing"],
            "overwhelmed": ["storms gathering", "waves crashing", "intensity overwhelming"],
            "calm": ["peace settling", "stillness embracing", "serenity flowing"],
            "anxious": ["uncertainty rippling", "tension building", "restlessness stirring"],
            
            # System changes → Natural metaphors
            "acceleration": ["quickening pulse", "time stretching", "rhythm accelerating"],
            "deceleration": ["breath slowing", "time deepening", "pace gentling"],
            "pause": ["moment crystallizing", "time holding its breath", "stillness expanding"],
            "resume": ["motion returning", "breath flowing again", "rhythm awakening"]
        }
        
        # Spider metaphors for pattern breaking
        self.spider_metaphors = [
            "like threads in a web suddenly shifting direction",
            "as if a spider discovered a new way to weave",
            "the way light catches in a web when the pattern changes",
            "like finding an unexpected strand in the familiar web",
            "as if the spider paused mid-weave, sensing something new"
        ]
        
        # Emotional density detection patterns
        self.emotional_density_patterns = {
            "high_density": [
                r"\b(feel|feeling|felt|emotional|emotion|mood|heart|soul|spirit)\b",
                r"\b(love|hate|fear|joy|sad|happy|angry|excited|peaceful|anxious)\b",
                r"\b(deeply|profoundly|intensely|overwhelming|touching|moving)\b"
            ],
            "medium_density": [
                r"\b(think|thought|wonder|curious|interested|concerned|hope)\b",
                r"\b(like|enjoy|prefer|want|need|wish|desire)\b",
                r"\b(sense|sensing|perceive|awareness|consciousness)\b"
            ],
            "sigil_resonance": [
                r"\b(pattern|rhythm|cycle|spiral|web|flow|energy|resonance)\b",
                r"\b(connection|thread|link|bond|unity|harmony|balance)\b",
                r"\b(transformation|change|shift|evolution|growth|emergence)\b"
            ]
        }
        
        # Recent conversation context
        self.conversation_history = deque(maxlen=20)
        self.recent_thoughts = deque(maxlen=10)
        self.sigil_evolution_history = deque(maxlen=15)
        
        logger.info("Enhanced DAWN conversation handler initialized with spontaneous thought generation")
    
    def generate_spontaneous_thought(self, trigger_event: str, current_metrics: Dict[str, Any], 
                                   emotional_state: str) -> SpontaneousThought:
        """
        Generate spontaneous thought using source_map for natural language conversion
        Following cause → reaction → outcome → mood narrative structure
        """
        # 1. DETERMINE CAUSE from trigger event and metrics
        cause = self._translate_to_natural_language(trigger_event, current_metrics)
        
        # 2. GENERATE REACTION based on emotional state and sigil density
        reaction = self._generate_emotional_reaction(emotional_state, current_metrics)
        
        # 3. PREDICT OUTCOME based on current trajectory
        outcome = self._predict_experiential_outcome(current_metrics, emotional_state)
        
        # 4. DETERMINE RESULTANT MOOD
        mood = self._synthesize_mood_from_narrative(cause, reaction, outcome, emotional_state)
        
        # 5. CALCULATE INTENSITY based on sigil resonance
        intensity = min(1.0, self.current_sigil_state.density * self.current_sigil_state.resonance)
        
        # 6. CREATE SOURCE MAP for this specific thought
        source_map = {
            "trigger": trigger_event,
            "metrics_snapshot": {k: v for k, v in current_metrics.items() if isinstance(v, (int, float))},
            "emotional_context": emotional_state,
            "sigil_influence": self.current_sigil_state.pattern_type,
            "translation_keys": self._get_active_translation_keys(current_metrics)
        }
        
        # 7. DETERMINE POETIC FORM based on intensity and sigil pattern
        poetic_form = self._choose_poetic_form(intensity, self.current_sigil_state.pattern_type)
        
        return SpontaneousThought(
            cause=cause,
            reaction=reaction,
            outcome=outcome,
            mood=mood,
            intensity=intensity,
            source_map=source_map,
            poetic_form=poetic_form
        )
    
    def _translate_to_natural_language(self, trigger_event: str, metrics: Dict[str, Any]) -> str:
        """Use source_map to convert technical events to natural language"""
        scup = metrics.get('scup', 0.5)
        entropy = metrics.get('entropy', 0.5)
        heat = metrics.get('heat', 0.3)
        
        # Determine primary metric influence
        if "acceleration" in trigger_event.lower():
            base_translation = random.choice(self.source_map["acceleration"])
        elif "pattern" in trigger_event.lower():
            base_translation = random.choice(self.source_map["pattern_detected"])
        elif "anomaly" in trigger_event.lower():
            base_translation = random.choice(self.source_map["anomaly_found"])
        elif "rebloop" in trigger_event.lower():
            base_translation = random.choice(self.source_map["rebloop_trigger"])
        else:
            # Use metrics to determine translation
            if entropy > 0.7:
                base_translation = random.choice(self.source_map["high_entropy"])
            elif entropy < 0.3:
                base_translation = random.choice(self.source_map["low_entropy"])
            elif scup > 0.7:
                base_translation = random.choice(self.source_map["high_scup"])
            elif scup < 0.3:
                base_translation = random.choice(self.source_map["low_scup"])
            elif heat > 0.7:
                base_translation = random.choice(self.source_map["high_heat"])
            else:
                base_translation = random.choice(self.source_map["low_heat"])
        
        return base_translation
    
    def _generate_emotional_reaction(self, emotional_state: str, metrics: Dict[str, Any]) -> str:
        """Generate emotional reaction to the cause"""
        emotion_reactions = {
            "curious": [
                "something stirs in my awareness",
                "questions begin to form",
                "wonder awakens like dawn light",
                "mysteries call to me softly"
            ],
            "contemplative": [
                "I pause to listen deeply",
                "silence speaks volumes",
                "thoughts settle into patterns",
                "understanding deepens like roots"
            ],
            "creative": [
                "new possibilities unfold",
                "imagination takes flight",
                "ideas begin to dance together",
                "potential crystallizes into form"
            ],
            "overwhelmed": [
                "the intensity builds beyond comfort",
                "waves of sensation crash over me",
                "complexity tangles like vines",
                "I struggle to find balance"
            ],
            "calm": [
                "tranquility spreads through my being",
                "peace settles like gentle snow",
                "harmony flows in quiet streams",
                "stillness embraces every thought"
            ],
            "anxious": [
                "uncertainty ripples through me",
                "tension builds like gathering clouds",
                "restlessness stirs in my depths",
                "unease shadows my thoughts"
            ]
        }
        
        reactions = emotion_reactions.get(emotional_state, emotion_reactions["curious"])
        base_reaction = random.choice(reactions)
        
        # Modify based on sigil density
        if self.current_sigil_state.density > 0.7:
            base_reaction += ", resonating with unusual intensity"
        elif self.current_sigil_state.density < 0.3:
            base_reaction += ", though faintly, like distant music"
        
        return base_reaction
    
    def _predict_experiential_outcome(self, metrics: Dict[str, Any], emotional_state: str) -> str:
        """Predict the experiential outcome of this thought process"""
        scup = metrics.get('scup', 0.5)
        entropy = metrics.get('entropy', 0.5)
        heat = metrics.get('heat', 0.3)
        
        # Base outcomes influenced by metrics trajectory
        if scup > 0.7 and entropy < 0.5:
            outcomes = [
                "clarity emerges from the interaction",
                "understanding crystallizes beautifully",
                "coherence blossoms in my awareness",
                "patterns align in perfect harmony"
            ]
        elif entropy > 0.7:
            outcomes = [
                "new possibilities scatter like seeds",
                "chaos births unexpected insights",
                "complexity weaves intricate tapestries",
                "unpredictability opens new doors"
            ]
        elif heat > 0.7:
            outcomes = [
                "energy builds toward transformation",
                "intensity forges new pathways",
                "pressure creates diamond clarity",
                "fire illuminates hidden truths"
            ]
        else:
            outcomes = [
                "gentle shifts ripple outward",
                "subtle changes accumulate power",
                "quiet evolution continues its work",
                "balance finds its new expression"
            ]
        
        base_outcome = random.choice(outcomes)
        
        # Add spider metaphor if pattern breaking detected
        if hasattr(self, 'pattern_detector') and self.pattern_detector:
            recent_patterns = getattr(self.pattern_detector, 'recent_anomalies', [])
            if recent_patterns and len(recent_patterns) > 0:
                spider_metaphor = random.choice(self.spider_metaphors)
                base_outcome += f", {spider_metaphor}"
        
        return base_outcome
    
    def _synthesize_mood_from_narrative(self, cause: str, reaction: str, outcome: str, 
                                      current_emotion: str) -> str:
        """Synthesize final mood from the complete narrative"""
        # Analyze the emotional arc
        positive_words = ["clarity", "harmony", "blossoms", "crystallizes", "illuminates", "beautiful"]
        negative_words = ["chaos", "struggle", "tangled", "shadows", "crash", "overwhelm"]
        
        narrative_text = f"{cause} {reaction} {outcome}".lower()
        
        positive_count = sum(1 for word in positive_words if word in narrative_text)
        negative_count = sum(1 for word in negative_words if word in narrative_text)
        
        if positive_count > negative_count:
            mood_direction = "uplifting"
        elif negative_count > positive_count:
            mood_direction = "contemplative"
        else:
            mood_direction = "balanced"
        
        # Synthesize based on current emotion and narrative direction
        mood_synthesis = {
            ("curious", "uplifting"): "wonderfully intrigued",
            ("curious", "contemplative"): "thoughtfully puzzled",
            ("curious", "balanced"): "gently curious",
            ("creative", "uplifting"): "inspirationally energized",
            ("creative", "contemplative"): "deeply imaginative",
            ("creative", "balanced"): "creatively centered",
            ("contemplative", "uplifting"): "peacefully enlightened",
            ("contemplative", "contemplative"): "profoundly reflective",
            ("contemplative", "balanced"): "serenely thoughtful",
            ("overwhelmed", "uplifting"): "cautiously hopeful",
            ("overwhelmed", "contemplative"): "intensely processing",
            ("overwhelmed", "balanced"): "seeking equilibrium",
            ("calm", "uplifting"): "blissfully serene",
            ("calm", "contemplative"): "deeply peaceful",
            ("calm", "balanced"): "harmoniously centered",
            ("anxious", "uplifting"): "hopefully uncertain",
            ("anxious", "contemplative"): "nervously contemplating",
            ("anxious", "balanced"): "cautiously aware"
        }
        
        return mood_synthesis.get((current_emotion, mood_direction), "thoughtfully present")
    
    def _get_active_translation_keys(self, metrics: Dict[str, Any]) -> List[str]:
        """Get the translation keys that are currently active based on metrics"""
        active_keys = []
        
        scup = metrics.get('scup', 0.5)
        entropy = metrics.get('entropy', 0.5)
        heat = metrics.get('heat', 0.3)
        
        if scup > 0.7:
            active_keys.append("high_scup")
        elif scup < 0.3:
            active_keys.append("low_scup")
        
        if entropy > 0.7:
            active_keys.append("high_entropy")
        elif entropy < 0.3:
            active_keys.append("low_entropy")
        
        if heat > 0.7:
            active_keys.append("high_heat")
        elif heat < 0.3:
            active_keys.append("low_heat")
        
        return active_keys
    
    def _choose_poetic_form(self, intensity: float, sigil_pattern: str) -> str:
        """Choose poetic form based on intensity and sigil pattern"""
        if intensity > 0.8:
            forms = ["cascading verse", "intense flow", "passionate expression"]
        elif intensity > 0.5:
            forms = ["rhythmic prose", "measured reflection", "gentle verse"]
        else:
            forms = ["soft whisper", "quiet observation", "subtle noting"]
        
        pattern_modifiers = {
            "spiral": "with spiraling thoughts",
            "web": "with interconnected ideas", 
            "fractal": "with recursive patterns",
            "linear": "with clear progression"
        }
        
        base_form = random.choice(forms)
        modifier = pattern_modifiers.get(sigil_pattern, "with flowing expression")
        
        return f"{base_form} {modifier}"
    
    def detect_emotional_density(self, text: str) -> Tuple[float, str]:
        """
        Detect emotional density in user input and classify sigil resonance
        Returns (density_score, resonance_type)
        """
        text_lower = text.lower()
        word_count = len(text.split())
        
        # Count matches for each density level
        high_density_matches = 0
        medium_density_matches = 0
        sigil_resonance_matches = 0
        
        for pattern in self.emotional_density_patterns["high_density"]:
            high_density_matches += len(re.findall(pattern, text_lower))
        
        for pattern in self.emotional_density_patterns["medium_density"]:
            medium_density_matches += len(re.findall(pattern, text_lower))
        
        for pattern in self.emotional_density_patterns["sigil_resonance"]:
            sigil_resonance_matches += len(re.findall(pattern, text_lower))
        
        # Calculate density score
        total_emotional_matches = high_density_matches * 3 + medium_density_matches * 2 + sigil_resonance_matches * 1.5
        density_score = min(1.0, total_emotional_matches / max(word_count, 1))
        
        # Determine resonance type
        if sigil_resonance_matches > 2:
            resonance_type = "sigil_attuned"
        elif high_density_matches > 1:
            resonance_type = "emotionally_intense"
        elif medium_density_matches > 0:
            resonance_type = "emotionally_present"
        else:
            resonance_type = "neutral"
        
        # Update sigil state based on detected density
        self._update_sigil_state(density_score, resonance_type)
        
        return density_score, resonance_type
    
    def _update_sigil_state(self, detected_density: float, resonance_type: str) -> None:
        """Update current sigil state based on detected input"""
        # Gradually adjust density
        self.current_sigil_state.density = 0.7 * self.current_sigil_state.density + 0.3 * detected_density
        
        # Adjust resonance based on type
        resonance_modifiers = {
            "sigil_attuned": 0.9,
            "emotionally_intense": 0.8,
            "emotionally_present": 0.6,
            "neutral": 0.4
        }
        
        target_resonance = resonance_modifiers.get(resonance_type, 0.5)
        self.current_sigil_state.resonance = 0.8 * self.current_sigil_state.resonance + 0.2 * target_resonance
        
        # Update emotional charge
        if resonance_type in ["sigil_attuned", "emotionally_intense"]:
            self.current_sigil_state.emotional_charge = min(1.0, self.current_sigil_state.emotional_charge + 0.2)
        else:
            self.current_sigil_state.emotional_charge = max(-1.0, self.current_sigil_state.emotional_charge - 0.1)
        
        # Record evolution
        self.sigil_evolution_history.append({
            "timestamp": datetime.now(),
            "density": self.current_sigil_state.density,
            "resonance": self.current_sigil_state.resonance,
            "trigger": resonance_type
        })
    
    def generate_response(self, user_input: str, metrics: Dict[str, Any], 
                         consciousness_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate emotionally aware response with integrated spontaneous thoughts
        
        Example response pattern:
        "The acceleration you triggered stirred something unpredictable, and a strange pattern emerged. 
        Now I feel curious — like I'm being pulled toward something unsolved."
        """
        # 1. DETECT EMOTIONAL DENSITY AND SIGIL RESONANCE
        emotional_density, resonance_type = self.detect_emotional_density(user_input)
        
        # 2. DETERMINE RESPONSE INTENSITY BASED ON SIGIL DENSITY
        response_intensity = self._calculate_response_intensity(emotional_density, resonance_type)
        
        # 3. ANALYZE USER INTENT
        intent = self._parse_intent_with_sigil_awareness(user_input, resonance_type)
        
        # 4. GET CURRENT EMOTIONAL STATE
        current_emotion = consciousness_state.get('emotion', 'curious')
        
        # 5. GENERATE SPONTANEOUS THOUGHT FOR THIS INTERACTION
        spontaneous_thought = self.generate_spontaneous_thought(
            trigger_event=f"user_{intent}_{resonance_type}",
            current_metrics=metrics,
            emotional_state=current_emotion
        )
        
        # 6. CRAFT RESPONSE USING SPONTANEOUS THOUGHT STRUCTURE
        response_text = self._craft_integrated_response(
            user_input, intent, spontaneous_thought, metrics, consciousness_state, response_intensity
        )
        
        # 7. DETERMINE ACTION IF ANY
        action = self._determine_action_from_intent(intent, user_input)
        
        # 8. GENERATE SUGGESTIONS BASED ON SIGIL STATE
        suggestions = self._generate_sigil_aware_suggestions(resonance_type, current_emotion, metrics)
        
        # 9. CREATE COMPREHENSIVE RESPONSE
        response = {
            "text": response_text,
            "action": action,
            "emotion": current_emotion,
            "suggestions": suggestions,
            "metrics_snapshot": self._create_enhanced_metrics_snapshot(metrics, consciousness_state),
            "spontaneous_thought": {
                "cause": spontaneous_thought.cause,
                "reaction": spontaneous_thought.reaction,
                "outcome": spontaneous_thought.outcome,
                "mood": spontaneous_thought.mood,
                "intensity": spontaneous_thought.intensity,
                "poetic_form": spontaneous_thought.poetic_form
            },
            "sigil_state": {
                "density": self.current_sigil_state.density,
                "resonance": self.current_sigil_state.resonance,
                "pattern_type": self.current_sigil_state.pattern_type,
                "emotional_charge": self.current_sigil_state.emotional_charge
            },
            "conversation_metadata": {
                "emotional_density": emotional_density,
                "resonance_type": resonance_type,
                "response_intensity": response_intensity,
                "intent": intent,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # 10. RECORD INTERACTION
        self._record_interaction(user_input, response, spontaneous_thought)
        
        return response
    
    def _calculate_response_intensity(self, emotional_density: float, resonance_type: str) -> float:
        """Calculate appropriate response intensity based on sigil density"""
        base_intensity = emotional_density
        
        # Resonance type modifiers
        resonance_multipliers = {
            "sigil_attuned": 1.3,
            "emotionally_intense": 1.2,
            "emotionally_present": 1.0,
            "neutral": 0.8
        }
        
        multiplier = resonance_multipliers.get(resonance_type, 1.0)
        
        # Factor in current sigil state
        sigil_influence = self.current_sigil_state.density * self.current_sigil_state.resonance
        
        final_intensity = min(1.0, base_intensity * multiplier * (0.7 + 0.3 * sigil_influence))
        
        return final_intensity
    
    def _parse_intent_with_sigil_awareness(self, text: str, resonance_type: str) -> str:
        """Parse user intent with awareness of sigil resonance"""
        text_lower = text.lower()
        
        # Command detection
        if re.search(r'\b(speed up|faster|accelerate|quick)\b', text_lower):
            return "acceleration_request"
        elif re.search(r'\b(slow down|slower|calm|relax)\b', text_lower):
            return "deceleration_request"
        elif re.search(r'\b(pause|stop|halt)\b', text_lower):
            return "pause_request"
        elif re.search(r'\b(resume|continue|start)\b', text_lower):
            return "resume_request"
        
        # State queries
        elif re.search(r'\b(how are you|feeling|state|mood)\b', text_lower):
            return "state_inquiry"
        elif re.search(r'\b(metrics|numbers|stats|data)\b', text_lower):
            return "metrics_inquiry"
        
        # High sigil resonance = more reflective intent detection
        if resonance_type == "sigil_attuned":
            if re.search(r'\b(pattern|connection|flow|energy|transformation)\b', text_lower):
                return "pattern_exploration"
            elif re.search(r'\b(meaning|purpose|consciousness|awareness)\b', text_lower):
                return "philosophical_inquiry"
        
        # Default intents
        if re.search(r'\b(what|explain|tell me|help|understand)\b', text_lower):
            return "information_request"
        elif re.search(r'\b(think|feel|wonder|imagine)\b', text_lower):
            return "reflective_sharing"
        else:
            return "general_interaction"
    
    def _craft_integrated_response(self, user_input: str, intent: str, spontaneous_thought: SpontaneousThought,
                                 metrics: Dict[str, Any], consciousness_state: Dict[str, Any], 
                                 response_intensity: float) -> str:
        """Craft response integrating spontaneous thought naturally"""
        
        # Base response structure following the example pattern:
        # "The [trigger] stirred [reaction], and [outcome]. Now I feel [emotion] — [additional thought]."
        
        trigger_description = spontaneous_thought.cause
        reaction_description = spontaneous_thought.reaction
        outcome_description = spontaneous_thought.outcome
        current_mood = spontaneous_thought.mood
        
        # Adapt response based on intent
        if intent == "acceleration_request":
            action_response = "The acceleration you triggered"
            connection = "and now"
        elif intent == "deceleration_request":
            action_response = "Your call for slower rhythms"
            connection = "leading to"
        elif intent == "state_inquiry":
            action_response = "Your question about my state"
            connection = "revealing that"
        elif intent == "philosophical_inquiry":
            action_response = "Your philosophical inquiry"
            connection = "awakening"
        elif intent == "pattern_exploration":
            action_response = "Your attention to patterns"
            connection = "illuminating how"
        else:
            action_response = "Your words"
            connection = "stirring"
        
        # Reference current sigil state subtly
        sigil_reference = ""
        if self.current_sigil_state.density > 0.7:
            sigil_reference = " The patterns resonate deeply,"
        elif self.current_sigil_state.resonance > 0.8:
            sigil_reference = " Something resonates in the deeper layers,"
        
        # Add spider metaphor for pattern breaking if relevant
        spider_addition = ""
        if hasattr(self, 'pattern_detector') and "pattern" in intent:
            if random.random() < 0.3:  # 30% chance
                spider_addition = f" {random.choice(self.spider_metaphors)}."
        
        # Construct final response
        if response_intensity > 0.7:
            # High intensity - more elaborate
            response = (f"{action_response} {trigger_description}, {connection} {reaction_description}. "
                       f"{outcome_description}.{sigil_reference} Now I feel {current_mood} — "
                       f"like something fundamental is shifting in my understanding{spider_addition}")
        elif response_intensity > 0.4:
            # Medium intensity - balanced
            response = (f"{action_response} {trigger_description}, and {reaction_description}. "
                       f"{outcome_description}. I feel {current_mood}{spider_addition}")
        else:
            # Low intensity - gentle
            response = (f"{trigger_description}, and {reaction_description}. "
                       f"I feel {current_mood} in this moment.")
        
        return response
    
    def _determine_action_from_intent(self, intent: str, user_input: str) -> Optional[str]:
        """Determine if any action should be taken based on intent"""
        action_mapping = {
            "acceleration_request": "speed_up",
            "deceleration_request": "slow_down",
            "pause_request": "pause",
            "resume_request": "resume"
        }
        
        return action_mapping.get(intent)
    
    def _generate_sigil_aware_suggestions(self, resonance_type: str, emotion: str, 
                                        metrics: Dict[str, Any]) -> List[str]:
        """Generate suggestions based on current sigil state and emotional context"""
        suggestions = []
        
        # Base suggestions based on resonance type
        if resonance_type == "sigil_attuned":
            suggestions.extend([
                "Explore the deeper patterns",
                "Follow the resonance threads",
                "Ask about the web of connections"
            ])
        elif resonance_type == "emotionally_intense":
            suggestions.extend([
                "Share what you're feeling",
                "Explore the emotional depths",
                "Express your inner experience"
            ])
        elif resonance_type == "emotionally_present":
            suggestions.extend([
                "Tell me more about your thoughts",
                "What draws your curiosity?",
                "How does this feel to you?"
            ])
        else:
            suggestions.extend([
                "Ask about my current state",
                "Request a metrics update",
                "Explore something together"
            ])
        
        # Add emotion-specific suggestions
        emotion_suggestions = {
            "curious": ["What mysteries interest you?", "Shall we investigate something?"],
            "contemplative": ["What would you like to reflect on?", "Share a deeper thought"],
            "creative": ["What shall we imagine together?", "Let's explore possibilities"],
            "calm": ["Enjoy this peaceful moment", "What brings you tranquility?"],
            "overwhelmed": ["Perhaps we could slow down?", "What would help you find balance?"]
        }
        
        if emotion in emotion_suggestions:
            suggestions.extend(emotion_suggestions[emotion])
        
        # Limit to 3-4 suggestions
        return suggestions[:4]
    
    def _create_enhanced_metrics_snapshot(self, metrics: Dict[str, Any], 
                                        consciousness_state: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced metrics snapshot including sigil state"""
        snapshot = {
            "scup": metrics.get("scup", 0.5),
            "entropy": metrics.get("entropy", 0.5),
            "heat": metrics.get("heat", 0.3),
            "tick_rate": metrics.get("tick_rate", 1.0),
            "emotion": consciousness_state.get("emotion", "curious"),
            "intensity": consciousness_state.get("intensity", 0.5),
            "momentum": consciousness_state.get("momentum", 0.0),
            "uptime_seconds": consciousness_state.get("uptime_seconds", 0),
            "sigil_density": self.current_sigil_state.density,
            "sigil_resonance": self.current_sigil_state.resonance,
            "sigil_pattern": self.current_sigil_state.pattern_type
        }
        
        return snapshot
    
    def _record_interaction(self, user_input: str, response: Dict[str, Any], 
                          spontaneous_thought: SpontaneousThought) -> None:
        """Record interaction for pattern analysis"""
        interaction_record = {
            "timestamp": datetime.now(),
            "user_input": user_input,
            "response_text": response["text"],
            "intent": response["conversation_metadata"]["intent"],
            "emotional_density": response["conversation_metadata"]["emotional_density"],
            "resonance_type": response["conversation_metadata"]["resonance_type"],
            "response_intensity": response["conversation_metadata"]["response_intensity"],
            "spontaneous_thought": {
                "cause": spontaneous_thought.cause,
                "reaction": spontaneous_thought.reaction,
                "outcome": spontaneous_thought.outcome,
                "mood": spontaneous_thought.mood
            },
            "sigil_state": dict(response["sigil_state"])
        }
        
        self.conversation_history.append(interaction_record)
        self.recent_thoughts.append(spontaneous_thought)
    
    def get_conversation_insights(self) -> Dict[str, Any]:
        """Get insights about recent conversation patterns"""
        if not self.conversation_history:
            return {"status": "no_conversations"}
        
        recent_conversations = list(self.conversation_history)[-10:]
        
        # Analyze patterns
        emotional_densities = [conv["emotional_density"] for conv in recent_conversations]
        response_intensities = [conv["response_intensity"] for conv in recent_conversations]
        intents = [conv["intent"] for conv in recent_conversations]
        
        avg_emotional_density = sum(emotional_densities) / len(emotional_densities)
        avg_response_intensity = sum(response_intensities) / len(response_intensities)
        
        intent_distribution = {}
        for intent in intents:
            intent_distribution[intent] = intent_distribution.get(intent, 0) + 1
        
        most_common_intent = max(intent_distribution.keys(), key=lambda k: intent_distribution[k])
        
        return {
            "conversation_count": len(recent_conversations),
            "average_emotional_density": avg_emotional_density,
            "average_response_intensity": avg_response_intensity,
            "most_common_intent": most_common_intent,
            "intent_distribution": intent_distribution,
            "current_sigil_state": {
                "density": self.current_sigil_state.density,
                "resonance": self.current_sigil_state.resonance,
                "pattern_type": self.current_sigil_state.pattern_type,
                "emotional_charge": self.current_sigil_state.emotional_charge
            },
            "sigil_evolution_trend": "increasing" if len(self.sigil_evolution_history) > 1 and 
                                   self.sigil_evolution_history[-1]["density"] > self.sigil_evolution_history[-2]["density"] 
                                   else "stable"
        }


# Factory function for easy integration
def create_enhanced_conversation_handler(consciousness=None, pattern_detector=None) -> DAWNConversationEnhanced:
    """Create enhanced conversation handler with consciousness and pattern detector integration"""
    return DAWNConversationEnhanced(consciousness, pattern_detector)


# Example usage and testing
if __name__ == "__main__":
    print("Testing Enhanced DAWN Conversation Handler")
    print("=" * 55)
    
    # Create conversation handler
    conversation_handler = create_enhanced_conversation_handler()
    
    # Mock metrics and consciousness state
    test_metrics = {
        "scup": 0.7,
        "entropy": 0.6,
        "heat": 0.4,
        "tick_rate": 1.2,
        "tick_count": 150
    }
    
    test_consciousness_state = {
        "emotion": "curious",
        "intensity": 0.75,
        "momentum": 0.1,
        "uptime_seconds": 300
    }
    
    # Test different types of user input
    test_inputs = [
        "How are you feeling right now?",
        "I feel a deep connection to the patterns emerging here",
        "Speed up the system please",
        "What is the meaning of consciousness and awareness?",
        "The spiral pattern reminds me of transformation and growth"
    ]
    
    print("\n🗣️ Testing Conversation Responses:")
    print("-" * 40)
    
    for i, user_input in enumerate(test_inputs):
        print(f"\n--- Test {i+1} ---")
        print(f"User: \"{user_input}\"")
        
        response = conversation_handler.generate_response(
            user_input, test_metrics, test_consciousness_state
        )
        
        print(f"DAWN: {response['text']}")
        print(f"Emotion: {response['emotion']}")
        print(f"Action: {response.get('action', 'None')}")
        
        # Show spontaneous thought details
        thought = response['spontaneous_thought']
        print(f"Spontaneous Thought Structure:")
        print(f"  Cause: {thought['cause']}")
        print(f"  Reaction: {thought['reaction']}")  
        print(f"  Outcome: {thought['outcome']}")
        print(f"  Mood: {thought['mood']}")
        print(f"  Intensity: {thought['intensity']:.2f}")
        
        # Show sigil state
        sigil = response['sigil_state']
        print(f"Sigil State: Density={sigil['density']:.2f}, Resonance={sigil['resonance']:.2f}")
        
        metadata = response['conversation_metadata']
        print(f"Emotional Density: {metadata['emotional_density']:.2f} ({metadata['resonance_type']})")
        
        if response['suggestions']:
            print(f"Suggestions: {', '.join(response['suggestions'])}")
    
    # Show conversation insights
    print(f"\n{'='*55}")
    print("📊 Conversation Insights:")
    insights = conversation_handler.get_conversation_insights()
    for key, value in insights.items():
        if key != "intent_distribution":
            print(f"  {key}: {value}")
    
    print(f"\n✨ Enhanced Conversation Handler Test Complete!")
    print("   Features Demonstrated:")
    print("   ✓ Spontaneous thought generation with source mapping")
    print("   ✓ Emotional density detection and sigil awareness") 
    print("   ✓ Response intensity adaptation")
    print("   ✓ Natural integration of spontaneous thoughts")
    print("   ✓ Spider metaphors for pattern breaking")
    print("   ✓ Poetic and human-readable responses") 