#!/usr/bin/env python3
"""
Test script for DAWN Unified Launcher GUI
Verifies the GUI can be created and all components are accessible.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def test_unified_gui_import():
    """Test that the unified GUI can be imported."""
    try:
        from dawn_core.unified_launcher_gui import DAWNUnifiedLauncherGUI
        print("✅ Unified GUI class imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_gui_creation():
    """Test that the GUI can be created (without showing it)."""
    try:
        import tkinter as tk
        from dawn_core.unified_launcher_gui import DAWNUnifiedLauncherGUI
        
        # Create GUI instance (but don't run mainloop)
        launcher = DAWNUnifiedLauncherGUI()
        
        # Test that key components exist
        assert hasattr(launcher, 'root')
        assert hasattr(launcher, 'output_text')
        assert hasattr(launcher, 'running_processes')
        assert hasattr(launcher, 'launch_script')
        
        # Destroy the GUI
        launcher.root.destroy()
        
        print("✅ Unified GUI creation successful")
        return True
        
    except ImportError:
        print("⚠️ GUI test skipped - tkinter not available")
        return False
    except Exception as e:
        print(f"❌ GUI creation error: {e}")
        return False

def test_launcher_paths():
    """Test that launcher script paths exist."""
    launcher_scripts = [
        "dawn_core/launch.py",
        "launcher_scripts/launch_dawn_unified.py",
        "launcher_scripts/launch_enhanced_dawn_gui.py",
        "launcher_scripts/launch_forecast_gui.py"
    ]
    
    existing_count = 0
    for script in launcher_scripts:
        script_path = project_root / script
        if script_path.exists():
            existing_count += 1
            print(f"✅ Found: {script}")
        else:
            print(f"⚠️ Missing: {script}")
    
    print(f"📊 Found {existing_count}/{len(launcher_scripts)} launcher scripts")
    return existing_count > 0

def main():
    """Run all tests."""
    print("🧪 Testing DAWN Unified Launcher GUI")
    print("=" * 40)
    
    # Test imports
    import_ok = test_unified_gui_import()
    print()
    
    # Test GUI creation
    if import_ok:
        gui_ok = test_gui_creation()
        print()
    else:
        gui_ok = False
    
    # Test launcher paths
    paths_ok = test_launcher_paths()
    print()
    
    # Summary
    if import_ok and gui_ok and paths_ok:
        print("🎯 All tests passed! Unified GUI is ready.")
        print("\nTo launch:")
        print("  python dawn_core/launch.py unified")
        print("  python launch_dawn_unified_gui.py")
    else:
        print("⚠️ Some tests failed - check the output above")

if __name__ == "__main__":
    main() 