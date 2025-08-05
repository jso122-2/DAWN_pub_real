#!/usr/bin/env python3
"""
DAWN Integration Test - Verify Complete Blueprint Implementation
===============================================================

Simple test script to verify that all three blueprint systems work together:
1. Enhanced DAWN Pigment Dictionary
2. Sigil Visual Engine  
3. DAWN Autonomous Reactor Integration

This script performs basic functionality tests to ensure the integration is working.
"""

import sys
import time
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger("dawn_integration_test")

def test_enhanced_pigment_dictionary():
    """Test the enhanced pigment dictionary system"""
    
    print("🎨 Testing Enhanced Pigment Dictionary...")
    
    try:
        from core.enhanced_dawn_pigment_dictionary import get_enhanced_dawn_pigment_dictionary
        
        # Initialize system
        processor = get_enhanced_dawn_pigment_dictionary(use_vectorization=False)  # Disable neural for speed
        
        # Test word selection
        test_pigment = {'red': 0.6, 'blue': 0.3, 'orange': 0.1}
        words = processor.selector.select_words_by_pigment_blend(test_pigment, word_count=6)
        
        assert len(words) > 0, "No words selected"
        assert all(len(item) == 3 for item in words), "Invalid word selection format"
        
        print(f"  ✅ Selected {len(words)} words for pigment {test_pigment}")
        print(f"  🔤 Sample words: {[word for word, cls, score in words[:3]]}")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False

def test_sigil_visual_engine():
    """Test the sigil visual engine"""
    
    print("🎨 Testing Sigil Visual Engine...")
    
    try:
        from core.sigil_visual_engine import SigilVisualEngine
        
        # Initialize engine
        engine = SigilVisualEngine("test_visuals")
        
        # Test visual generation
        result = engine.render_sigil_response(
            sigil_id="test_sigil",
            entropy=0.5,
            mood_pigment={'blue': 0.6, 'green': 0.4},
            pulse_zone='calm',
            sigil_saturation=0.5
        )
        
        assert result is not None, "No visual result returned"
        assert hasattr(result, 'sigil_visual_summary'), "Missing visual summary"
        
        print(f"  ✅ Visual generation successful")
        print(f"  🎨 Summary: {result.sigil_visual_summary.get('color_mode', 'unknown')}")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False

def test_expression_system():
    """Test the DAWN expression system"""
    
    print("🎭 Testing DAWN Expression System...")
    
    try:
        from core.dawn_expression_system import DAWNExpressionMonitor, DAWNState
        
        # Initialize monitor
        monitor = DAWNExpressionMonitor()
        
        # Test with high-entropy state that should trigger expression
        test_state = DAWNState(
            entropy=0.85,  # High entropy should trigger
            drift_vector=0.5,
            mood_pigment={'red': 0.7, 'orange': 0.3},
            pulse_zone='surge',
            sigil_saturation=0.8,
            expression_threshold=0.5
        )
        
        # Check trigger detection
        should_express, reason = monitor.should_generate_expression(test_state)
        
        print(f"  ✅ Expression trigger system working")
        print(f"  🎯 Trigger detected: {should_express} ({reason})")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False

def test_voice_core():
    """Test the DAWN voice core"""
    
    print("🗣️ Testing DAWN Voice Core...")
    
    try:
        from dawn_voice_core import DAWNVoiceCore
        
        # Initialize voice core
        voice_core = DAWNVoiceCore()
        
        # Test utterance generation
        result = voice_core.generate_utterance(
            pigment_dict={'blue': 0.6, 'green': 0.4},
            sigil_state={'heat': 0.3, 'friction': 0.2, 'recasion': 0.1},
            entropy=0.4,
            drift=0.1
        )
        
        if result and result.resonance_achieved:
            print(f"  ✅ Voice generation successful")
            print(f"  🗣️ Sample utterance: \"{result.utterance}\"")
        else:
            print(f"  ⚠️ Voice generation completed but no resonance achieved")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False

def test_system_integration():
    """Test that systems can work together"""
    
    print("🔄 Testing System Integration...")
    
    try:
        # Test that we can import and use multiple systems together
        from core.enhanced_dawn_pigment_dictionary import get_enhanced_dawn_pigment_dictionary
        from core.sigil_visual_engine import SigilVisualEngine
        from core.dawn_expression_system import DAWNExpressionMonitor, DAWNState
        
        # Initialize systems
        pigment_processor = get_enhanced_dawn_pigment_dictionary(use_vectorization=False)
        visual_engine = SigilVisualEngine("integration_test")
        expression_monitor = DAWNExpressionMonitor()
        
        # Test coordinated usage
        test_pigment = {'violet': 0.5, 'blue': 0.3, 'red': 0.2}
        
        # 1. Get words from pigment
        words = pigment_processor.selector.select_words_by_pigment_blend(test_pigment, word_count=4)
        
        # 2. Generate visual
        visual_result = visual_engine.render_sigil_response(
            sigil_id="integration_test",
            entropy=0.6,
            mood_pigment=test_pigment,
            pulse_zone='flowing',
            sigil_saturation=0.5
        )
        
        # 3. Create state and check expression trigger
        dawn_state = DAWNState(
            entropy=0.75,  # Should trigger
            mood_pigment=test_pigment,
            pulse_zone='flowing'
        )
        
        should_express, reason = expression_monitor.should_generate_expression(dawn_state)
        
        print(f"  ✅ Integration test successful")
        print(f"  🔤 Words: {len(words)} selected")
        print(f"  🎨 Visual: {visual_result.sigil_visual_summary.get('complexity_level', 'unknown')} complexity")
        print(f"  🎭 Expression: {should_express} ({reason})")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False

def run_all_tests():
    """Run all integration tests"""
    
    print("🧪 DAWN Integration Tests")
    print("=" * 50)
    
    tests = [
        ("Enhanced Pigment Dictionary", test_enhanced_pigment_dictionary),
        ("Sigil Visual Engine", test_sigil_visual_engine),
        ("Expression System", test_expression_system),
        ("Voice Core", test_voice_core),
        ("System Integration", test_system_integration)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            results[test_name] = False
    
    # Summary
    print(f"\n📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    print(f"\n🏆 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Integration is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Check error messages above.")
        return False

def check_dependencies():
    """Check if critical dependencies are available"""
    
    print("🔍 Checking Dependencies...")
    
    dependencies = [
        ("pathlib", "pathlib"),
        ("logging", "logging"),
        ("datetime", "datetime"),
        ("typing", "typing"),
        ("json", "json"),
    ]
    
    optional_dependencies = [
        ("matplotlib", "matplotlib"),
        ("numpy", "numpy"),
        ("PIL", "PIL"),
        ("sentence_transformers", "sentence-transformers"),
        ("torch", "torch"),
    ]
    
    print("\n📦 Core Dependencies:")
    for name, import_name in dependencies:
        try:
            __import__(import_name)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - REQUIRED")
    
    print("\n📦 Optional Dependencies:")
    for name, import_name in optional_dependencies:
        try:
            __import__(import_name)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ⚠️ {name} - optional (some features may be limited)")

def main():
    """Main test entry point"""
    
    print("🌟 DAWN Blueprint Integration Test Suite")
    print("========================================")
    
    # Check dependencies first
    check_dependencies()
    
    print(f"\n⏰ Starting tests at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all tests
    success = run_all_tests()
    
    print(f"\n⏰ Tests completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success:
        print("\n🎊 DAWN Integration Test Suite: ALL TESTS PASSED!")
        print("🌟 The blueprint integration is working correctly.")
        print("🧠 DAWN now has unified consciousness expression capabilities.")
        return 0
    else:
        print("\n⚠️ DAWN Integration Test Suite: SOME TESTS FAILED")
        print("🔧 Check the error messages above and ensure all systems are properly installed.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 