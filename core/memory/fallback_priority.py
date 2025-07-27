"""
Priority tree structure for fallback memory routing.
Implements efficient fallback chain selection based on system state.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import heapq
from enum import Enum

class FallbackCategory(Enum):
    GROUNDING = "grounding"
    STRUCTURAL = "structural"
    PHILOSOPHICAL = "philosophical"
    EMERGENCY = "emergency"

@dataclass
class FallbackNode:
    entry_id: str
    content: str
    stability_score: float
    trust_score: float
    category: FallbackCategory
    usage_count: int = 0
    priority_score: float = 0.0
    
    def __lt__(self, other):
        return self.priority_score > other.priority_score

class FallbackPriorityTree:
    def __init__(self):
        self.nodes: Dict[str, FallbackNode] = {}
        self.category_weights = {
            FallbackCategory.GROUNDING: 1.0,
            FallbackCategory.STRUCTURAL: 0.9,
            FallbackCategory.PHILOSOPHICAL: 0.8,
            FallbackCategory.EMERGENCY: 1.2
        }
        
    def add_node(self, node: FallbackNode):
        """Add a node to the priority tree."""
        self.nodes[node.entry_id] = node
        
    def update_priority_scores(self, coherence: float, entropy: float, 
                             pressure_zone: str):
        """Update priority scores for all nodes based on current state."""
        for node in self.nodes.values():
            # Base score from stability and trust
            base_score = (node.stability_score * 0.4 + 
                         node.trust_score * 0.3)
            
            # Category weight
            category_weight = self.category_weights[node.category]
            
            # State-based adjustments
            state_multiplier = self._calculate_state_multiplier(
                node.category, coherence, entropy, pressure_zone
            )
            
            # Usage penalty
            usage_penalty = min(node.usage_count * 0.01, 0.2)
            
            # Calculate final priority score
            node.priority_score = (base_score * category_weight * 
                                 state_multiplier * (1 - usage_penalty))
    
    def _calculate_state_multiplier(self, category: FallbackCategory,
                                  coherence: float, entropy: float,
                                  pressure_zone: str) -> float:
        """Calculate state-based multiplier for priority scoring."""
        multiplier = 1.0
        
        # Coherence-based adjustments
        if coherence < 0.4:  # Critical coherence
            if category == FallbackCategory.GROUNDING:
                multiplier *= 1.3
            elif category == FallbackCategory.EMERGENCY:
                multiplier *= 1.2
                
        # Entropy-based adjustments
        if entropy > 0.8:  # High entropy
            if category == FallbackCategory.STRUCTURAL:
                multiplier *= 1.3
            elif category == FallbackCategory.PHILOSOPHICAL:
                multiplier *= 1.2
                
        # Pressure zone adjustments
        if pressure_zone == "surge":
            if category in [FallbackCategory.GROUNDING, 
                          FallbackCategory.STRUCTURAL]:
                multiplier *= 1.2
        elif pressure_zone == "calm":
            if category == FallbackCategory.PHILOSOPHICAL:
                multiplier *= 1.1
                
        return multiplier
    
    def get_top_entries(self, count: int = 3) -> List[FallbackNode]:
        """Get top N entries based on priority scores."""
        # Convert to list and sort by priority score
        nodes = list(self.nodes.values())
        nodes.sort(key=lambda x: x.priority_score, reverse=True)
        
        # Update usage counts for selected nodes
        for node in nodes[:count]:
            node.usage_count += 1
            
        return nodes[:count]
    
    def get_category_entries(self, category: FallbackCategory) -> List[FallbackNode]:
        """Get all entries for a specific category."""
        return [node for node in self.nodes.values() 
                if node.category == category]
    
    def get_emergency_entries(self) -> List[FallbackNode]:
        """Get emergency fallback entries."""
        return self.get_category_entries(FallbackCategory.EMERGENCY)
    
    def reset_usage_counts(self):
        """Reset usage counts for all nodes."""
        for node in self.nodes.values():
            node.usage_count = 0 