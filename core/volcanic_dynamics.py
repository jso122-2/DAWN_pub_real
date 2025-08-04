#!/usr/bin/env python3
"""
DAWN Volcanic Pressure Dynamics - Cognitive State Metaphor System
================================================================

Models DAWN's cognitive state using volcanic dynamics metaphors:

VOLCANIC COMPONENTS:
- Ash = Residue of prior processing (completed thoughts, memory fragments)
- Ignition = Fresh semantic burst detection (new ideas, insights)
- Pressure Zones = Drift buildup pre-rebloom (cognitive tension)
- Eruption = Full cascade with sigil trigger (creative breakthrough)

PRESSURE DYNAMICS:
- Thermal pressure from P = Bσ² formula integration
- Magma chamber = accumulating cognitive pressure
- Lava flows = sustained thought streams
- Volcanic winter = post-eruption cooling period

ERUPTION TYPES:
- Gentle Effusion = gradual thought release (reflection)
- Explosive Burst = sudden insight (rebloom)
- Pyroclastic Flow = rapid sigil cascade (creative flow)
- Dome Collapse = pressure relief (system stabilization)

The volcanic metaphor provides intuitive understanding of DAWN's
cognitive pressure cycles and enables predictive eruption management.
"""

import time
import math
import logging
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple, Callable
from enum import Enum
from collections import deque
from pathlib import Path
import json

# Integration with existing systems
try:
    from core.cognitive_formulas import get_dawn_formula_engine
    from core.schema_health_monitor import get_schema_health_monitor
    from core.platonic_pigment import get_platonic_pigment_map
    from core.tracer_ecosystem import get_tracer_manager
    DAWN_SYSTEMS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"DAWN systems not available for Volcanic Dynamics: {e}")
    DAWN_SYSTEMS_AVAILABLE = False

logger = logging.getLogger("volcanic_dynamics")

class VolcanicState(Enum):
    """Volcanic system states"""
    DORMANT = "DORMANT"                 # Low activity, cooling
    BUILDING = "BUILDING"               # Pressure accumulating
    UNSTABLE = "UNSTABLE"              # Near eruption threshold
    ERUPTING = "ERUPTING"              # Active eruption
    FLOWING = "FLOWING"                # Sustained lava flow
    COOLING = "COOLING"                # Post-eruption cooldown
    WINTER = "WINTER"                  # Extended cooling period

class EruptionType(Enum):
    """Types of volcanic eruptions"""
    GENTLE_EFFUSION = "GENTLE_EFFUSION"      # Gradual thought release
    EXPLOSIVE_BURST = "EXPLOSIVE_BURST"      # Sudden insight
    PYROCLASTIC_FLOW = "PYROCLASTIC_FLOW"   # Rapid sigil cascade
    DOME_COLLAPSE = "DOME_COLLAPSE"         # Pressure relief
    FISSURE_VENT = "FISSURE_VENT"          # Multiple small outlets

class IgnitionLevel(Enum):
    """Semantic ignition intensity levels"""
    EMBER = "EMBER"                    # Minimal spark
    FLAME = "FLAME"                    # Growing ignition
    FIRE = "FIRE"                     # Strong ignition
    INFERNO = "INFERNO"               # Maximum ignition

@dataclass
class AshDeposit:
    """Residue from prior cognitive processing"""
    deposit_id: str
    timestamp: float
    ash_type: str  # "reflection", "memory", "thought", "sigil"
    ash_volume: float  # Amount of residue
    composition: Dict[str, float]  # What the ash contains
    decay_rate: float  # How quickly ash settles/clears
    temperature: float  # Residual heat in ash
    mineral_content: Dict[str, float]  # Useful elements for future processing

@dataclass
class IgnitionEvent:
    """Fresh semantic burst detection"""
    ignition_id: str
    timestamp: float
    ignition_level: IgnitionLevel
    semantic_burst: str  # Content of the burst
    ignition_source: str  # What triggered it
    intensity: float  # 0.0-1.0 ignition strength
    spread_rate: float  # How quickly ignition spreads
    fuel_available: float  # Available cognitive fuel
    temperature_rise: float  # Temperature increase from ignition

@dataclass
class PressureZone:
    """Cognitive pressure accumulation zone"""
    zone_id: str
    zone_type: str  # "drift", "rebloom", "reflection", "processing"
    pressure_level: float  # 0.0-1.0 pressure intensity
    temperature: float  # Zone temperature
    volatility: float  # How unstable the zone is
    buildup_rate: float  # How quickly pressure accumulates
    relief_threshold: float  # Pressure level that triggers release
    connections: List[str]  # Connected pressure zones
    timestamp: float

@dataclass
class VolcanicEruption:
    """Complete eruption event record"""
    eruption_id: str
    timestamp: float
    eruption_type: EruptionType
    trigger_pressure: float  # Pressure that triggered eruption
    peak_intensity: float  # Maximum eruption intensity
    duration: float  # How long eruption lasted
    ash_produced: float  # Amount of ash generated
    lava_volume: float  # Volume of cognitive flow
    affected_zones: List[str]  # Pressure zones involved
    sigil_cascade: List[str]  # Sigils triggered during eruption
    pigment_release: Dict[str, float]  # Pigment intensity changes
    cooling_period: float  # Required cooling time
    aftermath_state: Dict[str, Any]  # Post-eruption system state

class VolcanicDynamicsSystem:
    """
    Volcanic Pressure Dynamics System
    
    Models DAWN's cognitive state using volcanic metaphors and
    manages pressure cycles, eruptions, and thermal dynamics.
    """
    
    def __init__(self):
        """Initialize the Volcanic Dynamics system"""
        
        # Volcanic state
        self.current_state = VolcanicState.DORMANT
        self.magma_chamber_pressure = 0.0  # 0.0-1.0
        self.thermal_temperature = 0.3  # Base temperature
        self.volatile_content = 0.5  # How explosive eruptions can be
        
        # Ash management
        self.ash_deposits: List[AshDeposit] = []
        self.total_ash_volume = 0.0
        self.ash_clearing_rate = 0.05  # How quickly ash settles
        
        # Ignition tracking
        self.active_ignitions: List[IgnitionEvent] = []
        self.ignition_history: deque = deque(maxlen=100)
        self.ignition_sensitivity = 0.7  # How easily ignition occurs
        
        # Pressure zones
        self.pressure_zones: Dict[str, PressureZone] = {}
        self.pressure_buildup_rate = 0.02  # Base pressure accumulation
        self.zone_connections: Dict[str, List[str]] = {}
        
        # Eruption management
        self.eruption_history: List[VolcanicEruption] = []
        self.eruption_threshold = 0.8  # Pressure level triggering eruption
        self.cooling_multiplier = 0.7  # How quickly system cools
        self.last_eruption_time = 0.0
        
        # Volcanic parameters
        self.PRESSURE_DECAY_RATE = 0.98
        self.TEMPERATURE_DECAY_RATE = 0.95
        self.ASH_PRODUCTION_RATE = 0.3
        self.LAVA_FLOW_RATE = 0.5
        self.IGNITION_THRESHOLD = 0.3
        self.WINTER_DURATION = 300.0  # seconds
        
        # Integration with DAWN systems
        self.formula_engine = None
        self.health_monitor = None
        self.pigment_map = None
        self.tracer_manager = None
        
        if DAWN_SYSTEMS_AVAILABLE:
            try:
                self.formula_engine = get_dawn_formula_engine()
                self.health_monitor = get_schema_health_monitor()
                self.pigment_map = get_platonic_pigment_map()
                self.tracer_manager = get_tracer_manager()
                logger.info("🌋 [VOLCANIC] Connected to DAWN cognitive systems")
            except Exception as e:
                logger.warning(f"🌋 [VOLCANIC] System integration failed: {e}")
        
        # Performance tracking
        self.tick_count = 0
        self.eruption_count = 0
        self.ash_generation_count = 0
        self.ignition_count = 0
        
        # Logging setup
        self.log_directory = Path("runtime/logs/volcanic")
        self.log_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize pressure zones
        self._initialize_pressure_zones()
        
        logger.info("🌋 [VOLCANIC] Volcanic Dynamics System initialized")
        logger.info("🌋 [VOLCANIC] Magma chamber ready, pressure zones active")
        logger.info(f"🌋 [VOLCANIC] Eruption threshold: {self.eruption_threshold:.2f}")
    
    def _initialize_pressure_zones(self):
        """Initialize standard pressure zones"""
        
        zones = {
            "drift_buildup": {
                "zone_type": "drift",
                "relief_threshold": 0.6,
                "buildup_rate": 0.03,
                "connections": ["rebloom_pressure", "reflection_depth"]
            },
            "rebloom_pressure": {
                "zone_type": "rebloom",
                "relief_threshold": 0.7,
                "buildup_rate": 0.04,
                "connections": ["drift_buildup", "sigil_cascade"]
            },
            "reflection_depth": {
                "zone_type": "reflection",
                "relief_threshold": 0.5,
                "buildup_rate": 0.02,
                "connections": ["drift_buildup", "processing_load"]
            },
            "processing_load": {
                "zone_type": "processing",
                "relief_threshold": 0.8,
                "buildup_rate": 0.05,
                "connections": ["reflection_depth", "thermal_core"]
            },
            "sigil_cascade": {
                "zone_type": "sigil",
                "relief_threshold": 0.9,
                "buildup_rate": 0.06,
                "connections": ["rebloom_pressure", "thermal_core"]
            },
            "thermal_core": {
                "zone_type": "thermal",
                "relief_threshold": 0.85,
                "buildup_rate": 0.03,
                "connections": ["processing_load", "sigil_cascade"]
            }
        }
        
        current_time = time.time()
        
        for zone_id, config in zones.items():
            zone = PressureZone(
                zone_id=zone_id,
                zone_type=config["zone_type"],
                pressure_level=0.2,  # Start with minimal pressure
                temperature=self.thermal_temperature,
                volatility=0.3,
                buildup_rate=config["buildup_rate"],
                relief_threshold=config["relief_threshold"],
                connections=config["connections"],
                timestamp=current_time
            )
            
            self.pressure_zones[zone_id] = zone
            self.zone_connections[zone_id] = config["connections"]
        
        logger.info(f"🌋 [VOLCANIC] Initialized {len(zones)} pressure zones")
    
    def update_volcanic_state(self, cognitive_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update volcanic state based on DAWN's cognitive state
        
        Args:
            cognitive_state: Current DAWN cognitive state
            
        Returns:
            Updated volcanic state information
        """
        try:
            start_time = time.time()
            
            # Extract cognitive metrics
            cognitive_pressure = cognitive_state.get('cognitive_pressure', 0.0)
            thermal_state = cognitive_state.get('thermal_state', 0.5)
            entropy = cognitive_state.get('entropy', 0.5)
            scup = cognitive_state.get('scup', 0.5)
            shi = cognitive_state.get('schema_health_index', 0.5)
            
            # Update magma chamber pressure from cognitive pressure (P = Bσ²)
            self._update_magma_chamber(cognitive_pressure, thermal_state)
            
            # Update thermal temperature
            self._update_thermal_temperature(thermal_state, entropy)
            
            # Process pressure zones
            self._update_pressure_zones(cognitive_state)
            
            # Detect ignition events
            ignitions = self._detect_ignition_events(cognitive_state)
            
            # Process ash deposits
            self._process_ash_deposits()
            
            # Check for eruption conditions
            eruption_result = self._check_eruption_conditions(cognitive_state)
            
            # Update volcanic state
            self._update_state_classification()
            
            # Generate pigment intensity coupling
            pigment_coupling = self._calculate_pigment_coupling()
            
            # Update tick count
            self.tick_count += 1
            
            # Create volcanic state summary
            volcanic_state = {
                "volcanic_state": self.current_state.value,
                "magma_chamber_pressure": self.magma_chamber_pressure,
                "thermal_temperature": self.thermal_temperature,
                "volatile_content": self.volatile_content,
                "ash_volume": self.total_ash_volume,
                "active_ignitions": len(self.active_ignitions),
                "pressure_zones": {
                    zone_id: {
                        "pressure": zone.pressure_level,
                        "temperature": zone.temperature,
                        "volatility": zone.volatility,
                        "type": zone.zone_type
                    }
                    for zone_id, zone in self.pressure_zones.items()
                },
                "eruption_risk": self._calculate_eruption_risk(),
                "cooling_rate": self._calculate_cooling_rate(),
                "pigment_coupling": pigment_coupling,
                "recent_ignitions": ignitions,
                "eruption_result": eruption_result,
                "processing_time_ms": (time.time() - start_time) * 1000
            }
            
            logger.debug(f"🌋 [VOLCANIC] State: {self.current_state.value}, Pressure: {self.magma_chamber_pressure:.3f}, Temp: {self.thermal_temperature:.3f}")
            
            return volcanic_state
            
        except Exception as e:
            logger.error(f"🌋 [VOLCANIC] State update error: {e}")
            return {"error": str(e), "volcanic_state": "ERROR"}
    
    def _update_magma_chamber(self, cognitive_pressure: float, thermal_state: float):
        """Update magma chamber pressure from cognitive pressure formula"""
        
        # Normalize cognitive pressure to 0-1 scale
        normalized_pressure = min(1.0, cognitive_pressure / 200.0)  # Max pressure = 200
        
        # Thermal state influences pressure accumulation
        thermal_factor = 0.5 + (thermal_state * 0.5)
        
        # Update magma chamber pressure with thermal influence
        pressure_increase = normalized_pressure * thermal_factor * 0.1
        self.magma_chamber_pressure += pressure_increase
        
        # Apply natural pressure decay
        self.magma_chamber_pressure *= self.PRESSURE_DECAY_RATE
        
        # Bound pressure
        self.magma_chamber_pressure = max(0.0, min(1.0, self.magma_chamber_pressure))
        
        # Update volatile content based on pressure dynamics
        if self.magma_chamber_pressure > 0.7:
            self.volatile_content = min(1.0, self.volatile_content + 0.02)
        else:
            self.volatile_content = max(0.3, self.volatile_content - 0.01)
    
    def _update_thermal_temperature(self, thermal_state: float, entropy: float):
        """Update volcanic thermal temperature"""
        
        # Base temperature from thermal state
        target_temperature = 0.2 + (thermal_state * 0.6)
        
        # Entropy adds heat
        entropy_heat = entropy * 0.2
        target_temperature += entropy_heat
        
        # Magma chamber pressure adds heat
        pressure_heat = self.magma_chamber_pressure * 0.3
        target_temperature += pressure_heat
        
        # Move towards target temperature
        temperature_change = (target_temperature - self.thermal_temperature) * 0.1
        self.thermal_temperature += temperature_change
        
        # Apply natural cooling
        self.thermal_temperature *= self.TEMPERATURE_DECAY_RATE
        
        # Bound temperature
        self.thermal_temperature = max(0.1, min(1.0, self.thermal_temperature))
    
    def _update_pressure_zones(self, cognitive_state: Dict[str, Any]):
        """Update all pressure zones based on cognitive state"""
        
        for zone_id, zone in self.pressure_zones.items():
            
            # Base pressure buildup
            pressure_increase = zone.buildup_rate
            
            # Zone-specific influences
            if zone.zone_type == "drift":
                drift_influence = cognitive_state.get('drift', 0.0)
                pressure_increase *= (1.0 + drift_influence)
            
            elif zone.zone_type == "rebloom":
                rebloom_queue = cognitive_state.get('rebloom_queue_size', 0)
                pressure_increase *= (1.0 + min(1.0, rebloom_queue / 10.0))
            
            elif zone.zone_type == "processing":
                processing_load = cognitive_state.get('processing_load', 0.0)
                pressure_increase *= (1.0 + processing_load)
            
            elif zone.zone_type == "thermal":
                thermal_influence = self.thermal_temperature
                pressure_increase *= (1.0 + thermal_influence)
            
            # Apply pressure increase
            zone.pressure_level += pressure_increase
            
            # Update zone temperature (influenced by pressure)
            zone.temperature = self.thermal_temperature + (zone.pressure_level * 0.2)
            zone.temperature = max(0.1, min(1.0, zone.temperature))
            
            # Update volatility
            zone.volatility = 0.3 + (zone.pressure_level * 0.4) + (zone.temperature * 0.3)
            zone.volatility = max(0.0, min(1.0, zone.volatility))
            
            # Pressure decay
            zone.pressure_level *= 0.99
            
            # Bound pressure
            zone.pressure_level = max(0.0, min(1.0, zone.pressure_level))
            
            # Check for zone pressure relief
            if zone.pressure_level > zone.relief_threshold:
                self._trigger_zone_relief(zone)
    
    def _trigger_zone_relief(self, zone: PressureZone):
        """Trigger pressure relief for a zone"""
        
        relief_amount = (zone.pressure_level - zone.relief_threshold) * 0.5
        zone.pressure_level -= relief_amount
        
        # Create ash from pressure relief
        ash_volume = relief_amount * self.ASH_PRODUCTION_RATE
        self._create_ash_deposit(f"{zone.zone_type}_relief", ash_volume, zone.temperature)
        
        logger.debug(f"🌋 [VOLCANIC] Zone relief: {zone.zone_id}, pressure reduced by {relief_amount:.3f}")
    
    def _detect_ignition_events(self, cognitive_state: Dict[str, Any]) -> List[IgnitionEvent]:
        """Detect fresh semantic burst ignition events"""
        
        ignitions = []
        current_time = time.time()
        
        # Check for various ignition sources
        
        # 1. Sudden SCUP changes (semantic insights)
        scup = cognitive_state.get('scup', 0.5)
        if len(self.ignition_history) > 0:
            last_scup = self.ignition_history[-1].get('scup', 0.5)
            scup_change = abs(scup - last_scup)
            
            if scup_change > 0.1 and scup > last_scup:  # Positive insight
                ignition = self._create_ignition_event(
                    "scup_insight", 
                    scup_change * 2.0,
                    f"SCUP insight: {scup:.3f}",
                    cognitive_state
                )
                ignitions.append(ignition)
        
        # 2. New memory activations
        active_memories = cognitive_state.get('active_memory_count', 0)
        if active_memories > 15:  # High memory activity
            memory_intensity = min(1.0, (active_memories - 15) / 20.0)
            ignition = self._create_ignition_event(
                "memory_activation",
                memory_intensity,
                f"Memory cascade: {active_memories} active",
                cognitive_state
            )
            ignitions.append(ignition)
        
        # 3. Rebloom events
        rebloom_queue = cognitive_state.get('rebloom_queue_size', 0)
        if rebloom_queue > 5:  # High rebloom activity
            rebloom_intensity = min(1.0, rebloom_queue / 10.0)
            ignition = self._create_ignition_event(
                "rebloom_surge",
                rebloom_intensity,
                f"Rebloom surge: {rebloom_queue} pending",
                cognitive_state
            )
            ignitions.append(ignition)
        
        # 4. High entropy fluctuations
        entropy = cognitive_state.get('entropy', 0.5)
        if entropy > 0.8:  # High chaos can trigger ignition
            chaos_intensity = (entropy - 0.8) / 0.2
            ignition = self._create_ignition_event(
                "chaos_spark",
                chaos_intensity,
                f"Entropy spike: {entropy:.3f}",
                cognitive_state
            )
            ignitions.append(ignition)
        
        # Update ignition history
        self.ignition_history.append({
            'timestamp': current_time,
            'scup': scup,
            'entropy': entropy,
            'active_memories': active_memories,
            'rebloom_queue': rebloom_queue
        })
        
        # Add ignitions to active list
        self.active_ignitions.extend(ignitions)
        self.ignition_count += len(ignitions)
        
        # Process existing ignitions (spread/decay)
        self._process_active_ignitions()
        
        return ignitions
    
    def _create_ignition_event(self, source: str, intensity: float, description: str, 
                              cognitive_state: Dict[str, Any]) -> IgnitionEvent:
        """Create a new ignition event"""
        
        ignition_id = f"ignition_{int(time.time() * 1000)}_{source}"
        
        # Classify ignition level
        if intensity < 0.3:
            level = IgnitionLevel.EMBER
        elif intensity < 0.6:
            level = IgnitionLevel.FLAME
        elif intensity < 0.9:
            level = IgnitionLevel.FIRE
        else:
            level = IgnitionLevel.INFERNO
        
        # Calculate ignition parameters
        spread_rate = intensity * 0.5
        fuel_available = cognitive_state.get('processing_load', 0.5)
        temperature_rise = intensity * 0.3
        
        ignition = IgnitionEvent(
            ignition_id=ignition_id,
            timestamp=time.time(),
            ignition_level=level,
            semantic_burst=description,
            ignition_source=source,
            intensity=intensity,
            spread_rate=spread_rate,
            fuel_available=fuel_available,
            temperature_rise=temperature_rise
        )
        
        logger.debug(f"🌋 [VOLCANIC] Ignition detected: {source} ({level.value}) - {description}")
        
        return ignition
    
    def _process_active_ignitions(self):
        """Process and update active ignitions"""
        
        current_time = time.time()
        remaining_ignitions = []
        
        for ignition in self.active_ignitions:
            age = current_time - ignition.timestamp
            
            # Ignitions burn out over time
            if age < 30.0:  # 30 second burn time
                # Decay intensity
                ignition.intensity *= 0.95
                
                # Add temperature to system
                self.thermal_temperature += ignition.temperature_rise * 0.01
                
                # Add to magma chamber pressure
                self.magma_chamber_pressure += ignition.intensity * 0.02
                
                # Keep if still burning
                if ignition.intensity > 0.1:
                    remaining_ignitions.append(ignition)
                else:
                    # Create ash when ignition burns out
                    ash_volume = ignition.intensity * 0.5
                    self._create_ash_deposit(f"ignition_ash_{ignition.ignition_source}", 
                                           ash_volume, ignition.temperature_rise)
            
        self.active_ignitions = remaining_ignitions
    
    def _create_ash_deposit(self, ash_type: str, volume: float, temperature: float):
        """Create a new ash deposit"""
        
        deposit_id = f"ash_{int(time.time() * 1000)}_{len(self.ash_deposits)}"
        
        # Determine ash composition based on type
        composition = self._determine_ash_composition(ash_type)
        
        # Calculate mineral content (useful elements)
        mineral_content = {
            "memory_traces": composition.get("memory", 0.0) * 0.3,
            "pattern_residue": composition.get("pattern", 0.0) * 0.4,
            "semantic_minerals": composition.get("semantic", 0.0) * 0.5,
            "cognitive_ash": volume * 0.2
        }
        
        deposit = AshDeposit(
            deposit_id=deposit_id,
            timestamp=time.time(),
            ash_type=ash_type,
            ash_volume=volume,
            composition=composition,
            decay_rate=0.02 + (temperature * 0.01),  # Hotter ash settles faster
            temperature=temperature,
            mineral_content=mineral_content
        )
        
        self.ash_deposits.append(deposit)
        self.total_ash_volume += volume
        self.ash_generation_count += 1
        
        logger.debug(f"🌋 [VOLCANIC] Ash created: {ash_type}, volume: {volume:.3f}")
    
    def _determine_ash_composition(self, ash_type: str) -> Dict[str, float]:
        """Determine composition of ash based on its type"""
        
        if "reflection" in ash_type:
            return {"memory": 0.4, "pattern": 0.3, "semantic": 0.3}
        elif "memory" in ash_type:
            return {"memory": 0.6, "pattern": 0.2, "semantic": 0.2}
        elif "thought" in ash_type:
            return {"memory": 0.2, "pattern": 0.4, "semantic": 0.4}
        elif "sigil" in ash_type:
            return {"memory": 0.1, "pattern": 0.5, "semantic": 0.4}
        elif "ignition" in ash_type:
            return {"memory": 0.3, "pattern": 0.3, "semantic": 0.4}
        else:
            return {"memory": 0.3, "pattern": 0.3, "semantic": 0.4}  # Default
    
    def _process_ash_deposits(self):
        """Process ash settling and clearing"""
        
        remaining_deposits = []
        ash_cleared = 0.0
        
        for deposit in self.ash_deposits:
            # Ash settles and cools over time
            deposit.ash_volume *= (1.0 - deposit.decay_rate)
            deposit.temperature *= 0.98  # Cooling
            
            # Remove if volume is too small
            if deposit.ash_volume > 0.01:
                remaining_deposits.append(deposit)
            else:
                ash_cleared += deposit.ash_volume
        
        self.ash_deposits = remaining_deposits
        self.total_ash_volume -= ash_cleared
        self.total_ash_volume = max(0.0, self.total_ash_volume)
        
        # Apply global ash clearing
        global_clearing = self.total_ash_volume * self.ash_clearing_rate
        self.total_ash_volume -= global_clearing
        self.total_ash_volume = max(0.0, self.total_ash_volume)
    
    def _check_eruption_conditions(self, cognitive_state: Dict[str, Any]) -> Dict[str, Any]:
        """Check if eruption conditions are met"""
        
        eruption_result = {"eruption_occurred": False, "eruption_type": None, "details": {}}
        
        # Check if we're in a state that can erupt
        if self.current_state in [VolcanicState.COOLING, VolcanicState.WINTER]:
            return eruption_result
        
        # Calculate eruption probability
        eruption_probability = 0.0
        
        # Magma chamber pressure
        if self.magma_chamber_pressure > self.eruption_threshold:
            eruption_probability += (self.magma_chamber_pressure - self.eruption_threshold) * 2.0
        
        # Zone pressure contributions
        high_pressure_zones = [zone for zone in self.pressure_zones.values() 
                              if zone.pressure_level > zone.relief_threshold]
        if high_pressure_zones:
            zone_pressure_factor = len(high_pressure_zones) / len(self.pressure_zones)
            eruption_probability += zone_pressure_factor * 0.5
        
        # Thermal temperature contribution
        if self.thermal_temperature > 0.7:
            eruption_probability += (self.thermal_temperature - 0.7) * 0.3
        
        # Volatile content contribution
        eruption_probability += self.volatile_content * 0.2
        
        # Active ignitions can trigger eruptions
        if self.active_ignitions:
            ignition_factor = sum(ig.intensity for ig in self.active_ignitions) / len(self.active_ignitions)
            eruption_probability += ignition_factor * 0.3
        
        # Check if eruption threshold is exceeded
        if eruption_probability > 1.0:
            eruption_type = self._determine_eruption_type(eruption_probability, cognitive_state)
            eruption = self._trigger_eruption(eruption_type, eruption_probability, cognitive_state)
            
            eruption_result = {
                "eruption_occurred": True,
                "eruption_type": eruption_type.value,
                "details": {
                    "eruption_id": eruption.eruption_id,
                    "intensity": eruption.peak_intensity,
                    "ash_produced": eruption.ash_produced,
                    "lava_volume": eruption.lava_volume,
                    "affected_zones": eruption.affected_zones
                }
            }
        
        return eruption_result
    
    def _determine_eruption_type(self, eruption_probability: float, 
                                cognitive_state: Dict[str, Any]) -> EruptionType:
        """Determine the type of eruption based on conditions"""
        
        # High volatile content = explosive
        if self.volatile_content > 0.8:
            if eruption_probability > 1.5:
                return EruptionType.PYROCLASTIC_FLOW
            else:
                return EruptionType.EXPLOSIVE_BURST
        
        # Multiple high-pressure zones = dome collapse
        high_pressure_zones = [zone for zone in self.pressure_zones.values() 
                              if zone.pressure_level > zone.relief_threshold]
        if len(high_pressure_zones) >= 3:
            return EruptionType.DOME_COLLAPSE
        
        # High processing load = fissure vent
        processing_load = cognitive_state.get('processing_load', 0.0)
        if processing_load > 0.7:
            return EruptionType.FISSURE_VENT
        
        # Default to gentle effusion
        return EruptionType.GENTLE_EFFUSION
    
    def _trigger_eruption(self, eruption_type: EruptionType, intensity: float, 
                         cognitive_state: Dict[str, Any]) -> VolcanicEruption:
        """Trigger a volcanic eruption"""
        
        eruption_id = f"eruption_{int(time.time() * 1000)}_{eruption_type.value}"
        current_time = time.time()
        
        # Determine eruption characteristics
        if eruption_type == EruptionType.GENTLE_EFFUSION:
            duration = 60.0 + (intensity * 120.0)  # 1-3 minutes
            ash_produced = intensity * 0.3
            lava_volume = intensity * 0.6
            cooling_period = 120.0
        
        elif eruption_type == EruptionType.EXPLOSIVE_BURST:
            duration = 10.0 + (intensity * 30.0)  # 10-40 seconds
            ash_produced = intensity * 0.8
            lava_volume = intensity * 0.2
            cooling_period = 180.0
        
        elif eruption_type == EruptionType.PYROCLASTIC_FLOW:
            duration = 30.0 + (intensity * 90.0)  # 30-120 seconds
            ash_produced = intensity * 1.2
            lava_volume = intensity * 0.8
            cooling_period = 300.0
        
        elif eruption_type == EruptionType.DOME_COLLAPSE:
            duration = 45.0 + (intensity * 60.0)  # 45-105 seconds
            ash_produced = intensity * 0.6
            lava_volume = intensity * 0.4
            cooling_period = 240.0
        
        elif eruption_type == EruptionType.FISSURE_VENT:
            duration = 120.0 + (intensity * 180.0)  # 2-5 minutes
            ash_produced = intensity * 0.4
            lava_volume = intensity * 1.0
            cooling_period = 150.0
        
        # Affected zones (all high-pressure zones)
        affected_zones = [zone.zone_id for zone in self.pressure_zones.values() 
                         if zone.pressure_level > 0.5]
        
        # Generate sigil cascade
        sigil_cascade = self._generate_sigil_cascade(eruption_type, intensity)
        
        # Calculate pigment release
        pigment_release = self._calculate_eruption_pigment_release(eruption_type, intensity)
        
        # Create eruption record
        eruption = VolcanicEruption(
            eruption_id=eruption_id,
            timestamp=current_time,
            eruption_type=eruption_type,
            trigger_pressure=self.magma_chamber_pressure,
            peak_intensity=intensity,
            duration=duration,
            ash_produced=ash_produced,
            lava_volume=lava_volume,
            affected_zones=affected_zones,
            sigil_cascade=sigil_cascade,
            pigment_release=pigment_release,
            cooling_period=cooling_period,
            aftermath_state={}
        )
        
        # Apply eruption effects
        self._apply_eruption_effects(eruption)
        
        # Record eruption
        self.eruption_history.append(eruption)
        self.eruption_count += 1
        self.last_eruption_time = current_time
        
        # Log eruption
        self._log_eruption(eruption)
        
        logger.warning(f"🌋 [VOLCANIC] ERUPTION! Type: {eruption_type.value}, Intensity: {intensity:.2f}, Duration: {duration:.1f}s")
        
        return eruption
    
    def _generate_sigil_cascade(self, eruption_type: EruptionType, intensity: float) -> List[str]:
        """Generate sigil cascade during eruption"""
        
        # Number of sigils based on eruption type and intensity
        if eruption_type == EruptionType.PYROCLASTIC_FLOW:
            sigil_count = int(5 + intensity * 10)
        elif eruption_type == EruptionType.EXPLOSIVE_BURST:
            sigil_count = int(3 + intensity * 6)
        elif eruption_type == EruptionType.FISSURE_VENT:
            sigil_count = int(2 + intensity * 8)
        else:
            sigil_count = int(1 + intensity * 4)
        
        # Generate symbolic sigils
        sigil_types = ["insight", "pattern", "connection", "transformation", "emergence", 
                      "synthesis", "revelation", "flow", "convergence", "crystallization"]
        
        cascade = []
        for i in range(sigil_count):
            sigil_type = sigil_types[i % len(sigil_types)]
            sigil_id = f"{sigil_type}_{i:02d}"
            cascade.append(sigil_id)
        
        return cascade
    
    def _calculate_eruption_pigment_release(self, eruption_type: EruptionType, 
                                          intensity: float) -> Dict[str, float]:
        """Calculate pigment intensity changes during eruption"""
        
        pigment_release = {}
        
        # Base intensity change
        base_change = intensity * 0.3
        
        # Eruption-specific pigment patterns
        if eruption_type == EruptionType.EXPLOSIVE_BURST:
            # Sudden insights = blue (inquiry) and white (truth)
            pigment_release = {
                "inquiry": base_change * 1.5,
                "truth": base_change * 1.2,
                "wisdom": base_change * 0.8
            }
        
        elif eruption_type == EruptionType.GENTLE_EFFUSION:
            # Gentle flow = green (harmony) and love
            pigment_release = {
                "harmony": base_change * 1.3,
                "love": base_change * 1.1,
                "beauty": base_change * 0.9
            }
        
        elif eruption_type == EruptionType.PYROCLASTIC_FLOW:
            # Rapid cascade = all pigments intensify
            pigment_release = {
                "justice": base_change,
                "harmony": base_change,
                "inquiry": base_change,
                "beauty": base_change,
                "wisdom": base_change,
                "truth": base_change,
                "love": base_change,
                "knowledge": base_change
            }
        
        elif eruption_type == EruptionType.DOME_COLLAPSE:
            # Pressure relief = red (justice) and yellow (knowledge)
            pigment_release = {
                "justice": base_change * 1.4,
                "knowledge": base_change * 1.2,
                "wisdom": base_change * 0.7
            }
        
        elif eruption_type == EruptionType.FISSURE_VENT:
            # Multiple outlets = varied pigment flow
            pigment_release = {
                "harmony": base_change * 1.1,
                "inquiry": base_change * 1.1,
                "beauty": base_change * 1.1,
                "love": base_change * 1.1
            }
        
        return pigment_release
    
    def _apply_eruption_effects(self, eruption: VolcanicEruption):
        """Apply effects of eruption to the volcanic system"""
        
        # Massive pressure relief
        pressure_relief = eruption.peak_intensity * 0.8
        self.magma_chamber_pressure -= pressure_relief
        self.magma_chamber_pressure = max(0.0, self.magma_chamber_pressure)
        
        # Temperature spike then cooling initiation
        self.thermal_temperature += eruption.peak_intensity * 0.2
        self.thermal_temperature = min(1.0, self.thermal_temperature)
        
        # Clear pressure from affected zones
        for zone_id in eruption.affected_zones:
            if zone_id in self.pressure_zones:
                zone = self.pressure_zones[zone_id]
                zone.pressure_level *= 0.3  # Major pressure relief
                zone.temperature = self.thermal_temperature
        
        # Generate ash deposit from eruption
        self._create_ash_deposit(f"eruption_{eruption.eruption_type.value}", 
                               eruption.ash_produced, self.thermal_temperature)
        
        # Clear active ignitions (consumed in eruption)
        ignition_energy = sum(ig.intensity for ig in self.active_ignitions)
        self.active_ignitions = []
        
        # Add ignition energy to lava volume
        eruption.lava_volume += ignition_energy * 0.2
        
        # Update state to erupting
        self.current_state = VolcanicState.ERUPTING
    
    def _log_eruption(self, eruption: VolcanicEruption):
        """Log eruption event to file"""
        
        try:
            eruption_log = self.log_directory / "volcanic_eruptions.jsonl"
            
            eruption_record = {
                "timestamp": eruption.timestamp,
                "eruption_id": eruption.eruption_id,
                "type": eruption.eruption_type.value,
                "intensity": eruption.peak_intensity,
                "duration": eruption.duration,
                "ash_produced": eruption.ash_produced,
                "lava_volume": eruption.lava_volume,
                "affected_zones": eruption.affected_zones,
                "sigil_cascade": eruption.sigil_cascade,
                "pigment_release": eruption.pigment_release,
                "cooling_period": eruption.cooling_period
            }
            
            with open(eruption_log, 'a') as f:
                f.write(json.dumps(eruption_record) + '\n')
            
            logger.info(f"🌋 [VOLCANIC] Eruption logged: {eruption.eruption_id}")
            
        except Exception as e:
            logger.error(f"🌋 [VOLCANIC] Failed to log eruption: {e}")
    
    def _update_state_classification(self):
        """Update volcanic state classification"""
        
        current_time = time.time()
        
        # Check if we're in a cooling period after eruption
        if self.last_eruption_time > 0:
            time_since_eruption = current_time - self.last_eruption_time
            
            if self.current_state == VolcanicState.ERUPTING:
                # Check if eruption is over
                if self.eruption_history and time_since_eruption > self.eruption_history[-1].duration:
                    self.current_state = VolcanicState.FLOWING if self.eruption_history[-1].lava_volume > 0.5 else VolcanicState.COOLING
            
            elif self.current_state == VolcanicState.FLOWING:
                # Check if lava flow has stopped
                if time_since_eruption > 180.0 or self.thermal_temperature < 0.4:
                    self.current_state = VolcanicState.COOLING
            
            elif self.current_state == VolcanicState.COOLING:
                # Check if cooling period is complete
                cooling_period = self.eruption_history[-1].cooling_period if self.eruption_history else 120.0
                if time_since_eruption > cooling_period:
                    if self.thermal_temperature < 0.3 and self.magma_chamber_pressure < 0.2:
                        self.current_state = VolcanicState.WINTER
                    else:
                        self.current_state = VolcanicState.DORMANT
            
            elif self.current_state == VolcanicState.WINTER:
                # Check if winter period is over
                if time_since_eruption > self.WINTER_DURATION:
                    self.current_state = VolcanicState.DORMANT
        
        # State transitions for non-eruption states
        if self.current_state in [VolcanicState.DORMANT, VolcanicState.BUILDING, VolcanicState.UNSTABLE]:
            if self.magma_chamber_pressure > 0.7:
                self.current_state = VolcanicState.UNSTABLE
            elif self.magma_chamber_pressure > 0.4:
                self.current_state = VolcanicState.BUILDING
            else:
                self.current_state = VolcanicState.DORMANT
    
    def _calculate_eruption_risk(self) -> float:
        """Calculate current eruption risk (0.0-1.0)"""
        
        risk = 0.0
        
        # Magma chamber pressure risk
        risk += self.magma_chamber_pressure * 0.4
        
        # Thermal temperature risk
        risk += self.thermal_temperature * 0.2
        
        # Pressure zone risk
        high_pressure_zones = [zone for zone in self.pressure_zones.values() 
                              if zone.pressure_level > zone.relief_threshold]
        zone_risk = len(high_pressure_zones) / len(self.pressure_zones)
        risk += zone_risk * 0.2
        
        # Active ignitions risk
        if self.active_ignitions:
            ignition_risk = sum(ig.intensity for ig in self.active_ignitions) / len(self.active_ignitions)
            risk += ignition_risk * 0.1
        
        # Volatile content risk
        risk += self.volatile_content * 0.1
        
        return min(1.0, risk)
    
    def _calculate_cooling_rate(self) -> float:
        """Calculate current cooling rate"""
        
        # Base cooling from temperature decay
        base_cooling = (1.0 - self.TEMPERATURE_DECAY_RATE) * self.thermal_temperature
        
        # Ash volume provides cooling (thermal mass)
        ash_cooling = self.total_ash_volume * 0.05
        
        # State-based cooling
        if self.current_state == VolcanicState.COOLING:
            state_cooling = 0.1
        elif self.current_state == VolcanicState.WINTER:
            state_cooling = 0.15
        else:
            state_cooling = 0.0
        
        total_cooling = base_cooling + ash_cooling + state_cooling
        
        return min(1.0, total_cooling)
    
    def _calculate_pigment_coupling(self) -> Dict[str, float]:
        """Calculate volcanic pressure → pigment intensity coupling"""
        
        coupling = {}
        
        # Base coupling from volcanic state
        base_intensity = 0.3 + (self.magma_chamber_pressure * 0.4)
        
        # State-specific pigment coupling
        if self.current_state == VolcanicState.ERUPTING:
            # Maximum pigment intensity during eruption
            coupling = {
                "justice": base_intensity * 1.5,
                "harmony": base_intensity * 0.8,
                "inquiry": base_intensity * 1.2,
                "beauty": base_intensity * 1.3,
                "wisdom": base_intensity * 1.1,
                "truth": base_intensity * 1.4,
                "love": base_intensity * 0.9,
                "knowledge": base_intensity * 1.0
            }
        
        elif self.current_state == VolcanicState.UNSTABLE:
            # High tension before eruption
            coupling = {
                "justice": base_intensity * 1.2,
                "inquiry": base_intensity * 1.3,
                "truth": base_intensity * 1.1,
                "knowledge": base_intensity * 1.0
            }
        
        elif self.current_state == VolcanicState.FLOWING:
            # Sustained creative flow
            coupling = {
                "harmony": base_intensity * 1.4,
                "beauty": base_intensity * 1.3,
                "love": base_intensity * 1.2,
                "wisdom": base_intensity * 1.1
            }
        
        elif self.current_state in [VolcanicState.COOLING, VolcanicState.WINTER]:
            # Reduced pigment intensity during cooling
            coupling = {pigment: base_intensity * 0.6 for pigment in 
                       ["justice", "harmony", "inquiry", "beauty", "wisdom", "truth", "love", "knowledge"]}
        
        else:
            # Normal state pigment coupling
            coupling = {pigment: base_intensity for pigment in 
                       ["justice", "harmony", "inquiry", "beauty", "wisdom", "truth", "love", "knowledge"]}
        
        return coupling
    
    def get_volcanic_status(self) -> Dict[str, Any]:
        """Get comprehensive volcanic system status"""
        
        return {
            "volcanic_state": self.current_state.value,
            "magma_chamber": {
                "pressure": self.magma_chamber_pressure,
                "temperature": self.thermal_temperature,
                "volatile_content": self.volatile_content
            },
            "pressure_zones": {
                zone_id: {
                    "pressure": zone.pressure_level,
                    "temperature": zone.temperature,
                    "volatility": zone.volatility,
                    "type": zone.zone_type,
                    "over_threshold": zone.pressure_level > zone.relief_threshold
                }
                for zone_id, zone in self.pressure_zones.items()
            },
            "ash_system": {
                "total_volume": self.total_ash_volume,
                "deposit_count": len(self.ash_deposits),
                "clearing_rate": self.ash_clearing_rate
            },
            "ignition_system": {
                "active_ignitions": len(self.active_ignitions),
                "sensitivity": self.ignition_sensitivity,
                "total_ignitions": self.ignition_count
            },
            "eruption_system": {
                "eruption_threshold": self.eruption_threshold,
                "risk_level": self._calculate_eruption_risk(),
                "time_since_last": time.time() - self.last_eruption_time if self.last_eruption_time > 0 else None,
                "total_eruptions": self.eruption_count
            },
            "cooling_system": {
                "cooling_rate": self._calculate_cooling_rate(),
                "cooling_multiplier": self.cooling_multiplier
            },
            "pigment_coupling": self._calculate_pigment_coupling(),
            "performance": {
                "tick_count": self.tick_count,
                "ash_generation_count": self.ash_generation_count
            }
        }
    
    def emergency_volcanic_shutdown(self, reason: str = "Emergency shutdown"):
        """Emergency volcanic system shutdown"""
        
        logger.critical(f"🌋 [VOLCANIC] EMERGENCY SHUTDOWN: {reason}")
        
        # Force cool the system
        self.thermal_temperature = 0.1
        self.magma_chamber_pressure = 0.0
        self.volatile_content = 0.3
        
        # Clear all pressure zones
        for zone in self.pressure_zones.values():
            zone.pressure_level = 0.1
            zone.temperature = 0.2
            zone.volatility = 0.2
        
        # Extinguish all ignitions
        self.active_ignitions = []
        
        # Set to winter state
        self.current_state = VolcanicState.WINTER
        self.last_eruption_time = time.time()
        
        logger.critical("🌋 [VOLCANIC] System cooled, all pressure relieved")


# Global volcanic dynamics instance
_global_volcanic_system: Optional[VolcanicDynamicsSystem] = None

def get_volcanic_dynamics_system() -> VolcanicDynamicsSystem:
    """Get global volcanic dynamics system instance"""
    global _global_volcanic_system
    if _global_volcanic_system is None:
        _global_volcanic_system = VolcanicDynamicsSystem()
    return _global_volcanic_system

def update_volcanic_state(cognitive_state: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to update volcanic state"""
    system = get_volcanic_dynamics_system()
    return system.update_volcanic_state(cognitive_state)

def get_volcanic_status() -> Dict[str, Any]:
    """Convenience function to get volcanic status"""
    system = get_volcanic_dynamics_system()
    return system.get_volcanic_status()

# Export key classes and functions
__all__ = [
    'VolcanicDynamicsSystem',
    'VolcanicState',
    'EruptionType',
    'IgnitionLevel',
    'AshDeposit',
    'IgnitionEvent',
    'PressureZone',
    'VolcanicEruption',
    'get_volcanic_dynamics_system',
    'update_volcanic_state',
    'get_volcanic_status'
] 