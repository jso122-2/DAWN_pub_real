#!/usr/bin/env python3
"""
Development startup script for DAWN system
Starts both Python backend API and Tauri desktop app
"""

import subprocess
import sys
import os
import time
import signal
from pathlib import Path

def check_node_npm():
    """Check if Node.js and npm are available"""
    try:
        subprocess.run(["node", "--version"], capture_output=True, check=True)
        subprocess.run(["npm", "--version"], capture_output=True, check=True)
        print("✅ Node.js and npm found")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js or npm not found. Please install Node.js")
        return False

def check_python_deps():
    """Check if Python dependencies are available"""
    try:
        import fastapi
        import uvicorn
        print("✅ Python FastAPI dependencies found")
        return True
    except ImportError:
        print("❌ Python dependencies missing. Run: pip install -r ../requirements.txt")
        return False

def start_python_backend():
    """Start the Python backend API server"""
    print("🚀 Starting Python backend API...")
    backend_process = subprocess.Popen(
        [sys.executable, "../main.py"],
        cwd=Path(__file__).parent
    )
    return backend_process

def start_tauri_frontend():
    """Start the Tauri frontend"""
    print("🖥️  Starting Tauri frontend...")
    frontend_process = subprocess.Popen(
        ["npm", "run", "tauri:dev"],
        cwd=Path(__file__).parent
    )
    return frontend_process

def wait_for_backend(max_wait=30):
    """Wait for backend to be ready"""
    import requests
    
    print("⏳ Waiting for backend to be ready...")
    for i in range(max_wait):
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                print("✅ Backend is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        if i < max_wait - 1:
            time.sleep(1)
            print(f"   Waiting... ({i+1}/{max_wait})")
    
    print("❌ Backend failed to start within timeout")
    return False

def main():
    """Main development startup"""
    print("🌟 DAWN Development Environment")
    print("=" * 50)
    
    # Check dependencies
    if not check_python_deps():
        return False
    
    if not check_node_npm():
        return False
    
    # Start processes
    backend_proc = None
    frontend_proc = None
    
    try:
        # Start Python backend
        backend_proc = start_python_backend()
        
        # Wait for backend to be ready
        if not wait_for_backend():
            return False
        
        # Start Tauri frontend
        frontend_proc = start_tauri_frontend()
        
        print("\n🎉 DAWN Development Environment Started!")
        print("📡 Backend API: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("🖥️  Frontend: Running in Tauri window")
        print("\nPress Ctrl+C to stop all services")
        
        # Wait for processes
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_proc and backend_proc.poll() is not None:
                print("❌ Backend process stopped unexpectedly")
                break
                
            if frontend_proc and frontend_proc.poll() is not None:
                print("❌ Frontend process stopped unexpectedly")
                break
    
    except KeyboardInterrupt:
        print("\n🛑 Shutting down DAWN development environment...")
    
    finally:
        # Clean up processes
        if backend_proc:
            backend_proc.terminate()
            try:
                backend_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                backend_proc.kill()
        
        if frontend_proc:
            frontend_proc.terminate()
            try:
                frontend_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                frontend_proc.kill()
        
        print("✅ All processes stopped")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1) 