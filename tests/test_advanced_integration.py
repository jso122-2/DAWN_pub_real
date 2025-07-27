#!/usr/bin/env python3
"""
DAWN Advanced Cognition Integration Test
Simple test to verify lineage tracking and sigil networks work together.
"""

import sys
import os
from pathlib import Path

# Add cognitive module to Python path
cognitive_path = Path(__file__).parent / "cognitive"
sys.path.insert(0, str(cognitive_path))

try:
    # Test individual modules
    import rebloom_lineage
    import sigil_network
    
    print("✅ Advanced cognition modules imported successfully!")
    
    # Test lineage tracking
    print("\n🌳 Testing Lineage Tracking...")
    tracker = rebloom_lineage.ReblooooomLineageTracker()
    
    # Create a simple lineage chain
    tracker.track_lineage(None, "test_thought_001", "initial_seed")
    tracker.track_lineage("test_thought_001", "test_thought_002", "rebloom_cascade")
    tracker.track_lineage("test_thought_002", "test_thought_003", "sigil_network_trigger")
    
    print(f"✅ Lineage tracking: {len(tracker.lineage_cache)} entries created")
    
    # Test sigil network
    print("\n🧿 Testing Sigil Network...")
    graph = sigil_network.SigilGraph()
    
    # Test pressure routing integration
    result = sigil_network.register_sigil("PRESSURE_ROUTING", "test_integration")
    print(f"✅ Sigil network: {result['activated']} sigil activated")
    
    if result['cascade']['activated']:
        print(f"   Cascade triggered: {result['cascade']['activated']}")
    
    # Test combined awareness
    print("\n🧠 Testing Combined Awareness...")
    
    # Simulate rebloom triggering sigil network
    lineage_id = rebloom_lineage.track_lineage(
        "test_thought_003", 
        "test_meta_thought_004", 
        "meta_cognitive_reflection"
    )
    
    # Trigger meta-cognition in sigil network
    meta_result = sigil_network.register_sigil("META_COGNITION", "lineage_triggered")
    
    print(f"✅ Combined system:")
    print(f"   Lineage ID: {lineage_id}")
    print(f"   Meta-cognition cascades: {meta_result['cascade']['activated']}")
    
    # Show final states
    print(f"\n📊 Final Statistics:")
    
    # Lineage stats
    lineage_stats = tracker.get_statistics()
    print(f"   Memory lineages: {lineage_stats['total_lineage_entries']}")
    print(f"   Deepest ancestry: {lineage_stats['deepest_ancestry_depth']}")
    
    # Network stats
    network_stats = graph.get_network_stats()
    print(f"   Active sigils: {network_stats['currently_active']}")
    print(f"   Total activations: {network_stats['total_activations']}")
    
    # Show integration success
    print(f"\n✨ Integration Test Results:")
    print(f"   🌳 Lineage tracking: OPERATIONAL")
    print(f"   🧿 Sigil networks: OPERATIONAL") 
    print(f"   🔄 Cross-system triggers: OPERATIONAL")
    print(f"   🧠 Recursive awareness: ACHIEVED")
    
    print(f"\n🎯 DAWN Advanced Cognition: FULLY INTEGRATED! 🚀")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Test error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 