"""
Schema Calculator - Handles calculation of schema metrics and evolution
"""

import logging
import math
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class SchemaMetrics:
    """Schema metrics calculation results"""
    coherence: float
    entropy: float
    drift: float
    tension: float
    stability: float
    complexity: float
    alignment: float
    resonance: float

class SchemaCalculator:
    """Calculates schema metrics and handles schema evolution"""
    
    def __init__(self):
        """Initialize schema calculator"""
        self.metrics_history: List[SchemaMetrics] = []
        self.evolution_threshold = 0.7
        self.stability_threshold = 0.5
        logger.info("Initialized SchemaCalculator")
    
    async def calculate_metrics(self, state: Dict[str, Any]) -> Dict[str, float]:
        """Calculate schema metrics based on current state"""
        try:
            # Calculate base metrics
            coherence = self._calculate_coherence(state)
            entropy = self._calculate_entropy(state)
            drift = self._calculate_drift(state)
            tension = self._calculate_tension(state)
            
            # Calculate derived metrics
            stability = self._calculate_stability(coherence, entropy)
            complexity = self._calculate_complexity(state)
            alignment = self._calculate_alignment(state)
            resonance = self._calculate_resonance(state)
            
            # Create metrics object
            metrics = SchemaMetrics(
                coherence=coherence,
                entropy=entropy,
                drift=drift,
                tension=tension,
                stability=stability,
                complexity=complexity,
                alignment=alignment,
                resonance=resonance
            )
            
            # Store in history
            self.metrics_history.append(metrics)
            
            # Return as dictionary
            return {
                'coherence': coherence,
                'entropy': entropy,
                'drift': drift,
                'tension': tension,
                'stability': stability,
                'complexity': complexity,
                'alignment': alignment,
                'resonance': resonance
            }
            
        except Exception as e:
            logger.error(f"Error calculating schema metrics: {e}")
            return {
                'coherence': 0.5,
                'entropy': 0.5,
                'drift': 0.0,
                'tension': 0.0,
                'stability': 0.5,
                'complexity': 0.5,
                'alignment': 0.5,
                'resonance': 0.5
            }
    
    def _calculate_coherence(self, state: Dict[str, Any]) -> float:
        """Calculate schema coherence"""
        try:
            active_blooms = state.get('active_blooms', 0)
            sealed_blooms = state.get('sealed_blooms', 0)
            total_blooms = active_blooms + sealed_blooms
            
            if total_blooms == 0:
                return 0.5
                
            coherence = (sealed_blooms / total_blooms) * 0.7 + \
                       (state.get('rebloom_stability', 0.5) * 0.3)
            
            return min(max(coherence, 0.0), 1.0)
        except Exception as e:
            logger.error(f"Error calculating coherence: {e}")
            return 0.5
    
    def _calculate_entropy(self, state: Dict[str, Any]) -> float:
        """Calculate schema entropy"""
        try:
            preview_entropy = state.get('preview_entropy', 0.5)
            drift = state.get('drift', 0.0)
            
            entropy = (preview_entropy * 0.6) + (drift * 0.4)
            return min(max(entropy, 0.0), 1.0)
        except Exception as e:
            logger.error(f"Error calculating entropy: {e}")
            return 0.5
    
    def _calculate_drift(self, state: Dict[str, Any]) -> float:
        """Calculate schema drift"""
        try:
            if len(self.metrics_history) < 2:
                return 0.0
                
            current = self.metrics_history[-1]
            previous = self.metrics_history[-2]
            
            drift = abs(current.coherence - previous.coherence) * 0.4 + \
                   abs(current.entropy - previous.entropy) * 0.3 + \
                   abs(current.tension - previous.tension) * 0.3
                   
            return min(max(drift, 0.0), 1.0)
        except Exception as e:
            logger.error(f"Error calculating drift: {e}")
            return 0.0
    
    def _calculate_tension(self, state: Dict[str, Any]) -> float:
        """Calculate schema tension"""
        try:
            preview_heat = state.get('preview_heat', 0.0)
            preview_stability = state.get('preview_stability', 0.5)
            
            tension = (preview_heat * 0.7) + ((1 - preview_stability) * 0.3)
            return min(max(tension, 0.0), 1.0)
        except Exception as e:
            logger.error(f"Error calculating tension: {e}")
            return 0.0
    
    def _calculate_stability(self, coherence: float, entropy: float) -> float:
        """Calculate schema stability"""
        try:
            stability = (coherence * 0.6) + ((1 - entropy) * 0.4)
            return min(max(stability, 0.0), 1.0)
        except Exception as e:
            logger.error(f"Error calculating stability: {e}")
            return 0.5
    
    def _calculate_complexity(self, state: Dict[str, Any]) -> float:
        """Calculate schema complexity"""
        try:
            active_blooms = state.get('active_blooms', 0)
            sealed_blooms = state.get('sealed_blooms', 0)
            
            complexity = math.log2(max(active_blooms + sealed_blooms, 1)) / 10
            return min(max(complexity, 0.0), 1.0)
        except Exception as e:
            logger.error(f"Error calculating complexity: {e}")
            return 0.5
    
    def _calculate_alignment(self, state: Dict[str, Any]) -> float:
        """Calculate schema alignment"""
        try:
            coherence = state.get('coherence', 0.5)
            stability = state.get('rebloom_stability', 0.5)
            
            alignment = (coherence * 0.5) + (stability * 0.5)
            return min(max(alignment, 0.0), 1.0)
        except Exception as e:
            logger.error(f"Error calculating alignment: {e}")
            return 0.5
    
    def _calculate_resonance(self, state: Dict[str, Any]) -> float:
        """Calculate schema resonance"""
        try:
            coherence = state.get('coherence', 0.5)
            tension = state.get('tension', 0.0)
            
            resonance = (coherence * 0.7) + ((1 - tension) * 0.3)
            return min(max(resonance, 0.0), 1.0)
        except Exception as e:
            logger.error(f"Error calculating resonance: {e}")
            return 0.5
    
    def should_evolve(self, metrics: SchemaMetrics) -> bool:
        """Determine if schema should evolve based on metrics"""
        try:
            if metrics.stability < self.stability_threshold:
                return False
                
            evolution_score = (metrics.coherence * 0.3) + \
                            (metrics.complexity * 0.2) + \
                            (metrics.alignment * 0.3) + \
                            (metrics.resonance * 0.2)
                            
            return evolution_score >= self.evolution_threshold
        except Exception as e:
            logger.error(f"Error checking evolution: {e}")
            return False 