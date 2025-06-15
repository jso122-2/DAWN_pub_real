#!/usr/bin/env python3
"""
DAWN System Startup Script
Starts both backend (port 8001) and frontend (port 3000) services
"""

import subprocess
import sys
import time
import os
import threading
from pathlib import Path

def run_backend():
    """Start the DAWN backend on port 8000"""
    print("🧠 Starting DAWN Backend (Port 8000)...")
    try:
        # Try to run the backend from the backend directory
        backend_path = Path(__file__).parent / "src" / "backend" / "dawn_integrated_api.py"
        if backend_path.exists():
            subprocess.run([sys.executable, str(backend_path)], cwd=str(Path(__file__).parent))
        else:
            # Fallback to the other backend location
            backend_path = Path(__file__).parent / "backend" / "dawn_integrated_api.py"
            if backend_path.exists():
                subprocess.run([sys.executable, str(backend_path)], cwd=str(Path(__file__).parent))
            else:
                print("❌ Backend script not found!")
                sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Backend shutting down...")
    except Exception as e:
        print(f"❌ Backend error: {e}")

def run_frontend():
    """Start the React frontend on port 3000"""
    print("🌐 Starting React Frontend (Port 3000)...")
    try:
        # Wait a moment for backend to start
        time.sleep(3)
        
        # Start the frontend
        env = os.environ.copy()
        env['PORT'] = '3000'
        subprocess.run(['npm', 'run', 'dev'], cwd=str(Path(__file__).parent), env=env)
    except KeyboardInterrupt:
        print("\n🛑 Frontend shutting down...")
    except Exception as e:
        print(f"❌ Frontend error: {e}")

def main():
    """Main startup function"""
    print("=" * 60)
    print("🚀 DAWN System Startup")
    print("=" * 60)
    print("Backend (API + WebSocket): http://localhost:8000")
    print("Frontend (React App):      http://localhost:3000") 
    print("WebSocket Endpoint:        ws://localhost:8000/ws")
    print("=" * 60)
    
    # Check if we're in the right directory
    current_dir = Path(__file__).parent
    if not (current_dir / "package.json").exists():
        print("❌ Please run this script from the dawn-desktop directory")
        sys.exit(1)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Start frontend in main thread (so Ctrl+C works properly)
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down DAWN system...")
        sys.exit(0)

if __name__ == "__main__":
    main() 