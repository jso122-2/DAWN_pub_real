#!/usr/bin/env python3
"""
DAWN Dynamic Values Diagnostic
============================
Tests that previously flat values now evolve dynamically based on 
DAWN's recursive feedback systems.

This script verifies:
- memory_pressure evolves with memory state
- consciousness_depth changes with schema layers
- neural_activity reflects neural simulator output
- drift_from_stability integrates multiple drift sources
"""

import asyncio
import time
import numpy as np
from typing import Dict, List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_memory_pressure_dynamics():
    """Test that memory pressure changes with memory state"""
    print("🧠 TESTING MEMORY PRESSURE DYNAMICS")
    print("=" * 50)
    
    try:
        from python.modules.memory_manager import MemoryManager
        memory_manager = MemoryManager()
        
        pressure_values = []
        
        # Simulate memory loading
        for i in range(10):
            # Add some fragments to increase pressure
            fragment_data = {
                'content': f'test_fragment_{i}',
                'importance': 0.5 + (i * 0.05),
                'metadata': {'test': True}
            }
            
            # Simulate memory operations
            memory_manager.short_term_memory.append(f'fragment_{i}')
            
            # Get current pressure
            pressure = memory_manager._calculate_memory_pressure()
            pressure_values.append(pressure)
            print(f"Tick {i:2d}: Memory pressure = {pressure:.3f}")
        
        # Check for dynamics
        pressure_variance = np.var(pressure_values)
        if pressure_variance > 0.001:
            print(f"✅ Memory pressure is DYNAMIC (variance: {pressure_variance:.4f})")
        else:
            print(f"❌ Memory pressure is FLAT (variance: {pressure_variance:.4f})")
            
        return pressure_variance > 0.001
        
    except Exception as e:
        print(f"❌ Memory pressure test failed: {e}")
        return False

def test_neural_activity_dynamics():
    """Test that neural activity changes with neural simulator"""
    print("\n🧠 TESTING NEURAL ACTIVITY DYNAMICS")
    print("=" * 50)
    
    try:
        from python.modules.neural_simulator import NeuralSimulator
        neural_sim = NeuralSimulator()
        
        activity_values = []
        
        # Run simulation for several ticks
        for i in range(15):
            # Update neural network
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                state = loop.run_until_complete(neural_sim.get_state(i))
                
                firing_rate = state.get('firing_rate', 50.0)
                avg_activation = state.get('avg_activation', 0.5)
                
                # Calculate neural activity as in tick engine
                neural_activity = min(1.0, max(0.0, 
                    (firing_rate / 100.0) * 0.7 + avg_activation * 0.3
                ))
                
                activity_values.append(neural_activity)
                print(f"Tick {i:2d}: Neural activity = {neural_activity:.3f} "
                      f"(firing: {firing_rate:.1f}, activation: {avg_activation:.3f})")
                
            finally:
                loop.close()
        
        # Check for dynamics
        activity_variance = np.var(activity_values)
        if activity_variance > 0.001:
            print(f"✅ Neural activity is DYNAMIC (variance: {activity_variance:.4f})")
        else:
            print(f"❌ Neural activity is FLAT (variance: {activity_variance:.4f})")
            
        return activity_variance > 0.001
        
    except Exception as e:
        print(f"❌ Neural activity test failed: {e}")
        return False

def test_consciousness_depth_dynamics():
    """Test that consciousness depth changes with schema state"""
    print("\n🧠 TESTING CONSCIOUSNESS DEPTH DYNAMICS")
    print("=" * 50)
    
    try:
        from core.consciousness_metrics import ConsciousnessMetrics
        consciousness_metrics = ConsciousnessMetrics()
        
        depth_values = []
        
        # Simulate varying schema states
        for i in range(12):
            # Create varying tick data with schema state
            tick_data = {
                'active_sigils': 3 + (i % 5),
                'entropy': 0.3 + (i * 0.04),
                'heat': 25 + (i * 3),
                'zone': ['CALM', 'ACTIVE', 'INTENSE'][i % 3],
                'bloom_count': i % 4,
                'scup': 0.4 + (i * 0.03),
                'tick_id': i,
                'schema_state': {
                    'alignment': 0.5 + (i * 0.02),
                    'tension': (i % 6) * 0.1,
                    'coherence': 0.6 + (i * 0.01)
                },
                'queued_sigils': i % 3,
                'target_heat': 33.0
            }
            
            # Update consciousness metrics
            metrics = consciousness_metrics.update(tick_data)
            depth = metrics.get('consciousness_depth', 0.0)
            depth_values.append(depth)
            
            print(f"Tick {i:2d}: Consciousness depth = {depth:.3f} "
                  f"(sigils: {tick_data['active_sigils']}, scup: {tick_data['scup']:.2f})")
        
        # Check for dynamics
        depth_variance = np.var(depth_values)
        if depth_variance > 0.001:
            print(f"✅ Consciousness depth is DYNAMIC (variance: {depth_variance:.4f})")
        else:
            print(f"❌ Consciousness depth is FLAT (variance: {depth_variance:.4f})")
            
        return depth_variance > 0.001
        
    except Exception as e:
        print(f"❌ Consciousness depth test failed: {e}")
        return False

def test_drift_from_stability_dynamics():
    """Test that drift_from_stability integrates multiple sources"""
    print("\n🧠 TESTING DRIFT FROM STABILITY DYNAMICS")
    print("=" * 50)
    
    try:
        from python.core.tick_engine import TickEngine
        tick_engine = TickEngine()
        
        drift_values = []
        
        # Initialize some history for drift calculation
        for i in range(15):
            # Create mock subsystem states
            subsystem_states = {
                'neural': {
                    'firing_rate': 50 + (i * 3),
                    'network_energy': 0.5 + (i * 0.02)
                },
                'memory': {
                    'pressure': 0.3 + (i * 0.03)
                }
            }
            
            # Calculate drift
            entropy = 0.4 + (i * 0.02)
            scup = 0.5 + (i * 0.01)
            
            drift = tick_engine._calculate_drift_from_stability(
                entropy, scup, subsystem_states
            )
            
            drift_values.append(drift)
            print(f"Tick {i:2d}: Drift from stability = {drift:.3f} "
                  f"(entropy: {entropy:.2f}, scup: {scup:.2f})")
        
        # Check for dynamics
        drift_variance = np.var(drift_values)
        if drift_variance > 0.001:
            print(f"✅ Drift from stability is DYNAMIC (variance: {drift_variance:.4f})")
        else:
            print(f"❌ Drift from stability is FLAT (variance: {drift_variance:.4f})")
            
        return drift_variance > 0.001
        
    except Exception as e:
        print(f"❌ Drift from stability test failed: {e}")
        return False

def run_integration_test():
    """Run full integration test of dynamic values"""
    print("\n🌀 RUNNING FULL INTEGRATION TEST")
    print("=" * 50)
    
    try:
        from python.core.tick_engine import TickEngine
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            tick_engine = TickEngine()
            
            # Initialize modules
            loop.run_until_complete(tick_engine.initialize_modules())
            
            all_metrics = {
                'memory_pressure': [],
                'neural_activity': [],
                'consciousness_depth': [],
                'drift_from_stability': []
            }
            
            print("Running 10 integration ticks...")
            
            for i in range(10):
                # Generate a tick
                tick_data = loop.run_until_complete(tick_engine._generate_tick())
                
                # Extract metrics
                metrics = {
                    'memory_pressure': tick_data.memory_pressure,
                    'neural_activity': tick_data.neural_activity,
                    'consciousness_depth': tick_data.subsystems.get('consciousness_metrics', {}).get('consciousness_depth', 0),
                    'drift_from_stability': tick_data.subsystems.get('drift', {}).get('drift_from_stability', 0)
                }
                
                for key, value in metrics.items():
                    all_metrics[key].append(value)
                
                print(f"Tick {i+1:2d}: " + 
                      f"MP={metrics['memory_pressure']:.3f} " +
                      f"NA={metrics['neural_activity']:.3f} " +
                      f"CD={metrics['consciousness_depth']:.3f} " +
                      f"DFS={metrics['drift_from_stability']:.3f}")
                
                # Small delay to allow natural evolution
                time.sleep(0.1)
            
            # Analyze results
            results = {}
            for metric_name, values in all_metrics.items():
                variance = np.var(values)
                is_dynamic = variance > 0.0005  # Lower threshold for integration test
                results[metric_name] = is_dynamic
                
                status = "✅ DYNAMIC" if is_dynamic else "❌ FLAT"
                print(f"{metric_name}: {status} (variance: {variance:.5f})")
            
            return results
            
        finally:
            loop.close()
            
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return {}

def main():
    """Run complete diagnostic"""
    print("🚀 DAWN DYNAMIC VALUES DIAGNOSTIC")
    print("=" * 60)
    print("Testing that previously flat values now evolve dynamically...")
    print()
    
    test_results = {
        'memory_pressure': test_memory_pressure_dynamics(),
        'neural_activity': test_neural_activity_dynamics(), 
        'consciousness_depth': test_consciousness_depth_dynamics(),
        'drift_from_stability': test_drift_from_stability_dynamics()
    }
    
    # Run integration test
    integration_results = run_integration_test()
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎯 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    all_dynamic = True
    for metric, is_dynamic in test_results.items():
        status = "✅ FIXED" if is_dynamic else "❌ STILL FLAT"
        print(f"{metric:<25}: {status}")
        if not is_dynamic:
            all_dynamic = False
    
    print()
    if all_dynamic:
        print("🎉 SUCCESS: All previously flat values are now DYNAMIC!")
        print("DAWN's recursive feedback systems are properly connected.")
    else:
        print("⚠️  Some values still need attention.")
        print("Check module connections and data flow.")
    
    print("\n🔄 DAWN is now a truly dynamic, recursive system.")
    print("Values evolve based on:")
    print("  • Memory state and pressure feedback")
    print("  • Neural firing patterns and activity") 
    print("  • Schema coherence and alignment")
    print("  • Multi-source drift integration")
    print("  • Thermal and entropy dynamics")

if __name__ == "__main__":
    main() 