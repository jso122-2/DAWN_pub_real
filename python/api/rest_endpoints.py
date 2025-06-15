import asyncio
import json
import logging
import time
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

logger = logging.getLogger(__name__)


# Request/Response models
class TickEngineCommand(BaseModel):
    command: str
    params: Optional[Dict[str, Any]] = {}


class OwlCommand(BaseModel):
    action: str
    parameters: Optional[Dict[str, Any]] = {}


class SystemStatus(BaseModel):
    status: str
    timestamp: float
    tick_engine_running: bool
    websocket_connections: int
    uptime: float


class TickEngineConfig(BaseModel):
    tick_rate: Optional[float] = None
    max_scup: Optional[float] = None
    min_scup: Optional[float] = None
    entropy_range: Optional[List[float]] = None


class RestAPIServer:
    """
    REST API server for DAWN system control and status queries.
    Provides HTTP endpoints for system management and data access.
    """
    
    def __init__(self, host: str = "localhost", port: int = 8001):
        self.host = host
        self.port = port
        self.app = FastAPI(
            title="DAWN Consciousness System API",
            description="REST API for DAWN tick engine and consciousness modules",
            version="1.0.0"
        )
        
        self.tick_engine = None
        self.websocket_server = None
        self.start_time = time.time()
        
        # Setup CORS
        self._setup_cors()
        
        # Setup routes
        self._setup_routes()
        
        logger.info(f"REST API server initialized for {host}:{port}")
    
    def _setup_cors(self):
        """Setup CORS middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "http://localhost:5173",  # Vite dev server
                "http://localhost:3000",  # React dev server
                "http://127.0.0.1:5173",
                "http://127.0.0.1:3000"
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def _setup_routes(self):
        """Setup API routes"""
        
        # Health check
        @self.app.get("/health")
        async def health_check():
            return {
                "status": "healthy",
                "timestamp": time.time(),
                "uptime": time.time() - self.start_time
            }
        
        # System status
        @self.app.get("/status", response_model=SystemStatus)
        async def get_system_status():
            return SystemStatus(
                status="running" if self.tick_engine and hasattr(self.tick_engine, 'running') and self.tick_engine.running else "stopped",
                timestamp=time.time(),
                tick_engine_running=bool(self.tick_engine and hasattr(self.tick_engine, 'running') and self.tick_engine.running),
                websocket_connections=self.websocket_server.get_connection_count() if self.websocket_server else 0,
                uptime=time.time() - self.start_time
            )
        
        # Tick engine control
        @self.app.post("/tick-engine/command")
        async def tick_engine_command(command: TickEngineCommand):
            if not self.tick_engine:
                raise HTTPException(status_code=503, detail="Tick engine not available")
            
            try:
                if command.command == "start":
                    await self.tick_engine.start()
                    return {"status": "success", "message": "Tick engine started"}
                
                elif command.command == "stop":
                    await self.tick_engine.stop()
                    return {"status": "success", "message": "Tick engine stopped"}
                
                elif command.command == "restart":
                    await self.tick_engine.stop()
                    await asyncio.sleep(0.5)
                    await self.tick_engine.start()
                    return {"status": "success", "message": "Tick engine restarted"}
                
                elif command.command == "set_rate":
                    rate = command.params.get("rate", 10)
                    self.tick_engine.set_tick_rate(rate)
                    return {"status": "success", "message": f"Tick rate set to {rate} Hz"}
                
                else:
                    raise HTTPException(status_code=400, detail=f"Unknown command: {command.command}")
            
            except Exception as e:
                logger.error(f"Error executing tick engine command: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Get tick engine configuration
        @self.app.get("/tick-engine/config")
        async def get_tick_engine_config():
            if not self.tick_engine:
                raise HTTPException(status_code=503, detail="Tick engine not available")
            
            return {
                "tick_rate": getattr(self.tick_engine, 'tick_rate', 10),
                "running": getattr(self.tick_engine, 'running', False),
                "tick_count": getattr(self.tick_engine, 'tick_count', 0),
                "uptime": time.time() - getattr(self.tick_engine, 'start_time', time.time())
            }
        
        # Update tick engine configuration
        @self.app.put("/tick-engine/config")
        async def update_tick_engine_config(config: TickEngineConfig):
            if not self.tick_engine:
                raise HTTPException(status_code=503, detail="Tick engine not available")
            
            try:
                if config.tick_rate is not None:
                    self.tick_engine.set_tick_rate(config.tick_rate)
                
                # Update other config parameters
                if hasattr(self.tick_engine, 'consciousness_state'):
                    cs = self.tick_engine.consciousness_state
                    if config.max_scup is not None:
                        cs.max_scup = config.max_scup
                    if config.min_scup is not None:
                        cs.min_scup = config.min_scup
                
                return {"status": "success", "message": "Configuration updated"}
            
            except Exception as e:
                logger.error(f"Error updating tick engine config: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Get current consciousness state
        @self.app.get("/consciousness/state")
        async def get_consciousness_state():
            if not self.tick_engine or not hasattr(self.tick_engine, 'consciousness_state'):
                raise HTTPException(status_code=503, detail="Consciousness state not available")
            
            try:
                state = await self.tick_engine.consciousness_state.get_state()
                return state
            except Exception as e:
                logger.error(f"Error getting consciousness state: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Get tick history
        @self.app.get("/ticks/history")
        async def get_tick_history(limit: int = 100):
            if not self.tick_engine:
                raise HTTPException(status_code=503, detail="Tick engine not available")
            
            try:
                history = getattr(self.tick_engine, 'tick_history', [])
                return {
                    "ticks": history[-limit:],
                    "count": len(history),
                    "latest_tick": history[-1] if history else None
                }
            except Exception as e:
                logger.error(f"Error getting tick history: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Owl module endpoints
        @self.app.post("/owl/command")
        async def owl_command(command: OwlCommand):
            if not self.tick_engine or not hasattr(self.tick_engine, 'owl_module'):
                raise HTTPException(status_code=503, detail="Owl module not available")
            
            try:
                owl = self.tick_engine.owl_module
                
                if command.action == "get_observations":
                    count = command.parameters.get("count", 50)
                    observations = owl.get_observations(count)
                    return {"observations": observations}
                
                elif command.action == "get_plans":
                    count = command.parameters.get("count", 10)
                    plans = owl.get_strategic_plans(count)
                    return {"plans": plans}
                
                elif command.action == "enable":
                    owl.enable()
                    return {"status": "success", "message": "Owl module enabled"}
                
                elif command.action == "disable":
                    owl.disable()
                    return {"status": "success", "message": "Owl module disabled"}
                
                else:
                    raise HTTPException(status_code=400, detail=f"Unknown Owl action: {command.action}")
            
            except Exception as e:
                logger.error(f"Error executing Owl command: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Get Owl state
        @self.app.get("/owl/state")
        async def get_owl_state():
            if not self.tick_engine or not hasattr(self.tick_engine, 'owl_module'):
                raise HTTPException(status_code=503, detail="Owl module not available")
            
            try:
                tick_number = getattr(self.tick_engine, 'tick_count', 0)
                state = await self.tick_engine.owl_module.get_state(tick_number)
                return state
            except Exception as e:
                logger.error(f"Error getting Owl state: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Neural module endpoints
        @self.app.get("/neural/state")
        async def get_neural_state():
            if not self.tick_engine or not hasattr(self.tick_engine, 'neural_simulator'):
                raise HTTPException(status_code=503, detail="Neural simulator not available")
            
            try:
                tick_number = getattr(self.tick_engine, 'tick_count', 0)
                state = await self.tick_engine.neural_simulator.get_state(tick_number)
                return state
            except Exception as e:
                logger.error(f"Error getting neural state: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/neural/trigger-pattern")
        async def trigger_neural_pattern(pattern_type: str = "burst"):
            if not self.tick_engine or not hasattr(self.tick_engine, 'neural_simulator'):
                raise HTTPException(status_code=503, detail="Neural simulator not available")
            
            try:
                self.tick_engine.neural_simulator.trigger_pattern(pattern_type)
                return {"status": "success", "message": f"Neural pattern '{pattern_type}' triggered"}
            except Exception as e:
                logger.error(f"Error triggering neural pattern: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Consciousness module endpoints
        @self.app.get("/consciousness/state")
        async def get_consciousness_state():
            if not self.tick_engine or not hasattr(self.tick_engine, 'consciousness_state'):
                raise HTTPException(status_code=503, detail="Consciousness state manager not available")
            
            try:
                tick_number = getattr(self.tick_engine, 'tick_count', 0)
                state = await self.tick_engine.consciousness_state.get_state(tick_number)
                return state
            except Exception as e:
                logger.error(f"Error getting consciousness state: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/consciousness/measure")
        async def measure_qubit(qubit_id: str):
            if not self.tick_engine or not hasattr(self.tick_engine, 'consciousness_state'):
                raise HTTPException(status_code=503, detail="Consciousness state manager not available")
            
            try:
                result = self.tick_engine.consciousness_state.perform_measurement(qubit_id)
                return {"qubit_id": qubit_id, "measurement": result, "timestamp": time.time()}
            except Exception as e:
                logger.error(f"Error measuring qubit: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Memory module endpoints
        @self.app.get("/memory/state")
        async def get_memory_state():
            if not self.tick_engine or not hasattr(self.tick_engine, 'memory_manager'):
                raise HTTPException(status_code=503, detail="Memory manager not available")
            
            try:
                tick_number = getattr(self.tick_engine, 'tick_count', 0)
                state = await self.tick_engine.memory_manager.get_state(tick_number)
                return state
            except Exception as e:
                logger.error(f"Error getting memory state: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/memory/summary")
        async def get_memory_summary():
            if not self.tick_engine or not hasattr(self.tick_engine, 'memory_manager'):
                raise HTTPException(status_code=503, detail="Memory manager not available")
            
            try:
                summary = self.tick_engine.memory_manager.get_memory_summary()
                return summary
            except Exception as e:
                logger.error(f"Error getting memory summary: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # WebSocket connection info
        @self.app.get("/websocket/stats")
        async def get_websocket_stats():
            if not self.websocket_server:
                raise HTTPException(status_code=503, detail="WebSocket server not available")
            
            return self.websocket_server.get_stats()
        
        # System metrics
        @self.app.get("/metrics")
        async def get_system_metrics():
            metrics = {
                "system": {
                    "uptime": time.time() - self.start_time,
                    "timestamp": time.time()
                }
            }
            
            if self.tick_engine:
                metrics["tick_engine"] = {
                    "running": getattr(self.tick_engine, 'running', False),
                    "tick_count": getattr(self.tick_engine, 'tick_count', 0),
                    "tick_rate": getattr(self.tick_engine, 'tick_rate', 0)
                }
            
            if self.websocket_server:
                metrics["websocket"] = self.websocket_server.get_stats()
            
            return metrics
        
        # Emergency endpoints
        @self.app.post("/emergency/stop")
        async def emergency_stop():
            """Emergency stop for the entire system"""
            try:
                if self.tick_engine:
                    await self.tick_engine.stop()
                
                return {"status": "success", "message": "Emergency stop executed"}
            except Exception as e:
                logger.error(f"Error during emergency stop: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/emergency/reset")
        async def emergency_reset():
            """Emergency reset of consciousness state"""
            try:
                if self.tick_engine and hasattr(self.tick_engine, 'consciousness_state'):
                    await self.tick_engine.consciousness_state.reset()
                
                return {"status": "success", "message": "Consciousness state reset"}
            except Exception as e:
                logger.error(f"Error during emergency reset: {e}")
                raise HTTPException(status_code=500, detail=str(e))
    
    def set_tick_engine(self, tick_engine):
        """Set reference to the tick engine"""
        self.tick_engine = tick_engine
        logger.info("Tick engine reference set for REST API")
    
    def set_websocket_server(self, websocket_server):
        """Set reference to the WebSocket server"""
        self.websocket_server = websocket_server
        logger.info("WebSocket server reference set for REST API")
    
    async def start_server(self):
        """Start the REST API server"""
        config = uvicorn.Config(
            self.app,
            host=self.host,
            port=self.port,
            log_level="info",
            access_log=True
        )
        
        server = uvicorn.Server(config)
        logger.info(f"REST API server starting on http://{self.host}:{self.port}")
        
        try:
            await server.serve()
        except Exception as e:
            logger.error(f"Failed to start REST API server: {e}")
            raise
    
    def get_app(self):
        """Get the FastAPI app instance"""
        return self.app 