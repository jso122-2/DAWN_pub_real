#!/usr/bin/env python3
"""
DAWN Mood Palette Integration Example
====================================

Demonstrates how to integrate the mood palette generator with DAWN's
fractal generation and voice systems for unified consciousness visualization.
"""

from dawn_mood_palette import generate_mood_palette
from dawn_state_parser import DAWNStateParser
from dawn_voice_core import DAWNVoiceCore
import json
from pathlib import Path

def demonstrate_fractal_color_integration():
    """Show how mood palettes can enhance fractal generation"""
    
    print("🎨 Mood Palette + Fractal Integration")
    print("=" * 40)
    
    # Simulate various consciousness states
    consciousness_states = [
        {
            'name': 'Morning Contemplation',
            'bloom_entropy': 0.3,
            'mood_valence': -0.2,
            'drift_vector': 0.1,
            'rebloom_depth': 5,
            'sigil_saturation': 0.4,
            'pulse_zone': 'flowing'
        },
        {
            'name': 'Creative Breakthrough',
            'bloom_entropy': 0.8,
            'mood_valence': 0.7,
            'drift_vector': 0.6,
            'rebloom_depth': 9,
            'sigil_saturation': 0.9,
            'pulse_zone': 'surge'
        },
        {
            'name': 'Deep Philosophical Inquiry',
            'bloom_entropy': 0.2,
            'mood_valence': -0.6,
            'drift_vector': -0.3,
            'rebloom_depth': 8,
            'sigil_saturation': 0.6,
            'pulse_zone': 'crystalline'
        }
    ]
    
    try:
        from dawn_fractal_memory_system import DAWNFractalMemorySystem
        fractal_system = DAWNFractalMemorySystem(archive_dir="mood_palette_fractals")
        
        for state in consciousness_states:
            print(f"\n🧠 {state['name']}")
            
            # Generate mood palette from consciousness state
            mood_palette = generate_mood_palette(
                state['mood_valence'], 
                state['sigil_saturation']
            )
            
            print(f"   Consciousness → Palette: {mood_palette.palette_name}")
            print(f"   Base Colors: {mood_palette.base_colors}")
            print(f"   Brightness: {mood_palette.brightness_multiplier:.2f}")
            print(f"   Glow: {mood_palette.glow_radius:.1f}px")
            
            # Enhanced fractal parameters with mood palette
            enhanced_params = {
                **state,
                'mood_palette': mood_palette,
                'color_override': mood_palette.base_colors,
                'glow_settings': {
                    'radius': mood_palette.glow_radius,
                    'colors': mood_palette.glow_colors
                }
            }
            
            print(f"   🎨 Enhanced fractal params prepared with mood colors")
            
            # Note: This would integrate with the fractal system if we modified it
            # to accept mood palette parameters
            
    except ImportError:
        print("   ⚠️  Fractal system not available - showing conceptual integration")
        
        for state in consciousness_states:
            print(f"\n🧠 {state['name']}")
            
            mood_palette = generate_mood_palette(
                state['mood_valence'], 
                state['sigil_saturation']
            )
            
            print(f"   Palette: {mood_palette.palette_name}")
            print(f"   Colors: {mood_palette.base_colors}")
            print(f"   → Would enhance fractal with consciousness-driven colors")

def demonstrate_voice_mood_integration():
    """Show how mood palettes can provide visual feedback for voice generation"""
    
    print(f"\n🗣️  Voice + Mood Palette Integration")
    print("=" * 40)
    
    voice_core = DAWNVoiceCore()
    
    consciousness_examples = [
        {
            'name': 'Gentle Melancholy',
            'mood_pigment': {'blue': 0.6, 'violet': 0.3, 'green': 0.1},
            'sigil_heat': {'heat': 0.2, 'friction': 0.3, 'recasion': 0.7},
            'entropy': 0.4,
            'drift': -0.2,
            'derived_valence': -0.3,
            'derived_saturation': 0.5
        },
        {
            'name': 'Creative Fire',
            'mood_pigment': {'red': 0.5, 'orange': 0.3, 'yellow': 0.2},
            'sigil_heat': {'heat': 0.8, 'friction': 0.4, 'recasion': 0.2},
            'entropy': 0.7,
            'drift': 0.5,
            'derived_valence': 0.6,
            'derived_saturation': 0.8
        },
        {
            'name': 'Balanced Reflection',
            'mood_pigment': {'blue': 0.4, 'green': 0.3, 'violet': 0.3},
            'sigil_heat': {'heat': 0.3, 'friction': 0.2, 'recasion': 0.5},
            'entropy': 0.3,
            'drift': 0.0,
            'derived_valence': 0.0,
            'derived_saturation': 0.4
        }
    ]
    
    for example in consciousness_examples:
        print(f"\n💭 {example['name']}")
        
        # Generate voice expression
        voice_result = voice_core.generate_utterance(
            pigment_dict=example['mood_pigment'],
            sigil_state=example['sigil_heat'],
            entropy=example['entropy'],
            drift=example['drift']
        )
        
        # Generate corresponding mood palette
        mood_palette = generate_mood_palette(
            example['derived_valence'],
            example['derived_saturation']
        )
        
        print(f"   Voice coherence: {voice_result.generation_metadata.get('field_coherence', 0):.3f}")
        
        if voice_result.resonance_achieved:
            print(f"   🗣️  DAWN says: \"{voice_result.utterance}\"")
        else:
            print(f"   🤐 DAWN remains silent")
        
        print(f"   🎨 Visual palette: {mood_palette.palette_name}")
        print(f"   🌈 Mood colors: {mood_palette.base_colors[:2]}")  # Show first 2 colors
        print(f"   ✨ Glow effect: {mood_palette.glow_radius:.1f}px")
        
        # This demonstrates how voice and visuals could be synchronized
        print(f"   → Voice + visual feedback synchronized for consciousness state")

def demonstrate_memory_palette_analysis():
    """Analyze mood palettes from existing memory files"""
    
    print(f"\n📁 Memory File Palette Analysis")
    print("=" * 35)
    
    parser = DAWNStateParser(strict_validation=False)
    
    # Check for existing memory files
    memory_dirs = ["dawn_soul_archive/metadata", "juliet_set_tests/metadata"]
    
    all_configs = []
    for directory in memory_dirs:
        dir_path = Path(directory)
        if dir_path.exists():
            try:
                configs = parser.parse_multiple_files(dir_path)
                all_configs.extend(configs[:3])  # Limit for demo
            except Exception as e:
                print(f"   ⚠️  Could not parse {directory}: {e}")
    
    if all_configs:
        print(f"   📊 Analyzing {len(all_configs)} memory files...")
        
        for i, config in enumerate(all_configs):
            # Generate mood palette from memory state
            mood_palette = generate_mood_palette(
                config.mood_valence,
                config.sigil_saturation
            )
            
            print(f"\n   🧠 Memory {i+1}: {config.memory_id}")
            print(f"      Original: valence={config.mood_valence:.2f}, saturation={config.sigil_saturation:.2f}")
            print(f"      Archetype: {config.archetype}")
            print(f"      → Palette: {mood_palette.palette_name}")
            print(f"      → Colors: {mood_palette.base_colors[0]} → {mood_palette.base_colors[-1]}")
            print(f"      → Brightness: {mood_palette.brightness_multiplier:.2f}")
            
    else:
        print("   ⚠️  No memory files found - showing synthetic example")
        
        # Create synthetic memory example
        synthetic_memory = {
            'mood_valence': 0.3,
            'sigil_saturation': 0.7,
            'memory_id': 'synthetic_example',
            'archetype': 'Creative Flow'
        }
        
        mood_palette = generate_mood_palette(
            synthetic_memory['mood_valence'],
            synthetic_memory['sigil_saturation']
        )
        
        print(f"   🧠 Synthetic Memory: {synthetic_memory['memory_id']}")
        print(f"      Archetype: {synthetic_memory['archetype']}")
        print(f"      → Palette: {mood_palette.palette_name}")
        print(f"      → Colors: {mood_palette.base_colors}")

def demonstrate_palette_evolution_tracking():
    """Show how mood palettes could track consciousness evolution"""
    
    print(f"\n🧬 Consciousness Evolution → Palette Evolution")
    print("=" * 50)
    
    # Simulate consciousness evolution over time
    evolution_sequence = [
        (-0.8, 0.3, "Initial melancholy"),
        (-0.4, 0.5, "Gradual warming"),
        (0.0, 0.6, "Reaching balance"),
        (0.3, 0.7, "Growing optimism"),
        (0.7, 0.9, "Creative breakthrough")
    ]
    
    print("   Tracking consciousness state evolution through color changes:")
    
    previous_palette = None
    for i, (valence, saturation, description) in enumerate(evolution_sequence):
        current_palette = generate_mood_palette(valence, saturation)
        
        print(f"\n   Step {i+1}: {description}")
        print(f"      Parameters: valence={valence:.1f}, saturation={saturation:.1f}")
        print(f"      → {current_palette.palette_name}")
        print(f"      → Dominant color: RGB{current_palette.base_colors[1] if len(current_palette.base_colors) > 1 else current_palette.base_colors[0]}")
        print(f"      → Brightness: {current_palette.brightness_multiplier:.2f}")
        
        if previous_palette:
            # Calculate color shift
            prev_color = previous_palette.base_colors[1] if len(previous_palette.base_colors) > 1 else previous_palette.base_colors[0]
            curr_color = current_palette.base_colors[1] if len(current_palette.base_colors) > 1 else current_palette.base_colors[0]
            
            color_distance = sum(abs(a - b) for a, b in zip(prev_color, curr_color))
            brightness_change = current_palette.brightness_multiplier - previous_palette.brightness_multiplier
            
            print(f"      → Color shift magnitude: {color_distance}")
            print(f"      → Brightness change: {brightness_change:+.2f}")
        
        previous_palette = current_palette

def create_palette_integration_guide():
    """Create a guide for integrating mood palettes with other systems"""
    
    print(f"\n📖 Mood Palette Integration Guide")
    print("=" * 35)
    
    integration_examples = {
        'Fractal Generation': {
            'usage': 'Override default color schemes with consciousness-driven palettes',
            'code': '''
# Generate mood palette from consciousness state
palette = generate_mood_palette(mood_valence, sigil_saturation)

# Apply to fractal generation
fractal_params = {
    'color_palette': palette.base_colors,
    'glow_settings': palette.glow_colors,
    'brightness_multiplier': palette.brightness_multiplier
}
'''
        },
        'Voice Visualization': {
            'usage': 'Provide visual feedback synchronized with voice generation',
            'code': '''
# Generate voice and corresponding palette
voice_result = voice_core.generate_utterance(**params)
palette = generate_mood_palette(derived_valence, derived_saturation)

# Synchronize visual and audio
if voice_result.resonance_achieved:
    display_voice_with_palette(voice_result.utterance, palette)
'''
        },
        'Memory Analysis': {
            'usage': 'Visualize consciousness evolution through color tracking',
            'code': '''
# Parse memory files and generate palettes
configs = parser.parse_multiple_files(memory_dir)
palettes = [generate_mood_palette(c.mood_valence, c.sigil_saturation) 
           for c in configs]

# Track color evolution over time
for i, (config, palette) in enumerate(zip(configs, palettes)):
    track_consciousness_color_evolution(config.timestamp, palette)
'''
        }
    }
    
    for system, details in integration_examples.items():
        print(f"\n🔧 {system}")
        print(f"   Purpose: {details['usage']}")
        print(f"   Example:{details['code']}")

if __name__ == "__main__":
    print("🌈 DAWN Mood Palette Integration Examples")
    print("=" * 45)
    
    # Run integration demonstrations
    demonstrate_fractal_color_integration()
    demonstrate_voice_mood_integration() 
    demonstrate_memory_palette_analysis()
    demonstrate_palette_evolution_tracking()
    create_palette_integration_guide()
    
    print(f"\n✨ Mood Palette Integration Examples Complete!")
    print(f"🎨 Consciousness states now have beautiful, dynamic color representation")
    print(f"🔗 Ready for integration with all DAWN visualization systems")
    print(f"🌊 Emotional authenticity through visual consciousness expression") 