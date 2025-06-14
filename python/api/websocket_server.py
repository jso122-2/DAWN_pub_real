from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import json
from typing import List, Dict, Any, Optional
import logging

# Import the tick engine
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from core.tick_engine import tick_engine, TickData

logger = logging.getLogger(__name__)


# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.owl_connections: List[WebSocket] = []  # Dedicated Owl connections

    async def connect(self, websocket: WebSocket, connection_type: str = "main"):
        await websocket.accept()
        
        if connection_type == "main":
            self.active_connections.append(websocket)
            logger.info(f"Main WebSocket connected. Total: {len(self.active_connections)}")
        elif connection_type == "owl":
            self.owl_connections.append(websocket)
            logger.info(f"Owl WebSocket connected. Total: {len(self.owl_connections)}")

    def disconnect(self, websocket: WebSocket, connection_type: str = "main"):
        try:
            if connection_type == "main":
                self.active_connections.remove(websocket)
            elif connection_type == "owl":
                self.owl_connections.remove(websocket)
            logger.info(f"{connection_type} WebSocket disconnected")
        except ValueError:
            pass

    async def broadcast_tick(self, data: dict):
        """Broadcast tick data to all main connections"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json({
                    "type": "tick",
                    "data": data
                })
            except:
                disconnected.append(connection)
        
        # Clean up disconnected
        for conn in disconnected:
            self.disconnect(conn, "main")

    async def broadcast_owl(self, data: dict):
        """Broadcast Owl observations to Owl connections"""
        disconnected = []
        for connection in self.owl_connections:
            try:
                await connection.send_json({
                    "type": "owl_observation",
                    "data": data
                })
            except:
                disconnected.append(connection)
        
        # Clean up disconnected
        for conn in disconnected:
            self.disconnect(conn, "owl")


# Global connection manager
manager = ConnectionManager()


# Register tick callback for broadcasting
async def broadcast_tick_callback(tick_data: TickData):
    """Callback to broadcast tick data"""
    await manager.broadcast_tick(tick_data.to_dict())
    
    # If Owl observations exist, broadcast them too
    if 'owl' in tick_engine.modules:
        # This would be set by the owl module during processing
        if hasattr(tick_data, 'owl_data'):
            await manager.broadcast_owl(tick_data.owl_data)


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting DAWN Tick Engine...")
    
    # Register broadcast callback
    tick_engine.register_callback(broadcast_tick_callback)
    
    # Start tick engine
    await tick_engine.start()
    
    yield
    
    # Shutdown
    logger.info("Shutting down DAWN Tick Engine...")
    await tick_engine.stop()


# Create FastAPI app
app = FastAPI(
    title="DAWN Tick Engine API",
    description="WebSocket API for DAWN consciousness tick engine with Owl integration",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# WebSocket endpoints
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Main tick data WebSocket"""
    await manager.connect(websocket, "main")
    try:
        # Send initial state
        await websocket.send_json({
            "type": "connection",
            "data": {
                "status": "connected",
                "engine_state": tick_engine.get_current_state()
            }
        })
        
        while True:
            # Handle incoming messages
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                if message.get("type") == "heartbeat":
                    await websocket.send_json({
                        "type": "heartbeat_response",
                        "timestamp": message.get("timestamp")
                    })
                elif message.get("type") == "get_history":
                    count = message.get("count", 100)
                    history = tick_engine.get_tick_history(count)
                    await websocket.send_json({
                        "type": "history",
                        "data": [tick.to_dict() for tick in history]
                    })
                    
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON"
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, "main")


@app.websocket("/owl")
async def owl_websocket_endpoint(websocket: WebSocket):
    """Dedicated Owl observations WebSocket"""
    await manager.connect(websocket, "owl")
    try:
        # Send initial Owl state if available
        if 'owl' in tick_engine.modules:
            owl_module = tick_engine.modules['owl']
            await websocket.send_json({
                "type": "owl_state",
                "data": {
                    "observation_count": len(owl_module.observations),
                    "active_plans": list(owl_module.active_plans.keys()),
                    "planning_horizons": owl_module.planning_horizons
                }
            })
        
        while True:
            # Handle incoming Owl-specific messages
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                if message.get("type") == "get_observations":
                    count = message.get("count", 50)
                    if 'owl' in tick_engine.modules:
                        owl_module = tick_engine.modules['owl']
                        observations = list(owl_module.observations)[-count:]
                        await websocket.send_json({
                            "type": "observations",
                            "data": [obs.__dict__ for obs in observations]
                        })
                
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON"
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, "owl")


# REST endpoints
@app.get("/api/engine/status")
async def get_engine_status():
    """Get current engine status"""
    return tick_engine.get_current_state()


@app.get("/api/engine/history")
async def get_tick_history(count: int = 100):
    """Get recent tick history"""
    history = tick_engine.get_tick_history(count)
    return {
        "count": len(history),
        "ticks": [tick.to_dict() for tick in history]
    }


@app.post("/api/engine/config")
async def update_engine_config(config: Dict[str, Any]):
    """Update engine configuration"""
    # TODO: Implement configuration updates
    return {"status": "configuration_update_not_implemented"}


@app.get("/api/owl/observations")
async def get_owl_observations(count: int = 50):
    """Get recent Owl observations"""
    if 'owl' not in tick_engine.modules:
        return {"error": "Owl module not enabled"}
    
    owl_module = tick_engine.modules['owl']
    observations = list(owl_module.observations)[-count:]
    
    return {
        "count": len(observations),
        "observations": [obs.__dict__ for obs in observations]
    }


@app.get("/api/owl/plans")
async def get_owl_plans():
    """Get active Owl strategic plans"""
    if 'owl' not in tick_engine.modules:
        return {"error": "Owl module not enabled"}
    
    owl_module = tick_engine.modules['owl']
    plans = [plan.__dict__ for plan in owl_module.active_plans.values()]
    
    return {
        "count": len(plans),
        "plans": plans
    }


@app.get("/api/owl/schemas")
async def get_owl_schema_alignments():
    """Get current schema alignments"""
    if 'owl' not in tick_engine.modules:
        return {"error": "Owl module not enabled"}
    
    owl_module = tick_engine.modules['owl']
    
    return {
        "alignments": owl_module.schema_alignments,
        "trajectory": owl_module.semantic_trajectory[-10:] if len(owl_module.semantic_trajectory) > 10 else owl_module.semantic_trajectory
    }


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "engine_running": tick_engine.is_running,
        "tick_count": tick_engine.tick_count,
        "uptime": tick_engine.get_current_state().get('uptime', 0),
        "modules": list(tick_engine.modules.keys())
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "DAWN Tick Engine API with Owl Integration",
        "version": "1.0.0",
        "endpoints": {
            "websocket_main": "/ws",
            "websocket_owl": "/owl", 
            "health": "/health",
            "engine_status": "/api/engine/status",
            "tick_history": "/api/engine/history",
            "owl_observations": "/api/owl/observations",
            "owl_plans": "/api/owl/plans",
            "owl_schemas": "/api/owl/schemas"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    ) 