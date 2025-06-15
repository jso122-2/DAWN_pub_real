"""
Function Navigator - Cursor navigation through interpretable spline function space

This module implements the core cursor navigation functionality that traverses
the KAN topology through learnable spline functions.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime
import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from models import CursorState, FunctionPath, NavigationResult, NavigationStep, KANTopology
    from core.spline_neurons import SplineNeuronManager
    from cursor.interpretability import SplineInterpreter
except ImportError:
    # Fallback import structure
    from ..models import CursorState, FunctionPath, NavigationResult, NavigationStep, KANTopology
    from ..core.spline_neurons import SplineNeuronManager
    from ..cursor.interpretability import SplineInterpreter


class SplinePathfinder:
    """Pathfinding algorithms through spline networks"""
    
    def __init__(self, exploration_weight: float = 0.3):
        self.exploration_weight = exploration_weight
        self.logger = logging.getLogger(__name__)
    
    def find_spline_path(self, start_vector: np.ndarray, 
                        target_semantics: Dict[str, float],
                        kan_topology: KANTopology,
                        max_steps: int = 20) -> FunctionPath:
        """Find optimal path through spline space to target semantics"""
        
        # Initialize path
        path = FunctionPath(
            visited_neurons=[],
            gradient_history=[],
            activation_patterns=[],
            semantic_momentum=np.zeros_like(start_vector)
        )
        
        current_vector = start_vector.copy()
        visited_neurons = set()
        
        for step in range(max_steps):
            # Find best next neuron
            best_neuron_id, best_score = self._find_best_next_neuron(
                current_vector, target_semantics, kan_topology, visited_neurons
            )
            
            if best_neuron_id is None:
                break
            
            # Get neuron and compute activation
            neuron = kan_topology.spline_neurons[best_neuron_id]
            activation_pattern = self._compute_activation_pattern(
                neuron, current_vector
            )
            
            # Compute gradient toward target
            gradient = self._compute_semantic_gradient(
                current_vector, target_semantics, neuron
            )
            
            # Add step to path
            path.add_step(best_neuron_id, gradient, activation_pattern)
            
            # Update current position
            current_vector = self._update_position(current_vector, gradient)
            visited_neurons.add(best_neuron_id)
            
            # Check if we've reached target
            if self._is_target_reached(current_vector, target_semantics):
                break
        
        # Calculate path confidence
        path.path_confidence = self._calculate_path_confidence(path, target_semantics)
        
        return path
    
    def _find_best_next_neuron(self, current_vector: np.ndarray,
                              target_semantics: Dict[str, float],
                              kan_topology: KANTopology,
                              visited: set) -> Tuple[Optional[str], float]:
        """Find the best next neuron to visit"""
        
        best_neuron_id = None
        best_score = -float('inf')
        
        for neuron_id, neuron in kan_topology.spline_neurons.items():
            if neuron_id in visited:
                continue
            
            # Compute relevance score
            relevance = self._compute_neuron_relevance(
                neuron, current_vector, target_semantics
            )
            
            # Add exploration bonus
            exploration_bonus = self.exploration_weight * np.random.random()
            
            # Compute total score
            total_score = relevance + exploration_bonus
            
            if total_score > best_score:
                best_score = total_score
                best_neuron_id = neuron_id
        
        return best_neuron_id, best_score
    
    def _compute_neuron_relevance(self, neuron, current_vector: np.ndarray,
                                 target_semantics: Dict[str, float]) -> float:
        """Compute how relevant a neuron is for reaching target semantics"""
        
        # Compute confidence for current vector
        confidence = neuron.compute_confidence(current_vector)
        
        # Compute semantic alignment
        semantic_alignment = self._compute_semantic_alignment(
            neuron, target_semantics
        )
        
        # Combine scores
        relevance = 0.7 * confidence + 0.3 * semantic_alignment
        
        return relevance
    
    def _compute_semantic_alignment(self, neuron, target_semantics: Dict[str, float]) -> float:
        """Compute alignment between neuron features and target semantics"""
        alignment = 0.0
        
        for feature in neuron.input_features:
            if feature in target_semantics:
                # Higher alignment for matching features
                alignment += target_semantics[feature]
        
        # Normalize by number of features
        return alignment / len(neuron.input_features) if neuron.input_features else 0.0
    
    def _compute_activation_pattern(self, neuron, feature_vector: np.ndarray) -> Dict[str, float]:
        """Compute activation pattern for a neuron"""
        try:
            # Get cached glyph to extract activation pattern
            glyph = neuron.compute(feature_vector)
            return glyph.activation_pattern
        except Exception as e:
            self.logger.warning(f"Failed to compute activation pattern: {e}")
            return {feature: 0.0 for feature in neuron.input_features}
    
    def _compute_semantic_gradient(self, current_vector: np.ndarray,
                                  target_semantics: Dict[str, float],
                                  neuron) -> np.ndarray:
        """Compute gradient toward target semantics"""
        
        # Simple gradient computation
        gradient = np.zeros_like(current_vector)
        
        # For each feature in target semantics
        for i, feature in enumerate(neuron.input_features):
            if i < len(gradient) and feature in target_semantics:
                target_value = target_semantics[feature]
                current_value = current_vector[i] if i < len(current_vector) else 0.0
                
                # Gradient points toward target
                gradient[i] = target_value - current_value
        
        # Normalize gradient
        norm = np.linalg.norm(gradient)
        if norm > 0:
            gradient = gradient / norm
        
        return gradient
    
    def _update_position(self, current_vector: np.ndarray, 
                        gradient: np.ndarray, step_size: float = 0.1) -> np.ndarray:
        """Update position in function space"""
        return current_vector + step_size * gradient
    
    def _is_target_reached(self, current_vector: np.ndarray,
                          target_semantics: Dict[str, float],
                          threshold: float = 0.1) -> bool:
        """Check if target semantics have been reached"""
        
        # Simple distance check
        total_distance = 0.0
        feature_count = 0
        
        for i, (feature, target_value) in enumerate(target_semantics.items()):
            if i < len(current_vector):
                distance = abs(current_vector[i] - target_value)
                total_distance += distance
                feature_count += 1
        
        if feature_count == 0:
            return False
        
        average_distance = total_distance / feature_count
        return average_distance < threshold
    
    def _calculate_path_confidence(self, path: FunctionPath, 
                                  target_semantics: Dict[str, float]) -> float:
        """Calculate overall confidence for the path"""
        
        if not path.visited_neurons:
            return 0.0
        
        # Calculate confidence based on final position
        final_vector = path.gradient_history[-1] if path.gradient_history else np.zeros(1)
        final_distance = self._compute_target_distance(final_vector, target_semantics)
        
        # Convert distance to confidence (closer = more confident)
        confidence = max(0.0, 1.0 - final_distance)
        
        return confidence
    
    def _compute_target_distance(self, vector: np.ndarray, 
                                target_semantics: Dict[str, float]) -> float:
        """Compute distance from current vector to target semantics"""
        
        total_distance = 0.0
        feature_count = 0
        
        for i, (feature, target_value) in enumerate(target_semantics.items()):
            if i < len(vector):
                distance = abs(vector[i] - target_value)
                total_distance += distance
                feature_count += 1
        
        return total_distance / feature_count if feature_count > 0 else 1.0


class FunctionNavigator:
    """Main navigator for cursor movement through spline function space"""
    
    def __init__(self, cairrn_kan: KANTopology):
        self.kan = cairrn_kan
        self.pathfinder = SplinePathfinder()
        self.interpreter = SplineInterpreter()
        self.logger = logging.getLogger(__name__)
        self.current_cursor_state: Optional[CursorState] = None
    
    async def get_cursor_state(self) -> CursorState:
        """Get current cursor state"""
        if self.current_cursor_state is None:
            # Initialize default cursor state
            self.current_cursor_state = CursorState(
                active_splines=[],
                current_feature_vector=np.zeros(256),  # Default dimension
                navigation_trajectory=FunctionPath(
                    visited_neurons=[],
                    gradient_history=[],
                    activation_patterns=[],
                    semantic_momentum=np.zeros(256)
                ),
                interpretation_context={},
                confidence_scores={},
                session_id=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
        
        return self.current_cursor_state
    
    async def navigate_to_function(self, target_semantics: Dict[str, float]) -> NavigationResult:
        """Navigate cursor through spline space to desired semantic target"""
        start_time = datetime.now()
        
        try:
            current_state = await self.get_cursor_state()
            
            # Find optimal path through spline space
            path = self.pathfinder.find_spline_path(
                start_vector=current_state.current_feature_vector,
                target_semantics=target_semantics,
                kan_topology=self.kan,
                max_steps=20
            )
            
            # Execute navigation with real-time interpretation
            navigation_result = await self.execute_spline_navigation(path)
            
            # Update cursor state
            await self.update_cursor_from_navigation(navigation_result)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            navigation_result.execution_time = execution_time
            
            return navigation_result
            
        except Exception as e:
            self.logger.error(f"Navigation failed: {e}")
            
            # Return failed navigation result
            return NavigationResult(
                steps=[],
                final_state=await self.get_cursor_state(),
                interpretation_summary=f"Navigation failed: {str(e)}",
                navigation_success=False,
                total_confidence=0.0,
                execution_time=(datetime.now() - start_time).total_seconds()
            )
    
    async def execute_spline_navigation(self, path: FunctionPath) -> NavigationResult:
        """Execute navigation through interpretable function space"""
        
        results = []
        
        for step_idx, neuron_id in enumerate(path.visited_neurons):
            try:
                # Get neuron
                neuron = self.kan.spline_neurons.get(neuron_id)
                if not neuron:
                    self.logger.warning(f"Neuron {neuron_id} not found")
                    continue
                
                # Get feature vector for this step
                feature_vector = (path.gradient_history[step_idx] 
                                if step_idx < len(path.gradient_history)
                                else np.zeros(256))
                
                # Activate spline neuron
                spline_output = neuron.compute(feature_vector)
                
                # Get interpretable output
                interpretation = self.interpreter.explain_spline_computation(
                    neuron, feature_vector, spline_output
                )
                
                # Record step result
                step_result = NavigationStep(
                    neuron_id=neuron_id,
                    input_features=feature_vector,
                    spline_output=spline_output,
                    interpretation=interpretation,
                    confidence=neuron.compute_confidence(feature_vector)
                )
                results.append(step_result)
                
                # Update KAN weights incrementally
                await self.update_neuron_from_navigation(neuron, step_result)
                
            except Exception as e:
                self.logger.error(f"Step {step_idx} failed: {e}")
                continue
        
        # Compute final state
        final_state = await self.compute_final_state(results)
        
        # Generate interpretation summary
        interpretation_summary = self.interpreter.summarize_path(results)
        
        return NavigationResult(
            steps=results,
            final_state=final_state,
            interpretation_summary=interpretation_summary,
            navigation_success=len(results) > 0,
            total_confidence=np.mean([step.confidence for step in results]) if results else 0.0,
            execution_time=0.0  # Will be set by caller
        )
    
    async def compute_final_state(self, navigation_steps: List[NavigationStep]) -> CursorState:
        """Compute final cursor state after navigation"""
        
        current_state = await self.get_cursor_state()
        
        if not navigation_steps:
            return current_state
        
        # Update based on final step
        final_step = navigation_steps[-1]
        
        # Extract active splines from navigation
        active_splines = [step.neuron_id for step in navigation_steps]
        
        # Update feature vector (use final step's input)
        current_feature_vector = final_step.input_features
        
        # Update trajectory
        trajectory = FunctionPath(
            visited_neurons=active_splines,
            gradient_history=[step.input_features for step in navigation_steps],
            activation_patterns=[step.spline_output.activation_pattern for step in navigation_steps],
            semantic_momentum=np.mean([step.input_features for step in navigation_steps], axis=0)
        )
        
        # Update confidence scores
        confidence_scores = {
            step.neuron_id: step.confidence for step in navigation_steps
        }
        
        # Create updated cursor state
        updated_state = CursorState(
            active_splines=active_splines,
            current_feature_vector=current_feature_vector,
            navigation_trajectory=trajectory,
            interpretation_context=current_state.interpretation_context,
            confidence_scores=confidence_scores,
            session_id=current_state.session_id
        )
        
        return updated_state
    
    async def update_cursor_from_navigation(self, navigation_result: NavigationResult):
        """Update cursor state from navigation result"""
        self.current_cursor_state = navigation_result.final_state
        self.logger.info(f"Updated cursor state with {len(navigation_result.steps)} steps")
    
    async def update_neuron_from_navigation(self, neuron, step_result: NavigationStep):
        """Update neuron parameters based on navigation feedback"""
        
        # Simple update based on confidence
        if step_result.confidence > 0.8:
            # High confidence - reinforce
            neuron.entropy_level *= 0.95
        elif step_result.confidence < 0.3:
            # Low confidence - increase entropy
            neuron.entropy_level = min(1.0, neuron.entropy_level * 1.05)
        
        # Update access time
        neuron.last_accessed = datetime.now()
        neuron.access_count += 1
    
    async def get_kan_position(self) -> CursorState:
        """Get current cursor position in KAN function space"""
        return await self.get_cursor_state()
    
    def get_navigation_stats(self) -> Dict[str, Any]:
        """Get navigation statistics"""
        
        if not self.current_cursor_state:
            return {"no_navigation_history": True}
        
        trajectory = self.current_cursor_state.navigation_trajectory
        
        return {
            "total_steps": trajectory.total_steps,
            "visited_neurons": len(trajectory.visited_neurons),
            "average_confidence": np.mean(list(self.current_cursor_state.confidence_scores.values()))
                                if self.current_cursor_state.confidence_scores else 0.0,
            "semantic_momentum_magnitude": np.linalg.norm(trajectory.semantic_momentum),
            "session_id": self.current_cursor_state.session_id,
            "last_updated": self.current_cursor_state.last_updated.isoformat()
        } 