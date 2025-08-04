"""
Weave Router - Thread composition layer

This module handles routing of threads through spline function space,
enabling modular assemblage composition using KAN-based components.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
import logging
from datetime import datetime
import asyncio

from ...models import SplineNeuron, CachedGlyph, KANTopology


class WeaveRouter:
    """Routes threads through spline function space for assemblage composition"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.routing_cache = {}
        self.composition_history = []
        
    async def route_through_splines(self, 
                                  input_assemblage: Dict[str, Any],
                                  topology: KANTopology,
                                  routing_strategy: str = "adaptive") -> Dict[str, Any]:
        """Route an assemblage through spline space for modular composition"""
        
        route_start = datetime.now()
        
        try:
            # Convert assemblage to feature vector
            feature_vector = self._vectorize_assemblage(input_assemblage)
            
            # Select routing strategy
            if routing_strategy == "adaptive":
                spline_path = await self._adaptive_routing(feature_vector, topology)
            elif routing_strategy == "greedy":
                spline_path = await self._greedy_routing(feature_vector, topology)
            else:
                spline_path = await self._default_routing(feature_vector, topology)
            
            # Execute routing through selected splines
            composition_result = await self._compose_through_splines(
                feature_vector, spline_path, topology
            )
            
            # Build result
            result = {
                "input_assemblage": input_assemblage,
                "feature_vector": feature_vector.tolist(),
                "spline_path": spline_path,
                "composition_result": composition_result,
                "routing_strategy": routing_strategy,
                "execution_time": (datetime.now() - route_start).total_seconds(),
                "timestamp": datetime.now().isoformat()
            }
            
            # Update composition history
            self.composition_history.append(result)
            if len(self.composition_history) > 100:
                self.composition_history = self.composition_history[-50:]
            
            return result
            
        except Exception as e:
            self.logger.error(f"Routing failed: {e}")
            return {
                "error": str(e),
                "input_assemblage": input_assemblage,
                "routing_strategy": routing_strategy,
                "timestamp": datetime.now().isoformat()
            }
    
    def _vectorize_assemblage(self, assemblage: Dict[str, Any]) -> np.ndarray:
        """Convert assemblage to feature vector for spline processing"""
        
        # Extract key features from assemblage
        features = []
        
        # Semantic features
        if "semantics" in assemblage:
            semantics = assemblage["semantics"]
            if isinstance(semantics, dict):
                for key, value in semantics.items():
                    if isinstance(value, (int, float)):
                        features.append(float(value))
                    elif isinstance(value, str):
                        # Simple string hash to numeric
                        features.append(float(hash(value) % 1000) / 1000.0)
        
        # Ensure we have at least some features
        if len(features) < 10:
            # Pad with derived features
            base_hash = hash(str(assemblage)) % 10000
            for i in range(10 - len(features)):
                features.append(float((base_hash + i) % 1000) / 1000.0)
        
        # Normalize features
        feature_vector = np.array(features[:64])  # Cap at 64 features
        if len(feature_vector) < 64:
            # Pad to 64 dimensions
            padding = np.random.normal(0, 0.1, 64 - len(feature_vector))
            feature_vector = np.concatenate([feature_vector, padding])
        
        # Normalize to unit vector
        norm = np.linalg.norm(feature_vector)
        if norm > 0:
            feature_vector = feature_vector / norm
        
        return feature_vector
    
    async def _adaptive_routing(self, feature_vector: np.ndarray, 
                              topology: KANTopology) -> List[str]:
        """Adaptive routing based on spline activations"""
        
        spline_path = []
        
        # Find best splines for current vector
        for spline_id, neuron in topology.spline_neurons.items():
            activation = await self._compute_spline_activation(neuron, feature_vector)
            if activation > neuron.activation_threshold:
                spline_path.append(spline_id)
        
        return spline_path[:3]  # Return top 3
    
    async def _greedy_routing(self, feature_vector: np.ndarray, 
                            topology: KANTopology) -> List[str]:
        """Greedy routing - select highest activation splines"""
        
        spline_activations = []
        
        for spline_id, neuron in topology.spline_neurons.items():
            activation = await self._compute_spline_activation(neuron, feature_vector)
            if activation > neuron.activation_threshold:
                spline_activations.append((spline_id, activation))
        
        # Sort by activation strength
        spline_activations.sort(key=lambda x: x[1], reverse=True)
        
        # Return top activations (max 3)
        return [spline_id for spline_id, _ in spline_activations[:3]]
    
    async def _default_routing(self, feature_vector: np.ndarray, 
                             topology: KANTopology) -> List[str]:
        """Default routing - simple activation-based selection"""
        
        activated_splines = []
        
        for spline_id, neuron in topology.spline_neurons.items():
            activation = await self._compute_spline_activation(neuron, feature_vector)
            if activation > neuron.activation_threshold:
                activated_splines.append(spline_id)
        
        return activated_splines[:3]  # Return first 3
    
    async def _compute_spline_activation(self, neuron: SplineNeuron, 
                                       feature_vector: np.ndarray) -> float:
        """Compute activation strength of a spline neuron for given input"""
        
        try:
            # Compute spline output
            spline_output = neuron.compute(feature_vector)
            
            # Activation based on output magnitude and confidence
            if hasattr(spline_output.glyph_data, '__len__'):
                output_magnitude = np.linalg.norm(spline_output.glyph_data)
            else:
                output_magnitude = abs(float(spline_output.glyph_data))
            
            confidence = spline_output.confidence
            
            # Factor in entropy (lower entropy = higher activation)
            entropy_factor = 1.0 - neuron.entropy_level
            
            # Combine factors
            activation = output_magnitude * confidence * entropy_factor
            
            return float(activation)
            
        except Exception as e:
            self.logger.warning(f"Failed to compute activation for {neuron.assemblage_id}: {e}")
            return 0.0
    
    async def _compose_through_splines(self, feature_vector: np.ndarray,
                                     spline_path: List[str],
                                     topology: KANTopology) -> Dict[str, Any]:
        """Execute composition through selected spline path"""
        
        composition_result = {
            "spline_outputs": {},
            "confidence_scores": {},
            "execution_steps": []
        }
        
        for step_idx, spline_id in enumerate(spline_path):
            
            if spline_id not in topology.spline_neurons:
                continue
            
            neuron = topology.spline_neurons[spline_id]
            
            try:
                # Compute spline output
                spline_output = neuron.compute(feature_vector)
                
                # Record output
                composition_result["spline_outputs"][spline_id] = {
                    "confidence": spline_output.confidence,
                    "step": step_idx
                }
                
                composition_result["confidence_scores"][spline_id] = spline_output.confidence
                
                # Record execution step
                step_info = {
                    "step": step_idx,
                    "spline_id": spline_id,
                    "output_confidence": spline_output.confidence,
                    "neuron_entropy": neuron.entropy_level
                }
                composition_result["execution_steps"].append(step_info)
                
                # Update neuron access
                neuron.access_count += 1
                neuron.last_accessed = datetime.now()
                
            except Exception as e:
                self.logger.warning(f"Spline {spline_id} execution failed: {e}")
                continue
        
        return composition_result
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get statistics about routing performance"""
        
        stats = {
            "total_compositions": len(self.composition_history),
            "timestamp": datetime.now().isoformat()
        }
        
        if self.composition_history:
            # Success rate
            successful = [comp for comp in self.composition_history if "error" not in comp]
            stats["success_rate"] = len(successful) / len(self.composition_history)
        
        return stats 