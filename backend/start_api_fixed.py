from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import uvicorn
from typing import Dict, Any
from datetime import datetime
import signal
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import routers
from backend.api.routes import consciousness_router, visualization_router, talk_router

# Import managers
from backend.api.websocket_manager import WebSocketManager
from backend.core.unified_tick_engine import UnifiedTickEngine
from backend.core.dawn_central import DAWNCentral

# Global instances
tick_engine = None
dawn_central = None
ws_manager = None
shutdown_event = asyncio.Event()

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
        while not shutdown_event.is_set():
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
        
        while not shutdown_event.is_set():
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
    from backend.api.routes.talk import TalkHandler
    
    handler = TalkHandler(tick_engine, dawn_central, ws_manager)
    await handler.handle_connection(websocket)

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