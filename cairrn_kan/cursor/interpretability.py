"""
Spline Interpretability - Human-readable explanations of spline computations

This module provides interpretability for spline function operations, making
the KAN-Cairrn system transparent and auditable.
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
    from models import CachedGlyph, SplineNeuron, NavigationStep
except ImportError:
    # Fallback import structure
    from ..models import CachedGlyph, SplineNeuron, NavigationStep


class SplineInterpreter:
    """Interpreter for spline function operations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.interpretation_cache = {}
        self.feature_importance_threshold = 0.3
    
    def explain_spline_computation(self, neuron: SplineNeuron, 
                                 feature_vector: np.ndarray,
                                 spline_output: CachedGlyph) -> str:
        """Generate human-readable explanation of spline computation"""
        
        try:
            # Extract key information
            neuron_id = neuron.assemblage_id
            confidence = spline_output.confidence
            entropy = spline_output.entropy_level
            glyph_type = spline_output.glyph_type
            
            # Analyze feature contributions
            feature_contributions = self._analyze_feature_contributions(
                neuron, feature_vector, spline_output
            )
            
            # Generate natural language explanation
            explanation = self._generate_natural_explanation(
                neuron_id, confidence, entropy, glyph_type, feature_contributions
            )
            
            return explanation
            
        except Exception as e:
            self.logger.error(f"Failed to explain spline computation: {e}")
            return f"Spline {neuron.assemblage_id} activated with confidence {spline_output.confidence:.2f}"
    
    def _analyze_feature_contributions(self, neuron: SplineNeuron,
                                     feature_vector: np.ndarray,
                                     spline_output: CachedGlyph) -> Dict[str, float]:
        """Analyze which features contributed most to the spline output"""
        
        contributions = {}
        
        # Use activation pattern from spline output
        activation_pattern = spline_output.activation_pattern
        
        # Normalize contributions
        total_activation = sum(abs(v) for v in activation_pattern.values())
        
        if total_activation > 0:
            for feature, activation in activation_pattern.items():
                normalized_contribution = abs(activation) / total_activation
                contributions[feature] = normalized_contribution
        else:
            # Fallback to equal contributions
            for feature in neuron.input_features:
                contributions[feature] = 1.0 / len(neuron.input_features)
        
        return contributions
    
    def _generate_natural_explanation(self, neuron_id: str, confidence: float,
                                    entropy: float, glyph_type: str,
                                    feature_contributions: Dict[str, float]) -> str:
        """Generate natural language explanation"""
        
        # Start with neuron identification
        explanation = f"Spline neuron '{neuron_id}' "
        
        # Describe activation strength
        if confidence > 0.8:
            explanation += "strongly activated"
        elif confidence > 0.5:
            explanation += "moderately activated"
        elif confidence > 0.2:
            explanation += "weakly activated"
        else:
            explanation += "barely activated"
        
        # Add confidence and entropy context
        explanation += f" (confidence: {confidence:.2f}, entropy: {entropy:.2f}) "
        
        # Describe dominant features
        dominant_features = [
            feature for feature, contrib in feature_contributions.items()
            if contrib > self.feature_importance_threshold
        ]
        
        if dominant_features:
            if len(dominant_features) == 1:
                explanation += f"primarily driven by '{dominant_features[0]}' "
            elif len(dominant_features) == 2:
                explanation += f"driven by '{dominant_features[0]}' and '{dominant_features[1]}' "
            else:
                explanation += f"driven by {len(dominant_features)} features including '{dominant_features[0]}' "
        
        # Describe output glyph type
        glyph_descriptions = {
            "sigil": "producing a high-intensity symbolic sigil",
            "ritual": "generating a moderate ritual pattern",
            "mask": "creating a low-intensity identity mask",
            "fragment": "outputting a minimal identity fragment"
        }
        
        explanation += glyph_descriptions.get(glyph_type, f"generating a {glyph_type}")
        
        # Add interpretation based on entropy
        if entropy > 0.8:
            explanation += " with high uncertainty"
        elif entropy > 0.5:
            explanation += " with moderate uncertainty"
        else:
            explanation += " with high certainty"
        
        return explanation + "."
    
    def explain_spline_activations(self, active_functions: Dict[str, SplineNeuron],
                                 current_feature_vector: np.ndarray) -> Dict[str, str]:
        """Explain activation of multiple spline functions"""
        
        explanations = {}
        
        for spline_id, neuron in active_functions.items():
            try:
                # Compute spline output
                spline_output = neuron.compute(current_feature_vector)
                
                # Generate explanation
                explanation = self.explain_spline_computation(
                    neuron, current_feature_vector, spline_output
                )
                
                explanations[spline_id] = explanation
                
            except Exception as e:
                self.logger.error(f"Failed to explain spline {spline_id}: {e}")
                explanations[spline_id] = f"Spline {spline_id} activated with unknown pattern"
        
        return explanations
    
    def explain_momentum(self, trajectory_momentum: np.ndarray) -> str:
        """Explain semantic momentum in human terms"""
        
        momentum_magnitude = np.linalg.norm(trajectory_momentum)
        
        if momentum_magnitude < 0.1:
            return "minimal semantic momentum - cursor is stationary"
        elif momentum_magnitude < 0.5:
            return "low semantic momentum - cursor moving slowly through function space"
        elif momentum_magnitude < 1.0:
            return "moderate semantic momentum - cursor navigating steadily"
        else:
            return "high semantic momentum - cursor moving rapidly through function space"
    
    def summarize_path(self, navigation_steps: List[NavigationStep]) -> str:
        """Summarize a complete navigation path"""
        
        if not navigation_steps:
            return "No navigation steps taken."
        
        # Analyze path characteristics
        total_steps = len(navigation_steps)
        avg_confidence = np.mean([step.confidence for step in navigation_steps])
        
        # Identify dominant patterns
        glyph_types = [step.spline_output.glyph_type for step in navigation_steps]
        dominant_glyph = max(set(glyph_types), key=glyph_types.count)
        
        # Generate summary
        summary = f"Navigation completed in {total_steps} steps "
        summary += f"with average confidence {avg_confidence:.2f}. "
        
        # Describe trajectory pattern
        if avg_confidence > 0.7:
            summary += "Path showed high confidence throughout, "
        elif avg_confidence > 0.4:
            summary += "Path showed moderate confidence, "
        else:
            summary += "Path showed low confidence, "
        
        summary += f"predominantly generating {dominant_glyph} patterns. "
        
        # Describe confidence trend
        if len(navigation_steps) > 1:
            confidence_trend = (navigation_steps[-1].confidence - 
                              navigation_steps[0].confidence)
            
            if confidence_trend > 0.1:
                summary += "Confidence increased during navigation."
            elif confidence_trend < -0.1:
                summary += "Confidence decreased during navigation."
            else:
                summary += "Confidence remained stable during navigation."
        
        return summary
    
    def explain_global_state(self, activation_map: Dict[str, float]) -> Dict[str, Any]:
        """Explain the global state of the KAN system"""
        
        if not activation_map:
            return {
                "status": "No active splines",
                "interpretation": "KAN system is dormant"
            }
        
        # Analyze activation patterns
        total_activations = len(activation_map)
        active_splines = sum(1 for level in activation_map.values() if level > 0.1)
        avg_activation = np.mean(list(activation_map.values()))
        max_activation = max(activation_map.values())
        
        # Identify highly active splines
        highly_active = [
            spline_id for spline_id, level in activation_map.items()
            if level > 0.7
        ]
        
        # Generate interpretation
        interpretation = {
            "total_splines": total_activations,
            "active_splines": active_splines,
            "average_activation": avg_activation,
            "max_activation": max_activation,
            "highly_active_splines": highly_active,
            "activity_level": self._classify_activity_level(avg_activation),
            "interpretation": self._generate_global_interpretation(
                avg_activation, active_splines, total_activations
            )
        }
        
        return interpretation
    
    def _classify_activity_level(self, avg_activation: float) -> str:
        """Classify the overall activity level of the system"""
        
        if avg_activation > 0.8:
            return "high"
        elif avg_activation > 0.5:
            return "moderate"
        elif avg_activation > 0.2:
            return "low"
        else:
            return "minimal"
    
    def _generate_global_interpretation(self, avg_activation: float,
                                      active_splines: int,
                                      total_splines: int) -> str:
        """Generate global system interpretation"""
        
        activation_ratio = active_splines / total_splines if total_splines > 0 else 0
        
        interpretation = f"KAN system shows {self._classify_activity_level(avg_activation)} activity "
        interpretation += f"with {active_splines}/{total_splines} splines active. "
        
        if activation_ratio > 0.7:
            interpretation += "High concurrent activation suggests complex processing."
        elif activation_ratio > 0.4:
            interpretation += "Moderate activation indicates focused processing."
        elif activation_ratio > 0.1:
            interpretation += "Low activation suggests selective processing."
        else:
            interpretation += "Minimal activation indicates system in standby."
        
        return interpretation
    
    def generate_spline_report(self, neuron: SplineNeuron) -> Dict[str, Any]:
        """Generate comprehensive report for a single spline neuron"""
        
        report = {
            "neuron_id": neuron.assemblage_id,
            "input_features": neuron.input_features,
            "activation_threshold": neuron.activation_threshold,
            "entropy_level": neuron.entropy_level,
            "access_count": neuron.access_count,
            "last_accessed": neuron.last_accessed.isoformat(),
            "learning_rate": neuron.learning_rate,
            "status": self._classify_neuron_status(neuron),
            "recommendations": self._generate_neuron_recommendations(neuron)
        }
        
        return report
    
    def _classify_neuron_status(self, neuron: SplineNeuron) -> str:
        """Classify the status of a spline neuron"""
        
        if neuron.entropy_level > 0.8:
            return "high_entropy"
        elif neuron.access_count < 5:
            return "underutilized"
        elif neuron.access_count > 1000:
            return "overused"
        elif neuron.entropy_level < 0.2:
            return "well_trained"
        else:
            return "healthy"
    
    def _generate_neuron_recommendations(self, neuron: SplineNeuron) -> List[str]:
        """Generate recommendations for neuron optimization"""
        
        recommendations = []
        
        if neuron.entropy_level > 0.8:
            recommendations.append("Consider retraining or pruning due to high entropy")
        
        if neuron.access_count < 5:
            recommendations.append("Neuron may be underutilized - consider feature adjustment")
        
        if neuron.access_count > 1000:
            recommendations.append("High usage neuron - consider splitting or caching")
        
        if neuron.activation_threshold > 0.8:
            recommendations.append("High activation threshold may limit neuron utility")
        
        if not recommendations:
            recommendations.append("Neuron operating within normal parameters")
        
        return recommendations 