#!/usr/bin/env python3
"""
DAWN GUI Safe Launcher - Clean structured output
Uses comprehensive safe sigil processing to eliminate undefined errors
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
logger = CleanLogger("DAWN-SAFE")

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.warning("Interrupt signal received - initiating shutdown")
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
    """Main launcher with clean output"""
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    clean_section_header("DAWN GUI System Launcher")
    
    logger.info("Initializing queue-based communication")
    data_queue = queue.Queue(maxsize=100)
    
    logger.info("Setting up GUI with SigilOverlayPanel")
    
    # Initialize systems with error handling
    tick_engine = None
    gui = None
    tick_thread = None
    
    try:
        # Initialize tick engine
        logger.info("Creating CoreTickEngine")
        tick_engine = CoreTickEngine(data_queue=data_queue, tick_interval=0.5)
        logger.success("Tick engine initialized", {
            "interval": "0.5s",
            "safe_mode": True
        })
        
        # Initialize GUI
        logger.info("Creating DAWN GUI with safe sigil processing")
        root = tk.Tk()
        gui = DAWNGui(root=root, external_queue=data_queue)
        logger.success("GUI initialized with external queue")
        
        # Start tick engine in background
        logger.info("Starting DAWN tick engine")
        tick_thread = threading.Thread(
            target=run_tick_engine, 
            args=(tick_engine,),
            daemon=True,
            name="TickEngine"
        )
        tick_thread.start()
        logger.success("Tick engine thread started")
        
        # Display system status
        logger.status_list({
            "Queue Communication": True,
            "CoreTickEngine": tick_engine is not None,
            "DAWN GUI": gui is not None,
            "SigilOverlayPanel": hasattr(gui, 'sigil_panel'),
            "Safe Processing": True
        }, "System Status")
        
        # Show feature list
        logger.subsection("DAWN GUI Features")
        features = [
            "Real-time fractal bloom visualization",
            "Dynamic sigil overlay with house grouping", 
            "Heat-based color coding and decay animation",
            "Live cognitive state monitoring",
            "Queue-based tick engine communication",
            "Safe sigil processing (no undefined errors)"
        ]
        for feature in features:
            print(f"  • {feature}")
        
        logger.subsection("GUI Controls")
        controls = [
            "Hover over sigils for tooltips",
            "Watch sigils decay in real-time", 
            "Monitor cognitive heat and zones",
            "Observe fractal bloom signatures",
            "Close window to shutdown all systems"
        ]
        for control in controls:
            print(f"  • {control}")
        
        logger.info("Starting DAWN GUI")
        logger.info("Close window to shutdown all systems")
        
        # Start GUI main loop
        root.mainloop()
        
    except KeyboardInterrupt:
        logger.warning("Keyboard interrupt received")
    except Exception as e:
        logger.error("System initialization failed", {
            "error": str(e),
            "error_type": type(e).__name__
        })
    finally:
        # Cleanup
        logger.info("Shutting down systems")
        
        if tick_engine:
            try:
                tick_engine.stop()
                logger.success("Tick engine stopped")
            except Exception as e:
                logger.warning("Tick engine cleanup failed", {"error": str(e)})
        
        if tick_thread and tick_thread.is_alive():
            logger.info("Waiting for tick thread to finish")
            tick_thread.join(timeout=2.0)
            if tick_thread.is_alive():
                logger.warning("Tick thread did not terminate cleanly")
        
        clean_section_footer("DAWN GUI System")

if __name__ == "__main__":
    main() 