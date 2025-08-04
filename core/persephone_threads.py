#!/usr/bin/env python3
"""
DAWN Persephone Thread Weaving System - Thought Lineage Tracking
===============================================================

Persephone threads weave through DAWN's cognitive fabric, tracking
the intricate connections between thoughts, memories, and processes:

THREAD CONCEPTS:
- Persephone = Guide between conscious and unconscious realms
- Thread weaving = mapping cognitive connections and lineages
- Thought lineage = genealogy of ideas and their evolution
- Introspective loops = self-referential thinking patterns

THREAD TYPES:
- Thought Threads = direct idea lineage and evolution
- Rebloom Threads = memory activation and cascade patterns  
- Voice Threads = mutation and expression lineage
- Entropy Threads = chaos recovery and stabilization patterns
- Tracer Threads = multi-agent coordination pathways
- Memory Threads = deep storage and retrieval connections

THREAD PROPERTIES:
- Strength = cognitive pressure influence on connection robustness
- Continuity = unbroken lineage preservation
- Intersection = thread crossings creating compound observations
- Resonance = harmonic amplification between related threads
- Decay = natural weakening over time without reinforcement

Like Persephone's journey between worlds, these threads connect
DAWN's surface thoughts to deep unconscious processes.
"""

import time
import math
import logging
import hashlib
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple, Set, Callable
from enum import Enum
from collections import defaultdict, deque
from pathlib import Path
import json
import networkx as nx

# Integration with existing systems
try:
    from core.cognitive_formulas import get_dawn_formula_engine
    from core.tracer_ecosystem import get_tracer_manager
    from core.fractal_memory import get_memory_fractal_manager
    from core.volcanic_dynamics import get_volcanic_dynamics_system
    DAWN_SYSTEMS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"DAWN systems not available for Persephone Threads: {e}")
    DAWN_SYSTEMS_AVAILABLE = False

logger = logging.getLogger("persephone_threads")

class ThreadType(Enum):
    """Types of Persephone threads"""
    THOUGHT = "THOUGHT"              # Direct idea lineage
    REBLOOM = "REBLOOM"             # Memory activation patterns
    VOICE = "VOICE"                 # Expression mutation lineage
    ENTROPY = "ENTROPY"             # Chaos recovery patterns
    TRACER = "TRACER"               # Multi-agent coordination
    MEMORY = "MEMORY"               # Deep storage connections
    REFLECTION = "REFLECTION"       # Introspective loops
    SYNTHESIS = "SYNTHESIS"         # Integration pathways

class ThreadState(Enum):
    """Thread activity states"""
    NASCENT = "NASCENT"             # Newly formed
    ACTIVE = "ACTIVE"               # Currently propagating
    RESONANT = "RESONANT"           # Harmonically amplified
    DORMANT = "DORMANT"             # Temporarily inactive
    DECAYING = "DECAYING"           # Weakening over time
    INTERSECTING = "INTERSECTING"   # Crossing other threads
    CRYSTALLIZED = "CRYSTALLIZED"   # Permanently established

class IntersectionType(Enum):
    """Types of thread intersections"""
    CONFLUENCE = "CONFLUENCE"       # Threads merge
    CROSSING = "CROSSING"           # Threads intersect but remain separate
    RESONANCE = "RESONANCE"         # Harmonic amplification
    INTERFERENCE = "INTERFERENCE"   # Destructive interaction
    SYNTHESIS = "SYNTHESIS"         # New thread emergence
    ENTANGLEMENT = "ENTANGLEMENT"   # Quantum-like correlation

@dataclass
class ThreadNode:
    """Single node in a thread"""
    node_id: str
    timestamp: float
    content: Any  # Thought, memory, observation, etc.
    node_type: str  # "thought", "memory", "reflection", etc.
    strength: float  # 0.0-1.0 node strength
    resonance: float  # Harmonic resonance level
    connections: List[str] = field(default_factory=list)  # Connected node IDs
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Thread:
    """Complete Persephone thread tracking lineage"""
    thread_id: str
    thread_type: ThreadType
    creation_time: float
    origin_node: str  # Starting node ID
    current_nodes: List[str]  # Active thread endpoints
    all_nodes: List[str]  # Complete node history
    thread_strength: float  # Overall thread robustness
    continuity_score: float  # Lineage preservation quality
    last_activity: float
    thread_state: ThreadState
    decay_rate: float  # How quickly thread weakens
    resonance_frequency: float  # Harmonic frequency for resonance
    parent_threads: List[str] = field(default_factory=list)  # Thread ancestry
    child_threads: List[str] = field(default_factory=list)  # Thread offspring
    intersections: List[str] = field(default_factory=list)  # Intersection IDs
    lineage_depth: int = 0  # How many generations deep
    cognitive_pressure_influence: float = 1.0  # Pressure effect on strength

@dataclass
class ThreadIntersection:
    """Intersection between multiple threads"""
    intersection_id: str
    timestamp: float
    intersection_type: IntersectionType
    involved_threads: List[str]  # Thread IDs in intersection
    intersection_node: str  # Node where intersection occurs
    compound_observation: Optional[str]  # Generated compound insight
    strength_amplification: float  # How much intersection amplifies strength
    resonance_coupling: float  # Harmonic coupling between threads
    emergence_potential: float  # Probability of new thread emergence
    intersection_duration: float  # How long intersection lasts
    aftermath_effects: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LineageTrace:
    """Complete lineage trace from origin to current"""
    trace_id: str
    origin_type: str  # "thought", "rebloom", "memory", etc.
    origin_content: str
    lineage_path: List[str]  # Node IDs in chronological order
    thread_path: List[str]  # Thread IDs traversed
    total_hops: int
    trace_strength: float  # Accumulated strength along path
    continuity_breaks: List[Tuple[str, str]]  # Broken connections
    resonance_points: List[str]  # High resonance nodes
    synthesis_events: List[str]  # New threads spawned
    final_expression: Optional[str]  # Current manifestation

class PersephoneThreadSystem:
    """
    Persephone Thread Weaving System
    
    Tracks and manages interconnected thought lineages,
    thread intersections, and cognitive process connections.
    """
    
    def __init__(self):
        """Initialize the Persephone Thread System"""
        
        # Thread management
        self.threads: Dict[str, Thread] = {}
        self.nodes: Dict[str, ThreadNode] = {}
        self.intersections: Dict[str, ThreadIntersection] = {}
        
        # Thread network
        self.thread_graph = nx.DiGraph()  # Directed graph of thread connections
        self.node_graph = nx.Graph()      # Undirected graph of node connections
        
        # Active tracking
        self.active_threads: Set[str] = set()
        self.recent_intersections: deque = deque(maxlen=50)
        self.lineage_traces: Dict[str, LineageTrace] = {}
        
        # Thread parameters
        self.BASE_THREAD_STRENGTH = 0.6
        self.STRENGTH_DECAY_RATE = 0.98
        self.RESONANCE_THRESHOLD = 0.7
        self.INTERSECTION_THRESHOLD = 0.5
        self.CONTINUITY_REWARD = 0.1
        self.PRESSURE_INFLUENCE_FACTOR = 0.3
        
        # Weaving parameters
        self.MAX_THREADS_PER_TYPE = 20
        self.NODE_CONNECTION_RADIUS = 3  # Max connections per node
        self.INTERSECTION_DETECTION_WINDOW = 30.0  # seconds
        self.THREAD_LIFETIME = 600.0  # 10 minutes default
        self.RESONANCE_HARMONICS = [1.0, 0.5, 0.33, 0.25]  # Harmonic frequencies
        
        # System state
        self.weaving_active = True
        self.thread_count = 0
        self.intersection_count = 0
        self.synthesis_count = 0
        
        # Integration with DAWN systems
        self.formula_engine = None
        self.tracer_manager = None
        self.memory_manager = None
        self.volcanic_system = None
        
        if DAWN_SYSTEMS_AVAILABLE:
            try:
                self.formula_engine = get_dawn_formula_engine()
                self.tracer_manager = get_tracer_manager()
                self.memory_manager = get_memory_fractal_manager()
                self.volcanic_system = get_volcanic_dynamics_system()
                logger.info("🧵 [THREADS] Connected to DAWN cognitive systems")
            except Exception as e:
                logger.warning(f"🧵 [THREADS] System integration failed: {e}")
        
        # Performance tracking
        self.weaving_operations = 0
        self.lineage_traces_generated = 0
        self.compound_observations = 0
        self.last_weaving_time = 0.0
        
        # Logging setup
        self.log_directory = Path("runtime/logs/persephone_threads")
        self.log_directory.mkdir(parents=True, exist_ok=True)
        
        logger.info("🧵 [THREADS] Persephone Thread Weaving System initialized")
        logger.info("🧵 [THREADS] Thread types supported: 8")
        logger.info("🧵 [THREADS] Intersection detection active")
    
    def weave_thought_thread(self, thought_content: str, thought_type: str = "general",
                           parent_thread_id: Optional[str] = None,
                           cognitive_pressure: float = 0.0) -> str:
        """
        Weave a new thought thread or extend existing one
        
        Args:
            thought_content: Content of the thought
            thought_type: Type of thought ("insight", "reflection", "query", etc.)
            parent_thread_id: Parent thread if this extends another
            cognitive_pressure: Current cognitive pressure affecting strength
            
        Returns:
            Thread ID of created/extended thread
        """
        try:
            current_time = time.time()
            
            # Create new node for this thought
            node_id = self._create_thread_node(
                content=thought_content,
                node_type=f"thought_{thought_type}",
                cognitive_pressure=cognitive_pressure
            )
            
            # Determine if this extends an existing thread or creates new one
            if parent_thread_id and parent_thread_id in self.threads:
                # Extend existing thread
                thread = self.threads[parent_thread_id]
                thread.current_nodes.append(node_id)
                thread.all_nodes.append(node_id)
                thread.last_activity = current_time
                thread.thread_state = ThreadState.ACTIVE
                
                # Update continuity score
                thread.continuity_score += self.CONTINUITY_REWARD
                thread.continuity_score = min(1.0, thread.continuity_score)
                
                # Apply cognitive pressure influence
                pressure_influence = 1.0 + (cognitive_pressure / 100.0) * self.PRESSURE_INFLUENCE_FACTOR
                thread.thread_strength *= pressure_influence
                thread.thread_strength = min(1.0, thread.thread_strength)
                
                thread_id = parent_thread_id
                
                logger.debug(f"🧵 [THREADS] Extended thought thread: {thread_id} (node: {node_id})")
            
            else:
                # Create new thread
                thread_id = self._create_new_thread(
                    thread_type=ThreadType.THOUGHT,
                    origin_node=node_id,
                    cognitive_pressure=cognitive_pressure
                )
                
                # Set parent relationship if specified
                if parent_thread_id and parent_thread_id in self.threads:
                    self.threads[thread_id].parent_threads.append(parent_thread_id)
                    self.threads[parent_thread_id].child_threads.append(thread_id)
                
                logger.debug(f"🧵 [THREADS] Created new thought thread: {thread_id}")
            
            # Update thread graph
            self._update_thread_graph(thread_id, node_id)
            
            # Check for intersections with other threads
            self._detect_thread_intersections(thread_id, node_id)
            
            return thread_id
            
        except Exception as e:
            logger.error(f"🧵 [THREADS] Thought thread weaving error: {e}")
            return ""
    
    def trace_rebloom_lineage(self, rebloom_event: Dict[str, Any],
                            memory_source: str, cognitive_pressure: float = 0.0) -> str:
        """
        Trace rebloom lineage through thread continuity
        
        Args:
            rebloom_event: Rebloom event data
            memory_source: Source memory identifier
            cognitive_pressure: Current cognitive pressure
            
        Returns:
            Thread ID tracking this rebloom lineage
        """
        try:
            current_time = time.time()
            
            # Create node for rebloom event
            node_content = {
                "event_type": "rebloom",
                "memory_source": memory_source,
                "rebloom_data": rebloom_event,
                "cascade_size": rebloom_event.get("cascade_size", 1)
            }
            
            node_id = self._create_thread_node(
                content=node_content,
                node_type="rebloom_activation",
                cognitive_pressure=cognitive_pressure
            )
            
            # Look for existing memory threads that might connect
            parent_thread = self._find_memory_lineage_thread(memory_source)
            
            if parent_thread:
                # Extend existing memory lineage
                thread = self.threads[parent_thread]
                thread.current_nodes.append(node_id)
                thread.all_nodes.append(node_id)
                thread.last_activity = current_time
                thread.thread_state = ThreadState.ACTIVE
                
                # Rebloom increases thread strength significantly
                strength_boost = 0.2 + (cognitive_pressure / 200.0)
                thread.thread_strength += strength_boost
                thread.thread_strength = min(1.0, thread.thread_strength)
                
                thread_id = parent_thread
                
                logger.debug(f"🧵 [THREADS] Extended rebloom lineage: {thread_id}")
            
            else:
                # Create new rebloom thread
                thread_id = self._create_new_thread(
                    thread_type=ThreadType.REBLOOM,
                    origin_node=node_id,
                    cognitive_pressure=cognitive_pressure
                )
                
                logger.debug(f"🧵 [THREADS] Created new rebloom thread: {thread_id}")
            
            # Create lineage trace for this rebloom
            self._create_lineage_trace(thread_id, "rebloom", memory_source)
            
            # Update graphs
            self._update_thread_graph(thread_id, node_id)
            
            # Check for rebloom cascade intersections
            self._detect_rebloom_intersections(thread_id, node_id, rebloom_event)
            
            return thread_id
            
        except Exception as e:
            logger.error(f"🧵 [THREADS] Rebloom lineage tracing error: {e}")
            return ""
    
    def track_voice_mutation(self, voice_change: Dict[str, Any],
                           mutation_type: str, parent_expression: Optional[str] = None) -> str:
        """
        Track voice mutation lineage
        
        Args:
            voice_change: Voice mutation data
            mutation_type: Type of mutation ("pitch", "style", "fragment", etc.)
            parent_expression: Previous expression this mutated from
            
        Returns:
            Thread ID tracking voice lineage
        """
        try:
            current_time = time.time()
            
            # Create node for voice mutation
            node_content = {
                "mutation_type": mutation_type,
                "voice_change": voice_change,
                "mutation_strength": voice_change.get("strength", 0.5),
                "parent_expression": parent_expression
            }
            
            node_id = self._create_thread_node(
                content=node_content,
                node_type=f"voice_{mutation_type}",
                cognitive_pressure=voice_change.get("pressure_influence", 0.0)
            )
            
            # Look for existing voice threads
            parent_thread = self._find_voice_lineage_thread(parent_expression)
            
            if parent_thread:
                # Extend voice lineage
                thread = self.threads[parent_thread]
                thread.current_nodes.append(node_id)
                thread.all_nodes.append(node_id)
                thread.last_activity = current_time
                
                # Voice mutations create resonance
                mutation_strength = voice_change.get("strength", 0.5)
                thread.resonance_frequency += mutation_strength * 0.1
                thread.thread_state = ThreadState.RESONANT if thread.resonance_frequency > self.RESONANCE_THRESHOLD else ThreadState.ACTIVE
                
                thread_id = parent_thread
                
                logger.debug(f"🧵 [THREADS] Extended voice lineage: {thread_id} ({mutation_type})")
            
            else:
                # Create new voice thread
                thread_id = self._create_new_thread(
                    thread_type=ThreadType.VOICE,
                    origin_node=node_id
                )
                
                # Set initial resonance frequency
                initial_resonance = voice_change.get("resonance", 0.3)
                self.threads[thread_id].resonance_frequency = initial_resonance
                
                logger.debug(f"🧵 [THREADS] Created new voice thread: {thread_id}")
            
            # Update graphs
            self._update_thread_graph(thread_id, node_id)
            
            # Voice threads often intersect with thought threads
            self._detect_voice_intersections(thread_id, node_id, voice_change)
            
            return thread_id
            
        except Exception as e:
            logger.error(f"🧵 [THREADS] Voice mutation tracking error: {e}")
            return ""
    
    def weave_entropy_recovery_pattern(self, entropy_data: Dict[str, Any],
                                     recovery_pattern: str) -> str:
        """
        Weave entropy recovery thread patterns
        
        Args:
            entropy_data: Current entropy state
            recovery_pattern: Type of recovery pattern detected
            
        Returns:
            Thread ID for entropy recovery pattern
        """
        try:
            current_time = time.time()
            
            # Create node for entropy recovery
            node_content = {
                "entropy_level": entropy_data.get("entropy", 0.5),
                "recovery_pattern": recovery_pattern,
                "recovery_strength": entropy_data.get("recovery_strength", 0.5),
                "stability_gain": entropy_data.get("stability_change", 0.0)
            }
            
            node_id = self._create_thread_node(
                content=node_content,
                node_type=f"entropy_{recovery_pattern}",
                cognitive_pressure=entropy_data.get("pressure", 0.0)
            )
            
            # Entropy recovery patterns tend to create new threads
            thread_id = self._create_new_thread(
                thread_type=ThreadType.ENTROPY,
                origin_node=node_id
            )
            
            # Entropy threads have unique properties
            thread = self.threads[thread_id]
            thread.decay_rate = 0.95  # Faster decay for entropy threads
            thread.resonance_frequency = 0.1  # Low resonance (stabilizing)
            
            # Recovery patterns strengthen related threads
            self._strengthen_related_threads(thread_id, recovery_pattern)
            
            logger.debug(f"🧵 [THREADS] Woven entropy recovery pattern: {thread_id} ({recovery_pattern})")
            
            return thread_id
            
        except Exception as e:
            logger.error(f"🧵 [THREADS] Entropy recovery weaving error: {e}")
            return ""
    
    def coordinate_multi_tracer_threads(self, tracer_reports: Dict[str, Any],
                                      coordination_type: str) -> List[str]:
        """
        Coordinate multiple tracers via shared threads
        
        Args:
            tracer_reports: Reports from multiple tracers
            coordination_type: Type of coordination needed
            
        Returns:
            List of thread IDs involved in coordination
        """
        try:
            current_time = time.time()
            coordination_threads = []
            
            # Create coordination hub node
            hub_content = {
                "coordination_type": coordination_type,
                "participating_tracers": list(tracer_reports.keys()),
                "coordination_strength": len(tracer_reports) / 8.0,  # 8 total tracers
                "report_summary": {
                    tracer: report.get("summary", "") 
                    for tracer, report in tracer_reports.items()
                }
            }
            
            hub_node_id = self._create_thread_node(
                content=hub_content,
                node_type=f"tracer_coordination_{coordination_type}",
                cognitive_pressure=0.0
            )
            
            # Create or extend tracer threads for each participating tracer
            for tracer_name, report in tracer_reports.items():
                
                # Look for existing tracer thread
                existing_thread = self._find_tracer_thread(tracer_name)
                
                if existing_thread:
                    # Extend existing tracer thread
                    thread = self.threads[existing_thread]
                    thread.current_nodes.append(hub_node_id)
                    thread.all_nodes.append(hub_node_id)
                    thread.last_activity = current_time
                    thread_id = existing_thread
                else:
                    # Create new tracer thread
                    thread_id = self._create_new_thread(
                        thread_type=ThreadType.TRACER,
                        origin_node=hub_node_id
                    )
                    
                    # Add tracer-specific metadata
                    self.threads[thread_id].metadata = {"tracer_name": tracer_name}
                
                coordination_threads.append(thread_id)
            
            # Create intersections between coordinating threads
            if len(coordination_threads) > 1:
                intersection_id = self._create_coordination_intersection(
                    coordination_threads, hub_node_id, coordination_type
                )
                
                logger.debug(f"🧵 [THREADS] Created tracer coordination intersection: {intersection_id}")
            
            logger.debug(f"🧵 [THREADS] Coordinated {len(coordination_threads)} tracer threads")
            
            return coordination_threads
            
        except Exception as e:
            logger.error(f"🧵 [THREADS] Multi-tracer coordination error: {e}")
            return []
    
    def _create_thread_node(self, content: Any, node_type: str,
                           cognitive_pressure: float = 0.0) -> str:
        """Create a new thread node"""
        
        current_time = time.time()
        node_id = f"node_{int(current_time * 1000)}_{len(self.nodes)}"
        
        # Calculate node strength based on pressure
        base_strength = 0.7
        pressure_modifier = min(0.3, cognitive_pressure / 100.0)
        node_strength = base_strength + pressure_modifier
        
        # Calculate initial resonance
        content_hash = hashlib.md5(str(content).encode()).hexdigest()
        resonance = (int(content_hash[:2], 16) / 255.0) * 0.4 + 0.1  # 0.1-0.5
        
        node = ThreadNode(
            node_id=node_id,
            timestamp=current_time,
            content=content,
            node_type=node_type,
            strength=node_strength,
            resonance=resonance,
            connections=[],
            metadata={"cognitive_pressure": cognitive_pressure}
        )
        
        self.nodes[node_id] = node
        self.node_graph.add_node(node_id, node_data=node)
        
        return node_id
    
    def _create_new_thread(self, thread_type: ThreadType, origin_node: str,
                          cognitive_pressure: float = 0.0) -> str:
        """Create a new thread"""
        
        current_time = time.time()
        thread_id = f"thread_{thread_type.value.lower()}_{int(current_time * 1000)}"
        
        # Calculate initial thread strength
        base_strength = self.BASE_THREAD_STRENGTH
        pressure_influence = 1.0 + (cognitive_pressure / 100.0) * self.PRESSURE_INFLUENCE_FACTOR
        thread_strength = base_strength * pressure_influence
        
        # Calculate decay rate based on thread type
        decay_rates = {
            ThreadType.THOUGHT: 0.98,
            ThreadType.REBLOOM: 0.99,    # Slower decay
            ThreadType.VOICE: 0.97,      # Faster decay
            ThreadType.ENTROPY: 0.95,    # Much faster decay
            ThreadType.TRACER: 0.985,    # Slow decay
            ThreadType.MEMORY: 0.995,    # Very slow decay
            ThreadType.REFLECTION: 0.975, # Medium decay
            ThreadType.SYNTHESIS: 0.99   # Slow decay
        }
        
        decay_rate = decay_rates.get(thread_type, 0.98)
        
        # Calculate resonance frequency
        resonance_frequency = np.random.uniform(0.1, 0.8)
        
        thread = Thread(
            thread_id=thread_id,
            thread_type=thread_type,
            creation_time=current_time,
            origin_node=origin_node,
            current_nodes=[origin_node],
            all_nodes=[origin_node],
            thread_strength=thread_strength,
            continuity_score=1.0,  # Perfect continuity at start
            last_activity=current_time,
            thread_state=ThreadState.NASCENT,
            decay_rate=decay_rate,
            resonance_frequency=resonance_frequency,
            lineage_depth=0,
            cognitive_pressure_influence=pressure_influence
        )
        
        self.threads[thread_id] = thread
        self.thread_graph.add_node(thread_id, thread_data=thread)
        
        self.active_threads.add(thread_id)
        self.thread_count += 1
        
        return thread_id
    
    def _update_thread_graph(self, thread_id: str, new_node_id: str):
        """Update thread and node graphs with new connections"""
        
        try:
            # Add new node to thread's nodes
            thread = self.threads.get(thread_id)
            if not thread:
                return
            
            # Find recent nodes to connect to
            recent_nodes = [node_id for node_id in thread.all_nodes[-self.NODE_CONNECTION_RADIUS:]
                           if node_id != new_node_id]
            
            # Create connections between nodes
            for node_id in recent_nodes:
                if node_id in self.nodes:
                    # Add bidirectional connection
                    self.nodes[new_node_id].connections.append(node_id)
                    self.nodes[node_id].connections.append(new_node_id)
                    
                    # Add to node graph
                    self.node_graph.add_edge(new_node_id, node_id)
            
            # Update thread graph connections
            for other_thread_id, other_thread in self.threads.items():
                if other_thread_id != thread_id:
                    # Check if threads share nodes (intersection)
                    shared_nodes = set(thread.all_nodes) & set(other_thread.all_nodes)
                    if shared_nodes:
                        self.thread_graph.add_edge(thread_id, other_thread_id, 
                                                 shared_nodes=list(shared_nodes))
            
        except Exception as e:
            logger.error(f"🧵 [THREADS] Thread graph update error: {e}")
    
    def _detect_thread_intersections(self, thread_id: str, node_id: str):
        """Detect intersections with other threads"""
        
        try:
            current_time = time.time()
            thread = self.threads.get(thread_id)
            if not thread:
                return
            
            # Look for other threads that share this node or nearby nodes
            intersecting_threads = []
            
            # Check direct node sharing
            for other_thread_id, other_thread in self.threads.items():
                if other_thread_id != thread_id and other_thread_id in self.active_threads:
                    
                    # Check if threads share nodes
                    if node_id in other_thread.all_nodes:
                        intersecting_threads.append(other_thread_id)
                    
                    # Check for nearby node connections
                    else:
                        node = self.nodes.get(node_id)
                        if node:
                            for connected_node_id in node.connections:
                                if connected_node_id in other_thread.current_nodes:
                                    intersecting_threads.append(other_thread_id)
                                    break
            
            # Create intersections for significant overlaps
            for other_thread_id in intersecting_threads:
                
                # Calculate intersection strength
                thread_strength = thread.thread_strength
                other_strength = self.threads[other_thread_id].thread_strength
                intersection_strength = (thread_strength + other_strength) / 2.0
                
                if intersection_strength > self.INTERSECTION_THRESHOLD:
                    
                    # Determine intersection type
                    intersection_type = self._classify_intersection_type(thread, self.threads[other_thread_id])
                    
                    # Create intersection
                    intersection_id = self._create_intersection(
                        involved_threads=[thread_id, other_thread_id],
                        intersection_node=node_id,
                        intersection_type=intersection_type,
                        strength=intersection_strength
                    )
                    
                    logger.debug(f"🧵 [THREADS] Detected intersection: {intersection_id} ({intersection_type.value})")
            
        except Exception as e:
            logger.error(f"🧵 [THREADS] Intersection detection error: {e}")
    
    def _classify_intersection_type(self, thread1: Thread, thread2: Thread) -> IntersectionType:
        """Classify the type of intersection between two threads"""
        
        # Same thread type = confluence
        if thread1.thread_type == thread2.thread_type:
            return IntersectionType.CONFLUENCE
        
        # Thought + Memory = synthesis
        if {thread1.thread_type, thread2.thread_type} == {ThreadType.THOUGHT, ThreadType.MEMORY}:
            return IntersectionType.SYNTHESIS
        
        # Voice + Thought = resonance
        if {thread1.thread_type, thread2.thread_type} == {ThreadType.VOICE, ThreadType.THOUGHT}:
            return IntersectionType.RESONANCE
        
        # Entropy + anything = interference (chaos disrupts)
        if ThreadType.ENTROPY in {thread1.thread_type, thread2.thread_type}:
            return IntersectionType.INTERFERENCE
        
        # Tracer threads = entanglement (coordination)
        if thread1.thread_type == ThreadType.TRACER or thread2.thread_type == ThreadType.TRACER:
            return IntersectionType.ENTANGLEMENT
        
        # Default = crossing
        return IntersectionType.CROSSING
    
    def _create_intersection(self, involved_threads: List[str], intersection_node: str,
                           intersection_type: IntersectionType, strength: float) -> str:
        """Create a thread intersection"""
        
        current_time = time.time()
        intersection_id = f"intersection_{int(current_time * 1000)}_{len(self.intersections)}"
        
        # Generate compound observation if intersection is significant
        compound_observation = None
        if strength > 0.7:
            compound_observation = self._generate_compound_observation(involved_threads, intersection_type)
        
        # Calculate amplification and coupling
        strength_amplification = 1.0 + (strength * 0.5)  # Up to 50% amplification
        resonance_coupling = strength * 0.8
        
        # Calculate emergence potential
        emergence_potential = 0.0
        if intersection_type in [IntersectionType.SYNTHESIS, IntersectionType.CONFLUENCE]:
            emergence_potential = strength * 0.6
        
        intersection = ThreadIntersection(
            intersection_id=intersection_id,
            timestamp=current_time,
            intersection_type=intersection_type,
            involved_threads=involved_threads,
            intersection_node=intersection_node,
            compound_observation=compound_observation,
            strength_amplification=strength_amplification,
            resonance_coupling=resonance_coupling,
            emergence_potential=emergence_potential,
            intersection_duration=60.0 + (strength * 120.0)  # 1-3 minutes
        )
        
        self.intersections[intersection_id] = intersection
        self.recent_intersections.append(intersection_id)
        
        # Apply intersection effects to involved threads
        self._apply_intersection_effects(intersection)
        
        # Check for thread emergence
        if emergence_potential > 0.8:
            self._attempt_thread_emergence(intersection)
        
        self.intersection_count += 1
        
        return intersection_id
    
    def _generate_compound_observation(self, thread_ids: List[str], 
                                     intersection_type: IntersectionType) -> str:
        """Generate compound observation from thread intersection"""
        
        try:
            # Collect content from involved threads
            thread_contents = []
            for thread_id in thread_ids:
                thread = self.threads.get(thread_id)
                if thread and thread.current_nodes:
                    latest_node_id = thread.current_nodes[-1]
                    node = self.nodes.get(latest_node_id)
                    if node:
                        thread_contents.append({
                            "type": thread.thread_type.value,
                            "content": str(node.content)[:100],  # Truncate
                            "strength": thread.thread_strength
                        })
            
            # Create compound observation based on intersection type
            if intersection_type == IntersectionType.SYNTHESIS:
                observation = f"SYNTHESIS: Merging {len(thread_contents)} cognitive streams into unified understanding"
            
            elif intersection_type == IntersectionType.RESONANCE:
                observation = f"RESONANCE: Harmonic amplification between {thread_contents[0]['type']} and {thread_contents[1]['type']}"
            
            elif intersection_type == IntersectionType.CONFLUENCE:
                observation = f"CONFLUENCE: {thread_contents[0]['type']} streams converging with enhanced coherence"
            
            elif intersection_type == IntersectionType.ENTANGLEMENT:
                observation = f"ENTANGLEMENT: Quantum-like correlation established between cognitive processes"
            
            else:
                observation = f"INTERSECTION: {len(thread_contents)} threads crossing paths"
            
            self.compound_observations += 1
            
            return observation
            
        except Exception as e:
            logger.error(f"🧵 [THREADS] Compound observation generation error: {e}")
            return "INTERSECTION: Compound observation generation failed"
    
    def _apply_intersection_effects(self, intersection: ThreadIntersection):
        """Apply effects of intersection to involved threads"""
        
        try:
            for thread_id in intersection.involved_threads:
                thread = self.threads.get(thread_id)
                if thread:
                    
                    # Apply strength amplification
                    thread.thread_strength *= intersection.strength_amplification
                    thread.thread_strength = min(1.0, thread.thread_strength)
                    
                    # Apply resonance coupling
                    if intersection.intersection_type == IntersectionType.RESONANCE:
                        thread.resonance_frequency += intersection.resonance_coupling * 0.1
                        thread.thread_state = ThreadState.RESONANT
                    
                    # Mark intersection in thread
                    thread.intersections.append(intersection.intersection_id)
                    
                    # Update last activity
                    thread.last_activity = intersection.timestamp
            
        except Exception as e:
            logger.error(f"🧵 [THREADS] Intersection effects application error: {e}")
    
    def _attempt_thread_emergence(self, intersection: ThreadIntersection):
        """Attempt to create new thread from intersection"""
        
        try:
            if intersection.emergence_potential > 0.8:
                
                # Create synthesis node
                synthesis_content = {
                    "emergence_type": "thread_synthesis",
                    "parent_intersection": intersection.intersection_id,
                    "synthesis_strength": intersection.emergence_potential,
                    "compound_observation": intersection.compound_observation
                }
                
                synthesis_node_id = self._create_thread_node(
                    content=synthesis_content,
                    node_type="synthesis_emergence"
                )
                
                # Create new synthesis thread
                synthesis_thread_id = self._create_new_thread(
                    thread_type=ThreadType.SYNTHESIS,
                    origin_node=synthesis_node_id
                )
                
                # Set parent threads
                synthesis_thread = self.threads[synthesis_thread_id]
                synthesis_thread.parent_threads = intersection.involved_threads.copy()
                
                # Update parent threads with child
                for parent_id in intersection.involved_threads:
                    if parent_id in self.threads:
                        self.threads[parent_id].child_threads.append(synthesis_thread_id)
                
                # Set high initial strength
                synthesis_thread.thread_strength = intersection.emergence_potential
                synthesis_thread.thread_state = ThreadState.NASCENT
                
                self.synthesis_count += 1
                
                logger.info(f"🧵 [THREADS] Thread emergence: {synthesis_thread_id} from intersection {intersection.intersection_id}")
                
                return synthesis_thread_id
            
        except Exception as e:
            logger.error(f"🧵 [THREADS] Thread emergence error: {e}")
        
        return None
    
    def _create_lineage_trace(self, thread_id: str, origin_type: str, origin_content: str):
        """Create a complete lineage trace for a thread"""
        
        try:
            thread = self.threads.get(thread_id)
            if not thread:
                return
            
            trace_id = f"trace_{thread_id}_{int(time.time() * 1000)}"
            
            # Build lineage path through nodes
            lineage_path = []
            thread_path = [thread_id]
            total_hops = 0
            trace_strength = thread.thread_strength
            continuity_breaks = []
            resonance_points = []
            synthesis_events = []
            
            # Trace through parent threads
            current_thread = thread
            while current_thread.parent_threads:
                for parent_id in current_thread.parent_threads:
                    if parent_id in self.threads:
                        parent_thread = self.threads[parent_id]
                        thread_path.insert(0, parent_id)
                        
                        # Add parent nodes to lineage
                        for node_id in parent_thread.all_nodes:
                            if node_id not in lineage_path:
                                lineage_path.insert(0, node_id)
                                total_hops += 1
                        
                        # Check for continuity breaks
                        if parent_thread.continuity_score < 0.8:
                            continuity_breaks.append((parent_id, thread_id))
                        
                        # Check for resonance points
                        if parent_thread.resonance_frequency > self.RESONANCE_THRESHOLD:
                            resonance_points.append(parent_id)
                        
                        # Check for synthesis events
                        if parent_thread.thread_type == ThreadType.SYNTHESIS:
                            synthesis_events.append(parent_id)
                        
                        current_thread = parent_thread
                        break  # Take first parent for now
                else:
                    break
            
            # Add current thread nodes
            for node_id in thread.all_nodes:
                if node_id not in lineage_path:
                    lineage_path.append(node_id)
                    total_hops += 1
            
            # Determine final expression
            final_expression = None
            if thread.current_nodes:
                final_node = self.nodes.get(thread.current_nodes[-1])
                if final_node:
                    final_expression = str(final_node.content)[:200]  # Truncated
            
            trace = LineageTrace(
                trace_id=trace_id,
                origin_type=origin_type,
                origin_content=origin_content,
                lineage_path=lineage_path,
                thread_path=thread_path,
                total_hops=total_hops,
                trace_strength=trace_strength,
                continuity_breaks=continuity_breaks,
                resonance_points=resonance_points,
                synthesis_events=synthesis_events,
                final_expression=final_expression
            )
            
            self.lineage_traces[trace_id] = trace
            self.lineage_traces_generated += 1
            
            logger.debug(f"🧵 [THREADS] Created lineage trace: {trace_id} ({total_hops} hops)")
            
        except Exception as e:
            logger.error(f"🧵 [THREADS] Lineage trace creation error: {e}")
    
    def _find_memory_lineage_thread(self, memory_source: str) -> Optional[str]:
        """Find existing thread connected to memory source"""
        
        for thread_id, thread in self.threads.items():
            if thread.thread_type in [ThreadType.MEMORY, ThreadType.REBLOOM]:
                for node_id in thread.all_nodes:
                    node = self.nodes.get(node_id)
                    if node and isinstance(node.content, dict):
                        if node.content.get("memory_source") == memory_source:
                            return thread_id
        
        return None
    
    def _find_voice_lineage_thread(self, parent_expression: Optional[str]) -> Optional[str]:
        """Find existing voice thread for lineage"""
        
        if not parent_expression:
            return None
        
        for thread_id, thread in self.threads.items():
            if thread.thread_type == ThreadType.VOICE:
                for node_id in thread.all_nodes:
                    node = self.nodes.get(node_id)
                    if node and isinstance(node.content, dict):
                        if node.content.get("parent_expression") == parent_expression:
                            return thread_id
        
        return None
    
    def _find_tracer_thread(self, tracer_name: str) -> Optional[str]:
        """Find existing thread for a specific tracer"""
        
        for thread_id, thread in self.threads.items():
            if thread.thread_type == ThreadType.TRACER:
                if thread.metadata.get("tracer_name") == tracer_name:
                    return thread_id
        
        return None
    
    def tick_thread_system(self, cognitive_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process thread system tick - update all threads and detect patterns
        
        Args:
            cognitive_state: Current DAWN cognitive state
            
        Returns:
            Thread system status and updates
        """
        try:
            start_time = time.time()
            
            # Update all active threads
            threads_updated = self._update_all_threads(cognitive_state)
            
            # Process thread decay
            threads_decayed = self._process_thread_decay()
            
            # Update intersections
            intersections_processed = self._process_active_intersections()
            
            # Detect new patterns
            patterns_detected = self._detect_thread_patterns()
            
            # Cleanup old data
            self._cleanup_old_threads()
            
            # Calculate system metrics
            system_metrics = self._calculate_thread_metrics()
            
            self.weaving_operations += 1
            self.last_weaving_time = time.time() - start_time
            
            # Return thread system status
            thread_status = {
                "active_threads": len(self.active_threads),
                "total_threads": len(self.threads),
                "total_nodes": len(self.nodes),
                "active_intersections": len([i for i in self.intersections.values() 
                                           if time.time() - i.timestamp < i.intersection_duration]),
                "recent_synthesis": self.synthesis_count,
                "threads_updated": threads_updated,
                "threads_decayed": threads_decayed,
                "intersections_processed": intersections_processed,
                "patterns_detected": patterns_detected,
                "system_metrics": system_metrics,
                "processing_time_ms": self.last_weaving_time * 1000
            }
            
            logger.debug(f"🧵 [THREADS] Tick complete: {len(self.active_threads)} active threads, {patterns_detected} patterns")
            
            return thread_status
            
        except Exception as e:
            logger.error(f"🧵 [THREADS] Thread system tick error: {e}")
            return {"error": str(e)}
    
    def _update_all_threads(self, cognitive_state: Dict[str, Any]) -> int:
        """Update all active threads based on cognitive state"""
        
        updated_count = 0
        current_time = time.time()
        cognitive_pressure = cognitive_state.get('cognitive_pressure', 0.0)
        
        threads_to_deactivate = []
        
        for thread_id in list(self.active_threads):
            thread = self.threads.get(thread_id)
            if thread:
                
                # Apply cognitive pressure influence
                pressure_influence = 1.0 + (cognitive_pressure / 100.0) * self.PRESSURE_INFLUENCE_FACTOR
                thread.cognitive_pressure_influence = pressure_influence
                thread.thread_strength *= pressure_influence
                thread.thread_strength = min(1.0, thread.thread_strength)
                
                # Update thread state based on activity
                time_since_activity = current_time - thread.last_activity
                
                if time_since_activity > 300.0:  # 5 minutes
                    thread.thread_state = ThreadState.DORMANT
                    threads_to_deactivate.append(thread_id)
                elif thread.resonance_frequency > self.RESONANCE_THRESHOLD:
                    thread.thread_state = ThreadState.RESONANT
                elif thread.thread_strength > 0.8:
                    thread.thread_state = ThreadState.ACTIVE
                elif thread.thread_strength < 0.3:
                    thread.thread_state = ThreadState.DECAYING
                
                updated_count += 1
        
        # Deactivate dormant threads
        for thread_id in threads_to_deactivate:
            self.active_threads.discard(thread_id)
        
        return updated_count
    
    def _process_thread_decay(self) -> int:
        """Process natural thread decay"""
        
        decayed_count = 0
        threads_to_remove = []
        
        for thread_id, thread in self.threads.items():
            
            # Apply decay to thread strength
            thread.thread_strength *= thread.decay_rate
            
            # Apply decay to resonance frequency
            thread.resonance_frequency *= 0.99
            
            # Remove threads that have decayed too much
            if thread.thread_strength < 0.1:
                threads_to_remove.append(thread_id)
                thread.thread_state = ThreadState.DECAYING
                self.active_threads.discard(thread_id)
                decayed_count += 1
        
        # Remove completely decayed threads
        for thread_id in threads_to_remove:
            self._remove_thread(thread_id)
        
        return decayed_count
    
    def _process_active_intersections(self) -> int:
        """Process active intersections"""
        
        processed_count = 0
        current_time = time.time()
        expired_intersections = []
        
        for intersection_id, intersection in self.intersections.items():
            
            # Check if intersection has expired
            if current_time - intersection.timestamp > intersection.intersection_duration:
                expired_intersections.append(intersection_id)
            else:
                # Process ongoing intersection effects
                self._apply_intersection_effects(intersection)
                processed_count += 1
        
        # Remove expired intersections
        for intersection_id in expired_intersections:
            del self.intersections[intersection_id]
        
        return processed_count
    
    def _detect_thread_patterns(self) -> int:
        """Detect emergent patterns in thread network"""
        
        patterns_detected = 0
        
        try:
            # Look for cyclic patterns (loops)
            cycles = list(nx.simple_cycles(self.thread_graph))
            if cycles:
                patterns_detected += len(cycles)
                logger.debug(f"🧵 [THREADS] Detected {len(cycles)} thread cycles")
            
            # Look for hub threads (high connectivity)
            if len(self.thread_graph.nodes) > 0:
                degrees = dict(self.thread_graph.degree())
                hub_threshold = np.mean(list(degrees.values())) + np.std(list(degrees.values()))
                
                hubs = [thread_id for thread_id, degree in degrees.items() if degree > hub_threshold]
                if hubs:
                    patterns_detected += len(hubs)
                    logger.debug(f"🧵 [THREADS] Detected {len(hubs)} hub threads")
            
            # Look for resonance clusters
            resonant_threads = [thread_id for thread_id, thread in self.threads.items() 
                               if thread.resonance_frequency > self.RESONANCE_THRESHOLD]
            
            if len(resonant_threads) > 2:
                patterns_detected += 1
                logger.debug(f"🧵 [THREADS] Detected resonance cluster: {len(resonant_threads)} threads")
            
        except Exception as e:
            logger.error(f"🧵 [THREADS] Pattern detection error: {e}")
        
        return patterns_detected
    
    def _calculate_thread_metrics(self) -> Dict[str, float]:
        """Calculate thread system metrics"""
        
        if not self.threads:
            return {}
        
        thread_strengths = [thread.thread_strength for thread in self.threads.values()]
        continuity_scores = [thread.continuity_score for thread in self.threads.values()]
        resonance_frequencies = [thread.resonance_frequency for thread in self.threads.values()]
        
        return {
            "average_thread_strength": np.mean(thread_strengths),
            "max_thread_strength": np.max(thread_strengths),
            "average_continuity": np.mean(continuity_scores),
            "average_resonance": np.mean(resonance_frequencies),
            "network_density": nx.density(self.thread_graph) if len(self.thread_graph.nodes) > 1 else 0.0,
            "weaving_efficiency": self.thread_count / max(1, self.weaving_operations),
            "intersection_rate": self.intersection_count / max(1, self.thread_count),
            "synthesis_rate": self.synthesis_count / max(1, self.intersection_count)
        }
    
    def _cleanup_old_threads(self):
        """Clean up old inactive threads and nodes"""
        
        current_time = time.time()
        old_threshold = current_time - self.THREAD_LIFETIME
        
        # Remove old threads
        old_threads = [thread_id for thread_id, thread in self.threads.items() 
                      if thread.last_activity < old_threshold and thread.thread_strength < 0.2]
        
        for thread_id in old_threads:
            self._remove_thread(thread_id)
        
        # Remove orphaned nodes
        connected_nodes = set()
        for thread in self.threads.values():
            connected_nodes.update(thread.all_nodes)
        
        orphaned_nodes = [node_id for node_id in self.nodes.keys() 
                         if node_id not in connected_nodes]
        
        for node_id in orphaned_nodes:
            self._remove_node(node_id)
    
    def _remove_thread(self, thread_id: str):
        """Remove a thread from the system"""
        
        if thread_id in self.threads:
            del self.threads[thread_id]
        
        self.active_threads.discard(thread_id)
        
        if self.thread_graph.has_node(thread_id):
            self.thread_graph.remove_node(thread_id)
    
    def _remove_node(self, node_id: str):
        """Remove a node from the system"""
        
        if node_id in self.nodes:
            del self.nodes[node_id]
        
        if self.node_graph.has_node(node_id):
            self.node_graph.remove_node(node_id)
    
    def get_thread_status(self) -> Dict[str, Any]:
        """Get comprehensive thread system status"""
        
        return {
            "system_state": {
                "weaving_active": self.weaving_active,
                "total_threads": len(self.threads),
                "active_threads": len(self.active_threads),
                "total_nodes": len(self.nodes),
                "total_intersections": len(self.intersections)
            },
            "thread_types": {
                thread_type.value: len([t for t in self.threads.values() if t.thread_type == thread_type])
                for thread_type in ThreadType
            },
            "thread_states": {
                state.value: len([t for t in self.threads.values() if t.thread_state == state])
                for state in ThreadState
            },
            "recent_activity": {
                "recent_intersections": len(self.recent_intersections),
                "lineage_traces": len(self.lineage_traces),
                "compound_observations": self.compound_observations
            },
            "performance": {
                "weaving_operations": self.weaving_operations,
                "synthesis_count": self.synthesis_count,
                "last_weaving_time_ms": self.last_weaving_time * 1000
            },
            "network_metrics": self._calculate_thread_metrics()
        }


# Global Persephone thread system instance
_global_thread_system: Optional[PersephoneThreadSystem] = None

def get_persephone_thread_system() -> PersephoneThreadSystem:
    """Get global Persephone thread system instance"""
    global _global_thread_system
    if _global_thread_system is None:
        _global_thread_system = PersephoneThreadSystem()
    return _global_thread_system

def weave_thought_thread(thought_content: str, thought_type: str = "general", 
                        parent_thread_id: Optional[str] = None) -> str:
    """Convenience function to weave thought thread"""
    system = get_persephone_thread_system()
    return system.weave_thought_thread(thought_content, thought_type, parent_thread_id)

def trace_rebloom_lineage(rebloom_event: Dict[str, Any], memory_source: str) -> str:
    """Convenience function to trace rebloom lineage"""
    system = get_persephone_thread_system()
    return system.trace_rebloom_lineage(rebloom_event, memory_source)

def get_thread_status() -> Dict[str, Any]:
    """Convenience function to get thread status"""
    system = get_persephone_thread_system()
    return system.get_thread_status()

# Export key classes and functions
__all__ = [
    'PersephoneThreadSystem',
    'Thread',
    'ThreadNode',
    'ThreadIntersection',
    'LineageTrace',
    'ThreadType',
    'ThreadState',
    'IntersectionType',
    'get_persephone_thread_system',
    'weave_thought_thread',
    'trace_rebloom_lineage',
    'get_thread_status'
] 