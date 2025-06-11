#!/usr/bin/env python3
"""
Test DAWN Wiring
Validates that all modules can be imported and initialized
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all core modules can be imported"""
    print("🧪 Testing module imports...")
    
    modules_to_test = [
        ("core.event_bus", "EventBus"),
        ("core.config_loader", "ConfigLoader"),
        ("core.schema_state", "SchemaState"),
        ("core.tick_emitter", "TickEmitter"),
        ("core.system.dawn_orchestrator", "DAWNOrchestrator"),
        ("bloom.bloom_engine", "BloomEngine"),
        ("pulse.pulse_engine", "PulseEngine"),
        ("processors.codex.sigils", "SigilProcessor"),
        ("reflection.owl.owl", "OwlSystem"),
        ("mood.mood", "MoodEngine"),
        ("semantic.semantic_context_engine", "SemanticContextEngine"),
        ("core.dawn_central", "DAWNCentral"),
    ]
    
    failed = []
    
    for module_path, class_name in modules_to_test:
        try:
            module = __import__(module_path, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✅ {module_path}.{class_name}")
        except Exception as e:
            print(f"❌ {module_path}.{class_name}: {e}")
            failed.append((module_path, str(e)))
            
    if failed:
        print(f"\n❌ {len(failed)} imports failed:")
        for module, error in failed:
            print(f"  - {module}: {error}")
        return False
    else:
        print(f"\n✅ All {len(modules_to_test)} imports successful!")
        return True

def test_initialization():
    """Test basic initialization"""
    print("\n🧪 Testing initialization...")
    
    try:
        from core.dawn_central import DAWNCentral
        
        # Create instance
        print("Creating DAWNCentral instance...")
        dawn = DAWNCentral()
        print("✅ DAWNCentral created")
        
        # Test boot sequence
        print("Running boot sequence...")
        dawn.boot_sequence()
        print("✅ Boot sequence completed")
        
        # Get status
        status = dawn.get_status()
        print(f"✅ System status: {status}")
        
        # Shutdown
        print("Shutting down...")
        dawn.shutdown()
        print("✅ Shutdown completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_minimal_run():
    """Test minimal run with a few ticks"""
    print("\n🧪 Testing minimal run...")
    
    try:
        from core.dawn_central import DAWNCentral
        
        dawn = DAWNCentral()
        dawn.boot_sequence()
        
        # Run 5 ticks
        print("Running 5 ticks...")
        for i in range(5):
            dawn.tick_engine.emit_tick()
            print(f"  Tick {i+1} completed")
            
        dawn.shutdown()
        print("✅ Minimal run successful")
        return True
        
    except Exception as e:
        print(f"❌ Minimal run failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🌅 DAWN Wiring Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Initialization Test", test_initialization),
        ("Minimal Run Test", test_minimal_run),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        print("-" * 40)
        success = test_func()
        results.append((test_name, success))
        
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {test_name}: {status}")
        
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! DAWN is ready to run.")
        print("\nTo start DAWN:")
        print("  python dawn.py")
        print("\nFor test mode:")
        print("  python dawn.py --test")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())