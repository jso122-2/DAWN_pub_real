#!/usr/bin/env python3
"""
DAWN Forecast GUI Integration Test
Tests the integrated forecast GUI with DAWN's consciousness system.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_gui_imports():
    """Test that all GUI imports work correctly."""
    print("🧪 Testing GUI imports...")
    
    try:
        import tkinter as tk
        print("✅ Tkinter import successful")
    except ImportError:
        print("❌ Tkinter not available")
        return False
    
    try:
        from gui.dawn_forecast_visualizer import DAWNForecastGUI, TARGET_PROFILES, MOOD_STATES
        print("✅ GUI components import successful")
    except ImportError as e:
        print(f"❌ GUI components import failed: {e}")
        return False
    
    try:
        from cognitive.forecasting_models import Passion, Acquaintance, ForecastVector
        from cognitive.forecasting_engine import get_forecasting_engine
        from core.consciousness_core import DAWNConsciousness
        print("✅ DAWN forecasting imports successful")
    except ImportError as e:
        print(f"❌ DAWN forecasting imports failed: {e}")
        return False
    
    return True


def test_gui_initialization():
    """Test GUI initialization without actually showing the window."""
    print("\n🧪 Testing GUI initialization...")
    
    try:
        import tkinter as tk
        from gui.dawn_forecast_visualizer import DAWNForecastGUI
        
        # Create root window but don't show it
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Initialize GUI
        gui = DAWNForecastGUI(root)
        
        # Test basic attributes
        assert hasattr(gui, 'forecasting_engine'), "GUI should have forecasting engine"
        assert hasattr(gui, 'connected_to_dawn'), "GUI should have DAWN connection status"
        assert hasattr(gui, 'current_target'), "GUI should have current target"
        assert hasattr(gui, 'current_mood'), "GUI should have current mood"
        
        print(f"✅ GUI initialized successfully")
        print(f"   Connected to DAWN: {gui.connected_to_dawn}")
        print(f"   Current target: {gui.current_target}")
        print(f"   Current mood: {gui.current_mood}")
        
        # Test target profiles
        from gui.dawn_forecast_visualizer import TARGET_PROFILES, MOOD_STATES
        assert len(TARGET_PROFILES) > 0, "Should have target profiles"
        print(f"   Available targets: {list(TARGET_PROFILES.keys())}")
        
        # Test mood states
        assert len(MOOD_STATES) > 0, "Should have mood states"
        print(f"   Available moods: {list(MOOD_STATES.keys())}")
        
        # Clean up
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ GUI initialization failed: {e}")
        return False


def test_forecast_generation():
    """Test forecast generation through GUI methods."""
    print("\n🧪 Testing forecast generation...")
    
    try:
        import tkinter as tk
        from gui.dawn_forecast_visualizer import DAWNForecastGUI
        
        # Create hidden root window
        root = tk.Tk()
        root.withdraw()
        
        # Initialize GUI
        gui = DAWNForecastGUI(root)
        
        # Test creating target objects
        passion, acquaintance = gui.create_target_objects("dawn.core")
        
        assert passion is not None, "Should create passion object"
        assert acquaintance is not None, "Should create acquaintance object"
        assert passion.direction == "consciousness_expansion", "Should have correct passion direction"
        
        print(f"✅ Target objects created: {passion}")
        print(f"   Acquaintance events: {len(acquaintance.event_log)}")
        
        # Test mood parameters
        mood_params = gui.get_mood_params()
        assert 'mood_factor' in mood_params, "Should have mood factor"
        assert 'entropy_weight' in mood_params, "Should have entropy weight"
        
        print(f"✅ Mood parameters: {mood_params}")
        
        # Test forecast generation
        if gui.forecasting_engine:
            forecast = gui.forecasting_engine.generate_forecast(passion, acquaintance, **mood_params)
            
            assert forecast is not None, "Should generate forecast"
            assert hasattr(forecast, 'confidence'), "Forecast should have confidence"
            assert hasattr(forecast, 'predicted_behavior'), "Forecast should have predicted behavior"
            
            print(f"✅ Forecast generated: {forecast.predicted_behavior}")
            print(f"   Confidence: {forecast.confidence:.3f}")
            print(f"   Risk level: {forecast.risk_level()}")
        else:
            print("⚠️ No forecasting engine available")
        
        # Clean up
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ Forecast generation test failed: {e}")
        return False


def test_dawn_integration():
    """Test DAWN system integration."""
    print("\n🧪 Testing DAWN system integration...")
    
    try:
        import tkinter as tk
        from gui.dawn_forecast_visualizer import DAWNForecastGUI
        
        # Create hidden root window
        root = tk.Tk()
        root.withdraw()
        
        # Initialize GUI
        gui = DAWNForecastGUI(root)
        
        if gui.connected_to_dawn:
            print("✅ Connected to DAWN system")
            
            # Test DAWN consciousness access
            if gui.dawn_consciousness:
                print("✅ DAWN consciousness available")
                
                # Test getting current forecasts (if available)
                if hasattr(gui.dawn_consciousness, 'get_current_forecasts'):
                    try:
                        forecasts = gui.dawn_consciousness.get_current_forecasts()
                        print(f"✅ Current DAWN forecasts retrieved: {len(forecasts.get('recent_forecasts', []))} forecasts")
                    except Exception as e:
                        print(f"⚠️ Could not retrieve DAWN forecasts: {e}")
                
                # Test instant forecast generation (if available)
                if hasattr(gui.dawn_consciousness, 'generate_instant_forecast'):
                    try:
                        # Note: This would normally be async, but we'll test the method exists
                        print("✅ DAWN instant forecast method available")
                    except Exception as e:
                        print(f"⚠️ DAWN instant forecast issue: {e}")
            
        else:
            print("⚠️ Not connected to DAWN system - running in standalone mode")
        
        # Clean up
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ DAWN integration test failed: {e}")
        return False


def main():
    """Run all GUI integration tests."""
    print("🔮 DAWN Forecast GUI Integration Tests")
    print("=" * 60)
    
    tests = [
        test_gui_imports,
        test_gui_initialization,
        test_forecast_generation,
        test_dawn_integration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All GUI integration tests passed!")
        print("🔮 DAWN Forecast Visualizer is ready to launch!")
    else:
        print("⚠️ Some tests failed - check the output above")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 