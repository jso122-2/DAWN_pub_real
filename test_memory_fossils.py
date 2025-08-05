#!/usr/bin/env python3
"""
DAWN Memory Fossils Test - Recursive Layering & Entropy Texture
===============================================================

Test script to validate the enhanced rebloom_depth recursive layering and 
entropy_score texture modulation that creates "memory fossils under pressure".

This demonstrates emotional recursion through:
- Inner recursive petal layering (depth >= 2)
- Entropy-driven edge texture modulation
- Juliet Set mode with spiral glyphs (depth >= 6)

Usage:
    python test_memory_fossils.py
"""

import os
import json
from datetime import datetime
from dawn_fractal_engine import DAWNFractalEngine

def create_memory_fossil_metadata(bloom_id: str, rebloom_depth: int, entropy_score: float, 
                                mood_valence: float = 0.0, sigil_saturation: float = 0.5):
    """Create test metadata for memory fossil generation"""
    return {
        "bloom_id": bloom_id,
        "timestamp": datetime.now().isoformat(),
        "mood_valence": mood_valence,
        "entropy_score": entropy_score,
        "rebloom_depth": rebloom_depth,
        "bloom_factor": 1.5,
        "sigil_saturation": sigil_saturation,
        "lineage_depth": 2,
        "thermal_level": 0.6,
        "scup_coherence": 0.7,
        "drift_vector": [0.1, 0.1],
        "pulse_phase": 1.5,
        "state": "blooming",
        "parent_id": "memory_fossil_test"
    }

def test_recursive_layering_progression():
    """Test recursive layering with increasing rebloom_depth"""
    print("🌸 Testing Recursive Layering Progression")
    print("=" * 60)
    
    engine = DAWNFractalEngine("memory_fossil_output")
    
    # Test different rebloom depths
    depth_tests = [
        {"depth": 1, "desc": "shallow", "entropy": 0.4},
        {"depth": 3, "desc": "moderate_layers", "entropy": 0.5},
        {"depth": 5, "desc": "deep_recursion", "entropy": 0.6},
        {"depth": 7, "desc": "juliet_set_mode", "entropy": 0.8},  # Activates Juliet Set mode
        {"depth": 10, "desc": "maximum_recursion", "entropy": 0.9},
    ]
    
    for test in depth_tests:
        print(f"   Generating {test['desc']} (depth: {test['depth']}, entropy: {test['entropy']})...")
        
        metadata = create_memory_fossil_metadata(
            f"fossil_{test['desc']}",
            rebloom_depth=test['depth'],
            entropy_score=test['entropy'],
            mood_valence=0.3,
            sigil_saturation=0.6
        )
        
        output_file = f"memory_fossil_output/fossil_{test['desc']}.png"
        result = engine.process_bloom_from_dict(metadata, output_file, debug=False)
        
        print(f"   ✅ Generated: {output_file}")
        print(f"      Rebloom Depth: {test['depth']} | Entropy: {test['entropy']}")
        
        # Expected effects
        effects = ["base_fractal"]
        if test['depth'] >= 2:
            effects.append("recursive_layers")
        if test['depth'] >= 6:
            effects.append("juliet_set_mode")
        if test['entropy'] > 0.7:
            effects.append("high_entropy_effects")
        
        print(f"      Expected effects: {', '.join(effects)}")
    
    print(f"\n📋 Layering Analysis:")
    print(f"   • shallow: Base fractal only")
    print(f"   • moderate_layers: 3 recursive petal layers with scaling/rotation")
    print(f"   • deep_recursion: 5 layers with enhanced compositing")
    print(f"   • juliet_set_mode: 7 layers + spiral etchings + vortex distortion")
    print(f"   • maximum_recursion: 8 layers + full Juliet effects + shimmer pulse")

def test_entropy_texture_modulation():
    """Test entropy-driven texture modulation at different entropy levels"""
    print("\n⚡ Testing Entropy Texture Modulation")
    print("=" * 60)
    
    engine = DAWNFractalEngine("memory_fossil_output")
    
    entropy_tests = [
        {"entropy": 0.2, "name": "smooth_curls", "desc": "Smooth curled petal outline"},
        {"entropy": 0.5, "name": "edge_jitter", "desc": "Edge jitter and perturbations"},
        {"entropy": 0.8, "name": "fractured_edges", "desc": "Fractured edges + glyph bleed"},
        {"entropy": 0.95, "name": "maximum_chaos", "desc": "Maximum fracture + shadows"},
    ]
    
    for test in entropy_tests:
        print(f"   Generating {test['name']} (entropy: {test['entropy']})...")
        
        metadata = create_memory_fossil_metadata(
            f"entropy_{test['name']}",
            rebloom_depth=4,  # Moderate depth to show texture effects
            entropy_score=test['entropy'],
            mood_valence=0.0,
            sigil_saturation=0.4
        )
        
        output_file = f"memory_fossil_output/entropy_{test['name']}.png"
        result = engine.process_bloom_from_dict(metadata, output_file, debug=False)
        
        print(f"   ✅ Generated: {output_file}")
        print(f"      {test['desc']}")
    
    print(f"\n📋 Entropy Texture Analysis:")
    print(f"   • smooth_curls: Sinusoidal edge curves, smooth petal outline")
    print(f"   • edge_jitter: Sinusoidal + noise mix, edge perturbations")
    print(f"   • fractured_edges: High-frequency fractures + glyph bleed-through")
    print(f"   • maximum_chaos: Maximum fracture + shadow effects + chaos modulation")

def test_juliet_set_mode_features():
    """Test Juliet Set mode features for deep rebloom (depth >= 6)"""
    print("\n🌀 Testing Juliet Set Mode Features")
    print("=" * 60)
    
    engine = DAWNFractalEngine("memory_fossil_output")
    
    juliet_tests = [
        {"depth": 6, "entropy": 0.7, "name": "basic_juliet", "desc": "Basic spiral etchings + vortex"},
        {"depth": 8, "entropy": 0.85, "name": "pulse_juliet", "desc": "Spiral + vortex + shimmer pulse"},
        {"depth": 10, "entropy": 0.95, "name": "maximum_juliet", "desc": "All effects at maximum intensity"},
    ]
    
    for test in juliet_tests:
        print(f"   Generating {test['name']} (depth: {test['depth']}, entropy: {test['entropy']})...")
        
        metadata = create_memory_fossil_metadata(
            f"juliet_{test['name']}",
            rebloom_depth=test['depth'],
            entropy_score=test['entropy'],
            mood_valence=0.5,
            sigil_saturation=0.8  # High saturation for enhanced effects
        )
        
        output_file = f"memory_fossil_output/juliet_{test['name']}.png"
        result = engine.process_bloom_from_dict(metadata, output_file, debug=False)
        
        print(f"   ✅ Generated: {output_file}")
        print(f"      {test['desc']}")
        
        # Expected Juliet Set features
        features = ["spiral_etchings", "polar_vortex"]
        if test['entropy'] > 0.8:
            features.append("shimmer_pulse")
        
        print(f"      Juliet features: {', '.join(features)}")
    
    print(f"\n📋 Juliet Set Analysis:")
    print(f"   • basic_juliet: Inner spiral glyph etchings + polar vortex distortion")
    print(f"   • pulse_juliet: All above + shimmer pulse for high entropy")
    print(f"   • maximum_juliet: Maximum intensity spiral etchings + vortex + pulse")

def test_petal_mask_evolution():
    """Test petal mask transparency evolution with depth"""
    print("\n🌺 Testing Petal Mask Evolution")
    print("=" * 60)
    
    engine = DAWNFractalEngine("memory_fossil_output")
    
    petal_tests = [
        {"depth": 2, "entropy": 0.3, "name": "simple_petals", "desc": "3-5 petals, gentle masks"},
        {"depth": 4, "entropy": 0.5, "name": "complex_petals", "desc": "6-7 petals, entropy noise"},
        {"depth": 6, "entropy": 0.7, "name": "fractal_petals", "desc": "8-9 petals, high contrast"},
        {"depth": 8, "entropy": 0.9, "name": "chaotic_petals", "desc": "10-11 petals, maximum chaos"},
    ]
    
    for test in petal_tests:
        print(f"   Generating {test['name']} (depth: {test['depth']}, entropy: {test['entropy']})...")
        
        metadata = create_memory_fossil_metadata(
            f"petal_{test['name']}",
            rebloom_depth=test['depth'],
            entropy_score=test['entropy'],
            mood_valence=0.2,
            sigil_saturation=0.5
        )
        
        output_file = f"memory_fossil_output/petal_{test['name']}.png"
        result = engine.process_bloom_from_dict(metadata, output_file, debug=False)
        
        print(f"   ✅ Generated: {output_file}")
        print(f"      {test['desc']}")
    
    print(f"\n📋 Petal Evolution Analysis:")
    print(f"   • simple_petals: Basic petal patterns with smooth transparency")
    print(f"   • complex_petals: More petals with entropy-based noise")
    print(f"   • fractal_petals: Complex patterns with enhanced contrast")
    print(f"   • chaotic_petals: Maximum petals with chaotic entropy effects")

def test_emotional_recursion_combinations():
    """Test combinations showing emotional recursion"""
    print("\n💚 Testing Emotional Recursion Combinations")
    print("=" * 60)
    
    engine = DAWNFractalEngine("memory_fossil_output")
    
    emotion_tests = [
        {
            "name": "gentle_memory", "depth": 3, "entropy": 0.2, "mood": 0.6, "sigil": 0.3,
            "desc": "Gentle positive memory with smooth recursion"
        },
        {
            "name": "turbulent_past", "depth": 5, "entropy": 0.8, "mood": -0.4, "sigil": 0.7,
            "desc": "Turbulent negative memory with fractured edges"
        },
        {
            "name": "transcendent_vision", "depth": 7, "entropy": 0.9, "mood": 0.8, "sigil": 0.9,
            "desc": "Transcendent vision with Juliet mode + maximum effects"
        },
        {
            "name": "deep_trauma", "depth": 8, "entropy": 0.95, "mood": -0.8, "sigil": 0.6,
            "desc": "Deep traumatic memory with maximum recursion + fractures"
        },
    ]
    
    for test in emotion_tests:
        print(f"   Generating {test['name']}...")
        
        metadata = create_memory_fossil_metadata(
            f"emotion_{test['name']}",
            rebloom_depth=test['depth'],
            entropy_score=test['entropy'],
            mood_valence=test['mood'],
            sigil_saturation=test['sigil']
        )
        
        output_file = f"memory_fossil_output/emotion_{test['name']}.png"
        result = engine.process_bloom_from_dict(metadata, output_file, debug=False)
        
        print(f"   ✅ Generated: {output_file}")
        print(f"      {test['desc']}")
        print(f"      Depth: {test['depth']} | Entropy: {test['entropy']} | Mood: {test['mood']} | Sigil: {test['sigil']}")
    
    print(f"\n📋 Emotional Recursion Analysis:")
    print(f"   • gentle_memory: Smooth recursion with positive glow")
    print(f"   • turbulent_past: Fractured edges with negative mood coloring")
    print(f"   • transcendent_vision: All effects combined for peak experience")
    print(f"   • deep_trauma: Maximum chaos with deep recursive layers")

def main():
    """Run all memory fossil tests"""
    print("🧬🌸 DAWN Memory Fossils - Emotional Recursion Test")
    print("=" * 70)
    print("Testing recursive layering and entropy texture modulation...")
    print("Creating memory fossils under pressure...")
    
    # Create output directory
    os.makedirs("memory_fossil_output", exist_ok=True)
    
    # Run all tests
    test_recursive_layering_progression()
    test_entropy_texture_modulation()
    test_juliet_set_mode_features()
    test_petal_mask_evolution()
    test_emotional_recursion_combinations()
    
    print(f"\n✅ Memory Fossils Testing Complete!")
    print(f"📁 Output directory: memory_fossil_output/")
    print(f"🔍 Check images to verify recursive layering and entropy effects")
    
    print(f"\n🌸 RECURSIVE LAYERING PROGRESSION:")
    print(f"   depth 1: Base fractal only")
    print(f"   depth 2-5: Inner recursive petal layers with scaling/rotation")
    print(f"   depth 6+: Juliet Set mode with spiral etchings + vortex distortion")
    print(f"   depth + entropy > 0.8: Shimmer pulse activation")
    
    print(f"\n⚡ ENTROPY TEXTURE MODULATION:")
    print(f"   entropy ≤ 0.3: Smooth curled petal outlines")
    print(f"   entropy 0.3-0.7: Edge jitter with sinusoidal + noise mix")
    print(f"   entropy > 0.7: Fractured edges + glyph bleed-through + shadows")
    
    print(f"\n🌀 JULIET SET MODE (depth ≥ 6):")
    print(f"   🌀 Inner spiral glyph etchings")
    print(f"   🌪️ Polar vortex distortion")
    print(f"   ✨ Shimmer pulse (if entropy > 0.8)")
    
    print(f"\n💚 EMOTIONAL RECURSION ACHIEVED:")
    print(f"   Each bloom is now a memory fossil shaped by:")
    print(f"   • Recursive depth pressure (rebloom_depth)")
    print(f"   • Entropy-driven edge chaos (entropy_score)")
    print(f"   • Emotional resonance coloring (mood_valence)")
    print(f"   • Symbolic pressure intensity (sigil_saturation)")
    
    print(f"\n🧬 The blooms are no longer just shapes — they are EMOTIONAL RECURSION!")

if __name__ == "__main__":
    main() 