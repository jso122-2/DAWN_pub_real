from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
import time
from typing import List
from datetime import datetime
import logging
import sys

# Configure logging to see what's happening
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

print("Starting DAWN API...")

# Create FastAPI app
app = FastAPI(title="DAWN API", version="1.0.0")

# CRITICAL: Add CORS middleware BEFORE any routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("CORS middleware added")

# Store active connections
active_connections: List[WebSocket] = []

# Global tick state
current_tick = 0

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "DAWN API Running", "time": datetime.now().isoformat()}

# Forecasting endpoints
@app.get("/forecasting/status")
async def get_forecasting_status():
    """Get the status of the forecasting system"""
    logger.info("Forecasting status endpoint called")
    try:
        # Try to get DAWN consciousness instance
        from core.consciousness_core import consciousness_core
        
        if hasattr(consciousness_core, 'forecasting_processor') and consciousness_core.forecasting_processor:
            metrics = consciousness_core.forecasting_processor.get_metrics()
            return {
                "status": "active",
                "metrics": metrics,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "inactive",
                "message": "Forecasting processor not initialized",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"Error getting forecasting status: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/forecasting/current")
async def get_current_forecasts():
    """Get current behavioral forecasts"""
    logger.info("Current forecasts endpoint called")
    try:
        from core.consciousness_core import consciousness_core
        
        if hasattr(consciousness_core, 'get_current_forecasts'):
            forecasts = consciousness_core.get_current_forecasts()
            return forecasts
        else:
            return {
                "recent_forecasts": [],
                "metrics": {},
                "message": "Forecasting not available",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"Error getting current forecasts: {e}")
        return {
            "recent_forecasts": [],
            "metrics": {},
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/forecasting/direction/{direction}")
async def get_forecast_for_direction(direction: str):
    """Get forecast for a specific passion direction"""
    logger.info(f"Forecast for direction '{direction}' endpoint called")
    try:
        from core.consciousness_core import consciousness_core
        
        if hasattr(consciousness_core, 'get_forecast_for_direction'):
            forecast = consciousness_core.get_forecast_for_direction(direction)
            if forecast:
                return {
                    "direction": direction,
                    "forecast": forecast,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "direction": direction,
                    "forecast": None,
                    "message": f"No forecast available for direction '{direction}'",
                    "timestamp": datetime.now().isoformat()
                }
        else:
            return {
                "direction": direction,
                "forecast": None,
                "error": "Forecasting not available",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"Error getting forecast for direction '{direction}': {e}")
        return {
            "direction": direction,
            "forecast": None,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.post("/forecasting/generate/{direction}")
async def generate_instant_forecast(direction: str):
    """Generate an instant forecast for a specific direction"""
    logger.info(f"Generate instant forecast for '{direction}' endpoint called")
    try:
        from core.consciousness_core import consciousness_core
        
        if hasattr(consciousness_core, 'generate_instant_forecast'):
            forecast = await consciousness_core.generate_instant_forecast(direction)
            if forecast:
                return {
                    "direction": direction,
                    "forecast": forecast,
                    "generated_at": datetime.now().isoformat()
                }
            else:
                return {
                    "direction": direction,
                    "forecast": None,
                    "message": f"Could not generate forecast for direction '{direction}'",
                    "generated_at": datetime.now().isoformat()
                }
        else:
            return {
                "direction": direction,
                "forecast": None,
                "error": "Forecasting not available",
                "generated_at": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"Error generating instant forecast for '{direction}': {e}")
        return {
            "direction": direction,
            "forecast": None,
            "error": str(e),
            "generated_at": datetime.now().isoformat()
        }

@app.get("/forecasting/trends/{direction}")
async def get_forecast_trends(direction: str, hours: int = 24):
    """Get forecast trends for a direction over time"""
    logger.info(f"Forecast trends for '{direction}' over {hours} hours endpoint called")
    try:
        from core.consciousness_core import consciousness_core
        
        if hasattr(consciousness_core, 'get_forecast_trends'):
            trends = consciousness_core.get_forecast_trends(direction, hours)
            return {
                "direction": direction,
                "lookback_hours": hours,
                "trends": trends,
                "count": len(trends),
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "direction": direction,
                "lookback_hours": hours,
                "trends": [],
                "count": 0,
                "error": "Forecasting not available",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"Error getting forecast trends for '{direction}': {e}")
        return {
            "direction": direction,
            "lookback_hours": hours,
            "trends": [],
            "count": 0,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/processes/status")
async def get_processes_status():
    logger.info("Process status endpoint called")
    return {
        "processes": [
            {"name": "activation_histogram", "status": "available", "description": "Neural activation patterns"},
            {"name": "memory_stream", "status": "available", "description": "Memory formation visualizer"},
            {"name": "entropy_cascade", "status": "available", "description": "Chaos dynamics monitor"}
        ]
    }

@app.post("/processes/{process_name}/start")
async def start_process(process_name: str):
    logger.info(f"Starting process: {process_name}")
    return {"status": "started", "process": process_name}

@app.post("/processes/{process_name}/stop")
async def stop_process(process_name: str):
    logger.info(f"Stopping process: {process_name}")
    return {"status": "stopped", "process": process_name}

@app.get("/tick-snapshot/{process_name}")
async def get_tick_snapshot(process_name: str):
    return {"process": process_name, "tick": current_tick, "data": {"value": 0.75}}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logger.info("WebSocket connection attempt")
    await websocket.accept()
    active_connections.append(websocket)
    logger.info(f"WebSocket connected. Total: {len(active_connections)}")
    
    try:
        # Send initial message
        await websocket.send_text(json.dumps({
            "type": "connection",
            "message": "Connected to DAWN",
            "timestamp": time.time()
        }))
        
        # Keep connection alive
        while True:
            try:
                # Wait for messages with timeout
                data = await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
                logger.info(f"Received: {data}")
                await websocket.send_text(f"Echo: {data}")
            except asyncio.TimeoutError:
                # Send tick data
                await websocket.send_text(json.dumps({
                    "type": "tick",
                    "tick_number": current_tick,
                    "scup": 75 + (current_tick % 25),
                    "entropy": 0.5,
                    "mood": "calm"
                }))
                
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        if websocket in active_connections:
            active_connections.remove(websocket)

async def tick_counter():
    """Background task to increment tick"""
    global current_tick
    while True:
        current_tick += 1
        await asyncio.sleep(1)

@app.on_event("startup")
async def startup():
    logger.info("Starting background tasks...")
    asyncio.create_task(tick_counter())

if __name__ == "__main__":
    print(f"Python version: {sys.version}")
    print("Starting server on http://0.0.0.0:8000")
    
    try:
        import uvicorn
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8000,
            log_level="info"
        )
    except ImportError:
        print("ERROR: uvicorn not installed!")
        print("Run: pip install uvicorn fastapi")
    except Exception as e:
        print(f"ERROR starting server: {e}")