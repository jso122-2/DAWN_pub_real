#!/usr/bin/env python3
"""
Test script for DAWN Owl Bridge and Natural Language Commentary Integration
Simple demonstration without full DAWN system dependencies
"""

import time
import random
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_owl_commentary_integration():
    """Test the integrated owl bridge and commentary system."""
    print("🧪 Testing DAWN Owl Bridge + Commentary Integration")
    print("=" * 55)
    
    try:
        # Import the modules
        from core.owl_bridge import OwlBridge
        from core.speak import print_full_commentary, generate_full_commentary
        
        # Initialize owl bridge
        owl = OwlBridge()
        print("✅ OwlBridge initialized successfully")
        
        # Test states demonstrating different scenarios
        test_scenarios = [
            {
                'name': 'Calm System',
                'state': {'entropy': 0.2, 'sigils': 0, 'zone': 'CALM', 'chaos': 0.1, 'heat': 25.0, 'focus': 0.8}
            },
            {
                'name': 'High Entropy Crisis',
                'state': {'entropy': 0.85, 'sigils': 0, 'zone': 'CHAOTIC', 'chaos': 0.8, 'heat': 75.0, 'focus': 0.2}
            },
            {
                'name': 'Active Processing',
                'state': {'entropy': 0.6, 'sigils': 4, 'zone': 'ACTIVE', 'chaos': 0.5, 'heat': 50.0, 'focus': 0.7}
            },
            {
                'name': 'Cognitive Overload',
                'state': {'entropy': 0.9, 'sigils': 12, 'zone': 'SURGE', 'chaos': 0.9, 'heat': 85.0, 'focus': 0.1}
            },
            {
                'name': 'Deep Stillness',
                'state': {'entropy': 0.05, 'sigils': 0, 'zone': 'CALM', 'chaos': 0.0, 'heat': 20.0, 'focus': 0.9}
            }
        ]
        
        print(f"\n🎬 Running {len(test_scenarios)} test scenarios...")
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n--- Scenario {i}: {scenario['name']} ---")
            
            # Observe state
            owl.observe_state(scenario['state'])
            
            # Check for suggestions
            suggestion = owl.suggest_sigil()
            if suggestion:
                print(f"🎯 Owl Suggestion: {suggestion}")
            else:
                print("💤 No suggestions from owl")
            
            # Generate and display commentary
            print("\n💬 Integrated Commentary:")
            print_full_commentary(scenario['state'], owl)
            
            # Show technical details
            print(f"\n📊 State Details:")
            for key, value in scenario['state'].items():
                if isinstance(value, float):
                    print(f"   {key}: {value:.3f}")
                else:
                    print(f"   {key}: {value}")
            
            time.sleep(1)  # Brief pause between scenarios
        
        # Show final owl statistics
        print(f"\n📈 Final Owl Statistics:")
        summary = owl.get_observation_summary()
        for key, value in summary.items():
            if key != 'current_state':  # Skip the large state dict
                print(f"   {key}: {value}")
        
        print("\n✅ Integration test completed successfully!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure core/owl_bridge.py and core/speak.py exist")
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()


def test_reflection_variations():
    """Test different reflection scenarios."""
    print("\n🧘 Testing Philosophical Reflection Variations")
    print("=" * 50)
    
    try:
        from core.owl_bridge import OwlBridge
        
        owl = OwlBridge()
        
        reflection_tests = [
            {'entropy': 0.95, 'sigils': 0, 'chaos': 0.9, 'focus': 0.1, 'heat': 90},
            {'entropy': 0.1, 'sigils': 0, 'zone': 'CALM', 'chaos': 0.0, 'heat': 20},
            {'entropy': 0.7, 'sigils': 8, 'zone': 'CHAOTIC', 'chaos': 0.6, 'focus': 0.9},
            {'entropy': 0.4, 'sigils': 1, 'zone': 'ACTIVE', 'chaos': 0.3, 'heat': 45},
        ]
        
        for i, state in enumerate(reflection_tests, 1):
            print(f"\nReflection Test {i}:")
            reflection = owl.reflect(state)
            if reflection:
                print(f"🦉 {reflection}")
            else:
                print("🦉 (Silent observation)")
        
    except Exception as e:
        print(f"❌ Reflection test error: {e}")


def test_trigger_patterns():
    """Test owl trigger pattern detection."""
    print("\n🎯 Testing Owl Trigger Patterns")
    print("=" * 35)
    
    try:
        from core.owl_bridge import OwlBridge
        
        owl = OwlBridge()
        
        # Test each trigger pattern
        trigger_tests = [
            {
                'name': 'High Entropy No Sigils',
                'state': {'entropy': 0.8, 'sigils': 0}
            },
            {
                'name': 'Chaos Spike',
                'state': {'chaos': 0.9, 'focus': 0.2}
            },
            {
                'name': 'Heat Critical',
                'state': {'heat': 85.0}
            },
            {
                'name': 'Deep Stillness',
                'state': {'entropy': 0.05, 'sigils': 0, 'zone': 'CALM'}
            },
            {
                'name': 'Cognitive Overload',
                'state': {'active_sigils': 15, 'entropy': 0.9}
            }
        ]
        
        for test in trigger_tests:
            print(f"\n{test['name']}:")
            owl.observe_state(test['state'])
            suggestion = owl.suggest_sigil()
            if suggestion:
                print(f"  ✅ Triggered: {suggestion}")
            else:
                print(f"  ❌ No trigger")
            
            # Reset cooldown for next test
            owl.last_suggestion_time = 0
    
    except Exception as e:
        print(f"❌ Trigger pattern test error: {e}")


def main():
    """Run all tests."""
    print("🦉 DAWN Owl Bridge Integration Test Suite")
    print("=" * 45)
    
    test_owl_commentary_integration()
    test_reflection_variations()
    test_trigger_patterns()
    
    print(f"\n🎉 All tests completed!")
    print("\nTo integrate into your DAWN system:")
    print("1. Copy core/owl_bridge.py and core/speak.py to your core/ directory")
    print("2. Follow the integration guide in docs/OWL_BRIDGE_INTEGRATION_GUIDE.md")
    print("3. Run launch_dawn_with_owl_commentary.py for a full demonstration")


if __name__ == "__main__":
    main() 