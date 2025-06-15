"""
Semantic Field - Core semantic network and field dynamics
"""

import logging
import time
import math
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)

@dataclass
class NodeCharge:
    """Represents the charge state of a semantic node"""
    value: float = 0.0
    momentum: float = 0.0
    last_update: float = field(default_factory=time.time)
    history: List[Tuple[float, float]] = field(default_factory=list)  # (timestamp, value)
    
    def update(self, new_value: float, decay_rate: float = 0.95) -> None:
        """
        Update node charge with momentum and decay
        
        Args:
            new_value: New charge value
            decay_rate: Rate of charge decay
        """
        # Calculate time delta
        current_time = time.time()
        delta = current_time - self.last_update
        
        # Apply momentum
        self.momentum = (self.momentum + (new_value - self.value)) * decay_rate
        
        # Update value
        self.value = new_value + self.momentum
        
        # Record history
        self.history.append((current_time, self.value))
        
        # Trim history if too long
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        # Update timestamp
        self.last_update = current_time
    
    def get_stability(self) -> float:
        """Calculate charge stability based on history"""
        if len(self.history) < 2:
            return 1.0
        
        # Calculate variance in recent history
        recent_values = [v for _, v in self.history[-10:]]
        mean = sum(recent_values) / len(recent_values)
        variance = sum((x - mean) ** 2 for x in recent_values) / len(recent_values)
        
        # Convert to stability score (0-1)
        stability = 1.0 / (1.0 + math.sqrt(variance))
        return stability
    
    def get_trend(self) -> float:
        """Calculate charge trend over time"""
        if len(self.history) < 2:
            return 0.0
        
        # Calculate linear regression slope
        x_values = [t for t, _ in self.history[-10:]]
        y_values = [v for _, v in self.history[-10:]]
        
        n = len(x_values)
        if n < 2:
            return 0.0
        
        x_mean = sum(x_values) / n
        y_mean = sum(y_values) / n
        
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        if denominator == 0:
            return 0.0
        
        slope = numerator / denominator
        return slope

@dataclass
class SemanticNode:
    """Represents a node in the semantic network"""
    id: str
    content: str
    charge: NodeCharge = field(default_factory=NodeCharge)
    connections: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    last_activation: float = field(default_factory=time.time)
    
    def activate(self, strength: float = 1.0) -> None:
        """
        Activate the node with given strength
        
        Args:
            strength: Activation strength (0-1)
        """
        self.charge.update(strength)
        self.last_activation = time.time()
    
    def connect_to(self, target_id: str, weight: float = 1.0) -> None:
        """
        Create or update connection to another node
        
        Args:
            target_id: ID of target node
            weight: Connection weight
        """
        self.connections[target_id] = weight
    
    def get_connection_strength(self, target_id: str) -> float:
        """Get strength of connection to target node"""
        return self.connections.get(target_id, 0.0)
    
    def get_activation_level(self) -> float:
        """Get current activation level"""
        return self.charge.value

class SemanticField:
    """Manages semantic network and field dynamics"""
    
    def __init__(self):
        """Initialize semantic field"""
        self.nodes: Dict[str, SemanticNode] = {}
        self.field_charge = NodeCharge()
        self.last_update = time.time()
        self.config = {
            'charge_decay': 0.95,
            'connection_threshold': 0.3,
            'activation_threshold': 0.1,
            'field_coupling': 0.5
        }
        logger.info("Initialized SemanticField")
    
    def add_node(self, node_id: str, content: str, metadata: Optional[Dict] = None) -> SemanticNode:
        """
        Add a new node to the semantic field
        
        Args:
            node_id: Unique identifier for the node
            content: Node content/meaning
            metadata: Optional metadata
            
        Returns:
            Created SemanticNode
        """
        if node_id in self.nodes:
            raise ValueError(f"Node {node_id} already exists")
        
        node = SemanticNode(
            id=node_id,
            content=content,
            metadata=metadata or {}
        )
        self.nodes[node_id] = node
        return node
    
    def get_node(self, node_id: str) -> Optional[SemanticNode]:
        """Get node by ID"""
        return self.nodes.get(node_id)
    
    def connect_nodes(self, source_id: str, target_id: str, weight: float = 1.0) -> None:
        """
        Create connection between nodes
        
        Args:
            source_id: Source node ID
            target_id: Target node ID
            weight: Connection weight
        """
        if source_id not in self.nodes or target_id not in self.nodes:
            raise ValueError("Source or target node not found")
        
        self.nodes[source_id].connect_to(target_id, weight)
    
    def activate_node(self, node_id: str, strength: float = 1.0) -> None:
        """
        Activate a node and propagate activation
        
        Args:
            node_id: Node to activate
            strength: Activation strength
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not found")
        
        # Activate node
        self.nodes[node_id].activate(strength)
        
        # Update field charge
        self.field_charge.update(
            strength * self.config['field_coupling'],
            self.config['charge_decay']
        )
        
        # Propagate activation to connected nodes
        self._propagate_activation(node_id, strength)
    
    def _propagate_activation(self, source_id: str, base_strength: float) -> None:
        """
        Propagate activation through connected nodes
        
        Args:
            source_id: Source node ID
            base_strength: Base activation strength
        """
        source = self.nodes[source_id]
        visited = {source_id}
        to_visit = [(target_id, base_strength * weight)
                   for target_id, weight in source.connections.items()
                   if weight >= self.config['connection_threshold']]
        
        while to_visit:
            target_id, strength = to_visit.pop(0)
            if target_id in visited:
                continue
            
            visited.add(target_id)
            target = self.nodes[target_id]
            
            # Activate target
            target.activate(strength)
            
            # Add connected nodes to visit list
            for next_id, weight in target.connections.items():
                if (next_id not in visited and
                    weight >= self.config['connection_threshold']):
                    to_visit.append((next_id, strength * weight))
    
    def get_field_state(self) -> Dict:
        """Get current field state"""
        return {
            'node_count': len(self.nodes),
            'field_charge': self.field_charge.value,
            'field_stability': self.field_charge.get_stability(),
            'field_trend': self.field_charge.get_trend(),
            'active_nodes': sum(1 for node in self.nodes.values()
                              if node.charge.value > self.config['activation_threshold'])
        }
    
    def get_node_state(self, node_id: str) -> Optional[Dict]:
        """Get state of specific node"""
        node = self.get_node(node_id)
        if not node:
            return None
        
        return {
            'id': node.id,
            'content': node.content,
            'charge': node.charge.value,
            'stability': node.charge.get_stability(),
            'trend': node.charge.get_trend(),
            'connection_count': len(node.connections),
            'last_activation': node.last_activation,
            'metadata': node.metadata
        }

# Global instance
_semantic_field = None

def get_semantic_field() -> SemanticField:
    """Get or create the global semantic field instance"""
    global _semantic_field
    if _semantic_field is None:
        _semantic_field = SemanticField()
    return _semantic_field

__all__ = ['SemanticField', 'NodeCharge', 'SemanticNode', 'get_semantic_field'] 