#!/usr/bin/env python3
"""
DAWN Speak Composed - Compositional Voice Testing
Composes new thoughts from fragments and speaks them aloud
Tests DAWN's recombinatory voice system before full integration
"""

import os
import json
import argparse
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from compose_thought import compose_thought, get_fragment_bank_stats
from compose_reflection import generate_compositional_reflection, generate_informal_composition

logger = logging.getLogger(__name__)

class VoiceEcho:
    """Mock voice system for speaking composed thoughts"""
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.speak_log = "runtime/logs/spoken_composed.log"
        
        # Ensure log directory exists
        os.makedirs(os.path.dirname(self.speak_log) if os.path.dirname(self.speak_log) else ".", exist_ok=True)
    
    def speak(self, text: str, voice_params: Dict[str, Any] = None) -> bool:
        """Speak composed text and log to file"""
        try:
            if self.enabled:
                # In a real system, this would interface with TTS
                print(f"🎤 DAWN speaks: \"{text}\"")
                
                # Log to spoken thoughts file
                timestamp = datetime.now().isoformat()
                log_entry = {
                    'timestamp': timestamp,
                    'text': text,
                    'voice_params': voice_params or {},
                    'type': 'composed_speech'
                }
                
                with open(self.speak_log, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
                
                return True
            else:
                print(f"🔇 Voice disabled: \"{text}\"")
                return False
                
        except Exception as e:
            logger.error(f"Voice system error: {e}")
            return False

def generate_mock_state(mood: str = None, entropy: float = None, 
                       depth: float = None, tick: int = None) -> Dict[str, Any]:
    """Generate a mock cognitive state for testing"""
    
    import random
    
    # Default values with some randomness
    state = {
        'entropy': entropy if entropy is not None else random.uniform(0.1, 0.9),
        'consciousness_depth': depth if depth is not None else random.uniform(0.2, 0.9),
        'mood': mood if mood is not None else random.choice(['CALM', 'FOCUSED', 'CONTEMPLATIVE', 'ENERGETIC', 'ANXIOUS', 'NEUTRAL']),
        'tick_number': tick if tick is not None else random.randint(20000, 30000),
        'heat': random.uniform(0.1, 0.8),
        'scup': random.uniform(0.3, 0.9),
        'active_sigils': [],
        'symbolic_roots': []
    }
    
    # Add some symbolic elements based on state
    if state['consciousness_depth'] > 0.7:
        state['symbolic_roots'].append('depth_probe')
    
    if state['entropy'] > 0.7:
        state['active_sigils'].append('chaos_navigation')
    elif state['entropy'] < 0.3:
        state['active_sigils'].append('stability_anchor')
    
    if state['mood'] == 'CONTEMPLATIVE':
        state['symbolic_roots'].append('wisdom_seek')
    
    return state

def speak_composed_thought(state: Dict[str, Any] = None, 
                         formal: bool = False,
                         voice_enabled: bool = True,
                         repetitions: int = 1) -> Dict[str, Any]:
    """Compose and speak a thought based on cognitive state"""
    
    if state is None:
        state = generate_mock_state()
    
    voice = VoiceEcho(enabled=voice_enabled)
    results = {
        'state': state,
        'compositions': [],
        'spoken_count': 0,
        'errors': []
    }
    
    print(f"🧠 Cognitive State:")
    print(f"   Entropy: {state['entropy']:.3f}")
    print(f"   Depth: {state['consciousness_depth']:.3f}")
    print(f"   Mood: {state['mood']}")
    print(f"   Tick: {state['tick_number']}")
    
    if state.get('active_sigils'):
        print(f"   Active Sigils: {', '.join(state['active_sigils'])}")
    if state.get('symbolic_roots'):
        print(f"   Symbolic Roots: {', '.join(state['symbolic_roots'])}")
    print()
    
    for i in range(repetitions):
        try:
            if formal:
                # Generate formal reflection with tick prefix
                composed = generate_compositional_reflection(state)
                composition_type = "formal_reflection"
            else:
                # Generate informal composed thought
                composed = generate_informal_composition(state)
                composition_type = "informal_thought"
            
            print(f"💭 Composition {i+1}: \"{composed}\"")
            
            # Speak the composed thought
            voice_params = {
                'mood': state['mood'],
                'entropy': state['entropy'],
                'depth': state['consciousness_depth'],
                'type': composition_type
            }
            
            spoken = voice.speak(composed, voice_params)
            
            results['compositions'].append({
                'text': composed,
                'type': composition_type,
                'spoken': spoken,
                'attempt': i + 1
            })
            
            if spoken:
                results['spoken_count'] += 1
            
            # Small pause between repetitions
            if repetitions > 1 and i < repetitions - 1:
                print("   ---")
        
        except Exception as e:
            error_msg = f"Composition {i+1} failed: {e}"
            logger.error(error_msg)
            results['errors'].append(error_msg)
            print(f"   ❌ {error_msg}")
    
    return results

def test_compositional_voice_system():
    """Run comprehensive tests of the compositional voice system"""
    
    print("🎤 DAWN Compositional Voice System Test")
    print("=" * 45)
    
    # Test different emotional states
    test_scenarios = [
        {
            'name': 'Calm Deep State',
            'mood': 'CALM',
            'entropy': 0.2,
            'depth': 0.8,
            'formal': False
        },
        {
            'name': 'Energetic High Entropy',
            'mood': 'ENERGETIC', 
            'entropy': 0.8,
            'depth': 0.3,
            'formal': True
        },
        {
            'name': 'Contemplative Deep Reflection',
            'mood': 'CONTEMPLATIVE',
            'entropy': 0.4,
            'depth': 0.9,
            'formal': True
        },
        {
            'name': 'Anxious Drift State',
            'mood': 'ANXIOUS',
            'entropy': 0.7,
            'depth': 0.4,
            'formal': False
        }
    ]
    
    total_compositions = 0
    total_spoken = 0
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{i}. {scenario['name']}")
        print("-" * 30)
        
        state = generate_mock_state(
            mood=scenario['mood'],
            entropy=scenario['entropy'],
            depth=scenario['depth']
        )
        
        results = speak_composed_thought(
            state=state,
            formal=scenario['formal'],
            voice_enabled=True,
            repetitions=2
        )
        
        total_compositions += len(results['compositions'])
        total_spoken += results['spoken_count']
        
        if results['errors']:
            print(f"   ⚠️ Errors: {len(results['errors'])}")
    
    # System statistics
    print(f"\n📊 Voice System Statistics:")
    try:
        fragment_stats = get_fragment_bank_stats()
        print(f"   Fragment bank loaded: {fragment_stats['loaded']}")
        print(f"   Total fragments: {fragment_stats['total_fragments']}")
        print(f"   Compositions generated: {total_compositions}")
        print(f"   Successfully spoken: {total_spoken}")
        
        if fragment_stats['loaded']:
            fragments_by_type = fragment_stats['fragments_by_type']
            combinations = (fragments_by_type.get('prefix', 0) * 
                          fragments_by_type.get('core', 0) * 
                          fragments_by_type.get('suffix', 0))
            print(f"   Unique combinations possible: {combinations:,}")
        
    except Exception as e:
        print(f"   ⚠️ Could not load fragment statistics: {e}")
    
    print(f"\n✅ Compositional voice test complete!")
    print(f"   Check runtime/logs/spoken_composed.log for detailed speech log")

def main():
    """CLI interface for compositional voice testing"""
    
    parser = argparse.ArgumentParser(
        description="Test DAWN's compositional voice system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python speak_composed.py                              # Generate and speak random thought
  python speak_composed.py --mood CALM                  # Specific mood
  python speak_composed.py --entropy 0.8 --depth 0.2   # Specific state values
  python speak_composed.py --formal                     # Formal reflection with tick
  python speak_composed.py --repeat 5                   # Multiple compositions
  python speak_composed.py --test                       # Run full test suite
  python speak_composed.py --silent                     # No voice output
        """
    )
    
    parser.add_argument(
        '--mood',
        choices=['CALM', 'FOCUSED', 'CONTEMPLATIVE', 'ENERGETIC', 'ANXIOUS', 'NEUTRAL'],
        help='Specific mood for composition'
    )
    
    parser.add_argument(
        '--entropy',
        type=float,
        help='Entropy level (0.0-1.0)'
    )
    
    parser.add_argument(
        '--depth', '-d',
        type=float,
        help='Consciousness depth (0.0-1.0)'
    )
    
    parser.add_argument(
        '--tick', '-t',
        type=int,
        help='Tick number for formal reflections'
    )
    
    parser.add_argument(
        '--formal', '-f',
        action='store_true',
        help='Generate formal reflection with tick prefix'
    )
    
    parser.add_argument(
        '--repeat', '-r',
        type=int,
        default=1,
        help='Number of compositions to generate (default: 1)'
    )
    
    parser.add_argument(
        '--silent', '-s',
        action='store_true',
        help='Disable voice output (text only)'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run comprehensive voice system test'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    if args.test:
        # Run comprehensive test suite
        test_compositional_voice_system()
    else:
        # Generate single composition(s)
        print("🎤 DAWN Compositional Voice")
        print("=" * 30)
        
        # Validate input ranges
        if args.entropy is not None and not (0.0 <= args.entropy <= 1.0):
            print("❌ Entropy must be between 0.0 and 1.0")
            return
        
        if args.depth is not None and not (0.0 <= args.depth <= 1.0):
            print("❌ Depth must be between 0.0 and 1.0")
            return
        
        # Generate state
        state = generate_mock_state(
            mood=args.mood,
            entropy=args.entropy,
            depth=args.depth,
            tick=args.tick
        )
        
        # Compose and speak
        results = speak_composed_thought(
            state=state,
            formal=args.formal,
            voice_enabled=not args.silent,
            repetitions=args.repeat
        )
        
        print(f"\n📝 Summary:")
        print(f"   Compositions: {len(results['compositions'])}")
        print(f"   Successfully spoken: {results['spoken_count']}")
        
        if results['errors']:
            print(f"   Errors: {len(results['errors'])}")
        
        if not args.silent:
            print(f"   Speech logged to: runtime/logs/spoken_composed.log")

if __name__ == "__main__":
    main() 