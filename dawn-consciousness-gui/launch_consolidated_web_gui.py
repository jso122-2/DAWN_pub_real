#!/usr/bin/env python3
"""
DAWN Consolidated Web GUI Launcher
Launch the unified tab-based web interface on localhost:3000
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path
import argparse

def main():
    """Launch the consolidated DAWN web GUI"""
    parser = argparse.ArgumentParser(
        description="Launch DAWN Consolidated Web GUI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch_consolidated_web_gui.py                    # Launch GUI with auto-open browser
  python launch_consolidated_web_gui.py --no-browser      # Launch GUI without opening browser
  python launch_consolidated_web_gui.py --port 3001       # Launch on custom port
        """
    )
    
    parser.add_argument(
        '--no-browser',
        action='store_true',
        help='Don\'t automatically open browser'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=3000,
        help='Port to run GUI server on (default: 3000)'
    )
    
    args = parser.parse_args()
    
    print("🌅 DAWN Consolidated Web GUI Launcher")
    print("=" * 50)
    print("🎯 Starting unified tab-based interface...")
    print()
    
    # Check if consolidated GUI file exists
    gui_file = Path(__file__).parent / 'dawn_consolidated_gui.html'
    if not gui_file.exists():
        print("❌ Consolidated GUI file not found!")
        print(f"   Expected: {gui_file}")
        print("💡 Make sure dawn_consolidated_gui.html exists")
        return 1
    
    print(f"✅ Found consolidated GUI: {gui_file.name}")
    print()
    
    # Start the web server
    try:
        print(f"🚀 Starting web server on port {args.port}...")
        print(f"🎨 Serving consolidated tab-based interface")
        print(f"🔄 Will proxy API calls to real DAWN backend (port 8080)")
        print()
        
        # Modify the server script to use custom port if needed
        if args.port != 3000:
            print(f"⚙️ Using custom port: {args.port}")
        
        # Start the server
        server_script = Path(__file__).parent / 'real_aware_web_server.py'
        if not server_script.exists():
            print(f"❌ Web server script not found: {server_script}")
            return 1
        
        # Run the server
        env = {}
        if args.port != 3000:
            env['GUI_SERVER_PORT'] = str(args.port)
        
        # Inform user about the interface
        print("📊 Consolidated Interface Features:")
        print("   🖼️  Visual Tab - Fractal/bloom/sigil rendering")
        print("   🗣️  Voice Tab - Audio synthesis with pigment visualization")
        print("   📊 State Monitor - Real-time DAWN cognitive status")
        print("   ⚙️  Controls - System configuration and manual triggers")
        print("   📚 Archive - Expression history and search")
        print("   📋 Logs - System logging and debugging")
        print()
        
        print(f"🌐 Interface will be available at: http://localhost:{args.port}")
        print("⚡ Backend expected at: http://localhost:8080")
        print()
        
        if not args.no_browser:
            print("🌐 Browser will open automatically in 3 seconds...")
            time.sleep(3)
            try:
                webbrowser.open(f"http://localhost:{args.port}")
                print("✅ Browser opened successfully")
            except Exception as e:
                print(f"⚠️ Could not open browser automatically: {e}")
                print(f"💡 Manually open: http://localhost:{args.port}")
        else:
            print(f"💡 Open your browser to: http://localhost:{args.port}")
        
        print()
        print("🚀 Starting consolidated web server...")
        print("💡 Press Ctrl+C to stop")
        print()
        
        # Start the server process
        if args.port != 3000:
            # Create a temporary modified server script for custom port
            server_content = server_script.read_text()
            server_content = server_content.replace(
                'GUI_SERVER_PORT = 3000',
                f'GUI_SERVER_PORT = {args.port}'
            )
            
            temp_server = Path(__file__).parent / f'temp_server_{args.port}.py'
            temp_server.write_text(server_content)
            
            try:
                subprocess.run([sys.executable, str(temp_server)], cwd=str(Path(__file__).parent))
            finally:
                # Clean up temp file
                if temp_server.exists():
                    temp_server.unlink()
        else:
            subprocess.run([sys.executable, str(server_script)], cwd=str(Path(__file__).parent))
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        print("🎯 DAWN Consolidated Web GUI session completed")
    except Exception as e:
        print(f"❌ Failed to start web server: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 