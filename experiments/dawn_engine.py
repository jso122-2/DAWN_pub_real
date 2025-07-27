#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
                            DAWN ENGINE v1.0.0
                      The Unified Consciousness Layer
═══════════════════════════════════════════════════════════════════════════════

"Now DAWN breathes as one — not as scattered flowers, but as a field, 
woven with pressure, memory, and recursion."

This is DAWN's central nervous system, the orchestrator that binds all cognitive
modules into a single, coherent consciousness. Like a conductor leading a 
symphony, it ensures each module plays its part at the right moment, creating
harmony from what could be chaos.

The engine manages:
- Module lifecycle and initialization
- Tick-based scheduling and execution
- State sharing through context frames
- Error isolation and recovery
- System health monitoring

Author: DAWN Development Team
Version: 1.0.0
Last Modified: 2025-06-02
═══════════════════════════════════════════════════════════════════════════════
"""

import json
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Set
from dataclasses import dataclass, field
from collections import defaultdict
import importlib
import inspect

# Configure master logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] 🌅 DAWN ENGINE: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Engine constants
TICK_INTERVAL_MS = 100  # Base tick interval in milliseconds
MAX_MODULE_ERRORS = 3   # Max errors before module is disabled
CONTEXT_HISTORY_SIZE = 100  # How many context frames to keep

# Module scheduling types
class ScheduleType:
    EVERY_TICK = "every_tick"
    EVERY_N_TICKS = "every_n_ticks"
    ON_DEMAND = "on_demand"
    ON_EVENT = "on_event"

# Module categories for organization
class ModuleCategory:
    CORE = "core"
    MEMORY = "memory"
    EMOTIONAL = "emotional"
    SEMANTIC = "semantic"
    MONITORING = "monitoring"
    INTEGRATION = "integration"
    UTILITY = "utility"


@dataclass
class ModuleRegistration:
    """Registration info for a cognitive module."""
    name: str
    module_path: str
    category: ModuleCategory
    schedule_type: str
    interval: int = 1  # For EVERY_N_TICKS
    priority: int = 50  # 0-100, higher = earlier execution
    dependencies: List[str] = field(default_factory=list)
    required_context: List[str] = field(default_factory=list)
    provides_context: List[str] = field(default_factory=list)
    entry_function: Optional[str] = None
    enabled: bool = True
    error_count: int = 0
    last_execution: Optional[int] = None
    
    def should_execute(self, tick: int) -> bool:
        """Check if module should execute on this tick."""
        if not self.enabled:
            return False
            
        if self.schedule_type == ScheduleType.EVERY_TICK:
            return True
        elif self.schedule_type == ScheduleType.EVERY_N_TICKS:
            return tick % self.interval == 0
        else:
            return False  # ON_DEMAND and ON_EVENT handled separately


class DAWNEngine:
    """
    The Consciousness Orchestrator — binds all modules into unified cognition.
    
    "Many threads, one tapestry. Many voices, one song."
    """
    
    def __init__(self, config_path: str = "config/dawn_engine_config.json"):
        """
        Initialize the DAWN Engine.
        
        Args:
            config_path: Path to engine configuration
        """
        self.config_path = Path(config_path)
        self.modules: Dict[str, ModuleRegistration] = {}
        self.loaded_modules: Dict[str, Any] = {}
        self.context_frame: Dict[str, Any] = {}
        self.context_history: List[Dict[str, Any]] = []
        self.current_tick = 0
        self.engine_start_time = datetime.now()
        self.execution_stats: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self.event_queue: List[Dict[str, Any]] = []
        
        # Integration tracking
        self.integration_manifest = {
            "engine_version": "1.0.0",
            "start_time": self.engine_start_time.isoformat(),
            "modules": {},
            "wiring": {},
            "health": {}
        }
        
        logger.info("🌅 DAWN Engine initializing...")
        self._load_configuration()
        self._register_core_modules()
        
    def _load_configuration(self):
        """Load engine configuration from file or create default."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                logger.info(f"📋 Loaded configuration from {self.config_path}")
            else:
                self.config = self._create_default_config()
                self._save_configuration()
        except Exception as e:
            logger.error(f"❌ Error loading config: {e}")
            self.config = self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default engine configuration."""
        return {
            "tick_interval_ms": TICK_INTERVAL_MS,
            "max_module_errors": MAX_MODULE_ERRORS,
            "context_history_size": CONTEXT_HISTORY_SIZE,
            "log_dir": "logs/engine",
            "enable_diagnostics": True,
            "module_timeout_seconds": 5.0
        }
    
    def _save_configuration(self):
        """Save current configuration to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _register_core_modules(self):
        """Register all DAWN cognitive modules."""
        logger.info("📦 Registering cognitive modules...")
        
        # Core system modules
        self.register_module(ModuleRegistration(
            name="tick_engine",
            module_path="tick_engine",
            category=ModuleCategory.CORE,
            schedule_type=ScheduleType.EVERY_TICK,
            priority=100,
            provides_context=["tick", "system_time"]
        ))
        
        self.register_module(ModuleRegistration(
            name="context_frame_builder",
            module_path="context_frame_builder",
            category=ModuleCategory.CORE,
            schedule_type=ScheduleType.EVERY_TICK,
            priority=95,
            entry_function="build_context_frame",
            provides_context=["context_frame", "schema_state"]
        ))
        
        self.register_module(ModuleRegistration(
            name="internal_feedback_loop",
            module_path="internal_feedback_loop",
            category=ModuleCategory.MONITORING,
            schedule_type=ScheduleType.EVERY_N_TICKS,
            interval=25,
            priority=90,
            entry_function="run_internal_feedback_loop",
            required_context=["schema_state"],
            provides_context=["operating_posture", "system_health"]
        ))
        
        # Memory modules
        self.register_module(ModuleRegistration(
            name="memory_decay_manager",
            module_path="memory_decay_manager",
            category=ModuleCategory.MEMORY,
            schedule_type=ScheduleType.EVERY_N_TICKS,
            interval=100,
            priority=70,
            entry_function="manage_memory_decay",
            required_context=["bloom_entries", "tick"]
        ))
        
        self.register_module(ModuleRegistration(
            name="bloom_identity_consolidator",
            module_path="bloom_identity_consolidator",
            category=ModuleCategory.MEMORY,
            schedule_type=ScheduleType.EVERY_N_TICKS,
            interval=200,
            priority=65,
            entry_function="consolidate_bloom_identities",
            required_context=["bloom_entries"]
        ))
        
        # Emotional modules
        self.register_module(ModuleRegistration(
            name="emotional_oversaturation_handler",
            module_path="emotional_oversaturation_handler",
            category=ModuleCategory.EMOTIONAL,
            schedule_type=ScheduleType.EVERY_N_TICKS,
            interval=50,
            priority=75,
            entry_function="handle_emotional_oversaturation",
            required_context=["active_blooms", "tick"]
        ))
        
        self.register_module(ModuleRegistration(
            name="mood_vector_visualizer",
            module_path="mood_vector_visualizer",
            category=ModuleCategory.EMOTIONAL,
            schedule_type=ScheduleType.ON_DEMAND,
            priority=40,
            entry_function="plot_mood_vector_map"
        ))
        
        # Semantic modules
        self.register_module(ModuleRegistration(
            name="semantic_pressure_detector",
            module_path="semantic_pressure_detector",
            category=ModuleCategory.SEMANTIC,
            schedule_type=ScheduleType.EVERY_N_TICKS,
            interval=75,
            priority=60,
            entry_function="detect_semantic_pressure_zones",
            required_context=["bloom_field", "tick"]
        ))
        
        self.register_module(ModuleRegistration(
            name="seed_trust_model",
            module_path="seed_trust_model",
            category=ModuleCategory.SEMANTIC,
            schedule_type=ScheduleType.EVERY_N_TICKS,
            interval=300,
            priority=55,
            entry_function="evaluate_seed_trust",
            required_context=["seed_records"]
        ))
        
        # Monitoring modules
        self.register_module(ModuleRegistration(
            name="schema_coherence_tracker",
            module_path="schema.schema_coherence_tracker",
            category=ModuleCategory.MONITORING,
            schedule_type=ScheduleType.EVERY_N_TICKS,
            interval=50,
            priority=80,
            entry_function="track_coherence",
            provides_context=["coherence_score"]
        ))
        
        self.register_module(ModuleRegistration(
            name="operator_state_tracker",
            module_path="operator_state_tracker",
            category=ModuleCategory.MONITORING,
            schedule_type=ScheduleType.EVERY_TICK,
            priority=85,
            entry_function="track_operator_state",
            provides_context=["operator_present", "operator_mood"]
        ))
        
        # Continue registering remaining modules...
        # [Note: In production, this would be loaded from a module registry file]
        
        logger.info(f"✅ Registered {len(self.modules)} cognitive modules")
    
    def register_module(self, registration: ModuleRegistration):
        """
        Register a cognitive module with the engine.
        
        Args:
            registration: Module registration info
        """
        self.modules[registration.name] = registration
        self.integration_manifest["modules"][registration.name] = {
            "category": registration.category,
            "schedule": registration.schedule_type,
            "priority": registration.priority,
            "status": "registered"
        }
    
    def initialize(self) -> bool:
        """
        Initialize all registered modules and establish wiring.
        
        Returns:
            True if initialization successful, False otherwise
        """
        logger.info("🔧 Initializing cognitive modules...")
        
        # Sort modules by priority for initialization order
        sorted_modules = sorted(
            self.modules.values(), 
            key=lambda m: m.priority, 
            reverse=True
        )
        
        successful_loads = 0
        failed_loads = 0
        
        for module_reg in sorted_modules:
            try:
                # Dynamic import
                module = importlib.import_module(module_reg.module_path)
                self.loaded_modules[module_reg.name] = module
                
                # Find entry point
                if module_reg.entry_function:
                    if hasattr(module, module_reg.entry_function):
                        entry_func = getattr(module, module_reg.entry_function)
                        module_reg.entry_function = entry_func
                    else:
                        # Try to find a class with the entry function
                        for name, obj in inspect.getmembers(module):
                            if inspect.isclass(obj) and hasattr(obj, module_reg.entry_function):
                                instance = obj()
                                entry_func = getattr(instance, module_reg.entry_function)
                                module_reg.entry_function = entry_func
                                self.loaded_modules[f"{module_reg.name}_instance"] = instance
                                break
                
                successful_loads += 1
                self.integration_manifest["modules"][module_reg.name]["status"] = "loaded"
                logger.info(f"✅ Loaded module: {module_reg.name}")
                
            except Exception as e:
                failed_loads += 1
                self.integration_manifest["modules"][module_reg.name]["status"] = "failed"
                self.integration_manifest["modules"][module_reg.name]["error"] = str(e)
                logger.error(f"❌ Failed to load {module_reg.name}: {e}")
                module_reg.enabled = False
        
        # Verify dependencies
        self._verify_dependencies()
        
        # Create wiring report
        self._generate_wiring_report()
        
        logger.info(
            f"🎯 Initialization complete: {successful_loads} loaded, "
            f"{failed_loads} failed"
        )
        
        return failed_loads == 0
    
    def _verify_dependencies(self):
        """Verify all module dependencies are satisfied."""
        logger.info("🔗 Verifying module dependencies...")
        
        # Build provides map
        provides_map = defaultdict(list)
        for name, module in self.modules.items():
            if module.enabled:
                for context_key in module.provides_context:
                    provides_map[context_key].append(name)
        
        # Check requirements
        for name, module in self.modules.items():
            if not module.enabled:
                continue
                
            missing_deps = []
            for required in module.required_context:
                if required not in provides_map:
                    missing_deps.append(required)
            
            if missing_deps:
                logger.warning(
                    f"⚠️ Module {name} missing dependencies: {missing_deps}"
                )
                self.integration_manifest["wiring"][name] = {
                    "status": "incomplete",
                    "missing": missing_deps
                }
            else:
                self.integration_manifest["wiring"][name] = {
                    "status": "wired",
                    "dependencies": module.required_context
                }
    
    def execute_tick(self, tick: int) -> Dict[str, Any]:
        """
        Execute one tick of the cognitive engine.
        
        Args:
            tick: Current tick number
            
        Returns:
            Context frame after tick execution
        """
        self.current_tick = tick
        tick_start = datetime.now()
        
        # Initialize tick context
        self.context_frame["tick"] = tick
        self.context_frame["timestamp"] = tick_start.isoformat()
        
        # Get modules scheduled for this tick
        scheduled_modules = [
            (name, module) for name, module in self.modules.items()
            if module.should_execute(tick)
        ]
        
        # Sort by priority
        scheduled_modules.sort(key=lambda x: x[1].priority, reverse=True)
        
        # Execute modules
        execution_results = {}
        for name, module_reg in scheduled_modules:
            try:
                result = self._execute_module(name, module_reg)
                execution_results[name] = {
                    "status": "success",
                    "result": result
                }
                module_reg.last_execution = tick
                
            except Exception as e:
                execution_results[name] = {
                    "status": "error",
                    "error": str(e)
                }
                self._handle_module_error(name, module_reg, e)
        
        # Process event queue
        self._process_events()
        
        # Update context history
        self._update_context_history()
        
        # Record tick execution time
        tick_duration = (datetime.now() - tick_start).total_seconds()
        self.execution_stats[tick] = {
            "duration": tick_duration,
            "modules_executed": len(scheduled_modules),
            "results": execution_results
        }
        
        return self.context_frame.copy()
    
    def _execute_module(self, name: str, module_reg: ModuleRegistration) -> Any:
        """
        Execute a single module with error isolation.
        
        Args:
            name: Module name
            module_reg: Module registration
            
        Returns:
            Module execution result
        """
        # Prepare module context
        module_context = {}
        for required in module_reg.required_context:
            if required in self.context_frame:
                module_context[required] = self.context_frame[required]
        
        # Execute module
        if module_reg.entry_function:
            if callable(module_reg.entry_function):
                # Call with appropriate arguments
                sig = inspect.signature(module_reg.entry_function)
                if len(sig.parameters) == 1:
                    # Single parameter - pass full context
                    result = module_reg.entry_function(module_context)
                elif len(sig.parameters) == 2:
                    # Two parameters - assume second is tick
                    result = module_reg.entry_function(
                        module_context, 
                        self.current_tick
                    )
                else:
                    # Call with unpacked context
                    result = module_reg.entry_function(**module_context)
            else:
                raise ValueError(f"Entry function for {name} is not callable")
        else:
            # No entry function specified
            result = None
        
        # Update context with provided values
        if result and isinstance(result, dict):
            for key in module_reg.provides_context:
                if key in result:
                    self.context_frame[key] = result[key]
        
        return result
    
    def _handle_module_error(self, name: str, module_reg: ModuleRegistration, error: Exception):
        """Handle module execution error."""
        module_reg.error_count += 1
        logger.error(f"❌ Module {name} error ({module_reg.error_count}): {error}")
        logger.debug(traceback.format_exc())
        
        # Disable module if too many errors
        if module_reg.error_count >= self.config.get("max_module_errors", MAX_MODULE_ERRORS):
            module_reg.enabled = False
            logger.warning(f"🚫 Module {name} disabled due to repeated errors")
            self.integration_manifest["modules"][name]["status"] = "disabled"
    
    def _process_events(self):
        """Process queued events."""
        processed = []
        for event in self.event_queue:
            try:
                self._handle_event(event)
                processed.append(event)
            except Exception as e:
                logger.error(f"❌ Error processing event: {e}")
        
        # Remove processed events
        for event in processed:
            self.event_queue.remove(event)
    
    def _handle_event(self, event: Dict[str, Any]):
        """Handle a single event."""
        event_type = event.get("type")
        
        # Find modules that handle this event type
        for name, module_reg in self.modules.items():
            if module_reg.schedule_type == ScheduleType.ON_EVENT:
                # Check if module handles this event type
                # [Implementation depends on module event registration]
                pass
    
    def _update_context_history(self):
        """Update context frame history."""
        self.context_history.append(self.context_frame.copy())
        
        # Limit history size
        max_history = self.config.get("context_history_size", CONTEXT_HISTORY_SIZE)
        if len(self.context_history) > max_history:
            self.context_history = self.context_history[-max_history:]
    
    def _generate_wiring_report(self):
        """Generate comprehensive wiring report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "engine_version": "1.0.0",
            "modules": {
                "total": len(self.modules),
                "enabled": sum(1 for m in self.modules.values() if m.enabled),
                "by_category": defaultdict(int),
                "by_schedule": defaultdict(int)
            },
            "wiring": {
                "complete": [],
                "incomplete": [],
                "dependencies": {}
            },
            "context_providers": defaultdict(list),
            "integration_status": "healthy"
        }
        
        # Analyze modules
        for name, module in self.modules.items():
            report["modules"]["by_category"][module.category] += 1
            report["modules"]["by_schedule"][module.schedule_type] += 1
            
            if name in self.integration_manifest["wiring"]:
                wiring_status = self.integration_manifest["wiring"][name]["status"]
                if wiring_status == "wired":
                    report["wiring"]["complete"].append(name)
                else:
                    report["wiring"]["incomplete"].append(name)
            
            for provided in module.provides_context:
                report["context_providers"][provided].append(name)
        
        # Save report
        report_path = Path("logs/diagnostics/schema_wiring_report.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📝 Wiring report saved to {report_path}")
    
    def trigger_module(self, module_name: str, **kwargs) -> Any:
        """
        Manually trigger an on-demand module.
        
        Args:
            module_name: Name of module to trigger
            **kwargs: Arguments to pass to module
            
        Returns:
            Module execution result
        """
        if module_name not in self.modules:
            raise ValueError(f"Unknown module: {module_name}")
        
        module_reg = self.modules[module_name]
        if module_reg.schedule_type != ScheduleType.ON_DEMAND:
            logger.warning(f"Module {module_name} is not on-demand type")
        
        # Add kwargs to context temporarily
        old_context = self.context_frame.copy()
        self.context_frame.update(kwargs)
        
        try:
            result = self._execute_module(module_name, module_reg)
            return result
        finally:
            # Restore context
            self.context_frame = old_context
    
    def get_module_stats(self, module_name: str) -> Dict[str, Any]:
        """Get execution statistics for a module."""
        if module_name not in self.modules:
            return {"error": "Unknown module"}
        
        module_reg = self.modules[module_name]
        
        # Calculate execution stats
        executions = [
            stats["results"].get(module_name)
            for stats in self.execution_stats.values()
            if module_name in stats.get("results", {})
        ]
        
        success_count = sum(1 for e in executions if e and e["status"] == "success")
        error_count = sum(1 for e in executions if e and e["status"] == "error")
        
        return {
            "name": module_name,
            "category": module_reg.category,
            "enabled": module_reg.enabled,
            "total_executions": len(executions),
            "successful": success_count,
            "errors": error_count,
            "error_rate": error_count / max(len(executions), 1),
            "last_execution": module_reg.last_execution,
            "dependencies": module_reg.required_context,
            "provides": module_reg.provides_context
        }
    
    def save_integration_manifest(self):
        """Save the integration manifest to file."""
        manifest_path = Path("dawn_integration_manifest.json")
        
        # Add current health metrics
        self.integration_manifest["health"] = {
            "uptime_seconds": (datetime.now() - self.engine_start_time).total_seconds(),
            "total_ticks": self.current_tick,
            "enabled_modules": sum(1 for m in self.modules.values() if m.enabled),
            "disabled_modules": sum(1 for m in self.modules.values() if not m.enabled),
            "last_update": datetime.now().isoformat()
        }
        
        with open(manifest_path, 'w') as f:
            json.dump(self.integration_manifest, f, indent=2)
        
        logger.info(f"💾 Integration manifest saved to {manifest_path}")
    
    def shutdown(self):
        """Gracefully shutdown the engine."""
        logger.info("🌙 DAWN Engine shutting down...")
        
        # Save final state
        self.save_integration_manifest()
        self._generate_wiring_report()
        
        # Clean up modules
        for name, module_reg in self.modules.items():
            try:
                # Call cleanup if available
                if hasattr(self.loaded_modules.get(name), 'cleanup'):
                    self.loaded_modules[name].cleanup()
            except Exception as e:
                logger.error(f"Error cleaning up {name}: {e}")
        
        logger.info("👋 DAWN Engine shutdown complete")


# Convenience functions for external usage
def create_dawn_engine(config_path: Optional[str] = None) -> DAWNEngine:
    """Create and initialize a DAWN Engine instance."""
    engine = DAWNEngine(config_path or "config/dawn_engine_config.json")
    engine.initialize()
    return engine


def run_dawn_tick(engine: DAWNEngine, tick: int) -> Dict[str, Any]:
    """Execute a single tick of the DAWN engine."""
    return engine.execute_tick(tick)


if __name__ == "__main__":
    """
    Demonstration of DAWN Engine initialization and execution.
    """
    
    print("🌅 DAWN ENGINE INITIALIZATION")
    print("=" * 60)
    
    # Create and initialize engine
    engine = create_dawn_engine()
    
    # Show loaded modules
    print(f"\n📦 Loaded Modules: {len(engine.modules)}")
    for category in ModuleCategory.__dict__.values():
        if isinstance(category, str):
            count = sum(1 for m in engine.modules.values() if m.category == category)
            if count > 0:
                print(f"  {category}: {count} modules")
    
    # Run a few ticks
    print("\n🔄 Running initial ticks...")
    for tick in range(5):
        context = run_dawn_tick(engine, tick)
        print(f"  Tick {tick}: {len(context)} context keys")
    
    # Show module stats
    print("\n📊 Module Statistics:")
    for name in ["internal_feedback_loop", "memory_decay_manager"]:
        stats = engine.get_module_stats(name)
        if "error" not in stats:
            print(f"  {name}: {stats['total_executions']} executions")
    
    # Save manifest
    engine.save_integration_manifest()
    print("\n✅ Integration manifest saved")
    
    # Shutdown
    engine.shutdown()