from fastapi import APIRouter, HTTPException, Depends, Response
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from datetime import datetime
import base64
import io

visualization_router = APIRouter()

# Import visualizers
from backend.visualizers import (
    ConsciousnessWaveVisualizer,
    EntropyThermalVisualizer,
    NeuralActivityVisualizer,
    AlignmentMatrixVisualizer,
    BloomPatternVisualizer,
    MoodGradientVisualizer
)

# Pydantic models
class VisualizationRequest(BaseModel):
    type: str
    format: str = "base64"  # base64 or raw
    width: int = 800
    height: int = 600
    params: Optional[Dict[str, Any]] = None

class VisualizationList(BaseModel):
    visualizations: List[str]
    descriptions: Dict[str, str]

# Initialize visualizers
visualizers = {
    "consciousness_wave": ConsciousnessWaveVisualizer(),
    "entropy_thermal": EntropyThermalVisualizer(),
    "neural_activity": NeuralActivityVisualizer(),
    "alignment_matrix": AlignmentMatrixVisualizer(),
    "bloom_pattern": BloomPatternVisualizer(),
    "mood_gradient": MoodGradientVisualizer()
}

# Dependency to get dawn_central
async def get_dawn_central():
    from backend.start_api_fixed import dawn_central
    if not dawn_central:
        raise HTTPException(status_code=503, detail="Consciousness engine not initialized")
    return dawn_central

@visualization_router.get("/available", response_model=VisualizationList)
async def get_available_visualizations():
    """Get list of available visualizations"""
    descriptions = {
        "consciousness_wave": "Real-time SCUP wave visualization",
        "entropy_thermal": "Entropy distribution heat map",
        "neural_activity": "Neural network activity matrix",
        "alignment_matrix": "System alignment coherence",
        "bloom_pattern": "Consciousness bloom patterns",
        "mood_gradient": "Mood state transitions"
    }
    
    return VisualizationList(
        visualizations=list(visualizers.keys()),
        descriptions=descriptions
    )

@visualization_router.post("/generate")
async def generate_visualization(
    request: VisualizationRequest,
    dawn_central=Depends(get_dawn_central)
):
    """Generate a specific visualization"""
    if request.type not in visualizers:
        raise HTTPException(status_code=404, detail=f"Visualization type {request.type} not found")
    
    try:
        # Get visualizer
        visualizer = visualizers[request.type]
        
        # Prepare data based on visualization type
        if request.type == "consciousness_wave":
            data = {
                "scup_history": dawn_central.get_scup_history(100),
                "current_tick": dawn_central.tick_engine.current_tick
            }
        elif request.type == "entropy_thermal":
            data = {
                "entropy_map": dawn_central.get_entropy_distribution(),
                "temperature": dawn_central.get_system_temperature()
            }
        elif request.type == "neural_activity":
            data = {
                "neural_matrix": dawn_central.get_neural_activity_matrix(),
                "activation_levels": dawn_central.get_activation_levels()
            }
        elif request.type == "alignment_matrix":
            data = {
                "alignment_data": dawn_central.get_alignment_matrix(),
                "coherence": dawn_central.get_coherence_score()
            }
        elif request.type == "bloom_pattern":
            data = {
                "bloom_state": dawn_central.get_bloom_pattern(),
                "growth_rate": dawn_central.get_growth_metrics()
            }
        else:  # mood_gradient
            data = {
                "mood_vector": dawn_central.get_mood_vector(),
                "mood_history": dawn_central.get_mood_history(50)
            }
        
        # Apply custom parameters
        if request.params:
            data.update(request.params)
        
        # Generate visualization
        image_data = visualizer.generate(data, size=(request.width, request.height))
        
        if request.format == "raw":
            # Return raw image bytes
            image_bytes = base64.b64decode(image_data.split(',')[1])
            return Response(content=image_bytes, media_type="image/png")
        else:
            # Return base64 encoded
            return {
                "type": request.type,
                "data": image_data,
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visualization generation failed: {str(e)}")

@visualization_router.get("/stream/{viz_type}")
async def stream_visualization(
    viz_type: str,
    dawn_central=Depends(get_dawn_central)
):
    """Get streaming endpoint information for visualization"""
    if viz_type not in visualizers:
        raise HTTPException(status_code=404, detail=f"Visualization type {viz_type} not found")
    
    return {
        "type": viz_type,
        "websocket_topic": f"viz_{viz_type}",
        "update_rate": visualizers[viz_type].update_interval,
        "description": f"Subscribe to 'viz_{viz_type}' topic via WebSocket for real-time updates"
    }

@visualization_router.post("/snapshot/{viz_type}")
async def capture_snapshot(
    viz_type: str,
    dawn_central=Depends(get_dawn_central)
):
    """Capture a snapshot of current visualization state"""
    if viz_type not in visualizers:
        raise HTTPException(status_code=404, detail=f"Visualization type {viz_type} not found")
    
    # Similar to generate but optimized for quick capture
    request = VisualizationRequest(type=viz_type)
    return await generate_visualization(request, dawn_central)

@visualization_router.get("/composite")
async def get_composite_visualization(
    types: List[str],
    dawn_central=Depends(get_dawn_central)
):
    """Generate multiple visualizations at once"""
    results = {}
    
    for viz_type in types:
        if viz_type in visualizers:
            try:
                request = VisualizationRequest(type=viz_type, width=400, height=300)
                result = await generate_visualization(request, dawn_central)
                results[viz_type] = result
            except Exception as e:
                results[viz_type] = {"error": str(e)}
    
    return {
        "visualizations": results,
        "timestamp": datetime.now().isoformat()
    } 