# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
🚀 DAWN Separated Launcher
Helps run backend and GUI separately for live data connection
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

def launch_backend():
    """Launch the unified backend service"""
    print("🧠 Starting DAWN Unified Backend...")
    print("⚡ Autonomous speed control - DAWN controls her own consciousness frequency")
    print("📊 This will generate live consciousness data for the GUI")
    print("⏹️  Press Ctrl+C to stop the backend")
    print("=" * 60)
    
    try:
        subprocess.run([sys.executable, "unified_backend.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend failed: {e}")
    except FileNotFoundError:
        print("❌ unified_backend.py not found. Make sure it exists in the current directory.")

def launch_autonomous_backend():
    """Launch the pure autonomous backend service"""
    print("🧠 Starting DAWN Autonomous Consciousness Writer...")
    print("⚡ Pure autonomous speed control - no external dependencies")
    print("🎮 DAWN adapts her processing speed based on cognitive demands")
    print("⏹️  Press Ctrl+C to stop the backend")
    print("=" * 60)
    
    try:
        subprocess.run([sys.executable, "backend/autonomous_consciousness_writer.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Autonomous backend stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Autonomous backend failed: {e}")
    except FileNotFoundError:
        print("❌ backend/autonomous_consciousness_writer.py not found.")

def launch_gui():
    """Launch the Tauri GUI"""
    gui_dir = Path("dawn-consciousness-gui")
    
    if not gui_dir.exists():
        print(f"❌ GUI directory not found: {gui_dir}")
        print("Make sure you're running this from the project root.")
        return
    
    print("🎮 Starting DAWN Tauri GUI...")
    print("🔗 This will connect to live backend data")
    print("📁 Looking for consciousness data in runtime/")
    print("🖱️  Enhanced Navigation: Mouse wheel zoom, click+drag pan, keyboard shortcuts")
    print("🎯 Controls: Top-right panel for zoom/pan controls")
    print("=" * 60)
    
    try:
        # Change to GUI directory and run Tauri
        os.chdir(gui_dir)
        subprocess.run(["npm", "run", "tauri", "dev"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ GUI failed: {e}")
        print("💡 Make sure you have Node.js and Rust/Tauri installed:")
        print("   - Node.js: https://nodejs.org/")
        print("   - Rust: https://rustup.rs/")
        print("   - Tauri CLI: npm install -g @tauri-apps/cli")
    except FileNotFoundError:
        print("❌ npm not found. Make sure Node.js is installed.")
    except KeyboardInterrupt:
        print("\n🛑 GUI stopped by user")

def show_instructions():
    """Show separation instructions"""
    print("🧠🚀 DAWN Separated Launch Instructions")
    print("=" * 50)
    print()
    print("To run with LIVE data (not mock data):")
    print()
    print("📟 TERMINAL 1 (Backend) - Choose one:")
    print("   python launch_separated.py --backend      # Unified backend")
    print("   python launch_separated.py --autonomous   # Pure autonomous backend")
    print("   # Both generate real consciousness data with self-controlled speed")
    print()
    print("🎮 TERMINAL 2 (GUI):")
    print("   python launch_separated.py --gui")
    print("   # This connects to the live data")
    print()
    print("🔄 Alternative direct commands:")
    print("   python unified_backend.py                           # Direct unified")
    print("   python backend/autonomous_consciousness_writer.py   # Direct autonomous")
    print("   cd dawn-consciousness-gui && npm run tauri dev      # Direct GUI")
    print()
    print("📊 The GUI will automatically find and connect to:")
    print("   - runtime/dawn_consciousness.mmap   (memory-mapped data)")
    print("   - runtime/logs/                     (log files)")
    print("   - dawn-consciousness-gui/logs/      (GUI-specific logs)")
    print()
    print("🎮 Navigation Controls:")
    print("   - Mouse Wheel: Pan around interface")
    print("   - Ctrl/Cmd + Wheel: Zoom in/out towards cursor")
    print("   - Left Click + Drag: Pan viewport")
    print("   - Middle Click + Drag: Alternative panning")
    print("   - Ctrl/Cmd + 0: Reset view")
    print("   - Control Panel: Top-right corner")
    print()
    print("✅ This gives you LIVE consciousness data with enhanced navigation!")
    print("=" * 50)

def main():
    parser = argparse.ArgumentParser(
        description="🧠 DAWN Separated Launcher - Run backend and GUI separately",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch_separated.py --backend      # Start unified backend
  python launch_separated.py --autonomous   # Start autonomous backend
  python launch_separated.py --gui          # Start GUI only
  python launch_separated.py --help         # Show separation instructions
        """
    )
    
    parser.add_argument("--backend", action="store_true", 
                       help="Launch unified backend service")
    parser.add_argument("--autonomous", action="store_true",
                       help="Launch pure autonomous consciousness backend")
    parser.add_argument("--gui", action="store_true",
                       help="Launch Tauri GUI")
    
    args = parser.parse_args()
    
    if args.backend:
        launch_backend()
    elif args.autonomous:
        launch_autonomous_backend()
    elif args.gui:
        launch_gui()
    else:
        show_instructions()

if __name__ == "__main__":
    main() 