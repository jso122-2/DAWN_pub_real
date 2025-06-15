#!/usr/bin/env python3
"""
DAWN Quick Start Script
Automatically sets up and starts the DAWN consciousness system
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def print_banner():
    print("🧠" * 20)
    print("   DAWN CONSCIOUSNESS MATRIX")
    print("   Quick Start Script")
    print("🧠" * 20)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print("✅ Python version:", sys.version_info[:2])
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Failed to install dependencies:", e)
        return False

def start_backend():
    """Start the DAWN backend"""
    print("🚀 Starting DAWN consciousness engine...")
    
    backend_path = Path("src/backend")
    if not backend_path.exists():
        print("❌ Backend directory not found")
        return None
    
    # Change to backend directory
    os.chdir(backend_path)
    
    try:
        # Start the backend process
        process = subprocess.Popen([
            sys.executable, "dawn_integrated_api.py"
        ])
        print("✅ Backend started with PID:", process.pid)
        return process
    except Exception as e:
        print("❌ Failed to start backend:", e)
        return None

def main():
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        return
    
    print("\n🎉 DAWN System Started Successfully!")
    print("=" * 40)
    print("🌐 WebSocket: ws://localhost:8001/ws")
    print("🔗 REST API: http://localhost:8001")
    print("📊 Status: http://localhost:8001/status")
    print("=" * 40)
    print("\n💡 Next Steps:")
    print("1. Open your React development server (npm start)")
    print("2. Navigate to your dashboard component")
    print("3. Watch the consciousness come alive! 🧠")
    print("\n⏹️  Press Ctrl+C to stop the backend")
    
    try:
        # Keep the script running and show status
        while True:
            if backend_process.poll() is not None:
                print("❌ Backend process stopped unexpectedly")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping DAWN system...")
        backend_process.terminate()
        backend_process.wait()
        print("✅ DAWN system stopped successfully")

if __name__ == "__main__":
    main() 