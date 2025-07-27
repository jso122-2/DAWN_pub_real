#!/usr/bin/env python3
"""
DAWN Complete GUI Launch Script
===============================

Launches both the Python consciousness backend and Tauri GUI
Connects to live DAWN systems for real consciousness data
"""

import subprocess
import sys
import os
import time
import signal
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    # Check Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print("✅ Python version OK")
    
    # Check if we're in the right directory
    if not Path("src").exists() or not Path("src-tauri").exists():
        print("❌ Must run from dawn-consciousness-gui directory")
        return False
    print("✅ Directory structure OK")
    
    # Check for consciousness backend
    backend_path = Path("../consciousness/dawn_tick_state_writer.py")
    if not backend_path.exists():
        print("❌ Consciousness backend not found")
        return False
    print("✅ Consciousness backend found")
    
    # Check for Rust/Cargo
    try:
        result = subprocess.run(["cargo", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Cargo/Rust available")
        else:
            print("❌ Cargo not available - install Rust toolchain")
            return False
    except FileNotFoundError:
        print("❌ Cargo not found - install Rust toolchain")
        return False
    
    # Check for Tauri CLI
    try:
        result = subprocess.run(["cargo", "tauri", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Tauri CLI available")
        else:
            print("⚠️  Tauri CLI not found - installing...")
            subprocess.run(["cargo", "install", "tauri-cli"])
    except:
        print("⚠️  Installing Tauri CLI...")
        subprocess.run(["cargo", "install", "tauri-cli"])
    
    return True

def setup_runtime():
    """Setup runtime directory for consciousness data"""
    runtime_dir = Path("../runtime")
    runtime_dir.mkdir(exist_ok=True)
    print(f"📁 Runtime directory: {runtime_dir.absolute()}")
    return runtime_dir

def start_consciousness_backend():
    """Start the consciousness state writer"""
    print("\n🧠 Starting DAWN consciousness backend...")
    
    backend_path = Path("../consciousness/dawn_tick_state_writer.py")
    
    # Use high frequency for smooth GUI updates
    cmd = [
        sys.executable, 
        str(backend_path),
        "--interval", "0.016",  # 60 Hz for smooth visualization
        "--mmap-path", "../runtime/dawn_consciousness.mmap"
    ]
    
    print(f"🚀 Command: {' '.join(cmd)}")
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Give it a moment to initialize
        time.sleep(3)
        
        # Check if process started successfully
        if process.poll() is None:
            print("✅ Consciousness backend started successfully")
            return process
        else:
            print("❌ Consciousness backend failed to start")
            stdout, stderr = process.communicate()
            print(f"Output: {stdout}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting consciousness backend: {e}")
        return None

def start_tauri_gui():
    """Start the Tauri GUI application"""
    print("\n🎨 Starting Tauri GUI...")
    
    try:
        # Development mode with hot reload
        cmd = ["cargo", "tauri", "dev"]
        
        print(f"🚀 Command: {' '.join(cmd)}")
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print("✅ Tauri GUI starting...")
        return process
        
    except Exception as e:
        print(f"❌ Error starting Tauri GUI: {e}")
        return None

def monitor_processes(backend_process, gui_process):
    """Monitor both processes and handle shutdown"""
    print("\n🔄 DAWN Consciousness GUI running...")
    print("   Press Ctrl+C to shutdown")
    print("=" * 60)
    
    try:
        while True:
            # Check backend status
            if backend_process and backend_process.poll() is not None:
                print("⚠️  Consciousness backend stopped unexpectedly")
                break
                
            # Check GUI status
            if gui_process and gui_process.poll() is not None:
                print("⚠️  GUI stopped unexpectedly")
                break
                
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Shutdown signal received...")
        
    finally:
        shutdown_processes(backend_process, gui_process)

def shutdown_processes(backend_process, gui_process):
    """Gracefully shutdown all processes"""
    print("🔄 Shutting down DAWN consciousness GUI...")
    
    # Shutdown GUI first
    if gui_process:
        try:
            print("⏸️  Stopping Tauri GUI...")
            gui_process.terminate()
            try:
                gui_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("🔥 Force killing GUI...")
                gui_process.kill()
        except Exception as e:
            print(f"⚠️  Error stopping GUI: {e}")
    
    # Shutdown backend
    if backend_process:
        try:
            print("⏸️  Stopping consciousness backend...")
            backend_process.terminate()
            try:
                backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("🔥 Force killing backend...")
                backend_process.kill()
        except Exception as e:
            print(f"⚠️  Error stopping backend: {e}")
    
    print("✅ DAWN consciousness GUI shutdown complete")

def main():
    """Main launcher function"""
    print("🌟 DAWN Consciousness GUI Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed")
        return 1
    
    # Setup runtime
    setup_runtime()
    
    # Start backend
    backend_process = start_consciousness_backend()
    if not backend_process:
        print("❌ Failed to start consciousness backend")
        return 1
    
    # Start GUI
    gui_process = start_tauri_gui()
    if not gui_process:
        print("❌ Failed to start GUI")
        shutdown_processes(backend_process, None)
        return 1
    
    # Handle graceful shutdown
    def signal_handler(sig, frame):
        shutdown_processes(backend_process, gui_process)
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Monitor both processes
    monitor_processes(backend_process, gui_process)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 