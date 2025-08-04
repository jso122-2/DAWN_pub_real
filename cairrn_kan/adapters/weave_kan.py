"""
Weave KAN Adapter

Adapter for integrating KAN-Cairrn with weaving systems and thread composition.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime
import asyncio

from ...models import KANTopology, SplineNeuron, CachedGlyph
from core.weave_router import WeaveRouter


class WeaveKANAdapter:
    """Adapter for KAN-guided weaving operations"""
    
    def __init__(self, kan_topology: KANTopology, weave_router: WeaveRouter):
        self.kan_topology = kan_topology
        self.weave_router = weave_router
        self.logger = logging.getLogger(__name__)
        
        # Weaving state
        self.active_weaves = {}
        self.weave_history = []
        
    async def kan_guided_weaving(self, 
                               input_assemblage: Dict[str, Any],
                               weaving_strategy: str = "adaptive") -> Dict[str, Any]:
        """Execute KAN-guided weaving of assemblage components"""
        
        weave_start = datetime.now()
        weave_id = f"weave_{int(weave_start.timestamp())}"
        
        try:
            # Route through spline space
            routing_result = await self.weave_router.route_through_splines(
                input_assemblage, self.kan_topology, weaving_strategy
            )
            
            if "error" in routing_result:
                return routing_result
            
            # Extract spline outputs for weaving
            spline_components = self._extract_weaving_components(routing_result)
            
            # Execute modular weaving
            weaving_result = await self._execute_modular_weaving(
                spline_components, weaving_strategy
            )
            
            # Build complete result
            result = {
                "weave_id": weave_id,
                "input_assemblage": input_assemblage,
                "routing_result": routing_result,
                "spline_components": spline_components,
                "weaving_result": weaving_result,
                "strategy": weaving_strategy,
                "execution_time": (datetime.now() - weave_start).total_seconds(),
                "timestamp": datetime.now().isoformat()
            }
            
            # Store active weave
            self.active_weaves[weave_id] = result
            
            # Add to history
            self.weave_history.append(result)
            if len(self.weave_history) > 100:
                self.weave_history = self.weave_history[-50:]
            
            return result
            
        except Exception as e:
            self.logger.error(f"KAN-guided weaving failed: {e}")
            return {
                "error": str(e),
                "weave_id": weave_id,
                "input_assemblage": input_assemblage,
                "timestamp": datetime.now().isoformat()
            }
    
    def _extract_weaving_components(self, routing_result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract spline outputs as weaving components"""
        
        components = {
            "primary_components": [],
            "confidence_weights": {},
        }
        
        composition_result = routing_result.get("composition_result", {})
        spline_outputs = composition_result.get("spline_outputs", {})
        confidence_scores = composition_result.get("confidence_scores", {})
        
        # Categorize components by confidence
        for spline_id, output_data in spline_outputs.items():
            confidence = confidence_scores.get(spline_id, 0.0)
            
            component = {
                "spline_id": spline_id,
                "confidence": confidence,
                "step": output_data.get("step", 0),
                "data": output_data
            }
            
            components["primary_components"].append(component)
            components["confidence_weights"][spline_id] = confidence
        
        # Sort by confidence
        components["primary_components"].sort(key=lambda x: x["confidence"], reverse=True)
        
        return components
    
    async def _execute_modular_weaving(self, 
                                     spline_components: Dict[str, Any],
                                     strategy: str) -> Dict[str, Any]:
        """Execute modular weaving using spline components"""
        
        weaving_result = {
            "woven_output": None,
            "component_contributions": {},
            "final_confidence": 0.0,
        }
        
        try:
            # Get components
            primary_components = spline_components["primary_components"]
            confidence_weights = spline_components["confidence_weights"]
            
            if not primary_components:
                weaving_result["error"] = "No components available for weaving"
                return weaving_result
            
            # Simple weaving - use best component
            best_component = primary_components[0]
            
            weaving_result["woven_output"] = {
                "primary_component": best_component["spline_id"],
                "confidence": best_component["confidence"],
                "components_used": [best_component["spline_id"]]
            }
            
            weaving_result["final_confidence"] = best_component["confidence"]
            
            # Record component contributions
            for component in primary_components:
                spline_id = component["spline_id"]
                weaving_result["component_contributions"][spline_id] = {
                    "confidence": component["confidence"],
                    "contribution_weight": confidence_weights.get(spline_id, 0.0)
                }
            
        except Exception as e:
            self.logger.error(f"Modular weaving execution failed: {e}")
            weaving_result["error"] = str(e)
        
        return weaving_result
    
    def get_weaving_stats(self) -> Dict[str, Any]:
        """Get statistics about weaving operations"""
        
        stats = {
            "total_weaves": len(self.weave_history),
            "active_weaves": len(self.active_weaves),
            "timestamp": datetime.now().isoformat()
        }
        
        if self.weave_history:
            # Success rate
            successful_weaves = [
                w for w in self.weave_history 
                if "error" not in w and "error" not in w.get("weaving_result", {})
            ]
            stats["success_rate"] = len(successful_weaves) / len(self.weave_history)
        
        return stats 