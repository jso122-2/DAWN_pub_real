#!/usr/bin/env python3
"""
Startup script for DAWN Neural Monitor API
"""

import subprocess
import sys
import os
from pathlib import Path

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
    print("📡 Server will be available at: http://localhost:8000")
    print("🔗 WebSocket endpoint: ws://localhost:8000/ws")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("━" * 60)
    
    try:
        # Import and run the main application
        os.system("python main.py")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    if check_dependencies():
        start_server()
    else:
        sys.exit(1) 