from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cors import CORS
from contextlib import asynccontextmanager
import asyncio
import uvicorn
from typing import Dict, Any, List
from datetime import datetime
import signal
import sys
import os
from pydantic import BaseModel

# Add the root directory to Python path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

# Import routers
from backend.api.routes import consciousness_router, visualization_router, talk_router

# Import managers
from backend.api.websocket_manager import WebSocketManager
from core.unified_tick_engine import UnifiedTickEngine
from core.dawn_central import DAWNCentral

# Global instances
tick_engine = None
dawn_central = None
ws_manager = None
shutdown_event = asyncio.Event()

# Add new models for process management
class ProcessStatus(BaseModel):
    name: str
    is_running: bool
    start_time: str | None
    last_tick: int | None
    error: str | None

class ProcessResponse(BaseModel):
    success: bool
    message: str
    process_name: str
    status: ProcessStatus | None = None

# Add tick data broadcasting
async def broadcast_tick_data():
    tick = 0
    while not shutdown_event.is_set():
        tick += 1
        tick_data = {
            "type": "tick",
            "tick_number": tick,
            "scup": 75 + (tick % 25),  # Oscillating SCUP
            "entropy": 0.3 + (0.2 * (tick % 10) / 10),
            "mood": ["calm", "focused", "energetic", "chaotic"][tick % 4]
        }
        
        # Broadcast to all connected clients
        for connection in ws_manager.active_connections:
            await ws_manager.send_personal_message(tick_data, connection)
        
        await asyncio.sleep(1)  # Send tick every second

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    print("\n[DAWN] Received shutdown signal. Initiating graceful shutdown...")
    shutdown_event.set()

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

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
    
    # Start WebSocket broadcast loops
    broadcast_task = asyncio.create_task(ws_manager.broadcast_loop())
    tick_broadcast_task = asyncio.create_task(broadcast_tick_data())
    
    print("[DAWN] Consciousness engine online")
    
    yield
    
    # Shutdown
    print("[DAWN] Shutting down consciousness engine...")
    tick_task.cancel()
    broadcast_task.cancel()
    tick_broadcast_task.cancel()
    await tick_engine.shutdown()
    await ws_manager.disconnect_all()
    print("[DAWN] Shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="DAWN Consciousness Engine API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
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
        # Get client ID
        client_id = None
        for cid, conn_info in ws_manager.connections.items():
            if conn_info.websocket == websocket:
                client_id = cid
                break
        
        if client_id:
            # Subscribe to all updates by default
            await ws_manager.subscribe_client(client_id, ["tick_update", "talk", "consciousness"])
        
        while not shutdown_event.is_set():
            # Receive and process messages
            try:
                data = await websocket.receive_json()
                
                # Handle ping/pong
                if data.get("type") == "ping":
                    await websocket.send_json({"type": "pong", "timestamp": datetime.now().isoformat()})
                    continue
                
                # Process other messages
                response = await ws_manager.handle_message(websocket, data)
                if response:
                    await websocket.send_json(response)
                    
            except WebSocketDisconnect:
                break
            except Exception as e:
                print(f"WebSocket error: {e}")
                break
                
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket)

# Talk WebSocket endpoint
@app.websocket("/ws/talk")
async def talk_websocket_endpoint(websocket: WebSocket):
    """Dedicated WebSocket for talk interface"""
    from backend.api.routes.talk import TalkHandler
    
    handler = TalkHandler(tick_engine, dawn_central, ws_manager)
    await handler.handle_connection(websocket)

# Process management endpoints
@app.get("/processes/status")
async def get_processes_status():
    return {
        "processes": [
            {"name": "activation_histogram", "status": "available", "description": "Neural activation patterns"},
            {"name": "memory_stream", "status": "available", "description": "Memory formation visualizer"},
            {"name": "entropy_cascade", "status": "available", "description": "Chaos dynamics monitor"},
            {"name": "consciousness_map", "status": "available", "description": "Consciousness state mapper"},
            {"name": "quantum_flux", "status": "available", "description": "Quantum coherence analyzer"}
        ]
    }

@app.post("/processes/{process_name}/start")
async def start_process(process_name: str):
    # TODO: Actually start the Python process
    return {"status": "started", "process": process_name}

@app.post("/processes/{process_name}/stop")
async def stop_process(process_name: str):
    # TODO: Actually stop the Python process
    return {"status": "stopped", "process": process_name}

@app.get("/tick-snapshot/{process_name}")
async def get_tick_snapshot(process_name: str):
    # TODO: Get actual data from the process
    return {
        "process": process_name,
        "tick": 42,
        "data": {"value": 0.75, "timestamp": "2024-01-01T00:00:00Z"}
    }

if __name__ == "__main__":
    try:
        uvicorn.run(
            "start_api_fixed:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n[DAWN] Received keyboard interrupt. Shutting down...")
        sys.exit(0) 