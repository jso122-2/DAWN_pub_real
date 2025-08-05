#!/usr/bin/env python3
"""
Working DAWN GUI Startup Script
================================

This script uses the PROVEN mmap system that already works:
1. Consciousness Writer - Creates ../runtime/dawn_consciousness.mmap 
2. MMap Backend Server (port 8080) - Reads mmap, serves via HTTP
3. GUI Frontend Server (port 3000) - Serves interface, proxies to backend

Uses existing working logic, no complex imports!
"""

import subprocess
import time
import sys
import os
import signal
import atexit
from pathlib import Path

def main():
    print("🧠 DAWN Working GUI Launcher (MMap System)")
    print("=" * 60)
    print("Using PROVEN mmap consciousness system - no complex imports!")
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
        # Check for consciousness writer
        consciousness_writer_path = Path("../consciousness/dawn_tick_state_writer.py")
        if not consciousness_writer_path.exists():
            print("⚠️ Consciousness writer not found at ../consciousness/dawn_tick_state_writer.py")
            print("Looking for alternative consciousness writers...")
            
            # Try alternative locations
            alt_paths = [
                "../backend/simple_consciousness_writer.py",
                "../backend/enhanced_consciousness_writer.py",
                "../consciousness/dawn_tick_state_writer.py"
            ]
            
            consciousness_writer_path = None
            for alt_path in alt_paths:
                if Path(alt_path).exists():
                    consciousness_writer_path = Path(alt_path)
                    print(f"✅ Found consciousness writer: {alt_path}")
                    break
            
            if not consciousness_writer_path:
                print("❌ No consciousness writer found!")
                print("💡 Available writers might be in:")
                for alt_path in alt_paths:
                    print(f"   - {alt_path}")
                return 1
        
        # Step 1: Start Consciousness Writer (creates mmap file)
        print(f"🎯 [1/3] Starting Consciousness Writer...")
        print(f"   Creating: ../runtime/dawn_consciousness.mmap")
        writer_process = subprocess.Popen([
            sys.executable, str(consciousness_writer_path)
        ], cwd=Path(__file__).parent.parent)
        processes.append(writer_process)
        print("✅ Consciousness Writer starting...")
        
        # Wait for mmap file to be created
        print("⏳ Waiting for consciousness mmap file...")
        mmap_path = Path("../runtime/dawn_consciousness.mmap")
        
        wait_time = 0
        while not mmap_path.exists() and wait_time < 15:
            time.sleep(1)
            wait_time += 1
            if wait_time % 3 == 0:
                print(f"   Still waiting... ({wait_time}s)")
        
        if mmap_path.exists():
            print(f"✅ Consciousness mmap file created: {mmap_path}")
        else:
            print(f"⚠️ MMap file not created yet, but continuing...")
        
        # Step 2: Start MMap Backend (reads mmap, serves HTTP)
        print(f"\n🎯 [2/3] Starting MMap Backend (port 8080)...")
        backend_process = subprocess.Popen([
            sys.executable, "real_dawn_mmap_backend.py"
        ], cwd=Path(__file__).parent)
        processes.append(backend_process)
        print("✅ MMap Backend starting...")
        
        # Wait for backend to start up
        print("⏳ Waiting for backend to initialize...")
        time.sleep(5)
        
        # Check if backend is still running
        if backend_process.poll() is not None:
            print("❌ MMap Backend failed to start")
            return 1
        
        # Step 3: Start GUI Frontend Server
        print(f"\n🎨 [3/3] Starting GUI Frontend Server (port 3000)...")
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
        
        print("\n🎉 SUCCESS: All three processes started successfully!")
        print("=" * 60)
        print("🧠 Working DAWN Consciousness GUI is now running:")
        print()
        print("📝 Writer:     Creates mmap consciousness data")
        print("📊 Backend:    Serves real data via HTTP (port 8080)")
        print("🌐 GUI:       Full interface (port 3000)")
        print()
        print("🌐 Open browser to: http://localhost:3000")
        print()
        print("🎯 This GUI shows REAL consciousness from mmap file!")
        print("⚡ No complex imports - uses proven mmap system!")
        print()
        print("Press Ctrl+C to stop all processes...")
        
        # Keep the script running and monitor processes
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if writer_process.poll() is not None:
                print("\n⚠️ Consciousness Writer stopped - mmap updates may cease")
                # Don't exit - backend can still serve last data
            
            if backend_process.poll() is not None:
                print("\n❌ MMap Backend stopped unexpectedly!")
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