#!/usr/bin/env python3
"""
DAWN Simple GUI Launcher
========================

Launches the consciousness backend and simple Python GUI
"""

import subprocess
import sys
import time
import signal
import threading
from pathlib import Path

def start_consciousness_backend():
    """Start the consciousness backend"""
    print("🧠 Starting consciousness backend...")
    
    backend_path = Path("../consciousness/dawn_tick_state_writer.py")
    if not backend_path.exists():
        print(f"❌ Backend not found at: {backend_path}")
        return None
        
    try:
        process = subprocess.Popen(
            [sys.executable, str(backend_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        print(f"✅ Backend started (PID: {process.pid})")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_gui():
    """Start the Python GUI"""
    print("🎨 Starting Python GUI...")
    
    gui_path = Path("simple_python_gui.py")
    if not gui_path.exists():
        print(f"❌ GUI not found at: {gui_path}")
        return None
        
    try:
        process = subprocess.Popen(
            [sys.executable, str(gui_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        print(f"✅ GUI started (PID: {process.pid})")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start GUI: {e}")
        return None

def monitor_processes(backend_process, gui_process):
    """Monitor both processes"""
    print("\n🔄 Monitoring processes...")
    print("   Press Ctrl+C to stop")
    
    try:
        while True:
            # Check if processes are still running
            if backend_process and backend_process.poll() is not None:
                print("⚠️  Backend stopped")
                break
                
            if gui_process and gui_process.poll() is not None:
                print("⚠️  GUI stopped")
                break
                
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")

def cleanup_processes(backend_process, gui_process):
    """Clean up processes"""
    print("🧹 Cleaning up processes...")
    
    if gui_process:
        try:
            gui_process.terminate()
            gui_process.wait(timeout=5)
        except:
            gui_process.kill()
            
    if backend_process:
        try:
            backend_process.terminate()
            backend_process.wait(timeout=5)
        except:
            backend_process.kill()

def main():
    """Main launcher function"""
    print("🌟 DAWN Simple GUI Launcher")
    print("=" * 40)
    
    # Start backend
    backend_process = start_consciousness_backend()
    if not backend_process:
        print("❌ Failed to start backend")
        return 1
        
    # Wait a moment for backend to initialize
    time.sleep(3)
    
    # Start GUI
    gui_process = start_gui()
    if not gui_process:
        print("❌ Failed to start GUI")
        cleanup_processes(backend_process, None)
        return 1
        
    print("\n✅ Both processes started successfully!")
    print("   GUI should open in a new window")
    
    # Monitor processes
    try:
        monitor_processes(backend_process, gui_process)
    finally:
        cleanup_processes(backend_process, gui_process)
        
    print("✅ Shutdown complete")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 