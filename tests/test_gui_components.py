#!/usr/bin/env python3
"""
Test script to check GUI component availability
"""

import sys
import traceback

# Add the project root to Python path
sys.path.insert(0, '..')

def test_gui_component_availability():
    """Test what components are available in the GUI"""
    
    print("🔍 GUI Component Availability Test")
    print("=" * 50)
    
    try:
        # Import individual reflex components first
        print("🤖 Testing individual reflex component imports...")
        
        try:
            from reflex.reflex_executor import ReflexExecutor
            print("✅ ReflexExecutor import: SUCCESS")
        except Exception as e:
            print(f"❌ ReflexExecutor import: FAILED - {e}")
        
        try:
            from reflex.symbolic_notation import SymbolicNotation
            print("✅ SymbolicNotation import: SUCCESS")
        except Exception as e:
            print(f"❌ SymbolicNotation import: FAILED - {e}")
        
        try:
            from reflex.fractal_colorizer import FractalColorizer
            print("✅ FractalColorizer import: SUCCESS")
        except Exception as e:
            print(f"❌ FractalColorizer import: FAILED - {e}")

        try:
            from reflex.owl_panel import OwlPanel
            print("✅ OwlPanel import: SUCCESS")
        except Exception as e:
            print(f"❌ OwlPanel import: FAILED - {e}")

        # Now test GUI integration components
        print("\n🖼️ Testing GUI integration components...")
        
        try:
            from gui.dawn_gui_enhanced import EnhancedDawnGUI
            print("✅ EnhancedDawnGUI import: SUCCESS")
        except Exception as e:
            print(f"❌ EnhancedDawnGUI import: FAILED - {e}")
        
        try:
            from gui.dawn_gui_integration import DawnGUIIntegration
            print("✅ DawnGUIIntegration import: SUCCESS")
        except Exception as e:
            print(f"❌ DawnGUIIntegration import: FAILED - {e}")
        
        # Test core components that GUI depends on
        print("\n🧠 Testing core system components...")
        
        try:
            from core.pulse_controller import PulseController
            print("✅ PulseController import: SUCCESS")
        except Exception as e:
            print(f"❌ PulseController import: FAILED - {e}")
        
        try:
            from core.dawn_entropy_analyzer import EnhancedEntropyAnalyzer
            print("✅ EnhancedEntropyAnalyzer import: SUCCESS")
        except Exception as e:
            print(f"❌ EnhancedEntropyAnalyzer import: FAILED - {e}")
        
        print("\n📋 Component availability test completed!")
        
    except Exception as e:
        print(f"❌ Critical error during GUI component test: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    test_gui_component_availability() 