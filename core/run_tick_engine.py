#!/usr/bin/env python3
"""
Main runner for DAWN's tick engine
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.unified_tick_engine import tick_engine


async def main():
    """Run the tick engine"""
    print("🌅 DAWN Tick Engine Starting...")
    print("=" * 50)
    
    # Check for config file
    config_path = "config/tick_config.yaml"
    if not os.path.exists(config_path):
        print(f"⚠️  Config file not found at {config_path}")
        print("   Using default configuration")
        config_path = None
    
    try:
        await tick_engine.start()
    except KeyboardInterrupt:
        print("\n⚠️  Shutdown requested")
    except Exception as e:
        print(f"\n❌ Engine error: {e}")
        raise
    finally:
        await tick_engine.stop()
        print("\n✅ DAWN Tick Engine stopped")


if __name__ == "__main__":
    # Run with asyncio
    asyncio.run(main()) 