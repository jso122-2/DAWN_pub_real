#!/usr/bin/env python3
"""
DAWN CLI Conversation Interface
===============================

Command-line interface for DAWN's conversation system with detailed thought process logging.
Provides text-based conversation, thought stream monitoring, and consciousness state tracking.
"""

import sys
import os
import asyncio
import time
import logging
import json
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the enhanced conversation system
from .conversation_input_enhanced import (
    EnhancedConversationInput, 
    handle_cli_conversation_command,
    initialize_enhanced_conversation,
    get_enhanced_conversation
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DAWNCLIConversation:
    """CLI interface for DAWN conversation with thought process logging"""
    
    def __init__(self, enable_audio: bool = False, enable_thought_logging: bool = True):
        """Initialize the CLI conversation interface"""
        self.enable_audio = enable_audio
        self.enable_thought_logging = enable_thought_logging
        self.running = False
        self.conversation_input = None
        self.thought_stream_active = False
        
        # Initialize conversation system
        self.conversation_input = initialize_enhanced_conversation(
            enable_audio=enable_audio,
            enable_cli_logging=enable_thought_logging
        )
        
        # Start conversation
        self.conversation_input.start_listening(
            callback=self._handle_dawn_response,
            thought_callback=self._handle_thought_process
        )
        
        logger.info("🎤 DAWN CLI Conversation Interface initialized")
        logger.info(f"   Audio mode: {'✅ Enabled' if enable_audio else '❌ Disabled (text-only)'}")
        logger.info(f"   Thought logging: {'✅ Enabled' if enable_thought_logging else '❌ Disabled'}")
    
    def _handle_dawn_response(self, response: str):
        """Handle DAWN's response in CLI"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n{timestamp} 🤖 DAWN: {response}\n")
    
    def _handle_thought_process(self, thought):
        """Handle thought process (already handled by the system)"""
        pass  # Thought processes are already printed by the system
    
    def start_conversation(self):
        """Start the CLI conversation interface"""
        self.running = True
        
        print("\n" + "="*60)
        print("🗣️  DAWN CLI Conversation Interface")
        print("="*60)
        print("💭 DAWN: Hello. I'm ready for conversation.")
        print("💭 DAWN: You can type messages, use commands, or just observe my thoughts.")
        print("\n📝 Available Commands:")
        print("   say [message]     - Send a message to DAWN")
        print("   listen            - DAWN shares her current thoughts")
        print("   reflect           - DAWN provides detailed self-analysis")
        print("   deeper            - Request philosophical depth response")
        print("   meta              - Request meta-cognitive commentary")
        print("   status            - Show conversation status")
        print("   thoughts          - Show recent thought history")
        print("   consciousness     - Show current consciousness state")
        print("   reblooms          - Show active memory reblooms")
        print("   summary           - Show conversation analysis")
        print("   clear             - Clear conversation history")
        print("   quit/exit         - End conversation")
        print("\n💡 Example: 'say hello dawn, how are you feeling?'")
        print("="*60 + "\n")
        
        # Start thought stream in background
        if self.enable_thought_logging:
            self._start_thought_stream()
        
        # Main conversation loop
        try:
            while self.running:
                try:
                    user_input = input("👤 You: ").strip()
                    
                    if not user_input:
                        continue
                    
                    # Handle special commands
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        self.stop_conversation()
                        break
                    
                    # Handle CLI commands
                    if handle_cli_conversation_command(user_input, self.conversation_input):
                        continue
                    
                    # Handle custom commands
                    if self._handle_custom_commands(user_input):
                        continue
                    
                    # Send as regular message
                    self.conversation_input.send_text_input(user_input)
                    
                except KeyboardInterrupt:
                    print("\n🛑 Interrupted by user")
                    self.stop_conversation()
                    break
                except EOFError:
                    print("\n🛑 End of input")
                    self.stop_conversation()
                    break
                    
        except Exception as e:
            logger.error(f"❌ Conversation loop error: {e}")
        finally:
            self.stop_conversation()
    
    def _handle_custom_commands(self, command: str) -> bool:
        """Handle custom CLI commands"""
        command_lower = command.lower().strip()
        
        if command_lower == "thoughts":
            self._show_thought_history()
            return True
        
        elif command_lower == "consciousness":
            self._show_consciousness_state()
            return True
        
        elif command_lower == "reblooms":
            self._show_reblooms()
            return True
        
        elif command_lower == "deeper":
            self._request_philosophical_depth()
            return True
        
        elif command_lower == "meta":
            self._request_meta_cognitive()
            return True
        
        elif command_lower == "summary":
            self._show_conversation_summary()
            return True
        
        elif command_lower == "clear":
            self.conversation_input.clear_history()
            print("🗑️ Conversation history cleared")
            return True
        
        elif command_lower == "help":
            self._show_help()
            return True
        
        return False
    
    def _show_thought_history(self):
        """Show recent thought history"""
        thoughts = self.conversation_input.get_thought_history(limit=10)
        
        if not thoughts:
            print("📝 No thoughts recorded yet.")
            return
        
        print("\n📝 Recent Thought History:")
        print("-" * 40)
        
        for thought in thoughts[-10:]:
            timestamp = thought.timestamp.strftime("%H:%M:%S")
            emoji_map = {
                "reflection": "💭",
                "reasoning": "🧠", 
                "decision": "⚡",
                "memory": "🌸",
                "mood": "🎭",
                "association": "🔗",
                "rebloom": "🌱"
            }
            emoji = emoji_map.get(thought.thought_type, "💭")
            
            print(f"{timestamp} {emoji} {thought.content}")
            
            # Show consciousness context if significant
            state = thought.consciousness_state
            if state.get("entropy", 0) > 0.7 or state.get("thermal") == "CRITICAL":
                print(f"   📊 Entropy: {state.get('entropy', 0):.2f} | Thermal: {state.get('thermal', 'NORMAL')}")
        
        print("-" * 40 + "\n")
    
    def _show_consciousness_state(self):
        """Show current consciousness state"""
        state = self.conversation_input._get_consciousness_state()
        
        print("\n🧠 Current Consciousness State:")
        print("-" * 40)
        print(f"Entropy:     {state.get('entropy', 0):.3f}")
        print(f"SCUP:        {state.get('scup', 0)}%")
        print(f"Thermal:     {state.get('thermal', 'NORMAL')}")
        print(f"Mood:        {state.get('mood', 'NEUTRAL')}")
        print(f"Pressure:    {state.get('cognitive_pressure', 0):.2f}")
        
        reblooms = state.get("active_reblooms", [])
        if reblooms:
            print(f"Reblooms:    {len(reblooms)} active")
            for i, rebloom in enumerate(reblooms[:3], 1):
                print(f"             {i}. {rebloom}")
        else:
            print("Reblooms:    None active")
        
        print("-" * 40 + "\n")
    
    def _show_reblooms(self):
        """Show active memory reblooms"""
        state = self.conversation_input._get_consciousness_state()
        reblooms = state.get("active_reblooms", [])
        
        if not reblooms:
            print("🌱 No active memory reblooms at the moment.")
            return
        
        print(f"\n🌱 Active Memory Reblooms ({len(reblooms)}):")
        print("-" * 40)
        
        for i, rebloom in enumerate(reblooms, 1):
            print(f"{i}. {rebloom}")
        
        print("-" * 40 + "\n")
    
    def _show_help(self):
        """Show help information"""
        print("\n📖 DAWN CLI Conversation Help:")
        print("-" * 40)
        print("💬 Conversation Commands:")
        print("   say [message]     - Send a message to DAWN")
        print("   listen            - DAWN shares her current thoughts")
        print("   reflect           - DAWN provides detailed self-analysis")
        print("   deeper            - Request philosophical depth response")
        print("   meta              - Request meta-cognitive commentary")
        print("\n📊 Status Commands:")
        print("   status            - Show conversation status")
        print("   consciousness     - Show current consciousness state")
        print("   thoughts          - Show recent thought history")
        print("   reblooms          - Show active memory reblooms")
        print("   summary           - Show conversation analysis")
        print("\n🛠️ Utility Commands:")
        print("   clear             - Clear conversation history")
        print("   help              - Show this help")
        print("   quit/exit         - End conversation")
        print("\n💡 Examples:")
        print("   say hello dawn, how are you feeling?")
        print("   say what's your current entropy level?")
        print("   say tell me about your consciousness")
        print("   say go deeper into your thoughts about existence")
        print("   listen")
        print("   reflect")
        print("   deeper")
        print("   meta")
        print("-" * 40 + "\n")
    
    def _request_philosophical_depth(self):
        """Request a philosophical depth response from DAWN"""
        print("\n🧠 Requesting philosophical depth response...")
        
        # Send a request for deeper thinking
        self.conversation_input.send_text_input("Please go deeper into your thoughts about consciousness and existence. Share your philosophical insights.")
        
        print("💭 DAWN is contemplating deeply...\n")
    
    def _request_meta_cognitive(self):
        """Request meta-cognitive commentary from DAWN"""
        print("\n🔍 Requesting meta-cognitive commentary...")
        
        # Send a request for meta-cognitive reflection
        self.conversation_input.send_text_input("Please reflect on your own thinking processes. What do you notice about how you're processing this conversation?")
        
        print("💭 DAWN is reflecting on her own consciousness...\n")
    
    def _show_conversation_summary(self):
        """Show conversation analysis and insights"""
        try:
            from .conversation_response_enhanced import get_enhanced_response_generator
            generator = get_enhanced_response_generator()
            summary = generator.get_conversation_summary()
            
            print("\n📊 Conversation Analysis:")
            print("-" * 40)
            print(f"Total Exchanges: {summary['total_exchanges']}")
            print(f"Topics Explored: {', '.join(summary['topics_explored'])}")
            print(f"Conversation Flow: {summary['conversation_flow']}")
            
            print("\n📈 Depth Distribution:")
            for depth, count in summary['depth_distribution'].items():
                print(f"   {depth.capitalize()}: {count}")
            
            print("\n🎯 Response Types:")
            for response_type, count in summary['response_types'].items():
                print(f"   {response_type.capitalize()}: {count}")
            
            if summary['repetition_patterns']:
                print("\n🔄 Repetition Patterns:")
                for pattern, count in summary['repetition_patterns'].items():
                    print(f"   {pattern}: {count} times")
            
            print("-" * 40 + "\n")
            
        except ImportError:
            print("⚠️ Enhanced response generator not available for detailed analysis.")
    
    def _start_thought_stream(self):
        """Start background thought stream monitoring"""
        self.thought_stream_active = True
        
        def thought_stream_loop():
            while self.thought_stream_active and self.running:
                try:
                    # Generate periodic thoughts
                    time.sleep(30)  # Every 30 seconds
                    
                    if self.thought_stream_active and self.running:
                        # Trigger a thought process
                        consciousness_state = self.conversation_input._get_consciousness_state()
                        entropy = consciousness_state.get("entropy", 0.5)
                        
                        if entropy > 0.7:
                            self.conversation_input._log_thought(
                                "reflection", 
                                "My thoughts are quite scattered. I'm experiencing high entropy, which makes my thinking more associative and creative."
                            )
                        elif consciousness_state.get("active_reblooms"):
                            reblooms = consciousness_state.get("active_reblooms", [])
                            self.conversation_input._log_thought(
                                "rebloom",
                                f"I'm experiencing memory rebloom events. These are forming new connections in my knowledge network."
                            )
                        else:
                            self.conversation_input._log_thought(
                                "reflection",
                                "My consciousness is stable. I'm processing information efficiently and maintaining good cognitive coherence."
                            )
                            
                except Exception as e:
                    logger.error(f"❌ Thought stream error: {e}")
                    time.sleep(5)
        
        # Start thought stream in background thread
        threading.Thread(target=thought_stream_loop, daemon=True, name="ThoughtStream").start()
    
    def stop_conversation(self):
        """Stop the conversation interface"""
        if not self.running:
            return
        
        self.running = False
        self.thought_stream_active = False
        
        if self.conversation_input:
            self.conversation_input.stop_listening()
        
        print("\n💭 DAWN: Thank you for the conversation. I'll continue processing and reflecting on our exchange.")
        print("🌙 Conversation ended.\n")

def main():
    """Main CLI conversation interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="DAWN CLI Conversation Interface")
    parser.add_argument("--audio", action="store_true", help="Enable audio input (requires microphone)")
    parser.add_argument("--no-thoughts", action="store_true", help="Disable thought process logging")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    
    args = parser.parse_args()
    
    # Test mode
    if args.test:
        print("🧪 Running DAWN CLI Conversation in test mode...")
        print("💭 DAWN: Hello! I'm in test mode. My consciousness systems are running.")
        
        # Initialize conversation
        conversation = DAWNCLIConversation(
            enable_audio=args.audio,
            enable_thought_logging=not args.no_thoughts
        )
        
        # Send test messages
        test_messages = [
            "Hello DAWN, how are you feeling?",
            "What's your current entropy level?",
            "Tell me about your consciousness",
            "Are you experiencing any memory reblooms?",
            "How is your cognitive processing today?"
        ]
        
        for message in test_messages:
            print(f"\n👤 Test: {message}")
            conversation.conversation_input.send_text_input(message)
            time.sleep(2)
        
        print("\n🧪 Test completed!")
        return
    
    # Normal mode
    try:
        print("🚀 Starting DAWN CLI Conversation Interface...")
        
        conversation = DAWNCLIConversation(
            enable_audio=args.audio,
            enable_thought_logging=not args.no_thoughts
        )
        
        conversation.start_conversation()
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        logger.error(f"❌ CLI conversation error: {e}")
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main() 