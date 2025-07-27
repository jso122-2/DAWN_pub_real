#!/usr/bin/env python3
"""
DAWN Master Clean Launcher
Professional, emoji-free DAWN consciousness system
Combines fractal visualization, sigil overlay, and tick engine
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

class DAWNMasterSystem:
    """Master DAWN system with clean, professional output"""
    
    def __init__(self):
        self.logger = CleanLogger("DAWN-MASTER")
        self.data_queue = None
        self.tick_engine = None
        self.gui = None
        self.root = None
        self.tick_thread = None
        self.running = False
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.warning("Interrupt signal received - initiating shutdown")
        self.shutdown()
        sys.exit(0)
        
    def initialize_communication(self):
        """Initialize the queue-based communication system"""
        try:
            self.logger.info("Initializing communication queue")
            self.data_queue = queue.Queue(maxsize=100)
            self.logger.success("Communication queue created", {
                "maxsize": 100,
                "type": "thread_safe"
            })
            return True
        except Exception as e:
            self.logger.error("Failed to initialize communication", {
                "error": str(e),
                "error_type": type(e).__name__
            })
            return False
    
    def initialize_tick_engine(self):
        """Initialize the core tick engine"""
        try:
            self.logger.info("Creating core tick engine")
            self.tick_engine = CoreTickEngine(
                data_queue=self.data_queue, 
                tick_interval=0.5
            )
            self.logger.success("Tick engine initialized", {
                "interval": "0.5s",
                "queue_integration": True
            })
            return True
        except Exception as e:
            self.logger.error("Failed to initialize tick engine", {
                "error": str(e),
                "error_type": type(e).__name__
            })
            return False
    
    def initialize_gui(self):
        """Initialize the GUI system with fractal and sigil components"""
        try:
            self.logger.info("Creating GUI system")
            self.root = tk.Tk()
            self.root.title("DAWN Consciousness System - Professional Build")
            self.root.configure(bg="#1a1a1a")
            
            # Create DAWN GUI with external queue
            self.gui = DAWNGui(root=self.root, external_queue=self.data_queue)
            
            self.logger.success("GUI system initialized", {
                "fractal_canvas": True,
                "sigil_overlay": True,
                "external_queue": True
            })
            return True
        except Exception as e:
            self.logger.error("Failed to initialize GUI", {
                "error": str(e),
                "error_type": type(e).__name__
            })
            return False
    
    def start_tick_engine(self):
        """Start the tick engine in background thread"""
        try:
            self.logger.info("Starting tick engine thread")
            
            def run_tick_engine():
                try:
                    self.logger.tick("Tick engine thread starting")
                    self.tick_engine.start()
                except Exception as e:
                    self.logger.error("Tick engine thread failed", {
                        "error": str(e),
                        "error_type": type(e).__name__
                    })
            
            self.tick_thread = threading.Thread(
                target=run_tick_engine,
                daemon=True,
                name="DAWNTickEngine"
            )
            self.tick_thread.start()
            
            self.logger.success("Tick engine thread started")
            return True
        except Exception as e:
            self.logger.error("Failed to start tick engine", {
                "error": str(e),
                "error_type": type(e).__name__
            })
            return False
    
    def display_system_status(self):
        """Display comprehensive system status"""
        status = {
            "communication_queue": "ACTIVE" if self.data_queue else "FAILED",
            "tick_engine": "ACTIVE" if self.tick_engine else "FAILED",
            "gui_system": "ACTIVE" if self.gui else "FAILED",
            "fractal_renderer": "ACTIVE" if self.gui else "FAILED",
            "sigil_overlay": "ACTIVE" if self.gui else "FAILED"
        }
        
        self.logger.system("DAWN System Status", status)
        
        capabilities = {
            "real_time_visualization": "Fractal bloom rendering",
            "cognitive_monitoring": "Live consciousness state tracking",
            "sigil_processing": "Dynamic symbol generation and decay",
            "queue_communication": "Thread-safe data exchange",
            "professional_output": "Clean, emoji-free logging"
        }
        
        self.logger.system("System Capabilities", capabilities)
        
        controls = {
            "fractal_interaction": "Watch real-time bloom visualization",
            "sigil_monitoring": "Observe cognitive symbols and decay",
            "heat_tracking": "Monitor thermal consciousness states",
            "shutdown": "Close window to shutdown all systems"
        }
        
        self.logger.system("User Interface", controls)
    
    def startup(self):
        """Complete system startup sequence"""
        clean_section_header("DAWN CONSCIOUSNESS SYSTEM")
        self.logger.info("Professional build - emoji-free operation")
        
        # Setup signal handling
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Initialize components
        if not self.initialize_communication():
            return False
            
        if not self.initialize_tick_engine():
            return False
            
        if not self.initialize_gui():
            return False
            
        if not self.start_tick_engine():
            return False
        
        # Mark system as running
        self.running = True
        
        # Display status
        self.display_system_status()
        
        self.logger.success("DAWN system startup complete")
        clean_section_footer("DAWN CONSCIOUSNESS SYSTEM")
        
        return True
    
    def run(self):
        """Run the main system loop"""
        if not self.startup():
            self.logger.error("System startup failed - aborting")
            return False
        
        try:
            self.logger.info("Starting GUI main loop")
            self.root.mainloop()
        except Exception as e:
            self.logger.error("GUI main loop failed", {
                "error": str(e),
                "error_type": type(e).__name__
            })
        finally:
            self.shutdown()
        
        return True
    
    def shutdown(self):
        """Graceful system shutdown"""
        if not self.running:
            return
            
        self.logger.info("Initiating system shutdown")
        self.running = False
        
        # Stop tick engine
        if self.tick_engine:
            try:
                self.tick_engine.stop()
                self.logger.success("Tick engine stopped")
            except Exception as e:
                self.logger.warning("Error stopping tick engine", {"error": str(e)})
        
        # Close GUI
        if self.root:
            try:
                self.root.quit()
                self.logger.success("GUI system closed")
            except Exception as e:
                self.logger.warning("Error closing GUI", {"error": str(e)})
        
        self.logger.success("DAWN system shutdown complete")


def main():
    """Main entry point"""
    dawn_system = DAWNMasterSystem()
    
    try:
        success = dawn_system.run()
        if success:
            print("\nDAWN Master System completed successfully")
        else:
            print("\nDAWN Master System failed to start")
            return 1
    except KeyboardInterrupt:
        print("\nDAWN Master System interrupted by user")
    except Exception as e:
        print(f"\nDAWN Master System failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 