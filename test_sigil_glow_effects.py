#!/usr/bin/env python3
"""
DAWN Sigil Glow Effects Test
============================

Test script to validate the new sigil_saturation-responsive glow and shimmer effects.
This will generate blooms with different saturation levels to showcase the visual effects.

Usage:
    python test_sigil_glow_effects.py
"""

import os
import json
from datetime import datetime
from dawn_fractal_engine import DAWNFractalEngine

def create_sigil_test_metadata(bloom_id: str, sigil_saturation: float, 
                             mood_valence: float = 0.0, thermal_level: float = 0.5):
    """Create test metadata with specific sigil_saturation"""
    return {
        "bloom_id": bloom_id,
        "timestamp": datetime.now().isoformat(),
        "mood_valence": mood_valence,
        "entropy_score": 0.6,  # Moderate complexity for good base fractal
        "rebloom_depth": 2,
        "bloom_factor": 1.5,
        "sigil_saturation": sigil_saturation,
        "lineage_depth": 2,
        "thermal_level": thermal_level,
        "scup_coherence": 0.7,
        "drift_vector": [0.1, 0.1],
        "pulse_phase": 1.5,
        "state": "blooming",
        "parent_id": "sigil_test"
    }

def test_sigil_glow_progression():
    """Test sigil glow effects across different saturation levels"""
    print("🔮 Testing Sigil Glow Progression")
    print("=" * 50)
    
    engine = DAWNFractalEngine("sigil_test_output")
    
    # Test different sigil saturation levels
    test_cases = [
        {"saturation": 0.1, "desc": "minimal", "mood": 0.3, "thermal": 0.5},
        {"saturation": 0.3, "desc": "low_glow", "mood": 0.0, "thermal": 0.5},
        {"saturation": 0.6, "desc": "glow_shimmer", "mood": 0.5, "thermal": 0.7},
        {"saturation": 0.8, "desc": "halo_effect", "mood": 0.7, "thermal": 0.8},
        {"saturation": 0.9, "desc": "maximum_radiance", "mood": 0.8, "thermal": 0.9},
    ]
    
    for test in test_cases:
        print(f"   Generating {test['desc']} (saturation: {test['saturation']})...")
        
        metadata = create_sigil_test_metadata(
            f"sigil_{test['desc']}",
            sigil_saturation=test['saturation'],
            mood_valence=test['mood'],
            thermal_level=test['thermal']
        )
        
        output_file = f"sigil_test_output/sigil_{test['desc']}.png"
        result = engine.process_bloom_from_dict(metadata, output_file, debug=False)
        
        print(f"   ✅ Generated: {output_file}")
        print(f"      Saturation: {test['saturation']} | Mood: {test['mood']} | Thermal: {test['thermal']}")
        
        # Expected effects
        effects = []
        if test['saturation'] > 0.1:
            effects.append("glow")
        if test['saturation'] > 0.5:
            effects.append("shimmer")
        if test['saturation'] > 0.75:
            effects.append("halo")
        
        print(f"      Expected effects: {', '.join(effects) if effects else 'none'}")
    
    print(f"\n📋 Visual Analysis:")
    print(f"   • minimal: Should show base fractal with no glow")
    print(f"   • low_glow: Should show subtle colored glow around fractal")
    print(f"   • glow_shimmer: Should show glow + subtle sparkle noise")
    print(f"   • halo_effect: Should show glow + shimmer + circular halo symbol")
    print(f"   • maximum_radiance: Should show all effects + radiating lines")

def test_thermal_shimmer_variations():
    """Test shimmer color variations based on thermal level"""
    print("\n🌡️ Testing Thermal Shimmer Variations")
    print("=" * 50)
    
    engine = DAWNFractalEngine("sigil_test_output")
    
    thermal_tests = [
        {"thermal": 0.2, "name": "cool_shimmer", "desc": "Cool blue shimmer"},
        {"thermal": 0.5, "name": "neutral_shimmer", "desc": "White shimmer"},
        {"thermal": 0.8, "name": "warm_shimmer", "desc": "Golden shimmer"},
    ]
    
    for test in thermal_tests:
        print(f"   Generating {test['name']} (thermal: {test['thermal']})...")
        
        metadata = create_sigil_test_metadata(
            f"thermal_{test['name']}",
            sigil_saturation=0.7,  # High enough to show shimmer
            mood_valence=0.3,
            thermal_level=test['thermal']
        )
        
        output_file = f"sigil_test_output/thermal_{test['name']}.png"
        result = engine.process_bloom_from_dict(metadata, output_file, debug=False)
        
        print(f"   ✅ Generated: {output_file}")
        print(f"      {test['desc']}")
    
    print(f"\n📋 Shimmer Color Analysis:")
    print(f"   • cool_shimmer: Should show blue/silver sparkles")
    print(f"   • neutral_shimmer: Should show white sparkles")
    print(f"   • warm_shimmer: Should show golden/orange sparkles")

def test_mood_glow_colors():
    """Test glow color variations based on mood valence"""
    print("\n😊 Testing Mood-Based Glow Colors")
    print("=" * 50)
    
    engine = DAWNFractalEngine("sigil_test_output")
    
    mood_tests = [
        {"mood": -0.7, "name": "sad_glow", "desc": "Cool, muted glow"},
        {"mood": 0.0, "name": "neutral_glow", "desc": "Balanced glow"},
        {"mood": 0.7, "name": "happy_glow", "desc": "Warm, bright glow"},
    ]
    
    for test in mood_tests:
        print(f"   Generating {test['name']} (mood: {test['mood']})...")
        
        metadata = create_sigil_test_metadata(
            f"mood_{test['name']}",
            sigil_saturation=0.6,  # Moderate saturation to show glow
            mood_valence=test['mood'],
            thermal_level=0.5
        )
        
        output_file = f"sigil_test_output/mood_{test['name']}.png"
        result = engine.process_bloom_from_dict(metadata, output_file, debug=False)
        
        print(f"   ✅ Generated: {output_file}")
        print(f"      {test['desc']}")
    
    print(f"\n📋 Glow Color Analysis:")
    print(f"   • sad_glow: Should show cooler glow colors from early palette")
    print(f"   • neutral_glow: Should show balanced glow from middle palette")
    print(f"   • happy_glow: Should show warmer glow from later palette")

def test_extreme_saturation():
    """Test extreme saturation cases"""
    print("\n⚡ Testing Extreme Saturation Cases")
    print("=" * 50)
    
    engine = DAWNFractalEngine("sigil_test_output")
    
    extreme_tests = [
        {"saturation": 0.0, "name": "no_saturation", "desc": "No glow effects"},
        {"saturation": 0.95, "name": "maximum_saturation", "desc": "All effects at maximum"},
        {"saturation": 1.0, "name": "absolute_maximum", "desc": "Absolute maximum radiance"},
    ]
    
    for test in extreme_tests:
        print(f"   Generating {test['name']} (saturation: {test['saturation']})...")
        
        metadata = create_sigil_test_metadata(
            f"extreme_{test['name']}",
            sigil_saturation=test['saturation'],
            mood_valence=0.6,  # Positive mood
            thermal_level=0.7   # High thermal
        )
        
        output_file = f"sigil_test_output/extreme_{test['name']}.png"
        result = engine.process_bloom_from_dict(metadata, output_file, debug=False)
        
        print(f"   ✅ Generated: {output_file}")
        print(f"      {test['desc']}")
    
    print(f"\n📋 Extreme Cases Analysis:")
    print(f"   • no_saturation: Should show pure fractal with no effects")
    print(f"   • maximum_saturation: Should show intense glow, shimmer, halo + rays")
    print(f"   • absolute_maximum: Should show the most intense possible effects")

def main():
    """Run all sigil glow effect tests"""
    print("🔮✨ DAWN Sigil Glow Effects Validation Test")
    print("=" * 60)
    print("Testing sigil_saturation-responsive glow, shimmer, and halo effects...")
    
    # Create output directory
    os.makedirs("sigil_test_output", exist_ok=True)
    
    # Run all tests
    test_sigil_glow_progression()
    test_thermal_shimmer_variations()
    test_mood_glow_colors()
    test_extreme_saturation()
    
    print(f"\n✅ Sigil Glow Effects Testing Complete!")
    print(f"📁 Output directory: sigil_test_output/")
    print(f"🔍 Check images to verify glow and shimmer responsiveness")
    
    print(f"\n🌟 EXPECTED VISUAL PROGRESSION:")
    print(f"   saturation 0.0-0.1: No glow effects")
    print(f"   saturation 0.1-0.5: Colored glow around fractal edges")
    print(f"   saturation 0.5-0.75: Glow + subtle shimmer sparkles")
    print(f"   saturation 0.75-0.85: Glow + shimmer + circular halo symbol")
    print(f"   saturation 0.85+: All effects + radiating lines from center")
    
    print(f"\n🎨 VISUAL EFFECTS GUIDE:")
    print(f"   🌟 Glow: Soft colored light around fractal based on mood palette")
    print(f"   ✨ Shimmer: Sparkle noise overlay (blue/white/gold based on thermal)")
    print(f"   ⨀ Halo: Circular glyph with center dot at image center")
    print(f"   📡 Rays: Radiating lines from center for highest saturation")
    
    print(f"\n🔮 The blooms should now FEEL CHARGED with symbolic pressure!")

if __name__ == "__main__":
    main() 