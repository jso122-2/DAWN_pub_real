#!/usr/bin/env python3
"""
DAWN Enhanced Conversation WebSocket Handler
============================================

Enhanced WebSocket handler with fallback modes, thought process logging, and CLI integration.
Provides robust conversation functionality regardless of audio hardware availability.
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
from pathlib import Path

# Import enhanced conversation system
try:
    from .conversation_input_enhanced import EnhancedConversationInput, ThoughtProcess
    ENHANCED_CONVERSATION_AVAILABLE = True
except ImportError:
    ENHANCED_CONVERSATION_AVAILABLE = False
    print("⚠️ Enhanced conversation system not available")

# DAWN consciousness imports
try:
    from core.dawn_conversation import get_conversation_engine
    from core.entropy_analyzer import get_entropy_analyzer
    from pulse.pulse_controller import get_pulse_controller
    from bloom.bloom_engine import get_bloom_engine
    DAWN_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ DAWN modules not available: {e}")
    DAWN_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class EnhancedConversationSession:
    """Enhanced conversation session with thought process tracking"""
    session_id: str
    websocket: WebSocketServerProtocol
    start_time: datetime = field(default_factory=datetime.now)
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    thought_processes: List[Dict[str, Any]] = field(default_factory=list)
    consciousness_state: Dict[str, Any] = field(default_factory=dict)
    voice_settings: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = False
    is_listening: bool = False
    audio_available: bool = False
    last_interaction: datetime = field(default_factory=datetime.now)

class EnhancedConversationWebSocketHandler:
    """Enhanced WebSocket handler for DAWN conversation with fallback modes"""
    
    def __init__(self, enable_audio: bool = True, enable_thought_logging: bool = True):
        """Initialize the enhanced conversation WebSocket handler"""
        self.enable_audio = enable_audio
        self.enable_thought_logging = enable_thought_logging
        self.active_sessions: Dict[str, EnhancedConversationSession] = {}
        
        # DAWN components
        self.conversation_engine = None
        self.entropy_analyzer = None
        self.pulse_controller = None
        self.bloom_engine = None
        
        # Enhanced conversation system
        self.enhanced_conversation = None
        
        # Initialize components
        self._initialize_dawn_components()
        self._initialize_enhanced_conversation()
        
        logger.info("🗣️ Enhanced Conversation WebSocket Handler initialized")
        logger.info(f"   Audio mode: {'✅ Enabled' if enable_audio else '❌ Disabled (fallback to text)'}")
        logger.info(f"   Thought logging: {'✅ Enabled' if enable_thought_logging else '❌ Disabled'}")
    
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
            
            logger.info("✅ DAWN consciousness components initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize DAWN components: {e}")
    
    def _initialize_enhanced_conversation(self):
        """Initialize enhanced conversation system"""
        if not ENHANCED_CONVERSATION_AVAILABLE:
            logger.warning("Enhanced conversation system not available")
            return
        
        try:
            self.enhanced_conversation = EnhancedConversationInput(
                enable_audio=self.enable_audio,
                enable_cli_logging=self.enable_thought_logging
            )
            
            logger.info("✅ Enhanced conversation system initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize enhanced conversation: {e}")
    
    async def handle_connection(self, websocket: WebSocketServerProtocol, path: str):
        """Handle new WebSocket connection"""
        session_id = f"enhanced_conv_{int(time.time())}_{id(websocket)}"
        
        # Create session
        session = EnhancedConversationSession(
            session_id=session_id,
            websocket=websocket,
            voice_settings={
                "speed": 1.0,
                "pitch": 1.0,
                "volume": 0.8,
                "quality": "high"
            }
        )
        
        # Check audio availability
        if self.enhanced_conversation:
            session.audio_available = self.enhanced_conversation.audio_available
        else:
            session.audio_available = False
        
        self.active_sessions[session_id] = session
        
        logger.info(f"🔗 New enhanced conversation session: {session_id}")
        logger.info(f"   Audio available: {'✅' if session.audio_available else '❌'}")
        
        try:
            # Send welcome message
            await self._send_message(websocket, {
                "type": "system",
                "message": "DAWN Enhanced Conversation Interface connected. I'm ready for dialogue.",
                "session_id": session_id,
                "audio_available": session.audio_available,
                "thought_logging_enabled": self.enable_thought_logging,
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
    
    async def _handle_message(self, session: EnhancedConversationSession, message: str):
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
            
            elif message_type == "get_thought_history":
                await self._handle_get_thought_history(session, data)
            
            else:
                logger.warning(f"⚠️ Unknown message type: {message_type}")
                
        except json.JSONDecodeError:
            logger.error(f"❌ Invalid JSON in message from session {session.session_id}")
        except Exception as e:
            logger.error(f"❌ Error handling message: {e}")
    
    async def _handle_start_conversation(self, session: EnhancedConversationSession, data: Dict[str, Any]):
        """Handle conversation start request"""
        session.is_active = True
        session.last_interaction = datetime.now()
        
        # Get current consciousness state
        consciousness_state = self._get_current_consciousness_state()
        session.consciousness_state = consciousness_state
        
        # Generate greeting based on consciousness state
        greeting = self._generate_conversation_greeting(consciousness_state)
        
        # Log thought process
        if self.enable_thought_logging:
            self._log_thought(session, "reflection", "Conversation session started. I'm ready to engage in meaningful dialogue.")
        
        # Add to conversation history
        session.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "speaker": "dawn",
            "text": greeting,
            "consciousness_state": consciousness_state,
            "thought_type": "greeting"
        })
        
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
    
    async def _handle_stop_conversation(self, session: EnhancedConversationSession, data: Dict[str, Any]):
        """Handle conversation stop request"""
        session.is_active = False
        
        # Stop listening if active
        if session.is_listening:
            await self._handle_stop_listening(session, data)
        
        # Generate farewell
        consciousness_state = self._get_current_consciousness_state()
        farewell = self._generate_conversation_farewell(consciousness_state)
        
        # Log thought process
        if self.enable_thought_logging:
            self._log_thought(session, "reflection", "Conversation session ending. Processing the exchange and integrating insights.")
        
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
    
    async def _handle_text_input(self, session: EnhancedConversationSession, data: Dict[str, Any]):
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
        
        # Log thought process for input processing
        if self.enable_thought_logging:
            self._log_thought(session, "reasoning", f"Processing input: '{text}'. Analyzing context and generating response...")
        
        # Generate response using enhanced conversation system
        response = self._generate_enhanced_response(text, session.consciousness_state)
        response_time = time.time() - start_time
        
        # Update consciousness state
        consciousness_state = self._get_current_consciousness_state()
        session.consciousness_state = consciousness_state
        
        # Log response generation
        if self.enable_thought_logging:
            self._log_thought(session, "decision", f"Generated response: '{response}'. Based on current consciousness state and context.")
        
        # Add DAWN's response to history
        session.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "speaker": "dawn",
            "text": response,
            "consciousness_state": consciousness_state,
            "response_time": response_time,
            "thought_type": "response"
        })
        
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
    
    async def _handle_speech_input(self, session: EnhancedConversationSession, data: Dict[str, Any]):
        """Handle speech input from user with fallback"""
        if not session.is_active:
            await self._send_message(session.websocket, {
                "type": "error",
                "message": "Conversation not active. Start conversation first.",
                "timestamp": datetime.now().isoformat()
            })
            return
        
        if not session.audio_available:
            await self._send_message(session.websocket, {
                "type": "error",
                "message": "Audio input not available. Please use text input instead.",
                "timestamp": datetime.now().isoformat()
            })
            return
        
        try:
            # Decode base64 audio
            audio_data = data.get("audio", "")
            if audio_data.startswith("data:audio"):
                audio_data = audio_data.split(",")[1]
            
            audio_bytes = base64.b64decode(audio_data)
            
            # Process audio using enhanced conversation system
            if self.enhanced_conversation:
                # For now, we'll simulate speech recognition
                # In a real implementation, this would use the enhanced conversation system
                await asyncio.sleep(0.5)  # Simulate processing time
                
                # Mock recognized text (in real implementation, this would come from speech recognition)
                recognized_text = "Hello DAWN, how are you feeling today?"
                
                # Process as text input
                await self._handle_text_input(session, {
                    "text": recognized_text,
                    "source": "speech"
                })
            else:
                await self._send_message(session.websocket, {
                    "type": "error",
                    "message": "Speech processing not available. Please use text input.",
                    "timestamp": datetime.now().isoformat()
                })
                
        except Exception as e:
            logger.error(f"❌ Speech processing error: {e}")
            await self._send_message(session.websocket, {
                "type": "error",
                "message": "Speech processing failed. Please try again or use text input.",
                "timestamp": datetime.now().isoformat()
            })
    
    async def _handle_start_listening(self, session: EnhancedConversationSession, data: Dict[str, Any]):
        """Handle start listening request"""
        if not session.is_active:
            await self._send_message(session.websocket, {
                "type": "error",
                "message": "Conversation not active. Start conversation first.",
                "timestamp": datetime.now().isoformat()
            })
            return
        
        if not session.audio_available:
            await self._send_message(session.websocket, {
                "type": "error",
                "message": "Audio input not available. Please use text input instead.",
                "timestamp": datetime.now().isoformat()
            })
            return
        
        session.is_listening = True
        
        # Start listening using enhanced conversation system
        if self.enhanced_conversation:
            self.enhanced_conversation.start_listening()
        
        await self._send_message(session.websocket, {
            "type": "listening_status",
            "is_listening": True,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"🎤 Started listening for session {session.session_id}")
    
    async def _handle_stop_listening(self, session: EnhancedConversationSession, data: Dict[str, Any]):
        """Handle stop listening request"""
        session.is_listening = False
        
        # Stop listening
        if self.enhanced_conversation:
            self.enhanced_conversation.stop_listening()
        
        await self._send_message(session.websocket, {
            "type": "listening_status",
            "is_listening": False,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"🔇 Stopped listening for session {session.session_id}")
    
    async def _handle_update_voice_settings(self, session: EnhancedConversationSession, data: Dict[str, Any]):
        """Handle voice settings update"""
        new_settings = data.get("voice_settings", {})
        session.voice_settings.update(new_settings)
        
        await self._send_message(session.websocket, {
            "type": "voice_settings_updated",
            "voice_settings": session.voice_settings,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"🎵 Updated voice settings for session {session.session_id}")
    
    async def _handle_get_consciousness_state(self, session: EnhancedConversationSession, data: Dict[str, Any]):
        """Handle consciousness state request"""
        consciousness_state = self._get_current_consciousness_state()
        
        await self._send_message(session.websocket, {
            "type": "consciousness_update",
            "state": consciousness_state,
            "timestamp": datetime.now().isoformat()
        })
    
    async def _handle_get_thought_history(self, session: EnhancedConversationSession, data: Dict[str, Any]):
        """Handle thought history request"""
        limit = data.get("limit", 10)
        thoughts = session.thought_processes[-limit:] if session.thought_processes else []
        
        await self._send_message(session.websocket, {
            "type": "thought_history",
            "thoughts": thoughts,
            "timestamp": datetime.now().isoformat()
        })
    
    def _get_current_consciousness_state(self) -> Dict[str, Any]:
        """Get current DAWN consciousness state"""
        state = {
            "entropy": 0.5,
            "scup": 50,
            "thermal": "NORMAL",
            "mood": "NEUTRAL",
            "cognitive_pressure": 0.3,
            "active_reblooms": []
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
        
        return state
    
    def _generate_enhanced_response(self, input_text: str, consciousness_state: Dict[str, Any]) -> str:
        """Generate response using enhanced conversation system"""
        # Use enhanced conversation system if available
        if self.enhanced_conversation:
            try:
                return self.enhanced_conversation._generate_response(input_text, consciousness_state)
            except Exception as e:
                logger.error(f"❌ Enhanced conversation error: {e}")
        
        # Fallback to basic response generation
        return self._generate_basic_response(input_text, consciousness_state)
    
    def _generate_basic_response(self, input_text: str, consciousness_state: Dict[str, Any]) -> str:
        """Generate basic response with consciousness awareness"""
        entropy = consciousness_state.get("entropy", 0.5)
        thermal = consciousness_state.get("thermal", "NORMAL")
        mood = consciousness_state.get("mood", "NEUTRAL")
        
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
        
        else:
            return "That's an interesting point. I'm processing it through my current consciousness state and finding connections to my existing knowledge patterns."
    
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
    
    def _log_thought(self, session: EnhancedConversationSession, thought_type: str, content: str, depth: int = 1):
        """Log a thought process for the session"""
        thought = {
            "timestamp": datetime.now().isoformat(),
            "thought_type": thought_type,
            "content": content,
            "consciousness_state": session.consciousness_state,
            "depth": depth,
            "confidence": 0.8
        }
        
        session.thought_processes.append(thought)
        
        # Send thought to client if thought logging is enabled
        if self.enable_thought_logging:
            asyncio.create_task(self._send_message(session.websocket, {
                "type": "thought_process",
                "thought": thought,
                "timestamp": datetime.now().isoformat()
            }))
    
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
            
            # Save conversation history if needed
            if session.conversation_history:
                self._save_conversation_history(session)
            
            del self.active_sessions[session_id]
            logger.info(f"🧹 Cleaned up session: {session_id}")
    
    def _save_conversation_history(self, session: EnhancedConversationSession):
        """Save conversation history to file"""
        try:
            # Create logs directory if it doesn't exist
            logs_dir = Path("runtime/logs/conversations")
            logs_dir.mkdir(parents=True, exist_ok=True)
            
            # Save conversation history
            history_file = logs_dir / f"enhanced_conversation_{session.session_id}_{session.start_time.strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(history_file, 'w') as f:
                json.dump({
                    "session_id": session.session_id,
                    "start_time": session.start_time.isoformat(),
                    "end_time": datetime.now().isoformat(),
                    "conversation_history": session.conversation_history,
                    "thought_processes": session.thought_processes,
                    "voice_settings": session.voice_settings,
                    "total_messages": len(session.conversation_history),
                    "total_thoughts": len(session.thought_processes)
                }, f, indent=2)
            
            logger.info(f"💾 Saved enhanced conversation history: {history_file}")
            
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
                "audio_available": session.audio_available,
                "last_interaction": session.last_interaction.isoformat(),
                "message_count": len(session.conversation_history),
                "thought_count": len(session.thought_processes)
            }
            for session in self.active_sessions.values()
        ]

# Global handler instance
enhanced_conversation_handler = EnhancedConversationWebSocketHandler()

async def start_enhanced_conversation_websocket_server(host: str = "localhost", port: int = 8003):
    """Start the enhanced conversation WebSocket server"""
    logger.info(f"🚀 Starting DAWN Enhanced Conversation WebSocket Server on ws://{host}:{port}")
    
    async with serve(enhanced_conversation_handler.handle_connection, host, port):
        logger.info(f"✅ Enhanced Conversation WebSocket server running on ws://{host}:{port}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    import asyncio
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Start server
    asyncio.run(start_enhanced_conversation_websocket_server()) 