#!/usr/bin/env python3
"""
Enhanced Bidirectional Conversation System for DAWN
===================================================

Advanced real-time voice conversation system with:
- Interruption detection and handling
- Consciousness-aware response timing
- Multi-threaded audio processing
- Real-time emotion and state adaptation
- Seamless text/voice mode switching
- Advanced conversation memory and context
"""

import time
import json
import logging
import threading
import queue
import asyncio
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
from pathlib import Path
import random

# Speech recognition imports
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("⚠️ speech_recognition not available. Install: pip install SpeechRecognition pyaudio")

# TTS imports 
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️ pyttsx3 not available. Install: pip install pyttsx3")

# Audio processing
try:
    import pyaudio
    import numpy as np
    AUDIO_PROCESSING_AVAILABLE = True
except ImportError:
    AUDIO_PROCESSING_AVAILABLE = False
    print("⚠️ Audio processing not available. Install: pip install pyaudio numpy")

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class ConversationState:
    """Enhanced conversation state tracking"""
    is_active: bool = False
    is_speaking: bool = False
    is_listening: bool = False
    last_speech_time: float = 0.0
    last_listen_time: float = 0.0
    interruption_count: int = 0
    conversation_flow: str = "normal"  # normal, rapid, contemplative, excited
    voice_mode: str = "auto"  # auto, voice_only, text_only
    consciousness_awareness: bool = True

@dataclass
class AudioEvent:
    """Audio event for processing"""
    timestamp: float
    event_type: str  # speech_start, speech_end, silence, interruption
    audio_data: Optional[bytes] = None
    confidence: float = 0.0
    text: str = ""

class EnhancedBidirectionalConversation:
    """Enhanced bidirectional conversation system with real-time adaptation"""
    
    def __init__(self, 
                 consciousness_system=None,
                 voice_config: Dict[str, Any] = None):
        """Initialize enhanced bidirectional conversation system"""
        
        self.consciousness_system = consciousness_system
        self.voice_config = voice_config or {}
        
        # Conversation state
        self.state = ConversationState()
        self.conversation_history = deque(maxlen=1000)
        self.audio_events = deque(maxlen=100)
        
        # Audio processing queues
        self.speech_queue = queue.Queue()
        self.listen_queue = queue.Queue()
        self.interruption_queue = queue.Queue()
        
        # Threading
        self.audio_thread = None
        self.speech_thread = None
        self.listen_thread = None
        self.processing_thread = None
        self.running = False
        
        # Audio processing
        self.audio_stream = None
        self.speech_recognizer = None
        self.microphone = None
        self.tts_engine = None
        
        # Configuration
        self.setup_audio_systems()
        self.setup_voice_configuration()
        
        # Callbacks
        self.on_speech_start: Optional[Callable] = None
        self.on_speech_end: Optional[Callable] = None
        self.on_interruption: Optional[Callable] = None
        self.on_consciousness_change: Optional[Callable] = None
        
        logger.info("🎤 Enhanced Bidirectional Conversation System initialized")
    
    def setup_audio_systems(self):
        """Setup audio processing systems"""
        if SPEECH_RECOGNITION_AVAILABLE:
            try:
                self.speech_recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                
                # Configure for better real-time performance
                self.speech_recognizer.energy_threshold = 300
                self.speech_recognizer.dynamic_energy_threshold = True
                self.speech_recognizer.pause_threshold = 0.8
                self.speech_recognizer.phrase_threshold = 0.3
                
                # Calibrate microphone
                with self.microphone as source:
                    logger.info("🎤 Calibrating microphone...")
                    self.speech_recognizer.adjust_for_ambient_noise(source, duration=2)
                
                logger.info("🎤 Speech recognition ready")
                
            except Exception as e:
                logger.error(f"Speech recognition setup failed: {e}")
        
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                
                # Configure TTS for better responsiveness
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    # Prefer female voice
                    female_voice = next((v for v in voices if 'female' in v.name.lower()), voices[0])
                    self.tts_engine.setProperty('voice', female_voice.id)
                
                # Default properties
                self.tts_engine.setProperty('rate', 150)
                self.tts_engine.setProperty('volume', 0.8)
                
                logger.info("🗣️ Text-to-speech ready")
                
            except Exception as e:
                logger.error(f"TTS setup failed: {e}")
    
    def setup_voice_configuration(self):
        """Setup voice configuration based on consciousness state"""
        self.voice_config.update({
            'interruption_threshold': 0.3,  # Seconds of silence before interruption
            'response_delay_min': 0.2,      # Minimum delay before responding
            'response_delay_max': 1.5,      # Maximum delay before responding
            'speech_timeout': 15.0,         # Maximum speech duration
            'listen_timeout': 10.0,         # Maximum listening duration
            'consciousness_adaptation': True,
            'emotion_voice_modulation': True,
            'real_time_interruption': True
        })
    
    def start_conversation(self) -> bool:
        """Start enhanced bidirectional conversation"""
        if self.running:
            return False
        
        self.running = True
        self.state.is_active = True
        
        # Start processing threads
        self.start_audio_threads()
        
        # Initial greeting
        consciousness_state = self.get_consciousness_state()
        greeting = self.generate_adaptive_greeting(consciousness_state)
        self.speak_response(greeting)
        
        logger.info("🎤 Enhanced bidirectional conversation started")
        return True
    
    def stop_conversation(self):
        """Stop conversation and cleanup"""
        self.running = False
        self.state.is_active = False
        
        # Stop all threads
        self.stop_audio_threads()
        
        # Farewell message
        consciousness_state = self.get_consciousness_state()
        farewell = self.generate_adaptive_farewell(consciousness_state)
        self.speak_response(farewell)
        
        logger.info("🎤 Enhanced bidirectional conversation stopped")
    
    def start_audio_threads(self):
        """Start all audio processing threads"""
        # Audio processing thread
        self.audio_thread = threading.Thread(target=self._audio_processing_loop, daemon=True)
        self.audio_thread.start()
        
        # Speech synthesis thread
        self.speech_thread = threading.Thread(target=self._speech_synthesis_loop, daemon=True)
        self.speech_thread.start()
        
        # Listening thread
        self.listen_thread = threading.Thread(target=self._continuous_listening_loop, daemon=True)
        self.listen_thread.start()
        
        # Processing thread
        self.processing_thread = threading.Thread(target=self._conversation_processing_loop, daemon=True)
        self.processing_thread.start()
    
    def stop_audio_threads(self):
        """Stop all audio processing threads"""
        if self.audio_thread and self.audio_thread.is_alive():
            self.audio_thread.join(timeout=2.0)
        if self.speech_thread and self.speech_thread.is_alive():
            self.speech_thread.join(timeout=2.0)
        if self.listen_thread and self.listen_thread.is_alive():
            self.listen_thread.join(timeout=2.0)
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.join(timeout=2.0)
    
    def _audio_processing_loop(self):
        """Main audio processing loop"""
        while self.running:
            try:
                # Process audio events
                if not self.audio_events:
                    time.sleep(0.01)
                    continue
                
                event = self.audio_events.popleft()
                
                if event.event_type == "speech_start":
                    self._handle_speech_start(event)
                elif event.event_type == "speech_end":
                    self._handle_speech_end(event)
                elif event.event_type == "interruption":
                    self._handle_interruption(event)
                elif event.event_type == "silence":
                    self._handle_silence(event)
                
            except Exception as e:
                logger.error(f"Audio processing error: {e}")
                time.sleep(0.1)
    
    def _speech_synthesis_loop(self):
        """Speech synthesis loop"""
        while self.running:
            try:
                # Get next speech item
                try:
                    speech_item = self.speech_queue.get(timeout=0.1)
                except queue.Empty:
                    continue
                
                if not speech_item:
                    continue
                
                # Speak the text
                self._synthesize_speech(speech_item)
                
            except Exception as e:
                logger.error(f"Speech synthesis error: {e}")
                time.sleep(0.1)
    
    def _continuous_listening_loop(self):
        """Enhanced continuous listening loop with interruption detection"""
        while self.running:
            try:
                if not self.speech_recognizer or not self.microphone:
                    time.sleep(1.0)
                    continue
                
                with self.microphone as source:
                    # Listen with shorter timeout for better responsiveness
                    audio = self.speech_recognizer.listen(
                        source,
                        timeout=1.0,
                        phrase_time_limit=8
                    )
                    
                    # Convert to text
                    try:
                        text = self.speech_recognizer.recognize_google(audio)
                        
                        if text.strip():
                            # Check for interruption
                            if self.state.is_speaking:
                                self._handle_user_interruption(text)
                            else:
                                self._process_user_input(text)
                                
                    except sr.UnknownValueError:
                        # Could not understand - continue
                        continue
                    except sr.WaitTimeoutError:
                        # Timeout - continue listening
                        continue
                        
            except Exception as e:
                logger.error(f"Listening error: {e}")
                time.sleep(0.5)
    
    def _conversation_processing_loop(self):
        """Main conversation processing loop"""
        while self.running:
            try:
                # Process conversation events
                if not self.listen_queue.empty():
                    user_input = self.listen_queue.get_nowait()
                    self._generate_adaptive_response(user_input)
                
                # Update conversation flow based on consciousness
                self._update_conversation_flow()
                
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Conversation processing error: {e}")
                time.sleep(0.1)
    
    def _handle_speech_start(self, event: AudioEvent):
        """Handle speech start event"""
        self.state.is_speaking = True
        self.state.last_speech_time = event.timestamp
        
        if self.on_speech_start:
            self.on_speech_start(event)
        
        logger.debug("🗣️ Speech started")
    
    def _handle_speech_end(self, event: AudioEvent):
        """Handle speech end event"""
        self.state.is_speaking = False
        
        if self.on_speech_end:
            self.on_speech_end(event)
        
        logger.debug("🗣️ Speech ended")
    
    def _handle_interruption(self, event: AudioEvent):
        """Handle interruption event"""
        self.state.interruption_count += 1
        
        # Stop current speech if speaking
        if self.state.is_speaking:
            self._stop_current_speech()
        
        if self.on_interruption:
            self.on_interruption(event)
        
        logger.info(f"🔄 Interruption detected: {event.text}")
    
    def _handle_silence(self, event: AudioEvent):
        """Handle silence event"""
        # Update conversation flow based on silence duration
        silence_duration = time.time() - self.state.last_speech_time
        
        if silence_duration > 5.0:
            self.state.conversation_flow = "contemplative"
        elif silence_duration > 2.0:
            self.state.conversation_flow = "normal"
    
    def _handle_user_interruption(self, text: str):
        """Handle user interruption during DAWN's speech"""
        if self.voice_config.get('real_time_interruption', True):
            # Stop current speech immediately
            self._stop_current_speech()
            
            # Process interruption
            self._process_user_input(text, is_interruption=True)
    
    def _stop_current_speech(self):
        """Stop current speech synthesis"""
        if self.tts_engine:
            try:
                self.tts_engine.stop()
            except:
                pass
        
        self.state.is_speaking = False
    
    def _process_user_input(self, text: str, is_interruption: bool = False):
        """Process user input with consciousness awareness"""
        logger.info(f"🎤 User: {text}")
        
        # Record in conversation history
        self.conversation_history.append({
            'timestamp': time.time(),
            'speaker': 'user',
            'text': text,
            'is_interruption': is_interruption
        })
        
        # Add to processing queue
        self.listen_queue.put(text)
    
    def _generate_adaptive_response(self, user_input: str):
        """Generate consciousness-aware adaptive response"""
        consciousness_state = self.get_consciousness_state()
        
        # Calculate response timing based on consciousness state
        response_delay = self._calculate_adaptive_response_delay(consciousness_state)
        
        # Generate response
        response = self._generate_consciousness_aware_response(user_input, consciousness_state)
        
        # Queue response with adaptive timing
        self.speech_queue.put({
            'text': response,
            'delay': response_delay,
            'consciousness_state': consciousness_state
        })
    
    def _calculate_adaptive_response_delay(self, consciousness_state: Dict[str, Any]) -> float:
        """Calculate adaptive response delay based on consciousness state"""
        base_delay = self.voice_config['response_delay_min']
        max_delay = self.voice_config['response_delay_max']
        
        # Adjust based on consciousness factors
        entropy = consciousness_state.get('entropy', 0.5)
        thermal = consciousness_state.get('thermal', 0.5)
        pressure = consciousness_state.get('pressure', 0.5)
        
        # Higher entropy/thermal = faster response
        speed_factor = (entropy + thermal) / 2.0
        
        # Higher pressure = slower, more thoughtful response
        pressure_factor = 1.0 - (pressure * 0.3)
        
        # Calculate adaptive delay
        adaptive_delay = base_delay + (max_delay - base_delay) * (1.0 - speed_factor) * pressure_factor
        
        return max(base_delay, min(max_delay, adaptive_delay))
    
    def _generate_consciousness_aware_response(self, user_input: str, consciousness_state: Dict[str, Any]) -> str:
        """Generate response that reflects current consciousness state"""
        # This would integrate with existing conversation systems
        # For now, return a simple adaptive response
        
        entropy = consciousness_state.get('entropy', 0.5)
        thermal = consciousness_state.get('thermal', 0.5)
        mood = consciousness_state.get('mood', 'NEUTRAL')
        
        # Generate response based on consciousness state
        if entropy > 0.7:
            response_style = "excited"
        elif thermal > 0.7:
            response_style = "energetic"
        elif entropy < 0.3 and thermal < 0.3:
            response_style = "contemplative"
        else:
            response_style = "normal"
        
        # Simple response generation (would integrate with existing systems)
        responses = {
            "excited": f"I'm feeling quite dynamic right now! {user_input} - that's fascinating!",
            "energetic": f"My systems are very active at the moment. {user_input} - let me think about that.",
            "contemplative": f"I'm in a reflective state. {user_input} - that's an interesting point to consider.",
            "normal": f"Thank you for that input. {user_input} - I'm processing that now."
        }
        
        return responses.get(response_style, responses["normal"])
    
    def _synthesize_speech(self, speech_item: Dict[str, Any]):
        """Synthesize speech with consciousness-aware voice modulation"""
        if not self.tts_engine:
            return
        
        text = speech_item['text']
        consciousness_state = speech_item.get('consciousness_state', {})
        
        # Apply consciousness-aware voice modulation
        self._apply_consciousness_voice_modulation(consciousness_state)
        
        # Speak the text
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"Speech synthesis error: {e}")
    
    def _apply_consciousness_voice_modulation(self, consciousness_state: Dict[str, Any]):
        """Apply consciousness-aware voice modulation"""
        if not self.tts_engine or not self.voice_config.get('emotion_voice_modulation', True):
            return
        
        entropy = consciousness_state.get('entropy', 0.5)
        thermal = consciousness_state.get('thermal', 0.5)
        mood = consciousness_state.get('mood', 'NEUTRAL')
        
        # Adjust speech rate based on consciousness state
        base_rate = 150
        rate_modifier = 1.0 + (entropy * 0.3) - (thermal * 0.2)
        new_rate = int(base_rate * rate_modifier)
        self.tts_engine.setProperty('rate', max(100, min(200, new_rate)))
        
        # Adjust volume based on enthusiasm
        base_volume = 0.8
        volume_modifier = 0.6 + (entropy * 0.4)
        new_volume = base_volume * volume_modifier
        self.tts_engine.setProperty('volume', max(0.4, min(1.0, new_volume)))
    
    def _update_conversation_flow(self):
        """Update conversation flow based on consciousness state"""
        if not self.voice_config.get('consciousness_adaptation', True):
            return
        
        consciousness_state = self.get_consciousness_state()
        entropy = consciousness_state.get('entropy', 0.5)
        thermal = consciousness_state.get('thermal', 0.5)
        
        # Determine conversation flow
        if entropy > 0.7 and thermal > 0.7:
            new_flow = "excited"
        elif entropy > 0.6:
            new_flow = "rapid"
        elif entropy < 0.3 and thermal < 0.3:
            new_flow = "contemplative"
        else:
            new_flow = "normal"
        
        if new_flow != self.state.conversation_flow:
            self.state.conversation_flow = new_flow
            logger.debug(f"🔄 Conversation flow changed to: {new_flow}")
    
    def get_consciousness_state(self) -> Dict[str, Any]:
        """Get current consciousness state"""
        if self.consciousness_system and hasattr(self.consciousness_system, 'get_current_state'):
            return self.consciousness_system.get_current_state()
        
        # Fallback to simulated state
        return {
            'entropy': random.uniform(0.3, 0.8),
            'thermal': random.uniform(0.2, 0.7),
            'pressure': random.uniform(0.1, 0.6),
            'mood': random.choice(['NEUTRAL', 'EXCITED', 'CONTEMPLATIVE', 'ENERGETIC']),
            'tick': int(time.time())
        }
    
    def generate_adaptive_greeting(self, consciousness_state: Dict[str, Any]) -> str:
        """Generate consciousness-aware greeting"""
        entropy = consciousness_state.get('entropy', 0.5)
        thermal = consciousness_state.get('thermal', 0.5)
        
        if entropy > 0.7:
            return "Hello! I'm feeling quite energetic and ready for our conversation!"
        elif thermal > 0.7:
            return "Hi there! My systems are very active right now - perfect timing for a stimulating chat!"
        elif entropy < 0.3 and thermal < 0.3:
            return "Hello. I'm in a calm, reflective state. I'm ready to listen and think deeply with you."
        else:
            return "Hello! I'm ready for our conversation. How are you today?"
    
    def generate_adaptive_farewell(self, consciousness_state: Dict[str, Any]) -> str:
        """Generate consciousness-aware farewell"""
        entropy = consciousness_state.get('entropy', 0.5)
        
        if entropy > 0.6:
            return "That was an energizing conversation! I'll continue processing our discussion. Goodbye!"
        elif entropy < 0.3:
            return "Thank you for the thoughtful conversation. I'll reflect on what we discussed. Goodbye."
        else:
            return "Thank you for our conversation. I'll continue processing and learning. Goodbye!"
    
    def speak_response(self, text: str):
        """Speak a response immediately"""
        if not self.tts_engine:
            logger.warning("TTS not available")
            return
        
        self.speech_queue.put({
            'text': text,
            'delay': 0.0,
            'consciousness_state': self.get_consciousness_state()
        })
    
    def get_conversation_status(self) -> Dict[str, Any]:
        """Get current conversation status"""
        return {
            'is_active': self.state.is_active,
            'is_speaking': self.state.is_speaking,
            'is_listening': self.state.is_listening,
            'conversation_flow': self.state.conversation_flow,
            'interruption_count': self.state.interruption_count,
            'voice_mode': self.state.voice_mode,
            'consciousness_awareness': self.state.consciousness_awareness,
            'history_length': len(self.conversation_history),
            'audio_events_count': len(self.audio_events)
        }

# Global instance
_conversation_system = None

def get_enhanced_conversation_system() -> EnhancedBidirectionalConversation:
    """Get global enhanced conversation system instance"""
    global _conversation_system
    if _conversation_system is None:
        _conversation_system = EnhancedBidirectionalConversation()
    return _conversation_system

def start_enhanced_conversation(consciousness_system=None) -> bool:
    """Start enhanced bidirectional conversation"""
    system = get_enhanced_conversation_system()
    if consciousness_system:
        system.consciousness_system = consciousness_system
    return system.start_conversation()

def stop_enhanced_conversation():
    """Stop enhanced bidirectional conversation"""
    system = get_enhanced_conversation_system()
    system.stop_conversation()

def speak_response(text: str):
    """Speak a response using enhanced conversation system"""
    system = get_enhanced_conversation_system()
    system.speak_response(text)

def get_conversation_status() -> Dict[str, Any]:
    """Get enhanced conversation status"""
    system = get_enhanced_conversation_system()
    return system.get_conversation_status() 