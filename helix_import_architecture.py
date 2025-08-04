#!/usr/bin/env python3
"""
Helix Import Architecture - Root Level Proxy
============================================

This file provides access to DAWN's helix import system from the root level.
It proxies to the actual implementation in substrate/helix/helix_import_architecture.py
"""

import sys
import os
from pathlib import Path

# Ensure substrate can be imported
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    # Import the actual helix import system
    from substrate.helix.helix_import_architecture import (
        helix_import,
        HelixImportSystem,
        ComponentCache,
        HELIX_MAPPINGS
    )
    
    # Make these available at root level
    __all__ = ['helix_import', 'HelixImportSystem', 'ComponentCache', 'HELIX_MAPPINGS']
    
    print("✅ Helix import architecture loaded successfully")
    
except ImportError as e:
    print(f"⚠️ Helix import system not fully available: {e}")
    
    # Create a minimal fallback helix_import function
    def helix_import(module_name: str, force_reload: bool = False):
        """Fallback helix_import function"""
        print(f"⚠️ Helix fallback: attempting to import {module_name}")
        try:
            return __import__(module_name, fromlist=[''])
        except ImportError:
            print(f"⚠️ Helix fallback failed for {module_name}")
            return None
    
    class HelixImportSystem:
        """Fallback helix import system"""
        def __init__(self):
            pass
        
        def helix_import(self, module_name: str, force_reload: bool = False):
            return helix_import(module_name, force_reload)
    
    ComponentCache = {}
    HELIX_MAPPINGS = {}
    
    __all__ = ['helix_import', 'HelixImportSystem', 'ComponentCache', 'HELIX_MAPPINGS']

# Create default helix system instance
helix_system = HelixImportSystem() 