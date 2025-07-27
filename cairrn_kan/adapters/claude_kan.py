"""
Claude-KAN Integration Adapter

This module integrates Claude with the KAN-Cairrn system, providing contextual
prompt enrichment using interpretable spline function states.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime
import asyncio
import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from models import CursorState, KANTopology, CachedGlyph
    from cursor.function_navigator import FunctionNavigator
    from cursor.interpretability import SplineInterpreter
except ImportError:
    # Fallback import structure
    from ..models import CursorState, KANTopology, CachedGlyph
    from ..cursor.function_navigator import FunctionNavigator
    from ..cursor.interpretability import SplineInterpreter


class ClaudeKANAdapter:
    """Adapter for integrating Claude with KAN-Cairrn system"""
    
    def __init__(self, cairrn_kan: KANTopology, cursor_engine: FunctionNavigator):
        self.kan = cairrn_kan
        self.cursor = cursor_engine
        self.interpreter = SplineInterpreter()
        self.logger = logging.getLogger(__name__)
        
        # Claude client would be initialized here
        self.claude_client = None  # Placeholder for actual Claude client
        
        # Context caching
        self.context_cache = {}
        self.cache_ttl = 300  # 5 minutes
    
    async def synthesize_with_kan_context(self, prompt: str, 
                                        use_cache: bool = True) -> 'Response':
        """Claude synthesis guided by interpretable KAN state"""
        
        try:
            # Get current cursor position in function space
            cursor_state = await self.cursor.get_kan_position()
            
            # Extract interpretable context from active splines
            active_functions = self.kan.get_active_splines(cursor_state.active_splines)
            interpretable_context = self.interpreter.explain_spline_activations(
                active_functions, 
                cursor_state.current_feature_vector
            )
            
            # Build semantically-informed prompt
            enriched_prompt = self.build_kan_prompt(
                prompt,
                spline_context=interpretable_context,
                trajectory_momentum=cursor_state.navigation_trajectory.semantic_momentum,
                confidence_map=cursor_state.confidence_scores
            )
            
            # Execute with full transparency into reasoning
            response = await self.execute_claude_request(enriched_prompt)
            
            # Update KAN based on response patterns
            await self.update_kan_from_response(response, cursor_state)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Claude-KAN synthesis failed: {e}")
            # Fallback to basic response
            return await self.execute_claude_request(prompt)
    
    def build_kan_prompt(self, prompt: str, spline_context: Dict[str, str], 
                        trajectory_momentum: np.ndarray, 
                        confidence_map: Dict[str, float]) -> str:
        """Build prompt with interpretable KAN context"""
        
        context_lines = []
        
        # Add KAN system status
        context_lines.append("## 🧠 KAN-Cairrn Context:")
        context_lines.append(f"Active spline functions: {len(spline_context)}")
        
        if spline_context:
            context_lines.append("\n### Active Cached Assemblages:")
            for spline_id, explanation in spline_context.items():
                confidence = confidence_map.get(spline_id, 0.0)
                context_lines.append(f"- **{spline_id}**: {explanation} (confidence: {confidence:.2f})")
        
        # Add trajectory information  
        momentum_magnitude = np.linalg.norm(trajectory_momentum)
        if momentum_magnitude > 0.1:
            dominant_direction = self.interpreter.explain_momentum(trajectory_momentum)
            context_lines.append(f"\n### Navigation Momentum: {dominant_direction}")
        
        # Add system interpretability notice
        context_lines.append("\n### System Transparency:")
        context_lines.append("The above context comes from interpretable spline functions where every")
        context_lines.append("activation can be traced and explained. Your response will influence")
        context_lines.append("future spline weights through gradient-based learning.")
        
        # Combine with original prompt
        full_context = "\n".join(context_lines)
        return f"{full_context}\n\n## Current Query:\n{prompt}"
    
    async def execute_claude_request(self, prompt: str) -> 'Response':
        """Execute Claude request with error handling"""
        
        # This would integrate with actual Claude API
        # For now, return a mock response structure
        mock_response = {
            "content": f"Mock Claude response to: {prompt[:100]}...",
            "confidence": 0.85,
            "reasoning_trace": ["analyzed prompt", "considered context", "generated response"],
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "model": "claude-3-sonnet",
                "tokens_used": len(prompt.split())
            }
        }
        
        return Response(mock_response)
    
    async def update_kan_from_response(self, response: 'Response', 
                                     cursor_state: CursorState):
        """Update KAN based on Claude response patterns"""
        
        try:
            # Extract features from Claude response
            response_features = self._extract_response_features(response)
            
            # Update spline weights based on response quality
            success_score = response.get_success_score()
            
            for spline_id in cursor_state.active_splines:
                neuron = self.kan.spline_neurons.get(spline_id)
                if neuron:
                    # Update entropy based on response success
                    if success_score > 0.8:
                        # Good response - reduce entropy
                        neuron.entropy_level *= 0.95
                    elif success_score < 0.4:
                        # Poor response - increase entropy
                        neuron.entropy_level = min(1.0, neuron.entropy_level * 1.05)
                    
                    # Update access patterns
                    neuron.access_count += 1
                    neuron.last_accessed = datetime.now()
            
            # Update global entropy
            self.kan.update_global_entropy()
            
            self.logger.info(f"Updated KAN from Claude response (success: {success_score:.2f})")
            
        except Exception as e:
            self.logger.error(f"Failed to update KAN from response: {e}")
    
    def _extract_response_features(self, response: 'Response') -> np.ndarray:
        """Extract feature vector from Claude response"""
        
        # Simple feature extraction based on response characteristics
        features = []
        
        content = response.content
        
        # Length-based features
        features.append(min(1.0, len(content) / 1000))  # Normalized length
        
        # Complexity features (simplified)
        sentence_count = content.count('.') + content.count('!') + content.count('?')
        features.append(min(1.0, sentence_count / 10))
        
        # Confidence feature
        features.append(response.confidence)
        
        # Pad to standard dimension
        while len(features) < 256:
            features.append(0.0)
        
        return np.array(features[:256])
    
    async def get_contextual_suggestions(self, current_prompt: str) -> List[str]:
        """Get suggestions for improving prompt based on KAN state"""
        
        try:
            cursor_state = await self.cursor.get_kan_position()
            suggestions = []
            
            # Analyze current KAN state
            active_count = len(cursor_state.active_splines)
            avg_confidence = (np.mean(list(cursor_state.confidence_scores.values()))
                            if cursor_state.confidence_scores else 0.0)
            
            # Generate suggestions based on state
            if active_count == 0:
                suggestions.append("Consider adding more specific context to activate relevant cached assemblages")
            elif active_count > 10:
                suggestions.append("Prompt may be too broad - consider focusing on specific aspects")
            
            if avg_confidence < 0.3:
                suggestions.append("Low spline confidence - try rephrasing with clearer semantic targets")
            elif avg_confidence > 0.9:
                suggestions.append("High spline confidence - good semantic alignment detected")
            
            # Momentum-based suggestions
            momentum_mag = np.linalg.norm(cursor_state.navigation_trajectory.semantic_momentum)
            if momentum_mag < 0.1:
                suggestions.append("Consider building on previous context for better navigation continuity")
            
            return suggestions
            
        except Exception as e:
            self.logger.error(f"Failed to generate suggestions: {e}")
            return ["Unable to analyze current KAN state for suggestions"]
    
    def get_kan_visualization_data(self) -> Dict[str, Any]:
        """Get data for visualizing current KAN state"""
        
        try:
            # Get activation snapshot
            activation_map = self.kan.get_activation_snapshot()
            
            # Get global interpretation
            global_state = self.interpreter.explain_global_state(activation_map)
            
            # Prepare visualization data
            viz_data = {
                "timestamp": datetime.now().isoformat(),
                "spline_activations": activation_map,
                "global_entropy": self.kan.global_entropy,
                "total_neurons": len(self.kan.spline_neurons),
                "active_neurons": global_state.get("active_splines", 0),
                "interpretation": global_state.get("interpretation", ""),
                "activity_level": global_state.get("activity_level", "unknown"),
                "network_health": self._assess_network_health()
            }
            
            return viz_data
            
        except Exception as e:
            self.logger.error(f"Failed to generate visualization data: {e}")
            return {"error": str(e)}
    
    def _assess_network_health(self) -> Dict[str, Any]:
        """Assess overall health of the KAN network"""
        
        if not self.kan.spline_neurons:
            return {"status": "empty", "score": 0.0}
        
        # Calculate health metrics
        entropies = [n.entropy_level for n in self.kan.spline_neurons.values()]
        access_counts = [n.access_count for n in self.kan.spline_neurons.values()]
        
        avg_entropy = np.mean(entropies)
        entropy_variance = np.var(entropies)
        avg_access = np.mean(access_counts)
        
        # Health score (0-1, higher is better)
        entropy_score = 1.0 - avg_entropy  # Lower entropy is better
        access_score = min(1.0, avg_access / 100)  # Normalize access count
        variance_score = max(0.0, 1.0 - entropy_variance)  # Lower variance is better
        
        overall_score = (entropy_score + access_score + variance_score) / 3
        
        # Determine status
        if overall_score > 0.8:
            status = "excellent"
        elif overall_score > 0.6:
            status = "good"
        elif overall_score > 0.4:
            status = "fair"
        else:
            status = "poor"
        
        return {
            "status": status,
            "score": overall_score,
            "avg_entropy": avg_entropy,
            "avg_access_count": avg_access,
            "entropy_variance": entropy_variance,
            "recommendations": self._generate_health_recommendations(overall_score, avg_entropy, avg_access)
        }
    
    def _generate_health_recommendations(self, score: float, 
                                       avg_entropy: float, 
                                       avg_access: float) -> List[str]:
        """Generate recommendations for improving network health"""
        
        recommendations = []
        
        if score < 0.5:
            recommendations.append("Network health is poor - consider system maintenance")
        
        if avg_entropy > 0.7:
            recommendations.append("High average entropy - consider neuron pruning and retraining")
        
        if avg_access < 5:
            recommendations.append("Low average access - neurons may be underutilized")
        
        if avg_access > 500:
            recommendations.append("High average access - consider load balancing or neuron splitting")
        
        if not recommendations:
            recommendations.append("Network health is good - continue normal operation")
        
        return recommendations


class Response:
    """Mock response class for Claude integration"""
    
    def __init__(self, data: Dict[str, Any]):
        self.content = data.get("content", "")
        self.confidence = data.get("confidence", 0.5)
        self.reasoning_trace = data.get("reasoning_trace", [])
        self.metadata = data.get("metadata", {})
    
    def get_success_score(self) -> float:
        """Calculate success score based on response quality"""
        # Simple scoring based on confidence and content length
        length_score = min(1.0, len(self.content) / 500)
        return (self.confidence + length_score) / 2 