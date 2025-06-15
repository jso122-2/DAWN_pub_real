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
from typing import Dict, Optional, Any
from datetime import datetime

# Ensure project root is in sys.path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Add backend directory to sys.path
backend_dir = str(Path(__file__).parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Third-party imports
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np

# Local application imports
from semantic.semantic_field import RhizomicSemanticField, NodeCharge
from backend.core.unified_tick_engine import UnifiedTickEngine
from core.consciousness_core import DAWNConsciousness
from core.event_bus import EventBus
from core.thermal_visualizer import ThermalVisualizer
from core.entropy_visualizer import EntropyVisualizer
from core.alignment_visualizer import AlignmentVisualizer
from core.bloom_visualizer import BloomVisualizer
from core.dawn_visualizer import DAWNVisualizer
from backend.talk_to_handler import TalkToHandler
from backend.visual.base_visualizer import BaseVisualizer
from backend.visual.psl_integration import PSLVisualizer
from visual.consciousness_wave import ConsciousnessWaveVisualizer
from backend.visual_stream_handler import VisualStreamHandler
from schema.schema_evolution_engine import SchemaEvolutionEngine
from cognitive.qualia_kernel import QualiaKernel
from cognitive.mood_urgency_probe import MoodUrgencyProbe
from pulse.pulse_layer import PulseLayer
from pulse.scup_tracker import SCUPTracker
from pulse.pulse_heat import add_heat

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

def initialize_semantic_field() -> None:
    """Initialize the semantic field with foundational consciousness concepts."""
    logger.info("Initializing semantic field with consciousness concepts...")
    
    # Get the singleton instance
    semantic_field = RhizomicSemanticField.get_current_field()
    
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
            semantic_field.add_semantic_node(concept["content"], embedding, concept["charge"])
            logger.info(f"Added concept '{concept['content']}' [{concept['charge'].value}]")
        except Exception as e:
            logger.error(f"Failed to add concept '{concept['content']}': {e}")
            raise

class DAWNCentral:
    def __init__(self):
        self.tick_engine = UnifiedTickEngine()
        self.consciousness = DAWNConsciousness()
        self.event_bus = EventBus()
        self.visualizers = {
            'thermal': ThermalVisualizer(),
            'entropy': EntropyVisualizer(),
            'alignment': AlignmentVisualizer(),
            'bloom': BloomVisualizer(),
            'dawn': DAWNVisualizer()
        }
        self.talk_handler = TalkToHandler()
        self.visual_handler = VisualStreamHandler()
        self.schema_engine = SchemaEvolutionEngine()
        self.qualia_kernel = QualiaKernel()
        self.mood_probe = MoodUrgencyProbe()
        self.pulse_layer = PulseLayer()
        self.scup_tracker = SCUPTracker()
        
        # Initialize subsystems
        self._initialize_subsystems()
        
    def _initialize_subsystems(self):
        """Initialize and register all subsystems"""
        # Register with tick engine
        self.tick_engine.register_subsystem('pulse', self.pulse_layer, priority=1)
        self.tick_engine.register_subsystem('schema', self.schema_engine, priority=2)
        self.tick_engine.register_subsystem('visualizer', self.visualizers['dawn'], priority=3)
        self.tick_engine.register_subsystem('thermal', self.visualizers['thermal'], priority=4)
        self.tick_engine.register_subsystem('entropy', self.visualizers['entropy'], priority=5)
        self.tick_engine.register_subsystem('alignment', self.visualizers['alignment'], priority=6)
        self.tick_engine.register_subsystem('bloom', self.visualizers['bloom'], priority=7)
        
        # Initialize consciousness
        self.consciousness.update_subsystem('schema', self.schema_engine)
        self.consciousness.update_subsystem('event_bus', self.event_bus)
        self.consciousness.update_subsystem('visualizer', self.visualizers['dawn'])
        
    def get_state(self) -> Dict[str, Any]:
        """Get current engine state"""
        return {
            'tick': self.tick_engine.current_tick,
            'scup': self.scup_tracker.get_scup(),
            'entropy': self.visualizers['entropy'].get_entropy(),
            'mood': self.mood_probe.get_mood(),
            'consciousness_state': self.consciousness.get_state(),
            'active_processes': self.tick_engine.get_active_processes(),
            'timestamp': datetime.now().isoformat()
        }
    
    def is_active(self) -> bool:
        """Check if the engine is active"""
        return self.tick_engine.is_running and self.consciousness.is_active

# Create FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DAWN central system
dawn_central = DAWNCentral()
tick_engine = dawn_central.tick_engine
ws_manager = dawn_central.visual_handler

# Initialize visualizers
logger.info("Initializing visualizers...")
consciousness_wave = ConsciousnessWaveVisualizer(
    frequency=1.0,
    amplitude=0.8,
    wave_type='composite'
)

# Initialize handlers
logger.info("Initializing handlers...")
talk_handler = dawn_central.talk_handler
visual_handler = dawn_central.visual_handler

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
                state = dawn_central.get_state()
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
    """Initialize the server on startup"""
    logger.info("Starting up server...")
    try:
        # Initialize semantic field first
        logger.info("Initializing semantic field...")
        initialize_semantic_field()
        
        # Start the tick engine
        logger.info("Starting tick engine...")
        await tick_engine.start()
        
        # Start consciousness wave visualization
        logger.info("Starting consciousness wave visualization...")
        await consciousness_wave.start()
        
        logger.info("Server startup complete")
    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)
        # Ensure clean shutdown
        try:
            await tick_engine.stop()
        except Exception as stop_error:
            logger.error(f"Error during emergency shutdown: {stop_error}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on server shutdown"""
    logger.info("Shutting down server...")
    try:
        # Stop the tick engine
        await tick_engine.stop()
        
        # Stop consciousness wave visualization
        await consciousness_wave.stop()
        
        logger.info("Server shutdown complete")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}", exc_info=True)
        raise

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if dawn_central.is_active() else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "tick": tick_engine.current_tick if tick_engine else None,
        "scup": dawn_central.scup_tracker.get_scup() if dawn_central.scup_tracker else None,
        "entropy": dawn_central.visualizers['entropy'].get_entropy() if 'entropy' in dawn_central.visualizers else None,
        "mood": dawn_central.mood_probe.get_mood() if dawn_central.mood_probe else None,
        "consciousness_state": dawn_central.consciousness.get_state() if dawn_central.consciousness else None
    }

@app.get("/tick-snapshot/{process_id}")
async def get_tick_snapshot(process_id: str):
    """Get a snapshot of the tick engine state for a specific process"""
    try:
        state = dawn_central.get_state()
        return {
            "process_id": process_id,
            "state": state,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting tick snapshot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 