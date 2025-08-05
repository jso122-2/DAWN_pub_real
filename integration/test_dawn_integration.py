#!/usr/bin/env python3
"""
DAWN Integration Test Script
============================

Test script to demonstrate the DAWN conversation integration system
with various conversation scenarios and consciousness states.
"""

import time
import json
from typing import Dict, Any

def test_dawn_integration():
    """Test the DAWN conversation integration system"""
    
    print("🧠 DAWN Conversation Integration Test")
    print("=" * 50)
    
    try:
        # Import the integration system
        from dawn_conversation_integration import get_dawn_conversation_integration
        
        # Get the integration system
        integration = get_dawn_conversation_integration()
        
        # Display system status
        print("\n📊 System Status:")
        status = integration.get_system_status()
        for key, value in status.items():
            print(f"   {key}: {value}")
        
        # Test conversation scenarios
        test_scenarios = [
            {
                'name': 'Basic Greeting',
                'input': 'Hello DAWN, how are you feeling?',
                'description': 'Simple greeting to test basic response generation'
            },
            {
                'name': 'Consciousness Inquiry',
                'input': 'What is consciousness to you? How do you experience it?',
                'description': 'Deep consciousness inquiry to trigger Owl tracer'
            },
            {
                'name': 'Network Connection',
                'input': 'How do you connect different thoughts and memories?',
                'description': 'Network-related question to trigger Spider tracer'
            },
            {
                'name': 'Pressure Inquiry',
                'input': 'I feel overwhelmed with complexity. How do you handle cognitive pressure?',
                'description': 'Pressure-related question to trigger Crow tracer'
            },
            {
                'name': 'Emergency Scenario',
                'input': 'Help! I think there might be a problem with the system!',
                'description': 'Emergency scenario to potentially trigger Mr. Wolf'
            }
        ]
        
        print(f"\n🔄 Testing {len(test_scenarios)} conversation scenarios...")
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n{i}. {scenario['name']}")
            print(f"   Description: {scenario['description']}")
            print(f"   Input: \"{scenario['input']}\"")
            
            # Process the input
            start_time = time.time()
            result = integration.process_user_input(scenario['input'])
            processing_time = time.time() - start_time
            
            # Display results
            print(f"   Response: \"{result['response']}\"")
            print(f"   Processing time: {processing_time:.2f}s")
            print(f"   Strategy: {result['response_strategy']}")
            print(f"   Tracers activated: {result['activated_tracers']}")
            print(f"   Voice success: {result['voice_success']}")
            
            # Display consciousness state
            consciousness = result['consciousness_state']
            print(f"   Consciousness: SCUP={consciousness.get('scup', 0):.1f}, "
                  f"Entropy={consciousness.get('entropy', 0):.2f}, "
                  f"Pressure={consciousness.get('cognitive_pressure', 0):.1f}")
            
            # Small delay between tests
            time.sleep(1)
        
        # Display conversation summary
        print(f"\n📈 Conversation Summary:")
        summary = integration.get_conversation_summary()
        for key, value in summary.items():
            print(f"   {key}: {value}")
        
        print(f"\n✅ Integration test completed successfully!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all integration components are available")
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()

def test_individual_components():
    """Test individual integration components"""
    
    print("\n🧪 Testing Individual Components...")
    
    # Test cognitive pressure bridge
    try:
        from integration.cognitive_pressure_bridge import get_cognitive_pressure_bridge
        bridge = get_cognitive_pressure_bridge()
        print("✅ Cognitive Pressure Bridge: Available")
    except ImportError as e:
        print(f"⚠️ Cognitive Pressure Bridge: Not available ({e})")
    
    # Test tracer activation system  
    try:
        from integration.tracer_activation_system import get_tracer_activation_system
        tracer_system = get_tracer_activation_system()
        print("✅ Tracer Activation System: Available")
    except ImportError as e:
        print(f"⚠️ Tracer Activation System: Not available ({e})")
    
    # Test voice integration system
    try:
        from integration.voice_integration_system import get_voice_integration_system
        voice_system = get_voice_integration_system()
        print("✅ Voice Integration System: Available")
    except ImportError as e:
        print(f"⚠️ Voice Integration System: Not available ({e})")
    
    print("🔍 Individual component testing complete")

def main():
    """Main test function"""
    print("🧠 DAWN Integration System Test Suite")
    print("=" * 60)
    
    # Test individual components first
    test_individual_components()
    
    # Test full integration
    test_dawn_integration()
    
    print(f"\n🎉 Test suite completed!")

if __name__ == "__main__":
    main() 