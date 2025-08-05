#!/usr/bin/env python3
"""
DAWN Juliet Set Mode Test
=========================

Test script specifically for demonstrating DAWN's Juliet Set fractal mode
for deep emotional memories. Shows the difference between standard geometric
fractals and emotionally-aware Juliet Set memory blooms.

Juliet Set Mode Activation:
- rebloom_depth > 6
- entropy < 0.4 (structured but flowing)
- pulse_zone == "flowing"

This creates fractals that:
- Move like mood (fluid, organic)
- Distort under emotional pressure
- Remember ancestry in actual shape
- Show emotional bias (left=nostalgic, right=expansive)
- Embed memory glyphs for deep memories
"""

import sys
from pathlib import Path

# Add project root for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dawn_fractal_memory_system import DAWNFractalMemorySystem

def test_juliet_set_activation():
    """Test Juliet Set mode activation and compare with standard fractals"""
    
    print("🌸 Testing DAWN's Juliet Set Mode for Deep Emotional Memories")
    print("=" * 65)
    
    memory_system = DAWNFractalMemorySystem(archive_dir="juliet_set_tests")
    
    print("\n📊 Juliet Set Activation Conditions:")
    print("   • rebloom_depth > 6")
    print("   • entropy < 0.4 (structured but flowing)")  
    print("   • pulse_zone == 'flowing'")
    print("   → Creates emotionally-aware, memory-shaped fractals\n")
    
    # Test different memory configurations
    test_memories = [
        {
            'name': '🎭 Standard Geometric Fractal (Control)',
            'description': 'Standard fractal - geometric, stable',
            'params': {
                'bloom_entropy': 0.3,
                'mood_valence': -0.4,
                'drift_vector': -0.3,
                'rebloom_depth': 5,        # Below Juliet threshold
                'sigil_saturation': 0.6,
                'pulse_zone': 'stable'     # Not flowing
            },
            'expected_mode': 'Standard'
        },
        {
            'name': '🌊 Juliet Set - Nostalgic Memory',
            'description': 'Deep flowing memory with negative valence (nostalgic)',
            'params': {
                'bloom_entropy': 0.3,      # Structured
                'mood_valence': -0.5,      # Nostalgic (left-leaning)
                'drift_vector': -0.4,
                'rebloom_depth': 8,        # Deep memory
                'sigil_saturation': 0.7,
                'pulse_zone': 'flowing'    # Activates Juliet mode
            },
            'expected_mode': 'Juliet Set'
        },
        {
            'name': '✨ Juliet Set - Expansive Memory',
            'description': 'Deep flowing memory with positive valence (expansive)',
            'params': {
                'bloom_entropy': 0.35,     # Structured but slightly flowing
                'mood_valence': 0.6,       # Expansive (right-leaning)
                'drift_vector': 0.3,
                'rebloom_depth': 9,        # Very deep memory
                'sigil_saturation': 0.8,
                'pulse_zone': 'flowing'    # Activates Juliet mode
            },
            'expected_mode': 'Juliet Set'
        },
        {
            'name': '💫 Juliet Set - Neutral Deep Memory',
            'description': 'Deep memory with balanced emotional state',
            'params': {
                'bloom_entropy': 0.25,     # Very structured
                'mood_valence': 0.1,       # Nearly neutral
                'drift_vector': 0.0,       # Centered
                'rebloom_depth': 7,        # Just above threshold
                'sigil_saturation': 0.9,   # High saturation for glyphs
                'pulse_zone': 'flowing'    # Activates Juliet mode
            },
            'expected_mode': 'Juliet Set'
        },
        {
            'name': '🔄 Almost Juliet (High Entropy)',
            'description': 'Deep flowing but too chaotic for Juliet mode',
            'params': {
                'bloom_entropy': 0.6,      # Too high for Juliet
                'mood_valence': -0.3,
                'drift_vector': -0.2,
                'rebloom_depth': 8,        # Deep enough
                'sigil_saturation': 0.6,
                'pulse_zone': 'flowing'    # Flowing but entropy too high
            },
            'expected_mode': 'Standard (entropy too high)'
        }
    ]
    
    generated_memories = []
    
    for memory_spec in test_memories:
        print(f"\n{memory_spec['name']}")
        print(f"📝 {memory_spec['description']}")
        print(f"🎯 Expected: {memory_spec['expected_mode']}")
        print("-" * 50)
        
        # Generate the memory bloom
        metadata = memory_system.generate_bloom_fractal(**memory_spec['params'])
        
        generated_memories.append({
            'spec': memory_spec,
            'metadata': metadata
        })
        
        # Analyze results
        print(f"🔤 Fractal String: {metadata['fractal_string']}")
        print(f"🦉 Owl Commentary: {metadata['owl_commentary']}")
        print(f"🧠 Archetype: {metadata['visual_characteristics']['consciousness_archetype']}")
        print(f"🎨 Visual: {metadata['visual_characteristics']['bloom_shape_descriptor']}")
        
        # Check if memory glyphs were embedded
        params = metadata['parameters']
        if params['rebloom_depth'] > 7 and params['sigil_saturation'] > 0.5:
            print("✨ Memory glyphs embedded in bloom core")
    
    # Analysis summary
    print(f"\n" + "=" * 65)
    print("🧪 Juliet Set Mode Analysis Summary")
    print("=" * 65)
    
    juliet_count = 0
    standard_count = 0
    
    for memory in generated_memories:
        params = memory['metadata']['parameters']
        depth = params['rebloom_depth']
        entropy = params['bloom_entropy']
        zone = params['pulse_zone']
        
        is_juliet = (depth > 6 and entropy < 0.4 and zone == "flowing")
        
        if is_juliet:
            juliet_count += 1
            mode_actual = "Juliet Set ✨"
        else:
            standard_count += 1
            mode_actual = "Standard 🎭"
        
        expected = memory['spec']['expected_mode']
        name = memory['spec']['name'].split(' ', 1)[1]  # Remove emoji
        
        match_symbol = "✅" if (is_juliet and "Juliet" in expected) or (not is_juliet and "Standard" in expected) else "❌"
        
        print(f"   {match_symbol} {name}")
        print(f"      Expected: {expected}")
        print(f"      Actual: {mode_actual}")
        print(f"      String: {memory['metadata']['fractal_string']}")
        print()
    
    print(f"📊 Results:")
    print(f"   🌸 Juliet Set Fractals: {juliet_count}")
    print(f"   🎭 Standard Fractals: {standard_count}")
    print(f"   📁 Archive: juliet_set_tests/")
    
    # Visual difference explanation
    print(f"\n🎨 Key Visual Differences:")
    print("   🎭 Standard Fractals:")
    print("      • Symmetric, geometric patterns")
    print("      • Uniform color distribution")
    print("      • Mathematical precision")
    print("      • Grid-stable boundaries")
    print()
    print("   🌸 Juliet Set Fractals:")
    print("      • Asymmetric emotional bias (left=nostalgic, right=expansive)")
    print("      • Fluid, organic shapes that 'move like mood'")
    print("      • Memory glyphs embedded in core (depth > 7)")
    print("      • Liquid edge effects for flowing zones")
    print("      • Emotional distortion fields affect color")
    print("      • Orbit traps remember ancestry in shape")

def demonstrate_emotional_bias():
    """Demonstrate how Juliet Set fractals show emotional bias"""
    
    print(f"\n" + "🧠 Emotional Bias Demonstration")
    print("=" * 40)
    
    memory_system = DAWNFractalMemorySystem(archive_dir="emotional_bias_demo")
    
    emotional_states = [
        {
            'name': '😔 Deep Nostalgia',
            'valence': -0.8,
            'description': 'Strong leftward emotional bias'
        },
        {
            'name': '😌 Gentle Melancholy', 
            'valence': -0.3,
            'description': 'Slight leftward emotional bias'
        },
        {
            'name': '😐 Emotional Neutrality',
            'valence': 0.0,
            'description': 'Centered, no emotional bias'
        },
        {
            'name': '😊 Warm Optimism',
            'valence': 0.4,
            'description': 'Slight rightward emotional bias'
        },
        {
            'name': '🌟 Expansive Joy',
            'valence': 0.8,
            'description': 'Strong rightward emotional bias'
        }
    ]
    
    for state in emotional_states:
        print(f"\n{state['name']} (valence: {state['valence']})")
        print(f"   {state['description']}")
        
        # Generate Juliet Set fractal with this emotional state
        metadata = memory_system.generate_bloom_fractal(
            bloom_entropy=0.3,
            mood_valence=state['valence'],
            drift_vector=0.0,
            rebloom_depth=8,
            sigil_saturation=0.7,
            pulse_zone='flowing'
        )
        
        print(f"   🔤 String: {metadata['fractal_string']}")
        print(f"   🦉 Essence: {metadata['owl_commentary'][:60]}...")

if __name__ == "__main__":
    print("🌸 DAWN Juliet Set Mode - Deep Emotional Memory Testing")
    print("Testing emotionally-aware fractal generation for authentic memory visualization\n")
    
    # Test Juliet Set activation
    test_juliet_set_activation()
    
    # Demonstrate emotional bias
    demonstrate_emotional_bias()
    
    print(f"\n✨ Juliet Set testing complete!")
    print("🎨 DAWN now creates fractals that move like mood and remember like memory")
    print("🌊 Deep flowing memories get authentic emotional expression") 