#!/usr/bin/env python3
"""
DAWN GUI Launcher with Queue Communication Bridge
Launches tick engine and GUI with shared queue for real-time data transfer
"""

import os
import sys
import tkinter as tk
import threading
import queue
import time
import logging
from typing import Optional

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import DAWN components
try:
    from tick_engine.core_tick import CoreTickManager
    from gui.dawn_gui_tk import DAWNGui
    IMPORTS_SUCCESSFUL = True
except ImportError as e:
    logger.error(f"Failed to import DAWN components: {e}")
    IMPORTS_SUCCESSFUL = False

class DAWNLauncher:
    """Main launcher for DAWN GUI with queue-based tick engine"""
    
    def __init__(self, tick_interval: float = 0.5, queue_maxsize: int = 100):
        """
        Initialize DAWN launcher
        
        Args:
            tick_interval: Time between ticks in seconds
            queue_maxsize: Maximum size of the communication queue
        """
        self.tick_interval = tick_interval
        self.queue_maxsize = queue_maxsize
        
        # Shared communication queue (thread-safe)
        self.data_queue = queue.Queue(maxsize=queue_maxsize)
        
        # Subsystem managers
        self.tick_manager: Optional[CoreTickManager] = None
        self.gui: Optional[DAWNGui] = None
        self.gui_thread: Optional[threading.Thread] = None
        
        # Control flags
        self.running = False
        
        logger.info(f"DAWN Launcher initialized with {tick_interval}s tick interval")
    
    def start(self):
        """Start both tick engine and GUI with queue bridge"""
        if not IMPORTS_SUCCESSFUL:
            logger.error("Cannot start DAWN - import failures detected")
            return False
        
        logger.info("🚀 Starting DAWN GUI with Queue Communication Bridge")
        print("🌅 DAWN Cognitive Engine Launcher")
        print("=" * 50)
        print(f"⏰ Tick interval: {self.tick_interval}s")
        print(f"📊 Queue size: {self.queue_maxsize}")
        print(f"🔗 Communication: queue.Queue() bridge")
        print("=" * 50)
        
        try:
            # 1. Create and start tick engine (background thread)
            self.tick_manager = CoreTickManager(
                tick_interval=self.tick_interval,
                queue_maxsize=self.queue_maxsize
            )
            
            # Connect the shared queue to the tick manager
            self.tick_manager.data_queue = self.data_queue
            self.tick_manager.tick_engine.data_queue = self.data_queue
            
            # Start tick engine
            self.tick_manager.start()
            logger.info("✅ Tick engine started")
            
            # 2. Start GUI (main thread - Tkinter requirement)
            self.running = True
            self._start_gui()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start DAWN: {e}")
            self.stop()
            return False
    
    def _start_gui(self):
        """Start GUI on main thread"""
        try:
            logger.info("🖥️  Starting GUI on main thread...")
            
            # Create Tkinter root
            root = tk.Tk()
            
            # Create GUI with external queue
            self.gui = DAWNGui(root, external_queue=self.data_queue)
            
            # Setup window close handler
            def on_closing():
                logger.info("🛑 GUI closing - stopping all systems...")
                self.stop()
                root.destroy()
            
            root.protocol("WM_DELETE_WINDOW", on_closing)
            
            logger.info("✅ GUI initialized with queue bridge")
            print("\n🎮 DAWN GUI Started")
            print("📊 Real-time tick data streaming via queue.Queue()")
            print("🔄 Tick engine running in background thread")
            print("🖥️  GUI running on main thread")
            print("🛑 Close GUI window to stop all systems")
            print("\n" + "=" * 50)
            
            # Start GUI main loop (blocks until window closed)
            root.mainloop()
            
        except Exception as e:
            logger.error(f"GUI error: {e}")
            self.stop()
    
    def stop(self):
        """Stop all DAWN subsystems"""
        logger.info("🛑 Stopping DAWN systems...")
        
        self.running = False
        
        # Stop tick engine
        if self.tick_manager:
            self.tick_manager.stop()
            logger.info("✅ Tick engine stopped")
        
        # Clear queue
        try:
            while not self.data_queue.empty():
                self.data_queue.get_nowait()
        except queue.Empty:
            pass
        
        logger.info("✅ DAWN shutdown complete")
    
    def get_queue_stats(self) -> dict:
        """Get queue communication statistics"""
        return {
            "queue_size": self.data_queue.qsize(),
            "queue_maxsize": self.queue_maxsize,
            "tick_engine_running": self.tick_manager.tick_engine.running if self.tick_manager else False,
            "gui_running": self.running
        }

def test_queue_communication():
    """Test the queue communication system"""
    print("🧪 Testing Queue Communication System")
    print("-" * 40)
    
    # Create test queue
    test_queue = queue.Queue(maxsize=10)
    
    # Create tick manager
    tick_manager = CoreTickManager(tick_interval=0.2, queue_maxsize=10)
    tick_manager.data_queue = test_queue
    tick_manager.tick_engine.data_queue = test_queue
    
    # Start tick engine
    tick_manager.start()
    
    print("✅ Tick engine started")
    print("📊 Monitoring queue for 5 seconds...")
    
    try:
        start_time = time.time()
        tick_count = 0
        
        while time.time() - start_time < 5.0:
            try:
                data = test_queue.get_nowait()
                tick_count += 1
                print(f"📨 Received tick {tick_count}: {data['tick']}")
            except queue.Empty:
                time.sleep(0.1)
        
        print(f"\n✅ Test complete - received {tick_count} ticks in 5 seconds")
        print(f"📊 Average rate: {tick_count/5.0:.1f} ticks/second")
        
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted")
    
    finally:
        tick_manager.stop()
        print("✅ Test cleanup complete")

def main():
    """Main entry point"""
    print("🌅 DAWN GUI Launcher")
    print("Queue-based communication bridge between tick engine and GUI")
    print()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            test_queue_communication()
            return
        elif sys.argv[1] == "--help":
            print("Usage:")
            print("  python launch_dawn_gui.py          # Start DAWN GUI")
            print("  python launch_dawn_gui.py --test   # Test queue communication")
            print("  python launch_dawn_gui.py --help   # Show this help")
            return
    
    try:
        # Create and start DAWN launcher
        launcher = DAWNLauncher(tick_interval=0.5, queue_maxsize=100)
        
        if launcher.start():
            # GUI mainloop will run until window is closed
            pass
        else:
            logger.error("❌ Failed to start DAWN")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("🛑 Interrupted by user")
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 