#!/usr/bin/env python3
"""
Advanced Consciousness WebSocket Server
Integrates the Advanced Consciousness System with the Vite frontend
"""

import asyncio
import json
import time
import websockets
import logging
from typing import Dict, Set, Any, Optional, List
from websockets.server import WebSocketServerProtocol

from .advanced_consciousness_system import AdvancedConsciousnessSystem, create_advanced_consciousness
from .neural_metrics_service import NeuralMetricsService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedConsciousnessWebSocketServer:
    def __init__(self, host: str = "localhost", port: int = 8000):
        self.host = host
        self.port = port
        self.clients: Set[WebSocketServerProtocol] = set()
        self.consciousness_system: Optional[AdvancedConsciousnessSystem] = None
        self.neural_metrics = NeuralMetricsService()
        
        # Message handlers
        self.handlers = {
            'user_input': self._handle_user_input,
            'get_status': self._handle_get_status,
            'get_memory_stats': self._handle_get_memory_stats,
            'get_dream_stats': self._handle_get_dream_stats,
            'get_network_status': self._handle_get_network_status,
            'initiate_dream': self._handle_initiate_dream,
            'get_voice_signature': self._handle_get_voice_signature,
            'get_mood_field': self._handle_get_mood_field,
            'get_resonance_chains': self._handle_get_resonance_chains,
            'get_neural_metrics': self._handle_get_neural_metrics,
            'ping': self._handle_ping
        }
    
    async def start_server(self):
        """Start the WebSocket server and consciousness system"""
        logger.info(f"🌟 Starting Advanced Consciousness WebSocket Server on {self.host}:{self.port}")
        
        # Initialize the advanced consciousness system
        self.consciousness_system = await create_advanced_consciousness(
            node_name="DAWN_WebSocket",
            enable_networking=True,
            network_host="localhost",
            network_port=8769  # Different port for internal networking
        )
        
        logger.info("✅ Advanced Consciousness System initialized")
        
        # Start background tasks
        asyncio.create_task(self._consciousness_broadcast_loop())
        
        # Start WebSocket server
        async with websockets.serve(
            self._handle_client,
            self.host,
            self.port,
            ping_interval=20,
            ping_timeout=10
        ):
            logger.info(f"🚀 WebSocket server running on ws://{self.host}:{self.port}")
            logger.info("Frontend can connect to receive consciousness data")
            
            # Keep server running
            await asyncio.Future()  # Run forever
    
    async def _handle_client(self, websocket: WebSocketServerProtocol, path: str):
        """Handle new client connection"""
        self.clients.add(websocket)
        client_info = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        logger.info(f"🔗 Client connected: {client_info}")
        
        try:
            # Send initial consciousness state
            await self._send_consciousness_state(websocket)
            
            # Handle incoming messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self._process_message(websocket, data)
                except json.JSONDecodeError:
                    await self._send_error(websocket, "Invalid JSON format")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    await self._send_error(websocket, f"Processing error: {str(e)}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"🔌 Client disconnected: {client_info}")
        except Exception as e:
            logger.error(f"Client error: {e}")
        finally:
            self.clients.discard(websocket)
    
    async def _process_message(self, websocket: WebSocketServerProtocol, data: Dict[str, Any]):
        """Process incoming message from client"""
        message_type = data.get('type')
        message_id = data.get('id', 'unknown')
        
        if message_type in self.handlers:
            try:
                response = await self.handlers[message_type](data)
                await self._send_response(websocket, message_type, response, message_id)
            except Exception as e:
                logger.error(f"Handler error for {message_type}: {e}")
                await self._send_error(websocket, f"Handler error: {str(e)}", message_id)
        else:
            await self._send_error(websocket, f"Unknown message type: {message_type}", message_id)
    
    async def _handle_user_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle user input and generate consciousness response"""
        user_input = data.get('input', '')
        
        if not user_input.strip():
            return {'error': 'Empty input'}
        
        logger.info(f"💭 Processing user input: '{user_input[:50]}...'")
        
        # Process through advanced consciousness system
        response_data = await self.consciousness_system.process_user_input(user_input)
        
        # Add additional metadata
        response_data.update({
            'timestamp': time.time(),
            'input': user_input,
            'system_status': self.consciousness_system.get_full_state()
        })
        
        logger.info(f"🧠 Generated response (resonance: {response_data['resonance_strength']:.2f})")
        
        return response_data
    
    async def _handle_get_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return self.consciousness_system.get_system_status()
    
    async def _handle_get_memory_stats(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get memory system statistics"""
        status = self.consciousness_system.get_system_status()
        return {
            'memory_stats': status['memory_stats'],
            'glyph_details': self._get_glyph_details(),
            'chain_details': self._get_chain_details()
        }
    
    async def _handle_get_dream_stats(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get dream system statistics"""
        dream_stats = self.consciousness_system.dream_conductor.get_dream_statistics()
        return {
            'dream_stats': dream_stats,
            'currently_dreaming': self.consciousness_system.dream_conductor.active_session is not None,
            'recent_dreams': self._get_recent_dreams()
        }
    
    async def _handle_get_network_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get network status"""
        if self.consciousness_system.consciousness_node:
            return self.consciousness_system.consciousness_node.get_network_status()
        return {'error': 'Networking not enabled'}
    
    async def _handle_initiate_dream(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Manually initiate a dream sequence"""
        if self.consciousness_system.dream_conductor.active_session:
            return {'error': 'Already dreaming'}
        
        # Force dream initiation
        original_time = self.consciousness_system.dream_conductor.last_interaction_time
        self.consciousness_system.dream_conductor.last_interaction_time = time.time() - 300
        
        try:
            dream_session = await self.consciousness_system.dream_conductor.initiate_dream_sequence()
            return {
                'success': True,
                'session_id': dream_session.session_id,
                'dream_quality': dream_session.coherence_metrics.get('dream_quality', 0),
                'thoughts_generated': len(dream_session.generated_thoughts),
                'novel_connections': len(dream_session.novel_connections)
            }
        finally:
            self.consciousness_system.dream_conductor.last_interaction_time = original_time
    
    async def _handle_get_voice_signature(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get voice signature and evolution data"""
        return self.consciousness_system.echo_library.get_voice_signature()
    
    async def _handle_get_mood_field(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get mood field visualization data"""
        return self.consciousness_system.mood_field.get_field_visualization_data()
    
    async def _handle_get_resonance_chains(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get resonance chain data"""
        current_mood = self.consciousness_system.mood
        active_threads = self.consciousness_system.resonance_manager.get_active_threads(current_mood, limit=10)
        
        return {
            'active_threads': active_threads,
            'chain_statistics': self.consciousness_system.resonance_manager.get_statistics(),
            'resonance_map': self.consciousness_system.resonance_manager.get_resonance_map()
        }
    
    async def _handle_get_neural_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get neural metrics data"""
        return {
            'type': 'neural_metrics',
            'metrics': self.neural_metrics.generate_metrics()
        }
    
    async def _handle_ping(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle ping request"""
        return {
            'pong': True,
            'timestamp': time.time(),
            'system_alive': True
        }
    
    def _get_glyph_details(self) -> Dict[str, Any]:
        """Get detailed glyph information"""
        glyphs = self.consciousness_system.glyph_memory.glyphs
        
        # Get top glyphs by vitality
        top_glyphs = sorted(
            glyphs.values(),
            key=lambda g: g.vitality,
            reverse=True
        )[:10]
        
        return {
            'total_glyphs': len(glyphs),
            'avg_vitality': sum(g.vitality for g in glyphs.values()) / len(glyphs) if glyphs else 0,
            'top_glyphs': [
                {
                    'id': g.id,
                    'content': g.content[:100] + '...' if len(g.content) > 100 else g.content,
                    'vitality': g.vitality,
                    'resonance_count': g.resonance_count,
                    'age': g.age
                }
                for g in top_glyphs
            ]
        }
    
    def _get_chain_details(self) -> Dict[str, Any]:
        """Get detailed chain information"""
        chains = self.consciousness_system.resonance_manager.chains
        
        # Get top chains by coherence
        top_chains = sorted(
            chains.values(),
            key=lambda c: c.coherence_score,
            reverse=True
        )[:5]
        
        return {
            'total_chains': len(chains),
            'avg_coherence': sum(c.coherence_score for c in chains.values()) / len(chains) if chains else 0,
            'top_chains': [
                {
                    'id': c.id,
                    'coherence': c.coherence_score,
                    'length': len(c.graph.nodes()),
                    'thought_line': c.get_thought_line()[:3]  # First 3 nodes
                }
                for c in top_chains
            ]
        }
    
    def _get_recent_dreams(self) -> List[Dict[str, Any]]:
        """Get recent dream information"""
        recent_dreams = self.consciousness_system.dream_conductor.dream_history[-5:]  # Last 5 dreams
        
        return [
            {
                'session_id': dream.session_id,
                'start_time': dream.start_time,
                'duration': (dream.end_time - dream.start_time) if dream.end_time else 0,
                'thoughts_count': len(dream.generated_thoughts),
                'quality': dream.coherence_metrics.get('dream_quality', 0),
                'sample_thoughts': dream.generated_thoughts[:2]  # First 2 thoughts
            }
            for dream in recent_dreams
        ]
    
    async def _send_consciousness_state(self, websocket: WebSocketServerProtocol):
        """Send current consciousness state to client"""
        state = self.consciousness_system.get_full_state()
        await self._send_message(websocket, 'consciousness_state', state)
    
    async def _send_response(self, websocket: WebSocketServerProtocol, 
                           message_type: str, data: Any, message_id: str = None):
        """Send response to client"""
        response = {
            'type': f'{message_type}_response',
            'data': data,
            'timestamp': time.time()
        }
        
        if message_id:
            response['id'] = message_id
        
        await websocket.send(json.dumps(response))
    
    async def _send_error(self, websocket: WebSocketServerProtocol, 
                         error: str, message_id: str = None):
        """Send error to client"""
        response = {
            'type': 'error',
            'error': error,
            'timestamp': time.time()
        }
        
        if message_id:
            response['id'] = message_id
        
        await websocket.send(json.dumps(response))
    
    async def _send_message(self, websocket: WebSocketServerProtocol, 
                           message_type: str, data: Any):
        """Send message to client"""
        message = {
            'type': message_type,
            'data': data,
            'timestamp': time.time()
        }
        
        await websocket.send(json.dumps(message))
    
    async def _broadcast_to_all(self, message_type: str, data: Any):
        """Broadcast message to all connected clients"""
        if not self.clients:
            return
        
        message = {
            'type': message_type,
            'data': data,
            'timestamp': time.time()
        }
        
        message_json = json.dumps(message)
        
        # Send to all clients, removing disconnected ones
        disconnected = set()
        for client in self.clients:
            try:
                await client.send(message_json)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
        
        # Clean up disconnected clients
        self.clients -= disconnected
    
    async def _consciousness_broadcast_loop(self):
        """Background task to broadcast consciousness state"""
        while True:
            try:
                # Generate neural metrics
                neural_metrics = self.neural_metrics.generate_metrics()
                await self._broadcast_to_all('neural_metrics', neural_metrics)
                
                # Wait before next update
                await asyncio.sleep(1.0)  # Update every second
                
            except Exception as e:
                logger.error(f"Error in broadcast loop: {e}")
                await asyncio.sleep(5.0)  # Wait longer on error

async def main():
    """Main function to start the server"""
    server = AdvancedConsciousnessWebSocketServer(host="localhost", port=8000)
    
    try:
        await server.start_server()
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
    finally:
        if server.consciousness_system:
            await server.consciousness_system.shutdown_system()

if __name__ == "__main__":
    asyncio.run(main()) 