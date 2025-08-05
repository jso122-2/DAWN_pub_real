#!/usr/bin/env python3
"""
DAWN Consolidated GUI Launcher
Launch the unified tabbed interface for DAWN consciousness monitoring
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def setup_environment():
    """Setup the Python environment for DAWN components"""
    # Add project root to Python path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    # Add specific component directories
    component_dirs = [
        "backend",
        "backend/core",
        "backend/visual", 
        "backend/api",
        "visual",
        "BP",
        "fractal",
        "integration",
        "core"
    ]
    
    for comp_dir in component_dirs:
        comp_path = project_root / comp_dir
        if comp_path.exists():
            sys.path.insert(0, str(comp_path))

def check_dependencies():
    """Check if required dependencies are available"""
    missing_deps = []
    
    try:
        import tkinter
    except ImportError:
        missing_deps.append("tkinter")
    
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    
    try:
        import PIL
    except ImportError:
        missing_deps.append("Pillow")
    
    if missing_deps:
        print("⚠️  Missing dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\n💡 Install with: pip install tkinter numpy Pillow")
        return False
    
    return True

def start_backend_server(port=8000):
    """Start the DAWN backend server"""
    try:
        # Check if backend server is already running
        import requests
        response = requests.get(f"http://localhost:{port}/health", timeout=2)
        if response.status_code == 200:
            print(f"✅ Backend server already running on port {port}")
            return True
    except:
        pass
    
    # Try to start backend server
    backend_scripts = [
        "backend/api/websocket_server.py",
        "backend/main.py",
        "web_server.py",
        "launcher_scripts/start_backend_server.py"
    ]
    
    for script in backend_scripts:
        script_path = Path(script)
        if script_path.exists():
            print(f"🚀 Starting backend server: {script}")
            try:
                # Start in background
                subprocess.Popen([
                    sys.executable, str(script_path), 
                    "--port", str(port), "--host", "localhost"
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
            except Exception as e:
                print(f"⚠️  Failed to start {script}: {e}")
                continue
    
    print("⚠️  No backend server script found, running GUI standalone")
    return False

def launch_consolidated_gui(with_backend=True, port=8000):
    """Launch the consolidated DAWN GUI"""
    print("🌅 DAWN Consolidated GUI Launcher")
    print("=" * 50)
    print("🎯 Launching unified tabbed interface...")
    
    # Setup environment
    setup_environment()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Missing required dependencies")
        return False
    
    # Start backend if requested
    if with_backend:
        print("\n🔧 Starting backend services...")
        start_backend_server(port)
        
        # Give backend time to start
        import time
        time.sleep(2)
    
    # Launch GUI
    print("\n🖥️  Starting consolidated GUI...")
    try:
        from dawn_consolidated_gui import DAWNConsolidatedGUI
        
        app = DAWNConsolidatedGUI()
        
        print("✅ GUI launched successfully!")
        print("📊 Available tabs:")
        print("   🖼️  Visual - Fractal/bloom/sigil rendering")
        print("   🗣️  Voice - Audio synthesis with pigment visualization")  
        print("   📊 State Monitor - Real-time DAWN cognitive status")
        print("   ⚙️  Controls - System configuration and manual triggers")
        print("   📚 Archive - Expression history and search")
        print("   📋 Logs - System logging and debugging")
        print("\n🚀 GUI ready for use!")
        
        app.run()
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import GUI components: {e}")
        print("💡 Ensure all DAWN components are properly installed")
        return False
    except Exception as e:
        print(f"❌ GUI launch error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(
        description="DAWN Consolidated GUI Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch_dawn_consolidated_gui.py                # Full system with backend
  python launch_dawn_consolidated_gui.py --no-backend  # GUI only
  python launch_dawn_consolidated_gui.py --port 8080   # Custom backend port
        """
    )
    
    parser.add_argument(
        '--no-backend',
        action='store_true',
        help='Launch GUI without starting backend server'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Backend server port (default: 8000)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    args = parser.parse_args()
    
    # Set debug logging
    if args.debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    
    # Launch the consolidated GUI
    success = launch_consolidated_gui(
        with_backend=not args.no_backend,
        port=args.port
    )
    
    if success:
        print("\n🎯 DAWN Consolidated GUI session completed")
    else:
        print("\n❌ GUI launch failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 