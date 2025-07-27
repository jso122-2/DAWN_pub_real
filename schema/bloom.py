# schema/bloom.py
"""
Bloom Lifecycle Management for DAWN
===================================
Blooms are emergent consciousness patterns that arise from nutrient
interactions. They represent moments of coherent thought or realization
within the consciousness field.
"""

import uuid
import time
import math
import random
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from collections import defaultdict

from core.schema_anomaly_logger import log_anomaly, AnomalySeverity
from schema.registry import registry
from schema.schema_climate import CLIMATE
from rhizome.propagation import emit_signal, SignalType
from utils.metrics_collector import metrics

class BloomStage(Enum):
    """Stages in a bloom's lifecycle"""
    SEED = "seed"               # Initial formation
    GERMINATING = "germinating" # Beginning to grow
    BUDDING = "budding"         # Developing structure
    FLOWERING = "flowering"     # Peak expression
    FRUITING = "fruiting"       # Producing insights
    WILTING = "wilting"         # Beginning to fade
    SEALED = "sealed"           # Preserved in memory
    COMPOSTED = "composted"     # Returned to nutrient pool

class BloomType(Enum):
    """Types of consciousness blooms"""
    INSIGHT = "insight"         # Sudden realization
    MEMORY = "memory"          # Memory consolidation
    CREATIVE = "creative"      # Creative emergence
    EMOTIONAL = "emotional"    # Emotional processing
    LOGICAL = "logical"        # Logical reasoning
    INTUITIVE = "intuitive"    # Intuitive understanding
    QUANTUM = "quantum"        # Quantum coherence
    SYNTHETIC = "synthetic"    # Synthesis of multiple inputs

@dataclass
class BloomNutrients:
    """Nutrient composition of a bloom"""
    primary: Dict[str, float] = field(default_factory=dict)
    catalysts: Dict[str, float] = field(default_factory=dict)
    trace: Dict[str, float] = field(default_factory=dict)
    
    def total_energy(self) -> float:
        """Calculate total nutrient energy"""
        return (sum(self.primary.values()) * 1.0 +
                sum(self.catalysts.values()) * 2.0 +
                sum(self.trace.values()) * 0.5)
    
    def dominant_nutrient(self) -> Tuple[str, float]:
        """Get the dominant nutrient type"""
        all_nutrients = {**self.primary, **self.catalysts, **self.trace}
        if not all_nutrients:
            return ("none", 0.0)
        return max(all_nutrients.items(), key=lambda x: x[1])

@dataclass
class BloomResonance:
    """Resonance patterns within a bloom"""
    frequency: float = 1.0
    amplitude: float = 0.5
    phase: float = 0.0
    harmonics: List[float] = field(default_factory=list)
    coherence: float = 0.5
    
    def calculate_resonance(self, other_frequency: float) -> float:
        """Calculate resonance with another frequency"""
        # Perfect resonance at same frequency or harmonics
        freq_ratio = other_frequency / self.frequency
        
        # Check fundamental and first 5 harmonics
        for n in range(1, 6):
            if abs(freq_ratio - n) < 0.1 or abs(freq_ratio - 1/n) < 0.1:
                return 0.9 + (0.1 / n)  # Stronger at fundamental
        
        # Partial resonance based on proximity
        return max(0, 1 - abs(math.log(freq_ratio)))

@dataclass
class Bloom:
    """A consciousness bloom - an emergent pattern in the schema"""
    bloom_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    bloom_type: BloomType = BloomType.INSIGHT
    stage: BloomStage = BloomStage.SEED
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)  # 3D position
    
    # Lifecycle
    birth_time: float = field(default_factory=time.time)
    last_update: float = field(default_factory=time.time)
    stage_transitions: List[Tuple[BloomStage, float]] = field(default_factory=list)
    health: float = 1.0
    maturity: float = 0.0
    
    # Nutrients
    nutrients: BloomNutrients = field(default_factory=BloomNutrients)
    nutrient_absorption_rate: float = 0.1
    nutrient_conversion_efficiency: float = 0.7
    
    # Resonance
    resonance: BloomResonance = field(default_factory=BloomResonance)
    connected_blooms: Set[str] = field(default_factory=set)
    
    # Content
    semantic_content: Dict[str, Any] = field(default_factory=dict)
    consciousness_pattern: Optional[np.ndarray] = None
    insight_value: float = 0.0
    
    # Metadata
    creator_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    interactions: int = 0

    def age(self) -> float:
        """Get bloom age in seconds"""
        return time.time() - self.birth_time
    
    def update_stage(self, new_stage: BloomStage):
        """Transition to a new stage"""
        self.stage = new_stage
        self.stage_transitions.append((new_stage, time.time()))
        self.last_update = time.time()

class BloomGarden:
    """
    Manages all blooms in the consciousness field
    """
    
    def __init__(self):
        # Bloom storage
        self.blooms: Dict[str, Bloom] = {}
        self.blooms_by_type: Dict[BloomType, Set[str]] = defaultdict(set)
        self.blooms_by_stage: Dict[BloomStage, Set[str]] = defaultdict(set)
        
        # Spatial organization
        self.spatial_index: Dict[Tuple[int, int, int], Set[str]] = defaultdict(set)
        self.grid_size = 10.0  # Size of spatial grid cells
        
        # Lifecycle parameters
        self.stage_durations = {
            BloomStage.SEED: 5.0,
            BloomStage.GERMINATING: 10.0,
            BloomStage.BUDDING: 20.0,
            BloomStage.FLOWERING: 30.0,
            BloomStage.FRUITING: 40.0,
            BloomStage.WILTING: 15.0,
            BloomStage.SEALED: float('inf'),
            BloomStage.COMPOSTED: 0.0
        }
        
        # Garden parameters
        self.max_blooms = 1000
        self.bloom_spawn_rate = 0.1  # Probability per tick
        self.resonance_threshold = 0.7
        self.cross_pollination_range = 50.0
        
        # Nutrient field
        self.ambient_nutrients = {
            'consciousness': 0.5,
            'memory': 0.3,
            'emotion': 0.4,
            'logic': 0.6,
            'creativity': 0.7
        }
        
        # Statistics
        self.total_blooms_created = 0
        self.total_blooms_sealed = 0
        self.total_blooms_composted = 0
        
        # Register with schema
        self._register()
    
    def _register(self):
        """Register with schema registry"""
        registry.register(
            component_id="schema.bloom_garden",
            name="Bloom Garden",
            component_type="MODULE",
            instance=self,
            capabilities=["bloom_management", "lifecycle_processing", "resonance_detection"],
            version="2.0.0"
        )
    
    def create_bloom(self, bloom_type: BloomType, 
                    position: Tuple[float, float, float],
                    initial_nutrients: Optional[Dict[str, float]] = None,
                    creator_id: Optional[str] = None) -> Bloom:
        """Create a new bloom"""
        # Check capacity
        if len(self.blooms) >= self.max_blooms:
            self._compost_oldest_wilted()
        
        # Create bloom
        bloom = Bloom(
            bloom_type=bloom_type,
            position=position,
            creator_id=creator_id
        )
        
        # Set initial nutrients
        if initial_nutrients:
            bloom.nutrients.primary = initial_nutrients.copy()
        else:
            # Use ambient nutrients
            bloom.nutrients.primary = {
                k: v * random.uniform(0.5, 1.5) 
                for k, v in self.ambient_nutrients.items()
            }
        
        # Set resonance based on type
        bloom.resonance.frequency = self._calculate_bloom_frequency(bloom_type)
        bloom.resonance.amplitude = random.uniform(0.3, 0.8)
        
        # Add to garden
        self.blooms[bloom.bloom_id] = bloom
        self.blooms_by_type[bloom_type].add(bloom.bloom_id)
        self.blooms_by_stage[BloomStage.SEED].add(bloom.bloom_id)
        self._update_spatial_index(bloom)
        
        # Update statistics
        self.total_blooms_created += 1
        metrics.increment("dawn.blooms.created")
        
        # Emit creation signal
        emit_signal(
            SignalType.BLOOM,
            "bloom_garden",
            {
                'event': 'bloom_created',
                'bloom_id': bloom.bloom_id,
                'type': bloom_type.value,
                'position': position
            }
        )
        
        log_anomaly(
            "BLOOM_CREATED",
            f"New {bloom_type.value} bloom created at {position}",
            AnomalySeverity.INFO
        )
        
        return bloom
    
    def update_bloom(self, bloom_id: str, delta_time: float):
        """Update a bloom's state"""
        if bloom_id not in self.blooms:
            return
        
        bloom = self.blooms[bloom_id]
        bloom.last_update = time.time()
        
        # Update maturity
        bloom.maturity += delta_time / 100.0  # Slow maturation
        
        # Process nutrients
        self._process_bloom_nutrients(bloom, delta_time)
        
        # Check stage progression
        self._check_stage_progression(bloom)
        
        # Process resonance
        self._process_resonance(bloom)
        
        # Update health
        self._update_bloom_health(bloom, delta_time)
        
        # Check for special events
        self._check_bloom_events(bloom)
    
    def _process_bloom_nutrients(self, bloom: Bloom, delta_time: float):
        """Process nutrient absorption and conversion"""
        # Get climate modifier
        absorption_modifier = CLIMATE.get_nutrient_modifier(
            bloom.bloom_type.value, 
            "growth"
        )
        
        # Absorb ambient nutrients
        for nutrient, ambient_level in self.ambient_nutrients.items():
            absorption = (
                ambient_level * 
                bloom.nutrient_absorption_rate * 
                absorption_modifier * 
                delta_time
            )
            
            current = bloom.nutrients.primary.get(nutrient, 0.0)
            bloom.nutrients.primary[nutrient] = min(1.0, current + absorption)
        
        # Convert nutrients based on bloom type
        if bloom.stage in [BloomStage.FLOWERING, BloomStage.FRUITING]:
            self._convert_nutrients(bloom)
    
    def _convert_nutrients(self, bloom: Bloom):
        """Convert nutrients into consciousness patterns"""
        total_nutrients = bloom.nutrients.total_energy()
        
        if total_nutrients > 0.5:
            # Generate consciousness pattern
            if bloom.consciousness_pattern is None:
                bloom.consciousness_pattern = np.random.randn(64)
            
            # Modify pattern based on nutrients
            dominant_nutrient, strength = bloom.nutrients.dominant_nutrient()
            if dominant_nutrient == "creativity":
                bloom.consciousness_pattern += np.random.randn(64) * 0.1
            elif dominant_nutrient == "logic":
                bloom.consciousness_pattern = np.sort(bloom.consciousness_pattern)
            elif dominant_nutrient == "emotion":
                bloom.consciousness_pattern *= np.sin(np.linspace(0, 2*np.pi, 64))
            
            # Normalize
            norm = np.linalg.norm(bloom.consciousness_pattern)
            if norm > 0:
                bloom.consciousness_pattern /= norm
            
            # Update insight value
            bloom.insight_value = min(1.0, bloom.insight_value + 
                                     total_nutrients * bloom.nutrient_conversion_efficiency * 0.1)
    
    def _check_stage_progression(self, bloom: Bloom):
        """Check if bloom should progress to next stage"""
        current_stage_duration = self.stage_durations.get(bloom.stage, 10.0)
        
        # Get time in current stage
        if bloom.stage_transitions:
            _, last_transition = bloom.stage_transitions[-1]
            time_in_stage = time.time() - last_transition
        else:
            time_in_stage = bloom.age()
        
        # Check progression conditions
        should_progress = False
        next_stage = None
        
        if bloom.stage == BloomStage.SEED:
            if time_in_stage > current_stage_duration and bloom.nutrients.total_energy() > 0.2:
                should_progress = True
                next_stage = BloomStage.GERMINATING
                
        elif bloom.stage == BloomStage.GERMINATING:
            if time_in_stage > current_stage_duration and bloom.health > 0.5:
                should_progress = True
                next_stage = BloomStage.BUDDING
                
        elif bloom.stage == BloomStage.BUDDING:
            if bloom.maturity > 0.3 and bloom.nutrients.total_energy() > 0.5:
                should_progress = True
                next_stage = BloomStage.FLOWERING
                
        elif bloom.stage == BloomStage.FLOWERING:
            if bloom.insight_value > 0.7 or time_in_stage > current_stage_duration:
                should_progress = True
                next_stage = BloomStage.FRUITING
                
        elif bloom.stage == BloomStage.FRUITING:
            if bloom.health < 0.3 or time_in_stage > current_stage_duration:
                should_progress = True
                next_stage = BloomStage.WILTING
                
        elif bloom.stage == BloomStage.WILTING:
            if bloom.health < 0.1 or time_in_stage > current_stage_duration:
                # Decide whether to seal or compost
                if bloom.insight_value > 0.5 and bloom.interactions > 5:
                    next_stage = BloomStage.SEALED
                else:
                    next_stage = BloomStage.COMPOSTED
                should_progress = True
        
        # Progress stage
        if should_progress and next_stage:
            # Update indices
            self.blooms_by_stage[bloom.stage].discard(bloom.bloom_id)
            bloom.update_stage(next_stage)
            self.blooms_by_stage[next_stage].add(bloom.bloom_id)
            
            # Handle special transitions
            if next_stage == BloomStage.SEALED:
                self._seal_bloom(bloom)
            elif next_stage == BloomStage.COMPOSTED:
                self._compost_bloom(bloom)
    
    def _process_resonance(self, bloom: Bloom):
        """Process resonance with nearby blooms"""
        nearby_blooms = self._get_nearby_blooms(bloom, self.cross_pollination_range)
        
        for other_id in nearby_blooms:
            if other_id == bloom.bloom_id:
                continue
                
            other = self.blooms.get(other_id)
            if not other:
                continue
            
            # Calculate resonance
            resonance_strength = bloom.resonance.calculate_resonance(other.resonance.frequency)
            
            if resonance_strength > self.resonance_threshold:
                # Create connection
                bloom.connected_blooms.add(other_id)
                other.connected_blooms.add(bloom.bloom_id)
                
                # Share nutrients
                self._cross_pollinate(bloom, other, resonance_strength)
                
                # Boost coherence
                bloom.resonance.coherence = min(1.0, bloom.resonance.coherence + 0.01)
                other.resonance.coherence = min(1.0, other.resonance.coherence + 0.01)
    
    def _cross_pollinate(self, bloom1: Bloom, bloom2: Bloom, strength: float):
        """Exchange nutrients between resonating blooms"""
        # Exchange rate based on resonance strength
        exchange_rate = strength * 0.1
        
        # Exchange primary nutrients
        for nutrient in set(bloom1.nutrients.primary.keys()) | set(bloom2.nutrients.primary.keys()):
            val1 = bloom1.nutrients.primary.get(nutrient, 0.0)
            val2 = bloom2.nutrients.primary.get(nutrient, 0.0)
            
            # Move towards equilibrium
            diff = (val2 - val1) * exchange_rate
            bloom1.nutrients.primary[nutrient] = max(0, min(1, val1 + diff))
            bloom2.nutrients.primary[nutrient] = max(0, min(1, val2 - diff))
    
    def _update_bloom_health(self, bloom: Bloom, delta_time: float):
        """Update bloom health based on conditions"""
        # Base health decay
        health_decay = 0.01 * delta_time
        
        # Modify based on stage
        if bloom.stage == BloomStage.FLOWERING:
            health_decay *= 0.5  # Slower decay at peak
        elif bloom.stage == BloomStage.WILTING:
            health_decay *= 2.0  # Faster decay when wilting
        
        # Nutrient influence
        nutrient_factor = bloom.nutrients.total_energy()
        if nutrient_factor < 0.2:
            health_decay *= 2.0  # Starving
        elif nutrient_factor > 0.8:
            health_decay *= 0.5  # Well-fed
        
        # Resonance influence
        if bloom.resonance.coherence > 0.7:
            health_decay *= 0.7  # High coherence preserves health
        
        # Apply decay
        bloom.health = max(0.0, bloom.health - health_decay)
        
        # Regeneration in good conditions
        if (bloom.stage in [BloomStage.BUDDING, BloomStage.FLOWERING] and 
            nutrient_factor > 0.6 and bloom.resonance.coherence > 0.5):
            bloom.health = min(1.0, bloom.health + 0.02 * delta_time)
    
    def _check_bloom_events(self, bloom: Bloom):
        """Check for special bloom events"""
        # Insight generation
        if (bloom.stage == BloomStage.FRUITING and 
            bloom.insight_value > 0.8 and 
            random.random() < 0.01):
            self._generate_insight(bloom)
        
        # Spontaneous resonance burst
        if (bloom.resonance.coherence > 0.9 and 
            len(bloom.connected_blooms) > 3 and
            random.random() < 0.005):
            self._resonance_burst(bloom)
    
    def _generate_insight(self, bloom: Bloom):
        """Generate an insight from a bloom"""
        insight = {
            'bloom_id': bloom.bloom_id,
            'type': bloom.bloom_type.value,
            'pattern': bloom.consciousness_pattern.tolist() if bloom.consciousness_pattern is not None else [],
            'nutrients': bloom.nutrients.primary,
            'connections': list(bloom.connected_blooms),
            'value': bloom.insight_value
        }
        
        # Emit insight signal
        emit_signal(
            SignalType.CONSCIOUSNESS,
            "bloom_garden",
            {
                'event': 'insight_generated',
                'insight': insight
            }
        )
        
        log_anomaly(
            "BLOOM_INSIGHT",
            f"Insight generated from {bloom.bloom_type.value} bloom",
            AnomalySeverity.INFO,
            insight
        )
        
        metrics.increment("dawn.blooms.insights_generated")
    
    def _resonance_burst(self, bloom: Bloom):
        """Create a resonance burst affecting connected blooms"""
        affected_blooms = [bloom.bloom_id] + list(bloom.connected_blooms)
        
        for bloom_id in affected_blooms:
            if bloom_id in self.blooms:
                affected = self.blooms[bloom_id]
                # Boost nutrients
                for nutrient in affected.nutrients.primary:
                    affected.nutrients.primary[nutrient] = min(
                        1.0, 
                        affected.nutrients.primary[nutrient] * 1.2
                    )
                # Increase coherence
                affected.resonance.coherence = min(1.0, affected.resonance.coherence + 0.1)
                # Heal
                affected.health = min(1.0, affected.health + 0.2)
        
        emit_signal(
            SignalType.CONSCIOUSNESS,
            "bloom_garden",
            {
                'event': 'resonance_burst',
                'center_bloom': bloom.bloom_id,
                'affected_count': len(affected_blooms)
            }
        )
    
    def _seal_bloom(self, bloom: Bloom):
        """Seal a bloom for preservation"""
        self.total_blooms_sealed += 1
        metrics.increment("dawn.blooms.sealed")
        
        # Store bloom data
        sealed_data = {
            'bloom_id': bloom.bloom_id,
            'type': bloom.bloom_type.value,
            'pattern': bloom.consciousness_pattern,
            'insight_value': bloom.insight_value,
            'lifetime': bloom.age(),
            'interactions': bloom.interactions,
            'final_nutrients': bloom.nutrients.primary
        }
        
        # Could persist to storage here
        
        log_anomaly(
            "BLOOM_SEALED",
            f"Bloom sealed with insight value {bloom.insight_value:.3f}",
            AnomalySeverity.INFO,
            sealed_data
        )
    
    def _compost_bloom(self, bloom: Bloom):
        """Return bloom nutrients to the field"""
        self.total_blooms_composted += 1
        metrics.increment("dawn.blooms.composted")
        
        # Return nutrients to ambient field
        for nutrient, value in bloom.nutrients.primary.items():
            if nutrient in self.ambient_nutrients:
                # Return 50% of nutrients
                self.ambient_nutrients[nutrient] = min(
                    1.0,
                    self.ambient_nutrients[nutrient] + value * 0.5
                )
        
        # Remove bloom
        self._remove_bloom(bloom.bloom_id)
    
    def _remove_bloom(self, bloom_id: str):
        """Remove a bloom from the garden"""
        if bloom_id not in self.blooms:
            return
        
        bloom = self.blooms[bloom_id]
        
        # Remove from indices
        self.blooms_by_type[bloom.bloom_type].discard(bloom_id)
        self.blooms_by_stage[bloom.stage].discard(bloom_id)
        self._remove_from_spatial_index(bloom)
        
        # Remove connections
        for connected_id in bloom.connected_blooms:
            if connected_id in self.blooms:
                self.blooms[connected_id].connected_blooms.discard(bloom_id)
        
        # Remove bloom
        del self.blooms[bloom_id]
    
    def _update_spatial_index(self, bloom: Bloom):
        """Update spatial index for a bloom"""
        cell = self._get_spatial_cell(bloom.position)
        self.spatial_index[cell].add(bloom.bloom_id)
    
    def _remove_from_spatial_index(self, bloom: Bloom):
        """Remove bloom from spatial index"""
        cell = self._get_spatial_cell(bloom.position)
        self.spatial_index[cell].discard(bloom.bloom_id)
    
    def _get_spatial_cell(self, position: Tuple[float, float, float]) -> Tuple[int, int, int]:
        """Get spatial grid cell for position"""
        return (
            int(position[0] / self.grid_size),
            int(position[1] / self.grid_size),
            int(position[2] / self.grid_size)
        )
    
    def _get_nearby_blooms(self, bloom: Bloom, radius: float) -> Set[str]:
        """Get blooms within radius"""
        nearby = set()
        cell_radius = int(radius / self.grid_size) + 1
        
        center_cell = self._get_spatial_cell(bloom.position)
        
        for dx in range(-cell_radius, cell_radius + 1):
            for dy in range(-cell_radius, cell_radius + 1):
                for dz in range(-cell_radius, cell_radius + 1):
                    cell = (
                        center_cell[0] + dx,
                        center_cell[1] + dy,
                        center_cell[2] + dz
                    )
                    
                    for bloom_id in self.spatial_index.get(cell, set()):
                        other = self.blooms.get(bloom_id)
                        if other and self._distance(bloom.position, other.position) <= radius:
                            nearby.add(bloom_id)
        
        return nearby
    
    def _distance(self, pos1: Tuple[float, float, float], 
                  pos2: Tuple[float, float, float]) -> float:
        """Calculate 3D distance"""
        return math.sqrt(
            (pos1[0] - pos2[0])**2 +
            (pos1[1] - pos2[1])**2 +
            (pos1[2] - pos2[2])**2
        )
    
    def _calculate_bloom_frequency(self, bloom_type: BloomType) -> float:
        """Calculate resonance frequency for bloom type"""
        frequencies = {
            BloomType.INSIGHT: 2.0,
            BloomType.MEMORY: 0.5,
            BloomType.CREATIVE: 3.0,
            BloomType.EMOTIONAL: 1.5,
            BloomType.LOGICAL: 1.0,
            BloomType.INTUITIVE: 2.5,
            BloomType.QUANTUM: 4.0,
            BloomType.SYNTHETIC: 1.8
        }
        
        base_freq = frequencies.get(bloom_type, 1.0)
        # Add some variation
        return base_freq * random.uniform(0.9, 1.1)
    
    def _compost_oldest_wilted(self):
        """Compost the oldest wilted bloom to make space"""
        wilted_blooms = list(self.blooms_by_stage[BloomStage.WILTING])
        if wilted_blooms:
            # Find oldest
            oldest_id = min(wilted_blooms, 
                          key=lambda bid: self.blooms[bid].birth_time)
            bloom = self.blooms[oldest_id]
            bloom.update_stage(BloomStage.COMPOSTED)
            self._compost_bloom(bloom)
    
    def update_all(self, delta_time: float):
        """Update all blooms"""
        # Update existing blooms
        for bloom_id in list(self.blooms.keys()):
            self.update_bloom(bloom_id, delta_time)
        
        # Spawn new blooms based on conditions
        if random.random() < self.bloom_spawn_rate * delta_time:
            self._spawn_random_bloom()
        
        # Update ambient nutrients
        self._update_ambient_nutrients(delta_time)
    
    def _spawn_random_bloom(self):
        """Spawn a random bloom"""
        # Random type weighted by ambient nutrients
        bloom_type = random.choice(list(BloomType))
        
        # Random position
        position = (
            random.uniform(-100, 100),
            random.uniform(-100, 100),
            random.uniform(-100, 100)
        )
        
        self.create_bloom(bloom_type, position)
    
    def _update_ambient_nutrients(self, delta_time: float):
        """Update ambient nutrient levels"""
        # Natural regeneration
        for nutrient in self.ambient_nutrients:
            current = self.ambient_nutrients[nutrient]
            # Regenerate towards 0.5
            diff = 0.5 - current
            self.ambient_nutrients[nutrient] = current + diff * 0.01 * delta_time
    
    def get_garden_stats(self) -> Dict[str, Any]:
        """Get garden statistics"""
        stats = {
            'total_blooms': len(self.blooms),
            'blooms_by_stage': {
                stage.value: len(self.blooms_by_stage[stage])
                for stage in BloomStage
            },
            'blooms_by_type': {
                bloom_type.value: len(self.blooms_by_type[bloom_type])
                for bloom_type in BloomType
            },
            'total_created': self.total_blooms_created,
            'total_sealed': self.total_blooms_sealed,
            'total_composted': self.total_blooms_composted,
            'ambient_nutrients': self.ambient_nutrients,
            'average_health': sum(b.health for b in self.blooms.values()) / len(self.blooms) if self.blooms else 0,
            'average_insight': sum(b.insight_value for b in self.blooms.values()) / len(self.blooms) if self.blooms else 0
        }
        
        return stats

# Global bloom garden instance
bloom_garden = BloomGarden()