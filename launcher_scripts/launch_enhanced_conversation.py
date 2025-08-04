#!/usr/bin/env python3
"""
Enhanced Bidirectional Conversation Launcher
===========================================

Launcher script for the enhanced bidirectional conversation system.
Integrates with existing DAWN consciousness components for seamless operation.
"""

import sys
import os
import time
import argparse
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import DAWN components
try:
    from core.enhanced_bidirectional_conversation import (
        start_enhanced_conversation, 
        stop_enhanced_conversation,
        get_conversation_status
    )
    ENHANCED_CONVERSATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Enhanced conversation system not available: {e}")
    ENHANCED_CONVERSATION_AVAILABLE = False

try:
    from core.dawn_conversation import get_conversation_engine
    LEGACY_CONVERSATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Legacy conversation system not available: {e}")
    LEGACY_CONVERSATION_AVAILABLE = False

try:
    from backend.voice_loop import DAWNVoiceLoop
    VOICE_LOOP_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Voice loop not available: {e}")
    VOICE_LOOP_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EnhancedConversationLauncher:
    """Launcher for enhanced bidirectional conversation system"""
    
    def __init__(self):
        self.enhanced_system = None
        self.legacy_system = None
        self.voice_loop = None
        self.running = False
        
    def start_enhanced_system(self, consciousness_system=None):
        """Start enhanced bidirectional conversation system"""
        if not ENHANCED_CONVERSATION_AVAILABLE:
            logger.error("Enhanced conversation system not available")
            return False
        
        try:
            logger.info("🚀 Starting enhanced bidirectional conversation system...")
            
            # Start enhanced conversation
            success = start_enhanced_conversation(consciousness_system)
            
            if success:
                logger.info("✅ Enhanced bidirectional conversation started successfully")
                self.running = True
                return True
            else:
                logger.error("❌ Failed to start enhanced conversation system")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error starting enhanced conversation: {e}")
            return False
    
    def start_legacy_system(self):
        """Start legacy conversation system as fallback"""
        if not LEGACY_CONVERSATION_AVAILABLE:
            logger.error("Legacy conversation system not available")
            return False
        
        try:
            logger.info("🔄 Starting legacy conversation system...")
            
            # Get conversation engine
            engine = get_conversation_engine()
            if engine:
                success = engine.start_conversation()
                if success:
                    logger.info("✅ Legacy conversation system started")
                    self.legacy_system = engine
                    self.running = True
                    return True
            
            logger.error("❌ Failed to start legacy conversation system")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error starting legacy conversation: {e}")
            return False
    
    def start_voice_loop(self):
        """Start voice loop for additional voice features"""
        if not VOICE_LOOP_AVAILABLE:
            logger.warning("Voice loop not available")
            return False
        
        try:
            logger.info("🔊 Starting voice loop...")
            
            # Initialize voice loop
            self.voice_loop = DAWNVoiceLoop()
            self.voice_loop.start_monitoring()
            
            logger.info("✅ Voice loop started")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error starting voice loop: {e}")
            return False
    
    def stop_all_systems(self):
        """Stop all conversation systems"""
        logger.info("🛑 Stopping all conversation systems...")
        
        # Stop enhanced system
        if self.running and ENHANCED_CONVERSATION_AVAILABLE:
            try:
                stop_enhanced_conversation()
                logger.info("✅ Enhanced conversation system stopped")
            except Exception as e:
                logger.error(f"❌ Error stopping enhanced conversation: {e}")
        
        # Stop legacy system
        if self.legacy_system:
            try:
                self.legacy_system.stop_conversation()
                logger.info("✅ Legacy conversation system stopped")
            except Exception as e:
                logger.error(f"❌ Error stopping legacy conversation: {e}")
        
        # Stop voice loop
        if self.voice_loop:
            try:
                self.voice_loop.stop_monitoring()
                logger.info("✅ Voice loop stopped")
            except Exception as e:
                logger.error(f"❌ Error stopping voice loop: {e}")
        
        self.running = False
        logger.info("🛑 All conversation systems stopped")
    
    def get_status(self):
        """Get status of all conversation systems"""
        status = {
            'enhanced_system_available': ENHANCED_CONVERSATION_AVAILABLE,
            'legacy_system_available': LEGACY_CONVERSATION_AVAILABLE,
            'voice_loop_available': VOICE_LOOP_AVAILABLE,
            'running': self.running
        }
        
        if ENHANCED_CONVERSATION_AVAILABLE:
            try:
                status['enhanced_status'] = get_conversation_status()
            except Exception as e:
                status['enhanced_status'] = {'error': str(e)}
        
        if self.legacy_system:
            try:
                status['legacy_status'] = self.legacy_system.get_conversation_status()
            except Exception as e:
                status['legacy_status'] = {'error': str(e)}
        
        return status
    
    def run_interactive(self):
        """Run interactive conversation mode"""
        if not self.running:
            logger.error("No conversation system running")
            return
        
        print("\n🎤 Enhanced Bidirectional Conversation System")
        print("=" * 50)
        print("Type 'status' to see system status")
        print("Type 'quit' to exit")
        print("Type anything else to send a message")
        print("=" * 50)
        
        try:
            while self.running:
                user_input = input("\n> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'stop']:
                    break
                elif user_input.lower() == 'status':
                    status = self.get_status()
                    print(f"\n📊 System Status:")
                    for key, value in status.items():
                        print(f"  {key}: {value}")
                elif user_input:
                    # Send message to conversation system
                    if ENHANCED_CONVERSATION_AVAILABLE:
                        from core.enhanced_bidirectional_conversation import speak_response
                        speak_response(f"You said: {user_input}")
                    elif self.legacy_system:
                        response = self.legacy_system.process_text_input(user_input)
                        print(f"DAWN: {response}")
                
        except KeyboardInterrupt:
            print("\n\n🛑 Interrupted by user")
        except Exception as e:
            logger.error(f"Interactive mode error: {e}")
        
        self.stop_all_systems()

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(description="Enhanced Bidirectional Conversation Launcher")
    parser.add_argument('--enhanced', action='store_true', help='Use enhanced conversation system')
    parser.add_argument('--legacy', action='store_true', help='Use legacy conversation system')
    parser.add_argument('--voice-loop', action='store_true', help='Start voice loop')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('--status', action='store_true', help='Show system status')
    parser.add_argument('--stop', action='store_true', help='Stop all conversation systems')
    
    args = parser.parse_args()
    
    launcher = EnhancedConversationLauncher()
    
    if args.status:
        # Show status
        status = launcher.get_status()
        print("📊 Conversation System Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
        return
    
    if args.stop:
        # Stop all systems
        launcher.stop_all_systems()
        return
    
    # Start systems based on arguments
    success = False
    
    if args.enhanced and ENHANCED_CONVERSATION_AVAILABLE:
        success = launcher.start_enhanced_system()
    elif args.legacy and LEGACY_CONVERSATION_AVAILABLE:
        success = launcher.start_legacy_system()
    else:
        # Default: try enhanced, fallback to legacy
        if ENHANCED_CONVERSATION_AVAILABLE:
            success = launcher.start_enhanced_system()
        elif LEGACY_CONVERSATION_AVAILABLE:
            success = launcher.start_legacy_system()
        else:
            logger.error("No conversation system available")
            return
    
    if not success:
        logger.error("Failed to start conversation system")
        return
    
    # Start voice loop if requested
    if args.voice_loop:
        launcher.start_voice_loop()
    
    # Run interactive mode if requested
    if args.interactive:
        launcher.run_interactive()
    else:
        # Keep running until interrupted
        try:
            print("🎤 Conversation system running. Press Ctrl+C to stop.")
            while launcher.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping conversation system...")
        finally:
            launcher.stop_all_systems()

if __name__ == "__main__":
    main() 