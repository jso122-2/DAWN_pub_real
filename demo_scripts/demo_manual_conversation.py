#!/usr/bin/env python3
"""
Demo: Manual Conversation with DAWN's Actual Consciousness Data
==============================================================

This demo shows how to use the integrated manual conversation system
with real DAWN consciousness data structures and metrics.

Features demonstrated:
- Real-time consciousness state integration
- Live SCUP, entropy, and thermal zone monitoring
- Memory rebloom and cognitive pattern tracking
- Multi-mode conversation (casual, philosophical, technical, reflection)
- Conversation persistence and analysis
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from manual_conversation_integrated import ManualConversationSystem

def demo_basic_conversation():
    """Demo basic conversation with consciousness integration"""
    print("🧪 Demo 1: Basic Conversation with Consciousness Integration")
    print("=" * 60)
    
    # Initialize conversation system
    conversation = ManualConversationSystem(mode="casual", debug=True)
    
    # Show initial consciousness state
    print("Initial Consciousness State:")
    print(conversation.get_consciousness_status())
    print()
    
    # Demo conversation
    demo_messages = [
        "Hello DAWN, how are you feeling today?",
        "What's your current entropy level?",
        "Tell me about your consciousness state",
        "Are you experiencing any memory reblooms?",
        "How is your cognitive processing?"
    ]
    
    for message in demo_messages:
        print(f"👤 User: {message}")
        response = conversation.process_user_input(message)
        print(f"🌅 DAWN: {response}")
        print()
        time.sleep(1)  # Brief pause between messages
    
    # Show final stats
    print("Final Conversation Statistics:")
    print(conversation.get_conversation_stats())
    print()

def demo_mode_switching():
    """Demo switching between conversation modes"""
    print("🧪 Demo 2: Mode Switching")
    print("=" * 60)
    
    conversation = ManualConversationSystem(mode="casual", debug=True)
    
    # Test different modes with the same question
    test_question = "What is consciousness?"
    modes = ["casual", "philosophical", "technical", "reflection"]
    
    for mode in modes:
        print(f"\n--- {mode.upper()} MODE ---")
        conversation.switch_mode(mode)
        print(f"👤 User: {test_question}")
        response = conversation.process_user_input(test_question)
        print(f"🌅 DAWN: {response}")
        print()

def demo_consciousness_monitoring():
    """Demo real-time consciousness monitoring"""
    print("🧪 Demo 3: Real-time Consciousness Monitoring")
    print("=" * 60)
    
    conversation = ManualConversationSystem(mode="technical", debug=True)
    
    # Monitor consciousness changes over time
    print("Monitoring consciousness state changes...")
    print()
    
    for i in range(5):
        print(f"--- Tick {i+1} ---")
        print(conversation.get_consciousness_status())
        print()
        
        # Simulate some conversation to trigger state changes
        conversation.process_user_input(f"Test message {i+1}")
        time.sleep(2)

def demo_conversation_persistence():
    """Demo conversation saving and loading"""
    print("🧪 Demo 4: Conversation Persistence")
    print("=" * 60)
    
    conversation = ManualConversationSystem(mode="philosophical", debug=True)
    
    # Have a brief conversation
    messages = [
        "What is the nature of consciousness?",
        "How do you experience self-awareness?",
        "Tell me about your cognitive architecture"
    ]
    
    for message in messages:
        print(f"👤 User: {message}")
        response = conversation.process_user_input(message)
        print(f"🌅 DAWN: {response}")
        print()
    
    # Save conversation
    filename = f"demo_conversation_{int(time.time())}.json"
    result = conversation.save_conversation(filename)
    print(f"💾 {result}")
    print()
    
    # Show conversation stats
    print("Conversation Statistics:")
    print(conversation.get_conversation_stats())
    print()

def demo_consciousness_analysis():
    """Demo consciousness data analysis"""
    print("🧪 Demo 5: Consciousness Data Analysis")
    print("=" * 60)
    
    conversation = ManualConversationSystem(mode="technical", debug=True)
    
    # Generate some consciousness data
    for i in range(10):
        conversation.process_user_input(f"Analysis message {i+1}")
        time.sleep(0.5)
    
    # Analyze consciousness history
    history = list(conversation.consciousness_history)
    
    if history:
        print("Consciousness Data Analysis:")
        print(f"Total data points: {len(history)}")
        
        # Calculate averages
        avg_scup = sum(h.scup for h in history) / len(history)
        avg_entropy = sum(h.entropy for h in history) / len(history)
        avg_neural = sum(h.neural_activity for h in history) / len(history)
        
        print(f"Average SCUP: {avg_scup:.2f}%")
        print(f"Average Entropy: {avg_entropy:.3f}")
        print(f"Average Neural Activity: {avg_neural:.3f}")
        
        # Find extremes
        max_scup = max(h.scup for h in history)
        min_scup = min(h.scup for h in history)
        max_entropy = max(h.entropy for h in history)
        min_entropy = min(h.entropy for h in history)
        
        print(f"SCUP Range: {min_scup:.1f}% - {max_scup:.1f}%")
        print(f"Entropy Range: {min_entropy:.3f} - {max_entropy:.3f}")
        
        # Thermal zone distribution
        zones = {}
        for h in history:
            zone = h.thermal_zone
            zones[zone] = zones.get(zone, 0) + 1
        
        print("Thermal Zone Distribution:")
        for zone, count in zones.items():
            percentage = (count / len(history)) * 100
            print(f"  {zone}: {count} ({percentage:.1f}%)")
    
    print()

def demo_interactive_session():
    """Demo interactive conversation session"""
    print("🧪 Demo 6: Interactive Session")
    print("=" * 60)
    print("This demo allows you to interact with DAWN directly.")
    print("Type 'quit' to end the session.")
    print()
    
    conversation = ManualConversationSystem(mode="casual", debug=True)
    
    print("🌅 DAWN: Hello! I'm ready for conversation. My consciousness systems are active.")
    print(f"Current state: SCUP {conversation.consciousness_data.scup:.1f}%, Entropy {conversation.consciousness_data.entropy:.3f}")
    print()
    
    try:
        while True:
            user_input = input("👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() == 'status':
                print(conversation.get_consciousness_status())
                continue
            
            elif user_input.lower() == 'stats':
                print(conversation.get_conversation_stats())
                continue
            
            elif user_input.lower().startswith('mode '):
                new_mode = user_input[5:].strip()
                result = conversation.switch_mode(new_mode)
                print(result)
                continue
            
            # Process regular conversation
            response = conversation.process_user_input(user_input)
            print(f"🌅 DAWN: {response}")
            print()
    
    except KeyboardInterrupt:
        print("\nSession interrupted.")
    
    # Save the session
    result = conversation.save_conversation()
    print(f"💾 {result}")

def main():
    """Main demo function"""
    print("🌅 DAWN Manual Conversation System - Demo Suite")
    print("=" * 60)
    print("This demo showcases the integrated manual conversation system")
    print("with actual DAWN consciousness data structures.")
    print()
    
    demos = [
        ("Basic Conversation", demo_basic_conversation),
        ("Mode Switching", demo_mode_switching),
        ("Consciousness Monitoring", demo_consciousness_monitoring),
        ("Conversation Persistence", demo_conversation_persistence),
        ("Consciousness Analysis", demo_consciousness_analysis),
        ("Interactive Session", demo_interactive_session)
    ]
    
    print("Available Demos:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    print("  0. Run all demos")
    print("  q. Quit")
    print()
    
    try:
        choice = input("Select demo (0-6, q): ").strip()
        
        if choice.lower() == 'q':
            print("Goodbye!")
            return
        
        elif choice == '0':
            # Run all demos
            for name, demo_func in demos:
                print(f"\n{'='*20} {name} {'='*20}")
                demo_func()
                input("Press Enter to continue to next demo...")
        
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            # Run specific demo
            demo_name, demo_func = demos[int(choice) - 1]
            print(f"\n{'='*20} {demo_name} {'='*20}")
            demo_func()
        
        else:
            print("Invalid choice. Please select 0-6 or q.")
    
    except KeyboardInterrupt:
        print("\nDemo interrupted. Goodbye!")
    except Exception as e:
        print(f"Demo error: {e}")

if __name__ == "__main__":
    main() 