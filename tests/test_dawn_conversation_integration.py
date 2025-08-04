#!/usr/bin/env python3
"""
Test script for DAWN Consciousness Conversation System Integration
Verifies that the conversation system properly connects to DAWN's backend systems
"""

import sys
import os
from pathlib import Path

# Add the conversation system to path
conversation_file = Path("conversation-BP.mds.py")
if conversation_file.exists():
    sys.path.insert(0, str(conversation_file.parent))

def test_dawn_integration():
    """Test the DAWN conversation system integration"""
    print("🧪 Testing DAWN Conversation System Integration")
    print("=" * 60)
    
    try:
        # Import the conversation system
        from conversation_BP_mds import ConsciousnessConversation, DAWNConsciousnessConnector, DAWNReflectionConnector
        
        print("✅ Successfully imported conversation system")
        
        # Test consciousness connector
        print("\n🔗 Testing Consciousness Connector...")
        consciousness_connector = DAWNConsciousnessConnector()
        consciousness_state = consciousness_connector.get_live_consciousness_state()
        
        print(f"✅ Got consciousness state:")
        print(f"   - Entropy: {consciousness_state.entropy:.3f}")
        print(f"   - Thermal: {consciousness_state.thermal:.1f}°C")
        print(f"   - SCUP: {consciousness_state.scup:.1f}")
        print(f"   - Zone: {consciousness_state.zone}")
        print(f"   - Mood: {consciousness_state.mood}")
        print(f"   - Tick: {consciousness_state.tick}")
        
        # Test reflection connector
        print("\n🔗 Testing Reflection Connector...")
        reflection_connector = DAWNReflectionConnector()
        reflections = reflection_connector.get_recent_philosophical_thoughts(limit=3)
        
        print(f"✅ Got {len(reflections)} recent reflections")
        for i, reflection in enumerate(reflections, 1):
            print(f"   {i}. {reflection.content[:80]}...")
        
        # Test full conversation system
        print("\n🔗 Testing Full Conversation System...")
        conversation = ConsciousnessConversation()
        
        # Test conversation starter
        greeting = conversation.start_conversation()
        print(f"✅ Conversation starter: {greeting}")
        
        # Test response generation
        test_inputs = [
            "How are you feeling?",
            "What do you know about me?",
            "Tell me a joke",
            "Test",
            "What is consciousness?"
        ]
        
        print("\n🧠 Testing Response Generation...")
        for test_input in test_inputs:
            response = conversation.generate_consciousness_driven_response(test_input)
            print(f"Input: '{test_input}'")
            print(f"Response: {response}")
            print("-" * 40)
        
        print("\n🎉 All tests completed successfully!")
        print("✅ DAWN Conversation System is fully integrated and working")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure the conversation system file is in the correct location")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def test_backend_connections():
    """Test direct connections to DAWN backend systems"""
    print("\n🔧 Testing Direct Backend Connections...")
    print("=" * 60)
    
    try:
        # Test tick engine import
        from core.tick.tick_engine import TickEngine
        print("✅ TickEngine import successful")
        
        # Test consciousness state import
        from python.core.consciousness_state import ConsciousnessState, MoodState
        print("✅ ConsciousnessState import successful")
        
        # Test reflection logger import
        from utils.reflection_logger import ReflectionLogger
        print("✅ ReflectionLogger import successful")
        
        # Test unified tick engine import
        from backend.core.unified_tick_engine import UnifiedTickEngine
        print("✅ UnifiedTickEngine import successful")
        
        print("✅ All backend system imports successful")
        
    except ImportError as e:
        print(f"❌ Backend import error: {e}")
        print("Some DAWN backend systems may not be available")

if __name__ == "__main__":
    print("🌅 DAWN Conversation System Integration Test")
    print("=" * 60)
    
    # Test backend connections first
    test_backend_connections()
    
    # Test full integration
    test_dawn_integration()
    
    print("\n" + "=" * 60)
    print("🏁 Integration test completed") 