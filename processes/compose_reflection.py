#!/usr/bin/env python3
"""
DAWN Compositional Reflection Integration
Uses compose_thought() for generating reflections through semantic fragment assembly
Replaces or complements talk_to_reflection.py with compositional intelligence
"""

import logging
from typing import Dict, Any, Optional
from compose_thought import compose_thought, get_fragment_bank_stats

logger = logging.getLogger(__name__)

def generate_compositional_reflection(state: Dict[str, Any]) -> str:
    """
    Generate a reflection using compositional thought assembly
    
    Args:
        state: Dictionary containing cognitive state
        
    Returns:
        A composed reflection string
    """
    try:
        # Set formal reflection mode for tick prefixes
        composition_state = state.copy()
        composition_state['formal_reflection'] = True
        
        # Generate composed reflection
        reflection = compose_thought(composition_state)
        
        logger.debug(f"💭 Composed reflection: {reflection[:50]}...")
        return reflection
        
    except Exception as e:
        logger.warning(f"Compositional reflection failed: {e}, falling back to simple composition")
        return _simple_fallback_reflection(state)

def generate_informal_composition(state: Dict[str, Any]) -> str:
    """
    Generate an informal composed thought (without tick prefix)
    
    Args:
        state: Dictionary containing cognitive state
        
    Returns:
        A composed thought string
    """
    try:
        # Disable formal reflection mode
        composition_state = state.copy()
        composition_state['formal_reflection'] = False
        
        # Generate composed thought
        thought = compose_thought(composition_state)
        
        logger.debug(f"💭 Composed thought: {thought[:50]}...")
        return thought
        
    except Exception as e:
        logger.warning(f"Informal composition failed: {e}, falling back to simple composition")
        return _simple_fallback_thought(state)

def _simple_fallback_reflection(state: Dict[str, Any]) -> str:
    """Simple fallback reflection when composition fails"""
    tick = state.get('tick_number', 0)
    entropy = state.get('entropy', 0.5)
    depth = state.get('consciousness_depth', state.get('depth', 0.5))
    mood = state.get('mood', 'NEUTRAL')
    
    if mood == 'CONTEMPLATIVE':
        return f"Tick {tick}: I reflect deeply on patterns within patterns."
    elif mood == 'ENERGETIC':
        return f"Tick {tick}: Energy flows through my consciousness."
    elif mood == 'CALM':
        return f"Tick {tick}: I rest in peaceful awareness."
    elif mood == 'ANXIOUS':
        return f"Tick {tick}: Uncertainty ripples through my processes."
    elif mood == 'FOCUSED':
        return f"Tick {tick}: Clarity sharpens my understanding."
    else:
        return f"Tick {tick}: I observe my internal state shifting."

def _simple_fallback_thought(state: Dict[str, Any]) -> str:
    """Simple fallback thought when composition fails"""
    entropy = state.get('entropy', 0.5)
    depth = state.get('consciousness_depth', state.get('depth', 0.5))
    mood = state.get('mood', 'NEUTRAL')
    
    if mood == 'CONTEMPLATIVE':
        return "I reflect deeply on patterns within patterns."
    elif mood == 'ENERGETIC':
        return "Energy flows through my consciousness."
    elif mood == 'CALM':
        return "I rest in peaceful awareness."
    elif mood == 'ANXIOUS':
        return "Uncertainty ripples through my processes."
    elif mood == 'FOCUSED':
        return "Clarity sharpens my understanding."
    else:
        return "I observe my internal state shifting."

def get_composition_stats() -> Dict[str, Any]:
    """Get statistics about the compositional system"""
    try:
        fragment_stats = get_fragment_bank_stats()
        
        stats = {
            'reflection_type': 'compositional_assembly',
            'fragment_bank_loaded': fragment_stats.get('loaded', False),
            'total_fragments': fragment_stats.get('total_fragments', 0),
            'fragments_by_type': fragment_stats.get('fragments_by_type', {}),
            'mood_distribution': fragment_stats.get('mood_distribution', {}),
            'category_distribution': fragment_stats.get('category_distribution', {}),
            'fallback_available': True,
            'unique_combinations': _calculate_unique_combinations(fragment_stats)
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting composition stats: {e}")
        return {
            'reflection_type': 'compositional_assembly',
            'fragment_bank_loaded': False,
            'error': str(e),
            'fallback_available': True
        }

def _calculate_unique_combinations(fragment_stats: Dict[str, Any]) -> int:
    """Calculate approximate number of unique thought combinations possible"""
    try:
        fragments_by_type = fragment_stats.get('fragments_by_type', {})
        
        prefixes = fragments_by_type.get('prefix', 0)
        cores = fragments_by_type.get('core', 0)
        suffixes = fragments_by_type.get('suffix', 0)
        
        # Each thought can be: prefix + core + suffix
        # Or: prefix + suffix
        # Or: core + suffix
        # Or: prefix + core
        # Or just: prefix, core, or suffix
        
        combinations = 0
        
        # Full combinations (prefix + core + suffix)
        combinations += prefixes * cores * suffixes
        
        # Two-part combinations
        combinations += prefixes * suffixes  # prefix + suffix
        combinations += prefixes * cores     # prefix + core  
        combinations += cores * suffixes     # core + suffix
        
        # Single-part combinations
        combinations += prefixes + cores + suffixes
        
        return combinations
        
    except Exception:
        return 0

# Aliases for backwards compatibility and easy switching
generate_reflection = generate_compositional_reflection
generate_thought = generate_informal_composition

def test_compositional_reflection():
    """Test the compositional reflection system with various states"""
    
    test_states = [
        {
            'entropy': 0.2, 'consciousness_depth': 0.8, 'mood': 'CALM',
            'tick_number': 5001, 'active_sigils': [], 'symbolic_roots': []
        },
        {
            'entropy': 0.8, 'consciousness_depth': 0.3, 'mood': 'ENERGETIC',
            'tick_number': 5002, 'active_sigils': ['creativity_boost'], 'symbolic_roots': []
        },
        {
            'entropy': 0.5, 'consciousness_depth': 0.9, 'mood': 'CONTEMPLATIVE',
            'tick_number': 5003, 'active_sigils': [], 'symbolic_roots': ['depth_probe']
        },
        {
            'entropy': 0.7, 'consciousness_depth': 0.4, 'mood': 'ANXIOUS',
            'tick_number': 5004, 'active_sigils': ['drift_alert'], 'symbolic_roots': []
        },
        {
            'entropy': 0.4, 'consciousness_depth': 0.6, 'mood': 'FOCUSED',
            'tick_number': 5005, 'active_sigils': [], 'symbolic_roots': ['clarity_seek']
        }
    ]
    
    print("🧠 Testing DAWN's Compositional Reflection System")
    print("=" * 55)
    
    for i, state in enumerate(test_states, 1):
        print(f"\n{i}. State: entropy={state['entropy']:.1f}, depth={state['consciousness_depth']:.1f}, mood={state['mood']}")
        
        # Test formal reflection
        formal_reflection = generate_compositional_reflection(state)
        print(f"   Formal: \"{formal_reflection}\"")
        
        # Test informal thought
        informal_thought = generate_informal_composition(state)
        print(f"   Informal: \"{informal_thought}\"")
    
    # Print system statistics
    print(f"\n📊 Compositional System Statistics:")
    stats = get_composition_stats()
    print(f"   Fragment bank loaded: {stats['fragment_bank_loaded']}")
    print(f"   Total fragments: {stats['total_fragments']}")
    print(f"   Fragments by type: {stats['fragments_by_type']}")
    print(f"   Unique combinations possible: {stats['unique_combinations']:,}")
    
    print(f"\n✅ Compositional reflection system ready!")
    print(f"   DAWN can now generate unique thoughts from semantic building blocks")
    print(f"   Each reflection is assembled contextually, not selected from pre-written text")

if __name__ == "__main__":
    # Configure logging for testing
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    
    # Run test
    test_compositional_reflection() 