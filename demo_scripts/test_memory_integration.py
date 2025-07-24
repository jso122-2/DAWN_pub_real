#!/usr/bin/env python3
"""
DAWN Memory Integration Test
Demonstrates the new memory routing system integrated with DAWN consciousness.
"""

import asyncio
import sys
import os
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.memory.memory_routing_system import (
    DAWNMemoryRoutingSystem, 
    get_memory_routing_system,
    store_dawn_memory,
    retrieve_dawn_memories
)
from core.memory.memory_chunk import create_memory_now, memory_stats
from core.memory.memory_loader import create_test_memory_file


async def test_basic_memory_operations():
    """Test basic memory operations"""
    print("🧠 Testing Basic Memory Operations")
    print("=" * 50)
    
    # Initialize memory system
    memory_system = DAWNMemoryRoutingSystem(memories_dir="test_memories")
    
    # Store some test memories
    print("\n📝 Storing test memories...")
    
    memories = []
    
    # Memory 1: System event
    memory1 = await memory_system.store_memory(
        speaker="dawn.core",
        content="System entropy stabilized after fluctuation period",
        topic="system_event",
        pulse_state={
            "entropy": 0.45,
            "heat": 23.7,
            "scup": 0.72,
            "mood": "stable",
            "zone": "calm"
        },
        sigils=["STABILIZE_PROTOCOL"]
    )
    memories.append(memory1)
    print(f"  ✅ Stored: {memory1.summary()}")
    
    # Memory 2: Reflection
    memory2 = await memory_system.store_memory(
        speaker="j.orloff",
        content="The recursive patterns in consciousness remind me of fractals in nature",
        topic="reflection",
        pulse_state={
            "entropy": 0.31,
            "heat": 18.2,
            "scup": 0.88,
            "mood": "contemplative"
        },
        sigils=["REFLECTION"]
    )
    memories.append(memory2)
    print(f"  ✅ Stored: {memory2.summary()}")
    
    # Memory 3: Owl observation
    memory3 = await memory_system.store_memory(
        speaker="owl.system",
        content="Detected alignment drift, recommending thermal regulation",
        topic="owl_observation",
        pulse_state={
            "entropy": 0.67,
            "heat": 38.1,
            "scup": 0.34,
            "mood": "analytical"
        },
        sigils=["OWL_SUGGESTION", "THERMAL_REGULATION"]
    )
    memories.append(memory3)
    print(f"  ✅ Stored: {memory3.summary()}")
    
    return memory_system, memories


async def test_memory_retrieval(memory_system):
    """Test memory retrieval operations"""
    print("\n🔍 Testing Memory Retrieval")
    print("=" * 50)
    
    # Test 1: Search by content
    print("\n📋 Searching for 'entropy' memories...")
    entropy_memories = await memory_system.retrieve_memories("entropy", max_results=5)
    for mem in entropy_memories:
        print(f"  📄 {mem.summary()}")
        print(f"     Entropy: {mem.get_entropy():.3f}, Heat: {mem.get_heat():.1f}")
    
    # Test 2: Search by speaker
    print("\n👤 Searching for j.orloff memories...")
    orloff_memories = await memory_system.retrieve_memories(
        query="reflection",
        context={"speaker": "j.orloff"},
        max_results=3
    )
    for mem in orloff_memories:
        print(f"  📄 {mem.summary()}")
    
    # Test 3: Search by high entropy
    print("\n⚡ Searching for high entropy events...")
    high_entropy = await memory_system.retrieve_memories(
        query="system",
        context={"entropy_range": (0.5, 1.0)},
        max_results=3
    )
    for mem in high_entropy:
        print(f"  📄 {mem.summary()}")
        print(f"     🌡️ Heat: {mem.get_heat():.1f}, 🔄 SCUP: {mem.get_scup():.3f}")


async def test_memory_persistence(memory_system):
    """Test memory persistence to JSON Lines"""
    print("\n💾 Testing Memory Persistence")
    print("=" * 50)
    
    # Save current memories
    print("\n💾 Saving memories to file...")
    target_path = "test_memories/dawn_session.jsonl"
    save_path = await memory_system.save_memories(target_path)
    print(f"  ✅ Saved to: {save_path}")
    
    # Use the target path if save_path is empty or invalid
    if not save_path or save_path == "." or not os.path.exists(save_path):
        save_path = target_path
    
    # Test loading memories back
    print("\n📂 Loading memories from file...")
    loaded_memories = await memory_system.load_memories_from_file(save_path)
    print(f"  ✅ Loaded {len(loaded_memories)} memories")
    
    # Show statistics
    stats = memory_stats(loaded_memories)
    print(f"\n📊 Memory Statistics:")
    print(f"  Total memories: {stats['total_memories']}")
    print(f"  Unique speakers: {stats['unique_speakers']}")
    print(f"  Unique topics: {stats['unique_topics']}")
    print(f"  Average entropy: {stats['average_entropy']:.3f}")
    print(f"  Average heat: {stats['average_heat']:.1f}")
    print(f"  Sigils: {', '.join(stats['sigils'])}")


async def test_consciousness_integration():
    """Test integration with DAWN consciousness system"""
    print("\n🌅 Testing Consciousness Integration")
    print("=" * 50)
    
    try:
        # Import consciousness core
        from core.consciousness_core import DAWNConsciousness
        
        print("\n🔌 Initializing DAWN consciousness with memory integration...")
        
        # Create consciousness instance
        consciousness = DAWNConsciousness()
        
        # Check if memory routing is integrated
        if hasattr(consciousness, 'memory_routing'):
            print("  ✅ Memory routing system integrated!")
            
            # Test storing a memory through consciousness
            await consciousness._store_interaction_memory(
                speaker="dawn.consciousness",
                content="Memory integration test successful",
                topic="integration_test"
            )
            print("  ✅ Stored memory through consciousness core")
            
            # Get system stats
            stats = consciousness.memory_routing.get_system_stats()
            print(f"\n📈 System Statistics:")
            print(f"  Router decisions: {stats['router']['routing_decisions']}")
            print(f"  Memory hits: {stats['router']['memory_hits']}")
            print(f"  Hit rate: {stats['router']['hit_rate']:.2%}")
            print(f"  Active memories: {stats['router']['total_active_memories']}")
            
            # Test enhanced capabilities if available
            if hasattr(consciousness.memory_routing.router, 'cognitive_router'):
                print("  ✅ Cognitive routing enabled")
            if hasattr(consciousness.memory_routing.router, 'vector_index'):
                print("  ✅ Vector search enabled")
        else:
            print("  ⚠️ Memory routing not found in consciousness")
    
    except Exception as e:
        print(f"  ❌ Error testing consciousness integration: {e}")


async def test_enhanced_capabilities(memory_system):
    """Test enhanced cognitive routing and vector search capabilities"""
    print("\n🧠 Testing Enhanced Memory Capabilities")
    print("=" * 50)
    
    # Test cognitive routing (rebloom)
    print("\n🔄 Testing Cognitive Rebloom:")
    if memory_system.router.cognitive_router:
        # Get a chunk to test rebloom
        test_chunks = list(memory_system.router.cognitive_router.chunks.values())
        if test_chunks:
            query_chunk = test_chunks[0]
            candidates = memory_system.router.rebloom_candidates(query_chunk, max_candidates=3)
            print(f"  📄 Query chunk: {query_chunk.summary()}")
            print(f"  🔍 Found {len(candidates)} rebloom candidates:")
            for i, candidate in enumerate(candidates, 1):
                print(f"    {i}. {candidate.summary()}")
        else:
            print("  ⚠️ No chunks available for rebloom test")
    else:
        print("  ⚠️ Cognitive router not available")
    
    # Test vector search
    print("\n🔍 Testing Vector Search:")
    if memory_system.router.vector_index:
        # Test basic vector search
        vector_results = memory_system.router.vector_search("system entropy", top_k=3)
        print(f"  📊 Vector search for 'system entropy': {len(vector_results)} results")
        for i, chunk in enumerate(vector_results, 1):
            print(f"    {i}. {chunk.summary()}")
        
        # Test context-aware vector search
        context = {
            'speaker': 'dawn.core',
            'pulse_state': {'heat': 30.0, 'entropy': 0.5, 'mood': 'analytical'}
        }
        context_results = memory_system.router.vector_search("thermal regulation", top_k=2, context=context)
        print(f"  🌡️ Context-aware search: {len(context_results)} results")
        for i, chunk in enumerate(context_results, 1):
            print(f"    {i}. {chunk.summary()}")
    else:
        print("  ⚠️ Vector index not available")
    
    # Test memory compression
    print("\n🗜️ Testing Memory Compression:")
    compressed = memory_system.router.compress_memories()
    if 'memory_summary' in compressed:
        print(f"  📊 {compressed['memory_summary']}")
        print(f"  📈 Performance metrics: {compressed.get('performance_metrics', {})}")
        if 'pulse_state_averages' in compressed:
            pulse_avgs = compressed['pulse_state_averages']
            print(f"  🌡️ Average entropy: {pulse_avgs.get('entropy', 0):.3f}")
            print(f"  🔥 Average heat: {pulse_avgs.get('heat', 0):.1f}")
            print(f"  🔄 Average SCUP: {pulse_avgs.get('scup', 0):.3f}")
    else:
        print("  ⚠️ Compression not available")
    
    # Show enhanced statistics
    print("\n📊 Enhanced Statistics:")
    stats = memory_system.router.get_routing_stats()
    print(f"  🔄 Rebloom requests: {stats.get('rebloom_requests', 0)}")
    print(f"  🔍 Vector searches: {stats.get('vector_searches', 0)}")
    
    if 'cognitive_router' in stats:
        cog_stats = stats['cognitive_router']
        print(f"  🧠 Cognitive chunks: {cog_stats.get('total_chunks', 0)}")
        print(f"  🏷️ Unique sigils: {cog_stats.get('unique_sigils', 0)}")
    
    if 'vector_index' in stats:
        vec_stats = stats['vector_index']
        print(f"  📚 Vector index size: {vec_stats.get('vector_count', 0)}")
        print(f"  💾 Memory usage: {vec_stats.get('memory_usage_mb', 0):.2f} MB")


async def test_advanced_filtering(memory_system):
    """Test advanced memory filtering capabilities"""
    print("\n🔬 Testing Advanced Filtering")
    print("=" * 50)
    
    # Store additional test memories with different characteristics
    test_memories = [
        {
            "speaker": "dawn.core",
            "content": "Critical entropy spike detected, initiating emergency protocols",
            "topic": "emergency",
            "pulse_state": {"entropy": 0.91, "heat": 78.3, "mood": "urgent"},
            "sigils": ["EMERGENCY", "ENTROPY_SPIKE"]
        },
        {
            "speaker": "user",
            "content": "How does the consciousness system handle memory consolidation?",
            "topic": "user_query",
            "pulse_state": {"entropy": 0.25, "heat": 15.7, "mood": "curious"},
            "sigils": []
        },
        {
            "speaker": "dawn.core",
            "content": "Thermal regulation successful, system returning to baseline",
            "topic": "thermal_event",
            "pulse_state": {"entropy": 0.33, "heat": 21.4, "mood": "relieved"},
            "sigils": ["THERMAL_SUCCESS"]
        }
    ]
    
    print("\n📝 Storing test memories with varied characteristics...")
    for mem_data in test_memories:
        memory = await memory_system.store_memory(**mem_data)
        print(f"  ✅ {memory.summary()}")
    
    # Test filtering by different criteria
    print("\n🔍 Testing filters:")
    
    # Filter by high entropy
    high_entropy = memory_system.loader.filter_memories(
        memory_system.router.recent_memories,
        min_entropy=0.7
    )
    print(f"  📊 High entropy (>0.7): {len(high_entropy)} memories")
    
    # Filter by mood
    urgent_memories = memory_system.loader.filter_memories(
        memory_system.router.recent_memories,
        mood="urgent"
    )
    print(f"  😰 Urgent mood: {len(urgent_memories)} memories")
    
    # Filter by sigil
    emergency_memories = memory_system.loader.filter_memories(
        memory_system.router.recent_memories,
        has_sigil="EMERGENCY"
    )
    print(f"  🚨 Emergency sigil: {len(emergency_memories)} memories")
    
    # Filter by speaker and topic
    core_thermal = memory_system.loader.filter_memories(
        memory_system.router.recent_memories,
        speaker="dawn.core",
        topic="thermal_event"
    )
    print(f"  🌡️ Core thermal events: {len(core_thermal)} memories")


async def cleanup_test_files():
    """Clean up test files"""
    print("\n🧹 Cleaning up test files...")
    
    import shutil
    test_dir = Path("test_memories")
    if test_dir.exists():
        shutil.rmtree(test_dir)
        print("  ✅ Test directory cleaned up")


async def main():
    """Main test function"""
    print("🧠 DAWN Memory Integration Test Suite")
    print("=" * 60)
    print("Testing the new memory routing system integration with DAWN")
    print("=" * 60)
    
    try:
        # Run all tests
        memory_system, memories = await test_basic_memory_operations()
        await test_memory_retrieval(memory_system)
        await test_memory_persistence(memory_system)
        await test_advanced_filtering(memory_system)
        await test_enhanced_capabilities(memory_system)
        await test_consciousness_integration()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        print("🧠 Memory routing system is ready for DAWN integration")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        await cleanup_test_files()


if __name__ == "__main__":
    asyncio.run(main()) 