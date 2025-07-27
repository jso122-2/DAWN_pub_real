#!/usr/bin/env python3
"""
DAWN Consciousness Bridge - GUI Optimized
Starts consciousness writer optimized for GUI consumption
Reduces update rate to prevent overwhelming the Tauri app
"""

import os
import sys
import time
import threading
import logging
import signal
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OptimizedDAWNConsciousnessBridge:
    """GUI-optimized bridge between DAWN tick engine and Tauri GUI"""
    
    def __init__(self):
        self.running = False
        self.consciousness_writer = None
        self.tick_thread = None
        self.mmap_file_path = project_root / "runtime" / "dawn_consciousness.mmap"
        
        # Setup signal handling
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.shutdown()
        sys.exit(0)
    
    def start_consciousness_bridge(self):
        """Start the GUI-optimized consciousness data bridge"""
        logger.info("🧠 Starting GUI-optimized DAWN consciousness bridge...")
        
        try:
            # Import consciousness writer
            from consciousness.dawn_tick_state_writer import DAWNConsciousnessStateWriter
            
            # Create writer instance
            self.consciousness_writer = DAWNConsciousnessStateWriter(
                mmap_path=str(self.mmap_file_path)
            )
            
            # Disable history for GUI mode (saves memory and reduces complexity)
            self.consciousness_writer.enable_history = False
            
            # Start consciousness writer in background thread
            def consciousness_loop():
                try:
                    logger.info("🔄 Starting GUI-optimized consciousness tick loop...")
                    # Use 0.05s internal tick (20 Hz) but 0.1s GUI updates (10 Hz max)
                    self.consciousness_writer.run_consciousness_loop(tick_interval=0.05)
                except Exception as e:
                    logger.error(f"❌ Consciousness loop error: {e}")
                    import traceback
                    traceback.print_exc()
            
            self.tick_thread = threading.Thread(target=consciousness_loop, daemon=True)
            self.tick_thread.start()
            
            # Wait for initialization
            time.sleep(2)
            
            # Verify mmap file was created
            if self.mmap_file_path.exists():
                file_size = self.mmap_file_path.stat().st_size
                logger.info(f"✅ GUI-optimized consciousness bridge active")
                logger.info(f"📊 Memory-mapped file: {self.mmap_file_path}")
                logger.info(f"📈 File size: {file_size:,} bytes")
                logger.info(f"🎮 GUI update rate: 10 Hz maximum")
                logger.info(f"🔄 Internal tick rate: 20 Hz")
                return True
            else:
                logger.error("❌ Memory-mapped file not created")
                return False
                
        except ImportError as e:
            logger.error(f"❌ Could not import consciousness writer: {e}")
            logger.info("💡 Make sure you're in the DAWN project root directory")
            return False
        except Exception as e:
            logger.error(f"❌ Error starting consciousness bridge: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def monitor_bridge(self):
        """Monitor the consciousness bridge and display stats"""
        tick_count = 0
        last_tick_time = time.time()
        
        while self.running:
            try:
                current_time = time.time()
                
                # Check if writer is still alive
                if self.tick_thread and not self.tick_thread.is_alive():
                    logger.warning("⚠️ Consciousness thread stopped!")
                    break
                
                # Display periodic status
                if current_time - last_tick_time >= 10:  # Every 10 seconds
                    if self.consciousness_writer:
                        tick_count = getattr(self.consciousness_writer, 'current_tick', tick_count)
                        logger.info(f"📊 Bridge Status: Tick {tick_count}, File: {self.mmap_file_path.exists()}")
                        logger.info(f"🎮 GUI-optimized: Fixed slot reading, no rolling buffer")
                    last_tick_time = current_time
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ Monitor error: {e}")
                break
    
    def run(self):
        """Run the GUI-optimized consciousness bridge"""
        logger.info("🌅 DAWN GUI-Optimized Consciousness Bridge Starting")
        logger.info("=" * 60)
        
        # Start the bridge
        if not self.start_consciousness_bridge():
            logger.error("❌ Failed to start consciousness bridge")
            return False
        
        self.running = True
        
        # Print system status and instructions
        logger.info("=" * 60)
        logger.info("🧠 DAWN Consciousness Engine: GUI-OPTIMIZED MODE")
        logger.info(f"📊 Memory-mapped data stream: {self.mmap_file_path}")
        logger.info("🔄 Real-time consciousness data @ 10 Hz (GUI-friendly)")
        logger.info("🎮 Fixed slot reading (no rolling buffer complexity)")
        logger.info("")
        logger.info("🎮 To connect Tauri GUI:")
        logger.info("   1. Open a new terminal")
        logger.info("   2. cd dawn-consciousness-gui")
        logger.info("   3. npm run tauri:dev")
        logger.info("")
        logger.info("🛑 Press Ctrl+C to stop the bridge")
        logger.info("=" * 60)
        
        try:
            # Monitor the bridge
            self.monitor_bridge()
        except KeyboardInterrupt:
            logger.info("🛑 Received interrupt signal")
        finally:
            self.shutdown()
        
        return True
    
    def shutdown(self):
        """Shutdown the consciousness bridge"""
        logger.info("🔄 Shutting down GUI-optimized consciousness bridge...")
        
        self.running = False
        
        # Stop consciousness writer
        if self.consciousness_writer:
            try:
                logger.info("🛑 Stopping consciousness writer...")
                if hasattr(self.consciousness_writer, 'stop'):
                    self.consciousness_writer.stop()
                logger.info("✅ Consciousness writer stopped")
            except Exception as e:
                logger.error(f"❌ Error stopping consciousness writer: {e}")
        
        logger.info("✅ GUI-optimized consciousness bridge shutdown complete")

def main():
    """Main entry point"""
    print("🧠 DAWN GUI-Optimized Consciousness Bridge")
    print("Connecting DAWN tick loop to Tauri GUI with optimized data flow")
    print()
    
    try:
        # Create and run bridge
        bridge = OptimizedDAWNConsciousnessBridge()
        success = bridge.run()
        
        if success:
            logger.info("✅ Bridge completed successfully")
        else:
            logger.error("❌ Bridge failed")
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