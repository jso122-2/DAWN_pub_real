#!/usr/bin/env python3
"""
DAWN Unified Launcher
Single entry point for all DAWN GUI and backend options
Integrates: WebSocket GUI, Enhanced GUI, Local GUI, Backend Server
"""

import subprocess
import sys
import time
import os
import threading
import argparse
import queue
from pathlib import Path
from typing import Optional, Dict, Any

def check_dependencies():
    """Check and install required dependencies"""
    print("🔍 Checking dependencies...")
    
    required_packages = {
        'matplotlib': 'matplotlib',
        'numpy': 'numpy',
        'websocket': 'websocket-client',
        'tkinter': None  # Built into Python
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            if package == 'tkinter':
                import tkinter
                print(f"✅ {package}")
            elif package == 'websocket':
                import websocket
                print(f"✅ {package}")
            else:
                __import__(package)
                print(f"✅ {package}")
        except ImportError:
            if pip_name:
                missing_packages.append(pip_name)
            print(f"❌ {package} - missing")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print(f"📦 Install with: pip install {' '.join(missing_packages)}")
        
        response = input("\n🤔 Install missing packages automatically? (y/n): ").lower()
        if response == 'y':
            print("📦 Installing packages...")
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ Installation complete!")
        else:
            print("⚠️ Some features may not work without required packages")
        
    print("✅ Dependency check complete!")
    return len(missing_packages) == 0

def check_dawn_components():
    """Check availability of DAWN components"""
    print("\n🔍 Checking DAWN components...")
    
    components = {
        'core': ['core.pulse_controller', 'core.sigil_engine'],
        'reflex': ['reflex.reflex_executor', 'reflex.owl_panel'],
        'gui': ['gui.dawn_gui_tk', 'gui.dawn_gui_enhanced'],
        'backend': ['backend.main', 'backend.advanced_consciousness_system']
    }
    
    available = {}
    
    for category, modules in components.items():
        available[category] = []
        for module in modules:
            try:
                __import__(module)
                available[category].append(module)
                print(f"✅ {module}")
            except ImportError:
                print(f"❌ {module}")
    
    return available

def start_backend_server(port=8000):
    """Start DAWN backend server"""
    print(f"🚀 Starting DAWN backend server on port {port}...")
    
    backend_scripts = [
        "backend/main.py",
        "backend/start_api_fixed.py",
        "backend/advanced_consciousness_websocket.py"
    ]
    
    for script in backend_scripts:
        if Path(script).exists():
            print(f"📍 Using backend script: {script}")
            
            def run_backend():
                try:
                    subprocess.run([sys.executable, script], cwd=Path("."))
                except Exception as e:
                    print(f"❌ Backend error: {e}")
            
            backend_thread = threading.Thread(target=run_backend)
            backend_thread.daemon = True
            backend_thread.start()
            
            print(f"✅ Backend server starting...")
            return True
    
    print("❌ No backend script found!")
    return False

def launch_unified_gui(external_queue=None):
    """Launch the unified GUI"""
    print("🖼️ Starting DAWN Unified GUI...")
    
    try:
        # Try to import and launch the unified GUI
        try:
            from gui.dawn_gui_unified import DAWNUnifiedGUI
        except ImportError:
            from dawn_tkinter_gui import DAWNVisualizationGUI as DAWNUnifiedGUI
        
        import tkinter as tk
        
        root = tk.Tk()
        app = DAWNUnifiedGUI(root, external_queue=external_queue)
        
        def on_closing():
            app.on_closing()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        print("✅ Unified GUI launched successfully!")
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Failed to launch unified GUI: {e}")
        return False
    
    return True

def launch_enhanced_gui():
    """Launch the enhanced GUI with reflex components"""
    print("🤖 Starting Enhanced DAWN GUI...")
    
    try:
        from gui.dawn_gui_enhanced import EnhancedDAWNGui
        import tkinter as tk
        
        root = tk.Tk()
        app = EnhancedDAWNGui(root)
        
        print("✅ Enhanced GUI launched successfully!")
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Enhanced GUI not available: {e}")
        print("💡 Falling back to unified GUI...")
        return launch_unified_gui()
    except Exception as e:
        print(f"❌ Failed to launch enhanced GUI: {e}")
        return False
    
    return True

def launch_standard_gui():
    """Launch the standard DAWN GUI"""
    print("🔧 Starting Standard DAWN GUI...")
    
    try:
        from gui.dawn_gui_tk import DAWNGui
        import tkinter as tk
        
        root = tk.Tk()
        app = DAWNGui(root)
        
        print("✅ Standard GUI launched successfully!")
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Standard GUI not available: {e}")
        print("💡 Falling back to unified GUI...")
        return launch_unified_gui()
    except Exception as e:
        print(f"❌ Failed to launch standard GUI: {e}")
        return False
    
    return True

def launch_websocket_only_gui():
    """Launch WebSocket-only GUI"""
    print("🌐 Starting WebSocket-only GUI...")
    
    try:
        from dawn_tkinter_gui import DAWNVisualizationGUI
        import tkinter as tk
        
        root = tk.Tk()
        app = DAWNVisualizationGUI(root)
        
        print("✅ WebSocket GUI launched successfully!")
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Failed to launch WebSocket GUI: {e}")
        return False
    
    return True

def launch_with_tick_engine():
    """Launch GUI with integrated tick engine"""
    print("⚙️ Starting DAWN with integrated tick engine...")
    
    try:
        # Create communication queue
        comm_queue = queue.Queue(maxsize=100)
        
        # Start tick engine
        try:
            from tick_engine.core_tick import CoreTickEngine
            
            tick_engine = CoreTickEngine(comm_queue)
            tick_engine.start()
            
            print("✅ Tick engine started")
            
            # Launch GUI with queue
            return launch_unified_gui(external_queue=comm_queue)
            
        except ImportError:
            print("❌ Tick engine not available")
            return launch_unified_gui()
            
    except Exception as e:
        print(f"❌ Failed to launch with tick engine: {e}")
        return False

def launch_demo_mode():
    """Launch in demonstration mode"""
    print("🎭 Starting DAWN Demo Mode...")
    
    # Start backend if available
    backend_started = start_backend_server()
    
    if backend_started:
        print("⏳ Waiting for backend to initialize...")
        time.sleep(3)
    
    # Launch unified GUI which will auto-detect data sources
    return launch_unified_gui()

def launch_console_mode():
    """Launch console-only mode"""
    print("💻 Starting DAWN Console Mode...")
    
    try:
        # Try to import and run console interface
        from run_dawn_unified import main as console_main
        console_main()
        
    except ImportError:
        print("❌ Console mode not available")
        print("💡 Starting basic backend server...")
        start_backend_server()
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Console mode stopped")

def main():
    """Main launcher entry point"""
    print("🌊 DAWN Unified System Launcher")
    print("=" * 50)
    
    parser = argparse.ArgumentParser(description="DAWN Unified System Launcher")
    parser.add_argument('--mode', choices=[
        'auto', 'unified', 'enhanced', 'standard', 'websocket', 
        'tick-engine', 'demo', 'console', 'backend-only'
    ], default='auto', help='Launch mode')
    parser.add_argument('--port', type=int, default=8000, help='Backend server port')
    parser.add_argument('--no-backend', action='store_true', help='Skip backend server')
    parser.add_argument('--check-deps', action='store_true', help='Check dependencies only')
    parser.add_argument('--components', action='store_true', help='Check component availability')
    
    args = parser.parse_args()
    
    # Check dependencies if requested
    if args.check_deps:
        check_dependencies()
        return
    
    # Check components if requested
    if args.components:
        available = check_dawn_components()
        print(f"\n📊 Component Summary:")
        for category, modules in available.items():
            print(f"  {category}: {len(modules)} available")
        return
    
    # Quick dependency check
    if not check_dependencies():
        print("⚠️ Some dependencies missing - continuing anyway...")
    
    # Determine launch mode
    if args.mode == 'auto':
        print("\n🎯 Auto-detecting best launch mode...")
        
        # Check what's available
        available = check_dawn_components()
        
        if available['reflex']:
            mode = 'enhanced'
            print("🤖 Enhanced GUI mode selected (reflex components available)")
        elif available['gui']:
            mode = 'unified'
            print("🌊 Unified GUI mode selected (standard components available)")
        else:
            mode = 'websocket'
            print("🌐 WebSocket GUI mode selected (minimal dependencies)")
    else:
        mode = args.mode
        print(f"\n🎯 Launch mode: {mode}")
    
    # Start backend server unless disabled
    if not args.no_backend and mode not in ['console', 'backend-only']:
        backend_started = start_backend_server(args.port)
        
        if backend_started:
            print("⏳ Waiting for backend to initialize...")
            time.sleep(2)
    
    # Launch based on mode
    try:
        if mode == 'unified':
            success = launch_unified_gui()
        elif mode == 'enhanced':
            success = launch_enhanced_gui()
        elif mode == 'standard':
            success = launch_standard_gui()
        elif mode == 'websocket':
            success = launch_websocket_only_gui()
        elif mode == 'tick-engine':
            success = launch_with_tick_engine()
        elif mode == 'demo':
            success = launch_demo_mode()
        elif mode == 'console':
            success = launch_console_mode()
        elif mode == 'backend-only':
            success = start_backend_server(args.port)
            if success:
                print("🖥️ Backend server running. Press Ctrl+C to stop.")
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n👋 Backend server stopped")
        else:
            print(f"❌ Unknown mode: {mode}")
            success = False
        
        if success:
            print("\n✅ DAWN launcher completed successfully!")
        else:
            print("\n❌ DAWN launcher encountered errors")
            
    except KeyboardInterrupt:
        print("\n👋 DAWN launcher interrupted by user")
    except Exception as e:
        print(f"\n❌ DAWN launcher error: {e}")

if __name__ == "__main__":
    main() 