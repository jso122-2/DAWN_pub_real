#!/usr/bin/env python3
"""
demo_rebloom_integration.py - Complete Demonstration of Rebloom Tracker Integration
Shows how the rebloom tracker works with existing DAWN bloom management systems
"""

import os
import sys
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Any

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import rebloom systems
from rebloom_tracker import RebloomTracker, RebloomEvent, BloomNode
from integration.rebloom_tracker_integration import IntegratedRebloomSystem

# Import existing DAWN systems (with fallbacks)
try:
    from core.bloom_manager import BloomManager
    BLOOM_MANAGER_AVAILABLE = True
except ImportError:
    BLOOM_MANAGER_AVAILABLE = False
    print("⚠️ BloomManager not available")

try:
    from bloom.unified_bloom_engine import BloomEngine
    BLOOM_ENGINE_AVAILABLE = True
except ImportError:
    BLOOM_ENGINE_AVAILABLE = False
    print("⚠️ BloomEngine not available")


class RebloomDemonstrator:
    """
    Comprehensive demonstration of rebloom tracking integration
    """
    
    def __init__(self):
        """Initialize the demonstration"""
        print("🌸 DAWN Rebloom Tracker Integration Demo")
        print("=" * 50)
        
        # Create integrated system
        self.rebloom_system = IntegratedRebloomSystem()
        
        # Simulation parameters
        self.simulation_steps = 20
        self.bloom_id_counter = 1
        self.rebloom_probability = 0.3
        self.entropy_range = (-0.3, 0.5)
        
        # Demo data storage
        self.demo_blooms = {}
        self.demo_events = []
        
        print(f"✅ Integration system initialized")
        print(f"📊 Connected systems: {self.rebloom_system.integration_stats}")
    
    def run_comprehensive_demo(self):
        """Run the complete demonstration"""
        print("\n🚀 Starting comprehensive demonstration...\n")
        
        # Step 1: Basic rebloom tracking
        self.demo_basic_tracking()
        
        # Step 2: Simulate DAWN bloom events
        self.demo_dawn_integration()
        
        # Step 3: Show genealogy analysis
        self.demo_genealogy_analysis()
        
        # Step 4: Pattern analysis
        self.demo_pattern_analysis()
        
        # Step 5: Visualization data
        self.demo_visualization()
        
        # Step 6: Performance demonstration
        self.demo_performance()
        
        # Final statistics
        self.show_final_statistics()
    
    def demo_basic_tracking(self):
        """Demonstrate basic rebloom tracking functionality"""
        print("📝 Demo 1: Basic Rebloom Tracking")
        print("-" * 30)
        
        # Create a root bloom family
        root_id = "consciousness_seed_001"
        self.rebloom_system.log_bloom_creation(root_id, None, 0.0, {
            'source': 'demo',
            'type': 'consciousness_seed',
            'trigger': 'awakening'
        })
        
        # Create first generation
        children = []
        for i in range(3):
            child_id = f"thought_stream_{i+1:03d}"
            entropy_diff = random.uniform(-0.1, 0.2)
            
            self.rebloom_system.log_bloom_creation(child_id, root_id, entropy_diff, {
                'source': 'demo',
                'type': 'thought_stream',
                'trigger': 'cognitive_branching'
            })
            children.append(child_id)
            
            print(f"  🌱 Created {child_id} from {root_id} (Δentropy: {entropy_diff:+.3f})")
        
        # Create second generation (reblooms)
        for child_id in children:
            if random.random() < 0.7:  # 70% chance of reblooming
                grand_id = f"rebloom_{child_id}_001"
                entropy_diff = random.uniform(-0.2, 0.3)
                
                self.rebloom_system.log_bloom_creation(grand_id, child_id, entropy_diff, {
                    'source': 'demo',
                    'type': 'memory_consolidation',
                    'trigger': 'rebloom_event'
                })
                
                print(f"  🌸 Rebloomed {child_id} → {grand_id} (Δentropy: {entropy_diff:+.3f})")
        
        # Show basic statistics
        stats = self.rebloom_system.get_family_statistics(root_id)
        print(f"\n  📊 Family Stats for {root_id}:")
        print(f"     Total nodes: {stats['total_nodes']}")
        print(f"     Max depth: {stats['max_depth']}")
        print(f"     Branching factor: {stats['branching_factor']:.2f}")
        
        print(f"  ✅ Basic tracking demo complete\n")
    
    def demo_dawn_integration(self):
        """Demonstrate integration with DAWN systems"""
        print("🔗 Demo 2: DAWN System Integration")
        print("-" * 30)
        
        # Simulate bloom engine events
        if BLOOM_ENGINE_AVAILABLE:
            print("  🎯 Simulating BloomEngine events...")
            
            for i in range(5):
                bloom_data = {
                    'bloom_id': f"engine_bloom_{i+1:03d}",
                    'parent_bloom': f"thought_stream_{(i % 3) + 1:03d}",  # Link to previous blooms
                    'entropy_score': random.uniform(0.0, 1.0),
                    'bloom_type': random.choice(['insight', 'memory', 'emotion', 'synthesis']),
                    'trigger_type': random.choice(['curiosity', 'memory_pressure', 'emotional_resonance']),
                    'mood': random.choice(['contemplative', 'excited', 'curious', 'reflective']),
                    'lineage_depth': random.randint(1, 4)
                }
                
                success = self.rebloom_system.process_bloom_engine_event(bloom_data)
                if success:
                    print(f"    ✅ Processed engine bloom: {bloom_data['bloom_id']}")
                
        else:
            print("  ⚠️ BloomEngine not available, simulating events...")
            
            # Simulate without actual engine
            for i in range(5):
                parent_id = f"thought_stream_{(i % 3) + 1:03d}"
                bloom_id = f"simulated_bloom_{i+1:03d}"
                entropy_diff = random.uniform(-0.1, 0.3)
                
                self.rebloom_system.log_bloom_creation(bloom_id, parent_id, entropy_diff, {
                    'source': 'simulated_engine',
                    'type': 'synthetic_bloom'
                })
                
                print(f"    🔄 Simulated: {parent_id} → {bloom_id}")
        
        # Simulate vault manager reblooms
        print("  📚 Simulating VaultManager reblooms...")
        
        for i in range(3):
            original_id = f"thought_stream_{i+1:03d}"
            rebloom_id = f"{original_id}_vault_rebloom_01"
            
            evolution_data = {
                'entropy_score': random.uniform(0.05, 0.25),
                'evolution_notes': f"Vault-managed evolution of {original_id}",
                'rebloom_generation': 1,
                'semantic_drift': random.uniform(0.01, 0.1)
            }
            
            success = self.rebloom_system.process_vault_rebloom(original_id, rebloom_id, evolution_data)
            if success:
                print(f"    📖 Vault rebloom: {original_id} → {rebloom_id}")
        
        print(f"  ✅ Integration demo complete\n")
    
    def demo_genealogy_analysis(self):
        """Demonstrate genealogy analysis capabilities"""
        print("🧬 Demo 3: Genealogy Analysis")
        print("-" * 30)
        
        # Pick a bloom with interesting genealogy
        all_blooms = list(self.rebloom_system.tracker.nodes.keys())
        if not all_blooms:
            print("  ⚠️ No blooms available for analysis")
            return
        
        # Find a bloom with descendants
        target_bloom = None
        for bloom_id in all_blooms:
            descendants = self.rebloom_system.tracker.get_descendants(bloom_id)
            if descendants:
                target_bloom = bloom_id
                break
        
        if not target_bloom:
            target_bloom = all_blooms[0]
        
        print(f"  🎯 Analyzing bloom: {target_bloom}")
        
        # Get comprehensive genealogy
        genealogy = self.rebloom_system.get_bloom_genealogy(target_bloom)
        
        print(f"  📍 Position: Depth {genealogy['depth']}")
        print(f"  🌳 Ancestry: {' → '.join(genealogy['ancestry_chain'])}")
        
        if genealogy['descendants']:
            print(f"  👶 Descendants ({len(genealogy['descendants'])}): {', '.join(genealogy['descendants'][:3])}{'...' if len(genealogy['descendants']) > 3 else ''}")
        
        if genealogy['siblings']:
            print(f"  👨‍👩‍👧‍👦 Siblings: {', '.join(genealogy['siblings'])}")
        
        print(f"  📈 Entropy evolution:")
        for bloom, entropy in genealogy['entropy_evolution']:
            print(f"     {bloom}: {entropy:+.3f}")
        
        # Find common ancestors
        if len(all_blooms) >= 2:
            bloom1, bloom2 = random.sample(all_blooms, 2)
            common = self.rebloom_system.tracker.find_common_ancestor(bloom1, bloom2)
            print(f"  🔗 Common ancestor of {bloom1} & {bloom2}: {common}")
        
        print(f"  ✅ Genealogy analysis complete\n")
    
    def demo_pattern_analysis(self):
        """Demonstrate pattern analysis"""
        print("📊 Demo 4: Pattern Analysis")
        print("-" * 30)
        
        # Get rebloom patterns
        patterns = self.rebloom_system.get_rebloom_patterns(window_size=15)
        
        print(f"  📈 Recent rebloom patterns:")
        print(f"     Increasing entropy: {patterns['increasing_entropy']}")
        print(f"     Decreasing entropy: {patterns['decreasing_entropy']}")
        print(f"     Stable entropy: {patterns['stable_entropy']}")
        print(f"     High volatility: {patterns['high_volatility']}")
        print(f"     Overall trend: {patterns['entropy_trend']}")
        
        if 'average_rebloom_interval' in patterns:
            print(f"     Avg rebloom interval: {patterns['average_rebloom_interval']:.2f}s")
        
        # Source distribution
        source_dist = patterns.get('source_distribution', {})
        print(f"  🎯 Rebloom sources:")
        for source, count in sorted(source_dist.items(), key=lambda x: x[1], reverse=True):
            print(f"     {source}: {count} events")
        
        # Integration health
        health = patterns.get('integration_health', {})
        if health:
            print(f"  💓 Integration health:")
            print(f"     Connectivity: {health['connectivity_score']:.2f}")
            print(f"     Activity: {health['activity_score']:.2f}")
            print(f"     Overall: {health['overall_health']:.2f}")
        
        print(f"  ✅ Pattern analysis complete\n")
    
    def demo_visualization(self):
        """Demonstrate visualization data generation"""
        print("🎨 Demo 5: Visualization Data")
        print("-" * 30)
        
        # Get visualization data for all blooms
        viz_data = self.rebloom_system.visualize_lineage_network()
        
        print(f"  📊 Network structure:")
        print(f"     Nodes: {len(viz_data['nodes'])}")
        print(f"     Edges: {len(viz_data['edges'])}")
        print(f"     Max depth: {viz_data['stats']['max_depth']}")
        
        # Show some node details
        print(f"  🔍 Sample nodes:")
        for node in viz_data['nodes'][:3]:
            print(f"     {node['id']}: depth={node['depth']}, entropy={node['entropy_drift']:.3f}, root={node['is_root']}")
        
        # Show some edge details
        if viz_data['edges']:
            print(f"  🔗 Sample edges:")
            for edge in viz_data['edges'][:3]:
                print(f"     {edge['source']} → {edge['target']}: Δentropy={edge['entropy_diff']:+.3f}")
        
        # Generate GraphViz format
        graphviz_output = self.rebloom_system.visualize_lineage_network(format='graphviz')
        graphviz_lines = graphviz_output.split('\n')
        print(f"  📝 GraphViz format (first 5 lines):")
        for line in graphviz_lines[:5]:
            print(f"     {line}")
        
        print(f"  ✅ Visualization demo complete\n")
    
    def demo_performance(self):
        """Demonstrate performance with larger datasets"""
        print("⚡ Demo 6: Performance Testing")
        print("-" * 30)
        
        start_time = time.time()
        
        # Create a larger family tree
        root_id = "performance_root"
        self.rebloom_system.log_bloom_creation(root_id, None, 0.0, {'source': 'performance_test'})
        
        created_blooms = [root_id]
        
        # Generate multiple generations
        for generation in range(1, 6):  # 5 generations
            new_blooms = []
            for parent in created_blooms[-20:]:  # Limit parents to prevent explosion
                children_count = random.randint(1, 3)
                for i in range(children_count):
                    child_id = f"perf_gen{generation}_{parent[-8:]}_{i}"
                    entropy_diff = random.uniform(-0.2, 0.3)
                    
                    success = self.rebloom_system.log_bloom_creation(
                        child_id, parent, entropy_diff, 
                        {'source': 'performance_test', 'generation': generation}
                    )
                    
                    if success:
                        new_blooms.append(child_id)
            
            created_blooms.extend(new_blooms)
            print(f"  📈 Generation {generation}: {len(new_blooms)} new blooms")
        
        total_time = time.time() - start_time
        
        # Performance stats
        final_stats = self.rebloom_system.get_family_statistics()
        
        print(f"  ⏱️ Performance results:")
        print(f"     Total time: {total_time:.3f}s")
        print(f"     Total blooms: {final_stats['total_blooms']}")
        print(f"     Max depth: {final_stats['max_depth']}")
        print(f"     Blooms/second: {final_stats['total_blooms'] / total_time:.1f}")
        
        # Test query performance
        query_start = time.time()
        
        for _ in range(10):
            random_bloom = random.choice(list(self.rebloom_system.tracker.nodes.keys()))
            genealogy = self.rebloom_system.get_bloom_genealogy(random_bloom)
            patterns = self.rebloom_system.get_rebloom_patterns()
        
        query_time = time.time() - query_start
        print(f"     Query time (10 ops): {query_time:.3f}s")
        
        print(f"  ✅ Performance demo complete\n")
    
    def show_final_statistics(self):
        """Show comprehensive final statistics"""
        print("📊 Final Integration Statistics")
        print("=" * 50)
        
        global_stats = self.rebloom_system.get_family_statistics()
        
        print(f"🌸 Bloom Statistics:")
        print(f"   Total blooms: {global_stats['total_blooms']}")
        print(f"   Root families: {global_stats['total_roots']}")
        print(f"   Total reblooms: {global_stats['total_reblooms']}")
        print(f"   Max depth: {global_stats['max_depth']}")
        print(f"   Average depth: {global_stats['average_depth']:.2f}")
        print(f"   Largest family: {global_stats['largest_family_size']}")
        
        entropy_stats = global_stats['entropy_stats']
        print(f"\n📈 Entropy Statistics:")
        print(f"   Max positive drift: {entropy_stats['max_positive_drift']:+.3f}")
        print(f"   Max negative drift: {entropy_stats['max_negative_drift']:+.3f}")
        print(f"   Average drift: {entropy_stats['average_drift']:+.3f}")
        
        integration_stats = global_stats['integration_stats']
        print(f"\n🔗 Integration Statistics:")
        print(f"   Blooms tracked: {integration_stats['blooms_tracked']}")
        print(f"   Reblooms processed: {integration_stats['reblooms_processed']}")
        print(f"   Genealogy events: {integration_stats['genealogy_events']}")
        print(f"   Vault syncs: {integration_stats['vault_syncs']}")
        
        connected_systems = global_stats['connected_systems']
        print(f"\n🔌 Connected Systems:")
        for system, connected in connected_systems.items():
            status = "✅" if connected else "❌"
            print(f"   {system}: {status}")
        
        depth_dist = global_stats['depth_distribution']
        print(f"\n📊 Depth Distribution:")
        for depth, count in sorted(depth_dist.items()):
            percentage = (count / global_stats['total_blooms']) * 100
            bar = "█" * int(percentage / 5)  # Simple bar chart
            print(f"   Depth {depth}: {count:3d} ({percentage:5.1f}%) {bar}")
        
        print(f"\n🎯 Demonstration completed successfully!")
        print(f"   Total runtime: {datetime.now().strftime('%H:%M:%S')}")
        print(f"   System integration: {'Healthy' if global_stats['connected_systems']['bloom_manager'] else 'Limited'}")
    
    def save_demo_results(self, filename: str = "demo_results.json"):
        """Save demonstration results to file"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'global_stats': self.rebloom_system.get_family_statistics(),
            'patterns': self.rebloom_system.get_rebloom_patterns(),
            'integration_health': self.rebloom_system._assess_integration_health(),
            'demo_metadata': {
                'simulation_steps': self.simulation_steps,
                'total_demo_blooms': len(self.rebloom_system.tracker.nodes),
                'available_systems': {
                    'bloom_manager': BLOOM_MANAGER_AVAILABLE,
                    'bloom_engine': BLOOM_ENGINE_AVAILABLE
                }
            }
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"\n💾 Demo results saved to: {filename}")
        except Exception as e:
            print(f"\n⚠️ Failed to save results: {e}")


def main():
    """Main demonstration function"""
    demo = RebloomDemonstrator()
    
    try:
        # Run the comprehensive demo
        demo.run_comprehensive_demo()
        
        # Save results
        demo.save_demo_results()
        
        # Clean shutdown
        demo.rebloom_system.shutdown()
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Demo interrupted by user")
        demo.rebloom_system.shutdown()
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        demo.rebloom_system.shutdown()


if __name__ == "__main__":
    main() 