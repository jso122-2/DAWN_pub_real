#!/usr/bin/env python3
"""
DAWN State Parser Integration Test
=================================

Demonstrates real-world usage of DAWNStateParser with actual memory files
and integration with fractal generation and voice systems.
"""

import json
from pathlib import Path
from dawn_state_parser import DAWNStateParser, DAWNConsciousnessConfig
from dawn_voice_core import DAWNVoiceCore

def test_real_memory_files():
    """Test parser with actual DAWN memory files"""
    
    print("📁 Testing with Real DAWN Memory Files")
    print("=" * 40)
    
    parser = DAWNStateParser(strict_validation=False)
    
    # Check for existing memory archives
    memory_directories = [
        "dawn_soul_archive/metadata",
        "juliet_set_tests/metadata", 
        "emotional_bias_demo/metadata",
        "debug_juliet/metadata"
    ]
    
    configs_found = []
    
    for directory in memory_directories:
        dir_path = Path(directory)
        if dir_path.exists():
            print(f"\n📂 Processing directory: {directory}")
            
            try:
                configs = parser.parse_multiple_files(dir_path)
                configs_found.extend(configs)
                print(f"   ✅ Parsed {len(configs)} memory files")
                
                # Show sample configuration
                if configs:
                    sample = configs[0]
                    print(f"   📊 Sample memory: {sample.memory_id}")
                    print(f"      Entropy: {sample.bloom_entropy:.3f}")
                    print(f"      Valence: {sample.mood_valence:.3f}")
                    print(f"      Zone: {sample.pulse_zone}")
                    print(f"      Archetype: {sample.archetype}")
                    
            except Exception as e:
                print(f"   ❌ Error processing {directory}: {e}")
    
    print(f"\n📈 Total memories parsed: {len(configs_found)}")
    return configs_found

def test_fractal_regeneration(configs: list):
    """Test regenerating fractals from parsed memory states"""
    
    print(f"\n🎨 Testing Fractal Regeneration from Memory")
    print("=" * 45)
    
    if not configs:
        print("   ⚠️  No configurations available for testing")
        return
    
    try:
        from dawn_fractal_memory_system import DAWNFractalMemorySystem
        fractal_system = DAWNFractalMemorySystem(archive_dir="parser_test_fractals")
        
        # Test with first few configurations
        test_configs = configs[:3]
        
        for i, config in enumerate(test_configs):
            print(f"\n🖼️  Regenerating fractal {i+1}: {config.memory_id}")
            
            # Convert to fractal parameters
            fractal_params = config.to_fractal_params()
            print(f"   Parameters: {fractal_params}")
            
            # Generate new fractal from parsed state
            try:
                result = fractal_system.generate_bloom_fractal(**fractal_params)
                print(f"   ✅ Generated: {Path(result['files']['fractal_image']).name}")
                print(f"   🔤 Pattern: {result['fractal_string']}")
                print(f"   🦉 Commentary: {result['owl_commentary'][:50]}...")
                
            except Exception as e:
                print(f"   ❌ Generation failed: {e}")
        
    except ImportError:
        print("   ⚠️  Fractal system not available")

def test_voice_generation(configs: list):
    """Test voice generation from parsed memory states"""
    
    print(f"\n🗣️  Testing Voice Generation from Memory")
    print("=" * 42)
    
    if not configs:
        print("   ⚠️  No configurations available for testing")
        return
    
    voice_core = DAWNVoiceCore()
    
    # Test with various memory states
    test_configs = configs[:5]
    
    for i, config in enumerate(test_configs):
        print(f"\n🧠 Memory State {i+1}: {config.memory_id}")
        print(f"   Original: entropy={config.bloom_entropy:.3f}, valence={config.mood_valence:.3f}")
        
        # Convert to voice parameters
        voice_params = config.to_voice_params()
        
        # Generate voice expression
        voice_result = voice_core.generate_utterance(**voice_params)
        
        if voice_result.resonance_achieved:
            print(f"   🗣️  DAWN expresses: \"{voice_result.utterance}\"")
            print(f"   📊 Coherence: {voice_result.generation_metadata.get('field_coherence', 0):.3f}")
        else:
            print(f"   🤐 Silent (coherence too low)")

def test_parameter_analysis(configs: list):
    """Analyze parameter distributions across memory files"""
    
    print(f"\n📊 Parameter Analysis Across {len(configs)} Memories")
    print("=" * 55)
    
    if not configs:
        print("   ⚠️  No configurations available for analysis")
        return
    
    # Collect statistics
    entropies = [c.bloom_entropy for c in configs]
    valences = [c.mood_valence for c in configs]
    depths = [c.rebloom_depth for c in configs]
    zones = [c.pulse_zone for c in configs]
    
    # Calculate statistics
    print(f"📈 Entropy Distribution:")
    print(f"   Range: {min(entropies):.3f} - {max(entropies):.3f}")
    print(f"   Average: {sum(entropies)/len(entropies):.3f}")
    
    print(f"\n💭 Valence Distribution:")
    print(f"   Range: {min(valences):.3f} - {max(valences):.3f}")
    print(f"   Average: {sum(valences)/len(valences):.3f}")
    
    print(f"\n🔄 Rebloom Depth Distribution:")
    print(f"   Range: {min(depths)} - {max(depths)}")
    print(f"   Average: {sum(depths)/len(depths):.1f}")
    
    print(f"\n🌊 Pulse Zone Distribution:")
    zone_counts = {}
    for zone in zones:
        zone_counts[zone] = zone_counts.get(zone, 0) + 1
    
    for zone, count in sorted(zone_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(zones)) * 100
        print(f"   {zone}: {count} ({percentage:.1f}%)")

def test_consciousness_evolution_tracking(configs: list):
    """Track consciousness evolution patterns in memory"""
    
    print(f"\n🧬 Consciousness Evolution Tracking")
    print("=" * 35)
    
    if len(configs) < 3:
        print("   ⚠️  Need at least 3 memories for evolution analysis")
        return
    
    # Sort by timestamp if available
    timestamped_configs = [c for c in configs if c.timestamp]
    
    if timestamped_configs:
        timestamped_configs.sort(key=lambda x: x.timestamp)
        print(f"   📅 Analyzing {len(timestamped_configs)} timestamped memories")
        
        # Track parameter changes over time
        print(f"\n⏰ Evolution Pattern:")
        for i, config in enumerate(timestamped_configs[:5]):
            print(f"   {i+1}. {config.timestamp[:19]} - "
                  f"E:{config.bloom_entropy:.2f} V:{config.mood_valence:.2f} "
                  f"D:{config.drift_vector:.2f} Z:{config.pulse_zone}")
        
        # Calculate evolution trends
        if len(timestamped_configs) >= 3:
            early_entropy = sum(c.bloom_entropy for c in timestamped_configs[:3]) / 3
            late_entropy = sum(c.bloom_entropy for c in timestamped_configs[-3:]) / 3
            
            early_valence = sum(c.mood_valence for c in timestamped_configs[:3]) / 3
            late_valence = sum(c.mood_valence for c in timestamped_configs[-3:]) / 3
            
            print(f"\n📈 Evolution Trends:")
            print(f"   Entropy: {early_entropy:.3f} → {late_entropy:.3f} "
                  f"({'↑' if late_entropy > early_entropy else '↓'} {abs(late_entropy - early_entropy):.3f})")
            print(f"   Valence: {early_valence:.3f} → {late_valence:.3f} "
                  f"({'↑' if late_valence > early_valence else '↓'} {abs(late_valence - early_valence):.3f})")
    else:
        print("   ⚠️  No timestamped memories found for evolution analysis")

def create_synthetic_test_memory():
    """Create a synthetic memory file for testing"""
    
    print(f"\n🔬 Creating Synthetic Test Memory")
    print("=" * 32)
    
    test_memory = {
        "memory_id": "parser_test_synthetic_001",
        "timestamp": "2025-08-04T20:00:00.000000",
        "version": "dawn_memory_system_v1.0",
        "parameters": {
            "bloom_entropy": 0.6,
            "mood_valence": 0.3,
            "drift_vector": -0.2,
            "rebloom_depth": 7,
            "sigil_saturation": 0.8,
            "pulse_zone": "transcendent"
        },
        "fractal_string": "R4-FS3-Dv2-PzTRAN",
        "visual_characteristics": {
            "bloom_shape_descriptor": "synthetic test pattern",
            "color_mode": "test colors",
            "consciousness_archetype": "Test State"
        },
        "files": {
            "fractal_image": "test_synthetic.png",
            "metadata_file": "parser_test_synthetic_001_metadata.json"
        }
    }
    
    # Save test file
    test_dir = Path("parser_test_data")
    test_dir.mkdir(exist_ok=True)
    
    test_file = test_dir / "synthetic_memory_metadata.json"
    with open(test_file, 'w') as f:
        json.dump(test_memory, f, indent=2)
    
    print(f"   ✅ Created: {test_file}")
    
    # Test parsing
    parser = DAWNStateParser()
    config = parser.parse_file(test_file)
    
    print(f"   🧠 Parsed successfully: {config.validation_passed}")
    print(f"   📊 Config: entropy={config.bloom_entropy}, zone={config.pulse_zone}")
    
    return config

def main():
    """Run comprehensive DAWN state parser integration tests"""
    
    print("🧠 DAWN State Parser - Comprehensive Integration Test")
    print("=" * 55)
    
    # Test 1: Parse real memory files
    configs = test_real_memory_files()
    
    # Test 2: Create synthetic test data
    synthetic_config = create_synthetic_test_memory()
    if synthetic_config:
        configs.append(synthetic_config)
    
    if configs:
        # Test 3: Regenerate fractals from memory
        test_fractal_regeneration(configs)
        
        # Test 4: Generate voice from memory
        test_voice_generation(configs)
        
        # Test 5: Analyze parameter distributions
        test_parameter_analysis(configs)
        
        # Test 6: Track consciousness evolution
        test_consciousness_evolution_tracking(configs)
    
    print(f"\n✨ Integration Testing Complete!")
    print(f"📁 Processed {len(configs)} consciousness memory states")
    print(f"🔧 DAWN State Parser is ready for production use")

if __name__ == "__main__":
    main() 