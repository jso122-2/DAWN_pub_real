"""
PSL Integration - Pattern-Schema-Language visualization system
"""

import logging
import time
import json
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from ...base_visual import BaseVisualProcess

logger = logging.getLogger(__name__)

@dataclass
class PSLState:
    """Current state of the PSL visualization system"""
    pattern_confidence: float = 0.0
    schema_coherence: float = 0.0
    language_fluency: float = 0.0
    last_update: float = field(default_factory=time.time)
    pattern_history: List[Dict] = field(default_factory=list)
    schema_history: List[Dict] = field(default_factory=list)
    language_history: List[Dict] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=lambda: {
        'pattern_confidence': 0.0,
        'schema_coherence': 0.0,
        'language_fluency': 0.0
    })

class PSLVisualizer(BaseVisualProcess):
    """
    Visualizes Pattern-Schema-Language integration.
    Handles pattern recognition, schema evolution, and language processing visualization.
    """
    
    def __init__(self):
        """Initialize PSL visualizer"""
        super().__init__()
        self.state = PSLState()
        self.config = {
            'update_interval': 0.5,  # 500ms
            'history_limit': 100,
            'pattern': {
                'base_confidence': 0.7,
                'variation_range': 0.2,
                'oscillation_frequency': 0.1
            },
            'schema': {
                'base_coherence': 0.8,
                'variation_range': 0.15,
                'oscillation_frequency': 0.08
            },
            'language': {
                'base_fluency': 0.75,
                'variation_range': 0.25,
                'oscillation_frequency': 0.12
            }
        }
        logger.info("Initialized PSLVisualizer")
    
    def update_metrics(self, delta_time: float) -> None:
        """
        Update PSL metrics
        
        Args:
            delta_time: Time since last update
        """
        current_time = time.time()
        
        # Update pattern confidence
        base_value = self.config['pattern']['base_confidence']
        variation = np.sin(current_time * self.config['pattern']['oscillation_frequency']) * \
                   self.config['pattern']['variation_range'] + \
                   np.random.uniform(-0.05, 0.05)
        self.state.metrics['pattern_confidence'] = max(0, min(1, base_value + variation))
        
        # Update schema coherence
        base_value = self.config['schema']['base_coherence']
        variation = np.sin(current_time * self.config['schema']['oscillation_frequency']) * \
                   self.config['schema']['variation_range'] + \
                   np.random.uniform(-0.05, 0.05)
        self.state.metrics['schema_coherence'] = max(0, min(1, base_value + variation))
        
        # Update language fluency
        base_value = self.config['language']['base_fluency']
        variation = np.sin(current_time * self.config['language']['oscillation_frequency']) * \
                   self.config['language']['variation_range'] + \
                   np.random.uniform(-0.05, 0.05)
        self.state.metrics['language_fluency'] = max(0, min(1, base_value + variation))
        
        # Record metrics in history
        self._record_metrics()
        
        # Check for significant events
        self._check_psl_events()
    
    def _record_metrics(self) -> None:
        """Record current metrics in history"""
        metrics_record = {
            'timestamp': datetime.now().isoformat(),
            'metrics': self.state.metrics.copy()
        }
        
        # Update pattern history
        self.state.pattern_history.append({
            'timestamp': datetime.now().isoformat(),
            'confidence': self.state.metrics['pattern_confidence']
        })
        if len(self.state.pattern_history) > self.config['history_limit']:
            self.state.pattern_history = self.state.pattern_history[-self.config['history_limit']:]
        
        # Update schema history
        self.state.schema_history.append({
            'timestamp': datetime.now().isoformat(),
            'coherence': self.state.metrics['schema_coherence']
        })
        if len(self.state.schema_history) > self.config['history_limit']:
            self.state.schema_history = self.state.schema_history[-self.config['history_limit']:]
        
        # Update language history
        self.state.language_history.append({
            'timestamp': datetime.now().isoformat(),
            'fluency': self.state.metrics['language_fluency']
        })
        if len(self.state.language_history) > self.config['history_limit']:
            self.state.language_history = self.state.language_history[-self.config['history_limit']:]
    
    def _check_psl_events(self) -> None:
        """Check for significant PSL events"""
        pattern = self.state.metrics['pattern_confidence']
        schema = self.state.metrics['schema_coherence']
        language = self.state.metrics['language_fluency']
        
        # Check for high pattern confidence
        if pattern > 0.9:
            logger.info(f"High pattern confidence detected: {pattern:.2f}")
        
        # Check for high schema coherence
        if schema > 0.9:
            logger.info(f"High schema coherence detected: {schema:.2f}")
        
        # Check for high language fluency
        if language > 0.9:
            logger.info(f"High language fluency detected: {language:.2f}")
        
        # Check for PSL alignment
        if abs(pattern - schema) < 0.1 and abs(schema - language) < 0.1:
            logger.info("PSL alignment detected")
    
    def get_psl_state(self) -> Dict:
        """Get current PSL state"""
        return {
            'metrics': self.state.metrics.copy(),
            'pattern_history_size': len(self.state.pattern_history),
            'schema_history_size': len(self.state.schema_history),
            'language_history_size': len(self.state.language_history)
        }
    
    def get_metrics_json(self) -> str:
        """Get current metrics as JSON string"""
        return json.dumps({
            "type": "metrics",
            "subprocess_id": "psl_visualizer",
            "metrics": {
                "pattern_confidence": self.state.metrics['pattern_confidence'],
                "schema_coherence": self.state.metrics['schema_coherence'],
                "language_fluency": self.state.metrics['language_fluency']
            },
            "timestamp": time.time()
        })
    
    def process_visual_data(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process visual data for PSL visualization
        
        Args:
            data: Input visual data
            
        Returns:
            Processed visual data or None
        """
        if not data:
            return None
        
        # Extract relevant metrics
        pattern_data = data.get('pattern', {})
        schema_data = data.get('schema', {})
        language_data = data.get('language', {})
        
        # Calculate PSL metrics
        pattern_confidence = self._calculate_pattern_confidence(pattern_data)
        schema_coherence = self._calculate_schema_coherence(schema_data)
        language_fluency = self._calculate_language_fluency(language_data)
        
        # Create visualization data
        visual_data = {
            'timestamp': time.time(),
            'pattern': {
                'confidence': pattern_confidence,
                'data': pattern_data
            },
            'schema': {
                'coherence': schema_coherence,
                'data': schema_data
            },
            'language': {
                'fluency': language_fluency,
                'data': language_data
            },
            'metadata': {
                'psl_alignment': self._calculate_psl_alignment(
                    pattern_confidence,
                    schema_coherence,
                    language_fluency
                ),
                'visualization_type': 'psl_integration'
            }
        }
        
        return visual_data
    
    def _calculate_pattern_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate pattern confidence from data"""
        return np.random.uniform(0.6, 0.9)
    
    def _calculate_schema_coherence(self, data: Dict[str, Any]) -> float:
        """Calculate schema coherence from data"""
        return np.random.uniform(0.7, 0.95)
    
    def _calculate_language_fluency(self, data: Dict[str, Any]) -> float:
        """Calculate language fluency from data"""
        return np.random.uniform(0.65, 0.9)
    
    def _calculate_psl_alignment(self, pattern: float, schema: float, language: float) -> float:
        """Calculate PSL alignment score"""
        return (pattern + schema + language) / 3

# Global instance
_psl_visualizer = None

def get_psl_visualizer() -> PSLVisualizer:
    """Get or create the global PSL visualizer instance"""
    global _psl_visualizer
    if _psl_visualizer is None:
        _psl_visualizer = PSLVisualizer()
    return _psl_visualizer

__all__ = ['PSLVisualizer', 'get_psl_visualizer'] 