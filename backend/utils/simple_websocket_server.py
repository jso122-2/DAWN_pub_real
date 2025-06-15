#!/usr/bin/env python3
"""
Simple WebSocket server for DAWN subprocess manager
Provides mock data without complex dependencies
"""

import asyncio
import json
import time
import random
import math
import websockets
from websockets.server import serve
import logging
import sys
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleDAWNServer:
    def __init__(self):
        self.connected_clients = set()
        self.tick_count = 0
        self.start_time = time.time()
        
        # Mock subprocess data
        self.subprocesses = {
            "neural_activity": {
                "id": "neural_activity",
                "name": "Neural Activity Visualizer",
                "category": "neural",
                "enabled": True,
                "visible": True,
                "metrics": {
                    "cpu": 15.5,
                    "memory": 128.3,
                    "fps": 60.0,
                    "activity": 0.75
                }
            },
            "consciousness_analyzer": {
                "id": "consciousness_analyzer", 
                "name": "Consciousness Analyzer",
                "category": "consciousness",
                "enabled": True,
                "visible": True,
                "metrics": {
                    "cpu": 22.1,
                    "memory": 256.7,
                    "fps": 30.0,
                    "unity": 0.82
                }
            },
            "memory_consolidator": {
                "id": "memory_consolidator",
                "name": "Memory Consolidator", 
                "category": "memory",
                "enabled": True,
                "visible": True,
                "metrics": {
                    "cpu": 8.3,
                    "memory": 64.2,
                    "fps": 15.0,
                    "pressure": 0.45
                }
            },
            "entropy_reducer": {
                "id": "entropy_reducer",
                "name": "Entropy Reducer",
                "category": "system",
                "enabled": True,
                "visible": True,
                "metrics": {
                    "cpu": 12.7,
                    "memory": 89.1,
                    "fps": 45.0,
                    "reduction": 0.68
                }
            },
            "quantum_processor": {
                "id": "quantum_processor",
                "name": "Quantum State Processor",
                "category": "quantum",
                "enabled": True,
                "visible": True,
                "metrics": {
                    "cpu": 35.2,
                    "memory": 512.8,
                    "fps": 120.0,
                    "coherence": 0.91
                }
            }
        }

    async def register_client(self, websocket):
        """Register a new client"""
        self.connected_clients.add(websocket)
        logger.info(f"Client connected. Total: {len(self.connected_clients)}")
        
        # Send initial data
        await self.send_initial_data(websocket)

    async def unregister_client(self, websocket):
        """Unregister a client"""
        self.connected_clients.discard(websocket)
        logger.info(f"Client disconnected. Total: {len(self.connected_clients)}")

    async def send_initial_data(self, websocket):
        """Send initial connection data"""
        await websocket.send(json.dumps({
            "type": "connection",
            "data": {
                "status": "connected",
                "server_time": time.time(),
                "subprocess_count": len(self.subprocesses)
            }
        }))
        
        # Send subprocess list
        await websocket.send(json.dumps({
            "type": "subprocess_list",
            "data": list(self.subprocesses.values())
        }))

    async def handle_message(self, websocket, message):
        """Handle incoming messages"""
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            
            if msg_type == "heartbeat":
                await websocket.send(json.dumps({
                    "type": "heartbeat_response",
                    "timestamp": data.get("timestamp", time.time())
                }))
            
            elif msg_type == "toggle_process":
                process_id = data.get("process_id")
                if process_id in self.subprocesses:
                    self.subprocesses[process_id]["enabled"] = not self.subprocesses[process_id]["enabled"]
                    await self.broadcast_subprocess_update(process_id)
            
            elif msg_type == "toggle_visibility":
                process_id = data.get("process_id")
                if process_id in self.subprocesses:
                    self.subprocesses[process_id]["visible"] = not self.subprocesses[process_id]["visible"]
                    await self.broadcast_subprocess_update(process_id)
                    
        except json.JSONDecodeError:
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Invalid JSON"
            }))

    async def broadcast_subprocess_update(self, process_id):
        """Broadcast subprocess update to all clients"""
        if process_id in self.subprocesses:
            message = json.dumps({
                "type": "subprocess_update",
                "data": self.subprocesses[process_id]
            })
            
            disconnected = []
            # Create a copy to avoid "set changed size during iteration" error
            clients_copy = self.connected_clients.copy()
            
            for client in clients_copy:
                try:
                    await client.send(message)
                except websockets.exceptions.ConnectionClosed:
                    disconnected.append(client)
            
            # Clean up disconnected clients
            for client in disconnected:
                self.connected_clients.discard(client)

    async def broadcast_tick(self):
        """Broadcast tick data to all clients"""
        self.tick_count += 1
        current_time = time.time()
        
        # Generate mock consciousness data
        scup = 0.5 + 0.3 * math.sin(current_time * 0.1) + random.uniform(-0.1, 0.1)
        entropy = 0.4 + 0.2 * math.sin(current_time * 0.05) + random.uniform(-0.05, 0.05)
        heat = 0.3 + 0.4 * math.sin(current_time * 0.08) + random.uniform(-0.1, 0.1)
        
        # Update subprocess metrics
        for subprocess in self.subprocesses.values():
            if subprocess["enabled"]:
                # Add some realistic fluctuation
                subprocess["metrics"]["cpu"] += random.uniform(-2, 2)
                subprocess["metrics"]["cpu"] = max(0, min(100, subprocess["metrics"]["cpu"]))
                
                subprocess["metrics"]["memory"] += random.uniform(-5, 5)
                subprocess["metrics"]["memory"] = max(0, subprocess["metrics"]["memory"])
                
                subprocess["metrics"]["fps"] += random.uniform(-5, 5)
                subprocess["metrics"]["fps"] = max(0, subprocess["metrics"]["fps"])

        tick_data = {
            "type": "tick",
            "data": {
                "tick_number": self.tick_count,
                "timestamp": current_time,
                "scup": max(0, min(1, scup)),
                "entropy": max(0, min(1, entropy)),
                "heat": max(0, min(1, heat)),
                "mood": "focused" if scup > 0.6 else "contemplative" if scup > 0.4 else "dreaming",
                "neural_activity": random.uniform(0.3, 0.9),
                "consciousness_unity": random.uniform(0.5, 0.95),
                "memory_pressure": random.uniform(0.2, 0.8),
                "active_processes": [p["id"] for p in self.subprocesses.values() if p["enabled"]],
                "subprocesses": list(self.subprocesses.values())
            }
        }
        
        message = json.dumps(tick_data)
        disconnected = []
        
        # Create a copy of the connected clients to avoid "set changed size during iteration" error
        clients_copy = self.connected_clients.copy()
        
        for client in clients_copy:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.append(client)
        
        # Clean up disconnected clients
        for client in disconnected:
            self.connected_clients.discard(client)

    async def tick_loop(self):
        """Main tick loop"""
        while True:
            await self.broadcast_tick()
            await asyncio.sleep(0.1)  # 10Hz tick rate

    async def handle_client(self, websocket, path):
        """Handle individual client connections"""
        await self.register_client(websocket)
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister_client(websocket)

async def main():
    """Main server function"""
    server = SimpleDAWNServer()
    
    # Start tick loop
    asyncio.create_task(server.tick_loop())
    
    # Start WebSocket server
    logger.info("🌟 Starting Simple DAWN WebSocket Server")
    logger.info("📡 WebSocket endpoint: ws://localhost:8001/ws")
    logger.info("🔗 Connect your subprocess manager to ws://localhost:8001")
    
    async with serve(server.handle_client, "localhost", 8001):
        logger.info("✅ Server running on ws://localhost:8001")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user") 