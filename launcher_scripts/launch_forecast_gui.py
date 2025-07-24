#!/usr/bin/env python3
"""
DAWN Forecast GUI Launcher
Launches the integrated DAWN forecasting visualizer with proper environment setup.
"""

import sys
import os
from pathlib import Path
import subprocess

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def launch_forecast_gui():
    """Launch the DAWN Forecast Visualizer."""
    print("🔮 Launching DAWN Forecast Visualizer...")
    
    # Check for required dependencies
    try:
        import tkinter
        print("✅ Tkinter available")
    except ImportError:
        print("❌ Tkinter not available - GUI cannot run")
        print("   Install tkinter: sudo apt-get install python3-tk (Linux)")
        return False
    
    # Check for DAWN components
    try:
        from cognitive.forecasting_models import Passion, Acquaintance, ForecastVector
        from cognitive.forecasting_engine import get_forecasting_engine
        from core.consciousness_core import DAWNConsciousness
        print("✅ DAWN forecasting components available")
    except ImportError as e:
        print(f"⚠️ DAWN components not fully available: {e}")
        print("   GUI will run in limited mode")
    
    # Launch the GUI
    try:
        gui_path = project_root / "gui" / "dawn_forecast_visualizer.py"
        
        if gui_path.exists():
            # Import and run the GUI
            from gui.dawn_forecast_visualizer import main
            main()
        else:
            print(f"❌ GUI file not found at {gui_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = launch_forecast_gui()
    if not success:
        sys.exit(1) 