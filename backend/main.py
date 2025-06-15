"""
DAWN Tick Engine - Main server entry point
"""

# Standard library imports
import asyncio
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

# Third-party imports
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from semantic.semantic_field import SemanticField, NodeCharge

# Ensure project root is in sys.path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Add backend directory to sys.path
backend_dir = str(Path(__file__).parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Local application imports
from backend.core.unified_tick_engine import tick_engine
from backend.core.conversation_enhanced import EnhancedConversation
from backend.visual.consciousness_wave import ConsciousnessWaveVisualizer
from backend.visual.base_visualizer import BaseVisualizer
from backend.visual.visual_manager import VisualManager
from backend.visual_stream_handler import VisualStreamHandler
from backend.talk_to_handler import TalkToHandler
from backend.websocket_manager import manager as ws_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('backend.log')
    ]
)
logger = logging.getLogger(__name__)

logger.info("Starting DAWN Tick Engine server...")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize visualizers
logger.info("Initializing visualizers...")
consciousness_wave = ConsciousnessWaveVisualizer(
    frequency=1.0,
    amplitude=0.8,
    wave_type='composite'
)

# Initialize handlers
logger.info("Initializing handlers...")
talk_handler = TalkToHandler()
visual_handler = VisualStreamHandler()

# Global set to track connected WebSocket clients for tick streaming
active_tick_clients = set()

# Base WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Base WebSocket endpoint for general communication"""
    logger.info("New WebSocket connection request")
    try:
        await ws_manager.connect(websocket)
        logger.info(f"WebSocket connected: {websocket.client}")
        
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                logger.debug(f"Received message: {message}")
                await ws_manager.handle_message(message, websocket)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse message: {data}")
                await ws_manager.send_personal_message({
                    "type": "error",
                    "data": {"message": "Invalid JSON format"}
                }, websocket)
            except WebSocketDisconnect:
                logger.info("WebSocket disconnected")
                ws_manager.disconnect(websocket)
                break
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                await ws_manager.send_personal_message({
                    "type": "error",
                    "data": {"message": f"Processing error: {str(e)}"}
                }, websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket)

# Talk endpoint
@app.websocket("/ws/talk")
async def websocket_talk_endpoint(websocket: WebSocket):
    """WebSocket endpoint for DAWN communication"""
    logger.info("New talk WebSocket connection request")
    try:
        await ws_manager.connect(websocket)
        logger.info(f"Talk WebSocket connected: {websocket.client}")
        
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                logger.debug(f"Received talk message: {message}")
                
                if message.get('type') == 'talk':
                    await talk_handler.handle_message(message.get('data', {}), websocket)
                else:
                    await ws_manager.handle_message(message, websocket)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse talk message: {data}")
                await ws_manager.send_personal_message({
                    "type": "error",
                    "data": {"message": "Invalid JSON format"}
                }, websocket)
            except WebSocketDisconnect:
                logger.info("Talk WebSocket disconnected")
                ws_manager.disconnect(websocket)
                break
            except Exception as e:
                logger.error(f"Error processing talk message: {e}")
                await ws_manager.send_personal_message({
                    "type": "error",
                    "data": {"message": f"Processing error: {str(e)}"}
                }, websocket)
    except Exception as e:
        logger.error(f"Talk WebSocket error: {e}")
        ws_manager.disconnect(websocket)

# Tick engine state streaming endpoint
@app.websocket("/ws/tick")
async def websocket_tick_endpoint(websocket: WebSocket):
    """WebSocket endpoint for tick engine state streaming"""
    logger.info("New tick WebSocket connection request")
    try:
        await ws_manager.connect(websocket)
        logger.info(f"Tick WebSocket connected: {websocket.client}")
        
        while True:
            try:
                state = tick_engine.get_state()
                await ws_manager.send_personal_message({
                    "type": "tick",
                    "data": state,
                    "timestamp": time.time()
                }, websocket)
                await asyncio.sleep(1)
            except WebSocketDisconnect:
                logger.info("Tick WebSocket disconnected")
                ws_manager.disconnect(websocket)
                break
            except Exception as e:
                logger.error(f"Error sending tick state: {e}")
                await ws_manager.send_personal_message({
                    "type": "error",
                    "data": {"message": f"Error sending tick state: {str(e)}"}
                }, websocket)
                break
    except Exception as e:
        logger.error(f"Tick WebSocket error: {e}")
        ws_manager.disconnect(websocket)

@app.websocket("/ws/visualization")
async def websocket_visualization_endpoint(websocket: WebSocket):
    """WebSocket endpoint for streaming visualizations to the frontend"""
    logger.info("New visualization WebSocket connection request")
    try:
        await visual_handler.stream_visualizations(websocket)
    except WebSocketDisconnect:
        logger.info("Visualization WebSocket disconnected")
    except Exception as e:
        logger.error(f"Error in visualization WebSocket: {e}")

@app.websocket("/ws/tick-stream")
async def tick_stream(websocket: WebSocket):
    await websocket.accept()
    active_tick_clients.add(websocket)
    try:
        while True:
            await asyncio.sleep(60)  # Keep connection alive, actual sending is done elsewhere
    except WebSocketDisconnect:
        active_tick_clients.remove(websocket)

async def broadcast_tick_state(state: dict):
    data = json.dumps(state, default=str)
    for ws in list(active_tick_clients):
        try:
            await ws.send_text(data)
        except Exception:
            active_tick_clients.remove(ws)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up server...")
    # Start tick engine
    asyncio.create_task(tick_engine.start())
    
    # Start the consciousness wave visualization
    def get_consciousness_state():
        state = tick_engine.get_state()
        return {
            'frequency': state.get('neural_frequency', 1.0),
            'amplitude': state.get('scup', 0.8),
            'phase': state.get('phase_coherence', 0.0)
        }
    
    logger.info("Starting consciousness wave visualization...")
    consciousness_wave.start_live_stream(data_source=get_consciousness_state)
    
    # --- Semantic Field Initialization (after visualizers/handlers, before server start) ---
    def initialize_semantic_field(semantic_field):
        """
        Initialize the semantic field with foundational consciousness concepts.
        Each node represents a key aspect of the DAWN consciousness system.
        """
        import logging
        logging.info("Initializing semantic field with consciousness concepts...")
        
        consciousness_concepts = [
            {"content": "consciousness", "charge": NodeCharge.ACTIVE_POSITIVE},
            {"content": "awareness", "charge": NodeCharge.ACTIVE_POSITIVE},
            {"content": "unconscious", "charge": NodeCharge.LATENT_NEGATIVE},
            {"content": "perception", "charge": NodeCharge.ACTIVE_POSITIVE},
            {"content": "memory", "charge": NodeCharge.STATIC_NEUTRAL},
            {"content": "learning", "charge": NodeCharge.ACTIVE_POSITIVE},
            {"content": "emotion", "charge": NodeCharge.ACTIVE_POSITIVE},
            {"content": "contemplative", "charge": NodeCharge.LATENT_POSITIVE},
            {"content": "chaotic", "charge": NodeCharge.ACTIVE_NEGATIVE},
            {"content": "harmonious", "charge": NodeCharge.LATENT_POSITIVE},
            {"content": "entropy", "charge": NodeCharge.STATIC_NEUTRAL},
            {"content": "coherence", "charge": NodeCharge.ACTIVE_POSITIVE},
            {"content": "emergence", "charge": NodeCharge.ACTIVE_POSITIVE},
            {"content": "pattern", "charge": NodeCharge.STATIC_NEUTRAL},
            {"content": "symbol", "charge": NodeCharge.LATENT_POSITIVE},
            {"content": "meaning", "charge": NodeCharge.ACTIVE_POSITIVE},
            {"content": "superposition", "charge": NodeCharge.ACTIVE_POSITIVE},
            {"content": "entanglement", "charge": NodeCharge.ACTIVE_POSITIVE},
            {"content": "observation", "charge": NodeCharge.ACTIVE_NEGATIVE},
            {"content": "self", "charge": NodeCharge.ACTIVE_POSITIVE},
            {"content": "other", "charge": NodeCharge.LATENT_NEGATIVE},
            {"content": "reflection", "charge": NodeCharge.LATENT_POSITIVE},
        ]
        
        for concept in consciousness_concepts:
            try:
                embedding = np.random.randn(384)
                embedding = embedding / np.linalg.norm(embedding)
                SemanticField.add_semantic_node(concept["content"], embedding, concept["charge"])
                print(f"[INIT] Added concept '{concept['content']}' [{concept['charge'].value}]")
            except Exception as e:
                print(f"[INIT] Failed to add concept '{concept['content']}': {e}")

    # Only initialize if the field is empty
    if hasattr(SemanticField, 'nodes') and len(SemanticField.nodes) == 0:
        initialize_semantic_field(SemanticField)
    
    logger.info("Server startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down server...")
    # Stop tick engine
    await tick_engine.stop()
    logger.info("Server shutdown complete")

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring server and WebSocket status"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "websocket": {
            "connections": ws_manager.get_connection_stats(),
            "endpoints": [
                "/ws",
                "/ws/talk",
                "/ws/tick"
            ]
        },
        "tick_engine": {
            "running": tick_engine.is_running(),
            "tick_count": tick_engine.get_tick_count(),
            "last_tick": tick_engine.get_last_tick_time()
        }
    }

@app.get("/tick-snapshot/{process_id}")
async def get_tick_snapshot(process_id: str):
    """Get a snapshot of tick data for a specific visualization process"""
    try:
        # Get current tick state
        state = tick_engine.get_state()
        print(f"[DEBUG] /tick-snapshot/{process_id} called. Tick state: {state}")
        
        # Get drift vector field data if requested
        if process_id == "drift_vector_field":
            from semantic.semantic_field import get_current_field
            field = get_current_field()
            print(f"[DEBUG] get_current_field() returned: {field}")
            drift_vectors = field.get_drift_vectors() if field else {}
            print(f"[DEBUG] drift_vectors: {drift_vectors}")
            
            return {
                "tick_number": state["tick_count"],
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "drift_vectors": drift_vectors,
                    "tick_state": state
                }
            }
        
        # Default response for other processes
        return {
            "tick_number": state["tick_count"],
            "timestamp": datetime.now().isoformat(),
            "data": state
        }
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())  # This will print the full error to your backend log
        logger.error(f"Error getting tick snapshot for {process_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("Starting server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    ) 