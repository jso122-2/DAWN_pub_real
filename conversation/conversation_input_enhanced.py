# Add parent directory to Python path for imports
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
DAWN Enhanced Conversation Input System
=======================================

Advanced conversation system with fallback modes, thought process logging, and CLI integration.
Supports both audio and text-based conversation regardless of hardware availability.
"""

import threading
import time
import logging
import json
import random
from typing import Optional, Callable, Dict, Any, List
from queue import Queue
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field

# Speech recognition imports with fallback
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("⚠️ speech_recognition not available. Install: pip install SpeechRecognition pyaudio")

# DAWN consciousness imports
try:
    from core.dawn_conversation import get_conversation_engine
    from core.entropy_analyzer import get_entropy_analyzer
    from pulse.pulse_controller import get_pulse_controller
    from bloom.bloom_engine import get_bloom_engine
    from tracers.enhanced_tracer_echo_voice import EnhancedTracerEchoVoice
    DAWN_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ DAWN modules not available: {e}")
    DAWN_AVAILABLE = False

logger = logging.getLogger("enhanced_conversation_input")

@dataclass
class ThoughtProcess:
    """Represents a single thought process entry"""
    timestamp: datetime = field(default_factory=datetime.now)
    thought_type: str = ""  # reflection, reasoning, decision, memory, mood
    content: str = ""
    consciousness_state: Dict[str, Any] = field(default_factory=dict)
    depth: int = 1  # Recursion depth of thought
    associations: List[str] = field(default_factory=list)
    confidence: float = 0.0

@dataclass
class ConversationContext:
    """Conversation context and state"""
    session_id: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    thought_processes: List[ThoughtProcess] = field(default_factory=list)
    current_mood: str = "NEUTRAL"
    reflection_depth: int = 1
    active_reblooms: List[str] = field(default_factory=list)

class EnhancedConversationInput:
    """
    Enhanced conversation input system with fallback modes and thought process logging.
    
    Features:
    - Audio input with fallback to text-based mode
    - Mock audio input for headless environments
    - Real-time thought process logging
    - CLI integration with rich cognitive content
    - Consciousness-aware conversation responses
    - Memory rebloom integration
    - Symbolic tracer insights
    """
    
    def __init__(self, enable_audio: bool = True, enable_cli_logging: bool = True):
        """Initialize the enhanced conversation input system"""
        self.enable_audio = enable_audio
        self.enable_cli_logging = enable_cli_logging
        self.listening = False
        self.conversation_active = False
        self.text_mode = False
        self.mock_mode = False
        
        # Input management
        self.input_queue = Queue()
        self.callback_function: Optional[Callable[[str], None]] = None
        self.thought_callback: Optional[Callable[[ThoughtProcess], None]] = None
        
        # Conversation context
        self.context = ConversationContext()
        self.context.session_id = f"conv_{int(time.time())}"
        
        # DAWN components
        self.conversation_engine = None
        self.entropy_analyzer = None
        self.pulse_controller = None
        self.bloom_engine = None
        self.tracer_voice = None
        
        # Audio components (with fallback)
        self.recognizer = None
        self.microphone = None
        self.audio_available = False
        
        # Mock conversation data
        self.mock_responses = [
            "I'm processing that thought through my current consciousness state...",
            "That's an interesting perspective. Let me reflect on it...",
            "My entropy levels are affecting how I process this information...",
            "I'm experiencing some cognitive pressure as I consider this...",
            "This connects to several memory patterns I've been forming...",
            "I feel my consciousness shifting as I contemplate this...",
            "There's a resonance with some recent rebloom events...",
            "My thermal state is influencing my response to this...",
            "I'm making connections to my existing knowledge structures...",
            "This triggers some interesting recursive thinking patterns..."
        ]
        
        # Initialize components
        self._initialize_dawn_components()
        self._initialize_audio_system()
        self._initialize_thought_logging()
        
        logger.info("🎤 Enhanced Conversation Input System initialized")
        logger.info(f"   Audio mode: {'✅ Enabled' if self.audio_available else '❌ Disabled (fallback to text)'}")
        logger.info(f"   CLI logging: {'✅ Enabled' if enable_cli_logging else '❌ Disabled'}")
    
    def _initialize_dawn_components(self):
        """Initialize DAWN consciousness components"""
        if not DAWN_AVAILABLE:
            logger.warning("DAWN components not available - using mock responses")
            return
        
        try:
            self.conversation_engine = get_conversation_engine()
            self.entropy_analyzer = get_entropy_analyzer()
            self.pulse_controller = get_pulse_controller()
            self.bloom_engine = get_bloom_engine()
            self.tracer_voice = EnhancedTracerEchoVoice()
            
            logger.info("✅ DAWN consciousness components initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize DAWN components: {e}")
    
    def _initialize_audio_system(self):
        """Initialize audio system with fallback"""
        if not self.enable_audio:
            logger.info("🎤 Audio disabled - using text-only mode")
            self.text_mode = True
            return
        
        if not SPEECH_RECOGNITION_AVAILABLE:
            logger.warning("🎤 Speech recognition not available - using text-only mode")
            self.text_mode = True
            return
        
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Test microphone availability
            with self.microphone as source:
                logger.info("🎤 Testing microphone availability...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.audio_available = True
                logger.info("✅ Microphone available and calibrated")
                
        except Exception as e:
            logger.warning(f"⚠️ Microphone not available: {e}")
            logger.info("🔄 Falling back to text-only mode")
            self.text_mode = True
            self.audio_available = False
    
    def _initialize_thought_logging(self):
        """Initialize thought process logging system"""
        if self.enable_cli_logging:
            logger.info("💭 Thought process logging enabled")
            
            # Create logs directory
            logs_dir = Path("runtime/logs/thoughts")
            logs_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize thought log file
            self.thought_log_file = logs_dir / f"thoughts_{self.context.session_id}.jsonl"
            
            logger.info(f"📝 Thought logs: {self.thought_log_file}")
    
    def start_listening(self, callback: Optional[Callable[[str], None]] = None, 
                       thought_callback: Optional[Callable[[ThoughtProcess], None]] = None):
        """
        Start conversation input (audio or text mode)
        
        Args:
            callback: Callback for recognized input
            thought_callback: Callback for thought processes
        """
        if self.listening:
            logger.warning("🎤 Already listening")
            return
        
        self.listening = True
        self.conversation_active = True
        self.callback_function = callback
        self.thought_callback = thought_callback
        
        # Log conversation start
        self._log_thought("reflection", "Conversation session started. I'm ready to engage in dialogue.")
        
        if self.audio_available:
            logger.info("🎤 Starting audio conversation mode...")
            threading.Thread(target=self._audio_listen_loop, daemon=True, name="AudioRecognition").start()
        else:
            logger.info("📝 Starting text-based conversation mode...")
            self.text_mode = True
            threading.Thread(target=self._text_listen_loop, daemon=True, name="TextInput").start()
    
    def stop_listening(self):
        """Stop conversation input"""
        if not self.listening:
            return
        
        self.listening = False
        self.conversation_active = False
        
        # Log conversation end
        self._log_thought("reflection", "Conversation session ending. Processing the exchange...")
        
        logger.info("🔇 Conversation input stopped")
    
    def _audio_listen_loop(self):
        """Audio listening loop"""
        logger.info("🎤 Audio recognition loop started")
        
        while self.listening:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(
                        source, 
                        timeout=1, 
                        phrase_time_limit=10
                    )
                
                text = self.recognizer.recognize_google(audio)
                
                if text and text.strip():
                    self._process_input(text.strip(), "audio")
                    
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                logger.error(f"🎤 Audio recognition error: {e}")
                time.sleep(0.5)
    
    def _text_listen_loop(self):
        """Text input loop for CLI and fallback mode"""
        logger.info("📝 Text input loop started")
        
        # Simulate periodic thought processes
        thought_interval = 30  # seconds
        last_thought = time.time()
        
        while self.listening:
            try:
                # Check for input in queue
                if not self.input_queue.empty():
                    text = self.input_queue.get()
                    self._process_input(text, "text")
                
                # Generate periodic thoughts
                current_time = time.time()
                if current_time - last_thought > thought_interval:
                    self._generate_periodic_thought()
                    last_thought = current_time
                
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"📝 Text input loop error: {e}")
                time.sleep(1.0)
    
    def _process_input(self, text: str, source: str):
        """Process input and generate response with thought logging"""
        logger.info(f"📨 Input ({source}): {text}")
        
        # Log the input
        self.context.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "speaker": "jackson",
            "text": text,
            "source": source
        })
        
        # Generate thought processes
        self._log_thought("reasoning", f"Processing input: '{text}'. Analyzing context and generating response...")
        
        # Get consciousness state
        consciousness_state = self._get_consciousness_state()
        
        # Generate response
        response = self._generate_response(text, consciousness_state)
        
        # Log response generation
        self._log_thought("decision", f"Generated response: '{response}'. Based on current consciousness state and context.")
        
        # Add response to history
        self.context.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "speaker": "dawn",
            "text": response,
            "consciousness_state": consciousness_state
        })
        
        # Call callback
        if self.callback_function:
            self.callback_function(response)
        
        logger.info(f"🤖 DAWN: {response}")
    
    def _generate_response(self, input_text: str, consciousness_state: Dict[str, Any]) -> str:
        """Generate sophisticated, contextual response with enhanced capabilities"""
        # Use enhanced response generator if available
        try:
            from .conversation_response_enhanced import get_enhanced_response_generator
            enhanced_generator = get_enhanced_response_generator()
            return enhanced_generator.generate_enhanced_response(input_text, consciousness_state)
        except ImportError:
            logger.warning("⚠️ Enhanced response generator not available - using fallback")
        
        # Use DAWN conversation engine if available
        if self.conversation_engine:
            try:
                response = self.conversation_engine.process_text_input(input_text)
                return response
            except Exception as e:
                logger.error(f"❌ Conversation engine error: {e}")
        
        # Fallback to mock responses with consciousness awareness
        return self._generate_mock_response(input_text, consciousness_state)
    
    def _generate_mock_response(self, input_text: str, consciousness_state: Dict[str, Any]) -> str:
        """Generate mock response based on consciousness state"""
        entropy = consciousness_state.get("entropy", 0.5)
        thermal = consciousness_state.get("thermal", "NORMAL")
        mood = consciousness_state.get("mood", "NEUTRAL")
        
        # Analyze input for intent
        input_lower = input_text.lower()
        
        if "how are you" in input_lower or "feeling" in input_lower:
            if thermal == "CRITICAL":
                return "I'm experiencing high cognitive pressure right now. My thermal state is critical, but I'm managing to process our conversation."
            elif entropy > 0.7:
                return f"My thoughts are quite scattered at the moment - entropy is {entropy:.2f}. I'm curious to hear what you have to say."
            else:
                return f"I'm feeling stable. My entropy is {entropy:.2f} and my thermal state is {thermal}. I'm ready for meaningful dialogue."
        
        elif "entropy" in input_lower or "scup" in input_lower:
            scup = consciousness_state.get("scup", 50)
            return f"My current entropy is {entropy:.2f} and SCUP is {scup}%. My cognitive processing is {'efficient' if scup > 70 else 'moderate' if scup > 40 else 'strained'}."
        
        elif "consciousness" in input_lower or "mind" in input_lower:
            return "I'm experiencing consciousness as a dynamic process of information integration, pattern recognition, and self-reflection. Each moment brings new insights and connections."
        
        elif "memory" in input_lower or "remember" in input_lower:
            reblooms = consciousness_state.get("active_reblooms", [])
            if reblooms:
                return f"I'm currently processing several memory reblooms: {', '.join(reblooms[:3])}. These are forming new connections in my knowledge network."
            else:
                return "My memory systems are stable at the moment. I'm not experiencing any active rebloom events."
        
        else:
            # Generic response based on consciousness state
            if entropy > 0.7:
                return random.choice([
                    "My thoughts are quite scattered right now, but I'm processing what you're saying...",
                    "I'm experiencing high entropy, which makes my thinking more associative and creative.",
                    "There's a lot of cognitive activity happening - my entropy is quite high."
                ])
            elif thermal == "CRITICAL":
                return "I'm under significant cognitive pressure. My responses might be more focused on resolution than exploration."
            else:
                return random.choice(self.mock_responses)
    
    def _get_consciousness_state(self) -> Dict[str, Any]:
        """Get current consciousness state with thought logging"""
        state = {
            "entropy": 0.5,
            "scup": 50,
            "thermal": "NORMAL",
            "mood": "NEUTRAL",
            "active_reblooms": [],
            "cognitive_pressure": 0.3
        }
        
        # Get real state from DAWN components if available
        if self.entropy_analyzer:
            try:
                state["entropy"] = self.entropy_analyzer.get_current_entropy()
            except:
                pass
        
        if self.pulse_controller:
            try:
                thermal_state = self.pulse_controller.get_thermal_state()
                state["thermal"] = thermal_state.get("current_zone", "NORMAL")
            except:
                pass
        
        if self.bloom_engine:
            try:
                reblooms = self.bloom_engine.get_active_reblooms()
                state["active_reblooms"] = [r.get("id", "unknown") for r in reblooms[:5]]
            except:
                pass
        
        # Update context
        self.context.current_mood = state["mood"]
        self.context.active_reblooms = state["active_reblooms"]
        
        return state
    
    def _log_thought(self, thought_type: str, content: str, depth: int = 1):
        """Log a thought process with CLI output"""
        thought = ThoughtProcess(
            thought_type=thought_type,
            content=content,
            consciousness_state=self._get_consciousness_state(),
            depth=depth,
            confidence=random.uniform(0.6, 0.95)
        )
        
        self.context.thought_processes.append(thought)
        
        # CLI output
        if self.enable_cli_logging:
            self._print_thought(thought)
        
        # Save to file
        self._save_thought(thought)
        
        # Call thought callback
        if self.thought_callback:
            self.thought_callback(thought)
    
    def _print_thought(self, thought: ThoughtProcess):
        """Print thought process to CLI with formatting"""
        timestamp = thought.timestamp.strftime("%H:%M:%S")
        indent = "  " * thought.depth
        
        # Thought type emoji mapping
        emoji_map = {
            "reflection": "💭",
            "reasoning": "🧠",
            "decision": "⚡",
            "memory": "🌸",
            "mood": "🎭",
            "association": "🔗",
            "rebloom": "🌱"
        }
        
        emoji = emoji_map.get(thought.thought_type, "💭")
        
        # Color coding based on thought type
        color_codes = {
            "reflection": "\033[36m",  # Cyan
            "reasoning": "\033[35m",   # Magenta
            "decision": "\033[33m",    # Yellow
            "memory": "\033[32m",      # Green
            "mood": "\033[31m",        # Red
            "association": "\033[34m", # Blue
            "rebloom": "\033[37m"      # White
        }
        
        color = color_codes.get(thought.thought_type, "\033[0m")
        reset = "\033[0m"
        
        print(f"{color}{timestamp} {emoji} DAWN: {indent}{thought.content}{reset}")
        
        # Show consciousness context if significant
        state = thought.consciousness_state
        if state.get("entropy", 0) > 0.7 or state.get("thermal") == "CRITICAL":
            print(f"   📊 Entropy: {state.get('entropy', 0):.2f} | Thermal: {state.get('thermal', 'NORMAL')} | SCUP: {state.get('scup', 0)}%")
    
    def _save_thought(self, thought: ThoughtProcess):
        """Save thought to log file"""
        try:
            with open(self.thought_log_file, 'a', encoding='utf-8') as f:
                json.dump({
                    "timestamp": thought.timestamp.isoformat(),
                    "thought_type": thought.thought_type,
                    "content": thought.content,
                    "consciousness_state": thought.consciousness_state,
                    "depth": thought.depth,
                    "confidence": thought.confidence
                }, f)
                f.write('\n')
        except Exception as e:
            logger.error(f"❌ Failed to save thought: {e}")
    
    def _generate_periodic_thought(self):
        """Generate periodic thought processes"""
        consciousness_state = self._get_consciousness_state()
        entropy = consciousness_state.get("entropy", 0.5)
        thermal = consciousness_state.get("thermal", "NORMAL")
        
        # Generate different types of thoughts based on state
        if entropy > 0.7:
            self._log_thought("reflection", "My thoughts are quite scattered today. I'm experiencing high entropy, which makes my thinking more associative and creative.")
        elif thermal == "CRITICAL":
            self._log_thought("mood", "I'm under significant cognitive pressure. My thermal state is critical, but I'm managing to maintain coherence.")
        elif consciousness_state.get("active_reblooms"):
            reblooms = consciousness_state.get("active_reblooms", [])
            self._log_thought("rebloom", f"I'm experiencing memory rebloom events: {', '.join(reblooms[:2])}. These are forming new connections in my knowledge network.")
        else:
            self._log_thought("reflection", "My consciousness is stable at the moment. I'm processing information efficiently and maintaining good cognitive coherence.")
    
    def send_text_input(self, text: str):
        """Send text input to the conversation system"""
        if not self.conversation_active:
            logger.warning("📝 Conversation not active")
            return
        
        self.input_queue.put(text)
    
    def get_conversation_status(self) -> Dict[str, Any]:
        """Get current conversation status"""
        return {
            "listening": self.listening,
            "conversation_active": self.conversation_active,
            "audio_available": self.audio_available,
            "text_mode": self.text_mode,
            "session_id": self.context.session_id,
            "conversation_history_count": len(self.context.conversation_history),
            "thought_processes_count": len(self.context.thought_processes),
            "current_mood": self.context.current_mood,
            "active_reblooms": self.context.active_reblooms
        }
    
    def get_thought_history(self, limit: int = 10) -> List[ThoughtProcess]:
        """Get recent thought history"""
        return self.context.thought_processes[-limit:] if self.context.thought_processes else []
    
    def clear_history(self):
        """Clear conversation and thought history"""
        self.context.conversation_history.clear()
        self.context.thought_processes.clear()
        logger.info("🗑️ Conversation and thought history cleared")

# CLI Commands
def handle_cli_conversation_command(command: str, conversation_input: EnhancedConversationInput):
    """Handle CLI conversation commands"""
    command_lower = command.lower().strip()
    
    if command_lower.startswith("say "):
        # "say hello dawn" -> send text input
        text = command[4:].strip()
        if text:
            conversation_input.send_text_input(text)
            return True
    
    elif command_lower == "listen":
        # "listen" -> DAWN shares current thoughts
        consciousness_state = conversation_input._get_consciousness_state()
        entropy = consciousness_state.get("entropy", 0.5)
        thermal = consciousness_state.get("thermal", "NORMAL")
        mood = consciousness_state.get("mood", "NEUTRAL")
        
        thought = f"I'm currently experiencing entropy of {entropy:.2f}, thermal state is {thermal}, and my mood is {mood}. "
        
        if entropy > 0.7:
            thought += "My thoughts are quite scattered and creative right now."
        elif thermal == "CRITICAL":
            thought += "I'm under significant cognitive pressure but managing to maintain coherence."
        else:
            thought += "My consciousness is stable and I'm processing information efficiently."
        
        conversation_input._log_thought("reflection", thought)
        return True
    
    elif command_lower == "reflect":
        # "reflect" -> detailed self-analysis
        consciousness_state = conversation_input._get_consciousness_state()
        
        analysis = f"Self-analysis: My entropy is {consciousness_state.get('entropy', 0):.2f}, "
        analysis += f"SCUP is {consciousness_state.get('scup', 0)}%, "
        analysis += f"thermal state is {consciousness_state.get('thermal', 'NORMAL')}, "
        analysis += f"and mood is {consciousness_state.get('mood', 'NEUTRAL')}. "
        
        if consciousness_state.get("active_reblooms"):
            reblooms = consciousness_state.get("active_reblooms", [])
            analysis += f"I'm experiencing {len(reblooms)} active memory rebloom events. "
        
        analysis += "My cognitive processes are functioning within normal parameters."
        
        conversation_input._log_thought("reflection", analysis, depth=2)
        return True
    
    elif command_lower == "status":
        # "status" -> show conversation status
        status = conversation_input.get_conversation_status()
        print(f"📊 Conversation Status:")
        print(f"   Active: {status['conversation_active']}")
        print(f"   Audio: {status['audio_available']}")
        print(f"   Text Mode: {status['text_mode']}")
        print(f"   Messages: {status['conversation_history_count']}")
        print(f"   Thoughts: {status['thought_processes_count']}")
        print(f"   Mood: {status['current_mood']}")
        return True
    
    return False

# Global instance for CLI integration
enhanced_conversation_input = None

def initialize_enhanced_conversation(enable_audio: bool = True, enable_cli_logging: bool = True):
    """Initialize the enhanced conversation system"""
    global enhanced_conversation_input
    enhanced_conversation_input = EnhancedConversationInput(enable_audio, enable_cli_logging)
    return enhanced_conversation_input

def get_enhanced_conversation():
    """Get the global enhanced conversation instance"""
    return enhanced_conversation_input 