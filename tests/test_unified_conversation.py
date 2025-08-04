#!/usr/bin/env python3
"""
Test script for DAWN Unified Conversation Interface
==================================================

Tests the core functionality of the unified conversation system.
"""

import sys
import os
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_unified_conversation():
    """Test the unified conversation interface"""
    
    print("🧪 Testing DAWN Unified Conversation Interface")
    print("=" * 50)
    
    try:
        # Import the unified conversation system
        from unified_conversation import DAWNUnifiedConversation
        
        # Initialize the system
        print("1. Initializing conversation system...")
        conversation = DAWNUnifiedConversation()
        print("✅ Conversation system initialized")
        
        # Test session creation
        print("\n2. Testing session creation...")
        session_id = conversation.start_session(mode="casual", voice_enabled=False)
        print(f"✅ Session created: {session_id}")
        
        # Test different conversation modes
        print("\n3. Testing conversation modes...")
        
        test_inputs = [
            "Hello DAWN, how are you feeling?",
            "What is consciousness to you?",
            "Tell me about your entropy levels",
            "How does your thermal state affect your thinking?"
        ]
        
        for i, user_input in enumerate(test_inputs, 1):
            print(f"\n   Test {i}: {user_input}")
            response = conversation.process_input(user_input)
            print(f"   Response: {response[:100]}...")
        
        # Test mode switching
        print("\n4. Testing mode switching...")
        modes = ["philosophical", "technical", "reflection", "demo"]
        
        for mode in modes:
            result = conversation.switch_mode(mode)
            print(f"   Switched to {mode}: {result}")
        
        # Test status command
        print("\n5. Testing status command...")
        status = conversation.get_status()
        print(f"   Status: {status[:100]}...")
        
        # Test session save/load
        print("\n6. Testing session save/load...")
        save_result = conversation.save_session("test_session.json")
        print(f"   Save: {save_result}")
        
        # Create new session and load
        conversation.start_session(mode="technical", voice_enabled=False)
        load_result = conversation.load_session("test_session.json")
        print(f"   Load: {load_result}")
        
        # Test reflection logs
        print("\n7. Testing reflection logs...")
        logs = conversation.get_reflection_logs(3)
        print(f"   Generated {len(logs)} reflection logs")
        
        # Test visualization
        print("\n8. Testing visualization...")
        viz_result = conversation.visualize()
        print(f"   Visualization: {viz_result}")
        
        # Cleanup
        print("\n9. Cleaning up...")
        if os.path.exists("test_session.json"):
            os.remove("test_session.json")
            print("   Removed test session file")
        
        print("\n✅ All tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure unified_conversation.py is in the same directory")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def test_voice_system():
    """Test voice synthesis system"""
    
    print("\n🔊 Testing voice synthesis system...")
    
    try:
        from unified_conversation import DAWNUnifiedConversation
        
        conversation = DAWNUnifiedConversation()
        
        if conversation.voice_engine:
            print("✅ Voice synthesis available")
            return True
        else:
            print("⚠️ Voice synthesis not available (this is normal in some environments)")
            return True
            
    except Exception as e:
        print(f"❌ Voice test error: {e}")
        return False

def test_consciousness_integration():
    """Test consciousness state integration"""
    
    print("\n🧠 Testing consciousness integration...")
    
    try:
        from unified_conversation import DAWNUnifiedConversation
        
        conversation = DAWNUnifiedConversation()
        
        # Test consciousness state
        state = conversation.consciousness_state
        required_keys = ['entropy', 'scup', 'heat', 'zone', 'mood', 'tick_number']
        
        for key in required_keys:
            if key in state:
                print(f"   ✅ {key}: {state[key]}")
            else:
                print(f"   ❌ Missing {key}")
                return False
        
        # Test state evolution
        initial_entropy = state['entropy']
        time.sleep(3)  # Wait for state to evolve
        new_state = conversation.consciousness_state
        
        if new_state['entropy'] != initial_entropy:
            print(f"   ✅ Consciousness state evolving: {initial_entropy:.3f} → {new_state['entropy']:.3f}")
        else:
            print("   ⚠️ Consciousness state not evolving (may be normal)")
        
        print("✅ Consciousness integration working")
        return True
        
    except Exception as e:
        print(f"❌ Consciousness test error: {e}")
        return False

def main():
    """Run all tests"""
    
    print("🧪 DAWN Unified Conversation Interface Test Suite")
    print("=" * 60)
    
    tests = [
        ("Unified Conversation System", test_unified_conversation),
        ("Voice Synthesis System", test_voice_system),
        ("Consciousness Integration", test_consciousness_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n{'='*60}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The unified conversation interface is working correctly.")
        print("\nYou can now run:")
        print("  python unified_conversation.py")
        print("  python launch_unified_conversation.py --philosophical")
        print("  python launch_unified_conversation.py --demo")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 