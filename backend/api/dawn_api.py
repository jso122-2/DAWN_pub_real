"""
DAWN Neural System - FastAPI Backend
Provides real-time neural metrics and WebSocket streaming for the desktop app
"""

import asyncio
import json
import logging
import math
import os
import random
import time
import sys
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime, timedelta
import traceback

# Add the root directory to sys.path
root_dir = str(Path(__file__).parent.parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

print("Python path:", sys.path)
print("Current directory:", Path.cwd())
print("Root directory:", root_dir)
print("Core directory exists:", (Path(root_dir) / "core").exists())
print("consciousness_core.py exists:", (Path(root_dir) / "core" / "consciousness_core.py").exists())

# Now import the modules
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Import DAWN components from core
from core.consciousness_tracer import ConsciousnessTracer
from core.pattern_detector import create_pattern_detector
from core.state_machine import create_state_machine
from core.fractal_emotions import create_fractal_emotions
from core.memory_manager import create_memory_manager
from core.mood_gradient import create_mood_gradient_plotter
from core.consciousness_core import ConsciousnessCore as CoreConsciousness
from core.spontaneity_new import SpontaneityModule
from core.event_bus import event_bus
from core.dawn_central import DAWNSuite
from core.unified_tick_engine import UnifiedTickEngine

# Import cognitive components
from cognitive.consciousness import ConsciousnessModule as CognitiveConsciousness
from cognitive.spontaneity import SpontaneityModule as CognitiveSpontaneity
from cognitive.conversation import ConversationModule
from cognitive.entropy_fluctuation import EntropyFluctuation
from cognitive.mood_urgency_probe import MoodUrgencyProbe
from cognitive.qualia_kernel import QualiaKernel

# Import API components
from backend.api.websocket_manager import WebSocketManager

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for more detailed logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="DAWN Neural System API",
    description="Real-time neural metrics and WebSocket streaming for DAWN",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://172.30.234.157:3000",  # Your IP address
        "http://127.0.0.1:3000",
        "*"  # Allow all origins in development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
consciousness = CoreConsciousness()
tick_engine = UnifiedTickEngine()
dawn_central = DAWNSuite()
websocket_manager = WebSocketManager(tick_engine=tick_engine, dawn_central=dawn_central)

@app.get("/health")
async def health_check():
    """Health check endpoint with service status"""
    try:
        return {
            "status": "healthy",
            "services": {
                "tick_engine": tick_engine is not None,
                "websocket": websocket_manager is not None,
                "consciousness": dawn_central is not None,
                "core": consciousness is not None
            },
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        logger.error(traceback.format_exc())
        # Return basic health even if services aren't ready
        return {
            "status": "starting",
            "error": str(e),
            "timestamp": time.time()
        }

@app.get("/metrics")
async def get_metrics():
    """Get current neural metrics"""
    return {
        "scup": 0.5,  # Placeholder - will be replaced with actual metrics
        "entropy": 0.5,
        "mood": "neutral"
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    client_id = None
    try:
        logger.info("New WebSocket connection attempt")
        logger.info(f"Client headers: {websocket.headers}")
        logger.info(f"Client query params: {websocket.query_params}")
        
        # Accept the connection
        await websocket.accept()
        logger.info("WebSocket connection accepted")
        
        # Register the client
        client_id = await websocket_manager.connect(websocket)
        logger.info(f"WebSocket client {client_id} connected")
        
        # Send initial state
        initial_state = {
            "type": "connection_established",
            "client_id": client_id,
            "timestamp": time.time()
        }
        await websocket.send_json(initial_state)
        logger.info(f"Sent initial state to client {client_id}")
        
        while True:
            try:
                # Wait for messages
                data = await websocket.receive_json()
                logger.debug(f"Received message from client {client_id}: {data}")
                
                # Process message
                response = await websocket_manager.handle_message(websocket, data)
                if response:
                    await websocket.send_json(response)
                    
            except WebSocketDisconnect:
                logger.info(f"WebSocket client {client_id} disconnected")
                break
            except Exception as e:
                logger.error(f"Error processing message from client {client_id}: {e}")
                logger.error(traceback.format_exc())
                try:
                    await websocket.send_json({
                        "type": "error",
                        "message": str(e)
                    })
                except:
                    pass
                
    except Exception as e:
        logger.error(f"Error in WebSocket endpoint: {e}")
        logger.error(traceback.format_exc())
    finally:
        if client_id:
            websocket_manager.disconnect(websocket)
            logger.info(f"Cleaned up connection for client {client_id}")

if __name__ == "__main__":
    # Create and set the event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Start the broadcast loop
    broadcast_task = loop.create_task(websocket_manager.broadcast_loop())
    
    try:
        # Run the server
        config = uvicorn.Config(
            app,
            host="0.0.0.0",
            port=8000,  # Backend runs on port 8000
            loop=loop,
            log_level="debug"  # Set to debug for more detailed logs
        )
        server = uvicorn.Server(config)
        loop.run_until_complete(server.serve())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        # Clean up
        broadcast_task.cancel()
        try:
            loop.run_until_complete(broadcast_task)
        except asyncio.CancelledError:
            pass
        loop.close() 