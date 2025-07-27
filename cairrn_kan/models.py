"""
KAN-Cairrn Data Models

Core data structures for the interpretable function space navigation system.
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime
import numpy as np
import networkx as nx
from abc import ABC, abstractmethod


class SplineFunction(ABC):
    """Abstract base class for learnable spline functions"""
    
    @abstractmethod
    def evaluate(self, feature_vector: np.ndarray) -> 'CachedGlyph':
        """Transform input features into usable glyph/ritual/mask"""
        pass
    
    @abstractmethod
    def compute_gradient(self, feature_vector: np.ndarray) -> np.ndarray:
        """Compute gradient for learning updates"""
        pass
    
    @abstractmethod
    def update_parameters(self, gradient: np.ndarray, learning_rate: float):
        """Update spline parameters based on gradient"""
        pass


class LearnableSplineFunction(SplineFunction):
    """Concrete implementation of learnable spline function"""
    
    def __init__(self, input_dim: int, spline_order: int = 3, grid_size: int = 5):
        self.input_dim = input_dim
        self.spline_order = spline_order
        self.grid_size = grid_size
        
        # Initialize B-spline coefficients randomly
        self.coefficients = np.random.randn(grid_size, input_dim) * 0.1
        self.knot_vector = np.linspace(0, 1, grid_size + spline_order + 1)
        
    def evaluate(self, feature_vector: np.ndarray) -> 'CachedGlyph':
        """Evaluate spline at given feature vector"""
        # Simplified B-spline evaluation
        output_value = np.sum(self.coefficients * feature_vector[:self.input_dim])
        
        return CachedGlyph(
            glyph_type="spline_output",
            content={"value": float(output_value), "features": feature_vector.tolist()},
            confidence=min(1.0, abs(output_value)),
            entropy_level=0.3,
            interpretable_explanation=f"Spline evaluated to {output_value:.3f}",
            activation_pattern={"primary": float(output_value)}
        )
    
    def compute_gradient(self, feature_vector: np.ndarray) -> np.ndarray:
        """Compute gradient for learning updates"""
        # Simplified gradient computation
        return feature_vector[:self.input_dim]
    
    def update_parameters(self, gradient: np.ndarray, learning_rate: float):
        """Update spline parameters based on gradient"""
        # Simple gradient descent update
        if len(gradient) >= self.input_dim:
            self.coefficients += learning_rate * gradient[:self.input_dim].reshape(-1, 1)


@dataclass
class CachedGlyph:
    """Output from a spline neuron computation"""
    glyph_type: str  # 'ritual', 'mask', 'sigil', 'fragment'
    content: Dict[str, Any]
    confidence: float
    entropy_level: float
    interpretable_explanation: str
    activation_pattern: Dict[str, float]


@dataclass
class SplineNeuron:
    """A Cairrn cache unit as a learnable spline function"""
    assemblage_id: str
    spline_function: SplineFunction
    input_features: List[str]  # ['desire', 'ritual', 'grief-sigil']
    activation_threshold: float
    entropy_level: float
    last_accessed: datetime
    access_count: int = 0
    learning_rate: float = 0.001
    
    def compute(self, feature_vector: np.ndarray) -> CachedGlyph:
        """Transform input features into usable glyph/ritual/mask"""
        self.last_accessed = datetime.now()
        self.access_count += 1
        return self.spline_function.evaluate(feature_vector)
    
    def compute_confidence(self, feature_vector: np.ndarray) -> float:
        """Compute confidence score for given input"""
        # Based on distance from training examples and activation strength
        relevance = np.dot(feature_vector, self._get_feature_weights())
        return min(1.0, max(0.0, relevance / self.activation_threshold))
    
    def _get_feature_weights(self) -> np.ndarray:
        """Get current feature weights from spline function"""
        # This would be implemented based on specific spline function type
        return np.ones(len(self.input_features))


@dataclass 
class KANTopology:
    """Network structure mirroring Dawn's threading architecture"""
    spline_neurons: Dict[str, SplineNeuron]
    connection_graph: nx.DiGraph
    thread_routing_matrix: np.ndarray
    global_entropy: float
    entropy_threshold: float = 0.7
    last_updated: datetime = datetime.now()
    
    def get_active_splines(self, active_spline_ids: List[str]) -> Dict[str, SplineNeuron]:
        """Get spline neurons that are currently active"""
        return {sid: self.spline_neurons[sid] 
                for sid in active_spline_ids 
                if sid in self.spline_neurons}
    
    def update_global_entropy(self):
        """Recalculate global entropy based on all neurons"""
        if not self.spline_neurons:
            self.global_entropy = 0.0
            return
        
        entropies = [neuron.entropy_level for neuron in self.spline_neurons.values()]
        self.global_entropy = np.mean(entropies)
        self.last_updated = datetime.now()
    
    def get_activation_snapshot(self) -> Dict[str, float]:
        """Get current activation levels for all neurons"""
        return {
            neuron_id: neuron.entropy_level 
            for neuron_id, neuron in self.spline_neurons.items()
        }


@dataclass
class NavigationStep:
    """Single step in navigation through function space"""
    neuron_id: str
    input_features: np.ndarray
    spline_output: CachedGlyph
    interpretation: str
    confidence: float
    timestamp: datetime = datetime.now()


@dataclass
class FunctionPath:
    """Trajectory through spline space"""
    visited_neurons: List[str]
    gradient_history: List[np.ndarray]
    activation_patterns: List[Dict[str, float]]
    semantic_momentum: np.ndarray
    path_confidence: float = 0.0
    total_steps: int = 0
    
    def add_step(self, neuron_id: str, gradient: np.ndarray, 
                 activations: Dict[str, float]):
        """Add a navigation step to the path"""
        self.visited_neurons.append(neuron_id)
        self.gradient_history.append(gradient)
        self.activation_patterns.append(activations)
        self.total_steps += 1
        
        # Update semantic momentum (exponential moving average)
        alpha = 0.3
        if len(self.gradient_history) == 1:
            self.semantic_momentum = gradient
        else:
            self.semantic_momentum = (alpha * gradient + 
                                    (1 - alpha) * self.semantic_momentum)


@dataclass
class CursorState:
    """Cursor position in interpretable function space"""
    active_splines: List[str]
    current_feature_vector: np.ndarray
    navigation_trajectory: FunctionPath
    interpretation_context: Dict[str, Any]
    confidence_scores: Dict[str, float]
    session_id: str
    last_updated: datetime = datetime.now()
    
    def update_position(self, new_feature_vector: np.ndarray, 
                       active_splines: List[str]):
        """Update cursor position in function space"""
        self.current_feature_vector = new_feature_vector
        self.active_splines = active_splines
        self.last_updated = datetime.now()


@dataclass
class NavigationResult:
    """Result of navigation through spline space"""
    steps: List[NavigationStep]
    final_state: CursorState
    interpretation_summary: str
    navigation_success: bool
    total_confidence: float
    execution_time: float
    
    @property
    def path_length(self) -> int:
        return len(self.steps)
    
    @property
    def average_confidence(self) -> float:
        if not self.steps:
            return 0.0
        return np.mean([step.confidence for step in self.steps])


# Configuration classes
@dataclass
class KANConfig:
    """Configuration for KAN topology"""
    num_layers: int = 4
    neurons_per_layer: List[int] = None
    spline_order: int = 3
    grid_size: int = 5
    sparse_threshold: float = 0.01
    entropy_decay_rate: float = 0.95
    interpretability_weight: float = 0.3
    
    def __post_init__(self):
        if self.neurons_per_layer is None:
            self.neurons_per_layer = [64, 128, 128, 64]


@dataclass
class CairrConfig:
    """Configuration for Cairrn cache settings"""
    max_cached_assemblages: int = 1000
    activation_threshold: float = 0.1
    entropy_cleanup_interval: int = 3600  # 1 hour
    spline_update_learning_rate: float = 0.001
    feature_vector_dim: int = 256
    cache_decay_rate: float = 0.95
    max_access_count: int = 1000 