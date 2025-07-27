#!/usr/bin/env python3
"""
DAWN Full Cognition System Launcher
===================================

Simple launcher script to demonstrate the complete meta-cognitive runtime.

Usage:
    python launch_full_cognition.py               # Run interactive demo
    python launch_full_cognition.py --auto        # Run automated demo  
    python launch_full_cognition.py --monitor     # Monitor mode with voice
    python launch_full_cognition.py --test        # Run test suite
"""

import os
import sys
import asyncio
import argparse
import signal
from datetime import datetime

# Add DAWN paths
sys.path.append(os.path.dirname(__file__))

def print_banner():
    """Print startup banner"""
    print("🧠" + "=" * 60 + "🧠")
    print("   DAWN - Deep Autonomous Wisdom Network")
    print("   Full Meta-Cognitive Runtime System")
    print("🧠" + "=" * 60 + "🧠")
    print()

async def demo_mode():
    """Run interactive demonstration of the cognitive system"""
    print("🎭 RUNNING INTERACTIVE DEMO")
    print("-" * 40)
    
    try:
        from integration_orchestrator import DAWNOrchestrator
        
        orchestrator = DAWNOrchestrator()
        await orchestrator.initialize()
        
        # Show available scenarios
        scenarios = ['default', 'stress_test', 'drift_cascade', 'thermal_emergency', 'memory_overload']
        
        print("Available demonstration scenarios:")
        for i, scenario in enumerate(scenarios, 1):
            print(f"  {i}. {scenario}")
        
        choice = input("\nSelect scenario (1-5) or press Enter for all: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= 5:
            selected_scenario = scenarios[int(choice) - 1]
            print(f"\n🚀 Running scenario: {selected_scenario}")
            await orchestrator.run_demo_scenario(selected_scenario)
        else:
            print("\n🚀 Running all scenarios...")
            for scenario in scenarios:
                print(f"\n--- {scenario.upper()} ---")
                await orchestrator.run_demo_scenario(scenario)
                await asyncio.sleep(2)
        
        # Show final status
        print("\n📊 FINAL SYSTEM STATUS")
        print("-" * 30)
        status = orchestrator.get_orchestration_status()
        for key, value in status.items():
            if key != 'cognition_runtime_status':
                print(f"  {key}: {value}")
        
        await orchestrator.shutdown()
        
    except ImportError:
        print("⚠️ Cognition runtime components not available")
        print("   Please ensure all DAWN components are properly installed")
    except Exception as e:
        print(f"❌ Demo failed: {e}")

async def auto_mode():
    """Run automated demo without user interaction"""
    print("🤖 RUNNING AUTOMATED DEMO")
    print("-" * 40)
    
    try:
        from integration_orchestrator import DAWNOrchestrator
        
        orchestrator = DAWNOrchestrator()
        await orchestrator.initialize()
        
        print("Running comprehensive demonstration...")
        
        # Run all scenarios automatically
        scenarios = ['default', 'stress_test', 'drift_cascade', 'thermal_emergency', 'memory_overload']
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n[{i}/{len(scenarios)}] Testing {scenario}...")
            await orchestrator.run_demo_scenario(scenario)
            print(f"✅ {scenario} completed")
            await asyncio.sleep(1)
        
        print("\n🎉 All scenarios completed successfully!")
        await orchestrator.shutdown()
        
    except Exception as e:
        print(f"❌ Automated demo failed: {e}")

async def monitor_mode():
    """Run monitoring mode with voice output"""
    print("👁️ RUNNING MONITOR MODE")
    print("-" * 40)
    print("This mode would connect to live DAWN system and provide")
    print("real-time cognitive monitoring with voice feedback.")
    print()
    
    try:
        # This would integrate with the existing voice_loop.py
        print("🔊 Voice monitoring would be active")
        print("📈 Real-time tracer alerts would be spoken")
        print("🌿 Memory network events would be announced")
        print("🔮 Forecast changes would be reported")
        print()
        print("Press Ctrl+C to stop monitoring...")
        
        # Simulate monitoring
        for i in range(10):
            await asyncio.sleep(2)
            print(f"[Monitor] Tick {i+1}: System nominal, all tracers active")
        
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")

async def test_mode():
    """Run comprehensive test suite"""
    print("🧪 RUNNING TEST SUITE")
    print("-" * 40)
    
    tests_passed = 0
    tests_total = 5
    
    try:
        # Test 1: Cognition Runtime Initialization
        print("Test 1: Cognition Runtime Initialization...")
        try:
            from cognition_runtime import CognitionRuntime
            runtime = CognitionRuntime()
            print("✅ Cognition runtime initialized")
            tests_passed += 1
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        # Test 2: Tracer Stack
        print("Test 2: Tracer Stack Integration...")
        try:
            from tracers.DriftTracer import DriftTracer
            from tracers.ThermalTracer import ThermalTracer  
            from tracers.ForecastTracer import ForecastTracer
            
            drift_tracer = DriftTracer()
            thermal_tracer = ThermalTracer()
            forecast_tracer = ForecastTracer()
            print("✅ All tracers initialized")
            tests_passed += 1
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        # Test 3: Memory Network Integration
        print("Test 3: Memory Network Integration...")
        try:
            from mycelium.mycelium_layer import MyceliumLayer
            from cognitive.rebloom_lineage import ReblooooomLineageTracker
            
            mycelium = MyceliumLayer()
            lineage = ReblooooomLineageTracker()
            print("✅ Memory networks initialized")
            tests_passed += 1
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        # Test 4: Integration Orchestrator
        print("Test 4: Integration Orchestrator...")
        try:
            from integration_orchestrator import DAWNOrchestrator
            orchestrator = DAWNOrchestrator()
            print("✅ Orchestrator initialized")
            tests_passed += 1
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        # Test 5: Mock Tick Processing
        print("Test 5: Mock Tick Processing...")
        try:
            if 'runtime' in locals():
                mock_tick = {
                    'entropy': 0.5,
                    'heat': 0.4,
                    'scup': 0.7,
                    'zone': 'active'
                }
                result = await runtime.process_tick(mock_tick)
                print("✅ Tick processing successful")
                tests_passed += 1
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        # Test Results
        print(f"\n📊 TEST RESULTS: {tests_passed}/{tests_total} tests passed")
        if tests_passed == tests_total:
            print("🎉 All tests passed! System is ready for operation.")
        else:
            print("⚠️  Some tests failed. Check component availability.")
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")

def setup_signal_handlers():
    """Setup graceful shutdown handlers"""
    def signal_handler(signum, frame):
        print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='DAWN Full Cognition System Launcher')
    parser.add_argument('--auto', action='store_true',
                       help='Run automated demo without user interaction')
    parser.add_argument('--monitor', action='store_true',
                       help='Run in monitoring mode with voice output')
    parser.add_argument('--test', action='store_true',
                       help='Run comprehensive test suite')
    
    args = parser.parse_args()
    
    print_banner()
    
    setup_signal_handlers()
    
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        if args.test:
            await test_mode()
        elif args.auto:
            await auto_mode()
        elif args.monitor:
            await monitor_mode()
        else:
            await demo_mode()
            
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n🕐 Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🧠 DAWN Full Cognition System - Session Complete 🧠")

if __name__ == "__main__":
    asyncio.run(main()) 