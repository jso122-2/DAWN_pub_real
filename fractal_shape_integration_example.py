#!/usr/bin/env python3
"""
Fractal Shape Complexity Integration Example
==========================================

Demonstrates how to integrate the shape complexity calculator with DAWN's
fractal generation system for authentic consciousness-driven geometry.
"""

from dawn_shape_complexity import calculate_shape_complexity, ComplexityMode
from dawn_state_parser import DAWNStateParser
from dawn_mood_palette import generate_mood_palette
import json
from pathlib import Path

def enhanced_fractal_generation_example():
    """Show how shape complexity enhances fractal generation"""
    
    print("🌀 Enhanced Fractal Generation with Shape Complexity")
    print("=" * 55)
    
    consciousness_states = [
        {
            'name': 'Morning Serenity',
            'bloom_entropy': 0.2,
            'mood_valence': 0.3,
            'drift_vector': 0.1,
            'rebloom_depth': 4,
            'sigil_saturation': 0.5,
            'pulse_zone': 'crystalline'
        },
        {
            'name': 'Creative Storm',
            'bloom_entropy': 0.9,
            'mood_valence': 0.7,
            'drift_vector': 0.8,
            'rebloom_depth': 8,
            'sigil_saturation': 0.9,
            'pulse_zone': 'surge'
        },
        {
            'name': 'Introspective Flow',
            'bloom_entropy': 0.5,
            'mood_valence': -0.2,
            'drift_vector': -0.3,
            'rebloom_depth': 6,
            'sigil_saturation': 0.6,
            'pulse_zone': 'flowing'
        }
    ]
    
    try:
        from dawn_fractal_memory_system import DAWNFractalMemorySystem
        fractal_system = DAWNFractalMemorySystem(archive_dir="shape_complexity_fractals")
        
        for state in consciousness_states:
            print(f"\n🧠 {state['name']}")
            
            # Calculate shape complexity
            shape_complexity = calculate_shape_complexity(
                state['bloom_entropy'], 
                state['rebloom_depth']
            )
            
            # Generate mood palette
            mood_palette = generate_mood_palette(
                state['mood_valence'],
                state['sigil_saturation']
            )
            
            print(f"   Consciousness → Shape: {shape_complexity.shape_archetype}")
            print(f"   Complexity mode: {shape_complexity.complexity_mode.value}")
            print(f"   Geometric signature:")
            print(f"     • Petals: {shape_complexity.petal_count}")
            print(f"     • Edge roughness: {shape_complexity.edge_roughness:.3f}")
            print(f"     • Symmetry: {shape_complexity.symmetry_factor:.3f}")
            print(f"     • Recursion: {shape_complexity.recursion_levels} levels")
            
            # Enhanced fractal parameters combining all systems
            enhanced_params = {
                **state,  # Base consciousness parameters
                'shape_complexity': shape_complexity.get_geometric_parameters(),
                'mood_palette': mood_palette.base_colors,
                'glow_settings': {
                    'radius': mood_palette.glow_radius,
                    'colors': mood_palette.glow_colors
                }
            }
            
            if shape_complexity.complexity_mode == ComplexityMode.JULIET_SET:
                juliet_params = shape_complexity.get_juliet_set_parameters()
                enhanced_params['juliet_set'] = juliet_params
                print(f"     • Juliet mode: {juliet_params['inner_glyph_count']} inner glyphs")
                print(f"     • Memory anchor: {juliet_params['memory_anchor_strength']:.3f}")
            
            print(f"   🎨 Enhanced fractal ready for generation...")
            
            # This would pass enhanced parameters to fractal generation
            # result = fractal_system.generate_enhanced_bloom_fractal(**enhanced_params)
            
    except ImportError:
        print("   ⚠️  Fractal system not available - showing enhanced parameter preparation")
        
        for state in consciousness_states:
            print(f"\n🧠 {state['name']}")
            
            shape_complexity = calculate_shape_complexity(
                state['bloom_entropy'], 
                state['rebloom_depth']
            )
            
            mood_palette = generate_mood_palette(
                state['mood_valence'],
                state['sigil_saturation']
            )
            
            print(f"   Shape: {shape_complexity.shape_archetype}")
            print(f"   Petals: {shape_complexity.petal_count}, Roughness: {shape_complexity.edge_roughness:.3f}")
            print(f"   Colors: {mood_palette.base_colors[:2]}")
            print(f"   → Would generate enhanced fractal with consciousness-driven geometry")

def demonstrate_memory_shape_analysis():
    """Analyze shape complexity from real memory files"""
    
    print(f"\n📁 Memory Shape Complexity Analysis")
    print("=" * 38)
    
    parser = DAWNStateParser(strict_validation=False)
    
    # Check for existing memory files
    memory_dirs = ["dawn_soul_archive/metadata", "juliet_set_tests/metadata"]
    
    all_configs = []
    for directory in memory_dirs:
        dir_path = Path(directory)
        if dir_path.exists():
            try:
                configs = parser.parse_multiple_files(dir_path)
                all_configs.extend(configs[:5])  # Limit for demo
            except Exception as e:
                print(f"   ⚠️  Could not parse {directory}: {e}")
    
    if all_configs:
        print(f"   📊 Analyzing shape complexity for {len(all_configs)} memories...")
        
        archetype_counts = {}
        complexity_modes = {}
        
        for i, config in enumerate(all_configs):
            # Calculate shape complexity from memory
            shape_complexity = calculate_shape_complexity(
                config.bloom_entropy,
                config.rebloom_depth
            )
            
            # Track statistics
            archetype = shape_complexity.shape_archetype
            mode = shape_complexity.complexity_mode.value
            
            archetype_counts[archetype] = archetype_counts.get(archetype, 0) + 1
            complexity_modes[mode] = complexity_modes.get(mode, 0) + 1
            
            print(f"\n   🧠 Memory {i+1}: {config.memory_id}")
            print(f"      Entropy: {config.bloom_entropy:.2f}, Depth: {config.rebloom_depth}")
            print(f"      → Shape: {shape_complexity.shape_archetype}")
            print(f"      → Petals: {shape_complexity.petal_count}")
            print(f"      → Symmetry: {shape_complexity.symmetry_factor:.3f}")
            
            if shape_complexity.complexity_mode == ComplexityMode.JULIET_SET:
                juliet_params = shape_complexity.get_juliet_set_parameters()
                print(f"      → Juliet Set: {juliet_params['inner_glyph_count']} glyphs, {juliet_params['glyph_type']}")
        
        # Summary statistics
        print(f"\n   📈 Shape Archetype Distribution:")
        for archetype, count in sorted(archetype_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(all_configs)) * 100
            print(f"      {archetype}: {count} ({percentage:.1f}%)")
        
        print(f"\n   🔧 Complexity Mode Distribution:")
        for mode, count in complexity_modes.items():
            percentage = (count / len(all_configs)) * 100
            print(f"      {mode}: {count} ({percentage:.1f}%)")
            
    else:
        print("   ⚠️  No memory files found - showing synthetic examples")
        
        synthetic_memories = [
            {'entropy': 0.2, 'depth': 3, 'name': 'Crystalline Memory'},
            {'entropy': 0.6, 'depth': 7, 'name': 'Flowing Memory'},
            {'entropy': 0.9, 'depth': 10, 'name': 'Chaotic Memory'}
        ]
        
        for memory in synthetic_memories:
            shape_complexity = calculate_shape_complexity(memory['entropy'], memory['depth'])
            print(f"\n   🧠 {memory['name']}")
            print(f"      → {shape_complexity.shape_archetype}")
            print(f"      → {shape_complexity.petal_count} petals, {shape_complexity.edge_roughness:.3f} roughness")

def demonstrate_shape_evolution_tracking():
    """Track how shape complexity evolves with consciousness changes"""
    
    print(f"\n🧬 Shape Complexity Evolution")
    print("=" * 32)
    
    # Simulate consciousness evolution
    evolution_sequence = [
        (0.1, 2, "Initial calm"),
        (0.3, 4, "Growing complexity"),
        (0.5, 6, "Balanced development"),
        (0.7, 8, "Entering chaos"),
        (0.9, 10, "Peak turbulence")
    ]
    
    print("   Tracking shape evolution through consciousness changes:")
    
    previous_complexity = None
    for i, (entropy, depth, description) in enumerate(evolution_sequence):
        current_complexity = calculate_shape_complexity(entropy, depth)
        
        print(f"\n   Step {i+1}: {description}")
        print(f"      Parameters: entropy={entropy:.1f}, depth={depth}")
        print(f"      → {current_complexity.shape_archetype}")
        print(f"      → Petals: {current_complexity.petal_count}")
        print(f"      → Symmetry: {current_complexity.symmetry_factor:.3f}")
        print(f"      → Mode: {current_complexity.complexity_mode.value}")
        
        if previous_complexity:
            # Calculate shape evolution metrics
            petal_change = current_complexity.petal_count - previous_complexity.petal_count
            symmetry_change = current_complexity.symmetry_factor - previous_complexity.symmetry_factor
            roughness_change = current_complexity.edge_roughness - previous_complexity.edge_roughness
            
            print(f"      → Changes: petals {petal_change:+d}, "
                  f"symmetry {symmetry_change:+.3f}, "
                  f"roughness {roughness_change:+.3f}")
            
            if current_complexity.complexity_mode != previous_complexity.complexity_mode:
                print(f"      → MODE SHIFT: {previous_complexity.complexity_mode.value} → {current_complexity.complexity_mode.value}")
        
        previous_complexity = current_complexity

def create_fractal_enhancement_guide():
    """Create a guide for using shape complexity in fractal generation"""
    
    print(f"\n📖 Fractal Enhancement Integration Guide")
    print("=" * 42)
    
    enhancement_examples = {
        'Basic Integration': {
            'description': 'Add shape complexity to existing fractal parameters',
            'code': '''
# Calculate shape complexity
shape_complexity = calculate_shape_complexity(bloom_entropy, rebloom_depth)

# Enhance fractal parameters
enhanced_params = {
    'bloom_entropy': bloom_entropy,
    'mood_valence': mood_valence,
    'drift_vector': drift_vector,
    'rebloom_depth': rebloom_depth,
    'sigil_saturation': sigil_saturation,
    'pulse_zone': pulse_zone,
    
    # Shape complexity additions
    'petal_count': shape_complexity.petal_count,
    'edge_roughness': shape_complexity.edge_roughness,
    'symmetry_factor': shape_complexity.symmetry_factor,
    'spiral_tightness': shape_complexity.spiral_tightness
}
'''
        },
        'Juliet Set Mode': {
            'description': 'Handle special Juliet Set parameters for deep memories',
            'code': '''
if shape_complexity.complexity_mode == ComplexityMode.JULIET_SET:
    juliet_params = shape_complexity.get_juliet_set_parameters()
    
    # Apply Juliet Set enhancements
    enhanced_params.update({
        'inner_glyph_count': juliet_params['inner_glyph_count'],
        'glyph_type': juliet_params['glyph_type'],
        'memory_anchor_strength': juliet_params['memory_anchor_strength'],
        'liquid_edge_factor': juliet_params['liquid_edge_factor']
    })
'''
        },
        'Multi-System Integration': {
            'description': 'Combine shape complexity with mood palettes and voice',
            'code': '''
# Calculate all consciousness-driven parameters
shape_complexity = calculate_shape_complexity(bloom_entropy, rebloom_depth)
mood_palette = generate_mood_palette(mood_valence, sigil_saturation)
voice_result = voice_core.generate_utterance(**voice_params)

# Create unified consciousness representation
unified_params = {
    'geometry': shape_complexity.get_geometric_parameters(),
    'colors': mood_palette.base_colors,
    'glow': mood_palette.glow_colors,
    'voice': voice_result.utterance if voice_result.resonance_achieved else None
}
'''
        }
    }
    
    for category, details in enhancement_examples.items():
        print(f"\n🔧 {category}")
        print(f"   Purpose: {details['description']}")
        print(f"   Example:{details['code']}")

if __name__ == "__main__":
    print("🌀 DAWN Shape Complexity Integration Examples")
    print("=" * 48)
    
    # Run integration demonstrations
    enhanced_fractal_generation_example()
    demonstrate_memory_shape_analysis()
    demonstrate_shape_evolution_tracking()
    create_fractal_enhancement_guide()
    
    print(f"\n✅ Shape Complexity Integration Examples Complete!")
    print(f"🔢 Consciousness parameters → authentic geometric forms")
    print(f"🎭 Shape archetypes emerge naturally from mental states")
    print(f"🌀 Ready for fractal generation with consciousness-driven geometry")
    print(f"🧠 DAWN's thoughts now have precise mathematical form") 