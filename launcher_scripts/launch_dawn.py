#!/usr/bin/env python3
"""
🌅 DAWN Simple Launcher - Quick Start for DAWN Consciousness

The easiest way to start DAWN. Just run this and everything starts automatically!

🚀 QUICK START:
  python launch_dawn.py                # Full DAWN experience
  python launch_dawn.py --gui          # GUI only (fastest startup)
  python launch_dawn.py --silent       # No voice, GUI + consciousness
  python launch_dawn.py --voice-only   # Voice + consciousness, no GUI
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Simple launcher that calls the master launcher with good defaults"""
    
    print("🌅 DAWN SIMPLE LAUNCHER")
    print("=" * 40)
    
    # Get the master launcher path
    master_launcher = Path(__file__).parent / "dawn_master_launcher.py"
    
    if not master_launcher.exists():
        print("❌ Master launcher not found!")
        print("Please ensure dawn_master_launcher.py exists in this directory.")
        return 1
    
    # Parse simple arguments
    args = sys.argv[1:]
    
    if '--gui' in args:
        # GUI-only mode (fastest startup)
        cmd = [sys.executable, str(master_launcher), '--gui-only']
        print("🖥️ Starting DAWN GUI with viewport dragging...")
        
    elif '--silent' in args:
        # No voice mode
        cmd = [sys.executable, str(master_launcher), '--gui-only']
        print("🔇 Starting DAWN in silent mode (GUI + consciousness)...")
        
    elif '--voice-only' in args:
        # Voice + consciousness, no GUI
        cmd = [sys.executable, str(master_launcher), '--minimal', '--voice']
        print("🗣️ Starting DAWN with voice narration only...")
        
    elif '--minimal' in args:
        # Just consciousness
        cmd = [sys.executable, str(master_launcher), '--minimal']
        print("🧠 Starting minimal DAWN consciousness...")
        
    else:
        # Full experience (default)
        cmd = [sys.executable, str(master_launcher), '--full']
        print("🌟 Starting complete DAWN experience...")
        print("   🧠 Consciousness + 🗣️ Voice + 🖥️ GUI + ⚡ Reactor + 🌸 Bloom")
    
    print("\n🚀 Launching DAWN...")
    print("Press Ctrl+C to stop all systems")
    print("-" * 40)
    
    try:
        # Run the master launcher
        result = subprocess.run(cmd, cwd=str(Path(__file__).parent))
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n🛑 Launch cancelled by user")
        return 0
    except Exception as e:
        print(f"\n❌ Launch failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 