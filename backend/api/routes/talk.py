from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from datetime import datetime
import asyncio
import json
import logging

logger = logging.getLogger(__name__)

# Import conversation and cognitive modules
from backend.core.conversation_enhanced import EnhancedConversation
from backend.cognitive.consciousness import ConsciousnessModule
from backend.cognitive.conversation import ConversationModule
from backend.cognitive.spontaneity import SpontaneityModule
from backend.cognitive.entropy_fluctuation import EntropyFluctuation
from backend.cognitive.mood_urgency_probe import MoodUrgencyProbe
from backend.cognitive.qualia_kernel import QualiaKernel

talk_router = APIRouter()

# Pydantic models
class TalkMessage(BaseModel):
    content: str
    context: Optional[Dict[str, Any]] = None

class TalkResponse(BaseModel):
    response: str
    metadata: Dict[str, Any]
    timestamp: datetime

class ConversationHistory(BaseModel):
    messages: List[Dict[str, Any]]
    total_count: int
    session_id: Optional[str] = None

class VoiceCommentary(BaseModel):
    text: str
    highlight_color: str = "neutral"
    clarity: bool = False
    entropy: float = 0.5
    pulse_zone: str = "stable"
    timestamp: str

class TalkHandler:
    def __init__(self, tick_engine, dawn_central, ws_manager):
        self.tick_engine = tick_engine
        self.dawn_central = dawn_central
        self.ws_manager = ws_manager
        
        # Initialize cognitive modules
        self.cognitive_modules = {
            'consciousness': ConsciousnessModule(),
            'conversation': ConversationModule(),
            'spontaneity': SpontaneityModule(),
            'entropy': EntropyFluctuation(),
            'mood': MoodUrgencyProbe(),
            'qualia': QualiaKernel()
        }
        
        # Initialize conversation handler
        self.conversation = EnhancedConversation(
            consciousness=self.dawn_central,
            memory=self.dawn_central.memory_manager,
            cognitive_modules=self.cognitive_modules,
            processes=self.dawn_central.processes
        )
        
        # Active sessions
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    async def handle_connection(self, websocket: WebSocket):
        """Handle WebSocket connection for talk interface"""
        # Accept connection
        client_id = await self.ws_manager.connect(websocket)
        
        # Create session
        session_id = f"talk_{client_id}_{datetime.now().timestamp()}"
        self.sessions[session_id] = {
            "client_id": client_id,
            "websocket": websocket,
            "history": [],
            "context": {},
            "started_at": datetime.now()
        }
        
        # Subscribe to relevant topics
        await self.ws_manager.subscribe_client(client_id, [
            "tick_update",
            "consciousness_update",
            "process_event"
        ])
        
        try:
            # Send welcome message
            await websocket.send_json({
                "type": "system",
                "content": "DAWN consciousness interface connected. I am ready to converse.",
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            })
            
            # Handle messages
            while True:
                data = await websocket.receive_json()
                response = await self.process_talk_message(session_id, data)
                
                if response:
                    await websocket.send_json(response)
                    
        except WebSocketDisconnect:
            print(f"Talk session {session_id} disconnected")
        except Exception as e:
            print(f"Talk session error: {e}")
        finally:
            # Clean up session
            if session_id in self.sessions:
                del self.sessions[session_id]
            self.ws_manager.disconnect(websocket)
    
    async def process_talk_message(self, session_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming talk message"""
        if session_id not in self.sessions:
            return {"type": "error", "content": "Invalid session"}
        
        session = self.sessions[session_id]
        msg_type = data.get("type")
        
        if msg_type == "message":
            # Process through conversation system
            content = data.get("content", "")
            context = data.get("context", {})
            
            # Add session context
            context["session_id"] = session_id
            context["history"] = session["history"][-10:]  # Last 10 messages
            
            # Process message
            result = await self.conversation.process(
                content=content,
                context=context,
                connection_id=session["client_id"]
            )
            
            # Store in history
            session["history"].append({
                "role": "user",
                "content": content,
                "timestamp": datetime.now().isoformat()
            })
            
            session["history"].append({
                "role": "assistant",
                "content": result["content"],
                "metadata": result.get("metadata", {}),
                "timestamp": datetime.now().isoformat()
            })
            
            # Generate response
            return {
                "type": "response",
                "content": result["content"],
                "metadata": {
                    "tick": self.tick_engine.current_tick,
                    "scup": self.dawn_central.get_scup(),
                    "mood": self.dawn_central.get_mood(),
                    "entropy": self.dawn_central.get_entropy(),
                    "process": result.get("primary_process"),
                    "cognitive_path": result.get("cognitive_path"),
                    "confidence": result.get("confidence", 0.8)
                },
                "timestamp": datetime.now().isoformat()
            }
        
        elif msg_type == "get_history":
            # Return conversation history
            return {
                "type": "history",
                "data": session["history"],
                "count": len(session["history"]),
                "session_id": session_id
            }
        
        elif msg_type == "clear_history":
            # Clear conversation history
            session["history"] = []
            return {
                "type": "system",
                "content": "Conversation history cleared",
                "timestamp": datetime.now().isoformat()
            }
        
        elif msg_type == "set_context":
            # Update session context
            session["context"].update(data.get("context", {}))
            return {
                "type": "system",
                "content": "Context updated",
                "timestamp": datetime.now().isoformat()
            }
        
        return None

# Dependency to get talk handler
async def get_talk_handler():
    from backend.start_api_fixed import tick_engine, dawn_central, ws_manager
    if not all([tick_engine, dawn_central, ws_manager]):
        raise HTTPException(status_code=503, detail="Talk system not initialized")
    return TalkHandler(tick_engine, dawn_central, ws_manager)

@talk_router.post("/message", response_model=TalkResponse)
async def send_message(
    message: TalkMessage,
    handler: TalkHandler = Depends(get_talk_handler)
):
    """Send a message to DAWN (REST endpoint)"""
    # Create temporary session
    session_id = f"rest_{datetime.now().timestamp()}"
    
    # Process message
    result = await handler.conversation.process(
        content=message.content,
        context=message.context or {},
        connection_id=session_id
    )
    
    return TalkResponse(
        response=result["content"],
        metadata={
            "scup": handler.dawn_central.get_scup(),
            "mood": handler.dawn_central.get_mood(),
            "entropy": handler.dawn_central.get_entropy(),
            "cognitive_path": result.get("cognitive_path", [])
        },
        timestamp=datetime.now()
    )

@talk_router.get("/sessions")
async def get_active_sessions(handler: TalkHandler = Depends(get_talk_handler)):
    """Get list of active talk sessions"""
    sessions_info = []
    
    for session_id, session in handler.sessions.items():
        sessions_info.append({
            "session_id": session_id,
            "client_id": session["client_id"],
            "started_at": session["started_at"].isoformat(),
            "message_count": len(session["history"]),
            "duration": (datetime.now() - session["started_at"]).total_seconds()
        })
    
    return {
        "active_sessions": sessions_info,
        "total": len(sessions_info),
        "timestamp": datetime.now().isoformat()
    }

@talk_router.get("/cognitive/status")
async def get_cognitive_status(handler: TalkHandler = Depends(get_talk_handler)):
    """Get status of all cognitive modules"""
    status = {}
    
    for name, module in handler.cognitive_modules.items():
        status[name] = {
            "active": module.is_active(),
            "metrics": module.get_metrics(),
            "last_update": module.last_update.isoformat() if hasattr(module, 'last_update') else None
        }
    
    return {
        "cognitive_modules": status,
        "timestamp": datetime.now().isoformat()
    }

@talk_router.post("/cognitive/{module_name}/configure")
async def configure_cognitive_module(
    module_name: str,
    config: Dict[str, Any],
    handler: TalkHandler = Depends(get_talk_handler)
):
    """Configure a specific cognitive module"""
    if module_name not in handler.cognitive_modules:
        raise HTTPException(status_code=404, detail=f"Module {module_name} not found")
    
    module = handler.cognitive_modules[module_name]
    module.configure(config)
    
    return {
        "module": module_name,
        "status": "configured",
        "config": config,
        "timestamp": datetime.now().isoformat()
    }

@talk_router.post("/voice-commentary")
async def receive_voice_commentary(commentary: VoiceCommentary):
    """
    Receive DAWN's voice commentary for live GUI display.
    
    This endpoint receives utterances from DAWN's voice-to-gui-owl pipeline
    and can be used by the GUI to display real-time voice feedback with
    emotional coloring and cognitive state information.
    """
    try:
        # Log the received commentary
        logger.info(f"[VOICE] Received commentary: '{commentary.text[:50]}...' | "
                   f"Color: {commentary.highlight_color} | "
                   f"Entropy: {commentary.entropy:.2f} | "
                   f"Zone: {commentary.pulse_zone}")
        
        # Here you could broadcast to connected WebSocket clients
        # or store in a queue for GUI consumption
        
        # For now, just acknowledge receipt
        response = {
            "status": "received",
            "commentary_id": f"voice_{int(datetime.now().timestamp() * 1000)}",
            "processed_at": datetime.now().isoformat(),
            "text_length": len(commentary.text),
            "cognitive_markers": {
                "highlight_color": commentary.highlight_color,
                "clarity": commentary.clarity,
                "entropy": commentary.entropy,
                "pulse_zone": commentary.pulse_zone
            }
        }
        
        return response
        
    except Exception as e:
        logger.error(f"[VOICE] Error processing commentary: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing voice commentary: {str(e)}") 