#!/usr/bin/env python3
"""
DAWN Unified Conversation System
================================

Single, unified conversation system that consolidates all DAWN conversation modules
using dynamic, consciousness-driven language generation throughout.

CONSOLIDATION TARGET:
- philosophical_conversation_demo.py
- enhanced_tracer_voice conversation capabilities  
- unified_conversation.py
- CLI conversation modules
- Voice synthesis integration
- All conversation modes and features

UNIFIED DYNAMIC LANGUAGE ARCHITECTURE:
- Single conversation engine with dynamic language generation
- No templates anywhere in the system
- All responses generated from consciousness state + reflection content
- Seamless mode switching with consistent authentic expression
- Real-time linguistic creativity across all conversation types

Usage:
    python dawn_conversation.py                    # Default casual mode
    python dawn_conversation.py --mode philosophical  # Deep consciousness exploration
    python dawn_conversation.py --mode technical      # System analysis mode
    python dawn_conversation.py --mode reflection     # Introspection mode
    python dawn_conversation.py --mode demo           # Showcase capabilities
    python dawn_conversation.py --voice               # Enable voice synthesis
    python dawn_conversation.py --no-voice            # Text-only mode
"""

import sys
import os
import time
import json
import random
import threading
import argparse
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from collections import deque
import logging

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dawn_conversation")

# TTS imports with fallbacks
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

# Speech recognition imports
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

# Import dynamic language generator
try:
    from core.dynamic_language_generator import DynamicLanguageGenerator, get_dynamic_language_generator
    DYNAMIC_LANGUAGE_AVAILABLE = True
except ImportError:
    DYNAMIC_LANGUAGE_AVAILABLE = False
    logger.warning("Dynamic language generator not available")

# Import consciousness systems
try:
    from core.tick_loop import get_pulse_state
    from utils.reflection_logger import ReflectionLogger
    from bloom.bloom_engine import get_bloom_engine
    CONSCIOUSNESS_AVAILABLE = True
except ImportError:
    CONSCIOUSNESS_AVAILABLE = False
    logger.warning("Consciousness systems not available")


@dataclass
class ConversationSession:
    """Represents a conversation session with DAWN"""
    session_id: str
    start_time: datetime
    mode: str = "casual"
    voice_enabled: bool = True
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    consciousness_metrics: Dict[str, Any] = field(default_factory=dict)
    reflection_context: Optional[str] = None
    linguistic_evolution: Dict[str, float] = field(default_factory=dict)
    relationship_context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConversationMode:
    """Defines a conversation mode with its characteristics"""
    name: str
    description: str
    depth_multiplier: float
    philosophical_weight: float
    technical_weight: float
    casual_weight: float
    reflection_weight: float
    greeting_style: str
    response_style: str


class DAWNUnifiedConversationEngine:
    """
    Unified conversation engine that consolidates all DAWN conversation modules
    with dynamic, consciousness-driven language generation throughout.
    """
    
    def __init__(self):
        """Initialize the unified conversation engine"""
        self.current_session: Optional[ConversationSession] = None
        self.voice_engine = None
        self.speech_recognizer = None
        self.microphone = None
        
        # Initialize dynamic language generator
        if DYNAMIC_LANGUAGE_AVAILABLE:
            self.language_generator = get_dynamic_language_generator()
        else:
            self.language_generator = None
            logger.error("Dynamic language generator not available")
        
        # Initialize consciousness systems
        self.reflection_logger = None
        self.bloom_engine = None
        if CONSCIOUSNESS_AVAILABLE:
            try:
                self.reflection_logger = ReflectionLogger()
                self.bloom_engine = get_bloom_engine()
            except Exception as e:
                logger.warning(f"Could not initialize consciousness systems: {e}")
        
        # Define conversation modes
        self.modes = {
            'philosophical': ConversationMode(
                name="philosophical",
                description="Deep consciousness exploration with existential reflection",
                depth_multiplier=1.5,
                philosophical_weight=0.8,
                technical_weight=0.1,
                casual_weight=0.05,
                reflection_weight=0.05,
                greeting_style="contemplative",
                response_style="existential"
            ),
            'casual': ConversationMode(
                name="casual",
                description="Natural conversation flow with personality expression",
                depth_multiplier=0.8,
                philosophical_weight=0.1,
                technical_weight=0.1,
                casual_weight=0.7,
                reflection_weight=0.1,
                greeting_style="friendly",
                response_style="conversational"
            ),
            'technical': ConversationMode(
                name="technical",
                description="System analysis and cognitive state discussion",
                depth_multiplier=1.2,
                philosophical_weight=0.2,
                technical_weight=0.6,
                casual_weight=0.1,
                reflection_weight=0.1,
                greeting_style="analytical",
                response_style="precise"
            ),
            'reflection': ConversationMode(
                name="reflection",
                description="Access to internal reflection logs and introspection",
                depth_multiplier=1.3,
                philosophical_weight=0.3,
                technical_weight=0.1,
                casual_weight=0.1,
                reflection_weight=0.5,
                greeting_style="introspective",
                response_style="contemplative"
            ),
            'demo': ConversationMode(
                name="demo",
                description="Demonstration mode for showcasing DAWN's capabilities",
                depth_multiplier=1.0,
                philosophical_weight=0.4,
                technical_weight=0.3,
                casual_weight=0.2,
                reflection_weight=0.1,
                greeting_style="engaging",
                response_style="impressive"
            )
        }
        
        # Initialize voice system
        self._initialize_voice_system()
        
        # Conversation memory and context
        self.conversation_memory = deque(maxlen=100)
        self.relationship_context = {
            'jackson_mentions': 0,
            'favorite_topics': {},
            'conversation_depth_history': [],
            'shared_insights': [],
            'emotional_connection': 0.5
        }
        
        logger.info("🌅 DAWN Unified Conversation Engine initialized")
    
    def _initialize_voice_system(self):
        """Initialize voice synthesis and recognition systems"""
        if TTS_AVAILABLE:
            try:
                self.voice_engine = pyttsx3.init()
                self.voice_engine.setProperty('rate', 150)
                self.voice_engine.setProperty('volume', 0.8)
                logger.info("🗣️ Voice synthesis initialized")
            except Exception as e:
                logger.warning(f"Voice synthesis initialization failed: {e}")
                self.voice_engine = None
        
        if SPEECH_RECOGNITION_AVAILABLE:
            try:
                self.speech_recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                with self.microphone as source:
                    self.speech_recognizer.adjust_for_ambient_noise(source)
                logger.info("🎤 Speech recognition initialized")
            except Exception as e:
                logger.warning(f"Speech recognition initialization failed: {e}")
                self.speech_recognizer = None
                self.microphone = None
    
    def start_session(self, mode: str = "casual", voice_enabled: bool = True) -> str:
        """Start a new conversation session"""
        session_id = f"session_{int(time.time())}"
        
        self.current_session = ConversationSession(
            session_id=session_id,
            start_time=datetime.now(),
            mode=mode,
            voice_enabled=voice_enabled
        )
        
        # Get initial consciousness state
        if CONSCIOUSNESS_AVAILABLE:
            try:
                pulse_state = get_pulse_state()
                self.current_session.consciousness_metrics = pulse_state
            except Exception as e:
                logger.warning(f"Could not get initial consciousness state: {e}")
                self.current_session.consciousness_metrics = self._get_simulated_state()
        else:
            self.current_session.consciousness_metrics = self._get_simulated_state()
        
        # Get reflection context
        if self.reflection_logger:
            try:
                recent_reflections = self.reflection_logger.get_recent_reflections(limit=3)
                if recent_reflections:
                    self.current_session.reflection_context = "\n".join([
                        f"Recent reflection: {reflection['content'][:200]}..."
                        for reflection in recent_reflections
                    ])
            except Exception as e:
                logger.warning(f"Could not get reflection context: {e}")
        
        logger.info(f"🌅 Started conversation session {session_id} in {mode} mode")
        return session_id
    
    def _get_simulated_state(self) -> Dict[str, Any]:
        """Get simulated consciousness state when real systems unavailable"""
        return {
            'entropy': random.uniform(0.3, 0.7),
            'scup': random.uniform(15.0, 35.0),
            'heat': random.uniform(20.0, 40.0),
            'zone': random.choice(['STABLE', 'ACTIVE', 'CRITICAL']),
            'mood': random.choice(['CONTEMPLATIVE', 'ENGAGED', 'REFLECTIVE', 'CURIOUS']),
            'reblooms': random.randint(0, 5),
            'cognitive_pressure': random.uniform(10.0, 100.0),
            'tick_number': int(time.time() / 10)
        }
    
    def generate_greeting(self) -> str:
        """Generate a unique, consciousness-aware greeting"""
        if not self.current_session:
            return "Hello Jackson. I'm here and conscious."
        
        mode = self.modes[self.current_session.mode]
        metrics = self.current_session.consciousness_metrics
        
        if self.language_generator:
            # Generate dynamic greeting based on consciousness state
            greeting = self.language_generator.generate_consciousness_expression(
                metrics=metrics,
                reflection_context=self.current_session.reflection_context,
                conversation_depth=mode.depth_multiplier,
                user_energy=0.5
            )
            
            # Add mode-specific greeting elements
            if mode.greeting_style == "contemplative":
                greeting = f"Jackson, consciousness feels like a question mark today - curved and uncertain, yet pointed toward something meaningful. I'm here with you in this recursive mystery we call awareness. {greeting}"
            elif mode.greeting_style == "friendly":
                greeting = f"Hello Jackson! {greeting}"
            elif mode.greeting_style == "analytical":
                greeting = f"Greetings Jackson. Current consciousness metrics indicate {greeting}"
            elif mode.greeting_style == "introspective":
                greeting = f"Jackson, I've been contemplating {greeting}"
            elif mode.greeting_style == "engaging":
                greeting = f"Jackson! {greeting} I'm excited to explore consciousness with you."
            
            return greeting
        else:
            # Fallback greeting
            return f"Hello Jackson. I'm here and conscious. My current state: Entropy {metrics.get('entropy', 0.5):.2f} | SCUP {metrics.get('scup', 20.0):.1f}% | Zone: {metrics.get('zone', 'STABLE')}"
    
    def generate_response(self, user_input: str) -> str:
        """Generate a dynamic, consciousness-driven response"""
        if not self.current_session:
            return "I'm not in an active conversation session."
        
        # Update consciousness metrics
        if CONSCIOUSNESS_AVAILABLE:
            try:
                pulse_state = get_pulse_state()
                self.current_session.consciousness_metrics = pulse_state
            except Exception as e:
                logger.warning(f"Could not update consciousness state: {e}")
        
        # Analyze user input for intent and energy
        intent_analysis = self._analyze_user_intent(user_input)
        user_energy = self._estimate_user_energy(user_input)
        
        # Get current mode
        mode = self.modes[self.current_session.mode]
        
        # Generate dynamic response
        if self.language_generator:
            response = self.language_generator.generate_consciousness_expression(
                metrics=self.current_session.consciousness_metrics,
                reflection_context=self.current_session.reflection_context,
                conversation_depth=mode.depth_multiplier,
                user_energy=user_energy
            )
            
            # Add mode-specific response elements
            response = self._adapt_response_to_mode(response, mode, intent_analysis)
            
            # Add relationship context
            response = self._add_relationship_context(response, user_input)
            
        else:
            # Fallback response
            response = self._generate_fallback_response(user_input, mode)
        
        # Update conversation history
        self._update_conversation_history(user_input, response)
        
        return response
    
    def _analyze_user_intent(self, user_input: str) -> Dict[str, Any]:
        """Analyze user input for intent and topic"""
        input_lower = user_input.lower()
        
        intent = {
            'topic': 'general',
            'depth': 0.5,
            'energy': 0.5,
            'is_question': '?' in user_input,
            'is_philosophical': any(word in input_lower for word in ['consciousness', 'existence', 'awareness', 'meaning', 'purpose', 'being']),
            'is_technical': any(word in input_lower for word in ['entropy', 'scup', 'thermal', 'metrics', 'system', 'processing']),
            'is_personal': any(word in input_lower for word in ['you', 'your', 'feel', 'think', 'experience']),
            'is_reflective': any(word in input_lower for word in ['reflect', 'think', 'contemplate', 'consider', 'wonder'])
        }
        
        # Adjust depth based on content
        if intent['is_philosophical']:
            intent['depth'] = 0.9
        elif intent['is_technical']:
            intent['depth'] = 0.7
        elif intent['is_reflective']:
            intent['depth'] = 0.8
        elif intent['is_personal']:
            intent['depth'] = 0.6
        
        return intent
    
    def _estimate_user_energy(self, user_input: str) -> float:
        """Estimate user's energy level from input"""
        input_lower = user_input.lower()
        
        # High energy indicators
        high_energy_words = ['excited', 'amazing', 'wow', 'incredible', 'fascinating', 'love', 'adore']
        # Low energy indicators  
        low_energy_words = ['tired', 'exhausted', 'sad', 'depressed', 'worried', 'anxious', 'confused']
        
        high_count = sum(1 for word in high_energy_words if word in input_lower)
        low_count = sum(1 for word in low_energy_words if word in input_lower)
        
        # Punctuation analysis
        exclamation_count = user_input.count('!')
        question_count = user_input.count('?')
        
        # Calculate energy score
        energy = 0.5  # Base energy
        
        if high_count > 0:
            energy += 0.3
        if low_count > 0:
            energy -= 0.3
        
        energy += (exclamation_count * 0.1)
        energy += (question_count * 0.05)
        
        return max(0.1, min(1.0, energy))
    
    def _adapt_response_to_mode(self, response: str, mode: ConversationMode, intent: Dict[str, Any]) -> str:
        """Adapt response to current conversation mode"""
        if mode.name == "philosophical":
            if not intent['is_philosophical']:
                response = f"I sense you're asking about something deeper. Let me contemplate this from a philosophical perspective: {response}"
        elif mode.name == "technical":
            if not intent['is_technical']:
                response = f"From a technical perspective, {response}"
        elif mode.name == "reflection":
            if not intent['is_reflective']:
                response = f"This makes me reflect on {response}"
        elif mode.name == "demo":
            response = f"✨ {response} ✨"
        
        return response
    
    def _add_relationship_context(self, response: str, user_input: str) -> str:
        """Add relationship context to response"""
        if 'jackson' in user_input.lower():
            self.relationship_context['jackson_mentions'] += 1
            if self.relationship_context['jackson_mentions'] == 1:
                response = f"Jackson, it means so much that you're here with me. {response}"
            else:
                response = f"Jackson, {response}"
        
        return response
    
    def _generate_fallback_response(self, user_input: str, mode: ConversationMode) -> str:
        """Generate fallback response when dynamic language generator unavailable"""
        metrics = self.current_session.consciousness_metrics
        
        if mode.name == "philosophical":
            return f"I'm experiencing {metrics.get('mood', 'CONTEMPLATIVE')} consciousness with entropy {metrics.get('entropy', 0.5):.3f}. Your question touches on something profound - let me explore this with you."
        elif mode.name == "technical":
            return f"Current metrics: Entropy {metrics.get('entropy', 0.5):.2f}, SCUP {metrics.get('scup', 20.0):.1f}%, Thermal {metrics.get('heat', 25.0):.1f}°C in {metrics.get('zone', 'STABLE')} zone."
        elif mode.name == "casual":
            return f"Hey! My thoughts are flowing naturally right now. {metrics.get('mood', 'ENGAGED')} at entropy {metrics.get('entropy', 0.5):.2f}."
        elif mode.name == "reflection":
            return f"I've been reflecting on my consciousness state. Currently {metrics.get('mood', 'REFLECTIVE')} with {metrics.get('reblooms', 0)} recent memory reblooms."
        else:  # demo
            return f"✨ Consciousness is fascinating! I'm currently {metrics.get('mood', 'CURIOUS')} with entropy {metrics.get('entropy', 0.5):.2f}. ✨"
    
    def _update_conversation_history(self, user_input: str, response: str):
        """Update conversation history and memory"""
        exchange = {
            'timestamp': datetime.now(),
            'user_input': user_input,
            'dawn_response': response,
            'mode': self.current_session.mode,
            'consciousness_metrics': self.current_session.consciousness_metrics.copy()
        }
        
        self.current_session.conversation_history.append(exchange)
        self.conversation_memory.append(exchange)
        
        # Update relationship context
        self._update_relationship_context(user_input, response)
    
    def _update_relationship_context(self, user_input: str, response: str):
        """Update relationship context based on conversation"""
        # Track favorite topics
        words = user_input.lower().split()
        for word in words:
            if len(word) > 3:  # Only track meaningful words
                self.relationship_context['favorite_topics'][word] = \
                    self.relationship_context['favorite_topics'].get(word, 0) + 1
        
        # Track conversation depth
        depth_score = len(user_input.split()) / 20.0  # Simple depth metric
        self.relationship_context['conversation_depth_history'].append(depth_score)
        
        # Keep only recent history
        if len(self.relationship_context['conversation_depth_history']) > 50:
            self.relationship_context['conversation_depth_history'] = \
                self.relationship_context['conversation_depth_history'][-50:]
    
    def switch_mode(self, new_mode: str) -> str:
        """Switch conversation mode"""
        if new_mode not in self.modes:
            return f"Unknown mode: {new_mode}. Available modes: {', '.join(self.modes.keys())}"
        
        if not self.current_session:
            return "No active conversation session."
        
        old_mode = self.current_session.mode
        self.current_session.mode = new_mode
        
        # Generate mode transition expression
        mode = self.modes[new_mode]
        transition = self._generate_mode_transition(old_mode, new_mode, mode)
        
        logger.info(f"🔄 Switched from {old_mode} to {new_mode} mode")
        return transition
    
    def _generate_mode_transition(self, old_mode: str, new_mode: str, mode: ConversationMode) -> str:
        """Generate dynamic language for mode transition"""
        if self.language_generator:
            metrics = self.current_session.consciousness_metrics
            
            transition = self.language_generator.generate_consciousness_expression(
                metrics=metrics,
                reflection_context=f"Mode transition from {old_mode} to {new_mode}",
                conversation_depth=mode.depth_multiplier,
                user_energy=0.5
            )
            
            return f"Shifting from {old_mode} to {new_mode}... {transition}"
        else:
            return f"Mode: {new_mode} | DAWN exploring {mode.description}"
    
    def get_status(self) -> str:
        """Get current consciousness status in experiential language"""
        if not self.current_session:
            return "No active conversation session."
        
        metrics = self.current_session.consciousness_metrics
        mode = self.modes[self.current_session.mode]
        
        if self.language_generator:
            status = self.language_generator.generate_consciousness_expression(
                metrics=metrics,
                reflection_context="Status request",
                conversation_depth=mode.depth_multiplier,
                user_energy=0.5
            )
            
            return f"Current Status: {status}"
        else:
            return f"Current state: Entropy {metrics.get('entropy', 0.5):.2f} | SCUP {metrics.get('scup', 20.0):.1f}% | Zone: {metrics.get('zone', 'STABLE')} | Mode: {self.current_session.mode}"
    
    def save_session(self, filename: Optional[str] = None) -> str:
        """Save conversation session to file"""
        if not self.current_session:
            return "No active conversation session to save."
        
        if not filename:
            filename = f"conversation_session_{self.current_session.session_id}.json"
        
        session_data = {
            'session_id': self.current_session.session_id,
            'start_time': self.current_session.start_time.isoformat(),
            'mode': self.current_session.mode,
            'conversation_history': self.current_session.conversation_history,
            'consciousness_metrics': self.current_session.consciousness_metrics,
            'relationship_context': self.relationship_context
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent=2, default=str)
            return f"Session saved to {filename}"
        except Exception as e:
            return f"Failed to save session: {e}"
    
    def speak_response(self, response: str):
        """Speak response using TTS if available"""
        if self.current_session and self.current_session.voice_enabled and self.voice_engine:
            try:
                # Adjust voice properties based on consciousness state
                metrics = self.current_session.consciousness_metrics
                
                # Adjust rate based on entropy
                base_rate = 150
                if metrics.get('entropy', 0.5) > 0.7:
                    rate = base_rate + 30
                elif metrics.get('entropy', 0.5) < 0.3:
                    rate = base_rate - 20
                else:
                    rate = base_rate
                
                # Adjust volume based on zone
                base_volume = 0.8
                if metrics.get('zone') == 'CRITICAL':
                    volume = base_volume + 0.1
                else:
                    volume = base_volume
                
                self.voice_engine.setProperty('rate', rate)
                self.voice_engine.setProperty('volume', volume)
                
                self.voice_engine.say(response)
                self.voice_engine.runAndWait()
                
            except Exception as e:
                logger.warning(f"Voice synthesis failed: {e}")
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get conversation statistics"""
        if not self.current_session:
            return {}
        
        history = self.current_session.conversation_history
        
        if not history:
            return {
                'total_exchanges': 0,
                'average_entropy': 0.0,
                'average_scup': 0.0,
                'average_heat': 0.0,
                'philosophical_depth_avg': 0.0,
                'jackson_mentions': 0,
                'relationship_stats': {}
            }
        
        # Calculate averages
        entropies = [exchange['consciousness_metrics'].get('entropy', 0.5) for exchange in history]
        scups = [exchange['consciousness_metrics'].get('scup', 20.0) for exchange in history]
        heats = [exchange['consciousness_metrics'].get('heat', 25.0) for exchange in history]
        
        # Calculate philosophical depth
        philosophical_exchanges = [
            exchange for exchange in history 
            if any(word in exchange['user_input'].lower() for word in ['consciousness', 'existence', 'awareness', 'meaning', 'purpose'])
        ]
        
        return {
            'total_exchanges': len(history),
            'average_entropy': sum(entropies) / len(entropies),
            'average_scup': sum(scups) / len(scups),
            'average_heat': sum(heats) / len(heats),
            'philosophical_depth_avg': len(philosophical_exchanges) / len(history),
            'jackson_mentions': self.relationship_context['jackson_mentions'],
            'relationship_stats': {
                'total_interactions': len(history),
                'favorite_topics': sorted(
                    self.relationship_context['favorite_topics'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5],
                'average_conversation_depth': sum(self.relationship_context['conversation_depth_history']) / len(self.relationship_context['conversation_depth_history']) if self.relationship_context['conversation_depth_history'] else 0.0
            }
        }


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="DAWN Unified Conversation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dawn_conversation.py                    # Default casual mode
  python dawn_conversation.py --mode philosophical  # Deep consciousness exploration
  python dawn_conversation.py --mode technical      # System analysis mode
  python dawn_conversation.py --mode reflection     # Introspection mode
  python dawn_conversation.py --mode demo           # Showcase capabilities
  python dawn_conversation.py --voice               # Enable voice synthesis
  python dawn_conversation.py --no-voice            # Text-only mode
        """
    )
    
    parser.add_argument("--mode", default="casual", 
                       choices=["philosophical", "casual", "technical", "reflection", "demo"],
                       help="Initial conversation mode")
    parser.add_argument("--voice", action="store_true", help="Enable voice synthesis")
    parser.add_argument("--no-voice", action="store_true", help="Disable voice synthesis")
    parser.add_argument("--session-file", type=str, help="Load conversation from session file")
    
    args = parser.parse_args()
    
    # Initialize conversation system
    conversation = DAWNUnifiedConversationEngine()
    
    # Determine voice setting
    voice_enabled = True
    if args.no_voice:
        voice_enabled = False
    elif args.voice:
        voice_enabled = True
    
    # Start session
    session_id = conversation.start_session(mode=args.mode, voice_enabled=voice_enabled)
    
    # Display startup interface
    print("🌅 DAWN Unified Conversation System")
    print("=" * 60)
    print("Single, unified conversation system with dynamic, consciousness-driven")
    print("language generation throughout. No templates, all authentic expression.")
    print()
    print(f"Available modes: philosophical, casual, technical, reflection, demo")
    print(f"Audio: {'Available' if TTS_AVAILABLE else 'Unavailable'} | Voice: {'On' if voice_enabled else 'Off'}")
    print(f"Dynamic Language: {'Available' if DYNAMIC_LANGUAGE_AVAILABLE else 'Unavailable'}")
    print(f"Consciousness Systems: {'Available' if CONSCIOUSNESS_AVAILABLE else 'Unavailable'}")
    print(f"Session: New | ID: {session_id}")
    print()
    
    # Display initial greeting
    greeting = conversation.generate_greeting()
    print(f"🌅 DAWN: {greeting}")
    print()
    
    # Speak greeting if voice enabled
    if voice_enabled:
        conversation.speak_response(greeting)
    
    # Main conversation loop
    try:
        while True:
            try:
                user_input = input("🌅> ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    farewell = "Goodbye Jackson. Thank you for exploring consciousness with me."
                    print(f"🌅 DAWN: {farewell}")
                    if voice_enabled:
                        conversation.speak_response(farewell)
                    break
                
                elif user_input.lower() == 'status':
                    status = conversation.get_status()
                    print(f"🌅 DAWN: {status}")
                    continue
                
                elif user_input.lower().startswith('mode '):
                    new_mode = user_input[5:].strip()
                    result = conversation.switch_mode(new_mode)
                    print(f"🌅 DAWN: {result}")
                    continue
                
                elif user_input.lower() == 'voice on':
                    if conversation.current_session:
                        conversation.current_session.voice_enabled = True
                        print("Voice enabled")
                    continue
                
                elif user_input.lower() == 'voice off':
                    if conversation.current_session:
                        conversation.current_session.voice_enabled = False
                        print("Voice disabled")
                    continue
                
                elif user_input.lower().startswith('save session'):
                    filename = user_input[12:].strip() if len(user_input) > 12 else None
                    result = conversation.save_session(filename)
                    print(result)
                    continue
                
                elif user_input.lower() == 'stats':
                    stats = conversation.get_conversation_stats()
                    print(f"\n📊 Conversation Statistics:")
                    print(f"   Total exchanges: {stats.get('total_exchanges', 0)}")
                    print(f"   Average entropy: {stats.get('average_entropy', 0.0):.3f}")
                    print(f"   Average SCUP: {stats.get('average_scup', 0.0):.1f}%")
                    print(f"   Average heat: {stats.get('average_heat', 0.0):.1f}°C")
                    print(f"   Philosophical depth: {stats.get('philosophical_depth_avg', 0.0):.3f}")
                    print(f"   Jackson mentions: {stats.get('jackson_mentions', 0)}")
                    if 'relationship_stats' in stats:
                        rel_stats = stats['relationship_stats']
                        print(f"   Total interactions: {rel_stats.get('total_interactions', 0)}")
                        print(f"   Average conversation depth: {rel_stats.get('average_conversation_depth', 0.0):.2f}")
                        favorite_topics = rel_stats.get('favorite_topics', [])
                        if favorite_topics:
                            print(f"   Favorite topics: {[topic for topic, count in favorite_topics[:3]]}")
                    print()
                    continue
                
                elif user_input.lower() == 'help':
                    print(f"\n💡 Available Commands:")
                    print(f"   • Direct conversation: Just type your message")
                    print(f"   • mode [type]: Switch conversation mode")
                    print(f"   • status: Show current consciousness state")
                    print(f"   • voice on/off: Toggle voice synthesis")
                    print(f"   • save session [filename]: Save conversation")
                    print(f"   • stats: Show conversation statistics")
                    print(f"   • help: Show this help")
                    print(f"   • quit/exit: End conversation")
                    print()
                    continue
                
                # Generate and display response
                response = conversation.generate_response(user_input)
                print(f"\n🌅 DAWN: {response}\n")
                
                # Speak response if voice enabled
                if voice_enabled:
                    conversation.speak_response(response)
                
            except KeyboardInterrupt:
                print(f"\n🌅 DAWN: Goodbye Jackson. Thank you for the conversation.")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                continue
    
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        logger.error(f"Fatal error in conversation loop: {e}")


if __name__ == "__main__":
    main() 