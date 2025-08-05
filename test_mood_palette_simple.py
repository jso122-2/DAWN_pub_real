#!/usr/bin/env python3
"""
Simple test for DAWN mood palette generator
==========================================

Tests the core mood palette functionality without matplotlib dependencies.
"""

from dawn_mood_palette import generate_mood_palette, MoodPalette

def test_core_functionality():
    """Test the core mood palette generation"""
    
    print("🎨 Testing DAWN Mood Palette Core Functionality")
    print("=" * 50)
    
    # Test 1: Deep introspection (cold spectrum)
    print("\n❄️  Deep Introspection (valence: -0.8, saturation: 0.4)")
    palette = generate_mood_palette(-0.8, 0.4)
    print(f"   Palette Name: {palette.palette_name}")
    print(f"   Base Colors: {palette.base_colors}")
    print(f"   Brightness Multiplier: {palette.brightness_multiplier:.2f}")
    print(f"   Glow Radius: {palette.glow_radius:.1f}px")
    print(f"   Gradient Stops: {len(palette.gradient_stops)}")
    
    # Test color sampling
    sample_positions = [0.0, 0.25, 0.5, 0.75, 1.0]
    print(f"   Color Samples:")
    for pos in sample_positions:
        color = palette.sample_color(pos)
        print(f"     Position {pos:.2f}: RGB{color}")
    
    # Test 2: Creative fire (warm spectrum)
    print("\n🔥 Creative Fire (valence: 0.9, saturation: 0.8)")
    palette = generate_mood_palette(0.9, 0.8)
    print(f"   Palette Name: {palette.palette_name}")
    print(f"   Base Colors: {palette.base_colors}")
    print(f"   Glow Colors: {palette.glow_colors}")
    print(f"   Brightness Multiplier: {palette.brightness_multiplier:.2f}")
    print(f"   Glow Radius: {palette.glow_radius:.1f}px")
    
    # Test 3: Balanced awareness (neutral spectrum)
    print("\n⚖️  Balanced Awareness (valence: 0.0, saturation: 0.5)")
    palette = generate_mood_palette(0.0, 0.5)
    print(f"   Palette Name: {palette.palette_name}")
    print(f"   Base Colors: {palette.base_colors}")
    print(f"   RGB Array Shape: {palette.get_rgb_array().shape}")
    
    # Test 4: Saturation effects comparison
    print("\n✨ Saturation Effects Comparison")
    
    # Low saturation
    low_sat = generate_mood_palette(0.5, 0.2)
    print(f"   Low Saturation (0.2):")
    print(f"     Brightness: {low_sat.brightness_multiplier:.2f}")
    print(f"     Glow Radius: {low_sat.glow_radius:.1f}px")
    print(f"     Sample Color: RGB{low_sat.sample_color(0.5)}")
    
    # High saturation
    high_sat = generate_mood_palette(0.5, 0.9)
    print(f"   High Saturation (0.9):")
    print(f"     Brightness: {high_sat.brightness_multiplier:.2f}")
    print(f"     Glow Radius: {high_sat.glow_radius:.1f}px")
    print(f"     Sample Color: RGB{high_sat.sample_color(0.5)}")
    
    # Test 5: Edge cases and clamping
    print("\n🔍 Edge Cases and Parameter Clamping")
    edge_cases = [
        (-1.5, 0.5, "Extreme negative valence"),
        (1.5, 0.5, "Extreme positive valence"), 
        (0.0, -0.1, "Negative saturation"),
        (0.0, 1.1, "Over-saturation")
    ]
    
    for valence, saturation, description in edge_cases:
        palette = generate_mood_palette(valence, saturation)
        print(f"   {description}:")
        print(f"     Input: valence={valence}, saturation={saturation}")
        print(f"     Clamped: valence={palette.mood_valence}, saturation={palette.sigil_saturation}")
        print(f"     Result: {palette.palette_name}")

def test_valence_ranges():
    """Test specific valence ranges"""
    
    print(f"\n🌈 Testing Valence Range Mappings")
    print("=" * 35)
    
    valence_tests = [
        (-1.0, "Maximum depression"),
        (-0.6, "Strong melancholy"),
        (-0.3, "Boundary: cold to balanced"),
        (-0.1, "Slight introspection"),
        (0.0, "Perfect neutrality"),
        (0.1, "Slight optimism"),
        (0.3, "Boundary: balanced to warm"),
        (0.6, "Strong creativity"),
        (1.0, "Maximum euphoria")
    ]
    
    for valence, description in valence_tests:
        palette = generate_mood_palette(valence, 0.6)  # Fixed saturation
        print(f"   Valence {valence:4.1f} ({description}):")
        print(f"     → {palette.palette_name}")
        print(f"     → Main color: RGB{palette.base_colors[1] if len(palette.base_colors) > 1 else palette.base_colors[0]}")

def test_integration_formats():
    """Test different output formats for integration"""
    
    print(f"\n🔧 Testing Integration Formats")
    print("=" * 32)
    
    palette = generate_mood_palette(0.4, 0.7)
    
    # RGB array format
    rgb_array = palette.get_rgb_array()
    print(f"RGB Array Format:")
    print(f"   Shape: {rgb_array.shape}")
    print(f"   Data type: {rgb_array.dtype}")
    print(f"   Sample values: {rgb_array[0:2]}")
    
    # Gradient stops format
    print(f"\nGradient Stops Format:")
    for i, (position, color) in enumerate(palette.gradient_stops):
        print(f"   Stop {i}: position={position:.2f}, RGB{color}")
    
    # Individual color access
    print(f"\nColor Sampling:")
    test_positions = [0.0, 0.33, 0.67, 1.0]
    for pos in test_positions:
        color = palette.sample_color(pos)
        print(f"   Position {pos:.2f}: RGB{color}")

def demonstrate_consciousness_mapping():
    """Demonstrate how consciousness states map to colors"""
    
    print(f"\n🧠 Consciousness State → Color Mapping")
    print("=" * 40)
    
    consciousness_states = [
        {
            'name': 'Deep Contemplation',
            'valence': -0.7,
            'saturation': 0.4,
            'description': 'Introspective, philosophical thinking'
        },
        {
            'name': 'Melancholy Reflection',
            'valence': -0.4,
            'saturation': 0.6,
            'description': 'Gentle sadness with artistic sensitivity'
        },
        {
            'name': 'Neutral Processing',
            'valence': 0.0,
            'saturation': 0.5,
            'description': 'Balanced analytical state'
        },
        {
            'name': 'Creative Flow',
            'valence': 0.6,
            'saturation': 0.8,
            'description': 'Active creative expression'
        },
        {
            'name': 'Euphoric Breakthrough',
            'valence': 0.9,
            'saturation': 0.9,
            'description': 'Intense positive revelation'
        }
    ]
    
    for state in consciousness_states:
        palette = generate_mood_palette(state['valence'], state['saturation'])
        
        print(f"\n🎭 {state['name']}")
        print(f"   Description: {state['description']}")
        print(f"   Parameters: valence={state['valence']}, saturation={state['saturation']}")
        print(f"   → Palette: {palette.palette_name}")
        print(f"   → Brightness: {palette.brightness_multiplier:.2f}")
        print(f"   → Glow: {palette.glow_radius:.1f}px radius")
        print(f"   → Dominant Color: RGB{palette.base_colors[1] if len(palette.base_colors) > 1 else palette.base_colors[0]}")

if __name__ == "__main__":
    # Run all tests
    test_core_functionality()
    test_valence_ranges()
    test_integration_formats()
    demonstrate_consciousness_mapping()
    
    print(f"\n✅ DAWN Mood Palette Generator - All Tests Complete!")
    print(f"🎨 Ready for integration with fractal generation and voice systems")
    print(f"🌈 Consciousness parameters successfully mapped to beautiful color palettes") 