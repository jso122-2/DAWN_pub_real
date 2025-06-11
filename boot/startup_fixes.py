"""
Startup Fixes Module - Applies critical fixes during system initialization
"""

import sys
import os
import asyncio
import builtins
from typing import Optional, Any

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Add substrate directory to path
substrate_path = os.path.join(project_root, 'substrate')
if substrate_path not in sys.path:
    sys.path.append(substrate_path)

try:
    from helix.helix_import_architecture import helix_import
except ImportError:
    print("No existing HelixBridge found, using custom implementation")
    async def helix_import(module_name: str) -> Any:
        """Fallback implementation of helix_import"""
        try:
            return __import__(module_name)
        except ImportError as e:
            print(f"  ⚠️ Could not import {module_name}: {e}")
            return None

async def apply_quick_healing() -> None:
    """Apply quick healing patches to critical components"""
    print("🚑 Applying quick healing patches...")
    
    try:
        # Patch alignment
        semantic_field = await helix_import('core.semantic_field')
        if semantic_field:
            builtins.get_current_alignment = semantic_field.get_current_alignment
    except Exception as e:
        print(f"  ⚠️ Could not patch alignment: {e}")
        
    print("✅ Quick healing complete!")

async def apply_complete_dawn_fixes() -> None:
    """Apply complete set of DAWN fixes"""
    print("🔧 Applying complete DAWN fixes...")
    
    try:
        # Patch global get_current_alignment
        semantic_field = await helix_import('core.semantic_field')
        if semantic_field:
            builtins.get_current_alignment = semantic_field.get_current_alignment
    except Exception as e:
        print(f"  ⚠️ Could not patch global get_current_alignment: {e}")
        
    try:
        # Add suppression override with a real config
        schema_engine = await helix_import('schema.schema_evolution_engine')
        if schema_engine:
            override_config = {
                "id": "startup",
                "reason": "boot_patch",
                "active": True,
                "timestamp": __import__('datetime').datetime.now().isoformat()
            }
            schema_engine.add_suppression_override(override_config)
    except Exception as e:
        print(f"  ⚠️ Could not add suppression_override: {e}")
        
    try:
        # Patch tick engine with a real handler
        tick_engine = await helix_import('core.unified_tick_engine')
        if tick_engine:
            def startup_tick_handler(data):
                # Example: log tick event or perform startup check
                print(f"[StartupFix] Tick event: {data}")
            tick_engine.patch_tick_engine(startup_tick_handler)
    except Exception as e:
        print(f"  ⚠️ Could not patch tick engine: {e}")
        
    print("✅ Complete DAWN fixes applied!")

def run_fixes():
    """Run all fixes using asyncio"""
    asyncio.run(apply_quick_healing())
    asyncio.run(apply_complete_dawn_fixes())

if __name__ == "__main__":
    run_fixes() 