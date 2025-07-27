from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio

app = FastAPI()

# Enable CORS - this is critical!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store WebSocket connections
connections = []

@app.get("/")
async def root():
    return {"message": "DAWN API Running"}

@app.get("/processes/status")
async def get_processes_status():
    return {
        "processes": [
            {"name": "activation_histogram", "status": "available", "description": "Neural activation patterns"},
            {"name": "memory_stream", "status": "available", "description": "Memory formation visualizer"}
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
    connections.append(websocket)
    
    try:
        # Send tick data every second
        tick = 0
        while True:
            tick += 1
            message = {
                "type": "tick",
                "tick_number": tick,
                "scup": 75,
                "entropy": 0.5,
                "mood": "calm"
            }
            await websocket.send_text(json.dumps(message))
            await asyncio.sleep(1)
    except:
        connections.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)