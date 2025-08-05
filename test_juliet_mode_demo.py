#!/usr/bin/env python3
"""
DAWN Juliet Mode Demo - Bloom Rendering Refinements
==================================================

Demonstrates the Juliet Mode visual optimizations for reducing oversaturation
in high-entropy, high-depth bloom states while maintaining structural clarity.

Juliet Mode conditions: depth ≥ 6, entropy ≥ 0.7
Key optimizations:
1. Reduced glow radius when entropy > 0.7 and sigil_saturation > 0.6
2. Capped shimmer noise opacity to 0.15
3. Prioritized core petal structure in high-depth blooms
4. Optional clarity_mode toggle for complete background fog removal
"""

from fractal_generator_v3_enhanced import DAWNFractalGeneratorV3


def demo_standard_vs_juliet_mode():
    """Compare standard rendering vs Juliet Mode optimizations"""
    
    print("🌸 DAWN Juliet Mode Demo")
    print("=" * 50)
    
    # Initialize generator
    generator = DAWNFractalGeneratorV3("juliet_mode_demo_output")
    
    # Test parameters that trigger Juliet Mode
    test_params = {
        'bloom_entropy': 0.8,          # High entropy (>0.7)
        'mood_valence': -0.3,          # Slightly negative mood
        'drift_vector': 0.4,           # Some asymmetry
        'rebloom_depth': 7,            # High depth (≥6)
        'sigil_saturation': 0.7,       # High saturation (>0.6)
        'pulse_zone': 'fragile'        # Fragile pulse zone (high noise)
    }
    
    print(f"Test Parameters:")
    print(f"  Entropy: {test_params['bloom_entropy']:.3f} (Juliet threshold: ≥0.7)")
    print(f"  Depth: {test_params['rebloom_depth']} (Juliet threshold: ≥6)")
    print(f"  Saturation: {test_params['sigil_saturation']:.3f} (Glow reduction threshold: >0.6)")
    print(f"  Pulse Zone: {test_params['pulse_zone']} (naturally high noise)")
    print()
    
    # Test 1: Standard Mode
    print("🔄 Generating Standard Mode bloom...")
    standard_result = generator.generate_bloom_fractal(
        **test_params,
        clarity_mode=False  # Standard rendering
    )
    print(f"Standard bloom: {standard_result['bloom_id']}")
    print()
    
    # Test 2: Automatic Juliet Mode (triggered by depth + entropy)
    print("🎭 Generating Automatic Juliet Mode bloom...")
    juliet_auto_result = generator.generate_bloom_fractal(
        **test_params,
        clarity_mode=False  # Let Juliet Mode trigger automatically
    )
    print(f"Auto Juliet bloom: {juliet_auto_result['bloom_id']}")
    print()
    
    # Test 3: Forced Clarity Mode
    print("✨ Generating Clarity Mode bloom (no background fog)...")
    clarity_result = generator.generate_bloom_fractal(
        **test_params,
        clarity_mode=True  # Force clarity mode
    )
    print(f"Clarity bloom: {clarity_result['bloom_id']}")
    print()
    
    # Show optimizations applied
    print("🎯 Optimization Summary:")
    print("-" * 30)
    
    for result, mode in [(standard_result, "Standard"), 
                         (juliet_auto_result, "Auto Juliet"), 
                         (clarity_result, "Clarity")]:
        print(f"{mode} Mode:")
        if 'clarity_optimizations' in result:
            opts = result['clarity_optimizations']
            print(f"  Juliet Mode Active: {result.get('juliet_mode', False)}")
            print(f"  Reduced Glow: {opts.get('reduced_glow', False)}")
            print(f"  Capped Noise: {opts.get('capped_noise_opacity', False)}")
            print(f"  Structural Priority: {opts.get('structural_priority', False)}")
            print(f"  Clarity Forced: {opts.get('clarity_mode_forced', False)}")
        else:
            print("  Standard rendering (no optimizations)")
        print()


def demo_edge_case_scenarios():
    """Test various edge cases for Juliet Mode"""
    
    print("🧪 Testing Edge Case Scenarios")
    print("=" * 40)
    
    generator = DAWNFractalGeneratorV3("juliet_edge_cases")
    
    edge_cases = [
        {
            'name': 'High Depth, Low Entropy',
            'params': {
                'bloom_entropy': 0.4,      # Below Juliet threshold
                'rebloom_depth': 8,        # Above Juliet threshold
                'sigil_saturation': 0.5,
                'mood_valence': 0.2,
                'drift_vector': 0.1,
                'pulse_zone': 'calm'
            }
        },
        {
            'name': 'Low Depth, High Entropy',
            'params': {
                'bloom_entropy': 0.9,      # Above Juliet threshold
                'rebloom_depth': 4,        # Below Juliet threshold
                'sigil_saturation': 0.8,
                'mood_valence': -0.5,
                'drift_vector': 0.6,
                'pulse_zone': 'volatile'
            }
        },
        {
            'name': 'Maximum Chaos (Both High)',
            'params': {
                'bloom_entropy': 0.95,     # Maximum entropy
                'rebloom_depth': 10,       # Maximum depth
                'sigil_saturation': 0.9,   # High saturation
                'mood_valence': -0.8,      # Strong negative
                'drift_vector': 0.9,       # Maximum drift
                'pulse_zone': 'volatile'   # Chaotic zone
            }
        }
    ]
    
    for case in edge_cases:
        print(f"Testing: {case['name']}")
        result = generator.generate_bloom_fractal(**case['params'])
        
        is_juliet = result.get('juliet_mode', False)
        print(f"  Juliet Mode Triggered: {is_juliet}")
        if is_juliet:
            opts = result.get('clarity_optimizations', {})
            print(f"  Glow Reduced: {opts.get('reduced_glow', False)}")
            print(f"  Noise Capped: {opts.get('capped_noise_opacity', False)}")
        print()


def demo_clarity_mode_comparison():
    """Show the dramatic difference clarity mode makes"""
    
    print("🔍 Clarity Mode Comparison")
    print("=" * 30)
    
    generator = DAWNFractalGeneratorV3("clarity_comparison")
    
    # Parameters that would normally create a very chaotic bloom
    chaotic_params = {
        'bloom_entropy': 0.85,
        'mood_valence': -0.6,
        'drift_vector': 0.7,
        'rebloom_depth': 8,
        'sigil_saturation': 0.8,
        'pulse_zone': 'volatile'
    }
    
    print("Generating chaotic bloom in both modes...")
    
    # Normal mode
    normal = generator.generate_bloom_fractal(**chaotic_params, clarity_mode=False)
    print(f"Normal Mode: {normal['bloom_id']}")
    
    # Clarity mode
    clear = generator.generate_bloom_fractal(**chaotic_params, clarity_mode=True)
    print(f"Clarity Mode: {clear['bloom_id']}")
    
    print("\nClarity mode should show:")
    print("  ✓ Clear petal structure")
    print("  ✓ Minimal background fog")
    print("  ✓ Enhanced edge definition")
    print("  ✓ Fragile but clear aesthetic")


if __name__ == "__main__":
    print("Starting DAWN Juliet Mode Demonstration...")
    print()
    
    try:
        demo_standard_vs_juliet_mode()
        demo_edge_case_scenarios()
        demo_clarity_mode_comparison()
        
        print("🎉 Demo completed successfully!")
        print("\nOutput files saved in:")
        print("  - juliet_mode_demo_output/")
        print("  - juliet_edge_cases/")
        print("  - clarity_comparison/")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc() 