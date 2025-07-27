from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

consciousness_router = APIRouter()

# Pydantic models
class ConsciousnessState(BaseModel):
    tick: int
    scup: float = Field(..., ge=0, le=100)
    entropy: float = Field(..., ge=0, le=1)
    mood: str
    state: str
    timestamp: datetime

class ConsciousnessUpdate(BaseModel):
    entropy: Optional[float] = Field(None, ge=0, le=1)
    mood: Optional[str] = None
    process_activation: Optional[Dict[str, bool]] = None

class ConsciousnessMetrics(BaseModel):
    neural_activity: float
    quantum_coherence: float
    pattern_recognition: float
    memory_utilization: float
    chaos_factor: float

# Dependency to get dawn_central
async def get_dawn_central():
    from backend.start_api_fixed import dawn_central
    if not dawn_central:
        raise HTTPException(status_code=503, detail="Consciousness engine not initialized")
    return dawn_central

@consciousness_router.get("/state", response_model=ConsciousnessState)
async def get_consciousness_state(dawn_central=Depends(get_dawn_central)):
    """Get current consciousness state"""
    return ConsciousnessState(
        tick=dawn_central.tick_engine.current_tick,
        scup=dawn_central.get_scup(),
        entropy=dawn_central.get_entropy(),
        mood=dawn_central.get_mood(),
        state=dawn_central.get_state(),
        timestamp=datetime.now()
    )

@consciousness_router.post("/update")
async def update_consciousness(
    update: ConsciousnessUpdate,
    dawn_central=Depends(get_dawn_central)
):
    """Update consciousness parameters"""
    if update.entropy is not None:
        dawn_central.set_entropy(update.entropy)
    
    if update.mood:
        dawn_central.set_mood(update.mood)
    
    if update.process_activation:
        for process, active in update.process_activation.items():
            if active:
                dawn_central.activate_process(process)
            else:
                dawn_central.deactivate_process(process)
    
    return {"status": "updated", "timestamp": datetime.now()}

@consciousness_router.get("/metrics", response_model=ConsciousnessMetrics)
async def get_consciousness_metrics(dawn_central=Depends(get_dawn_central)):
    """Get detailed consciousness metrics"""
    metrics = dawn_central.get_consciousness_metrics()
    return ConsciousnessMetrics(**metrics)

@consciousness_router.get("/history")
async def get_consciousness_history(
    duration: int = 100,
    dawn_central=Depends(get_dawn_central)
):
    """Get consciousness state history"""
    history = dawn_central.get_history(duration)
    return {
        "duration": duration,
        "history": history,
        "timestamp": datetime.now()
    }

@consciousness_router.post("/reset")
async def reset_consciousness(dawn_central=Depends(get_dawn_central)):
    """Reset consciousness to initial state"""
    dawn_central.reset()
    return {"status": "reset", "timestamp": datetime.now()}

@consciousness_router.get("/processes")
async def get_active_processes(dawn_central=Depends(get_dawn_central)):
    """Get list of active processes"""
    return {
        "active": dawn_central.get_active_processes(),
        "available": dawn_central.get_available_processes(),
        "timestamp": datetime.now()
    }

@consciousness_router.post("/process/{process_name}/{action}")
async def control_process(
    process_name: str,
    action: str,
    dawn_central=Depends(get_dawn_central)
):
    """Control process execution (start/stop/restart)"""
    if action not in ["start", "stop", "restart"]:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    if action == "start":
        success = dawn_central.activate_process(process_name)
    elif action == "stop":
        success = dawn_central.deactivate_process(process_name)
    else:  # restart
        dawn_central.deactivate_process(process_name)
        success = dawn_central.activate_process(process_name)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"Process {process_name} not found")
    
    return {
        "process": process_name,
        "action": action,
        "status": "success",
        "timestamp": datetime.now()
    } 