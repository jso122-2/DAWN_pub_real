#!/usr/bin/env python3
"""
DAWN Consciousness WebSocket Server
Sends real-time consciousness data to the frontend for visualization
"""

import asyncio
import json
import logging
import time
import random
import math
from typing import Dict, Any, List
import websockets
from websockets.server import WebSocketServerProtocol
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConsciousnessDataGenerator:
    """Generates simulated consciousness data with realistic patterns"""
    
    def __init__(self):
        self.base_time = time.time()
        self.entropy_trend = 0.5
        self.neural_trend = 0.5
        self.quantum_trend = 0.5
        self.system_load = 0.3
        self.mood_timer = 0
        self.current_mood = 'active'
        
    def generate_tick_data(self) -> Dict[str, Any]:
        """Generate realistic consciousness tick data"""
        current_time = time.time()
        elapsed = current_time - self.base_time
        
        # Add wave patterns for more realistic data
        wave_factor = math.sin(elapsed * 0.1) * 0.2
        
        # Update trends slowly
        self.entropy_trend += (random.random() - 0.5) * 0.01
        self.neural_trend += (random.random() - 0.5) * 0.01
        self.quantum_trend += (random.random() - 0.5) * 0.01
        self.system_load += (random.random() - 0.5) * 0.005
        
        # Clamp values
        self.entropy_trend = max(0.1, min(0.9, self.entropy_trend))
        self.neural_trend = max(0.1, min(0.9, self.neural_trend))
        self.quantum_trend = max(0.1, min(0.9, self.quantum_trend))
        self.system_load = max(0.05, min(0.8, self.system_load))
        
        # Add some noise
        entropy = max(0, min(1, self.entropy_trend + wave_factor + (random.random() - 0.5) * 0.1))
        neural_activity = max(0, min(1, self.neural_trend + wave_factor + (random.random() - 0.5) * 0.1))
        quantum_coherence = max(0, min(1, self.quantum_trend + wave_factor + (random.random() - 0.5) * 0.1))
        system_load = max(0, min(1, self.system_load + (random.random() - 0.5) * 0.05))
        
        # Calculate SCUP
        scup = (entropy + neural_activity + quantum_coherence) / 3 * 100
        
        # Update mood periodically
        self.mood_timer += 1
        if self.mood_timer > 30:  # Change mood every 30 ticks
            self.mood_timer = 0
            self.current_mood = self._calculate_mood(entropy, neural_activity, quantum_coherence, system_load)
        
        return {
            'timestamp': int(current_time * 1000),
            'entropy': entropy,
            'neuralActivity': neural_activity,
            'quantumCoherence': quantum_coherence,
            'systemLoad': system_load,
            'scup': scup,
            'mood': self.current_mood,
            'performance': {
                'fps': 60 + random.randint(-5, 5),
                'latency': 10 + random.randint(0, 20),
                'memoryUsage': 0.4 + random.random() * 0.3
            }
        }
    
    def _calculate_mood(self, entropy: float, neural: float, quantum: float, load: float) -> str:
        """Calculate mood based on consciousness metrics"""
        activity = (neural + quantum) / 2
        stability = 1 - entropy
        stress = load
        
        if stress > 0.8:
            return 'critical'
        elif entropy > 0.7:
            return 'chaotic'
        elif activity > 0.8 and stability > 0.6:
            return 'euphoric'
        elif activity > 0.6 and stability > 0.7:
            return 'excited'
        elif stability > 0.8 and activity < 0.4:
            return 'serene'
        elif activity < 0.3:
            return 'contemplative'
        elif stress > 0.6 or entropy > 0.6:
            return 'anxious'
        else:
            return 'active'

class ConsciousnessWebSocketServer:
    """WebSocket server for consciousness data streaming"""
    
    def __init__(self, host: str = 'localhost', port: int = 8000):
        self.host = host
        self.port = port
        self.clients: List[WebSocketServerProtocol] = []
        self.data_generator = ConsciousnessDataGenerator()
        self.is_running = False
        
    async def register_client(self, websocket: WebSocketServerProtocol):
        """Register a new client"""
        self.clients.append(websocket)
        logger.info(f"Client connected: {websocket.remote_address}. Total clients: {len(self.clients)}")
        
        # Send initial data
        initial_data = {
            'type': 'consciousness_update',
            'data': self.data_generator.generate_tick_data(),
            'timestamp': int(time.time() * 1000)
        }
        await websocket.send(json.dumps(initial_data))
        
    async def unregister_client(self, websocket: WebSocketServerProtocol):
        """Unregister a client"""
        if websocket in self.clients:
            self.clients.remove(websocket)
        logger.info(f"Client disconnected: {websocket.remote_address}. Total clients: {len(self.clients)}")
        
    async def broadcast_to_clients(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients"""
        if not self.clients:
            return
            
        message_str = json.dumps(message)
        disconnected_clients = []
        
        for client in self.clients:
            try:
                await client.send(message_str)
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.append(client)
            except Exception as e:
                logger.error(f"Error sending to client {client.remote_address}: {e}")
                disconnected_clients.append(client)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            await self.unregister_client(client)
    
    async def handle_client_message(self, websocket: WebSocketServerProtocol, message: str):
        """Handle incoming client messages"""
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            if message_type == 'request_consciousness_data':
                # Send current consciousness data
                response = {
                    'type': 'consciousness_update',
                    'data': self.data_generator.generate_tick_data(),
                    'timestamp': int(time.time() * 1000)
                }
                await websocket.send(json.dumps(response))
                logger.info(f"Sent consciousness data to {websocket.remote_address}")
                
            elif message_type == 'heartbeat':
                # Respond to heartbeat
                response = {
                    'type': 'heartbeat_response',
                    'timestamp': int(time.time() * 1000)
                }
                await websocket.send(json.dumps(response))
                
            else:
                logger.warning(f"Unknown message type: {message_type}")
                
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON from {websocket.remote_address}: {message}")
        except Exception as e:
            logger.error(f"Error handling message from {websocket.remote_address}: {e}")
    
    async def client_handler(self, websocket: WebSocketServerProtocol, path: str):
        """Handle individual client connections"""
        await self.register_client(websocket)
        
        try:
            async for message in websocket:
                await self.handle_client_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            logger.error(f"Error in client handler: {e}")
        finally:
            await self.unregister_client(websocket)
    
    async def tick_loop(self):
        """Main tick loop that generates and broadcasts consciousness data"""
        logger.info("Starting consciousness tick loop")
        
        while self.is_running:
            try:
                # Generate consciousness data
                tick_data = self.data_generator.generate_tick_data()
                
                # Broadcast to all clients
                message = {
                    'type': 'tick_data',
                    'data': tick_data,
                    'timestamp': int(time.time() * 1000)
                }
                
                await self.broadcast_to_clients(message)
                
                # Wait for next tick (60 FPS = ~16.67ms)
                await asyncio.sleep(1.0 / 60.0)
                
            except Exception as e:
                logger.error(f"Error in tick loop: {e}")
                await asyncio.sleep(0.1)
    
    async def start_server(self):
        """Start the WebSocket server"""
        self.is_running = True
        
        logger.info(f"Starting Consciousness WebSocket Server on {self.host}:{self.port}")
        
        # Start the WebSocket server
        server = await websockets.serve(
            self.client_handler,
            self.host,
            self.port,
            ping_interval=30,
            ping_timeout=10
        )
        
        # Start the tick loop
        tick_task = asyncio.create_task(self.tick_loop())
        
        logger.info("🧠 Consciousness WebSocket Server is running!")
        logger.info(f"Connect your frontend to: ws://{self.host}:{self.port}")
        
        try:
            # Keep the server running
            await server.wait_closed()
        except KeyboardInterrupt:
            logger.info("Received interrupt, shutting down...")
        finally:
            self.is_running = False
            tick_task.cancel()
            server.close()
            await server.wait_closed()

async def main():
    """Main entry point"""
    server = ConsciousnessWebSocketServer(host='localhost', port=8000)
    await server.start_server()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🧠 Consciousness server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        print(f"❌ Server failed: {e}") 