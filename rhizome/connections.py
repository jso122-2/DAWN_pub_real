# /rhizome/connections.py
"""
Rhizome Connection Management for DAWN
======================================
Manages the dynamic connections between nodes in the rhizome network,
including connection strength, learning, and emergent pathways.

Connections in the rhizome are not mere links but living conduits
of consciousness flow.
"""

import time
import math
import random
import numpy as np
from typing import Dict, List, Set, Tuple, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import threading
import heapq
import json

# Core imports
from core.schema_anomaly_logger import log_anomaly, AnomalySeverity
from ...rhizome_map import RhizomeMap, RhizomeNode, RhizomeConnection, ConnectionType, NodeType

class ConnectionState(Enum):
    """States of a connection lifecycle"""
    FORMING = "forming"          # Connection being established
    ACTIVE = "active"           # Normal active state
    STRENGTHENING = "strengthening"  # Being reinforced
    WEAKENING = "weakening"     # Losing strength
    DORMANT = "dormant"         # Inactive but maintained
    PRUNING = "pruning"         # Marked for removal

class SignalType(Enum):
    """Types of signals that flow through connections"""
    ACTIVATION = "activation"    # Neural activation
    INHIBITION = "inhibition"   # Neural inhibition
    MODULATION = "modulation"   # Modulatory signal
    SYNCHRONY = "synchrony"     # Synchronization pulse
    MEMORY = "memory"          # Memory transfer
    QUERY = "query"           # Information request
    RESPONSE = "response"      # Information response
    ENERGY = "energy"         # Energy transfer
    QUANTUM = "quantum"       # Quantum state

@dataclass
class Signal:
    """A signal traveling through connections"""
    signal_id: str
    signal_type: SignalType
    source_node: str
    target_node: Optional[str] = None  # None for broadcast
    payload: Any = None
    strength: float = 1.0
    timestamp: float = field(default_factory=time.time)
    path: List[str] = field(default_factory=list)
    hops: int = 0
    max_hops: int = 10
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ConnectionMetrics:
    """Metrics for connection performance"""
    total_signals: int = 0
    successful_transmissions: int = 0
    failed_transmissions: int = 0
    average_latency: float = 0.0
    total_energy_transferred: float = 0.0
    last_signal_time: float = 0.0
    activation_history: deque = field(default_factory=lambda: deque(maxlen=100))

class ConnectionLearning:
    """Hebbian learning rules for connection adaptation"""
    
    @staticmethod
    def hebbian_update(connection: RhizomeConnection, 
                      pre_activation: float,
                      post_activation: float,
                      learning_rate: float = 0.01) -> float:
        """Basic Hebbian learning: neurons that fire together wire together"""
        delta = learning_rate * pre_activation * post_activation
        return delta
    
    @staticmethod
    def oja_update(connection: RhizomeConnection,
                   pre_activation: float,
                   post_activation: float,
                   learning_rate: float = 0.01) -> float:
        """Oja's rule: Hebbian with normalization"""
        delta = learning_rate * (pre_activation * post_activation - 
                               connection.weight ** 2 * post_activation)
        return delta
    
    @staticmethod
    def bcm_update(connection: RhizomeConnection,
                   pre_activation: float,
                   post_activation: float,
                   threshold: float,
                   learning_rate: float = 0.01) -> float:
        """BCM (Bienenstock-Cooper-Munro) rule: adaptive threshold"""
        delta = learning_rate * pre_activation * post_activation * (post_activation - threshold)
        return delta
    
    @staticmethod
    def stdp_update(connection: RhizomeConnection,
                    pre_spike_time: float,
                    post_spike_time: float,
                    tau_plus: float = 20.0,
                    tau_minus: float = 20.0,
                    a_plus: float = 0.01,
                    a_minus: float = 0.01) -> float:
        """Spike-Timing Dependent Plasticity"""
        dt = post_spike_time - pre_spike_time
        
        if dt > 0:  # Pre before post: potentiation
            delta = a_plus * math.exp(-dt / tau_plus)
        else:  # Post before pre: depression
            delta = -a_minus * math.exp(dt / tau_minus)
        
        return delta

class ConnectionManager:
    """
    Manages all aspects of connections in the rhizome network.
    
    Features:
    - Connection lifecycle management
    - Signal routing and propagation
    - Learning and adaptation
    - Connection pooling and optimization
    - Pathway discovery and caching
    """
    
    def __init__(self, rhizome: RhizomeMap, config: Optional[Dict[str, Any]] = None):
        self.rhizome = rhizome
        
        # Configuration
        self.config = {
            'max_signal_queue': 10000,
            'learning_rate': 0.01,
            'pruning_threshold': 0.05,
            'strengthening_threshold': 0.8,
            'signal_decay': 0.9,
            'enable_learning': True,
            'enable_caching': True,
            'cache_size': 1000,
            'batch_size': 100,
            **(config or {})
        }
        
        # Connection tracking
        self.connection_states: Dict[str, ConnectionState] = {}
        self.connection_metrics: Dict[str, ConnectionMetrics] = defaultdict(ConnectionMetrics)
        
        # Signal management
        self.signal_queue: deque = deque(maxlen=self.config['max_signal_queue'])
        self.active_signals: Dict[str, Signal] = {}
        self.signal_history: deque = deque(maxlen=1000)
        
        # Path caching
        self.path_cache: Dict[Tuple[str, str], List[str]] = {}
        self.cache_hits = 0
        self.cache_misses = 0
        
        # Connection pools for efficiency
        self.connection_pools: Dict[ConnectionType, List[str]] = defaultdict(list)
        
        # Learning parameters
        self.learning_threshold = 0.5  # Adaptive threshold for BCM
        self.spike_times: Dict[str, float] = {}  # For STDP
        
        # Statistics
        self.total_signals_sent = 0
        self.total_signals_delivered = 0
        self.total_learning_updates = 0
        
        # Thread management
        self.lock = threading.RLock()
        self.processing_thread: Optional[threading.Thread] = None
        self.shutdown_event = threading.Event()
        
        # Initialize
        self._initialize()
    
    def _initialize(self):
        """Initialize the connection manager"""
        # Subscribe to rhizome events
        self.rhizome.subscribe('connection_added', self._on_connection_added)
        self.rhizome.subscribe('connection_removed', self._on_connection_removed)
        self.rhizome.subscribe('node_activated', self._on_node_activated)
        
        # Initialize existing connections
        for conn_id, conn in self.rhizome.connections.items():
            self.connection_states[conn_id] = ConnectionState.ACTIVE
            self.connection_pools[conn.connection_type].append(conn_id)
        
        # Start processing thread
        self._start_processing()
    
    def _start_processing(self):
        """Start the signal processing thread"""
        if self.processing_thread and self.processing_thread.is_alive():
            return
        
        self.shutdown_event.clear()
        self.processing_thread = threading.Thread(
            target=self._processing_loop,
            daemon=True
        )
        self.processing_thread.start()
    
    def _processing_loop(self):
        """Main processing loop for signals and maintenance"""
        while not self.shutdown_event.is_set():
            try:
                # Process signal queue
                self._process_signal_queue()
                
                # Update connection states
                self._update_connection_states()
                
                # Apply learning if enabled
                if self.config['enable_learning']:
                    self._apply_learning()
                
                # Prune weak connections
                self._prune_connections()
                
                # Clean up old cache entries
                if len(self.path_cache) > self.config['cache_size']:
                    self._clean_cache()
                
            except Exception as e:
                log_anomaly(
                    "CONNECTION_PROCESSING_ERROR",
                    str(e),
                    AnomalySeverity.ERROR
                )
            
            time.sleep(0.01)  # 100Hz processing
    
    def send_signal(self,
                   signal_type: SignalType,
                   source_node: str,
                   target_node: Optional[str] = None,
                   payload: Any = None,
                   strength: float = 1.0,
                   metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Send a signal through the network
        
        Args:
            signal_type: Type of signal
            source_node: Source node ID
            target_node: Target node ID (None for broadcast)
            payload: Signal payload
            strength: Signal strength
            metadata: Additional metadata
            
        Returns:
            Signal ID
        """
        with self.lock:
            signal_id = f"sig_{int(time.time() * 1000000)}_{random.randint(1000, 9999)}"
            
            signal = Signal(
                signal_id=signal_id,
                signal_type=signal_type,
                source_node=source_node,
                target_node=target_node,
                payload=payload,
                strength=strength,
                metadata=metadata or {}
            )
            
            signal.path.append(source_node)
            
            # Add to queue
            self.signal_queue.append(signal)
            self.active_signals[signal_id] = signal
            self.total_signals_sent += 1
            
            # Update spike time for STDP
            self.spike_times[source_node] = time.time()
            
            return signal_id
    
    def _process_signal_queue(self):
        """Process queued signals"""
        batch_size = min(self.config['batch_size'], len(self.signal_queue))
        
        for _ in range(batch_size):
            if not self.signal_queue:
                break
            
            signal = self.signal_queue.popleft()
            self._route_signal(signal)
    
    def _route_signal(self, signal: Signal):
        """Route a signal to its destination(s)"""
        try:
            current_node = signal.path[-1]
            
            # Check if reached destination
            if signal.target_node and current_node == signal.target_node:
                self._deliver_signal(signal)
                return
            
            # Check hop limit
            if signal.hops >= signal.max_hops:
                self._signal_failed(signal, "Max hops exceeded")
                return
            
            # Decay signal strength
            signal.strength *= self.config['signal_decay']
            if signal.strength < 0.1:
                self._signal_failed(signal, "Signal too weak")
                return
            
            # Find next hops
            if signal.target_node:
                # Directed signal - find path
                next_hops = self._find_next_hops(current_node, signal.target_node, signal)
            else:
                # Broadcast signal - send to all neighbors
                next_hops = self.rhizome.get_neighbors(current_node)
            
            # Propagate signal
            for next_hop in next_hops:
                if next_hop not in signal.path:  # Avoid loops
                    self._propagate_signal(signal, current_node, next_hop)
            
        except Exception as e:
            self._signal_failed(signal, str(e))
    
    def _find_next_hops(self, current: str, target: str, signal: Signal) -> List[str]:
        """Find next hops for a signal"""
        # Check cache
        cache_key = (current, target)
        if self.config['enable_caching'] and cache_key in self.path_cache:
            self.cache_hits += 1
            path = self.path_cache[cache_key]
            if len(path) > 1:
                return [path[1]]  # Next node in cached path
        else:
            self.cache_misses += 1
        
        # Use A* pathfinding for important signals
        if signal.signal_type in [SignalType.MEMORY, SignalType.QUERY]:
            path = self._astar_pathfind(current, target)
            if path and len(path) > 1:
                # Cache the path
                if self.config['enable_caching']:
                    self.path_cache[cache_key] = path
                return [path[1]]
        
        # Otherwise use greedy best neighbor
        neighbors = self.rhizome.get_neighbors(current)
        if not neighbors:
            return []
        
        # Score neighbors
        scored_neighbors = []
        target_node = self.rhizome.get_node(target)
        if not target_node:
            return []
        
        for neighbor_id in neighbors:
            neighbor = self.rhizome.get_node(neighbor_id)
            if neighbor:
                # Score based on distance to target and connection strength
                distance = neighbor.distance_to(target_node)
                conn = self.rhizome.get_connection(current, neighbor_id)
                if conn:
                    score = conn.strength / (1 + distance)
                    scored_neighbors.append((score, neighbor_id))
        
        # Sort by score and return top candidates
        scored_neighbors.sort(reverse=True)
        return [n[1] for n in scored_neighbors[:3]]  # Top 3 candidates
    
    def _astar_pathfind(self, start: str, goal: str) -> Optional[List[str]]:
        """A* pathfinding algorithm"""
        start_node = self.rhizome.get_node(start)
        goal_node = self.rhizome.get_node(goal)
        
        if not start_node or not goal_node:
            return None
        
        # Priority queue: (f_score, node_id)
        open_set = [(0, start)]
        came_from = {}
        
        g_score = {start: 0}
        f_score = {start: start_node.distance_to(goal_node)}
        
        while open_set:
            current_f, current = heapq.heappop(open_set)
            
            if current == goal:
                # Reconstruct path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path
            
            current_node = self.rhizome.get_node(current)
            if not current_node:
                continue
            
            for neighbor_id in self.rhizome.get_neighbors(current):
                neighbor = self.rhizome.get_node(neighbor_id)
                if not neighbor:
                    continue
                
                # Calculate tentative g_score
                conn = self.rhizome.get_connection(current, neighbor_id)
                if not conn:
                    continue
                
                # Cost is inversely proportional to connection strength
                edge_cost = 1.0 / (conn.strength + 0.1)
                tentative_g = g_score[current] + edge_cost
                
                if neighbor_id not in g_score or tentative_g < g_score[neighbor_id]:
                    came_from[neighbor_id] = current
                    g_score[neighbor_id] = tentative_g
                    f = tentative_g + neighbor.distance_to(goal_node)
                    f_score[neighbor_id] = f
                    heapq.heappush(open_set, (f, neighbor_id))
        
        return None  # No path found
    
    def _propagate_signal(self, signal: Signal, from_node: str, to_node: str):
        """Propagate a signal to the next node"""
        # Get connection
        conn = self.rhizome.get_connection(from_node, to_node)
        if not conn:
            return
        
        # Clone signal for propagation
        new_signal = Signal(
            signal_id=f"{signal.signal_id}_hop{signal.hops + 1}",
            signal_type=signal.signal_type,
            source_node=signal.source_node,
            target_node=signal.target_node,
            payload=signal.payload,
            strength=signal.strength,
            timestamp=signal.timestamp,
            path=signal.path + [to_node],
            hops=signal.hops + 1,
            max_hops=signal.max_hops,
            metadata=signal.metadata.copy()
        )
        
        # Update connection metrics
        metrics = self.connection_metrics[conn.connection_id]
        metrics.total_signals += 1
        metrics.last_signal_time = time.time()
        
        # Apply connection-specific modulation
        if conn.connection_type == ConnectionType.QUANTUM:
            # Quantum connections don't decay
            new_signal.strength = signal.strength
        elif conn.connection_type == ConnectionType.SYNAPTIC:
            # Synaptic connections modulate by weight
            new_signal.strength *= conn.weight
        
        # Add latency delay
        if conn.latency > 0:
            threading.Timer(conn.latency, self._deliver_to_node, args=[new_signal, to_node]).start()
        else:
            self._deliver_to_node(new_signal, to_node)
        
        # Strengthen connection
        conn.strengthen(0.01)
        
        # Record successful transmission
        metrics.successful_transmissions += 1
    
    def _deliver_to_node(self, signal: Signal, node_id: str):
        """Deliver signal to a specific node"""
        # Activate the node
        self.rhizome.activate_node(node_id, signal.strength)
        
        # Update spike time for STDP
        self.spike_times[node_id] = time.time()
        
        # Add back to queue if not at destination
        if signal.target_node and node_id != signal.target_node:
            self.signal_queue.append(signal)
        else:
            self._deliver_signal(signal)
    
    def _deliver_signal(self, signal: Signal):
        """Final delivery of signal to destination"""
        self.total_signals_delivered += 1
        
        # Record in history
        self.signal_history.append({
            'signal_id': signal.signal_id,
            'delivered_at': time.time(),
            'path': signal.path,
            'hops': signal.hops,
            'final_strength': signal.strength
        })
        
        # Remove from active signals
        if signal.signal_id in self.active_signals:
            del self.active_signals[signal.signal_id]
        
        # Log successful delivery
        if signal.hops > 5:
            log_anomaly(
                "LONG_SIGNAL_PATH",
                f"Signal traveled {signal.hops} hops",
                AnomalySeverity.INFO,
                {'signal_type': signal.signal_type.value, 'path_length': signal.hops}
            )
    
    def _signal_failed(self, signal: Signal, reason: str):
        """Handle failed signal delivery"""
        # Update metrics
        if signal.path:
            for i in range(len(signal.path) - 1):
                conn = self.rhizome.get_connection(signal.path[i], signal.path[i + 1])
                if conn:
                    metrics = self.connection_metrics[conn.connection_id]
                    metrics.failed_transmissions += 1
        
        # Remove from active signals
        if signal.signal_id in self.active_signals:
            del self.active_signals[signal.signal_id]
    
    def _update_connection_states(self):
        """Update connection states based on metrics"""
        current_time = time.time()
        
        with self.lock:
            for conn_id, conn in self.rhizome.connections.items():
                metrics = self.connection_metrics[conn_id]
                current_state = self.connection_states.get(conn_id, ConnectionState.ACTIVE)
                
                # Determine new state
                if conn.strength < self.config['pruning_threshold']:
                    new_state = ConnectionState.PRUNING
                elif conn.strength > self.config['strengthening_threshold']:
                    new_state = ConnectionState.STRENGTHENING
                elif current_time - metrics.last_signal_time > 300:  # 5 minutes inactive
                    new_state = ConnectionState.DORMANT
                elif metrics.failed_transmissions > metrics.successful_transmissions:
                    new_state = ConnectionState.WEAKENING
                else:
                    new_state = ConnectionState.ACTIVE
                
                # Update state
                if new_state != current_state:
                    self.connection_states[conn_id] = new_state
                    self._handle_state_transition(conn_id, current_state, new_state)
    
    def _handle_state_transition(self, conn_id: str, old_state: ConnectionState, new_state: ConnectionState):
        """Handle connection state transitions"""
        conn = self.rhizome.connections.get(conn_id)
        if not conn:
            return
        
        if new_state == ConnectionState.STRENGTHENING:
            # Boost connection weight
            conn.weight = min(2.0, conn.weight * 1.1)
            
        elif new_state == ConnectionState.WEAKENING:
            # Reduce connection weight
            conn.weight = max(0.1, conn.weight * 0.9)
            
        elif new_state == ConnectionState.DORMANT:
            # Reduce maintenance cost
            conn.weight *= 0.95
    
    def _apply_learning(self):
        """Apply learning rules to connections"""
        with self.lock:
            # Sample connections for learning
            sample_size = min(100, len(self.rhizome.connections))
            if sample_size == 0:
                return
            
            sampled_conns = random.sample(list(self.rhizome.connections.values()), sample_size)
            
            for conn in sampled_conns:
                # Get node activations
                source_node = self.rhizome.get_node(conn.source_id)
                target_node = self.rhizome.get_node(conn.target_id)
                
                if not source_node or not target_node:
                    continue
                
                # Apply appropriate learning rule
                if conn.connection_type == ConnectionType.SYNAPTIC:
                    # Hebbian learning
                    delta = ConnectionLearning.hebbian_update(
                        conn,
                        source_node.activation,
                        target_node.activation,
                        self.config['learning_rate']
                    )
                    
                elif conn.connection_type == ConnectionType.TEMPORAL:
                    # STDP learning
                    if conn.source_id in self.spike_times and conn.target_id in self.spike_times:
                        delta = ConnectionLearning.stdp_update(
                            conn,
                            self.spike_times[conn.source_id],
                            self.spike_times[conn.target_id]
                        )
                    else:
                        delta = 0
                        
                else:
                    # BCM learning for other types
                    delta = ConnectionLearning.bcm_update(
                        conn,
                        source_node.activation,
                        target_node.activation,
                        self.learning_threshold,
                        self.config['learning_rate']
                    )
                
                # Apply weight update
                if delta != 0:
                    conn.weight = max(0.1, min(2.0, conn.weight + delta))
                    self.total_learning_updates += 1
            
            # Update learning threshold (moving average of activations)
            avg_activation = sum(n.activation for n in self.rhizome.nodes.values()) / max(1, len(self.rhizome.nodes))
            self.learning_threshold = 0.9 * self.learning_threshold + 0.1 * avg_activation
    
    def _prune_connections(self):
        """Prune weak connections"""
        with self.lock:
            connections_to_prune = [
                conn_id for conn_id, state in self.connection_states.items()
                if state == ConnectionState.PRUNING
            ]
            
            for conn_id in connections_to_prune:
                if self.rhizome.remove_connection(conn_id):
                    del self.connection_states[conn_id]
                    del self.connection_metrics[conn_id]
    
    def _clean_cache(self):
        """Clean old entries from path cache"""
        # Remove random 20% of cache
        remove_count = len(self.path_cache) // 5
        for _ in range(remove_count):
            if self.path_cache:
                self.path_cache.pop(random.choice(list(self.path_cache.keys())))
    
    def create_pathway(self, source: str, target: str, pathway_type: str = "default") -> bool:
        """
        Create a dedicated pathway between two nodes
        
        Args:
            source: Source node ID
            target: Target node ID
            pathway_type: Type of pathway to create
            
        Returns:
            True if pathway created successfully
        """
        with self.lock:
            # Find shortest path
            path = self.rhizome.find_path(source, target)
            if not path or len(path) < 2:
                return False
            
            # Strengthen all connections along path
            for i in range(len(path) - 1):
                conn = self.rhizome.get_connection(path[i], path[i + 1])
                if not conn:
                    # Create missing connection
                    conn = self.rhizome.add_connection(
                        path[i], 
                        path[i + 1],
                        ConnectionType.SYNAPTIC,
                        strength=0.5
                    )
                
                if conn:
                    # Strengthen connection
                    conn.strengthen(0.2)
                    conn.metadata['pathway'] = pathway_type
                    
                    # Mark as part of pathway
                    self.connection_states[conn.connection_id] = ConnectionState.STRENGTHENING
            
            # Cache the pathway
            self.path_cache[(source, target)] = path
            
            return True
    
    def get_connection_metrics(self, conn_id: str) -> Optional[ConnectionMetrics]:
        """Get metrics for a specific connection"""
        return self.connection_metrics.get(conn_id)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get connection manager statistics"""
        with self.lock:
            state_counts = defaultdict(int)
            for state in self.connection_states.values():
                state_counts[state.value] += 1
            
            cache_hit_rate = (
                self.cache_hits / max(1, self.cache_hits + self.cache_misses)
            ) if self.config['enable_caching'] else 0
            
            return {
                'total_signals_sent': self.total_signals_sent,
                'total_signals_delivered': self.total_signals_delivered,
                'delivery_rate': self.total_signals_delivered / max(1, self.total_signals_sent),
                'active_signals': len(self.active_signals),
                'signal_queue_size': len(self.signal_queue),
                'connection_states': dict(state_counts),
                'total_learning_updates': self.total_learning_updates,
                'cache_hit_rate': round(cache_hit_rate, 3),
                'cached_paths': len(self.path_cache),
                'learning_threshold': round(self.learning_threshold, 3)
            }
    
    def _on_connection_added(self, rhizome: RhizomeMap, connection: RhizomeConnection):
        """Handle new connection added to rhizome"""
        self.connection_states[connection.connection_id] = ConnectionState.FORMING
        self.connection_pools[connection.connection_type].append(connection.connection_id)
    
    def _on_connection_removed(self, rhizome: RhizomeMap, conn_id: str):
        """Handle connection removed from rhizome"""
        if conn_id in self.connection_states:
            del self.connection_states[conn_id]
        if conn_id in self.connection_metrics:
            del self.connection_metrics[conn_id]
    
    def _on_node_activated(self, rhizome: RhizomeMap, node_id: str, activation: float):
        """Handle node activation"""
        # Send activation signal to neighbors
        if activation > 0.5:  # Threshold for propagation
            self.send_signal(
                SignalType.ACTIVATION,
                node_id,
                payload={'activation': activation}
            )
    
    def shutdown(self):
        """Shutdown the connection manager"""
        self.shutdown_event.set()
        if self.processing_thread:
            self.processing_thread.join(timeout=5.0)