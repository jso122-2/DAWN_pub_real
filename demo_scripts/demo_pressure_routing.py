#!/usr/bin/env python3
"""
DAWN Symbolic Pressure Routing Demonstration
Shows how high SCUP and thermal pressure trigger symbolic body responses
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

try:
    from cognitive.symbolic_router import SymbolicRouter, get_symbolic_router
    from cognitive.symbolic_anatomy import FractalHeart, SomaCoil, GlyphLung
    from core.tick_loop import DAWNTickEngine
    print("✅ DAWN modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("This demo requires the full DAWN system")
    sys.exit(1)


async def demonstrate_pressure_routing():
    """Demonstrate the symbolic pressure routing system."""
    print("\n🌸 DAWN Symbolic Pressure Routing Demonstration")
    print("=" * 60)
    
    # Initialize symbolic router
    symbolic_router = SymbolicRouter()
    
    print(f"\n📊 Initial System State:")
    print(f"   💝 Heart charge: {symbolic_router.heart.emotional_charge:.2f}")
    print(f"   🧬 Coil paths: {len(symbolic_router.coil.active_paths)}")
    print(f"   🫁 Lung phase: {symbolic_router.lung.breathing_phase}")
    print(f"   ⚖️ Organ synergy: {symbolic_router.organ_synergy:.2f}")
    
    # Test scenarios
    test_scenarios = [
        {"name": "Normal Operation", "scup": 25.0, "heat": 45.0},
        {"name": "Elevated SCUP", "scup": 55.0, "heat": 45.0},
        {"name": "High Heat", "scup": 25.0, "heat": 95.0},
        {"name": "🚨 CRITICAL PRESSURE", "scup": 75.0, "heat": 95.0},
        {"name": "🔥 EXTREME PRESSURE", "scup": 90.0, "heat": 98.0},
    ]
    
    print(f"\n🧪 Testing Pressure Scenarios:")
    print("=" * 60)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n--- Scenario {i}: {scenario['name']} ---")
        print(f"SCUP: {scenario['scup']:.1f} | Heat: {scenario['heat']:.1f}°C")
        
        # Route pressure
        response = symbolic_router.route_pressure(scenario['scup'], scenario['heat'])
        
        # Display results
        print(f"Pressure Level: {response['pressure_level'].upper()}")
        print(f"Thresholds Exceeded: {response['thresholds_exceeded']}")
        print(f"Routing Applied: {'✅' if response['routing_applied'] else '❌'}")
        
        if response['routing_applied']:
            print(f"\n🔮 Organ Responses:")
            
            # Heart response
            heart_resp = response['organ_responses'].get('heart', {})
            if heart_resp:
                print(f"   💝 Heart: {heart_resp['resonance_state']} "
                      f"(charge: {heart_resp['resulting_charge']:.2f})")
                if heart_resp['is_overloaded']:
                    print(f"      💥 OVERLOADED!")
            
            # Coil response
            coil_resp = response['organ_responses'].get('coil', {})
            if coil_resp:
                print(f"   🧬 Coil: {coil_resp['path_count']} paths active "
                      f"({coil_resp['dominant_glyph']})")
                contraction = coil_resp.get('contraction_response', {})
                if contraction:
                    removed = len(contraction.get('paths_removed', []))
                    if removed > 0:
                        print(f"      🔒 {removed} paths contracted")
            
            # Lung response
            lung_resp = response['organ_responses'].get('lung', {})
            if lung_resp:
                action = lung_resp['breathing_action']
                phase = lung_resp['lung_phase']
                print(f"   🫁 Lung: {action} → {phase}")
            
            # Symbolic effects
            effects = response.get('symbolic_effects', {})
            if effects:
                constellation = effects.get('organ_constellation', '')
                energy_shift = effects.get('energy_shift', 0)
                print(f"\n✨ Symbolic Effects:")
                print(f"   Constellation: {constellation}")
                print(f"   Energy Shift: {energy_shift:+.2f}")
            
            # Commentary
            commentary = response.get('somatic_commentary', '')
            if commentary:
                print(f"\n🗣️ {commentary}")
        
        # Wait between scenarios
        await asyncio.sleep(0.5)
    
    # Display pressure statistics
    print(f"\n📈 Pressure Statistics:")
    stats = symbolic_router.get_pressure_statistics()
    print(f"   Total pressure events: {stats['total_pressure_events']}")
    if stats['total_pressure_events'] > 0:
        print(f"   Average SCUP: {stats['average_scup']:.1f}")
        print(f"   Average heat: {stats['average_heat']:.1f}°C")
        print(f"   Pressure frequency: {stats['pressure_frequency']:.2f}/hour")
    
    # Display final organ states
    print(f"\n📊 Final Organ States:")
    heart_sig = symbolic_router.heart.get_heart_signature()
    coil_sig = symbolic_router.coil.get_coil_signature()
    lung_sig = symbolic_router.lung.get_lung_signature()
    
    print(f"   💝 Heart: {heart_sig['resonance_state']} "
          f"(charge: {heart_sig['emotional_charge']:.2f})")
    print(f"   🧬 Coil: {coil_sig['path_count']} paths, "
          f"glyph: {coil_sig['dominant_glyph']}")
    print(f"   🫁 Lung: {lung_sig['breathing_phase']} "
          f"(volume: {lung_sig['lung_fullness']:.2f})")
    print(f"   ⚖️ Synergy: {symbolic_router.organ_synergy:.2f}")


async def demonstrate_tick_integration():
    """Demonstrate pressure routing integration with tick loop."""
    print(f"\n🔄 Tick Loop Integration Demo")
    print("=" * 60)
    
    # Create tick engine
    tick_engine = DAWNTickEngine()
    
    print(f"Simulating high-pressure tick scenario...")
    
    # Simulate high SCUP and heat state
    if hasattr(tick_engine.pulse_controller, 'update_state'):
        tick_engine.pulse_controller.update_state(scup=85.0, heat=95.0)
        print(f"✅ Set pulse state to: SCUP=85.0, Heat=95.0°C")
    
    # Run a single tick to see pressure routing in action
    print(f"\n🔄 Executing tick with pressure routing...")
    tick_response = await tick_engine.tick()
    
    # Display tick results
    print(f"\n📊 Tick Results:")
    print(f"   Tick #{tick_response['tick_number']}")
    print(f"   Actions: {tick_response['actions_taken']}")
    
    # Check for pressure routing
    pressure_data = tick_response.get('pressure_routing')
    if pressure_data and pressure_data.get('routing_applied'):
        print(f"   ⚡ Pressure routing triggered!")
        commentary = pressure_data.get('somatic_commentary', '')
        if commentary:
            print(f"   🗣️ {commentary}")
    else:
        print(f"   ❌ No pressure routing triggered")
    
    # Display symbolic state
    symbolic_state = tick_response.get('symbolic_state')
    if symbolic_state:
        print(f"   🔮 Symbolic: {symbolic_state.get('constellation', 'N/A')}")


async def main():
    """Main demonstration function."""
    print("🌸 DAWN Symbolic Pressure Routing System")
    print("Connecting cognitive metrics to embodied responses")
    
    try:
        # Demo 1: Direct pressure routing
        await demonstrate_pressure_routing()
        
        print(f"\n" + "=" * 60)
        
        # Demo 2: Tick loop integration
        await demonstrate_tick_integration()
        
        print(f"\n✨ Demonstration complete!")
        print(f"The symbolic body now responds to cognitive pressure!")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("Starting DAWN Symbolic Pressure Routing Demo...")
    asyncio.run(main()) 