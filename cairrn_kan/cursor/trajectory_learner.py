"""
Trajectory Learner - Adaptive pathfinding in KAN space

This module implements learning algorithms for optimal trajectory
finding through spline function space.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime
import asyncio

from ..models import KANTopology, FunctionPath, CursorState, NavigationResult


class TrajectoryLearner:
    """Learns optimal trajectories through spline function space"""
    
    def __init__(self, learning_rate: float = 0.01):
        self.learning_rate = learning_rate
        self.logger = logging.getLogger(__name__)
        
        # Learning state
        self.trajectory_history = []
        self.success_patterns = {}
        self.exploration_memory = {}
        
    async def learn_trajectory(self, 
                             start_state: CursorState,
                             target_semantics: Dict[str, float],
                             topology: KANTopology,
                             navigation_result: NavigationResult) -> Dict[str, Any]:
        """Learn from a completed navigation trajectory"""
        
        learning_start = datetime.now()
        
        try:
            # Extract trajectory features
            trajectory_features = self._extract_trajectory_features(
                start_state, target_semantics, navigation_result
            )
            
            # Compute trajectory success score
            success_score = self._compute_success_score(navigation_result, target_semantics)
            
            # Update learning patterns
            pattern_updates = await self._update_success_patterns(
                trajectory_features, success_score
            )
            
            # Update exploration memory
            exploration_updates = await self._update_exploration_memory(
                start_state, navigation_result, success_score
            )
            
            # Record in history
            learning_record = {
                "timestamp": learning_start.isoformat(),
                "trajectory_features": trajectory_features,
                "success_score": success_score,
                "pattern_updates": pattern_updates,
                "exploration_updates": exploration_updates,
                "learning_duration": (datetime.now() - learning_start).total_seconds()
            }
            
            self.trajectory_history.append(learning_record)
            
            # Trim history
            if len(self.trajectory_history) > 200:
                self.trajectory_history = self.trajectory_history[-100:]
            
            self.logger.info(f"Learned trajectory with success score {success_score:.3f}")
            
            return learning_record
            
        except Exception as e:
            self.logger.error(f"Trajectory learning failed: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def _extract_trajectory_features(self, 
                                   start_state: CursorState,
                                   target_semantics: Dict[str, float],
                                   navigation_result: NavigationResult) -> Dict[str, Any]:
        """Extract features from a navigation trajectory"""
        
        features = {
            "start_features": {},
            "target_features": {},
            "path_features": {},
            "outcome_features": {}
        }
        
        # Start state features
        features["start_features"] = {
            "active_splines_count": len(start_state.active_splines),
            "feature_vector_norm": float(np.linalg.norm(start_state.current_feature_vector)),
            "avg_confidence": np.mean(list(start_state.confidence_scores.values())) if start_state.confidence_scores else 0.0
        }
        
        # Target features
        features["target_features"] = {
            "target_dimension": len(target_semantics),
            "target_magnitude": float(np.linalg.norm(list(target_semantics.values()))),
            "target_complexity": self._compute_semantic_complexity(target_semantics)
        }
        
        # Path features
        if hasattr(navigation_result, 'steps') and navigation_result.steps:
            path_confidences = [step.confidence for step in navigation_result.steps]
            features["path_features"] = {
                "path_length": len(navigation_result.steps),
                "avg_path_confidence": np.mean(path_confidences),
                "confidence_variance": np.var(path_confidences),
                "unique_splines": len(set(step.neuron_id for step in navigation_result.steps))
            }
        
        # Outcome features
        if hasattr(navigation_result, 'final_state'):
            features["outcome_features"] = {
                "final_confidence": getattr(navigation_result.final_state, 'confidence', 0.0),
                "semantic_distance": self._compute_semantic_distance(navigation_result, target_semantics)
            }
        
        return features
    
    def _compute_semantic_complexity(self, semantics: Dict[str, float]) -> float:
        """Compute complexity measure for semantic target"""
        
        if not semantics:
            return 0.0
        
        values = list(semantics.values())
        
        # Complexity based on variance and entropy
        variance = np.var(values)
        
        # Entropy-like measure
        normalized_values = np.abs(values) / (np.sum(np.abs(values)) + 1e-8)
        entropy = -np.sum(normalized_values * np.log(normalized_values + 1e-8))
        
        return float(variance + entropy)
    
    def _compute_semantic_distance(self, navigation_result: NavigationResult, 
                                 target_semantics: Dict[str, float]) -> float:
        """Compute distance between achieved and target semantics"""
        
        # Simplified distance computation
        if not hasattr(navigation_result, 'final_state'):
            return 1.0  # Maximum distance
        
        # For now, use a simple heuristic based on confidence
        final_confidence = getattr(navigation_result.final_state, 'confidence', 0.0)
        
        # Higher confidence indicates closer to target
        distance = 1.0 - final_confidence
        
        return float(distance)
    
    def _compute_success_score(self, navigation_result: NavigationResult,
                             target_semantics: Dict[str, float]) -> float:
        """Compute overall success score for a navigation trajectory"""
        
        score_components = []
        
        # Confidence score
        if hasattr(navigation_result, 'steps') and navigation_result.steps:
            avg_confidence = np.mean([step.confidence for step in navigation_result.steps])
            score_components.append(avg_confidence)
        
        # Semantic distance score (inverse of distance)
        semantic_distance = self._compute_semantic_distance(navigation_result, target_semantics)
        semantic_score = 1.0 - semantic_distance
        score_components.append(semantic_score)
        
        # Path efficiency score
        if hasattr(navigation_result, 'steps'):
            path_length = len(navigation_result.steps)
            efficiency_score = 1.0 / (1.0 + path_length * 0.1)  # Penalize long paths
            score_components.append(efficiency_score)
        
        # Overall score
        if score_components:
            overall_score = np.mean(score_components)
        else:
            overall_score = 0.0
        
        return float(np.clip(overall_score, 0.0, 1.0))
    
    async def _update_success_patterns(self, 
                                     trajectory_features: Dict[str, Any],
                                     success_score: float) -> Dict[str, Any]:
        """Update patterns associated with successful trajectories"""
        
        updates = {"patterns_updated": 0, "new_patterns": 0}
        
        try:
            # Create pattern key from features
            pattern_key = self._create_pattern_key(trajectory_features)
            
            if pattern_key in self.success_patterns:
                # Update existing pattern
                existing = self.success_patterns[pattern_key]
                
                # Weighted average of success scores
                weight = 0.3  # Learning rate for pattern updates
                new_score = weight * success_score + (1 - weight) * existing["avg_success"]
                
                existing["avg_success"] = new_score
                existing["observation_count"] += 1
                existing["last_updated"] = datetime.now().isoformat()
                
                updates["patterns_updated"] = 1
            else:
                # Create new pattern
                self.success_patterns[pattern_key] = {
                    "avg_success": success_score,
                    "observation_count": 1,
                    "created": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "features": trajectory_features
                }
                
                updates["new_patterns"] = 1
            
            # Limit pattern storage
            if len(self.success_patterns) > 500:
                # Remove patterns with low observation counts
                sorted_patterns = sorted(
                    self.success_patterns.items(),
                    key=lambda x: x[1]["observation_count"],
                    reverse=True
                )
                self.success_patterns = dict(sorted_patterns[:250])
            
        except Exception as e:
            self.logger.warning(f"Pattern update failed: {e}")
            updates["error"] = str(e)
        
        return updates
    
    def _create_pattern_key(self, trajectory_features: Dict[str, Any]) -> str:
        """Create a key for pattern matching from trajectory features"""
        
        key_components = []
        
        # Start features
        start_features = trajectory_features.get("start_features", {})
        spline_count = start_features.get("active_splines_count", 0)
        key_components.append(f"splines:{spline_count}")
        
        # Target features
        target_features = trajectory_features.get("target_features", {})
        target_dim = target_features.get("target_dimension", 0)
        target_complexity = target_features.get("target_complexity", 0.0)
        key_components.append(f"target:{target_dim}:{target_complexity:.2f}")
        
        # Path features
        path_features = trajectory_features.get("path_features", {})
        path_length = path_features.get("path_length", 0)
        key_components.append(f"path:{path_length}")
        
        return "|".join(key_components)
    
    async def _update_exploration_memory(self, 
                                       start_state: CursorState,
                                       navigation_result: NavigationResult,
                                       success_score: float) -> Dict[str, Any]:
        """Update exploration memory for future pathfinding"""
        
        updates = {"memory_updates": 0}
        
        try:
            # Create memory key from start state
            memory_key = self._create_memory_key(start_state)
            
            # Extract spline sequence from navigation
            spline_sequence = []
            if hasattr(navigation_result, 'steps'):
                spline_sequence = [step.neuron_id for step in navigation_result.steps]
            
            if memory_key in self.exploration_memory:
                # Update existing memory
                memory_entry = self.exploration_memory[memory_key]
                
                # Add new spline sequence
                if spline_sequence not in memory_entry["sequences"]:
                    memory_entry["sequences"].append({
                        "sequence": spline_sequence,
                        "success_score": success_score,
                        "timestamp": datetime.now().isoformat()
                    })
                    updates["memory_updates"] = 1
                
                # Keep only best sequences
                memory_entry["sequences"].sort(key=lambda x: x["success_score"], reverse=True)
                memory_entry["sequences"] = memory_entry["sequences"][:10]  # Top 10
                
            else:
                # Create new memory entry
                self.exploration_memory[memory_key] = {
                    "sequences": [{
                        "sequence": spline_sequence,
                        "success_score": success_score,
                        "timestamp": datetime.now().isoformat()
                    }],
                    "created": datetime.now().isoformat()
                }
                updates["memory_updates"] = 1
            
            # Limit memory size
            if len(self.exploration_memory) > 200:
                # Keep most recent entries
                sorted_memory = sorted(
                    self.exploration_memory.items(),
                    key=lambda x: x[1]["created"],
                    reverse=True
                )
                self.exploration_memory = dict(sorted_memory[:100])
            
        except Exception as e:
            self.logger.warning(f"Exploration memory update failed: {e}")
            updates["error"] = str(e)
        
        return updates
    
    def _create_memory_key(self, start_state: CursorState) -> str:
        """Create memory key from cursor start state"""
        
        # Simple key based on active splines and feature vector characteristics
        active_splines = sorted(start_state.active_splines)
        splines_hash = hash(tuple(active_splines)) % 10000
        
        feature_norm = np.linalg.norm(start_state.current_feature_vector)
        feature_bin = int(feature_norm * 10)  # Discretize
        
        return f"splines:{splines_hash}|features:{feature_bin}"
    
    async def suggest_trajectory(self, 
                               start_state: CursorState,
                               target_semantics: Dict[str, float],
                               topology: KANTopology) -> Optional[List[str]]:
        """Suggest optimal trajectory based on learned patterns"""
        
        try:
            # Extract features from current situation
            current_features = self._extract_current_features(start_state, target_semantics)
            
            # Find matching patterns
            matching_patterns = self._find_matching_patterns(current_features)
            
            if not matching_patterns:
                # No patterns found, return None for exploration
                return None
            
            # Select best pattern
            best_pattern = max(matching_patterns, key=lambda x: x[1]["avg_success"])
            
            # Extract suggested spline sequence from exploration memory
            memory_key = self._create_memory_key(start_state)
            
            if memory_key in self.exploration_memory:
                sequences = self.exploration_memory[memory_key]["sequences"]
                if sequences:
                    # Return best sequence
                    best_sequence = max(sequences, key=lambda x: x["success_score"])
                    return best_sequence["sequence"]
            
            # Fallback: suggest based on pattern features
            return self._generate_trajectory_from_pattern(best_pattern[1], topology)
            
        except Exception as e:
            self.logger.warning(f"Trajectory suggestion failed: {e}")
            return None
    
    def _extract_current_features(self, 
                                start_state: CursorState,
                                target_semantics: Dict[str, float]) -> Dict[str, Any]:
        """Extract features from current navigation context"""
        
        return {
            "start_features": {
                "active_splines_count": len(start_state.active_splines),
                "feature_vector_norm": float(np.linalg.norm(start_state.current_feature_vector)),
                "avg_confidence": np.mean(list(start_state.confidence_scores.values())) if start_state.confidence_scores else 0.0
            },
            "target_features": {
                "target_dimension": len(target_semantics),
                "target_magnitude": float(np.linalg.norm(list(target_semantics.values()))),
                "target_complexity": self._compute_semantic_complexity(target_semantics)
            }
        }
    
    def _find_matching_patterns(self, current_features: Dict[str, Any]) -> List[Tuple[str, Dict[str, Any]]]:
        """Find patterns that match current navigation context"""
        
        matching_patterns = []
        
        for pattern_key, pattern_data in self.success_patterns.items():
            similarity = self._compute_pattern_similarity(current_features, pattern_data["features"])
            
            if similarity > 0.7:  # Similarity threshold
                matching_patterns.append((pattern_key, pattern_data))
        
        return matching_patterns
    
    def _compute_pattern_similarity(self, current_features: Dict[str, Any], 
                                  pattern_features: Dict[str, Any]) -> float:
        """Compute similarity between current features and stored pattern"""
        
        similarities = []
        
        # Compare start features
        current_start = current_features.get("start_features", {})
        pattern_start = pattern_features.get("start_features", {})
        
        if current_start and pattern_start:
            # Spline count similarity
            current_splines = current_start.get("active_splines_count", 0)
            pattern_splines = pattern_start.get("active_splines_count", 0)
            spline_sim = 1.0 - abs(current_splines - pattern_splines) / max(1, max(current_splines, pattern_splines))
            similarities.append(spline_sim)
        
        # Compare target features
        current_target = current_features.get("target_features", {})
        pattern_target = pattern_features.get("target_features", {})
        
        if current_target and pattern_target:
            # Complexity similarity
            current_complexity = current_target.get("target_complexity", 0.0)
            pattern_complexity = pattern_target.get("target_complexity", 0.0)
            complexity_sim = 1.0 - abs(current_complexity - pattern_complexity) / max(1.0, max(current_complexity, pattern_complexity))
            similarities.append(complexity_sim)
        
        return np.mean(similarities) if similarities else 0.0
    
    def _generate_trajectory_from_pattern(self, pattern_data: Dict[str, Any], 
                                        topology: KANTopology) -> List[str]:
        """Generate trajectory suggestion from pattern data"""
        
        # Simple heuristic: select splines with good entropy/confidence balance
        available_splines = list(topology.spline_neurons.keys())
        
        if len(available_splines) <= 3:
            return available_splines
        
        # Score splines based on entropy and access patterns
        spline_scores = []
        for spline_id, neuron in topology.spline_neurons.items():
            # Prefer lower entropy and higher access count
            entropy_score = 1.0 - neuron.entropy_level
            access_score = min(1.0, neuron.access_count / 10.0)
            
            combined_score = 0.7 * entropy_score + 0.3 * access_score
            spline_scores.append((spline_id, combined_score))
        
        # Sort and return top splines
        spline_scores.sort(key=lambda x: x[1], reverse=True)
        return [spline_id for spline_id, _ in spline_scores[:3]]
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning statistics and performance metrics"""
        
        stats = {
            "total_trajectories": len(self.trajectory_history),
            "success_patterns": len(self.success_patterns),
            "exploration_memory": len(self.exploration_memory),
            "timestamp": datetime.now().isoformat()
        }
        
        if self.trajectory_history:
            # Success score distribution
            success_scores = [t.get("success_score", 0.0) for t in self.trajectory_history]
            stats["success_distribution"] = {
                "mean": np.mean(success_scores),
                "std": np.std(success_scores),
                "min": np.min(success_scores),
                "max": np.max(success_scores)
            }
            
            # Learning trend
            recent_scores = success_scores[-20:] if len(success_scores) >= 20 else success_scores
            older_scores = success_scores[:-20] if len(success_scores) >= 40 else success_scores[:len(success_scores)//2]
            
            if recent_scores and older_scores:
                stats["learning_trend"] = {
                    "recent_avg": np.mean(recent_scores),
                    "older_avg": np.mean(older_scores),
                    "improvement": np.mean(recent_scores) - np.mean(older_scores)
                }
        
        # Pattern quality
        if self.success_patterns:
            pattern_scores = [p["avg_success"] for p in self.success_patterns.values()]
            stats["pattern_quality"] = {
                "mean_success": np.mean(pattern_scores),
                "top_patterns": sum(1 for score in pattern_scores if score > 0.8)
            }
        
        return stats 