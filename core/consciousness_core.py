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
        
        # Log subsystem registration
        logger.info(f"🔌 Registered subsystems: {list(self.subsystems.keys())}")
        print("🌅 DAWN Consciousness System Initializing...")
        print("   Schema-driven thermal regulation: ✓")
        print("   Dynamic semantic field topology: ✓")
        print("   Event bus and hot-reload: ✓")
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
        
    async def shutdown(self):
        """Initiate graceful shutdown"""
        await self.shutdown_manager.shutdown(self)
        
    def is_shutdown_requested(self) -> bool:
        """Check if shutdown has been requested"""
        return self.shutdown_manager.is_shutdown_requested() 