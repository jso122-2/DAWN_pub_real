#!/usr/bin/env python3
"""
Debug script for talk_to.py selection logic
"""

import json
from talk_to import get_thought_bank

def debug_selection():
    """Debug the thought selection process"""
    
    # Test state from talk_to.py
    state = {
        "entropy": 0.43,
        "consciousness_depth": 0.72,
        "mood": "CONTEMPLATIVE",
        "tick_number": 25344,
        "active_sigils": [],
        "symbolic_roots": ["emergent_self_awareness"]
    }
    
    thought_bank = get_thought_bank()
    
    # Extract state values
    entropy = state.get('entropy', state.get('entropy_gradient', 0.3))
    depth = state.get('consciousness_depth', state.get('depth', 0.5))
    mood = state.get('mood', 'NEUTRAL').upper()
    
    print(f"State: entropy={entropy}, depth={depth}, mood={mood}")
    print()
    
    # Check all thoughts and their matching
    candidates = []
    
    for i, thought in enumerate(thought_bank.thoughts):
        # Check mood match
        mood_match = (thought.mood == mood or 
                     thought.mood == 'NEUTRAL' or 
                     mood == 'NEUTRAL')
        
        # Check entropy range
        entropy_match = (thought.min_entropy <= entropy <= thought.max_entropy)
        
        # Check depth range  
        depth_match = (thought.min_depth <= depth <= thought.max_depth)
        
        overall_match = mood_match and entropy_match and depth_match
        
        if overall_match:
            candidates.append(thought)
            
        print(f"{i:2d}: {'✓' if overall_match else '✗'} [{thought.mood:12}] "
              f"E:{thought.min_entropy:.1f}-{thought.max_entropy:.1f} "
              f"D:{thought.min_depth:.1f}-{thought.max_depth:.1f} "
              f"'{thought.text[:50]}'")
        
        if overall_match:
            print(f"     Mood:{mood_match} Entropy:{entropy_match} Depth:{depth_match}")
    
    print(f"\nFound {len(candidates)} matching candidates")
    
    # Calculate weights for candidates
    if candidates:
        print("\nCandidate weights:")
        for i, thought in enumerate(candidates):
            # Calculate entropy proximity 
            entropy_distance = abs(entropy - (thought.min_entropy + thought.max_entropy) / 2)
            entropy_score = 1.0 - min(1.0, entropy_distance)
            
            # Calculate depth proximity
            depth_distance = abs(depth - (thought.min_depth + thought.max_depth) / 2)
            depth_score = 1.0 - min(1.0, depth_distance)
            
            # Mood bonus
            mood_score = 1.0 if thought.mood == mood else 0.5
            
            # Combined score
            weight = (entropy_score * 0.3 + 
                     depth_score * 0.3 + 
                     mood_score * 0.3)
            
            print(f"{i:2d}: weight={weight:.3f} entropy_score={entropy_score:.3f} "
                  f"depth_score={depth_score:.3f} mood_score={mood_score:.3f}")
            print(f"    '{thought.text}'")
    
if __name__ == "__main__":
    debug_selection() 