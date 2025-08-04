#!/usr/bin/env python3
"""
DAWN Visual GUI Launcher

Launches the clean visual GUI and connects it to the DAWN system.
"""

import sys
import os
import subprocess
import threading
import time
from pathlib import Path

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Main launcher function"""
    print("🌅 DAWN Visual GUI Launcher")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("dawn_runner.py").exists():
        print("❌ Error: dawn_runner.py not found. Please run from the DAWN project root.")
        return
    
    # Check if visual integration is available
    try:
        from visual.visual_integration import get_visual_integration
        print("✅ Visual integration available")
    except ImportError as e:
        print(f"⚠️  Visual integration not available: {e}")
        print("   Running in demo mode only")
    
    # Start the visual GUI
    print("\n🚀 Starting DAWN Visual GUI...")
    
    try:
        # Import and start the GUI
        from visual.dawn_visual_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ Error importing GUI: {e}")
        print("   Make sure dawn_visual_gui.py is in the current directory")
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")

if __name__ == "__main__":
    main() 