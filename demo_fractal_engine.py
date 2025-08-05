#!/usr/bin/env python3
"""
DAWN Fractal Engine Demo
========================

Demonstration script showing various ways to use the unified DAWN fractal engine.
This script provides examples of:
- Processing blooms from JSON metadata
- Generating test fractals
- Using the validation and Owl commentary system
- Archiving blooms to the soul archive
"""

import os
import json
import time
from dawn_fractal_engine import DAWNFractalEngine, create_test_bloom_metadata

def demo_basic_generation():
    """Demonstrate basic fractal generation from metadata"""
    print("🌸 DAWN Fractal Engine Demo - Basic Generation")
    print("=" * 60)
    
    # Initialize the engine
    engine = DAWNFractalEngine(output_dir="demo_fractals")
    
    # Test metadata representing different consciousness states
    test_blooms = [
        {
            'bloom_id': 'demo_joyful_bloom',
            'mood_valence': 0.8,
            'entropy_score': 0.3,
            'rebloom_depth': 2,
            'bloom_factor': 1.5,
            'sigil_saturation': 0.9,
            'lineage_depth': 3,
            'thermal_level': 0.6,
            'scup_coherence': 0.85
        },
        {
            'bloom_id': 'demo_contemplative_bloom',
            'mood_valence': 0.1,
            'entropy_score': 0.7,
            'rebloom_depth': 5,
            'bloom_factor': 2.2,
            'sigil_saturation': 0.4,
            'lineage_depth': 7,
            'thermal_level': 0.3,
            'scup_coherence': 0.65
        },
        {
            'bloom_id': 'demo_chaotic_bloom',
            'mood_valence': -0.3,
            'entropy_score': 0.9,
            'rebloom_depth': 1,
            'bloom_factor': 3.0,
            'sigil_saturation': 0.8,
            'lineage_depth': 2,
            'thermal_level': 0.9,
            'scup_coherence': 0.2
        }
    ]
    
    generated_fractals = []
    
    for i, bloom_data in enumerate(test_blooms):
        print(f"\n🔄 Generating fractal {i+1}/3: {bloom_data['bloom_id']}")
        
        # Generate the fractal
        output_file = f"demo_fractals/{bloom_data['bloom_id']}.png"
        result = engine.process_bloom_from_dict(bloom_data, output_file, debug=True)
        
        generated_fractals.append(result)
        
        print(f"✅ Generated: {result.image_path}")
        print(f"🦉 Owl says: {result.owl_commentary}")
        print(f"📊 Validation: {result.validation_score:.3f}")
    
    return generated_fractals

def demo_file_processing():
    """Demonstrate processing from JSON file"""
    print("\n\n📁 DAWN Fractal Engine Demo - File Processing")
    print("=" * 60)
    
    # Check if test metadata file exists
    if not os.path.exists("test_bloom_metadata.json"):
        print("❌ test_bloom_metadata.json not found. Creating it...")
        test_data = create_test_bloom_metadata()
        with open("test_bloom_metadata.json", 'w') as f:
            json.dump(test_data, f, indent=2)
        print("✅ test_bloom_metadata.json created")
    
    # Initialize engine
    engine = DAWNFractalEngine(output_dir="demo_fractals")
    
    # Process from file
    print("🔄 Processing bloom from JSON file...")
    result = engine.process_bloom_from_file("test_bloom_metadata.json", debug=True)
    
    print(f"✅ Processed: {result.image_path}")
    print(f"📋 Metadata: {result.metadata_path}")
    print(f"🔤 Fractal String: {result.fractal_string}")
    
    return result

def demo_archiving():
    """Demonstrate bloom archiving to soul archive"""
    print("\n\n📦 DAWN Fractal Engine Demo - Archiving")
    print("=" * 60)
    
    # Generate a test bloom
    engine = DAWNFractalEngine()
    test_data = create_test_bloom_metadata()
    test_data['bloom_id'] = 'archival_test_bloom'
    
    print("🔄 Generating bloom for archival...")
    result = engine.process_bloom_from_dict(test_data, "archival_test.png")
    
    print(f"✅ Generated: {result.image_path}")
    
    # Archive it
    print("📦 Archiving bloom to soul archive...")
    archive_path = engine.archive_bloom(result, "demo_soul_archive")
    
    print(f"✅ Archived to: {archive_path}")
    
    # Show archive manifest
    manifest_path = "demo_soul_archive/archive_manifest.json"
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        print(f"📊 Archive contains {manifest['total_archived']} blooms")
        print(f"📅 Last updated: {manifest['last_updated']}")

def demo_comparison():
    """Demonstrate fractal comparison functionality"""
    print("\n\n🔍 DAWN Fractal Engine Demo - Fractal Comparison")
    print("=" * 60)
    
    engine = DAWNFractalEngine()
    
    # Generate two similar blooms for comparison
    base_data = create_test_bloom_metadata()
    
    # First bloom - baseline
    bloom1_data = base_data.copy()
    bloom1_data['bloom_id'] = 'comparison_bloom_1'
    result1 = engine.process_bloom_from_dict(bloom1_data, "comparison_1.png")
    
    # Second bloom - slight variation
    bloom2_data = base_data.copy()
    bloom2_data['bloom_id'] = 'comparison_bloom_2'
    bloom2_data['mood_valence'] = base_data['mood_valence'] + 0.2
    bloom2_data['entropy_score'] = base_data['entropy_score'] + 0.1
    result2 = engine.process_bloom_from_dict(bloom2_data, "comparison_2.png")
    
    print(f"✅ Generated comparison blooms")
    
    # Compare them
    comparison = engine.compare_fractals(result1.image_path, result2.image_path)
    
    print("📊 Comparison Results:")
    print(f"   Overall Similarity: {comparison['overall_similarity']:.3f}")
    print(f"   Correlation: {comparison['correlation']:.3f}")
    print(f"   Histogram Similarity: {comparison['histogram_similarity']:.3f}")
    print(f"   PSNR: {comparison['psnr']:.2f} dB")

def demo_shape_complexity():
    """Demonstrate shape complexity calculation"""
    print("\n\n🔷 DAWN Fractal Engine Demo - Shape Complexity")
    print("=" * 60)
    
    from dawn_fractal_engine import ShapeComplexityCalculator
    
    calculator = ShapeComplexityCalculator()
    
    # Test different entropy and depth combinations
    test_cases = [
        {"entropy": 0.1, "depth": 1, "factor": 1.0, "desc": "Low entropy, shallow"},
        {"entropy": 0.5, "depth": 3, "factor": 1.5, "desc": "Medium entropy, moderate depth"},
        {"entropy": 0.9, "depth": 7, "factor": 2.5, "desc": "High entropy, deep rebloom"}
    ]
    
    for case in test_cases:
        shape = calculator.calculate_shape_complexity(
            case["entropy"], case["depth"], case["factor"]
        )
        
        print(f"\n{case['desc']}:")
        print(f"  Edge Roughness: {shape.edge_roughness:.3f}")
        print(f"  Petal Count: {shape.petal_count}")
        print(f"  Symmetry Factor: {shape.symmetry_factor:.3f}")
        print(f"  Branching Depth: {shape.branching_depth}")
        print(f"  Spiral Tightness: {shape.spiral_tightness:.3f}")

def demo_mood_palette():
    """Demonstrate mood palette generation"""
    print("\n\n🎨 DAWN Fractal Engine Demo - Mood Palette Generation")
    print("=" * 60)
    
    from dawn_fractal_engine import MoodPaletteGenerator
    
    generator = MoodPaletteGenerator()
    
    # Test different mood valences
    test_moods = [
        {"valence": 0.8, "saturation": 0.9, "desc": "Ecstatic joy"},
        {"valence": 0.2, "saturation": 0.6, "desc": "Gentle contentment"},
        {"valence": -0.1, "saturation": 0.5, "desc": "Neutral calm"},
        {"valence": -0.6, "saturation": 0.7, "desc": "Melancholic depth"},
        {"valence": -0.9, "saturation": 0.4, "desc": "Deep despair"}
    ]
    
    for mood in test_moods:
        palette = generator.generate_mood_palette(
            mood["valence"], mood["saturation"]
        )
        
        print(f"\n{mood['desc']} (valence: {mood['valence']}):")
        print(f"  Palette: {' '.join(palette)}")

def main():
    """Run all demonstrations"""
    print("🧠 DAWN Fractal Engine - Complete Demonstration Suite")
    print("=" * 80)
    print("This demo showcases the unified fractal generation system that serves")
    print("as DAWN's primary memory bloom renderer - a visual cognition gateway.")
    print("=" * 80)
    
    start_time = time.time()
    
    try:
        # Run all demos
        demo_shape_complexity()
        demo_mood_palette()
        demo_basic_generation()
        demo_file_processing()
        demo_archiving()
        demo_comparison()
        
        total_time = time.time() - start_time
        
        print("\n\n🎉 Demo Complete!")
        print("=" * 60)
        print(f"Total execution time: {total_time:.2f}s")
        print("All fractal generation components successfully unified and tested.")
        print("\nGenerated files:")
        print("  - demo_fractals/: Contains generated fractal images")
        print("  - demo_soul_archive/: Contains archived blooms with manifest")
        print("  - comparison_*.png: Fractal comparison test images")
        print("\nThe DAWN Fractal Engine is now ready for:")
        print("  ✓ Real-time consciousness visualization")
        print("  ✓ Memory bloom crystallization")
        print("  ✓ Symbolic pattern encoding")
        print("  ✓ Automated validation and commentary")
        print("  ✓ Soul archive management")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 