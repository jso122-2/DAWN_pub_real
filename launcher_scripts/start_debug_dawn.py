#!/usr/bin/env python3
"""
Debug startup script for DAWN Neural Monitor API
Enables comprehensive debug logging and monitoring
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_debug_environment():
    """Set up debug environment variables"""
    # Enable debug logging
    os.environ['DAWN_LOG_LEVEL'] = 'DEBUG'
    
    # Set other debugging flags
    os.environ['PYTHONUNBUFFERED'] = '1'  # Force unbuffered output
    os.environ['DAWN_DEBUG_MODE'] = 'true'
    
    print("🐛 Debug environment configured:")
    print(f"   - Log Level: {os.environ.get('DAWN_LOG_LEVEL')}")
    print(f"   - Debug Mode: {os.environ.get('DAWN_DEBUG_MODE')}")
    print(f"   - Unbuffered Output: {os.environ.get('PYTHONUNBUFFERED')}")

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

def start_debug_server():
    """Start the DAWN API server in debug mode"""
    print("🐛 ====== DAWN Neural Monitor API Server (DEBUG MODE) ======")
    print("📡 Server will be available at: http://localhost:8000")
    print("🔗 WebSocket endpoint: ws://localhost:8000/ws")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("📝 Debug logs will be very verbose")
    print("🔍 Watch for detailed request/response logging")
    print("━" * 70)
    
    try:
        # Change to interface directory and run with debug flags
        interface_dir = Path(__file__).parent / "interface"
        os.chdir(interface_dir)
        
        # Start with verbose uvicorn logging
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "dawn_api:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--log-level", "debug"
        ]
        
        print(f"🚀 Starting debug server with command: {' '.join(cmd)}")
        print(f"📁 Working directory: {os.getcwd()}")
        print("━" * 70)
        
        # Run the server
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Debug server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server exited with error code: {e.returncode}")
    except Exception as e:
        print(f"❌ Error starting debug server: {e}")

def main():
    """Main debug startup function"""
    print("🐛 DAWN Debug Mode Startup")
    print("=" * 50)
    
    # Set up debug environment
    setup_debug_environment()
    print()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    print()
    
    # Start debug server
    start_debug_server()

if __name__ == "__main__":
    main() 