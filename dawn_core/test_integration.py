#!/usr/bin/env python3
"""
DAWN Core Integration Test
Verify all components work together correctly.
"""

import sys
import time
import threading
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def test_imports():
    """Test that all required modules can be imported."""
    print("🔧 Testing module imports...")
    
    try:
        from dawn_core.main import DAWNCognitiveEngine, create_dawn_engine
        print("✅ Main engine imports successful")
    except ImportError as e:
        print(f"⚠️ Main engine import warning: {e}")
    
    try:
        from dawn_core.snapshot_exporter import DAWNSnapshotExporter
        print("✅ Snapshot exporter imports successful")
    except ImportError as e:
        print(f"⚠️ Snapshot exporter import warning: {e}")
    
    try:
        from dawn_core.gui.forecast_dashboard import DAWNForecastDashboard
        print("✅ GUI dashboard imports successful")
    except ImportError as e:
        print(f"⚠️ GUI dashboard import warning: {e}")
    
    print("📋 Import tests complete\n")


def test_engine_creation():
    """Test creating a DAWN cognitive engine."""
    print("🧠 Testing engine creation...")
    
    try:
        from dawn_core.main import create_dawn_engine
        engine = create_dawn_engine()
        
        print(f"✅ Engine created successfully")
        print(f"   Tick count: {engine.tick_count}")
        print(f"   Entropy: {engine.current_entropy:.2f}")
        print(f"   Zone: {engine.current_zone}")
        
        return engine
        
    except Exception as e:
        print(f"❌ Engine creation failed: {e}")
        return None


def test_single_tick(engine):
    """Test running a single cognitive tick."""
    print("⚡ Testing single tick execution...")
    
    if not engine:
        print("❌ No engine available for tick test")
        return
    
    try:
        initial_tick = engine.tick_count
        initial_entropy = engine.current_entropy
        
        engine.tick()
        
        print(f"✅ Tick executed successfully")
        print(f"   Tick count: {initial_tick} → {engine.tick_count}")
        print(f"   Entropy: {initial_entropy:.2f} → {engine.current_entropy:.2f}")
        print(f"   Zone: {engine.current_zone}")
        
        if engine.forecast_cache:
            forecast = engine.forecast_cache
            print(f"   Forecast confidence: {forecast.get('confidence', 0):.2f}")
            print(f"   Risk level: {forecast.get('risk_level', 0):.2f}")
    
    except Exception as e:
        print(f"❌ Tick execution failed: {e}")


def test_multiple_ticks(engine, count=5):
    """Test running multiple ticks."""
    print(f"🔄 Testing {count} consecutive ticks...")
    
    if not engine:
        print("❌ No engine available for multi-tick test")
        return
    
    try:
        initial_tick = engine.tick_count
        
        for i in range(count):
            engine.tick()
            print(f"   Tick {i+1}/{count}: Zone={engine.current_zone}, Entropy={engine.current_entropy:.2f}")
            time.sleep(0.1)  # Brief pause
        
        print(f"✅ {count} ticks completed")
        print(f"   Total ticks: {initial_tick} → {engine.tick_count}")
        
    except Exception as e:
        print(f"❌ Multi-tick test failed: {e}")


def test_snapshot_creation(engine):
    """Test creating a system snapshot."""
    print("📦 Testing snapshot creation...")
    
    try:
        from dawn_core.snapshot_exporter import DAWNSnapshotExporter
        exporter = DAWNSnapshotExporter(dawn_engine=engine)
        
        # Test state export
        state = exporter.get_state()
        print(f"✅ State export successful")
        print(f"   Entropy: {state['system_metrics']['entropy']:.2f}")
        print(f"   Zone: {state['system_metrics']['zone']}")
        
        # Test forecast export
        forecast = exporter.get_forecast("next_24h")
        print(f"✅ Forecast export successful")
        print(f"   Confidence: {forecast['confidence']:.2f}")
        
        # Test symbolic trace
        symbolic_path = exporter.export_symbolic_trace()
        print(f"✅ Symbolic trace exported: {Path(symbolic_path).name}")
        
    except Exception as e:
        print(f"❌ Snapshot test failed: {e}")


def test_gui_creation():
    """Test creating the GUI dashboard (without showing it)."""
    print("🖥️ Testing GUI dashboard creation...")
    
    try:
        import tkinter as tk
        from dawn_core.gui.forecast_dashboard import DAWNForecastDashboard
        
        # Test that GUI can be created (but don't show it)
        dashboard = DAWNForecastDashboard()
        
        # Test that widgets exist
        assert hasattr(dashboard, 'entropy_label')
        assert hasattr(dashboard, 'zone_label')
        assert hasattr(dashboard, 'commentary_text')
        
        # Destroy the GUI
        dashboard.root.destroy()
        
        print("✅ GUI dashboard creation successful")
        
    except ImportError:
        print("⚠️ GUI test skipped - tkinter not available")
    except Exception as e:
        print(f"❌ GUI test failed: {e}")


def test_error_handling():
    """Test error handling and fallback mechanisms."""
    print("🛡️ Testing error handling...")
    
    try:
        from dawn_core.main import DAWNCognitiveEngine
        
        # Test engine with no existing DAWN systems
        engine = DAWNCognitiveEngine()
        
        # Should still work with fallbacks
        engine.tick()
        
        state = engine.get_state()
        assert 'system_metrics' in state
        
        print("✅ Error handling and fallbacks working")
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")


def run_integration_test():
    """Run the complete integration test suite."""
    print("🧪 DAWN Core Integration Test Suite")
    print("=" * 40)
    
    # Test imports
    test_imports()
    
    # Test engine creation
    engine = test_engine_creation()
    print()
    
    # Test single tick
    test_single_tick(engine)
    print()
    
    # Test multiple ticks
    test_multiple_ticks(engine, count=3)
    print()
    
    # Test snapshot creation
    test_snapshot_creation(engine)
    print()
    
    # Test GUI creation
    test_gui_creation()
    print()
    
    # Test error handling
    test_error_handling()
    print()
    
    print("🎯 Integration test complete!")
    print("\nTo run DAWN Core:")
    print("  python dawn_core/launch.py engine    # Start cognitive engine")
    print("  python dawn_core/launch.py gui       # Start GUI dashboard")
    print("  python dawn_core/launch.py snapshot  # Create system snapshot")


if __name__ == "__main__":
    run_integration_test() 