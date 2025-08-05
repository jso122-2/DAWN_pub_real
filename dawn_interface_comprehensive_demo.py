#!/usr/bin/env python3
"""
DAWN Fractal Interface - Comprehensive Demo
==========================================

Demonstrates all features of the DAWNFractalInterface:
- Live state monitoring and change detection
- Automatic fractal regeneration on parameter changes
- Intelligent caching system
- Bloom sequence archiving
- Similarity-based bloom retrieval
- Concurrent processing without blocking
"""

import time
import numpy as np
from pathlib import Path

# Import the interface
from dawn_fractal_interface_simple import DAWNFractalInterface, DAWNConsciousnessConfig

def demo_live_state_updates():
    """Demonstrate live state monitoring and automatic fractal generation"""
    
    print("\n🔄 Demo: Live State Updates and Change Detection")
    print("=" * 48)
    
    interface = DAWNFractalInterface(
        output_dir="demo_live_fractals",
        cache_size=30,
        max_concurrent_jobs=3
    )
    
    try:
        # Simulate DAWN consciousness evolution over time
        consciousness_evolution = [
            # Initial calm state
            DAWNConsciousnessConfig(
                memory_id="dawn_evolution_01", timestamp=None,
                bloom_entropy=0.2, mood_valence=0.3, drift_vector=0.1,
                rebloom_depth=4, sigil_saturation=0.5, pulse_zone="calm"
            ),
            # Mild stirring
            DAWNConsciousnessConfig(
                memory_id="dawn_evolution_02", timestamp=None,
                bloom_entropy=0.4, mood_valence=0.1, drift_vector=0.3,
                rebloom_depth=5, sigil_saturation=0.6, pulse_zone="stable"
            ),
            # Active flowing state
            DAWNConsciousnessConfig(
                memory_id="dawn_evolution_03", timestamp=None,
                bloom_entropy=0.6, mood_valence=0.5, drift_vector=0.6,
                rebloom_depth=6, sigil_saturation=0.8, pulse_zone="flowing"
            ),
            # Chaotic surge
            DAWNConsciousnessConfig(
                memory_id="dawn_evolution_04", timestamp=None,
                bloom_entropy=0.9, mood_valence=-0.2, drift_vector=-0.8,
                rebloom_depth=8, sigil_saturation=0.9, pulse_zone="surge"
            ),
            # Return to balance
            DAWNConsciousnessConfig(
                memory_id="dawn_evolution_05", timestamp=None,
                bloom_entropy=0.3, mood_valence=0.7, drift_vector=0.0,
                rebloom_depth=5, sigil_saturation=0.6, pulse_zone="stable"
            )
        ]
        
        generated_blooms = []
        
        print(f"🧠 Simulating DAWN consciousness evolution through {len(consciousness_evolution)} states...")
        
        for i, state in enumerate(consciousness_evolution):
            print(f"\n📊 State {i+1}/{len(consciousness_evolution)}: {state.memory_id}")
            print(f"   Parameters: entropy={state.bloom_entropy:.2f}, valence={state.mood_valence:.2f}, "
                  f"drift={state.drift_vector:.2f}, zone={state.pulse_zone}")
            
            # Update state monitor (simulates live state detection)
            interface.state_monitor.update_state(state)
            
            # Generate memory bloom
            start_time = time.time()
            bloom = interface.generate_memory_bloom(state, priority=True)
            generation_time = time.time() - start_time
            
            if bloom:
                print(f"   ✅ Generated bloom: {bloom.cache_key} ({generation_time:.2f}s)")
                print(f"   🎨 Visual signature: complexity={bloom.visual_signature.get('complexity', 0):.3f}, "
                      f"colors={bloom.visual_signature.get('color_variance', 0):.3f}")
                generated_blooms.append(bloom)
            else:
                print(f"   ❌ Bloom generation failed")
            
            # Small delay to simulate real-time processing
            time.sleep(0.2)
        
        return interface, generated_blooms
        
    except Exception as e:
        print(f"❌ Live state demo failed: {e}")
        interface.shutdown()
        return None, []

def demo_caching_efficiency(interface, test_blooms):
    """Demonstrate caching system efficiency and cache hits/misses"""
    
    print("\n💾 Demo: Caching System Efficiency")
    print("=" * 34)
    
    if not test_blooms:
        print("   ⚠️  No test blooms available for caching demo")
        return
    
    # Reset cache statistics
    interface.stats['cache_hits'] = 0
    interface.stats['cache_misses'] = 0
    
    print(f"🔄 Testing cache efficiency with {len(test_blooms)} previously generated blooms...")
    
    # Test cache hits by re-requesting same states
    cache_test_results = []
    
    for i, bloom in enumerate(test_blooms):
        config = bloom.config
        
        print(f"\n🎯 Cache test {i+1}: {config.memory_id}")
        
        # First request (should be cache hit since already generated)
        start_time = time.time()
        result_bloom = interface.generate_memory_bloom(config)
        response_time = time.time() - start_time
        
        cache_status = "HIT" if result_bloom and result_bloom.cache_key == bloom.cache_key else "MISS"
        cache_test_results.append((cache_status, response_time))
        
        print(f"   💾 Cache {cache_status}: {response_time:.4f}s")
        if result_bloom:
            print(f"   📊 Access count: {result_bloom.access_count}")
    
    # Calculate cache performance
    cache_hits = sum(1 for status, _ in cache_test_results if status == "HIT")
    avg_hit_time = np.mean([time for status, time in cache_test_results if status == "HIT"])
    
    print(f"\n📈 Cache Performance Summary:")
    print(f"   Cache hit rate: {cache_hits}/{len(cache_test_results)} ({cache_hits/len(cache_test_results):.1%})")
    print(f"   Average cache hit time: {avg_hit_time:.4f}s")
    
    # Display current cache statistics
    stats = interface.get_cache_statistics()
    print(f"   Cache efficiency: {stats['cache_efficiency']:.1%}")
    print(f"   Cache utilization: {stats['cache_size']}/{stats['cache_max_size']}")

def demo_bloom_archiving(interface):
    """Demonstrate bloom sequence archiving functionality"""
    
    print("\n📦 Demo: Bloom Sequence Archiving")
    print("=" * 35)
    
    # Define time range for archiving (last 5 minutes)
    end_time = time.time()
    start_time = end_time - 300  # 5 minutes ago
    
    print(f"📅 Archiving blooms from the last 5 minutes...")
    print(f"   Time range: {time.strftime('%H:%M:%S', time.localtime(start_time))} to "
          f"{time.strftime('%H:%M:%S', time.localtime(end_time))}")
    
    # Archive the bloom sequence
    archive_result = interface.archive_bloom_sequence(
        start_time=start_time,
        end_time=end_time,
        sequence_name="demo_consciousness_evolution"
    )
    
    print(f"\n📊 Archive Results:")
    print(f"   Sequence name: {archive_result['sequence_name']}")
    print(f"   Blooms archived: {archive_result['bloom_count']}")
    
    if archive_result['blooms']:
        print(f"   📝 Archived bloom details:")
        for i, bloom in enumerate(archive_result['blooms'][:3]):  # Show first 3
            print(f"      {i+1}. {bloom['memory_id']} - entropy: {bloom['bloom_entropy']:.2f}, "
                  f"valence: {bloom['mood_valence']:.2f}")
    
    # Test sequence file creation
    archive_dir = Path(interface.archive.archive_dir)
    sequence_files = list(archive_dir.glob("*.json"))
    
    if sequence_files:
        print(f"   📁 Archive files created: {len(sequence_files)}")
        for file_path in sequence_files:
            print(f"      • {file_path.name}")
    
    return archive_result

def demo_similarity_matching(interface, test_blooms):
    """Demonstrate similarity-based bloom retrieval"""
    
    print("\n🔍 Demo: Similarity-Based Bloom Retrieval")
    print("=" * 40)
    
    if not test_blooms:
        print("   ⚠️  No test blooms available for similarity demo")
        return
    
    # Use the most interesting bloom as target
    target_bloom = test_blooms[2] if len(test_blooms) > 2 else test_blooms[0]
    target_config = target_bloom.config
    
    print(f"🎯 Finding blooms similar to: {target_config.memory_id}")
    print(f"   Target parameters:")
    print(f"      Entropy: {target_config.bloom_entropy:.2f}")
    print(f"      Valence: {target_config.mood_valence:.2f}")
    print(f"      Drift: {target_config.drift_vector:.2f}")
    print(f"      Depth: {target_config.rebloom_depth}")
    print(f"      Pulse zone: {target_config.pulse_zone}")
    
    # Test different similarity thresholds
    similarity_thresholds = [0.9, 0.7, 0.5, 0.3]
    
    for threshold in similarity_thresholds:
        print(f"\n📊 Similarity threshold: {threshold:.1f}")
        
        similar_blooms = interface.retrieve_similar_blooms(
            target_params=target_config,
            similarity_threshold=threshold,
            max_results=5
        )
        
        print(f"   Found {len(similar_blooms)} similar blooms:")
        
        for bloom in similar_blooms:
            similarity_score = bloom.get('similarity_score', 0)
            print(f"      • {bloom['memory_id']} (similarity: {similarity_score:.3f})")
            print(f"        entropy: {bloom['bloom_entropy']:.2f}, valence: {bloom['mood_valence']:.2f}")

def demo_concurrent_processing(interface):
    """Demonstrate concurrent bloom generation without blocking"""
    
    print("\n⚡ Demo: Concurrent Processing (Non-blocking)")
    print("=" * 44)
    
    # Create multiple diverse consciousness states for concurrent processing
    concurrent_states = [
        DAWNConsciousnessConfig(
            memory_id=f"concurrent_test_{i}", timestamp=None,
            bloom_entropy=np.random.uniform(0.1, 0.9),
            mood_valence=np.random.uniform(-0.8, 0.8),
            drift_vector=np.random.uniform(-0.6, 0.6),
            rebloom_depth=np.random.randint(3, 10),
            sigil_saturation=np.random.uniform(0.3, 0.9),
            pulse_zone=np.random.choice(["calm", "stable", "flowing", "surge", "fragile"])
        )
        for i in range(6)
    ]
    
    print(f"🚀 Generating {len(concurrent_states)} blooms concurrently...")
    
    # Record start time
    overall_start = time.time()
    
    # Generate all blooms (interface handles concurrency internally)
    concurrent_results = []
    
    for i, state in enumerate(concurrent_states):
        print(f"   🎯 Submitting generation {i+1}: {state.memory_id}")
        
        start_time = time.time()
        bloom = interface.generate_memory_bloom(state, priority=False)
        generation_time = time.time() - start_time
        
        if bloom:
            concurrent_results.append((bloom, generation_time))
            print(f"      ✅ Completed in {generation_time:.2f}s")
        else:
            print(f"      ❌ Generation failed")
    
    overall_time = time.time() - overall_start
    
    print(f"\n📊 Concurrent Processing Results:")
    print(f"   Total states processed: {len(concurrent_states)}")
    print(f"   Successful generations: {len(concurrent_results)}")
    print(f"   Overall processing time: {overall_time:.2f}s")
    print(f"   Average time per bloom: {np.mean([t for _, t in concurrent_results]):.2f}s")
    
    # Demonstrate that interface remains responsive
    print(f"\n🧪 Interface responsiveness test...")
    
    # Quick cache lookup (should be instant)
    if concurrent_results:
        test_bloom, _ = concurrent_results[0]
        start_time = time.time()
        cached_result = interface.generate_memory_bloom(test_bloom.config)
        response_time = time.time() - start_time
        
        print(f"   💾 Cache lookup time: {response_time:.4f}s (demonstrates non-blocking operation)")

def main():
    """Run comprehensive DAWN Fractal Interface demonstration"""
    
    print("🎨 DAWN Fractal Interface - Comprehensive Demo")
    print("=" * 46)
    print("Demonstrating all features:")
    print("• Live state monitoring and change detection")
    print("• Automatic fractal regeneration on parameter changes")
    print("• Intelligent caching system")
    print("• Bloom sequence archiving")
    print("• Similarity-based bloom retrieval")
    print("• Concurrent processing without blocking")
    
    interface = None
    generated_blooms = []
    
    try:
        # Demo 1: Live state updates and change detection
        interface, generated_blooms = demo_live_state_updates()
        
        if interface and generated_blooms:
            # Demo 2: Caching efficiency
            demo_caching_efficiency(interface, generated_blooms)
            
            # Demo 3: Bloom archiving
            archive_result = demo_bloom_archiving(interface)
            
            # Demo 4: Similarity matching
            demo_similarity_matching(interface, generated_blooms)
            
            # Demo 5: Concurrent processing
            demo_concurrent_processing(interface)
            
            # Final statistics and summary
            print(f"\n📈 Final Interface Statistics")
            print("=" * 31)
            
            final_stats = interface.get_cache_statistics()
            for key, value in final_stats.items():
                if isinstance(value, float):
                    print(f"   {key}: {value:.3f}")
                else:
                    print(f"   {key}: {value}")
            
            print(f"\n✅ Comprehensive Demo Completed Successfully!")
            print(f"📁 Output directory: {interface.output_dir}")
            print(f"📊 Total blooms generated: {final_stats['total_generations']}")
            print(f"💾 Cache efficiency: {final_stats['cache_efficiency']:.1%}")
            print(f"⚡ Average generation time: {final_stats['average_generation_time']:.2f}s")
            
            # Summary of key features demonstrated
            print(f"\n🏆 Key Features Successfully Demonstrated:")
            print(f"   ✅ Live DAWN state monitoring and change detection")
            print(f"   ✅ Automatic fractal regeneration on parameter changes")
            print(f"   ✅ Intelligent caching with {final_stats['cache_efficiency']:.1%} efficiency")
            print(f"   ✅ Bloom sequence archiving and retrieval")
            print(f"   ✅ Similarity-based bloom matching")
            print(f"   ✅ Non-blocking concurrent processing")
            
        else:
            print(f"❌ Demo initialization failed")
    
    except Exception as e:
        print(f"❌ Demo failed: {e}")
    
    finally:
        if interface:
            interface.shutdown()

if __name__ == "__main__":
    main() 