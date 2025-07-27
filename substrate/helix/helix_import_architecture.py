# substrate/helix/helix_import_architecture.py
"""
Helix Import Architecture - Dynamic Component Loading
====================================================
Special import system for DAWN's consciousness components
"""

import importlib
import sys
from typing import Any, Dict, Optional, Set, List, Tuple
from pathlib import Path
import re
from datetime import datetime
import weakref
import logging
import asyncio
from enum import Enum
from dataclasses import dataclass
from typing import Protocol
import json
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('helix_import')

class ComponentStatus(Enum):
    UNKNOWN = "unknown"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    ERROR = "error"
    STUB = "stub"
    DEPRECATED = "deprecated"

@dataclass
class ComponentInfo:
    name: str
    version: str
    status: ComponentStatus
    dependencies: List[str]
    last_health_check: datetime
    health_status: bool
    error_message: Optional[str] = None

class ComponentLifecycle(Protocol):
    async def initialize(self) -> None: ...
    async def shutdown(self) -> None: ...
    async def health_check(self) -> bool: ...

# Module mappings for helix imports
HELIX_MAPPINGS = {
    'pulse_heat': 'pulse.pulse_heat.PulseHeat',
    'bloom_engine': 'bloom.bloom_engine.BloomEngine',
    'owl_system': 'reflection.owl.owl.OwlSystem',
    'sigil_processor': 'processors.codex.sigils.SigilProcessor',
    'tick_engine': 'core.tick_emitter.TickEngine',
    'semantic_engine': 'semantic.semantic_context_engine.SemanticContextEngine',
}

# Component tracking
_component_cache: Dict[str, Any] = {}
_import_history: Dict[str, datetime] = {}
_circular_deps: Set[str] = set()
_stub_components: Set[str] = set()
_component_info: Dict[str, ComponentInfo] = {}
_component_dependencies: Dict[str, Set[str]] = {}
_version_requirements: Dict[str, Dict[str, str]] = {}

# Pulse state tracking
PULSE_STATE_PATH = "pulse_state.json"

def update_pulse_state():
    """Update the pulse state file with current component status"""
    state = {
        "components_loaded": len(_component_cache),
        "genome_components": {},
        "last_update": datetime.now().isoformat(),
        "component_status": {}
    }
    
    # Track genome components
    for name, component in _component_cache.items():
        if 'genome' in name.lower() or 'sequencer' in name.lower():
            status = "stub" if is_stub_component(component) else "active"
            state["genome_components"][name] = status
        
        # Track all component statuses
        if name in _component_info:
            info = _component_info[name]
            state["component_status"][name] = {
                "status": info.status.value,
                "version": info.version,
                "health": info.health_status,
                "last_check": info.last_health_check.isoformat()
            }
    
    # Write to file
    try:
        with open(PULSE_STATE_PATH, 'w') as f:
            json.dump(state, f, indent=2)
        logger.debug("Updated pulse state file")
    except Exception as e:
        logger.error(f"Failed to update pulse state: {e}")

async def check_mood_state() -> Tuple[float, float]:
    """
    Check current mood state for entropy and fragility
    Returns: (entropy_level, fragility_level) both 0.0 to 1.0
    """
    try:
        # Try to import mood engine
        mood_engine = await helix_import('mood_engine', force_reload=True)
        if not is_stub_component(mood_engine):
            entropy = await mood_engine.get_entropy()
            fragility = await mood_engine.get_fragility()
            return entropy, fragility
    except Exception as e:
        logger.warning(f"Failed to get mood state: {e}")
    
    # Default to low entropy/fragility if mood engine unavailable
    return 0.0, 0.0

def should_defer_initialization(entropy: float, fragility: float, force: bool = False) -> bool:
    """
    Determine if component initialization should be deferred based on mood state
    """
    if force:
        return False
    
    # Defer if either entropy or fragility is high
    return entropy > 0.7 or fragility > 0.7

def validate_component_name(name: str) -> bool:
    """Validate component name format"""
    if not name or not isinstance(name, str):
        logger.error(f"Invalid component name type: {type(name)}")
        return False
    # Allow alphanumeric, dots, and underscores
    if not re.match(r'^[a-zA-Z0-9_.]+$', name):
        logger.error(f"Invalid component name format: {name}")
        return False
    return True

def is_stub_component(component: Any) -> bool:
    """Check if a component is a stub"""
    return hasattr(component, '_stub') and component._stub

def get_component_version(component: Any) -> str:
    """Get component version if available"""
    try:
        return getattr(component, '__version__', 'unknown')
    except Exception as e:
        logger.warning(f"Failed to get version for component: {e}")
        return 'unknown'

def check_version_compatibility(component_name: str, version: str) -> bool:
    """Check if component version is compatible with requirements"""
    if component_name not in _version_requirements:
        return True
    
    requirements = _version_requirements[component_name]
    try:
        from packaging import version as pkg_version
        current = pkg_version.parse(version)
        required = pkg_version.parse(requirements.get('min_version', '0.0.0'))
        max_required = pkg_version.parse(requirements.get('max_version', '999.999.999'))
        
        return required <= current <= max_required
    except Exception as e:
        logger.error(f"Version compatibility check failed: {e}")
        return False

async def check_component_health(component_name: str) -> bool:
    """Check component health status"""
    if component_name not in _component_cache:
        logger.error(f"Component not found: {component_name}")
        return False
    
    component = _component_cache[component_name]
    try:
        if hasattr(component, 'health_check'):
            return await component.health_check()
        return True
    except Exception as e:
        logger.error(f"Health check failed for {component_name}: {e}")
        return False

def register_genome_component(name: str, path: str, dependencies: List[str] = None, version_requirements: Dict[str, str] = None) -> bool:
    """
    Register a new genome component for dynamic loading.
    
    Args:
        name: The component name to register (must contain 'genome' or 'sequencer')
        path: The full import path for the component (e.g., 'module.submodule.ClassName')
        dependencies: List of component names this component depends on
        version_requirements: Dict of version requirements (min_version, max_version)
    
    Returns:
        bool: True if registration was successful, False if:
            - name doesn't contain 'genome' or 'sequencer'
            - path is invalid
            - name already exists in mappings
            - path already exists in mappings
    
    Raises:
        ValueError: If name or path is empty or invalid
    """
    if not name or not path:
        raise ValueError("Component name and path cannot be empty")
    
    if not isinstance(name, str) or not isinstance(path, str):
        raise ValueError("Component name and path must be strings")
    
    # Check if this is a genome-related component
    if 'genome' not in name.lower() and 'sequencer' not in name.lower():
        logger.warning(f"Component {name} doesn't appear to be a genome component")
        return False
    
    # Check for name collision
    if name in HELIX_MAPPINGS:
        logger.warning(f"Component name '{name}' already registered")
        return False
    
    # Check for path collision
    if path in HELIX_MAPPINGS.values():
        logger.warning(f"Import path '{path}' already registered for another component")
        return False
    
    # Validate path format (should contain at least one dot)
    if '.' not in path:
        logger.error(f"Invalid import path format: {path}")
        return False
    
    # Register the component
    HELIX_MAPPINGS[name] = path
    _component_dependencies[name] = set(dependencies or [])
    if version_requirements:
        _version_requirements[name] = version_requirements
    
    logger.info(f"Registered genome component: {name} -> {path}")
    return True

async def helix_import(component_name: str, force_reload: bool = False, force_initialize: bool = False) -> Any:
    """
    Special import function for DAWN components
    Handles missing modules gracefully with stubs
    """
    # Special diagnostic logging for genome/sequence components
    if 'genome' in component_name.lower() or 'sequence' in component_name.lower():
        logger.info(f"Loading genetic component: {component_name}")
        logger.debug(f"Component path: {HELIX_MAPPINGS.get(component_name, 'direct import')}")

    if not validate_component_name(component_name):
        raise ValueError(f"Invalid component name: {component_name}")

    # Check cache first unless force_reload is True
    if not force_reload and component_name in _component_cache:
        return _component_cache[component_name]

    # Check for circular dependencies
    if component_name in _circular_deps:
        raise ImportError(f"Circular dependency detected for component: {component_name}")

    _circular_deps.add(component_name)
    
    try:
        if component_name in HELIX_MAPPINGS:
            full_path = HELIX_MAPPINGS[component_name]
            module_path, class_name = full_path.rsplit('.', 1)
            
            try:
                # Try standard import first
                module = importlib.import_module(module_path)
                component = getattr(module, class_name)
                
                # Check version if available
                version = get_component_version(component)
                if version != 'unknown':
                    logger.info(f"Loaded {component_name} version {version}")
                    if not check_version_compatibility(component_name, version):
                        logger.warning(f"Version {version} of {component_name} may not be compatible")
                
                # Cache the component
                _component_cache[component_name] = component
                _import_history[component_name] = datetime.now()
                _stub_components.discard(component_name)
                
                # Initialize component info
                _component_info[component_name] = ComponentInfo(
                    name=component_name,
                    version=version,
                    status=ComponentStatus.ACTIVE,
                    dependencies=_component_dependencies.get(component_name, []),
                    last_health_check=datetime.now(),
                    health_status=True
                )
                
                # Check mood state before initialization
                entropy, fragility = await check_mood_state()
                if not should_defer_initialization(entropy, fragility, force_initialize):
                    # Initialize component if it supports lifecycle
                    if isinstance(component, ComponentLifecycle):
                        await component.initialize()
                else:
                    logger.info(f"Deferred initialization of {component_name} due to high entropy/fragility")
                    _component_info[component_name].status = ComponentStatus.INITIALIZING
                
                # Update pulse state
                update_pulse_state()
                
                return component
            except (ImportError, AttributeError) as e:
                logger.error(f"Failed to import {component_name}: {e}")
                # Return a stub class if import fails
                stub = create_stub_class(class_name, module_path)
                _stub_components.add(component_name)
                
                # Update pulse state
                update_pulse_state()
                
                return stub
        
        # Try direct import for unknown components
        try:
            if '.' in component_name:
                module_path, class_name = component_name.rsplit('.', 1)
                module = importlib.import_module(module_path)
                component = getattr(module, class_name)
                _component_cache[component_name] = component
                _import_history[component_name] = datetime.now()
                
                # Update pulse state
                update_pulse_state()
                
                return component
            else:
                component = importlib.import_module(component_name)
                _component_cache[component_name] = component
                _import_history[component_name] = datetime.now()
                
                # Update pulse state
                update_pulse_state()
                
                return component
        except Exception as e:
            logger.error(f"Failed to import {component_name}: {e}")
            stub = create_stub_class(component_name, 'unknown')
            _stub_components.add(component_name)
            
            # Update pulse state
            update_pulse_state()
            
            return stub
    finally:
        _circular_deps.discard(component_name)

def create_stub_class(class_name: str, module_path: str) -> type:
    """Create a stub class for missing components"""
    
    class StubComponent:
        _stub = True
        
        def __init__(self, **kwargs):
            self._name = class_name
            self._module = module_path
            self._initialized = True
            self._active = False
            self._last_attempt = datetime.now()
            self._error_message = None
            
        async def initialize(self, *args, **kwargs):
            self._active = True
            logger.info(f"Stub component initialized: {self._name}")
            
        async def shutdown(self):
            self._active = False
            logger.info(f"Stub component shut down: {self._name}")
            
        async def health_check(self) -> bool:
            return self._active
            
        def get_status(self):
            return {
                'stub': True,
                'name': self._name,
                'active': self._active,
                'last_attempt': self._last_attempt.isoformat(),
                'module_path': self._module,
                'error': self._error_message
            }
            
        def is_active(self):
            return self._active
            
        async def tick(self, *args, **kwargs):
            pass
            
        def __repr__(self):
            return f"<Stub:{self._name}>"
    
    # Add genome-specific method if component is genome-related
    if 'genome' in class_name.lower() or 'sequencer' in class_name.lower():
        def get_genome_status(self) -> str:
            return 'no sequence loaded'
        
        setattr(StubComponent, 'get_genome_status', get_genome_status)
    
    # Give it the proper name
    StubComponent.__name__ = class_name
    StubComponent.__qualname__ = class_name
    
    return StubComponent

async def cleanup_unused_stubs(max_age_hours: int = 24):
    """Remove unused stub components older than max_age_hours"""
    now = datetime.now()
    to_remove = set()
    
    for component_name in _stub_components:
        if component_name in _import_history:
            age = now - _import_history[component_name]
            if age.total_seconds() > (max_age_hours * 3600):
                to_remove.add(component_name)
    
    for component_name in to_remove:
        if component_name in _component_cache:
            component = _component_cache[component_name]
            if hasattr(component, 'shutdown'):
                await component.shutdown()
        clear_component_cache(component_name)
        logger.info(f"Cleaned up unused stub: {component_name}")
    
    # Update pulse state after cleanup
    update_pulse_state()

async def monitor_component_health():
    """Monitor health of all active components"""
    while True:
        for component_name, component in _component_cache.items():
            if not is_stub_component(component):
                health_status = await check_component_health(component_name)
                if component_name in _component_info:
                    _component_info[component_name].health_status = health_status
                    _component_info[component_name].last_health_check = datetime.now()
                    if not health_status:
                        logger.warning(f"Component health check failed: {component_name}")
        
        # Update pulse state after health check
        update_pulse_state()
        await asyncio.sleep(60)  # Check every minute