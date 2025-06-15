# /core/semantic_field.py

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

from backend.cognitive.mood_urgency_probe import get_mood_probe
from backend.cognitive.entropy_fluctuation import get_entropy_fluctuation
from backend.cognitive.qualia_kernel import get_qualia_kernel
from pulse.pulse_heat import pulse, PulseHeat, add_heat

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
    
    def update_field_position(self, field_center: np.ndarray, field_dynamics: Dict):
        """Update position in semantic field based on physics"""
        # Calculate radial position using enhanced formula
        access_factor = math.log(self.semantic_vector.access_count + 1)
        relevance_factor = self.semantic_vector.contextual_relevance
        
        # Schema feedback from PulseHeat system
        thermal_profile = pulse.get_thermal_profile()
        schema_feedback = thermal_profile.get('stability_index', 0.5)
        
        # Semantic field position formula (from your formula set)
        alpha, beta, gamma = 0.4, 0.3, 0.3  # Weighting factors
        radial_distance = 1.0 / ((access_factor * alpha) + 
                                (relevance_factor * beta) + 
                                (schema_feedback * gamma))
        
        # Convert to 3D coordinates with some angular distribution
        theta = hash(self.node_id) % 360 * math.pi / 180
        phi = (hash(self.node_id + "phi") % 180) * math.pi / 180
        
        self.field_position = field_center + radial_distance * np.array([
            math.sin(phi) * math.cos(theta),
            math.sin(phi) * math.sin(theta),
            math.cos(phi)
        ])
        
        # Update local pressure based on nearby nodes
        self._update_local_pressure(field_dynamics)
    
    def _update_local_pressure(self, field_dynamics: Dict):
        """Calculate local semantic pressure from nearby nodes"""
        nearby_pressure = field_dynamics.get('pressure_map', {}).get(self.node_id, 0.0)
        thermal_pressure = pulse.current_heat / pulse.heat_capacity
        
        self.local_pressure = (nearby_pressure * 0.7) + (thermal_pressure * 0.3)

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
        print("[SemanticField] 🌱 Rhizomic field initialized")
    
    @classmethod
    def get_current_field(cls) -> 'RhizomicSemanticField':
        """Get the current semantic field instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def add_semantic_node(self, content: str, embedding: np.ndarray, 
                         charge_type: NodeCharge = NodeCharge.STATIC_NEUTRAL) -> str:
        """Add new semantic node to the field"""
        with self._lock:
            node_id = f"node_{len(self.nodes)}_{hash(content) % 10000}"
            
            semantic_vector = SemanticVector(
                content=content,
                embedding=embedding,
                charge_type=charge_type,
                charge_intensity=0.5
            )
            
            node = SemanticNode(node_id, semantic_vector)
            node.update_field_position(self.field_center, self._get_field_dynamics())
            
            self.nodes[node_id] = node
            
            # Establish initial connections
            self._establish_rhizomic_connections(node)
            
            # Add thermal energy for new node
            add_heat("semantic_growth", 0.1, f"new node: {content[:20]}")
            
            print(f"[SemanticField] 🌱 Added node {node_id}: {content[:30]}...")
            return node_id
    
    def _establish_rhizomic_connections(self, new_node: SemanticNode):
        """Establish connections based on semantic similarity and field dynamics"""
        connection_candidates = []
        
        for existing_node in self.nodes.values():
            if existing_node.node_id == new_node.node_id:
                continue
                
            similarity = new_node.calculate_semantic_similarity(existing_node)
            distance = np.linalg.norm(new_node.field_position - existing_node.field_position)
            
            # Hybrid pathfinding score (from your formula set)
            path_cost = distance * (1 - similarity)
            
            if similarity > 0.3:  # Minimum similarity threshold
                connection_candidates.append((existing_node.node_id, similarity, path_cost))
        
        # Sort by path cost and connect to best candidates
        connection_candidates.sort(key=lambda x: x[2])
        max_connections = min(5, len(connection_candidates))  # Limit connections per node
        
        for i in range(max_connections):
            target_id, similarity, _ = connection_candidates[i]
            self._create_rhizomic_connection(new_node.node_id, target_id, similarity)
    
    def _create_rhizomic_connection(self, source_id: str, target_id: str, base_strength: float):
        """Create bidirectional rhizomic connection between nodes"""
        now = datetime.utcnow()
        
        # Forward connection
        forward_conn = RhizomicConnection(
            source_id=source_id,
            target_id=target_id,
            base_strength=base_strength,
            current_strength=base_strength,
            last_activation=now,
            rattling_phase=np.random.uniform(0, 2*math.pi)
        )
        
        # Reverse connection with different rattling phase
        reverse_conn = RhizomicConnection(
            source_id=target_id,
            target_id=source_id,
            base_strength=base_strength,
            current_strength=base_strength,
            last_activation=now,
            rattling_phase=np.random.uniform(0, 2*math.pi)
        )
        
        self.nodes[source_id].connections[target_id] = forward_conn
        self.nodes[target_id].connections[source_id] = reverse_conn
    
    def tick_update(self) -> Dict:
        """Per-tick field dynamics update"""
        with self._lock:
            self.tick_count += 1
            current_time = datetime.utcnow()
            delta_time = (current_time - self.last_update).total_seconds()
            self.last_update = current_time
            
            # Update all nodes
            field_dynamics = self._get_field_dynamics()
            
            for node in self.nodes.values():
                self._update_node_dynamics(node, delta_time, field_dynamics)
            
            # Update connections and nutrient flow
            self._update_connection_dynamics(delta_time)
            
            # Update field pressure map
            self._update_pressure_map()
            
            # Trigger callbacks for visualization
            self._trigger_field_callbacks()
            
            stats = {
                'node_count': len(self.nodes),
                'active_connections': sum(len(n.connections) for n in self.nodes.values()),
                'total_nutrient_flow': sum(self.nutrient_reservoirs.values()),
                'average_pressure': np.mean(list(self.pressure_map.values())) if self.pressure_map else 0.0,
                'field_energy': self.growth_energy
            }
            
            return stats
    
    def _update_node_dynamics(self, node: SemanticNode, delta_time: float, field_dynamics: Dict):
        """Update individual node dynamics"""
        # Update field position
        node.update_field_position(self.field_center, field_dynamics)
        
        # Rhizomic growth based on nutrient availability
        if node.nutrient_level > 0.7:
            node.growth_rate = min(node.growth_rate * 1.1, 0.5)
            self.growth_energy += 0.1
        elif node.nutrient_level < 0.3:
            node.growth_rate = max(node.growth_rate * 0.9, 0.01)
        
        # Update charge intensity based on recent activity
        time_since_access = (datetime.utcnow() - node.semantic_vector.last_accessed).total_seconds()
        decay_factor = math.exp(-time_since_access / 3600)  # 1 hour decay
        node.semantic_vector.charge_intensity *= (0.9 + 0.1 * decay_factor)
    
    def _update_connection_dynamics(self, delta_time: float):
        """Update rhizomic connection strengths and rattling"""
        for node in self.nodes.values():
            for connection in node.connections.values():
                # Update rattling phase (quantum-like oscillation)
                connection.rattling_phase += delta_time * 2.0  # 2 rad/sec base frequency
                if connection.rattling_phase > 2 * math.pi:
                    connection.rattling_phase -= 2 * math.pi
                
                # Nutrient flow decay
                connection.nutrient_flow *= 0.95
                
                # Connection strength adaptation
                time_since_activation = (datetime.utcnow() - connection.last_activation).total_seconds()
                if time_since_activation > 300:  # 5 minutes
                    connection.current_strength *= 0.99  # Gradual decay
                
                # Update nutrient reservoirs
                target_node = self.nodes.get(connection.target_id)
                if target_node:
                    nutrient_transfer = connection.nutrient_flow * delta_time
                    target_node.nutrient_level = min(target_node.nutrient_level + nutrient_transfer, 1.0)
    
    def _update_pressure_map(self):
        """Update semantic pressure heatmap"""
        self.pressure_map.clear()
        
        for node_id, node in self.nodes.items():
            # Calculate pressure from connections and nutrient flow
            connection_pressure = sum(
                conn.get_directional_strength() * conn.nutrient_flow 
                for conn in node.connections.values()
            )
            
            # Add thermal pressure contribution
            thermal_contribution = pulse.current_heat * 0.1
            
            total_pressure = connection_pressure + thermal_contribution
            self.pressure_map[node_id] = total_pressure
    
    def _get_field_dynamics(self) -> Dict:
        """Get current field dynamics for node updates"""
        thermal_profile = pulse.get_thermal_profile()
        return {
            'pressure_map': self.pressure_map,
            'growth_energy': self.growth_energy,
            'field_center': self.field_center,
            'thermal_state': thermal_profile
        }

    
    def activate_semantic_pathway(self, start_content: str, end_content: str) -> Optional[List[str]]:
        """Activate pathway between semantic concepts with nutrient flow"""
        start_node = self._find_node_by_content(start_content)
        end_node = self._find_node_by_content(end_content)
        
        if not start_node or not end_node:
            return None
        
        # Find path using semantic similarity and field dynamics
        path = self._find_semantic_path(start_node.node_id, end_node.node_id)
        
        if path:
            # Activate pathway with nutrient flow
            self._flow_nutrients_along_path(path)
            add_heat("semantic_activation", 0.2, f"pathway: {start_content} -> {end_content}")
        
        return [self.nodes[node_id].semantic_vector.content for node_id in path] if path else None
    
    def _find_node_by_content(self, content: str) -> Optional[SemanticNode]:
        """Find node by semantic content (fuzzy matching)"""
        best_match = None
        best_similarity = 0.0
        
        # Create temporary embedding for search content
        # In practice, this would use the same embedding model as node creation
        search_embedding = np.random.randn(384)  # Placeholder
        search_embedding = search_embedding / np.linalg.norm(search_embedding)
        
        for node in self.nodes.values():
            similarity = np.dot(search_embedding, node.semantic_vector.embedding)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = node
        
        return best_match if best_similarity > 0.5 else None
    
    def _find_semantic_path(self, start_id: str, end_id: str) -> Optional[List[str]]:
        """Find optimal path using semantic similarity and field dynamics"""
        # Simplified A* pathfinding with semantic heuristics
        visited = set()
        queue = [(0, [start_id])]
        
        while queue:
            current_cost, path = queue.pop(0)
            current_id = path[-1]
            
            if current_id == end_id:
                return path
            
            if current_id in visited:
                continue
            visited.add(current_id)
            
            current_node = self.nodes[current_id]
            
            for target_id, connection in current_node.connections.items():
                if target_id not in visited:
                    # Calculate path cost using hybrid formula
                    target_node = self.nodes[target_id]
                    similarity = current_node.calculate_semantic_similarity(target_node)
                    hop_cost = 1.0 * (1 - similarity)  # From your formula set
                    
                    new_path = path + [target_id]
                    total_cost = current_cost + hop_cost
                    
                    queue.append((total_cost, new_path))
            
            # Sort queue by cost
            queue.sort(key=lambda x: x[0])
        
        return None
    
    def _flow_nutrients_along_path(self, path: List[str]):
        """Flow nutrients along activated pathway"""
        nutrient_amount = 1.0
        
        for i in range(len(path) - 1):
            source_id, target_id = path[i], path[i + 1]
            source_node = self.nodes[source_id]
            
            if target_id in source_node.connections:
                connection = source_node.connections[target_id]
                connection.nutrient_flow += nutrient_amount * 0.8  # Some loss along path
                connection.last_activation = datetime.utcnow()
                connection.activation_count += 1
                
                # Strengthen frequently used pathways
                if connection.activation_count > 5:
                    connection.base_strength = min(connection.base_strength * 1.05, 1.0)
    
    def register_field_callback(self, callback: Callable):
        """Register callback for field state changes"""
        self._field_update_callbacks.append(callback)
    
    def _trigger_field_callbacks(self):
        """Trigger registered field callbacks"""
        field_state = self.get_field_visualization_data()
        for callback in self._field_update_callbacks:
            try:
                callback(field_state)
            except Exception as e:
                print(f"[SemanticField] ❌ Callback error: {e}")
    
    def get_field_visualization_data(self) -> Dict:
        """Get comprehensive field data for visualization"""
        return {
            'nodes': {
                node_id: {
                    'position': node.field_position.tolist(),
                    'content': node.semantic_vector.content,
                    'charge_type': node.semantic_vector.charge_type.value,
                    'charge_intensity': node.semantic_vector.charge_intensity,
                    'local_pressure': node.local_pressure,
                    'nutrient_level': node.nutrient_level,
                    'access_count': node.semantic_vector.access_count
                }
                for node_id, node in self.nodes.items()
            },
            'connections': [
                {
                    'source': node_id,
                    'target': conn.target_id,
                    'strength': conn.get_directional_strength(),
                    'nutrient_flow': conn.nutrient_flow,
                    'rattling_phase': conn.rattling_phase
                }
                for node_id, node in self.nodes.items()
                for conn in node.connections.values()
            ],
            'pressure_map': self.pressure_map,
            'field_center': self.field_center.tolist(),
            'field_stats': {
                'node_count': len(self.nodes),
                'total_connections': sum(len(n.connections) for n in self.nodes.values()),
                'growth_energy': self.growth_energy,
                'tick_count': self.tick_count
            }
        }

    def get_drift_vectors(self) -> Dict[str, Dict[str, float]]:
        """Get drift vectors for all nodes in the field"""
        drift_vectors = {}
        print(f"[DEBUG] get_drift_vectors called. Node count: {len(self.nodes)}")
        
        for node_id, node in self.nodes.items():
            # Calculate drift based on local pressure and position changes
            drift_magnitude = node.local_pressure
            drift_direction = math.atan2(
                node.field_position[1] - self.field_center[1],
                node.field_position[0] - self.field_center[0]
            )
            
            drift_vectors[node_id] = {
                'magnitude': float(drift_magnitude),
                'direction': float(drift_direction),
                'x': float(node.field_position[0]),
                'y': float(node.field_position[1]),
                'z': float(node.field_position[2])
            }
        print(f"[DEBUG] get_drift_vectors returning: {drift_vectors}")
        return drift_vectors

# Global semantic field instance
SemanticField = RhizomicSemanticField()

def get_current_field() -> RhizomicSemanticField:
    """Get the current semantic field instance"""
    return SemanticField.get_current_field()

# Convenience functions
def add_concept(content: str, embedding: np.ndarray, charge_type: NodeCharge = NodeCharge.STATIC_NEUTRAL) -> str:
    """Add semantic concept to the field"""
    return SemanticField.add_semantic_node(content, embedding, charge_type)

def activate_pathway(start: str, end: str) -> Optional[List[str]]:
    """Activate semantic pathway between concepts"""
    return SemanticField.activate_semantic_pathway(start, end)

def get_field_state() -> Dict:
    """Get current field state for visualization"""
    return SemanticField.get_field_visualization_data()

def tick_semantic_field() -> Dict:
    """Perform per-tick field update"""
    return SemanticField.tick_update()
