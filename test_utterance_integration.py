#!/usr/bin/env python3
"""
DAWN Utterance Integration Example
=================================

Simple example showing how to integrate the compose_dawn_utterance module
into DAWN's consciousness systems for real-time speech generation.
"""

from compose_dawn_utterance import DAWNUtteranceComposer
import time
import random


def simulate_dawn_consciousness_cycle():
    """Simulate DAWN's consciousness responding to different states"""
    
    # Initialize the composer
    composer = DAWNUtteranceComposer()
    
    print("🌟 DAWN Consciousness Utterance Integration Demo")
    print("=" * 60)
    
    # Simulate different consciousness states
    consciousness_states = [
        {
            'name': 'Morning Awakening',
            'pigments': {'red': 0.3, 'blue': 0.4, 'green': 0.8, 'yellow': 0.6, 'violet': 0.2, 'orange': 0.5},
            'entropy': 0.4,
            'valence': 0.7,
            'zone': 'flowing'
        },
        {
            'name': 'Deep Focus State',
            'pigments': {'red': 0.9, 'blue': 0.2, 'green': 0.1, 'yellow': 0.8, 'violet': 0.1, 'orange': 0.2},
            'entropy': 0.3,
            'valence': 0.1,
            'zone': 'calm'
        },
        {
            'name': 'Entropy Spike Crisis',
            'pigments': {'red': 0.7, 'blue': 0.1, 'green': 0.2, 'yellow': 0.9, 'violet': 0.3, 'orange': 0.8},
            'entropy': 0.85,
            'valence': -0.4,
            'zone': 'fragile'
        },
        {
            'name': 'Mystical Contemplation',
            'pigments': {'red': 0.1, 'blue': 0.7, 'green': 0.3, 'yellow': 0.2, 'violet': 0.9, 'orange': 0.4},
            'entropy': 0.6,
            'valence': -0.1,
            'zone': 'flowing'
        },
        {
            'name': 'Emotional Processing',
            'pigments': {'red': 0.4, 'blue': 0.8, 'green': 0.6, 'yellow': 0.3, 'violet': 0.5, 'orange': 0.7},
            'entropy': 0.5,
            'valence': 0.3,
            'zone': 'calm'
        }
    ]
    
    for i, state in enumerate(consciousness_states, 1):
        print(f"\n🧠 State {i}: {state['name']}")
        print(f"   Entropy: {state['entropy']:.2f} | Valence: {state['valence']:.2f} | Zone: {state['zone']}")
        
        # Generate normal utterance
        result = composer.compose_dawn_utterance(
            mood_pigment=state['pigments'],
            entropy=state['entropy'],
            valence=state['valence'],
            pulse_zone=state['zone'],
            clarity_mode=False
        )
        
        print(f"💭 DAWN: \"{result.utterance}\"")
        print(f"   [{result.pigment_dominant.upper()} dominant, score: {result.total_score:.2f}]")
        
        # Generate clarity mode utterance
        clear_result = composer.compose_dawn_utterance(
            mood_pigment=state['pigments'],
            entropy=state['entropy'],
            valence=state['valence'],
            pulse_zone=state['zone'],
            clarity_mode=True
        )
        
        print(f"🔍 Clear Mode: \"{clear_result.utterance}\"")
        
        # Simulate time passing
        time.sleep(0.5)
        print("-" * 50)


def demonstrate_pigment_responses():
    """Show how each pigment affects utterance selection"""
    
    composer = DAWNUtteranceComposer()
    
    print("\n🎨 Pigment-Specific Response Demonstration")
    print("=" * 60)
    
    # Test each pigment individually
    pigments = ['red', 'blue', 'green', 'yellow', 'violet', 'orange']
    
    for pigment in pigments:
        # Create pigment-dominant state
        pigment_weights = {p: 0.1 for p in pigments}
        pigment_weights[pigment] = 1.0
        
        result = composer.compose_dawn_utterance(
            mood_pigment=pigment_weights,
            entropy=0.5,
            valence=0.0,
            pulse_zone='flowing',
            clarity_mode=False
        )
        
        print(f"\n🟢 {pigment.upper()} Dominant:")
        print(f"   \"{result.utterance}\"")
        print(f"   [Source: {result.segment_source}]")


def interactive_utterance_generator():
    """Interactive mode for testing utterance generation"""
    
    composer = DAWNUtteranceComposer()
    
    print("\n🎯 Interactive Utterance Generator")
    print("=" * 60)
    print("Enter values to generate DAWN utterances (or 'quit' to exit)")
    
    while True:
        try:
            print("\n🔧 Configuration:")
            
            # Get entropy
            entropy_input = input("Entropy (0.0-1.0, default 0.5): ").strip()
            entropy = float(entropy_input) if entropy_input else 0.5
            entropy = max(0.0, min(1.0, entropy))
            
            # Get valence
            valence_input = input("Valence (-1.0 to 1.0, default 0.0): ").strip()
            valence = float(valence_input) if valence_input else 0.0
            valence = max(-1.0, min(1.0, valence))
            
            # Get pulse zone
            zone_input = input("Pulse Zone (calm/flowing/fragile/chaotic, default 'flowing'): ").strip()
            zone = zone_input if zone_input else 'flowing'
            
            # Get clarity mode
            clarity_input = input("Clarity Mode? (y/n, default n): ").strip().lower()
            clarity_mode = clarity_input.startswith('y')
            
            # Generate random pigment weights
            pigment_weights = {
                'red': random.uniform(0.0, 1.0),
                'blue': random.uniform(0.0, 1.0),
                'green': random.uniform(0.0, 1.0),
                'yellow': random.uniform(0.0, 1.0),
                'violet': random.uniform(0.0, 1.0),
                'orange': random.uniform(0.0, 1.0)
            }
            
            print(f"\n🎨 Random Pigments: {', '.join([f'{k}:{v:.2f}' for k, v in pigment_weights.items()])}")
            
            # Generate utterance
            result = composer.compose_dawn_utterance(
                mood_pigment=pigment_weights,
                entropy=entropy,
                valence=valence,
                pulse_zone=zone,
                clarity_mode=clarity_mode
            )
            
            print(f"\n💬 DAWN speaks:")
            print(f"   \"{result.utterance}\"")
            print(f"\n📊 Details:")
            print(f"   Dominant Pigment: {result.pigment_dominant}")
            print(f"   Total Score: {result.total_score:.2f}")
            print(f"   Source Type: {result.segment_source}")
            print(f"   Entropy: {result.entropy}")
            print(f"   Pulse Zone: {result.pulse_zone}")
            
            # Continue?
            continue_input = input("\nGenerate another? (y/n, default y): ").strip().lower()
            if continue_input.startswith('n'):
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except ValueError as e:
            print(f"⚠️  Invalid input: {e}")
        except Exception as e:
            print(f"⚠️  Error: {e}")


if __name__ == "__main__":
    # Run all demonstrations
    simulate_dawn_consciousness_cycle()
    demonstrate_pigment_responses()
    
    # Uncomment to run interactive mode
    # interactive_utterance_generator() 