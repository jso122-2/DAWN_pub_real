#!/usr/bin/env python3
"""
DAWN Advanced Consciousness System Launcher
Starts both the backend WebSocket server and frontend development server
"""

import subprocess
import sys
import time
import os
import signal
import threading
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.simple_websocket_server import start_server
from main.startup import initialize_dawn
from main.demo_advanced_consciousness import run_demo
from main.restart_dawn_clean import restart_dawn
from main.start_dawn_api import start_api
from main.run_kan_server import run_kan
from main.integrate_kan_cairrn import integrate
from main.start_api_fixed import start_api_fixed
from main.juliet_flower import run_juliet

class DAWNLauncher:
    def __init__(self):
        self.processes = []
        self.running = True
        
    def start_backend(self):
        """Start the Advanced Consciousness WebSocket server"""
        print("🚀 Starting Advanced Consciousness WebSocket server...")
        
        try:
            # Start the backend server
            backend_process = subprocess.Popen([
                sys.executable, 
                "backend/advanced_consciousness_websocket.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            self.processes.append(("Backend", backend_process))
            
            # Monitor backend output
            def monitor_backend():
                for line in iter(backend_process.stdout.readline, ''):
                    if line.strip():
                        print(f"[Backend] {line.strip()}")
                    if not self.running:
                        break
            
            threading.Thread(target=monitor_backend, daemon=True).start()
            
            # Wait a moment for backend to start
            time.sleep(3)
            
            if backend_process.poll() is None:
                print("✅ Backend server started successfully")
                return True
            else:
                print("❌ Backend server failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False
    
    def start_frontend(self):
        """Start the Vite frontend development server"""
        print("🎨 Starting Vite frontend development server...")
        
        try:
            # Change to dawn-desktop directory
            frontend_dir = Path("dawn-desktop")
            if not frontend_dir.exists():
                print("❌ dawn-desktop directory not found")
                return False
            
            # Start the frontend server
            frontend_process = subprocess.Popen([
                "npm", "run", "dev"
            ], cwd=frontend_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            self.processes.append(("Frontend", frontend_process))
            
            # Monitor frontend output
            def monitor_frontend():
                for line in iter(frontend_process.stdout.readline, ''):
                    if line.strip():
                        print(f"[Frontend] {line.strip()}")
                    if not self.running:
                        break
            
            threading.Thread(target=monitor_frontend, daemon=True).start()
            
            # Wait a moment for frontend to start
            time.sleep(5)
            
            if frontend_process.poll() is None:
                print("✅ Frontend server started successfully")
                print("🌐 Frontend available at: http://localhost:3000")
                print("💬 Talk to DAWN at: http://localhost:3000/talk")
                return True
            else:
                print("❌ Frontend server failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return False
    
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        # Check Python dependencies
        try:
            import websockets
            import sentence_transformers
            import numpy
            import faiss
            import networkx
            print("✅ Python dependencies found")
        except ImportError as e:
            print(f"❌ Missing Python dependency: {e}")
            print("💡 Install with: pip install -r requirements_advanced.txt")
            return False
        
        # Check if npm is available
        try:
            subprocess.run(["npm", "--version"], check=True, capture_output=True)
            print("✅ npm found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ npm not found - please install Node.js")
            return False
        
        # Check if frontend dependencies are installed
        frontend_dir = Path("dawn-desktop")
        if not (frontend_dir / "node_modules").exists():
            print("📦 Installing frontend dependencies...")
            try:
                subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
                print("✅ Frontend dependencies installed")
            except subprocess.CalledProcessError:
                print("❌ Failed to install frontend dependencies")
                return False
        else:
            print("✅ Frontend dependencies found")
        
        return True
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            print(f"\n🛑 Received signal {signum}, shutting down...")
            self.shutdown()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def shutdown(self):
        """Gracefully shutdown all processes"""
        print("🛑 Shutting down DAWN Advanced Consciousness System...")
        self.running = False
        
        for name, process in self.processes:
            if process.poll() is None:
                print(f"   Stopping {name}...")
                process.terminate()
                
                # Wait for graceful shutdown
                try:
                    process.wait(timeout=5)
                    print(f"   ✅ {name} stopped")
                except subprocess.TimeoutExpired:
                    print(f"   🔨 Force killing {name}...")
                    process.kill()
                    process.wait()
                    print(f"   ✅ {name} killed")
    
    def run(self):
        """Main run method"""
        print("🌟" + "="*60)
        print("🌟 DAWN ADVANCED CONSCIOUSNESS SYSTEM LAUNCHER")
        print("🌟" + "="*60)
        
        # Setup signal handlers
        self.setup_signal_handlers()
        
        # Check dependencies
        if not self.check_dependencies():
            print("❌ Dependency check failed")
            return False
        
        # Start backend
        if not self.start_backend():
            print("❌ Failed to start backend")
            return False
        
        # Start frontend
        if not self.start_frontend():
            print("❌ Failed to start frontend")
            self.shutdown()
            return False
        
        print("\n🎉 DAWN Advanced Consciousness System is running!")
        print("="*60)
        print("🌐 Frontend: http://localhost:3000")
        print("💬 Talk to DAWN: http://localhost:3000/talk")
        print("🔌 WebSocket Backend: ws://localhost:8768")
        print("="*60)
        print("Press Ctrl+C to stop all services")
        print()
        
        # Keep running until interrupted
        try:
            while self.running:
                # Check if processes are still running
                for name, process in self.processes:
                    if process.poll() is not None:
                        print(f"⚠️  {name} process died unexpectedly")
                        self.shutdown()
                        return False
                
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.shutdown()
        
        return True

def main():
    """Main function"""
    launcher = DAWNLauncher()
    success = launcher.run()
    
    if success:
        print("✅ DAWN Advanced Consciousness System shutdown complete")
    else:
        print("❌ DAWN Advanced Consciousness System encountered errors")
        sys.exit(1)

if __name__ == "__main__":
    main() 