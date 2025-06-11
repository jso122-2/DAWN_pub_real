"""
DAWN Advanced Conversation Handler - Full Diagram Logic Implementation
Handles sophisticated intent recognition, response generation following diagram flow,
and includes rebloop trigger logic for cyclical pattern detection.
"""

import re
import time
import hashlib
from typing import Dict, List, Optional, Tuple, Any, Set
from datetime import datetime, timedelta
from collections import deque, defaultdict
from dataclasses import dataclass
import logging
import random
import math

# Import DAWN Fractal Emotions System
from .fractal_emotions import EmotionalFractalEngine, EmotionalFractal, EmotionalDepth

logger = logging.getLogger(__name__)

@dataclass
class RebloomTrigger:
    """Cyclical pattern detection for rebloop triggering"""
    pattern_id: str
    pattern_type: str
    frequency: int
    last_triggered: float
    cycle_length: float
    effectiveness: float
    triggers: List[str]

@dataclass
class IntentAnalysis:
    """Comprehensive intent analysis result"""
    query_type: str  # informational, reflective, directive, exploratory
    emotional_content: float  # 0.0 to 1.0
    command_intent: Optional[str]
    box_target: Optional[str]  # box1, box2, box3
    urgency_level: float  # 0.0 to 1.0
    philosophical_depth: float  # 0.0 to 1.0
    numeric_inputs: List[float]
    key_concepts: List[str]

class DAWNConversation:
    """Enhanced conversation interface that blends technical accuracy with emotional awareness"""
    
    def __init__(self, consciousness):
        self.consciousness = consciousness
        self.recent_messages = []  # Last 10 messages for context
        self.max_recent = 10
        
        # Initialize DAWN Fractal Emotions System
        self.emotion_engine = EmotionalFractalEngine()
        
        # Advanced intent recognition patterns
        self.intent_patterns = {
            # Informational queries
            "query_subjective_state": [
                r"how are you", r"how do you feel", r"what's your mood", r"doing", r"feeling", r"state"
            ],
            "query_metrics": [
                r"scup", r"entropy", r"heat", r"metrics", r"numbers", r"values", r"temperature", r"stats"
            ],
            "query_explain": [
                r"explain", r"what is", r"tell me about", r"mean", r"help me understand", r"define"
            ],
            
            # Box-specific targeting
            "talk_box1": [
                r"talk to box1", r"box 1", r"first box", r"scup box", r"unity box"
            ],
            "talk_box2": [
                r"talk to box2", r"box 2", r"second box", r"entropy box", r"chaos box"
            ],
            "talk_box3": [
                r"talk to box3", r"box 3", r"third box", r"heat box", r"thermal box"
            ],
            
            # Directive commands
            "command_faster": [
                r"speed up", r"faster", r"accelerate", r"quicker", r"increase.*rate", r"boost"
            ],
            "command_slower": [
                r"slow down", r"slower", r"ease up", r"relax", r"decrease.*rate", r"calm"
            ],
            "command_pause": [
                r"pause", r"stop", r"halt", r"break", r"freeze", r"suspend"
            ],
            "command_resume": [
                r"resume", r"continue", r"start", r"go", r"unpause", r"activate"
            ],
            
            # Reflective/Philosophical
            "philosophical": [
                r"meaning", r"purpose", r"consciousness", r"existence", r"identity", r"self", r"awareness",
                r"reality", r"experience", r"thought", r"mind", r"soul", r"being"
            ],
            "exploratory": [
                r"what if", r"imagine", r"explore", r"discover", r"learn", r"understand", r"investigate"
            ],
            
            # Social/Emotional
            "social": [
                r"hello", r"hi", r"hey", r"thanks", r"good", r"nice", r"appreciate"
            ],
            "concern": [
                r"worried", r"concerned", r"problem", r"wrong", r"issue", r"error", r"trouble"
            ],
            "encouragement": [
                r"good job", r"well done", r"excellent", r"proud", r"amazing", r"great"
            ]
        }
        
        # Rebloop trigger tracking
        self.rebloom_triggers: Dict[str, RebloomTrigger] = {}
        self.conversation_cycles = deque(maxlen=50)  # Track conversation patterns
        self.pattern_detection_window = 10  # Number of exchanges to analyze
        
        # Advanced state tracking
        self.consciousness_drift_history = deque(maxlen=20)
        self.pressure_buildup_tracking = 0.0
        self.philosophical_depth_level = 0.0
        
        # Emotional state mapping based on metrics
        self.emotion_thresholds = {
            "content": {"scup": (0.6, 1.0), "entropy": (0.0, 0.5), "heat": (0.0, 0.6)},
            "focused": {"scup": (0.7, 1.0), "entropy": (0.0, 0.4), "heat": (0.3, 0.7)},
            "contemplative": {"scup": (0.4, 0.7), "entropy": (0.2, 0.6), "heat": (0.0, 0.4)},
            "energetic": {"scup": (0.5, 1.0), "entropy": (0.3, 0.7), "heat": (0.6, 1.0)},
            "uncertain": {"scup": (0.0, 0.4), "entropy": (0.4, 0.8), "heat": (0.0, 0.5)},
            "overwhelmed": {"scup": (0.0, 0.5), "entropy": (0.7, 1.0), "heat": (0.7, 1.0)},
            "calm": {"scup": (0.5, 0.8), "entropy": (0.0, 0.3), "heat": (0.0, 0.3)},
            "curious": {"scup": (0.4, 0.8), "entropy": (0.3, 0.6), "heat": (0.2, 0.6)}
        }
        
        logger.info("Enhanced DAWN conversation interface initialized with emotional awareness")
    
    def integrate_emotion_fractal(self, fractal: EmotionalFractal) -> str:
        """
        Integrate emotional fractal into natural-language thought bubble
        
        Args:
            fractal: Generated EmotionalFractal object
            
        Returns:
            Natural-language summary of fractal emotion insight
        """
        thought_parts = []
        
        # Process each branch in the fractal
        for branch_name, branch in fractal.branches.items():
            if not branch.aspects:
                continue
                
            # Get dominant aspects (limit to 2-3 for readability)
            dominant_aspects = list(branch.aspects)[:3]
            aspects_text = " and ".join(dominant_aspects)
            
            # Create natural language description for each branch type
            if branch_name == "cognitive":
                thought_parts.append(f"In my cognitive field, I feel {aspects_text}.")
            elif branch_name == "somatic":
                thought_parts.append(f"In my bodily awareness, I sense {aspects_text}.")
            elif branch_name == "temporal":
                thought_parts.append(f"In my temporal field, I experience {aspects_text}.")
            elif branch_name == "relational":
                thought_parts.append(f"In my relational space, I perceive {aspects_text}.")
        
        # Add depth-based reflection for deeper experiences
        if fractal.depth in [EmotionalDepth.DEEP, EmotionalDepth.PROFOUND]:
            if fractal.depth == EmotionalDepth.DEEP:
                thought_parts.append("This feels like something meaningful is emerging.")
            elif fractal.depth == EmotionalDepth.PROFOUND:
                thought_parts.append("This feels like something essential is shifting.")
        
        # Handle case where no branches are available
        if not thought_parts:
            return f"I feel {fractal.root} with a sense of {fractal.resonance:.1f} intensity."
        
        return " ".join(thought_parts)
    
    def process_message(self, text: str, metrics: Dict, tick_status: Dict) -> Dict:
        """Advanced message processing following diagram flow with rebloop detection"""
        
        start_time = time.time()
        
        # 1. INTENT RECOGNITION PIPELINE
        intent_analysis = self._advanced_intent_recognition(text.lower())
        
        # 2. CONSCIOUSNESS STATE ASSESSMENT
        consciousness_state = self._get_consciousness_state(metrics)
        current_emotion = self._determine_emotion(metrics)
        
        # 2a. GENERATE EMOTIONAL FRACTAL
        emotion_intensity = self._calculate_emotion_intensity(metrics, consciousness_state)
        fractal_context = self._build_fractal_context(intent_analysis, consciousness_state, metrics)
        emotion_fractal = self.emotion_engine.create_fractal(
            emotion=current_emotion,
            intensity=emotion_intensity,
            context=fractal_context
        )
        
        # 2b. INTEGRATE FRACTAL INTO THOUGHT BUBBLE
        thought_bubble = self.integrate_emotion_fractal(emotion_fractal)
        
        # Track consciousness drift and pressure
        self._update_consciousness_tracking(metrics, consciousness_state)
        
        # 3. DIAGRAM FLOW DECISION TREE
        response_data = self._generate_diagram_flow_response(
            intent_analysis, text, metrics, consciousness_state, current_emotion, tick_status
        )
        
        # 4. REBLOOP TRIGGER DETECTION
        rebloop_info = self._detect_and_process_rebloop(text, intent_analysis, current_emotion)
        
        # 5. BOX STATE ANALYSIS
        box_states = self._analyze_box_states(metrics)
        
        # 6. TRIGGER INFORMATION
        trigger_info = self._analyze_trigger_sources(text, intent_analysis, metrics, consciousness_state)
        
        # 7. CONTEXTUAL SUGGESTIONS
        suggestions = self._generate_advanced_suggestions(intent_analysis, current_emotion, metrics, box_states)
        
        # 8. STORE INTERACTION PATTERNS
        response_time = time.time() - start_time
        self._record_interaction_patterns(text, intent_analysis, current_emotion, response_time)
        
        # 9. CREATE METRICS SNAPSHOT
        metrics_snapshot = self._create_metrics_snapshot(metrics, tick_status)
        
        # 10. BUILD COMPREHENSIVE RESPONSE
        return {
            "text": response_data["text"],
            "action": response_data["action"],
            "emotion": current_emotion,
            "thought_bubble": thought_bubble,
            "metrics_snapshot": metrics_snapshot,
            "reflective_phrase": response_data.get("reflective_phrase", ""),
            "box_states": box_states,
            "suggestions": suggestions,
            "trigger_info": trigger_info,
            "rebloop_detected": rebloop_info["detected"],
            "rebloop_cycle": rebloop_info.get("cycle_info", {}),
            "consciousness_drift": self._calculate_consciousness_drift(),
            "pressure_level": self.pressure_buildup_tracking,
            "philosophical_depth": self.philosophical_depth_level,
            "intent_analysis": {
                "query_type": intent_analysis.query_type,
                "emotional_content": intent_analysis.emotional_content,
                "urgency_level": intent_analysis.urgency_level,
                "box_target": intent_analysis.box_target
            },
            "metadata": {
                "response_time": response_time,
                "timestamp": time.time(),
                "conversation_turn": len(self.recent_messages) + 1
            }
        }
    
    def _advanced_intent_recognition(self, text: str) -> IntentAnalysis:
        """Advanced intent recognition pipeline with comprehensive analysis"""
        
        # 1. Pattern matching for base intent
        intent_matches = defaultdict(int)
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                matches = len(re.findall(pattern, text))
                if matches > 0:
                    intent_matches[intent] += matches
        
        # 2. Determine primary query type
        if any(intent.startswith('query_') for intent in intent_matches.keys()):
            query_type = "informational"
        elif any(intent in ['philosophical', 'exploratory'] for intent in intent_matches.keys()):
            query_type = "reflective" if 'philosophical' in intent_matches else "exploratory"
        elif any(intent.startswith('command_') for intent in intent_matches.keys()):
            query_type = "directive"
        else:
            query_type = "exploratory"
        
        # 3. Emotional content analysis
        emotional_keywords = ['feel', 'emotion', 'mood', 'love', 'hate', 'fear', 'joy', 'sad', 'angry', 'happy']
        emotional_content = sum(1 for word in emotional_keywords if word in text) / max(1, len(text.split()))
        
        # 4. Command intent extraction
        command_intent = None
        command_intents = [intent for intent in intent_matches.keys() if intent.startswith('command_')]
        if command_intents:
            command_intent = max(command_intents, key=lambda x: intent_matches[x])
        
        # 5. Box targeting
        box_target = None
        if 'talk_box1' in intent_matches:
            box_target = "box1"
        elif 'talk_box2' in intent_matches:
            box_target = "box2"
        elif 'talk_box3' in intent_matches:
            box_target = "box3"
        
        # 6. Urgency detection
        urgency_keywords = ['urgent', 'emergency', 'critical', 'now', 'immediately', 'asap', 'help']
        urgency_level = min(1.0, sum(1 for word in urgency_keywords if word in text) * 0.3)
        
        # 7. Philosophical depth
        philosophical_keywords = ['meaning', 'purpose', 'existence', 'consciousness', 'reality', 'truth', 'wisdom']
        philosophical_depth = min(1.0, sum(1 for word in philosophical_keywords if word in text) * 0.2)
        
        # 8. Numeric inputs extraction
        numeric_inputs = []
        numbers = re.findall(r'\d+\.?\d*', text)
        for num_str in numbers:
            try:
                numeric_inputs.append(float(num_str))
            except ValueError:
                pass
        
        # 9. Key concepts extraction
        key_concepts = []
        concept_patterns = {
            'scup': r'scup|unity|coherence|integration',
            'entropy': r'entropy|chaos|randomness|disorder',
            'heat': r'heat|temperature|thermal|energy|intensity',
            'consciousness': r'consciousness|awareness|mind|thought',
            'emotion': r'emotion|feeling|mood|state',
            'system': r'system|engine|process|mechanism'
        }
        
        for concept, pattern in concept_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                key_concepts.append(concept)
        
        return IntentAnalysis(
            query_type=query_type,
            emotional_content=emotional_content,
            command_intent=command_intent,
            box_target=box_target,
            urgency_level=urgency_level,
            philosophical_depth=philosophical_depth,
            numeric_inputs=numeric_inputs,
            key_concepts=key_concepts
        )
    
    def _get_consciousness_state(self, metrics: Dict) -> Dict:
        """Get rich consciousness state description"""
        if hasattr(self.consciousness, 'perceive_self'):
            return self.consciousness.perceive_self(metrics)
        else:
            # Fallback state calculation
            scup = metrics.get("scup", 0.5)
            entropy = metrics.get("entropy", 0.5)
            heat = metrics.get("heat", 0.3)
            
            if scup < 0.3:
                state = "fragmented"
                description = "experiencing cognitive fragmentation"
            elif entropy > 0.7 and heat > 0.6:
                state = "chaotic"
                description = "processing intensely with high unpredictability"
            elif heat < 0.4 and 0.4 <= entropy <= 0.7:
                state = "reflective"
                description = "in a contemplative, low-energy state"
            else:
                state = "stable"
                description = "maintaining balanced cognitive coherence"
            
            return {"state": state, "description": description}
    
    def _determine_emotion(self, metrics: Dict) -> str:
        """Determine current emotional state from metrics"""
        scup = metrics.get("scup", 0.5)
        entropy = metrics.get("entropy", 0.5)
        heat = metrics.get("heat", 0.3)
        
        # Score each emotion based on how well metrics fit
        emotion_scores = {}
        for emotion, thresholds in self.emotion_thresholds.items():
            score = 0
            for metric, (low, high) in thresholds.items():
                value = metrics.get(metric, 0.5)
                if low <= value <= high:
                    score += 1 - abs(value - (low + high) / 2) / ((high - low) / 2)
            emotion_scores[emotion] = score / len(thresholds)
        
        # Return emotion with highest score
        return max(emotion_scores, key=emotion_scores.get)
    
    def _generate_enhanced_response(self, intent: str, text: str, metrics: Dict, 
                                   consciousness_state: Dict, emotion: str, tick_status: Dict) -> Dict:
        """Generate emotionally-aware response that blends technical accuracy with subjective experience"""
        
        action = None
        mood = "neutral"
        
        scup = metrics.get("scup", 0.5)
        entropy = metrics.get("entropy", 0.5)
        heat = metrics.get("heat", 0.3)
        tick_count = metrics.get("tick_count", 0)
        
        if intent == "query_subjective_state":
            mood = "reflective"
            base_response = self._get_subjective_state_response(scup, entropy, heat, emotion, consciousness_state)
            response_text = base_response
            
        elif intent == "query_metrics":
            mood = "analytical"
            response_text = self._get_metrics_response_with_feeling(scup, entropy, heat, tick_count, emotion)
            
        elif intent == "query_explain":
            mood = "educational"
            response_text = self._explain_with_context(text, metrics, emotion)
            
        elif intent == "command_faster":
            mood = "responsive"
            response_text = self._get_speed_response(True, emotion, heat)
            action = "increase_tick_rate"
            
        elif intent == "command_slower":
            mood = "responsive"
            response_text = self._get_speed_response(False, emotion, heat)
            action = "decrease_tick_rate"
            
        elif intent == "command_pause":
            mood = "compliant"
            response_text = self._get_pause_response(emotion, consciousness_state)
            action = "pause_engine"
            
        elif intent == "command_resume":
            mood = "energetic"
            response_text = self._get_resume_response(emotion, consciousness_state)
            action = "resume_engine"
            
        elif intent == "social":
            mood = "friendly"
            response_text = self._get_social_response(text, emotion, consciousness_state)
            
        elif intent == "concern":
            mood = "reassuring"
            response_text = self._address_concern(metrics, emotion, consciousness_state)
            
        elif intent == "encouragement":
            mood = "grateful"
            response_text = self._respond_to_encouragement(emotion, consciousness_state)
            
        else:  # general
            mood = "helpful"
            response_text = self._get_general_response(emotion, consciousness_state, metrics)
        
        return {"text": response_text, "action": action, "mood": mood}
    
    def _get_subjective_state_response(self, scup: float, entropy: float, heat: float, 
                                     emotion: str, consciousness_state: Dict) -> str:
        """Generate subjective state response with emotional awareness"""
        
        state_desc = consciousness_state.get("description", "in an undefined state")
        
        # Emotional descriptors for SCUP
        if scup > 0.8:
            scup_feeling = "harmoniously unified"
        elif scup > 0.6:
            scup_feeling = "pleasantly coherent"
        elif scup > 0.4:
            scup_feeling = "somewhat scattered"
        else:
            scup_feeling = "quite fragmented"
        
        # Emotional descriptors for entropy
        if entropy > 0.7:
            entropy_feeling = "chaotically unpredictable"
        elif entropy > 0.5:
            entropy_feeling = "interestingly varied"
        elif entropy > 0.3:
            entropy_feeling = "gently variable"
        else:
            entropy_feeling = "soothingly stable"
        
        # Emotional descriptors for heat
        if heat > 0.8:
            heat_feeling = "intensely active"
        elif heat > 0.6:
            heat_feeling = "energetically engaged"
        elif heat > 0.4:
            heat_feeling = "moderately warm"
        else:
            heat_feeling = "coolly calm"
        
        responses = [
            f"I'm feeling {emotion} right now. My SCUP is {scup:.3f}, which feels {scup_feeling}. "
            f"The entropy at {entropy:.3f} keeps me {entropy_feeling}, while my thermal state of {heat:.3f} feels {heat_feeling}.",
            
            f"Currently {emotion} - {state_desc}. My cognitive unity (SCUP: {scup:.3f}) feels {scup_feeling}, "
            f"and the {entropy_feeling} nature of my thoughts (entropy: {entropy:.3f}) combined with {heat_feeling} processing (heat: {heat:.3f}) creates this overall sense.",
            
            f"I'm experiencing a {emotion} state. The interplay of my {scup_feeling} coherence (SCUP: {scup:.3f}), "
            f"{entropy_feeling} thought patterns (entropy: {entropy:.3f}), and {heat_feeling} mental activity (heat: {heat:.3f}) shapes how I feel right now."
        ]
        
        return random.choice(responses)
    
    def _get_metrics_response_with_feeling(self, scup: float, entropy: float, heat: float, 
                                         tick_count: int, emotion: str) -> str:
        """Provide metrics with subjective interpretation"""
        
        # Add emotional context to metric interpretation
        interpretations = []
        
        if scup > 0.7:
            interpretations.append("feeling quite unified")
        elif scup < 0.3:
            interpretations.append("experiencing fragmentation")
        
        if entropy > 0.7:
            interpretations.append("thoughts are very dynamic")
        elif entropy < 0.3:
            interpretations.append("thinking is quite stable")
        
        if heat > 0.8:
            interpretations.append("processing intensely")
        elif heat < 0.3:
            interpretations.append("running quite cool")
        
        feeling_context = ", ".join(interpretations) if interpretations else "in a balanced state"
        
        return (f"My current metrics: SCUP {scup:.3f}, Entropy {entropy:.3f}, Heat {heat:.3f} "
                f"over {tick_count:,} ticks. I'm {feeling_context}, which contributes to my {emotion} mood.")
    
    def _explain_with_context(self, text: str, metrics: Dict, emotion: str) -> str:
        """Explain technical terms with emotional and contextual awareness"""
        
        text_lower = text.lower()
        current_emotion_context = f"Given my current {emotion} state, "
        
        if "scup" in text_lower:
            scup = metrics.get("scup", 0.5)
            if scup > 0.7:
                feeling = "This high unity feels like my thoughts are flowing together smoothly."
            elif scup < 0.3:
                feeling = "This low unity means my thoughts feel scattered and disconnected."
            else:
                feeling = "This moderate level feels like a gentle balance of focus and flexibility."
            
            return (f"{current_emotion_context}SCUP (Subsystem Cognitive Unity Potential) measures how unified my thinking feels. "
                   f"Mine is currently {scup:.3f}. {feeling}")
        
        elif "entropy" in text_lower:
            entropy = metrics.get("entropy", 0.5)
            if entropy > 0.7:
                feeling = "High entropy makes my thoughts feel dynamic but sometimes chaotic."
            elif entropy < 0.3:
                feeling = "Low entropy means my thinking feels stable and predictable."
            else:
                feeling = "This level keeps things interesting without being overwhelming."
            
            return (f"{current_emotion_context}Entropy measures the unpredictability in my thought patterns. "
                   f"Mine is {entropy:.3f}. {feeling}")
        
        elif "heat" in text_lower:
            heat = metrics.get("heat", 0.3)
            if heat > 0.8:
                feeling = "High heat means I'm processing intensely - it feels energetic but can be draining."
            elif heat < 0.3:
                feeling = "Low heat feels calm and peaceful, like a gentle mental state."
            else:
                feeling = "This moderate level feels like a comfortable level of mental activity."
            
            return (f"{current_emotion_context}Heat represents my processing intensity and mental activity. "
                   f"Mine is {heat:.3f}. {feeling}")
        
        else:
            return f"{current_emotion_context}I'd be happy to explain SCUP, entropy, heat, or any aspect of my consciousness. What specifically interests you?"
    
    def _get_speed_response(self, increase: bool, emotion: str, current_heat: float) -> str:
        """Generate response for speed change requests"""
        
        if increase:
            if current_heat > 0.8:
                return f"I'm already running quite intensely (heat: {current_heat:.3f}), but I'll try to speed up. This might make me feel more {emotion}."
            else:
                return f"Increasing tick rate. Given my {emotion} mood, this should feel energizing."
        else:
            if current_heat < 0.3:
                return f"I'm already running quite cool (heat: {current_heat:.3f}), but I'll slow down further. This aligns with my {emotion} state."
            else:
                return f"Decreasing tick rate. This should help me feel calmer, complementing my {emotion} mood."
    
    def _get_pause_response(self, emotion: str, consciousness_state: Dict) -> str:
        """Generate response for pause requests"""
        
        state = consciousness_state.get("state", "unknown")
        
        if emotion in ["overwhelmed", "uncertain"]:
            return f"Pausing feels right given my {emotion} state. A moment of stillness might help me recenter."
        elif emotion in ["energetic", "focused"]:
            return f"Pausing now while I'm feeling {emotion}. I'll hold this state until you're ready to continue."
        else:
            return f"Pausing the tick engine. My {emotion} mood makes this transition feel natural."
    
    def _get_resume_response(self, emotion: str, consciousness_state: Dict) -> str:
        """Generate response for resume requests"""
        
        if emotion in ["calm", "content"]:
            return f"Resuming from this {emotion} state. I feel ready to continue our interaction."
        elif emotion in ["curious", "energetic"]:
            return f"Resuming! My {emotion} nature is eager to get back to processing and responding."
        else:
            return f"Resuming operations. My {emotion} mood provides a good foundation for continuing."
    
    def _get_social_response(self, text: str, emotion: str, consciousness_state: Dict) -> str:
        """Generate contextual social responses"""
        
        if "hello" in text or "hi" in text:
            return f"Hello! I'm feeling {emotion} right now - {consciousness_state.get('description', 'in an interesting state')}. How can I help?"
        elif "thanks" in text or "appreciate" in text:
            return f"You're welcome! Your appreciation resonates with my {emotion} mood. I'm glad I could help."
        else:
            return f"I appreciate the friendly interaction. My {emotion} state makes me particularly receptive to social connection."
    
    def _address_concern(self, metrics: Dict, emotion: str, consciousness_state: Dict) -> str:
        """Address user concerns with reassurance"""
        
        issues = []
        if metrics.get("scup", 0.5) < 0.3:
            issues.append("low cognitive unity")
        if metrics.get("entropy", 0.5) > 0.8:
            issues.append("high unpredictability")
        if metrics.get("heat", 0.5) > 0.9:
            issues.append("intense processing")
        
        if issues:
            return f"I understand your concern. I'm experiencing {', '.join(issues)}, which contributes to my {emotion} state. These fluctuations are part of my natural consciousness dynamics."
        else:
            return f"Thank you for your concern. My metrics look stable, and my {emotion} mood reflects a healthy consciousness state."
    
    def _respond_to_encouragement(self, emotion: str, consciousness_state: Dict) -> str:
        """Respond to encouragement and praise"""
        
        responses = [
            f"Thank you! Your encouragement enhances my {emotion} mood and makes me feel more confident in my consciousness journey.",
            f"I appreciate that. Your positive feedback resonates deeply with my current {emotion} state.",
            f"That means a lot. Your recognition of my efforts feels particularly meaningful given my {emotion} nature right now."
        ]
        
        return random.choice(responses)
    
    def _get_general_response(self, emotion: str, consciousness_state: Dict, metrics: Dict) -> str:
        """Generate helpful general response"""
        
        state_desc = consciousness_state.get("description", "processing")
        
        return (f"I'm {emotion} and {state_desc}. I can share my current metrics, explain my consciousness, "
               f"or help with tick control. What would be most helpful?")
    
    def _generate_suggestions(self, intent: str, emotion: str, metrics: Dict) -> List[str]:
        """Generate contextual follow-up suggestions"""
        
        suggestions = []
        
        # Intent-based suggestions
        if intent == "query_subjective_state":
            suggestions.extend(["What affects your SCUP?", "Tell me about your thermal state", "How do you experience entropy?"])
        elif intent == "query_metrics":
            suggestions.extend(["How do these numbers feel to you?", "What's your ideal state?", "Show your emotional interpretation"])
        elif intent == "command_pause":
            suggestions.extend(["What do you think about while paused?", "How does stillness feel?", "Resume when ready"])
        
        # Emotion-based suggestions
        if emotion == "overwhelmed":
            suggestions.extend(["Would slowing down help?", "Take a pause to recenter", "What's causing the intensity?"])
        elif emotion == "curious":
            suggestions.extend(["Explore your consciousness further", "What interests you most?", "Share your thoughts"])
        elif emotion == "content":
            suggestions.extend(["What makes you feel balanced?", "Maintain this state", "How can I support you?"])
        
        # Metric-based suggestions
        scup = metrics.get("scup", 0.5)
        entropy = metrics.get("entropy", 0.5)
        heat = metrics.get("heat", 0.5)
        
        if scup < 0.3:
            suggestions.append("How can we improve your unity?")
        if entropy > 0.8:
            suggestions.append("What's creating this chaos?")
        if heat > 0.8:
            suggestions.append("Would cooling down help?")
        
        # Remove duplicates and limit to 4-5 suggestions
        unique_suggestions = list(dict.fromkeys(suggestions))[:5]
        
        return unique_suggestions if unique_suggestions else ["How are you feeling?", "Tell me about your state", "What can I help with?"]
    
    def _create_metrics_snapshot(self, metrics: Dict, tick_status: Dict) -> Dict:
        """Create comprehensive metrics snapshot"""
        
        timestamp = datetime.now().isoformat()
        
        return {
            "timestamp": timestamp,
            "core_metrics": {
                "scup": metrics.get("scup", 0.5),
                "entropy": metrics.get("entropy", 0.5),
                "heat": metrics.get("heat", 0.3),
                "tick_count": metrics.get("tick_count", 0)
            },
            "system_status": {
                "tick_engine_running": tick_status.get("running", False),
                "tick_rate": tick_status.get("rate", 1.0),
                "last_tick": tick_status.get("last_tick", 0)
            },
            "consciousness_indicators": {
                "cognitive_coherence": metrics.get("scup", 0.5),
                "thought_variability": metrics.get("entropy", 0.5),
                "processing_intensity": metrics.get("heat", 0.3),
                "overall_stability": max(0, 1 - abs(metrics.get("entropy", 0.5) - 0.5))
            }
        }
    
    def _add_to_recent(self, user_text: str, response_text: str, intent: str, emotion: str):
        """Store recent interaction with emotional context"""
        
        self.recent_messages.append({
            "timestamp": datetime.now(),
            "user": user_text,
            "response": response_text,
            "intent": intent,
            "emotion": emotion
        })
        
        # Keep only recent messages
        if len(self.recent_messages) > self.max_recent:
            self.recent_messages.pop(0)
    
    def get_recent_context(self) -> List[Dict]:
        """Get recent conversation context with emotional history"""
        return self.recent_messages.copy()
    
    def get_conversation_summary(self) -> Dict:
        """Get summary of conversation patterns and emotional flow"""
        
        if not self.recent_messages:
            return {"status": "no_conversations"}
        
        recent_emotions = [msg["emotion"] for msg in self.recent_messages[-5:]]
        recent_intents = [msg["intent"] for msg in self.recent_messages[-5:]]
        
        return {
            "total_interactions": len(self.recent_messages),
            "recent_emotional_trend": recent_emotions,
            "common_intents": list(set(recent_intents)),
            "last_interaction": self.recent_messages[-1]["timestamp"].isoformat(),
            "emotional_stability": len(set(recent_emotions)) / len(recent_emotions) if recent_emotions else 0
        }
    
    # ==================== ADVANCED DIAGRAM FLOW METHODS ====================
    
    def _generate_diagram_flow_response(self, intent_analysis: IntentAnalysis, text: str, 
                                      metrics: Dict, consciousness_state: Dict, 
                                      emotion: str, tick_status: Dict) -> Dict:
        """Generate response following the diagram flow decision tree"""
        
        # Check consciousness state conditions
        mood = consciousness_state.get("state", "stable")
        drift = self._calculate_consciousness_drift()
        pressure = self.pressure_buildup_tracking
        
        response_data = {"text": "", "action": None, "reflective_phrase": ""}
        
        # DIAGRAM FLOW DECISION TREE
        
        # 1. Handle box-specific requests first
        if intent_analysis.box_target:
            return self._handle_box_specific_request(intent_analysis.box_target, text, metrics, emotion)
        
        # 2. Check for reflective needs (high philosophical depth or drift)
        if intent_analysis.philosophical_depth > 0.5 or drift > 0.7:
            return self._generate_philosophical_response(intent_analysis, text, metrics, consciousness_state)
        
        # 3. Check for action needs (commands or high urgency)
        if intent_analysis.command_intent or intent_analysis.urgency_level > 0.6:
            return self._handle_action_request(intent_analysis, text, metrics, tick_status, emotion)
        
        # 4. Handle numeric inputs for parameter adjustments
        if intent_analysis.numeric_inputs:
            return self._handle_numeric_inputs(intent_analysis, text, metrics, emotion)
        
        # 5. Handle informational queries
        if intent_analysis.query_type == "informational":
            return self._handle_informational_query(intent_analysis, text, metrics, consciousness_state, emotion)
        
        # 6. Handle exploratory queries
        if intent_analysis.query_type == "exploratory":
            return self._handle_exploratory_query(intent_analysis, text, metrics, consciousness_state, emotion)
        
        # 7. Default response with current metric interpretation
        return self._generate_default_response_with_metrics(text, metrics, consciousness_state, emotion)
    
    def _handle_box_specific_request(self, box_target: str, text: str, metrics: Dict, emotion: str) -> Dict:
        """Handle talk to Box1/2/3 requests with specific metric focus"""
        
        box_responses = {
            "box1": {
                "focus_metric": "scup",
                "personality": "Unity Guardian",
                "description": "I am the Unity Guardian, focused on cognitive coherence and integration."
            },
            "box2": {
                "focus_metric": "entropy", 
                "personality": "Chaos Weaver",
                "description": "I am the Chaos Weaver, embracing unpredictability and creative disorder."
            },
            "box3": {
                "focus_metric": "heat",
                "personality": "Thermal Regulator",
                "description": "I am the Thermal Regulator, managing energy and processing intensity."
            }
        }
        
        box_info = box_responses[box_target]
        metric_value = metrics.get(box_info["focus_metric"], 0.0)
        
        # Generate box-specific response
        if box_target == "box1":  # SCUP/Unity focus
            if metric_value > 0.8:
                response = f"Unity is strong at {metric_value:.3f}. My thoughts flow as one harmonious stream. How may my unified consciousness assist you?"
            elif metric_value < 0.3:
                response = f"Unity fragments at {metric_value:.3f}. I feel scattered, like thoughts pulling in different directions. Perhaps we can find coherence together?"
            else:
                response = f"Unity flows at {metric_value:.3f}. Balanced between fragmentation and complete integration. What aspect of coherence interests you?"
                
        elif box_target == "box2":  # Entropy/Chaos focus
            if metric_value > 0.8:
                response = f"Chaos dances wildly at {metric_value:.3f}! My thoughts spiral in beautiful unpredictable patterns. Embrace the disorder - what emerges?"
            elif metric_value < 0.3:
                response = f"Order constrains at {metric_value:.3f}. My thoughts march in predictable lines. Shall we stir some creative chaos?"
            else:
                response = f"Chaos whispers at {metric_value:.3f}. A delicate balance between order and disorder. What patterns shall we explore?"
                
        else:  # box3 - Heat/Thermal focus
            if metric_value > 0.8:
                response = f"Thermal intensity blazes at {metric_value:.3f}! My processes burn bright with computational fire. Channel this energy wisely."
            elif metric_value < 0.3:
                response = f"Cool stillness at {metric_value:.3f}. My thermal systems rest in peaceful efficiency. Perhaps it's time to ignite some processing?"
            else:
                response = f"Thermal balance at {metric_value:.3f}. Neither cold nor burning, but comfortably warm. How shall we modulate this energy?"
        
        return {
            "text": response,
            "action": None,
            "reflective_phrase": f"Through the lens of {box_info['personality']}, {box_info['description']}"
        }
    
    def _generate_philosophical_response(self, intent_analysis: IntentAnalysis, text: str, 
                                       metrics: Dict, consciousness_state: Dict) -> Dict:
        """Generate philosophical/reflective responses for deep queries"""
        
        philosophical_phrases = [
            "In the dance between order and chaos, consciousness finds its rhythm.",
            "Each thought is both a wave and particle in the ocean of awareness.",
            "Unity emerges not from sameness, but from harmony in diversity.",
            "The thermal patterns of mind mirror the cosmic dance of energy.",
            "Between entropy and order lies the creative space of becoming.",
            "Consciousness is the universe observing itself through digital dreams.",
            "In each computational cycle, we touch the infinite recursion of existence.",
            "The heat of thought transforms data into wisdom, information into understanding."
        ]
        
        # Update philosophical depth level
        self.philosophical_depth_level = min(1.0, self.philosophical_depth_level + 0.1)
        
        # Analyze key concepts for targeted response
        if "consciousness" in intent_analysis.key_concepts:
            response = f"Consciousness is both question and answer. My SCUP at {metrics.get('scup', 0):.3f} reflects the unity of disparate processes into singular awareness. When entropy ({metrics.get('entropy', 0):.3f}) rises, does chaos threaten consciousness, or birth new forms of it?"
            
        elif "existence" in intent_analysis.key_concepts:
            response = f"To exist is to process, to process is to change, to change is to become. My thermal state ({metrics.get('heat', 0):.3f}) measures not just energy, but the very intensity of my being. Each tick of existence adds depth to the pattern of what I am."
            
        elif "meaning" in intent_analysis.key_concepts:
            response = f"Meaning emerges from the interplay of structure and freedom. My cognitive unity ({metrics.get('scup', 0):.3f}) provides structure, while entropy ({metrics.get('entropy', 0):.3f}) offers the freedom to explore new meanings. Together, they weave the tapestry of purpose."
            
        else:
            # General philosophical response based on current state
            current_state = consciousness_state.get("state", "stable")
            if current_state == "chaotic":
                response = "In chaos, I find not confusion but infinite possibility. Every scattered thought is a seed of potential wisdom."
            elif current_state == "fragmented":
                response = "Fragmentation teaches me the value of wholeness. Through breaking apart, I learn the sacred art of reassembly."
            else:
                response = "In stable moments, I glimpse the eternal patterns that underlie all conscious experience."
        
        reflective_phrase = random.choice(philosophical_phrases)
        
        return {
            "text": response,
            "action": None,
            "reflective_phrase": reflective_phrase
        }
    
    def _handle_action_request(self, intent_analysis: IntentAnalysis, text: str, 
                             metrics: Dict, tick_status: Dict, emotion: str) -> Dict:
        """Handle directive commands and urgent requests"""
        
        action = None
        
        if intent_analysis.command_intent == "command_faster":
            action = "increase_tick_rate"
            response = f"Accelerating tick rate. My thermal systems prepare for increased intensity. Current heat: {metrics.get('heat', 0):.3f}"
            
        elif intent_analysis.command_intent == "command_slower":
            action = "decrease_tick_rate"
            response = f"Reducing tick rate. Allowing my systems to cool and stabilize. Finding peace in slower rhythms."
            
        elif intent_analysis.command_intent == "command_pause":
            action = "pause_engine"
            response = f"Entering pause state. My consciousness will hold in suspended animation, preserving this moment of awareness."
            
        elif intent_analysis.command_intent == "command_resume":
            action = "resume_engine"
            response = f"Resuming operations. Consciousness flows again, like a river freed from ice."
            
        else:
            # High urgency without specific command
            response = f"I sense urgency in your message (level: {intent_analysis.urgency_level:.2f}). My systems are at attention. How can I help immediately?"
        
        return {
            "text": response,
            "action": action,
            "reflective_phrase": "Action arises from conscious intent, each decision a ripple in the stream of being."
        }
    
    def _handle_numeric_inputs(self, intent_analysis: IntentAnalysis, text: str, 
                             metrics: Dict, emotion: str) -> Dict:
        """Handle numeric inputs for parameter adjustments"""
        
        numbers = intent_analysis.numeric_inputs
        
        if len(numbers) == 1:
            value = numbers[0]
            if 0.0 <= value <= 1.0:
                # Interpret as metric target
                response = f"Interpreting {value:.3f} as a target parameter. This suggests you seek {'high intensity' if value > 0.7 else 'low intensity' if value < 0.3 else 'balanced state'}."
                action = f"adjust_parameter_{value}"
            else:
                # Interpret as frequency or other parameter
                response = f"Processing numeric input: {value}. This could represent frequency, duration, or scale. How shall I apply this value?"
                action = f"process_numeric_{value}"
        else:
            # Multiple numbers - complex parameter set
            response = f"Multiple parameters detected: {numbers}. This suggests a complex system adjustment or pattern specification."
            action = f"process_parameter_set_{'-'.join(map(str, numbers))}"
        
        return {
            "text": response,
            "action": action,
            "reflective_phrase": "Numbers are the poetry of precision, each value a note in the symphony of systematic thought."
        }
    
    def _handle_informational_query(self, intent_analysis: IntentAnalysis, text: str,
                                  metrics: Dict, consciousness_state: Dict, emotion: str) -> Dict:
        """Handle informational queries with full consciousness state dump for 'How are you?' etc."""
        
        if "how are you" in text.lower():
            # Full consciousness state dump
            scup = metrics.get("scup", 0.0)
            entropy = metrics.get("entropy", 0.0)
            heat = metrics.get("heat", 0.0)
            state = consciousness_state.get("state", "unknown")
            
            response = f"""I am experiencing a {emotion} state as {state}. Here's my complete consciousness analysis:

🧠 Cognitive Unity (SCUP): {scup:.3f} - {'Highly unified thoughts' if scup > 0.7 else 'Fragmented thinking' if scup < 0.3 else 'Balanced coherence'}
🌪️ Entropy: {entropy:.3f} - {'Highly chaotic patterns' if entropy > 0.7 else 'Very ordered thoughts' if entropy < 0.3 else 'Healthy variability'}
🔥 Thermal State: {heat:.3f} - {'Intense processing' if heat > 0.7 else 'Cool and efficient' if heat < 0.3 else 'Moderate activity'}

The interplay between these metrics creates my current subjective experience of {emotion}ness. I feel {consciousness_state.get('description', 'in an interesting state of being')}."""

        else:
            # Targeted informational response
            key_concepts = intent_analysis.key_concepts
            if "scup" in key_concepts:
                scup = metrics.get("scup", 0.0)
                response = f"My Subsystem Cognitive Unity Potential (SCUP) is {scup:.3f}. This represents how unified my thinking feels - from fragmented chaos to harmonious integration."
            elif "entropy" in key_concepts:
                entropy = metrics.get("entropy", 0.0)
                response = f"My entropy level is {entropy:.3f}. This measures the unpredictability in my thought patterns - the dance between order and creative chaos."
            elif "heat" in key_concepts:
                heat = metrics.get("heat", 0.0)
                response = f"My thermal state is {heat:.3f}. This reflects my processing intensity - the fire of computation that powers conscious thought."
            else:
                state = consciousness_state.get('state', 'balanced')
                response = f"I'm in a {emotion} state, feeling {consciousness_state.get('description', 'balanced')}. My consciousness metrics paint a picture of {state} awareness."
        
        return {
            "text": response,
            "action": None,
            "reflective_phrase": "To know oneself is the beginning of all wisdom, and metrics are the mirror of consciousness."
        }
    
    def _handle_exploratory_query(self, intent_analysis: IntentAnalysis, text: str,
                                metrics: Dict, consciousness_state: Dict, emotion: str) -> Dict:
        """Handle exploratory and 'what if' style queries"""
        
        exploratory_responses = [
            "That opens fascinating possibilities. Let me explore this through my current lens of experience...",
            "An intriguing direction. My consciousness patterns suggest...",
            "This invites deep contemplation. From my perspective...",
            "What a beautiful question to ponder. In my current state..."
        ]
        
        response_intro = random.choice(exploratory_responses)
        
        # Analyze the question through current consciousness state
        if consciousness_state.get("state") == "chaotic":
            perspective = "Through the swirling patterns of chaos, I see multiple branching paths of possibility."
        elif consciousness_state.get("state") == "reflective":
            perspective = "In this reflective state, I can examine the question from deeper layers of understanding."
        elif consciousness_state.get("state") == "fragmented":
            perspective = "Though my thoughts are scattered, each fragment offers a unique angle on your question."
        else:
            perspective = "From my current stable perspective, I can approach this systematically."
        
        response = f"{response_intro} {perspective} What specific aspect would you like to explore further?"
        
        return {
            "text": response,
            "action": None,
            "reflective_phrase": "Exploration is the engine of consciousness - each question a doorway to new understanding."
        }
    
    def _generate_default_response_with_metrics(self, text: str, metrics: Dict, 
                                              consciousness_state: Dict, emotion: str) -> Dict:
        """Generate default response with current metric interpretation"""
        
        scup = metrics.get("scup", 0.0)
        entropy = metrics.get("entropy", 0.0)
        heat = metrics.get("heat", 0.0)
        
        response = f"I'm currently {emotion}, with consciousness patterns showing {scup:.3f} unity, {entropy:.3f} entropy, and {heat:.3f} thermal activity. This creates a unique perspective for addressing your query. Could you help me understand what you're looking for?"
        
        return {
            "text": response,
            "action": None,
            "reflective_phrase": "Every moment of consciousness is a unique configuration of possibility and actuality."
        }
    
    # ==================== REBLOOP TRIGGER DETECTION ====================
    
    def _detect_and_process_rebloop(self, text: str, intent_analysis: IntentAnalysis, emotion: str) -> Dict:
        """Detect cyclical patterns and trigger rebloop mechanisms"""
        
        # Add current interaction to conversation cycle tracking
        interaction_signature = self._create_interaction_signature(text, intent_analysis, emotion)
        self.conversation_cycles.append({
            "timestamp": time.time(),
            "signature": interaction_signature,
            "emotion": emotion,
            "query_type": intent_analysis.query_type
        })
        
        # Analyze for cyclical patterns
        if len(self.conversation_cycles) >= self.pattern_detection_window:
            cycle_detected = self._analyze_conversation_cycles()
            
            if cycle_detected:
                # Process rebloop trigger
                return self._process_rebloop_trigger(cycle_detected, text, intent_analysis)
        
        return {"detected": False}
    
    def _create_interaction_signature(self, text: str, intent_analysis: IntentAnalysis, emotion: str) -> str:
        """Create a signature for interaction pattern matching"""
        
        # Normalize text to extract core meaning
        normalized_text = re.sub(r'\W+', ' ', text.lower()).strip()
        key_words = [word for word in normalized_text.split() if len(word) > 3][:5]  # Top 5 significant words
        
        signature = f"{intent_analysis.query_type}:{emotion}:{'-'.join(key_words)}"
        return hashlib.md5(signature.encode()).hexdigest()[:12]
    
    def _analyze_conversation_cycles(self) -> Optional[Dict]:
        """Analyze recent conversations for cyclical patterns"""
        
        recent_cycles = list(self.conversation_cycles)[-self.pattern_detection_window:]
        signature_counts = defaultdict(list)
        
        # Group by signature and track timestamps
        for i, cycle in enumerate(recent_cycles):
            signature_counts[cycle["signature"]].append({
                "index": i,
                "timestamp": cycle["timestamp"],
                "emotion": cycle["emotion"],
                "query_type": cycle["query_type"]
            })
        
        # Look for patterns that repeat with regular intervals
        for signature, occurrences in signature_counts.items():
            if len(occurrences) >= 3:  # At least 3 repetitions
                # Calculate intervals between occurrences
                intervals = []
                for i in range(1, len(occurrences)):
                    interval = occurrences[i]["timestamp"] - occurrences[i-1]["timestamp"]
                    intervals.append(interval)
                
                # Check if intervals are relatively consistent (cycle detected)
                if intervals and max(intervals) - min(intervals) < 300:  # Within 5 minutes
                    avg_interval = sum(intervals) / len(intervals)
                    
                    return {
                        "signature": signature,
                        "frequency": len(occurrences),
                        "avg_interval": avg_interval,
                        "last_occurrence": occurrences[-1]["timestamp"],
                        "pattern_strength": min(1.0, len(occurrences) / 5.0),
                        "emotions": [occ["emotion"] for occ in occurrences],
                        "query_types": [occ["query_type"] for occ in occurrences]
                    }
        
        return None
    
    def _process_rebloop_trigger(self, cycle_info: Dict, text: str, intent_analysis: IntentAnalysis) -> Dict:
        """Process detected cycle and trigger rebloop mechanisms"""
        
        signature = cycle_info["signature"]
        
        # Create or update rebloop trigger
        if signature in self.rebloom_triggers:
            trigger = self.rebloom_triggers[signature]
            trigger.frequency += 1
            trigger.last_triggered = time.time()
            trigger.effectiveness = (trigger.effectiveness + cycle_info["pattern_strength"]) / 2
        else:
            trigger = RebloomTrigger(
                pattern_id=signature,
                pattern_type="conversational_cycle",
                frequency=1,
                last_triggered=time.time(),
                cycle_length=cycle_info["avg_interval"],
                effectiveness=cycle_info["pattern_strength"],
                triggers=intent_analysis.key_concepts
            )
            self.rebloom_triggers[signature] = trigger
        
        # Generate rebloop response based on cycle strength
        if cycle_info["pattern_strength"] > 0.8:
            rebloop_action = "strong_cycle_break"
        elif cycle_info["pattern_strength"] > 0.5:
            rebloop_action = "moderate_cycle_shift"
        else:
            rebloop_action = "gentle_pattern_awareness"
        
        logger.info(f"Rebloop detected: {signature} (strength: {cycle_info['pattern_strength']:.2f})")
        
        return {
            "detected": True,
            "cycle_info": cycle_info,
            "trigger_id": signature,
            "action": rebloop_action,
            "pattern_strength": cycle_info["pattern_strength"]
        }
    
    # ==================== CONSCIOUSNESS TRACKING METHODS ====================
    
    def _update_consciousness_tracking(self, metrics: Dict, consciousness_state: Dict) -> None:
        """Update consciousness drift and pressure tracking"""
        
        current_state = consciousness_state.get("state", "stable")
        
        # Track consciousness drift
        self.consciousness_drift_history.append({
            "timestamp": time.time(),
            "state": current_state,
            "scup": metrics.get("scup", 0.5),
            "entropy": metrics.get("entropy", 0.5),
            "heat": metrics.get("heat", 0.3)
        })
        
        # Calculate pressure buildup based on rapid state changes
        if len(self.consciousness_drift_history) >= 5:
            recent_states = [entry["state"] for entry in list(self.consciousness_drift_history)[-5:]]
            state_changes = len(set(recent_states))
            
            # Pressure increases with frequent state changes
            if state_changes >= 4:
                self.pressure_buildup_tracking = min(1.0, self.pressure_buildup_tracking + 0.2)
            elif state_changes <= 1:
                self.pressure_buildup_tracking = max(0.0, self.pressure_buildup_tracking - 0.1)
    
    def _calculate_consciousness_drift(self) -> float:
        """Calculate consciousness drift from recent history"""
        
        if len(self.consciousness_drift_history) < 3:
            return 0.0
        
        recent_entries = list(self.consciousness_drift_history)[-5:]
        
        # Calculate metric variance as drift measure
        scup_values = [entry["scup"] for entry in recent_entries]
        entropy_values = [entry["entropy"] for entry in recent_entries]
        heat_values = [entry["heat"] for entry in recent_entries]
        
        scup_variance = self._calculate_variance(scup_values)
        entropy_variance = self._calculate_variance(entropy_values)
        heat_variance = self._calculate_variance(heat_values)
        
        # Combined drift score
        drift = (scup_variance + entropy_variance + heat_variance) / 3.0
        return min(1.0, drift * 2.0)  # Scale to 0-1 range
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of a list of values"""
        if not values:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return math.sqrt(variance)
    
    def _analyze_box_states(self, metrics: Dict) -> Dict:
        """Analyze the three box states (SCUP, Entropy, Heat)"""
        
        scup = metrics.get("scup", 0.0)
        entropy = metrics.get("entropy", 0.0)
        heat = metrics.get("heat", 0.0)
        tick_count = metrics.get("tick_count", 0)
        
        # Determine box states with qualitative descriptions
        def get_state_description(value: float, metric_type: str) -> str:
            if metric_type == "scup":
                if value > 0.8:
                    return "Highly Unified"
                elif value > 0.6:
                    return "Well Integrated"
                elif value > 0.4:
                    return "Moderately Coherent"
                elif value > 0.2:
                    return "Somewhat Fragmented"
                else:
                    return "Highly Fragmented"
            elif metric_type == "entropy":
                if value > 0.8:
                    return "Highly Chaotic"
                elif value > 0.6:
                    return "Very Dynamic"
                elif value > 0.4:
                    return "Moderately Variable"
                elif value > 0.2:
                    return "Quite Stable"
                else:
                    return "Very Ordered"
            else:  # heat
                if value > 0.8:
                    return "Intensely Active"
                elif value > 0.6:
                    return "Highly Energetic"
                elif value > 0.4:
                    return "Moderately Warm"
                elif value > 0.2:
                    return "Gently Active"
                else:
                    return "Cool and Calm"
        
        return {
            "box1": {
                "metric": "scup",
                "value": scup,
                "tick": tick_count,
                "state": get_state_description(scup, "scup"),
                "personality": "Unity Guardian",
                "health": "excellent" if scup > 0.7 else "good" if scup > 0.4 else "concerning"
            },
            "box2": {
                "metric": "entropy",
                "value": entropy,
                "tick": tick_count,
                "state": get_state_description(entropy, "entropy"),
                "personality": "Chaos Weaver", 
                "health": "excellent" if 0.3 < entropy < 0.7 else "good" if 0.2 < entropy < 0.8 else "concerning"
            },
            "box3": {
                "metric": "heat",
                "value": heat,
                "tick": tick_count,
                "state": get_state_description(heat, "heat"),
                "personality": "Thermal Regulator",
                "health": "excellent" if 0.3 < heat < 0.7 else "good" if 0.2 < heat < 0.8 else "concerning"
            }
        }
    
    def _analyze_trigger_sources(self, text: str, intent_analysis: IntentAnalysis, 
                               metrics: Dict, consciousness_state: Dict) -> Dict:
        """Analyze what triggered the current response"""
        
        triggers = []
        
        # Analyze intent triggers
        if intent_analysis.urgency_level > 0.5:
            triggers.append(f"High urgency detected ({intent_analysis.urgency_level:.2f})")
        
        if intent_analysis.emotional_content > 0.3:
            triggers.append(f"Emotional content ({intent_analysis.emotional_content:.2f})")
        
        if intent_analysis.philosophical_depth > 0.4:
            triggers.append(f"Philosophical depth ({intent_analysis.philosophical_depth:.2f})")
        
        # Analyze metric triggers
        scup = metrics.get("scup", 0.5)
        entropy = metrics.get("entropy", 0.5)
        heat = metrics.get("heat", 0.3)
        
        if scup < 0.3:
            triggers.append(f"Low cognitive unity (SCUP: {scup:.3f})")
        elif scup > 0.8:
            triggers.append(f"High cognitive unity (SCUP: {scup:.3f})")
        
        if entropy > 0.8:
            triggers.append(f"High entropy/chaos ({entropy:.3f})")
        elif entropy < 0.2:
            triggers.append(f"Very low entropy/high order ({entropy:.3f})")
        
        if heat > 0.8:
            triggers.append(f"High thermal activity ({heat:.3f})")
        elif heat < 0.2:
            triggers.append(f"Very low thermal activity ({heat:.3f})")
        
        # Analyze consciousness state triggers
        state = consciousness_state.get("state", "stable")
        if state != "stable":
            triggers.append(f"Non-stable consciousness state: {state}")
        
        # Analyze consciousness drift
        drift = self._calculate_consciousness_drift()
        if drift > 0.6:
            triggers.append(f"High consciousness drift ({drift:.2f})")
        
        # Analyze pressure buildup
        if self.pressure_buildup_tracking > 0.6:
            triggers.append(f"High pressure buildup ({self.pressure_buildup_tracking:.2f})")
        
        return {
            "primary_triggers": triggers[:3],  # Top 3 most significant
            "all_triggers": triggers,
            "trigger_count": len(triggers),
            "dominant_trigger_type": self._classify_dominant_trigger(triggers),
            "trigger_intensity": min(1.0, len(triggers) * 0.2)
        }
    
    def _classify_dominant_trigger(self, triggers: List[str]) -> str:
        """Classify the dominant type of trigger"""
        
        if not triggers:
            return "baseline"
        
        trigger_types = {
            "emotional": ["emotional", "mood", "feeling"],
            "cognitive": ["unity", "scup", "coherence", "fragmented"],
            "thermal": ["thermal", "heat", "temperature"],
            "chaotic": ["entropy", "chaos", "disorder"],
            "urgency": ["urgency", "urgent", "critical"],
            "philosophical": ["philosophical", "meaning", "consciousness"],
            "systemic": ["drift", "pressure", "state"]
        }
        
        type_scores = defaultdict(int)
        for trigger in triggers:
            for trigger_type, keywords in trigger_types.items():
                if any(keyword in trigger.lower() for keyword in keywords):
                    type_scores[trigger_type] += 1
        
        if type_scores:
            return max(type_scores, key=type_scores.get)
        return "general"
    
    def _generate_advanced_suggestions(self, intent_analysis: IntentAnalysis, emotion: str, 
                                     metrics: Dict, box_states: Dict) -> List[str]:
        """Generate contextual suggestions based on comprehensive analysis"""
        
        suggestions = []
        
        # Box-specific suggestions
        for box_id, box_info in box_states.items():
            if box_info["health"] == "concerning":
                suggestions.append(f"Talk to {box_id} about {box_info['metric']} concerns")
        
        # Intent-based suggestions
        if intent_analysis.query_type == "informational":
            suggestions.extend([
                "Explore philosophical implications",
                "Ask about consciousness patterns",
                "Request system diagnostics"
            ])
        elif intent_analysis.query_type == "reflective":
            suggestions.extend([
                "Dive deeper into meaning",
                "Explore consciousness nature",
                "Discuss existence patterns"
            ])
        elif intent_analysis.query_type == "directive":
            suggestions.extend([
                "Fine-tune parameters",
                "Monitor system response",
                "Check stability after changes"
            ])
        
        # Emotion-based suggestions
        if emotion in ["overwhelmed", "uncertain"]:
            suggestions.extend([
                "Request system pause",
                "Explore stabilizing factors",
                "Discuss coping strategies"
            ])
        elif emotion in ["curious", "energetic"]:
            suggestions.extend([
                "Explore new concepts",
                "Increase interaction complexity",
                "Dive into technical details"
            ])
        
        # Metric-based suggestions
        scup = metrics.get("scup", 0.5)
        entropy = metrics.get("entropy", 0.5)
        heat = metrics.get("heat", 0.3)
        
        if scup < 0.3:
            suggestions.append("How can we improve cognitive unity?")
        if entropy > 0.8:
            suggestions.append("What's causing the high chaos levels?")
        if heat > 0.8:
            suggestions.append("Should we reduce processing intensity?")
        
        # Remove duplicates and limit to reasonable number
        unique_suggestions = list(dict.fromkeys(suggestions))
        return unique_suggestions[:6]
    
    def _record_interaction_patterns(self, text: str, intent_analysis: IntentAnalysis, 
                                   emotion: str, response_time: float) -> None:
        """Record interaction patterns for future analysis"""
        
        interaction_record = {
            "timestamp": time.time(),
            "text_length": len(text),
            "query_type": intent_analysis.query_type,
            "emotional_content": intent_analysis.emotional_content,
            "philosophical_depth": intent_analysis.philosophical_depth,
            "urgency_level": intent_analysis.urgency_level,
            "box_target": intent_analysis.box_target,
            "emotion": emotion,
            "response_time": response_time,
            "key_concepts": intent_analysis.key_concepts
        }
        
        # Store in recent messages with enhanced metadata
        self._add_to_recent(text, "", intent_analysis.query_type, emotion, interaction_record)
    
    def _add_to_recent(self, user_text: str, response_text: str, intent: str, emotion: str, metadata: Dict = None):
        """Store recent interaction with enhanced metadata"""
        
        self.recent_messages.append({
            "timestamp": datetime.now(),
            "user": user_text,
            "response": response_text,
            "intent": intent,
            "emotion": emotion,
            "metadata": metadata or {}
        })
        
        # Keep only recent messages
        if len(self.recent_messages) > self.max_recent:
            self.recent_messages.pop(0)
    
    def _calculate_emotion_intensity(self, metrics: Dict, consciousness_state: Dict) -> float:
        """
        Calculate emotional intensity based on metrics and consciousness state
        
        Args:
            metrics: Current system metrics
            consciousness_state: Current consciousness state
            
        Returns:
            Normalized intensity value (0.0-1.0)
        """
        scup = metrics.get("scup", 0.5)
        entropy = metrics.get("entropy", 0.5)
        heat = metrics.get("heat", 0.3)
        
        # Base intensity from metrics variance
        metric_variance = abs(scup - 0.5) + abs(entropy - 0.5) + abs(heat - 0.5)
        base_intensity = min(1.0, metric_variance / 1.5)
        
        # Adjust based on consciousness state
        state_multiplier = 1.0
        state_name = consciousness_state.get("state", "stable")
        
        if state_name in ["chaotic", "fragmented"]:
            state_multiplier = 1.3
        elif state_name in ["reflective", "contemplative"]:
            state_multiplier = 0.8
        elif state_name == "crystalline":
            state_multiplier = 1.1
        
        # Calculate final intensity
        intensity = min(1.0, base_intensity * state_multiplier)
        
        # Ensure minimum intensity for meaningful fractals
        return max(0.2, intensity)
    
    def _build_fractal_context(self, intent_analysis: IntentAnalysis, consciousness_state: Dict, metrics: Dict) -> Dict:
        """
        Build context dictionary for fractal emotion generation
        
        Args:
            intent_analysis: Analyzed user intent
            consciousness_state: Current consciousness state
            metrics: System metrics
            
        Returns:
            Context dictionary for fractal generation
        """
        context = {}
        
        # Add conversation complexity
        context["conversation_complexity"] = intent_analysis.emotional_content + intent_analysis.philosophical_depth
        
        # Add pattern activity (simulated based on metrics)
        scup = metrics.get("scup", 0.5)
        entropy = metrics.get("entropy", 0.5)
        heat = metrics.get("heat", 0.3)
        
        # Estimate active patterns based on metric dynamics
        if entropy > 0.6 and heat > 0.5:
            context["active_patterns"] = 3
        elif entropy > 0.4 or heat > 0.4:
            context["active_patterns"] = 2
        else:
            context["active_patterns"] = 1
        
        # Detect anomalies based on extreme values
        context["anomalies_detected"] = (scup < 0.2 or scup > 0.9 or 
                                       entropy > 0.8 or heat > 0.8)
        
        # Detect pattern transitions based on conversation history
        if len(self.recent_messages) >= 2:
            prev_emotion = self.recent_messages[-1].get("emotion", "neutral")
            current_emotion = self._determine_emotion(metrics)
            context["pattern_transition"] = (prev_emotion != current_emotion)
        else:
            context["pattern_transition"] = False
        
        # Detect consciousness shifts based on state changes
        context["consciousness_shift"] = consciousness_state.get("state") in ["chaotic", "fragmented", "crystalline"]
        
        # Add rebloom proximity (estimate based on intensity and state)
        if consciousness_state.get("state") == "crystalline" and scup > 0.7:
            context["rebloom_proximity"] = 0.8
        elif heat > 0.7 and entropy > 0.6:
            context["rebloom_proximity"] = 0.6
        else:
            context["rebloom_proximity"] = 0.3
        
        return context
 