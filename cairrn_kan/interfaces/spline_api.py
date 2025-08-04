"""
Spline API - REST interface for KAN-Cairrn operations

This module provides HTTP endpoints for interacting with the KAN-Cairrn system,
including spline neuron operations and cursor navigation.
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import numpy as np
import logging
from datetime import datetime
import asyncio
import json
import sys
import os

# Add parent directory to path for imports
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ...models import CursorState, NavigationResult, KANTopology, CachedGlyph
    from core.spline_neurons import SplineNeuronManager
    from ..cursor.function_navigator import FunctionNavigator
    from ..cursor.interpretability import SplineInterpreter
    from ..adapters.claude_kan import ClaudeKANAdapter
except ImportError as e:
    print(f"Import error: {e}")
    # Create placeholder classes for development
    class SplineNeuronManager: pass
    class FunctionNavigator: pass
    class SplineInterpreter: pass
    class ClaudeKANAdapter: pass


# Pydantic models for API
class SplineComputeRequest(BaseModel):
    feature_vector: List[float] = Field(..., description="Input feature vector")
    normalize: bool = Field(True, description="Whether to normalize input")

class SplineComputeResponse(BaseModel):
    glyph_type: str
    confidence: float
    entropy_level: float
    interpretable_explanation: str
    activation_pattern: Dict[str, float]
    computation_time: float

class NavigationRequest(BaseModel):
    target_semantics: Dict[str, float] = Field(..., description="Target semantic coordinates")
    max_steps: int = Field(20, description="Maximum navigation steps")
    exploration_weight: float = Field(0.3, description="Exploration vs exploitation balance")

class NavigationResponse(BaseModel):
    navigation_success: bool
    total_steps: int
    final_confidence: float
    execution_time: float
    interpretation_summary: str
    path_length: int

class NeuronTuneRequest(BaseModel):
    learning_rate: float = Field(0.001, description="Learning rate for parameter updates")
    target_entropy: float = Field(0.5, description="Target entropy level")
    gradient_data: Optional[List[float]] = Field(None, description="Gradient for manual update")

class VisualizationData(BaseModel):
    timestamp: str
    spline_activations: Dict[str, float]
    global_entropy: float
    total_neurons: int
    active_neurons: int
    interpretation: str
    activity_level: str
    network_health: Dict[str, Any]


class SplineAPI:
    """Main API class for KAN-Cairrn operations"""
    
    def __init__(self):
        self.app = FastAPI(
            title="KAN-Cairrn Spline API",
            description="REST API for interpretable function space navigation",
            version="1.0.0"
        )
        
        # Initialize components
        self.neuron_manager = SplineNeuronManager()
        self.topology = None  # Will be injected
        self.navigator = None  # Will be injected
        self.interpreter = SplineInterpreter()
        self.claude_adapter = None  # Will be injected
        
        self.logger = logging.getLogger(__name__)
        
        # Setup routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup all API routes"""
        
        # Spline neuron operations
        @self.app.get("/kan/neurons", response_model=List[str])
        async def list_neurons():
            """List all spline neurons"""
            return list(self.neuron_manager.neurons.keys())
        
        @self.app.get("/kan/neurons/{neuron_id}")
        async def get_neuron_details(neuron_id: str):
            """Get specific neuron details"""
            neuron = self.neuron_manager.get_neuron(neuron_id)
            if not neuron:
                raise HTTPException(status_code=404, detail="Neuron not found")
            
            return self.interpreter.generate_spline_report(neuron)
        
        @self.app.post("/kan/neurons/{neuron_id}/compute", response_model=SplineComputeResponse)
        async def compute_spline_output(neuron_id: str, request: SplineComputeRequest):
            """Compute spline output for input"""
            start_time = datetime.now()
            
            try:
                feature_vector = np.array(request.feature_vector)
                
                if request.normalize and len(feature_vector) > 0:
                    # Simple normalization
                    feature_vector = (feature_vector - np.mean(feature_vector)) / (np.std(feature_vector) + 1e-8)
                
                # Activate neuron
                glyph = self.neuron_manager.activate_neuron(neuron_id, feature_vector)
                
                if not glyph:
                    raise HTTPException(status_code=400, detail="Neuron activation failed")
                
                computation_time = (datetime.now() - start_time).total_seconds()
                
                return SplineComputeResponse(
                    glyph_type=glyph.glyph_type,
                    confidence=glyph.confidence,
                    entropy_level=glyph.entropy_level,
                    interpretable_explanation=glyph.interpretable_explanation,
                    activation_pattern=glyph.activation_pattern,
                    computation_time=computation_time
                )
                
            except Exception as e:
                self.logger.error(f"Compute failed for neuron {neuron_id}: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.put("/kan/neurons/{neuron_id}/tune")
        async def tune_neuron_parameters(neuron_id: str, request: NeuronTuneRequest):
            """Update spline parameters"""
            neuron = self.neuron_manager.get_neuron(neuron_id)
            if not neuron:
                raise HTTPException(status_code=404, detail="Neuron not found")
            
            try:
                # Update learning rate
                neuron.learning_rate = request.learning_rate
                
                # Update target entropy
                if request.target_entropy != neuron.entropy_level:
                    # Gradual entropy adjustment
                    alpha = 0.1
                    neuron.entropy_level = (alpha * request.target_entropy + 
                                          (1 - alpha) * neuron.entropy_level)
                
                # Apply gradient if provided
                if request.gradient_data:
                    gradient = np.array(request.gradient_data)
                    neuron.spline_function.update_parameters(gradient, request.learning_rate)
                
                return {"status": "success", "message": f"Tuned neuron {neuron_id}"}
                
            except Exception as e:
                self.logger.error(f"Tuning failed for neuron {neuron_id}: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/kan/neurons/{neuron_id}/interpretation")
        async def get_neuron_interpretation(neuron_id: str):
            """Human-readable spline explanation"""
            neuron = self.neuron_manager.get_neuron(neuron_id)
            if not neuron:
                raise HTTPException(status_code=404, detail="Neuron not found")
            
            report = self.interpreter.generate_spline_report(neuron)
            return report
        
        # Cursor navigation in function space
        @self.app.post("/cursor/navigate-splines", response_model=NavigationResponse)
        async def navigate_through_splines(request: NavigationRequest):
            """Navigate through spline space"""
            if not self.navigator:
                raise HTTPException(status_code=503, detail="Navigator not initialized")
            
            try:
                result = await self.navigator.navigate_to_function(request.target_semantics)
                
                return NavigationResponse(
                    navigation_success=result.navigation_success,
                    total_steps=len(result.steps),
                    final_confidence=result.total_confidence,
                    execution_time=result.execution_time,
                    interpretation_summary=result.interpretation_summary,
                    path_length=result.path_length
                )
                
            except Exception as e:
                self.logger.error(f"Navigation failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/cursor/function-position")
        async def get_cursor_position():
            """Current position in function space"""
            if not self.navigator:
                raise HTTPException(status_code=503, detail="Navigator not initialized")
            
            cursor_state = await self.navigator.get_cursor_state()
            
            return {
                "active_splines": cursor_state.active_splines,
                "current_feature_vector": cursor_state.current_feature_vector.tolist(),
                "confidence_scores": cursor_state.confidence_scores,
                "session_id": cursor_state.session_id,
                "last_updated": cursor_state.last_updated.isoformat()
            }
        
        @self.app.get("/cursor/spline-activations")
        async def get_spline_activations():
            """Currently active spline neurons"""
            if not self.topology:
                raise HTTPException(status_code=503, detail="Topology not initialized")
            
            activation_map = self.topology.get_activation_snapshot()
            global_state = self.interpreter.explain_global_state(activation_map)
            
            return {
                "activations": activation_map,
                "global_interpretation": global_state,
                "timestamp": datetime.now().isoformat()
            }
        
        @self.app.post("/cursor/interpret-position")
        async def interpret_cursor_position():
            """Get human explanation of cursor state"""
            if not self.navigator:
                raise HTTPException(status_code=503, detail="Navigator not initialized")
            
            cursor_state = await self.navigator.get_cursor_state()
            active_functions = self.topology.get_active_splines(cursor_state.active_splines)
            
            interpretations = self.interpreter.explain_spline_activations(
                active_functions, cursor_state.current_feature_vector
            )
            
            momentum_explanation = self.interpreter.explain_momentum(
                cursor_state.navigation_trajectory.semantic_momentum
            )
            
            return {
                "spline_interpretations": interpretations,
                "momentum_explanation": momentum_explanation,
                "navigation_stats": self.navigator.get_navigation_stats()
            }
        
        # KAN topology operations
        @self.app.get("/kan/topology")
        async def get_kan_topology():
            """Network structure and connections"""
            if not self.topology:
                raise HTTPException(status_code=503, detail="Topology not initialized")
            
            return {
                "total_neurons": len(self.topology.spline_neurons),
                "global_entropy": self.topology.global_entropy,
                "entropy_threshold": self.topology.entropy_threshold,
                "last_updated": self.topology.last_updated.isoformat(),
                "neuron_ids": list(self.topology.spline_neurons.keys()),
                "connection_count": self.topology.connection_graph.number_of_edges() if self.topology.connection_graph else 0
            }
        
        @self.app.get("/kan/entropy")
        async def get_entropy_levels():
            """Global and per-neuron entropy levels"""
            if not self.topology:
                raise HTTPException(status_code=503, detail="Topology not initialized")
            
            neuron_entropies = {
                neuron_id: neuron.entropy_level
                for neuron_id, neuron in self.topology.spline_neurons.items()
            }
            
            return {
                "global_entropy": self.topology.global_entropy,
                "neuron_entropies": neuron_entropies,
                "entropy_stats": {
                    "mean": np.mean(list(neuron_entropies.values())) if neuron_entropies else 0,
                    "std": np.std(list(neuron_entropies.values())) if neuron_entropies else 0,
                    "min": min(neuron_entropies.values()) if neuron_entropies else 0,
                    "max": max(neuron_entropies.values()) if neuron_entropies else 0
                }
            }
        
        @self.app.post("/kan/optimize")
        async def trigger_entropy_optimization(background_tasks: BackgroundTasks):
            """Trigger entropy-based optimization"""
            
            async def optimize_task():
                try:
                    # Prune high-entropy neurons
                    pruned = self.neuron_manager.prune_neurons(
                        entropy_threshold=0.8,
                        access_threshold=5
                    )
                    
                    # Update global entropy
                    self.topology.update_global_entropy()
                    
                    self.logger.info(f"Optimization completed. Pruned {len(pruned)} neurons.")
                    
                except Exception as e:
                    self.logger.error(f"Optimization failed: {e}")
            
            background_tasks.add_task(optimize_task)
            
            return {"status": "optimization_started", "message": "Entropy optimization running in background"}
        
        @self.app.get("/kan/visualization", response_model=VisualizationData)
        async def get_visualization_data():
            """Network topology for visualization"""
            if not self.claude_adapter:
                raise HTTPException(status_code=503, detail="Claude adapter not initialized")
            
            viz_data = self.claude_adapter.get_kan_visualization_data()
            
            return VisualizationData(**viz_data)
        
        # Weaving integration
        @self.app.post("/weave/kan-guided") 
        async def execute_kan_guided_weaving(request: Dict[str, Any]):
            """Execute KAN-guided weaving"""
            # This would integrate with the weaving system
            return {"status": "not_implemented", "message": "KAN-guided weaving not yet implemented"}
        
        @self.app.get("/weave/spline-components")
        async def get_spline_components():
            """Available spline-based components"""
            components = []
            
            for neuron_id, neuron in self.neuron_manager.neurons.items():
                components.append({
                    "id": neuron_id,
                    "features": neuron.input_features,
                    "entropy": neuron.entropy_level,
                    "access_count": neuron.access_count,
                    "last_used": neuron.last_accessed.isoformat()
                })
            
            return {"components": components, "total": len(components)}
        
        @self.app.post("/weave/interpret-result")
        async def interpret_weaving_result(result_data: Dict[str, Any]):
            """Explain weaving result in terms of splines"""
            # This would analyze weaving results through spline interpretations
            return {"status": "not_implemented", "message": "Weaving interpretation not yet implemented"}
        
        # Health and status endpoints
        @self.app.get("/health")
        async def health_check():
            """API health check"""
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "components": {
                    "neuron_manager": bool(self.neuron_manager),
                    "topology": bool(self.topology),
                    "navigator": bool(self.navigator),
                    "interpreter": bool(self.interpreter),
                    "claude_adapter": bool(self.claude_adapter)
                }
            }
        
        @self.app.get("/stats")
        async def get_system_stats():
            """System statistics"""
            stats = self.neuron_manager.get_neuron_stats()
            
            if self.navigator:
                nav_stats = self.navigator.get_navigation_stats()
                stats.update(nav_stats)
            
            return stats
    
    def set_components(self, topology: 'KANTopology', navigator: 'FunctionNavigator', 
                      claude_adapter: 'ClaudeKANAdapter'):
        """Inject system components"""
        self.topology = topology
        self.navigator = navigator
        self.claude_adapter = claude_adapter
        
        # Update navigator reference in neuron_manager if needed
        if hasattr(self.neuron_manager, 'set_topology'):
            self.neuron_manager.set_topology(topology)


# Create global API instance
spline_api = SplineAPI()
app = spline_api.app


class SplineAPIServer:
    """Server wrapper for the Spline API"""
    
    def __init__(self, kan_topology=None, function_navigator=None, spline_interpreter=None):
        self.api = spline_api
        
        # Set components if provided
        if kan_topology and function_navigator:
            self.api.set_components(kan_topology, function_navigator, None)
    
    def get_app(self):
        """Get the FastAPI app instance"""
        return self.api.app
    
    def set_components(self, kan_topology, function_navigator, claude_adapter=None):
        """Set system components"""
        self.api.set_components(kan_topology, function_navigator, claude_adapter)


# Export the main app for deployment
__all__ = ['app', 'spline_api', 'SplineAPIServer'] 