# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
Test DAWN Conversation System
=============================

Simple test script to verify the conversation system components work correctly.
Tests speech recognition, response generation, and voice synthesis.
"""

import sys
import os
import time
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("test_conversation")

def test_conversation_input():
    """Test the conversation input system"""
    print("🎤 Testing Conversation Input System...")
    
    try:
        from .conversation_input import ConversationInput
        
        # Initialize conversation input
        conv_input = ConversationInput()
        print("✅ ConversationInput initialized successfully")
        
        # Test status
        status = conv_input.get_status()
        print(f"📊 Input Status: {status}")
        
        return True
        
    except ImportError as e:
        print(f"❌ ConversationInput import failed: {e}")
        print("💡 Install dependencies: pip install SpeechRecognition PyAudio")
        return False
    except Exception as e:
        print(f"❌ ConversationInput test failed: {e}")
        return False

def test_conversation_response():
    """Test the conversation response generator"""
    print("\n🧠 Testing Conversation Response Generator...")
    
    try:
        from .conversation_response import ConversationResponse
        
        # Create a mock state provider
        class MockStateProvider:
            def __init__(self):
                self.entropy = 0.5
                self.heat = 25.0
                self.scup = 20.0
                self.zone = "STABLE"
                self.reblooms = 0
                self.cognitive_pressure = 0.0
                self.schema_health = 0.5
            
            def get_current_state(self):
                return {
                    'entropy': self.entropy,
                    'heat': self.heat,
                    'scup': self.scup,
                    'zone': self.zone,
                    'reblooms': self.reblooms,
                    'cognitive_pressure': self.cognitive_pressure,
                    'schema_health': self.schema_health
                }
        
        # Initialize response generator
        state_provider = MockStateProvider()
        response_gen = ConversationResponse(state_provider)
        print("✅ ConversationResponse initialized successfully")
        
        # Test response generation
        test_inputs = [
            "Hello DAWN, how are you feeling?",
            "What's your current entropy level?",
            "Are you experiencing any thermal stress?",
            "Tell me about your cognitive state."
        ]
        
        print("\n💬 Testing Response Generation:")
        for i, test_input in enumerate(test_inputs, 1):
            response = response_gen.generate_response(test_input)
            print(f"  {i}. Input: {test_input}")
            print(f"     Response: {response}")
            print()
        
        # Test different cognitive states
        print("🧪 Testing Different Cognitive States:")
        
        # High entropy state
        state_provider.entropy = 0.8
        state_provider.zone = "ACTIVE"
        response = response_gen.generate_response("How are you feeling now?")
        print(f"  High Entropy: {response}")
        
        # Low entropy state
        state_provider.entropy = 0.2
        state_provider.zone = "STABLE"
        response = response_gen.generate_response("And now?")
        print(f"  Low Entropy: {response}")
        
        # Critical thermal state
        state_provider.entropy = 0.5
        state_provider.zone = "CRITICAL"
        state_provider.heat = 85.0
        response = response_gen.generate_response("What's happening?")
        print(f"  Critical Thermal: {response}")
        
        # Test conversation stats
        stats = response_gen.get_conversation_stats()
        print(f"\n📊 Conversation Stats: {stats}")
        
        return True
        
    except ImportError as e:
        print(f"❌ ConversationResponse import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ ConversationResponse test failed: {e}")
        return False

def test_enhanced_voice_system():
    """Test the enhanced voice system"""
    print("\n🔊 Testing Enhanced Voice System...")
    
    try:
        from tracers.enhanced_tracer_echo_voice import get_enhanced_voice_echo
        
        # Get voice system
        voice_system = get_enhanced_voice_echo()
        print("✅ Enhanced Voice System initialized")
        
        # Test voice stats
        stats = voice_system.get_voice_stats()
        print(f"📊 Voice Stats: {stats}")
        
        # Test conversation status
        conv_status = voice_system.get_conversation_status()
        print(f"💬 Conversation Status: {conv_status}")
        
        # Test immediate speech (if TTS available)
        if voice_system.tts_engine:
            print("🗣️ Testing voice synthesis...")
            voice_system.speak_immediate("Testing DAWN conversation system", "system")
            print("✅ Voice synthesis test completed")
        else:
            print("⚠️ No TTS engine available - skipping voice synthesis test")
        
        return True
        
    except ImportError as e:
        print(f"❌ Enhanced Voice System import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Enhanced Voice System test failed: {e}")
        return False

def test_integration():
    """Test integration between components"""
    print("\n🔗 Testing Component Integration...")
    
    try:
        # Test that conversation components can work together
        from .conversation_input import ConversationInput
        from .conversation_response import ConversationResponse
        from tracers.enhanced_tracer_echo_voice import get_enhanced_voice_echo
        
        # Initialize all components
        conv_input = ConversationInput()
        
        class MockStateProvider:
            def __init__(self):
                self.entropy = 0.5
                self.heat = 25.0
                self.scup = 20.0
                self.zone = "STABLE"
                self.reblooms = 0
                self.cognitive_pressure = 0.0
                self.schema_health = 0.5
        
        state_provider = MockStateProvider()
        response_gen = ConversationResponse(state_provider)
        voice_system = get_enhanced_voice_echo()
        
        print("✅ All components initialized successfully")
        
        # Test response generation and voice synthesis
        test_message = "Hello DAWN, this is a test of the conversation system."
        response = response_gen.generate_response(test_message)
        
        print(f"💬 Generated Response: {response}")
        
        if voice_system.tts_engine:
            print("🗣️ Speaking response...")
            voice_system.speak_with_state_modulation(response)
            print("✅ Integration test completed")
        else:
            print("⚠️ No TTS engine - integration test completed without voice")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Run all conversation system tests"""
    print("🧪 DAWN Conversation System Test Suite")
    print("=" * 50)
    
    tests = [
        ("Conversation Input", test_conversation_input),
        ("Conversation Response", test_conversation_response),
        ("Enhanced Voice System", test_enhanced_voice_system),
        ("Component Integration", test_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📋 Test Results Summary")
    print("=" * 30)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Conversation system is ready.")
        print("\n💡 Next steps:")
        print("   1. Run: python scripts/run_dawn_unified.py")
        print("   2. Type: talk")
        print("   3. Start speaking to DAWN!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        print("\n💡 Common issues:")
        print("   - Install dependencies: pip install -r conversation_requirements.txt")
        print("   - On Windows, try: pip install pipwin && pipwin install pyaudio")
        print("   - Ensure microphone is available and working")

if __name__ == "__main__":
    main() 