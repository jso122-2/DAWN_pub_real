#!/usr/bin/env python3
"""
DAWN HTML GUI Launcher
======================

Opens the HTML-based consciousness monitor in a browser
"""

import webbrowser
import os
from pathlib import Path

def main():
    """Open the HTML GUI in a browser"""
    print("🌐 Launching DAWN HTML Consciousness Monitor...")
    
    # Get the path to the HTML file
    html_path = Path("dawn_monitor.html")
    
    if not html_path.exists():
        print(f"❌ HTML file not found: {html_path}")
        return 1
        
    # Convert to absolute path
    abs_path = html_path.absolute()
    
    # Convert to file:// URL
    file_url = f"file:///{abs_path.as_posix()}"
    
    print(f"📁 Opening: {file_url}")
    
    try:
        # Open in default browser
        webbrowser.open(file_url)
        print("✅ HTML GUI opened in browser")
        print("   The GUI will show simulated consciousness data")
        print("   Close the browser tab to exit")
        
        return 0
        
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print("   Try opening the file manually:")
        print(f"   {abs_path}")
        return 1

if __name__ == "__main__":
    exit(main()) 