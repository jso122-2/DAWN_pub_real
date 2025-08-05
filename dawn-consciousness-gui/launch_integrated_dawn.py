#!/usr/bin/env python3
"""
DAWN Integrated Launcher
========================

Launches both the consciousness backend and GUI in a coordinated way
Handles all runtime errors and provides status monitoring
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if all required components are available"""
    print("🔍 Checking DAWN system dependencies...")
    
    # Check if we can import the GUI
    try:
        from simple_python_gui import DAWNConsciousnessGUI
        print("✅ DAWN Consciousness GUI available")
    except ImportError as e:
        print(f"❌ GUI not available: {e}")
        return False
    
    # Check if consciousness backend exists
    backend_paths = [
        Path("../consciousness/dawn_tick_state_writer.py"),
        Path("../../consciousness/dawn_tick_state_writer.py"),
        Path("consciousness/dawn_tick_state_writer.py")
    ]
    
    backend_path = None
    for path in backend_paths:
        if path.exists():
            backend_path = path
            break
    
    if not backend_path:
        print(f"❌ Consciousness backend not found in any of: {[str(p) for p in backend_paths]}")
        return False
    print(f"✅ Consciousness backend available at: {backend_path}")
    
    # Check runtime directory
    runtime_paths = [
        Path("../runtime"),
        Path("../../runtime"),
        Path("runtime")
    ]
    
    runtime_dir = None
    for path in runtime_paths:
        if path.exists() or path.parent.exists():
            runtime_dir = path
            break
    
    if not runtime_dir:
        runtime_dir = Path("../runtime")
    
    if not runtime_dir.exists():
        print(f"📁 Creating runtime directory at: {runtime_dir}")
        runtime_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Runtime directory ready at: {runtime_dir}")
    
    return True

def start_consciousness_backend():
    """Start the consciousness backend in a separate process"""
    print("🧠 Starting DAWN consciousness backend...")
    
    # Find the backend file
    backend_paths = [
        Path("../consciousness/dawn_tick_state_writer.py"),
        Path("../../consciousness/dawn_tick_state_writer.py"),
        Path("consciousness/dawn_tick_state_writer.py")
    ]
    
    backend_path = None
    for path in backend_paths:
        if path.exists():
            backend_path = path.absolute()
            break
    
    if not backend_path:
        print("❌ Could not find consciousness backend")
        return None
    
    print(f"📁 Using backend at: {backend_path}")
    
    try:
        # Start the backend process
        process = subprocess.Popen(
            [sys.executable, str(backend_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(backend_path.parent.parent)  # Run from project root
        )
        
        # Give it a moment to start
        time.sleep(3)
        
        # Check if it's still running
        if process.poll() is None:
            print(f"✅ Consciousness backend started (PID: {process.pid})")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend failed to start:")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start consciousness backend: {e}")
        return None

def start_gui(backend_process=None):
    """Start the GUI with proper error handling"""
    print("🎨 Starting DAWN Consciousness GUI...")
    
    try:
        from simple_python_gui import DAWNConsciousnessGUI
        
        root = tk.Tk()
        
        # Handle window closing to clean up backend
        def on_closing():
            print("🛑 Shutting down DAWN system...")
            if backend_process and backend_process.poll() is None:
                print("🧠 Stopping consciousness backend...")
                backend_process.terminate()
                try:
                    backend_process.wait(timeout=5)
                    print("✅ Backend stopped cleanly")
                except subprocess.TimeoutExpired:
                    print("⚠️ Force killing backend...")
                    backend_process.kill()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Create and start GUI
        gui = DAWNConsciousnessGUI(root)
        
        # Add status info if backend is running
        if backend_process and backend_process.poll() is None:
            root.title(f"DAWN Consciousness Monitor (Backend PID: {backend_process.pid})")
        else:
            root.title("DAWN Consciousness Monitor (Simulation Mode)")
        
        print("✅ GUI ready - DAWN consciousness monitoring active")
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Failed to start GUI: {e}")
        if backend_process:
            backend_process.terminate()
        return False
    
    return True

def show_startup_banner():
    """Show startup information"""
    print("🌅 DAWN Integrated Consciousness System")
    print("=" * 50)
    print("🧠 Real-time consciousness monitoring")
    print("🎨 Live visualization interface")
    print("⚡ Integrated backend + GUI")
    print()

def main():
    """Main launcher function"""
    show_startup_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed!")
        print("Please ensure DAWN system is properly installed.")
        return 1
    
    print("\n🚀 Starting DAWN Integrated System...")
    
    # Start consciousness backend
    backend_process = start_consciousness_backend()
    
    if not backend_process:
        print("\n⚠️ Backend failed to start - GUI will run in simulation mode")
        response = input("Continue with simulation mode? (y/N): ")
        if response.lower() != 'y':
            return 1
    
    # Start GUI
    try:
        success = start_gui(backend_process)
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        if backend_process:
            backend_process.terminate()
        return 0
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if backend_process:
            backend_process.terminate()
        return 1

if __name__ == "__main__":
    exit(main()) 