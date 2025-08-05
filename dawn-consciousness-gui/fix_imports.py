#!/usr/bin/env python3
"""
Fix DAWN Import Paths
=====================

This script tests different import strategies to fix the
"attempted relative import beyond top-level package" error.
"""

import sys
import os
from pathlib import Path

def test_import_paths():
    """Test different import path strategies"""
    print("🔧 Testing DAWN import paths...")
    
    # Get current and parent directories
    current_dir = Path(__file__).parent.resolve()
    parent_dir = current_dir.parent.resolve()
    
    print(f"📍 Current directory: {current_dir}")
    print(f"📍 Parent directory: {parent_dir}")
    print(f"📍 Current working directory: {Path.cwd()}")
    
    # Add paths to sys.path
    paths_to_add = [
        str(parent_dir),
        str(current_dir),
        str(parent_dir / "core"),
        str(parent_dir / "pulse"),
        str(parent_dir / "bloom"),
        str(parent_dir / "tracers"),
    ]
    
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
            print(f"➕ Added to Python path: {path}")
    
    print(f"\n🐍 Python path (first 10 entries):")
    for i, path in enumerate(sys.path[:10]):
        print(f"  {i}: {path}")
    
    # Test imports
    import_tests = [
        ("core.consciousness_core", "DAWNConsciousness"),
        ("core.cognitive_formulas", "DAWNFormulaEngine"),
        ("pulse.pulse_layer", "PulseLayer"),
        ("bloom.unified_bloom_engine", "BloomEngine"),
    ]
    
    successful_imports = []
    failed_imports = []
    
    for module_name, class_name in import_tests:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✅ Successfully imported {module_name}.{class_name}")
            successful_imports.append((module_name, class_name, cls))
        except Exception as e:
            print(f"❌ Failed to import {module_name}.{class_name}: {e}")
            failed_imports.append((module_name, class_name, e))
    
    print(f"\n📊 Import Results:")
    print(f"✅ Successful: {len(successful_imports)}")
    print(f"❌ Failed: {len(failed_imports)}")
    
    # Test basic functionality if imports worked
    if successful_imports:
        print(f"\n🧪 Testing basic functionality...")
        for module_name, class_name, cls in successful_imports:
            try:
                if class_name == "DAWNFormulaEngine":
                    engine = cls()
                    print(f"✅ Created {class_name} instance")
                elif class_name == "PulseLayer":
                    layer = cls()
                    print(f"✅ Created {class_name} instance")
                elif class_name == "BloomEngine":
                    engine = cls()
                    print(f"✅ Created {class_name} instance")
            except Exception as e:
                print(f"⚠️ Failed to create {class_name} instance: {e}")
    
    return successful_imports, failed_imports

def find_dawn_modules():
    """Find DAWN modules in the filesystem"""
    print(f"\n🔍 Searching for DAWN modules...")
    
    search_dirs = [
        Path.cwd().parent,  # Parent directory
        Path.cwd(),         # Current directory
    ]
    
    modules_found = {}
    
    for search_dir in search_dirs:
        for module_dir in ["core", "pulse", "bloom", "tracers"]:
            module_path = search_dir / module_dir
            if module_path.exists():
                print(f"📁 Found {module_dir} at: {module_path}")
                modules_found[module_dir] = module_path
                
                # List Python files in the module
                py_files = list(module_path.glob("*.py"))
                if py_files:
                    print(f"   🐍 Python files: {[f.name for f in py_files[:5]]}")
    
    return modules_found

if __name__ == "__main__":
    print("🧠 DAWN Import Path Fixer")
    print("=" * 40)
    
    # Search for modules
    modules_found = find_dawn_modules()
    
    # Test imports
    successful_imports, failed_imports = test_import_paths()
    
    # Generate import strategy
    print(f"\n🎯 Recommended Import Strategy:")
    
    if successful_imports:
        print("✅ Current import paths work! Use this configuration:")
        current_dir = Path(__file__).parent.resolve()
        parent_dir = current_dir.parent.resolve()
        
        print(f"""
import sys
from pathlib import Path

# Add DAWN paths
project_root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(project_root))

# Import real DAWN components
try:
    {chr(10).join([f"    from {module}.{cls} import {cls}" for module, cls, _ in successful_imports])}
    REAL_DAWN_AVAILABLE = True
except ImportError as e:
    REAL_DAWN_AVAILABLE = False
""")
    else:
        print("❌ No imports successful. Need to check DAWN component locations.")
        if modules_found:
            print("💡 Suggestion: Copy missing components or fix import paths.")
        else:
            print("💡 Suggestion: DAWN core components not found in expected locations.") 