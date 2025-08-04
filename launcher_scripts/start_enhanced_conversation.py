#!/usr/bin/env python3
"""
DAWN Enhanced Conversation System Launcher
==========================================

Launcher for the enhanced conversation system with CLI interface and WebSocket server.
Provides fallback modes for audio device issues and detailed thought process logging.
"""

import asyncio
import logging
import argparse
import sys
import time
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('runtime/logs/enhanced_conversation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def start_cli_conversation(enable_audio: bool = False, enable_thought_logging: bool = True):
    """Start CLI conversation interface"""
    try:
        from .cli_dawn_conversation import DAWNCLIConversation
        
        logger.info("🚀 Starting DAWN CLI Conversation Interface...")
        
        conversation = DAWNCLIConversation(
            enable_audio=enable_audio,
            enable_thought_logging=enable_thought_logging
        )
        
        conversation.start_conversation()
        
    except ImportError as e:
        logger.error(f"❌ Failed to import CLI conversation module: {e}")
        print("❌ CLI conversation module not available. Please check your installation.")
    except Exception as e:
        logger.error(f"❌ CLI conversation error: {e}")
        print(f"❌ Error: {e}")

async def start_websocket_server(host: str = "localhost", port: int = 8003, enable_audio: bool = True, enable_thought_logging: bool = True):
    """Start WebSocket conversation server"""
    try:
        from backend.api.routes.conversation_websocket_enhanced import start_enhanced_conversation_websocket_server
        
        logger.info(f"🚀 Starting DAWN Enhanced Conversation WebSocket Server...")
        logger.info(f"   Host: {host}")
        logger.info(f"   Port: {port}")
        logger.info(f"   Audio: {'✅ Enabled' if enable_audio else '❌ Disabled'}")
        logger.info(f"   Thought Logging: {'✅ Enabled' if enable_thought_logging else '❌ Disabled'}")
        
        await start_enhanced_conversation_websocket_server(host, port)
        
    except ImportError as e:
        logger.error(f"❌ Failed to import WebSocket server module: {e}")
        print("❌ WebSocket server module not available. Please check your installation.")
    except Exception as e:
        logger.error(f"❌ WebSocket server error: {e}")
        print(f"❌ Error: {e}")

def run_test_mode():
    """Run enhanced conversation system in test mode"""
    try:
        from .cli_dawn_conversation import DAWNCLIConversation
        
        print("🧪 Running DAWN Enhanced Conversation System in test mode...")
        print("💭 DAWN: Hello! I'm in test mode. My enhanced consciousness systems are running.")
        
        # Initialize conversation
        conversation = DAWNCLIConversation(
            enable_audio=False,  # Disable audio for test mode
            enable_thought_logging=True
        )
        
        # Send test messages
        test_messages = [
            "Hello DAWN, how are you feeling?",
            "What's your current entropy level?",
            "Tell me about your consciousness",
            "Are you experiencing any memory reblooms?",
            "How is your cognitive processing today?",
            "Can you share your current thoughts?",
            "What's your thermal state?",
            "How are your memory systems functioning?"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n🧪 Test {i}: {message}")
            conversation.conversation_input.send_text_input(message)
            time.sleep(2)
        
        # Show thought history
        print("\n📝 Recent Thought History:")
        conversation._show_thought_history()
        
        # Show consciousness state
        print("\n🧠 Final Consciousness State:")
        conversation._show_consciousness_state()
        
        print("\n🧪 Enhanced conversation system test completed!")
        print("✅ All systems functioning correctly.")
        
    except Exception as e:
        logger.error(f"❌ Test mode error: {e}")
        print(f"❌ Test failed: {e}")

def check_system_status():
    """Check the status of the enhanced conversation system"""
    print("🔍 DAWN Enhanced Conversation System Status Check")
    print("=" * 50)
    
    # Check required modules
    modules_to_check = [
        ("conversation_input_enhanced", "Enhanced conversation input system"),
        ("cli_dawn_conversation", "CLI conversation interface"),
        ("backend.api.routes.conversation_websocket_enhanced", "WebSocket server"),
        ("speech_recognition", "Speech recognition (optional)"),
        ("websockets", "WebSocket support"),
    ]
    
    for module_name, description in modules_to_check:
        try:
            __import__(module_name)
            print(f"✅ {description}: Available")
        except ImportError:
            print(f"❌ {description}: Not available")
    
    # Check DAWN components
    print("\n🧠 DAWN Consciousness Components:")
    dawn_components = [
        ("core.dawn_conversation", "Conversation engine"),
        ("core.entropy_analyzer", "Entropy analyzer"),
        ("pulse.pulse_controller", "Pulse controller"),
        ("bloom.bloom_engine", "Bloom engine"),
    ]
    
    for component_name, description in dawn_components:
        try:
            __import__(component_name)
            print(f"✅ {description}: Available")
        except ImportError:
            print(f"❌ {description}: Not available (will use fallback)")
    
    # Check directories
    print("\n📁 Directory Structure:")
    directories = [
        ("runtime/logs", "Log files"),
        ("runtime/logs/thoughts", "Thought process logs"),
        ("runtime/logs/conversations", "Conversation history"),
    ]
    
    for dir_path, description in directories:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ {description}: {path}")
        else:
            print(f"❌ {description}: {path} (will be created)")
    
    print("\n" + "=" * 50)

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(
        description="DAWN Enhanced Conversation System Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start CLI conversation (text-only mode)
  python launcher_scripts/start_enhanced_conversation.py --cli
  
  # Start CLI conversation with audio
  python launcher_scripts/start_enhanced_conversation.py --cli --audio
  
  # Start WebSocket server
  python launcher_scripts/start_enhanced_conversation.py --websocket
  
  # Start WebSocket server without audio
  python launcher_scripts/start_enhanced_conversation.py --websocket --no-audio
  
  # Run test mode
  python launcher_scripts/start_enhanced_conversation.py --test
  
  # Check system status
  python launcher_scripts/start_enhanced_conversation.py --status
        """
    )
    
    parser.add_argument("--cli", action="store_true", 
                       help="Start CLI conversation interface")
    parser.add_argument("--websocket", action="store_true", 
                       help="Start WebSocket conversation server")
    parser.add_argument("--test", action="store_true", 
                       help="Run system in test mode")
    parser.add_argument("--status", action="store_true", 
                       help="Check system status and component availability")
    
    parser.add_argument("--audio", action="store_true", 
                       help="Enable audio input (requires microphone)")
    parser.add_argument("--no-audio", action="store_true", 
                       help="Disable audio input (text-only mode)")
    parser.add_argument("--no-thoughts", action="store_true", 
                       help="Disable thought process logging")
    
    parser.add_argument("--host", default="localhost", 
                       help="WebSocket server host (default: localhost)")
    parser.add_argument("--port", type=int, default=8003, 
                       help="WebSocket server port (default: 8003)")
    
    args = parser.parse_args()
    
    # Create necessary directories
    Path("runtime/logs").mkdir(parents=True, exist_ok=True)
    Path("runtime/logs/thoughts").mkdir(parents=True, exist_ok=True)
    Path("runtime/logs/conversations").mkdir(parents=True, exist_ok=True)
    
    # Determine audio and thought logging settings
    enable_audio = args.audio and not args.no_audio
    enable_thought_logging = not args.no_thoughts
    
    # Handle different modes
    if args.status:
        check_system_status()
        return
    
    elif args.test:
        run_test_mode()
        return
    
    elif args.cli:
        start_cli_conversation(enable_audio, enable_thought_logging)
        return
    
    elif args.websocket:
        try:
            asyncio.run(start_websocket_server(
                host=args.host,
                port=args.port,
                enable_audio=enable_audio,
                enable_thought_logging=enable_thought_logging
            ))
        except KeyboardInterrupt:
            print("\n🛑 WebSocket server stopped by user")
        except Exception as e:
            logger.error(f"❌ WebSocket server error: {e}")
            print(f"❌ Error: {e}")
        return
    
    else:
        # Default: start CLI conversation
        print("🚀 Starting DAWN Enhanced Conversation System (CLI mode)...")
        print("💡 Use --help for more options")
        start_cli_conversation(enable_audio, enable_thought_logging)

if __name__ == "__main__":
    main() 