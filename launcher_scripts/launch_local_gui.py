#!/usr/bin/env python3
"""
🖥️ DAWN Local GUI Launcher - 100% Local Experience

Launches the DAWN consciousness GUI as a local HTML file.
No servers, no dependencies, no network connections required.
Pure local operation as per project requirements.

🚀 USAGE:
  python launch_local_gui.py    # Opens local GUI directly
"""

import sys
import os
import subprocess
import webbrowser
from pathlib import Path

def main():
    """Launch the local DAWN GUI"""
    
    print("🖥️ DAWN LOCAL GUI LAUNCHER")
    print("=" * 50)
    print("🎯 100% Local Experience - No External Dependencies")
    
    project_root = Path(__file__).parent
    gui_file = project_root / "dawn_local_gui.html"
    
    if not gui_file.exists():
        print("❌ Local GUI file not found!")
        print(f"Looking for: {gui_file}")
        print("Please ensure dawn_local_gui.html exists in this directory.")
        return 1
    
    print("✅ Local GUI file found")
    print(f"📁 File: {gui_file}")
    
    # Get absolute path for browser
    gui_url = f"file://{gui_file.absolute()}"
    
    print(f"🌐 Opening: {gui_url}")
    
    try:
        # Check environment and open appropriately
        if os.name == 'nt':  # Windows
            os.startfile(str(gui_file))
            print("✅ Opened with default Windows browser")
            
        elif os.path.exists('/proc/version'):
            # Check if we're in WSL
            with open('/proc/version', 'r') as f:
                version_info = f.read()
                if 'Microsoft' in version_info or 'WSL' in version_info:
                    # WSL - use Windows browser via cmd
                    subprocess.Popen([
                        'cmd.exe', '/c', 'start', '', str(gui_file.absolute())
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    print("✅ Opened via WSL → Windows browser")
                else:
                    # Regular Linux
                    subprocess.Popen([
                        'xdg-open', str(gui_file.absolute())
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    print("✅ Opened with Linux default browser")
        else:
            # Fallback to webbrowser module
            webbrowser.open(gui_url)
            print("✅ Opened with Python webbrowser module")
            
    except Exception as e:
        print(f"⚠️ Auto-open failed: {e}")
        print(f"💡 Please manually open: {gui_url}")
        print("   Or drag the dawn_local_gui.html file into your browser")
        return 1
    
    print("\n" + "=" * 50)
    print("🎮 DAWN LOCAL GUI READY!")
    print("=" * 50)
    print("🎯 VIEWPORT FEATURES:")
    print("  • Drag dark background to pan around")
    print("  • Watch coordinates update in status bar")
    print("  • Click '🎯 Center' to reset position")
    print("  • See grid pattern when moving")
    print("  • All panels remain interactive")
    print("\n📊 LIVE FEATURES:")
    print("  • Real-time consciousness simulation")
    print("  • Live entropy/tick updates")
    print("  • Dynamic reflection stream")
    print("  • Simulated sigil traces")
    print("\n🛡️ 100% LOCAL:")
    print("  • No servers required")
    print("  • No network connections")
    print("  • No external dependencies")
    print("  • Pure local HTML/CSS/JS")
    
    print(f"\n📁 Local file: {gui_file.name}")
    print("💡 You can bookmark this file for instant access!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 