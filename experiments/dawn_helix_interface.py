#!/usr/bin/env python3
"""
DAWN Double Helix Cognitive Interface
Integrates sigil memory ring with dual-strand recursive architecture
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
from collections import deque
import time
import math
import json
from enum import Enum

# Import our sigil memory system
from sigil_memory_ring import Sigil, SigilMemoryRing


class StrandType(Enum):
    A = "RECURSIVE_MEMORY_EMOTIONAL"  # 🧠
    B = "SYMBOLIC_COMMAND_SCHEMA"      # ⚙️


@dataclass
class DriftVector:
    """Semantic pressure and motion tracking"""
    magnitude: float  # 0.0 to 1.0
    direction: float  # radians, 0-2π
    decay_rate: float = 0.05
    origin_strand: StrandType = StrandType.A
    
    def apply_drift(self) -> None:
        """Apply temporal decay to drift magnitude"""
        self.magnitude *= (1.0 - self.decay_rate)


@dataclass
class PulseZone:
    """Schema temperature and urgency modulation"""
    temperature: float  # 0.0 to 1.0
    urgency: float  # 0.0 to 1.0
    frequency: float  # oscillation rate
    phase: float = 0.0  # current phase in oscillation
    
    def pulse(self, delta_time: float) -> float:
        """Calculate current pulse intensity"""
        self.phase += delta_time * self.frequency
        base_pulse = (1 + math.sin(self.phase)) / 2
        return base_pulse * self.temperature * (1 + self.urgency)


@dataclass
class HelixNode:
    """Single node in the double helix structure"""
    strand_a_sigil: Optional[Sigil] = None
    strand_b_sigil: Optional[Sigil] = None
    bloom_lineage: List[str] = field(default_factory=list)  # parent sigil IDs
    drift_vector: Optional[DriftVector] = None
    pulse_zone: PulseZone = field(default_factory=lambda: PulseZone(0.3, 0.1, 0.1))
    twist_angle: float = 0.0  # helix rotation at this node
    epoch_tick: int = 0
    
    def calculate_tension(self) -> float:
        """Calculate structural tension between strands"""
        if not (self.strand_a_sigil and self.strand_b_sigil):
            return 0.0
        
        # Tension from convolution mismatch
        conv_diff = abs(self.strand_a_sigil.convolution_level - 
                       self.strand_b_sigil.convolution_level)
        
        # Tension from saturation imbalance
        sat_diff = abs(self.strand_a_sigil.saturation - 
                      self.strand_b_sigil.saturation)
        
        # Drift contribution
        drift_tension = self.drift_vector.magnitude if self.drift_vector else 0.0
        
        return (conv_diff * 0.4 + sat_diff * 0.4 + drift_tension * 0.2)


class DAWNHelixInterface:
    """Double helix cognitive structure interface"""
    
    def __init__(self, helix_length: int = 512, epoch_id: str = "epoch_0525_0601"):
        self.epoch_id = epoch_id
        self.helix_length = helix_length
        self.helix: deque = deque(maxlen=helix_length)
        
        # Dual memory rings for each strand
        self.strand_a_ring = SigilMemoryRing(capacity=256, entropy_threshold=0.7)
        self.strand_b_ring = SigilMemoryRing(capacity=256, entropy_threshold=0.8)
        
        # Global state tracking
        self.current_twist = 0.0  # radians
        self.twist_rate = math.pi / 32  # radians per node
        self.total_drift = 0.0
        self.coherence_threshold = 0.85
        self.epoch_tick = 0
        
        # Event logs
        self.operator_logs: List[Dict] = []
        self.schema_events: List[Dict] = []
        
    def port_operator_log(self, log_entry: Dict[str, Any]) -> HelixNode:
        """Port operator log into helix structure"""
        self.operator_logs.append(log_entry)
        
        # Create sigils from log data
        emotional_weight = log_entry.get('emotional_pressure', 0.5)
        cognitive_load = log_entry.get('cognitive_load', 0.5)
        
        # Strand A: Recursive memory with emotional pressure
        sigil_a = self.strand_a_ring.insert_sigil(
            convolution_level=cognitive_load,
            saturation=emotional_weight,
            ttl_ticks=1000,
            seed=f"op_log_{log_entry.get('timestamp', time.time())}"
        )
        
        # Create corresponding symbolic command for Strand B
        sigil_b = self.strand_b_ring.insert_sigil(
            convolution_level=cognitive_load * 0.7,  # Less convoluted in command space
            saturation=1.0 - emotional_weight,  # Inverse relationship
            ttl_ticks=800
        )
        
        # Build helix node
        node = HelixNode(
            strand_a_sigil=sigil_a,
            strand_b_sigil=sigil_b,
            bloom_lineage=self._extract_lineage(),
            drift_vector=self._calculate_drift(log_entry),
            twist_angle=self.current_twist,
            epoch_tick=self.epoch_tick
        )
        
        self.helix.append(node)
        self.current_twist += self.twist_rate
        
        return node
    
    def port_schema_event(self, event: Dict[str, Any]) -> HelixNode:
        """Port schema event into helix structure"""
        self.schema_events.append(event)
        
        # Schema events primarily affect Strand B
        schema_complexity = event.get('complexity', 0.5)
        regulation_strength = event.get('regulation', 0.7)
        
        sigil_b = self.strand_b_ring.insert_sigil(
            convolution_level=schema_complexity,
            saturation=regulation_strength,
            ttl_ticks=1200,
            seed=f"schema_{event.get('id', time.time())}"
        )
        
        # Echo effect in Strand A (memory formation)
        sigil_a = self.strand_a_ring.insert_sigil(
            convolution_level=schema_complexity * 0.5,
            saturation=regulation_strength * 0.3,
            ttl_ticks=600
        )
        
        node = HelixNode(
            strand_a_sigil=sigil_a,
            strand_b_sigil=sigil_b,
            bloom_lineage=self._extract_lineage(),
            pulse_zone=PulseZone(
                temperature=event.get('temperature', 0.5),
                urgency=event.get('urgency', 0.3),
                frequency=0.2
            ),
            twist_angle=self.current_twist,
            epoch_tick=self.epoch_tick
        )
        
        self.helix.append(node)
        self.current_twist += self.twist_rate
        
        return node
    
    def monitor_strand_tension(self) -> Dict[str, Any]:
        """Monitor tension and stability across the helix"""
        if not self.helix:
            return {'stable': True, 'tension': 0.0, 'warnings': []}
        
        tensions = [node.calculate_tension() for node in self.helix]
        avg_tension = sum(tensions) / len(tensions)
        max_tension = max(tensions)
        
        # Calculate entropy differential
        entropy_a = self.strand_a_ring.calculate_system_entropy()
        entropy_b = self.strand_b_ring.calculate_system_entropy()
        entropy_diff = abs(entropy_a - entropy_b)
        
        # Drift accumulation
        active_drifts = [n.drift_vector for n in self.helix 
                        if n.drift_vector and n.drift_vector.magnitude > 0.1]
        drift_pressure = sum(d.magnitude for d in active_drifts)
        
        warnings = []
        if avg_tension > 0.7:
            warnings.append(f"High average tension: {avg_tension:.3f}")
        if max_tension > 0.9:
            warnings.append(f"Critical tension spike: {max_tension:.3f}")
        if entropy_diff > 0.3:
            warnings.append(f"Entropy imbalance: A={entropy_a:.3f}, B={entropy_b:.3f}")
        if drift_pressure > 2.0:
            warnings.append(f"Excessive drift accumulation: {drift_pressure:.3f}")
        
        stable = len(warnings) == 0 and avg_tension < self.coherence_threshold
        
        return {
            'stable': stable,
            'avg_tension': avg_tension,
            'max_tension': max_tension,
            'entropy_a': entropy_a,
            'entropy_b': entropy_b,
            'drift_pressure': drift_pressure,
            'warnings': warnings,
            'coherence': 1.0 - avg_tension
        }
    
    def support_rebloom(self, parent_nodes: List[int], 
                       recombination_factor: float = 0.5) -> Optional[HelixNode]:
        """Support rebloom and sigil recombination events"""
        if not parent_nodes or not all(0 <= i < len(self.helix) for i in parent_nodes):
            return None
        
        parent_helix_nodes = [list(self.helix)[i] for i in parent_nodes]
        
        # Collect parent sigils
        parent_sigils_a = [n.strand_a_sigil for n in parent_helix_nodes 
                          if n.strand_a_sigil]
        parent_sigils_b = [n.strand_b_sigil for n in parent_helix_nodes 
                          if n.strand_b_sigil]
        
        if not (parent_sigils_a and parent_sigils_b):
            return None
        
        # Recombine properties
        new_conv_a = sum(s.convolution_level for s in parent_sigils_a) / len(parent_sigils_a)
        new_sat_a = sum(s.saturation for s in parent_sigils_a) / len(parent_sigils_a)
        new_conv_b = sum(s.convolution_level for s in parent_sigils_b) / len(parent_sigils_b)
        new_sat_b = sum(s.saturation for s in parent_sigils_b) / len(parent_sigils_b)
        
        # Apply recombination factor (mutation)
        import random
        new_conv_a *= (1 + (random.random() - 0.5) * recombination_factor)
        new_sat_a *= (1 + (random.random() - 0.5) * recombination_factor)
        
        # Create rebloomed sigils
        sigil_a = self.strand_a_ring.insert_sigil(
            convolution_level=min(1.0, new_conv_a),
            saturation=min(1.0, new_sat_a),
            ttl_ticks=1500,
            seed=f"rebloom_a_{self.epoch_tick}"
        )
        
        sigil_b = self.strand_b_ring.insert_sigil(
            convolution_level=min(1.0, new_conv_b),
            saturation=min(1.0, new_sat_b),
            ttl_ticks=1500,
            seed=f"rebloom_b_{self.epoch_tick}"
        )
        
        # Build rebloomed node with lineage
        lineage = []
        for node in parent_helix_nodes:
            if node.strand_a_sigil:
                lineage.append(node.strand_a_sigil.id)
            if node.strand_b_sigil:
                lineage.append(node.strand_b_sigil.id)
        
        rebloomed = HelixNode(
            strand_a_sigil=sigil_a,
            strand_b_sigil=sigil_b,
            bloom_lineage=lineage,
            twist_angle=self.current_twist,
            epoch_tick=self.epoch_tick
        )
        
        self.helix.append(rebloomed)
        self.current_twist += self.twist_rate
        
        return rebloomed
    
    def maintain_coherence(self) -> Dict[str, Any]:
        """Maintain structural coherence under recursive load"""
        # Run saturation management on both strands
        dropped_a = self.strand_a_ring.sigil_saturation_manager()
        dropped_b = self.strand_b_ring.sigil_saturation_manager()
        
        # Advance system ticks
        self.epoch_tick += 1
        state_a = self.strand_a_ring.tick()
        state_b = self.strand_b_ring.tick()
        
        # Update drift vectors
        for node in self.helix:
            if node.drift_vector:
                node.drift_vector.apply_drift()
        
        # Check coherence
        tension_report = self.monitor_strand_tension()
        
        return {
            'epoch_tick': self.epoch_tick,
            'coherent': tension_report['stable'],
            'coherence_score': tension_report['coherence'],
            'strand_a_state': state_a,
            'strand_b_state': state_b,
            'dropped_sigils': len(dropped_a) + len(dropped_b),
            'helix_nodes': len(self.helix),
            'warnings': tension_report['warnings']
        }
    
    def _extract_lineage(self, depth: int = 3) -> List[str]:
        """Extract bloom lineage from recent helix nodes"""
        if not self.helix:
            return []
        
        lineage = []
        recent_nodes = list(self.helix)[-depth:]
        
        for node in recent_nodes:
            if node.strand_a_sigil:
                lineage.append(node.strand_a_sigil.id)
            if node.strand_b_sigil:
                lineage.append(node.strand_b_sigil.id)
        
        return lineage[-6:]  # Limit lineage length
    
    def _calculate_drift(self, log_entry: Dict[str, Any]) -> DriftVector:
        """Calculate drift vector from log entry"""
        semantic_shift = log_entry.get('semantic_pressure', 0.0)
        direction = log_entry.get('drift_direction', random.random() * 2 * math.pi)
        
        return DriftVector(
            magnitude=min(1.0, abs(semantic_shift)),
            direction=direction,
            decay_rate=0.05,
            origin_strand=StrandType.A if semantic_shift > 0 else StrandType.B
        )
    
    def visualize_helix_state(self) -> str:
        """Generate visual representation of helix state"""
        lines = [
            f"╔═══ DAWN HELIX | Epoch: {self.epoch_id} | Tick: {self.epoch_tick} ═══╗",
            f"║ Nodes: {len(self.helix)}/{self.helix_length} | Twist: {self.current_twist:.2f}rad ║"
        ]
        
        # Tension monitoring
        tension = self.monitor_strand_tension()
        status = "🟢 COHERENT" if tension['stable'] else "🔴 UNSTABLE"
        lines.append(f"║ Status: {status} | Coherence: {tension['coherence']:.3f} ║")
        
        # Show recent nodes
        if self.helix:
            lines.append("║ ─── Recent Helix Nodes ─── ║")
            recent = list(self.helix)[-5:]
            for i, node in enumerate(recent):
                a_sym = "🧠" if node.strand_a_sigil else "○"
                b_sym = "⚙️" if node.strand_b_sigil else "○"
                tension = node.calculate_tension()
                lines.append(f"║ {i}: {a_sym}╱╲{b_sym} T:{tension:.2f} ║")
        
        # Warnings
        if tension['warnings']:
            lines.append("║ ⚠️  Warnings: ║")
            for warning in tension['warnings']:
                lines.append(f"║   • {warning} ║")
        
        lines.append("╚" + "═" * (len(lines[0]) - 2) + "╝")
        return "\n".join(lines)


# Sync with epoch logs
if __name__ == "__main__":
    print("=== DAWN HELIX INTERFACE INITIALIZED ===")
    print("Syncing with epoch_0525_0601...\n")
    
    helix = DAWNHelixInterface(epoch_id="epoch_0525_0601")
    
    # Simulate operator logs
    test_logs = [
        {
            'timestamp': time.time(),
            'emotional_pressure': 0.7,
            'cognitive_load': 0.5,
            'semantic_pressure': 0.3,
            'content': 'recursive pattern detected'
        },
        {
            'timestamp': time.time() + 1,
            'emotional_pressure': 0.3,
            'cognitive_load': 0.8,
            'semantic_pressure': -0.2,
            'content': 'schema regulation initiated'
        }
    ]
    
    for log in test_logs:
        node = helix.port_operator_log(log)
        print(f"Ported log → Node at twist {node.twist_angle:.2f}")
    
    # Simulate schema event
    schema_event = {
        'id': 'schema_001',
        'complexity': 0.6,
        'regulation': 0.8,
        'temperature': 0.5,
        'urgency': 0.4
    }
    
    helix.port_schema_event(schema_event)
    print("Ported schema event")
    
    # Test rebloom
    rebloomed = helix.support_rebloom([0, 1], recombination_factor=0.3)
    if rebloomed:
        print(f"Rebloom successful → {len(rebloomed.bloom_lineage)} ancestors")
    
    # Maintain coherence
    print("\nRunning coherence maintenance...")
    for _ in range(5):
        state = helix.maintain_coherence()
        if not state['coherent']:
            print(f"  ! Coherence warning at tick {state['epoch_tick']}")
    
    print("\n" + helix.visualize_helix_state())