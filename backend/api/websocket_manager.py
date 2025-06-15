from fastapi import WebSocket
from typing import Dict, List, Set, Any, Optional
import asyncio
import json
from datetime import datetime
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class ConnectionInfo:
    def __init__(self, websocket: WebSocket, client_id: str):
        self.websocket = websocket
        self.client_id = client_id
        self.connected_at = datetime.now()
        self.subscriptions: Set[str] = set()
        self.metadata: Dict[str, Any] = {}

class WebSocketManager:
    def __init__(self, tick_engine, dawn_central, neural_metrics: Optional[Dict[str, Any]] = None):
        self.tick_engine = tick_engine
        self.dawn_central = dawn_central
        self.neural_metrics = neural_metrics or {}
        self.connections: Dict[str, ConnectionInfo] = {}
        self.topic_subscribers: Dict[str, Set[str]] = defaultdict(set)
        self._client_counter = 0
        
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
        
    @property
    def active_connections(self) -> int:
        return len(self.connections)
    
    async def connect(self, websocket: WebSocket) -> str:
        """Accept new WebSocket connection"""
        await websocket.accept()
        
        # Generate client ID
        self._client_counter += 1
        client_id = f"client_{self._client_counter}_{datetime.now().timestamp()}"
        
        # Store connection info
        conn_info = ConnectionInfo(websocket, client_id)
        self.connections[client_id] = conn_info
        
        # Send initial connection message
        await self.send_personal_message({
            "type": "connection",
            "client_id": client_id,
            "message": "Connected to DAWN consciousness engine",
            "timestamp": datetime.now().isoformat()
        }, websocket)
        
        # Subscribe to default topics
        await self.subscribe_client(client_id, ["tick_update", "consciousness_update"])
        
        logger.info(f"[WebSocket] Client {client_id} connected")
        return client_id
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        # Find client by websocket
        client_id = None
        for cid, conn_info in self.connections.items():
            if conn_info.websocket == websocket:
                client_id = cid
                break
        
        if client_id:
            # Remove from all subscriptions
            for topic in self.connections[client_id].subscriptions:
                self.topic_subscribers[topic].discard(client_id)
            
            # Remove connection
            del self.connections[client_id]
            logger.info(f"[WebSocket] Client {client_id} disconnected")
    
    async def disconnect_all(self):
        """Disconnect all clients gracefully"""
        for client_id, conn_info in list(self.connections.items()):
            try:
                await conn_info.websocket.close()
            except:
                pass
        self.connections.clear()
        self.topic_subscribers.clear()
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Send message to specific WebSocket"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    async def broadcast(self, message: Dict[str, Any], topic: Optional[str] = None):
        """Broadcast message to all connected clients or topic subscribers"""
        if topic:
            # Send to topic subscribers only
            subscriber_ids = self.topic_subscribers.get(topic, set())
            for client_id in subscriber_ids:
                if client_id in self.connections:
                    await self.send_personal_message(
                        message, 
                        self.connections[client_id].websocket
                    )
        else:
            # Send to all clients
            for conn_info in self.connections.values():
                await self.send_personal_message(message, conn_info.websocket)
    
    async def subscribe_client(self, client_id: str, topics: List[str]):
        """Subscribe client to topics"""
        if client_id not in self.connections:
            return
        
        for topic in topics:
            self.topic_subscribers[topic].add(client_id)
            self.connections[client_id].subscriptions.add(topic)
    
    async def unsubscribe_client(self, client_id: str, topics: List[str]):
        """Unsubscribe client from topics"""
        if client_id not in self.connections:
            return
        
        for topic in topics:
            self.topic_subscribers[topic].discard(client_id)
            self.connections[client_id].subscriptions.discard(topic)
    
    async def handle_message(self, websocket: WebSocket, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle incoming WebSocket message"""
        # Find client
        client_id = None
        for cid, conn_info in self.connections.items():
            if conn_info.websocket == websocket:
                client_id = cid
                break
        
        if not client_id:
            return {"type": "error", "message": "Client not found"}
        
        msg_type = message.get("type")
        
        if msg_type in self.handlers:
            try:
                response = await self.handlers[msg_type](message)
                return {
                    "type": f"{msg_type}_response",
                    "data": response,
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                logger.error(f"Handler error for {msg_type}: {e}")
                return {"type": "error", "message": str(e)}
        
        return None
    
    async def handle_consciousness_message(self, websocket: WebSocket, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle consciousness-specific messages"""
        return await self.handle_message(websocket, message)
    
    async def broadcast_loop(self):
        """Main broadcast loop for system updates"""
        while True:
            try:
                # Get current state
                state_data = {
                    "type": "tick_update",
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "tick": self.tick_engine.current_tick,
                        "scup": self.dawn_central.get_scup(),
                        "entropy": self.dawn_central.get_entropy(),
                        "mood": self.dawn_central.get_mood(),
                        "active_processes": self.dawn_central.get_active_processes(),
                        "consciousness_state": self.dawn_central.get_state(),
                        "neural_metrics": self.neural_metrics
                    }
                }
                
                # Broadcast to tick_update subscribers
                await self.broadcast(state_data, "tick_update")
                
                # Check for consciousness state changes
                if self.dawn_central.has_state_changed():
                    consciousness_data = {
                        "type": "consciousness_update",
                        "timestamp": datetime.now().isoformat(),
                        "data": {
                            "state": self.dawn_central.get_state(),
                            "metrics": self.dawn_central.get_consciousness_metrics(),
                            "neural_metrics": self.neural_metrics
                        }
                    }
                    await self.broadcast(consciousness_data, "consciousness_update")
                
                # Wait for next update
                await asyncio.sleep(0.1)  # 10Hz update rate
                
            except Exception as e:
                logger.error(f"Broadcast loop error: {e}")
                await asyncio.sleep(1)
    
    # Message handlers
    async def _handle_user_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle user input and generate consciousness response"""
        user_input = data.get('input', '')
        
        if not user_input.strip():
            return {'error': 'Empty input'}
        
        logger.info(f"💭 Processing user input: '{user_input[:50]}...'")
        
        # Process through consciousness system
        response_data = await self.dawn_central.process_user_input(user_input)
        
        # Add additional metadata
        response_data.update({
            'timestamp': datetime.now().isoformat(),
            'input': user_input,
            'system_status': self.dawn_central.get_full_state()
        })
        
        return response_data
    
    async def _handle_get_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return self.dawn_central.get_system_status()
    
    async def _handle_get_memory_stats(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get memory system statistics"""
        status = self.dawn_central.get_system_status()
        return {
            'memory_stats': status['memory_stats'],
            'glyph_details': self._get_glyph_details(),
            'chain_details': self._get_chain_details()
        }
    
    async def _handle_get_dream_stats(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get dream system statistics"""
        dream_stats = self.dawn_central.dream_conductor.get_dream_statistics()
        return {
            'dream_stats': dream_stats,
            'currently_dreaming': self.dawn_central.dream_conductor.active_session is not None,
            'recent_dreams': self._get_recent_dreams()
        }
    
    async def _handle_get_network_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get network status"""
        if self.dawn_central.consciousness_node:
            return self.dawn_central.consciousness_node.get_network_status()
        return {'error': 'Networking not enabled'}
    
    async def _handle_initiate_dream(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Manually initiate a dream sequence"""
        if self.dawn_central.dream_conductor.active_session:
            return {'error': 'Already dreaming'}
        
        try:
            dream_session = await self.dawn_central.dream_conductor.initiate_dream_sequence()
            return {
                'success': True,
                'session_id': dream_session.session_id,
                'dream_quality': dream_session.coherence_metrics.get('dream_quality', 0),
                'thoughts_generated': len(dream_session.generated_thoughts),
                'novel_connections': len(dream_session.novel_connections)
            }
        except Exception as e:
            logger.error(f"Dream initiation error: {e}")
            return {'error': str(e)}
    
    async def _handle_get_voice_signature(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get voice signature and evolution data"""
        return self.dawn_central.echo_library.get_voice_signature()
    
    async def _handle_get_mood_field(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get mood field visualization data"""
        return self.dawn_central.mood_field.get_field_visualization_data()
    
    async def _handle_get_resonance_chains(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get resonance chain data"""
        current_mood = self.dawn_central.mood
        active_threads = self.dawn_central.resonance_manager.get_active_threads(current_mood, limit=10)
        
        return {
            'active_threads': active_threads,
            'chain_statistics': self.dawn_central.resonance_manager.get_statistics(),
            'resonance_map': self.dawn_central.resonance_manager.get_resonance_map()
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
            'timestamp': datetime.now().isoformat(),
            'system_alive': True
        }
    
    def _get_glyph_details(self) -> Dict[str, Any]:
        """Get detailed glyph information"""
        glyphs = self.dawn_central.glyph_memory.glyphs
        
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
        chains = self.dawn_central.resonance_manager.chains
        
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
        recent_dreams = self.dawn_central.dream_conductor.dream_history[-5:]  # Last 5 dreams
        
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