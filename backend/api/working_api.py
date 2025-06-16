from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from typing import List

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active connections
active_connections: List[WebSocket] = []

@app.get("/")
async def root():
    return {"message": "DAWN API is running!"}

@app.get("/processes/status")
async def get_processes_status():
    return {
        "processes": [
            {"name": "activation_histogram", "status": "available", "description": "Neural activation patterns"},
            {"name": "memory_stream", "status": "available", "description": "Memory formation visualizer"},
            {"name": "entropy_cascade", "status": "available", "description": "Chaos dynamics monitor"},
        ]
    }

@app.post("/processes/{process_name}/start")
async def start_process(process_name: str):
    return {"status": "started", "process": process_name}

@app.post("/processes/{process_name}/stop")
async def stop_process(process_name: str):
    return {"status": "stopped", "process": process_name}

@app.get("/tick-snapshot/{process_name}")
async def get_tick_snapshot(process_name: str):
    return {"process": process_name, "tick": 42, "data": {"value": 0.75}}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        # Keep connection alive and send tick data
        while True:
            # Just echo for now
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)

# Background task to broadcast tick data
async def broadcast_ticks():
    tick = 0
    while True:
        tick += 1
        message = json.dumps({
            "type": "tick",
            "tick_number": tick,
            "scup": 75 + (tick % 25),
            "entropy": 0.3 + (0.2 * (tick % 10) / 10),
            "mood": ["calm", "focused", "energetic", "chaotic"][tick % 4]
        })
        
        # Send to all connected clients
        disconnected = []
        for connection in active_connections:
            try:
                await connection.send_text(message)
            except:
                disconnected.append(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            if conn in active_connections:
                active_connections.remove(conn)
        
        await asyncio.sleep(1)

@app.on_event("startup")
async def startup():
    asyncio.create_task(broadcast_ticks())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)