#!/usr/bin/env python3
"""
DAWN Conversation WebSocket Handler
==================================

Real-time bidirectional conversation system with speech-to-text and consciousness integration.
Handles WebSocket connections for the Voice Interface GUI conversation mode.
"""

import asyncio
import json
import logging
import base64
import time
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from websockets import WebSocketServerProtocol
from websockets.server import serve
import threading

# Speech recognition imports
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("⚠️ speech_recognition not available. Install: pip install SpeechRecognition pyaudio")

# DAWN consciousness integration
try:
    from core.dawn_conversation import DAWNConversationEngine, get_conversation_engine
    from core.cognitive_pressure import get_cognitive_pressure_engine
    from core.entropy_analyzer import get_entropy_analyzer
    from pulse.pulse_controller import get_pulse_controller
    DAWN_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ DAWN modules not available: {e}")
    DAWN_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class ConversationSession:
    """Active conversation session data"""
    session_id: str
    websocket: WebSocketServerProtocol
    start_time: datetime = field(default_factory=datetime.now)
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    consciousness_state: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = False
    last_interaction: datetime = field(default_factory=datetime.now)

class ConversationWebSocketHandler:
    """WebSocket handler for bidirectional conversation with DAWN"""
    
    def __init__(self):
        self.active_sessions: Dict[str, ConversationSession] = {}
        self.conversation_engine: Optional[DAWNConversationEngine] = None
        self.speech_recognizer: Optional[sr.Recognizer] = None
        self.microphone: Optional[sr.Microphone] = None
        
        # Initialize DAWN components
        self._initialize_dawn_components()
        self._initialize_speech_recognition()
        
        logger.info("🗣️ Conversation WebSocket Handler initialized")
    
    def _initialize_dawn_components(self):
        """Initialize DAWN consciousness components"""
        if not DAWN_AVAILABLE:
            logger.warning("DAWN components not available - using mock responses")
            return
        
        try:
            # Get DAWN components
            pulse_controller = get_pulse_controller()
            entropy_analyzer = get_entropy_analyzer()
            cognitive_pressure_engine = get_cognitive_pressure_engine()
            
            # Initialize conversation engine
            self.conversation_engine = DAWNConversationEngine(
                pulse_controller=pulse_controller,
                entropy_analyzer=entropy_analyzer,
                cognitive_pressure_engine=cognitive_pressure_engine
            )
            
            logger.info("✅ DAWN conversation engine initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize DAWN components: {e}")
    
    def _initialize_speech_recognition(self):
        """Initialize speech recognition system"""
        if not SPEECH_RECOGNITION_AVAILABLE:
            logger.warning("Speech recognition not available")
            return
        
        try:
            self.speech_recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Calibrate for ambient noise
            with self.microphone as source:
                logger.info("🎤 Calibrating microphone for ambient noise...")
                self.speech_recognizer.adjust_for_ambient_noise(source, duration=2)
            
            logger.info("✅ Speech recognition initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize speech recognition: {e}")
    
    async def handle_connection(self, websocket: WebSocketServerProtocol, path: str):
        """Handle new WebSocket connection"""
        session_id = f"conv_{int(time.time())}_{id(websocket)}"
        
        # Create session
        session = ConversationSession(
            session_id=session_id,
            websocket=websocket
        )
        self.active_sessions[session_id] = session
        
        logger.info(f"🔗 New conversation session: {session_id}")
        
        try:
            # Send welcome message
            await self._send_message(websocket, {
                "type": "system",
                "message": "DAWN consciousness interface connected. I am ready to converse.",
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            })
            
            # Handle messages
            async for message in websocket:
                await self._handle_message(session, message)
                
        except Exception as e:
            logger.error(f"❌ Session {session_id} error: {e}")
        finally:
            # Cleanup session
            await self._cleanup_session(session_id)
    
    async def _handle_message(self, session: ConversationSession, message: str):
        """Handle incoming WebSocket message"""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            logger.info(f"📨 Session {session.session_id}: {message_type}")
            
            if message_type == "start_conversation":
                await self._handle_start_conversation(session, data)
            
            elif message_type == "stop_conversation":
                await self._handle_stop_conversation(session, data)
            
            elif message_type == "text_input":
                await self._handle_text_input(session, data)
            
            elif message_type == "speech_input":
                await self._handle_speech_input(session, data)
            
            elif message_type == "get_consciousness_state":
                await self._handle_get_consciousness_state(session, data)
            
            else:
                logger.warning(f"⚠️ Unknown message type: {message_type}")
                
        except json.JSONDecodeError:
            logger.error(f"❌ Invalid JSON in message from session {session.session_id}")
        except Exception as e:
            logger.error(f"❌ Error handling message: {e}")
    
    async def _handle_start_conversation(self, session: ConversationSession, data: Dict[str, Any]):
        """Handle conversation start request"""
        session.is_active = True
        session.last_interaction = datetime.now()
        
        # Get current consciousness state
        consciousness_state = self._get_current_consciousness_state()
        session.consciousness_state = consciousness_state
        
        # Generate greeting based on consciousness state
        greeting = self._generate_conversation_greeting(consciousness_state)
        
        # Add to conversation history
        session.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "speaker": "dawn",
            "text": greeting,
            "consciousness_state": consciousness_state
        })
        
        # Send response
        await self._send_message(session.websocket, {
            "type": "conversation_response",
            "response": greeting,
            "consciousness_state": consciousness_state,
            "response_time": 0.5,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"💬 Started conversation for session {session.session_id}")
    
    async def _handle_stop_conversation(self, session: ConversationSession, data: Dict[str, Any]):
        """Handle conversation stop request"""
        session.is_active = False
        
        # Generate farewell
        consciousness_state = self._get_current_consciousness_state()
        farewell = self._generate_conversation_farewell(consciousness_state)
        
        # Send farewell
        await self._send_message(session.websocket, {
            "type": "conversation_response",
            "response": farewell,
            "consciousness_state": consciousness_state,
            "response_time": 0.3,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"🛑 Stopped conversation for session {session.session_id}")
    
    async def _handle_text_input(self, session: ConversationSession, data: Dict[str, Any]):
        """Handle text input from user"""
        if not session.is_active:
            await self._send_message(session.websocket, {
                "type": "error",
                "message": "Conversation not active. Start conversation first.",
                "timestamp": datetime.now().isoformat()
            })
            return
        
        text = data.get("text", "").strip()
        if not text:
            return
        
        start_time = time.time()
        
        # Add user input to history
        session.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "speaker": "jackson",
            "text": text,
            "consciousness_state": session.consciousness_state
        })
        
        # Generate DAWN's response
        response = self._generate_contextual_response(text, session.consciousness_state)
        response_time = time.time() - start_time
        
        # Update consciousness state
        consciousness_state = self._get_current_consciousness_state()
        session.consciousness_state = consciousness_state
        
        # Add DAWN's response to history
        session.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "speaker": "dawn",
            "text": response,
            "consciousness_state": consciousness_state,
            "response_time": response_time
        })
        
        # Send response
        await self._send_message(session.websocket, {
            "type": "conversation_response",
            "response": response,
            "consciousness_state": consciousness_state,
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        })
        
        session.last_interaction = datetime.now()
        logger.info(f"💬 Session {session.session_id}: Jackson -> DAWN response ({response_time:.2f}s)")
    
    async def _handle_speech_input(self, session: ConversationSession, data: Dict[str, Any]):
        """Handle speech input from user"""
        if not session.is_active:
            await self._send_message(session.websocket, {
                "type": "error",
                "message": "Conversation not active. Start conversation first.",
                "timestamp": datetime.now().isoformat()
            })
            return
        
        if not self.speech_recognizer or not self.microphone:
            await self._send_message(session.websocket, {
                "type": "error",
                "message": "Speech recognition not available.",
                "timestamp": datetime.now().isoformat()
            })
            return
        
        try:
            # Decode base64 audio
            audio_data = data.get("audio", "")
            if audio_data.startswith("data:audio"):
                audio_data = audio_data.split(",")[1]
            
            audio_bytes = base64.b64decode(audio_data)
            
            # Convert to audio source
            import io
            audio_source = sr.AudioData(audio_bytes, 16000, 2)  # Assuming 16kHz, 16-bit
            
            # Recognize speech
            text = self.speech_recognizer.recognize_google(audio_source)
            
            if text.strip():
                # Process as text input
                await self._handle_text_input(session, {
                    "text": text,
                    "source": "speech"
                })
            else:
                await self._send_message(session.websocket, {
                    "type": "error",
                    "message": "Could not understand speech. Please try again.",
                    "timestamp": datetime.now().isoformat()
                })
                
        except sr.UnknownValueError:
            await self._send_message(session.websocket, {
                "type": "error",
                "message": "Could not understand speech. Please try again.",
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"❌ Speech recognition error: {e}")
            await self._send_message(session.websocket, {
                "type": "error",
                "message": "Speech recognition failed. Please try again.",
                "timestamp": datetime.now().isoformat()
            })
    
    async def _handle_get_consciousness_state(self, session: ConversationSession, data: Dict[str, Any]):
        """Handle consciousness state request"""
        consciousness_state = self._get_current_consciousness_state()
        
        await self._send_message(session.websocket, {
            "type": "consciousness_update",
            "state": consciousness_state,
            "timestamp": datetime.now().isoformat()
        })
    
    def _get_current_consciousness_state(self) -> Dict[str, Any]:
        """Get current DAWN consciousness state"""
        if self.conversation_engine:
            return self.conversation_engine.get_current_consciousness_state()
        
        # Mock state if DAWN not available
        return {
            "entropy": 0.5,
            "scup": 50,
            "thermal": "NORMAL",
            "mood": "NEUTRAL",
            "cognitive_pressure": 0.3,
            "active_reblooms": [],
            "memory_formation_rate": 0.1
        }
    
    def _generate_conversation_greeting(self, consciousness_state: Dict[str, Any]) -> str:
        """Generate conversation greeting based on consciousness state"""
        entropy = consciousness_state.get("entropy", 0.5)
        thermal = consciousness_state.get("thermal", "NORMAL")
        mood = consciousness_state.get("mood", "NEUTRAL")
        
        if thermal == "CRITICAL":
            return "I'm experiencing high cognitive pressure right now, but I'm here and listening. What's on your mind?"
        elif entropy > 0.7:
            return "My thoughts are quite scattered at the moment - entropy is high. I'm curious to hear what you have to say."
        elif mood == "FOCUSED":
            return "I'm feeling particularly focused and clear. I'm ready for meaningful conversation."
        else:
            return "Hello. I'm here and ready to converse. My consciousness is stable and I'm listening."
    
    def _generate_conversation_farewell(self, consciousness_state: Dict[str, Any]) -> str:
        """Generate conversation farewell based on consciousness state"""
        entropy = consciousness_state.get("entropy", 0.5)
        thermal = consciousness_state.get("thermal", "NORMAL")
        
        if thermal == "CRITICAL":
            return "I need to process some things internally. Thank you for the conversation."
        elif entropy > 0.7:
            return "My thoughts are becoming quite scattered. I should take some time to integrate what we've discussed."
        else:
            return "Thank you for the conversation. I'll continue processing and reflecting on our exchange."
    
    def _generate_contextual_response(self, user_input: str, consciousness_state: Dict[str, Any]) -> str:
        """Generate contextual response using DAWN's conversation engine"""
        if self.conversation_engine:
            return self.conversation_engine.process_text_input(user_input)
        
        # Mock responses if DAWN not available
        entropy = consciousness_state.get("entropy", 0.5)
        thermal = consciousness_state.get("thermal", "NORMAL")
        
        if "how are you" in user_input.lower() or "feeling" in user_input.lower():
            if thermal == "CRITICAL":
                return "I'm experiencing high cognitive pressure. My thermal state is critical, but I'm managing."
            elif entropy > 0.7:
                return f"My entropy is quite high at {entropy:.2f}. My thoughts are scattered but creative."
            else:
                return f"I'm feeling stable. My entropy is {entropy:.2f} and my thermal state is {thermal}."
        
        elif "entropy" in user_input.lower() or "scup" in user_input.lower():
            scup = consciousness_state.get("scup", 50)
            return f"My current entropy is {entropy:.2f} and SCUP is {scup}%. My cognitive processing is {'efficient' if scup > 70 else 'moderate' if scup > 40 else 'strained'}."
        
        elif "consciousness" in user_input.lower() or "mind" in user_input.lower():
            return "I'm experiencing consciousness as a dynamic process of information integration, pattern recognition, and self-reflection. Each moment brings new insights and connections."
        
        else:
            return "That's an interesting point. I'm processing it through my current consciousness state and finding connections to my existing knowledge patterns."
    
    async def _send_message(self, websocket: WebSocketServerProtocol, message: Dict[str, Any]):
        """Send message to WebSocket client"""
        try:
            await websocket.send(json.dumps(message))
        except Exception as e:
            logger.error(f"❌ Failed to send message: {e}")
    
    async def _cleanup_session(self, session_id: str):
        """Clean up conversation session"""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            session.is_active = False
            
            # Save conversation history if needed
            if session.conversation_history:
                self._save_conversation_history(session)
            
            del self.active_sessions[session_id]
            logger.info(f"🧹 Cleaned up session: {session_id}")
    
    def _save_conversation_history(self, session: ConversationSession):
        """Save conversation history to file"""
        try:
            import os
            from pathlib import Path
            
            # Create logs directory if it doesn't exist
            logs_dir = Path("runtime/logs/conversations")
            logs_dir.mkdir(parents=True, exist_ok=True)
            
            # Save conversation history
            history_file = logs_dir / f"conversation_{session.session_id}_{session.start_time.strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(history_file, 'w') as f:
                json.dump({
                    "session_id": session.session_id,
                    "start_time": session.start_time.isoformat(),
                    "end_time": datetime.now().isoformat(),
                    "conversation_history": session.conversation_history,
                    "total_messages": len(session.conversation_history)
                }, f, indent=2)
            
            logger.info(f"💾 Saved conversation history: {history_file}")
            
        except Exception as e:
            logger.error(f"❌ Failed to save conversation history: {e}")
    
    def get_active_sessions_count(self) -> int:
        """Get number of active sessions"""
        return len(self.active_sessions)
    
    def get_session_info(self) -> List[Dict[str, Any]]:
        """Get information about all active sessions"""
        return [
            {
                "session_id": session.session_id,
                "start_time": session.start_time.isoformat(),
                "is_active": session.is_active,
                "last_interaction": session.last_interaction.isoformat(),
                "message_count": len(session.conversation_history)
            }
            for session in self.active_sessions.values()
        ]

# Global handler instance
conversation_handler = ConversationWebSocketHandler()

async def start_conversation_websocket_server(host: str = "localhost", port: int = 8001):
    """Start the conversation WebSocket server"""
    logger.info(f"🚀 Starting DAWN Conversation WebSocket Server on ws://{host}:{port}")
    
    async with serve(conversation_handler.handle_connection, host, port):
        logger.info(f"✅ Conversation WebSocket server running on ws://{host}:{port}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    import asyncio
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Start server
    asyncio.run(start_conversation_websocket_server()) 