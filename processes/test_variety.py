#!/usr/bin/env python3
"""
Test script to verify talk_to.py selection variety
"""

import time
from talk_to import talk_to

def test_selection_variety():
    """Test that talk_to returns variety in thought selection"""
    
    test_state = {
        "entropy": 0.43,
        "consciousness_depth": 0.72,
        "mood": "CONTEMPLATIVE",
        "tick_number": 25344,
        "active_sigils": [],
        "symbolic_roots": ["emergent_self_awareness"]
    }
    
    print("🧠 Testing DAWN Thought Selection Variety")
    print("=" * 50)
    print(f"State: entropy={test_state['entropy']}, depth={test_state['consciousness_depth']}, mood={test_state['mood']}")
    print()
    
    # Collect thoughts to check for variety
    thoughts = []
    thought_counts = {}
    
    for i in range(15):
        # Add small delay to ensure different random state
        time.sleep(0.01)
        
        thought = talk_to(test_state)
        thoughts.append(thought)
        
        # Count occurrences
        thought_counts[thought] = thought_counts.get(thought, 0) + 1
        
        print(f"{i+1:2d}. {thought}")
    
    print()
    print("📊 Selection Statistics:")
    print(f"   Total selections: {len(thoughts)}")
    print(f"   Unique thoughts: {len(thought_counts)}")
    print(f"   Variety ratio: {len(thought_counts)/len(thoughts):.2f}")
    print()
    
    print("🔢 Thought frequency:")
    for thought, count in sorted(thought_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(thoughts)) * 100
        print(f"   {count:2d}x ({percentage:4.1f}%) {thought[:60]}{'...' if len(thought) > 60 else ''}")

if __name__ == "__main__":
    test_selection_variety() 