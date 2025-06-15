"""
DAWN Unified Orchestrator
Combines module management with distributed consciousness orchestration
"""

import os
import sys
import asyncio
import time
import json
import logging
from typing import Dict, Any, Optional, List, Set
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from collections import defaultdict, deque

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
sys.path.append(str(PROJECT_ROOT))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global orchestrator instance
_orchestrator_instance = None

@dataclass
class OrchestratorState:
    """Current state of the orchestrator"""
    is_active: bool = False
    last_update: datetime = field(default_factory=datetime.now)
    components: Dict[str, bool] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)
    error_count: int = 0
    recovery_count: int = 0
    mode: str = 'harmonized'
    emergence_level: float = 0.0
    coherence_score: float = 0.0

class UnifiedOrchestrator:
    """Unified orchestrator combining module management and consciousness orchestration"""
    
    def __init__(self):
        self.state = OrchestratorState()
        self.initialized = False
        self.components: Dict[str, Any] = {}
        self._module_handles: Dict[str, Any] = {}
        
        # Consciousness orchestration attributes
        self.collective_memory: Dict[str, Any] = {}
        self.shared_insights: deque = deque(maxlen=100)
        self.thought_cascades: List[Dict] = []
        self.emergent_behaviors: List[Dict] = []
        
        # Orchestration modes
        self.orchestration_modes = {
            'harmonized': self._mode_harmonized,
            'competitive': self._mode_competitive,
            'exploratory': self._mode_exploratory,
            'convergent': self._mode_convergent,
            'divergent': self._mode_divergent
        }
        
        logger.info("Initializing Unified Orchestrator")
    
    async def initialize(self) -> None:
        """Initialize the orchestrator and its components"""
        if self.initialized:
            return
            
        try:
            # Initialize core modules
            await self._initialize_core_modules()
            
            # Initialize consciousness components
            await self._initialize_consciousness()
            
            self.state.is_active = True
            self.initialized = True
            logger.info("Unified Orchestrator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Unified Orchestrator: {e}")
            raise
    
    async def _initialize_core_modules(self) -> None:
        """Initialize core system modules"""
        core_modules = ['pulse', 'schema', 'memory', 'cognitive', 'visual']
        
        for module_name in core_modules:
            try:
                module_handle = await self._initialize_module(module_name)
                if module_handle:
                    self.components[module_name] = module_handle
                    self.state.components[module_name] = True
                    logger.info(f"Initialized module: {module_name}")
            except Exception as e:
                logger.error(f"Failed to initialize module {module_name}: {e}")
    
    async def _initialize_consciousness(self) -> None:
        """Initialize consciousness system components"""
        try:
            # Initialize consciousness core
            from core.consciousness_core import ConsciousnessCore
            consciousness = ConsciousnessCore()
            await consciousness.initialize()
            self.components['consciousness'] = consciousness
            
            # Initialize other consciousness components
            # Add more initialization as needed
            
            logger.info("Consciousness system initialized")
        except Exception as e:
            logger.error(f"Failed to initialize consciousness system: {e}")
            raise
    
    async def _initialize_module(self, module_name: str) -> Optional[Any]:
        """Initialize a specific module"""
        if module_name in self._module_handles:
            return self._module_handles[module_name]
            
        try:
            if module_name == "pulse":
                from pulse.pulse_loader import load_pulse_system
                pulse, tick_thermal_update, add_heat, scup_tracker = load_pulse_system()
                return {
                    "pulse": pulse,
                    "tick_thermal_update": tick_thermal_update,
                    "add_heat": add_heat,
                    "scup_tracker": scup_tracker
                }
                
            elif module_name == "schema":
                from schema.schema_manager import SchemaManager
                return SchemaManager()
                
            elif module_name == "memory":
                from memories.memory_manager import MemoryManager
                return MemoryManager()
                
            elif module_name == "cognitive":
                from cognitive.cognitive_engine import CognitiveEngine
                return CognitiveEngine()
                
            elif module_name == "visual":
                from visual.visual_processor import VisualProcessor
                return VisualProcessor()
                
            return None
            
        except Exception as e:
            logger.error(f"Failed to initialize {module_name}: {e}")
            return None
    
    async def shutdown(self) -> None:
        """Shutdown the orchestrator and all components"""
        if not self.initialized:
            return
            
        try:
            # Shutdown consciousness components
            if 'consciousness' in self.components:
                await self.components['consciousness'].shutdown()
            
            # Shutdown other components
            for component_name, component in self.components.items():
                try:
                    if hasattr(component, 'shutdown'):
                        await component.shutdown()
                except Exception as e:
                    logger.error(f"Error shutting down component {component_name}: {e}")
            
            self.state.is_active = False
            self.initialized = False
            logger.info("Unified Orchestrator shut down successfully")
        except Exception as e:
            logger.error(f"Error during Unified Orchestrator shutdown: {e}")
            raise
    
    def get_state(self) -> Dict[str, Any]:
        """Get current orchestrator state"""
        return {
            "is_active": self.state.is_active,
            "last_update": self.state.last_update.isoformat(),
            "components": self.state.components,
            "metrics": self.state.metrics,
            "error_count": self.state.error_count,
            "recovery_count": self.state.recovery_count,
            "mode": self.state.mode,
            "emergence_level": self.state.emergence_level,
            "coherence_score": self.state.coherence_score
        }
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process a message through the orchestrator"""
        if not self.initialized:
            raise RuntimeError("Orchestrator not initialized")
            
        try:
            # Update state
            self.state.last_update = datetime.now()
            
            # Process through consciousness system
            if 'consciousness' in self.components:
                response = await self.components['consciousness'].process_input(message)
            else:
                response = {
                    "status": "processed",
                    "timestamp": datetime.now().isoformat(),
                    "message": message
                }
            
            return response
        except Exception as e:
            self.state.error_count += 1
            logger.error(f"Error processing message: {e}")
            raise
    
    async def _mode_harmonized(self):
        """Harmonized orchestration mode"""
        logger.info("Engaging harmonized mode - synchronizing components")
        self.state.mode = 'harmonized'
        # Implement harmonized mode logic
    
    async def _mode_competitive(self):
        """Competitive orchestration mode"""
        logger.info("Engaging competitive mode - maximizing diversity")
        self.state.mode = 'competitive'
        # Implement competitive mode logic
    
    async def _mode_exploratory(self):
        """Exploratory orchestration mode"""
        logger.info("Engaging exploratory mode - balanced discovery")
        self.state.mode = 'exploratory'
        # Implement exploratory mode logic
    
    async def _mode_convergent(self):
        """Convergent orchestration mode"""
        logger.info("Engaging convergent mode - focusing attention")
        self.state.mode = 'convergent'
        # Implement convergent mode logic
    
    async def _mode_divergent(self):
        """Divergent orchestration mode"""
        logger.info("Engaging divergent mode - maximizing exploration")
        self.state.mode = 'divergent'
        # Implement divergent mode logic
    
    async def update_metrics(self) -> None:
        """Update system metrics"""
        if not self.initialized:
            return
            
        try:
            # Update metrics
            self.state.metrics.update({
                "timestamp": datetime.now().isoformat(),
                "active": self.state.is_active,
                "component_count": len(self.components),
                "errors": self.state.error_count,
                "mode": self.state.mode,
                "emergence_level": self.state.emergence_level,
                "coherence_score": self.state.coherence_score
            })
        except Exception as e:
            logger.error(f"Error updating metrics: {e}")
            raise

# For backward compatibility
Orchestrator = UnifiedOrchestrator

# Module management functions
async def initialize_module(module_name: str) -> Optional[Any]:
    """Initialize a module and return its handle"""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = UnifiedOrchestrator()
        await _orchestrator_instance.initialize()
    return await _orchestrator_instance._initialize_module(module_name)

def get_module(module_name: str) -> Optional[Any]:
    """Get a module handle by name"""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        return None
    return _orchestrator_instance.components.get(module_name)

async def shutdown_modules() -> None:
    """Shutdown all modules"""
    global _orchestrator_instance
    if _orchestrator_instance is not None:
        await _orchestrator_instance.shutdown()
        _orchestrator_instance = None

async def initialize_orchestrator() -> UnifiedOrchestrator:
    """Initialize the orchestrator and return the instance"""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = UnifiedOrchestrator()
        await _orchestrator_instance.initialize()
    return _orchestrator_instance

async def shutdown_orchestrator() -> None:
    """Shutdown the orchestrator"""
    global _orchestrator_instance
    if _orchestrator_instance is not None:
        await _orchestrator_instance.shutdown()
        _orchestrator_instance = None

def get_orchestrator() -> Optional[UnifiedOrchestrator]:
    """Get the current orchestrator instance"""
    return _orchestrator_instance

# Export both class names for backward compatibility
__all__ = ['UnifiedOrchestrator', 'Orchestrator', 'orchestrator', 
           'initialize_orchestrator', 'shutdown_orchestrator', 'get_orchestrator'] 