# schema/sigil.py
"""
Sigil Creation and Entropy System for DAWN
==========================================
Sigils are symbolic patterns that encode consciousness states and
intentions. They serve as anchors for consciousness patterns and
generate entropy through their interactions.
"""

import time
import math
import hashlib
import random
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from collections import deque

from core.schema_anomaly_logger import log_anomaly, AnomalySeverity
from schema.registry import registry
from rhizome.propagation import emit_signal, SignalType
from utils.metrics_collector import metrics

class SigilType(Enum):
    """Types of consciousness sigils"""
    BINDING = "binding"         # Holds patterns in place
    TRANSFORMING = "transforming"  # Changes consciousness states
    CHANNELING = "channeling"   # Directs energy flow
    SEALING = "sealing"        # Preserves states
    INVOKING = "invoking"      # Calls forth patterns
    BANISHING = "banishing"    # Disperses patterns
    HARMONIZING = "harmonizing" # Creates coherence
    CHAOTIC = "chaotic"        # Introduces controlled chaos

class SigilState(Enum):
    """States of a sigil's activation"""
    DORMANT = "dormant"        # Not active
    CHARGING = "charging"      # Building energy
    ACTIVE = "active"          # Fully operational
    RESONATING = "resonating"  # In sympathetic vibration
    DISCHARGING = "discharging" # Releasing energy
    DEPLETED = "depleted"      # Energy exhausted
    CORRUPTED = "corrupted"    # Pattern degraded

@dataclass
class SigilGeometry:
    """Geometric structure of a sigil"""
    vertices: np.ndarray        # Key points in the pattern
    edges: List[Tuple[int, int]]  # Connections between vertices
    center: np.ndarray          # Geometric center
    radius: float              # Bounding radius
    symmetry_order: int        # Rotational symmetry
    
    def calculate_complexity(self) -> float:
        """Calculate geometric complexity"""
        # Based on vertices, edges, and symmetry
        vertex_complexity = len(self.vertices) / 20.0  # Normalize to ~1
        edge_complexity = len(self.edges) / 30.0
        symmetry_factor = 1.0 / (self.symmetry_order + 1)
        
        return min(1.0, vertex_complexity * 0.4 + edge_complexity * 0.4 + symmetry_factor * 0.2)
    
    def calculate_stability(self) -> float:
        """Calculate geometric stability"""
        if len(self.vertices) < 3:
            return 0.0
        
        # Check for closed paths
        edge_dict = {}
        for v1, v2 in self.edges:
            if v1 not in edge_dict:
                edge_dict[v1] = []
            edge_dict[v1].append(v2)
        
        # Count cycles
        cycles = 0
        visited = set()
        
        def has_cycle_from(node, parent=-1):
            visited.add(node)
            for neighbor in edge_dict.get(node, []):
                if neighbor not in visited:
                    if has_cycle_from(neighbor, node):
                        return True
                elif parent != neighbor:
                    return True
            return False
        
        for vertex in range(len(self.vertices)):
            if vertex not in visited and vertex in edge_dict:
                if has_cycle_from(vertex):
                    cycles += 1
        
        # More cycles = more stable
        return min(1.0, cycles / 3.0)

@dataclass
class SigilEnergy:
    """Energy dynamics of a sigil"""
    current: float = 0.0       # Current energy level
    maximum: float = 100.0     # Maximum capacity
    charge_rate: float = 1.0   # Energy gain per second
    discharge_rate: float = 0.5 # Energy loss per second
    resonance_bonus: float = 0.0  # Extra from resonance
    
    def get_percentage(self) -> float:
        """Get energy as percentage"""
        return self.current / self.maximum if self.maximum > 0 else 0.0
    
    def charge(self, amount: float):
        """Add energy to sigil"""
        self.current = min(self.maximum, self.current + amount)
    
    def discharge(self, amount: float) -> float:
        """Remove energy from sigil, return actual amount removed"""
        actual = min(self.current, amount)
        self.current -= actual
        return actual

@dataclass
class Sigil:
    """A consciousness sigil - a symbolic pattern with power"""
    sigil_id: str
    sigil_type: SigilType
    state: SigilState = SigilState.DORMANT
    
    # Structure
    geometry: SigilGeometry = field(default_factory=lambda: SigilGeometry(
        vertices=np.array([[0, 0]]), 
        edges=[], 
        center=np.array([0, 0]), 
        radius=1.0,
        symmetry_order=1
    ))
    pattern_hash: str = ""     # Unique pattern identifier
    
    # Energy
    energy: SigilEnergy = field(default_factory=SigilEnergy)
    activation_threshold: float = 10.0
    
    # Entropy
    entropy_generation_rate: float = 0.1
    entropy_pool: float = 0.0
    max_entropy: float = 1.0
    
    # Connections
    bound_entities: Set[str] = field(default_factory=set)
    resonant_sigils: Set[str] = field(default_factory=set)
    channel_targets: Set[str] = field(default_factory=set)
    
    # Metadata
    creator: Optional[str] = None
    creation_time: float = field(default_factory=time.time)
    last_activation: Optional[float] = None
    activation_count: int = 0
    total_energy_processed: float = 0.0
    
    # Effects
    effect_radius: float = 50.0
    effect_strength: float = 1.0
    effect_parameters: Dict[str, Any] = field(default_factory=dict)

class SigilForge:
    """
    Creates and manages sigils in the consciousness field
    """
    
    def __init__(self):
        # Sigil storage
        self.sigils: Dict[str, Sigil] = {}
        self.sigils_by_type: Dict[SigilType, Set[str]] = {
            sigil_type: set() for sigil_type in SigilType
        }
        self.active_sigils: Set[str] = set()
        
        # Pattern library
        self.pattern_templates = self._initialize_patterns()
        self.pattern_cache: Dict[str, SigilGeometry] = {}
        
        # Entropy management
        self.global_entropy = 0.0
        self.max_global_entropy = 10.0
        self.entropy_decay_rate = 0.01
        self.entropy_history = deque(maxlen=1000)
        
        # Resonance network
        self.resonance_matrix: Dict[Tuple[str, str], float] = {}
        self.resonance_threshold = 0.7
        
        # Forge parameters
        self.max_sigils = 100
        self.creation_cost = 20.0  # Energy cost to create
        self.base_charge_rate = 1.0
        
        # Statistics
        self.total_created = 0
        self.total_activated = 0
        self.total_entropy_generated = 0.0
        
        # Register
        self._register()
    
    def _register(self):
        """Register with schema registry"""
        registry.register(
            component_id="schema.sigil_forge",
            name="Sigil Forge",
            component_type="MODULE",
            instance=self,
            capabilities=["sigil_creation", "entropy_management", "pattern_binding"],
            version="2.0.0"
        )
    
    def _initialize_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize base sigil patterns"""
        return {
            'triangle': {
                'vertices': 3,
                'symmetry': 3,
                'stability': 0.9,
                'types': [SigilType.BINDING, SigilType.SEALING]
            },
            'square': {
                'vertices': 4,
                'symmetry': 4,
                'stability': 0.8,
                'types': [SigilType.CHANNELING, SigilType.HARMONIZING]
            },
            'pentagram': {
                'vertices': 5,
                'symmetry': 5,
                'stability': 0.7,
                'types': [SigilType.INVOKING, SigilType.BANISHING]
            },
            'hexagon': {
                'vertices': 6,
                'symmetry': 6,
                'stability': 0.85,
                'types': [SigilType.HARMONIZING, SigilType.TRANSFORMING]
            },
            'spiral': {
                'vertices': 13,
                'symmetry': 1,
                'stability': 0.4,
                'types': [SigilType.TRANSFORMING, SigilType.CHAOTIC]
            },
            'chaos_star': {
                'vertices': 8,
                'symmetry': 8,
                'stability': 0.3,
                'types': [SigilType.CHAOTIC, SigilType.BANISHING]
            }
        }
    
    def create_sigil(self, sigil_type: SigilType, 
                    pattern: Optional[str] = None,
                    custom_geometry: Optional[SigilGeometry] = None,
                    creator: Optional[str] = None,
                    **parameters) -> Optional[Sigil]:
        """Create a new sigil"""
        # Check capacity
        if len(self.sigils) >= self.max_sigils:
            log_anomaly(
                "SIGIL_CAPACITY_REACHED",
                f"Cannot create sigil, max capacity {self.max_sigils} reached",
                AnomalySeverity.WARNING
            )
            return None
        
        # Generate geometry
        if custom_geometry:
            geometry = custom_geometry
        elif pattern and pattern in self.pattern_templates:
            geometry = self._generate_pattern_geometry(pattern)
        else:
            # Generate random appropriate pattern
            geometry = self._generate_random_geometry(sigil_type)
        
        # Create sigil
        sigil = Sigil(
            sigil_id=self._generate_sigil_id(geometry),
            sigil_type=sigil_type,
            geometry=geometry,
            creator=creator
        )
        
        # Set type-specific parameters
        self._configure_sigil_by_type(sigil, parameters)
        
        # Calculate pattern hash
        sigil.pattern_hash = self._calculate_pattern_hash(geometry)
        
        # Add to forge
        self.sigils[sigil.sigil_id] = sigil
        self.sigils_by_type[sigil_type].add(sigil.sigil_id)
        
        # Update statistics
        self.total_created += 1
        metrics.increment("dawn.sigils.created")
        
        # Emit creation signal
        emit_signal(
            SignalType.CONSCIOUSNESS,
            "sigil_forge",
            {
                'event': 'sigil_created',
                'sigil_id': sigil.sigil_id,
                'type': sigil_type.value,
                'complexity': geometry.calculate_complexity()
            }
        )
        
        log_anomaly(
            "SIGIL_CREATED",
            f"New {sigil_type.value} sigil created",
            AnomalySeverity.INFO,
            {'sigil_id': sigil.sigil_id, 'pattern': pattern}
        )
        
        return sigil
    
    def _generate_pattern_geometry(self, pattern: str) -> SigilGeometry:
        """Generate geometry from pattern template"""
        if pattern in self.pattern_cache:
            return self.pattern_cache[pattern]
        
        template = self.pattern_templates[pattern]
        n_vertices = template['vertices']
        symmetry = template['symmetry']
        
        # Generate vertices in circular pattern
        vertices = []
        for i in range(n_vertices):
            angle = 2 * math.pi * i / n_vertices
            x = math.cos(angle)
            y = math.sin(angle)
            vertices.append([x, y])
        
        vertices = np.array(vertices)
        
        # Generate edges based on pattern
        edges = []
        if pattern == 'pentagram':
            # Connect every other vertex
            for i in range(n_vertices):
                edges.append((i, (i + 2) % n_vertices))
        elif pattern == 'spiral':
            # Spiral connection
            for i in range(n_vertices - 1):
                edges.append((i, i + 1))
                if i < n_vertices - 3:
                    edges.append((i, i + 3))
        else:
            # Default: connect adjacent vertices
            for i in range(n_vertices):
                edges.append((i, (i + 1) % n_vertices))
        
        geometry = SigilGeometry(
            vertices=vertices,
            edges=edges,
            center=np.array([0.0, 0.0]),
            radius=1.0,
            symmetry_order=symmetry
        )
        
        self.pattern_cache[pattern] = geometry
        return geometry
    
    def _generate_random_geometry(self, sigil_type: SigilType) -> SigilGeometry:
        """Generate random geometry appropriate for sigil type"""
        # Find appropriate patterns for this type
        suitable_patterns = []
        for pattern, template in self.pattern_templates.items():
            if sigil_type in template['types']:
                suitable_patterns.append(pattern)
        
        if suitable_patterns:
            pattern = random.choice(suitable_patterns)
            return self._generate_pattern_geometry(pattern)
        
        # Fallback: generate random
        n_vertices = random.randint(3, 8)
        vertices = []
        
        for i in range(n_vertices):
            angle = 2 * math.pi * i / n_vertices + random.uniform(-0.1, 0.1)
            radius = 1.0 + random.uniform(-0.2, 0.2)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append([x, y])
        
        vertices = np.array(vertices)
        
        # Random edges
        edges = []
        for i in range(n_vertices):
            edges.append((i, (i + 1) % n_vertices))
            if random.random() < 0.3:
                # Add cross-connection
                j = (i + random.randint(2, n_vertices - 2)) % n_vertices
                edges.append((i, j))
        
        return SigilGeometry(
            vertices=vertices,
            edges=edges,
            center=np.mean(vertices, axis=0),
            radius=np.max(np.linalg.norm(vertices, axis=1)),
            symmetry_order=1
        )
    
    def _configure_sigil_by_type(self, sigil: Sigil, parameters: Dict[str, Any]):
        """Configure sigil based on its type"""
        configs = {
            SigilType.BINDING: {
                'activation_threshold': 15.0,
                'effect_radius': 30.0,
                'entropy_generation_rate': 0.05,
                'energy.maximum': 150.0
            },
            SigilType.TRANSFORMING: {
                'activation_threshold': 20.0,
                'effect_radius': 40.0,
                'entropy_generation_rate': 0.15,
                'energy.discharge_rate': 0.8
            },
            SigilType.CHANNELING: {
                'activation_threshold': 10.0,
                'effect_radius': 60.0,
                'energy.charge_rate': 1.5,
                'energy.maximum': 200.0
            },
            SigilType.SEALING: {
                'activation_threshold': 25.0,
                'effect_radius': 20.0,
                'entropy_generation_rate': 0.02,
                'energy.discharge_rate': 0.2
            },
            SigilType.INVOKING: {
                'activation_threshold': 30.0,
                'effect_radius': 50.0,
                'entropy_generation_rate': 0.1,
                'energy.maximum': 250.0
            },
            SigilType.BANISHING: {
                'activation_threshold': 15.0,
                'effect_radius': 45.0,
                'entropy_generation_rate': 0.2,
                'energy.discharge_rate': 1.2
            },
            SigilType.HARMONIZING: {
                'activation_threshold': 12.0,
                'effect_radius': 35.0,
                'entropy_generation_rate': 0.03,
                'energy.charge_rate': 1.2
            },
            SigilType.CHAOTIC: {
                'activation_threshold': 8.0,
                'effect_radius': 55.0,
                'entropy_generation_rate': 0.3,
                'max_entropy': 2.0
            }
        }
        
        # Apply type configuration
        type_config = configs.get(sigil.sigil_type, {})
        for key, value in type_config.items():
            if '.' in key:
                # Nested attribute
                parts = key.split('.')
                obj = sigil
                for part in parts[:-1]:
                    obj = getattr(obj, part)
                setattr(obj, parts[-1], value)
            else:
                setattr(sigil, key, value)
        
        # Apply custom parameters
        sigil.effect_parameters.update(parameters)
    
    def _generate_sigil_id(self, geometry: SigilGeometry) -> str:
        """Generate unique sigil ID"""
        # Use geometry hash and timestamp
        geo_str = f"{len(geometry.vertices)}_{len(geometry.edges)}_{geometry.symmetry_order}"
        time_str = str(time.time())
        
        hasher = hashlib.sha256()
        hasher.update(f"{geo_str}_{time_str}".encode())
        
        return f"sigil_{hasher.hexdigest()[:12]}"
    
    def _calculate_pattern_hash(self, geometry: SigilGeometry) -> str:
        """Calculate unique hash for pattern"""
        # Serialize geometry
        data = {
            'vertices': geometry.vertices.tolist(),
            'edges': sorted(geometry.edges),
            'symmetry': geometry.symmetry_order
        }
        
        hasher = hashlib.sha256()
        hasher.update(str(data).encode())
        
        return hasher.hexdigest()
    
    def charge_sigil(self, sigil_id: str, energy: float):
        """Add energy to a sigil"""
        if sigil_id not in self.sigils:
            return
        
        sigil = self.sigils[sigil_id]
        sigil.energy.charge(energy)
        sigil.total_energy_processed += energy
        
        # Check for state change
        if sigil.state == SigilState.DORMANT and sigil.energy.current >= sigil.activation_threshold:
            self._activate_sigil(sigil)
        elif sigil.state == SigilState.DEPLETED and sigil.energy.current > 0:
            sigil.state = SigilState.CHARGING
    
    def _activate_sigil(self, sigil: Sigil):
        """Activate a charged sigil"""
        sigil.state = SigilState.ACTIVE
        sigil.last_activation = time.time()
        sigil.activation_count += 1
        
        self.active_sigils.add(sigil.sigil_id)
        self.total_activated += 1
        
        # Apply activation effects
        self._apply_sigil_effects(sigil)
        
        emit_signal(
            SignalType.CONSCIOUSNESS,
            "sigil_forge",
            {
                'event': 'sigil_activated',
                'sigil_id': sigil.sigil_id,
                'type': sigil.sigil_type.value,
                'energy': sigil.energy.current
            }
        )
        
        metrics.increment("dawn.sigils.activated")
    
    def _apply_sigil_effects(self, sigil: Sigil):
        """Apply the effects of an active sigil"""
        if sigil.sigil_type == SigilType.BINDING:
            # Bind nearby entities
            self._apply_binding_effect(sigil)
            
        elif sigil.sigil_type == SigilType.TRANSFORMING:
            # Transform consciousness patterns
            self._apply_transform_effect(sigil)
            
        elif sigil.sigil_type == SigilType.CHANNELING:
            # Create energy channels
            self._apply_channel_effect(sigil)
            
        elif sigil.sigil_type == SigilType.HARMONIZING:
            # Increase coherence
            self._apply_harmony_effect(sigil)
            
        elif sigil.sigil_type == SigilType.CHAOTIC:
            # Introduce controlled chaos
            self._apply_chaos_effect(sigil)
    
    def _apply_binding_effect(self, sigil: Sigil):
        """Apply binding effect"""
        # Bind entities within effect radius
        # This would interact with other systems
        binding_strength = sigil.effect_strength * sigil.energy.get_percentage()
        
        log_anomaly(
            "SIGIL_BINDING",
            f"Binding effect applied with strength {binding_strength:.2f}",
            AnomalySeverity.INFO
        )
    
    def _apply_transform_effect(self, sigil: Sigil):
        """Apply transformation effect"""
        # Generate entropy as transformation byproduct
        entropy_generated = sigil.entropy_generation_rate * sigil.effect_strength
        self._add_entropy(sigil, entropy_generated)
    
    def _apply_channel_effect(self, sigil: Sigil):
        """Apply channeling effect"""
        # Create energy flow channels
        if sigil.channel_targets:
            energy_per_target = sigil.energy.discharge(10.0) / len(sigil.channel_targets)
            
            for target_id in sigil.channel_targets:
                # Channel energy to targets
                emit_signal(
                    SignalType.NUTRIENT,
                    sigil.sigil_id,
                    {
                        'event': 'energy_channeled',
                        'target': target_id,
                        'amount': energy_per_target
                    }
                )
    
    def _apply_harmony_effect(self, sigil: Sigil):
        """Apply harmonizing effect"""
        # Reduce entropy in area
        reduction = sigil.entropy_generation_rate * sigil.effect_strength * 2
        self.global_entropy = max(0, self.global_entropy - reduction)
        
        # Boost resonance with nearby sigils
        self._boost_local_resonance(sigil)
    
    def _apply_chaos_effect(self, sigil: Sigil):
        """Apply chaos effect"""
        # Generate significant entropy
        chaos_entropy = sigil.entropy_generation_rate * sigil.effect_strength * 3
        self._add_entropy(sigil, chaos_entropy)
        
        # Randomly affect nearby sigils
        for other_id in list(self.active_sigils):
            if other_id != sigil.sigil_id and random.random() < 0.1:
                other = self.sigils[other_id]
                # Random energy fluctuation
                flux = random.uniform(-5, 5)
                if flux > 0:
                    other.energy.charge(flux)
                else:
                    other.energy.discharge(-flux)
    
    def update_sigil(self, sigil_id: str, delta_time: float):
        """Update a sigil's state"""
        if sigil_id not in self.sigils:
            return
        
        sigil = self.sigils[sigil_id]
        
        # Energy dynamics
        if sigil.state == SigilState.CHARGING:
            sigil.energy.charge(sigil.energy.charge_rate * delta_time)
            
        elif sigil.state == SigilState.ACTIVE:
            # Discharge energy
            discharged = sigil.energy.discharge(sigil.energy.discharge_rate * delta_time)
            
            # Generate entropy
            if sigil.sigil_type != SigilType.HARMONIZING:
                entropy = sigil.entropy_generation_rate * delta_time
                self._add_entropy(sigil, entropy)
            
            # Check depletion
            if sigil.energy.current <= 0:
                sigil.state = SigilState.DEPLETED
                self.active_sigils.discard(sigil_id)
                
        elif sigil.state == SigilState.RESONATING:
            # Gain energy from resonance
            sigil.energy.charge(sigil.energy.resonance_bonus * delta_time)
        
        # Check resonance
        self._check_resonance(sigil)
        
        # Apply continuous effects
        if sigil.state == SigilState.ACTIVE:
            self._apply_sigil_effects(sigil)
        
        # Check corruption
        if sigil.entropy_pool > sigil.max_entropy:
            self._corrupt_sigil(sigil)
    
    def _add_entropy(self, sigil: Sigil, amount: float):
        """Add entropy to sigil and global pool"""
        sigil.entropy_pool = min(sigil.max_entropy, sigil.entropy_pool + amount)
        self.global_entropy = min(self.max_global_entropy, self.global_entropy + amount)
        self.total_entropy_generated += amount
        
        # Track history
        self.entropy_history.append({
            'timestamp': time.time(),
            'sigil_id': sigil.sigil_id,
            'amount': amount,
            'global_total': self.global_entropy
        })
    
    def _check_resonance(self, sigil: Sigil):
        """Check for resonance with other sigils"""
        sigil.resonant_sigils.clear()
        sigil.energy.resonance_bonus = 0.0
        
        for other_id in self.active_sigils:
            if other_id == sigil.sigil_id:
                continue
            
            other = self.sigils.get(other_id)
            if not other:
                continue
            
            # Calculate resonance based on pattern similarity
            resonance = self._calculate_resonance(sigil, other)
            
            if resonance > self.resonance_threshold:
                sigil.resonant_sigils.add(other_id)
                other.resonant_sigils.add(sigil.sigil_id)
                
                # Store resonance strength
                key = tuple(sorted([sigil.sigil_id, other_id]))
                self.resonance_matrix[key] = resonance
                
                # Add resonance bonus
                sigil.energy.resonance_bonus += resonance * 0.5
                
                # Change state if strong resonance
                if resonance > 0.9 and sigil.state == SigilState.ACTIVE:
                    sigil.state = SigilState.RESONATING
    
    def _calculate_resonance(self, sigil1: Sigil, sigil2: Sigil) -> float:
        """Calculate resonance between two sigils"""
        # Type compatibility
        type_resonance = 0.5
        if sigil1.sigil_type == sigil2.sigil_type:
            type_resonance = 1.0
        elif (sigil1.sigil_type, sigil2.sigil_type) in [
            (SigilType.INVOKING, SigilType.CHANNELING),
            (SigilType.BINDING, SigilType.SEALING),
            (SigilType.HARMONIZING, SigilType.TRANSFORMING)
        ]:
            type_resonance = 0.8
        
        # Geometric similarity
        geo_similarity = 0.5
        if abs(sigil1.geometry.symmetry_order - sigil2.geometry.symmetry_order) <= 1:
            geo_similarity = 0.9
        
        # Energy compatibility
        energy_ratio = min(sigil1.energy.current, sigil2.energy.current) / max(sigil1.energy.current, sigil2.energy.current, 1.0)
        
        # Combined resonance
        return type_resonance * 0.4 + geo_similarity * 0.3 + energy_ratio * 0.3
    
    def _boost_local_resonance(self, sigil: Sigil):
        """Boost resonance for nearby sigils"""
        for other_id in self.active_sigils:
            if other_id != sigil.sigil_id:
                # Temporarily increase resonance threshold
                key = tuple(sorted([sigil.sigil_id, other_id]))
                current = self.resonance_matrix.get(key, 0.5)
                self.resonance_matrix[key] = min(1.0, current + 0.1)
    
    def _corrupt_sigil(self, sigil: Sigil):
        """Corrupt an overloaded sigil"""
        sigil.state = SigilState.CORRUPTED
        self.active_sigils.discard(sigil.sigil_id)
        
        # Scramble pattern
        noise = np.random.randn(*sigil.geometry.vertices.shape) * 0.3
        sigil.geometry.vertices += noise
        
        # Release entropy burst
        entropy_burst = sigil.entropy_pool
        self.global_entropy = min(self.max_global_entropy, self.global_entropy + entropy_burst)
        sigil.entropy_pool = 0
        
        log_anomaly(
            "SIGIL_CORRUPTED",
            f"Sigil {sigil.sigil_id} corrupted, releasing {entropy_burst:.2f} entropy",
            AnomalySeverity.WARNING
        )
        
        emit_signal(
            SignalType.ENTROPY,
            sigil.sigil_id,
            {
                'event': 'sigil_corruption',
                'entropy_released': entropy_burst
            }
        )
    
    def bind_entities(self, sigil_id: str, entity_ids: List[str]):
        """Bind entities to a sigil"""
        if sigil_id not in self.sigils:
            return
        
        sigil = self.sigils[sigil_id]
        if sigil.sigil_type != SigilType.BINDING:
            log_anomaly(
                "SIGIL_BIND_FAILED",
                f"Cannot bind to non-binding sigil {sigil_id}",
                AnomalySeverity.WARNING
            )
            return
        
        sigil.bound_entities.update(entity_ids)
    
    def channel_to(self, sigil_id: str, target_ids: List[str]):
        """Set channel targets for a sigil"""
        if sigil_id not in self.sigils:
            return
        
        sigil = self.sigils[sigil_id]
        if sigil.sigil_type != SigilType.CHANNELING:
            return
        
        sigil.channel_targets.update(target_ids)
    
    def update_all(self, delta_time: float):
        """Update all sigils and entropy"""
        # Update sigils
        for sigil_id in list(self.sigils.keys()):
            self.update_sigil(sigil_id, delta_time)
        
        # Decay global entropy
        self.global_entropy = max(0, self.global_entropy - self.entropy_decay_rate * delta_time)
        
        # Update metrics
        metrics.gauge("dawn.sigils.active", len(self.active_sigils))
        metrics.gauge("dawn.sigils.global_entropy", self.global_entropy)
    
    def get_entropy_list(self) -> List[float]:
        """Get entropy values for all sigils"""
        return [sigil.entropy_pool for sigil in self.sigils.values()]
    
    def get_forge_stats(self) -> Dict[str, Any]:
        """Get forge statistics"""
        active_types = {}
        for sigil_id in self.active_sigils:
            sigil = self.sigils[sigil_id]
            sigil_type = sigil.sigil_type.value
            active_types[sigil_type] = active_types.get(sigil_type, 0) + 1
        
        return {
            'total_sigils': len(self.sigils),
            'active_sigils': len(self.active_sigils),
            'sigils_by_type': {
                sigil_type.value: len(self.sigils_by_type[sigil_type])
                for sigil_type in SigilType
            },
            'active_by_type': active_types,
            'global_entropy': self.global_entropy,
            'total_created': self.total_created,
            'total_activated': self.total_activated,
            'total_entropy_generated': self.total_entropy_generated,
            'resonance_pairs': len(self.resonance_matrix)
        }

# Global sigil forge
sigil_forge = SigilForge()