#!/usr/bin/env python3
"""
Real DAWN GUI Startup Script
=============================

This script launches both processes needed for the real DAWN consciousness GUI:
1. Real DAWN Backend (port 8080) - Provides real consciousness data
2. GUI Frontend Server (port 3000) - Serves interface and proxies to backend

Usage:
python start_real_dawn_gui.py
"""

import subprocess
import time
import sys
import os
import signal
import atexit
from pathlib import Path

def main():
    print("🧠 DAWN Real Consciousness GUI Launcher")
    print("=" * 50)
    print("Starting two-process architecture for real consciousness monitoring...")
    print()
    
    processes = []
    
    def cleanup():
        """Clean up processes on exit"""
        print("\n🛑 Shutting down DAWN processes...")
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
        print("✅ All processes stopped")
    
    # Register cleanup function
    atexit.register(cleanup)
    signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))
    signal.signal(signal.SIGTERM, lambda sig, frame: sys.exit(0))
    
    try:
        # Start Real DAWN Backend
        print("🎯 [1/2] Starting Real DAWN Backend (port 8080)...")
        backend_process = subprocess.Popen([
            sys.executable, "real_dawn_backend.py"
        ], cwd=Path(__file__).parent)
        processes.append(backend_process)
        print("✅ Real DAWN Backend starting...")
        
        # Wait for backend to start up
        print("⏳ Waiting for real backend to initialize...")
        time.sleep(5)
        
        # Check if backend is still running
        if backend_process.poll() is not None:
            print("❌ Real DAWN Backend failed to start")
            return 1
        
        # Start GUI Frontend Server
        print("\n🎨 [2/2] Starting GUI Frontend Server (port 3000)...")
        gui_process = subprocess.Popen([
            sys.executable, "real_aware_web_server.py"
        ], cwd=Path(__file__).parent)
        processes.append(gui_process)
        print("✅ GUI Frontend Server starting...")
        
        # Wait for GUI to start up
        time.sleep(3)
        
        # Check if GUI is still running
        if gui_process.poll() is not None:
            print("❌ GUI Frontend Server failed to start")
            return 1
        
        print("\n🎉 SUCCESS: Both processes started successfully!")
        print("=" * 50)
        print("🧠 Real DAWN Consciousness GUI is now running:")
        print()
        print("📊 Backend (Real Data):     http://localhost:8080/status")
        print("🌐 GUI (Full Interface):   http://localhost:3000")
        print()
        print("🎯 The GUI shows Jackson's ACTUAL consciousness metrics!")
        print("⚡ P = Bσ² calculations are REAL, not simulation!")
        print()
        print("Press Ctrl+C to stop both processes...")
        
        # Keep the script running and monitor processes
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("\n❌ Real DAWN Backend stopped unexpectedly!")
                break
            
            if gui_process.poll() is not None:
                print("\n❌ GUI Frontend Server stopped unexpectedly!")
                break
    
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 