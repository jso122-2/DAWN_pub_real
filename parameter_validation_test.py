#!/usr/bin/env python3
"""
DAWN Fractal Parameter Validation Test
======================================

Comprehensive validation tests to ensure all consciousness parameters 
create visible differences in fractal output.

Usage:
    python parameter_validation_test.py
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from dawn_fractal_engine import DAWNFractalEngine, create_test_bloom_metadata

def create_parameter_test_metadata(base_bloom_id: str, **overrides):
    """Create test metadata with specific parameter overrides"""
    base_metadata = {
        "bloom_id": base_bloom_id,
        "timestamp": datetime.now().isoformat(),
        "mood_valence": 0.0,
        "entropy_score": 0.5,
        "rebloom_depth": 2,
        "bloom_factor": 1.5,
        "sigil_saturation": 0.5,
        "lineage_depth": 2,
        "thermal_level": 0.5,
        "scup_coherence": 0.5,
        "drift_vector": [0.0, 0.0],
        "pulse_phase": 0.0,
        "state": "spawning",
        "parent_id": "validation_test"
    }
    
    # Apply overrides
    base_metadata.update(overrides)
    return base_metadata

def test_entropy_responsiveness():
    """Test 1: Entropy should create dramatic complexity differences"""
    print("\n🧪 Test 1: Entropy Responsiveness")
    print("=" * 50)
    
    engine = DAWNFractalEngine("validation_output")
    
    entropy_values = [0.1, 0.5, 0.9]
    for entropy in entropy_values:
        print(f"   Generating entropy {entropy} fractal...")
        
        metadata = create_parameter_test_metadata(
            f"entropy_test_{entropy}",
            entropy_score=entropy
        )
        
        output_file = f"validation_output/entropy_{entropy}_test.png"
        result = engine.process_bloom_from_dict(metadata, output_file, debug=False)
        
        print(f"   ✅ Generated: {output_file}")
        print(f"      Fractal String: {result.fractal_string}")
    
    print("\n📋 Analysis: Check if entropy 0.1 (simple) vs 0.9 (chaotic) show dramatic visual differences")

def test_drift_vector_responsiveness():
    """Test 2: Drift vector should create visible offsets/rotations"""
    print("\n🧪 Test 2: Drift Vector Responsiveness")
    print("=" * 50)
    
    engine = DAWNFractalEngine("validation_output")
    
    drift_vectors = [
        [0.0, 0.0],    # No drift
        [0.3, 0.1],    # Small drift
        [-0.2, 0.4],   # Different direction
        [0.5, -0.3],   # Strong drift
    ]
    
    for i, drift in enumerate(drift_vectors):
        print(f"   Generating drift vector {drift} fractal...")
        
        metadata = create_parameter_test_metadata(
            f"drift_test_{i}",
            drift_vector=drift
        )
        
        output_file = f"validation_output/drift_{i}_test.png"
        result = engine.process_bloom_from_dict(metadata, output_file, debug=False)
        
        print(f"   ✅ Generated: {output_file}")
        print(f"      Drift: {drift} -> {result.fractal_string}")
    
    print("\n📋 Analysis: Each drift vector should create visibly different patterns/positions")

def test_rebloom_depth_layering():
    """Test 3: Rebloom depth should create visible layer count differences"""
    print("\n🧪 Test 3: Rebloom Depth Layering")
    print("=" * 50)
    
    engine = DAWNFractalEngine("validation_output")
    
    rebloom_depths = [1, 3, 5]
    for depth in rebloom_depths:
        print(f"   Generating rebloom depth {depth} fractal...")
        
        metadata = create_parameter_test_metadata(
            f"rebloom_test_{depth}",
            rebloom_depth=depth
        )
        
        output_file = f"validation_output/rebloom_{depth}_test.png"
        result = engine.process_bloom_from_dict(metadata, output_file, debug=False)
        
        print(f"   ✅ Generated: {output_file}")
        print(f"      Layers: {depth} -> Processing time: {result.processing_time:.1f}s")
    
    print("\n📋 Analysis: Higher rebloom depths should show multiple overlapping fractal layers")

def test_edge_roughness_effects():
    """Test 4: Edge roughness should create smooth vs chaotic boundaries"""
    print("\n🧪 Test 4: Edge Roughness Effects")
    print("=" * 50)
    
    engine = DAWNFractalEngine("validation_output")
    
    roughness_values = [0.1, 0.5, 0.9]
    for roughness in roughness_values:
        print(f"   Generating edge roughness {roughness} fractal...")
        
        metadata = create_parameter_test_metadata(
            f"roughness_test_{roughness}",
            entropy_score=roughness  # Using entropy_score as edge_roughness proxy
        )
        
        output_file = f"validation_output/roughness_{roughness}_test.png"
        result = engine.process_bloom_from_dict(metadata, output_file, debug=False)
        
        print(f"   ✅ Generated: {output_file}")
        print(f"      Roughness: {roughness} -> {result.fractal_string}")
    
    print("\n📋 Analysis: Edge roughness 0.1 (smooth) vs 0.9 (chaotic) should show boundary differences")

def test_thermal_mood_effects():
    """Test 5: Thermal and mood should create color temperature differences"""
    print("\n🧪 Test 5: Thermal and Mood Effects")
    print("=" * 50)
    
    engine = DAWNFractalEngine("validation_output")
    
    test_combinations = [
        {"thermal_level": 0.1, "mood_valence": -0.7, "name": "cold_sad"},
        {"thermal_level": 0.5, "mood_valence": 0.0, "name": "neutral"},
        {"thermal_level": 0.9, "mood_valence": 0.8, "name": "hot_happy"},
    ]
    
    for combo in test_combinations:
        print(f"   Generating {combo['name']} fractal...")
        
        metadata = create_parameter_test_metadata(
            f"thermal_mood_{combo['name']}",
            thermal_level=combo['thermal_level'],
            mood_valence=combo['mood_valence']
        )
        
        output_file = f"validation_output/thermal_mood_{combo['name']}_test.png"
        result = engine.process_bloom_from_dict(metadata, output_file, debug=False)
        
        print(f"   ✅ Generated: {output_file}")
        print(f"      {combo['name']}: thermal={combo['thermal_level']}, mood={combo['mood_valence']}")
    
    print("\n📋 Analysis: cold_sad should be blue/dark, hot_happy should be orange/bright")

def test_scup_pulse_effects():
    """Test 6: SCUP coherence and pulse phase should create glow/rhythm effects"""
    print("\n🧪 Test 6: SCUP and Pulse Effects")
    print("=" * 50)
    
    engine = DAWNFractalEngine("validation_output")
    
    test_combinations = [
        {"scup_coherence": 0.1, "pulse_phase": 0.0, "name": "low_scup_no_pulse"},
        {"scup_coherence": 0.9, "pulse_phase": 0.0, "name": "high_scup_no_pulse"},
        {"scup_coherence": 0.9, "pulse_phase": 3.14, "name": "high_scup_with_pulse"},
    ]
    
    for combo in test_combinations:
        print(f"   Generating {combo['name']} fractal...")
        
        metadata = create_parameter_test_metadata(
            f"scup_pulse_{combo['name']}",
            scup_coherence=combo['scup_coherence'],
            pulse_phase=combo['pulse_phase']
        )
        
        output_file = f"validation_output/scup_pulse_{combo['name']}_test.png"
        result = engine.process_bloom_from_dict(metadata, output_file, debug=False)
        
        print(f"   ✅ Generated: {output_file}")
        print(f"      {combo['name']}: SCUP={combo['scup_coherence']}, pulse={combo['pulse_phase']}")
    
    print("\n📋 Analysis: High SCUP should add glow, pulse_phase should create brightness patterns")

def test_color_palette_utilization():
    """Test 7: Verify full 5-color palette is being used"""
    print("\n🧪 Test 7: Color Palette Utilization")
    print("=" * 50)
    
    engine = DAWNFractalEngine("validation_output")
    
    # Generate high-entropy fractal to ensure complex iteration patterns
    metadata = create_parameter_test_metadata(
        "color_palette_test",
        entropy_score=0.8,
        rebloom_depth=3,
        thermal_level=0.6,
        mood_valence=0.4
    )
    
    output_file = "validation_output/color_palette_test.png"
    result = engine.process_bloom_from_dict(metadata, output_file, debug=True)
    
    print(f"   ✅ Generated: {output_file}")
    print(f"      High complexity fractal for color analysis")
    
    print("\n📋 Analysis: Check if multiple colors from palette are visible (not just 2 colors)")

def generate_comparison_grid():
    """Generate a grid of comparison fractals for visual validation"""
    print("\n🎨 Generating Comparison Grid")
    print("=" * 50)
    
    engine = DAWNFractalEngine("validation_output")
    
    # Create matrix of parameter combinations
    parameter_matrix = [
        {"entropy": 0.2, "depth": 1, "thermal": 0.2, "mood": -0.5, "name": "simple_cold_sad"},
        {"entropy": 0.2, "depth": 1, "thermal": 0.8, "mood": 0.5, "name": "simple_hot_happy"},
        {"entropy": 0.8, "depth": 1, "thermal": 0.2, "mood": -0.5, "name": "complex_cold_sad"},
        {"entropy": 0.8, "depth": 1, "thermal": 0.8, "mood": 0.5, "name": "complex_hot_happy"},
        {"entropy": 0.2, "depth": 4, "thermal": 0.5, "mood": 0.0, "name": "simple_layered"},
        {"entropy": 0.8, "depth": 4, "thermal": 0.5, "mood": 0.0, "name": "complex_layered"},
    ]
    
    for combo in parameter_matrix:
        print(f"   Generating {combo['name']}...")
        
        metadata = create_parameter_test_metadata(
            f"grid_{combo['name']}",
            entropy_score=combo['entropy'],
            rebloom_depth=combo['depth'],
            thermal_level=combo['thermal'],
            mood_valence=combo['mood'],
            drift_vector=[combo['entropy'] * 0.3, combo['mood'] * 0.2]
        )
        
        output_file = f"validation_output/grid_{combo['name']}.png"
        result = engine.process_bloom_from_dict(metadata, output_file, debug=False)
        
        print(f"   ✅ {combo['name']}: {result.fractal_string}")
    
    print("\n📋 Analysis: Each grid image should show distinct visual characteristics")

def main():
    """Run comprehensive parameter validation tests"""
    print("🌸 DAWN Fractal Parameter Validation Test Suite")
    print("=" * 60)
    print("Testing visual responsiveness of consciousness parameters...")
    
    # Create output directory
    os.makedirs("validation_output", exist_ok=True)
    
    start_time = time.time()
    
    # Run all validation tests
    test_entropy_responsiveness()
    test_drift_vector_responsiveness()
    test_rebloom_depth_layering()
    test_edge_roughness_effects()
    test_thermal_mood_effects()
    test_scup_pulse_effects()
    test_color_palette_utilization()
    generate_comparison_grid()
    
    total_time = time.time() - start_time
    
    print(f"\n✅ Validation Complete!")
    print(f"⏱️  Total time: {total_time:.1f}s")
    print(f"📁 Output directory: validation_output/")
    print(f"🔍 Check images to verify parameter responsiveness")
    
    print("\n🎯 SUCCESS CRITERIA:")
    print("   • Entropy 0.1 vs 0.9 should show dramatic complexity differences")
    print("   • Drift vectors should create visibly different positions/rotations")
    print("   • Rebloom depths should show layering (1 vs 3 vs 5 layers)")
    print("   • Edge roughness should show smooth vs chaotic boundaries")
    print("   • Thermal/mood should show cool/warm color temperature shifts")
    print("   • SCUP/pulse should show glow and brightness pattern effects")
    print("   • Color palettes should use multiple colors (not just 2)")
    print("\n🌸 Every parameter change should produce a VISIBLE difference!")

if __name__ == "__main__":
    main() 