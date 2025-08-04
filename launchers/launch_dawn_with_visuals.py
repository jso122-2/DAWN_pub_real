# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
DAWN with Visual Integration - Complete Launcher

Launches DAWN with integrated visual processes and GUI.
"""

import sys
import os
import subprocess
import threading
import time
import signal
from pathlib import Path

def main():
    """Main launcher function"""
    print("🌅 DAWN with Visual Integration")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("dawn_runner.py").exists():
        print("❌ Error: dawn_runner.py not found. Please run from the DAWN project root.")
        return
    
    # Check visual integration
    try:
        from visual.visual_integration import get_visual_integration
        print("✅ Visual integration available")
    except ImportError as e:
        print(f"⚠️  Visual integration not available: {e}")
    
    # Check GUI availability
    gui_available = Path("dawn_visual_gui.py").exists()
    if gui_available:
        print("✅ Visual GUI available")
    else:
        print("⚠️  Visual GUI not found")
    
    print("\n🚀 Starting DAWN with visual integration...")
    
    # Start DAWN in background
    dawn_process = None
    gui_process = None
    
    try:
        # Start DAWN runner
        print("🧠 Starting DAWN Unified Runner...")
        dawn_process = subprocess.Popen(
            [sys.executable, "launch_dawn.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Give DAWN time to start
        time.sleep(3)
        
        # Start visual GUI if available
        if gui_available:
            print("🎨 Starting Visual GUI...")
            gui_process = subprocess.Popen(
                [sys.executable, "dawn_visual_gui.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
        
        print("\n✅ DAWN with Visual Integration is running!")
        print("   - DAWN Runner: PID", dawn_process.pid if dawn_process else "N/A")
        print("   - Visual GUI: PID", gui_process.pid if gui_process else "N/A")
        print("\nPress Ctrl+C to stop all processes...")
        
        # Monitor processes
        while True:
            if dawn_process and dawn_process.poll() is not None:
                print("❌ DAWN Runner stopped unexpectedly")
                break
            if gui_process and gui_process.poll() is not None:
                print("❌ Visual GUI stopped unexpectedly")
                break
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Cleanup
        if dawn_process:
            print("🛑 Stopping DAWN Runner...")
            dawn_process.terminate()
            dawn_process.wait(timeout=5)
        
        if gui_process:
            print("🛑 Stopping Visual GUI...")
            gui_process.terminate()
            gui_process.wait(timeout=5)
        
        print("✅ All processes stopped")

if __name__ == "__main__":
    main() 