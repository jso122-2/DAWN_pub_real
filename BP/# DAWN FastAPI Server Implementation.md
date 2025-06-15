# DAWN FastAPI Server Implementation

## 1. Main API Server

```python
# backend/start_api_fixed.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import uvicorn
from typing import Dict, Any
from datetime import datetime

# Import routers
from api.routes.consciousness import consciousness_router
from api.routes.visualization import visualization_router
from api.routes.talk import talk_router

# Import managers
from api.websocket_manager import WebSocketManager
from core.unified_tick_engine import UnifiedTickEngine
from core.dawn_central import DAWNCentral

# Global instances
tick_engine = None
dawn_central = None
ws_manager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global tick_engine, dawn_central, ws_manager
    
    print("[DAWN] Initializing consciousness engine...")
    
    # Initialize core systems
    tick_engine = UnifiedTickEngine()
    dawn_central = DAWNCentral()
    ws_manager = WebSocketManager(tick_engine, dawn_central)
    
    # Start tick loop
    tick_task = asyncio.create_task(tick_engine.start())
    
    # Start WebSocket broadcast loop
    broadcast_task = asyncio.create_task(ws_manager.broadcast_loop())
    
    print("[DAWN] Consciousness engine online")
    
    yield
    
    # Shutdown
    print("[DAWN] Shutting down consciousness engine...")
    tick_task.cancel()
    broadcast_task.cancel()
    await tick_engine.shutdown()
    await ws_manager.disconnect_all()

# Create FastAPI app
app = FastAPI(
    title="DAWN Consciousness Engine API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(consciousness_router, prefix="/api/consciousness", tags=["consciousness"])
app.include_router(visualization_router, prefix="/api/visualization", tags=["visualization"])
app.include_router(talk_router, prefix="/api/talk", tags=["talk"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "status": "online",
        "engine": "DAWN Consciousness Engine",
        "version": "1.0.0",
        "tick": tick_engine.current_tick if tick_engine else 0
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "tick_engine": tick_engine is not None and tick_engine.is_running,
            "websocket": ws_manager is not None and ws_manager.active_connections > 0,
            "consciousness": dawn_central is not None and dawn_central.is_active
        }
    }

# Main WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Main WebSocket connection for real-time updates"""
    await ws_manager.connect(websocket)
    
    try:
        while True:
            # Receive and process messages
            data = await websocket.receive_json()
            response = await ws_manager.handle_message(websocket, data)
            
            if response:
                await websocket.send_json(response)
                
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket)

# Tick stream WebSocket endpoint
@app.websocket("/ws/tick-stream")
async def tick_stream_endpoint(websocket: WebSocket):
    """Dedicated WebSocket for tick stream updates"""
    await ws_manager.connect(websocket)
    
    try:
        # Subscribe to tick updates
        client_id = None
        for cid, conn_info in ws_manager.connections.items():
            if conn_info.websocket == websocket:
                client_id = cid
                break
        
        if client_id:
            await ws_manager.subscribe_client(client_id, ["tick_update"])
        
        while True:
            # Keep connection alive and handle any messages
            try:
                data = await websocket.receive_json()
                if data.get("type") == "ping":
                    await websocket.send_json({"type": "pong", "timestamp": datetime.now().isoformat()})
            except WebSocketDisconnect:
                break
            except Exception as e:
                print(f"Tick stream error: {e}")
                break
                
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        print(f"Tick stream error: {e}")
        ws_manager.disconnect(websocket)

# Talk WebSocket endpoint
@app.websocket("/ws/talk")
async def talk_websocket_endpoint(websocket: WebSocket):
    """Dedicated WebSocket for talk interface"""
    from api.routes.talk import TalkHandler
    
    handler = TalkHandler(tick_engine, dawn_central, ws_manager)
    await handler.handle_connection(websocket)

if __name__ == "__main__":
    uvicorn.run(
        "start_api_fixed:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
```

## 2. WebSocket Manager

```python
# backend/api/websocket_manager.py
from fastapi import WebSocket
from typing import Dict, List, Set, Any, Optional
import asyncio
import json
from datetime import datetime
from collections import defaultdict

class ConnectionInfo:
    def __init__(self, websocket: WebSocket, client_id: str):
        self.websocket = websocket
        self.client_id = client_id
        self.connected_at = datetime.now()
        self.subscriptions: Set[str] = set()
        self.metadata: Dict[str, Any] = {}

class WebSocketManager:
    def __init__(self, tick_engine, dawn_central):
        self.tick_engine = tick_engine
        self.dawn_central = dawn_central
        self.connections: Dict[str, ConnectionInfo] = {}
        self.topic_subscribers: Dict[str, Set[str]] = defaultdict(set)
        self._client_counter = 0
        
    @property
    def active_connections(self) -> int:
        return len(self.connections)
    
    async def connect(self, websocket: WebSocket) -> str:
        """Accept new WebSocket connection"""
        await websocket.accept()
        
        # Generate client ID
        self._client_counter += 1
        client_id = f"client_{self._client_counter}_{datetime.now().timestamp()}"
        
        # Store connection info
        conn_info = ConnectionInfo(websocket, client_id)
        self.connections[client_id] = conn_info
        
        # Send initial connection message
        await self.send_personal_message({
            "type": "connection",
            "client_id": client_id,
            "message": "Connected to DAWN consciousness engine",
            "timestamp": datetime.now().isoformat()
        }, websocket)
        
        # Subscribe to default topics
        await self.subscribe_client(client_id, ["tick_update", "consciousness_update"])
        
        print(f"[WebSocket] Client {client_id} connected")
        return client_id
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        # Find client by websocket
        client_id = None
        for cid, conn_info in self.connections.items():
            if conn_info.websocket == websocket:
                client_id = cid
                break
        
        if client_id:
            # Remove from all subscriptions
            for topic in self.connections[client_id].subscriptions:
                self.topic_subscribers[topic].discard(client_id)
            
            # Remove connection
            del self.connections[client_id]
            print(f"[WebSocket] Client {client_id} disconnected")
    
    async def disconnect_all(self):
        """Disconnect all clients gracefully"""
        for client_id, conn_info in list(self.connections.items()):
            try:
                await conn_info.websocket.close()
            except:
                pass
        self.connections.clear()
        self.topic_subscribers.clear()
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Send message to specific WebSocket"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending message: {e}")
    
    async def broadcast(self, message: Dict[str, Any], topic: Optional[str] = None):
        """Broadcast message to all connected clients or topic subscribers"""
        if topic:
            # Send to topic subscribers only
            subscriber_ids = self.topic_subscribers.get(topic, set())
            for client_id in subscriber_ids:
                if client_id in self.connections:
                    await self.send_personal_message(
                        message, 
                        self.connections[client_id].websocket
                    )
        else:
            # Send to all clients
            for conn_info in self.connections.values():
                await self.send_personal_message(message, conn_info.websocket)
    
    async def subscribe_client(self, client_id: str, topics: List[str]):
        """Subscribe client to topics"""
        if client_id not in self.connections:
            return
        
        for topic in topics:
            self.topic_subscribers[topic].add(client_id)
            self.connections[client_id].subscriptions.add(topic)
    
    async def unsubscribe_client(self, client_id: str, topics: List[str]):
        """Unsubscribe client from topics"""
        if client_id not in self.connections:
            return
        
        for topic in topics:
            self.topic_subscribers[topic].discard(client_id)
            self.connections[client_id].subscriptions.discard(topic)
    
    async def handle_message(self, websocket: WebSocket, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle incoming WebSocket message"""
        # Find client
        client_id = None
        for cid, conn_info in self.connections.items():
            if conn_info.websocket == websocket:
                client_id = cid
                break
        
        if not client_id:
            return {"type": "error", "message": "Client not found"}
        
        msg_type = message.get("type")
        
        if msg_type == "ping":
            return {"type": "pong", "timestamp": datetime.now().isoformat()}
        
        elif msg_type == "subscribe":
            topics = message.get("topics", [])
            await self.subscribe_client(client_id, topics)
            return {"type": "subscribed", "topics": topics}
        
        elif msg_type == "unsubscribe":
            topics = message.get("topics", [])
            await self.unsubscribe_client(client_id, topics)
            return {"type": "unsubscribed", "topics": topics}
        
        elif msg_type == "get_state":
            # Return current system state
            return {
                "type": "state",
                "data": {
                    "tick": self.tick_engine.current_tick,
                    "scup": self.dawn_central.get_scup(),
                    "entropy": self.dawn_central.get_entropy(),
                    "mood": self.dawn_central.get_mood(),
                    "consciousness_state": self.dawn_central.get_state()
                }
            }
        
        return None
    
    async def broadcast_loop(self):
        """Main broadcast loop for system updates"""
        while True:
            try:
                # Get current state
                state_data = {
                    "type": "tick_update",
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "tick": self.tick_engine.current_tick,
                        "scup": self.dawn_central.get_scup(),
                        "entropy": self.dawn_central.get_entropy(),
                        "mood": self.dawn_central.get_mood(),
                        "active_processes": self.dawn_central.get_active_processes(),
                        "consciousness_state": self.dawn_central.get_state()
                    }
                }
                
                # Broadcast to tick_update subscribers
                await self.broadcast(state_data, "tick_update")
                
                # Check for consciousness state changes
                if self.dawn_central.has_state_changed():
                    consciousness_data = {
                        "type": "consciousness_update",
                        "timestamp": datetime.now().isoformat(),
                        "data": {
                            "state": self.dawn_central.get_state(),
                            "metrics": self.dawn_central.get_consciousness_metrics()
                        }
                    }
                    await self.broadcast(consciousness_data, "consciousness_update")
                
                # Wait for next update
                await asyncio.sleep(0.1)  # 10Hz update rate
                
            except Exception as e:
                print(f"Broadcast loop error: {e}")
                await asyncio.sleep(1)
```

## 3. Consciousness Routes

```python
# backend/api/routes/consciousness.py
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

consciousness_router = APIRouter()

# Pydantic models
class ConsciousnessState(BaseModel):
    tick: int
    scup: float = Field(..., ge=0, le=100)
    entropy: float = Field(..., ge=0, le=1)
    mood: str
    state: str
    timestamp: datetime

class ConsciousnessUpdate(BaseModel):
    entropy: Optional[float] = Field(None, ge=0, le=1)
    mood: Optional[str] = None
    process_activation: Optional[Dict[str, bool]] = None

class ConsciousnessMetrics(BaseModel):
    neural_activity: float
    quantum_coherence: float
    pattern_recognition: float
    memory_utilization: float
    chaos_factor: float

# Dependency to get dawn_central
async def get_dawn_central():
    from start_api_fixed import dawn_central
    if not dawn_central:
        raise HTTPException(status_code=503, detail="Consciousness engine not initialized")
    return dawn_central

@consciousness_router.get("/state", response_model=ConsciousnessState)
async def get_consciousness_state(dawn_central=Depends(get_dawn_central)):
    """Get current consciousness state"""
    return ConsciousnessState(
        tick=dawn_central.tick_engine.current_tick,
        scup=dawn_central.get_scup(),
        entropy=dawn_central.get_entropy(),
        mood=dawn_central.get_mood(),
        state=dawn_central.get_state(),
        timestamp=datetime.now()
    )

@consciousness_router.post("/update")
async def update_consciousness(
    update: ConsciousnessUpdate,
    dawn_central=Depends(get_dawn_central)
):
    """Update consciousness parameters"""
    if update.entropy is not None:
        dawn_central.set_entropy(update.entropy)
    
    if update.mood:
        dawn_central.set_mood(update.mood)
    
    if update.process_activation:
        for process, active in update.process_activation.items():
            if active:
                dawn_central.activate_process(process)
            else:
                dawn_central.deactivate_process(process)
    
    return {"status": "updated", "timestamp": datetime.now()}

@consciousness_router.get("/metrics", response_model=ConsciousnessMetrics)
async def get_consciousness_metrics(dawn_central=Depends(get_dawn_central)):
    """Get detailed consciousness metrics"""
    metrics = dawn_central.get_consciousness_metrics()
    return ConsciousnessMetrics(**metrics)

@consciousness_router.get("/history")
async def get_consciousness_history(
    duration: int = 100,
    dawn_central=Depends(get_dawn_central)
):
    """Get consciousness state history"""
    history = dawn_central.get_history(duration)
    return {
        "duration": duration,
        "history": history,
        "timestamp": datetime.now()
    }

@consciousness_router.post("/reset")
async def reset_consciousness(dawn_central=Depends(get_dawn_central)):
    """Reset consciousness to initial state"""
    dawn_central.reset()
    return {"status": "reset", "timestamp": datetime.now()}

@consciousness_router.get("/processes")
async def get_active_processes(dawn_central=Depends(get_dawn_central)):
    """Get list of active processes"""
    return {
        "active": dawn_central.get_active_processes(),
        "available": dawn_central.get_available_processes(),
        "timestamp": datetime.now()
    }

@consciousness_router.post("/process/{process_name}/{action}")
async def control_process(
    process_name: str,
    action: str,
    dawn_central=Depends(get_dawn_central)
):
    """Control process execution (start/stop/restart)"""
    if action not in ["start", "stop", "restart"]:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    if action == "start":
        success = dawn_central.activate_process(process_name)
    elif action == "stop":
        success = dawn_central.deactivate_process(process_name)
    else:  # restart
        dawn_central.deactivate_process(process_name)
        success = dawn_central.activate_process(process_name)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"Process {process_name} not found")
    
    return {
        "process": process_name,
        "action": action,
        "status": "success",
        "timestamp": datetime.now()
    }
```

## 4. Visualization Routes

```python
# backend/api/routes/visualization.py
from fastapi import APIRouter, HTTPException, Depends, Response
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from datetime import datetime
import base64
import io

visualization_router = APIRouter()

# Import visualizers
from visualizers.matplotlib_visualizers import (
    ConsciousnessWaveVisualizer,
    EntropyThermalVisualizer,
    NeuralActivityVisualizer,
    AlignmentMatrixVisualizer,
    BloomPatternVisualizer,
    MoodGradientVisualizer
)

# Pydantic models
class VisualizationRequest(BaseModel):
    type: str
    format: str = "base64"  # base64 or raw
    width: int = 800
    height: int = 600
    params: Optional[Dict[str, Any]] = None

class VisualizationList(BaseModel):
    visualizations: List[str]
    descriptions: Dict[str, str]

# Initialize visualizers
visualizers = {
    "consciousness_wave": ConsciousnessWaveVisualizer(),
    "entropy_thermal": EntropyThermalVisualizer(),
    "neural_activity": NeuralActivityVisualizer(),
    "alignment_matrix": AlignmentMatrixVisualizer(),
    "bloom_pattern": BloomPatternVisualizer(),
    "mood_gradient": MoodGradientVisualizer()
}

# Dependency to get dawn_central
async def get_dawn_central():
    from start_api_fixed import dawn_central
    if not dawn_central:
        raise HTTPException(status_code=503, detail="Consciousness engine not initialized")
    return dawn_central

@visualization_router.get("/available", response_model=VisualizationList)
async def get_available_visualizations():
    """Get list of available visualizations"""
    descriptions = {
        "consciousness_wave": "Real-time SCUP wave visualization",
        "entropy_thermal": "Entropy distribution heat map",
        "neural_activity": "Neural network activity matrix",
        "alignment_matrix": "System alignment coherence",
        "bloom_pattern": "Consciousness bloom patterns",
        "mood_gradient": "Mood state transitions"
    }
    
    return VisualizationList(
        visualizations=list(visualizers.keys()),
        descriptions=descriptions
    )

@visualization_router.post("/generate")
async def generate_visualization(
    request: VisualizationRequest,
    dawn_central=Depends(get_dawn_central)
):
    """Generate a specific visualization"""
    if request.type not in visualizers:
        raise HTTPException(status_code=404, detail=f"Visualization type {request.type} not found")
    
    try:
        # Get visualizer
        visualizer = visualizers[request.type]
        
        # Prepare data based on visualization type
        if request.type == "consciousness_wave":
            data = {
                "scup_history": dawn_central.get_scup_history(100),
                "current_tick": dawn_central.tick_engine.current_tick
            }
        elif request.type == "entropy_thermal":
            data = {
                "entropy_map": dawn_central.get_entropy_distribution(),
                "temperature": dawn_central.get_system_temperature()
            }
        elif request.type == "neural_activity":
            data = {
                "neural_matrix": dawn_central.get_neural_activity_matrix(),
                "activation_levels": dawn_central.get_activation_levels()
            }
        elif request.type == "alignment_matrix":
            data = {
                "alignment_data": dawn_central.get_alignment_matrix(),
                "coherence": dawn_central.get_coherence_score()
            }
        elif request.type == "bloom_pattern":
            data = {
                "bloom_state": dawn_central.get_bloom_pattern(),
                "growth_rate": dawn_central.get_growth_metrics()
            }
        else:  # mood_gradient
            data = {
                "mood_vector": dawn_central.get_mood_vector(),
                "mood_history": dawn_central.get_mood_history(50)
            }
        
        # Apply custom parameters
        if request.params:
            data.update(request.params)
        
        # Generate visualization
        image_data = visualizer.generate(data, size=(request.width, request.height))
        
        if request.format == "raw":
            # Return raw image bytes
            image_bytes = base64.b64decode(image_data.split(',')[1])
            return Response(content=image_bytes, media_type="image/png")
        else:
            # Return base64 encoded
            return {
                "type": request.type,
                "data": image_data,
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visualization generation failed: {str(e)}")

@visualization_router.get("/stream/{viz_type}")
async def stream_visualization(
    viz_type: str,
    dawn_central=Depends(get_dawn_central)
):
    """Get streaming endpoint information for visualization"""
    if viz_type not in visualizers:
        raise HTTPException(status_code=404, detail=f"Visualization type {viz_type} not found")
    
    return {
        "type": viz_type,
        "websocket_topic": f"viz_{viz_type}",
        "update_rate": visualizers[viz_type].update_interval,
        "description": f"Subscribe to 'viz_{viz_type}' topic via WebSocket for real-time updates"
    }

@visualization_router.post("/snapshot/{viz_type}")
async def capture_snapshot(
    viz_type: str,
    dawn_central=Depends(get_dawn_central)
):
    """Capture a snapshot of current visualization state"""
    if viz_type not in visualizers:
        raise HTTPException(status_code=404, detail=f"Visualization type {viz_type} not found")
    
    # Similar to generate but optimized for quick capture
    request = VisualizationRequest(type=viz_type)
    return await generate_visualization(request, dawn_central)

@visualization_router.get("/composite")
async def get_composite_visualization(
    types: List[str],
    dawn_central=Depends(get_dawn_central)
):
    """Generate multiple visualizations at once"""
    results = {}
    
    for viz_type in types:
        if viz_type in visualizers:
            try:
                request = VisualizationRequest(type=viz_type, width=400, height=300)
                result = await generate_visualization(request, dawn_central)
                results[viz_type] = result
            except Exception as e:
                results[viz_type] = {"error": str(e)}
    
    return {
        "visualizations": results,
        "timestamp": datetime.now().isoformat()
    }
```

## 5. Talk Routes

```python
# backend/api/routes/talk.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from datetime import datetime
import asyncio
import json

# Import conversation and cognitive modules
from core.conversation_enhanced import EnhancedConversation
from cognitive.consciousness import ConsciousnessModule
from cognitive.conversation import ConversationModule
from cognitive.spontaneity import SpontaneityModule
from cognitive.entropy_fluctuation import EntropyFluctuation
from cognitive.mood_urgency_probe import MoodUrgencyProbe
from cognitive.qualia_kernel import QualiaKernel

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
    from start_api_fixed import tick_engine, dawn_central, ws_manager
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
```

## 6. Requirements

```txt
# backend/requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
websockets==12.0
pydantic==2.5.0
python-multipart==0.0.6
asyncio==3.4.3
numpy==1.24.3
matplotlib==3.7.1
Pillow==10.0.0
```

## 7. Running the Server

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python start_api_fixed.py

# Or with auto-reload for development
uvicorn start_api_fixed:app --reload --host 0.0.0.0 --port 8000
```

## Key Features

1. **Complete FastAPI Server**:
   - WebSocket support for real-time communication
   - REST endpoints for all major functions
   - Proper error handling and validation

2. **WebSocket Manager**:
   - Topic-based subscriptions
   - Client management
   - Automatic broadcasting of system updates

3. **Consciousness Routes**:
   - Full CRUD operations for consciousness state
   - Process management
   - Historical data access

4. **Visualization Routes**:
   - Multiple visualization types
   - Base64 and raw image formats
   - Composite visualizations

5. **Talk Interface**:
   - WebSocket-based conversation handling
   - Session management
   - Cognitive module integration

6. **Production Ready**:
   - CORS configured
   - Health checks
   - Proper startup/shutdown handling
   - Type hints throughout

This implementation provides a complete backend for your DAWN consciousness engine with all the necessary endpoints and WebSocket support!