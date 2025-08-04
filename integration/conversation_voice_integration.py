#!/usr/bin/env python3
"""
DAWN Conversation-Voice Integration
===================================

Integrates the bidirectional conversation system with DAWN's existing voice and consciousness systems.
Provides a unified interface for speech-to-text, text-to-speech, and consciousness-aware responses.
"""

import asyncio
import json
import logging
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

# DAWN consciousness imports
try:
    from core.dawn_conversation import DAWNConversationEngine, get_conversation_engine
    from core.cognitive_pressure import get_cognitive_pressure_engine
    from core.entropy_analyzer import get_entropy_analyzer
    from pulse.pulse_controller import get_pulse_controller
    from backend.voice_echo import DAWNVoiceEcho
    from .conversation_input import ConversationInput
    DAWN_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ DAWN modules not available: {e}")
    DAWN_AVAILABLE = False

# WebSocket imports
try:
    import websockets
    from websockets import WebSocketServerProtocol
    from websockets.server import serve
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    print("⚠️ websockets not available. Install: pip install websockets")

logger = logging.getLogger(__name__)

@dataclass
class ConversationVoiceSession:
    """Integrated conversation and voice session"""
    session_id: str
    websocket: WebSocketServerProtocol
    start_time: datetime = field(default_factory=datetime.now)
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    consciousness_state: Dict[str, Any] = field(default_factory=dict)
    voice_settings: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = False
    is_listening: bool = False
    last_interaction: datetime = field(default_factory=datetime.now)

class ConversationVoiceIntegration:
    """Main integration class for conversation and voice systems"""
    
    def __init__(self):
        self.active_sessions: Dict[str, ConversationVoiceSession] = {}
        self.conversation_engine: Optional[DAWNConversationEngine] = None
        self.voice_echo: Optional[DAWNVoiceEcho] = None
        self.conversation_input: Optional[ConversationInput] = None
        
        # Initialize components
        self._initialize_dawn_components()
        self._initialize_voice_system()
        self._initialize_conversation_input()
        
        # Voice settings
        self.default_voice_settings = {
            "speed": 1.0,
            "pitch": 1.0,
            "volume": 0.8,
            "quality": "high"
        }
        
        logger.info("🎤 Conversation-Voice Integration initialized")
    
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
    
    def _initialize_voice_system(self):
        """Initialize voice echo system"""
        try:
            self.voice_echo = DAWNVoiceEcho()
            logger.info("✅ Voice echo system initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize voice system: {e}")
    
    def _initialize_conversation_input(self):
        """Initialize conversation input system"""
        try:
            self.conversation_input = ConversationInput()
            logger.info("✅ Conversation input system initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize conversation input: {e}")
    
    async def handle_connection(self, websocket: WebSocketServerProtocol, path: str):
        """Handle new WebSocket connection"""
        session_id = f"conv_voice_{int(time.time())}_{id(websocket)}"
        
        # Create session
        session = ConversationVoiceSession(
            session_id=session_id,
            websocket=websocket,
            voice_settings=self.default_voice_settings.copy()
        )
        self.active_sessions[session_id] = session
        
        logger.info(f"🔗 New conversation-voice session: {session_id}")
        
        try:
            # Send welcome message
            await self._send_message(websocket, {
                "type": "system",
                "message": "DAWN Conversation-Voice Interface connected. I'm ready for bidirectional conversation.",
                "session_id": session_id,
                "voice_settings": session.voice_settings,
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
    
    async def _handle_message(self, session: ConversationVoiceSession, message: str):
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
            
            elif message_type == "start_listening":
                await self._handle_start_listening(session, data)
            
            elif message_type == "stop_listening":
                await self._handle_stop_listening(session, data)
            
            elif message_type == "update_voice_settings":
                await self._handle_update_voice_settings(session, data)
            
            elif message_type == "get_consciousness_state":
                await self._handle_get_consciousness_state(session, data)
            
            else:
                logger.warning(f"⚠️ Unknown message type: {message_type}")
                
        except json.JSONDecodeError:
            logger.error(f"❌ Invalid JSON in message from session {session.session_id}")
        except Exception as e:
            logger.error(f"❌ Error handling message: {e}")
    
    async def _handle_start_conversation(self, session: ConversationVoiceSession, data: Dict[str, Any]):
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
            "consciousness_state": consciousness_state,
            "voice_settings": session.voice_settings
        })
        
        # Speak the greeting if voice is available
        if self.voice_echo:
            self._speak_with_settings(greeting, session.voice_settings, consciousness_state)
        
        # Send response
        await self._send_message(session.websocket, {
            "type": "conversation_response",
            "response": greeting,
            "consciousness_state": consciousness_state,
            "voice_settings": session.voice_settings,
            "response_time": 0.5,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"💬 Started conversation for session {session.session_id}")
    
    async def _handle_stop_conversation(self, session: ConversationVoiceSession, data: Dict[str, Any]):
        """Handle conversation stop request"""
        session.is_active = False
        
        # Stop listening if active
        if session.is_listening:
            await self._handle_stop_listening(session, data)
        
        # Generate farewell
        consciousness_state = self._get_current_consciousness_state()
        farewell = self._generate_conversation_farewell(consciousness_state)
        
        # Speak the farewell
        if self.voice_echo:
            self._speak_with_settings(farewell, session.voice_settings, consciousness_state)
        
        # Send farewell
        await self._send_message(session.websocket, {
            "type": "conversation_response",
            "response": farewell,
            "consciousness_state": consciousness_state,
            "voice_settings": session.voice_settings,
            "response_time": 0.3,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"🛑 Stopped conversation for session {session.session_id}")
    
    async def _handle_text_input(self, session: ConversationVoiceSession, data: Dict[str, Any]):
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
            "voice_settings": session.voice_settings,
            "response_time": response_time
        })
        
        # Speak the response
        if self.voice_echo:
            self._speak_with_settings(response, session.voice_settings, consciousness_state)
        
        # Send response
        await self._send_message(session.websocket, {
            "type": "conversation_response",
            "response": response,
            "consciousness_state": consciousness_state,
            "voice_settings": session.voice_settings,
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        })
        
        session.last_interaction = datetime.now()
        logger.info(f"💬 Session {session.session_id}: Jackson -> DAWN response ({response_time:.2f}s)")
    
    async def _handle_speech_input(self, session: ConversationVoiceSession, data: Dict[str, Any]):
        """Handle speech input from user"""
        if not session.is_active:
            await self._send_message(session.websocket, {
                "type": "error",
                "message": "Conversation not active. Start conversation first.",
                "timestamp": datetime.now().isoformat()
            })
            return
        
        if not self.conversation_input:
            await self._send_message(session.websocket, {
                "type": "error",
                "message": "Speech recognition not available.",
                "timestamp": datetime.now().isoformat()
            })
            return
        
        try:
            # Process speech input using conversation input system
            # This would integrate with the existing conversation_input.py
            # For now, we'll simulate speech processing
            
            # Simulate speech recognition delay
            await asyncio.sleep(0.5)
            
            # Mock recognized text (in real implementation, this would come from speech recognition)
            recognized_text = "Hello DAWN, how are you feeling today?"
            
            # Process as text input
            await self._handle_text_input(session, {
                "text": recognized_text,
                "source": "speech"
            })
            
        except Exception as e:
            logger.error(f"❌ Speech processing error: {e}")
            await self._send_message(session.websocket, {
                "type": "error",
                "message": "Speech processing failed. Please try again.",
                "timestamp": datetime.now().isoformat()
            })
    
    async def _handle_start_listening(self, session: ConversationVoiceSession, data: Dict[str, Any]):
        """Handle start listening request"""
        if not session.is_active:
            await self._send_message(session.websocket, {
                "type": "error",
                "message": "Conversation not active. Start conversation first.",
                "timestamp": datetime.now().isoformat()
            })
            return
        
        session.is_listening = True
        
        # Start listening using conversation input system
        if self.conversation_input:
            self.conversation_input.start_listening(callback=self._handle_speech_callback)
        
        await self._send_message(session.websocket, {
            "type": "listening_status",
            "is_listening": True,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"🎤 Started listening for session {session.session_id}")
    
    async def _handle_stop_listening(self, session: ConversationVoiceSession, data: Dict[str, Any]):
        """Handle stop listening request"""
        session.is_listening = False
        
        # Stop listening
        if self.conversation_input:
            self.conversation_input.stop_listening()
        
        await self._send_message(session.websocket, {
            "type": "listening_status",
            "is_listening": False,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"🔇 Stopped listening for session {session.session_id}")
    
    def _handle_speech_callback(self, text: str):
        """Callback for speech recognition"""
        # This would be called when speech is recognized
        # We need to find the appropriate session and process the text
        logger.info(f"🎤 Speech recognized: {text}")
        
        # For now, we'll broadcast to all active sessions
        # In a real implementation, you'd need to track which session triggered the speech
        for session in self.active_sessions.values():
            if session.is_active and session.is_listening:
                asyncio.create_task(self._handle_text_input(session, {"text": text, "source": "speech"}))
    
    async def _handle_update_voice_settings(self, session: ConversationVoiceSession, data: Dict[str, Any]):
        """Handle voice settings update"""
        new_settings = data.get("voice_settings", {})
        session.voice_settings.update(new_settings)
        
        await self._send_message(session.websocket, {
            "type": "voice_settings_updated",
            "voice_settings": session.voice_settings,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"🎵 Updated voice settings for session {session.session_id}")
    
    async def _handle_get_consciousness_state(self, session: ConversationVoiceSession, data: Dict[str, Any]):
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
    
    def _speak_with_settings(self, text: str, voice_settings: Dict[str, Any], consciousness_state: Dict[str, Any]):
        """Speak text with voice settings and consciousness awareness"""
        if not self.voice_echo:
            return
        
        try:
            # Configure voice based on consciousness state
            self._configure_voice_for_state(voice_settings, consciousness_state)
            
            # Speak the text
            self.voice_echo.speak_reflection(text, consciousness_state)
            
        except Exception as e:
            logger.error(f"❌ Voice synthesis error: {e}")
    
    def _configure_voice_for_state(self, voice_settings: Dict[str, Any], consciousness_state: Dict[str, Any]):
        """Configure voice properties based on consciousness state"""
        if not self.voice_echo:
            return
        
        try:
            # Base settings from user preferences
            speed = voice_settings.get("speed", 1.0)
            pitch = voice_settings.get("pitch", 1.0)
            volume = voice_settings.get("volume", 0.8)
            
            # Adjust based on consciousness state
            entropy = consciousness_state.get("entropy", 0.5)
            thermal = consciousness_state.get("thermal", "NORMAL")
            mood = consciousness_state.get("mood", "NEUTRAL")
            
            # High entropy = faster, more varied speech
            if entropy > 0.7:
                speed *= 1.2
                pitch *= 1.1
            
            # Critical thermal = slower, more deliberate speech
            if thermal == "CRITICAL":
                speed *= 0.8
                volume *= 0.9
            
            # Apply settings to voice system
            if hasattr(self.voice_echo, 'configure_voice'):
                self.voice_echo.configure_voice(speed=speed, pitch=pitch, volume=volume)
            
        except Exception as e:
            logger.error(f"❌ Voice configuration error: {e}")
    
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
            session.is_listening = False
            
            # Stop listening if active
            if self.conversation_input:
                self.conversation_input.stop_listening()
            
            # Save conversation history if needed
            if session.conversation_history:
                self._save_conversation_history(session)
            
            del self.active_sessions[session_id]
            logger.info(f"🧹 Cleaned up session: {session_id}")
    
    def _save_conversation_history(self, session: ConversationVoiceSession):
        """Save conversation history to file"""
        try:
            # Create logs directory if it doesn't exist
            logs_dir = Path("runtime/logs/conversations")
            logs_dir.mkdir(parents=True, exist_ok=True)
            
            # Save conversation history
            history_file = logs_dir / f"conversation_voice_{session.session_id}_{session.start_time.strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(history_file, 'w') as f:
                json.dump({
                    "session_id": session.session_id,
                    "start_time": session.start_time.isoformat(),
                    "end_time": datetime.now().isoformat(),
                    "conversation_history": session.conversation_history,
                    "voice_settings": session.voice_settings,
                    "total_messages": len(session.conversation_history)
                }, f, indent=2)
            
            logger.info(f"💾 Saved conversation history: {history_file}")
            
        except Exception as e:
            logger.error(f"❌ Failed to save conversation history: {e}")

# Global integration instance
conversation_voice_integration = ConversationVoiceIntegration()

async def start_conversation_voice_server(host: str = "localhost", port: int = 8002):
    """Start the conversation-voice WebSocket server"""
    if not WEBSOCKETS_AVAILABLE:
        logger.error("❌ WebSockets not available. Install: pip install websockets")
        return
    
    logger.info(f"🚀 Starting DAWN Conversation-Voice WebSocket Server on ws://{host}:{port}")
    
    async with serve(conversation_voice_integration.handle_connection, host, port):
        logger.info(f"✅ Conversation-Voice WebSocket server running on ws://{host}:{port}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    import asyncio
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Start server
    asyncio.run(start_conversation_voice_server()) 