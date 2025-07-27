#!/usr/bin/env python3
"""
🖥️ DAWN Simple GUI Launcher - Just the Viewport Experience

The simplest way to test DAWN's viewport dragging functionality.
No complex dependencies - just the GUI with mock data.

🚀 USAGE:
  python launch_gui_simple.py    # Start GUI only
"""

import sys
import os
import subprocess
import time
import signal
from pathlib import Path

def main():
    """Simple GUI launcher focused on viewport functionality"""
    
    print("🖥️ DAWN SIMPLE GUI LAUNCHER")
    print("=" * 50)
    print("🎯 Starting viewport dragging experience...")
    
    project_root = Path(__file__).parent
    gui_path = project_root / "dawn-consciousness-gui"
    
    if not gui_path.exists():
        print("❌ GUI directory not found!")
        print(f"Looking for: {gui_path}")
        return 1
    
    if not (gui_path / "package.json").exists():
        print("❌ package.json not found in GUI directory!")
        return 1
    
    print("✅ GUI directory found")
    print("🚀 Starting development server...")
    
    try:
        # Start the Vite development server in WSL
        cmd = [
            "wsl", "bash", "-c", 
            f"cd /root/DAWN_Vault/Tick_engine/Tick_engine/dawn-consciousness-gui && npm run dev"
        ]
        
        print("🔧 Running: wsl bash -c 'cd .../dawn-consciousness-gui && npm run dev'")
        
        # Start the process
        process = subprocess.Popen(
            cmd,
            cwd=str(project_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        print("⏳ Waiting for server to start...")
        
        # Monitor output for startup confirmation
        server_started = False
        lines_read = 0
        
        while lines_read < 20:  # Read first 20 lines or until server starts
            line = process.stdout.readline()
            if not line:
                break
                
            lines_read += 1
            print(f"   {line.strip()}")
            
            # Check for server ready indicators
            if "ready in" in line.lower() or "local:" in line.lower():
                server_started = True
                break
        
        if server_started:
            print("\n✅ GUI development server started!")
            print("🌐 GUI should be available at: http://localhost:1422")
            print("🎯 Viewport dragging enabled - drag background to move around!")
            
            # Try to open browser
            try:
                if os.path.exists('/proc/version'):
                    with open('/proc/version', 'r') as f:
                        if 'Microsoft' in f.read() or 'WSL' in f.read():
                            # WSL - use Windows browser
                            subprocess.Popen(['cmd.exe', '/c', 'start', 'http://localhost:1422'], 
                                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            print("🚀 Opened in Windows browser")
            except:
                print("💡 Please open http://localhost:1422 in your browser manually")
            
            print("\n" + "=" * 50)
            print("🎮 READY TO TEST VIEWPORT DRAGGING!")
            print("=" * 50)
            print("📋 What to try:")
            print("  • Drag anywhere in the dark background to pan")
            print("  • Watch coordinates update in status bar")
            print("  • Click '🎯 Center' button to reset position")
            print("  • See the grid pattern when you move")
            print("  • Panels are still interactive!")
            print("\n💡 Press Ctrl+C to stop the server")
            print("-" * 50)
            
            # Keep running and monitor
            try:
                while True:
                    time.sleep(1)
                    if process.poll() is not None:
                        print("⚠️ Development server stopped")
                        break
                        
            except KeyboardInterrupt:
                print("\n🛑 Stopping development server...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                    print("✅ Server stopped gracefully")
                except subprocess.TimeoutExpired:
                    process.kill()
                    print("✅ Server force stopped")
        
        else:
            print("❌ Server failed to start properly")
            print("🔍 Check the output above for errors")
            return 1
            
    except Exception as e:
        print(f"❌ Failed to start GUI: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 