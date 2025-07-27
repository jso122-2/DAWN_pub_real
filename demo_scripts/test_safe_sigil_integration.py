#!/usr/bin/env python3
"""
Test Safe Sigil Integration
Verifies that the safe sigil processor eliminates undefined errors
"""

import queue
import time
import json
from typing import Dict, Any

def test_safe_sigil_processor():
    """Test the safe sigil processor standalone"""
    print("🔍 Testing Safe Sigil Processor...")
    
    from gui.sigil_safe_processor import SafeSigilProcessor, safe_process_sigils
    
    processor = SafeSigilProcessor()
    
    # Test cases that would cause undefined errors
    test_cases = [
        ("None data", None),
        ("Empty string", ""),
        ("Invalid dict", {"invalid": "data"}),
        ("Mixed list", [{"symbol": "🔥"}, "string", None, 123]),
        ("NaN values", {"heat": float('nan'), "decay": float('inf')}),
        ("Missing fields", {"symbol": "🌟"}),
        ("Complete valid", {
            "id": "test",
            "symbol": "🔥",
            "meaning": "Test sigil",
            "house": "fire",
            "heat": 0.8,
            "decay": 0.9,
            "source": "test",
            "timestamp": time.time(),
            "x": 0.5,
            "y": 0.5
        })
    ]
    
    for case_name, case_data in test_cases:
        print(f"\n  Testing: {case_name}")
        
        try:
            result = processor.process_sigil_data(case_data)
            print(f"    ✅ Success: {len(result)} sigils generated")
            
            # Verify all required fields are present
            for sigil in result:
                required_fields = ["id", "symbol", "meaning", "house", "heat", "decay", "source", "timestamp", "x", "y"]
                missing_fields = [field for field in required_fields if field not in sigil]
                
                if missing_fields:
                    print(f"    ❌ Missing fields: {missing_fields}")
                    return False
                
                # Verify no undefined/None values
                undefined_fields = [field for field, value in sigil.items() if value is None]
                if undefined_fields:
                    print(f"    ❌ Undefined fields: {undefined_fields}")
                    return False
                
                print(f"    🎯 Sigil: {sigil['symbol']} ({sigil['house']}) - heat: {sigil['heat']:.2f}")
            
        except Exception as e:
            print(f"    ❌ Exception: {e}")
            return False
    
    print("✅ Safe Sigil Processor test passed!")
    return True

def test_tick_engine_integration():
    """Test the tick engine with safe sigil integration"""
    print("\n🔍 Testing Tick Engine Integration...")
    
    try:
        from tick_engine.core_tick import CoreTickEngine
        
        # Create test queue
        test_queue = queue.Queue(maxsize=10)
        
        # Initialize tick engine
        engine = CoreTickEngine(test_queue, tick_interval=0.1)
        
        print("  ✅ Tick engine initialized")
        
        # Generate test tick data
        tick_data = engine._generate_tick_data()
        
        print(f"  ✅ Tick data generated: {len(tick_data)} fields")
        
        # Check sigils specifically
        if "sigils" in tick_data:
            sigils = tick_data["sigils"]
            print(f"  🎯 Found {len(sigils)} sigils")
            
            # Verify each sigil is valid
            for i, sigil in enumerate(sigils):
                if not isinstance(sigil, dict):
                    print(f"    ❌ Sigil {i} is not a dict: {type(sigil)}")
                    return False
                
                # Check required fields
                required_fields = ["id", "symbol", "meaning", "house", "heat", "decay"]
                missing_fields = [field for field in required_fields if field not in sigil]
                
                if missing_fields:
                    print(f"    ❌ Sigil {i} missing fields: {missing_fields}")
                    return False
                
                # Check for undefined values
                undefined_fields = [field for field, value in sigil.items() 
                                  if value is None or (isinstance(value, float) and value != value)]
                
                if undefined_fields:
                    print(f"    ❌ Sigil {i} undefined fields: {undefined_fields}")
                    return False
                
                print(f"    ✅ Sigil {i}: {sigil['symbol']} ({sigil['house']}) - valid")
        else:
            print("  ❌ No sigils field in tick data")
            return False
        
        print("✅ Tick Engine Integration test passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ Tick engine test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gui_data_flow():
    """Test the data flow that would reach the GUI"""
    print("\n🔍 Testing GUI Data Flow...")
    
    try:
        # Simulate data that might come from various sources
        test_data_sources = [
            {"sigils": [{"symbol": "🔥", "heat": 0.8}]},  # Partial data
            {"sigils": "invalid_string"},                  # Invalid type
            {"sigils": None},                             # None value
            {"sigils": []},                               # Empty list
            {"no_sigils": "field"},                       # Missing sigils
            {},                                           # Empty dict
            None,                                         # None input
        ]
        
        from gui.sigil_safe_processor import safe_process_sigils
        
        for i, test_data in enumerate(test_data_sources):
            print(f"\n  Test case {i+1}: {type(test_data)}")
            
            try:
                # Extract sigils like GUI would
                if test_data is None:
                    sigil_data = None
                elif isinstance(test_data, dict):
                    sigil_data = test_data.get("sigils", [])
                else:
                    sigil_data = test_data
                
                print(f"    Extracted: {type(sigil_data)}")
                
                # Process through safe processor
                safe_sigils = safe_process_sigils(sigil_data, minimum_sigils=1)
                
                print(f"    ✅ Processed: {len(safe_sigils)} safe sigils")
                
                # Verify GUI could safely use this data
                for sigil in safe_sigils:
                    # Simulate GUI operations that might cause undefined errors
                    symbol = sigil["symbol"]          # Should never be undefined
                    heat = float(sigil["heat"])       # Should be valid number
                    x = float(sigil["x"])             # Should be valid position
                    y = float(sigil["y"])             # Should be valid position
                    house = str(sigil["house"])       # Should be valid string
                    
                    # Check ranges that GUI expects
                    assert 0.0 <= heat <= 1.0, f"Heat out of range: {heat}"
                    assert 0.0 <= x <= 1.0, f"X position out of range: {x}"
                    assert 0.0 <= y <= 1.0, f"Y position out of range: {y}"
                    
                    print(f"      ✅ {symbol} - heat:{heat:.2f} pos:({x:.2f},{y:.2f}) house:{house}")
                
            except Exception as e:
                print(f"    ❌ Test case {i+1} failed: {e}")
                return False
        
        print("✅ GUI Data Flow test passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ GUI data flow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_live_system_simulation():
    """Test a live system simulation"""
    print("\n🔍 Testing Live System Simulation...")
    
    try:
        from tick_engine.core_tick import CoreTickEngine
        from gui.sigil_safe_processor import safe_process_sigils
        
        # Create tick engine
        test_queue = queue.Queue()
        engine = CoreTickEngine(test_queue, tick_interval=0.1)
        
        # Simulate several ticks
        for tick in range(5):
            print(f"\n  Tick {tick + 1}:")
            
            # Generate tick data
            tick_data = engine._generate_tick_data()
            
            # Extract and process sigils
            raw_sigils = tick_data.get("sigils", [])
            safe_sigils = safe_process_sigils(raw_sigils)
            
            print(f"    Generated: {len(safe_sigils)} sigils")
            
            # Simulate GUI processing each sigil
            for i, sigil in enumerate(safe_sigils):
                # Test operations that would happen in GUI
                tooltip_text = f"{sigil['meaning']} (Heat: {sigil['heat']:.1%})"
                canvas_x = int(sigil['x'] * 300)  # Canvas width
                canvas_y = int(sigil['y'] * 200)  # Canvas height
                color_intensity = int(255 * sigil['heat'])
                
                print(f"      Sigil {i}: {sigil['symbol']} at ({canvas_x},{canvas_y}) - intensity:{color_intensity}")
            
            # Advance engine state
            engine.tick_count += 1
            engine.heat = (engine.heat + 5) % 100
            engine.scup = (engine.scup + 0.1) % 1.0
        
        print("✅ Live System Simulation test passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ Live simulation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 DAWN Safe Sigil Integration Test Suite")
    print("=" * 60)
    
    tests = [
        test_safe_sigil_processor,
        test_tick_engine_integration,
        test_gui_data_flow,
        test_live_system_simulation
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_func.__name__} failed")
        except Exception as e:
            print(f"❌ {test_func.__name__} crashed: {e}")
    
    print("\n" + "=" * 60)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ ALL TESTS PASSED - Sigil system is safe from undefined errors!")
        print("\n🔧 Integration recommendations:")
        print("  1. Always use safe_process_sigils() for any sigil data")
        print("  2. The system now handles None, invalid types, and missing fields")
        print("  3. GUI can safely access all sigil properties without undefined errors")
        print("  4. Fallback sigils are generated when needed")
    else:
        print("❌ Some tests failed - check the output above for details")
    
    return passed == total

if __name__ == "__main__":
    main() 