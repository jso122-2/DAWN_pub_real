#!/usr/bin/env python3
"""
DAWN Integrated API
Main backend for DAWN consciousness engine with subprocess management
"""

import asyncio
import json
import time
import math
import random
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from subprocess_manager import SubprocessManager, ProcessStatus
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DAWNWebSocketManager:
    def __init__(self):
        self.connections: List[WebSocket] = []
    
    async def add_connection(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.connections)}")
    
    def remove_connection(self, websocket: WebSocket):
        if websocket in self.connections:
            self.connections.remove(websocket)
            logger.info(f"Client disconnected. Total connections: {len(self.connections)}")
    
    async def broadcast(self, message: Dict[str, Any]):
        if not self.connections:
            return
        
        message_json = json.dumps(message)
        disconnected = []
        
        for connection in self.connections:
            try:
                await connection.send_text(message_json)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            self.remove_connection(conn)

class DAWNConsciousnessEngine:
    def __init__(self, websocket_manager: DAWNWebSocketManager):
        self.websocket_manager = websocket_manager
        self.subprocess_manager = SubprocessManager(websocket_manager)
        
        # Core consciousness metrics
        self.tick_number = 0
        self.scup = 78.8  # System Consciousness Unity Percentage
        self.entropy = 285285
        self.heat = 498498
        self.mood = "FOCUSED"
        
        # Consciousness state
        self.awareness_level = 0.88
        self.creativity_index = 0.72
        self.intuition_strength = 0.95
        
        self.running = True
        
    async def start(self):
        """Start the consciousness engine"""
        logger.info("🧠 Starting DAWN Consciousness Engine...")
        
        # Start all configured subprocesses
        await self.start_all_subprocesses()
        
        # Start main consciousness loop
        asyncio.create_task(self.consciousness_loop())
        
        logger.info("✅ DAWN Consciousness Engine started successfully")
    
    async def start_all_subprocesses(self):
        """Start all configured subprocesses"""
        logger.info("🚀 Starting all subprocesses...")
        
        for subprocess_id in self.subprocess_manager.subprocesses.keys():
            success = await self.subprocess_manager.start_subprocess(subprocess_id)
            if success:
                logger.info(f"✅ Started {subprocess_id}")
            else:
                logger.warning(f"❌ Failed to start {subprocess_id}")
    
    async def consciousness_loop(self):
        """Main consciousness processing loop"""
        logger.info("🔄 Starting consciousness loop...")
        
        while self.running:
            try:
                # Update core metrics
                await self.update_consciousness_state()
                
                # Broadcast tick data
                await self.broadcast_tick_data()
                
                # Update tick counter
                self.tick_number += 1
                
                # Sleep for next tick (targeting ~2000 Hz like your screenshot)
                await asyncio.sleep(0.0005)  # 0.5ms = 2000 Hz
                
            except Exception as e:
                logger.error(f"Error in consciousness loop: {e}")
                await asyncio.sleep(0.1)
    
    async def update_consciousness_state(self):
        """Update consciousness metrics based on subprocess data"""
        
        # Get subprocess metrics
        subprocess_data = self.subprocess_manager.get_subprocess_list()
        
        # Calculate SCUP based on neural processes
        neural_processes = [sp for sp in subprocess_data if sp['category'] == 'neural']
        if neural_processes:
            neural_avg = sum(
                list(sp['metrics'].values())[0]['value'] 
                for sp in neural_processes 
                if sp['metrics']
            ) / len(neural_processes)
            
            # Smooth SCUP changes
            target_scup = min(100, max(0, neural_avg))
            self.scup += (target_scup - self.scup) * 0.1
        else:
            # Fallback simulation
            self.scup += math.sin(time.time() * 0.1) * 2 + random.uniform(-1, 1)
            self.scup = min(100, max(0, self.scup))
        
        # Update entropy based on quantum processes
        quantum_processes = [sp for sp in subprocess_data if sp['category'] == 'quantum']
        if quantum_processes:
            quantum_activity = sum(
                list(sp['metrics'].values())[0]['value'] 
                for sp in quantum_processes 
                if sp['metrics']
            )
            self.entropy += int(quantum_activity * 100 + random.uniform(-5000, 5000))
        else:
            self.entropy += random.randint(-10000, 10000)
        
        # Update heat based on system load
        system_processes = [sp for sp in subprocess_data if sp['category'] == 'system']
        if system_processes:
            system_load = sum(
                list(sp['metrics'].values())[0]['value'] 
                for sp in system_processes 
                if sp['metrics']
            ) / len(system_processes)
            
            target_heat = system_load * 10000
            self.heat += int((target_heat - self.heat) * 0.05)
        else:
            self.heat += random.randint(-25000, 25000)
        
        # Update mood based on overall system state
        active_count = len([sp for sp in subprocess_data if sp['status'] == 'running'])
        total_count = len(subprocess_data)
        
        if total_count > 0:
            health_ratio = active_count / total_count
            if health_ratio > 0.8:
                moods = ["FOCUSED", "OPTIMAL", "TRANSCENDENT", "ENLIGHTENED"]
            elif health_ratio > 0.6:
                moods = ["ACTIVE", "PROCESSING", "ENGAGED"]
            else:
                moods = ["DEGRADED", "STRUGGLING", "RECOVERING"]
            
            # Occasionally change mood
            if random.random() < 0.01:  # 1% chance per tick
                self.mood = random.choice(moods)
    
    async def broadcast_tick_data(self):
        """Broadcast current tick data to all connected clients"""
        tick_data = {
            "type": "tick",
            "tick_number": self.tick_number,
            "scup": round(self.scup, 1),
            "entropy": int(self.entropy),
            "heat": int(self.heat),
            "mood": self.mood,
            "timestamp": time.time()
        }
        
        await self.websocket_manager.broadcast(tick_data)
    
    async def handle_client_message(self, websocket: WebSocket, data: Dict[str, Any]):
        """Handle messages from clients"""
        message_type = data.get("type")
        
        if message_type == "get_subprocesses":
            # Send subprocess list
            subprocess_list = {
                "type": "subprocess_list",
                "processes": self.subprocess_manager.get_subprocess_list()
            }
            await websocket.send_text(json.dumps(subprocess_list))
            
        elif message_type == "control_subprocess":
            subprocess_id = data.get("subprocess_id")
            action = data.get("action")
            
            if subprocess_id and action:
                logger.info(f"🎮 Client requested {action} for {subprocess_id}")
                
                if action == "start":
                    await self.subprocess_manager.start_subprocess(subprocess_id)
                elif action == "stop":
                    await self.subprocess_manager.stop_subprocess(subprocess_id)
                elif action == "restart":
                    await self.subprocess_manager.restart_subprocess(subprocess_id)
        
        elif message_type == "get_status":
            # Send system status
            status = {
                "type": "system_status",
                "tick_number": self.tick_number,
                "running_processes": len([
                    sp for sp in self.subprocess_manager.get_subprocess_list() 
                    if sp['status'] == 'running'
                ]),
                "total_processes": len(self.subprocess_manager.get_subprocess_list()),
                "uptime": time.time() - self.start_time if hasattr(self, 'start_time') else 0
            }
            await websocket.send_text(json.dumps(status))
    
    async def shutdown(self):
        """Shutdown the consciousness engine"""
        logger.info("🛑 Shutting down DAWN Consciousness Engine...")
        
        self.running = False
        await self.subprocess_manager.shutdown()
        
        logger.info("✅ DAWN Consciousness Engine shutdown complete")

# FastAPI application
app = FastAPI(title="DAWN Consciousness Engine API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
websocket_manager = DAWNWebSocketManager()
consciousness_engine = DAWNConsciousnessEngine(websocket_manager)

@app.on_event("startup")
async def startup_event():
    """Initialize the consciousness engine on startup"""
    consciousness_engine.start_time = time.time()
    await consciousness_engine.start()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await consciousness_engine.shutdown()

@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "online",
        "service": "DAWN Consciousness Engine",
        "version": "1.0.0",
        "tick": consciousness_engine.tick_number,
        "uptime": time.time() - consciousness_engine.start_time if hasattr(consciousness_engine, 'start_time') else 0
    }

@app.get("/status")
async def get_status():
    """Get detailed system status"""
    subprocess_data = consciousness_engine.subprocess_manager.get_subprocess_list()
    
    return {
        "consciousness": {
            "tick_number": consciousness_engine.tick_number,
            "scup": consciousness_engine.scup,
            "entropy": consciousness_engine.entropy,
            "heat": consciousness_engine.heat,
            "mood": consciousness_engine.mood
        },
        "subprocesses": {
            "total": len(subprocess_data),
            "running": len([sp for sp in subprocess_data if sp['status'] == 'running']),
            "stopped": len([sp for sp in subprocess_data if sp['status'] == 'stopped']),
            "error": len([sp for sp in subprocess_data if sp['status'] == 'error'])
        },
        "uptime": time.time() - consciousness_engine.start_time if hasattr(consciousness_engine, 'start_time') else 0
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Main WebSocket endpoint for real-time communication"""
    await websocket_manager.add_connection(websocket)
    
    # Send initial data
    try:
        # Send subprocess list
        subprocess_list = {
            "type": "subprocess_list",
            "processes": consciousness_engine.subprocess_manager.get_subprocess_list()
        }
        await websocket.send_text(json.dumps(subprocess_list))
        
        # Listen for client messages
        while True:
            data = await websocket.receive_json()
            await consciousness_engine.handle_client_message(websocket, data)
            
    except WebSocketDisconnect:
        websocket_manager.remove_connection(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        websocket_manager.remove_connection(websocket)

if __name__ == "__main__":
    print("🧠 DAWN Consciousness Engine")
    print("=" * 40)
    print("Starting integrated API server...")
    print("WebSocket: ws://localhost:8001/ws")
    print("REST API: http://localhost:8001")
    print("Status: http://localhost:8001/status")
    print("=" * 40)
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8001,
        log_level="info",
        access_log=True
    ) 