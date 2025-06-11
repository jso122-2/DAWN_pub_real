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
from typing import Dict, Any, List
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Pydantic models for API
class MetricsResponse(BaseModel):
    scup: float
    entropy: float
    heat: float
    mood: str
    timestamp: float
    tick_count: int

class SubsystemInfo(BaseModel):
    id: str
    name: str
    status: str
    state: Dict[str, Any]

class SubsystemCreate(BaseModel):
    name: str
    config: Dict[str, Any] = {}

class AlertThreshold(BaseModel):
    metric: str
    threshold: float
    direction: str = "above"

class DAWNSystem:
    def __init__(self):
        self.is_booted = True
        self.running = False
        self.start_time = time.time()
        
        # Current metrics for API (with dynamic updates)
        self.current_metrics = {
            "scup": 0.5,
            "entropy": 0.5,
            "heat": 0.3,
            "mood": "initializing",
            "timestamp": time.time(),
            "tick_count": 0
        }
        
        # Alert thresholds
        self.alert_thresholds = {}
        
        # Mock subsystems for demo
        self.subsystems = {
            "pulse": {"status": "active", "state": {"pulse_rate": 1.2, "amplitude": 0.8}},
            "schema": {"status": "active", "state": {"coherence": 0.7, "drift": 0.1}},
            "thermal": {"status": "active", "state": {"temperature": 298.5, "cooling": True}},
            "entropy": {"status": "active", "state": {"entropy_rate": 0.03, "stable": True}},
            "alignment": {"status": "active", "state": {"alignment": 0.85, "drift": 0.02}},
            "bloom": {"status": "active", "state": {"bloom_intensity": 0.9, "phase": "expansion"}}
        }
        
        logger.info("DAWN System initialized")

    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current system metrics with realistic simulation"""
        # Simulate realistic DAWN metrics with some variation
        current_time = time.time()
        runtime = current_time - self.start_time
        time_factor = runtime / 10  # Slow oscillation
        
        # Generate realistic SCUP (Subsystem Cognitive Unity Potential: 0.3 to 0.9)
        scup_base = 0.6 + 0.2 * math.sin(time_factor)
        scup_noise = random.uniform(-0.05, 0.05)
        scup = max(0.3, min(0.9, scup_base + scup_noise))
        
        # Generate entropy (0.2 to 0.8, inversely related to SCUP)
        entropy_base = 0.5 - 0.2 * math.sin(time_factor)
        entropy_noise = random.uniform(-0.03, 0.03)
        entropy = max(0.2, min(0.8, entropy_base + entropy_noise))
        
        # Generate heat (0.1 to 0.7)
        heat_base = 0.3 + 0.2 * math.cos(time_factor * 1.3)
        heat_noise = random.uniform(-0.02, 0.02)
        heat = max(0.1, min(0.7, heat_base + heat_noise))
        
        # Dynamic mood based on metrics
        if scup > 0.7:
            mood = random.choice(["focused", "analytical", "optimized", "confident"])
        elif scup > 0.5:
            mood = random.choice(["reflective", "processing", "balanced", "stable"])
        else:
            mood = random.choice(["uncertain", "searching", "adaptive", "recalibrating"])
        
        # Update metrics
        self.current_metrics.update({
            "scup": round(scup, 3),
            "entropy": round(entropy, 3),
            "heat": round(heat, 3),
            "mood": mood,
            "tick_count": self.current_metrics["tick_count"] + 1,
            "timestamp": current_time
        })
        
        return self.current_metrics.copy()

    def get_subsystems(self) -> List[Dict[str, Any]]:
        """Get all registered subsystems"""
        subsystems = []
        for name, info in self.subsystems.items():
            # Add some dynamic state updates
            if name == "pulse":
                info["state"]["pulse_rate"] = 1.0 + 0.4 * math.sin(time.time() / 5)
            elif name == "thermal":
                info["state"]["temperature"] = 298.0 + 2.0 * math.sin(time.time() / 8)
            
            subsystems.append({
                "id": name,
                "name": name,
                "status": info["status"],
                "state": info["state"]
            })
        return subsystems

    async def run(self):
        """Main system loop"""
        self.running = True
        logger.info("DAWN system running in simulation mode")
        
        while self.running:
            try:
                # Update metrics periodically
                self.get_current_metrics()
                await asyncio.sleep(0.5)  # Update every 500ms
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(1)

    def stop(self):
        """Stop the system"""
        self.running = False
        logger.info("DAWN system stopped")

# Global DAWN system instance
dawn_system = DAWNSystem()

class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast_metrics(self, metrics: dict):
        """Broadcast metrics to all connected clients"""
        if not self.active_connections:
            return
            
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(metrics)
            except Exception as e:
                logger.error(f"Error sending to WebSocket: {e}")
                disconnected.append(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection)

# WebSocket connection manager
manager = ConnectionManager()

async def broadcast_metrics_periodically():
    """Periodically broadcast metrics to WebSocket clients"""
    while True:
        try:
            if dawn_system and manager.active_connections:
                metrics = dawn_system.get_current_metrics()
                await manager.broadcast_metrics(metrics)
            await asyncio.sleep(0.5)  # Send updates every 500ms
        except Exception as e:
            logger.error(f"Error broadcasting metrics: {e}")
            await asyncio.sleep(1)

# Initialize FastAPI app
app = FastAPI(
    title="DAWN Neural Monitor API",
    description="Real-time neural system monitoring API for DAWN desktop application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5175", "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoints

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "booted": dawn_system.is_booted,
        "running": dawn_system.running,
        "timestamp": time.time(),
        "uptime": time.time() - dawn_system.start_time
    }

@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get current system metrics"""
    metrics = dawn_system.get_current_metrics()
    return MetricsResponse(**metrics)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time metrics streaming"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle client messages
            data = await websocket.receive_text()
            logger.debug(f"Received WebSocket message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

@app.get("/subsystems", response_model=List[SubsystemInfo])
async def get_subsystems():
    """Get all registered subsystems"""
    subsystems = dawn_system.get_subsystems()
    return [SubsystemInfo(**sub) for sub in subsystems]

@app.get("/subsystems/{subsystem_id}")
async def get_subsystem(subsystem_id: str):
    """Get specific subsystem details"""
    subsystems = dawn_system.get_subsystems()
    for sub in subsystems:
        if sub["id"] == subsystem_id:
            return SubsystemInfo(**sub)
    
    raise HTTPException(status_code=404, detail="Subsystem not found")

@app.post("/subsystems/add")
async def add_subsystem(subsystem: SubsystemCreate):
    """Add a new subsystem (placeholder for future implementation)"""
    raise HTTPException(status_code=501, detail="Dynamic subsystem addition not implemented yet")

@app.delete("/subsystems/{subsystem_id}")
async def remove_subsystem(subsystem_id: str):
    """Remove a subsystem (placeholder for future implementation)"""
    raise HTTPException(status_code=501, detail="Dynamic subsystem removal not implemented yet")

@app.post("/alerts/threshold")
async def set_alert_threshold(threshold: AlertThreshold):
    """Set alert threshold for a metric"""
    dawn_system.alert_thresholds[threshold.metric] = {
        "threshold": threshold.threshold,
        "direction": threshold.direction
    }
    
    return {"message": f"Alert threshold set for {threshold.metric}"}

@app.get("/alerts/threshold")
async def get_alert_thresholds():
    """Get all alert thresholds"""
    return dawn_system.alert_thresholds

@app.on_event("startup")
async def startup_event():
    """Start background tasks on startup"""
    logger.info("Starting DAWN Neural Monitor API Server")
    
    # Start DAWN system in background
    asyncio.create_task(dawn_system.run())
    
    # Start metrics broadcast task
    asyncio.create_task(broadcast_metrics_periodically())

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down DAWN system")
    dawn_system.stop()

if __name__ == "__main__":
    print("🌟 Starting DAWN Neural Monitor API Server")
    print("🔗 WebSocket endpoint: ws://localhost:8000/ws")
    print("📊 Metrics endpoint: http://localhost:8000/metrics")
    print("🏥 Health check: http://localhost:8000/health")
    
    uvicorn.run(
        "dawn_api:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    ) 