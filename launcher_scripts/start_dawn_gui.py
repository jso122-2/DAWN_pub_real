#!/usr/bin/env python3
"""
DAWN GUI Launcher - Unified System
Legacy launcher updated to use the new unified system
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Main launcher - now redirects to unified launcher"""
    print("🌊 DAWN GUI Launcher")
    print("=" * 40)
    print("📍 Redirecting to unified launcher system...")
    print()
    
    # Check if unified launcher exists
    unified_launcher = Path("dawn_unified_launcher.py")
    if unified_launcher.exists():
        print("🚀 Using DAWN Unified Launcher")
        
        # Parse any old-style arguments and convert to new format
        args = sys.argv[1:] if len(sys.argv) > 1 else []
        
        if "--standalone" in args:
            # Convert old standalone flag to websocket mode
            subprocess.run([sys.executable, "dawn_unified_launcher.py", "--mode", "websocket", "--no-backend"])
        elif "--with-engine" in args:
            # Convert old engine flag to tick-engine mode
            subprocess.run([sys.executable, "dawn_unified_launcher.py", "--mode", "tick-engine"])
        else:
            # Default to demo mode (backend + gui)
            subprocess.run([sys.executable, "dawn_unified_launcher.py", "--mode", "demo"])
    else:
        print("❌ Unified launcher not found!")
        print("💡 Falling back to legacy GUI...")
        
        # Fall back to original implementation
        try:
            from dawn_tkinter_gui import main as legacy_main
            legacy_main()
        except ImportError:
            print("❌ Legacy GUI also not available!")
            print("📦 Please ensure all components are properly installed")
            sys.exit(1)

if __name__ == "__main__":
    main() 