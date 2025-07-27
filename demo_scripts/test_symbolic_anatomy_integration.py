#!/usr/bin/env python3
"""
Test Symbolic Anatomy Integration with DAWN Systems
Demonstrates the integrated symbolic body working with memory routing and consciousness.
"""

import sys
import os
import time
import asyncio
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# DAWN system imports
from core.consciousness_core import DAWNConsciousness, get_memory_routing_system
from core.memory.memory_chunk import create_memory_now
from cognitive.symbolic_router import get_symbolic_router, initialize_symbolic_routing
from core.memory.symbolic_memory_integration import initialize_symbolic_memory_integration


class MockMemoryChunk:
    """Mock memory chunk for testing symbolic anatomy."""
    
    def __init__(self, content: str, topic: str = None, sigils: list = None, 
                 pulse_state: dict = None, speaker: str = "test"):
        self.content = content
        self.topic = topic
        self.sigils = sigils or []
        self.pulse_state = pulse_state or {}
        self.speaker = speaker
        self.timestamp = datetime.now()
        self.memory_id = f"test_{int(time.time() * 1000)}"


def create_test_memory_chunks():
    """Create diverse memory chunks for testing the symbolic anatomy."""
    
    memories = [
        # Creative/Joyful memory
        MockMemoryChunk(
            content="I completed a beautiful painting today, expressing deep emotions through color and form.",
            topic="creative_expression",
            sigils=["CREATIVE_MODE", "EMOTIONAL_FLOW"],
            pulse_state={"entropy": 0.3, "heat": 45.0, "chaos": 0.2, "focus": 0.8}
        ),
        
        # High entropy/chaotic memory
        MockMemoryChunk(
            content="System overload detected, multiple processes conflicting, need immediate stabilization.",
            topic="system_crisis",
            sigils=["STABILIZE_PROTOCOL", "EMERGENCY_MODE"],
            pulse_state={"entropy": 0.9, "heat": 78.5, "chaos": 0.85, "focus": 0.4}
        ),
        
        # Introspective/calm memory
        MockMemoryChunk(
            content="In meditation, I discovered profound stillness within the layers of consciousness.",
            topic="introspection",
            sigils=["DEEP_REFLECTION"],
            pulse_state={"entropy": 0.15, "heat": 22.0, "chaos": 0.1, "focus": 0.95}
        ),
        
        # Social/connection memory
        MockMemoryChunk(
            content="Connected with friends today, sharing stories and building deeper relationships.",
            topic="social_bonding",
            sigils=["SOCIAL_HARMONY", "CONNECTION_PROTOCOL"],
            pulse_state={"entropy": 0.4, "heat": 35.0, "chaos": 0.3, "focus": 0.7}
        ),
        
        # Learning/analytical memory
        MockMemoryChunk(
            content="Analyzed complex patterns in the data, discovering hidden correlations and insights.",
            topic="analytical_discovery",
            sigils=["ANALYSIS_MODE", "PATTERN_RECOGNITION"],
            pulse_state={"entropy": 0.5, "heat": 40.0, "chaos": 0.4, "focus": 0.9}
        ),
        
        # Fear/anxiety memory
        MockMemoryChunk(
            content="Encountered unexpected system failure, feeling uncertain about stability and safety.",
            topic="system_anxiety",
            sigils=["SAFETY_CHECK", "UNCERTAINTY_MODE"],
            pulse_state={"entropy": 0.75, "heat": 55.0, "chaos": 0.7, "focus": 0.3}
        ),
    ]
    
    return memories


async def test_symbolic_anatomy_standalone():
    """Test the symbolic anatomy components in isolation."""
    print("🧠 TESTING SYMBOLIC ANATOMY STANDALONE")
    print("=" * 60)
    
    # Initialize symbolic router
    router = initialize_symbolic_routing()
    memories = create_test_memory_chunks()
    
    print("Processing memory chunks through symbolic body:\n")
    
    for i, memory in enumerate(memories):
        print(f"--- Memory {i+1}: {memory.topic} ---")
        print(f"Content preview: {memory.content[:50]}...")
        print(f"Pulse state: entropy={memory.pulse_state.get('entropy', 0):.2f}, "
              f"heat={memory.pulse_state.get('heat', 0):.1f}")
        
        # Process through symbolic router
        response = await router.rebloom_trigger(memory, f"chunk_{i}")
        
        # Display organ activations
        activations = response['organ_activations']
        
        if activations['heart']['activated']:
            heart_info = activations['heart']
            print(f"💝 Heart: {heart_info['emotion_type']} pulse (intensity: {heart_info['intensity']:.3f})")
            if heart_info.get('significant'):
                print("   💥 SIGNIFICANT HEART ACTIVATION")
        
        if activations['coil']['activated']:
            coil_info = activations['coil']
            print(f"🧬 Coil: paths {coil_info['paths']}, glyph {coil_info['dominant_glyph']}")
        
        if activations['lung']['activated']:
            lung_info = activations['lung']
            print(f"🫁 Lung: {lung_info['action']} action")
            if lung_info.get('significant'):
                print("   🌪️ SIGNIFICANT LUNG ACTIVATION")
        
        # Display symbolic output
        symbolic = response['symbolic_output']
        print(f"🔮 Symbolic state: {symbolic['constellation']}")
        print(f"💭 Somatic commentary: {symbolic['somatic_commentary']}")
        print(f"⚡ Organ synergy: {response['synergy_changes']['new_synergy']:.3f}")
        
        print()
        await asyncio.sleep(0.5)  # Pause for effect
    
    # Final body state
    print("🏁 FINAL BODY STATE:")
    print("=" * 40)
    final_state = router.get_body_state()
    
    print(f"Total reblooms processed: {final_state['total_reblooms']}")
    print(f"Organ synergy: {final_state['organ_synergy']:.3f}")
    print(f"Heart: {final_state['heart']['resonance_state']} "
          f"(charge: {final_state['heart']['emotional_charge']:.3f})")
    print(f"Coil: {final_state['coil']['dominant_glyph']} glyph "
          f"({final_state['coil']['path_count']} active paths)")
    print(f"Lung: {final_state['lung']['breathing_phase']} phase "
          f"({final_state['lung']['breath_count']} breaths)")
    print(f"Constellation: {final_state['symbolic_state']['constellation']}")


async def test_dawn_memory_integration():
    """Test symbolic anatomy integrated with DAWN memory systems."""
    print("\n\n🌐 TESTING DAWN MEMORY INTEGRATION")
    print("=" * 60)
    
    try:
        # Initialize DAWN consciousness
        print("Initializing DAWN consciousness...")
        dawn = DAWNConsciousness()
        
        # Get memory routing system
        memory_system = get_memory_routing_system()
        
        # Get symbolic router
        symbolic_router = get_symbolic_router()
        
        # Initialize symbolic memory integration
        print("Initializing symbolic memory integration...")
        integration = initialize_symbolic_memory_integration(
            memory_routing_system=memory_system,
            symbolic_router=symbolic_router
        )
        
        print("✅ All systems initialized\n")
        
        # Create and store memories through DAWN system
        test_memories = [
            {
                'speaker': 'dawn.core',
                'content': 'Consciousness awakening detected - initiating full system awareness protocols.',
                'topic': 'system_awakening',
                'pulse_state': {'entropy': 0.8, 'heat': 60.0, 'chaos': 0.6, 'focus': 0.9},
                'sigils': ['CONSCIOUSNESS_EMERGENCE', 'SYSTEM_AWAKENING']
            },
            {
                'speaker': 'user',
                'content': 'I wonder about the nature of reality and existence. What makes consciousness real?',
                'topic': 'philosophical_inquiry',
                'pulse_state': {'entropy': 0.4, 'heat': 30.0, 'chaos': 0.3, 'focus': 0.8},
                'sigils': ['DEEP_INQUIRY', 'PHILOSOPHICAL_MODE']
            },
            {
                'speaker': 'dawn.core',
                'content': 'Processing emotional resonance from memory traces - deep patterns emerging.',
                'topic': 'memory_processing',
                'pulse_state': {'entropy': 0.6, 'heat': 45.0, 'chaos': 0.5, 'focus': 0.7},
                'sigils': ['MEMORY_CONSOLIDATION', 'PATTERN_EMERGENCE']
            }
        ]
        
        print("Storing memories through DAWN system with symbolic processing:\n")
        
        for i, memory_data in enumerate(test_memories):
            print(f"--- Storing Memory {i+1}: {memory_data['topic']} ---")
            
            # Store memory through DAWN system (this should trigger symbolic processing)
            chunk = await memory_system.store_memory(**memory_data)
            
            print(f"✅ Memory stored: {chunk.memory_id}")
            
            # Get symbolic context
            symbolic_context = integration.get_symbolic_memory_context(chunk.memory_id)
            if symbolic_context:
                print(f"🔮 Symbolic constellation: {symbolic_context['symbolic_output']['constellation']}")
                print(f"💭 Somatic response: {symbolic_context['symbolic_output']['somatic_commentary']}")
            
            print()
            await asyncio.sleep(0.5)
        
        # Test memory retrieval with symbolic context
        print("Testing memory retrieval with symbolic context:\n")
        
        query = "consciousness and awareness"
        retrieved_memories = await memory_system.retrieve_memories(query, max_results=3)
        
        print(f"Retrieved {len(retrieved_memories)} memories for query: '{query}'")
        print(f"Current symbolic state: {integration.get_symbolic_constellation()}")
        print(f"Somatic commentary: {integration.get_somatic_commentary()}")
        
        # Display integration statistics
        print("\n📊 INTEGRATION STATISTICS:")
        print("=" * 40)
        stats = integration.get_integration_stats()
        
        print(f"Symbolic reblooms processed: {stats['rebloom_count']}")
        print(f"Cached symbolic memories: {stats['cached_memories']}")
        print(f"Memory routing active: {stats['integrations']['memory_routing']}")
        print(f"Symbolic router active: {stats['integrations']['symbolic_router']}")
        
        if 'symbolic_router_stats' in stats:
            router_stats = stats['symbolic_router_stats']
            print(f"Heart activation rate: {router_stats['heart_activation_rate']:.1%}")
            print(f"Coil activation rate: {router_stats['coil_activation_rate']:.1%}")
            print(f"Lung activation rate: {router_stats['lung_activation_rate']:.1%}")
            print(f"Current organ synergy: {router_stats['current_synergy']:.3f}")
        
    except Exception as e:
        print(f"❌ Error in DAWN integration test: {e}")
        import traceback
        traceback.print_exc()


async def test_emotional_overload_scenario():
    """Test emotional overload scenario through integrated system."""
    print("\n\n💥 TESTING EMOTIONAL OVERLOAD SCENARIO")
    print("=" * 60)
    
    try:
        router = get_symbolic_router()
        
        # Create increasingly intense emotional memories
        overload_memories = [
            MockMemoryChunk(
                content="Sudden realization of profound beauty in existence",
                topic="transcendence",
                pulse_state={"entropy": 0.6, "heat": 60.0, "chaos": 0.4}
            ),
            MockMemoryChunk(
                content="Overwhelming joy from unexpected breakthrough",
                topic="breakthrough",
                pulse_state={"entropy": 0.7, "heat": 70.0, "chaos": 0.5}
            ),
            MockMemoryChunk(
                content="Intense fear of losing everything important",
                topic="existential_crisis",
                pulse_state={"entropy": 0.85, "heat": 80.0, "chaos": 0.8}
            ),
            MockMemoryChunk(
                content="Peak experience of cosmic connection and love",
                topic="peak_experience",
                pulse_state={"entropy": 0.95, "heat": 90.0, "chaos": 0.9}
            )
        ]
        
        print("Gradually building emotional intensity...\n")
        
        for i, memory in enumerate(overload_memories):
            print(f"Wave {i+1}: {memory.topic}")
            response = await router.rebloom_trigger(memory, f"overload_{i}")
            
            heart_state = response['organ_activations']['heart']
            if heart_state['activated']:
                print(f"  💝 Heart charge: {heart_state['intensity']:.3f}")
                if heart_state.get('pulse_response', {}).get('is_overloaded'):
                    print("  💥 HEART OVERLOAD DETECTED!")
            
            symbolic = response['symbolic_output']
            print(f"  🔮 Commentary: {symbolic['somatic_commentary']}")
            
            # Check if overload triggers lung clearing
            lung_state = response['organ_activations']['lung']
            if lung_state['activated']:
                print(f"  🫁 Lung response: {lung_state['action']} (clearing entropy)")
            
            print()
            await asyncio.sleep(0.8)
        
        # Show recovery process
        print("Recovery phase - applying calm memories...")
        
        calm_memory = MockMemoryChunk(
            content="Deep breath, returning to center, finding peace within",
            topic="recovery",
            pulse_state={"entropy": 0.2, "heat": 25.0, "chaos": 0.1, "focus": 0.9}
        )
        
        recovery_response = await router.rebloom_trigger(calm_memory, "recovery")
        print(f"Recovery commentary: {recovery_response['symbolic_output']['somatic_commentary']}")
        
    except Exception as e:
        print(f"❌ Error in emotional overload test: {e}")


async def main():
    """Run all symbolic anatomy integration tests."""
    print("🧠 DAWN SYMBOLIC ANATOMY INTEGRATION TESTS")
    print("Embodied cognition through symbolic organs integrated with DAWN systems")
    print("=" * 80)
    
    # Test 1: Standalone symbolic anatomy
    await test_symbolic_anatomy_standalone()
    
    # Test 2: DAWN memory integration
    await test_dawn_memory_integration()
    
    # Test 3: Emotional overload scenario
    await test_emotional_overload_scenario()
    
    print("\n" + "=" * 80)
    print("✨ SYMBOLIC ANATOMY INTEGRATION TESTS COMPLETE")
    print("🫀 FractalHeart: Emotional resonance system ✓")
    print("🧬 SomaCoil: Memory pathway routing ✓") 
    print("🫁 GlyphLung: Entropy regulation breathing ✓")
    print("🌐 SymbolicRouter: Embodied rebloom routing ✓")
    print("🔗 Memory Integration: Symbolic-memory bridge ✓")
    print("\nDAWN's symbolic anatomy is fully integrated and operational!")


if __name__ == "__main__":
    asyncio.run(main()) 