#!/usr/bin/env python3
"""
DAWN Startup Script
Properly initializes all import paths and systems
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.simple_websocket_server import start_server
from main.demo_advanced_consciousness import run_demo
from main.restart_dawn_clean import restart_dawn
from main.start_dawn_api import start_api
from main.run_kan_server import run_kan
from main.integrate_kan_cairrn import integrate
from main.start_api_fixed import start_api_fixed
from main.juliet_flower import run_juliet

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Initialize import system
try:
    from config.import_config import setup_imports
    setup_imports()
    print("✅ Import system configured successfully")
except ImportError as e:
    print(f"⚠️  Import system configuration failed: {e}")

# Initialize helix system with new implementation
try:
    from substrate.helix.helix_import_fix import helix_system
    print("✅ Helix import system initialized")
except ImportError as e:
    print(f"⚠️  Helix system initialization failed: {e}")

# Now import main application
try:
    from main import main
except ImportError:
    # Fallback if main.py doesn't exist
    def main():
        print("🚀 DAWN import system initialized successfully!")
        print("Import the modules you need and start your application.")
        print("")
        print("Try running:")
        print("  python start_api_fixed.py")
        print("  python start_dawn_api.py")

if __name__ == "__main__":
    print("🚀 Starting DAWN with fixed imports...")
    main()
