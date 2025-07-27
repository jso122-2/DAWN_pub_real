"""
Entropy Engine - Gradient-based cache decay and optimization

This module manages entropy levels across the KAN-Cairrn system and implements
gradient-based optimization for spline function parameters.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime, timedelta
import asyncio

from ..models import KANTopology, SplineNeuron, CairrConfig


class EntropyEngine:
    """Engine for managing entropy and gradient-based optimization"""
    
    def __init__(self, config: CairrConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Optimization state
        self.optimization_history = []
        self.last_cleanup = datetime.now()
        self.gradient_cache = {}
        
    async def run_entropy_cycle(self, topology: KANTopology) -> Dict[str, Any]:
        """Run one cycle of entropy management and optimization"""
        
        cycle_start = datetime.now()
        results = {
            "timestamp": cycle_start.isoformat(),
            "neurons_processed": 0,
            "neurons_pruned": 0,
            "gradients_computed": 0,
            "entropy_reductions": 0,
            "global_entropy_before": topology.global_entropy,
            "global_entropy_after": 0.0
        }
        
        try:
            # Step 1: Compute entropy gradients for all neurons
            gradients = await self._compute_entropy_gradients(topology)
            results["gradients_computed"] = len(gradients)
            
            # Step 2: Apply gradient-based entropy reduction
            entropy_reductions = await self._apply_entropy_gradients(topology, gradients)
            results["entropy_reductions"] = entropy_reductions
            
            # Step 3: Update global entropy
            topology.update_global_entropy()
            results["global_entropy_after"] = topology.global_entropy
            
            # Step 4: Cache gradients for future use
            self.gradient_cache.update(gradients)
            
            results["neurons_processed"] = len(topology.spline_neurons)
            results["cycle_duration"] = (datetime.now() - cycle_start).total_seconds()
            
            # Log optimization step
            self.optimization_history.append(results.copy())
            
            # Keep only recent history
            if len(self.optimization_history) > 100:
                self.optimization_history = self.optimization_history[-50:]
            
            self.logger.info(f"Entropy cycle completed: {results['entropy_reductions']} reductions")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Entropy cycle failed: {e}")
            results["error"] = str(e)
            return results
    
    async def _compute_entropy_gradients(self, topology: KANTopology) -> Dict[str, np.ndarray]:
        """Compute entropy gradients for all neurons"""
        
        gradients = {}
        
        for neuron_id, neuron in topology.spline_neurons.items():
            try:
                # Compute gradient based on entropy and access patterns
                gradient = self._compute_neuron_entropy_gradient(neuron, topology)
                gradients[neuron_id] = gradient
                
            except Exception as e:
                self.logger.warning(f"Failed to compute gradient for {neuron_id}: {e}")
                continue
        
        return gradients
    
    def _compute_neuron_entropy_gradient(self, neuron: SplineNeuron, 
                                       topology: KANTopology) -> np.ndarray:
        """Compute entropy gradient for a single neuron"""
        
        # Base gradient from current entropy level
        entropy_factor = neuron.entropy_level - 0.5  # Target entropy of 0.5
        
        # Access frequency factor
        access_factor = 1.0 / max(1.0, neuron.access_count)
        
        # Time decay factor
        time_since_access = (datetime.now() - neuron.last_accessed).total_seconds()
        time_factor = min(1.0, time_since_access / 3600)  # 1 hour normalization
        
        # Combine factors
        gradient_magnitude = entropy_factor * (1.0 + access_factor + time_factor)
        
        # Create gradient vector (simplified - in practice would be more sophisticated)
        feature_dim = len(neuron.input_features)
        gradient = np.random.normal(0, abs(gradient_magnitude), feature_dim)
        
        # Apply direction (reduce entropy if too high)
        if neuron.entropy_level > 0.7:
            gradient *= -1  # Negative gradient to reduce entropy
        
        return gradient
    
    async def _apply_entropy_gradients(self, topology: KANTopology, 
                                     gradients: Dict[str, np.ndarray]) -> int:
        """Apply entropy gradients to reduce entropy levels"""
        
        reductions = 0
        learning_rate = self.config.spline_update_learning_rate
        
        for neuron_id, gradient in gradients.items():
            neuron = topology.spline_neurons.get(neuron_id)
            if not neuron:
                continue
            
            try:
                # Apply gradient to spline function
                neuron.spline_function.update_parameters(gradient, learning_rate)
                
                # Update entropy level based on gradient application
                entropy_change = -np.linalg.norm(gradient) * learning_rate * 0.1
                new_entropy = neuron.entropy_level + entropy_change
                
                # Clamp entropy to valid range
                neuron.entropy_level = np.clip(new_entropy, 0.0, 1.0)
                
                if entropy_change < 0:
                    reductions += 1
                
            except Exception as e:
                self.logger.warning(f"Failed to apply gradient to {neuron_id}: {e}")
                continue
        
        return reductions
    
    def get_entropy_stats(self, topology: KANTopology) -> Dict[str, Any]:
        """Get comprehensive entropy statistics"""
        
        if not topology.spline_neurons:
            return {"error": "No neurons in topology"}
        
        entropies = [neuron.entropy_level for neuron in topology.spline_neurons.values()]
        access_counts = [neuron.access_count for neuron in topology.spline_neurons.values()]
        
        # Age analysis
        now = datetime.now()
        ages = [(now - neuron.last_accessed).total_seconds() / 3600 
                for neuron in topology.spline_neurons.values()]
        
        stats = {
            "global_entropy": topology.global_entropy,
            "neuron_count": len(topology.spline_neurons),
            "entropy_distribution": {
                "mean": np.mean(entropies),
                "std": np.std(entropies),
                "min": np.min(entropies),
                "max": np.max(entropies),
                "median": np.median(entropies)
            },
            "access_distribution": {
                "mean": np.mean(access_counts),
                "std": np.std(access_counts),
                "min": np.min(access_counts),
                "max": np.max(access_counts),
                "total": np.sum(access_counts)
            },
            "age_distribution": {
                "mean_hours": np.mean(ages),
                "max_hours": np.max(ages),
                "neurons_older_than_24h": sum(1 for age in ages if age > 24)
            },
            "optimization_history": len(self.optimization_history),
            "last_cleanup": self.last_cleanup.isoformat(),
            "cached_gradients": len(self.gradient_cache)
        }
        
        return stats 