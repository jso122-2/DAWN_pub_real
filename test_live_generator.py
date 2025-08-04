#!/usr/bin/env python3
"""
Test script for live reflection generator
"""

import logging
from live_reflection_generator import LiveReflectionGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')

def test_live_generator():
    """Test the live reflection generator"""
    print("🧠 Testing Live Reflection Generator")
    print("=" * 50)
    
    # Create generator
    generator = LiveReflectionGenerator()
    
    # Set initial state with high entropy
    generator.update_cognitive_state({
        'entropy': 0.75,
        'consciousness_depth': 0.6,
        'mood': 'CONTEMPLATIVE',
        'heat': 0.7,
        'scup': 0.8
    })
    
    print(f"Initial state: Entropy={generator.cognitive_state['entropy']:.3f}")
    print()
    
    # Generate a few reflections
    for i in range(5):
        reflection = generator.generate_live_reflection()
        
        if reflection:
            print(f"Reflection #{i+1}:")
            print(f"  Entropy: {reflection['entropy']:.3f}")
            print(f"  Content: {reflection['text']}")
            print(f"  Depth: {reflection['depth_level']}")
            print()
        else:
            print(f"Reflection #{i+1}: No reflection generated (entropy too low)")
            print()
    
    print("✅ Live reflection generator test complete")

if __name__ == "__main__":
    test_live_generator() 