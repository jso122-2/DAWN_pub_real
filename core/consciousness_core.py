"""
DAWN Consciousness Core - Core consciousness system components
"""

import sys
import time
import math
import random
import threading
import asyncio
from datetime import datetime, timezone
from collections import deque
from typing import Dict, List, Optional, Any, Tuple, Callable, Set
from core.entropy_tracker import EntropyTracker
from core.tension_tracker import TensionTracker
from core.mood_tracker import MoodTracker
from core.sigil_memory import SigilMemory
from core.alignment_probe import AlignmentProbe
from core.bloom_manager import BloomManager
from schema.schema_calculator import SchemaCalculator
from core.dawn_visualizer import DAWNVisualizer
from core.thermal_visualizer import ThermalVisualizer
from core.entropy_visualizer import EntropyVisualizer
from core.alignment_visualizer import AlignmentVisualizer
from core.bloom_visualizer import BloomVisualizer
from core.tick.tick_signals import listen_signal, set_signal, get_signal

import logging
import json
import os
from dataclasses import dataclass
from core.event_bus import EventBus
from core.hot_reload import reload_module
from core.shutdown_manager import ShutdownManager

import numpy as np

# Memory routing system integration
from core.memory.memory_routing_system import initialize_memory_routing, get_memory_routing_system

# Symbolic anatomy integration - NEW
try:
    from cognitive.symbolic_router import initialize_symbolic_routing, get_symbolic_router
    SYMBOLIC_ROUTER_AVAILABLE = True
except ImportError:
    SYMBOLIC_ROUTER_AVAILABLE = False
    def initialize_symbolic_routing(*args, **kwargs):
        return None
    def get_symbolic_router():
        return None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Core components
from core.semantic_field import SemanticField
from core.schema_interface import SchemaInterface
from schema.schema_evolution_engine import SchemaEvolutionEngine

# Initialize components
semantic_field = SemanticField()
schema_interface = SchemaInterface()
schema_calculator = SchemaCalculator()
thermal_visualizer = ThermalVisualizer()
entropy_visualizer = EntropyVisualizer()
alignment_visualizer = AlignmentVisualizer()
bloom_visualizer = BloomVisualizer()
dawn_visualizer = DAWNVisualizer()
schema_evolution_engine = SchemaEvolutionEngine()

# Register subsystems with priorities (adjust if needed)
from core.tick.tick_engine import tick_engine
from core.pulse_layer import pulse_layer
from schema.schema_evolution_engine import schema_evolution_engine
from core.dawn_visualizer import DAWNVisualizer
from core.thermal_visualizer import ThermalVisualizer
from core.entropy_visualizer import EntropyVisualizer
from core.alignment_visualizer import AlignmentVisualizer
from core.bloom_visualizer import BloomVisualizer

tick_engine.register_subsystem("pulse", pulse_layer, priority=1)
tick_engine.register_subsystem("schema_evolution_engine", schema_evolution_engine, priority=2)
tick_engine.register_subsystem("dawn_visualizer", DAWNVisualizer(), priority=3)
tick_engine.register_subsystem("thermal_visualizer", ThermalVisualizer(), priority=4)
tick_engine.register_subsystem("entropy_visualizer", EntropyVisualizer(), priority=5)
tick_engine.register_subsystem("alignment_visualizer", AlignmentVisualizer(), priority=6)
tick_engine.register_subsystem("bloom_visualizer", BloomVisualizer(), priority=7)

def safe_float(val, default=0.0):
    """Safely convert a value to float with a default fallback"""
    try:
        return float(val)
    except (ValueError, TypeError):
        return default

class ConsciousnessCore:
    def __init__(self):
        self.state = {
            "neural_activity": np.zeros((10, 10)),
            "quantum_coherence": 0.0,
            "pattern_recognition": 0.0,
            "memory_utilization": 0.0,
            "chaos_factor": 0.0,
            "last_update": datetime.now()
        }
        self.history = {
            "neural_activity": [],
            "quantum_coherence": [],
            "pattern_recognition": [],
            "memory_utilization": [],
            "chaos_factor": []
        }
        self.max_history_size = 1000
        logger.info("Initialized ConsciousnessCore")
    
    def update_state(self, new_state: Dict[str, Any]) -> None:
        """Update consciousness state"""
        self.state.update(new_state)
        self.state["last_update"] = datetime.now()
        
        # Update history
        for key, value in new_state.items():
            if key in self.history:
                self.history[key].append(value)
                if len(self.history[key]) > self.max_history_size:
                    self.history[key] = self.history[key][-self.max_history_size:]
    
    def get_state(self) -> Dict[str, Any]:
        """Get current consciousness state"""
        return self.state
    
    def get_history(self, duration: int = 100) -> Dict[str, List[Any]]:
        """Get historical data"""
        return {
            key: values[-duration:] if len(values) > duration else values
            for key, values in self.history.items()
        }
    
    def get_metrics(self) -> Dict[str, float]:
        """Get current consciousness metrics"""
        return {
            "neural_activity": float(np.mean(self.state["neural_activity"])),
            "quantum_coherence": self.state["quantum_coherence"],
            "pattern_recognition": self.state["pattern_recognition"],
            "memory_utilization": self.state["memory_utilization"],
            "chaos_factor": self.state["chaos_factor"]
        }
    
    def reset(self) -> None:
        """Reset consciousness state"""
        self.state = {
            "neural_activity": np.zeros((10, 10)),
            "quantum_coherence": 0.0,
            "pattern_recognition": 0.0,
            "memory_utilization": 0.0,
            "chaos_factor": 0.0,
            "last_update": datetime.now()
        }
        self.history = {
            "neural_activity": [],
            "quantum_coherence": [],
            "pattern_recognition": [],
            "memory_utilization": [],
            "chaos_factor": []
        }
        logger.info("Reset ConsciousnessCore state")

# Global instance
consciousness_core = ConsciousnessCore()

class DAWNConsciousness:
    """
    Unified consciousness system with dynamic schema calculations.
    All values derived from DAWN's formal equations and live state.
    """
    
    def __init__(self, **subsystems):
        """Initialize DAWN consciousness with dynamic subsystem injection"""
        from schema.schema_evolution_engine import SchemaEvolutionEngine

        # Initialize subsystem registry
        self.subsystems: Dict[str, Any] = {}
        self.missing_subsystems: Set[str] = set()
        
        # Initialize performance metrics
        self.performance_metrics = {
            'ticks_per_second': 0.0,
            'last_tick': 0.0,
            'uptime': 0.0,
            'memory_usage': 0.0,
            'cpu_usage': 0.0
        }
        
        # Initialize timing
        self.start_time = time.time()
        self.last_tick = 0
        self.tick_count = 0
        
        # Initialize state tracking
        self._current_scup = 0.5
        self._current_entropy = 0.5
        self._current_mood = "neutral"
        
        # Register provided subsystems
        for name, subsystem in subsystems.items():
            self.update_subsystem(name, subsystem)
            
        # Create schema engine if not provided
        if "schema_evolution_engine" not in self.subsystems:
            self.schema_evolution_engine = SchemaEvolutionEngine()
            self.subsystems["schema_evolution_engine"] = self.schema_evolution_engine

        # Add event bus as a core subsystem
        if "event_bus" not in self.subsystems:
            self.event_bus = EventBus()
            self.subsystems["event_bus"] = self.event_bus
        else:
            self.event_bus = self.subsystems["event_bus"]
            
        # Initialize visualizer if not provided
        if "visualizer" not in self.subsystems:
            self.visualizer = DAWNVisualizer()
            self.subsystems["visualizer"] = self.visualizer
        else:
            self.visualizer = self.subsystems["visualizer"]
        
        # Initialize memory routing system
        if "memory_routing" not in self.subsystems:
            # Get pulse controller if available for integration
            pulse_controller = self.subsystems.get("pulse_controller") or self.subsystems.get("pulse")
            self.memory_routing = initialize_memory_routing(
                memories_dir="memories",
                pulse_controller=pulse_controller
            )
            self.subsystems["memory_routing"] = self.memory_routing
            logger.info("🧠 Memory routing system integrated with consciousness core")
        else:
            self.memory_routing = self.subsystems["memory_routing"]

        # Initialize symbolic anatomy router
        if "symbolic_router" not in self.subsystems:
            self.symbolic_router = initialize_symbolic_routing(
                consciousness_core=consciousness_core,
                memory_system=self.memory_routing
            )
            self.subsystems["symbolic_router"] = self.symbolic_router
            logger.info("🧠 Symbolic anatomy router integrated with consciousness core")
        else:
            self.symbolic_router = self.subsystems["symbolic_router"]
        
        # Initialize symbolic memory integration
        if "symbolic_memory_integration" not in self.subsystems:
            from core.memory.symbolic_memory_integration import initialize_symbolic_memory_integration
            self.symbolic_memory_integration = initialize_symbolic_memory_integration(
                memory_routing_system=self.memory_routing,
                symbolic_router=self.symbolic_router
            )
            self.subsystems["symbolic_memory_integration"] = self.symbolic_memory_integration
            logger.info("🔗 Symbolic memory integration active")
        else:
            self.symbolic_memory_integration = self.subsystems["symbolic_memory_integration"]
        
        # Initialize snapshot exporter
        if "snapshot_exporter" not in self.subsystems:
            from core.snapshot_exporter import initialize_snapshot_exporter
            self.snapshot_exporter = initialize_snapshot_exporter(dawn_consciousness=self)
            self.subsystems["snapshot_exporter"] = self.snapshot_exporter
            logger.info("📤 DAWN Snapshot Exporter integrated with consciousness core")
        else:
            self.snapshot_exporter = self.subsystems["snapshot_exporter"]

        # Initialize shutdown manager
        self.shutdown_manager = ShutdownManager()
        self._register_cleanup_hooks()

        # Register hot-reload event
        self.event_bus.on("reload", lambda module_name: reload_module(module_name))

        # Initialize system state
        self.is_running = False
        self.stop_event = asyncio.Event()
        
        # Register tick engine signal handlers
        listen_signal("tick_complete", self._handle_tick_complete)
        listen_signal("claude_query_needed", self._handle_claude_query)
        
        # Set up memory event handlers
        self._setup_memory_event_handlers()
        
        # Initialize forecasting system
        self._initialize_forecasting_system()
        
        # Log subsystem registration
        logger.info(f"🔌 Registered subsystems: {list(self.subsystems.keys())}")
        print("🌅 DAWN Consciousness System Initializing...")
        print("   Schema-driven thermal regulation: ✓")
        print("   Dynamic semantic field topology: ✓")
        print("   Event bus and hot-reload: ✓")
        print("   Memory routing and persistence: ✓")
        print("   Behavioral forecasting engine: ✓")
        print("   Graceful shutdown system: ✓")
    
    def update_subsystem(self, name: str, subsystem: Any) -> None:
        """Update or register a subsystem"""
        self.subsystems[name] = subsystem
        setattr(self, name, subsystem)
        logger.info(f"Registered subsystem: {name}")
    
    def get_subsystem(self, name: str) -> Optional[Any]:
        """Get a subsystem by name"""
        return self.subsystems.get(name)
        
    def has_subsystem(self, name: str) -> bool:
        """Check if a subsystem exists"""
        return name in self.subsystems
        
    async def try_call(self, subsystem_name: str, method_name: str, *args, **kwargs) -> Optional[Any]:
        """Safely call a method on a subsystem, handling coroutines properly"""
        try:
            subsystem = self.get_subsystem(subsystem_name)
            if not subsystem:
                if subsystem_name not in self.missing_subsystems:
                    logger.warning(f"⚠️ Subsystem '{subsystem_name}' not found")
                    self.missing_subsystems.add(subsystem_name)
                return None
                
            method = getattr(subsystem, method_name, None)
            if not method or not callable(method):
                if f"{subsystem_name}.{method_name}" not in self.missing_subsystems:
                    logger.warning(f"⚠️ Method '{method_name}' not found on '{subsystem_name}'")
                    self.missing_subsystems.add(f"{subsystem_name}.{method_name}")
                return None
                
            result = method(*args, **kwargs)
            if asyncio.iscoroutine(result):
                return await result
            return result
            
        except Exception as e:
            logger.error(f"Error calling {method_name} on {subsystem_name}: {e}")
            return None
            
    async def update_state(self, scup: float = 0.5, entropy: float = 0.5, mood: str = "neutral") -> None:
        """Update system state with new values
        
        Args:
            scup: Current SCUP value (0.0-1.0)
            entropy: Current entropy value (0.0-1.0)
            mood: Current mood state
        """
        try:
            # Update internal state
            self._current_scup = scup
            self._current_entropy = entropy
            self._current_mood = mood
            
            # Get drift and tension from subsystems
            drift = 0.0
            tension = 0.0
            
            # Get tension from pulse if available
            if self.has_subsystem("pulse"):
                tension = await self.try_call("pulse", "get_tension") or tension
                await self.try_call("pulse", "update_health", scup, entropy)
                
            # Update visual state
            await self._update_visual_consciousness({
                "scup": scup,
                "entropy": entropy,
                "mood": mood,
                "drift": drift,
                "tension": tension
            })
            
            # Save state periodically
            if self.tick_count % 100 == 0:
                await self._save_state()
                
        except Exception as e:
            logger.error(f"Error updating state: {e}")
    
    async def _handle_tick_complete(self, signal_name: str, data: dict) -> None:
        """Handle tick completion events"""
        try:
            # Update health metrics
            await self._update_health_metrics()
            
            # Update performance metrics
            self.performance_metrics['ticks_per_second'] = self.tick_count / (time.time() - self.start_time)
            self.performance_metrics['last_tick'] = time.time()
            self.performance_metrics['uptime'] = time.time() - self.start_time
            
            # Save state periodically
            if self.tick_count % 100 == 0:
                await self._save_state()
                
        except Exception as e:
            logger.error(f"Error handling tick complete: {e}")
    
    async def _handle_claude_query(self, signal_name: str, data: dict) -> None:
        """Handle Claude query events"""
        try:
            scup = data.get('scup', 0.0)
            mood = data.get('mood', 'neutral')
            
            # Store query in memory system
            await self._store_interaction_memory(
                speaker="dawn.core",
                content=f"Claude query event: {data}",
                topic="system_query"
            )
            
            # Update state with new values
            await self.update_state(scup=scup, mood=mood)
            
        except Exception as e:
            logger.error(f"Error handling Claude query: {e}")
    
    async def boot_consciousness(self) -> None:
        """Boot the consciousness system"""
        if self.is_running:
            return
            
        self.is_running = True
        print("🌅 DAWN Consciousness System Booting...")
        print("   Tick engine integration: ✓")
        print("   Schema evolution ready: ✓")
        print("   Visual system active: ✓")
        
        # Initialize subsystems
        for name, subsystem in self.subsystems.items():
            try:
                if hasattr(subsystem, "initialize"):
                    await subsystem.initialize()
            except Exception as e:
                logger.error(f"Error initializing {name}: {e}")
                self.is_running = False
                return
                
        logger.info("DAWN Consciousness booted")
        
    async def shutdown(self) -> None:
        """Gracefully shutdown the consciousness system"""
        if not self.is_running:
            return
            
        self.is_running = False
        self.stop_event.set()
        
        try:
            # Save final state
            await self._save_state()
            
            # Cleanup subsystems
            await self._cleanup_subsystems()
            
            # Stop event loop
            await self._stop_event_loop()
            
            logger.info("✅ DAWN Consciousness shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
            raise
    
    def _handle_shutdown(self, signum, frame):
        """Handle shutdown signal"""
        print(f"\n⚠️  Received signal {signum}, initiating shutdown...")
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(self.shutdown())
        else:
            loop.run_until_complete(self.shutdown())
    
    async def _update_health_metrics(self) -> None:
        """Update system health metrics"""
        try:
            # Get current values
            scup = self._current_scup
            entropy = self._current_entropy
            drift = 0.0
            tension = 0.0
            
            # Get tension from pulse if available
            if self.has_subsystem("pulse"):
                tension = await self.try_call("pulse", "get_tension") or tension
                
            # Update entropy tracker if available
            if self.has_subsystem("entropy_tracker"):
                await self.try_call("entropy_tracker", "update_health", entropy, tension)
                
            # Update visualizer if available
            if self.has_subsystem("visualizer"):
                await self.try_call("visualizer", "update", {
                    "scup": scup,
                    "entropy": entropy,
                    "tension": tension,
                    "drift": drift
                })
                
        except Exception as e:
            logger.error(f"Error updating health metrics: {e}")
    
    def _assess_thermal_health_from_schema(self, current_heat, stability, scup):
        """Assess thermal health based on schema state"""
        if current_heat > 0.9:
            return 'critical'
        elif current_heat > 0.7:
            return 'warning'
        elif stability < 0.3:
            return 'unstable'
        elif scup < 0.3:
            return 'degraded'
        return 'healthy'
    
    def _assess_semantic_health_from_schema(self, node_count, connections, entropy):
        """Assess semantic health based on schema state"""
        if node_count < 10:
            return 'minimal'
        elif entropy > 0.8:
            return 'chaotic'
        elif connections < node_count * 0.5:
            return 'fragmented'
        return 'coherent'
    
    def _assess_alignment_health_from_schema(self, drift, scup):
        """Assess alignment health based on schema state"""
        if abs(drift) > 0.8:
            return 'misaligned'
        elif scup < 0.3:
            return 'unstable'
        elif abs(drift) > 0.5:
            return 'drifting'
        return 'aligned'
    
    def _assess_entropy_health_from_schema(self, entropy, tension):
        """Assess entropy health based on schema state"""
        if entropy > 0.9:
            return 'chaotic'
        elif tension > 0.8:
            return 'tense'
        elif entropy < 0.1:
            return 'stagnant'
        return 'balanced'
    
    def _schema_health_to_score(self, status: str) -> float:
        """Convert health status to numerical score"""
        status_scores = {
            'healthy': 1.0,
            'coherent': 1.0,
            'aligned': 1.0,
            'balanced': 1.0,
            'warning': 0.7,
            'unstable': 0.6,
            'degraded': 0.5,
            'fragmented': 0.4,
            'drifting': 0.3,
            'tense': 0.3,
            'stagnant': 0.2,
            'minimal': 0.2,
            'critical': 0.1,
            'chaotic': 0.1,
            'misaligned': 0.1
        }
        return status_scores.get(status, 0.0)
    
    def _gather_consciousness_state(self) -> Dict:
        """Gather current consciousness state"""
        return {
            'schema_state': self.schema_state.copy(),
            'mood_state': self.mood_state.copy(),
            'system_health': self.system_health.copy(),
            'performance_metrics': self.performance_metrics.copy(),
            'tick_count': self.tick_count,
            'uptime': (datetime.now(timezone.utc) - self.boot_time).total_seconds() if hasattr(self, 'boot_time') else 0.0
        }
    
    async def _update_visual_consciousness(self, consciousness_state: Dict) -> None:
        """Update visual representation of consciousness state"""
        try:
            if self.has_subsystem("visualizer"):
                await self.try_call("visualizer", "update", consciousness_state)
            else:
                logger.warning("No visualizer subsystem available")
        except Exception as e:
            logger.error(f"Error updating visual consciousness: {e}")
    
    def get_consciousness_status(self) -> Dict:
        """Get current consciousness status"""
        return {
            'is_running': self.is_running,
            'tick_count': self.tick_count,
            'uptime': (datetime.now(timezone.utc) - self.boot_time).total_seconds() if hasattr(self, 'boot_time') else 0.0,
            'schema_state': self.schema_state.copy(),
            'mood_state': self.mood_state.copy(),
            'system_health': self.system_health.copy(),
            'performance_metrics': self.performance_metrics.copy()
        }
    
    def apply_config(self, config: dict, schema: dict):
        """Apply configuration with schema validation"""
        print("🔧 Applying configuration with schema validation...")
        
        # Track validation results
        valid_keys = []
        invalid_keys = []
        missing_keys = []
        
        # Validate and apply each config value
        for key, expected_type in schema.items():
            value = config.get(key)
            if value is not None:
                if isinstance(value, expected_type):
                    setattr(self, key, value)
                    valid_keys.append(key)
                else:
                    invalid_keys.append((key, type(value), expected_type))
            else:
                missing_keys.append(key)
                
        # Log validation results
        if valid_keys:
            print(f"✅ Valid config keys: {', '.join(valid_keys)}")
        if invalid_keys:
            for key, actual_type, expected_type in invalid_keys:
                print(f"⚠️ Invalid type for '{key}': got {actual_type.__name__}, expected {expected_type.__name__}")
        if missing_keys:
            print(f"⚠️ Missing config keys: {', '.join(missing_keys)}")
            
        return {
            'valid': valid_keys,
            'invalid': invalid_keys,
            'missing': missing_keys
        }
        
    def get_config_schema(self):
        """Get the current configuration schema"""
        return {
            'tick_interval': float,
            'max_heat': float,
            'baseline_entropy': float,
            'visual_update_rate': float,
            'memory_capacity': int,
            'schema_evolution_rate': float,
            'thermal_decay_rate': float,
            'entropy_threshold': float,
            'alignment_threshold': float,
            'bloom_threshold': float
        }
        
    def export_config(self):
        """Export current configuration state"""
        schema = self.get_config_schema()
        config = {}
        for key in schema:
            value = getattr(self, key, None)
            if value is not None:
                config[key] = value
        return config 

    def _register_cleanup_hooks(self):
        """Register cleanup hooks for graceful shutdown"""
        # Save current state
        self.shutdown_manager.register_cleanup(self._save_state)
        
        # Cleanup subsystems
        self.shutdown_manager.register_cleanup(self._cleanup_subsystems)
        
        # Stop event loop
        self.shutdown_manager.register_cleanup(self._stop_event_loop)
        
    async def _save_state(self) -> None:
        """Save current consciousness state"""
        try:
            state = {
                'tick_count': self.tick_count,
                'uptime': time.time() - self.start_time,
                'subsystems': list(self.subsystems.keys()),
                'is_running': self.is_running,
                'performance_metrics': self.performance_metrics
            }
            
            # Add subsystem states
            for name, subsystem in self.subsystems.items():
                if hasattr(subsystem, 'get_state'):
                    try:
                        state[f'{name}_state'] = subsystem.get_state()
                    except Exception as e:
                        logger.error(f"Error getting state for {name}: {e}")
                    
            # Save to file
            state_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tick_state.json')
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving state: {e}")
    
    def _setup_memory_event_handlers(self):
        """Set up event handlers for memory integration"""
        if hasattr(self, 'memory_routing'):
            # Listen for significant system events
            self.event_bus.on("mood_change", self._handle_mood_change_memory)
            self.event_bus.on("entropy_spike", self._handle_entropy_spike_memory)
            self.event_bus.on("thermal_event", self._handle_thermal_event_memory)
            self.event_bus.on("sigil_activation", self._handle_sigil_activation_memory)
            logger.info("🧠 Memory event handlers configured")
    
    def _initialize_forecasting_system(self):
        """Initialize DAWN's behavioral forecasting system"""
        try:
            from cognitive.forecasting_processor import initialize_forecasting_processor
            
            # Initialize forecasting processor with consciousness components
            memory_manager = getattr(self, 'memory_routing', None)
            
            self.forecasting_processor = initialize_forecasting_processor(
                consciousness_core=self,
                memory_manager=memory_manager,
                event_bus=self.event_bus
            )
            
            # Register as subsystem
            self.subsystems["forecasting_processor"] = self.forecasting_processor
            
            # Set up forecasting event handlers
            self.event_bus.on("forecasts_generated", self._handle_forecasts_generated)
            
            logger.info("🔮 DAWN Forecasting System initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize forecasting system: {e}")
            # Continue without forecasting - non-critical system
            self.forecasting_processor = None
        
        # Initialize tick engine for autonomous cognitive loop
        self._initialize_tick_engine()
    
    def _initialize_tick_engine(self):
        """Initialize the DAWN autonomous cognitive tick engine."""
        try:
            from ...tick_loop import integrate_tick_engine
            
            # Initialize tick engine with full consciousness integration
            self.tick_engine = integrate_tick_engine(self)
            
            # Register as subsystem
            self.subsystems["tick_engine"] = self.tick_engine
            
            logger.info("🔄 DAWN Autonomous Tick Engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize tick engine: {e}")
            # Continue without tick engine - consciousness can still function
            self.tick_engine = None
    
    async def _store_interaction_memory(self, speaker: str, content: str, topic: str = None, **kwargs):
        """Store an interaction in the memory system"""
        if hasattr(self, 'memory_routing'):
            try:
                # Get current system state
                pulse_state = self._get_current_system_state()
                
                # Store memory
                memory_chunk = await self.memory_routing.store_memory(
                    speaker=speaker,
                    content=content,
                    topic=topic,
                    pulse_state=pulse_state,
                    **kwargs
                )
                
                logger.debug(f"Stored interaction memory: {memory_chunk.memory_id}")
                return memory_chunk
                
            except Exception as e:
                logger.error(f"Error storing interaction memory: {e}")
        return None
    
    def _handle_mood_change_memory(self, event_data):
        """Handle mood change events for memory storage"""
        asyncio.create_task(self._store_interaction_memory(
            speaker="dawn.core",
            content=f"Mood changed to {event_data.get('new_mood', 'unknown')}",
            topic="mood_transition",
            sigils=["MOOD_SHIFT"]
        ))
    
    def _handle_entropy_spike_memory(self, event_data):
        """Handle entropy spike events for memory storage"""
        asyncio.create_task(self._store_interaction_memory(
            speaker="dawn.core",
            content=f"Entropy spike detected: {event_data.get('entropy_value', 'unknown')}",
            topic="system_event",
            sigils=["ENTROPY_SPIKE", "STABILIZE_PROTOCOL"]
        ))
    
    def _handle_thermal_event_memory(self, event_data):
        """Handle thermal events for memory storage"""
        asyncio.create_task(self._store_interaction_memory(
            speaker="dawn.core",
            content=f"Thermal event: {event_data.get('event_type', 'unknown')}",
            topic="thermal_regulation",
            sigils=["THERMAL_EVENT"]
        ))
    
    def _handle_sigil_activation_memory(self, event_data):
        """Handle sigil activation events for memory storage"""
        sigil_name = event_data.get('sigil_name', 'unknown')
        asyncio.create_task(self._store_interaction_memory(
            speaker="dawn.core",
            content=f"Sigil activated: {sigil_name}",
            topic="sigil_activation",
            sigils=[sigil_name]
        ))
    
    def _handle_forecasts_generated(self, event_data):
        """Handle forecasting events for integration and memory storage"""
        try:
            forecasts = event_data.get('forecasts', {})
            consciousness_state = event_data.get('consciousness_state', {})
            
            # Store forecasting event in memory
            forecast_summary = f"Generated {len(forecasts)} behavioral forecasts based on current consciousness state"
            asyncio.create_task(self._store_interaction_memory(
                speaker="dawn.forecasting",
                content=forecast_summary,
                topic="behavioral_forecasting",
                sigils=["FORECAST_GENERATED", "BEHAVIORAL_PREDICTION"]
            ))
            
            # Log interesting forecasts
            high_confidence_forecasts = [
                f for f in forecasts.values() 
                if hasattr(f, 'confidence') and f.confidence > 0.7
            ]
            
            if high_confidence_forecasts:
                logger.info(f"🔮 Generated {len(high_confidence_forecasts)} high-confidence forecasts")
                for forecast in high_confidence_forecasts[:3]:  # Log top 3
                    logger.debug(f"   {forecast.passion_direction}: {forecast.predicted_behavior} ({forecast.confidence:.3f})")
            
        except Exception as e:
            logger.warning(f"Error handling forecasts generated event: {e}")
    
    def _get_current_system_state(self):
        """Get current system state for memory storage"""
        state = {
            'timestamp': time.time(),
            'tick_count': getattr(self, 'tick_count', 0)
        }
        
        # Get pulse state if available
        if hasattr(self, 'pulse') and self.pulse:
            try:
                state.update({
                    'heat': getattr(self.pulse, 'current_heat', 0.0),
                    'zone': getattr(self.pulse, 'current_zone', 'unknown')
                })
            except Exception:
                pass
        
        # Get mood and entropy if available
        try:
            state.update({
                'mood': getattr(self, '_current_mood', 'neutral'),
                'entropy': getattr(self, '_current_entropy', 0.5),
                'scup': getattr(self, '_current_scup', 0.5)
            })
        except Exception:
            pass
        
        return state
            
    async def _cleanup_subsystems(self) -> None:
        """Clean up all subsystems"""
        for name, subsystem in self.subsystems.items():
            try:
                if hasattr(subsystem, 'cleanup'):
                    result = subsystem.cleanup()
                    if asyncio.iscoroutine(result):
                        await result
                elif hasattr(subsystem, 'shutdown'):
                    result = subsystem.shutdown()
                    if asyncio.iscoroutine(result):
                        await result
                logger.info(f"🧹 Cleaned up {name}")
            except Exception as e:
                logger.error(f"Error cleaning up {name}: {e}")
                
    async def _stop_event_loop(self) -> None:
        """Stop the event loop"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.stop()
        except Exception as e:
            logger.error(f"Error stopping event loop: {e}")
        
    # Forecasting system integration methods
    
    def get_current_forecasts(self) -> Dict[str, Any]:
        """Get current behavioral forecasts"""
        if hasattr(self, 'forecasting_processor') and self.forecasting_processor:
            try:
                recent_forecasts = self.forecasting_processor.get_recent_forecasts()
                forecast_metrics = self.forecasting_processor.get_metrics()
                
                return {
                    'recent_forecasts': [f.to_dict() for f in recent_forecasts],
                    'metrics': forecast_metrics,
                    'timestamp': datetime.now().isoformat()
                }
            except Exception as e:
                logger.warning(f"Error getting current forecasts: {e}")
        
        return {'recent_forecasts': [], 'metrics': {}, 'timestamp': datetime.now().isoformat()}
    
    def get_forecast_for_direction(self, direction: str) -> Optional[Dict[str, Any]]:
        """Get forecast for a specific passion direction"""
        if hasattr(self, 'forecasting_processor') and self.forecasting_processor:
            try:
                forecast = self.forecasting_processor.get_forecast_for_direction(direction)
                return forecast.to_dict() if forecast else None
            except Exception as e:
                logger.warning(f"Error getting forecast for {direction}: {e}")
        
        return None
    
    async def generate_instant_forecast(self, direction: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Generate an instant forecast for a specific direction"""
        if hasattr(self, 'forecasting_processor') and self.forecasting_processor:
            try:
                forecast = await self.forecasting_processor.generate_instant_forecast(direction, **kwargs)
                return forecast.to_dict() if forecast else None
            except Exception as e:
                logger.warning(f"Error generating instant forecast for {direction}: {e}")
        
        return None
    
    def get_forecast_trends(self, direction: str, lookback_hours: int = 24) -> List[Dict[str, Any]]:
        """Get forecast trends for a direction over time"""
        if hasattr(self, 'forecasting_processor') and self.forecasting_processor:
            try:
                trends = self.forecasting_processor.get_forecast_trends(direction, lookback_hours)
                return [f.to_dict() for f in trends]
            except Exception as e:
                logger.warning(f"Error getting forecast trends for {direction}: {e}")
        
        return []
    
    async def start_forecasting(self):
        """Start the forecasting processing loop"""
        if hasattr(self, 'forecasting_processor') and self.forecasting_processor:
            await self.forecasting_processor.start_processing()
            logger.info("🔮 Started DAWN forecasting processing")
    
    async def stop_forecasting(self):
        """Stop the forecasting processing loop"""
        if hasattr(self, 'forecasting_processor') and self.forecasting_processor:
            await self.forecasting_processor.stop_processing()
            logger.info("🔮 Stopped DAWN forecasting processing")
    
    async def start_autonomous_loop(self, max_ticks: Optional[int] = None, tick_interval: float = 2.0, adaptive_speed: bool = True):
        """Start the autonomous cognitive tick loop with optional adaptive speed control"""
        if hasattr(self, 'tick_engine') and self.tick_engine:
            logger.info("🔄 Starting DAWN autonomous cognitive loop")
            await self.tick_engine.run_continuous_loop(max_ticks=max_ticks, tick_interval=tick_interval, adaptive_speed=adaptive_speed)
        else:
            logger.warning("Tick engine not available")
    
    async def execute_single_tick(self):
        """Execute a single cognitive tick"""
        if hasattr(self, 'tick_engine') and self.tick_engine:
            return await self.tick_engine.tick()
        else:
            logger.warning("Tick engine not available")
            return None
    
    def stop_autonomous_loop(self):
        """Stop the autonomous cognitive loop"""
        if hasattr(self, 'tick_engine') and self.tick_engine:
            self.tick_engine.running = False
            logger.info("🔄 Stopped DAWN autonomous cognitive loop")
    
    def get_tick_status(self) -> Dict[str, Any]:
        """Get status of the tick engine"""
        if hasattr(self, 'tick_engine') and self.tick_engine:
            return self.tick_engine.get_system_status()
        else:
            return {'tick_engine': 'not_available'}

    async def shutdown(self):
        """Initiate graceful shutdown"""
        # Stop autonomous loop
        self.stop_autonomous_loop()
        
        # Stop forecasting before shutdown
        await self.stop_forecasting()
        await self.shutdown_manager.shutdown(self)
        
    def is_shutdown_requested(self) -> bool:
        """Check if shutdown has been requested"""
        return self.shutdown_manager.is_shutdown_requested() 