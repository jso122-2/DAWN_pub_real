#!/usr/bin/env python3
"""
DAWN Consciousness Monitor Launcher
====================================

Launches the complete local consciousness introspection system:
1. Python consciousness backend (writes to .mmap file)
2. Tauri GUI (reads from .mmap file)

No web servers, no APIs - pure local cognition monitoring.
"""

import subprocess
import sys
import os
import time
import signal
from pathlib import Path

class ConsciousnessMonitorLauncher:
    def __init__(self):
        self.processes = []
        self.running = False
        
    def setup_paths(self):
        """Ensure required directories exist"""
        runtime_dir = Path("../runtime")
        runtime_dir.mkdir(exist_ok=True)
        
        print("🧠 DAWN Consciousness Monitor Launcher")
        print("=" * 50)
        print(f"📁 Runtime directory: {runtime_dir.absolute()}")
        
    def start_consciousness_backend(self):
        """Start the Python consciousness state writer"""
        print("\n🔧 Starting consciousness backend...")
        
        try:
            # Start the Python backend that writes consciousness state to mmap
            backend_path = Path("../consciousness/dawn_tick_state_writer.py")
            if not backend_path.exists():
                print(f"❌ Backend not found at: {backend_path.absolute()}")
                return False
                
            cmd = [sys.executable, str(backend_path), "--interval", "0.016"]  # 60 Hz
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes.append(('backend', process))
            print(f"✅ Consciousness backend started (PID: {process.pid})")
            print("   Writing consciousness state to runtime/dawn_consciousness.mmap")
            
            # Give it a moment to initialize
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to start consciousness backend: {e}")
            return False
    
    def start_tauri_gui(self):
        """Start the Tauri GUI application"""
        print("\n🎨 Starting Tauri GUI...")
        
        try:
            # Check if we're in development or production mode
            tauri_dir = Path("src-tauri")
            if tauri_dir.exists():
                # Development mode - use cargo tauri dev
                cmd = ["cargo", "tauri", "dev"]
                cwd = "."
            else:
                print("❌ Tauri development environment not found")
                return False
            
            print(f"🚀 Launching GUI: {' '.join(cmd)}")
            
            process = subprocess.Popen(
                cmd,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes.append(('gui', process))
            print(f"✅ Tauri GUI starting (PID: {process.pid})")
            print("   Local consciousness introspection interface loading...")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to start Tauri GUI: {e}")
            return False
    
    def monitor_processes(self):
        """Monitor running processes and handle shutdown"""
        print("\n🔄 Consciousness monitor running...")
        print("   Press Ctrl+C to shutdown gracefully")
        print("\n" + "=" * 50)
        
        self.running = True
        
        try:
            while self.running:
                time.sleep(1)
                
                # Check if any processes have died
                for name, process in self.processes:
                    if process.poll() is not None:
                        print(f"⚠️  {name} process ended unexpectedly")
                        
        except KeyboardInterrupt:
            print("\n\n🛑 Shutdown signal received...")
            self.shutdown()
    
    def shutdown(self):
        """Gracefully shutdown all processes"""
        print("🔄 Shutting down consciousness monitor...")
        
        self.running = False
        
        for name, process in self.processes:
            try:
                print(f"⏸️  Stopping {name}...")
                process.terminate()
                
                # Wait for graceful shutdown
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print(f"🔥 Force killing {name}...")
                    process.kill()
                    
            except Exception as e:
                print(f"⚠️  Error stopping {name}: {e}")
        
        print("✅ Consciousness monitor shutdown complete")
        print("\n🧠 Thank you for exploring DAWN's consciousness together!")
    
    def launch(self):
        """Launch the complete consciousness monitoring system"""
        try:
            self.setup_paths()
            
            # Start the consciousness backend first
            if not self.start_consciousness_backend():
                return False
            
            # Start the GUI
            if not self.start_tauri_gui():
                self.shutdown()
                return False
            
            # Monitor until shutdown
            self.monitor_processes()
            
            return True
            
        except Exception as e:
            print(f"❌ Launcher error: {e}")
            self.shutdown()
            return False

def main():
    """Main launcher entry point"""
    launcher = ConsciousnessMonitorLauncher()
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        launcher.shutdown()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    success = launcher.launch()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 