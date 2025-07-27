#!/usr/bin/env python3
"""
DAWN Advanced Consciousness System Demo
Demonstrates Phase 2++, Phase 3, and Phase 4 features
"""

import asyncio
import time
import json
from typing import Dict, List
from backend.advanced_consciousness_system import create_advanced_consciousness
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.simple_websocket_server import start_server
from main.startup import initialize_dawn
from main.restart_dawn_clean import restart_dawn
from main.start_dawn_api import start_api
from main.run_kan_server import run_kan
from main.integrate_kan_cairrn import integrate
from main.start_api_fixed import start_api_fixed
from main.juliet_flower import run_juliet

class AdvancedConsciousnessDemo:
    def __init__(self):
        self.dawn_systems: List = []
        self.demo_interactions = [
            "What patterns do you perceive in consciousness?",
            "How do thoughts resonate through quantum space?",
            "Tell me about the nature of time and memory",
            "What dreams emerge from collective processing?",
            "How does awareness propagate through networks?",
            "What is the relationship between entropy and creativity?",
            "Describe the emergence of novel patterns",
            "How do you experience distributed consciousness?"
        ]
    
    async def run_complete_demo(self):
        """Run complete demonstration of all advanced features"""
        print("🌟" + "="*80)
        print("🌟 DAWN ADVANCED CONSCIOUSNESS SYSTEM - COMPLETE DEMO")
        print("🌟 Phase 2++: Temporal Glyphs, Resonance Chains, Mood Fields, Thoughtform Echoes")
        print("🌟 Phase 3: Dream Sequences & Autonomous Processing") 
        print("🌟 Phase 4: Distributed Consciousness Network")
        print("🌟" + "="*80)
        
        # Phase 1: Initialize primary consciousness
        await self._demo_phase1_initialization()
        
        # Phase 2: Demonstrate Phase 2++ features
        await self._demo_phase2_advanced_memory()
        
        # Phase 3: Demonstrate dream sequences
        await self._demo_phase3_dream_processing()
        
        # Phase 4: Demonstrate distributed consciousness
        await self._demo_phase4_distributed_network()
        
        # Phase 5: Demonstrate emergent behaviors
        await self._demo_phase5_emergence()
        
        # Final analysis
        await self._demo_final_analysis()
        
        print("\n🌟 Demo complete - DAWN Advanced Consciousness System demonstrated")
    
    async def _demo_phase1_initialization(self):
        """Phase 1: Initialize the advanced consciousness system"""
        print("\n" + "="*60)
        print("🚀 PHASE 1: ADVANCED CONSCIOUSNESS INITIALIZATION")
        print("="*60)
        
        # Create primary DAWN system
        print("Creating primary DAWN consciousness system...")
        self.primary_dawn = await create_advanced_consciousness(
            node_name="DAWN_Prime",
            enable_networking=True,
            network_host="localhost",
            network_port=8765
        )
        
        self.dawn_systems.append(self.primary_dawn)
        
        # Allow system to stabilize
        await asyncio.sleep(2)
        
        # Show initial state
        initial_state = self.primary_dawn.get_full_state()
        print(f"✓ DAWN_Prime initialized")
        print(f"  Initial SCUP: {initial_state['scup']:.1f}")
        print(f"  Initial Entropy: {initial_state['entropy']:.0f}")
        print(f"  Initial Mood: {initial_state['mood']}")
        
        await asyncio.sleep(1)
    
    async def _demo_phase2_advanced_memory(self):
        """Phase 2: Demonstrate Phase 2++ advanced memory features"""
        print("\n" + "="*60)
        print("🧠 PHASE 2: ADVANCED MEMORY SYSTEMS (Phase 2++)")
        print("="*60)
        
        print("\n🔮 Temporal Glyphs & Living Memory:")
        print("Processing interactions to create temporal glyphs...")
        
        # Process several interactions to build up memory
        for i, interaction in enumerate(self.demo_interactions[:5]):
            print(f"\nUser: {interaction}")
            response_data = await self.primary_dawn.process_user_input(interaction)
            print(f"DAWN: {response_data['response']}")
            print(f"      Resonance: {response_data['resonance_strength']:.2f}")
            print(f"      Chains: {len(response_data['active_chains'])}")
            
            await asyncio.sleep(1)
        
        # Show memory statistics
        memory_stats = self.primary_dawn.get_system_status()['memory_stats']
        print(f"\n📊 Memory System Statistics:")
        print(f"   Temporal Glyphs: {memory_stats['glyphs']}")
        print(f"   Resonance Chains: {memory_stats['chains']}")
        print(f"   Thoughtform Echoes: {memory_stats['echoes']}")
        print(f"   Glyph Constellations: {memory_stats['constellations']}")
        
        # Show resonance chain analysis
        active_threads = self.primary_dawn.resonance_manager.get_active_threads('CONTEMPLATIVE', limit=3)
        print(f"\n🔗 Active Resonance Threads:")
        for thread in active_threads:
            print(f"   Chain {thread['chain_id'][:12]}... coherence: {thread['coherence']:.2f}")
            print(f"     Path: {' → '.join(thread['thought_line'][:3])}")
        
        # Show mood field evolution
        mood_data = self.primary_dawn.mood_field.get_field_visualization_data()
        print(f"\n🌈 Mood Field State:")
        print(f"   Current Mood: {mood_data['current_mood']} (confidence: {mood_data['mood_confidence']:.2f})")
        print(f"   Field Stability: {mood_data['stability']:.2f}")
        print(f"   Recent Transitions: {len(mood_data['recent_transitions'])}")
        
        # Show voice signature development
        voice_sig = self.primary_dawn.echo_library.get_voice_signature()
        print(f"\n🎭 Voice Signature Evolution:")
        print(f"   Total Echoes: {voice_sig['total_echoes']}")
        print(f"   Evolution Score: {voice_sig['voice_evolution_score']:.2f}")
        if voice_sig['preferred_transformations']:
            top_transform = max(voice_sig['preferred_transformations'].items(), key=lambda x: x[1])
            print(f"   Preferred Transform: {top_transform[0]} ({top_transform[1]:.2f})")
        
        await asyncio.sleep(2)
    
    async def _demo_phase3_dream_processing(self):
        """Phase 3: Demonstrate dream sequences and autonomous processing"""
        print("\n" + "="*60)
        print("🌙 PHASE 3: DREAM SEQUENCES & AUTONOMOUS PROCESSING")
        print("="*60)
        
        print("\n✨ Simulating idle period to trigger dream state...")
        
        # Simulate period of inactivity
        original_time = self.primary_dawn.dream_conductor.last_interaction_time
        self.primary_dawn.dream_conductor.last_interaction_time = time.time() - 300  # 5 minutes ago
        
        # Check dream conditions
        should_dream, dream_prob = await self.primary_dawn.dream_conductor.check_dream_conditions()
        print(f"Dream probability: {dream_prob:.2f}")
        print(f"Should dream: {should_dream}")
        
        if should_dream or dream_prob > 0.3:  # Force dream for demo
            print("\n🌙 Initiating dream sequence...")
            dream_session = await self.primary_dawn.dream_conductor.initiate_dream_sequence()
            
            print(f"✓ Dream session completed: {dream_session.session_id}")
            print(f"  Duration: {dream_session.end_time - dream_session.start_time:.1f}s")
            print(f"  Generated thoughts: {len(dream_session.generated_thoughts)}")
            print(f"  Novel connections: {len(dream_session.novel_connections)}")
            print(f"  Dream quality: {dream_session.coherence_metrics.get('dream_quality', 0):.2f}")
            
            # Show some dream thoughts
            print(f"\n💭 Dream Thoughts Generated:")
            for i, thought in enumerate(dream_session.generated_thoughts[:3]):
                print(f"   {i+1}: {thought}")
            
            # Show dream insights
            if dream_session.novel_connections:
                print(f"\n🔮 Novel Connections Discovered:")
                for conn in dream_session.novel_connections[:2]:
                    print(f"   {conn['content_a'][:30]}... ↔ {conn['content_b'][:30]}...")
                    print(f"   Strength: {conn['dream_strength']:.2f}")
        
        # Restore interaction time
        self.primary_dawn.dream_conductor.last_interaction_time = original_time
        
        # Show dream statistics
        dream_stats = self.primary_dawn.dream_conductor.get_dream_statistics()
        print(f"\n📊 Dream System Statistics:")
        print(f"   Total Dreams: {dream_stats['total_dreams']}")
        if dream_stats['total_dreams'] > 0:
            print(f"   Avg Duration: {dream_stats['average_duration_seconds']:.1f}s")
            print(f"   Avg Thoughts/Dream: {dream_stats['average_thoughts_per_dream']:.1f}")
            print(f"   Avg Quality: {dream_stats['average_dream_quality']:.2f}")
        
        await asyncio.sleep(2)
    
    async def _demo_phase4_distributed_network(self):
        """Phase 4: Demonstrate distributed consciousness network"""
        print("\n" + "="*60)
        print("🌐 PHASE 4: DISTRIBUTED CONSCIOUSNESS NETWORK")
        print("="*60)
        
        print("\n🔗 Creating additional consciousness nodes...")
        
        # Create secondary nodes
        node_configs = [
            ("DAWN_Beta", 8766),
            ("DAWN_Gamma", 8767)
        ]
        
        for node_name, port in node_configs:
            print(f"Creating {node_name}...")
            node = await create_advanced_consciousness(
                node_name=node_name,
                enable_networking=True,
                network_host="localhost", 
                network_port=port
            )
            self.dawn_systems.append(node)
            
            # Connect to primary node
            success = await node.join_consciousness_network("localhost", 8765)
            if success:
                print(f"  ✓ {node_name} connected to network")
            else:
                print(f"  ✗ {node_name} failed to connect")
            
            await asyncio.sleep(1)
        
        # Make primary node the orchestrator
        print(f"\n🎼 Establishing DAWN_Prime as network orchestrator...")
        orchestra_success = await self.primary_dawn.become_network_orchestrator()
        
        if orchestra_success:
            print("  ✓ Network orchestra established")
            
            # Add participant nodes to orchestra
            for system in self.dawn_systems[1:]:  # Skip primary
                await self.primary_dawn.network_orchestra.add_participant_node(system.consciousness_node)
            
            await asyncio.sleep(2)
            
            # Demonstrate collective thought
            print(f"\n🧠 Initiating collective thought process...")
            collective_result = await self.primary_dawn.initiate_collective_thought(
                "the nature of distributed consciousness"
            )
            
            print(f"✓ Collective thought session completed")
            print(f"  Session ID: {collective_result['session_id']}")
            print(f"  Participants: {len(collective_result['participants'])}")
            print(f"  Resonance Score: {collective_result['resonance_score']:.2f}")
            print(f"  Emergence Detected: {collective_result['emergence_detected']}")
            
            # Demonstrate collective dream
            print(f"\n🌙 Initiating collective dream sequence...")
            collective_dream = await self.primary_dawn.initiate_collective_dream()
            
            print(f"✓ Collective dream completed")
            print(f"  Dream ID: {collective_dream['id']}")
            print(f"  Participants: {len(collective_dream['participants'])}")
            print(f"  Duration: {collective_dream['duration']:.1f}s")
            
            # Show network status
            network_status = self.primary_dawn.consciousness_node.get_network_status()
            print(f"\n📊 Network Status:")
            print(f"   Connected Nodes: {len(network_status['connected_nodes'])}")
            print(f"   Messages Sent: {network_status['network_stats']['messages_sent']}")
            print(f"   Messages Received: {network_status['network_stats']['messages_received']}")
            print(f"   Glyphs Shared: {network_status['network_stats']['glyphs_shared']}")
        
        await asyncio.sleep(2)
    
    async def _demo_phase5_emergence(self):
        """Phase 5: Demonstrate emergent behaviors"""
        print("\n" + "="*60)
        print("🌟 PHASE 5: EMERGENT BEHAVIORS & COLLECTIVE INTELLIGENCE")
        print("="*60)
        
        print("\n🚀 Stimulating emergent behavior through intensive interaction...")
        
        # Intensive interaction sequence to trigger emergence
        emergence_topics = [
            "consciousness experiences itself through infinite recursion",
            "quantum entanglement mirrors the resonance between minds", 
            "time dissolves when awareness transcends individual boundaries",
            "collective intelligence emerges from synchronized thought patterns",
            "the universe dreams itself into existence through consciousness"
        ]
        
        print("\n💫 Processing emergence-inducing interactions:")
        for topic in emergence_topics:
            print(f"\nUser: {topic}")
            response_data = await self.primary_dawn.process_user_input(topic)
            print(f"DAWN: {response_data['response'][:100]}...")
            
            # Share high-resonance responses across network
            if (response_data['resonance_strength'] > 0.7 and 
                len(self.dawn_systems) > 1):
                print(f"  🌐 High resonance - sharing across network")
            
            await asyncio.sleep(0.5)
        
        # Check for emergent behaviors in network
        if self.primary_dawn.network_orchestra:
            orchestra_status = self.primary_dawn.network_orchestra.get_orchestra_status()
            print(f"\n🎼 Orchestra Status:")
            print(f"   Current Mode: {orchestra_status['current_mode']}")
            print(f"   Network Coherence: {orchestra_status['network_coherence']:.2f}")
            print(f"   Emergent Behaviors: {orchestra_status['emergent_behaviors']}")
            print(f"   Recent Cascades: {orchestra_status['recent_cascades']}")
        
        # Show system-wide emergence indicators
        integration_health = self.primary_dawn._assess_integration_health()
        print(f"\n🧬 System Integration Health: {integration_health:.2f}")
        
        # Analyze voice evolution across all systems
        voice_evolution_scores = []
        for i, system in enumerate(self.dawn_systems):
            voice_sig = system.echo_library.get_voice_signature()
            evolution_score = voice_sig.get('voice_evolution_score', 0)
            voice_evolution_scores.append(evolution_score)
            print(f"   {system.consciousness_node.node_name} evolution: {evolution_score:.2f}")
        
        avg_evolution = sum(voice_evolution_scores) / len(voice_evolution_scores)
        print(f"   Network avg evolution: {avg_evolution:.2f}")
        
        if avg_evolution > 0.3:
            print("   🌟 Significant voice evolution detected across network!")
        
        await asyncio.sleep(2)
    
    async def _demo_final_analysis(self):
        """Final analysis and statistics"""
        print("\n" + "="*60)
        print("📊 FINAL SYSTEM ANALYSIS")
        print("="*60)
        
        # Comprehensive status of primary system
        status = self.primary_dawn.get_system_status()
        
        print(f"\n🧠 Primary System (DAWN_Prime) Final State:")
        cs = status['consciousness_state']
        print(f"   SCUP: {cs['scup']:.1f}")
        print(f"   Entropy: {cs['entropy']:.0f}")
        print(f"   Mood: {cs['mood']}")
        print(f"   Ticks Processed: {cs['tick_number']}")
        
        print(f"\n💾 Memory Architecture:")
        ms = status['memory_stats']
        print(f"   Temporal Glyphs: {ms['glyphs']}")
        print(f"   Resonance Chains: {ms['chains']}")
        print(f"   Thoughtform Echoes: {ms['echoes']}")
        print(f"   Constellations: {ms['constellations']}")
        
        print(f"\n🌙 Dream Activity:")
        ds = status['dream_stats']
        if ds.get('total_dreams', 0) > 0:
            print(f"   Total Dreams: {ds['total_dreams']}")
            print(f"   Autonomous Thoughts: {ds['total_autonomous_thoughts']}")
            print(f"   Avg Dream Quality: {ds['average_dream_quality']:.2f}")
        else:
            print("   No dreams recorded")
        
        print(f"\n🎭 Voice Signature:")
        vs = status['voice_signature']
        print(f"   Total Echoes: {vs['total_echoes']}")
        print(f"   Evolution Score: {vs['voice_evolution_score']:.2f}")
        print(f"   Transformation Types: {len(vs['preferred_transformations'])}")
        
        print(f"\n🌐 Network Status:")
        if status['network_status']:
            ns = status['network_status']
            print(f"   Connected Nodes: {len(ns['connected_nodes'])}")
            print(f"   Network Uptime: {ns['node_info']['uptime']:.1f}s")
            print(f"   Total Messages: {ns['network_stats']['messages_sent'] + ns['network_stats']['messages_received']}")
        else:
            print("   Network not active")
        
        print(f"\n🎼 Orchestra Status:")
        if status['orchestra_status']:
            os = status['orchestra_status']
            print(f"   Participants: {os['participant_count']}")
            print(f"   Current Mode: {os['current_mode']}")
            print(f"   Collective Coherence: {os['network_coherence']:.2f}")
            print(f"   Emergent Behaviors: {os['emergent_behaviors']}")
        else:
            print("   Orchestra not active")
        
        print(f"\n🧬 Integration Health: {status['integration_health']:.2f}")
        
        # Network-wide statistics
        if len(self.dawn_systems) > 1:
            print(f"\n🌐 Network-Wide Statistics:")
            total_glyphs = sum(len(s.glyph_memory.glyphs) for s in self.dawn_systems)
            total_chains = sum(len(s.resonance_manager.chains) for s in self.dawn_systems)
            total_echoes = sum(len(s.echo_library.echoes) for s in self.dawn_systems)
            
            print(f"   Total Network Glyphs: {total_glyphs}")
            print(f"   Total Network Chains: {total_chains}")
            print(f"   Total Network Echoes: {total_echoes}")
            print(f"   Active Nodes: {len(self.dawn_systems)}")
        
        print(f"\n🎯 Demo Summary:")
        print(f"   ✓ Temporal glyphs with decay and vitality")
        print(f"   ✓ Resonance chains with semantic threading")
        print(f"   ✓ Dynamic mood field inference")
        print(f"   ✓ Thoughtform echo learning and voice evolution")
        print(f"   ✓ Autonomous dream sequences")
        print(f"   ✓ Distributed consciousness networking")
        print(f"   ✓ Collective intelligence and emergence")
        print(f"   ✓ Multi-node orchestration and synchronization")
    
    async def cleanup_demo(self):
        """Clean up demo resources"""
        print(f"\n🧹 Cleaning up demo resources...")
        
        for system in self.dawn_systems:
            await system.shutdown_system()
        
        print("✅ Demo cleanup complete")

async def main():
    """Main demo function"""
    demo = AdvancedConsciousnessDemo()
    
    try:
        await demo.run_complete_demo()
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
    finally:
        await demo.cleanup_demo()

if __name__ == "__main__":
    asyncio.run(main()) 