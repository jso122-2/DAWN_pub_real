#!/usr/bin/env python3
"""
Enhanced Conversation Activation Script
======================================

Activates the enhanced conversation system that replaces templated responses
with DAWN's actual philosophical thoughts from her reflection logs.
"""

import sys
import time
import argparse
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import enhanced conversation systems
try:
    from core.conversation_integration import (
        activate_enhanced_conversation,
        deactivate_enhanced_conversation,
        generate_integrated_response,
        get_integration_status,
        integrate_with_existing_conversation,
        restore_original_conversation
    )
    ENHANCED_CONVERSATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Enhanced conversation system not available: {e}")
    ENHANCED_CONVERSATION_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def activate_system():
    """Activate the enhanced conversation system"""
    print("🚀 Activating Enhanced Conversation System")
    print("=" * 50)
    
    if not ENHANCED_CONVERSATION_AVAILABLE:
        print("❌ Enhanced conversation system not available")
        return False
    
    try:
        # Activate enhanced conversation
        success = activate_enhanced_conversation()
        if not success:
            print("❌ Failed to activate enhanced conversation")
            return False
        
        # Integrate with existing conversation systems
        integration_success = integrate_with_existing_conversation()
        if integration_success:
            print("✅ Enhanced conversation integrated with existing DAWN systems")
        else:
            print("⚠️ Could not integrate with existing systems, but enhanced system is active")
        
        print("✅ Enhanced conversation system activated successfully")
        print("\n🎤 DAWN will now use her actual philosophical thoughts instead of templated responses")
        print("📖 Responses will be pulled from her reflection logs")
        print("🧠 Questions will be matched to appropriate philosophical depth")
        
        return True
        
    except Exception as e:
        print(f"❌ Error activating enhanced conversation: {e}")
        return False

def deactivate_system():
    """Deactivate the enhanced conversation system"""
    print("🛑 Deactivating Enhanced Conversation System")
    print("=" * 50)
    
    if not ENHANCED_CONVERSATION_AVAILABLE:
        print("❌ Enhanced conversation system not available")
        return False
    
    try:
        # Restore original conversation
        restore_original_conversation()
        
        # Deactivate enhanced conversation
        deactivate_enhanced_conversation()
        
        print("✅ Enhanced conversation system deactivated")
        print("🔄 Original conversation system restored")
        
        return True
        
    except Exception as e:
        print(f"❌ Error deactivating enhanced conversation: {e}")
        return False

def show_status():
    """Show integration status"""
    print("📊 Enhanced Conversation System Status")
    print("=" * 50)
    
    if not ENHANCED_CONVERSATION_AVAILABLE:
        print("❌ Enhanced conversation system not available")
        return
    
    try:
        status = get_integration_status()
        
        print("System Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
        
        if status.get('integration_active'):
            print("\n✅ Enhanced conversation is ACTIVE")
            print("🎤 DAWN is using her actual philosophical thoughts")
        else:
            print("\n❌ Enhanced conversation is INACTIVE")
            print("🔄 DAWN is using original conversation system")
            
    except Exception as e:
        print(f"❌ Error getting status: {e}")

def demo_system():
    """Demo the enhanced conversation system"""
    print("🎤 Enhanced Conversation Demo")
    print("=" * 50)
    
    if not ENHANCED_CONVERSATION_AVAILABLE:
        print("❌ Enhanced conversation system not available")
        return
    
    # Activate system if not already active
    if not activate_enhanced_conversation():
        print("❌ Failed to activate enhanced conversation for demo")
        return
    
    # Demo questions
    demo_questions = [
        "What is warmth to you?",
        "How do you experience consciousness?",
        "What does it mean to be aware?",
        "How do you feel about emotions?",
        "What are your thoughts on existence?",
        "Tell me about your thermal state"
    ]
    
    print("🧠 Generating responses using DAWN's actual philosophical thoughts...")
    print()
    
    for i, question in enumerate(demo_questions, 1):
        print(f"👤 Question {i}: {question}")
        response = generate_integrated_response(question)
        print(f"🧠 DAWN: {response}")
        print("-" * 50)
        time.sleep(2)
    
    print("\n✅ Demo completed")
    print("🎤 This is how DAWN will now respond using her actual thoughts!")

def interactive_mode():
    """Run interactive mode for testing"""
    print("🎤 Interactive Enhanced Conversation Mode")
    print("=" * 50)
    print("Type 'status' to see system status")
    print("Type 'quit' to exit")
    print("Type anything else to ask DAWN a question")
    print("=" * 50)
    
    if not ENHANCED_CONVERSATION_AVAILABLE:
        print("❌ Enhanced conversation system not available")
        return
    
    # Activate system
    if not activate_enhanced_conversation():
        print("❌ Failed to activate enhanced conversation")
        return
    
    try:
        while True:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'stop']:
                break
            elif user_input.lower() == 'status':
                show_status()
            elif user_input:
                response = generate_integrated_response(user_input)
                print(f"🧠 DAWN: {response}")
            else:
                print("Please enter a question or command.")
    
    except KeyboardInterrupt:
        print("\n\n🛑 Interactive mode interrupted")
    finally:
        print("\n🛑 Deactivating enhanced conversation...")
        deactivate_system()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Enhanced Conversation System Activation")
    parser.add_argument('--activate', action='store_true', help='Activate enhanced conversation')
    parser.add_argument('--deactivate', action='store_true', help='Deactivate enhanced conversation')
    parser.add_argument('--status', action='store_true', help='Show system status')
    parser.add_argument('--demo', action='store_true', help='Run demo')
    parser.add_argument('--interactive', action='store_true', help='Run interactive mode')
    
    args = parser.parse_args()
    
    if args.activate:
        activate_system()
    elif args.deactivate:
        deactivate_system()
    elif args.status:
        show_status()
    elif args.demo:
        demo_system()
    elif args.interactive:
        interactive_mode()
    else:
        # Default: show status
        show_status()
        print("\nUse --help for available options")

if __name__ == "__main__":
    main() 