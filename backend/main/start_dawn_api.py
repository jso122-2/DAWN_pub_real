#!/usr/bin/env python3
"""
Startup script for DAWN Neural Monitor API
"""

import subprocess
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path
from utils.simple_websocket_server import start_server
from main.startup import initialize_dawn
from main.demo_advanced_consciousness import run_demo
from main.restart_dawn_clean import restart_dawn
from main.run_kan_server import run_kan
from main.integrate_kan_cairrn import integrate
from main.start_api_fixed import start_api_fixed
from main.juliet_flower import run_juliet

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import websockets
        import pydantic
        print("✅ FastAPI dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def start_server():
    """Start the DAWN API server"""
    print("🌟 Starting DAWN Neural Monitor API Server")
    print("📡 Server will be available at: http://localhost:8002")
    print("🔗 WebSocket endpoint: ws://localhost:8002/ws")
    print("📚 API Documentation: http://localhost:8002/docs")
    print("━" * 60)
    
    try:
        # Change to interface directory and run with uvicorn
        interface_dir = Path(__file__).parent / "interface"
        os.chdir(interface_dir)
        
        # Start with uvicorn
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "dawn_api:app", 
            "--reload", 
            "--host", "127.0.0.1", 
            "--port", "8002"
        ]
        
        print(f"🚀 Starting server with command: {' '.join(cmd)}")
        print(f"📁 Working directory: {os.getcwd()}")
        
        # Run the server
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server exited with error code: {e.returncode}")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    if check_dependencies():
        start_server()
    else:
        sys.exit(1) 