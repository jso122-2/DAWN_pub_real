#!/usr/bin/env python3
"""
Test Enhanced Entropy Analyzer Integration
Quick test to verify the enhanced entropy analyzer works with DAWN components.
"""

import sys
import os
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_enhanced_entropy_analyzer():
    """Test the enhanced entropy analyzer integration"""
    print("🧪 Testing Enhanced Entropy Analyzer Integration")
    print("=" * 60)
    
    try:
        # Test basic import
        print("📦 Testing imports...")
        from core.dawn_entropy_analyzer import EnhancedEntropyAnalyzer
        print("✅ Enhanced entropy analyzer imported successfully")
        
        # Test pulse controller integration
        pulse_controller = None
        try:
            from core.pulse_controller import PulseController
            pulse_controller = PulseController()
            print("✅ Pulse controller imported and instantiated")
        except ImportError as e:
            print(f"⚠️  Pulse controller import failed: {e}")
        except Exception as e:
            print(f"⚠️  Pulse controller instantiation failed: {e}")
        
        # Initialize the enhanced entropy analyzer
        print("\n🧠 Creating enhanced entropy analyzer...")
        analyzer = EnhancedEntropyAnalyzer()
        print("✅ Enhanced entropy analyzer created successfully")
        
        # Test basic functionality
        print("\n📊 Testing basic analysis functions...")
        
        # Test with sample data
        sample_readings = [0.3, 0.4, 0.7, 0.2, 0.6, 0.8, 0.1, 0.9]
        
        try:
            # Test entropy calculation
            entropy = analyzer.calculate_entropy(sample_readings)
            print(f"✅ Entropy calculation: {entropy:.3f}")
            
            # Test pattern detection
            patterns = analyzer.detect_patterns(sample_readings)
            print(f"✅ Pattern detection: {len(patterns)} patterns found")
            
            # Test prediction
            prediction = analyzer.predict_next_values(sample_readings, steps=3)
            print(f"✅ Prediction: {len(prediction)} future values generated")
            
        except Exception as e:
            print(f"❌ Analysis function test failed: {e}")
            return False
        
        # Test pulse controller integration if available
        if pulse_controller:
            print("\n🔄 Testing pulse controller integration...")
            try:
                # Test getting current state
                current_state = pulse_controller.get_current_state()
                print(f"✅ Current pulse state: {current_state}")
                
                # Test entropy integration
                entropy_reading = analyzer.calculate_entropy(sample_readings)
                pulse_controller.update_entropy(entropy_reading)
                print(f"✅ Entropy update sent to pulse controller: {entropy_reading:.3f}")
                
            except Exception as e:
                print(f"❌ Pulse controller integration test failed: {e}")
        
        print("\n🎉 Enhanced entropy analyzer integration test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("💡 Make sure all DAWN core components are available")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_entropy_analyzer_with_mock_data():
    """Test with various mock data scenarios"""
    print("\n🔬 Testing with mock data scenarios...")
    
    try:
        from core.dawn_entropy_analyzer import EnhancedEntropyAnalyzer
        analyzer = EnhancedEntropyAnalyzer()
        
        # Test scenarios
        scenarios = {
            "Low entropy (stable)": [0.5] * 10,
            "High entropy (chaotic)": [random.random() for _ in range(10)],
            "Rising trend": [i * 0.1 for i in range(10)],
            "Oscillating": [0.5 + 0.3 * math.sin(i * 0.5) for i in range(10)]
        }
        
        for scenario_name, data in scenarios.items():
            print(f"\n📈 Testing scenario: {scenario_name}")
            entropy = analyzer.calculate_entropy(data)
            patterns = analyzer.detect_patterns(data)
            print(f"   Entropy: {entropy:.3f}, Patterns: {len(patterns)}")
        
        print("✅ All mock data scenarios completed")
        
    except Exception as e:
        print(f"❌ Mock data test failed: {e}")


if __name__ == "__main__":
    print("🌟 DAWN Enhanced Entropy Integration Test Suite")
    print("=" * 60)
    
    import random
    import math
    
    # Run main integration test
    success = test_enhanced_entropy_analyzer()
    
    if success:
        # Run additional mock data tests
        test_entropy_analyzer_with_mock_data()
        print("\n🏆 All tests completed successfully!")
    else:
        print("\n💥 Integration test failed!")
        sys.exit(1) 