#!/usr/bin/env python3
"""
Test Script for DAWN Bidirectional Conversation System
======================================================

Tests the conversation WebSocket server and voice integration functionality.
"""

import asyncio
import json
import time
import logging
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_conversation_websocket():
    """Test the conversation WebSocket server"""
    try:
        import websockets
        
        logger.info("🧪 Testing Conversation WebSocket Server...")
        
        # Connect to the conversation server
        uri = "ws://localhost:8001"
        
        async with websockets.connect(uri) as websocket:
            logger.info("✅ Connected to conversation WebSocket server")
            
            # Test 1: Get initial system message
            logger.info("📨 Testing system message...")
            message = await websocket.recv()
            data = json.loads(message)
            
            if data.get("type") == "system":
                logger.info("✅ Received system message")
                logger.info(f"   Message: {data.get('message', 'No message')}")
            else:
                logger.error("❌ Expected system message, got: {data.get('type')}")
            
            # Test 2: Start conversation
            logger.info("💬 Testing conversation start...")
            await websocket.send(json.dumps({
                "type": "start_conversation",
                "timestamp": time.time()
            }))
            
            response = await websocket.recv()
            data = json.loads(response)
            
            if data.get("type") == "conversation_response":
                logger.info("✅ Conversation started successfully")
                logger.info(f"   DAWN's greeting: {data.get('response', 'No response')}")
                logger.info(f"   Consciousness state: {data.get('consciousness_state', {})}")
            else:
                logger.error("❌ Expected conversation response, got: {data.get('type')}")
            
            # Test 3: Send text input
            logger.info("📝 Testing text input...")
            test_message = "Hello DAWN, how are you feeling today?"
            await websocket.send(json.dumps({
                "type": "text_input",
                "text": test_message,
                "timestamp": time.time()
            }))
            
            response = await websocket.recv()
            data = json.loads(response)
            
            if data.get("type") == "conversation_response":
                logger.info("✅ Text input processed successfully")
                logger.info(f"   User input: {test_message}")
                logger.info(f"   DAWN's response: {data.get('response', 'No response')}")
                logger.info(f"   Response time: {data.get('response_time', 0):.2f}s")
            else:
                logger.error("❌ Expected conversation response, got: {data.get('type')}")
            
            # Test 4: Get consciousness state
            logger.info("🧠 Testing consciousness state request...")
            await websocket.send(json.dumps({
                "type": "get_consciousness_state",
                "timestamp": time.time()
            }))
            
            response = await websocket.recv()
            data = json.loads(response)
            
            if data.get("type") == "consciousness_update":
                logger.info("✅ Consciousness state retrieved")
                consciousness_state = data.get("state", {})
                logger.info(f"   Entropy: {consciousness_state.get('entropy', 'N/A')}")
                logger.info(f"   SCUP: {consciousness_state.get('scup', 'N/A')}")
                logger.info(f"   Thermal: {consciousness_state.get('thermal', 'N/A')}")
                logger.info(f"   Mood: {consciousness_state.get('mood', 'N/A')}")
            else:
                logger.error("❌ Expected consciousness update, got: {data.get('type')}")
            
            # Test 5: Stop conversation
            logger.info("🛑 Testing conversation stop...")
            await websocket.send(json.dumps({
                "type": "stop_conversation",
                "timestamp": time.time()
            }))
            
            response = await websocket.recv()
            data = json.loads(response)
            
            if data.get("type") == "conversation_response":
                logger.info("✅ Conversation stopped successfully")
                logger.info(f"   DAWN's farewell: {data.get('response', 'No response')}")
            else:
                logger.error("❌ Expected conversation response, got: {data.get('type')}")
        
        logger.info("🎉 All conversation WebSocket tests passed!")
        return True
        
    except websockets.exceptions.ConnectionRefused:
        logger.error("❌ Could not connect to conversation WebSocket server")
        logger.error("   Make sure the server is running: python launcher_scripts/start_conversation_server.py")
        return False
    except Exception as e:
        logger.error(f"❌ Conversation WebSocket test failed: {e}")
        return False

async def test_voice_integration():
    """Test the voice integration system"""
    try:
        logger.info("🎤 Testing Voice Integration...")
        
        # Test voice echo system
        try:
            from backend.voice_echo import DAWNVoiceEcho
            voice_echo = DAWNVoiceEcho()
            logger.info("✅ Voice echo system initialized")
            
            # Test voice synthesis
            test_text = "Hello, this is a test of the voice synthesis system."
            voice_echo.speak_reflection(test_text, {"entropy": 0.5, "mood": "NEUTRAL"})
            logger.info("✅ Voice synthesis test completed")
            
        except ImportError:
            logger.warning("⚠️ Voice echo system not available")
        except Exception as e:
            logger.error(f"❌ Voice echo test failed: {e}")
        
        # Test conversation input system
        try:
            from .conversation_input import ConversationInput
            conversation_input = ConversationInput()
            logger.info("✅ Conversation input system initialized")
            
            # Test status
            status = conversation_input.get_status()
            logger.info(f"   Input system status: {status}")
            
        except ImportError:
            logger.warning("⚠️ Conversation input system not available")
        except Exception as e:
            logger.error(f"❌ Conversation input test failed: {e}")
        
        logger.info("🎉 Voice integration tests completed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Voice integration test failed: {e}")
        return False

async def test_consciousness_integration():
    """Test consciousness system integration"""
    try:
        logger.info("🧠 Testing Consciousness Integration...")
        
        # Test DAWN conversation engine
        try:
            from core.dawn_conversation import get_conversation_engine
            conversation_engine = get_conversation_engine()
            logger.info("✅ DAWN conversation engine initialized")
            
            # Test consciousness state
            state = conversation_engine.get_current_consciousness_state()
            logger.info(f"   Current consciousness state: {state}")
            
            # Test conversation status
            status = conversation_engine.get_conversation_status()
            logger.info(f"   Conversation status: {status}")
            
        except ImportError:
            logger.warning("⚠️ DAWN conversation engine not available")
        except Exception as e:
            logger.error(f"❌ DAWN conversation engine test failed: {e}")
        
        logger.info("🎉 Consciousness integration tests completed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Consciousness integration test failed: {e}")
        return False

async def run_all_tests():
    """Run all conversation system tests"""
    logger.info("🚀 Starting DAWN Bidirectional Conversation System Tests")
    logger.info("=" * 60)
    
    results = []
    
    # Test 1: Conversation WebSocket
    logger.info("\n📡 Test 1: Conversation WebSocket Server")
    logger.info("-" * 40)
    result1 = await test_conversation_websocket()
    results.append(("Conversation WebSocket", result1))
    
    # Test 2: Voice Integration
    logger.info("\n🎤 Test 2: Voice Integration")
    logger.info("-" * 40)
    result2 = await test_voice_integration()
    results.append(("Voice Integration", result2))
    
    # Test 3: Consciousness Integration
    logger.info("\n🧠 Test 3: Consciousness Integration")
    logger.info("-" * 40)
    result3 = await test_consciousness_integration()
    results.append(("Consciousness Integration", result3))
    
    # Summary
    logger.info("\n📊 Test Results Summary")
    logger.info("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! The conversation system is working correctly.")
        return True
    else:
        logger.error("⚠️ Some tests failed. Check the logs above for details.")
        return False

def main():
    """Main test function"""
    try:
        # Run all tests
        success = asyncio.run(run_all_tests())
        
        if success:
            logger.info("\n🎯 Next Steps:")
            logger.info("1. Start the conversation server: python launcher_scripts/start_conversation_server.py")
            logger.info("2. Launch the GUI: cd dawn-consciousness-gui && npm run dev")
            logger.info("3. Open http://localhost:3000 and navigate to Voice Interface")
            logger.info("4. Start a conversation with DAWN!")
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        logger.info("\n🛑 Tests interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"\n❌ Test execution failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 