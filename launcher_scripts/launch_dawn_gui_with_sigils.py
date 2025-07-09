#!/usr/bin/env python3

"""
DAWN GUI Launcher with Sigil Overlay Panel - Clean Version
Professional structured output without emoji characters
"""

import sys
import threading
import queue
import signal
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.clean_logger import CleanLogger, clean_section_header, clean_section_footer
from tick_engine.core_tick import CoreTickEngine
from gui.dawn_gui_tk import DAWNGui
import tkinter as tk

# Initialize clean logger
logger = CleanLogger("DAWN-SIGILS")

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.warning("Interrupt signal received")
    sys.exit(0)

def run_tick_engine(tick_engine):
    """Run tick engine in background thread"""
    try:
        logger.tick("Starting tick engine background thread")
        tick_engine.start()
    except Exception as e:
        logger.error("Tick engine failed", {
            "error": str(e),
            "error_type": type(e).__name__
        })

def main():
    """Main application launcher"""
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # System initialization
        clean_section_header("DAWN GUI SYSTEM LAUNCHER")
        logger.info("Initializing queue-based communication")
        
        # Create communication queue
        data_queue = queue.Queue(maxsize=100)
        logger.success("Communication queue created", {"maxsize": 100})
        
        # Initialize GUI first
        logger.info("Setting up GUI with SigilOverlayPanel")
        root = tk.Tk()
        gui = DAWNGui(root=root, external_queue=data_queue)
        logger.success("GUI system prepared")
        
        # Initialize tick engine
        logger.info("Starting DAWN tick engine")
        tick_engine = CoreTickEngine(data_queue=data_queue, tick_interval=0.5)
        logger.success("Tick engine configured", {"interval": "0.5s"})
        
        # Start tick engine in background thread
        tick_thread = threading.Thread(
            target=run_tick_engine, 
            args=(tick_engine,),
            daemon=True,
            name="TickEngine"
        )
        tick_thread.start()
        logger.tick("Tick engine thread started")
        
        # Startup complete
        logger.success("All systems initialized")
        
        # System capabilities
        logger.system("DAWN GUI Features", {
            "fractal_visualization": "Real-time bloom rendering",
            "sigil_overlay": "Dynamic house grouping with heat coloring", 
            "decay_animation": "Real-time sigil lifecycle visualization",
            "cognitive_monitoring": "Live state tracking",
            "queue_communication": "Thread-safe tick engine integration"
        })
        
        logger.system("GUI Controls", {
            "sigil_tooltips": "Hover over sigils for details",
            "decay_monitoring": "Watch sigils decay in real-time",
            "heat_zones": "Monitor cognitive heat and zones",
            "fractal_signatures": "Observe bloom visualization",
            "shutdown": "Close window to shutdown all systems"
        })
        
        logger.info("Starting DAWN GUI")
        clean_section_footer("DAWN GUI SYSTEM LAUNCHER")
        
        # Start GUI main loop
        root.mainloop()
        
    except Exception as e:
        logger.error("System initialization failed", {
            "error": str(e),
            "error_type": type(e).__name__
        })
    finally:
        # Shutdown systems
        logger.info("Shutting down systems")
        if 'tick_engine' in locals():
            tick_engine.stop()
        
        logger.success("DAWN GUI system shutdown complete")

if __name__ == "__main__":
    main() 