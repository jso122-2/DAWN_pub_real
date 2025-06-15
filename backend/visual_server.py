import asyncio
import base64
import io
import json
import logging
import os
import subprocess
from typing import Dict, Optional, List

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from pydantic import BaseModel
from visual.visual_manager import VisualManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="DAWN Visual Process Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create visual manager instance
visual_manager = VisualManager()

# Load visual process modules
visual_manager.load_process_modules()

class ProcessRequest(BaseModel):
    name: str
    width: Optional[int] = 800
    height: Optional[int] = 600

class ProcessResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict] = None

@app.get("/")
async def root():
    return {"message": "DAWN Visual Process Server"}

@app.get("/processes", response_model=List[Dict])
async def list_processes():
    """Get list of all registered visual processes."""
    return visual_manager.list_processes()

@app.post("/processes", response_model=ProcessResponse)
async def create_process(request: ProcessRequest):
    """Create a new visual process instance."""
    try:
        process = visual_manager.create_process(
            request.name,
            width=request.width,
            height=request.height
        )
        if process:
            return ProcessResponse(
                success=True,
                message=f"Created process: {request.name}",
                data=process.get_metadata()
            )
        raise HTTPException(status_code=404, detail=f"Process class not found: {request.name}")
    except Exception as e:
        logger.error(f"Error creating process: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/processes/{name}", response_model=ProcessResponse)
async def get_process(name: str):
    """Get information about a specific process."""
    process = visual_manager.get_process(name)
    if process:
        return ProcessResponse(
            success=True,
            message=f"Found process: {name}",
            data=process.get_metadata()
        )
    raise HTTPException(status_code=404, detail=f"Process not found: {name}")

@app.post("/processes/{name}/start", response_model=ProcessResponse)
async def start_process(name: str):
    """Start a visual process."""
    if visual_manager.start_process(name):
        return ProcessResponse(
            success=True,
            message=f"Started process: {name}"
        )
    raise HTTPException(status_code=404, detail=f"Process not found: {name}")

@app.post("/processes/{name}/stop", response_model=ProcessResponse)
async def stop_process(name: str):
    """Stop a visual process."""
    if visual_manager.stop_process(name):
        return ProcessResponse(
            success=True,
            message=f"Stopped process: {name}"
        )
    raise HTTPException(status_code=404, detail=f"Process not found: {name}")

@app.get("/processes/{name}/frame")
async def capture_frame(name: str):
    """Capture a frame from a specific process."""
    frame = visual_manager.capture_frame(name)
    if frame:
        return {"frame": frame}
    raise HTTPException(status_code=404, detail=f"Process not found or inactive: {name}")

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                request = json.loads(data)
                if request.get("type") == "capture_frame":
                    process_name = request.get("process")
                    frame = visual_manager.capture_frame(process_name)
                    if frame:
                        await websocket.send_json({
                            "type": "frame",
                            "process": process_name,
                            "frame": frame
                        })
                    else:
                        await websocket.send_json({
                            "type": "error",
                            "message": f"Process not found or inactive: {process_name}"
                        })
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON"
                })
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Background task to update processes
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(update_processes())

async def update_processes():
    while True:
        visual_manager.update_all()
        await asyncio.sleep(1/30)  # 30 FPS update rate

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 