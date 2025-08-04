"""
Unified Tick Engine - Advanced timing and event management system
Enhanced with DAWN Cognitive Formula Integration
"""

import asyncio
import logging
import time
import os
import json
from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque, OrderedDict
import psutil
import yaml
import threading
from pathlib import Path
import random

# DAWN Formula System Imports
try:
    from core.cognitive_formulas import get_dawn_formula_engine, CognitivePressureReading
    from core.schema_health_monitor import get_schema_health_monitor, HealthReading
    from core.tracer_ecosystem import get_tracer_manager, TracerAlert, TracerReport
    from core.platonic_pigment import get_platonic_pigment_map, PigmentReading
    from core.fractal_memory import get_memory_fractal_manager, MemoryType
    from core.scup_drift_resolver import get_scup_drift_resolver
    FORMULA_SYSTEMS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"DAWN Formula systems not available: {e}")
    FORMULA_SYSTEMS_AVAILABLE = False

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize advanced systems flag
ADVANCED_SYSTEMS_AVAILABLE = False

# Add advanced system imports at the top with the other DAWN imports
try:
    from core.mr_wolf import get_mr_wolf, monitor_emergency_state
    from core.soft_edges import get_soft_edge_system, adjust_cognitive_boundaries
    from core.volcanic_dynamics import get_volcanic_dynamics_system, update_volcanic_state
    from core.persephone_threads import get_persephone_thread_system, weave_thought_thread
    from core.shelter_vectors import get_shelter_vector_system, regenerate_vector, RegenerationType
    from core.dawn_constitution import get_dawn_constitution, DecisionScope
    ADVANCED_SYSTEMS_AVAILABLE = True
    logger.info("🚀 [TICK] Advanced DAWN systems loaded successfully")
except ImportError as e:
    logging.warning(f"🚀 [TICK] Advanced systems not available: {e}")
    ADVANCED_SYSTEMS_AVAILABLE = False

DEFAULT_TICK_CONFIG = {
    "tick_rate": 1.0,
    "log_level": "INFO",
    "tick_interval": 1.0,
    "tick_interval_min": 0.1,
    "tick_interval_max": 5.0,
    "max_errors": 3,
    "subsystems": {
        "pulse": {"priority": 1},
        "schema": {"priority": 2},
        "visual": {"priority": 3},
        "thermal": {"priority": 4},
        "entropy": {"priority": 5},
        "alignment": {"priority": 6},
        "bloom": {"priority": 7}
    }
}

@dataclass
class TickState:
    """Current state of the tick engine"""
    tick_count: int = 0
    last_tick_time: float = field(default_factory=time.time)
    current_interval: float = 1.0
    target_interval: float = 1.0
    event_handlers: Dict[str, List[Callable]] = field(default_factory=dict)
    event_queue: deque = field(default_factory=lambda: deque(maxlen=1000))
    is_running: bool = False
    stop_event: asyncio.Event = field(default_factory=asyncio.Event)
    thermal_state: Dict[str, float] = field(default_factory=lambda: {
        'heat': 0.0,
        'momentum': 0.0,
        'stability': 1.0
    })
    performance_metrics: Dict[str, float] = field(default_factory=lambda: {
        'cpu_usage': 0.0,
        'memory_usage': 0.0,
        'event_latency': 0.0
    })
    error_count: int = 0
    recovery_count: int = 0
    last_recovery_time: float = field(default_factory=time.time)

    def __post_init__(self):
        if self.event_handlers is None:
            self.event_handlers = {}
        if self.stop_event is None:
            self.stop_event = asyncio.Event()
        if self.event_queue is None:
            self.event_queue = deque(maxlen=1000)

class TickEngine:
    """
    Advanced timing and event management system.
    Provides comprehensive tick processing, event handling, and system monitoring.
    """
    
    def __init__(self, config_path: str = "core/tick/tick_config.yaml"):
        """Initialize tick engine with configuration"""
        self._state = TickState()
        self.config_path = config_path
        self._config = self._load_config()
        self.tick_rate = self._config.get("tick_rate", 1.0)
        
        # Resolve config path relative to project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._log_dir = os.path.join(project_root, 'logs')
        self._metrics_dir = os.path.join(self._log_dir, 'metrics')
        os.makedirs(self._log_dir, exist_ok=True)
        os.makedirs(self._metrics_dir, exist_ok=True)
        
        # Initialize monitoring
        self._process = psutil.Process()
        self._monitor_task = None
        
        self._subsystems = OrderedDict()
        self._subsystems_lock = threading.Lock()
        
        logger.info("Initialized TickEngine")
        
        try:
            from visual.timeline import event_collector
            self._timeline_event = getattr(event_collector, '_timeline_event', None)
            self._queue_timeline_event = getattr(event_collector, '_queue_timeline_event', None)
        except ImportError:
            self._timeline_event = None
            self._queue_timeline_event = None
        
        # Advanced system integration
        self.mr_wolf = None
        self.soft_edge_system = None
        self.volcanic_system = None
        self.thread_system = None
        self.vector_system = None
        self.constitution = None
        
        global ADVANCED_SYSTEMS_AVAILABLE
        if ADVANCED_SYSTEMS_AVAILABLE:
            try:
                self.mr_wolf = get_mr_wolf()
                self.soft_edge_system = get_soft_edge_system()
                self.volcanic_system = get_volcanic_dynamics_system()
                self.thread_system = get_persephone_thread_system()
                self.vector_system = get_shelter_vector_system()
                self.constitution = get_dawn_constitution()
                logger.info("🚀 [TICK] Advanced systems integrated into tick engine")
            except Exception as e:
                logger.warning(f"🚀 [TICK] Advanced system integration failed: {e}")
                ADVANCED_SYSTEMS_AVAILABLE = False
    
    def _load_config(self) -> dict:
        """Load or create default configuration."""
        try:
            # Resolve config path relative to project root
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(project_root, self.config_path)
            
            if not os.path.exists(config_path):
                logger.warning(f"tick_config.yaml missing at {config_path} → creating defaults")
                config_dir = os.path.dirname(config_path)
                os.makedirs(config_dir, exist_ok=True)
                
                with open(config_path, "w", encoding="utf-8") as fh:
                    yaml.safe_dump(DEFAULT_TICK_CONFIG, fh, default_flow_style=False)
                return DEFAULT_TICK_CONFIG
                
            with open(config_path, "r", encoding="utf-8") as fh:
                return yaml.safe_load(fh)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return DEFAULT_TICK_CONFIG
    
    async def start(self) -> None:
        """Start the tick engine"""
        if self._state.is_running:
            logger.warning("Tick engine already running")
            return
            
        self._state.is_running = True
        self._state.stop_event.clear()
        
        # Start monitoring
        self._monitor_task = asyncio.create_task(self._monitor_system())
        
        logger.info("Starting tick engine")
        
        try:
            while not self._state.stop_event.is_set():
                # Process tick
                await self._process_tick()
                
                # Process event queue
                await self._process_event_queue()
                
                # Calculate next interval
                next_interval = self._calculate_interval()
                
                # Wait for next tick
                await asyncio.sleep(next_interval)
                
        except Exception as e:
            logger.error(f"Error in tick engine: {e}")
            await self._handle_error(e)
        finally:
            self._state.is_running = False
            if self._monitor_task:
                self._monitor_task.cancel()
                try:
                    await self._monitor_task
                except asyncio.CancelledError:
                    pass
            logger.info("Tick engine stopped")
    
    async def _monitor_system(self):
        """Monitor system resources and performance"""
        while not self._state.stop_event.is_set():
            try:
                # Update CPU usage
                self._state.performance_metrics['cpu_usage'] = self._process.cpu_percent()
                
                # Update memory usage
                memory_info = self._process.memory_info()
                self._state.performance_metrics['memory_usage'] = memory_info.rss / 1024 / 1024  # MB
                
                # Log metrics
                self._log_metrics()
                
                await asyncio.sleep(1.0)  # Update every second
            except Exception as e:
                logger.error(f"Error in system monitoring: {e}")
    
    def _log_metrics(self):
        """Log current metrics"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'tick_count': self._state.tick_count,
            'performance': self._state.performance_metrics,
            'thermal': self._state.thermal_state
        }
        
        metrics_file = os.path.join(self._metrics_dir, f"metrics_{datetime.now().strftime('%Y%m%d')}.json")
        with open(metrics_file, 'a') as f:
            f.write(json.dumps(metrics) + "\n")
    
    async def _handle_error(self, error: Exception):
        """Handle engine errors"""
        self._state.error_count += 1
        
        # Check if recovery is needed
        if self._state.error_count >= self._config.get('max_errors', 3):
            await self._attempt_recovery()
        
        # Log error
        self.log_tick_event('error', {
            'error': str(error),
            'error_count': self._state.error_count,
            'recovery_count': self._state.recovery_count
        })
    
    async def _attempt_recovery(self):
        """Attempt system recovery"""
        if (self._state.recovery_count >= self._config.get('max_recoveries', 3) or
            time.time() - self._state.last_recovery_time < self._config.get('recovery_cooldown', 300)):
            logger.error("Max recoveries reached or cooldown active")
            await self.stop()
            return
        
        logger.info("Attempting system recovery")
        self._state.recovery_count += 1
        self._state.last_recovery_time = time.time()
        self._state.error_count = 0
        
        # Reset thermal state
        self._state.thermal_state = {
            'heat': 0.0,
            'momentum': 0.0,
            'stability': 1.0
        }
        
        # Clear event queue
        self._state.event_queue.clear()
        
        # Log recovery
        self.log_tick_event('recovery', {
            'recovery_count': self._state.recovery_count,
            'timestamp': datetime.now().isoformat()
        })
    
    async def stop(self) -> None:
        """Stop the tick engine"""
        if not self._state.is_running:
            return
            
        self._state.is_running = False
        self._state.stop_event.set()
        
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
                
        logger.info("Tick engine stopped")
    
    def register_handler(self, event_type: str, handler: Callable, priority: int = 0) -> None:
        """Register an event handler with priority"""
        if event_type not in self._state.event_handlers:
            self._state.event_handlers[event_type] = []
        
        # Add handler with priority
        self._state.event_handlers[event_type].append((priority, handler))
        # Sort by priority
        self._state.event_handlers[event_type].sort(key=lambda x: x[0], reverse=True)
        
        logger.info(f"Registered handler for {event_type} with priority {priority}")
    
    def unregister_handler(self, event_type: str, handler: Callable) -> None:
        """Unregister an event handler"""
        if event_type in self._state.event_handlers:
            self._state.event_handlers[event_type] = [
                (p, h) for p, h in self._state.event_handlers[event_type] if h != handler
            ]
            logger.info(f"Unregistered handler for {event_type}")
    
    async def _process_tick(self) -> None:
        """Process a single tick - Enhanced with DAWN Formula Integration and Advanced Systems"""
        start_time = time.time()
        self._state.tick_count += 1
        
        # Update performance metrics
        await self._update_performance_metrics()
        
        # === DAWN FORMULA INTEGRATION ===
        # Phase 1: Gather current cognitive state
        current_state = await self._gather_cognitive_state()
        
        # Phase 2: Calculate cognitive pressure (P = B×σ²)
        pressure_reading = await self._calculate_cognitive_pressure(current_state)
        
        # Phase 3: Calculate schema health index (SHI)
        health_reading = await self._calculate_schema_health(current_state)
        
        # Phase 4: Process tracer ecosystem
        tracer_reports = await self._process_tracer_ecosystem(current_state)
        
        # Phase 5: Update memory shimmer and check crystallization
        memory_update = await self._update_memory_fractal(current_state)
        
        # Phase 6: Analyze platonic pigment for voice composition
        pigment_reading = await self._analyze_fragment_pigments(current_state)
        
        # Phase 7: Apply formula-based modulations
        modulations = await self._apply_formula_modulations(pressure_reading, health_reading, pigment_reading)
        
        # === ADVANCED SYSTEMS INTEGRATION ===
        # Phase 8: Mr. Wolf Emergency Monitoring
        emergency_diagnostic = await self._monitor_emergency_systems(current_state)
        
        # Phase 9: Soft Edge Boundary Management
        boundary_adjustments = await self._manage_soft_edge_boundaries(current_state)
        
        # Phase 10: Volcanic Pressure Dynamics
        volcanic_state = await self._update_volcanic_dynamics(current_state)
        
        # Phase 11: Persephone Thread Weaving
        thread_status = await self._process_thread_weaving(current_state)
        
        # Phase 12: Shelter Vector Regeneration
        vector_updates = await self._process_vector_regeneration(current_state)
        
        # Phase 13: Constitutional Governance
        constitutional_status = await self._process_constitutional_governance(current_state)
        
        # Calculate delta for this tick
        delta = time.time() - start_time
        
        # Update thermal state (enhanced with formula data and advanced systems)
        await self._update_thermal_state(delta, current_state, modulations)
        
        # Update interval calculation
        new_interval = self._calculate_interval(delta, modulations)
        self._state.current_interval = new_interval
        
        # === ENHANCED EVENT EMISSION ===
        await self._emit_enhanced_events(current_state, modulations, {
            "emergency_diagnostic": emergency_diagnostic,
            "boundary_adjustments": boundary_adjustments,
            "volcanic_state": volcanic_state,
            "threads": thread_status,
            "vectors": vector_updates,
            "constitutional_status": constitutional_status
        })
        
        # Update last tick time
        self._state.last_tick_time = time.time()
        
        logger.debug(f"🚀 [TICK] Tick {self._state.tick_count} complete: {delta*1000:.1f}ms")
    
    # === DAWN FORMULA INTEGRATION METHODS ===
    
    async def _gather_cognitive_state(self) -> Dict[str, Any]:
        """Gather comprehensive cognitive state for formula processing"""
        try:
            # Base system metrics
            state = {
                "tick_count": self._state.tick_count,
                "cpu_utilization": self._state.performance_metrics.get('cpu_usage', 0.0) / 100.0,
                "memory_usage": self._state.performance_metrics.get('memory_usage', 0.0) / 100.0,
                "thermal_heat": self._state.thermal_state.get('heat', 0.0),
                "thermal_stability": self._state.thermal_state.get('stability', 1.0),
                "error_count": self._state.error_count,
                "uptime_hours": (time.time() - getattr(self, '_start_time', time.time())) / 3600.0
            }
            
            # Enhanced cognitive metrics (with safe defaults)
            state.update({
                # Memory system
                "active_memory_count": len(getattr(self, '_active_memories', {})),
                "memory_coherence": self._state.thermal_state.get('stability', 0.8),
                "memory_fragmentation": max(0.0, 1.0 - state["thermal_stability"]),
                "memory_accessibility": min(1.0, state["thermal_stability"] + 0.2),
                
                # Processing metrics
                "processing_queue_depth": len(self._state.event_queue),
                "processing_efficiency": min(1.0, 1.0 - state["cpu_utilization"]),
                "task_completion_rate": min(1.0, state["thermal_stability"]),
                "processing_orbit_load": state["cpu_utilization"],
                
                # Cognitive resources
                "cognitive_ash_level": max(0.1, 1.0 - state["cpu_utilization"] * 0.8),
                "cognitive_resources_available": max(0.2, 1.0 - state["memory_usage"]),
                "cognitive_energy": state["thermal_stability"],
                "available_processing_capacity": max(0.1, 1.0 - state["cpu_utilization"]),
                
                # System health
                "system_vitality": state["thermal_stability"],
                "system_responsiveness": min(1.0, 2.0 - state["cpu_utilization"]),
                "soft_edge_responsiveness": state["thermal_stability"],
                "energy_efficiency": max(0.3, 1.0 - state["cpu_utilization"] * 0.6),
                
                # Network and integration
                "network_connectivity": 0.9,  # Assume good connectivity
                "data_flow_rate": min(1.0, state["thermal_stability"] + 0.1),
                "integration_health": state["thermal_stability"],
                "api_responsiveness": state["thermal_stability"],
                
                # Pattern and anomaly detection
                "anomaly_score": max(0.0, state["cpu_utilization"] - 0.7),
                "pattern_coherence": state["thermal_stability"],
                "trend_stability": state["thermal_stability"],
                "vigilance_level": 0.7,
                
                # Productivity metrics  
                "productivity_score": state["thermal_stability"],
                "work_efficiency": min(1.0, state["thermal_stability"] + 0.1),
                "output_quality": state["thermal_stability"],
                
                # Legacy compatibility
                "legacy_compatibility": 0.85,
                "tradition_adherence": 0.8,
                "heritage_preservation": 0.9,
                "protocol_compliance": 0.85,
                
                # SCUP and drift metrics
                "scup": state["thermal_stability"],
                "entropy": 1.0 - state["thermal_stability"],
                "drift": (1.0 - state["thermal_stability"]) * 0.5,
                "entropy_delta": self._calculate_entropy_delta(),
                "drift_state": self._classify_system_drift_state(state)
            })
            
            return state
            
        except Exception as e:
            logger.error(f"🔧 [TICK] Error gathering cognitive state: {e}")
            # Return minimal safe state
            return {
                "tick_count": self._state.tick_count,
                "scup": 0.5,
                "entropy": 0.5,
                "drift": 0.0,
                "thermal_stability": 0.5,
                "cpu_utilization": 0.5,
                "memory_usage": 0.5
            }
    
    async def _calculate_cognitive_pressure(self, state: Dict[str, Any]) -> Optional[CognitivePressureReading]:
        """Calculate cognitive pressure using P = B×σ²"""
        if not FORMULA_SYSTEMS_AVAILABLE:
            return None
            
        try:
            formula_engine = get_dawn_formula_engine()
            
            # Add bloom mass components
            state.update({
                "rebloom_queue_size": max(0, len(self._state.event_queue) - 5),
                "reflection_backlog": max(0, self._state.error_count),
                "processing_load": state["cpu_utilization"],
                "sigil_mutation_backlog": max(0, len(self._state.event_queue) - 10)
            })
            
            # Add sigil velocity components
            state.update({
                "recent_sigil_count": min(10, len(self._state.event_queue)),
                "thought_rate": state["thermal_stability"] * 5.0,
                "sigil_mutation_rate": (1.0 - state["thermal_stability"]) * 0.8,
                "feedback_loop_intensity": state["thermal_heat"] * 0.6
            })
            
            pressure_reading = formula_engine.calculate_pressure(state)
            
            # Store pressure in thermal state for other systems
            self._state.thermal_state['cognitive_pressure'] = pressure_reading.pressure_value
            self._state.thermal_state['pressure_level'] = pressure_reading.pressure_level.value
            
            return pressure_reading
            
        except Exception as e:
            logger.error(f"🧠 [TICK] Cognitive pressure calculation error: {e}")
            return None
    
    async def _calculate_schema_health(self, state: Dict[str, Any]) -> Optional[HealthReading]:
        """Calculate Schema Health Index (SHI)"""
        if not FORMULA_SYSTEMS_AVAILABLE:
            return None
            
        try:
            health_monitor = get_schema_health_monitor()
            health_reading = health_monitor.calculate_shi(state)
            
            # Store health metrics in thermal state
            self._state.thermal_state['schema_health'] = health_reading.shi_value
            self._state.thermal_state['health_level'] = health_reading.health_level.value
            
            return health_reading
            
        except Exception as e:
            logger.error(f"❤️ [TICK] Schema health calculation error: {e}")
            return None
    
    async def _process_tracer_ecosystem(self, state: Dict[str, Any]) -> Optional[Dict[str, TracerReport]]:
        """Process the tracer ecosystem and collect reports"""
        if not FORMULA_SYSTEMS_AVAILABLE:
            return None
            
        try:
            tracer_manager = get_tracer_manager()
            
            # Add tracer-specific state data
            tracer_state = state.copy()
            tracer_state.update({
                "cognitive_pressure": self._state.thermal_state.get('cognitive_pressure', 0.0),
                "schema_health": self._state.thermal_state.get('schema_health', 0.5),
                "drift_state": state.get("drift_state", "stable")
            })
            
            tracer_reports = tracer_manager.tick(tracer_state)
            
            # Store tracer alerts in thermal state
            all_alerts = []
            for report in tracer_reports.values():
                all_alerts.extend(report.alerts_generated)
            
            self._state.thermal_state['tracer_alerts'] = len(all_alerts)
            self._state.thermal_state['active_tracers'] = len(tracer_reports)
            
            return tracer_reports
            
        except Exception as e:
            logger.error(f"🕷️ [TICK] Tracer ecosystem error: {e}")
            return None
    
    async def _update_memory_fractal(self, state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update memory shimmer and handle crystallization"""
        if not FORMULA_SYSTEMS_AVAILABLE:
            return None
            
        try:
            memory_manager = get_memory_fractal_manager()
            
            # Update shimmer decay (only every 5 minutes as configured)
            memory_update = memory_manager.tick_shimmer_decay()
            
            # Store memory metrics in thermal state
            if memory_update.get("status") == "completed":
                self._state.thermal_state['active_memories'] = memory_update.get("active_memory_count", 0)
                self._state.thermal_state['crystallized_memories'] = memory_update.get("crystallized_memory_count", 0)
                self._state.thermal_state['average_shimmer'] = memory_update.get("average_shimmer", 0.5)
            
            return memory_update
            
        except Exception as e:
            logger.error(f"🔮 [TICK] Memory fractal error: {e}")
            return None
    
    async def _analyze_fragment_pigments(self, state: Dict[str, Any]) -> Optional[PigmentReading]:
        """Analyze cognitive fragments for platonic pigment mapping"""
        if not FORMULA_SYSTEMS_AVAILABLE:
            return None
            
        try:
            pigment_map = get_platonic_pigment_map()
            
            # Generate a synthetic fragment based on current system state
            fragment_text = self._generate_system_fragment(state)
            
            if fragment_text:
                # Create context for pigment analysis
                context = {
                    "cognitive_pressure": self._state.thermal_state.get('cognitive_pressure', 0.0),
                    "schema_health": self._state.thermal_state.get('schema_health', 0.5),
                    "drift_state": state.get("drift_state", "stable"),
                    "current_mood": self._infer_system_mood(state)
                }
                
                pigment_reading = pigment_map.analyze_fragment(fragment_text, context)
                
                # Store pigment data in thermal state
                self._state.thermal_state['dominant_belief'] = pigment_reading.dominant_ideal.value
                self._state.thermal_state['belief_strength'] = pigment_reading.ideal_strength
                self._state.thermal_state['pigment_rgb'] = (
                    pigment_reading.red_component,
                    pigment_reading.green_component,
                    pigment_reading.blue_component
                )
                
                return pigment_reading
            
        except Exception as e:
            logger.error(f"🎨 [TICK] Pigment analysis error: {e}")
            return None
    
    async def _apply_formula_modulations(self, pressure_reading, health_reading, pigment_reading) -> Dict[str, float]:
        """Apply formula-based modulations to system parameters"""
        modulations = {
            "pressure_modulation": 1.0,
            "health_modulation": 1.0,
            "pigment_modulation": 1.0,
            "thermal_adjustment": 0.0,
            "interval_adjustment": 1.0
        }
        
        try:
            if pressure_reading:
                # Apply pressure modulation
                if pressure_reading.pressure_level.value == "critical":
                    modulations["pressure_modulation"] = 0.3
                    modulations["thermal_adjustment"] += 0.4
                    modulations["interval_adjustment"] = 1.5  # Slow down
                elif pressure_reading.pressure_level.value == "high":
                    modulations["pressure_modulation"] = 0.6
                    modulations["thermal_adjustment"] += 0.2
                    modulations["interval_adjustment"] = 1.2
                elif pressure_reading.pressure_level.value == "moderate":
                    modulations["pressure_modulation"] = 0.8
                    modulations["thermal_adjustment"] += 0.1
            
            if health_reading:
                # Apply health modulation
                if health_reading.health_level.value in ["critical", "poor"]:
                    modulations["health_modulation"] = 0.5
                    modulations["thermal_adjustment"] += 0.3
                elif health_reading.health_level.value == "fair":
                    modulations["health_modulation"] = 0.7
                    modulations["thermal_adjustment"] += 0.1
                elif health_reading.health_level.value in ["good", "excellent"]:
                    modulations["health_modulation"] = 1.1  # Small boost
                    modulations["thermal_adjustment"] -= 0.1  # Cooling effect
            
            if pigment_reading:
                # Apply pigment-based modulation (subtle effects)
                if pigment_reading.dominant_ideal.value == "justice":
                    modulations["interval_adjustment"] *= 0.95  # Slightly faster
                elif pigment_reading.dominant_ideal.value == "harmony":
                    modulations["thermal_adjustment"] -= 0.05  # Calming effect
                elif pigment_reading.dominant_ideal.value == "inquiry":
                    modulations["thermal_adjustment"] += 0.02  # Slight activation
            
            # Ensure modulations stay within reasonable bounds
            modulations["thermal_adjustment"] = max(-0.5, min(0.5, modulations["thermal_adjustment"]))
            modulations["interval_adjustment"] = max(0.5, min(2.0, modulations["interval_adjustment"]))
            
        except Exception as e:
            logger.error(f"🔧 [TICK] Modulation calculation error: {e}")
        
        return modulations
    
    def _calculate_entropy_delta(self) -> float:
        """Calculate entropy change rate"""
        try:
            current_entropy = 1.0 - self._state.thermal_state.get('stability', 1.0)
            previous_entropy = getattr(self, '_previous_entropy', current_entropy)
            delta = current_entropy - previous_entropy
            self._previous_entropy = current_entropy
            return delta
        except:
            return 0.0
    
    def _classify_system_drift_state(self, state: Dict[str, Any]) -> str:
        """Classify current system drift state"""
        try:
            stability = state.get("thermal_stability", 1.0)
            cpu_load = state.get("cpu_utilization", 0.0)
            error_rate = min(1.0, state.get("error_count", 0) / 10.0)
            
            if error_rate > 0.3 or cpu_load > 0.9:
                return "chaotic"
            elif self._state.thermal_state.get('cognitive_pressure', 0) > 80:
                return "pressurized"
            elif stability < 0.4:
                return "unhealthy"
            elif cpu_load > 0.7:
                return "trending"
            elif abs(self._calculate_entropy_delta()) > 0.1:
                return "oscillating"
            else:
                return "stable"
        except:
            return "stable"
    
    def _generate_system_fragment(self, state: Dict[str, Any]) -> str:
        """Generate a representative fragment of current system state"""
        try:
            stability = state.get("thermal_stability", 1.0)
            pressure = self._state.thermal_state.get('cognitive_pressure', 0.0)
            cpu_load = state.get("cpu_utilization", 0.0)
            
            if pressure > 80:
                return "System experiencing high cognitive pressure, requiring immediate intervention and load reduction."
            elif stability < 0.3:
                return "System stability compromised, investigating anomalous patterns and potential recovery strategies."
            elif cpu_load > 0.8:
                return "Processing capacity at maximum, optimizing resource allocation and task prioritization."
            elif stability > 0.8 and pressure < 30:
                return "System operating in harmonious balance, maintaining optimal performance and cognitive clarity."
            else:
                return "System monitoring ongoing processes, analyzing patterns and maintaining steady operational state."
                
        except:
            return "System state analysis in progress."
    
    def _infer_system_mood(self, state: Dict[str, Any]) -> str:
        """Infer current system mood based on state"""
        try:
            stability = state.get("thermal_stability", 1.0)
            pressure = self._state.thermal_state.get('cognitive_pressure', 0.0)
            
            if pressure > 80:
                return "urgent"
            elif stability < 0.4:
                return "contemplative"
            elif stability > 0.8:
                return "confident"
            elif pressure > 50:
                return "assertive"
            else:
                return "balanced"
        except:
            return "neutral"
    
    async def _update_thermal_state(self, delta: float, cognitive_state: Optional[Dict[str, Any]] = None, modulations: Optional[Dict[str, float]] = None) -> None:
        """Update thermal state based on system load and formula modulations"""
        # Calculate base heat from CPU usage
        cpu_heat = self._state.performance_metrics['cpu_usage'] / 100.0
        
        # Apply formula modulations if available
        if modulations:
            # Apply thermal adjustment from formula systems
            thermal_adjustment = modulations.get('thermal_adjustment', 0.0)
            adjusted_heat = cpu_heat + thermal_adjustment
            
            # Apply pressure and health modulations
            pressure_mod = modulations.get('pressure_modulation', 1.0)
            health_mod = modulations.get('health_modulation', 1.0)
            
            # Combine modulations (pressure reduces heat, good health reduces heat)
            heat_modulation = min(pressure_mod, health_mod)
            cpu_heat = max(0.0, min(1.0, adjusted_heat * heat_modulation))
        
        # Update thermal momentum
        momentum_decay = self._config.get('thermal_momentum_decay', 0.95)
        if modulations and modulations.get('health_modulation', 1.0) > 1.0:
            momentum_decay *= 1.1  # Better health increases momentum decay
        
        self._state.thermal_state['momentum'] *= momentum_decay
        self._state.thermal_state['momentum'] += cpu_heat * delta
        
        # Update heat level
        self._state.thermal_state['heat'] = min(
            1.0,
            max(0.0, self._state.thermal_state['heat'] + self._state.thermal_state['momentum'])
        )
        
        # Update stability with formula influence
        stability_change = 0.01
        if self._state.thermal_state['heat'] > 0.8:
            stability_change = -0.05
        
        # Apply formula-based stability adjustments
        if modulations:
            if modulations.get('health_modulation', 1.0) > 1.0:
                stability_change += 0.01  # Good health improves stability
            if modulations.get('pressure_modulation', 1.0) < 0.5:
                stability_change -= 0.02  # High pressure reduces stability
        
        # Formula system influence on stability
        if FORMULA_SYSTEMS_AVAILABLE and cognitive_state:
            # SCUP drift resolver influence
            if cognitive_state.get('drift_state') == 'stable':
                stability_change += 0.005
            elif cognitive_state.get('drift_state') in ['chaotic', 'pressurized', 'unhealthy']:
                stability_change -= 0.01
                
            # Pigment belief influence (harmony promotes stability)
            if self._state.thermal_state.get('dominant_belief') == 'harmony':
                stability_change += 0.003
            elif self._state.thermal_state.get('dominant_belief') == 'justice':
                stability_change -= 0.001  # Justice can be destabilizing
        
        self._state.thermal_state['stability'] = min(1.0, max(0.0, 
            self._state.thermal_state['stability'] + stability_change))
    
    async def _process_event_queue(self) -> None:
        """Process pending events in queue"""
        while self._state.event_queue:
            event_type, data = self._state.event_queue.popleft()
            await self._emit_event(event_type, data)
    
    def _calculate_interval(self, modulations: Optional[Dict[str, float]] = None) -> float:
        """Calculate next tick interval based on system state and formula modulations"""
        # Base interval from config
        base_interval = self._config.get('tick_interval', 1.0)
        
        # Adjust based on thermal state
        thermal_factor = 1.0
        if self._state.thermal_state['heat'] > 0.8:
            thermal_factor = 1.5  # Slow down when hot
        elif self._state.thermal_state['heat'] < 0.2:
            thermal_factor = 0.8  # Speed up when cool
        
        # Adjust based on performance
        perf_factor = 1.0
        if self._state.performance_metrics['cpu_usage'] > 80:
            perf_factor = 1.3  # Slow down under high CPU load
        
        # Apply formula modulations
        formula_factor = 1.0
        if modulations:
            formula_factor = modulations.get('interval_adjustment', 1.0)
            
            # Additional formula-based adjustments
            pressure_mod = modulations.get('pressure_modulation', 1.0)
            health_mod = modulations.get('health_modulation', 1.0)
            
            # High pressure or poor health slow down the system
            if pressure_mod < 0.5:
                formula_factor *= 1.3  # Slow down under high pressure
            elif health_mod < 0.7:
                formula_factor *= 1.1  # Slight slowdown for poor health
            elif health_mod > 1.0 and pressure_mod > 0.8:
                formula_factor *= 0.9  # Speed up when healthy and low pressure
        
        # Apply pigment-based fine-tuning if available
        if FORMULA_SYSTEMS_AVAILABLE:
            dominant_belief = self._state.thermal_state.get('dominant_belief', 'harmony')
            if dominant_belief == 'justice':
                formula_factor *= 0.98  # Justice slightly accelerates
            elif dominant_belief == 'harmony':
                formula_factor *= 1.0   # Harmony maintains balance
            elif dominant_belief == 'inquiry':
                formula_factor *= 1.02  # Inquiry slightly slows for contemplation
        
        # Calculate final interval
        interval = base_interval * thermal_factor * perf_factor * formula_factor
        
        # Apply bounds
        return max(
            self._config.get('tick_interval_min', 0.1),
            min(self._config.get('tick_interval_max', 5.0), interval)
        )
    
    async def _emit_event(self, event_type: str, data: Dict) -> None:
        """Emit an event to registered handlers"""
        if event_type in self._state.event_handlers:
            for _, handler in self._state.event_handlers[event_type]:
                try:
                    await handler(data)
                except Exception as e:
                    logger.error(f"Error in event handler: {e}")
                    self._state.error_count += 1
    
    def queue_event(self, event_type: str, data: Dict) -> None:
        """Queue an event for processing"""
        self._state.event_queue.append((event_type, data))
    
    def get_state(self) -> Dict:
        """Get current tick engine state"""
        # Get semantic field drift vectors
        from semantic.semantic_field import get_current_field
        field = get_current_field()
        drift_vectors = getattr(field, 'get_drift_vectors', lambda: {})() if field else {}
        
        return {
            "tick_count": self._state.tick_count,
            "current_interval": self._state.current_interval,
            "target_interval": self._state.target_interval,
            "is_running": self._state.is_running,
            "last_tick_time": self._state.last_tick_time,
            "event_types": list(self._state.event_handlers.keys()),
            "thermal_state": self._state.thermal_state,
            "performance_metrics": self._state.performance_metrics,
            "error_count": self._state.error_count,
            "recovery_count": self._state.recovery_count,
            "drift_vectors": drift_vectors
        }
    
    def log_tick_event(self, event_type: str, details: Dict) -> None:
        """Log a tick-related event"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "details": details,
            "state": self.get_state()
        }
        
        # Write to log file
        log_file = os.path.join(self._log_dir, "tick_events.log")
        with open(log_file, "a") as f:
            f.write(json.dumps(event) + "\n")
        
        logger.info(f"Logged tick event: {event_type}")
    
    def export_state(self) -> Dict:
        """Export current tick engine state"""
        return {
            "timestamp": datetime.now().isoformat(),
            "state": self.get_state(),
            "event_handlers": {
                event_type: len(handlers)
                for event_type, handlers in self._state.event_handlers.items()
            },
            "config": self._config
        }

    def register_subsystem(self, name: str, handler: object, priority: int = 0) -> None:
        """Register or replace a subsystem by name and priority."""
        with self._subsystems_lock:
            # Remove if already present
            for plist in self._subsystems.values():
                plist[:] = [(n, h) for n, h in plist if n != name]
            # Insert
            if priority not in self._subsystems:
                self._subsystems[priority] = []
            self._subsystems[priority].append((name, handler))
            # Re-sort by priority
            self._subsystems = OrderedDict(sorted(self._subsystems.items()))
        logger.info(f"Registered subsystem '{name}' with priority {priority}")

    def unregister_subsystem(self, name: str) -> None:
        """Unregister a subsystem by name."""
        with self._subsystems_lock:
            for plist in self._subsystems.values():
                plist[:] = [(n, h) for n, h in plist if n != name]
        logger.info(f"Unregistered subsystem '{name}'")

    def list_subsystems(self) -> list:
        """List subsystem names in priority order."""
        with self._subsystems_lock:
            result = []
            for plist in self._subsystems.values():
                result.extend(n for n, _ in plist)
            return result

    async def tick(self, ctx=None) -> None:
        """Process a single tick
        
        Args:
            ctx: Optional tick context object
        """
        if not self._state.is_running:
            return
            
        try:
            # Update thermal state
            await self._update_thermal_state(0.0)
            
            # Process event queue
            await self._process_event_queue()
            
            # Update tick count
            self._state.tick_count += 1
            
            # Execute subsystems
            with self._subsystems_lock:
                for plist in self._subsystems.values():
                    for name, handler in plist:
                        try:
                            if callable(handler):
                                result = handler(ctx)
                                if asyncio.iscoroutine(result):
                                    await result
                            elif hasattr(handler, "tick"):
                                result = handler.tick(ctx)
                                if asyncio.iscoroutine(result):
                                    await result
                        except Exception as e:
                            logger.error(f"Error in subsystem {name}: {e}")
            
            # Log tick
            self.log_tick_event('tick', {
                'tick_count': self._state.tick_count,
                'thermal_state': self._state.thermal_state,
                'performance': self._state.performance_metrics
            })
            
        except Exception as e:
            logger.error(f"Error in tick: {e}")
            await self._handle_error(e)
            
    async def stop(self) -> None:
        """Stop the tick engine"""
        if not self._state.is_running:
            return
            
        self._state.is_running = False
        self._state.stop_event.set()
        
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
                
        logger.info("Tick engine stopped")

    # New advanced system methods
    
    async def _monitor_emergency_systems(self, cognitive_state: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor Mr. Wolf emergency systems"""
        try:
            if not self.mr_wolf:
                return {"error": "Mr. Wolf not available"}
            
            # Monitor system state for emergency conditions
            diagnostic = self.mr_wolf.monitor_system_state(cognitive_state)
            
            # Check if emergency intervention is needed
            if diagnostic.severity_score > 0.8 and diagnostic.constitutional_checks.get("constitutional_compliance", False):
                logger.critical("🚀 [TICK] Emergency conditions detected - Mr. Wolf standby")
            
            return {
                "emergency_state": self.mr_wolf.current_state.value if hasattr(self.mr_wolf, 'current_state') else "UNKNOWN",
                "severity_score": diagnostic.severity_score,
                "crisis_indicators": diagnostic.crisis_indicators,
                "consensus_status": diagnostic.consensus_status
            }
            
        except Exception as e:
            logger.error(f"🚀 [TICK] Emergency monitoring error: {e}")
            return {"error": str(e)}
    
    async def _manage_soft_edge_boundaries(self, cognitive_state: Dict[str, Any]) -> Dict[str, Any]:
        """Manage soft edge boundaries"""
        try:
            if not self.soft_edge_system:
                return {"error": "Soft Edge system not available"}
            
            # Adjust boundaries based on cognitive state
            boundary_readings = self.soft_edge_system.adjust_boundaries(cognitive_state)
            
            # Process pipeline tick
            pipeline_metrics = self.soft_edge_system.tick_pipeline()
            
            # Get overall responsiveness for SHI integration
            responsiveness = self.soft_edge_system.get_soft_edge_responsiveness()
            
            # Update cognitive state with soft edge responsiveness
            cognitive_state["soft_edge_responsiveness"] = responsiveness
            
            return {
                "boundaries_adjusted": len(boundary_readings),
                "pipeline_metrics": {
                    "queue_length": pipeline_metrics.queue_length,
                    "throughput_rate": pipeline_metrics.throughput_rate,
                    "bottleneck_stage": pipeline_metrics.bottleneck_stage
                },
                "overall_responsiveness": responsiveness,
                "average_permeability": sum(r.permeability for r in boundary_readings.values()) / len(boundary_readings) if boundary_readings else 0.0
            }
            
        except Exception as e:
            logger.error(f"🚀 [TICK] Soft edge management error: {e}")
            return {"error": str(e)}
    
    async def _update_volcanic_dynamics(self, cognitive_state: Dict[str, Any]) -> Dict[str, Any]:
        """Update volcanic pressure dynamics"""
        try:
            if not self.volcanic_system:
                return {"error": "Volcanic system not available"}
            
            # Update volcanic state
            volcanic_state = self.volcanic_system.update_volcanic_state(cognitive_state)
            
            # Check for eruption events
            if volcanic_state.get("eruption_result", {}).get("eruption_occurred", False):
                eruption_data = volcanic_state["eruption_result"]
                
                # Create thread for eruption event
                if self.thread_system:
                    eruption_content = f"Volcanic eruption: {eruption_data['eruption_type']} (intensity: {eruption_data['details']['intensity']:.2f})"
                    thread_id = weave_thought_thread(eruption_content, "volcanic_eruption")
                    logger.info(f"🚀 [TICK] Volcanic eruption thread created: {thread_id}")
                
                # Trigger vector regeneration from eruption
                if self.vector_system and eruption_data["details"]["ash_produced"] > 0.5:
                    # Regenerate vectors affected by volcanic activity
                    for vector_id in list(self.vector_system.vectors.keys())[:5]:  # Sample of vectors
                        regenerate_vector(vector_id, RegenerationType.PRESSURE_MODULATION)
            
            return {
                "volcanic_state": volcanic_state.get("volcanic_state", "UNKNOWN"),
                "magma_pressure": volcanic_state.get("magma_chamber_pressure", 0.0),
                "thermal_temperature": volcanic_state.get("thermal_temperature", 0.0),
                "eruption_risk": volcanic_state.get("eruption_risk", 0.0),
                "recent_eruption": volcanic_state.get("eruption_result", {}).get("eruption_occurred", False)
            }
            
        except Exception as e:
            logger.error(f"🚀 [TICK] Volcanic dynamics error: {e}")
            return {"error": str(e)}
    
    async def _process_thread_weaving(self, cognitive_state: Dict[str, Any]) -> Dict[str, Any]:
        """Process Persephone thread weaving"""
        try:
            if not self.thread_system:
                return {"error": "Thread system not available"}
            
            # Process thread system tick
            thread_status = self.thread_system.tick_thread_system(cognitive_state)
            
            # Create thought threads for significant cognitive events
            if cognitive_state.get("cognitive_pressure", 0) > 100:
                pressure_content = f"High cognitive pressure detected: {cognitive_state['cognitive_pressure']:.1f}"
                thread_id = self.thread_system.weave_thought_thread(
                    pressure_content, "pressure_spike", cognitive_pressure=cognitive_state["cognitive_pressure"]
                )
                logger.debug(f"🚀 [TICK] Pressure thread woven: {thread_id}")
            
            # Track rebloom events through threads
            if cognitive_state.get("rebloom_queue_size", 0) > 5:
                rebloom_event = {
                    "cascade_size": cognitive_state["rebloom_queue_size"],
                    "type": "queue_buildup",
                    "intensity": min(1.0, cognitive_state["rebloom_queue_size"] / 10.0)
                }
                thread_id = self.thread_system.trace_rebloom_lineage(rebloom_event, "queue_pressure")
                logger.debug(f"🚀 [TICK] Rebloom thread traced: {thread_id}")
            
            return {
                "active_threads": thread_status.get("active_threads", 0),
                "total_threads": thread_status.get("total_threads", 0),
                "recent_intersections": thread_status.get("recent_intersections", 0),
                "patterns_detected": thread_status.get("patterns_detected", 0)
            }
            
        except Exception as e:
            logger.error(f"🚀 [TICK] Thread weaving error: {e}")
            return {"error": str(e)}
    
    async def _process_vector_regeneration(self, cognitive_state: Dict[str, Any]) -> Dict[str, Any]:
        """Process shelter vector regeneration"""
        try:
            if not self.vector_system:
                return {"error": "Vector system not available"}
            
            # Process vector system tick
            vector_status = self.vector_system.tick_vector_system(cognitive_state)
            
            # Trigger regeneration based on cognitive pressure
            pressure = cognitive_state.get("cognitive_pressure", 0.0)
            if pressure > 80:
                # High pressure - regenerate vectors for better performance
                active_vectors = list(self.vector_system.vectors.keys())[:3]  # Sample
                for vector_id in active_vectors:
                    success = self.vector_system.regenerate_vector(
                        vector_id, RegenerationType.PRESSURE_MODULATION, 
                        cognitive_pressure=pressure
                    )
                    if success:
                        logger.debug(f"🚀 [TICK] Vector regenerated under pressure: {vector_id}")
            
            # Context shift regeneration
            if cognitive_state.get("entropy_delta", 0) > 0.2:
                # Significant entropy change - context shift
                context_vectors = list(self.vector_system.vectors.keys())[:2]
                for vector_id in context_vectors:
                    self.vector_system.regenerate_vector(vector_id, RegenerationType.CONTEXT_SHIFT)
            
            # Manage active bloom pool
            pool_management = self.vector_system.manage_active_bloom_pool(
                target_intensity=min(1.0, cognitive_state.get("cognitive_pressure", 0) / 100.0)
            )
            
            return {
                "total_vectors": vector_status.get("system_status", {}).get("total_vectors", 0),
                "active_vectors": vector_status.get("system_status", {}).get("active_vectors", 0),
                "regeneration_count": self.vector_system.regeneration_count,
                "pool_management": pool_management
            }
            
        except Exception as e:
            logger.error(f"🚀 [TICK] Vector regeneration error: {e}")
            return {"error": str(e)}
    
    async def _process_constitutional_governance(self, cognitive_state: Dict[str, Any]) -> Dict[str, Any]:
        """Process constitutional governance"""
        try:
            if not self.constitution:
                return {"error": "Constitution not available"}
            
            # Process constitutional system tick
            constitutional_status = self.constitution.tick_constitutional_system(cognitive_state)
            
            # Check for constitutional violations based on system state
            scup = cognitive_state.get("scup", 0.5)
            pressure = cognitive_state.get("cognitive_pressure", 0.0)
            
            # Monitor for emergency conditions requiring constitutional response
            if scup < 0.2 and pressure > 150:
                # Potential system crisis - constitutional oversight needed
                emergency_declared = self.constitution.declare_emergency(
                    f"System crisis: SCUP={scup:.2f}, Pressure={pressure:.1f}",
                    "dawn_core"
                )
                if emergency_declared:
                    logger.critical("🚀 [TICK] Constitutional emergency declared")
            
            # Monitor for consensus on routine operations
            if self._state.tick_count % 100 == 0:  # Every 100 ticks
                # Routine system health decision
                health_proposal = f"System operating normally - SHI: {cognitive_state.get('schema_health_index', 0.5):.2f}"
                decision_id = self.constitution.propose_decision(
                    health_proposal, "dawn_core", DecisionScope.ROUTINE, 
                    "Regular system health confirmation"
                )
                
                # Auto-approve routine operations
                if decision_id:
                    self.constitution.cast_vote(decision_id, "dawn_core", 1.0, "System health confirmed")
                    if "owl_tracer" in self.constitution.agents:
                        self.constitution.cast_vote(decision_id, "owl_tracer", 0.8, "Routine oversight approval")
            
            return {
                "constitutional_health": constitutional_status.get("constitutional_status", {}).get("constitutional_health", 0.5),
                "active_decisions": constitutional_status.get("constitutional_status", {}).get("active_decisions", 0),
                "emergency_active": constitutional_status.get("constitutional_status", {}).get("emergency_active", False),
                "consensus_success_rate": self.constitution.consensus_success_rate
            }
            
        except Exception as e:
            logger.error(f"🚀 [TICK] Constitutional governance error: {e}")
            return {"error": str(e)}
    
    async def _emit_enhanced_events(self, cognitive_state: Dict[str, Any], modulations: Dict[str, float], 
                                  advanced_systems: Dict[str, Any]):
        """Emit enhanced events including advanced systems data"""
        try:
            # Enhanced tick event with formula data
            tick_data = {
                "tick": self._state.tick_count,
                "delta": time.time() - self._state.last_tick_time if self._state.last_tick_time else 0,
                "interval": self._state.current_interval,
                "thermal": self._state.thermal_state,
                "performance": self._state.performance_metrics
            }
            
            # Add formula system data if available
            if FORMULA_SYSTEMS_AVAILABLE:
                formula_data = {
                    "cognitive_pressure": self._state.thermal_state.get('cognitive_pressure', 0.0),
                    "pressure_level": self._state.thermal_state.get('pressure_level', 'low'),
                    "schema_health_index": self._state.thermal_state.get('schema_health_index', 0.5),
                    "health_level": self._state.thermal_state.get('health_level', 'unknown'),
                    "pigment_belief": self._state.thermal_state.get('pigment_belief', 'unknown'),
                    "pigment_intensity": self._state.thermal_state.get('pigment_intensity', 0.5),
                    "memory_crystallizations": self._state.thermal_state.get('memory_crystallizations', 0),
                    "tracer_alerts": self._state.thermal_state.get('tracer_alerts', 0)
                }
                tick_data["formula_state"] = formula_data
            
            # Add advanced systems data if available
            if ADVANCED_SYSTEMS_AVAILABLE:
                advanced_data = {
                    "mr_wolf": advanced_systems.get("emergency_diagnostic", {}),
                    "soft_edges": advanced_systems.get("boundary_adjustments", {}),
                    "volcanic": advanced_systems.get("volcanic_state", {}),
                    "threads": advanced_systems.get("thread_status", {}),
                    "vectors": advanced_systems.get("vector_updates", {}),
                    "constitution": advanced_systems.get("constitutional_status", {})
                }
                tick_data["advanced_systems"] = advanced_data
            
            # Emit main tick event
            await self._emit_event("tick", tick_data)
            
            # Emit specific formula events for specialized handlers
            if FORMULA_SYSTEMS_AVAILABLE:
                await self._emit_event("pressure_state", {
                    "tick": self._state.tick_count,
                    "pressure": self._state.thermal_state.get('cognitive_pressure', 0.0),
                    "level": self._state.thermal_state.get('pressure_level', 'low'),
                    "bloom_mass": self._state.thermal_state.get('bloom_mass', 0.0),
                    "sigil_velocity": self._state.thermal_state.get('sigil_velocity', 0.0),
                    "relief_actions": self._state.thermal_state.get('pressure_relief_actions', [])
                })
                
                await self._emit_event("shi_state", {
                    "tick": self._state.tick_count,
                    "shi_value": self._state.thermal_state.get('schema_health_index', 0.5),
                    "health_level": self._state.thermal_state.get('health_level', 'unknown'),
                    "vitality": self._state.thermal_state.get('vitality', 0.5),
                    "memory_health": self._state.thermal_state.get('memory_health', 0.5),
                    "soft_edge_responsiveness": cognitive_state.get('soft_edge_responsiveness', 0.5)
                })
                
                if self._state.thermal_state.get('tracer_alerts', 0) > 0:
                    await self._emit_event("tracer_alert", {
                        "tick": self._state.tick_count,
                        "alert_count": self._state.thermal_state.get('tracer_alerts', 0),
                        "active_tracers": self._state.thermal_state.get('active_tracers', []),
                        "alert_details": self._state.thermal_state.get('tracer_alert_details', [])
                    })
                
                await self._emit_event("belief_state", {
                    "tick": self._state.tick_count,
                    "dominant_belief": self._state.thermal_state.get('pigment_belief', 'unknown'),
                    "belief_intensity": self._state.thermal_state.get('pigment_intensity', 0.5),
                    "pigment_coupling": self._state.thermal_state.get('pigment_coupling', {}),
                    "voice_modulation": self._state.thermal_state.get('voice_modulation', {})
                })
            
            # Emit advanced system events
            if ADVANCED_SYSTEMS_AVAILABLE:
                
                # Volcanic eruption events
                volcanic_state = advanced_systems.get("volcanic_state", {})
                if volcanic_state.get("recent_eruption", False):
                    await self._emit_event("volcanic_eruption", {
                        "tick": self._state.tick_count,
                        "eruption_type": volcanic_state.get("eruption_type", "unknown"),
                        "intensity": volcanic_state.get("intensity", 0.0),
                        "ash_produced": volcanic_state.get("ash_produced", 0.0)
                    })
                
                # Thread intersection events
                thread_status = advanced_systems.get("thread_status", {})
                if thread_status.get("recent_intersections", 0) > 0:
                    await self._emit_event("thread_intersection", {
                        "tick": self._state.tick_count,
                        "intersection_count": thread_status.get("recent_intersections", 0),
                        "patterns_detected": thread_status.get("patterns_detected", 0)
                    })
                
                # Constitutional events
                constitutional_status = advanced_systems.get("constitutional_status", {})
                if constitutional_status.get("emergency_active", False):
                    await self._emit_event("constitutional_emergency", {
                        "tick": self._state.tick_count,
                        "emergency_active": True,
                        "constitutional_health": constitutional_status.get("constitutional_health", 0.5)
                    })
            
        except Exception as e:
            logger.error(f"🚀 [TICK] Enhanced event emission error: {e}")

# Global instance
tick_engine = TickEngine()

def register_handler(event_type: str, handler: Callable, priority: int = 0) -> None:
    """Register an event handler"""
    return tick_engine.register_handler(event_type, handler, priority)

def unregister_handler(event_type: str, handler: Callable) -> None:
    """Unregister an event handler"""
    return tick_engine.unregister_handler(event_type, handler)

def patch_tick_engine(handler: Callable, event_type: str = 'tick', priority: int = 0) -> None:
    """
    Patch the tick engine with a custom handler.
    
    Args:
        handler: The handler function to register
        event_type: The type of event to handle (default: 'tick')
        priority: Handler priority (default: 0)
    """
    tick_engine.register_handler(event_type, handler, priority)
    logger.info(f"Patched tick engine with handler for {event_type}")

# Export key functions
__all__ = [
    'tick_engine',
    'register_handler',
    'unregister_handler',
    'patch_tick_engine'
] 