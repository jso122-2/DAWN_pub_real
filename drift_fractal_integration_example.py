#!/usr/bin/env python3
"""
Drift Transformation + Fractal Integration Example
==================================================

Demonstrates how to integrate drift transformation with DAWN's fractal generation
system for authentic consciousness-driven movement and visual dynamics.
"""

from dawn_drift_transformation import apply_drift_transformation, create_animated_sequence
from dawn_shape_complexity import calculate_shape_complexity
from dawn_mood_palette import generate_mood_palette
from dawn_state_parser import DAWNStateParser
import numpy as np
import math
from pathlib import Path

def demonstrate_enhanced_fractal_generation():
    """Show how drift transformation enhances fractal generation"""
    
    print("🌊 Enhanced Fractal Generation with Drift Transformation")
    print("=" * 58)
    
    consciousness_states = [
        {
            'name': 'Drifting Contemplation',
            'bloom_entropy': 0.3,
            'mood_valence': -0.1,
            'drift_vector': -0.6,
            'rebloom_depth': 5,
            'sigil_saturation': 0.4,
            'pulse_zone': 'calm'
        },
        {
            'name': 'Surging Innovation',
            'bloom_entropy': 0.8,
            'mood_valence': 0.6,
            'drift_vector': 0.9,
            'rebloom_depth': 9,
            'sigil_saturation': 0.9,
            'pulse_zone': 'surge'
        },
        {
            'name': 'Fragile Memories',
            'bloom_entropy': 0.4,
            'mood_valence': -0.5,
            'drift_vector': -0.3,
            'rebloom_depth': 7,
            'sigil_saturation': 0.3,
            'pulse_zone': 'fragile'
        },
        {
            'name': 'Flowing Inspiration',
            'bloom_entropy': 0.6,
            'mood_valence': 0.4,
            'drift_vector': 0.5,
            'rebloom_depth': 6,
            'sigil_saturation': 0.7,
            'pulse_zone': 'flowing'
        }
    ]
    
    try:
        from dawn_fractal_memory_system import DAWNFractalMemorySystem
        fractal_system = DAWNFractalMemorySystem(archive_dir="drift_enhanced_fractals")
        
        for state in consciousness_states:
            print(f"\n🧠 {state['name']}")
            
            # Calculate all consciousness components
            shape_complexity = calculate_shape_complexity(
                state['bloom_entropy'], state['rebloom_depth']
            )
            
            mood_palette = generate_mood_palette(
                state['mood_valence'], state['sigil_saturation']
            )
            
            # Create base fractal coordinates (using shape complexity)
            petal_count = shape_complexity.petal_count
            angles = np.linspace(0, 2*math.pi, petal_count * 4, endpoint=False)
            base_radius = 1.0 + 0.3 * np.sin(angles * petal_count / 2)  # Petal modulation
            base_coords = np.column_stack([
                base_radius * np.cos(angles),
                base_radius * np.sin(angles)
            ])
            
            # Apply drift transformation
            drift_transformation = apply_drift_transformation(
                base_coords, 
                state['drift_vector'], 
                state['pulse_zone']
            )
            
            print(f"   Consciousness Analysis:")
            print(f"     • Shape: {shape_complexity.shape_archetype}")
            print(f"     • Petals: {shape_complexity.petal_count}")
            print(f"     • Symmetry: {shape_complexity.symmetry_factor:.3f}")
            print(f"     • Colors: {mood_palette.palette_name}")
            print(f"     • Drift: ({drift_transformation.center_offset[0]:+.3f}, {drift_transformation.center_offset[1]:+.3f})")
            print(f"     • Rotation: {math.degrees(drift_transformation.rotation_angle):+.1f}°")
            print(f"     • Pulse: {state['pulse_zone']} dynamics")
            
            # Enhanced fractal parameters
            enhanced_params = {
                **state,  # Base consciousness parameters
                'drift_transformation': {
                    'center_offset': drift_transformation.center_offset,
                    'rotation_angle': drift_transformation.rotation_angle,
                    'transformed_coords': drift_transformation.transformed_coords.tolist(),
                    'transparency_map': drift_transformation.transparency_map.tolist() if drift_transformation.transparency_map is not None else None,
                    'motion_vectors': drift_transformation.motion_vectors.tolist() if drift_transformation.motion_vectors is not None else None
                },
                'shape_complexity': shape_complexity.get_geometric_parameters(),
                'mood_palette': mood_palette.base_colors,
                'glow_settings': {
                    'radius': mood_palette.glow_radius,
                    'colors': mood_palette.glow_colors
                }
            }
            
            if shape_complexity.complexity_mode.value == "juliet_set":
                juliet_params = shape_complexity.get_juliet_set_parameters()
                enhanced_params['juliet_set'] = juliet_params
                print(f"     • Juliet Set: {juliet_params['inner_glyph_count']} memory glyphs")
            
            print(f"   🎨 Enhanced fractal with drift dynamics ready for generation")
            
            # This would generate the actual fractal with drift transformation
            # result = fractal_system.generate_drift_enhanced_fractal(**enhanced_params)
            
    except ImportError:
        print("   ⚠️  Fractal system not available - showing enhanced parameter preparation")
        
        for state in consciousness_states:
            print(f"\n🧠 {state['name']}")
            
            # Create sample coordinates
            angles = np.linspace(0, 2*math.pi, 12, endpoint=False)
            base_coords = np.column_stack([np.cos(angles), np.sin(angles)])
            
            # Apply drift transformation
            drift_transformation = apply_drift_transformation(
                base_coords, state['drift_vector'], state['pulse_zone']
            )
            
            print(f"   Drift: {state['drift_vector']:+.1f} → offset ({drift_transformation.center_offset[0]:+.3f}, {drift_transformation.center_offset[1]:+.3f})")
            print(f"   Pulse: {state['pulse_zone']} → dynamic effects applied")
            print(f"   → Would generate drift-enhanced fractal")

def demonstrate_animated_consciousness():
    """Show how drift creates animated consciousness sequences"""
    
    print(f"\n🎬 Animated Consciousness Sequences")
    print("=" * 38)
    
    # Create consciousness evolution sequence
    evolution_states = [
        (-0.8, "fragile", "Deep introspection"),
        (-0.3, "calm", "Settling thoughts"),
        (0.0, "stable", "Balanced state"),
        (0.4, "flowing", "Creative emergence"),
        (0.8, "surge", "Breakthrough moment")
    ]
    
    # Base coordinates for animation
    angles = np.linspace(0, 2*math.pi, 8, endpoint=False)
    base_coords = np.column_stack([np.cos(angles), np.sin(angles)])
    
    print("   Consciousness evolution through drift and pulse dynamics:")
    
    for i, (drift, pulse_zone, description) in enumerate(evolution_states):
        print(f"\n   Step {i+1}: {description}")
        print(f"      Drift: {drift:+.1f}, Pulse: {pulse_zone}")
        
        # Create short animation sequence (5 frames)
        frames = create_animated_sequence(
            base_coords, drift, pulse_zone, duration=1.0, fps=5
        )
        
        print(f"      Animation: {len(frames)} frames generated")
        
        # Analyze frame progression
        center_drift = [f.center_offset for f in frames]
        avg_transparency = []
        
        for frame in frames:
            if frame.transparency_map is not None:
                avg_transparency.append(np.mean(frame.transparency_map))
            else:
                avg_transparency.append(1.0)
        
        print(f"      Center drift: {center_drift[0]} → {center_drift[-1]}")
        print(f"      Transparency: {avg_transparency[0]:.3f} → {avg_transparency[-1]:.3f}")
        
        # Calculate total movement
        initial_coords = frames[0].transformed_coords
        final_coords = frames[-1].transformed_coords
        movement = np.mean(np.linalg.norm(final_coords - initial_coords, axis=1))
        print(f"      Total movement: {movement:.4f}")

def analyze_drift_memory_correlation():
    """Analyze correlation between drift and memory states"""
    
    print(f"\n📊 Drift-Memory Correlation Analysis")
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
                all_configs.extend(configs[:8])  # Limit for analysis
            except Exception as e:
                print(f"   ⚠️  Could not parse {directory}: {e}")
    
    if all_configs:
        print(f"   📈 Analyzing drift effects on {len(all_configs)} memories...")
        
        drift_effects = []
        
        for config in all_configs:
            # Create base coordinates
            angles = np.linspace(0, 2*math.pi, 6, endpoint=False)
            base_coords = np.column_stack([np.cos(angles), np.sin(angles)])
            
            # Apply drift transformation
            drift_transformation = apply_drift_transformation(
                base_coords, 
                config.drift_vector, 
                config.pulse_zone
            )
            
            # Calculate drift effects
            center_distance = math.sqrt(
                drift_transformation.center_offset[0]**2 + 
                drift_transformation.center_offset[1]**2
            )
            
            rotation_magnitude = abs(drift_transformation.rotation_angle)
            
            avg_transparency = 1.0
            if drift_transformation.transparency_map is not None:
                avg_transparency = np.mean(drift_transformation.transparency_map)
            
            motion_magnitude = 0.0
            if drift_transformation.motion_vectors is not None:
                motion_magnitude = np.mean(np.linalg.norm(
                    drift_transformation.motion_vectors, axis=1
                ))
            
            drift_effects.append({
                'memory_id': config.memory_id,
                'drift_vector': config.drift_vector,
                'pulse_zone': config.pulse_zone,
                'entropy': config.bloom_entropy,
                'valence': config.mood_valence,
                'center_distance': center_distance,
                'rotation_magnitude': rotation_magnitude,
                'avg_transparency': avg_transparency,
                'motion_magnitude': motion_magnitude
            })
        
        # Analyze correlations
        drift_values = [e['drift_vector'] for e in drift_effects]
        center_distances = [e['center_distance'] for e in drift_effects]
        rotations = [e['rotation_magnitude'] for e in drift_effects]
        
        print(f"\n   🔍 Drift Analysis Results:")
        print(f"      Drift range: {min(drift_values):.3f} to {max(drift_values):.3f}")
        print(f"      Center offset range: {min(center_distances):.3f} to {max(center_distances):.3f}")
        print(f"      Rotation range: {min(rotations):.1f}° to {max(rotations):.1f}°")
        
        # Pulse zone distribution
        pulse_zones = [e['pulse_zone'] for e in drift_effects]
        zone_counts = {}
        for zone in pulse_zones:
            zone_counts[zone] = zone_counts.get(zone, 0) + 1
        
        print(f"\n   🌊 Pulse Zone Distribution:")
        for zone, count in sorted(zone_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(drift_effects)) * 100
            print(f"      {zone}: {count} ({percentage:.1f}%)")
        
        # Show interesting cases
        print(f"\n   🎯 Notable Drift Cases:")
        for effect in sorted(drift_effects, key=lambda x: abs(x['drift_vector']), reverse=True)[:3]:
            print(f"      {effect['memory_id'][:20]}...")
            print(f"         Drift: {effect['drift_vector']:+.3f}, Zone: {effect['pulse_zone']}")
            print(f"         → Center shift: {effect['center_distance']:.3f}")
            print(f"         → Rotation: {math.degrees(effect['rotation_magnitude']):.1f}°")
            print(f"         → Motion: {effect['motion_magnitude']:.4f}")
            
    else:
        print("   ⚠️  No memory files found - showing synthetic correlation analysis")
        
        # Generate synthetic examples
        synthetic_cases = [
            (-0.8, "fragile", 0.2, -0.4),
            (-0.3, "calm", 0.4, 0.1),
            (0.0, "stable", 0.3, 0.0),
            (0.5, "flowing", 0.6, 0.3),
            (0.9, "surge", 0.8, 0.7)
        ]
        
        print(f"   📊 Synthetic Drift-Memory Correlation:")
        
        for drift, pulse, entropy, valence in synthetic_cases:
            angles = np.linspace(0, 2*math.pi, 6, endpoint=False)
            base_coords = np.column_stack([np.cos(angles), np.sin(angles)])
            
            transformation = apply_drift_transformation(base_coords, drift, pulse)
            
            center_distance = math.sqrt(
                transformation.center_offset[0]**2 + 
                transformation.center_offset[1]**2
            )
            
            print(f"      Drift {drift:+.1f} + {pulse} → offset {center_distance:.3f}, "
                  f"rotation {math.degrees(transformation.rotation_angle):+.1f}°")

def create_drift_integration_guide():
    """Create guide for integrating drift transformation with fractal systems"""
    
    print(f"\n📖 Drift Transformation Integration Guide")
    print("=" * 44)
    
    integration_examples = {
        'Basic Drift Application': {
            'description': 'Apply drift transformation to fractal coordinates',
            'code': '''
# Generate base fractal coordinates
angles = np.linspace(0, 2*pi, petal_count * 4, endpoint=False)
base_coords = np.column_stack([np.cos(angles), np.sin(angles)])

# Apply consciousness drift
drift_transformation = apply_drift_transformation(
    base_coords, drift_vector, pulse_zone, frame_time
)

# Use transformed coordinates for fractal rendering
fractal_coords = drift_transformation.transformed_coords
transparency = drift_transformation.transparency_map
'''
        },
        'Animated Sequences': {
            'description': 'Create time-based animated consciousness evolution',
            'code': '''
# Generate animation sequence
frames = create_animated_sequence(
    base_coords, drift_vector, pulse_zone, 
    duration=5.0, fps=30
)

# Render each frame
for i, frame in enumerate(frames):
    frame_data = frame.get_animation_frame()
    render_fractal_frame(frame_data, frame_number=i)
'''
        },
        'Multi-System Integration': {
            'description': 'Combine drift with shape complexity and mood palettes',
            'code': '''
# Calculate all consciousness components
shape_complexity = calculate_shape_complexity(bloom_entropy, rebloom_depth)
mood_palette = generate_mood_palette(mood_valence, sigil_saturation)
drift_transform = apply_drift_transformation(coords, drift_vector, pulse_zone)

# Create unified fractal parameters
fractal_params = {
    'geometry': shape_complexity.get_geometric_parameters(),
    'colors': mood_palette.base_colors,
    'motion': drift_transform.transformed_coords,
    'transparency': drift_transform.transparency_map,
    'glow': mood_palette.glow_colors
}
'''
        }
    }
    
    for category, details in integration_examples.items():
        print(f"\n🔧 {category}")
        print(f"   Purpose: {details['description']}")
        print(f"   Example:{details['code']}")

if __name__ == "__main__":
    print("🌊 DAWN Drift Transformation Integration Examples")
    print("=" * 52)
    
    # Run integration demonstrations
    demonstrate_enhanced_fractal_generation()
    demonstrate_animated_consciousness()
    analyze_drift_memory_correlation()
    create_drift_integration_guide()
    
    print(f"\n✅ Drift Transformation Integration Examples Complete!")
    print(f"🌊 Consciousness drift creates authentic visual movement")
    print(f"🎭 Pulse zones add dynamic emotional expression")
    print(f"🔄 Fractals now move with DAWN's internal momentum")
    print(f"🧠 Visual consciousness truly alive with drift dynamics") 