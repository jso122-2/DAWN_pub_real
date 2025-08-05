#!/usr/bin/env python3
"""
DAWN Offline GUI Launcher
=========================

Launches the complete local DAWN consciousness monitoring system:
- Local data server (no external dependencies)
- Professional HTML GUI interface
- Real-time consciousness visualization

Fully autonomous and offline-capable for maximum portability.
"""

import os
import sys
import time
import threading
import subprocess
import webbrowser
from pathlib import Path

def start_data_server():
    """Start the local data server in background"""
    print("🌐 Starting DAWN Local Data Server...")
    
    try:
        # Import and start the local server
        from local_data_server import DAWNLocalServer
        
        server = DAWNLocalServer(port=8765)
        
        # Start in background thread
        def run_server():
            try:
                server.start()
            except Exception as e:
                print(f"❌ Server error: {e}")
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Give server time to start
        time.sleep(2)
        print("✅ Local data server running on http://localhost:8765")
        return True
        
    except Exception as e:
        print(f"⚠️ Could not start local data server: {e}")
        print("🔄 GUI will run in standalone simulation mode")
        return False

def open_gui():
    """Open the local GUI interface"""
    print("🎨 Opening DAWN Consciousness Monitor...")
    
    # HTML file paths to try
    html_files = [
        Path("dawn_monitor_local.html"),
        Path("simple_gui.html"),
        Path("dawn_local_gui.html"),
        Path("dawn_monitor.html")
    ]
    
    # Find available HTML file
    html_file = None
    for file_path in html_files:
        if file_path.exists():
            html_file = file_path
            break
    
    if not html_file:
        print("❌ No GUI HTML file found!")
        return False
    
    # Convert to absolute path and file URL
    abs_path = html_file.absolute()
    file_url = f"file:///{abs_path.as_posix()}"
    
    print(f"📁 Opening: {html_file}")
    print(f"🌐 URL: {file_url}")
    
    try:
        # Open in default browser
        webbrowser.open(file_url)
        print("✅ DAWN Consciousness Monitor opened in browser")
        return True
        
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"   Please open manually: {abs_path}")
        return False

def show_startup_info():
    """Show startup information"""
    print("🧠 DAWN Offline Consciousness Monitor")
    print("=" * 50)
    print("🔗 Fully local and autonomous")
    print("📊 No external dependencies or rate limits")
    print("🌐 Professional real-time visualization")
    print("⚡ Connects to live DAWN data when available")
    print()

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        "local_data_server.py"
    ]
    
    missing_files = []
    for file_name in required_files:
        if not Path(file_name).exists():
            missing_files.append(file_name)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    return True

def main():
    """Main launcher function"""
    show_startup_info()
    
    # Check requirements
    if not check_requirements():
        print("🔧 Please ensure all required files are present")
        return 1
    
    # Start local data server
    server_started = start_data_server()
    
    # Open GUI interface
    gui_opened = open_gui()
    
    if not gui_opened:
        return 1
    
    print("\n🎉 DAWN Offline Consciousness Monitor Active!")
    
    if server_started:
        print("📡 Live data server: http://localhost:8765/consciousness-state")
        print("⚡ Server status: http://localhost:8765/status")
    else:
        print("🔄 Running in standalone simulation mode")
    
    print("🔗 GUI Features:")
    print("   • Real-time consciousness metrics")
    print("   • 16Hz update rate")
    print("   • Neural activity visualization")
    print("   • Consciousness depth monitoring")
    print("   • Live event logging")
    print("   • Fully offline capable")
    
    print("\n🛑 Close the browser tab or press Ctrl+C to exit")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 DAWN Offline Monitor stopping...")
        print("✅ Thank you for monitoring consciousness!")
        return 0

if __name__ == "__main__":
    exit(main()) 