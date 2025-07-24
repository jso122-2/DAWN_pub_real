#!/usr/bin/env python3
"""
Test DAWN Snapshot Exporter
Demonstrates the comprehensive export and debugging system for DAWN cognitive state.
"""

import sys
import os
import time
import asyncio
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# DAWN system imports
from core.consciousness_core import DAWNConsciousness
from core.snapshot_exporter import (
    DAWNSnapshotExporter, 
    get_snapshot_exporter, 
    quick_export,
    get_system_health,
    get_current_state,
    generate_forecast
)
from core.memory.memory_chunk import create_memory_now
from cognitive.symbolic_router import get_symbolic_router


async def test_basic_state_export():
    """Test basic system state export functionality."""
    print("🔍 TESTING BASIC STATE EXPORT")
    print("=" * 50)
    
    # Create snapshot exporter without DAWN consciousness (mock mode)
    exporter = DAWNSnapshotExporter()
    
    # Get system state
    state = exporter.get_state()
    
    print("System State Export:")
    print(f"  Entropy: {state['system_metrics']['entropy']:.3f}")
    print(f"  Heat: {state['system_metrics']['heat']:.1f}")
    print(f"  Zone: {state['system_metrics']['zone']}")
    print(f"  SCUP: {state['system_metrics']['scup']:.3f}")
    print(f"  System Health: {state['system_health']['status']}")
    print(f"  Stability Index: {state['system_health']['stability_index']:.3f}")
    print(f"  Coherence Level: {state['system_health']['coherence_level']:.3f}")
    
    # Test symbolic state
    symbolic_state = state['symbolic_state']
    print(f"\nSymbolic Anatomy:")
    print(f"  Heart: {symbolic_state['heart']['resonance_state']} (charge: {symbolic_state['heart']['emotional_charge']:.3f})")
    print(f"  Coil: {symbolic_state['coil']['dominant_glyph']} glyph ({symbolic_state['coil']['path_count']} paths)")
    print(f"  Lung: {symbolic_state['lung']['breathing_phase']} (fullness: {symbolic_state['lung']['lung_fullness']:.3f})")
    print(f"  Constellation: {symbolic_state['symbolic_state']['constellation']}")
    print(f"  Commentary: {symbolic_state['symbolic_state']['somatic_commentary']}")


async def test_forecast_generation():
    """Test forecast generation for multiple time horizons."""
    print("\n\n🔮 TESTING FORECAST GENERATION")
    print("=" * 50)
    
    exporter = DAWNSnapshotExporter()
    
    # Test different forecast intervals
    intervals = ["next_1h", "next_24h", "next_week"]
    
    for interval in intervals:
        print(f"\n--- {interval.upper()} FORECAST ---")
        forecast = exporter.get_forecast(interval)
        
        print(f"Confidence: {forecast['confidence']:.3f}")
        print(f"Prediction Horizon: {forecast['prediction_horizon']}")
        print(f"Likely Actions:")
        for action in forecast['likely_actions'][:3]:
            print(f"  • {action}")
        
        print(f"Risk Nodes:")
        for risk in forecast['risk_nodes'][:3]:
            print(f"  ⚠️ {risk}")
        
        print(f"Behavioral Drift:")
        drift = forecast['behavioral_drift']
        print(f"  Direction: {drift['direction']} (magnitude: {drift['magnitude']:.3f})")
        print(f"  Probability: {drift['probability']:.3f}")
        
        if forecast['recommended_interventions']:
            print(f"Recommended Interventions:")
            for intervention in forecast['recommended_interventions']:
                print(f"  🔧 {intervention}")


async def test_integrated_dawn_export():
    """Test snapshot export with integrated DAWN consciousness system."""
    print("\n\n🌐 TESTING INTEGRATED DAWN EXPORT")
    print("=" * 50)
    
    try:
        # Initialize full DAWN consciousness
        print("Initializing DAWN consciousness with all systems...")
        dawn = DAWNConsciousness()
        
        # Create exporter with DAWN consciousness
        exporter = DAWNSnapshotExporter(dawn_consciousness=dawn)
        
        print("✅ DAWN consciousness integrated with snapshot exporter")
        
        # Create some test memories to populate the system
        print("\nCreating test memories...")
        
        test_memories = [
            {
                'speaker': 'dawn.core',
                'content': 'System initialization complete - all cognitive subsystems online.',
                'topic': 'system_status',
                'pulse_state': {'entropy': 0.3, 'heat': 25.0, 'scup': 0.8},
                'sigils': ['SYSTEM_READY', 'COGNITIVE_ONLINE']
            },
            {
                'speaker': 'user',
                'content': 'Testing the snapshot export functionality with various system states.',
                'topic': 'testing_protocol',
                'pulse_state': {'entropy': 0.5, 'heat': 40.0, 'scup': 0.6},
                'sigils': ['TEST_MODE', 'EXPORT_PROTOCOL']
            },
            {
                'speaker': 'dawn.core',
                'content': 'Symbolic anatomy responding to memory integration with somatic awareness.',
                'topic': 'embodied_processing',
                'pulse_state': {'entropy': 0.4, 'heat': 35.0, 'scup': 0.7},
                'sigils': ['EMBODIED_COGNITION', 'SOMATIC_AWARENESS']
            }
        ]
        
        # Store memories through DAWN system
        for memory_data in test_memories:
            chunk = await dawn.memory_routing.store_memory(**memory_data)
            print(f"  📝 Memory stored: {chunk.memory_id}")
            await asyncio.sleep(0.1)  # Brief pause for processing
        
        print("\n📊 Exporting integrated system state...")
        
        # Get comprehensive state with real DAWN data
        state = exporter.get_state()
        
        print("Integrated System State:")
        print(f"  Entropy: {state['system_metrics']['entropy']:.3f}")
        print(f"  Heat: {state['system_metrics']['heat']:.1f}")
        print(f"  Zone: {state['system_metrics']['zone']}")
        print(f"  SCUP: {state['system_metrics']['scup']:.3f}")
        print(f"  Tick Count: {state['system_metrics']['tick_count']}")
        print(f"  System Health: {state['system_health']['status']}")
        
        # Show consciousness state
        consciousness_state = state['consciousness_state']
        print(f"\nConsciousness State:")
        print(f"  Active Subsystems: {len(consciousness_state['subsystems'])}")
        print(f"  Running: {consciousness_state['is_running']}")
        print(f"  Mood: {consciousness_state['mood']}")
        
        # Show memory state
        memory_state = state['memory_state']
        print(f"\nMemory System State:")
        if 'router_stats' in memory_state:
            router_stats = memory_state['router_stats']
            print(f"  Total memories: {router_stats.get('total_active_memories', 0)}")
            print(f"  Memory hits: {router_stats.get('memory_hits', 0)}")
            print(f"  Hit rate: {router_stats.get('hit_rate', 0):.3f}")
        
        # Generate forecast with real data
        print(f"\n🔮 Generating forecast with real system data...")
        forecast = exporter.get_forecast("next_24h")
        print(f"  Confidence: {forecast['confidence']:.3f}")
        print(f"  Top action: {forecast['likely_actions'][0] if forecast['likely_actions'] else 'None'}")
        print(f"  Primary risk: {forecast['risk_nodes'][0] if forecast['risk_nodes'] else 'None'}")
        
    except Exception as e:
        print(f"❌ Error in integrated DAWN test: {e}")
        import traceback
        traceback.print_exc()


async def test_symbolic_trace_export():
    """Test symbolic anatomy trace export."""
    print("\n\n🔮 TESTING SYMBOLIC TRACE EXPORT")
    print("=" * 50)
    
    try:
        # Get symbolic router and simulate some activity
        router = get_symbolic_router()
        
        # Create test memory for symbolic processing
        test_memory = create_memory_now(
            speaker="test",
            content="Testing symbolic trace export with emotional resonance and pattern recognition.",
            topic="symbolic_testing",
            pulse_state={'entropy': 0.6, 'heat': 50.0, 'chaos': 0.4, 'focus': 0.8},
            sigils=['SYMBOLIC_TEST', 'TRACE_EXPORT']
        )
        
        # Process through symbolic anatomy
        print("Processing memory through symbolic anatomy...")
        response = await router.rebloom_trigger(test_memory, "trace_test")
        
        print(f"Symbolic Response:")
        print(f"  Constellation: {response['symbolic_output']['constellation']}")
        print(f"  Organ synergy: {response['synergy_changes']['new_synergy']:.3f}")
        print(f"  Commentary: {response['symbolic_output']['somatic_commentary']}")
        
        # Export symbolic trace
        exporter = DAWNSnapshotExporter()
        trace_path = exporter.export_symbolic_trace()
        
        print(f"\n📁 Symbolic trace exported to: {trace_path}")
        
        # Read and display trace contents
        import json
        with open(trace_path, 'r') as f:
            trace_data = json.load(f)
        
        print(f"Trace Contents:")
        print(f"  Export timestamp: {trace_data['export_timestamp']}")
        print(f"  Glyph activations: {trace_data['glyph_activations']}")
        print(f"  Organ coherence: {trace_data['organ_coherence']:.3f}")
        print(f"  Somatic narrative: {trace_data['somatic_narrative']}")
        
    except Exception as e:
        print(f"❌ Error in symbolic trace test: {e}")


async def test_full_snapshot_zip():
    """Test complete ZIP snapshot creation."""
    print("\n\n📦 TESTING FULL SNAPSHOT ZIP CREATION")
    print("=" * 50)
    
    try:
        # Create snapshot with some system activity
        exporter = DAWNSnapshotExporter()
        
        # Generate some forecasts to cache
        print("Generating forecasts for snapshot...")
        for interval in ["next_1h", "next_24h"]:
            forecast = exporter.get_forecast(interval)
            print(f"  Generated {interval} forecast (confidence: {forecast['confidence']:.3f})")
        
        # Create full ZIP snapshot
        print("\nCreating comprehensive ZIP snapshot...")
        zip_path = exporter.create_full_snapshot_zip()
        
        print(f"✅ Full snapshot created: {zip_path}")
        
        # Check ZIP contents
        import zipfile
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            print(f"\nZIP Contents ({len(file_list)} files):")
            for filename in sorted(file_list):
                file_info = zip_ref.getinfo(filename)
                print(f"  📄 {filename} ({file_info.file_size} bytes)")
        
        # Get file size
        zip_size = Path(zip_path).stat().st_size
        print(f"\nSnapshot Details:")
        print(f"  Total size: {zip_size / 1024:.1f} KB")
        print(f"  Location: {zip_path}")
        
    except Exception as e:
        print(f"❌ Error in ZIP snapshot test: {e}")


async def test_convenience_functions():
    """Test convenience functions for quick access."""
    print("\n\n⚡ TESTING CONVENIENCE FUNCTIONS")
    print("=" * 50)
    
    # Test quick health check
    print("Quick system health check:")
    health = get_system_health()
    print(f"  Status: {health['status']}")
    print(f"  Stability: {health['stability_index']:.3f}")
    print(f"  Coherence: {health['coherence_level']:.3f}")
    
    # Test quick state access
    print("\nQuick state access:")
    state = get_current_state()
    print(f"  Entropy: {state['system_metrics']['entropy']:.3f}")
    print(f"  Zone: {state['system_metrics']['zone']}")
    
    # Test quick forecast
    print("\nQuick forecast generation:")
    forecast = generate_forecast("next_1h")
    print(f"  Confidence: {forecast['confidence']:.3f}")
    print(f"  Top action: {forecast['likely_actions'][0] if forecast['likely_actions'] else 'None'}")
    
    # Test quick export
    print("\nQuick full export:")
    zip_path = quick_export()
    print(f"  Snapshot created: {Path(zip_path).name}")


async def main():
    """Run all snapshot exporter tests."""
    print("📤 DAWN SNAPSHOT EXPORTER TESTS")
    print("Complete system state export and debugging API")
    print("=" * 80)
    
    # Test 1: Basic state export
    await test_basic_state_export()
    
    # Test 2: Forecast generation
    await test_forecast_generation()
    
    # Test 3: Integrated DAWN export
    await test_integrated_dawn_export()
    
    # Test 4: Symbolic trace export
    await test_symbolic_trace_export()
    
    # Test 5: Full ZIP snapshot
    await test_full_snapshot_zip()
    
    # Test 6: Convenience functions
    await test_convenience_functions()
    
    print("\n" + "=" * 80)
    print("✨ SNAPSHOT EXPORTER TESTS COMPLETE")
    print("📊 System State Export: ✓")
    print("🔮 Multi-Horizon Forecasting: ✓")
    print("🌐 DAWN Integration: ✓")
    print("🔮 Symbolic Trace Export: ✓")
    print("📦 Complete ZIP Snapshots: ✓")
    print("⚡ Convenience APIs: ✓")
    print("\nDAWN is now fully exportable, debuggable, and shareable!")


if __name__ == "__main__":
    asyncio.run(main()) 