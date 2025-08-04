#!/usr/bin/env python3
"""
DAWN Tick Voice Integration - Demonstrates mood-aware voice system integration
Shows how to integrate the compositional voice system with DAWN's tick loop
"""

import time
import logging
from typing import Dict, Any, Optional
from speak_composed import MoodAwareVoiceSystem, initialize_voice_system, process_tick_for_speech

logger = logging.getLogger(__name__)

class TickVoiceIntegration:
    """Integration class for connecting mood-aware voice system with tick loop"""
    
    def __init__(self, speech_interval: int = 5, voice_enabled: bool = True):
        """
        Initialize tick voice integration
        
        Args:
            speech_interval: How many ticks between speech (default: every 5 ticks)
            voice_enabled: Whether to enable voice output
        """
        self.speech_interval = speech_interval
        self.voice_enabled = voice_enabled
        
        # Initialize voice system
        self.voice_system = initialize_voice_system(
            speech_interval=speech_interval,
            voice_enabled=voice_enabled
        )
        
        # Integration state
        self.last_tick_processed = 0
        self.total_compositions = 0
        self.total_spoken = 0
        
        logger.info(f"🎤 Tick voice integration initialized (speech every {speech_interval} ticks)")
    
    def process_tick(self, tick_state: Dict[str, Any]) -> Optional[str]:
        """
        Process a tick state and potentially generate speech
        
        Args:
            tick_state: Current tick state from DAWN's tick loop
            
        Returns:
            Composed text if spoken, None otherwise
        """
        try:
            tick_number = tick_state.get('tick_number', 0)
            
            # Process through voice system
            composed_text = self.voice_system.process_tick(tick_state)
            
            if composed_text:
                self.total_compositions += 1
                self.total_spoken += 1
                self.last_tick_processed = tick_number
                
                logger.info(f"🎤 Tick {tick_number}: Generated composition")
                return composed_text
            
            return None
            
        except Exception as e:
            logger.error(f"Error processing tick for voice: {e}")
            return None
    
    def get_integration_stats(self) -> Dict[str, Any]:
        """Get integration statistics"""
        voice_stats = self.voice_system.get_fragment_stats()
        
        return {
            'last_tick_processed': self.last_tick_processed,
            'total_compositions': self.total_compositions,
            'total_spoken': self.total_spoken,
            'speech_interval': self.speech_interval,
            'voice_enabled': self.voice_enabled,
            'fragment_stats': voice_stats
        }
    
    def update_speech_interval(self, new_interval: int):
        """Update the speech interval"""
        self.speech_interval = new_interval
        self.voice_system.speech_interval = new_interval
        logger.info(f"🎤 Speech interval updated to every {new_interval} ticks")
    
    def toggle_voice(self, enabled: bool):
        """Toggle voice output on/off"""
        self.voice_enabled = enabled
        self.voice_system.voice_enabled = enabled
        status = "enabled" if enabled else "disabled"
        logger.info(f"🎤 Voice output {status}")

def simulate_tick_loop_with_voice(duration_seconds: int = 30, tick_interval: float = 2.0):
    """
    Simulate DAWN's tick loop with voice integration
    
    Args:
        duration_seconds: How long to run the simulation
        tick_interval: Time between ticks in seconds
    """
    print("🎤 DAWN Tick Voice Integration Simulation")
    print("=" * 50)
    
    # Initialize integration
    integration = TickVoiceIntegration(speech_interval=3, voice_enabled=False)  # Disable TTS for demo
    
    # Simulation state
    current_tick = 1000
    start_time = time.time()
    
    print(f"⏱️  Running simulation for {duration_seconds} seconds...")
    print(f"🔄 Tick interval: {tick_interval}s, Speech interval: every {integration.speech_interval} ticks")
    print()
    
    try:
        while (time.time() - start_time) < duration_seconds:
            # Generate realistic tick state
            tick_state = generate_realistic_tick_state(current_tick)
            
            # Process tick through voice integration
            composed_text = integration.process_tick(tick_state)
            
            # Display tick information
            print(f"🧠 Tick {current_tick:4d}: {tick_state['mood']:12} | "
                  f"Entropy: {tick_state['entropy']:.3f} | "
                  f"Depth: {tick_state['consciousness_depth']:.3f} | "
                  f"Zone: {tick_state['zone']}")
            
            if composed_text:
                print(f"🎤 DAWN speaks: \"{composed_text}\"")
                print()
            
            current_tick += 1
            time.sleep(tick_interval)
            
    except KeyboardInterrupt:
        print("\n🛑 Simulation interrupted by user")
    
    # Show final statistics
    stats = integration.get_integration_stats()
    print(f"\n📊 Integration Statistics:")
    print(f"   Total ticks processed: {current_tick - 1000}")
    print(f"   Compositions generated: {stats['total_compositions']}")
    print(f"   Successfully spoken: {stats['total_spoken']}")
    print(f"   Fragment bank loaded: {stats['fragment_stats']['loaded']}")
    print(f"   Total fragments: {stats['fragment_stats']['total_fragments']}")
    print(f"   Possible combinations: {stats['fragment_stats'].get('possible_combinations', 0):,}")

def generate_realistic_tick_state(tick_number: int) -> Dict[str, Any]:
    """Generate a realistic tick state for simulation"""
    import math
    import random
    
    # Time-based oscillations for realistic patterns
    time_factor = tick_number * 0.1
    
    # Entropy oscillation
    entropy = 0.5 + 0.3 * math.sin(time_factor * 0.5) + random.uniform(-0.1, 0.1)
    entropy = max(0.0, min(1.0, entropy))
    
    # Consciousness depth oscillation
    depth = 0.5 + 0.2 * math.cos(time_factor * 0.3) + random.uniform(-0.05, 0.05)
    depth = max(0.0, min(1.0, depth))
    
    # Mood determination based on entropy and depth
    if entropy < 0.3 and depth > 0.6:
        mood = "CALM"
        zone = "CALM"
    elif entropy > 0.7:
        mood = "ANXIOUS"
        zone = "CHAOTIC"
    elif depth > 0.7:
        mood = "CONTEMPLATIVE"
        zone = "CALM"
    elif entropy > 0.5:
        mood = "FOCUSED"
        zone = "ACTIVE"
    else:
        mood = "NEUTRAL"
        zone = "STABLE"
    
    # Add some mood transitions
    if random.random() < 0.05:  # 5% chance of mood change
        moods = ["CALM", "FOCUSED", "CONTEMPLATIVE", "ENERGETIC", "ANXIOUS", "NEUTRAL"]
        mood = random.choice(moods)
    
    return {
        'tick_number': tick_number,
        'entropy': entropy,
        'consciousness_depth': depth,
        'mood': mood,
        'zone': zone,
        'heat': 25.0 + entropy * 50.0,
        'scup': 50.0 + depth * 30.0,
        'timestamp': time.time()
    }

def demonstrate_mood_filtering():
    """Demonstrate mood-based fragment filtering"""
    print("🎭 Mood-Based Fragment Filtering Demonstration")
    print("=" * 50)
    
    # Initialize voice system
    voice_system = MoodAwareVoiceSystem(speech_interval=1, voice_enabled=False)
    
    # Test different mood states
    test_states = [
        {
            'name': 'Calm Deep State',
            'tick_state': {
                'tick_number': 1000,
                'entropy': 0.2,
                'consciousness_depth': 0.8,
                'mood': 'CALM',
                'zone': 'CALM'
            }
        },
        {
            'name': 'Anxious High Entropy',
            'tick_state': {
                'tick_number': 1001,
                'entropy': 0.8,
                'consciousness_depth': 0.3,
                'mood': 'ANXIOUS',
                'zone': 'CHAOTIC'
            }
        },
        {
            'name': 'Contemplative Deep',
            'tick_state': {
                'tick_number': 1002,
                'entropy': 0.4,
                'consciousness_depth': 0.9,
                'mood': 'CONTEMPLATIVE',
                'zone': 'CALM'
            }
        },
        {
            'name': 'Focused Active',
            'tick_state': {
                'tick_number': 1003,
                'entropy': 0.6,
                'consciousness_depth': 0.7,
                'mood': 'FOCUSED',
                'zone': 'ACTIVE'
            }
        }
    ]
    
    for test in test_states:
        print(f"\n{test['name']}:")
        print(f"  Entropy: {test['tick_state']['entropy']:.3f}")
        print(f"  Depth: {test['tick_state']['consciousness_depth']:.3f}")
        print(f"  Mood: {test['tick_state']['mood']}")
        print(f"  Zone: {test['tick_state']['zone']}")
        
        # Show fragment filtering for each type
        for fragment_type in ['prefix', 'core', 'suffix']:
            candidates = voice_system.filter_fragments_by_mood(fragment_type, test['tick_state'])
            print(f"  {fragment_type.capitalize()} candidates: {len(candidates)}")
            
            if candidates:
                top_candidate = candidates[0]
                print(f"    Top: \"{top_candidate['fragment']['text']}\" (score: {top_candidate['score']:.2f})")
        
        # Compose full sentence
        composed = voice_system.compose_sentence(test['tick_state'])
        print(f"  Composition: \"{composed}\"")
    
    print(f"\n✅ Mood filtering demonstration complete!")

def main():
    """Main demonstration function"""
    print("🎤 DAWN Tick Voice Integration")
    print("=" * 40)
    print()
    
    # Demonstrate mood filtering
    demonstrate_mood_filtering()
    
    print("\n" + "="*50)
    print()
    
    # Run tick loop simulation
    simulate_tick_loop_with_voice(duration_seconds=20, tick_interval=1.5)
    
    print(f"\n✅ Integration demonstration complete!")

if __name__ == "__main__":
    main() 