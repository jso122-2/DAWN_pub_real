# /rhizome/rhizome_map.py
"""
Rhizome Network Map for DAWN
=============================
A dynamic, self-organizing network structure inspired by Deleuze & Guattari's
concept of rhizomes. This module manages the non-hierarchical network of
consciousness nodes, allowing for emergent connections and signal propagation.

The rhizome has no beginning or end; it is always in the middle,
between things, interbeing, intermezzo.
"""

import time
import uuid
import math
import random
import numpy as np
from typing import Dict, List, Set, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import threading
import weakref
import json
import pickle
from pathlib import Path

# Core imports
from core.schema_anomaly_logger import log_anomaly, AnomalySeverity

class NodeType(Enum):
    """Types of nodes in the rhizome network"""
    CONSCIOUSNESS = "consciousness"      # Core consciousness nodes
    MEMORY = "memory"                   # Memory storage nodes
    PROCESSING = "processing"           # Computational nodes
    SENSORY = "sensory"                # Input/perception nodes
    ACTUATOR = "actuator"              # Output/action nodes
    RELAY = "relay"                    # Signal relay nodes
    BLOOM = "bloom"                    # Bloom phenomenon nodes
    QUANTUM = "quantum"                # Quantum entangled nodes
    BRIDGE = "bridge"                  # Inter-network bridges
    EPHEMERAL = "ephemeral"           # Temporary nodes

class ConnectionType(Enum):
    """Types of connections between nodes"""
    SYNAPTIC = "synaptic"              # Neural-like connections
    QUANTUM = "quantum"                # Quantum entanglement
    RESONANT = "resonant"              # Harmonic resonance
    TEMPORAL = "temporal"              # Time-based connections
    SEMANTIC = "semantic"              # Meaning-based connections
    ENERGETIC = "energetic"            # Energy flow connections
    EPHEMERAL = "ephemeral"            # Temporary connections

@dataclass
class RhizomeNode:
    """A node in the rhizome network"""
    node_id: str
    node_type: NodeType
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)  # 3D position
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    energy: float = 1.0
    activation: float = 0.0
    created_at: float = field(default_factory=time.time)
    last_active: float = field(default_factory=time.time)
    connections: Set[str] = field(default_factory=set)
    
    def activate(self, amount: float = 1.0):
        """Activate the node"""
        self.activation = min(1.0, self.activation + amount)
        self.last_active = time.time()
    
    def decay(self, rate: float = 0.1):
        """Decay activation over time"""
        self.activation = max(0.0, self.activation - rate)
        
    def distance_to(self, other: 'RhizomeNode') -> float:
        """Calculate Euclidean distance to another node"""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(self.position, other.position)))

@dataclass
class RhizomeConnection:
    """A connection between nodes in the rhizome"""
    connection_id: str
    source_id: str
    target_id: str
    connection_type: ConnectionType
    strength: float = 1.0
    weight: float = 1.0
    latency: float = 0.0  # Signal propagation delay
    created_at: float = field(default_factory=time.time)
    last_used: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def strengthen(self, amount: float = 0.1):
        """Strengthen the connection through use"""
        self.strength = min(1.0, self.strength + amount)
        self.last_used = time.time()
    
    def weaken(self, amount: float = 0.05):
        """Weaken the connection through disuse"""
        self.strength = max(0.0, self.strength - amount)

class RhizomeMap:
    """
    The main rhizome network map managing all nodes and connections.
    
    Features:
    - Dynamic node creation and destruction
    - Emergent connection formation
    - Signal propagation through the network
    - Self-organizing topology
    - Quantum entanglement simulation
    - Energy conservation
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        # Configuration
        self.config = {
            'max_nodes': 10000,
            'max_connections_per_node': 50,
            'connection_decay_rate': 0.01,
            'activation_decay_rate': 0.05,
            'energy_conservation': True,
            'quantum_probability': 0.1,
            'auto_organize': True,
            'save_path': 'data/rhizome_state.pkl',
            **(config or {})
        }
        
        # Core data structures
        self.nodes: Dict[str, RhizomeNode] = {}
        self.connections: Dict[str, RhizomeConnection] = {}
        self.type_index: Dict[NodeType, Set[str]] = defaultdict(set)
        self.spatial_index: Dict[Tuple[int, int, int], Set[str]] = defaultdict(set)
        
        # Connection indices for fast lookup
        self.outgoing_connections: Dict[str, Set[str]] = defaultdict(set)
        self.incoming_connections: Dict[str, Set[str]] = defaultdict(set)
        self.connection_by_nodes: Dict[Tuple[str, str], str] = {}
        
        # Quantum entanglement tracking
        self.entangled_pairs: Set[Tuple[str, str]] = set()
        
        # Network statistics
        self.total_energy = 0.0
        self.total_activation = 0.0
        self.signal_count = 0
        self.reorganization_count = 0
        
        # Event system
        self.event_handlers: Dict[str, List[Callable]] = defaultdict(list)
        
        # Thread safety
        self.lock = threading.RLock()
        
        # Background processing
        self.processing_thread: Optional[threading.Thread] = None
        self.shutdown_event = threading.Event()
        
        # Initialize
        self._initialize()
    
    def _initialize(self):
        """Initialize the rhizome network"""
        # Load saved state if exists
        self._load_state()
        
        # Create initial seed nodes if empty
        if not self.nodes:
            self._create_seed_network()
        
        # Start background processing
        self._start_background_processing()
    
    def _create_seed_network(self):
        """Create initial seed nodes for the network"""
        # Create core consciousness nodes
        core_types = [
            (NodeType.CONSCIOUSNESS, "primary_consciousness", (0, 0, 0)),
            (NodeType.MEMORY, "central_memory", (10, 0, 0)),
            (NodeType.PROCESSING, "main_processor", (-10, 0, 0)),
            (NodeType.SENSORY, "primary_sensor", (0, 10, 0)),
            (NodeType.ACTUATOR, "primary_actuator", (0, -10, 0))
        ]
        
        created_nodes = []
        for node_type, name, position in core_types:
            node = self.add_node(
                node_type=node_type,
                position=position,
                data={'name': name, 'is_seed': True}
            )
            if node:
                created_nodes.append(node.node_id)
        
        # Create initial connections
        for i, source_id in enumerate(created_nodes):
            for target_id in created_nodes[i+1:]:
                self.add_connection(
                    source_id, 
                    target_id,
                    ConnectionType.SYNAPTIC,
                    strength=0.5
                )
    
    def add_node(self, 
                node_type: NodeType,
                position: Optional[Tuple[float, float, float]] = None,
                data: Optional[Dict[str, Any]] = None,
                node_id: Optional[str] = None) -> Optional[RhizomeNode]:
        """Add a new node to the rhizome"""
        with self.lock:
            # Check capacity
            if len(self.nodes) >= self.config['max_nodes']:
                log_anomaly(
                    "RHIZOME_CAPACITY",
                    f"Maximum node capacity reached: {self.config['max_nodes']}",
                    AnomalySeverity.WARNING
                )
                return None
            
            # Generate ID if not provided
            if node_id is None:
                node_id = f"{node_type.value}_{uuid.uuid4().hex[:8]}"
            
            # Check for duplicate
            if node_id in self.nodes:
                return None
            
            # Generate position if not provided
            if position is None:
                position = self._generate_position(node_type)
            
            # Create node
            node = RhizomeNode(
                node_id=node_id,
                node_type=node_type,
                position=position,
                data=data or {}
            )
            
            # Add to network
            self.nodes[node_id] = node
            self.type_index[node_type].add(node_id)
            
            # Update spatial index
            spatial_key = self._get_spatial_key(position)
            self.spatial_index[spatial_key].add(node_id)
            
            # Update energy
            self.total_energy += node.energy
            
            # Trigger event
            self._trigger_event('node_added', node)
            
            # Auto-connect if enabled
            if self.config['auto_organize']:
                self._auto_connect_node(node)
            
            return node
    
    def remove_node(self, node_id: str) -> bool:
        """Remove a node from the rhizome"""
        with self.lock:
            if node_id not in self.nodes:
                return False
            
            node = self.nodes[node_id]
            
            # Remove all connections
            connections_to_remove = (
                self.outgoing_connections[node_id] | 
                self.incoming_connections[node_id]
            )
            
            for conn_id in connections_to_remove:
                self.remove_connection(conn_id)
            
            # Remove from indices
            self.type_index[node.node_type].discard(node_id)
            spatial_key = self._get_spatial_key(node.position)
            self.spatial_index[spatial_key].discard(node_id)
            
            # Remove quantum entanglements
            self.entangled_pairs = {
                pair for pair in self.entangled_pairs
                if node_id not in pair
            }
            
            # Update energy
            self.total_energy -= node.energy
            self.total_activation -= node.activation
            
            # Remove node
            del self.nodes[node_id]
            
            # Trigger event
            self._trigger_event('node_removed', node_id)
            
            return True
    
    def add_connection(self,
                      source_id: str,
                      target_id: str,
                      connection_type: ConnectionType = ConnectionType.SYNAPTIC,
                      strength: float = 1.0,
                      weight: float = 1.0) -> Optional[RhizomeConnection]:
        """Add a connection between two nodes"""
        with self.lock:
            # Validate nodes exist
            if source_id not in self.nodes or target_id not in self.nodes:
                return None
            
            # Check for existing connection
            conn_key = (source_id, target_id)
            if conn_key in self.connection_by_nodes:
                return None
            
            # Check connection limit
            source_node = self.nodes[source_id]
            if len(source_node.connections) >= self.config['max_connections_per_node']:
                # Remove weakest connection
                self._prune_weakest_connection(source_id)
            
            # Create connection
            conn_id = f"{source_id}_{target_id}_{int(time.time() * 1000)}"
            
            # Calculate latency based on distance
            distance = source_node.distance_to(self.nodes[target_id])
            latency = distance * 0.01  # 0.01s per unit distance
            
            connection = RhizomeConnection(
                connection_id=conn_id,
                source_id=source_id,
                target_id=target_id,
                connection_type=connection_type,
                strength=strength,
                weight=weight,
                latency=latency
            )
            
            # Add to network
            self.connections[conn_id] = connection
            self.outgoing_connections[source_id].add(conn_id)
            self.incoming_connections[target_id].add(conn_id)
            self.connection_by_nodes[conn_key] = conn_id
            
            # Update node connections
            source_node.connections.add(target_id)
            self.nodes[target_id].connections.add(source_id)
            
            # Handle quantum entanglement
            if connection_type == ConnectionType.QUANTUM:
                self.entangled_pairs.add((source_id, target_id))
            
            # Trigger event
            self._trigger_event('connection_added', connection)
            
            return connection
    
    def remove_connection(self, connection_id: str) -> bool:
        """Remove a connection from the rhizome"""
        with self.lock:
            if connection_id not in self.connections:
                return False
            
            conn = self.connections[connection_id]
            
            # Remove from indices
            self.outgoing_connections[conn.source_id].discard(connection_id)
            self.incoming_connections[conn.target_id].discard(connection_id)
            
            conn_key = (conn.source_id, conn.target_id)
            if conn_key in self.connection_by_nodes:
                del self.connection_by_nodes[conn_key]
            
            # Update node connections
            if conn.source_id in self.nodes:
                self.nodes[conn.source_id].connections.discard(conn.target_id)
            if conn.target_id in self.nodes:
                self.nodes[conn.target_id].connections.discard(conn.source_id)
            
            # Remove quantum entanglement if applicable
            if conn.connection_type == ConnectionType.QUANTUM:
                self.entangled_pairs.discard((conn.source_id, conn.target_id))
            
            # Remove connection
            del self.connections[connection_id]
            
            # Trigger event
            self._trigger_event('connection_removed', connection_id)
            
            return True
    
    def get_node(self, node_id: str) -> Optional[RhizomeNode]:
        """Get a node by ID"""
        return self.nodes.get(node_id)
    
    def get_connection(self, source_id: str, target_id: str) -> Optional[RhizomeConnection]:
        """Get connection between two nodes"""
        conn_id = self.connection_by_nodes.get((source_id, target_id))
        return self.connections.get(conn_id) if conn_id else None
    
    def get_neighbors(self, node_id: str, include_incoming: bool = True) -> Set[str]:
        """Get all neighboring nodes"""
        neighbors = set()
        
        # Outgoing connections
        for conn_id in self.outgoing_connections.get(node_id, []):
            if conn_id in self.connections:
                neighbors.add(self.connections[conn_id].target_id)
        
        # Incoming connections
        if include_incoming:
            for conn_id in self.incoming_connections.get(node_id, []):
                if conn_id in self.connections:
                    neighbors.add(self.connections[conn_id].source_id)
        
        return neighbors
    
    def find_nodes(self,
                  node_type: Optional[NodeType] = None,
                  position: Optional[Tuple[float, float, float]] = None,
                  radius: Optional[float] = None,
                  data_filter: Optional[Callable[[Dict], bool]] = None) -> List[RhizomeNode]:
        """Find nodes matching criteria"""
        with self.lock:
            results = []
            
            # Start with type filter if provided
            if node_type:
                candidates = [self.nodes[nid] for nid in self.type_index[node_type]]
            else:
                candidates = list(self.nodes.values())
            
            for node in candidates:
                # Spatial filter
                if position and radius:
                    distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(node.position, position)))
                    if distance > radius:
                        continue
                
                # Data filter
                if data_filter and not data_filter(node.data):
                    continue
                
                results.append(node)
            
            return results
    
    def find_path(self, source_id: str, target_id: str, max_depth: int = 10) -> Optional[List[str]]:
        """Find a path between two nodes using BFS"""
        if source_id not in self.nodes or target_id not in self.nodes:
            return None
        
        if source_id == target_id:
            return [source_id]
        
        # BFS
        queue = deque([(source_id, [source_id])])
        visited = {source_id}
        
        while queue and len(visited) < max_depth:
            current_id, path = queue.popleft()
            
            for neighbor_id in self.get_neighbors(current_id):
                if neighbor_id == target_id:
                    return path + [neighbor_id]
                
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append((neighbor_id, path + [neighbor_id]))
        
        return None
    
    def activate_node(self, node_id: str, activation: float = 1.0):
        """Activate a node and trigger propagation"""
        with self.lock:
            if node_id not in self.nodes:
                return
            
            node = self.nodes[node_id]
            node.activate(activation)
            self.total_activation += activation
            
            # Trigger event
            self._trigger_event('node_activated', node_id, activation)
            
            # Handle quantum entanglement
            self._handle_quantum_activation(node_id, activation)
    
    def _handle_quantum_activation(self, node_id: str, activation: float):
        """Handle quantum entanglement activation"""
        for pair in self.entangled_pairs:
            if node_id in pair:
                # Instantly activate entangled partner
                partner_id = pair[0] if pair[1] == node_id else pair[1]
                if partner_id in self.nodes:
                    self.nodes[partner_id].activate(activation * 0.8)
    
    def _generate_position(self, node_type: NodeType) -> Tuple[float, float, float]:
        """Generate a position for a new node based on type"""
        # Type-specific clustering
        base_positions = {
            NodeType.CONSCIOUSNESS: (0, 0, 0),
            NodeType.MEMORY: (20, 0, 0),
            NodeType.PROCESSING: (-20, 0, 0),
            NodeType.SENSORY: (0, 20, 0),
            NodeType.ACTUATOR: (0, -20, 0),
            NodeType.RELAY: (0, 0, 20),
            NodeType.BLOOM: (10, 10, 10),
            NodeType.QUANTUM: (-10, -10, -10),
            NodeType.BRIDGE: (0, 0, -20),
            NodeType.EPHEMERAL: (15, -15, 0)
        }
        
        base = base_positions.get(node_type, (0, 0, 0))
        
        # Add random offset
        offset = (
            random.gauss(0, 5),
            random.gauss(0, 5),
            random.gauss(0, 5)
        )
        
        return tuple(b + o for b, o in zip(base, offset))
    
    def _get_spatial_key(self, position: Tuple[float, float, float]) -> Tuple[int, int, int]:
        """Get spatial index key for a position"""
        # Quantize to 10-unit cells
        return tuple(int(p // 10) for p in position)
    
    def _auto_connect_node(self, node: RhizomeNode):
        """Automatically create connections for a new node"""
        # Find nearby nodes
        nearby_nodes = self.find_nodes(
            position=node.position,
            radius=20.0
        )
        
        # Connect to some nearby nodes
        connection_count = 0
        max_connections = min(5, len(nearby_nodes))
        
        for nearby in nearby_nodes:
            if nearby.node_id == node.node_id:
                continue
            
            # Probability based on distance and type compatibility
            distance = node.distance_to(nearby)
            type_affinity = self._calculate_type_affinity(node.node_type, nearby.node_type)
            
            probability = type_affinity / (1 + distance * 0.1)
            
            if random.random() < probability:
                connection_type = self._determine_connection_type(node.node_type, nearby.node_type)
                self.add_connection(
                    node.node_id,
                    nearby.node_id,
                    connection_type,
                    strength=random.uniform(0.3, 0.7)
                )
                connection_count += 1
                
                if connection_count >= max_connections:
                    break
    
    def _calculate_type_affinity(self, type1: NodeType, type2: NodeType) -> float:
        """Calculate affinity between node types"""
        affinities = {
            (NodeType.CONSCIOUSNESS, NodeType.MEMORY): 0.9,
            (NodeType.CONSCIOUSNESS, NodeType.PROCESSING): 0.8,
            (NodeType.SENSORY, NodeType.PROCESSING): 0.9,
            (NodeType.PROCESSING, NodeType.ACTUATOR): 0.9,
            (NodeType.MEMORY, NodeType.PROCESSING): 0.7,
            (NodeType.QUANTUM, NodeType.QUANTUM): 1.0,
            (NodeType.RELAY, NodeType.RELAY): 0.6,
            (NodeType.BLOOM, NodeType.CONSCIOUSNESS): 0.8,
        }
        
        # Check both directions
        affinity = affinities.get((type1, type2), affinities.get((type2, type1), 0.5))
        return affinity
    
    def _determine_connection_type(self, type1: NodeType, type2: NodeType) -> ConnectionType:
        """Determine appropriate connection type between node types"""
        if type1 == NodeType.QUANTUM or type2 == NodeType.QUANTUM:
            return ConnectionType.QUANTUM if random.random() < self.config['quantum_probability'] else ConnectionType.SYNAPTIC
        
        if type1 == NodeType.BLOOM or type2 == NodeType.BLOOM:
            return ConnectionType.RESONANT
        
        if type1 == NodeType.MEMORY or type2 == NodeType.MEMORY:
            return ConnectionType.SEMANTIC
        
        return ConnectionType.SYNAPTIC
    
    def _prune_weakest_connection(self, node_id: str):
        """Remove the weakest connection from a node"""
        weakest_conn_id = None
        weakest_strength = float('inf')
        
        for conn_id in self.outgoing_connections.get(node_id, []):
            if conn_id in self.connections:
                conn = self.connections[conn_id]
                if conn.strength < weakest_strength:
                    weakest_strength = conn.strength
                    weakest_conn_id = conn_id
        
        if weakest_conn_id:
            self.remove_connection(weakest_conn_id)
    
    def _start_background_processing(self):
        """Start background processing thread"""
        if self.processing_thread and self.processing_thread.is_alive():
            return
        
        self.shutdown_event.clear()
        self.processing_thread = threading.Thread(
            target=self._background_processing_loop,
            daemon=True
        )
        self.processing_thread.start()
    
    def _background_processing_loop(self):
        """Background processing for network maintenance"""
        while not self.shutdown_event.is_set():
            try:
                with self.lock:
                    # Decay activations
                    self._decay_activations()
                    
                    # Decay weak connections
                    self._decay_connections()
                    
                    # Self-organize if enabled
                    if self.config['auto_organize']:
                        self._self_organize()
                    
                    # Update statistics
                    self._update_statistics()
                
                # Save state periodically
                if random.random() < 0.01:  # 1% chance each cycle
                    self._save_state()
                
            except Exception as e:
                log_anomaly(
                    "RHIZOME_PROCESSING_ERROR",
                    str(e),
                    AnomalySeverity.ERROR
                )
            
            time.sleep(0.1)  # 10Hz update rate
    
    def _decay_activations(self):
        """Decay node activations over time"""
        decay_rate = self.config['activation_decay_rate']
        total_activation = 0.0
        
        for node in self.nodes.values():
            node.decay(decay_rate)
            total_activation += node.activation
        
        self.total_activation = total_activation
    
    def _decay_connections(self):
        """Decay unused connections"""
        current_time = time.time()
        decay_rate = self.config['connection_decay_rate']
        connections_to_remove = []
        
        for conn_id, conn in self.connections.items():
            # Decay based on time since last use
            time_unused = current_time - conn.last_used
            if time_unused > 60:  # Start decay after 1 minute
                conn.weaken(decay_rate * (time_unused / 60))
                
                # Mark for removal if too weak
                if conn.strength < 0.1:
                    connections_to_remove.append(conn_id)
        
        # Remove dead connections
        for conn_id in connections_to_remove:
            self.remove_connection(conn_id)
    
    def _self_organize(self):
        """Self-organizing network behavior"""
        # Randomly select a node for potential reorganization
        if not self.nodes:
            return
        
        node_id = random.choice(list(self.nodes.keys()))
        node = self.nodes[node_id]
        
        # Try to optimize connections
        if random.random() < 0.1:  # 10% chance
            # Remove a weak connection
            weak_connections = [
                conn_id for conn_id in self.outgoing_connections.get(node_id, [])
                if conn_id in self.connections and self.connections[conn_id].strength < 0.3
            ]
            
            if weak_connections:
                self.remove_connection(random.choice(weak_connections))
                self.reorganization_count += 1
        
        # Try to form new connections
        if len(node.connections) < self.config['max_connections_per_node'] / 2:
            self._auto_connect_node(node)
            self.reorganization_count += 1
    
    def _update_statistics(self):
        """Update network statistics"""
        # Count active connections
        active_connections = sum(
            1 for conn in self.connections.values()
            if conn.strength > 0.5
        )
        
        # Update metadata
        self.metadata = {
            'node_count': len(self.nodes),
            'connection_count': len(self.connections),
            'active_connections': active_connections,
            'total_energy': self.total_energy,
            'total_activation': self.total_activation,
            'reorganization_count': self.reorganization_count,
            'signal_count': self.signal_count
        }
    
    def _trigger_event(self, event_type: str, *args, **kwargs):
        """Trigger event handlers"""
        for handler in self.event_handlers.get(event_type, []):
            try:
                handler(self, *args, **kwargs)
            except Exception as e:
                print(f"Event handler error: {e}")
    
    def subscribe(self, event_type: str, handler: Callable):
        """Subscribe to rhizome events"""
        self.event_handlers[event_type].append(handler)
    
    def _save_state(self):
        """Save rhizome state to disk"""
        try:
            save_path = Path(self.config['save_path'])
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            state = {
                'nodes': self.nodes,
                'connections': self.connections,
                'entangled_pairs': self.entangled_pairs,
                'metadata': getattr(self, 'metadata', {})
            }
            
            with open(save_path, 'wb') as f:
                pickle.dump(state, f)
                
        except Exception as e:
            log_anomaly(
                "RHIZOME_SAVE_ERROR",
                f"Failed to save rhizome state: {e}",
                AnomalySeverity.WARNING
            )
    
    def _load_state(self):
        """Load rhizome state from disk"""
        try:
            save_path = Path(self.config['save_path'])
            if not save_path.exists():
                return
            
            with open(save_path, 'rb') as f:
                state = pickle.load(f)
            
            self.nodes = state.get('nodes', {})
            self.connections = state.get('connections', {})
            self.entangled_pairs = state.get('entangled_pairs', set())
            
            # Rebuild indices
            self._rebuild_indices()
            
        except Exception as e:
            log_anomaly(
                "RHIZOME_LOAD_ERROR",
                f"Failed to load rhizome state: {e}",
                AnomalySeverity.WARNING
            )
    
    def _rebuild_indices(self):
        """Rebuild internal indices from loaded state"""
        # Clear indices
        self.type_index.clear()
        self.spatial_index.clear()
        self.outgoing_connections.clear()
        self.incoming_connections.clear()
        self.connection_by_nodes.clear()
        
        # Rebuild node indices
        for node_id, node in self.nodes.items():
            self.type_index[node.node_type].add(node_id)
            spatial_key = self._get_spatial_key(node.position)
            self.spatial_index[spatial_key].add(node_id)
        
        # Rebuild connection indices
        for conn_id, conn in self.connections.items():
            self.outgoing_connections[conn.source_id].add(conn_id)
            self.incoming_connections[conn.target_id].add(conn_id)
            self.connection_by_nodes[(conn.source_id, conn.target_id)] = conn_id
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive network statistics"""
        with self.lock:
            # Calculate additional metrics
            avg_connections = (
                sum(len(node.connections) for node in self.nodes.values()) / 
                len(self.nodes)
            ) if self.nodes else 0
            
            node_type_counts = {
                node_type.value: len(nodes)
                for node_type, nodes in self.type_index.items()
            }
            
            connection_type_counts = defaultdict(int)
            for conn in self.connections.values():
                connection_type_counts[conn.connection_type.value] += 1
            
            return {
                'node_count': len(self.nodes),
                'connection_count': len(self.connections),
                'average_connections_per_node': round(avg_connections, 2),
                'node_types': node_type_counts,
                'connection_types': dict(connection_type_counts),
                'quantum_entanglements': len(self.entangled_pairs),
                'total_energy': round(self.total_energy, 2),
                'total_activation': round(self.total_activation, 2),
                'signal_count': self.signal_count,
                'reorganization_count': self.reorganization_count
            }
    
    def shutdown(self):
        """Shutdown the rhizome network"""
        self.shutdown_event.set()
        if self.processing_thread:
            self.processing_thread.join(timeout=5.0)
        self._save_state()

# Global instance
rhizome = RhizomeMap()