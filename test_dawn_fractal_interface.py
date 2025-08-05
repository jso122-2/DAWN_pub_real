#!/usr/bin/env python3
"""
DAWN Fractal Interface Test
==========================

Test script for the DAWNFractalInterface class, focusing on core functionality:
- Memory bloom generation
- Caching system
- Archive and retrieval
- Similarity matching
"""

import time
import json
from pathlib import Path

# Import the interface
from dawn_fractal_interface import DAWNFractalInterface, DAWNConsciousnessConfig
from dawn_state_parser import DAWNStateParser

def test_memory_bloom_generation():
    """Test basic memory bloom generation"""
    
    print("\n🎨 Testing Memory Bloom Generation")
    print("=" * 35)
    
    interface = DAWNFractalInterface(
        output_dir="test_fractal_output",
        cache_size=50,
        max_concurrent_jobs=2
    )
    
    try:
        # Create test consciousness states
        test_states = [
            DAWNConsciousnessConfig(
                memory_id="test_calm_state", timestamp=None,
                bloom_entropy=0.2, mood_valence=0.5, drift_vector=0.1,
                rebloom_depth=4, sigil_saturation=0.6, pulse_zone="calm"
            ),
            DAWNConsciousnessConfig(
                memory_id="test_chaotic_state", timestamp=None,
                bloom_entropy=0.8, mood_valence=-0.3, drift_vector=-0.7,
                rebloom_depth=8, sigil_saturation=0.9, pulse_zone="surge"
            ),
            DAWNConsciousnessConfig(
                memory_id="test_flowing_state", timestamp=None,
                bloom_entropy=0.4, mood_valence=0.2, drift_vector=0.5,
                rebloom_depth=6, sigil_saturation=0.7, pulse_zone="flowing"
            )
        ]
        
        generated_blooms = []
        
        # Generate blooms synchronously
        for i, state in enumerate(test_states):
            print(f"\n🎯 Generating bloom {i+1}/3: {state.memory_id}")
            
            start_time = time.time()
            
            # Use the internal generation method directly for testing
            cache_key = interface._create_cache_key(state)
            
            try:
                bloom = interface._generate_bloom_job(state, cache_key)
                generation_time = time.time() - start_time
                
                print(f"   ✅ Generated: {bloom.cache_key}")
                print(f"   ⏱️  Time: {generation_time:.2f}s")
                print(f"   📊 Complexity: {bloom.visual_signature.get('complexity', 0):.3f}")
                print(f"   🎨 Color variance: {bloom.visual_signature.get('color_variance', 0):.3f}")
                print(f"   📁 File: {Path(bloom.file_path).name}")
                
                generated_blooms.append(bloom)
                
            except Exception as e:
                print(f"   ❌ Generation failed: {e}")
        
        return interface, generated_blooms
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        interface.shutdown()
        return None, []

def test_caching_system(interface, test_states):
    """Test caching system efficiency"""
    
    print("\n💾 Testing Caching System")
    print("=" * 27)
    
    # Clear cache statistics
    interface.stats['cache_hits'] = 0
    interface.stats['cache_misses'] = 0
    
    # Test cache hits by regenerating same states
    for i, state in enumerate(test_states):
        cache_key = interface._create_cache_key(state)
        
        print(f"\n🔍 Testing cache for state {i+1}: {state.memory_id}")
        
        # First call - should be cache miss (if not already cached)
        cached_bloom = interface._get_from_cache(cache_key)
        if cached_bloom:
            print(f"   💾 Cache HIT: {cache_key}")
        else:
            print(f"   🔍 Cache MISS: {cache_key}")
        
        # Second call - should be cache hit
        cached_bloom = interface._get_from_cache(cache_key)
        if cached_bloom:
            print(f"   💾 Cache HIT (second call): {cache_key}")
            print(f"   📊 Access count: {cached_bloom.access_count}")
    
    # Display cache statistics
    stats = interface.get_cache_statistics()
    print(f"\n📊 Cache Statistics:")
    print(f"   Cache size: {stats['cache_size']}/{stats['cache_max_size']}")
    print(f"   Cache efficiency: {stats['cache_efficiency']:.1%}")
    print(f"   Total hits: {stats['cache_hits']}")
    print(f"   Total misses: {stats['cache_misses']}")

def test_archive_and_retrieval(interface):
    """Test archive and retrieval functionality"""
    
    print("\n📦 Testing Archive and Retrieval")
    print("=" * 33)
    
    # Test time-based retrieval
    current_time = time.time()
    start_time = current_time - 3600  # Last hour
    end_time = current_time
    
    print(f"🔍 Retrieving blooms from last hour...")
    archived_blooms = interface.archive_bloom_sequence(start_time, end_time, "test_sequence")
    
    print(f"   📦 Archived sequence: {archived_blooms['sequence_name']}")
    print(f"   📊 Bloom count: {archived_blooms['bloom_count']}")
    
    if archived_blooms['blooms']:
        print(f"   📝 Recent blooms:")
        for bloom in archived_blooms['blooms'][:3]:  # Show first 3
            print(f"      • {bloom['memory_id']} (entropy: {bloom['bloom_entropy']:.2f})")

def test_similarity_matching(interface, test_states):
    """Test similarity matching functionality"""
    
    print("\n🔍 Testing Similarity Matching")
    print("=" * 31)
    
    if not test_states:
        print("   ⚠️  No test states available for similarity testing")
        return
    
    target_state = test_states[0]  # Use first state as target
    
    print(f"🎯 Finding blooms similar to: {target_state.memory_id}")
    print(f"   Parameters: entropy={target_state.bloom_entropy:.2f}, "
          f"valence={target_state.mood_valence:.2f}, depth={target_state.rebloom_depth}")
    
    # Test different similarity thresholds
    thresholds = [0.9, 0.7, 0.5]
    
    for threshold in thresholds:
        similar_blooms = interface.retrieve_similar_blooms(
            target_state, 
            similarity_threshold=threshold, 
            max_results=5
        )
        
        print(f"\n📊 Similarity threshold {threshold:.1f}:")
        print(f"   Found {len(similar_blooms)} similar blooms")
        
        for bloom in similar_blooms[:3]:  # Show top 3
            print(f"   • {bloom['memory_id']} (similarity: {bloom.get('similarity_score', 0):.3f})")

def test_state_monitoring(interface):
    """Test state monitoring functionality"""
    
    print("\n🔍 Testing State Monitoring")
    print("=" * 28)
    
    # Check if state monitoring is active
    if interface.state_monitor.monitoring:
        print("   ✅ State monitoring is active")
        print(f"   📂 Monitor interval: {interface.state_monitor.monitor_interval}s")
        print(f"   🎯 Change threshold: {interface.state_monitor.change_threshold}")
    else:
        print("   ⚠️  State monitoring is not active")
    
    # Test manual state updates
    print("\n📝 Testing manual state updates...")
    
    test_state1 = DAWNConsciousnessConfig(
        memory_id="manual_test_1", timestamp=None,
        bloom_entropy=0.3, mood_valence=0.0, drift_vector=0.0,
        rebloom_depth=5, sigil_saturation=0.5, pulse_zone="stable"
    )
    
    test_state2 = DAWNConsciousnessConfig(
        memory_id="manual_test_2", timestamp=None,
        bloom_entropy=0.8, mood_valence=0.6, drift_vector=0.4,
        rebloom_depth=7, sigil_saturation=0.8, pulse_zone="flowing"
    )
    
    # Update states manually
    interface.state_monitor.update_state(test_state1)
    print(f"   📊 State 1 updated: {test_state1.memory_id}")
    
    time.sleep(0.1)  # Small delay
    
    interface.state_monitor.update_state(test_state2)
    print(f"   📊 State 2 updated: {test_state2.memory_id}")
    
    # Check if change was detected
    if hasattr(interface.state_monitor, 'state_history') and interface.state_monitor.state_history:
        print(f"   📚 State history length: {len(interface.state_monitor.state_history)}")

def main():
    """Run comprehensive DAWN Fractal Interface tests"""
    
    print("🧪 DAWN Fractal Interface Comprehensive Tests")
    print("=" * 46)
    
    interface = None
    generated_blooms = []
    test_states = []
    
    try:
        # Test 1: Memory bloom generation
        interface, generated_blooms = test_memory_bloom_generation()
        
        if interface and generated_blooms:
            # Extract test states from generated blooms
            test_states = [bloom.config for bloom in generated_blooms]
            
            # Test 2: Caching system
            test_caching_system(interface, test_states)
            
            # Test 3: Archive and retrieval
            test_archive_and_retrieval(interface)
            
            # Test 4: Similarity matching
            test_similarity_matching(interface, test_states)
            
            # Test 5: State monitoring
            test_state_monitoring(interface)
            
            # Final statistics
            print("\n📈 Final Interface Statistics")
            print("=" * 31)
            final_stats = interface.get_cache_statistics()
            
            for key, value in final_stats.items():
                if isinstance(value, float):
                    print(f"   {key}: {value:.3f}")
                else:
                    print(f"   {key}: {value}")
        
        print(f"\n✅ All tests completed successfully!")
        print(f"📁 Output directory: {interface.output_dir if interface else 'N/A'}")
        print(f"📊 Blooms generated: {len(generated_blooms)}")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
    
    finally:
        if interface:
            interface.shutdown()

if __name__ == "__main__":
    main() 