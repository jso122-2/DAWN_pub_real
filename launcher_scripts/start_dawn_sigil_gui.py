#!/usr/bin/env python3
"""
Fresh DAWN GUI Launcher with Sigil Overlay Panel
Uses queue-based communication between CoreTickEngine and GUI with SigilOverlayPanel.
"""

import tkinter as tk
import queue
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Launch DAWN GUI with SigilOverlayPanel"""
    print("🚀 DAWN Sigil GUI Launcher (Fresh)")
    print("=" * 40)
    
    # Create communication queue
    print("🔧 Creating communication queue...")
    comm_queue = queue.Queue(maxsize=100)
    
    # Import and initialize components
    print("📦 Importing DAWN components...")
    try:
        from gui.dawn_gui_tk import DAWNGui
        from tick_engine.core_tick import CoreTickEngine
        print("✅ Components imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return
    
    # Create GUI
    print("🖼️  Creating GUI...")
    root = tk.Tk()
    gui = DAWNGui(root, external_queue=comm_queue)
    
    # Create and start tick engine
    print("⚙️  Creating CoreTickEngine...")
    tick_engine = CoreTickEngine(comm_queue)
    
    print("🎯 Starting tick engine...")
    tick_engine.start()
    print("✅ Tick engine started")
    
    print("\n🌟 DAWN GUI Features Active:")
    print("   • Real-time fractal bloom visualization")
    print("   • Dynamic sigil overlay with house grouping")
    print("   • Heat-based color coding and decay animation")
    print("   • Live cognitive state monitoring")
    print("   • Queue-based communication")
    
    print("\n🎮 Interactive Features:")
    print("   • Hover over sigils for tooltips")
    print("   • Watch sigils decay in real-time")
    print("   • Monitor cognitive heat and zones")
    print("   • Observe fractal bloom signatures")
    
    print("\n🌸 Starting DAWN GUI... (Close window to exit)")
    
    try:
        # Run GUI main loop
        root.mainloop()
    except KeyboardInterrupt:
        print("\n⏹️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ GUI error: {e}")
    finally:
        print("\n🔄 Shutting down...")
        tick_engine.stop()
        print("✨ DAWN GUI shutdown complete")

if __name__ == "__main__":
    main() 