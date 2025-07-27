"""
🌅 DAWN Interactive Runner - Live Testing Environment
═══════════════════════════════════════════════════════════════════

Runs DAWN's tick loop in the background while providing an interactive
command interface for real-time testing and monitoring.
"""

import threading
import time
import sys
import os
from typing import Optional
import logging
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import DAWN components
try:
    from main import DAWNGenomeConsciousnessWrapper
    from dawn_command_interface import (
        run_command_from_input, 
        connect_to_dawn, 
        interactive_mode,
        _tick_active,
        _tick_lock
    )
    IMPORTS_SUCCESSFUL = True
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure main.py and dawn_command_interface.py are in the same directory")
    IMPORTS_SUCCESSFUL = False
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(name)s] %(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("DAWNRunner")


class DawnTickRunner:
    """Manages DAWN's tick loop in a background thread"""
    
    def __init__(self, dawn_instance):
        self.dawn = dawn_instance  # Store the DAWN instance
        self.running = False
        self.thread = None
        self.tick_interval = 0.1  # Default 100ms per tick
        self.tick_count = 0
        self.last_error = None
        self.paused = False
        
    def start(self):
        """Start the tick loop in a background thread"""
        if self.running:
            logger.warning("Tick loop already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._tick_loop, daemon=True)
        self.thread.start()
        logger.info("✅ DAWN tick loop started")
        
    def stop(self):
        """Stop the tick loop"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        logger.info("🛑 DAWN tick loop stopped")
        
    def pause(self):
        """Pause the tick loop"""
        self.paused = True
        logger.info("⏸️  DAWN tick loop paused")
        
    def resume(self):
        """Resume the tick loop"""
        self.paused = False
        logger.info("▶️  DAWN tick loop resumed")
        
    def set_speed(self, interval: float):
        """Set tick interval in seconds"""
        self.tick_interval = max(0.01, interval)  # Minimum 10ms
        logger.info(f"⏱️  Tick interval set to {self.tick_interval}s")
        
    def _tick_loop(self):
        """Main tick loop running in background thread"""
        logger.info("🔄 Tick loop thread started")
        
        while self.running:
            try:
                if not self.paused and self.dawn:  # Check dawn exists
                    # Set tick active flag for command safety
                    with _tick_lock:
                        import dawn_command_interface
                        dawn_command_interface._tick_active = True
                    
                    # Execute tick
                    tick_start = time.time()
                    
                    # Call DAWN's tick method
                    if hasattr(self.dawn, 'tick'):
                        self.dawn.tick()
                    elif hasattr(self.dawn, 'run_tick'):
                        self.dawn.run_tick()
                    else:
                        logger.error("DAWN instance has no tick method!")
                        break
                    
                    tick_duration = time.time() - tick_start
                    self.tick_count += 1
                    
                    # Clear tick active flag
                    with _tick_lock:
                        dawn_command_interface._tick_active = False
                    
                    # Log slow ticks
                    if tick_duration > self.tick_interval * 0.8:
                        logger.warning(f"Slow tick {self.tick_count}: {tick_duration:.3f}s")
                
                # Sleep for remainder of interval
                time.sleep(self.tick_interval)
                
            except Exception as e:
                self.last_error = str(e)
                logger.error(f"❌ Tick error: {e}")
                # Don't crash the loop, just log and continue
                time.sleep(self.tick_interval)
        
        logger.info("🔄 Tick loop thread ended")


class InteractiveCommands:
    """Extended commands for interactive testing"""
    
    def __init__(self, runner: DawnTickRunner):
        self.runner = runner
        self._register_commands()
        
    def _register_commands(self):
        """Register interactive-specific commands"""
        from dawn_command_interface import router
        
        # Tick control commands
        router.register("pause", self.pause_ticks, "Pause the tick loop")
        router.register("resume", self.resume_ticks, "Resume the tick loop")
        router.register("speed", self.set_tick_speed, "Set tick speed (seconds)")
        router.register("tick_info", self.tick_info, "Show tick loop information")
        
        # Monitoring commands
        router.register("watch", self.watch_value, "Watch a DAWN attribute")
        router.register("monitor", self.monitor_mode, "Enter monitoring mode")
        
        # Genome commands
        router.register("genome", self.toggle_genome_mode, "Toggle genome mode")
        router.register("genome_status", self.genome_status, "Show genome status")
        
    def pause_ticks(self):
        """Pause the tick loop"""
        self.runner.pause()
        
    def resume_ticks(self):
        """Resume the tick loop"""
        self.runner.resume()
        
    def set_tick_speed(self, interval: float = 0.1):
        """Set tick interval"""
        self.runner.set_speed(interval)
        
    def tick_info(self):
        """Display tick loop information"""
        logger.info("🔄 Tick Loop Information")
        logger.info("─" * 40)
        logger.info(f"Status:        {'RUNNING' if self.runner.running else 'STOPPED'}")
        logger.info(f"Paused:        {'YES' if self.runner.paused else 'NO'}")
        logger.info(f"Tick Count:    {self.runner.tick_count}")
        logger.info(f"Tick Interval: {self.runner.tick_interval}s")
        logger.info(f"Ticks/Second:  {1/self.runner.tick_interval:.1f}")
        
        if self.runner.last_error:
            logger.info(f"Last Error:    {self.runner.last_error}")
        
        # Try to get DAWN's current tick
        if self.runner.dawn and hasattr(self.runner.dawn, 'tick_count'):
            logger.info(f"DAWN Tick:     {self.runner.dawn.tick_count}")
            
    def watch_value(self, attribute: str):
        """Watch a specific DAWN attribute"""
        if not self.runner.dawn or not hasattr(self.runner.dawn, attribute):
            logger.error(f"DAWN has no attribute '{attribute}'")
            return
            
        value = getattr(self.runner.dawn, attribute)
        logger.info(f"📊 {attribute} = {value}")
        
    def monitor_mode(self, duration: int = 10):
        """Enter monitoring mode for specified seconds"""
        logger.info(f"📊 Monitoring mode for {duration}s...")
        logger.info("─" * 50)
        
        if not self.runner.dawn:
            logger.error("No DAWN instance to monitor")
            return
        
        start_time = time.time()
        last_tick = 0
        
        while time.time() - start_time < duration:
            current_tick = self.runner.tick_count
            if current_tick != last_tick:
                # Get key metrics
                metrics = []
                
                # Try to get various DAWN attributes
                if hasattr(self.runner.dawn, 'tick_count'):
                    metrics.append(f"T:{self.runner.dawn.tick_count}")
                if hasattr(self.runner.dawn, 'current_entropy'):
                    metrics.append(f"E:{self.runner.dawn.current_entropy:.2f}")
                if hasattr(self.runner.dawn, 'current_mood_valence'):
                    metrics.append(f"M:{self.runner.dawn.current_mood_valence:+.2f}")
                if hasattr(self.runner.dawn, 'coherence_score'):
                    metrics.append(f"C:{self.runner.dawn.coherence_score:.2f}")
                if hasattr(self.runner.dawn, 'genome_mode'):
                    metrics.append(f"G:{'ON' if self.runner.dawn.genome_mode else 'OFF'}")
                
                logger.info(f"[{current_tick:04d}] " + " | ".join(metrics))
                last_tick = current_tick
                
            time.sleep(0.1)
        
        logger.info("─" * 50)
        logger.info("📊 Monitoring complete")
        
    def toggle_genome_mode(self):
        """Toggle genome mode on/off"""
        if not self.runner.dawn:
            logger.error("No DAWN instance")
            return
            
        if hasattr(self.runner.dawn, 'genome_mode'):
            current = getattr(self.runner.dawn, 'genome_mode', False)
            if current and hasattr(self.runner.dawn, 'disable_genome_mode'):
                self.runner.dawn.disable_genome_mode()
                logger.info("🧬 Genome mode disabled")
            elif hasattr(self.runner.dawn, 'enable_genome_mode'):
                self.runner.dawn.enable_genome_mode()
                logger.info("🧬 Genome mode enabled")
        else:
            logger.warning("⚠️  Genome mode not available")
            
    def genome_status(self):
        """Show genome status"""
        if not self.runner.dawn:
            logger.error("No DAWN instance")
            return
            
        if hasattr(self.runner.dawn, 'get_status'):
            status = self.runner.dawn.get_status()
            logger.info(f"🧬 Genome Status: {status}")
        else:
            logger.info("⚠️  Genome status not available")


def print_banner():
    """Print welcome banner"""
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║       🌅 DAWN INTERACTIVE TESTING ENVIRONMENT 🌅      ║
    ╠═══════════════════════════════════════════════════════╣
    ║  DAWN's tick loop runs in the background while you    ║
    ║  test and monitor her systems in real-time.           ║
    ║                                                        ║
    ║  Commands:                                             ║
    ║    help     - Show all available commands             ║
    ║    status   - Check DAWN's current state              ║
    ║    pause    - Pause the tick loop                     ║
    ║    resume   - Resume the tick loop                    ║
    ║    monitor  - Enter monitoring mode                   ║
    ║    genome   - Toggle genome mode                      ║
    ║    exit     - Shutdown DAWN and exit                  ║
    ╚═══════════════════════════════════════════════════════╝
    """)


def run_interactive_dawn():
    """Main function to run DAWN with interactive commands"""
    
    print_banner()
    
    # Create DAWN instance
    logger.info("🌅 Initializing DAWN...")
    try:
        dawn = DAWNGenomeConsciousnessWrapper()
        logger.info("✅ DAWN instance created")
    except Exception as e:
        logger.error(f"❌ Failed to create DAWN: {e}")
        return
    
    # Connect command interface to DAWN
    if not connect_to_dawn(dawn):
        logger.error("❌ Failed to connect command interface to DAWN")
        return
    
    # Create tick runner WITH the dawn instance
    runner = DawnTickRunner(dawn)  # Pass dawn here!
    
    # Register interactive commands
    interactive_cmds = InteractiveCommands(runner)
    
    # Start tick loop
    runner.start()
    
    # Small delay to let tick loop start
    time.sleep(0.5)
    
    # Show initial status
    run_command_from_input("tick_info")
    run_command_from_input("status")
    
    logger.info("\n💡 Tip: Use 'monitor 5' to watch DAWN's vitals for 5 seconds")
    logger.info("💡 Tip: Use 'pause' to pause ticks, 'resume' to continue")
    logger.info("💡 Tip: Use 'speed 0.5' to slow down to 2 ticks/second")
    logger.info("💡 Tip: Use 'genome' to toggle genome mode\n")
    
    try:
        # Enter interactive mode
        interactive_mode()
    except KeyboardInterrupt:
        logger.info("\n⚡ Interrupted by user")
    finally:
        # Cleanup
        logger.info("🌅 Shutting down DAWN...")
        runner.stop()
        logger.info("✅ DAWN shutdown complete")


if __name__ == "__main__":
    if IMPORTS_SUCCESSFUL:
        run_interactive_dawn()
    else:
        print("Cannot run due to import errors")