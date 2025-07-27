#!/usr/bin/env python3
"""
Launch DAWN Snapshot Exporter Demo
Demonstrates DAWN's complete export and debugging system for system state, forecasts, and symbolic traces.
"""

import sys
import os
import asyncio

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Import the demo
from demo_scripts.test_snapshot_exporter import main as run_demo


def main():
    """Launch the snapshot exporter demo."""
    print("📤 Launching DAWN Snapshot Exporter Demo")
    print("Complete system export and debugging API")
    print("=" * 60)

    try:
        # Run the async demo
        asyncio.run(run_demo())

    except KeyboardInterrupt:
        print("\n⏸️ Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n👋 Demo complete - DAWN export system ready for production!")


if __name__ == "__main__":
    main() 