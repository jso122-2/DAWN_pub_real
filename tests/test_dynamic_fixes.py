#!/usr/bin/env python3
"""
DAWN Dynamic Values Test
======================
Quick test to verify flat metrics are now dynamic and responsive.
"""

import asyncio
import numpy as np
import time

def test_memory_pressure():
    """Test memory pressure responds to rebloom queue and drift"""
    print("🧠 Testing Memory Pressure...")
    
    try:
        from python.modules.memory_manager import MemoryManager
        memory_mgr = MemoryManager()
        
        # Add fragments to increase base pressure
        for i in range(5):
            memory_mgr.short_term_memory.append(f'fragment_{i}')
        
        # Test with varying consolidation events (simulates rebloom queue)
        pressures = []
        for i in range(8):
            # Simulate rebloom queue growth
            if hasattr(memory_mgr, 'consolidation_events'):
                memory_mgr.consolidation_events.extend([{'test': j} for j in range(i)])
            
            pressure = memory_mgr._calculate_memory_pressure()
            pressures.append(pressure)
            print(f"  Tick {i}: pressure = {pressure:.3f}")
        
        variance = np.var(pressures)
        print(f"  Variance: {variance:.4f} {'✅ DYNAMIC' if variance > 0.001 else '❌ FLAT'}")
        return variance > 0.001
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_neural_activity():
    """Test neural activity responds to SCUP/entropy/mood"""
    print("\n🧠 Testing Neural Activity...")
    
    try:
        from python.modules.neural_simulator import NeuralSimulator
        neural_sim = NeuralSimulator()
        
        activities = []
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            for i in range(6):
                # Simulate different SCUP/entropy/mood states by varying tick number
                state = loop.run_until_complete(neural_sim.get_state(i * 5))
                
                firing_rate = state.get('firing_rate', 50.0)
                avg_activation = state.get('avg_activation', 0.5)
                activity = (firing_rate / 100.0) * 0.7 + avg_activation * 0.3
                
                activities.append(activity)
                print(f"  Tick {i}: activity = {activity:.3f} (firing: {firing_rate:.1f})")
        
        finally:
            loop.close()
        
        variance = np.var(activities)
        print(f"  Variance: {variance:.4f} {'✅ DYNAMIC' if variance > 0.001 else '❌ FLAT'}")
        return variance > 0.001
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_consciousness_depth():
    """Test consciousness depth reflects schema stack and recursive observation"""
    print("\n🧠 Testing Consciousness Depth...")
    
    try:
        from core.consciousness_metrics import ConsciousnessMetrics
        consciousness_metrics = ConsciousnessMetrics()
        
        depths = []
        
        for i in range(7):
            # Vary schema state to test responsiveness
            tick_data = {
                'active_sigils': 2 + (i % 4),
                'entropy': 0.2 + (i * 0.08),
                'heat': 30 + (i * 5),
                'zone': ['CALM', 'ACTIVE', 'INTENSE'][i % 3],
                'bloom_count': i % 3,
                'scup': 0.3 + (i * 0.07),
                'tick_id': i,
                'schema_state': {
                    'alignment': 0.4 + (i * 0.05),
                    'tension': (i % 5) * 0.15,
                    'coherence': 0.5 + (i * 0.04),
                    'breathing_phase': (i * 0.2) % 1.0
                }
            }
            
            metrics = consciousness_metrics.update(tick_data)
            depth = metrics.get('consciousness_depth', 0.0)
            depths.append(depth)
            
            print(f"  Tick {i}: depth = {depth:.3f} (tension: {tick_data['schema_state']['tension']:.2f})")
        
        variance = np.var(depths)
        print(f"  Variance: {variance:.4f} {'✅ DYNAMIC' if variance > 0.001 else '❌ FLAT'}")
        return variance > 0.001
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_drift_from_stability():
    """Test drift tracks semantic tension"""
    print("\n🧠 Testing Drift from Stability...")
    
    try:
        from python.core.tick_engine import TickEngine
        from python.core.tick_engine import TickData
        
        tick_engine = TickEngine()
        
        # Create mock tick history for drift calculation
        mock_ticks = []
        for i in range(8):
            # Vary SCUP and entropy to create semantic tension
            scup = 0.3 + (i * 0.08)
            entropy = 0.6 - (i * 0.05)  # Diverging from SCUP
            
            mock_tick = TickData(
                tick_number=i,
                timestamp=time.time() + i,
                scup=scup,
                entropy=entropy,
                mood=f"mood_{i%3}",
                neural_activity=0.4 + (i * 0.03),
                consciousness_unity=0.5,
                memory_pressure=0.3,
                active_processes=[],
                subsystems={}
            )
            mock_ticks.append(mock_tick)
        
        tick_engine.tick_history.extend(mock_ticks)
        
        drifts = []
        
        for i in range(5):
            # Calculate drift with varying conditions
            entropy = 0.4 + (i * 0.1)
            scup = 0.6 - (i * 0.05)  # Creating divergence = semantic tension
            
            subsystem_states = {
                'neural': {'firing_rate': 50 + (i * 5)},
                'memory': {'pressure': 0.3 + (i * 0.05)}
            }
            
            drift = tick_engine._calculate_drift_from_stability(entropy, scup, subsystem_states)
            drifts.append(drift)
            
            print(f"  Tick {i}: drift = {drift:.3f} (scup: {scup:.2f}, entropy: {entropy:.2f})")
        
        variance = np.var(drifts)
        print(f"  Variance: {variance:.4f} {'✅ DYNAMIC' if variance > 0.001 else '❌ FLAT'}")
        return variance > 0.001
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🔧 DAWN DYNAMIC VALUES VERIFICATION")
    print("=" * 50)
    
    results = {
        'memory_pressure': test_memory_pressure(),
        'neural_activity': test_neural_activity(),
        'consciousness_depth': test_consciousness_depth(),
        'drift_from_stability': test_drift_from_stability()
    }
    
    print("\n" + "=" * 50)
    print("📊 RESULTS SUMMARY")
    print("=" * 50)
    
    all_fixed = True
    for metric, is_dynamic in results.items():
        status = "✅ FIXED" if is_dynamic else "❌ STILL FLAT"
        print(f"{metric:<20}: {status}")
        if not is_dynamic:
            all_fixed = False
    
    print("\n" + "=" * 50)
    if all_fixed:
        print("🎉 SUCCESS: All metrics are now DYNAMIC!")
        print("DAWN responds to internal state changes.")
    else:
        print("⚠️  Some metrics need more work.")
    
    print("\n🌀 Fixed Logic:")
    print("• memory_pressure: Rebloom queue + drift accumulation")
    print("• consciousness_depth: Schema stack + recursive observation") 
    print("• neural_activity: SCUP drive + entropy chaos + mood spikes")
    print("• drift_from_stability: Semantic tension (40% weight)")

if __name__ == "__main__":
    main() 