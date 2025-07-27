"""
DAWN Orchestrator - Central Import Hub
Manages module initialization and prevents circular imports
"""

import os
import sys
from typing import Dict, Any, Optional
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.absolute()
sys.path.append(str(PROJECT_ROOT))

# Module handles dictionary
_module_handles: Dict[str, Any] = {}

def initialize_module(module_name: str) -> Optional[Any]:
    """Initialize a module and return its handle"""
    if module_name in _module_handles:
        return _module_handles[module_name]
        
    try:
        if module_name == "pulse":
            from pulse.pulse_loader import load_pulse_system
            pulse, tick_thermal_update, add_heat, scup_tracker = load_pulse_system()
            _module_handles["pulse"] = {
                "pulse": pulse,
                "tick_thermal_update": tick_thermal_update,
                "add_heat": add_heat,
                "scup_tracker": scup_tracker
            }
            
        elif module_name == "schema":
            from schema.schema_manager import SchemaManager
            _module_handles["schema"] = SchemaManager()
            
        elif module_name == "memory":
            from memories.memory_manager import MemoryManager
            _module_handles["memory"] = MemoryManager()
            
        elif module_name == "cognitive":
            from cognitive.cognitive_engine import CognitiveEngine
            _module_handles["cognitive"] = CognitiveEngine()
            
        elif module_name == "visual":
            from visual.visual_processor import VisualProcessor
            _module_handles["visual"] = VisualProcessor()
            
        return _module_handles[module_name]
        
    except Exception as e:
        print(f"Failed to initialize {module_name}: {e}")
        return None

def get_module(module_name: str) -> Optional[Any]:
    """Get a module handle, initializing it if necessary"""
    if module_name not in _module_handles:
        return initialize_module(module_name)
    return _module_handles[module_name]

def shutdown_modules():
    """Clean shutdown of all initialized modules"""
    for module_name, handle in _module_handles.items():
        try:
            if hasattr(handle, "shutdown"):
                handle.shutdown()
        except Exception as e:
            print(f"Error shutting down {module_name}: {e}")
    _module_handles.clear() 