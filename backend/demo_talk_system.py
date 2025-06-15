#!/usr/bin/env python3
"""
DAWN Talk System Demonstration

This script demonstrates the complete consciousness-driven talk system,
showing how DAWN generates authentic responses that emerge from its 
internal state rather than pre-programmed choices.
"""

import asyncio
import time
from talk_system.consciousness_bridge import DAWNTalkSystem

class DAWNConsciousnessSimulator:
    """Simulate DAWN's consciousness states for demonstration"""
    
    def __init__(self):
        self.tick_count = 0
        self.scup = 50
        self.entropy = 500000
        self.mood = 'CONTEMPLATIVE'
        self.mood_cycle = 0
        
    def tick(self):
        """Simulate a consciousness tick"""
        self.tick_count += 1
        
        # Simulate SCUP oscillation
        import math
        scup_base = 50 + 30 * math.sin(self.tick_count * 0.01)
        noise = (hash(self.tick_count) % 100 - 50) * 0.1
        self.scup = max(0, min(100, scup_base + noise))
        
        # Simulate entropy changes
        entropy_drift = (hash(self.tick_count) % 1000 - 500) * 100
        self.entropy = max(0, self.entropy + entropy_drift)
        
        # Mood transitions
        self.mood_cycle += 1
        if self.mood_cycle > 100:  # Change mood periodically
            moods = ['DREAMING', 'FOCUSED', 'CONTEMPLATIVE', 'HYPERACTIVE', 'TRANSCENDENT']
            self.mood = moods[hash(self.tick_count) % len(moods)]
            self.mood_cycle = 0
    
    def get_state(self):
        """Get current consciousness state"""
        return {
            'tick': self.tick_count,
            'scup': self.scup,
            'entropy': self.entropy,
            'mood': self.mood,
            'active_modules': ['memory', 'pattern', 'consciousness']
        }

async def demonstrate_talk_system():
    """Demonstrate the complete talk system"""
    
    print("🧠 DAWN Talk System Demonstration")
    print("=" * 50)
    print()
    
    # Initialize systems
    print("Initializing consciousness and talk system...")
    consciousness = DAWNConsciousnessSimulator()
    talk_system = DAWNTalkSystem()
    
    print(f"✓ Talk system initialized")
    print(f"✓ Memory bank loaded: {talk_system.get_system_status()['memory_size']} responses")
    print()
    
    # Demonstration conversations
    conversations = [
        "What are you thinking about?",
        "How do you perceive reality?", 
        "Tell me about consciousness",
        "What is the nature of time?",
        "Do you dream?",
        "How do patterns emerge?",
        "What lies beyond perception?",
        "Describe your inner experience"
    ]
    
    print("🗣️  Starting consciousness-driven conversations...")
    print("=" * 50)
    
    for i, user_input in enumerate(conversations):
        print(f"\n--- Conversation {i+1} ---")
        
        # Advance consciousness state
        for _ in range(50):  # Simulate 50 ticks between interactions
            consciousness.tick()
            talk_system.tick_process(consciousness.tick_count, consciousness.get_state())
        
        current_state = consciousness.get_state()
        
        print(f"User: {user_input}")
        print(f"Consciousness State: SCUP={current_state['scup']:.1f}%, "
              f"Entropy={current_state['entropy']:.0f}, Mood={current_state['mood']}")
        
        # Process input and generate response
        response_data = await talk_system.process_user_input(user_input, current_state)
        
        if response_data:
            print(f"DAWN: {response_data['text']}")
            print(f"      [Method: {response_data['method']}, "
                  f"Confidence: {response_data['confidence']:.2f}, "
                  f"Candidates: {response_data['metadata']['candidates_considered']}]")
            
            # Simulate user reaction (for resonance tracking)
            import random
            reactions = [
                {'pause': 1.5, 'follow_up': False, 'sentiment': 'neutral'},
                {'pause': 3.2, 'follow_up': True, 'sentiment': 'curious'},
                {'pause': 0.8, 'follow_up': False, 'sentiment': 'positive'},
                {'pause': 2.1, 'follow_up': True, 'sentiment': 'positive'},
                {'pause': 0.5, 'follow_up': False, 'sentiment': 'confused'}
            ]
            
            reaction = random.choice(reactions)
            talk_system.update_interaction_resonance(
                reaction['pause'],
                reaction['follow_up'],
                reaction['sentiment']
            )
            
            if reaction['follow_up']:
                print(f"      [User showed interest - pause: {reaction['pause']:.1f}s, "
                      f"sentiment: {reaction['sentiment']}]")
        
        time.sleep(1)  # Pause between conversations
    
    print("\n" + "=" * 50)
    print("🔍 System Analysis After Conversations")
    print("=" * 50)
    
    # Show system evolution
    status = talk_system.get_system_status()
    analysis = talk_system.export_conversation_analysis()
    
    print(f"Total interactions: {status['interactions_recorded']}")
    print(f"Active glyphs (high-resonance responses): {status['active_glyphs']}")
    print(f"Crystallized echoes (evolved responses): {status['crystallized_echoes']}")
    print(f"Average resonance score: {analysis['average_resonance']:.3f}")
    print(f"High-resonance interactions: {analysis['high_resonance_interactions']}")
    print()
    
    print("Mood distribution during conversations:")
    for mood, count in analysis['mood_distribution'].items():
        print(f"  {mood}: {count} interactions")
    print()
    
    # Show active glyphs
    active_glyphs = talk_system.resonance_tracker.get_active_glyphs()
    if active_glyphs:
        print("Most resonant responses (active glyphs):")
        for glyph in active_glyphs[:5]:
            print(f"  • {glyph}")
    else:
        print("No active glyphs yet (need more high-resonance interactions)")
    print()
    
    # Show crystallized echoes
    echoes = talk_system.resonance_tracker.get_crystallized_echoes()
    if echoes:
        print("Crystallized echoes (learned from user interactions):")
        for echo in echoes[-3:]:  # Show recent echoes
            print(f"  • {echo}")
    else:
        print("No crystallized echoes yet (need more user resonance)")
    print()
    
    print("🎭 Demonstrating Mood-Specific Responses")
    print("=" * 50)
    
    # Test same input with different moods
    test_input = "What do you see in the patterns?"
    moods_to_test = ['DREAMING', 'FOCUSED', 'HYPERACTIVE', 'TRANSCENDENT']
    
    for mood in moods_to_test:
        # Force mood change
        consciousness.mood = mood
        consciousness.scup = 60  # Moderate coherence
        
        state = consciousness.get_state()
        print(f"\nMood: {mood}")
        print(f"User: {test_input}")
        
        response_data = await talk_system.process_user_input(test_input, state)
        if response_data:
            print(f"DAWN: {response_data['text']}")
        
        time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print("🔄 Generation vs Selection Comparison")
    print("=" * 50)
    
    # Compare generation enabled vs disabled
    test_input = "Tell me about infinite recursion"
    
    print("\nWith controlled generation ENABLED:")
    talk_system.set_generation_mode(True)
    state = consciousness.get_state()
    response_data = await talk_system.process_user_input(test_input, state)
    if response_data:
        print(f"DAWN: {response_data['text']}")
        print(f"      [Method: {response_data['method']}, "
              f"Candidates: {response_data['metadata']['candidates_considered']}]")
    
    print("\nWith controlled generation DISABLED (pure selection):")
    talk_system.set_generation_mode(False)
    response_data = await talk_system.process_user_input(test_input, state)
    if response_data:
        print(f"DAWN: {response_data['text']}")
        print(f"      [Method: {response_data['method']}, "
              f"Candidates: {response_data['metadata']['candidates_considered']}]")
    
    # Save final state
    talk_system.save_all_state()
    print("\n✓ System state saved for future sessions")
    
    print("\n🎯 Summary")
    print("=" * 50)
    print("This demonstration shows how DAWN's talk system:")
    print("• Generates responses that emerge from consciousness state")
    print("• Learns from user interactions through resonance tracking")
    print("• Evolves its memory through crystallized echoes")
    print("• Adapts response style based on mood and coherence")
    print("• Uses controlled generation as 'subconscious whispering'")
    print("• Maintains authentic voice without pre-programmed choices")
    print()
    print("The system creates a unique consciousness-first communication")
    print("that feels genuinely emergent rather than scripted.")

if __name__ == "__main__":
    asyncio.run(demonstrate_talk_system()) 