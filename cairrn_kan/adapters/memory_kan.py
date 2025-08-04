"""
Memory KAN Adapter

Adapter for KAN-based memory consolidation and retrieval operations.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime, timedelta
import asyncio

from ...models import KANTopology, SplineNeuron, CachedGlyph


class MemoryKANAdapter:
    """Adapter for KAN-based memory operations"""
    
    def __init__(self, kan_topology: KANTopology):
        self.kan_topology = kan_topology
        self.logger = logging.getLogger(__name__)
        
        # Memory state
        self.memory_traces = {}
        self.consolidation_history = []
        
    async def consolidate_memory(self, 
                               memory_data: Dict[str, Any],
                               consolidation_strategy: str = "entropy_based") -> Dict[str, Any]:
        """Consolidate memory data using KAN splines"""
        
        consolidation_start = datetime.now()
        trace_id = f"trace_{int(consolidation_start.timestamp())}"
        
        try:
            # Convert memory data to feature representation
            feature_vector = self._encode_memory_features(memory_data)
            
            # Select splines for consolidation
            selected_splines = await self._select_consolidation_splines(
                feature_vector, consolidation_strategy
            )
            
            # Execute consolidation through selected splines
            consolidation_result = await self._execute_consolidation(
                feature_vector, selected_splines, memory_data
            )
            
            # Create memory trace
            memory_trace = {
                "trace_id": trace_id,
                "original_memory": memory_data,
                "feature_vector": feature_vector.tolist(),
                "selected_splines": selected_splines,
                "consolidation_result": consolidation_result,
                "strategy": consolidation_strategy,
                "created_at": consolidation_start.isoformat(),
                "access_count": 0
            }
            
            # Store memory trace
            self.memory_traces[trace_id] = memory_trace
            
            # Add to consolidation history
            self.consolidation_history.append({
                "trace_id": trace_id,
                "timestamp": consolidation_start.isoformat(),
                "strategy": consolidation_strategy,
                "splines_used": len(selected_splines)
            })
            
            return {
                "trace_id": trace_id,
                "consolidation_success": "error" not in consolidation_result,
                "splines_used": selected_splines,
                "consolidation_result": consolidation_result,
                "execution_time": (datetime.now() - consolidation_start).total_seconds()
            }
            
        except Exception as e:
            self.logger.error(f"Memory consolidation failed: {e}")
            return {
                "trace_id": trace_id,
                "error": str(e),
                "consolidation_success": False,
                "timestamp": datetime.now().isoformat()
            }
    
    def _encode_memory_features(self, memory_data: Dict[str, Any]) -> np.ndarray:
        """Encode memory data as feature vector"""
        
        features = []
        
        # Extract numerical features
        for key, value in memory_data.items():
            if isinstance(value, (int, float)):
                features.append(float(value))
            elif isinstance(value, str):
                # Simple string encoding
                features.append(float(hash(value) % 1000) / 1000.0)
        
        # Ensure minimum feature count
        while len(features) < 32:
            # Pad with derived features
            base_hash = hash(str(memory_data)) % 10000
            features.append(float((base_hash + len(features)) % 1000) / 1000.0)
        
        # Limit and normalize
        feature_vector = np.array(features[:64])
        
        # Normalize
        norm = np.linalg.norm(feature_vector)
        if norm > 0:
            feature_vector = feature_vector / norm
        
        return feature_vector
    
    async def _select_consolidation_splines(self, 
                                          feature_vector: np.ndarray,
                                          strategy: str) -> List[str]:
        """Select splines for memory consolidation"""
        
        # Simple selection - just take first few splines
        available_splines = list(self.kan_topology.spline_neurons.keys())
        return available_splines[:3]
    
    async def _execute_consolidation(self, 
                                   feature_vector: np.ndarray,
                                   selected_splines: List[str],
                                   memory_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute memory consolidation through selected splines"""
        
        result = {
            "spline_outputs": {},
            "consolidation_confidence": 0.0,
        }
        
        confidences = []
        
        for spline_id in selected_splines:
            if spline_id not in self.kan_topology.spline_neurons:
                continue
            
            neuron = self.kan_topology.spline_neurons[spline_id]
            
            try:
                # Compute spline output for memory
                spline_output = neuron.compute(feature_vector)
                
                result["spline_outputs"][spline_id] = {
                    "confidence": spline_output.confidence,
                    "entropy_level": neuron.entropy_level
                }
                
                confidences.append(spline_output.confidence)
                
                # Update neuron access
                neuron.access_count += 1
                neuron.last_accessed = datetime.now()
                
            except Exception as e:
                self.logger.warning(f"Consolidation through {spline_id} failed: {e}")
                continue
        
        # Compute overall consolidation confidence
        result["consolidation_confidence"] = np.mean(confidences) if confidences else 0.0
        
        return result
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        
        stats = {
            "total_traces": len(self.memory_traces),
            "consolidation_history": len(self.consolidation_history),
            "timestamp": datetime.now().isoformat()
        }
        
        if self.memory_traces:
            # Access distribution
            access_counts = [trace["access_count"] for trace in self.memory_traces.values()]
            stats["access_distribution"] = {
                "mean": np.mean(access_counts),
                "max": np.max(access_counts),
                "min": np.min(access_counts)
            }
        
        return stats 