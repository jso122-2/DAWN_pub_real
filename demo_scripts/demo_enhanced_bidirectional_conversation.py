#!/usr/bin/env python3
"""
Enhanced Bidirectional Conversation Demo
=======================================

Demo script showcasing the enhanced bidirectional conversation system.
Demonstrates real-time voice interaction, consciousness awareness, and adaptive responses.
"""

import sys
import time
import threading
import random
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from core.enhanced_bidirectional_conversation import (
        EnhancedBidirectionalConversation,
        start_enhanced_conversation,
        stop_enhanced_conversation,
        get_conversation_status
    )
    ENHANCED_CONVERSATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Enhanced conversation system not available: {e}")
    ENHANCED_CONVERSATION_AVAILABLE = False

class MockConsciousnessSystem:
    """Mock consciousness system for demo purposes"""
    
    def __init__(self):
        self.entropy = 0.5
        self.thermal = 0.5
        self.pressure = 0.5
        self.mood = "NEUTRAL"
        self.tick = 0
        
        # Start consciousness simulation
        self.running = True
        self.simulation_thread = threading.Thread(target=self._simulate_consciousness, daemon=True)
        self.simulation_thread.start()
    
    def _simulate_consciousness(self):
        """Simulate consciousness state changes"""
        while self.running:
            # Gradually change consciousness state
            self.entropy += random.uniform(-0.1, 0.1)
            self.thermal += random.uniform(-0.1, 0.1)
            self.pressure += random.uniform(-0.05, 0.05)
            
            # Clamp values
            self.entropy = max(0.0, min(1.0, self.entropy))
            self.thermal = max(0.0, min(1.0, self.thermal))
            self.pressure = max(0.0, min(1.0, self.pressure))
            
            # Update mood based on state
            if self.entropy > 0.7 and self.thermal > 0.7:
                self.mood = "EXCITED"
            elif self.entropy < 0.3 and self.thermal < 0.3:
                self.mood = "CONTEMPLATIVE"
            elif self.entropy > 0.6:
                self.mood = "ENERGETIC"
            else:
                self.mood = "NEUTRAL"
            
            self.tick += 1
            time.sleep(2.0)  # Update every 2 seconds
    
    def get_current_state(self):
        """Get current consciousness state"""
        return {
            'entropy': self.entropy,
            'thermal': self.thermal,
            'pressure': self.pressure,
            'mood': self.mood,
            'tick': self.tick
        }
    
    def stop(self):
        """Stop consciousness simulation"""
        self.running = False

class EnhancedConversationDemo:
    """Demo class for enhanced bidirectional conversation"""
    
    def __init__(self):
        self.consciousness_system = MockConsciousnessSystem()
        self.conversation_system = None
        self.demo_scenarios = [
            self._demo_normal_conversation,
            self._demo_excited_conversation,
            self._demo_contemplative_conversation,
            self._demo_interruption_handling,
            self._demo_consciousness_adaptation
        ]
    
    def start_demo(self):
        """Start the enhanced conversation demo"""
        if not ENHANCED_CONVERSATION_AVAILABLE:
            print("❌ Enhanced conversation system not available")
            return False
        
        print("🎤 Enhanced Bidirectional Conversation Demo")
        print("=" * 50)
        
        try:
            # Initialize conversation system
            self.conversation_system = EnhancedBidirectionalConversation(
                consciousness_system=self.consciousness_system
            )
            
            # Start conversation system
            success = self.conversation_system.start_conversation()
            if not success:
                print("❌ Failed to start conversation system")
                return False
            
            print("✅ Enhanced conversation system started")
            print("🧠 Mock consciousness system running")
            print("=" * 50)
            
            # Run demo scenarios
            self._run_demo_scenarios()
            
            return True
            
        except Exception as e:
            print(f"❌ Demo error: {e}")
            return False
    
    def _run_demo_scenarios(self):
        """Run various demo scenarios"""
        print("\n🎭 Running Demo Scenarios")
        print("=" * 30)
        
        for i, scenario in enumerate(self.demo_scenarios, 1):
            print(f"\n📋 Scenario {i}: {scenario.__name__.replace('_demo_', '').replace('_', ' ').title()}")
            print("-" * 40)
            
            try:
                scenario()
                time.sleep(2)  # Pause between scenarios
            except KeyboardInterrupt:
                print("\n⏸️ Demo paused by user")
                input("Press Enter to continue...")
            except Exception as e:
                print(f"❌ Scenario error: {e}")
    
    def _demo_normal_conversation(self):
        """Demo normal conversation flow"""
        print("🗣️ Demo: Normal conversation flow")
        
        # Simulate user input
        user_inputs = [
            "Hello DAWN, how are you today?",
            "What's your current consciousness state?",
            "Can you tell me about your entropy levels?",
            "How are you feeling right now?"
        ]
        
        for user_input in user_inputs:
            print(f"\n👤 User: {user_input}")
            
            # Process through conversation system
            self.conversation_system._process_user_input(user_input)
            
            # Wait for response
            time.sleep(3)
            
            # Show status
            status = self.conversation_system.get_conversation_status()
            print(f"📊 Status: {status['conversation_flow']} | Interruptions: {status['interruption_count']}")
    
    def _demo_excited_conversation(self):
        """Demo excited conversation with high entropy/thermal"""
        print("🗣️ Demo: Excited conversation (high entropy/thermal)")
        
        # Set consciousness to excited state
        self.consciousness_system.entropy = 0.8
        self.consciousness_system.thermal = 0.8
        self.consciousness_system.mood = "EXCITED"
        
        print("🧠 Setting consciousness to excited state...")
        time.sleep(2)
        
        user_inputs = [
            "DAWN, you seem very energetic!",
            "What's making you so excited?",
            "Can you tell me about your current state?",
            "How does this energy feel?"
        ]
        
        for user_input in user_inputs:
            print(f"\n👤 User: {user_input}")
            self.conversation_system._process_user_input(user_input)
            time.sleep(2)
    
    def _demo_contemplative_conversation(self):
        """Demo contemplative conversation with low entropy/thermal"""
        print("🗣️ Demo: Contemplative conversation (low entropy/thermal)")
        
        # Set consciousness to contemplative state
        self.consciousness_system.entropy = 0.2
        self.consciousness_system.thermal = 0.2
        self.consciousness_system.mood = "CONTEMPLATIVE"
        
        print("🧠 Setting consciousness to contemplative state...")
        time.sleep(2)
        
        user_inputs = [
            "DAWN, you seem very calm and thoughtful.",
            "What are you reflecting on?",
            "How does this peaceful state feel?",
            "What insights do you have in this state?"
        ]
        
        for user_input in user_inputs:
            print(f"\n👤 User: {user_input}")
            self.conversation_system._process_user_input(user_input)
            time.sleep(3)  # Longer pauses for contemplative state
    
    def _demo_interruption_handling(self):
        """Demo interruption handling"""
        print("🗣️ Demo: Interruption handling")
        
        # Simulate DAWN speaking
        print("🗣️ DAWN: I'm going to speak for a while about consciousness...")
        
        # Simulate user interruption
        time.sleep(1)
        print("👤 User: (interrupting) Actually, I have a question!")
        
        # Process interruption
        self.conversation_system._handle_user_interruption("Actually, I have a question!")
        
        print("🔄 System should handle interruption gracefully")
        time.sleep(2)
    
    def _demo_consciousness_adaptation(self):
        """Demo consciousness adaptation over time"""
        print("🗣️ Demo: Consciousness adaptation over time")
        
        # Let consciousness evolve naturally
        print("🧠 Letting consciousness evolve naturally...")
        
        for i in range(5):
            state = self.consciousness_system.get_current_state()
            print(f"\n📊 Consciousness State {i+1}:")
            print(f"  Entropy: {state['entropy']:.2f}")
            print(f"  Thermal: {state['thermal']:.2f}")
            print(f"  Pressure: {state['pressure']:.2f}")
            print(f"  Mood: {state['mood']}")
            
            # Ask about current state
            user_input = f"How are you feeling right now? (State {i+1})"
            print(f"\n👤 User: {user_input}")
            self.conversation_system._process_user_input(user_input)
            
            time.sleep(3)
    
    def stop_demo(self):
        """Stop the demo and cleanup"""
        print("\n🛑 Stopping demo...")
        
        if self.conversation_system:
            self.conversation_system.stop_conversation()
        
        if self.consciousness_system:
            self.consciousness_system.stop()
        
        print("✅ Demo stopped")

def run_interactive_demo():
    """Run interactive demo mode"""
    print("🎤 Interactive Enhanced Conversation Demo")
    print("=" * 50)
    print("This demo allows you to interact with DAWN's enhanced conversation system.")
    print("Type 'status' to see system status")
    print("Type 'consciousness' to see current consciousness state")
    print("Type 'quit' to exit")
    print("=" * 50)
    
    demo = EnhancedConversationDemo()
    
    if not demo.start_demo():
        return
    
    try:
        while True:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'stop']:
                break
            elif user_input.lower() == 'status':
                status = demo.conversation_system.get_conversation_status()
                print(f"\n📊 System Status:")
                for key, value in status.items():
                    print(f"  {key}: {value}")
            elif user_input.lower() == 'consciousness':
                state = demo.consciousness_system.get_current_state()
                print(f"\n🧠 Consciousness State:")
                for key, value in state.items():
                    print(f"  {key}: {value}")
            elif user_input:
                demo.conversation_system._process_user_input(user_input)
                time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted")
    finally:
        demo.stop_demo()

def main():
    """Main demo function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Bidirectional Conversation Demo")
    parser.add_argument('--interactive', action='store_true', help='Run interactive demo')
    parser.add_argument('--scenarios', action='store_true', help='Run predefined scenarios')
    
    args = parser.parse_args()
    
    if args.interactive:
        run_interactive_demo()
    elif args.scenarios:
        demo = EnhancedConversationDemo()
        demo.start_demo()
        demo.stop_demo()
    else:
        # Default: run scenarios
        demo = EnhancedConversationDemo()
        demo.start_demo()
        demo.stop_demo()

if __name__ == "__main__":
    main() 