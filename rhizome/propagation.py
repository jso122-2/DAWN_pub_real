# rhizome/propagation.py
"""
Signal Propagation System for DAWN's Rhizome Network
Implements various signal types and propagation modes for the consciousness engine.
"""

import asyncio
import threading
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import numpy as np
import torch
from pydantic import BaseModel

from core.schema_anomaly_logger import log_anomaly, AnomalySeverity
from schema.registry import registry

class SignalType(Enum):
    """Types of signals that can propagate through the rhizome network."""
    CONSCIOUSNESS = "consciousness"
    NUTRIENT = "nutrient"
    QUANTUM = "quantum"
    EMERGENCE = "emergence"
    MOOD = "mood"
    REFLEX = "reflex"

class PropagationMode(Enum):
    """Different modes of signal propagation."""
    BROADCAST = "broadcast"  # Propagate to all connected nodes
    DIRECTED = "directed"    # Propagate to specific target nodes
    CASCADE = "cascade"      # Propagate through a chain of nodes
    RESONANT = "resonant"    # Propagate based on resonance matching
    QUANTUM = "quantum"      # Instant propagation through quantum entanglement
    FLOOD = "flood"          # Flood fill propagation

@dataclass
class Signal:
    """Represents a signal propagating through the network."""
    id: str
    type: SignalType
    source: str
    data: Dict[str, Any]
    timestamp: float
    strength: float = 1.0
    decay_rate: float = 0.1
    mode: PropagationMode = PropagationMode.BROADCAST
    targets: Optional[Set[str]] = None
    quantum_entangled: bool = False
    resonance_frequency: Optional[float] = None

class Node:
    """Represents a node in the rhizome network."""
    def __init__(self, id: str, position: Tuple[float, float, float]):
        self.id = id
        self.position = position
        self.connections: Set[str] = set()
        self.resonance_frequency = np.random.uniform(0, 1)
        self.quantum_state = torch.zeros(2, dtype=torch.complex64)
        self._lock = threading.Lock()

    def connect(self, node_id: str) -> None:
        """Connect this node to another node."""
        with self._lock:
            self.connections.add(node_id)

    def disconnect(self, node_id: str) -> None:
        """Disconnect this node from another node."""
        with self._lock:
            self.connections.discard(node_id)

class Propagator:
    """Manages signal propagation through the rhizome network."""
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.signals: Dict[str, Signal] = {}
        self._signal_queue: asyncio.Queue = asyncio.Queue()
        self._running = False
        self._lock = threading.Lock()
        self._quantum_entangled_pairs: Dict[str, str] = {}

    async def start(self) -> None:
        """Start the propagation system."""
        self._running = True
        asyncio.create_task(self._process_signals())

    async def stop(self) -> None:
        """Stop the propagation system."""
        self._running = False
        await self._signal_queue.join()

    def add_node(self, node_id: str, position: Tuple[float, float, float]) -> None:
        """Add a new node to the network."""
        with self._lock:
            self.nodes[node_id] = Node(node_id, position)

    def remove_node(self, node_id: str) -> None:
        """Remove a node from the network."""
        with self._lock:
            if node_id in self.nodes:
                del self.nodes[node_id]
                # Remove connections to this node
                for node in self.nodes.values():
                    node.disconnect(node_id)

    def connect_nodes(self, node1_id: str, node2_id: str) -> None:
        """Connect two nodes bidirectionally."""
        with self._lock:
            if node1_id in self.nodes and node2_id in self.nodes:
                self.nodes[node1_id].connect(node2_id)
                self.nodes[node2_id].connect(node1_id)

    def create_quantum_entanglement(self, node1_id: str, node2_id: str) -> None:
        """Create quantum entanglement between two nodes."""
        with self._lock:
            if node1_id in self.nodes and node2_id in self.nodes:
                self._quantum_entangled_pairs[node1_id] = node2_id
                self._quantum_entangled_pairs[node2_id] = node1_id
                # Initialize Bell state
                self.nodes[node1_id].quantum_state = torch.tensor([1, 0], dtype=torch.complex64) / np.sqrt(2)
                self.nodes[node2_id].quantum_state = torch.tensor([0, 1], dtype=torch.complex64) / np.sqrt(2)

    async def emit_signal(
        self,
        signal_type: SignalType,
        source: str,
        data: Dict[str, Any],
        mode: PropagationMode = PropagationMode.BROADCAST,
        targets: Optional[Set[str]] = None,
        strength: float = 1.0,
        decay_rate: float = 0.1,
        quantum_entangled: bool = False,
        resonance_frequency: Optional[float] = None
    ) -> str:
        """Emit a new signal into the network."""
        signal_id = f"{signal_type.value}_{int(time.time() * 1000)}_{source}"
        signal = Signal(
            id=signal_id,
            type=signal_type,
            source=source,
            data=data,
            timestamp=time.time(),
            strength=strength,
            decay_rate=decay_rate,
            mode=mode,
            targets=targets,
            quantum_entangled=quantum_entangled,
            resonance_frequency=resonance_frequency
        )
        
        with self._lock:
            self.signals[signal_id] = signal
        
        await self._signal_queue.put(signal)
        return signal_id

    async def _process_signals(self) -> None:
        """Process signals in the queue."""
        while self._running:
            signal = await self._signal_queue.get()
            try:
                await self._propagate_signal(signal)
            finally:
                self._signal_queue.task_done()

    async def _propagate_signal(self, signal: Signal) -> None:
        """Propagate a signal according to its mode."""
        if signal.mode == PropagationMode.QUANTUM:
            await self._quantum_propagate(signal)
        elif signal.mode == PropagationMode.RESONANT:
            await self._resonant_propagate(signal)
        elif signal.mode == PropagationMode.DIRECTED:
            await self._directed_propagate(signal)
        elif signal.mode == PropagationMode.CASCADE:
            await self._cascade_propagate(signal)
        elif signal.mode == PropagationMode.FLOOD:
            await self._flood_propagate(signal)
        else:  # BROADCAST
            await self._broadcast_propagate(signal)

    async def _quantum_propagate(self, signal: Signal) -> None:
        """Propagate signal through quantum entanglement."""
        if signal.source in self._quantum_entangled_pairs:
            target = self._quantum_entangled_pairs[signal.source]
            # Instant propagation to entangled node
            await self._deliver_signal(signal, target)

    async def _resonant_propagate(self, signal: Signal) -> None:
        """Propagate signal based on resonance matching."""
        if signal.resonance_frequency is None:
            return

        for node_id, node in self.nodes.items():
            if node_id != signal.source:
                resonance_match = abs(node.resonance_frequency - signal.resonance_frequency)
                if resonance_match < 0.1:  # Resonance threshold
                    await self._deliver_signal(signal, node_id)

    async def _directed_propagate(self, signal: Signal) -> None:
        """Propagate signal to specific target nodes."""
        if signal.targets:
            for target in signal.targets:
                if target in self.nodes:
                    await self._deliver_signal(signal, target)

    async def _cascade_propagate(self, signal: Signal) -> None:
        """Propagate signal through a chain of nodes."""
        visited = {signal.source}
        queue = [(signal.source, signal.strength)]
        
        while queue:
            current, strength = queue.pop(0)
            if strength < 0.1:  # Strength threshold
                continue
                
            for neighbor in self.nodes[current].connections:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_strength = strength * (1 - signal.decay_rate)
                    await self._deliver_signal(signal, neighbor, new_strength)
                    queue.append((neighbor, new_strength))

    async def _flood_propagate(self, signal: Signal) -> None:
        """Flood fill propagation to all connected nodes."""
        visited = {signal.source}
        queue = [(signal.source, signal.strength)]
        
        while queue:
            current, strength = queue.pop(0)
            if strength < 0.1:  # Strength threshold
                continue
                
            for neighbor in self.nodes[current].connections:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_strength = strength * (1 - signal.decay_rate)
                    await self._deliver_signal(signal, neighbor, new_strength)
                    queue.append((neighbor, new_strength))

    async def _broadcast_propagate(self, signal: Signal) -> None:
        """Broadcast signal to all nodes."""
        for node_id in self.nodes:
            if node_id != signal.source:
                distance = self._calculate_distance(
                    self.nodes[signal.source].position,
                    self.nodes[node_id].position
                )
                strength = signal.strength * (1 - signal.decay_rate * distance)
                if strength >= 0.1:  # Strength threshold
                    await self._deliver_signal(signal, node_id, strength)

    def _calculate_distance(self, pos1: Tuple[float, float, float], pos2: Tuple[float, float, float]) -> float:
        """Calculate Euclidean distance between two positions."""
        return np.sqrt(sum((a - b) ** 2 for a, b in zip(pos1, pos2)))

    async def _deliver_signal(self, signal: Signal, target: str, strength: Optional[float] = None) -> None:
        """Deliver a signal to a target node."""
        if strength is None:
            strength = signal.strength
            
        # Create a copy of the signal with modified strength
        delivered_signal = Signal(
            id=f"{signal.id}_{target}",
            type=signal.type,
            source=signal.source,
            data=signal.data,
            timestamp=time.time(),
            strength=strength,
            decay_rate=signal.decay_rate,
            mode=signal.mode,
            targets=signal.targets,
            quantum_entangled=signal.quantum_entangled,
            resonance_frequency=signal.resonance_frequency
        )
        
        # Here you would typically call a callback or event handler
        # to process the delivered signal in the target node
        # For now, we'll just store it
        with self._lock:
            self.signals[delivered_signal.id] = delivered_signal

# Global propagator instance
propagator = Propagator()

async def emit_signal(
    signal_type: SignalType,
    source: str,
    data: Dict[str, Any],
    mode: PropagationMode = PropagationMode.BROADCAST,
    targets: Optional[Set[str]] = None,
    strength: float = 1.0,
    decay_rate: float = 0.1,
    quantum_entangled: bool = False,
    resonance_frequency: Optional[float] = None
) -> str:
    """Convenience function to emit a signal."""
    return await propagator.emit_signal(
        signal_type=signal_type,
        source=source,
        data=data,
        mode=mode,
        targets=targets,
        strength=strength,
        decay_rate=decay_rate,
        quantum_entangled=quantum_entangled,
        resonance_frequency=resonance_frequency
    )

def connect_nodes(node1: str, node2: str, weight: float = 1.0):
    """Connect two nodes in the network"""
    propagator.connect_nodes(node1, node2)

def entangle_nodes(node1: str, node2: str):
    """Create quantum entanglement between nodes"""
    propagator.create_quantum_entanglement(node1, node2)

def get_network_stats(self) -> Dict[str, Any]:
    """Get comprehensive network statistics"""
    with self.lock:
        total_connections = sum(len(conns) for conns in self.connections.values()) // 2
        
        return {
            'nodes': len(self.nodes),
            'connections': total_connections,
            'active_signals': len(self.active_signals),
            'total_signals': len(self.signal_history),
            'entangled_pairs': len(self.entangled_pairs),
            'metrics': dict(self.signal_metrics),
            'signal_types': {
                sig_type.value: sum(
                    1 for sig in self.signal_history 
                    if sig.signal_type == sig_type
                )
                for sig_type in SignalType
            }
        }