"""
Simplified helix import system that actually works
Replaces the over-engineered original
"""
import importlib
import logging
from typing import Any, Optional, Dict, Callable
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

class HelixImportSystem:
    """Simplified helix import with better error handling"""
    
    def __init__(self):
        self.module_registry: Dict[str, str] = {}
        self.fallback_registry: Dict[str, Callable] = {}
        self.failed_imports: set = set()
        self._setup_module_registry()
    
    def _setup_module_registry(self):
        """Setup known module mappings"""
        self.module_registry = {
            # Core modules
            "pulse_heat": "substrate.pulse_heat",
            "echo_module": "substrate.echo_module",
            "resonance": "substrate.resonance",
            "quantum_foam": "substrate.quantum_foam",
            
            # Visual modules
            "visual_cortex": "visual.visual_cortex",
            "pattern_recognition": "visual.pattern_recognition",
            
            # Core systems
            "consciousness_engine": "core.consciousness_engine",
            "tick_engine": "core.tick_engine",
            
            # Add more mappings as needed
        }
    
    def register_module(self, alias: str, full_path: str):
        """Register a module mapping"""
        self.module_registry[alias] = full_path
        logger.info(f"Registered module: {alias} -> {full_path}")
    
    def register_fallback(self, module_name: str, fallback_func: Callable):
        """Register a fallback function for a module"""
        self.fallback_registry[module_name] = fallback_func
        logger.info(f"Registered fallback for: {module_name}")
    
    def helix_import(self, module_name: str, force_reload: bool = False) -> Any:
        """
        Import a module through the helix system
        
        Args:
            module_name: Module to import (alias or full name)
            force_reload: Force reload the module
            
        Returns:
            Imported module or fallback
        """
        # Check if we've already failed to import this
        if module_name in self.failed_imports and not force_reload:
            return self._get_fallback(module_name)
        
        # Get the full module path
        full_path = self.module_registry.get(module_name, module_name)
        
        try:
            # Try to import the module
            if force_reload and full_path in sys.modules:
                del sys.modules[full_path]
                
            module = importlib.import_module(full_path)
            logger.debug(f"Successfully imported: {module_name} ({full_path})")
            
            # Remove from failed imports if it was there
            self.failed_imports.discard(module_name)
            
            return module
            
        except ImportError as e:
            logger.error(f"Failed to import {module_name} ({full_path}): {e}")
            self.failed_imports.add(module_name)
            return self._get_fallback(module_name)
        except Exception as e:
            logger.error(f"Unexpected error importing {module_name}: {e}")
            self.failed_imports.add(module_name)
            return self._get_fallback(module_name)
    
    def _get_fallback(self, module_name: str) -> Any:
        """Get fallback for a module"""
        if module_name in self.fallback_registry:
            logger.info(f"Using registered fallback for {module_name}")
            return self.fallback_registry[module_name]()
        
        # Return a mock module
        logger.warning(f"Creating mock module for {module_name}")
        return self._create_mock_module(module_name)
    
    def _create_mock_module(self, module_name: str) -> Any:
        """Create a mock module with basic functionality"""
        class MockModule:
            def __init__(self, name):
                self.__name__ = name
                self.__file__ = f"<mock {name}>"
                
            def __getattr__(self, name):
                logger.warning(f"Accessing mock attribute: {self.__name__}.{name}")
                return lambda *args, **kwargs: None
                
        return MockModule(module_name)
    
    def get_failed_imports(self) -> list:
        """Get list of failed imports"""
        return list(self.failed_imports)
    
    def clear_cache(self):
        """Clear the failed imports cache"""
        self.failed_imports.clear()
        logger.info("Cleared helix import cache")

# Global helix system instance
helix_system = HelixImportSystem()

# Convenience function to match existing code
def helix_import(module_name: str, force_reload: bool = False) -> Any:
    """Global helix import function"""
    return helix_system.helix_import(module_name, force_reload)

# Register fallbacks for critical modules
def register_default_fallbacks():
    """Register default fallbacks for critical modules"""
    
    def pulse_heat_fallback():
        """Fallback for pulse_heat module"""
        class PulseHeatMock:
            def pulse(self, *args, **kwargs):
                logger.warning("Using pulse_heat mock")
                return {"status": "mock", "value": 0}
        return PulseHeatMock()
    
    helix_system.register_fallback("pulse_heat", pulse_heat_fallback)
    
    # Add more fallbacks as needed

# Initialize on import
register_default_fallbacks() 