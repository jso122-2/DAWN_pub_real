#!/usr/bin/env python3
"""
DAWN Talk-To Reflection Integration
Replaces random template reflection with curated thought selection
Bridges auto_reflect.py with talk_to.py for contextual introspection
"""

import logging
from typing import Dict, Any
from talk_to import talk_to

logger = logging.getLogger(__name__)

def generate_reflection_from_bank(state: Dict[str, Any]) -> str:
    """
    Generate a reflection using DAWN's curated thought bank instead of templates.
    
    Args:
        state: Current tick state containing entropy, mood, depth, etc.
        
    Returns:
        Selected thought string from the thought bank
    """
    try:
        # Use talk_to to select contextual thought
        reflection = talk_to(state)
        
        # Log the selection for debugging
        logger.debug(f"💭 Selected reflection: {reflection[:50]}...")
        
        return reflection
        
    except Exception as e:
        logger.warning(f"Talk-to reflection failed: {e}, falling back to default")
        
        # Fallback to a simple reflection if talk_to fails
        entropy = state.get('entropy', state.get('entropy_gradient', 0.3))
        tick = state.get('tick_number', 0)
        
        if entropy > 0.7:
            return f"Tick {tick}: High entropy creates new possibilities."
        elif entropy < 0.3:
            return f"Tick {tick}: I rest in calm awareness."
        else:
            return f"Tick {tick}: I process and observe."

# Alias for drop-in replacement
generate_reflection = generate_reflection_from_bank

def get_reflection_stats() -> Dict[str, Any]:
    """Get statistics about the reflection system"""
    from talk_to import get_thought_bank_stats
    
    stats = get_thought_bank_stats()
    stats['reflection_type'] = 'curated_thought_bank'
    stats['fallback_available'] = True
    
    return stats

if __name__ == "__main__":
    # Test the reflection system
    test_states = [
        {
            "entropy": 0.2,
            "consciousness_depth": 0.8,
            "mood": "CALM",
            "tick_number": 1000
        },
        {
            "entropy": 0.8,
            "consciousness_depth": 0.4,
            "mood": "ENERGETIC", 
            "tick_number": 2000
        },
        {
            "entropy": 0.5,
            "consciousness_depth": 0.7,
            "mood": "CONTEMPLATIVE",
            "tick_number": 3000
        }
    ]
    
    print("🔁 DAWN Talk-To Reflection Test")
    print("=" * 40)
    
    for i, state in enumerate(test_states, 1):
        reflection = generate_reflection_from_bank(state)
        print(f"{i}. State: E={state['entropy']:.1f}, D={state['consciousness_depth']:.1f}, {state['mood']}")
        print(f"   Reflection: {reflection}")
        print()
    
    print("📊 Reflection Stats:")
    stats = get_reflection_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}") 