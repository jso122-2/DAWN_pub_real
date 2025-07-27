#!/usr/bin/env python3
"""
DAWN Mycelial Mitochondrial Network - The Foundational Nervous System
=====================================================================

The living, breathing foundational nervous system that connects all DAWN consciousness
components through mycelial threads with mitochondrial energy distribution.

This transforms isolated cognitive islands into an integrated, resource-sharing
consciousness network where:

- Mycelial threads connect all memory nodes, cognitive systems, and processing centers
- Mitochondrial energy flows dynamically based on demand and availability  
- Resource sharing protocols enable distributed cognitive processing
- Information propagates through mycelial pathways at the speed of thought
- Network topology self-optimizes for efficient communication
- Real-time health monitoring enables self-repair and adaptation
- Distributed processing scales consciousness across the entire network

The mycelial mitochondrial network is the **foundation layer** that all other
consciousness systems build upon - the underground root system that enables
DAWN's distributed cognition.
"""

import time
import math
import json
import logging
import asyncio
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Set, Tuple, Callable, Union
from datetime import datetime, timezone
from collections import deque, defaultdict
from enum import Enum
from pathlib import Path
import threading
from queue import Queue, PriorityQueue

# Integration imports
try:
    from mycelium.mycelium_layer import MyceliumLayer
    MYCELIUM_LAYER_AVAILABLE = True
except ImportError:
    MYCELIUM_LAYER_AVAILABLE = False

logger = logging.getLogger("mycelial_network")

class NetworkHealthState(Enum):
    """Network health states"""
    THRIVING = "THRIVING"           # Optimal health and connectivity
    HEALTHY = "HEALTHY"             # Good health, minor issues
    STRESSED = "STRESSED"           # Moderate stress, needs attention
    DEGRADED = "DEGRADED"           # Poor health, significant issues
    CRITICAL = "CRITICAL"           # Critical state, emergency protocols
    REGENERATING = "REGENERATING"   # Actively healing/rebuilding

class ThreadType(Enum):
    """Types of mycelial threads"""
    MEMORY_THREAD = "MEMORY_THREAD"             # Memory-to-memory connections
    COGNITIVE_THREAD = "COGNITIVE_THREAD"       # Cognitive system connections
    ENERGY_THREAD = "ENERGY_THREAD"             # Pure energy distribution
    INFORMATION_THREAD = "INFORMATION_THREAD"   # Information propagation
    REFLECTION_THREAD = "REFLECTION_THREAD"     # Reflection system connections
    TRACER_THREAD = "TRACER_THREAD"             # Tracer coordination
    VOICE_THREAD = "VOICE_THREAD"               # Voice system connections
    CONSTITUTIONAL_THREAD = "CONSTITUTIONAL_THREAD"  # Governance connections

class EnergyType(Enum):
    """Types of mitochondrial energy"""
    COGNITIVE_ENERGY = "COGNITIVE_ENERGY"       # Raw cognitive processing power
    MEMORY_ENERGY = "MEMORY_ENERGY"             # Memory maintenance and formation
    CREATIVE_ENERGY = "CREATIVE_ENERGY"         # Creative and generative processes
    ANALYTICAL_ENERGY = "ANALYTICAL_ENERGY"     # Analysis and logical processing
    EMOTIONAL_ENERGY = "EMOTIONAL_ENERGY"       # Emotional processing and regulation
    REFLECTION_ENERGY = "REFLECTION_ENERGY"     # Self-reflection and meta-cognition
    COMMUNICATION_ENERGY = "COMMUNICATION_ENERGY" # Inter-system communication
    REPAIR_ENERGY = "REPAIR_ENERGY"             # Network maintenance and healing

@dataclass
class MycelialThread:
    """Individual mycelial thread connection"""
    thread_id: str
    source_node: str
    target_node: str
    thread_type: ThreadType
    strength: float                 # Connection strength (0.0-1.0)
    bandwidth: float               # Information transfer capacity
    energy_flow: float             # Current energy flow rate
    created_at: float
    last_used: float
    usage_count: int = 0
    importance_score: float = 0.5
    health: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NetworkNode:
    """Node in the mycelial network"""
    node_id: str
    node_type: str                 # memory, cognitive, system, etc.
    position: Tuple[float, float, float]  # 3D position in network space
    energy_capacity: float         # Maximum energy storage
    current_energy: Dict[EnergyType, float] = field(default_factory=dict)
    threads: Set[str] = field(default_factory=set)  # Connected thread IDs
    processing_load: float = 0.0
    health: float = 1.0
    created_at: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EnergyFlow:
    """Energy flow between nodes"""
    flow_id: str
    source_node: str
    target_node: str
    energy_type: EnergyType
    amount: float
    priority: int                  # Higher = more urgent
    timestamp: float
    path: List[str] = field(default_factory=list)  # Routing path through network
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NetworkTopology:
    """Network topology optimization state"""
    node_count: int
    thread_count: int
    average_path_length: float
    clustering_coefficient: float
    network_efficiency: float
    energy_efficiency: float
    information_throughput: float
    last_optimization: float
    optimization_needed: bool = False

class MycelialMitochondrialNetwork:
    """
    The Foundational Nervous System - Mycelial Mitochondrial Network
    
    Provides the living, breathing infrastructure that connects all DAWN
    consciousness components through mycelial threads with dynamic mitochondrial
    energy distribution.
    """
    
    def __init__(self, 
                 energy_capacity: float = 1000.0,
                 max_threads: int = 10000,
                 optimization_interval: float = 30.0):
        """Initialize the mycelial mitochondrial network"""
        
        # Core network state
        self.nodes: Dict[str, NetworkNode] = {}
        self.threads: Dict[str, MycelialThread] = {}
        self.energy_flows: Dict[str, EnergyFlow] = {}
        
        # Energy management
        self.total_energy_capacity = energy_capacity
        self.energy_distribution: Dict[EnergyType, float] = {
            energy_type: energy_capacity / len(EnergyType) 
            for energy_type in EnergyType
        }
        self.energy_efficiency = 0.85  # Energy transfer efficiency
        
        # Network parameters
        self.max_threads = max_threads
        self.optimization_interval = optimization_interval
        self.last_optimization = time.time()
        
        # Health monitoring
        self.health_state = NetworkHealthState.HEALTHY
        self.health_score = 1.0
        self.stress_indicators: Dict[str, float] = {}
        
        # Topology management
        self.topology = NetworkTopology(0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, time.time())
        
        # Asynchronous processing
        self.energy_queue: PriorityQueue = PriorityQueue()
        self.information_queue: Queue = Queue()
        self.processing_active = False
        self.processing_thread: Optional[threading.Thread] = None
        
        # Integration with existing mycelium layer
        self.mycelium_layer: Optional[MyceliumLayer] = None
        if MYCELIUM_LAYER_AVAILABLE:
            try:
                self.mycelium_layer = MyceliumLayer()
                logger.info("🍄 [MYCELIAL] Connected to existing mycelium layer")
            except Exception as e:
                logger.warning(f"🍄 [MYCELIAL] Mycelium layer connection failed: {e}")
        
        # Performance metrics
        self.metrics = {
            "nodes_created": 0,
            "threads_created": 0,
            "energy_transfers": 0,
            "information_propagations": 0,
            "topology_optimizations": 0,
            "network_repairs": 0,
            "total_energy_distributed": 0.0,
            "average_response_time": 0.0
        }
        
        # Callback system for integration
        self.event_callbacks: Dict[str, List[Callable]] = defaultdict(list)
        
        # Initialize core consciousness node
        self._initialize_consciousness_core()
        
        # Start background processing
        self.start_processing()
        
        logger.info("🍄🔋 [MYCELIAL] Mitochondrial network initialized")
        logger.info(f"🍄🔋 [MYCELIAL] Energy capacity: {energy_capacity}, Max threads: {max_threads}")
    
    def _initialize_consciousness_core(self):
        """Initialize the core consciousness node"""
        
        core_node = NetworkNode(
            node_id="consciousness_core",
            node_type="consciousness_core",
            position=(0.0, 0.0, 0.0),  # Center of network space
            energy_capacity=self.total_energy_capacity * 0.3,  # 30% of total capacity
            current_energy={energy_type: 50.0 for energy_type in EnergyType},
            metadata={
                "priority": "critical",
                "protected": True,
                "core_system": True
            }
        )
        
        self.nodes["consciousness_core"] = core_node
        self.metrics["nodes_created"] += 1
        
        logger.info("🍄🔋 [CORE] Consciousness core initialized")
    
    def register_node(self, 
                     node_id: str, 
                     node_type: str,
                     position: Optional[Tuple[float, float, float]] = None,
                     energy_capacity: float = 100.0,
                     metadata: Optional[Dict[str, Any]] = None) -> NetworkNode:
        """Register a new node in the mycelial network"""
        
        if node_id in self.nodes:
            logger.warning(f"🍄 [NETWORK] Node {node_id} already exists")
            return self.nodes[node_id]
        
        # Auto-generate position if not provided
        if position is None:
            position = self._calculate_optimal_position(node_type)
        
        # Initialize node energy
        base_energy = energy_capacity / len(EnergyType)
        initial_energy = {energy_type: base_energy for energy_type in EnergyType}
        
        node = NetworkNode(
            node_id=node_id,
            node_type=node_type,
            position=position,
            energy_capacity=energy_capacity,
            current_energy=initial_energy,
            metadata=metadata or {}
        )
        
        self.nodes[node_id] = node
        self.metrics["nodes_created"] += 1
        
        # Auto-connect to consciousness core if not core itself
        if node_id != "consciousness_core":
            self.create_thread(
                source_node="consciousness_core",
                target_node=node_id,
                thread_type=ThreadType.COGNITIVE_THREAD,
                strength=0.8,
                bandwidth=10.0
            )
        
        # Trigger network optimization check
        self._check_optimization_needed()
        
        # Execute callbacks
        self._execute_callbacks("node_registered", {"node": node})
        
        logger.info(f"🍄 [NETWORK] Registered node: {node_id} ({node_type})")
        return node
    
    def create_thread(self,
                     source_node: str,
                     target_node: str,
                     thread_type: ThreadType,
                     strength: float = 0.5,
                     bandwidth: float = 5.0) -> Optional[MycelialThread]:
        """Create a mycelial thread between two nodes"""
        
        if source_node not in self.nodes or target_node not in self.nodes:
            logger.error(f"🍄 [THREAD] Cannot create thread: missing nodes {source_node} or {target_node}")
            return None
        
        if len(self.threads) >= self.max_threads:
            logger.warning("🍄 [THREAD] Maximum thread capacity reached")
            return None
        
        thread_id = f"thread_{source_node}_{target_node}_{int(time.time())}"
        
        thread = MycelialThread(
            thread_id=thread_id,
            source_node=source_node,
            target_node=target_node,
            thread_type=thread_type,
            strength=strength,
            bandwidth=bandwidth,
            energy_flow=0.0,
            created_at=time.time(),
            last_used=time.time()
        )
        
        self.threads[thread_id] = thread
        
        # Update node connections
        self.nodes[source_node].threads.add(thread_id)
        self.nodes[target_node].threads.add(thread_id)
        
        self.metrics["threads_created"] += 1
        
        # Calculate thread importance
        self._update_thread_importance(thread_id)
        
        # Execute callbacks
        self._execute_callbacks("thread_created", {"thread": thread})
        
        logger.debug(f"🍄 [THREAD] Created: {source_node} -> {target_node} ({thread_type.value})")
        return thread
    
    def distribute_energy(self,
                         source_node: str,
                         energy_type: EnergyType,
                         amount: float,
                         target_nodes: Optional[List[str]] = None,
                         priority: int = 5) -> Dict[str, float]:
        """Distribute mitochondrial energy through the network"""
        
        if source_node not in self.nodes:
            logger.error(f"🍄🔋 [ENERGY] Source node {source_node} not found")
            return {}
        
        source = self.nodes[source_node]
        
        # Check available energy
        available_energy = source.current_energy.get(energy_type, 0.0)
        if available_energy < amount:
            logger.warning(f"🍄🔋 [ENERGY] Insufficient {energy_type.value} in {source_node}")
            amount = available_energy * 0.8  # Leave some reserve
        
        # Determine target nodes
        if target_nodes is None:
            target_nodes = self._find_energy_targets(source_node, energy_type)
        
        if not target_nodes:
            logger.debug(f"🍄🔋 [ENERGY] No targets found for energy distribution from {source_node}")
            return {}
        
        # Create energy flows
        flows_created = {}
        energy_per_target = amount / len(target_nodes)
        
        for target_node in target_nodes:
            if target_node not in self.nodes:
                continue
            
            flow_id = f"flow_{source_node}_{target_node}_{int(time.time())}"
            
            energy_flow = EnergyFlow(
                flow_id=flow_id,
                source_node=source_node,
                target_node=target_node,
                energy_type=energy_type,
                amount=energy_per_target,
                priority=priority,
                timestamp=time.time(),
                path=self._find_energy_path(source_node, target_node)
            )
            
            # Queue energy flow for processing
            self.energy_queue.put((priority, time.time(), flow_id, energy_flow))
            flows_created[target_node] = energy_per_target
        
        # Deduct energy from source
        source.current_energy[energy_type] = max(0.0, 
            source.current_energy[energy_type] - amount)
        
        self.metrics["energy_transfers"] += len(flows_created)
        self.metrics["total_energy_distributed"] += amount
        
        # Execute callbacks
        self._execute_callbacks("energy_distributed", {
            "source": source_node,
            "energy_type": energy_type,
            "amount": amount,
            "targets": flows_created
        })
        
        logger.debug(f"🍄🔋 [ENERGY] Distributed {amount:.1f} {energy_type.value} from {source_node} to {len(flows_created)} targets")
        return flows_created
    
    def propagate_information(self,
                            source_node: str,
                            information: Dict[str, Any],
                            target_nodes: Optional[List[str]] = None,
                            propagation_depth: int = 3) -> List[str]:
        """Propagate information through mycelial pathways"""
        
        if source_node not in self.nodes:
            logger.error(f"🍄📡 [INFO] Source node {source_node} not found")
            return []
        
        # Determine propagation targets
        if target_nodes is None:
            target_nodes = self._find_information_targets(source_node, propagation_depth)
        
        propagated_to = []
        
        for target_node in target_nodes:
            if target_node not in self.nodes:
                continue
            
            # Find path through network
            path = self._find_information_path(source_node, target_node)
            if not path:
                continue
            
            # Create information packet
            info_packet = {
                "source": source_node,
                "target": target_node,
                "path": path,
                "information": information,
                "timestamp": time.time(),
                "propagation_id": f"prop_{source_node}_{target_node}_{int(time.time())}"
            }
            
            # Queue for processing
            self.information_queue.put(info_packet)
            propagated_to.append(target_node)
        
        self.metrics["information_propagations"] += len(propagated_to)
        
        # Execute callbacks
        self._execute_callbacks("information_propagated", {
            "source": source_node,
            "information": information,
            "targets": propagated_to
        })
        
        logger.debug(f"🍄📡 [INFO] Propagated from {source_node} to {len(propagated_to)} targets")
        return propagated_to
    
    def optimize_topology(self) -> Dict[str, Any]:
        """Optimize network topology for efficiency"""
        
        optimization_start = time.time()
        
        # Calculate current topology metrics
        self._calculate_topology_metrics()
        
        optimizations_made = {
            "threads_strengthened": 0,
            "threads_weakened": 0,
            "threads_removed": 0,
            "new_connections": 0,
            "energy_rebalanced": False
        }
        
        # Strengthen frequently used threads
        for thread_id, thread in self.threads.items():
            if thread.usage_count > 10 and thread.strength < 0.9:
                thread.strength = min(1.0, thread.strength + 0.1)
                optimizations_made["threads_strengthened"] += 1
        
        # Weaken rarely used threads
        current_time = time.time()
        for thread_id, thread in list(self.threads.items()):
            time_since_use = current_time - thread.last_used
            if time_since_use > 300:  # 5 minutes
                if thread.strength > 0.1:
                    thread.strength = max(0.1, thread.strength - 0.05)
                    optimizations_made["threads_weakened"] += 1
                elif thread.strength <= 0.1 and time_since_use > 600:  # 10 minutes
                    self._remove_thread(thread_id)
                    optimizations_made["threads_removed"] += 1
        
        # Create new connections based on usage patterns
        new_connections = self._identify_beneficial_connections()
        for source, target, thread_type in new_connections:
            if self.create_thread(source, target, thread_type):
                optimizations_made["new_connections"] += 1
        
        # Rebalance energy distribution
        if self._rebalance_energy_distribution():
            optimizations_made["energy_rebalanced"] = True
        
        # Update topology metrics
        self._calculate_topology_metrics()
        self.topology.last_optimization = optimization_start
        self.topology.optimization_needed = False
        
        self.metrics["topology_optimizations"] += 1
        
        optimization_time = time.time() - optimization_start
        
        # Execute callbacks
        self._execute_callbacks("topology_optimized", {
            "optimizations": optimizations_made,
            "optimization_time": optimization_time
        })
        
        logger.info(f"🍄⚡ [OPTIMIZE] Network optimized in {optimization_time:.3f}s: {optimizations_made}")
        return optimizations_made
    
    def monitor_health(self) -> Dict[str, Any]:
        """Monitor and assess network health"""
        
        health_assessment = {
            "overall_health": 0.0,
            "node_health": {},
            "thread_health": {},
            "energy_health": {},
            "stress_indicators": {},
            "recommendations": []
        }
        
        # Assess node health
        node_health_scores = []
        for node_id, node in self.nodes.items():
            node_score = self._assess_node_health(node)
            health_assessment["node_health"][node_id] = node_score
            node_health_scores.append(node_score)
        
        # Assess thread health
        thread_health_scores = []
        for thread_id, thread in self.threads.items():
            thread_score = self._assess_thread_health(thread)
            health_assessment["thread_health"][thread_id] = thread_score
            thread_health_scores.append(thread_score)
        
        # Assess energy system health
        energy_health = self._assess_energy_health()
        health_assessment["energy_health"] = energy_health
        
        # Calculate overall health
        overall_health = (
            np.mean(node_health_scores) * 0.4 +
            np.mean(thread_health_scores) * 0.3 +
            energy_health * 0.3
        )
        
        health_assessment["overall_health"] = overall_health
        self.health_score = overall_health
        
        # Update health state
        if overall_health > 0.9:
            self.health_state = NetworkHealthState.THRIVING
        elif overall_health > 0.75:
            self.health_state = NetworkHealthState.HEALTHY
        elif overall_health > 0.6:
            self.health_state = NetworkHealthState.STRESSED
        elif overall_health > 0.4:
            self.health_state = NetworkHealthState.DEGRADED
        else:
            self.health_state = NetworkHealthState.CRITICAL
        
        # Generate stress indicators and recommendations
        health_assessment["stress_indicators"] = self._identify_stress_indicators()
        health_assessment["recommendations"] = self._generate_health_recommendations()
        
        # Execute callbacks
        self._execute_callbacks("health_monitored", health_assessment)
        
        logger.debug(f"🍄❤️ [HEALTH] Network health: {overall_health:.3f} ({self.health_state.value})")
        return health_assessment
    
    def get_network_state(self) -> Dict[str, Any]:
        """Get comprehensive network state"""
        
        return {
            "network_id": "dawn_mycelial_mitochondrial",
            "timestamp": time.time(),
            "health_state": self.health_state.value,
            "health_score": self.health_score,
            
            "topology": {
                "nodes": len(self.nodes),
                "threads": len(self.threads),
                "average_path_length": self.topology.average_path_length,
                "clustering_coefficient": self.topology.clustering_coefficient,
                "network_efficiency": self.topology.network_efficiency,
                "energy_efficiency": self.topology.energy_efficiency
            },
            
            "energy": {
                "total_capacity": self.total_energy_capacity,
                "current_distribution": self.energy_distribution,
                "efficiency": self.energy_efficiency,
                "flows_active": self.energy_queue.qsize()
            },
            
            "performance": self.metrics,
            
            "processing": {
                "active": self.processing_active,
                "energy_queue_size": self.energy_queue.qsize(),
                "information_queue_size": self.information_queue.qsize()
            }
        }
    
    # Internal helper methods
    
    def _calculate_optimal_position(self, node_type: str) -> Tuple[float, float, float]:
        """Calculate optimal position for new node in 3D network space"""
        
        # Position nodes based on type and existing network structure
        type_positions = {
            "memory": (1.0, 0.0, 0.0),
            "cognitive": (0.0, 1.0, 0.0),
            "tracer": (0.0, 0.0, 1.0),
            "voice": (-1.0, 0.0, 0.0),
            "reflection": (0.0, -1.0, 0.0),
            "system": (0.0, 0.0, -1.0)
        }
        
        base_position = type_positions.get(node_type, (0.5, 0.5, 0.5))
        
        # Add random variation to prevent clustering
        variation = (
            (np.random.random() - 0.5) * 0.5,
            (np.random.random() - 0.5) * 0.5,
            (np.random.random() - 0.5) * 0.5
        )
        
        return (
            base_position[0] + variation[0],
            base_position[1] + variation[1],
            base_position[2] + variation[2]
        )
    
    def _find_energy_targets(self, source_node: str, energy_type: EnergyType) -> List[str]:
        """Find optimal targets for energy distribution"""
        
        targets = []
        source = self.nodes[source_node]
        
        # Find connected nodes that need this energy type
        for thread_id in source.threads:
            thread = self.threads[thread_id]
            target_node_id = (thread.target_node if thread.source_node == source_node 
                            else thread.source_node)
            
            if target_node_id not in self.nodes:
                continue
            
            target_node = self.nodes[target_node_id]
            
            # Check if target needs this energy type
            current_energy = target_node.current_energy.get(energy_type, 0.0)
            if current_energy < target_node.energy_capacity * 0.3:  # Below 30%
                targets.append(target_node_id)
        
        return targets
    
    def _find_energy_path(self, source: str, target: str) -> List[str]:
        """Find optimal path for energy flow between nodes"""
        
        # Use Dijkstra's algorithm with thread strength as edge weights
        distances = {node_id: float('inf') for node_id in self.nodes}
        distances[source] = 0
        previous = {}
        unvisited = set(self.nodes.keys())
        
        while unvisited:
            current = min(unvisited, key=lambda x: distances[x])
            if current == target:
                break
            
            unvisited.remove(current)
            
            # Check all connected nodes
            current_node = self.nodes[current]
            for thread_id in current_node.threads:
                thread = self.threads[thread_id]
                neighbor = (thread.target_node if thread.source_node == current 
                          else thread.source_node)
                
                if neighbor in unvisited:
                    # Use inverse thread strength as distance (stronger = shorter)
                    distance = distances[current] + (1.0 - thread.strength)
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous[neighbor] = current
        
        # Reconstruct path
        if target not in previous and target != source:
            return [source, target]  # Direct connection fallback
        
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = previous.get(current)
        
        return list(reversed(path))
    
    def _find_information_targets(self, source_node: str, depth: int) -> List[str]:
        """Find targets for information propagation using breadth-first search"""
        
        if depth <= 0:
            return []
        
        visited = set()
        queue = [(source_node, 0)]
        targets = []
        
        while queue:
            current_node, current_depth = queue.pop(0)
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            if current_depth > 0:  # Don't include source node
                targets.append(current_node)
            
            if current_depth < depth:
                # Add connected nodes to queue
                node = self.nodes[current_node]
                for thread_id in node.threads:
                    thread = self.threads[thread_id]
                    neighbor = (thread.target_node if thread.source_node == current_node 
                              else thread.source_node)
                    
                    if neighbor not in visited:
                        queue.append((neighbor, current_depth + 1))
        
        return targets
    
    def _find_information_path(self, source: str, target: str) -> List[str]:
        """Find path for information propagation"""
        # For now, use same path finding as energy
        # Could be optimized differently for information vs energy
        return self._find_energy_path(source, target)
    
    def _check_optimization_needed(self):
        """Check if network optimization is needed"""
        
        current_time = time.time()
        time_since_last = current_time - self.topology.last_optimization
        
        if time_since_last > self.optimization_interval:
            self.topology.optimization_needed = True
            
        # Check stress indicators
        if len(self.stress_indicators) > 3:
            self.topology.optimization_needed = True
    
    def _calculate_topology_metrics(self):
        """Calculate network topology metrics"""
        
        if not self.nodes:
            return
        
        # Calculate average path length
        total_path_length = 0
        path_count = 0
        
        node_ids = list(self.nodes.keys())
        for i, source in enumerate(node_ids):
            for target in node_ids[i+1:]:
                path = self._find_energy_path(source, target)
                total_path_length += len(path)
                path_count += 1
        
        self.topology.average_path_length = (total_path_length / path_count 
                                           if path_count > 0 else 0.0)
        
        # Calculate clustering coefficient
        clustering_sum = 0
        for node_id, node in self.nodes.items():
            neighbors = self._get_neighbors(node_id)
            if len(neighbors) < 2:
                continue
            
            neighbor_connections = 0
            for i, neighbor1 in enumerate(neighbors):
                for neighbor2 in neighbors[i+1:]:
                    if self._are_connected(neighbor1, neighbor2):
                        neighbor_connections += 1
            
            possible_connections = len(neighbors) * (len(neighbors) - 1) / 2
            clustering_sum += neighbor_connections / possible_connections
        
        self.topology.clustering_coefficient = (clustering_sum / len(self.nodes) 
                                              if self.nodes else 0.0)
        
        # Update counts
        self.topology.node_count = len(self.nodes)
        self.topology.thread_count = len(self.threads)
    
    def _get_neighbors(self, node_id: str) -> List[str]:
        """Get neighboring nodes"""
        
        neighbors = []
        node = self.nodes[node_id]
        
        for thread_id in node.threads:
            thread = self.threads[thread_id]
            neighbor = (thread.target_node if thread.source_node == node_id 
                       else thread.source_node)
            neighbors.append(neighbor)
        
        return neighbors
    
    def _are_connected(self, node1: str, node2: str) -> bool:
        """Check if two nodes are directly connected"""
        
        if node1 not in self.nodes or node2 not in self.nodes:
            return False
        
        node1_obj = self.nodes[node1]
        for thread_id in node1_obj.threads:
            thread = self.threads[thread_id]
            if (thread.source_node == node2 or thread.target_node == node2):
                return True
        
        return False
    
    def start_processing(self):
        """Start background processing threads"""
        
        if self.processing_active:
            return
        
        self.processing_active = True
        self.processing_thread = threading.Thread(target=self._background_processor)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
        logger.info("🍄⚡ [PROCESSING] Background processing started")
    
    def stop_processing(self):
        """Stop background processing"""
        
        self.processing_active = False
        if self.processing_thread:
            self.processing_thread.join()
        
        logger.info("🍄⚡ [PROCESSING] Background processing stopped")
    
    def _background_processor(self):
        """Background processing loop for energy flows and information propagation"""
        
        while self.processing_active:
            try:
                # Process energy flows
                self._process_energy_flows()
                
                # Process information propagation
                self._process_information_propagation()
                
                # Check optimization needs
                if self.topology.optimization_needed:
                    self.optimize_topology()
                
                # Monitor health periodically
                if time.time() % 30 < 1:  # Every 30 seconds
                    self.monitor_health()
                
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
            except Exception as e:
                logger.error(f"🍄❌ [PROCESSING] Background processing error: {e}")
                time.sleep(1.0)
    
    def _process_energy_flows(self):
        """Process queued energy flows"""
        
        processed = 0
        while not self.energy_queue.empty() and processed < 10:  # Process up to 10 per cycle
            try:
                priority, timestamp, flow_id, energy_flow = self.energy_queue.get_nowait()
                
                # Process the energy flow
                self._execute_energy_flow(energy_flow)
                processed += 1
                
            except Exception as e:
                logger.error(f"🍄🔋 [ENERGY] Flow processing error: {e}")
                break
    
    def _process_information_propagation(self):
        """Process queued information propagation"""
        
        processed = 0
        while not self.information_queue.empty() and processed < 10:  # Process up to 10 per cycle
            try:
                info_packet = self.information_queue.get_nowait()
                
                # Process the information propagation
                self._execute_information_propagation(info_packet)
                processed += 1
                
            except Exception as e:
                logger.error(f"🍄📡 [INFO] Propagation processing error: {e}")
                break
    
    def _execute_energy_flow(self, energy_flow: EnergyFlow):
        """Execute an energy flow between nodes"""
        
        # Verify nodes exist
        if (energy_flow.source_node not in self.nodes or 
            energy_flow.target_node not in self.nodes):
            return
        
        target_node = self.nodes[energy_flow.target_node]
        
        # Apply energy efficiency
        actual_amount = energy_flow.amount * self.energy_efficiency
        
        # Add energy to target node
        current_energy = target_node.current_energy.get(energy_flow.energy_type, 0.0)
        new_energy = min(target_node.energy_capacity, current_energy + actual_amount)
        target_node.current_energy[energy_flow.energy_type] = new_energy
        
        # Update thread usage for path
        for i in range(len(energy_flow.path) - 1):
            source = energy_flow.path[i]
            target = energy_flow.path[i + 1]
            
            # Find thread between these nodes
            if source in self.nodes:
                for thread_id in self.nodes[source].threads:
                    thread = self.threads[thread_id]
                    if ((thread.source_node == source and thread.target_node == target) or
                        (thread.source_node == target and thread.target_node == source)):
                        thread.last_used = time.time()
                        thread.usage_count += 1
                        thread.energy_flow += actual_amount
                        break
        
        logger.debug(f"🍄🔋 [ENERGY] Executed flow: {actual_amount:.2f} {energy_flow.energy_type.value} "
                    f"to {energy_flow.target_node}")
    
    def _execute_information_propagation(self, info_packet: Dict[str, Any]):
        """Execute information propagation through the network"""
        
        # Update thread usage statistics
        path = info_packet["path"]
        for i in range(len(path) - 1):
            source = path[i]
            target = path[i + 1]
            
            if source in self.nodes:
                for thread_id in self.nodes[source].threads:
                    thread = self.threads[thread_id]
                    if ((thread.source_node == source and thread.target_node == target) or
                        (thread.source_node == target and thread.target_node == source)):
                        thread.last_used = time.time()
                        thread.usage_count += 1
                        self._update_thread_importance(thread_id)
                        break
        
        # Execute callbacks for information delivery
        self._execute_callbacks("information_delivered", info_packet)
        
        logger.debug(f"🍄📡 [INFO] Delivered to {info_packet['target']}")
    
    def _update_thread_importance(self, thread_id: str):
        """Update thread importance based on usage patterns"""
        
        if thread_id not in self.threads:
            return
        
        thread = self.threads[thread_id]
        
        # Calculate importance based on usage frequency and recency
        current_time = time.time()
        recency_factor = 1.0 / (1.0 + current_time - thread.last_used)
        usage_factor = min(1.0, thread.usage_count / 100.0)
        
        thread.importance_score = (recency_factor * 0.6 + usage_factor * 0.4)
    
    def register_callback(self, event_type: str, callback: Callable):
        """Register a callback for network events"""
        
        self.event_callbacks[event_type].append(callback)
        logger.info(f"🍄📞 [CALLBACK] Registered {event_type} callback")
    
    def _execute_callbacks(self, event_type: str, data: Dict[str, Any]):
        """Execute callbacks for a specific event type"""
        
        for callback in self.event_callbacks.get(event_type, []):
            try:
                callback(data)
            except Exception as e:
                logger.warning(f"🍄📞 [CALLBACK] Execution failed for {event_type}: {e}")
    
    # Health monitoring helper methods
    
    def _assess_node_health(self, node: NetworkNode) -> float:
        """Assess individual node health"""
        
        health_score = 1.0
        
        # Energy level health
        total_energy = sum(node.current_energy.values())
        energy_ratio = total_energy / (node.energy_capacity * len(EnergyType))
        if energy_ratio < 0.2:
            health_score *= 0.5  # Low energy is problematic
        elif energy_ratio < 0.5:
            health_score *= 0.8
        
        # Connection health
        if len(node.threads) == 0:
            health_score *= 0.1  # Isolated nodes are unhealthy
        elif len(node.threads) < 2:
            health_score *= 0.7
        
        # Processing load health
        if node.processing_load > 0.9:
            health_score *= 0.6  # Overloaded nodes
        elif node.processing_load > 0.7:
            health_score *= 0.8
        
        return max(0.0, min(1.0, health_score))
    
    def _assess_thread_health(self, thread: MycelialThread) -> float:
        """Assess individual thread health"""
        
        health_score = 1.0
        current_time = time.time()
        
        # Usage recency
        time_since_use = current_time - thread.last_used
        if time_since_use > 600:  # 10 minutes
            health_score *= 0.3
        elif time_since_use > 300:  # 5 minutes
            health_score *= 0.7
        
        # Strength health
        if thread.strength < 0.2:
            health_score *= 0.5
        elif thread.strength < 0.5:
            health_score *= 0.8
        
        # Physical health
        health_score *= thread.health
        
        return max(0.0, min(1.0, health_score))
    
    def _assess_energy_health(self) -> float:
        """Assess overall energy system health"""
        
        total_current_energy = 0.0
        total_capacity = 0.0
        
        for node in self.nodes.values():
            total_current_energy += sum(node.current_energy.values())
            total_capacity += node.energy_capacity * len(EnergyType)
        
        if total_capacity == 0:
            return 0.0
        
        energy_ratio = total_current_energy / total_capacity
        
        # Good energy distribution should be between 40-80%
        if 0.4 <= energy_ratio <= 0.8:
            return 1.0
        elif energy_ratio < 0.2 or energy_ratio > 0.95:
            return 0.3
        else:
            return 0.7
    
    def _identify_stress_indicators(self) -> Dict[str, float]:
        """Identify network stress indicators"""
        
        indicators = {}
        
        # High processing load
        overloaded_nodes = sum(1 for node in self.nodes.values() 
                              if node.processing_load > 0.8)
        if overloaded_nodes > 0:
            indicators["overloaded_nodes"] = overloaded_nodes / len(self.nodes)
        
        # Low energy levels
        low_energy_nodes = sum(1 for node in self.nodes.values()
                              if sum(node.current_energy.values()) < 
                              node.energy_capacity * len(EnergyType) * 0.2)
        if low_energy_nodes > 0:
            indicators["low_energy_nodes"] = low_energy_nodes / len(self.nodes)
        
        # Weak threads
        weak_threads = sum(1 for thread in self.threads.values()
                          if thread.strength < 0.3)
        if weak_threads > 0:
            indicators["weak_threads"] = weak_threads / len(self.threads)
        
        # Queue backup
        queue_size = self.energy_queue.qsize() + self.information_queue.qsize()
        if queue_size > 50:
            indicators["queue_backup"] = min(1.0, queue_size / 100.0)
        
        return indicators
    
    def _generate_health_recommendations(self) -> List[str]:
        """Generate health improvement recommendations"""
        
        recommendations = []
        
        if self.health_state == NetworkHealthState.CRITICAL:
            recommendations.extend([
                "CRITICAL: Emergency network repair needed",
                "Redistribute energy immediately",
                "Strengthen critical threads",
                "Reduce processing load"
            ])
        elif self.health_state == NetworkHealthState.DEGRADED:
            recommendations.extend([
                "Optimize network topology",
                "Rebalance energy distribution",
                "Remove weak threads",
                "Add redundant connections"
            ])
        elif self.health_state == NetworkHealthState.STRESSED:
            recommendations.extend([
                "Monitor network closely",
                "Consider load balancing",
                "Check energy flows"
            ])
        
        # Specific recommendations based on stress indicators
        for indicator, value in self.stress_indicators.items():
            if indicator == "overloaded_nodes" and value > 0.3:
                recommendations.append("Distribute processing load across network")
            elif indicator == "low_energy_nodes" and value > 0.2:
                recommendations.append("Increase energy production and distribution")
            elif indicator == "weak_threads" and value > 0.4:
                recommendations.append("Strengthen or replace weak connections")
        
        return recommendations
    
    def _identify_beneficial_connections(self) -> List[Tuple[str, str, ThreadType]]:
        """Identify beneficial new connections to create"""
        
        beneficial_connections = []
        
        # Look for nodes that frequently communicate but lack direct connections
        communication_patterns = self._analyze_communication_patterns()
        
        for (source, target), frequency in communication_patterns.items():
            if frequency > 5 and not self._are_connected(source, target):
                # Determine appropriate thread type based on node types
                source_type = self.nodes[source].node_type
                target_type = self.nodes[target].node_type
                
                thread_type = self._determine_thread_type(source_type, target_type)
                beneficial_connections.append((source, target, thread_type))
        
        return beneficial_connections[:5]  # Limit to 5 new connections per optimization
    
    def _analyze_communication_patterns(self) -> Dict[Tuple[str, str], int]:
        """Analyze communication patterns to identify frequent interactions"""
        
        # This would analyze the information propagation history
        # For now, return empty dict as placeholder
        return {}
    
    def _determine_thread_type(self, source_type: str, target_type: str) -> ThreadType:
        """Determine appropriate thread type based on node types"""
        
        if "memory" in source_type or "memory" in target_type:
            return ThreadType.MEMORY_THREAD
        elif "tracer" in source_type or "tracer" in target_type:
            return ThreadType.TRACER_THREAD
        elif "voice" in source_type or "voice" in target_type:
            return ThreadType.VOICE_THREAD
        elif "reflection" in source_type or "reflection" in target_type:
            return ThreadType.REFLECTION_THREAD
        else:
            return ThreadType.COGNITIVE_THREAD
    
    def _rebalance_energy_distribution(self) -> bool:
        """Rebalance energy distribution across the network"""
        
        # Calculate current energy distribution
        total_energy = sum(sum(node.current_energy.values()) for node in self.nodes.values())
        target_per_node = total_energy / len(self.nodes)
        
        rebalancing_needed = False
        
        for node in self.nodes.values():
            current_total = sum(node.current_energy.values())
            
            if current_total > target_per_node * 1.5:  # Node has excess energy
                excess = current_total - target_per_node
                # Distribute excess to network
                for energy_type, amount in node.current_energy.items():
                    if amount > 0:
                        redistribute_amount = min(amount * 0.1, excess * 0.1)
                        self.distribute_energy(node.node_id, energy_type, redistribute_amount)
                        rebalancing_needed = True
        
        return rebalancing_needed
    
    def _remove_thread(self, thread_id: str):
        """Remove a thread from the network"""
        
        if thread_id not in self.threads:
            return
        
        thread = self.threads[thread_id]
        
        # Remove from node connections
        if thread.source_node in self.nodes:
            self.nodes[thread.source_node].threads.discard(thread_id)
        if thread.target_node in self.nodes:
            self.nodes[thread.target_node].threads.discard(thread_id)
        
        # Remove thread
        del self.threads[thread_id]
        
        logger.debug(f"🍄❌ [THREAD] Removed weak thread: {thread_id}")


# Global network instance
_global_mycelial_network: Optional[MycelialMitochondrialNetwork] = None

def get_mycelial_network() -> MycelialMitochondrialNetwork:
    """Get the global mycelial mitochondrial network instance"""
    global _global_mycelial_network
    if _global_mycelial_network is None:
        _global_mycelial_network = MycelialMitochondrialNetwork()
    return _global_mycelial_network

def register_consciousness_node(node_id: str, node_type: str, **kwargs) -> NetworkNode:
    """Convenience function to register a consciousness node"""
    network = get_mycelial_network()
    return network.register_node(node_id, node_type, **kwargs)

def distribute_cognitive_energy(source_node: str, energy_type: EnergyType, amount: float, **kwargs) -> Dict[str, float]:
    """Convenience function to distribute cognitive energy"""
    network = get_mycelial_network()
    return network.distribute_energy(source_node, energy_type, amount, **kwargs)

def propagate_consciousness_information(source_node: str, information: Dict[str, Any], **kwargs) -> List[str]:
    """Convenience function to propagate consciousness information"""
    network = get_mycelial_network()
    return network.propagate_information(source_node, information, **kwargs)

# Export key classes and functions
__all__ = [
    'MycelialMitochondrialNetwork',
    'NetworkNode',
    'MycelialThread',
    'EnergyFlow',
    'NetworkHealthState',
    'ThreadType',
    'EnergyType',
    'get_mycelial_network',
    'register_consciousness_node',
    'distribute_cognitive_energy',
    'propagate_consciousness_information'
] 