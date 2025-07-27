#!/usr/bin/env python3
"""
Launch Symbolic Anatomy Demo
Demonstrates DAWN's integrated symbolic body working with memory and consciousness systems.
"""

import sys
import os
import asyncio

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Import the demo
from demo_scripts.test_symbolic_anatomy_integration import main as run_demo


def main():
    """Launch the symbolic anatomy integration demo."""
    print("🚀 Launching DAWN Symbolic Anatomy Demo")
    print("=" * 50)
    
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
        print("\n👋 Demo complete - symbolic anatomy ready for integration!")


if __name__ == "__main__":
    main() 