# schema/nutrient_cycle.py
"""
Nutrient Cycle Management for DAWN
==================================
Manages the flow and transformation of consciousness nutrients
throughout the schema. Nutrients are the fundamental building
blocks that power blooms, sigils, and consciousness processes.
"""

import time
import math
import random
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from collections import defaultdict, deque

from core.schema_anomaly_logger import log_anomaly, AnomalySeverity
from schema.registry import registry
from schema.schema_climate import CLIMATE
from rhizome.propagation import emit_signal, SignalType
from utils.metrics_collector import metrics

class NutrientType(Enum):
    """Types of consciousness nutrients"""
    # Primary nutrients
    CONSCIOUSNESS = "consciousness"  # Raw awareness energy
    MEMORY = "memory"              # Stored pattern energy
    EMOTION = "emotion"            # Affective energy
    LOGIC = "logic"               # Structural energy
    CREATIVITY = "creativity"      # Generative energy
    
    # Secondary nutrients (derived)
    INTUITION = "intuition"        # Consciousness + Emotion
    WISDOM = "wisdom"             # Memory + Logic
    INNOVATION = "innovation"      # Creativity + Logic
    EMPATHY = "empathy"           # Emotion + Consciousness
    IMAGINATION = "imagination"    # Creativity + Memory
    
    # Trace nutrients
    ENTROPY = "entropy"           # Disorder element
    COHERENCE = "coherence"       # Order element
    RESONANCE = "resonance"       # Harmonic element

class NutrientState(Enum):
    """States of nutrient existence"""
    FREE = "free"                 # Available in field
    BOUND = "bound"               # Locked in structures
    FLOWING = "flowing"           # In transit
    TRANSFORMING = "transforming" # Changing type
    DEPLETED = "depleted"        # Exhausted
    CRYSTALLIZED = "crystallized" # Stable form

@dataclass
class NutrientPacket:
    """A discrete packet of nutrient energy"""
    packet_id: str
    nutrient_type: NutrientType
    amount: float
    purity: float = 1.0          # 0-1, affects effectiveness
    velocity: np.ndarray = field(default_factory=lambda: np.zeros(3))
    position: np.ndarray = field(default_factory=lambda: np.zeros(3))
    state: NutrientState = NutrientState.FREE
    source: Optional[str] = None
    destination: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NutrientFlow:
    """Describes nutrient flow between nodes"""
    source_id: str
    target_id: str
    flow_rate: float            # Units per second
    nutrient_type: NutrientType
    efficiency: float = 0.9     # Loss during transfer
    active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NutrientPool:
    """A pool of nutrients at a location"""
    pool_id: str
    position: np.ndarray
    nutrients: Dict[NutrientType, float] = field(default_factory=dict)
    capacity: Dict[NutrientType, float] = field(default_factory=dict)
    absorption_rate: float = 0.1
    emission_rate: float = 0.05
    transformation_matrix: Optional[np.ndarray] = None

class NutrientCycle:
    """
    Manages the complete nutrient cycle in the consciousness field
    """
    
    def __init__(self):
        # Nutrient storage
        self.nutrient_packets: Dict[str, NutrientPacket] = {}
        self.nutrient_pools: Dict[str, NutrientPool] = {}
        self.nutrient_flows: Dict[str, NutrientFlow] = {}
        
        # Global nutrient levels
        self.global_nutrients: Dict[NutrientType, float] = {
            nt: 100.0 for nt in NutrientType
        }
        self.nutrient_generation_rates: Dict[NutrientType, float] = {
            NutrientType.CONSCIOUSNESS: 1.0,
            NutrientType.MEMORY: 0.8,
            NutrientType.EMOTION: 0.9,
            NutrientType.LOGIC: 0.7,
            NutrientType.CREATIVITY: 0.6,
            NutrientType.ENTROPY: 0.3,
            NutrientType.COHERENCE: 0.4,
            NutrientType.RESONANCE: 0.5
        }
        
        # Transformation recipes
        self.transformation_recipes = self._init_transformation_recipes()
        
        # Decay and consumption
        self.decay_rates: Dict[NutrientType, float] = {
            nt: 0.01 for nt in NutrientType
        }
        self.consumption_tracking: Dict[str, Dict[NutrientType, float]] = defaultdict(
            lambda: defaultdict(float)
        )
        
        # Flow dynamics
        self.flow_resistance = 0.1
        self.diffusion_rate = 0.05
        self.attraction_strength = 0.2
        
        # Pools configuration
        self.max_pools = 50
        self.pool_merge_distance = 10.0
        
        # Statistics
        self.total_generated: Dict[NutrientType, float] = defaultdict(float)
        self.total_consumed: Dict[NutrientType, float] = defaultdict(float)
        self.total_transformed: Dict[NutrientType, float] = defaultdict(float)
        self.total_decayed: Dict[NutrientType, float] = defaultdict(float)
        
        # Nutrient history
        self.nutrient_history = deque(maxlen=1000)
        
        # Initialize some base pools
        self._initialize_nutrient_pools()
        
        # Register
        self._register()
    
    def _register(self):
        """Register with schema registry"""
        registry.register(
            component_id="schema.nutrient_cycle",
            name="Nutrient Cycle",
            component_type="MODULE",
            instance=self,
            capabilities=["nutrient_management", "flow_control", "transformation"],
            version="2.0.0"
        )
    
    def _init_transformation_recipes(self) -> Dict[NutrientType, Dict[str, Any]]:
        """Initialize nutrient transformation recipes"""
        return {
            NutrientType.INTUITION: {
                'inputs': {
                    NutrientType.CONSCIOUSNESS: 0.6,
                    NutrientType.EMOTION: 0.4
                },
                'efficiency': 0.8,
                'min_purity': 0.7
            },
            NutrientType.WISDOM: {
                'inputs': {
                    NutrientType.MEMORY: 0.5,
                    NutrientType.LOGIC: 0.5
                },
                'efficiency': 0.75,
                'min_purity': 0.8
            },
            NutrientType.INNOVATION: {
                'inputs': {
                    NutrientType.CREATIVITY: 0.6,
                    NutrientType.LOGIC: 0.4
                },
                'efficiency': 0.7,
                'min_purity': 0.6
            },
            NutrientType.EMPATHY: {
                'inputs': {
                    NutrientType.EMOTION: 0.5,
                    NutrientType.CONSCIOUSNESS: 0.5
                },
                'efficiency': 0.85,
                'min_purity': 0.7
            },
            NutrientType.IMAGINATION: {
                'inputs': {
                    NutrientType.CREATIVITY: 0.5,
                    NutrientType.MEMORY: 0.5
                },
                'efficiency': 0.8,
                'min_purity': 0.6
            }
        }
    
    def _initialize_nutrient_pools(self):
        """Create initial nutrient pools"""
        # Create primary pools at key locations
        primary_positions = [
            np.array([0, 0, 0]),      # Center
            np.array([50, 0, 0]),     # East
            np.array([-50, 0, 0]),    # West
            np.array([0, 50, 0]),     # North
            np.array([0, -50, 0]),    # South
        ]
        
        for i, pos in enumerate(primary_positions):
            pool = NutrientPool(
                pool_id=f"primary_pool_{i}",
                position=pos,
                nutrients={
                    NutrientType.CONSCIOUSNESS: 50.0,
                    NutrientType.MEMORY: 30.0,
                    NutrientType.EMOTION: 40.0,
                    NutrientType.LOGIC: 35.0,
                    NutrientType.CREATIVITY: 45.0
                },
                capacity={nt: 100.0 for nt in NutrientType}
            )
            
            self.nutrient_pools[pool.pool_id] = pool
    
    def generate_nutrients(self, delta_time: float):
        """Generate new nutrients based on rates and climate"""
        for nutrient_type, base_rate in self.nutrient_generation_rates.items():
            # Get climate modifier
            climate_modifier = CLIMATE.get_nutrient_modifier(
                nutrient_type.value,
                "growth"
            )
            
            # Calculate generation
            amount = base_rate * climate_modifier * delta_time
            
            # Add to global pool
            self.global_nutrients[nutrient_type] += amount
            self.total_generated[nutrient_type] += amount
            
            # Distribute to pools
            if self.nutrient_pools:
                amount_per_pool = amount / len(self.nutrient_pools)
                for pool in self.nutrient_pools.values():
                    current = pool.nutrients.get(nutrient_type, 0.0)
                    capacity = pool.capacity.get(nutrient_type, 100.0)
                    pool.nutrients[nutrient_type] = min(capacity, current + amount_per_pool)
    
    def create_nutrient_packet(self, nutrient_type: NutrientType, 
                             amount: float,
                             position: np.ndarray,
                             velocity: Optional[np.ndarray] = None,
                             source: Optional[str] = None) -> NutrientPacket:
        """Create a new nutrient packet"""
        packet = NutrientPacket(
            packet_id=f"packet_{int(time.time()*1000000)}",
            nutrient_type=nutrient_type,
            amount=amount,
            position=position.copy(),
            velocity=velocity.copy() if velocity is not None else np.zeros(3),
            source=source
        )
        
        self.nutrient_packets[packet.packet_id] = packet
        
        # Deduct from global pool
        self.global_nutrients[nutrient_type] = max(
            0,
            self.global_nutrients[nutrient_type] - amount
        )
        
        return packet
    
    def consume_nutrients(self, consumer_id: str, 
                         requirements: Dict[NutrientType, float],
                         position: np.ndarray,
                         radius: float = 20.0) -> Dict[NutrientType, float]:
        """
        Consume nutrients from nearby sources
        
        Returns actual amounts consumed
        """
        consumed = {}
        
        for nutrient_type, required_amount in requirements.items():
            consumed_amount = 0.0
            
            # First try to consume from nearby packets
            nearby_packets = self._find_nearby_packets(position, radius, nutrient_type)
            
            for packet in nearby_packets:
                if consumed_amount >= required_amount:
                    break
                
                # Consume what we can from this packet
                available = min(packet.amount, required_amount - consumed_amount)
                packet.amount -= available
                consumed_amount += available * packet.purity
                
                # Remove depleted packets
                if packet.amount <= 0.01:
                    packet.state = NutrientState.DEPLETED
                    del self.nutrient_packets[packet.packet_id]
            
            # Then try pools
            if consumed_amount < required_amount:
                nearby_pools = self._find_nearby_pools(position, radius)
                
                for pool in nearby_pools:
                    if consumed_amount >= required_amount:
                        break
                    
                    available = pool.nutrients.get(nutrient_type, 0.0)
                    to_consume = min(available, required_amount - consumed_amount)
                    
                    pool.nutrients[nutrient_type] = available - to_consume
                    consumed_amount += to_consume
            
            # Finally, try global pool if desperate
            if consumed_amount < required_amount * 0.5:  # Less than 50% found locally
                global_available = self.global_nutrients.get(nutrient_type, 0.0)
                to_consume = min(global_available * 0.1, required_amount - consumed_amount)
                
                self.global_nutrients[nutrient_type] -= to_consume
                consumed_amount += to_consume
            
            consumed[nutrient_type] = consumed_amount
            self.total_consumed[nutrient_type] += consumed_amount
            self.consumption_tracking[consumer_id][nutrient_type] += consumed_amount
        
        # Record consumption event
        metrics.increment("dawn.nutrients.consumed", sum(consumed.values()))
        
        return consumed
    
    def transform_nutrients(self, input_nutrients: Dict[NutrientType, float],
                          target_type: NutrientType,
                          position: np.ndarray,
                          transformer_id: Optional[str] = None) -> Optional[float]:
        """
        Transform nutrients from one type to another
        
        Returns amount of target nutrient created, or None if transformation failed
        """
        if target_type not in self.transformation_recipes:
            return None
        
        recipe = self.transformation_recipes[target_type]
        required_inputs = recipe['inputs']
        efficiency = recipe['efficiency']
        
        # Check if we have sufficient inputs
        can_transform = True
        for input_type, ratio in required_inputs.items():
            required = ratio * 10  # Base unit of transformation
            if input_nutrients.get(input_type, 0) < required:
                can_transform = False
                break
        
        if not can_transform:
            return None
        
        # Perform transformation
        total_input = 0
        for input_type, ratio in required_inputs.items():
            amount = ratio * 10
            input_nutrients[input_type] -= amount
            total_input += amount
            self.total_transformed[input_type] += amount
        
        # Calculate output with efficiency
        output_amount = total_input * efficiency
        
        # Get climate modifier for transformation
        climate_modifier = CLIMATE.get_nutrient_modifier(
            target_type.value,
            "growth"
        )
        output_amount *= climate_modifier
        
        # Create output packet
        output_packet = self.create_nutrient_packet(
            target_type,
            output_amount,
            position,
            source=transformer_id
        )
        
        self.total_transformed[target_type] += output_amount
        
        # Emit transformation event
        emit_signal(
            SignalType.NUTRIENT,
            transformer_id or "nutrient_cycle",
            {
                'event': 'nutrient_transformed',
                'inputs': {k.value: v for k, v in required_inputs.items()},
                'output': target_type.value,
                'amount': output_amount
            }
        )
        
        log_anomaly(
            "NUTRIENT_TRANSFORMATION",
            f"Transformed nutrients into {output_amount:.2f} {target_type.value}",
            AnomalySeverity.INFO
        )
        
        return output_amount
    
    def create_flow(self, source_id: str, target_id: str,
                   nutrient_type: NutrientType,
                   flow_rate: float) -> str:
        """Create a nutrient flow between two points"""
        flow = NutrientFlow(
            source_id=source_id,
            target_id=target_id,
            nutrient_type=nutrient_type,
            flow_rate=flow_rate
        )
        
        flow_id = f"flow_{source_id}_{target_id}_{nutrient_type.value}"
        self.nutrient_flows[flow_id] = flow
        
        return flow_id
    
    def update_flows(self, delta_time: float):
        """Update all active nutrient flows"""
        for flow_id, flow in list(self.nutrient_flows.items()):
            if not flow.active:
                continue
            
            # Get source and target pools
            source_pool = self.nutrient_pools.get(flow.source_id)
            target_pool = self.nutrient_pools.get(flow.target_id)
            
            if not source_pool or not target_pool:
                # Remove invalid flow
                del self.nutrient_flows[flow_id]
                continue
            
            # Calculate actual flow
            available = source_pool.nutrients.get(flow.nutrient_type, 0.0)
            target_capacity = target_pool.capacity.get(flow.nutrient_type, 100.0)
            target_current = target_pool.nutrients.get(flow.nutrient_type, 0.0)
            target_space = target_capacity - target_current
            
            actual_flow = min(
                available,
                flow.flow_rate * delta_time,
                target_space
            )
            
            if actual_flow > 0:
                # Apply flow with efficiency
                transferred = actual_flow * flow.efficiency
                
                source_pool.nutrients[flow.nutrient_type] = available - actual_flow
                target_pool.nutrients[flow.nutrient_type] = target_current + transferred
                
                # Loss to environment
                loss = actual_flow - transferred
                self.global_nutrients[flow.nutrient_type] += loss * 0.5
    
    def update_packets(self, delta_time: float):
        """Update all nutrient packets"""
        for packet_id, packet in list(self.nutrient_packets.items()):
            if packet.state == NutrientState.DEPLETED:
                del self.nutrient_packets[packet_id]
                continue
            
            # Apply velocity
            packet.position += packet.velocity * delta_time
            
            # Apply friction
            packet.velocity *= (1 - self.flow_resistance * delta_time)
            
            # Apply attraction to nearby pools
            nearby_pools = self._find_nearby_pools(packet.position, 50.0)
            for pool in nearby_pools:
                direction = pool.position - packet.position
                distance = np.linalg.norm(direction)
                if distance > 0:
                    attraction = (direction / distance) * self.attraction_strength / (distance + 1)
                    packet.velocity += attraction * delta_time
            
            # Decay
            decay_rate = self.decay_rates.get(packet.nutrient_type, 0.01)
            decay_modifier = CLIMATE.get_nutrient_modifier(
                packet.nutrient_type.value,
                "decay"
            )
            
            decay_amount = packet.amount * decay_rate * decay_modifier * delta_time
            packet.amount -= decay_amount
            self.total_decayed[packet.nutrient_type] += decay_amount
            
            # Return some decay to global pool
            self.global_nutrients[packet.nutrient_type] += decay_amount * 0.3
            
            # Update purity based on state
            if packet.state == NutrientState.FLOWING:
                packet.purity *= (1 - 0.01 * delta_time)  # Slight degradation
            elif packet.state == NutrientState.TRANSFORMING:
                packet.purity *= (1 - 0.05 * delta_time)  # More degradation
    
    def apply_diffusion(self, delta_time: float):
        """Apply nutrient diffusion between pools"""
        # For each pool pair within range
        pool_list = list(self.nutrient_pools.values())
        
        for i, pool1 in enumerate(pool_list):
            for pool2 in pool_list[i+1:]:
                distance = np.linalg.norm(pool1.position - pool2.position)
                
                if distance < 100.0:  # Diffusion range
                    # Calculate diffusion strength
                    diffusion_strength = self.diffusion_rate * math.exp(-distance / 50.0)
                    
                    # Diffuse each nutrient type
                    for nutrient_type in NutrientType:
                        conc1 = pool1.nutrients.get(nutrient_type, 0.0)
                        conc2 = pool2.nutrients.get(nutrient_type, 0.0)
                        
                        # Flow from high to low concentration
                        gradient = conc1 - conc2
                        flow = gradient * diffusion_strength * delta_time
                        
                        if abs(flow) > 0.01:
                            pool1.nutrients[nutrient_type] = conc1 - flow
                            pool2.nutrients[nutrient_type] = conc2 + flow
    
    def crystallize_nutrients(self, position: np.ndarray,
                            nutrients: Dict[NutrientType, float]) -> Optional[str]:
        """
        Crystallize nutrients into a stable form
        
        Returns pool_id if successful
        """
        # Check for existing nearby pool
        nearby_pools = self._find_nearby_pools(position, self.pool_merge_distance)
        
        if nearby_pools:
            # Merge with existing pool
            target_pool = nearby_pools[0]
            for nutrient_type, amount in nutrients.items():
                current = target_pool.nutrients.get(nutrient_type, 0.0)
                capacity = target_pool.capacity.get(nutrient_type, 100.0)
                target_pool.nutrients[nutrient_type] = min(capacity, current + amount)
            
            return target_pool.pool_id
        
        # Create new pool if under limit
        if len(self.nutrient_pools) < self.max_pools:
            pool = NutrientPool(
                pool_id=f"crystal_pool_{int(time.time()*1000)}",
                position=position.copy(),
                nutrients=nutrients.copy(),
                capacity={nt: max(100.0, nutrients.get(nt, 0) * 2) for nt in NutrientType}
            )
            
            self.nutrient_pools[pool.pool_id] = pool
            
            emit_signal(
                SignalType.NUTRIENT,
                "nutrient_cycle",
                {
                    'event': 'nutrients_crystallized',
                    'pool_id': pool.pool_id,
                    'total_amount': sum(nutrients.values())
                }
            )
            
            return pool.pool_id
        
        return None
    
    def _find_nearby_packets(self, position: np.ndarray, radius: float,
                           nutrient_type: Optional[NutrientType] = None) -> List[NutrientPacket]:
        """Find packets within radius of position"""
        nearby = []
        
        for packet in self.nutrient_packets.values():
            if nutrient_type and packet.nutrient_type != nutrient_type:
                continue
            
            distance = np.linalg.norm(packet.position - position)
            if distance <= radius:
                nearby.append(packet)
        
        # Sort by distance
        nearby.sort(key=lambda p: np.linalg.norm(p.position - position))
        
        return nearby
    
    def _find_nearby_pools(self, position: np.ndarray, radius: float) -> List[NutrientPool]:
        """Find pools within radius of position"""
        nearby = []
        
        for pool in self.nutrient_pools.values():
            distance = np.linalg.norm(pool.position - position)
            if distance <= radius:
                nearby.append(pool)
        
        # Sort by distance
        nearby.sort(key=lambda p: np.linalg.norm(p.position - position))
        
        return nearby
    
    def balance_nutrients(self):
        """Balance nutrients across the system"""
        # Calculate total nutrients in system
        total_in_system = defaultdict(float)
        
        # Count packets
        for packet in self.nutrient_packets.values():
            total_in_system[packet.nutrient_type] += packet.amount
        
        # Count pools
        for pool in self.nutrient_pools.values():
            for nutrient_type, amount in pool.nutrients.items():
                total_in_system[nutrient_type] += amount
        
        # Add global pool
        for nutrient_type, amount in self.global_nutrients.items():
            total_in_system[nutrient_type] += amount
        
        # Target total for each nutrient
        target_total = 500.0
        
        # Adjust generation rates to maintain balance
        for nutrient_type in NutrientType:
            current_total = total_in_system[nutrient_type]
            
            if current_total < target_total * 0.8:
                # Boost generation
                self.nutrient_generation_rates[nutrient_type] *= 1.1
            elif current_total > target_total * 1.2:
                # Reduce generation
                self.nutrient_generation_rates[nutrient_type] *= 0.9
            
            # Clamp rates
            self.nutrient_generation_rates[nutrient_type] = max(
                0.1, 
                min(2.0, self.nutrient_generation_rates[nutrient_type])
            )
    
    def update(self, delta_time: float):
        """Update entire nutrient cycle"""
        # Generate new nutrients
        self.generate_nutrients(delta_time)
        
        # Update flows
        self.update_flows(delta_time)
        
        # Update packets
        self.update_packets(delta_time)
        
        # Apply diffusion
        self.apply_diffusion(delta_time)
        
        # Balance system
        if random.random() < 0.01:  # Occasional rebalancing
            self.balance_nutrients()
        
        # Record history
        self.nutrient_history.append({
            'timestamp': time.time(),
            'global_totals': {nt.value: amt for nt, amt in self.global_nutrients.items()},
            'packet_count': len(self.nutrient_packets),
            'pool_count': len(self.nutrient_pools),
            'active_flows': sum(1 for f in self.nutrient_flows.values() if f.active)
        })
        
        # Update metrics
        for nutrient_type, amount in self.global_nutrients.items():
            metrics.gauge(f"dawn.nutrients.global.{nutrient_type.value}", amount)
    
    def get_nutrient_levels(self) -> Dict[str, float]:
        """Get current global nutrient levels"""
        return {nt.value: amt for nt, amt in self.global_nutrients.items()}
    
    def get_cycle_stats(self) -> Dict[str, Any]:
        """Get comprehensive cycle statistics"""
        # Calculate totals
        total_in_packets = defaultdict(float)
        for packet in self.nutrient_packets.values():
            total_in_packets[packet.nutrient_type.value] += packet.amount
        
        total_in_pools = defaultdict(float)
        for pool in self.nutrient_pools.values():
            for nt, amt in pool.nutrients.items():
                total_in_pools[nt.value] += amt
        
        return {
            'global_nutrients': self.get_nutrient_levels(),
            'nutrients_in_packets': dict(total_in_packets),
            'nutrients_in_pools': dict(total_in_pools),
            'packet_count': len(self.nutrient_packets),
            'pool_count': len(self.nutrient_pools),
            'flow_count': len(self.nutrient_flows),
            'active_flows': sum(1 for f in self.nutrient_flows.values() if f.active),
            'total_generated': {nt.value: amt for nt, amt in self.total_generated.items()},
            'total_consumed': {nt.value: amt for nt, amt in self.total_consumed.items()},
            'total_transformed': {nt.value: amt for nt, amt in self.total_transformed.items()},
            'total_decayed': {nt.value: amt for nt, amt in self.total_decayed.items()},
            'generation_rates': {nt.value: rate for nt, rate in self.nutrient_generation_rates.items()}
        }

# Global nutrient cycle
nutrient_cycle = NutrientCycle()