from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import json
from typing import List, Dict, Any, Optional, Set
import logging
import time
import websockets
from websockets.server import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosed, WebSocketException

# Import the tick engine
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from core.tick_engine import tick_engine, TickData

logger = logging.getLogger(__name__)


# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.owl_connections: List[WebSocket] = []  # Dedicated Owl connections

    async def connect(self, websocket: WebSocket, connection_type: str = "main"):
        await websocket.accept()
        
        if connection_type == "main":
            self.active_connections.append(websocket)
            logger.info(f"Main WebSocket connected. Total: {len(self.active_connections)}")
        elif connection_type == "owl":
            self.owl_connections.append(websocket)
            logger.info(f"Owl WebSocket connected. Total: {len(self.owl_connections)}")

    def disconnect(self, websocket: WebSocket, connection_type: str = "main"):
        try:
            if connection_type == "main":
                self.active_connections.remove(websocket)
            elif connection_type == "owl":
                self.owl_connections.remove(websocket)
            logger.info(f"{connection_type} WebSocket disconnected")
        except ValueError:
            pass

    async def broadcast_tick(self, data: dict):
        """Broadcast tick data to all main connections"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json({
                    "type": "tick",
                    "data": data
                })
            except:
                disconnected.append(connection)
        
        # Clean up disconnected
        for conn in disconnected:
            self.disconnect(conn, "main")

    async def broadcast_owl(self, data: dict):
        """Broadcast Owl observations to Owl connections"""
        disconnected = []
        for connection in self.owl_connections:
            try:
                await connection.send_json({
                    "type": "owl_observation",
                    "data": data
                })
            except:
                disconnected.append(connection)
        
        # Clean up disconnected
        for conn in disconnected:
            self.disconnect(conn, "owl")


# Global connection manager
manager = ConnectionManager()


# Register tick callback for broadcasting
async def broadcast_tick_callback(tick_data: TickData):
    """Callback to broadcast tick data"""
    await manager.broadcast_tick(tick_data.to_dict())
    
    # If Owl observations exist, broadcast them too
    if 'owl' in tick_engine.modules:
        # This would be set by the owl module during processing
        if hasattr(tick_data, 'owl_data'):
            await manager.broadcast_owl(tick_data.owl_data)


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting DAWN Tick Engine...")
    
    # Register broadcast callback
    tick_engine.register_callback(broadcast_tick_callback)
    
    # Start tick engine
    await tick_engine.start()
    
    yield
    
    # Shutdown
    logger.info("Shutting down DAWN Tick Engine...")
    await tick_engine.stop()


# Create FastAPI app
app = FastAPI(
    title="DAWN Tick Engine API",
    description="WebSocket API for DAWN consciousness tick engine with Owl integration",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# WebSocket endpoints
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Main tick data WebSocket"""
    await manager.connect(websocket, "main")
    try:
        # Send initial state
        await websocket.send_json({
            "type": "connection",
            "data": {
                "status": "connected",
                "engine_state": tick_engine.get_current_state()
            }
        })
        
        while True:
            # Handle incoming messages
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                if message.get("type") == "heartbeat":
                    await websocket.send_json({
                        "type": "heartbeat_response",
                        "timestamp": message.get("timestamp")
                    })
                elif message.get("type") == "get_history":
                    count = message.get("count", 100)
                    history = tick_engine.get_tick_history(count)
                    await websocket.send_json({
                        "type": "history",
                        "data": [tick.to_dict() for tick in history]
                    })
                    
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON"
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, "main")


@app.websocket("/owl")
async def owl_websocket_endpoint(websocket: WebSocket):
    """Dedicated Owl observations WebSocket"""
    await manager.connect(websocket, "owl")
    try:
        # Send initial Owl state if available
        if 'owl' in tick_engine.modules:
            owl_module = tick_engine.modules['owl']
            await websocket.send_json({
                "type": "owl_state",
                "data": {
                    "observation_count": len(owl_module.observations),
                    "active_plans": list(owl_module.active_plans.keys()),
                    "planning_horizons": owl_module.planning_horizons
                }
            })
        
        while True:
            # Handle incoming Owl-specific messages
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                if message.get("type") == "get_observations":
                    count = message.get("count", 50)
                    if 'owl' in tick_engine.modules:
                        owl_module = tick_engine.modules['owl']
                        observations = list(owl_module.observations)[-count:]
                        await websocket.send_json({
                            "type": "observations",
                            "data": [obs.__dict__ for obs in observations]
                        })
                
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON"
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, "owl")


# REST endpoints
@app.get("/api/engine/status")
async def get_engine_status():
    """Get current engine status"""
    return tick_engine.get_current_state()


@app.get("/api/engine/history")
async def get_tick_history(count: int = 100):
    """Get recent tick history"""
    history = tick_engine.get_tick_history(count)
    return {
        "count": len(history),
        "ticks": [tick.to_dict() for tick in history]
    }


@app.post("/api/engine/config")
async def update_engine_config(config: Dict[str, Any]):
    """Update engine configuration"""
    # TODO: Implement configuration updates
    return {"status": "configuration_update_not_implemented"}


@app.get("/api/owl/observations")
async def get_owl_observations(count: int = 50):
    """Get recent Owl observations"""
    if 'owl' not in tick_engine.modules:
        return {"error": "Owl module not enabled"}
    
    owl_module = tick_engine.modules['owl']
    observations = list(owl_module.observations)[-count:]
    
    return {
        "count": len(observations),
        "observations": [obs.__dict__ for obs in observations]
    }


@app.get("/api/owl/plans")
async def get_owl_plans():
    """Get active Owl strategic plans"""
    if 'owl' not in tick_engine.modules:
        return {"error": "Owl module not enabled"}
    
    owl_module = tick_engine.modules['owl']
    plans = [plan.__dict__ for plan in owl_module.active_plans.values()]
    
    return {
        "count": len(plans),
        "plans": plans
    }


@app.get("/api/owl/schemas")
async def get_owl_schema_alignments():
    """Get current schema alignments"""
    if 'owl' not in tick_engine.modules:
        return {"error": "Owl module not enabled"}
    
    owl_module = tick_engine.modules['owl']
    
    return {
        "alignments": owl_module.schema_alignments,
        "trajectory": owl_module.semantic_trajectory[-10:] if len(owl_module.semantic_trajectory) > 10 else owl_module.semantic_trajectory
    }


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "engine_running": tick_engine.is_running,
        "tick_count": tick_engine.tick_count,
        "uptime": tick_engine.get_current_state().get('uptime', 0),
        "modules": list(tick_engine.modules.keys())
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "DAWN Tick Engine API with Owl Integration",
        "version": "1.0.0",
        "endpoints": {
            "websocket_main": "/ws",
            "websocket_owl": "/owl", 
            "health": "/health",
            "engine_status": "/api/engine/status",
            "tick_history": "/api/engine/history",
            "owl_observations": "/api/owl/observations",
            "owl_plans": "/api/owl/plans",
            "owl_schemas": "/api/owl/schemas"
        }
    }


class WebSocketServer:
    """
    WebSocket server for real-time communication with DAWN frontend.
    Handles tick broadcasting, Owl observations, and bidirectional messaging.
    """
    
    def __init__(self, host: str = "localhost", port: int = 8001):
        self.host = host
        self.port = port
        self.connections: Set[WebSocketServerProtocol] = set()
        self.tick_engine = None
        self.running = False
        
        # Message queues for different channels
        self.tick_queue = asyncio.Queue()
        self.owl_queue = asyncio.Queue()
        self.command_queue = asyncio.Queue()
        
        # Connection tracking
        self.connection_stats = {
            'total_connections': 0,
            'active_connections': 0,
            'messages_sent': 0,
            'messages_received': 0,
            'errors': 0
        }
        
        # CORS settings for frontend integration
        self.cors_origins = [
            "http://localhost:5173",  # Vite dev server
            "http://localhost:3000",  # React dev server
            "http://127.0.0.1:5173",
            "http://127.0.0.1:3000"
        ]
        
        logger.info(f"WebSocket server initialized for {host}:{port}")
    
    def set_tick_engine(self, tick_engine):
        """Set reference to the tick engine"""
        self.tick_engine = tick_engine
        logger.info("Tick engine reference set")
    
    async def start_server(self):
        """Start the WebSocket server"""
        try:
            # Add CORS headers
            async def handle_connection(websocket, path):
                await self._handle_connection(websocket, path)
            
            # Start server with CORS support
            server = await websockets.serve(
                handle_connection,
                self.host,
                self.port,
                origins=self.cors_origins,
                compression=None,  # Disable compression for real-time performance
                max_size=10**6,   # 1MB max message size
                max_queue=32      # Connection queue size
            )
            
            self.running = True
            logger.info(f"WebSocket server started on ws://{self.host}:{self.port}")
            
            # Start background tasks
            await asyncio.gather(
                self._broadcast_ticks(),
                self._broadcast_owl_messages(),
                self._process_commands(),
                server.wait_closed()
            )
            
        except Exception as e:
            logger.error(f"Failed to start WebSocket server: {e}")
            raise
    
    async def _handle_connection(self, websocket: WebSocketServerProtocol, path: str):
        """Handle a new WebSocket connection"""
        client_ip = websocket.remote_address[0] if websocket.remote_address else "unknown"
        
        try:
            # Add connection
            self.connections.add(websocket)
            self.connection_stats['total_connections'] += 1
            self.connection_stats['active_connections'] += 1
            
            logger.info(f"New WebSocket connection from {client_ip} (path: {path})")
            
            # Send initial state
            await self._send_initial_state(websocket)
            
            # Handle messages from this connection
            async for message in websocket:
                await self._handle_message(websocket, message)
                
        except ConnectionClosed:
            logger.info(f"WebSocket connection from {client_ip} closed")
        except WebSocketException as e:
            logger.warning(f"WebSocket error from {client_ip}: {e}")
            self.connection_stats['errors'] += 1
        except Exception as e:
            logger.error(f"Unexpected error handling connection from {client_ip}: {e}")
            self.connection_stats['errors'] += 1
        finally:
            # Remove connection
            self.connections.discard(websocket)
            self.connection_stats['active_connections'] -= 1
            logger.debug(f"Connection from {client_ip} cleaned up")
    
    async def _send_initial_state(self, websocket: WebSocketServerProtocol):
        """Send initial system state to new connection"""
        try:
            initial_state = {
                'type': 'initial_state',
                'data': {
                    'server_time': time.time(),
                    'status': 'connected',
                    'tick_engine_running': self.tick_engine is not None and hasattr(self.tick_engine, 'running') and self.tick_engine.running,
                    'connection_id': id(websocket),
                    'supported_messages': [
                        'tick_data',
                        'owl_observation', 
                        'owl_plan',
                        'command',
                        'status_update'
                    ]
                },
                'timestamp': time.time()
            }
            
            await websocket.send(json.dumps(initial_state))
            logger.debug("Sent initial state to new connection")
            
        except Exception as e:
            logger.error(f"Failed to send initial state: {e}")
    
    async def _handle_message(self, websocket: WebSocketServerProtocol, message: str):
        """Handle incoming message from WebSocket client"""
        try:
            data = json.loads(message)
            self.connection_stats['messages_received'] += 1
            
            message_type = data.get('type')
            
            if message_type == 'command':
                await self._handle_command(websocket, data)
            elif message_type == 'subscription':
                await self._handle_subscription(websocket, data)
            elif message_type == 'ping':
                await self._handle_ping(websocket, data)
            elif message_type == 'owl_feedback':
                await self._handle_owl_feedback(websocket, data)
            else:
                logger.warning(f"Unknown message type: {message_type}")
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON received from WebSocket client")
        except Exception as e:
            logger.error(f"Error handling WebSocket message: {e}")
    
    async def _handle_command(self, websocket: WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle command from frontend"""
        command = data.get('command')
        params = data.get('params', {})
        
        try:
            if command == 'start_tick_engine':
                if self.tick_engine:
                    await self.tick_engine.start()
                    response = {'status': 'success', 'message': 'Tick engine started'}
                else:
                    response = {'status': 'error', 'message': 'Tick engine not available'}
            
            elif command == 'stop_tick_engine':
                if self.tick_engine:
                    await self.tick_engine.stop()
                    response = {'status': 'success', 'message': 'Tick engine stopped'}
                else:
                    response = {'status': 'error', 'message': 'Tick engine not available'}
            
            elif command == 'adjust_tick_rate':
                rate = params.get('rate', 10)
                if self.tick_engine:
                    self.tick_engine.set_tick_rate(rate)
                    response = {'status': 'success', 'message': f'Tick rate set to {rate} Hz'}
                else:
                    response = {'status': 'error', 'message': 'Tick engine not available'}
            
            elif command == 'trigger_pattern':
                pattern_type = params.get('pattern', 'burst')
                # Add to command queue for tick engine to process
                await self.command_queue.put({
                    'command': 'trigger_pattern',
                    'params': {'pattern': pattern_type}
                })
                response = {'status': 'success', 'message': f'Pattern {pattern_type} triggered'}
            
            elif command == 'get_status':
                response = await self._get_system_status()
            
            else:
                response = {'status': 'error', 'message': f'Unknown command: {command}'}
            
            # Send response
            await websocket.send(json.dumps({
                'type': 'command_response',
                'data': response,
                'timestamp': time.time()
            }))
            
        except Exception as e:
            logger.error(f"Error handling command {command}: {e}")
            await websocket.send(json.dumps({
                'type': 'command_response',
                'data': {'status': 'error', 'message': str(e)},
                'timestamp': time.time()
            }))
    
    async def _handle_subscription(self, websocket: WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle subscription requests"""
        subscription_type = data.get('subscription')
        
        # For now, all connections get all data
        # In future, could implement selective subscriptions
        response = {
            'status': 'success',
            'message': f'Subscribed to {subscription_type}',
            'subscriptions': ['tick_data', 'owl_observations', 'system_status']
        }
        
        await websocket.send(json.dumps({
            'type': 'subscription_response',
            'data': response,
            'timestamp': time.time()
        }))
    
    async def _handle_ping(self, websocket: WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle ping for connection health"""
        await websocket.send(json.dumps({
            'type': 'pong',
            'data': {
                'server_time': time.time(),
                'client_time': data.get('timestamp', 0)
            },
            'timestamp': time.time()
        }))
    
    async def _handle_owl_feedback(self, websocket: WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle feedback from Owl module in frontend"""
        feedback = data.get('feedback', {})
        
        # Process Owl feedback (recommendations, plan updates, etc.)
        if self.tick_engine and hasattr(self.tick_engine, 'owl_module'):
            # Forward feedback to Owl module
            await self.command_queue.put({
                'command': 'owl_feedback',
                'params': feedback
            })
        
        logger.debug(f"Received Owl feedback: {feedback}")
    
    async def _broadcast_ticks(self):
        """Broadcast tick data to all connected clients"""
        while self.running:
            try:
                # Wait for tick data
                tick_data = await self.tick_queue.get()
                
                if self.connections:
                    message = json.dumps({
                        'type': 'tick_data',
                        'data': tick_data,
                        'timestamp': time.time()
                    })
                    
                    # Broadcast to all connections
                    await self._broadcast_message(message)
                
            except Exception as e:
                logger.error(f"Error broadcasting tick: {e}")
                await asyncio.sleep(0.1)
    
    async def _broadcast_owl_messages(self):
        """Broadcast Owl observations and plans"""
        while self.running:
            try:
                # Wait for Owl data
                owl_data = await self.owl_queue.get()
                
                if self.connections:
                    message = json.dumps({
                        'type': 'owl_update',
                        'data': owl_data,
                        'timestamp': time.time()
                    })
                    
                    # Broadcast to all connections
                    await self._broadcast_message(message)
                
            except Exception as e:
                logger.error(f"Error broadcasting Owl message: {e}")
                await asyncio.sleep(0.1)
    
    async def _process_commands(self):
        """Process commands from the command queue"""
        while self.running:
            try:
                # Wait for commands
                command_data = await self.command_queue.get()
                
                # Forward to tick engine if available
                if self.tick_engine and hasattr(self.tick_engine, 'process_external_command'):
                    await self.tick_engine.process_external_command(command_data)
                
            except Exception as e:
                logger.error(f"Error processing command: {e}")
                await asyncio.sleep(0.1)
    
    async def _broadcast_message(self, message: str):
        """Broadcast message to all connected clients"""
        if not self.connections:
            return
        
        # Send to all connections, removing dead ones
        dead_connections = set()
        
        for connection in self.connections.copy():
            try:
                await connection.send(message)
                self.connection_stats['messages_sent'] += 1
            except ConnectionClosed:
                dead_connections.add(connection)
            except Exception as e:
                logger.warning(f"Error sending to connection: {e}")
                dead_connections.add(connection)
        
        # Remove dead connections
        for connection in dead_connections:
            self.connections.discard(connection)
            self.connection_stats['active_connections'] -= 1
    
    async def _get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            'server_running': self.running,
            'active_connections': len(self.connections),
            'tick_engine_running': self.tick_engine is not None and hasattr(self.tick_engine, 'running') and self.tick_engine.running,
            'connection_stats': self.connection_stats.copy(),
            'server_time': time.time()
        }
    
    # Public methods for tick engine integration
    
    async def broadcast_tick(self, tick_data: Dict[str, Any]):
        """Add tick data to broadcast queue"""
        await self.tick_queue.put(tick_data)
    
    async def broadcast_owl_update(self, owl_data: Dict[str, Any]):
        """Add Owl update to broadcast queue"""
        await self.owl_queue.put(owl_data)
    
    async def send_status_update(self, status_data: Dict[str, Any]):
        """Send status update to all connections"""
        if self.connections:
            message = json.dumps({
                'type': 'status_update',
                'data': status_data,
                'timestamp': time.time()
            })
            
            await self._broadcast_message(message)
    
    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.connections)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get server statistics"""
        return {
            'running': self.running,
            'connections': len(self.connections),
            'stats': self.connection_stats.copy(),
            'host': self.host,
            'port': self.port
        }
    
    async def stop_server(self):
        """Stop the WebSocket server"""
        self.running = False
        
        # Close all connections
        if self.connections:
            await asyncio.gather(
                *[connection.close() for connection in self.connections],
                return_exceptions=True
            )
        
        logger.info("WebSocket server stopped")


if __name__ == "__main__":
    import uvicorn
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    ) 