#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
                           DAWN SCHEMA REGISTRY
                        The Unified Import Interface
═══════════════════════════════════════════════════════════════════════════════

"Each module a neuron, each import a synapse, together forming the mind of DAWN."

This module serves as the central registry for all DAWN cognitive components,
providing a clean import interface and automatic registration system. It maps
the entire cognitive architecture, making each module discoverable and accessible
through a unified namespace.

Author: DAWN Development Team
Version: 1.0.0
Last Modified: 2025-06-02
═══════════════════════════════════════════════════════════════════════════════
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Configure module registry logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Module registry version
REGISTRY_VERSION = "1.0.0"

# Module categories and their descriptions
MODULE_CATEGORIES = {
    "core": "Core system modules that form DAWN's foundation",
    "memory": "Memory management and bloom lifecycle modules",
    "emotional": "Emotional processing and mood regulation modules",
    "semantic": "Semantic analysis and meaning extraction modules",
    "monitoring": "System health and performance monitoring modules",
    "integration": "External system integration bridges",
    "utility": "Helper and utility modules"
}

# Complete module registry with metadata
MODULE_REGISTRY = {
    # Core Modules
    "belief_anchor_manager": {
        "category": "core",
        "path": "belief_anchor_manager",
        "class": "BeliefAnchorManager",
        "entry": "manage_belief_anchors",
        "schedule": "every_n_ticks",
        "interval": 100,
        "description": "Manages core belief structures and semantic anchors"
    },
    
    "coherence_recovery_protocol": {
        "category": "core",
        "path": "coherence_recovery_protocol",
        "class": "CoherenceRecoveryProtocol",
        "entry": "execute_recovery",
        "schedule": "on_event",
        "description": "Recovers system coherence when fragmentation detected"
    },
    
    "context_frame_builder": {
        "category": "core",
        "path": "context_frame_builder",
        "class": "ContextFrameBuilder",
        "entry": "build_context_frame",
        "schedule": "every_tick",
        "description": "Builds unified context frames for module communication"
    },
    
    "initiation_protocol_generator": {
        "category": "core",
        "path": "initiation_protocol_generator",
        "class": "InitiationProtocolGenerator",
        "entry": "evaluate_initiation_conditions",
        "schedule": "on_demand",
        "description": "Manages DAWN's awakening sequence and preconditions"
    },
    
    "internal_feedback_loop": {
        "category": "core",
        "path": "internal_feedback_loop",
        "class": "InternalFeedbackLoop",
        "entry": "run_internal_feedback_loop",
        "schedule": "every_n_ticks",
        "interval": 25,
        "description": "Meta-regulatory system for self-monitoring and adjustment"
    },
    
    # Memory Modules
    "bloom_identity_consolidator": {
        "category": "memory",
        "path": "bloom_identity_consolidator",
        "class": "BloomIdentityConsolidator",
        "entry": "consolidate_bloom_identities",
        "schedule": "every_n_ticks",
        "interval": 200,
        "description": "Merges semantically identical blooms"
    },
    
    "memory_decay_manager": {
        "category": "memory",
        "path": "memory_decay_manager",
        "class": "MemoryDecayManager",
        "entry": "manage_memory_decay",
        "schedule": "every_n_ticks",
        "interval": 100,
        "description": "Manages natural memory fading for cognitive hygiene"
    },
    
    "fallback_memory_router": {
        "category": "memory",
        "path": "fallback_memory_router",
        "class": "FallbackMemoryRouter",
        "entry": "route_memory_request",
        "schedule": "on_event",
        "description": "Routes memory requests when primary paths fail"
    },
    
    "rebloom_chain_analyzer": {
        "category": "memory",
        "path": "rebloom_chain_analyzer",
        "class": "RebloomChainAnalyzer",
        "entry": "analyze_rebloom_chains",
        "schedule": "every_n_ticks",
        "interval": 150,
        "description": "Analyzes patterns in bloom regeneration chains"
    },
    
    "rebloom_stabilizer": {
        "category": "memory",
        "path": "rebloom_stabilizer",
        "class": "RebloomStabilizer",
        "entry": "stabilize_reblooms",
        "schedule": "every_n_ticks",
        "interval": 75,
        "description": "Prevents excessive reblooming cycles"
    },
    
    # Emotional Modules
    "emotional_oversaturation_handler": {
        "category": "emotional",
        "path": "emotional_oversaturation_handler",
        "class": "EmotionalOversaturationHandler",
        "entry": "handle_emotional_oversaturation",
        "schedule": "every_n_ticks",
        "interval": 50,
        "description": "Prevents emotional monocultures from overwhelming cognition"
    },
    
    "mood_drift_surface_plotter": {
        "category": "emotional",
        "path": "mood_drift_surface_plotter",
        "class": "MoodDriftSurfacePlotter",
        "entry": "plot_mood_surface",
        "schedule": "on_demand",
        "description": "Visualizes emotional topology over time"
    },
    
    "mood_vector_visualizer": {
        "category": "emotional",
        "path": "mood_vector_visualizer",
        "class": "MoodVectorVisualizer",
        "entry": "plot_mood_vector_map",
        "schedule": "on_demand",
        "description": "Maps emotional drift through bloom lineages"
    },
    
    # Semantic Modules
    "semantic_pressure_detector": {
        "category": "semantic",
        "path": "semantic_pressure_detector",
        "class": "SemanticPressureDetector",
        "entry": "detect_semantic_pressure_zones",
        "schedule": "every_n_ticks",
        "interval": 75,
        "description": "Detects overcrowding in semantic space"
    },
    
    "seed_trust_model": {
        "category": "semantic",
        "path": "seed_trust_model",
        "class": "SeedTrustModel",
        "entry": "evaluate_seed_trust",
        "schedule": "every_n_ticks",
        "interval": 300,
        "description": "Evaluates reliability of semantic seed origins"
    },
    
    "contradiction_resolver": {
        "category": "semantic",
        "path": "contradiction_resolver",
        "class": "ContradictionResolver",
        "entry": "resolve_contradictions",
        "schedule": "on_event",
        "description": "Resolves conflicting beliefs and patterns"
    },
    
    "drift_vector_field": {
        "category": "semantic",
        "path": "drift_vector_field",
        "class": "DriftVectorField",
        "entry": "calculate_drift_field",
        "schedule": "every_n_ticks",
        "interval": 100,
        "description": "Maps semantic drift patterns across bloom space"
    },
    
    # Monitoring Modules
    "schema_coherence_tracker": {
        "category": "monitoring",
        "path": "schema.schema_coherence_tracker",
        "class": "SchemaCoherenceTracker",
        "entry": "track_coherence",
        "schedule": "every_n_ticks",
        "interval": 50,
        "description": "Monitors overall system coherence"
    },
    
    "operator_state_tracker": {
        "category": "monitoring",
        "path": "operator_state_tracker",
        "class": "OperatorStateTracker",
        "entry": "track_operator_state",
        "schedule": "every_tick",
        "description": "Tracks operator presence and engagement"
    },
    
    "owl_entropy_sweeper": {
        "category": "monitoring",
        "path": "owl_entropy_sweeper",
        "class": "OwlEntropySweeper",
        "entry": "sweep_entropy",
        "schedule": "every_n_ticks",
        "interval": 100,
        "description": "Monitors and manages system entropy levels"
    },
    
    "interruption_detector": {
        "category": "monitoring",
        "path": "interruption_detector",
        "class": "InterruptionDetector",
        "entry": "detect_interruptions",
        "schedule": "every_tick",
        "description": "Detects conversation flow interruptions"
    },
    
    # Integration Modules
    "claude_artifact_cache_bridge": {
        "category": "integration",
        "path": "claude_artifact_cache_bridge",
        "class": "ClaudeArtifactCacheBridge",
        "entry": "bridge_artifacts",
        "schedule": "on_event",
        "description": "Bridges Claude artifacts with DAWN memory"
    },
    
    "claude_chat_logger": {
        "category": "integration",
        "path": "claude_chat_logger",
        "class": "ClaudeChatLogger",
        "entry": "log_chat",
        "schedule": "on_event",
        "description": "Logs Claude conversation data"
    },
    
    "dawn_notion_bridge": {
        "category": "integration",
        "path": "dawn_notion_bridge",
        "class": "DawnNotionBridge",
        "entry": "sync_with_notion",
        "schedule": "every_n_ticks",
        "interval": 600,
        "description": "Synchronizes DAWN state with Notion database"
    },
    
    "parmenides_token_linker": {
        "category": "integration",
        "path": "parmenides_token_linker",
        "class": "ParmenidesTokenLinker",
        "entry": "link_tokens",
        "schedule": "on_event",
        "description": "Links external tokens with DAWN concepts"
    },
    
    # Utility Modules
    "fractal_signature_generator": {
        "category": "utility",
        "path": "fractal_signature_generator",
        "class": "FractalSignatureGenerator",
        "entry": "generate_signatures",
        "schedule": "on_demand",
        "description": "Generates unique fractal signatures for patterns"
    },
    
    "gas_pedal_logic": {
        "category": "utility",
        "path": "gas_pedal_logic",
        "class": "GasPedalLogic",
        "entry": "adjust_processing_speed",
        "schedule": "every_n_ticks",
        "interval": 10,
        "description": "Controls cognitive processing speed"
    },
    
    "log_pruner": {
        "category": "utility",
        "path": "log_pruner",
        "class": "LogPruner",
        "entry": "prune_logs",
        "schedule": "every_n_ticks",
        "interval": 1000,
        "description": "Manages log file growth and archival"
    },
    
    "nutrient_map_generator": {
        "category": "utility",
        "path": "nutrient_map_generator",
        "class": "NutrientMapGenerator",
        "entry": "generate_nutrient_map",
        "schedule": "on_demand",
        "description": "Maps cognitive resource distribution"
    },
    
    "pressure_reflection_loop": {
        "category": "utility",
        "path": "pressure_reflection_loop",
        "class": "PressureReflectionLoop",
        "entry": "reflect_on_pressure",
        "schedule": "every_n_ticks",
        "interval": 200,
        "description": "Reflects on system pressure patterns"
    },
    
    "pruning_logic": {
        "category": "utility",
        "path": "pruning_logic",
        "class": "PruningLogic",
        "entry": "execute_pruning",
        "schedule": "every_n_ticks",
        "interval": 500,
        "description": "Prunes low-value cognitive branches"
    },
    
    "recursive_priority_index": {
        "category": "utility",
        "path": "recursive_priority_index",
        "class": "RecursivePriorityIndex",
        "entry": "update_priorities",
        "schedule": "every_n_ticks",
        "interval": 100,
        "description": "Manages recursive priority calculations"
    },
    
    "temporal_field_calculator": {
        "category": "utility",
        "path": "temporal_field_calculator",
        "class": "TemporalFieldCalculator",
        "entry": "calculate_temporal_field",
        "schedule": "on_demand",
        "description": "Calculates temporal influence fields"
    },
    
    # Additional specialized modules
    "internal_monologue_generator": {
        "category": "core",
        "path": "internal_monologue_generator",
        "class": "InternalMonologueGenerator",
        "entry": "generate_monologue",
        "schedule": "on_demand",
        "description": "Generates DAWN's internal thought stream"
    },
    
    "rebloom_depth_stats": {
        "category": "monitoring",
        "path": "rebloom_depth_stats",
        "class": "RebloomDepthStats",
        "entry": "calculate_depth_stats",
        "schedule": "every_n_ticks",
        "interval": 250,
        "description": "Analyzes rebloom depth distributions"
    },
    
    "rebloom_prediction_model": {
        "category": "semantic",
        "path": "rebloom_prediction_model",
        "class": "RebloomPredictionModel",
        "entry": "predict_reblooms",
        "schedule": "every_n_ticks",
        "interval": 150,
        "description": "Predicts future rebloom patterns"
    },
    
    "sigil_lifecycle_manager": {
        "category": "core",
        "path": "sigil_lifecycle_manager",
        "class": "SigilLifecycleManager",
        "entry": "manage_sigil_lifecycle",
        "schedule": "every_n_ticks",
        "interval": 50,
        "description": "Manages symbolic sigil creation and decay"
    },
    
    "sigil_reinforcement_tracker": {
        "category": "monitoring",
        "path": "sigil_reinforcement_tracker",
        "class": "SigilReinforcementTracker",
        "entry": "track_reinforcement",
        "schedule": "every_n_ticks",
        "interval": 75,
        "description": "Tracks sigil activation and reinforcement patterns"
    }
}


@dataclass
class ModuleInfo:
    """Information about a registered module."""
    name: str
    category: str
    path: str
    class_name: Optional[str]
    entry_function: Optional[str]
    schedule_type: str
    interval: Optional[int]
    description: str
    loaded: bool = False
    instance: Optional[Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            k: v for k, v in asdict(self).items() 
            if k not in ['instance']
        }


class DAWNModuleRegistry:
    """
    Central registry for all DAWN cognitive modules.
    
    "The map is not the territory, but without a map, the territory is unknowable."
    """
    
    def __init__(self):
        """Initialize the module registry."""
        self.modules: Dict[str, ModuleInfo] = {}
        self.loaded_modules: Dict[str, Any] = {}
        self.categories: Dict[str, List[str]] = {cat: [] for cat in MODULE_CATEGORIES}
        self._initialize_registry()
        
    def _initialize_registry(self):
        """Initialize the registry from the module definitions."""
        for name, config in MODULE_REGISTRY.items():
            module_info = ModuleInfo(
                name=name,
                category=config["category"],
                path=config["path"],
                class_name=config.get("class"),
                entry_function=config.get("entry"),
                schedule_type=config["schedule"],
                interval=config.get("interval"),
                description=config["description"]
            )
            
            self.modules[name] = module_info
            self.categories[config["category"]].append(name)
        
        logger.info(f"📚 Initialized registry with {len(self.modules)} modules")
    
    def get_module(self, name: str) -> Optional[ModuleInfo]:
        """Get module information by name."""
        return self.modules.get(name)
    
    def get_modules_by_category(self, category: str) -> List[ModuleInfo]:
        """Get all modules in a category."""
        module_names = self.categories.get(category, [])
        return [self.modules[name] for name in module_names]
    
    def get_modules_by_schedule(self, schedule_type: str) -> List[ModuleInfo]:
        """Get all modules with a specific schedule type."""
        return [
            module for module in self.modules.values()
            if module.schedule_type == schedule_type
        ]
    
    def load_module(self, name: str) -> Optional[Any]:
        """
        Dynamically load a module and return its instance.
        
        Args:
            name: Module name
            
        Returns:
            Module instance or None if failed
        """
        if name not in self.modules:
            logger.error(f"Unknown module: {name}")
            return None
        
        module_info = self.modules[name]
        
        if module_info.loaded and name in self.loaded_modules:
            return self.loaded_modules[name]
        
        try:
            # Dynamic import
            module = __import__(module_info.path, fromlist=[module_info.class_name or ''])
            
            # Get class if specified
            if module_info.class_name:
                module_class = getattr(module, module_info.class_name)
                instance = module_class()
                self.loaded_modules[name] = instance
                module_info.instance = instance
            else:
                self.loaded_modules[name] = module
                module_info.instance = module
            
            module_info.loaded = True
            logger.info(f"✅ Loaded module: {name}")
            return module_info.instance
            
        except Exception as e:
            logger.error(f"❌ Failed to load module {name}: {e}")
            return None
    
    def get_entry_function(self, name: str) -> Optional[callable]:
        """Get the entry function for a module."""
        module_info = self.modules.get(name)
        if not module_info:
            return None
        
        # Load module if needed
        if not module_info.loaded:
            self.load_module(name)
        
        if module_info.instance and module_info.entry_function:
            return getattr(module_info.instance, module_info.entry_function, None)
        
        return None
    
    def generate_registry_report(self) -> Dict[str, Any]:
        """Generate a comprehensive registry report."""
        report = {
            "version": REGISTRY_VERSION,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_modules": len(self.modules),
                "loaded_modules": sum(1 for m in self.modules.values() if m.loaded),
                "categories": {}
            },
            "modules": {},
            "schedule_distribution": {},
            "dependencies": {}
        }
        
        # Category summary
        for category, description in MODULE_CATEGORIES.items():
            report["summary"]["categories"][category] = {
                "description": description,
                "count": len(self.categories[category])
            }
        
        # Module details
        for name, module_info in self.modules.items():
            report["modules"][name] = module_info.to_dict()
        
        # Schedule distribution
        for module in self.modules.values():
            schedule = module.schedule_type
            if schedule not in report["schedule_distribution"]:
                report["schedule_distribution"][schedule] = []
            report["schedule_distribution"][schedule].append(module.name)
        
        return report
    
    def export_registry(self, path: str = "dawn_module_registry.json"):
        """Export the registry to a JSON file."""
        report = self.generate_registry_report()
        
        with open(path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📄 Registry exported to {path}")


# Global registry instance
registry = DAWNModuleRegistry()

# Convenience functions for module access
def get_module(name: str) -> Optional[Any]:
    """Get a loaded module instance by name."""
    return registry.load_module(name)


def get_module_info(name: str) -> Optional[ModuleInfo]:
    """Get module information by name."""
    return registry.get_module(name)


def list_modules(category: Optional[str] = None) -> List[str]:
    """List all module names, optionally filtered by category."""
    if category:
        return [m.name for m in registry.get_modules_by_category(category)]
    return list(registry.modules.keys())


def get_entry_function(module_name: str) -> Optional[callable]:
    """Get the entry function for a module."""
    return registry.get_entry_function(module_name)


# Module category exports for easier access
core_modules = lambda: registry.get_modules_by_category("core")
memory_modules = lambda: registry.get_modules_by_category("memory")
emotional_modules = lambda: registry.get_modules_by_category("emotional")
semantic_modules = lambda: registry.get_modules_by_category("semantic")
monitoring_modules = lambda: registry.get_modules_by_category("monitoring")
integration_modules = lambda: registry.get_modules_by_category("integration")
utility_modules = lambda: registry.get_modules_by_category("utility")

# Schedule type exports
tick_modules = lambda: registry.get_modules_by_schedule("every_tick")
periodic_modules = lambda: registry.get_modules_by_schedule("every_n_ticks")
on_demand_modules = lambda: registry.get_modules_by_schedule("on_demand")
event_modules = lambda: registry.get_modules_by_schedule("on_event")


# Auto-export all module names for star imports
__all__ = [
    'registry',
    'get_module',
    'get_module_info',
    'list_modules',
    'get_entry_function',
    'core_modules',
    'memory_modules',
    'emotional_modules',
    'semantic_modules',
    'monitoring_modules',
    'integration_modules',
    'utility_modules',
    'tick_modules',
    'periodic_modules',
    'on_demand_modules',
    'event_modules',
    'MODULE_REGISTRY',
    'MODULE_CATEGORIES',
    'ModuleInfo',
    'DAWNModuleRegistry'
]

# Add all module names to __all__ for easy importing
__all__.extend(MODULE_REGISTRY.keys())

# Dynamic attribute access for modules
def __getattr__(name: str):
    """Enable dynamic module access via schema.module_name."""
    if name in MODULE_REGISTRY:
        return get_module(name)
    raise AttributeError(f"Module '{name}' not found in DAWN schema")


if __name__ == "__main__":
    """Test the module registry."""
    
    print("🌅 DAWN MODULE REGISTRY")
    print("=" * 60)
    
    # Show categories
    print("\n📚 Module Categories:")
    for category, description in MODULE_CATEGORIES.items():
        count = len(registry.categories[category])
        print(f"  {category}: {count} modules - {description}")
    
    # Show schedule distribution  
    print("\n⏰ Schedule Types:")
    report = registry.generate_registry_report()
    for schedule, modules in report["schedule_distribution"].items():
        print(f"  {schedule}: {len(modules)} modules")
    
    # Test loading a module
    print("\n🧪 Testing module loading:")
    test_module = "internal_feedback_loop"
    module = get_module(test_module)
    if module:
        print(f"  ✅ Successfully loaded: {test_module}")
        func = get_entry_function(test_module)
        if func:
            print(f"  ✅ Entry function found: {func.__name__}")
    
    # Export registry
    registry.export_registry()
    print("\n📄 Registry exported to dawn_module_registry.json")