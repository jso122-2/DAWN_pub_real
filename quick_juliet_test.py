#!/usr/bin/env python3
"""
Quick Juliet Set Debug Test
===========================

Test a single fractal that should definitely activate Juliet Set mode
and check if the activation logic is working correctly.
"""

from dawn_fractal_memory_system import DAWNFractalMemorySystem

def test_single_juliet_activation():
    """Test one clear Juliet Set case to debug activation"""
    
    print("🔍 Testing Single Juliet Set Activation")
    print("=" * 40)
    
    memory_system = DAWNFractalMemorySystem(archive_dir="debug_juliet")
    
    # Parameters that should DEFINITELY activate Juliet Set mode
    params = {
        'bloom_entropy': 0.3,      # < 0.4 ✓
        'mood_valence': -0.5,      # Nostalgic
        'drift_vector': -0.4,      # Some drift
        'rebloom_depth': 8,        # > 6 ✓  
        'sigil_saturation': 0.7,   # High saturation
        'pulse_zone': 'flowing'    # flowing ✓
    }
    
    print("🎯 Test Parameters:")
    for key, value in params.items():
        print(f"   {key}: {value}")
    
    print(f"\n📋 Juliet Set Activation Check:")
    depth_check = params['rebloom_depth'] > 6
    entropy_check = params['bloom_entropy'] < 0.4
    zone_check = params['pulse_zone'] == 'flowing'
    
    print(f"   • rebloom_depth > 6: {depth_check} ({params['rebloom_depth']} > 6)")
    print(f"   • entropy < 0.4: {entropy_check} ({params['bloom_entropy']} < 0.4)")
    print(f"   • pulse_zone == 'flowing': {zone_check} ('{params['pulse_zone']}')")
    
    should_activate = depth_check and entropy_check and zone_check
    print(f"   → Should Activate Juliet Set: {should_activate}")
    
    if should_activate:
        print(f"\n🌸 Generating test fractal...")
        print("   (Watch for 'Activating Juliet Set mode' message)")
    
    # Generate fractal
    metadata = memory_system.generate_bloom_fractal(**params)
    
    # Analyze result
    print(f"\n📊 Results:")
    print(f"   🔤 Fractal String: {metadata['fractal_string']}")
    print(f"   🦉 Owl Commentary: {metadata['owl_commentary']}")
    print(f"   🎨 Bloom Shape: {metadata['visual_characteristics']['bloom_shape_descriptor']}")
    
    # Check if it has Juliet characteristics
    fractal_string = metadata['fractal_string']
    has_flow_zone = "PzFLOW" in fractal_string
    
    print(f"\n🔍 Juliet Set Indicators:")
    print(f"   • Contains 'PzFLOW': {has_flow_zone}")
    
    if has_flow_zone:
        print("   ✅ Fractal shows flowing pulse zone")
    else:
        print("   ❌ Fractal does not show flowing pulse zone")
    
    # Check parameters in metadata match input
    stored_params = metadata['parameters']
    print(f"\n🔬 Parameter Verification:")
    for key, expected in params.items():
        actual = stored_params[key]
        match = actual == expected
        print(f"   • {key}: {actual} (expected {expected}) {'✅' if match else '❌'}")

if __name__ == "__main__":
    test_single_juliet_activation() 