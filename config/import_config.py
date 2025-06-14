"""
Central import configuration for DAWN
Replaces the problematic helix import system with a simpler approach
"""
import sys
import os
from pathlib import Path
from typing import List, Optional, Any
import importlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImportManager:
    """Centralized import management for DAWN"""
    
    def __init__(self):
        self.project_root = self._find_project_root()
        self.required_paths = self._get_required_paths()
        self._setup_paths()
        self._module_cache = {}
        
    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path(__file__).parent
        
        # Look for key indicator files
        indicators = ['main.py', 'start_api_fixed.py', '.git']
        
        while current != current.parent:
            for indicator in indicators:
                if (current / indicator).exists():
                    logger.info(f"Found project root: {current}")
                    return current
            current = current.parent
            
        # Fallback
        fallback = Path(__file__).parent.parent
        logger.warning(f"Using fallback project root: {fallback}")
        return fallback
    
    def _get_required_paths(self) -> List[Path]:
        """Get all required Python paths"""
        return [
            self.project_root,
            self.project_root / "substrate",
            self.project_root / "core",
            self.project_root / "visual",
            self.project_root / "config",
            self.project_root / "utils",
            self.project_root / "substrate" / "helix",
            self.project_root / "Ticket_engine",
            self.project_root / "api"
        ]
    
    def _setup_paths(self):
        """Add all required paths to sys.path"""
        for path in self.required_paths:
            str_path = str(path.absolute())
            if str_path not in sys.path and path.exists():
                sys.path.insert(0, str_path)
                logger.debug(f"Added to sys.path: {str_path}")
            elif not path.exists():
                logger.warning(f"Path does not exist: {str_path}")
    
    def safe_import(self, module_name: str, fallback: Any = None) -> Any:
        """
        Safely import a module with fallback support
        
        Args:
            module_name: Name of the module to import
            fallback: Fallback value if import fails
            
        Returns:
            Imported module or fallback value
        """
        # Check cache first
        if module_name in self._module_cache:
            return self._module_cache[module_name]
        
        try:
            # Try standard import
            module = importlib.import_module(module_name)
            self._module_cache[module_name] = module
            logger.debug(f"Successfully imported: {module_name}")
            return module
        except ImportError as e:
            logger.warning(f"Failed to import {module_name}: {e}")
            
            # Try alternative import patterns
            alternatives = [
                module_name.replace('_', '.'),
                f"substrate.{module_name}",
                f"core.{module_name}",
                f"visual.{module_name}"
            ]
            
            for alt in alternatives:
                try:
                    module = importlib.import_module(alt)
                    self._module_cache[module_name] = module
                    logger.info(f"Imported {module_name} as {alt}")
                    return module
                except ImportError:
                    continue
            
            # Return fallback
            logger.error(f"All import attempts failed for {module_name}, using fallback")
            return fallback
    
    def get_module_attr(self, module_name: str, attr_name: str, fallback: Any = None) -> Any:
        """Get an attribute from a module safely"""
        module = self.safe_import(module_name)
        if module and hasattr(module, attr_name):
            return getattr(module, attr_name)
        return fallback

# Global import manager instance
import_manager = ImportManager()

# Convenience functions
def safe_import(module_name: str, fallback: Any = None) -> Any:
    """Global safe import function"""
    return import_manager.safe_import(module_name, fallback)

def setup_imports():
    """Setup function to be called at startup"""
    import_manager._setup_paths()
    logger.info("Import paths configured successfully") 