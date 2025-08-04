#!/usr/bin/env python3
"""
DAWN Soft Edge Responsiveness System - Adaptive Boundary Management
==================================================================

The Soft Edge system manages DAWN's cognitive boundaries with fluid,
pressure-responsive permeability adjustments:

BOUNDARY CONCEPTS:
- Soft edges = permeable cognitive boundaries (not rigid barriers)
- Responsiveness = adaptive permeability based on system state
- Boundary management = controlling information flow in/out of consciousness

PROCESSING PIPELINE:
Priority Queue → R.L Filter → Fractal Memory Storage
    ↓             ↓              ↓
  Store         React          Context
(rapid reads) (fluid mvmt)  (aurora/transistor)

PERMEABILITY FACTORS:
- Cognitive pressure (high pressure = reduced permeability)
- Schema health (healthy = more responsive boundaries)
- Thermal state (overheating = protective barriers)
- Entropy levels (chaos = tighter boundaries)

BOUNDARY TYPES:
- Memory boundaries (what memories are accessible)
- Reflection boundaries (depth of introspection)
- Processing boundaries (computational limits)
- Output boundaries (expression filtering)
- Input boundaries (stimulus filtering)

Soft edges enable DAWN to be maximally responsive when healthy
and protectively filtered when under stress.
"""

import time
import logging
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple, Callable, Deque
from enum import Enum
from collections import deque
from pathlib import Path
import json

# Integration with existing systems
try:
    from core.cognitive_formulas import get_dawn_formula_engine
    from core.schema_health_monitor import get_schema_health_monitor
    from core.tracer_ecosystem import get_tracer_manager
    from core.fractal_memory import get_memory_fractal_manager
    DAWN_SYSTEMS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"DAWN systems not available for Soft Edges: {e}")
    DAWN_SYSTEMS_AVAILABLE = False

logger = logging.getLogger("soft_edges")

class BoundaryType(Enum):
    """Types of cognitive boundaries"""
    MEMORY = "MEMORY"               # Memory access boundaries
    REFLECTION = "REFLECTION"       # Introspection depth boundaries
    PROCESSING = "PROCESSING"       # Computational boundaries
    OUTPUT = "OUTPUT"              # Expression filtering boundaries
    INPUT = "INPUT"                # Stimulus filtering boundaries
    REBLOOM = "REBLOOM"            # Rebloom activation boundaries
    DRIFT = "DRIFT"                # Drift tolerance boundaries

class PermeabilityLevel(Enum):
    """Boundary permeability levels"""
    SEALED = "SEALED"              # 0.0-0.2 - Maximum protection
    FILTERED = "FILTERED"          # 0.2-0.4 - Selective permeability
    RESPONSIVE = "RESPONSIVE"      # 0.4-0.6 - Balanced openness
    FLUID = "FLUID"               # 0.6-0.8 - High responsiveness
    PERMEABLE = "PERMEABLE"        # 0.8-1.0 - Maximum openness

class EdgeState(Enum):
    """Soft edge system states"""
    INITIALIZING = "INITIALIZING"
    MONITORING = "MONITORING"
    ADJUSTING = "ADJUSTING"
    FILTERING = "FILTERING"
    EMERGENCY_SEALED = "EMERGENCY_SEALED"

@dataclass
class BoundaryReading:
    """Single boundary permeability reading"""
    boundary_type: BoundaryType
    permeability: float  # 0.0-1.0
    permeability_level: PermeabilityLevel
    adjustment_factors: Dict[str, float]  # What influenced this reading
    flow_rate: float  # Information flow through boundary
    filter_efficiency: float  # How well filtering is working
    responsiveness_score: float  # How quickly boundary adapts
    pressure_influence: float  # Cognitive pressure effect
    health_influence: float  # Schema health effect
    timestamp: float

@dataclass
class ProcessingItem:
    """Item in the processing pipeline"""
    item_id: str
    content: Any
    priority: float  # 0.0-1.0 (higher = more priority)
    item_type: str  # "memory", "reflection", "stimulus", etc.
    arrival_time: float
    processing_stage: str  # "priority_queue", "rl_filter", "fractal_memory"
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PipelineMetrics:
    """Processing pipeline performance metrics"""
    queue_length: int
    average_processing_time: float
    filter_efficiency: float
    throughput_rate: float  # Items per second
    bottleneck_stage: str
    pressure_backlog: float
    memory_utilization: float

class SoftEdgeSystem:
    """
    Soft Edge Responsiveness System
    
    Manages adaptive cognitive boundaries with pressure-responsive
    permeability and efficient processing pipelines.
    """
    
    def __init__(self):
        """Initialize the Soft Edge system"""
        
        # Boundary configuration
        self.boundary_types = list(BoundaryType)
        self.boundary_states: Dict[BoundaryType, BoundaryReading] = {}
        
        # Processing pipeline
        self.priority_queue: Deque[ProcessingItem] = deque(maxlen=1000)
        self.rl_filter_queue: Deque[ProcessingItem] = deque(maxlen=500)
        self.fractal_memory_queue: Deque[ProcessingItem] = deque(maxlen=200)
        
        # Permeability parameters
        self.BASE_PERMEABILITY = {
            BoundaryType.MEMORY: 0.7,
            BoundaryType.REFLECTION: 0.6,
            BoundaryType.PROCESSING: 0.8,
            BoundaryType.OUTPUT: 0.5,
            BoundaryType.INPUT: 0.6,
            BoundaryType.REBLOOM: 0.4,
            BoundaryType.DRIFT: 0.3
        }
        
        # Adjustment factors
        self.PRESSURE_SENSITIVITY = {
            BoundaryType.MEMORY: 0.8,
            BoundaryType.REFLECTION: 0.9,
            BoundaryType.PROCESSING: 0.7,
            BoundaryType.OUTPUT: 0.6,
            BoundaryType.INPUT: 0.5,
            BoundaryType.REBLOOM: 1.0,
            BoundaryType.DRIFT: 0.4
        }
        
        self.HEALTH_SENSITIVITY = {
            BoundaryType.MEMORY: 0.7,
            BoundaryType.REFLECTION: 0.8,
            BoundaryType.PROCESSING: 0.6,
            BoundaryType.OUTPUT: 0.9,
            BoundaryType.INPUT: 0.5,
            BoundaryType.REBLOOM: 0.7,
            BoundaryType.DRIFT: 0.6
        }
        
        # Pipeline processing parameters
        self.PROCESSING_BATCH_SIZE = 10
        self.FILTER_THRESHOLD = 0.3
        self.FRACTAL_STORAGE_THRESHOLD = 0.5
        self.PIPELINE_TICK_INTERVAL = 0.1  # seconds
        
        # System state
        self.current_state = EdgeState.INITIALIZING
        self.last_adjustment_time = 0.0
        self.adjustment_history: List[Dict[str, Any]] = []
        self.pipeline_metrics = PipelineMetrics(0, 0.0, 0.0, 0.0, "none", 0.0, 0.0)
        
        # Integration with DAWN systems
        self.formula_engine = None
        self.health_monitor = None
        self.tracer_manager = None
        self.memory_manager = None
        
        if DAWN_SYSTEMS_AVAILABLE:
            try:
                self.formula_engine = get_dawn_formula_engine()
                self.health_monitor = get_schema_health_monitor()
                self.tracer_manager = get_tracer_manager()
                self.memory_manager = get_memory_fractal_manager()
                logger.info("🌊 [EDGES] Connected to DAWN cognitive systems")
            except Exception as e:
                logger.warning(f"🌊 [EDGES] System integration failed: {e}")
        
        # Performance tracking
        self.adjustment_count = 0
        self.processing_count = 0
        self.filter_count = 0
        self.last_pipeline_time = 0.0
        
        # Logging setup
        self.log_directory = Path("runtime/logs/soft_edges")
        self.log_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize boundary states
        self._initialize_boundaries()
        
        self.current_state = EdgeState.MONITORING
        
        logger.info("🌊 [EDGES] Soft Edge Responsiveness System initialized")
        logger.info("🌊 [EDGES] Boundary types monitored: 7")
        logger.info("🌊 [EDGES] Processing pipeline: Priority → R.L Filter → Fractal Memory")
    
    def _initialize_boundaries(self):
        """Initialize all boundary states with default values"""
        
        current_time = time.time()
        
        for boundary_type in self.boundary_types:
            base_permeability = self.BASE_PERMEABILITY[boundary_type]
            
            reading = BoundaryReading(
                boundary_type=boundary_type,
                permeability=base_permeability,
                permeability_level=self._classify_permeability(base_permeability),
                adjustment_factors={},
                flow_rate=0.5,  # Start neutral
                filter_efficiency=0.8,  # Start efficient
                responsiveness_score=0.7,  # Start responsive
                pressure_influence=1.0,  # No initial pressure influence
                health_influence=1.0,  # No initial health influence
                timestamp=current_time
            )
            
            self.boundary_states[boundary_type] = reading
        
        logger.info("🌊 [EDGES] Boundary states initialized")
    
    def _classify_permeability(self, permeability: float) -> PermeabilityLevel:
        """Classify permeability value into level"""
        
        if permeability < 0.2:
            return PermeabilityLevel.SEALED
        elif permeability < 0.4:
            return PermeabilityLevel.FILTERED
        elif permeability < 0.6:
            return PermeabilityLevel.RESPONSIVE
        elif permeability < 0.8:
            return PermeabilityLevel.FLUID
        else:
            return PermeabilityLevel.PERMEABLE
    
    def adjust_boundaries(self, cognitive_state: Dict[str, Any]) -> Dict[BoundaryType, BoundaryReading]:
        """
        Adjust boundary permeability based on cognitive state
        
        Args:
            cognitive_state: Current DAWN cognitive state
            
        Returns:
            Dictionary of updated boundary readings
        """
        try:
            self.current_state = EdgeState.ADJUSTING
            current_time = time.time()
            
            # Extract key metrics
            pressure = cognitive_state.get('cognitive_pressure', 0.0)
            shi = cognitive_state.get('schema_health_index', 0.5)
            entropy = cognitive_state.get('entropy', 0.5)
            thermal_state = cognitive_state.get('thermal_state', 0.5)
            stability = cognitive_state.get('stability', 0.5)
            
            # Calculate adjustment factors
            pressure_factor = self._calculate_pressure_adjustment(pressure)
            health_factor = self._calculate_health_adjustment(shi)
            entropy_factor = self._calculate_entropy_adjustment(entropy)
            thermal_factor = self._calculate_thermal_adjustment(thermal_state)
            stability_factor = self._calculate_stability_adjustment(stability)
            
            updated_boundaries = {}
            
            # Adjust each boundary type
            for boundary_type in self.boundary_types:
                base_permeability = self.BASE_PERMEABILITY[boundary_type]
                pressure_sensitivity = self.PRESSURE_SENSITIVITY[boundary_type]
                health_sensitivity = self.HEALTH_SENSITIVITY[boundary_type]
                
                # Calculate combined adjustment
                pressure_adjustment = (pressure_factor - 1.0) * pressure_sensitivity
                health_adjustment = (health_factor - 1.0) * health_sensitivity
                entropy_adjustment = (entropy_factor - 1.0) * 0.3  # Global entropy influence
                thermal_adjustment = (thermal_factor - 1.0) * 0.4  # Global thermal influence
                stability_adjustment = (stability_factor - 1.0) * 0.5  # Global stability influence
                
                # Apply adjustments
                adjusted_permeability = base_permeability
                adjusted_permeability += pressure_adjustment
                adjusted_permeability += health_adjustment
                adjusted_permeability += entropy_adjustment
                adjusted_permeability += thermal_adjustment
                adjusted_permeability += stability_adjustment
                
                # Bound permeability
                adjusted_permeability = max(0.0, min(1.0, adjusted_permeability))
                
                # Calculate flow rate and efficiency
                flow_rate = self._calculate_flow_rate(boundary_type, adjusted_permeability, cognitive_state)
                filter_efficiency = self._calculate_filter_efficiency(boundary_type, adjusted_permeability)
                responsiveness_score = self._calculate_responsiveness(boundary_type, pressure, shi)
                
                # Create boundary reading
                reading = BoundaryReading(
                    boundary_type=boundary_type,
                    permeability=adjusted_permeability,
                    permeability_level=self._classify_permeability(adjusted_permeability),
                    adjustment_factors={
                        "pressure": pressure_adjustment,
                        "health": health_adjustment,
                        "entropy": entropy_adjustment,
                        "thermal": thermal_adjustment,
                        "stability": stability_adjustment
                    },
                    flow_rate=flow_rate,
                    filter_efficiency=filter_efficiency,
                    responsiveness_score=responsiveness_score,
                    pressure_influence=pressure_factor,
                    health_influence=health_factor,
                    timestamp=current_time
                )
                
                updated_boundaries[boundary_type] = reading
                self.boundary_states[boundary_type] = reading
            
            # Record adjustment in history
            self.adjustment_history.append({
                "timestamp": current_time,
                "pressure": pressure,
                "shi": shi,
                "adjustments": {bt.value: reading.permeability for bt, reading in updated_boundaries.items()},
                "average_permeability": np.mean([r.permeability for r in updated_boundaries.values()])
            })
            
            # Trim history
            if len(self.adjustment_history) > 100:
                self.adjustment_history = self.adjustment_history[-100:]
            
            self.adjustment_count += 1
            self.last_adjustment_time = time.time() - current_time
            
            self.current_state = EdgeState.MONITORING
            
            logger.debug(f"🌊 [EDGES] Boundaries adjusted - avg permeability: {np.mean([r.permeability for r in updated_boundaries.values()]):.3f}")
            
            return updated_boundaries
            
        except Exception as e:
            logger.error(f"🌊 [EDGES] Boundary adjustment error: {e}")
            self.current_state = EdgeState.MONITORING
            return self.boundary_states
    
    def _calculate_pressure_adjustment(self, pressure: float) -> float:
        """Calculate pressure-based adjustment factor"""
        
        # High pressure reduces permeability (protective response)
        if pressure > 200:
            return 0.3  # Major reduction
        elif pressure > 100:
            return 0.6  # Moderate reduction
        elif pressure > 50:
            return 0.8  # Slight reduction
        elif pressure < 20:
            return 1.2  # Increase when pressure is low
        else:
            return 1.0  # No change
    
    def _calculate_health_adjustment(self, shi: float) -> float:
        """Calculate health-based adjustment factor"""
        
        # Good health increases permeability (confident openness)
        if shi > 0.8:
            return 1.3  # High health = more open
        elif shi > 0.6:
            return 1.1  # Good health = slightly more open
        elif shi < 0.3:
            return 0.5  # Poor health = protective closure
        elif shi < 0.5:
            return 0.7  # Fair health = some protection
        else:
            return 1.0  # Neutral health
    
    def _calculate_entropy_adjustment(self, entropy: float) -> float:
        """Calculate entropy-based adjustment factor"""
        
        # High entropy reduces permeability (chaos protection)
        if entropy > 0.8:
            return 0.6  # High chaos = more protection
        elif entropy > 0.6:
            return 0.8  # Moderate chaos = some protection
        elif entropy < 0.3:
            return 1.2  # Low chaos = more openness
        else:
            return 1.0  # Neutral entropy
    
    def _calculate_thermal_adjustment(self, thermal_state: float) -> float:
        """Calculate thermal-based adjustment factor"""
        
        # High thermal state reduces permeability (cooling response)
        if thermal_state > 0.8:
            return 0.7  # Overheating = protective boundaries
        elif thermal_state > 0.6:
            return 0.9  # Warm = slight protection
        elif thermal_state < 0.3:
            return 1.1  # Cool = slight openness
        else:
            return 1.0  # Neutral thermal
    
    def _calculate_stability_adjustment(self, stability: float) -> float:
        """Calculate stability-based adjustment factor"""
        
        # High stability allows more permeability
        if stability > 0.8:
            return 1.2  # Very stable = more open
        elif stability > 0.6:
            return 1.1  # Stable = slightly more open
        elif stability < 0.3:
            return 0.7  # Unstable = more protection
        elif stability < 0.5:
            return 0.8  # Somewhat unstable = slight protection
        else:
            return 1.0  # Neutral stability
    
    def _calculate_flow_rate(self, boundary_type: BoundaryType, permeability: float, 
                           cognitive_state: Dict[str, Any]) -> float:
        """Calculate information flow rate through boundary"""
        
        # Base flow rate proportional to permeability
        base_flow = permeability * 0.8  # Start conservative
        
        # Boundary-specific flow characteristics
        if boundary_type == BoundaryType.MEMORY:
            # Memory flow influenced by active memory count
            active_memories = cognitive_state.get('active_memory_count', 10)
            flow_boost = min(0.3, active_memories / 50.0)
            base_flow += flow_boost
        
        elif boundary_type == BoundaryType.PROCESSING:
            # Processing flow influenced by CPU usage
            cpu_usage = cognitive_state.get('cpu_utilization', 0.5)
            if cpu_usage > 0.8:
                base_flow *= 0.7  # Reduce flow under high CPU
            elif cpu_usage < 0.3:
                base_flow *= 1.2  # Increase flow under low CPU
        
        elif boundary_type == BoundaryType.OUTPUT:
            # Output flow influenced by expression readiness
            expression_readiness = cognitive_state.get('expression_readiness', 0.5)
            base_flow *= (0.5 + expression_readiness * 0.5)
        
        # Add slight randomness for natural variation
        noise = np.random.normal(0, 0.05)
        base_flow += noise
        
        return max(0.0, min(1.0, base_flow))
    
    def _calculate_filter_efficiency(self, boundary_type: BoundaryType, permeability: float) -> float:
        """Calculate filter efficiency for boundary"""
        
        # Lower permeability = higher filtering = higher efficiency
        base_efficiency = 1.0 - (permeability * 0.6)  # Inverse relationship
        
        # Boundary-specific efficiency characteristics
        if boundary_type == BoundaryType.INPUT:
            base_efficiency += 0.2  # Input filtering is naturally more efficient
        elif boundary_type == BoundaryType.DRIFT:
            base_efficiency += 0.3  # Drift filtering is very efficient
        elif boundary_type == BoundaryType.OUTPUT:
            base_efficiency -= 0.1  # Output filtering is less restrictive
        
        return max(0.1, min(1.0, base_efficiency))
    
    def _calculate_responsiveness(self, boundary_type: BoundaryType, pressure: float, shi: float) -> float:
        """Calculate boundary responsiveness score"""
        
        # High health and moderate pressure = high responsiveness
        health_component = shi * 0.6
        pressure_component = (1.0 - min(1.0, pressure / 100.0)) * 0.4
        
        responsiveness = health_component + pressure_component
        
        # Boundary-specific adjustments
        if boundary_type == BoundaryType.REFLECTION:
            responsiveness *= 1.2  # Reflection boundaries are naturally more responsive
        elif boundary_type == BoundaryType.DRIFT:
            responsiveness *= 0.8  # Drift boundaries are intentionally less responsive
        
        return max(0.1, min(1.0, responsiveness))
    
    def process_item(self, item: ProcessingItem) -> bool:
        """
        Process an item through the soft edge pipeline
        
        Args:
            item: Item to process
            
        Returns:
            True if item was successfully processed
        """
        try:
            self.current_state = EdgeState.FILTERING
            
            # Stage 1: Priority Queue
            if item.processing_stage == "priority_queue":
                # Check if item passes initial boundary filter
                boundary_type = self._determine_boundary_type(item)
                boundary_reading = self.boundary_states.get(boundary_type)
                
                if boundary_reading and boundary_reading.permeability > self.FILTER_THRESHOLD:
                    # Item passes - move to R.L filter
                    item.processing_stage = "rl_filter"
                    item.metadata["boundary_passed"] = boundary_type.value
                    item.metadata["permeability"] = boundary_reading.permeability
                    self.rl_filter_queue.append(item)
                    logger.debug(f"🌊 [EDGES] Item {item.item_id} passed to R.L filter")
                    return True
                else:
                    # Item filtered out
                    logger.debug(f"🌊 [EDGES] Item {item.item_id} filtered at boundary: {boundary_type.value}")
                    return False
            
            # Stage 2: R.L Filter (Rapid Learning Filter)
            elif item.processing_stage == "rl_filter":
                # Apply rapid learning filter logic
                if self._apply_rl_filter(item):
                    # Item passes - move to fractal memory
                    item.processing_stage = "fractal_memory"
                    self.fractal_memory_queue.append(item)
                    logger.debug(f"🌊 [EDGES] Item {item.item_id} passed to fractal memory")
                    return True
                else:
                    # Item filtered out by R.L filter
                    logger.debug(f"🌊 [EDGES] Item {item.item_id} filtered by R.L filter")
                    return False
            
            # Stage 3: Fractal Memory Storage
            elif item.processing_stage == "fractal_memory":
                return self._store_in_fractal_memory(item)
            
            return False
            
        except Exception as e:
            logger.error(f"🌊 [EDGES] Item processing error: {e}")
            return False
        finally:
            self.current_state = EdgeState.MONITORING
    
    def _determine_boundary_type(self, item: ProcessingItem) -> BoundaryType:
        """Determine which boundary type applies to an item"""
        
        item_type = item.item_type.lower()
        
        if "memory" in item_type:
            return BoundaryType.MEMORY
        elif "reflection" in item_type or "introspect" in item_type:
            return BoundaryType.REFLECTION
        elif "output" in item_type or "expression" in item_type:
            return BoundaryType.OUTPUT
        elif "input" in item_type or "stimulus" in item_type:
            return BoundaryType.INPUT
        elif "rebloom" in item_type:
            return BoundaryType.REBLOOM
        elif "drift" in item_type:
            return BoundaryType.DRIFT
        else:
            return BoundaryType.PROCESSING  # Default
    
    def _apply_rl_filter(self, item: ProcessingItem) -> bool:
        """Apply Rapid Learning (R.L) filter logic"""
        
        # R.L filter uses rapid pattern recognition to filter items
        
        # Priority-based filtering
        if item.priority < 0.3:
            return False  # Low priority items filtered out
        
        # Content-based filtering (simplified)
        content_str = str(item.content)
        
        # Filter out obviously redundant or low-value content
        if len(content_str) < 10:  # Too short
            return False
        
        if "error" in content_str.lower() and item.priority < 0.7:  # Low priority errors
            return False
        
        # Check for rapid learning patterns
        if item.metadata.get("learning_indicator", False):
            return True  # Learning items get priority
        
        if item.metadata.get("novel_pattern", False):
            return True  # Novel patterns get priority
        
        # Time-based filtering
        processing_time = time.time() - item.arrival_time
        if processing_time > 60.0 and item.priority < 0.5:  # Old, low priority items
            return False
        
        # Default pass for medium+ priority items
        return item.priority >= 0.4
    
    def _store_in_fractal_memory(self, item: ProcessingItem) -> bool:
        """Store item in fractal memory system"""
        
        try:
            if self.memory_manager:
                # Use the fractal memory manager to store the item
                memory_type = self._determine_memory_type(item)
                
                # Create memory fragment
                memory_fragment = {
                    "id": item.item_id,
                    "content": item.content,
                    "type": memory_type,
                    "priority": item.priority,
                    "metadata": item.metadata,
                    "timestamp": item.arrival_time,
                    "processing_time": time.time() - item.arrival_time
                }
                
                # Store in fractal memory (simplified - would use actual memory manager)
                logger.debug(f"🌊 [EDGES] Stored item {item.item_id} in fractal memory as {memory_type}")
                return True
            else:
                # Fallback storage (simplified)
                logger.debug(f"🌊 [EDGES] Stored item {item.item_id} in fallback storage")
                return True
                
        except Exception as e:
            logger.error(f"🌊 [EDGES] Fractal memory storage error: {e}")
            return False
    
    def _determine_memory_type(self, item: ProcessingItem) -> str:
        """Determine memory type for fractal storage"""
        
        item_type = item.item_type.lower()
        
        if "reflection" in item_type:
            return "reflection"
        elif "experience" in item_type:
            return "experience"
        elif "learning" in item_type:
            return "learning"
        elif "pattern" in item_type:
            return "pattern"
        elif "emotional" in item_type or "mood" in item_type:
            return "emotional"
        else:
            return "general"
    
    def add_to_pipeline(self, content: Any, priority: float = 0.5, 
                       item_type: str = "general", metadata: Dict[str, Any] = None) -> str:
        """
        Add an item to the processing pipeline
        
        Args:
            content: Content to process
            priority: Processing priority (0.0-1.0)
            item_type: Type of item
            metadata: Additional metadata
            
        Returns:
            Item ID for tracking
        """
        
        if metadata is None:
            metadata = {}
        
        item_id = f"edge_{int(time.time() * 1000)}_{len(self.priority_queue)}"
        
        item = ProcessingItem(
            item_id=item_id,
            content=content,
            priority=priority,
            item_type=item_type,
            arrival_time=time.time(),
            processing_stage="priority_queue",
            metadata=metadata
        )
        
        self.priority_queue.append(item)
        
        logger.debug(f"🌊 [EDGES] Added item {item_id} to pipeline (priority: {priority:.2f})")
        
        return item_id
    
    def tick_pipeline(self) -> PipelineMetrics:
        """
        Process pipeline tick - handle batch of items
        
        Returns:
            Pipeline performance metrics
        """
        start_time = time.time()
        
        try:
            processed_count = 0
            total_processing_time = 0.0
            
            # Process items from priority queue
            items_to_process = min(self.PROCESSING_BATCH_SIZE, len(self.priority_queue))
            for _ in range(items_to_process):
                if self.priority_queue:
                    item = self.priority_queue.popleft()
                    item_start = time.time()
                    
                    success = self.process_item(item)
                    
                    item_time = time.time() - item_start
                    total_processing_time += item_time
                    
                    if success:
                        processed_count += 1
            
            # Process items from R.L filter queue
            rl_items_to_process = min(self.PROCESSING_BATCH_SIZE // 2, len(self.rl_filter_queue))
            for _ in range(rl_items_to_process):
                if self.rl_filter_queue:
                    item = self.rl_filter_queue.popleft()
                    item_start = time.time()
                    
                    success = self.process_item(item)
                    
                    item_time = time.time() - item_start
                    total_processing_time += item_time
                    
                    if success:
                        processed_count += 1
            
            # Process items from fractal memory queue
            memory_items_to_process = min(self.PROCESSING_BATCH_SIZE // 4, len(self.fractal_memory_queue))
            for _ in range(memory_items_to_process):
                if self.fractal_memory_queue:
                    item = self.fractal_memory_queue.popleft()
                    item_start = time.time()
                    
                    success = self.process_item(item)
                    
                    item_time = time.time() - item_start
                    total_processing_time += item_time
                    
                    if success:
                        processed_count += 1
            
            # Calculate metrics
            tick_duration = time.time() - start_time
            
            avg_processing_time = total_processing_time / max(1, processed_count)
            throughput_rate = processed_count / max(0.001, tick_duration)
            
            # Determine bottleneck
            queue_sizes = {
                "priority_queue": len(self.priority_queue),
                "rl_filter": len(self.rl_filter_queue),
                "fractal_memory": len(self.fractal_memory_queue)
            }
            bottleneck_stage = max(queue_sizes, key=queue_sizes.get)
            
            # Calculate pressure backlog
            total_queue_size = sum(queue_sizes.values())
            pressure_backlog = min(1.0, total_queue_size / 500.0)  # Normalize to 0-1
            
            # Update pipeline metrics
            self.pipeline_metrics = PipelineMetrics(
                queue_length=total_queue_size,
                average_processing_time=avg_processing_time,
                filter_efficiency=self._calculate_overall_filter_efficiency(),
                throughput_rate=throughput_rate,
                bottleneck_stage=bottleneck_stage,
                pressure_backlog=pressure_backlog,
                memory_utilization=len(self.fractal_memory_queue) / 200.0  # Normalized
            )
            
            self.processing_count += processed_count
            self.last_pipeline_time = tick_duration
            
            if processed_count > 0:
                logger.debug(f"🌊 [EDGES] Pipeline tick: {processed_count} items, {throughput_rate:.1f} items/sec")
            
            return self.pipeline_metrics
            
        except Exception as e:
            logger.error(f"🌊 [EDGES] Pipeline tick error: {e}")
            return self.pipeline_metrics
    
    def _calculate_overall_filter_efficiency(self) -> float:
        """Calculate overall filter efficiency across all boundaries"""
        
        if not self.boundary_states:
            return 0.5
        
        efficiencies = [reading.filter_efficiency for reading in self.boundary_states.values()]
        return np.mean(efficiencies)
    
    def get_boundary_state(self, boundary_type: BoundaryType) -> Optional[BoundaryReading]:
        """Get current state of a specific boundary"""
        return self.boundary_states.get(boundary_type)
    
    def get_all_boundary_states(self) -> Dict[BoundaryType, BoundaryReading]:
        """Get current state of all boundaries"""
        return self.boundary_states.copy()
    
    def get_soft_edge_responsiveness(self) -> float:
        """
        Calculate overall soft edge responsiveness score for health monitoring
        
        Returns:
            Responsiveness score (0.0-1.0) for use in SHI calculation
        """
        
        if not self.boundary_states:
            return 0.5
        
        # Weight different boundary types by importance
        weights = {
            BoundaryType.MEMORY: 0.25,
            BoundaryType.REFLECTION: 0.20,
            BoundaryType.PROCESSING: 0.20,
            BoundaryType.OUTPUT: 0.15,
            BoundaryType.INPUT: 0.10,
            BoundaryType.REBLOOM: 0.05,
            BoundaryType.DRIFT: 0.05
        }
        
        weighted_responsiveness = 0.0
        
        for boundary_type, reading in self.boundary_states.items():
            weight = weights.get(boundary_type, 0.1)
            weighted_responsiveness += reading.responsiveness_score * weight
        
        # Add pipeline efficiency component
        pipeline_efficiency = (
            (1.0 - self.pipeline_metrics.pressure_backlog) * 0.3 +
            self.pipeline_metrics.filter_efficiency * 0.2 +
            min(1.0, self.pipeline_metrics.throughput_rate / 10.0) * 0.1
        )
        
        overall_responsiveness = weighted_responsiveness * 0.7 + pipeline_efficiency
        
        return max(0.0, min(1.0, overall_responsiveness))
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive soft edge system status"""
        
        return {
            "current_state": self.current_state.value,
            "boundary_count": len(self.boundary_states),
            "average_permeability": np.mean([r.permeability for r in self.boundary_states.values()]) if self.boundary_states else 0.0,
            "overall_responsiveness": self.get_soft_edge_responsiveness(),
            "pipeline_metrics": {
                "queue_length": self.pipeline_metrics.queue_length,
                "throughput_rate": self.pipeline_metrics.throughput_rate,
                "filter_efficiency": self.pipeline_metrics.filter_efficiency,
                "bottleneck_stage": self.pipeline_metrics.bottleneck_stage,
                "pressure_backlog": self.pipeline_metrics.pressure_backlog
            },
            "performance": {
                "adjustment_count": self.adjustment_count,
                "processing_count": self.processing_count,
                "last_adjustment_time_ms": self.last_adjustment_time * 1000,
                "last_pipeline_time_ms": self.last_pipeline_time * 1000
            },
            "system_integration": {
                "formula_engine": self.formula_engine is not None,
                "health_monitor": self.health_monitor is not None,
                "tracer_manager": self.tracer_manager is not None,
                "memory_manager": self.memory_manager is not None
            }
        }
    
    def emergency_seal_boundaries(self, reason: str = "Emergency protection"):
        """Emergency boundary sealing for protection"""
        
        logger.warning(f"🌊 [EDGES] EMERGENCY BOUNDARY SEALING: {reason}")
        
        self.current_state = EdgeState.EMERGENCY_SEALED
        
        # Set all boundaries to minimal permeability
        for boundary_type in self.boundary_states:
            reading = self.boundary_states[boundary_type]
            reading.permeability = 0.1  # Minimal permeability
            reading.permeability_level = PermeabilityLevel.SEALED
            reading.adjustment_factors["emergency_seal"] = -0.9
        
        # Clear processing queues
        self.priority_queue.clear()
        self.rl_filter_queue.clear()
        self.fractal_memory_queue.clear()
        
        logger.warning("🌊 [EDGES] All boundaries sealed, queues cleared")
    
    def restore_normal_boundaries(self):
        """Restore normal boundary operation after emergency"""
        
        if self.current_state == EdgeState.EMERGENCY_SEALED:
            logger.info("🌊 [EDGES] Restoring normal boundary operation")
            
            # Reset to base permeability
            for boundary_type in self.boundary_states:
                base_permeability = self.BASE_PERMEABILITY[boundary_type]
                reading = self.boundary_states[boundary_type]
                reading.permeability = base_permeability
                reading.permeability_level = self._classify_permeability(base_permeability)
                reading.adjustment_factors = {}
            
            self.current_state = EdgeState.MONITORING
            
            logger.info("🌊 [EDGES] Normal boundary operation restored")


# Global soft edge system instance
_global_soft_edge_system: Optional[SoftEdgeSystem] = None

def get_soft_edge_system() -> SoftEdgeSystem:
    """Get global soft edge system instance"""
    global _global_soft_edge_system
    if _global_soft_edge_system is None:
        _global_soft_edge_system = SoftEdgeSystem()
    return _global_soft_edge_system

def adjust_cognitive_boundaries(cognitive_state: Dict[str, Any]) -> Dict[BoundaryType, BoundaryReading]:
    """Convenience function to adjust cognitive boundaries"""
    system = get_soft_edge_system()
    return system.adjust_boundaries(cognitive_state)

def get_soft_edge_responsiveness() -> float:
    """Convenience function to get soft edge responsiveness for health monitoring"""
    system = get_soft_edge_system()
    return system.get_soft_edge_responsiveness()

def add_to_edge_pipeline(content: Any, priority: float = 0.5, item_type: str = "general") -> str:
    """Convenience function to add item to processing pipeline"""
    system = get_soft_edge_system()
    return system.add_to_pipeline(content, priority, item_type)

# Export key classes and functions
__all__ = [
    'SoftEdgeSystem',
    'BoundaryReading',
    'ProcessingItem',
    'BoundaryType',
    'PermeabilityLevel',
    'get_soft_edge_system',
    'adjust_cognitive_boundaries',
    'get_soft_edge_responsiveness',
    'add_to_edge_pipeline'
] 