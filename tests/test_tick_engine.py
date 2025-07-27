#!/usr/bin/env python3
"""
Interactive test for DAWN's tick engine
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.unified_tick_engine import tick_engine
from core.unified_tick_engine import register_handler, unregister_handler


class TickMonitor:
    """Monitor tick engine activity"""
    
    def __init__(self):
        self.tick_count = 0
        self.last_scup = 0.0
        self.claude_triggers = 0
        
    async def on_tick(self, data: dict):
        """Handle tick events"""
        self.tick_count += 1
        self.last_scup = data.get('scup', 0.0)
        
        # Clear screen for clean display (optional)
        if os.name == 'posix':
            os.system('clear')
        
        print("🌅 DAWN TICK ENGINE - LIVE MONITOR")
        print("=" * 50)
        print(f"Tick:     {data['tick']}")
        print(f"Uptime:   {data['uptime']:.1f}s")
        print(f"SCUP:     {data['scup']:.3f} {'⚡' if data['scup'] > 0.8 else ''}")
        print(f"Mood:     {data['mood']}")
        print(f"Entropy:  {data['entropy']:.3f}")
        print("-" * 50)
        
        # Show subsystem states
        for subsystem in ['pulse', 'schema', 'memory', 'visual']:
            state = data.get(f'{subsystem}_state', {})
            if state:
                print(f"{subsystem.upper()}:")
                for key, value in state.items():
                    if isinstance(value, float):
                        print(f"  {key}: {value:.3f}")
                    else:
                        print(f"  {key}: {value}")
        
        print("-" * 50)
        print(f"Claude Triggers: {self.claude_triggers}")
        print("\nPress Ctrl+C to stop")
        
    async def on_claude_query(self, data: dict):
        """Handle Claude query events"""
        self.claude_triggers += 1
        print("\n" + "🧠" * 20)
        print(f"CLAUDE QUERY TRIGGERED! (#{self.claude_triggers})")
        print(f"SCUP Level: {data['scup']:.3f}")
        print("🧠" * 20 + "\n")
        await asyncio.sleep(2)  # Pause to show the message


async def run_test():
    """Run interactive test"""
    print("🚀 Starting DAWN Tick Engine Test")
    print("This will run the engine with live monitoring")
    print("-" * 50)
    
    # Create monitor
    monitor = TickMonitor()
    
    # Register listeners
    register_handler("tick_complete", monitor.on_tick)
    register_handler("claude_query_needed", monitor.on_claude_query)
    
    # Create tasks for testing
    async def scup_simulator():
        """Gradually increase SCUP to trigger Claude"""
        await asyncio.sleep(5)
        print("\n📈 Starting SCUP simulation...")
        
        # Gradually increase SCUP
        for i in range(10):
            current_scup = 0.7 + (i * 0.03)
            # This would normally be set by the schema subsystem
            # but we can simulate it for testing
            await asyncio.sleep(2)
    
    # Start SCUP simulator
    asyncio.create_task(scup_simulator())
    
    # Optional: Stop after 30 seconds
    async def auto_stop():
        await asyncio.sleep(30)
        print("\n⏰ Auto-stop after 30 seconds")
        await tick_engine.stop()
    
    # Uncomment to enable auto-stop
    # asyncio.create_task(auto_stop())
    
    try:
        # Start engine
        await tick_engine.start()
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    finally:
        await tick_engine.stop()
        print(f"\n📊 Final Statistics:")
        print(f"   Total Ticks: {monitor.tick_count}")
        print(f"   Claude Triggers: {monitor.claude_triggers}")
        print(f"   Final SCUP: {monitor.last_scup:.3f}")
        print("\n✅ Test completed!")


if __name__ == "__main__":
    asyncio.run(run_test()) 