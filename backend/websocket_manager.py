"""
WebSocket Manager for DAWN Tick Engine
"""

import json
import logging
import asyncio
import time
from typing import List, Dict, Callable, Any, Optional
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.message_handlers: Dict[str, List[Callable]] = {}
        self.debug = True
        self.tick_count = 0
        self.last_tick_time = None
        self.connection_metadata: Dict[WebSocket, Dict[str, Any]] = {}
        self.ping_interval = 30  # seconds
        self.ping_timeout = 10   # seconds
        self.max_reconnect_attempts = 5
        self.reconnect_delay = 1  # seconds

    async def connect(self, websocket: WebSocket):
        """Connect a new WebSocket client with metadata tracking and error handling"""
        try:
            await websocket.accept()
            self.active_connections.append(websocket)
            self.connection_metadata[websocket] = {
                "connected_at": time.time(),
                "last_ping": time.time(),
                "message_count": 0,
                "error_count": 0,
                "reconnect_attempts": 0
            }
            
            if self.debug:
                logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
                await self.send_personal_message({
                    "type": "connection_status",
                    "data": {
                        "status": "connected",
                        "message": "Connected to DAWN Tick Engine",
                        "timestamp": time.time()
                    }
                }, websocket)
            
            # Start ping task for this connection
            asyncio.create_task(self._ping_client(websocket))
            
        except Exception as e:
            logger.error(f"Error accepting WebSocket connection: {e}")
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
            if websocket in self.connection_metadata:
                del self.connection_metadata[websocket]
            raise

    def disconnect(self, websocket: WebSocket):
        """Disconnect a WebSocket client and clean up metadata"""
        try:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
                if websocket in self.connection_metadata:
                    del self.connection_metadata[websocket]
                if self.debug:
                    logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
        except Exception as e:
            logger.error(f"Error during WebSocket disconnect: {e}")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific client with error handling and reconnection logic"""
        if websocket not in self.active_connections:
            return

        try:
            if websocket.client_state == WebSocketState.CONNECTED:
                await websocket.send_json(message)
                if self.debug:
                    logger.debug(f"Sent message: {message}")
                self.connection_metadata[websocket]["message_count"] += 1
            else:
                logger.warning("Attempted to send message to disconnected client")
                self.disconnect(websocket)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            self.connection_metadata[websocket]["error_count"] += 1
            
            # Attempt reconnection if within limits
            if self.connection_metadata[websocket]["reconnect_attempts"] < self.max_reconnect_attempts:
                self.connection_metadata[websocket]["reconnect_attempts"] += 1
                await asyncio.sleep(self.reconnect_delay)
                try:
                    await websocket.accept()
                except Exception as reconnect_error:
                    logger.error(f"Reconnection failed: {reconnect_error}")
                    self.disconnect(websocket)
            else:
                logger.error("Max reconnection attempts reached")
                self.disconnect(websocket)

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients with error handling"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await self.send_personal_message(message, connection)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

    def on(self, message_type: str, handler: Callable[[Any], None]):
        """Register a handler for a specific message type"""
        if message_type not in self.message_handlers:
            self.message_handlers[message_type] = []
        self.message_handlers[message_type].append(handler)

    def off(self, message_type: str, handler: Callable[[Any], None]):
        """Remove a handler for a specific message type"""
        if message_type in self.message_handlers:
            self.message_handlers[message_type].remove(handler)

    async def handle_message(self, message: dict, websocket: WebSocket):
        """Handle incoming messages with validation and error handling"""
        try:
            message_type = message.get("type")
            if not message_type:
                raise ValueError("Message type is required")
            
            # Update connection metadata
            self.connection_metadata[websocket]["last_ping"] = time.time()
            
            # Handle ping messages
            if message_type == "ping":
                await self.send_personal_message({
                    "type": "pong",
                    "data": {"timestamp": time.time()}
                }, websocket)
                return
            
            # Handle other message types
            handlers = self.message_handlers.get(message_type, [])
            for handler in handlers:
                try:
                    await handler(message.get("data", {}), websocket)
                except Exception as e:
                    logger.error(f"Error in message handler {handler.__name__}: {e}")
                    self.connection_metadata[websocket]["error_count"] += 1
                    
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await self.send_personal_message({
                "type": "error",
                "data": {"message": f"Error processing message: {str(e)}"}
            }, websocket)

    async def _ping_client(self, websocket: WebSocket):
        """Maintain connection health with periodic pings and error handling"""
        try:
            while websocket in self.active_connections:
                await asyncio.sleep(self.ping_interval)
                if websocket in self.active_connections:
                    try:
                        if websocket.client_state == WebSocketState.CONNECTED:
                            await websocket.send_json({
                                "type": "ping",
                                "data": {"timestamp": time.time()}
                            })
                            self.connection_metadata[websocket]["last_ping"] = time.time()
                        else:
                            logger.warning("Client not in connected state during ping")
                            self.disconnect(websocket)
                            break
                    except Exception as e:
                        logger.error(f"Error during ping: {e}")
                        self.disconnect(websocket)
                        break
        except Exception as e:
            logger.error(f"Error in ping task: {e}")
            self.disconnect(websocket)

    def get_connection_stats(self) -> Dict[str, Any]:
        """Get statistics about current connections"""
        return {
            "total_connections": len(self.active_connections),
            "connections": [
                {
                    "connected_at": meta["connected_at"],
                    "message_count": meta["message_count"],
                    "error_count": meta["error_count"],
                    "reconnect_attempts": meta["reconnect_attempts"],
                    "uptime": time.time() - meta["connected_at"]
                }
                for meta in self.connection_metadata.values()
            ]
        }

    async def send_tick_data(self, tick_data: dict):
        """Send tick data to all connected clients"""
        self.tick_count += 1
        message = {
            "type": "tick",
            "data": {
                **tick_data,
                "tick_count": self.tick_count,
                "timestamp": asyncio.get_event_loop().time()
            }
        }
        await self.broadcast(message)

# Create global manager instance
manager = WebSocketManager() 