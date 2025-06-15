#!/usr/bin/env python3
"""
KAN-Cairrn Server Launcher

Simple launcher for the KAN-Cairrn API server.
Run this from the Tick_engine directory.
"""

import uvicorn
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.simple_websocket_server import start_server
from main.startup import initialize_dawn
from main.demo_advanced_consciousness import run_demo
from main.restart_dawn_clean import restart_dawn
from main.start_dawn_api import start_api
from main.integrate_kan_cairrn import integrate
from main.start_api_fixed import start_api_fixed
from main.juliet_flower import run_juliet

def main():
    """Launch the KAN-Cairrn server"""
    
    # Check if we can import the system
    try:
        from cairrn_kan.interfaces.spline_api import app
        print("✅ KAN-Cairrn system available")
        
        # Launch server
        print("🚀 Starting KAN-Cairrn API server...")
        print("📖 API documentation will be available at http://127.0.0.1:8000/docs")
        print("🔗 Health check: http://127.0.0.1:8000/health")
        print("💡 Press Ctrl+C to stop the server")
        
        uvicorn.run(
            "cairrn_kan.interfaces.spline_api:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Could not import KAN-Cairrn system: {e}")
        print("Please ensure all required packages are installed:")
        print("pip install -r cairrn_kan_requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n✅ Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 