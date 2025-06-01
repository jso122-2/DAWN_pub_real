"""
Launch script for DAWN Unified Tick Engine
Demonstrates standalone and integrated operation modes
"""

import asyncio
import argparse
import sys
import os
import json
from typing import Optional

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the unified tick engine
from core.unified_tick_engine import create_unified_tick_engine, UnifiedTickEngine


class MockSensors:
    """Mock sensor implementations for testing"""
    
    def __init__(self):
        self.tick_count = 0
        self.base_activity = 0.5
        self.base_pressure = 0.0
        self.base_mood = 0.0
    
    async def activity_sensor(self) -> float:
        """Simulate activity with some variation"""
        # Add sine wave variation
        import math
        variation = math.sin(self.tick_count * 0.1) * 0.2
        return max(0, min(1, self.base_activity + variation))
    
    async def pressure_sensor(self) -> float:
        """Simulate pressure that builds over time"""
        # Pressure builds slowly then releases
        cycle_position = (self.tick_count % 100) / 100.0
        if cycle_position < 0.7:
            pressure = cycle_position * 0.8
        else:
            pressure = 0.8 * (1 - (cycle_position - 0.7) / 0.3)
        return max(0, min(1, self.base_pressure + pressure))
    
    async def mood_sensor(self) -> float:
        """Simulate mood swings"""
        import math
        # Mood swings on a longer cycle
        mood = math.sin(self.tick_count * 0.05) * 0.5 + 0.5
        return max(0, min(1, self.base_mood + mood))


class UnifiedEngineRunner:
    """Runner class for the unified tick engine"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "tick_engine_config.json"
        self.engine: Optional[UnifiedTickEngine] = None
        self.sensors = MockSensors()
        self.visualization_enabled = False
        
    def load_config(self) -> dict:
        """Load configuration from file"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file {self.config_path} not found, using defaults")
            return {}
    
    async def run_standalone(self, 
                           base_interval: float = 1.0,
                           max_ticks: Optional[int] = None,
                           enable_narrative: bool = True):
        """Run engine in standalone mode with mock sensors"""
        print("=" * 60)
        print("DAWN Unified Tick Engine - Standalone Mode")
        print("=" * 60)
        print(f"Base interval: {base_interval}s")
        print(f"Max ticks: {max_ticks or 'unlimited'}")
        print(f"Narrative: {'enabled' if enable_narrative else 'disabled'}")
        print("=" * 60)
        
        # Create engine with mock sensors
        self.engine = create_unified_tick_engine(
            base_interval=base_interval,
            activity_sensor=self.sensors.activity_sensor,
            pressure_sensor=self.sensors.pressure_sensor,
            mood_sensor=self.sensors.mood_sensor,
            enable_narrative=enable_narrative
        )
        
        # Start engine in background
        engine_task = asyncio.create_task(self.engine.start())
        
        try:
            # Run for specified ticks or until interrupted
            tick_count = 0
            while not max_ticks or tick_count < max_ticks:
                await asyncio.sleep(1)
                tick_count += 1
                self.sensors.tick_count = tick_count
                
                # Print status every 10 ticks
                if tick_count % 10 == 0:
                    stats = self.engine.get_engine_stats()
                    print(f"\n[Status] Tick {tick_count}")
                    print(f"  Zone: {stats['current_zone']}")
                    print(f"  SCUP trend: {[f'{s:.2f}' for s in stats['scup_trend'][-5:]]}")
                    print(f"  Entropy trend: {[f'{e:.2f}' for e in stats['entropy_trend'][-5:]]}")
                    
                    exp_state = stats['experimental_state']
                    print(f"  Stasis heat: {exp_state['stasis_heat']:.3f}")
                    print(f"  Drift: {exp_state['drift_magnitude']:.3f}")
                    print(f"  Cascade risk: {exp_state['cascade_risk']:.3f}")
                
        except KeyboardInterrupt:
            print("\n[Runner] Interrupted by user")
        finally:
            # Stop engine
            self.engine.stop()
            engine_task.cancel()
            try:
                await engine_task
            except asyncio.CancelledError:
                pass
    
    async def run_integrated(self, visualization_port: int = 8000):
        """Run engine with visualization bridge"""
        print("=" * 60)
        print("DAWN Unified Tick Engine - Integrated Mode")
        print("=" * 60)
        print(f"Visualization port: {visualization_port}")
        print("=" * 60)
        
        try:
            # Import visualization bridge
            from visualization_bridge import DAWNVisualizationBridge
            
            # Create bridge
            bridge = DAWNVisualizationBridge(port=visualization_port)
            bridge.start_local_server()
            
            # Create engine with visualization hooks
            self.engine = create_unified_tick_engine(
                activity_sensor=self.sensors.activity_sensor,
                pressure_sensor=self.sensors.pressure_sensor,
                mood_sensor=self.sensors.mood_sensor,
                enable_narrative=True
            )
            
            # Hook into engine for visualization updates
            original_save_state = self.engine._save_state
            
            def enhanced_save_state():
                # Call original
                original_save_state()
                
                # Update visualization
                state = self.engine.state
                bridge.update_visualization({
                    "blooms": [
                        {
                            "id": i,
                            "x": 200 + (i * 30) % 600,
                            "y": 200 + (i // 20) * 30,
                            "heat": state.pulse_heat,
                            "entropy": state.entropy,
                            "mood": state.valence
                        }
                        for i in range(min(state.tick, 50))
                    ],
                    "metrics": {
                        "entropy": state.entropy,
                        "coherence": state.scup,
                        "heat": state.pulse_heat,
                        "mood": state.valence,
                        "drift": state.drift_magnitude,
                        "cascade_risk": state.cascade_risk,
                        "tick": state.tick
                    },
                    "zone": state.current_zone,
                    "narrative": list(self.engine.narrative_history)[-5:]
                })
            
            self.engine._save_state = enhanced_save_state
            
            # Run engine
            await self.run_standalone(enable_narrative=True)
            
        except ImportError:
            print("Visualization bridge not found. Running without visualization.")
            await self.run_standalone()
    
    async def run_test_sequence(self):
        """Run a test sequence demonstrating all features"""
        print("=" * 60)
        print("DAWN Unified Tick Engine - Test Sequence")
        print("=" * 60)
        
        self.engine = create_unified_tick_engine(
            base_interval=0.5,  # Faster for testing
            activity_sensor=self.sensors.activity_sensor,
            pressure_sensor=self.sensors.pressure_sensor,
            mood_sensor=self.sensors.mood_sensor,
            enable_narrative=True
        )
        
        # Start engine
        engine_task = asyncio.create_task(self.engine.start())
        
        try:
            print("\n[Test 1] Normal operation - 20 ticks")
            for i in range(20):
                await asyncio.sleep(0.5)
                self.sensors.tick_count = i
            
            print("\n[Test 2] High pressure scenario")
            self.sensors.base_pressure = 0.7
            for i in range(20, 40):
                await asyncio.sleep(0.5)
                self.sensors.tick_count = i
            
            print("\n[Test 3] Emotional volatility")
            self.sensors.base_mood = -0.5
            self.sensors.base_activity = 0.8
            for i in range(40, 60):
                await asyncio.sleep(0.5)
                self.sensors.tick_count = i
            
            print("\n[Test 4] Return to baseline")
            self.sensors.base_pressure = 0.0
            self.sensors.base_mood = 0.0
            self.sensors.base_activity = 0.5
            for i in range(60, 80):
                await asyncio.sleep(0.5)
                self.sensors.tick_count = i
            
            # Final report
            print("\n" + "=" * 60)
            print("Test Sequence Complete - Final Report")
            print("=" * 60)
            
            stats = self.engine.get_engine_stats()
            exp_state = stats['experimental_state']
            
            print(f"Total ticks: {stats['tick_count']}")
            print(f"Final zone: {stats['current_zone']}")
            print(f"Rebloom count: {exp_state['rebloom_count']}")
            print(f"Max cascade risk: {max(self.engine.state.cascade_risk, exp_state['cascade_risk']):.3f}")
            print(f"Zone transitions: {len(self.engine.zone_transitions)}")
            
            # Read narrative log
            try:
                with open("cognitive_states/narrative_log.txt", "r") as f:
                    lines = f.readlines()
                    print("\nRecent narrative entries:")
                    for line in lines[-10:]:
                        print(f"  {line.strip()}")
            except:
                pass
                
        finally:
            self.engine.stop()
            engine_task.cancel()
            try:
                await engine_task
            except asyncio.CancelledError:
                pass


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='DAWN Unified Tick Engine Launcher')
    parser.add_argument('--mode', choices=['standalone', 'integrated', 'test'], 
                       default='standalone', help='Running mode')
    parser.add_argument('--interval', type=float, default=1.0, 
                       help='Base tick interval in seconds')
    parser.add_argument('--max-ticks', type=int, help='Maximum number of ticks')
    parser.add_argument('--no-narrative', action='store_true', 
                       help='Disable narrative engine')
    parser.add_argument('--config', type=str, help='Path to config file')
    parser.add_argument('--viz-port', type=int, default=8000, 
                       help='Visualization server port')
    
    args = parser.parse_args()
    
    # Create runner
    runner = UnifiedEngineRunner(config_path=args.config)
    
    # Run based on mode
    if args.mode == 'standalone':
        await runner.run_standalone(
            base_interval=args.interval,
            max_ticks=args.max_ticks,
            enable_narrative=not args.no_narrative
        )
    elif args.mode == 'integrated':
        await runner.run_integrated(visualization_port=args.viz_port)
    elif args.mode == 'test':
        await runner.run_test_sequence()


if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("cognitive_states", exist_ok=True)
    os.makedirs("juliet_flowers/cluster_report", exist_ok=True)
    
    # Run main
    asyncio.run(main())