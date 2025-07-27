#!/usr/bin/env python3
import json
import time
import random
import math
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class CreativeState:
    """Current state of the creative system"""
    inspiration_level: float = 0.0
    novelty: float = 0.0
    coherence: float = 0.0
    last_idea_time: float = field(default_factory=time.time)
    idea_history: List[Dict] = field(default_factory=list)
    active_concepts: List[str] = field(default_factory=list)

class CreativityEngine:
    """Manages DAWN's creative processes and idea generation"""
    
    def __init__(self):
        """Initialize the creativity engine"""
        self.state = CreativeState()
        self.config = {
            'max_concepts': 10,
            'inspiration_decay': 0.95,
            'novelty_threshold': 0.7,
            'coherence_threshold': 0.6,
            'idea_generation_interval': 5.0
        }
        logger.info("Initialized CreativityEngine")
    
    def update_creative_state(self,
                            inspiration: Optional[float] = None,
                            novelty: Optional[float] = None,
                            coherence: Optional[float] = None) -> None:
        """
        Update the current creative state
        
        Args:
            inspiration: New inspiration level (0 to 1)
            novelty: New novelty level (0 to 1)
            coherence: New coherence level (0 to 1)
        """
        # Update values if provided
        if inspiration is not None:
            self.state.inspiration_level = max(0.0, min(1.0, inspiration))
        if novelty is not None:
            self.state.novelty = max(0.0, min(1.0, novelty))
        if coherence is not None:
            self.state.coherence = max(0.0, min(1.0, coherence))
        
        # Record state
        self._record_state()
        
        # Check for creative opportunities
        self._check_creative_opportunities()
    
    def _record_state(self) -> None:
        """Record current state in history"""
        state_record = {
            'timestamp': time.time(),
            'inspiration': self.state.inspiration_level,
            'novelty': self.state.novelty,
            'coherence': self.state.coherence,
            'concepts': self.state.active_concepts.copy()
        }
        
        self.state.idea_history.append(state_record)
        
        # Trim history if too long
        if len(self.state.idea_history) > 100:
            self.state.idea_history = self.state.idea_history[-100:]
    
    def _check_creative_opportunities(self) -> None:
        """Check for opportunities to generate new ideas"""
        # Check if enough time has passed
        time_since_last = time.time() - self.state.last_idea_time
        if time_since_last < self.config['idea_generation_interval']:
            return
        
        # Check if conditions are right for idea generation
        if (self.state.inspiration_level > 0.7 and
            self.state.novelty > self.config['novelty_threshold'] and
            self.state.coherence > self.config['coherence_threshold']):
            
            # Generate new idea
            self._generate_idea()
    
    def _generate_idea(self) -> None:
        """Generate a new creative idea"""
        # Update last idea time
        self.state.last_idea_time = time.time()
        
        # Generate idea based on current state
        idea = {
            'timestamp': time.time(),
            'inspiration': self.state.inspiration_level,
            'novelty': self.state.novelty,
            'coherence': self.state.coherence,
            'concepts': self.state.active_concepts.copy()
        }
        
        # Add to history
        self.state.idea_history.append(idea)
        
        # Log significant ideas
        if idea['novelty'] > 0.8 and idea['coherence'] > 0.8:
            logger.info(f"Generated significant idea: novelty={idea['novelty']:.2f}, coherence={idea['coherence']:.2f}")
    
    def add_concept(self, concept: str) -> None:
        """
        Add a new concept to active concepts
        
        Args:
            concept: The concept to add
        """
        if concept not in self.state.active_concepts:
            self.state.active_concepts.append(concept)
            
            # Trim if too many concepts
            if len(self.state.active_concepts) > self.config['max_concepts']:
                self.state.active_concepts = self.state.active_concepts[-self.config['max_concepts']:]
    
    def remove_concept(self, concept: str) -> None:
        """
        Remove a concept from active concepts
        
        Args:
            concept: The concept to remove
        """
        if concept in self.state.active_concepts:
            self.state.active_concepts.remove(concept)
    
    def get_state(self) -> Dict:
        """Get current creative state"""
        return {
            'inspiration': self.state.inspiration_level,
            'novelty': self.state.novelty,
            'coherence': self.state.coherence,
            'active_concepts': self.state.active_concepts.copy(),
            'last_idea_time': self.state.last_idea_time
        }
    
    def get_idea_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get idea generation history"""
        if limit is None:
            return self.state.idea_history
        return self.state.idea_history[-limit:]
    
    def process_creative_input(self, input_data: Dict[str, Any]) -> None:
        """
        Process creative input data and update state
        
        Args:
            input_data: Dictionary containing creative metrics and concepts
        """
        # Extract metrics
        inspiration = input_data.get('inspiration', 0.0)
        novelty = input_data.get('novelty', 0.0)
        coherence = input_data.get('coherence', 0.0)
        
        # Extract concepts
        concepts = input_data.get('concepts', [])
        
        # Update state
        self.update_creative_state(inspiration, novelty, coherence)
        
        # Update concepts
        for concept in concepts:
            self.add_concept(concept)
        
        # Log significant creative states
        if inspiration > 0.8 or (novelty > 0.8 and coherence > 0.8):
            logger.info(f"Significant creative state: inspiration={inspiration:.2f}, novelty={novelty:.2f}, coherence={coherence:.2f}")

# Global instance
_creativity_engine = None

def get_creativity_engine() -> CreativityEngine:
    """Get or create the global creativity engine instance"""
    global _creativity_engine
    if _creativity_engine is None:
        _creativity_engine = CreativityEngine()
    return _creativity_engine

__all__ = ['CreativityEngine', 'get_creativity_engine']

def main():
    """Dummy subprocess for Creativity Engine"""
    metrics = {
        "creativity_index": {
                "value": 72.3,
                "unit": "%"
        },
        "novelty": {
                "value": 68.9,
                "unit": "%"
        },
        "divergence": {
                "value": 81.2,
                "unit": "%"
        }
}
    
    t = 0
    while True:
        # Update metrics with some variation
        current_metrics = {}
        
        for metric_name, metric_info in metrics.items():
            base_value = metric_info["value"]
            unit = metric_info["unit"]
            
            if unit == "%":
                # Oscillate between bounds
                variation = math.sin(t * 0.1) * 10 + random.uniform(-2, 2)
                value = max(0, min(100, base_value + variation))
            else:
                # Random walk
                variation = random.uniform(-0.1, 0.1) * base_value
                value = max(0, base_value + variation)
            
            current_metrics[metric_name] = value
        
        # Output metrics as JSON
        print(json.dumps({
            "type": "metrics",
            "subprocess_id": "creativity_engine",
            "metrics": current_metrics,
            "timestamp": time.time()
        }))
        
        time.sleep(0.5)  # Update every 500ms
        t += 0.5

if __name__ == "__main__":
    main()
