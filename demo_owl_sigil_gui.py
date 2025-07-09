#!/usr/bin/env python3
"""
Demo: DAWN GUI with Owl-Sigil Bridge Integration
================================================
Demonstrates the updated GUI with integrated owl console and sigil stream
connected through the owl-sigil bridge system.
"""

import sys
import os
import threading
import time
import random
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Launch the DAWN GUI with owl-sigil bridge integration"""
    
    print("🦉🔮 DAWN Owl-Sigil Bridge GUI Demo")
    print("=" * 50)
    print("Starting integrated cognitive monitoring interface...")
    
    try:
        # Import and launch the GUI
        from gui.dawn_gui_tk import main as gui_main
        
        print("✅ GUI components loaded successfully")
        print("🚀 Launching DAWN Cognitive Engine with:")
        print("   • Pulse Controller Integration")
        print("   • Entropy Analysis System") 
        print("   • Owl Cognitive Observer")
        print("   • Sigil Command Stream")
        print("   • Fractal Bloom Visualization")
        print("   • Real-time Bridge Monitoring")
        print()
        print("🎯 Features demonstrated:")
        print("   - Owl observations in terminal-style console")
        print("   - Sigil commands with decay tracking")
        print("   - Bridge activity monitoring")
        print("   - Real-time cognitive state visualization")
        print("   - Thermal regulation with visual feedback")
        print()
        print("📋 GUI Layout:")
        print("   Top: Pulse Controller | Main Monitoring")
        print("   Bottom: Fractal | Entropy | Owl Console | Sigils")
        print()
        print("🔄 Starting GUI... (Close window to exit)")
        print()
        
        # Launch the GUI main function
        gui_main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("⚠️  Make sure you're running from the project root directory")
        print("💡 Try: python demo_owl_sigil_gui.py")
        return 1
    
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        return 1
    
    print("👋 GUI closed. Demo complete!")
    return 0

if __name__ == "__main__":
    exit(main()) 