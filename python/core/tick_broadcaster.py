import asyncio
import json
import logging
from typing import Set, Any, Dict
from dataclasses import asdict

logger = logging.getLogger(__name__)


class TickBroadcaster:
    """
    Handles broadcasting tick data to connected WebSocket clients
    """
    
    def __init__(self):
        self.connections: Set[Any] = set()
        self.broadcast_enabled = True
        
    def add_connection(self, websocket):
        """Add a WebSocket connection"""
        self.connections.add(websocket)
        logger.info(f"Added WebSocket connection. Total: {len(self.connections)}")
    
    def remove_connection(self, websocket):
        """Remove a WebSocket connection"""
        self.connections.discard(websocket)
        logger.info(f"Removed WebSocket connection. Total: {len(self.connections)}")
    
    async def broadcast_tick(self, tick_data):
        """Broadcast tick data to all connected clients"""
        if not self.broadcast_enabled or not self.connections:
            return
        
        # Convert tick data to dict for JSON serialization
        if hasattr(tick_data, 'to_dict'):
            data = tick_data.to_dict()
        elif hasattr(tick_data, '__dict__'):
            data = asdict(tick_data) if hasattr(tick_data, '__dataclass_fields__') else tick_data.__dict__
        else:
            data = tick_data
        
        message = {
            'type': 'tick',
            'data': data,
            'timestamp': data.get('timestamp', 0)
        }
        
        # Send to all connections
        disconnected = []
        for connection in self.connections:
            try:
                await connection.send(json.dumps(message))
            except Exception as e:
                logger.warning(f"Failed to send to connection: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected connections
        for connection in disconnected:
            self.remove_connection(connection)
    
    async def broadcast_message(self, message_type: str, data: Dict[str, Any]):
        """Broadcast a custom message to all connected clients"""
        if not self.broadcast_enabled or not self.connections:
            return
        
        message = {
            'type': message_type,
            'data': data,
            'timestamp': asyncio.get_event_loop().time()
        }
        
        # Send to all connections
        disconnected = []
        for connection in self.connections:
            try:
                await connection.send(json.dumps(message))
            except Exception as e:
                logger.warning(f"Failed to send message to connection: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected connections
        for connection in disconnected:
            self.remove_connection(connection)
    
    def enable_broadcasting(self):
        """Enable tick broadcasting"""
        self.broadcast_enabled = True
        logger.info("Tick broadcasting enabled")
    
    def disable_broadcasting(self):
        """Disable tick broadcasting"""
        self.broadcast_enabled = False
        logger.info("Tick broadcasting disabled")
    
    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.connections)
    
    async def close_all_connections(self):
        """Close all WebSocket connections"""
        for connection in list(self.connections):
            try:
                await connection.close()
            except Exception as e:
                logger.warning(f"Error closing connection: {e}")
        
        self.connections.clear()
        logger.info("All WebSocket connections closed") 