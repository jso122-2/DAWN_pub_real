"""
Spline Neurons - Cairrn units as learnable spline functions

This module implements the core spline neuron functionality where cached assemblages
are represented as interpretable spline functions.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from models import SplineFunction, CachedGlyph, SplineNeuron
except ImportError:
    # Fallback import structure
    from ..models import SplineFunction, CachedGlyph, SplineNeuron


class LearnableSplineFunction(SplineFunction):
    """Learnable B-spline function for assemblage caching"""
    
    def __init__(self, input_dim: int, spline_order: int = 3, 
                 grid_size: int = 5, feature_names: List[str] = None):
        self.input_dim = input_dim
        self.spline_order = spline_order
        self.grid_size = grid_size
        self.feature_names = feature_names or [f"feature_{i}" for i in range(input_dim)]
        
        # Initialize B-spline parameters
        self.knots = self._create_knot_vectors()
        self.coefficients = self._initialize_coefficients()
        self.training_examples = []
        self.last_updated = datetime.now()
        
    def _create_knot_vectors(self) -> List[np.ndarray]:
        """Create knot vectors for each input dimension"""
        knots = []
        for _ in range(self.input_dim):
            # Create uniform knot vector
            knot_vector = np.linspace(0, 1, self.grid_size + self.spline_order + 1)
            knots.append(knot_vector)
        return knots
    
    def _initialize_coefficients(self) -> np.ndarray:
        """Initialize spline coefficients randomly"""
        # Multi-dimensional coefficient tensor
        coeff_shape = [self.grid_size] * self.input_dim + [4]  # 4D output
        return np.random.normal(0, 0.1, coeff_shape)
    
    def evaluate(self, feature_vector: np.ndarray) -> CachedGlyph:
        """Transform input features into cached glyph"""
        # Normalize feature vector to [0, 1]
        normalized_features = self._normalize_features(feature_vector)
        
        # Evaluate spline function
        spline_output = self._evaluate_spline(normalized_features)
        
        # Extract components
        confidence = self._sigmoid(spline_output[0])
        entropy_level = self._sigmoid(spline_output[1])
        activation_strength = self._sigmoid(spline_output[2])
        interpretation_score = self._sigmoid(spline_output[3])
        
        # Generate interpretable explanation
        explanation = self._generate_explanation(
            normalized_features, spline_output, activation_strength
        )
        
        # Create activation pattern
        activation_pattern = {
            name: float(normalized_features[i] * activation_strength)
            for i, name in enumerate(self.feature_names)
        }
        
        # Determine glyph type based on activation pattern
        glyph_type = self._classify_glyph_type(activation_pattern)
        
        return CachedGlyph(
            glyph_type=glyph_type,
            content={
                "raw_output": spline_output.tolist(),
                "normalized_input": normalized_features.tolist(),
                "feature_names": self.feature_names,
                "spline_metadata": {
                    "grid_size": self.grid_size,
                    "spline_order": self.spline_order,
                    "last_updated": self.last_updated.isoformat()
                }
            },
            confidence=confidence,
            entropy_level=entropy_level,
            interpretable_explanation=explanation,
            activation_pattern=activation_pattern
        )
    
    def compute_gradient(self, feature_vector: np.ndarray) -> np.ndarray:
        """Compute gradient for learning updates"""
        h = 1e-6  # Small perturbation for numerical gradient
        normalized_features = self._normalize_features(feature_vector)
        
        base_output = self._evaluate_spline(normalized_features)
        gradients = []
        
        for i in range(len(normalized_features)):
            # Perturb each dimension
            perturbed_features = normalized_features.copy()
            perturbed_features[i] += h
            perturbed_output = self._evaluate_spline(perturbed_features)
            
            # Numerical gradient
            gradient = (perturbed_output - base_output) / h
            gradients.append(gradient)
        
        return np.array(gradients)
    
    def update_parameters(self, gradient: np.ndarray, learning_rate: float):
        """Update spline parameters based on gradient"""
        # Apply gradient update to coefficients
        coeff_gradient = self._compute_coefficient_gradient(gradient)
        self.coefficients -= learning_rate * coeff_gradient
        self.last_updated = datetime.now()
    
    def _normalize_features(self, features: np.ndarray) -> np.ndarray:
        """Normalize features to [0, 1] range"""
        return np.clip((features + 1) / 2, 0, 1)
    
    def _evaluate_spline(self, normalized_features: np.ndarray) -> np.ndarray:
        """Evaluate the multi-dimensional B-spline"""
        result = np.zeros(4)
        
        for i in range(4):  # 4 output dimensions
            # Compute weighted sum of basis functions
            weights = self._compute_basis_weights(normalized_features)
            coeff_slice = self.coefficients[..., i].flatten()
            result[i] = np.dot(weights, coeff_slice[:len(weights)])
        
        return result
    
    def _compute_basis_weights(self, features: np.ndarray) -> np.ndarray:
        """Compute B-spline basis function weights"""
        n_basis = min(self.grid_size ** self.input_dim, 1000)  # Cap for performance
        weights = np.ones(n_basis)
        
        # Apply feature influence
        for i, feature_val in enumerate(features):
            centers = np.linspace(0, 1, self.grid_size)
            for j, center in enumerate(centers):
                if j >= len(weights):
                    break
                distance = abs(feature_val - center)
                weight = np.exp(-distance ** 2 / 0.1)
                weights[j] *= weight
        
        # Normalize weights
        return weights / (np.sum(weights) + 1e-8)
    
    def _compute_coefficient_gradient(self, output_gradient: np.ndarray) -> np.ndarray:
        """Compute gradient with respect to coefficients"""
        grad_shape = self.coefficients.shape
        gradient = np.random.normal(0, 0.01, grad_shape)  # Placeholder
        return gradient
    
    def _sigmoid(self, x: float) -> float:
        """Sigmoid activation function"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def _generate_explanation(self, features: np.ndarray, 
                            spline_output: np.ndarray, 
                            activation: float) -> str:
        """Generate human-readable explanation of spline computation"""
        dominant_features = []
        for i, (name, value) in enumerate(zip(self.feature_names, features)):
            if value > 0.5:  # Threshold for significance
                dominant_features.append(f"{name}({value:.2f})")
        
        if not dominant_features:
            dominant_features = ["low activation"]
        
        explanation = f"Spline activated by {', '.join(dominant_features)} → "
        explanation += f"confidence={self._sigmoid(spline_output[0]):.2f}, "
        explanation += f"entropy={self._sigmoid(spline_output[1]):.2f}, "
        explanation += f"strength={activation:.2f}"
        
        return explanation
    
    def _classify_glyph_type(self, activation_pattern: Dict[str, float]) -> str:
        """Classify the type of glyph based on activation pattern"""
        max_activation = max(activation_pattern.values()) if activation_pattern else 0
        
        if max_activation > 0.8:
            return "sigil"
        elif max_activation > 0.6:
            return "ritual"
        elif max_activation > 0.4:
            return "mask"
        else:
            return "fragment"


class SplineNeuronManager:
    """Manager for collections of spline neurons"""
    
    def __init__(self, feature_dim: int = 256):
        self.feature_dim = feature_dim
        self.neurons: Dict[str, SplineNeuron] = {}
        self.access_log: List[Tuple[str, datetime]] = []
        self.logger = logging.getLogger(__name__)
    
    def create_neuron(self, assemblage_id: str, input_features: List[str],
                     activation_threshold: float = 0.1) -> SplineNeuron:
        """Create a new spline neuron"""
        spline_function = LearnableSplineFunction(
            input_dim=len(input_features),
            feature_names=input_features
        )
        
        neuron = SplineNeuron(
            assemblage_id=assemblage_id,
            spline_function=spline_function,
            input_features=input_features,
            activation_threshold=activation_threshold,
            entropy_level=0.5,  # Initial entropy
            last_accessed=datetime.now()
        )
        
        self.neurons[assemblage_id] = neuron
        self.logger.info(f"Created spline neuron: {assemblage_id}")
        return neuron
    
    def get_neuron(self, assemblage_id: str) -> Optional[SplineNeuron]:
        """Retrieve a spline neuron by ID"""
        return self.neurons.get(assemblage_id)
    
    def activate_neuron(self, assemblage_id: str, 
                       feature_vector: np.ndarray) -> Optional[CachedGlyph]:
        """Activate a spline neuron with given features"""
        neuron = self.neurons.get(assemblage_id)
        if not neuron:
            return None
        
        # Check activation threshold
        confidence = neuron.compute_confidence(feature_vector)
        if confidence < neuron.activation_threshold:
            return None
        
        # Compute output
        result = neuron.compute(feature_vector)
        
        # Log access
        self.access_log.append((assemblage_id, datetime.now()))
        
        return result
    
    def update_neuron_learning(self, assemblage_id: str, 
                              feature_vector: np.ndarray,
                              target_output: CachedGlyph,
                              learning_rate: float = 0.001):
        """Update neuron parameters based on training example"""
        neuron = self.neurons.get(assemblage_id)
        if not neuron:
            return
        
        # Compute gradient based on target
        gradient = neuron.spline_function.compute_gradient(feature_vector)
        
        # Update parameters
        neuron.spline_function.update_parameters(gradient, learning_rate)
        
        # Update entropy based on prediction error
        current_output = neuron.compute(feature_vector)
        error = abs(current_output.confidence - target_output.confidence)
        neuron.entropy_level = 0.9 * neuron.entropy_level + 0.1 * error
    
    def prune_neurons(self, entropy_threshold: float = 0.8,
                     access_threshold: int = 10) -> List[str]:
        """Remove neurons with high entropy or low access"""
        to_remove = []
        
        for assemblage_id, neuron in self.neurons.items():
            if (neuron.entropy_level > entropy_threshold or 
                neuron.access_count < access_threshold):
                to_remove.append(assemblage_id)
        
        for assemblage_id in to_remove:
            del self.neurons[assemblage_id]
            self.logger.info(f"Pruned neuron: {assemblage_id}")
        
        return to_remove
    
    def get_neuron_stats(self) -> Dict[str, Any]:
        """Get statistics about managed neurons"""
        if not self.neurons:
            return {"total_neurons": 0}
        
        entropies = [n.entropy_level for n in self.neurons.values()]
        access_counts = [n.access_count for n in self.neurons.values()]
        
        return {
            "total_neurons": len(self.neurons),
            "avg_entropy": np.mean(entropies),
            "max_entropy": np.max(entropies),
            "avg_access_count": np.mean(access_counts),
            "total_accesses": sum(access_counts),
            "recent_accesses": len([log for log in self.access_log 
                                  if (datetime.now() - log[1]).seconds < 3600])
        } 