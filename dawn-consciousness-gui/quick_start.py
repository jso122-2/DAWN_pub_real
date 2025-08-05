#!/usr/bin/env python3
"""
DAWN Quick Start - Offline GUI
==============================

Simple launcher for the DAWN consciousness monitoring system.
Just run this and it opens a beautiful, professional GUI that works completely offline.
"""

import webbrowser
from pathlib import Path

def main():
    print("🧠 DAWN Consciousness Monitor - Quick Start")
    print("=" * 45)
    
    # Find the best GUI file
    gui_files = [
        "dawn_monitor_local.html",
        "simple_gui.html", 
        "dawn_local_gui.html"
    ]
    
    gui_file = None
    for filename in gui_files:
        if Path(filename).exists():
            gui_file = Path(filename)
            break
    
    if not gui_file:
        print("❌ No GUI file found!")
        print("📁 Available files:")
        for file in Path(".").glob("*.html"):
            print(f"   {file}")
        return 1
    
    print(f"🎨 Opening: {gui_file}")
    print("🌟 Features:")
    print("   • Real-time consciousness visualization")
    print("   • Fully offline - no internet required")
    print("   • Professional interface")
    print("   • 16Hz update rate")
    print("   • Neural activity monitoring")
    
    # Open in browser
    file_url = f"file:///{gui_file.absolute().as_posix()}"
    webbrowser.open(file_url)
    
    print("✅ DAWN Consciousness Monitor opened!")
    print("🛑 Close the browser tab when finished")
    
    return 0

if __name__ == "__main__":
    exit(main()) 