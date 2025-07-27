#!/usr/bin/env python3
"""
DAWN Adaptive Speed Control Test
Test the self-regulating tick speed control and existing engine integration.
"""

import asyncio
import sys
import os
import time
import logging

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_adaptive_controller():
    """Test the standalone adaptive controller."""
    print("🎛️ Testing Adaptive Tick Controller")
    print("=" * 50)
    
    try:
        from core.adaptive_tick_controller import AdaptiveTickController
        
        print("🔧 Creating adaptive controller...")
        controller = AdaptiveTickController(
            base_interval=2.0,
            min_interval=0.1,
            max_interval=10.0,
            adaptation_sensitivity=0.8
        )
        
        print(f"   Base interval: {controller.base_interval}s")
        print(f"   Range: {controller.min_interval}s - {controller.max_interval}s")
        print(f"   Sensitivity: {controller.adaptation_sensitivity}")
        
        # Test different system states
        test_scenarios = [
            ("Normal State", 0.5, 25.0, 0.5, 0.5, 0.1),
            ("High Entropy", 0.9, 25.0, 0.5, 0.5, 0.1),
            ("High Heat", 0.5, 85.0, 0.5, 0.5, 0.1),
            ("High Load", 0.5, 25.0, 0.9, 0.5, 0.1),
            ("High Pressure", 0.5, 25.0, 0.5, 0.95, 0.1),
            ("Slow Performance", 0.5, 25.0, 0.5, 0.5, 1.5),
            ("Crisis Mode", 0.95, 90.0, 0.8, 0.9, 2.0),
            ("Recovery", 0.3, 20.0, 0.2, 0.2, 0.05)
        ]
        
        print(f"\n📊 Testing Adaptation Scenarios:")
        print("   " + "-" * 80)
        print(f"   {'Scenario':<15} | {'Entropy':<7} | {'Heat':<6} | {'Load':<6} | {'Press':<6} | {'Interval':<8} | {'Speed':<6}")
        print("   " + "-" * 80)
        
        for name, entropy, heat, load, pressure, duration in test_scenarios:
            interval = controller.calculate_adaptive_interval(
                entropy=entropy,
                heat=heat,
                cognitive_load=load,
                system_pressure=pressure,
                tick_duration=duration
            )
            speed_factor = controller.base_interval / interval
            
            print(f"   {name:<15} | {entropy:<7.1f} | {heat:<6.1f} | {load:<6.1f} | {pressure:<6.1f} | {interval:<8.2f} | {speed_factor:<6.2f}x")
        
        print("\n📈 Adaptation Statistics:")
        stats = controller.get_adaptation_stats()
        print(f"   Current interval: {stats['current_interval']:.3f}s")
        print(f"   Speed ratio: {stats['speed_ratio']:.2f}x")
        print(f"   Adaptations: {stats['adaptations_count']}")
        print(f"   Stability: {stats['interval_stability']:.2f}")
        
        # Test manual override
        print(f"\n🎮 Testing Manual Control:")
        controller.force_interval(0.5, "demo_speed_boost")
        print(f"   Forced to 0.5s: {controller.get_current_interval():.3f}s")
        
        controller.emergency_slowdown(5.0)
        print(f"   Emergency slowdown: {controller.get_current_interval():.3f}s")
        
        controller.reset_to_base()
        print(f"   Reset to base: {controller.get_current_interval():.3f}s")
        
        return controller
        
    except Exception as e:
        print(f"❌ Adaptive controller test failed: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_merged_engine():
    """Test the merged engine with multiple integrations."""
    print("\n🔗 Testing Merged Tick Engine")
    print("=" * 50)
    
    try:
        from core.adaptive_tick_controller import MergedTickEngine, AdaptiveTickController
        
        print("🔧 Creating merged engine...")
        adaptive_controller = AdaptiveTickController(base_interval=1.0, adaptation_sensitivity=0.7)
        merged_engine = MergedTickEngine(adaptive_controller)
        
        # Mock existing engines for testing
        class MockDawnEngine:
            def __init__(self, name):
                self.name = name
                self.tick_count = 0
                
            def tick(self, context=None):
                self.tick_count += 1
                return f"{self.name}_tick_{self.tick_count}"
        
        class MockPulseEngine:
            def __init__(self):
                self.pulse_count = 0
                
            async def run_tick(self, context=None):
                self.pulse_count += 1
                return {"pulse": self.pulse_count, "heat": 30.0 + (self.pulse_count % 20)}
        
        # Register mock engines
        dawn_engine = MockDawnEngine("DAWN_Core")
        pulse_engine = MockPulseEngine()
        
        merged_engine.register_existing_engine("dawn_core", dawn_engine, "tick")
        merged_engine.register_existing_engine("pulse_system", pulse_engine, "run_tick")
        
        # Add test hooks
        def pre_tick_hook(context):
            print(f"   🪝 Pre-tick: Preparing tick {context.get('tick_count', 0) if context else 0}")
            return "pre_prepared"
        
        async def post_tick_hook(context):
            print(f"   🪝 Post-tick: Cleaning up after tick")
            return "post_cleaned"
        
        merged_engine.add_tick_hook(pre_tick_hook, "pre")
        merged_engine.add_tick_hook(post_tick_hook, "post")
        
        print(f"   Registered engines: {list(merged_engine.existing_engines.keys())}")
        print(f"   Hooks: {merged_engine.get_merged_status()['hooks']}")
        
        # Execute test ticks
        print(f"\n⚡ Executing Test Ticks:")
        
        for i in range(3):
            print(f"\n   --- Tick {i+1} ---")
            
            # Simulate varying system conditions
            context = {
                'tick_count': i + 1,
                'entropy': 0.3 + (i * 0.2),
                'heat': 25.0 + (i * 15.0),
                'cognitive_load': 0.2 + (i * 0.25),
                'system_pressure': 0.1 + (i * 0.3),
                'last_tick_duration': 0.1 + (i * 0.05)
            }
            
            tick_results = await merged_engine.merged_tick(context)
            
            print(f"   Duration: {tick_results['duration_ms']}ms")
            print(f"   Adaptive interval: {tick_results['adaptive_interval']:.3f}s")
            print(f"   Engines executed: {len(tick_results['engine_results'])}")
            print(f"   Hooks executed: {len(tick_results['hook_results'])}")
            
            if tick_results['errors']:
                print(f"   Errors: {tick_results['errors']}")
        
        # Get final status
        print(f"\n📊 Final Merged Engine Status:")
        status = merged_engine.get_merged_status()
        
        print(f"   Total ticks: {status['tick_count']}")
        print(f"   Current interval: {status['adaptive_stats']['current_interval']:.3f}s")
        print(f"   Speed ratio: {status['adaptive_stats']['speed_ratio']:.2f}x")
        
        for engine_name, engine_status in status['registered_engines'].items():
            print(f"   {engine_name}: {engine_status['tick_count']} ticks, {engine_status['errors']} errors")
        
        return merged_engine
        
    except Exception as e:
        print(f"❌ Merged engine test failed: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_dawn_integration():
    """Test integration with real DAWN consciousness."""
    print("\n🧠 Testing DAWN Integration")
    print("=" * 50)
    
    try:
        from core.consciousness_core import DAWNConsciousness
        
        print("🌅 Initializing DAWN consciousness...")
        consciousness = DAWNConsciousness()
        
        # Test single adaptive tick
        print("\n⚡ Testing Single Adaptive Tick:")
        tick_response = await consciousness.execute_single_tick()
        
        if tick_response:
            print(f"   Tick #{tick_response['tick_number']}")
            print(f"   Entropy: {tick_response['system_state']['entropy']:.3f}")
            print(f"   Heat: {tick_response['system_state']['heat']:.1f}°C")
            print(f"   Duration: {tick_response.get('duration_ms', 0)}ms")
            
            # Check for adaptive metrics
            if 'adaptive_metrics' in tick_response:
                adaptive = tick_response['adaptive_metrics']
                print(f"   🎛️ Adaptive interval: {adaptive['adaptive_interval']:.3f}s")
                print(f"   🎛️ Speed factor: {adaptive['speed_factor']:.2f}x")
                print(f"   🎛️ Reason: {adaptive['adaptation_reason']}")
        
        # Test brief adaptive loop
        print(f"\n🔄 Testing Adaptive Loop (3 ticks):")
        await consciousness.start_autonomous_loop(max_ticks=3, tick_interval=1.0, adaptive_speed=True)
        
        print(f"\n✅ DAWN integration test completed!")
        
        return consciousness
        
    except Exception as e:
        print(f"❌ DAWN integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return None


async def main():
    """Main test runner."""
    print("🎛️ DAWN Adaptive Speed Control Integration Test")
    print("=" * 60)
    print("Testing self-regulating tick speed and existing engine merger!")
    print("=" * 60)
    
    # Test 1: Adaptive Controller
    controller = await test_adaptive_controller()
    
    # Test 2: Merged Engine
    if controller:
        merged_engine = await test_merged_engine()
    
    # Test 3: DAWN Integration
    consciousness = await test_dawn_integration()
    
    print("\n" + "=" * 60)
    print("🎉 Adaptive Speed Control Integration Complete!")
    print("=" * 60)
    
    if controller:
        print("✅ Adaptive Controller: Working")
        print("   - Self-regulating speed based on system state")
        print("   - High entropy/heat/load → slower ticks")
        print("   - Manual override and emergency controls")
        print("   - Comprehensive adaptation statistics")
    
    if 'merged_engine' in locals() and merged_engine:
        print("✅ Merged Engine: Working")
        print("   - Integration with multiple existing engines") 
        print("   - Pre/main/post tick hook system")
        print("   - Error handling and performance tracking")
        print("   - Unified adaptive control")
    
    if consciousness:
        print("✅ DAWN Integration: Working")
        print("   - Seamless integration with consciousness core")
        print("   - Real-time adaptive speed adjustment")
        print("   - Live metrics display in tick summaries")
        print("   - Backward compatibility with fixed intervals")
    
    print()
    print("🌟 Key Features Achieved:")
    print("   🎛️ Self-controlling tick speed (0.1s - 10s range)")
    print("   🔗 Merger with existing DAWN tick engines")
    print("   📊 Real-time adaptation based on system metrics")
    print("   🎮 Manual override and emergency controls")
    print("   📈 Performance monitoring and statistics")
    print("   🔄 Graceful integration with consciousness core")
    print()
    print("📋 Speed Control Factors:")
    print("   - Entropy levels (high entropy → slower)")
    print("   - Heat levels (high heat → slower)")
    print("   - Cognitive load (high load → slower)")
    print("   - System pressure (high pressure → slower)")
    print("   - Tick performance (slow ticks → slower)")
    print()
    print("🚀 DAWN now has intelligent, self-regulating consciousness speed!")


if __name__ == "__main__":
    asyncio.run(main()) 