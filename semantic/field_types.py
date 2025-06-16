"""
Semantic Field Types
Core types and classes for the semantic field system
"""

import math
import threading
import numpy as np
from typing import Dict, List, Set, Optional, Tuple, Callable
from dataclasses import dataclass, field
from collections import defaultdict, deque
from datetime import datetime, timedelta
from enum import Enum
import logging
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NodeCharge(Enum):
    """Semantic charge types for field dynamics"""
    ACTIVE_POSITIVE = "active+"
    ACTIVE_NEGATIVE = "active-"
    STATIC_NEUTRAL = "static"
    LATENT_POSITIVE = "latent+"
    LATENT_NEGATIVE = "latent-"

@dataclass
class SemanticVector:
    """Embedded meaning representation with magnetic properties"""
    content: str
    embedding: np.ndarray
    charge_type: NodeCharge
    charge_intensity: float = 0.5
    last_accessed: datetime = field(default_factory=datetime.utcnow)
    access_count: int = 0
    contextual_relevance: float = 0.5
    
    def __post_init__(self):
        # Normalize embedding vector
        if np.linalg.norm(self.embedding) > 0:
            self.embedding = self.embedding / np.linalg.norm(self.embedding)

@dataclass
class RhizomicConnection:
    """Dynamic connection between semantic nodes"""
    source_id: str
    target_id: str
    base_strength: float
    current_strength: float
    last_activation: datetime
    activation_count: int = 0
    nutrient_flow: float = 0.0
    rattling_phase: float = 0.0  # Quantum-like oscillation
    
    def get_directional_strength(self, direction: str = "forward") -> float:
        """Get connection strength with directional rattling"""
        rattle_factor = math.sin(self.rattling_phase) * 0.2 + 1.0
        if direction == "reverse":
            rattle_factor = math.cos(self.rattling_phase) * 0.2 + 1.0
        return self.current_strength * rattle_factor

class SemanticNode:
    """Individual node in the rhizomic semantic field"""
    
    def __init__(self, node_id: str, semantic_vector: SemanticVector):
        self.node_id = node_id
        self.semantic_vector = semantic_vector
        self.field_position = np.array([0.0, 0.0, 0.0])  # 3D field coordinates
        self.connections: Dict[str, RhizomicConnection] = {}
        self.nutrient_level = 0.5
        self.growth_rate = 0.1
        self.local_pressure = 0.0
        self.stability_index = 1.0
        self.creation_time = datetime.utcnow()
        
    def calculate_semantic_similarity(self, other_node: 'SemanticNode') -> float:
        """Calculate cosine similarity with charge modification"""
        base_similarity = np.dot(self.semantic_vector.embedding, 
                               other_node.semantic_vector.embedding)
        
        # Charge interaction modifies similarity
        charge_modifier = self._calculate_charge_interaction(other_node)
        return base_similarity * charge_modifier
    
    def _calculate_charge_interaction(self, other_node: 'SemanticNode') -> float:
        """Calculate how semantic charges affect connection strength"""
        self_charge = self.semantic_vector.charge_type
        other_charge = other_node.semantic_vector.charge_type
        
        # Charge interaction matrix
        if self_charge == other_charge:
            return 1.1  # Like charges slightly attract in semantic space
        elif (self_charge.value.endswith('+') and other_charge.value.endswith('-')) or \
             (self_charge.value.endswith('-') and other_charge.value.endswith('+')):
            return 1.3  # Opposite charges strongly attract
        elif 'static' in [self_charge.value, other_charge.value]:
            return 0.9  # Static provides stability but less attraction
        else:
            return 1.0  # Neutral interaction

class RhizomicSemanticField:
    """Main semantic field implementing rhizomic growth dynamics"""
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, field_capacity: int = 10000):
        if hasattr(self, 'initialized'):
            return
            
        self.nodes: Dict[str, SemanticNode] = {}
        self.field_center = np.array([0.0, 0.0, 0.0])
        self.field_capacity = field_capacity
        self.field_radius = 100.0
        
        # Growth dynamics
        self.growth_energy = 0.0
        self.nutrient_reservoirs = defaultdict(float)
        self.pressure_map: Dict[str, float] = {}
        
        # Threading for real-time updates
        self._lock = threading.RLock()
        self._field_update_callbacks: List[Callable] = []
        
        # Performance tracking
        self.tick_count = 0
        self.last_update = datetime.utcnow()
        
        self.initialized = True
        logger.info("Initialized RhizomicSemanticField")
    
    def add_semantic_node(self, content: str, embedding: np.ndarray, charge_type: NodeCharge = NodeCharge.STATIC_NEUTRAL) -> str:
        """Add a new semantic node to the field"""
        with self._lock:
            node_id = str(uuid.uuid4())
            semantic_vector = SemanticVector(content=content, embedding=embedding, charge_type=charge_type)
            self.nodes[node_id] = SemanticNode(node_id, semantic_vector)
            return node_id
    
    def activate_semantic_pathway(self, start: str, end: str) -> Optional[List[str]]:
        """Activate a pathway between two semantic nodes"""
        if start not in self.nodes or end not in self.nodes:
            return None
            
        # Simple direct connection for now
        return [start, end]
    
    def get_field_visualization_data(self) -> Dict:
        """Get current field state for visualization"""
        return {
            'node_count': len(self.nodes),
            'field_radius': self.field_radius,
            'growth_energy': self.growth_energy,
            'tick_count': self.tick_count,
            'last_update': self.last_update.isoformat()
        }
    
    def tick_update(self) -> Dict:
        """Perform per-tick field update"""
        with self._lock:
            self.tick_count += 1
            self.last_update = datetime.utcnow()
            
            # Update field dynamics
            self._update_field_dynamics()
            
            # Notify callbacks
            for callback in self._field_update_callbacks:
                try:
                    callback(self)
                except Exception as e:
                    logger.error(f"Error in field update callback: {e}")
            
            return self.get_field_visualization_data()
    
    def _update_field_dynamics(self):
        """Update field dynamics and growth"""
        # Update nutrient levels
        for node in self.nodes.values():
            node.nutrient_level = max(0.0, min(1.0, node.nutrient_level + node.growth_rate))
            
        # Update field radius based on growth
        self.field_radius = min(200.0, self.field_radius + 0.01)
        
        # Update growth energy
        self.growth_energy = sum(node.nutrient_level for node in self.nodes.values()) / max(1, len(self.nodes))

__all__ = ['NodeCharge', 'SemanticVector', 'RhizomicConnection', 'SemanticNode', 'RhizomicSemanticField'] 