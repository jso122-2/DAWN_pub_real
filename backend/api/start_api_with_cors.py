from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from datetime import datetime
from typing import List

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Connection might be closed
                pass

manager = ConnectionManager()

# Process status endpoint
@app.get("/processes/status")
async def get_processes_status():
    return {
        "processes": [
            {"name": "activation_histogram", "status": "available", "description": "Neural activation patterns"},
            {"name": "memory_stream", "status": "available", "description": "Memory formation visualizer"},
            {"name": "entropy_cascade", "status": "available", "description": "Chaos dynamics monitor"},
            {"name": "consciousness_map", "status": "available", "description": "Consciousness state mapper"},
            {"name": "quantum_flux", "status": "available", "description": "Quantum coherence analyzer"}
        ]
    }

# Start process endpoint
@app.post("/processes/{process_name}/start")
async def start_process(process_name: str):
    return {"status": "started", "process": process_name, "timestamp": datetime.now().isoformat()}

# Stop process endpoint  
@app.post("/processes/{process_name}/stop")
async def stop_process(process_name: str):
    return {"status": "stopped", "process": process_name, "timestamp": datetime.now().isoformat()}

# Get tick snapshot
@app.get("/tick-snapshot/{process_name}")
async def get_tick_snapshot(process_name: str):
    return {
        "process": process_name,
        "tick": 42,
        "data": {"value": 0.75, "timestamp": datetime.now().isoformat()}
    }

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Echo: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Background task to send tick data
async def broadcast_tick_data():
    tick = 0
    while True:
        tick += 1
        tick_data = {
            "type": "tick",
            "tick_number": tick,
            "scup": 75 + (tick % 25),  # Oscillating SCUP
            "entropy": 0.3 + (0.2 * (tick % 10) / 10),
            "mood": ["calm", "focused", "energetic", "chaotic"][tick % 4],
            "timestamp": datetime.now().isoformat()
        }
        
        # Broadcast to all connected clients
        await manager.broadcast(json.dumps(tick_data))
        
        await asyncio.sleep(1)  # Send tick every second

# Start the broadcast task when app starts
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(broadcast_tick_data())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)