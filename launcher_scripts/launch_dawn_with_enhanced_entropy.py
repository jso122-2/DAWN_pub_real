#!/usr/bin/env python3
"""
DAWN Enhanced Entropy Analyzer GUI Launcher
Launches DAWN with the enhanced entropy analyzer integrated into the GUI system.

Features:
- Enhanced entropy detection with thermal correlation
- Real-time entropy visualization in GUI
- Autonomous threshold-based alerting
- Integration with pulse controller and sigil engine
"""

import sys
import os
import tkinter as tk
import threading
import queue
import time
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EnhancedEntropyDAWNSystem:
    """DAWN system with enhanced entropy analyzer integration"""
    
    def __init__(self):
        self.running = False
        self.data_queue = queue.Queue(maxsize=200)
        
        # Components
        self.enhanced_entropy_analyzer = None
        self.pulse_controller = None
        self.sigil_engine = None
        self.tick_engine = None
        self.gui = None
        
        # Threading
        self.system_thread = None
        self.entropy_monitor_thread = None
        
    def initialize_components(self):
        """Initialize all DAWN components with enhanced entropy integration"""
        logger.info("🧬 Initializing DAWN with Enhanced Entropy Analyzer...")
        
        try:
            # Initialize pulse controller
            from core.pulse_controller import PulseController
            self.pulse_controller = PulseController(initial_heat=25.0)
            logger.info("✅ Pulse controller initialized")
        except ImportError as e:
            logger.warning(f"⚠️ Pulse controller not available: {e}")
        
        try:
            # Initialize sigil engine
            from core.sigil_engine import SigilEngine
            self.sigil_engine = SigilEngine(initial_heat=25.0)
            logger.info("✅ Sigil engine initialized")
        except ImportError as e:
            logger.warning(f"⚠️ Sigil engine not available: {e}")
        
        try:
            # Initialize enhanced entropy analyzer
            from core.dawn_entropy_analyzer import EnhancedEntropyAnalyzer
            self.enhanced_entropy_analyzer = EnhancedEntropyAnalyzer(
                pulse_controller=self.pulse_controller,
                sigil_engine=self.sigil_engine
            )
            logger.info("✅ Enhanced entropy analyzer initialized")
        except ImportError as e:
            logger.error(f"❌ Enhanced entropy analyzer not available: {e}")
            # Fall back to basic entropy analyzer
            try:
                from core.dawn_entropy_analyzer import EntropyAnalyzer
                self.enhanced_entropy_analyzer = EntropyAnalyzer()
                logger.info("✅ Basic entropy analyzer initialized as fallback")
            except ImportError:
                logger.error("❌ No entropy analyzer available")
                return False
        
        try:
            # Initialize basic tick engine for data generation
            from tick_engine.core_tick import CoreTickEngine
            self.tick_engine = CoreTickEngine(
                data_queue=self.data_queue,
                tick_interval=0.5
            )
            logger.info("✅ Core tick engine initialized")
        except ImportError as e:
            logger.warning(f"⚠️ Core tick engine not available: {e}")
        
        return True
    
    def start_entropy_monitoring(self):
        """Start entropy monitoring in background thread"""
        if not self.enhanced_entropy_analyzer:
            return
        
        def entropy_monitor():
            """Background entropy monitoring loop"""
            entropy_value = 0.3  # Starting entropy
            
            while self.running:
                try:
                    # Simulate realistic entropy fluctuations
                    import random
                    import math
                    
                    # Base entropy oscillation
                    time_factor = time.time() * 0.1
                    base_entropy = 0.4 + 0.2 * math.sin(time_factor)
                    
                    # Add thermal influence if pulse controller available
                    if self.pulse_controller:
                        thermal_stats = self.pulse_controller.get_heat_statistics()
                        heat_influence = thermal_stats['current_heat'] / 100.0 * 0.2
                        base_entropy += heat_influence
                    
                    # Add cognitive load influence if sigil engine available
                    if self.sigil_engine and self.sigil_engine.is_running:
                        cognitive_load = len(self.sigil_engine.active_sigils) * 0.05
                        base_entropy += cognitive_load
                    
                    # Add some realistic noise
                    noise = random.gauss(0, 0.03)
                    entropy_value = max(0.0, min(1.0, base_entropy + noise))
                    
                    # Analyze entropy with enhanced analyzer
                    result = self.enhanced_entropy_analyzer.analyze(
                        entropy_value, 
                        source="entropy_monitor"
                    )
                    
                    # Send data to GUI queue
                    gui_data = {
                        'type': 'entropy_analysis',
                        'entropy': entropy_value,
                        'delta': result.delta,
                        'status': result.status,
                        'warning': result.warning_triggered,
                        'thermal_context': result.thermal_context,
                        'sigil_context': result.sigil_context,
                        'timestamp': time.time()
                    }
                    
                    try:
                        self.data_queue.put_nowait(gui_data)
                    except queue.Full:
                        # Remove old data if queue is full
                        try:
                            self.data_queue.get_nowait()
                            self.data_queue.put_nowait(gui_data)
                        except queue.Empty:
                            pass
                    
                    # Sleep before next analysis
                    time.sleep(1.0)
                    
                except Exception as e:
                    logger.error(f"Entropy monitoring error: {e}")
                    time.sleep(2.0)
        
        self.entropy_monitor_thread = threading.Thread(
            target=entropy_monitor,
            daemon=True,
            name="EntropyMonitor"
        )
        self.entropy_monitor_thread.start()
        logger.info("🔄 Entropy monitoring started")
    
    def start_system_simulation(self):
        """Start system simulation for demonstration"""
        def system_simulator():
            """System simulation loop"""
            tick_count = 0
            
            while self.running:
                try:
                    tick_count += 1
                    
                    # Update pulse controller if available
                    if self.pulse_controller:
                        # Simulate heat changes
                        import random
                        heat_delta = random.gauss(0, 2.0)
                        new_heat = self.pulse_controller.current_heat + heat_delta
                        self.pulse_controller.update_heat(new_heat)
                    
                    # Update sigil engine if available
                    if self.sigil_engine and tick_count % 10 == 0:
                        # Simulate sigil activity periodically
                        pass
                    
                    # Send general system data to GUI
                    system_data = {
                        'type': 'system_tick',
                        'tick': tick_count,
                        'timestamp': time.time(),
                        'heat': self.pulse_controller.current_heat if self.pulse_controller else 25.0,
                        'zone': self.pulse_controller.current_zone if self.pulse_controller else 'ACTIVE',
                        'active_sigils': len(self.sigil_engine.active_sigils) if self.sigil_engine else 0
                    }
                    
                    try:
                        self.data_queue.put_nowait(system_data)
                    except queue.Full:
                        try:
                            self.data_queue.get_nowait()
                            self.data_queue.put_nowait(system_data)
                        except queue.Empty:
                            pass
                    
                    time.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"System simulation error: {e}")
                    time.sleep(1.0)
        
        self.system_thread = threading.Thread(
            target=system_simulator,
            daemon=True,
            name="SystemSimulator"
        )
        self.system_thread.start()
        logger.info("🔄 System simulation started")
    
    def start_gui(self):
        """Start the DAWN GUI with enhanced entropy visualization"""
        try:
            from gui.dawn_gui_tk import DAWNGui
            
            # Create GUI
            root = tk.Tk()
            root.title("DAWN - Enhanced Entropy Analyzer Integration")
            root.geometry("1200x800")
            
            # Initialize GUI with external queue
            self.gui = DAWNGui(root, external_queue=self.data_queue)
            
            # Setup window close handler
            def on_closing():
                logger.info("🛑 Shutting down DAWN Enhanced Entropy System...")
                self.stop()
                root.destroy()
            
            root.protocol("WM_DELETE_WINDOW", on_closing)
            
            logger.info("✅ DAWN GUI initialized with enhanced entropy integration")
            
            # Start GUI main loop
            root.mainloop()
            
        except Exception as e:
            logger.error(f"GUI error: {e}")
            self.stop()
    
    def start(self):
        """Start the complete DAWN system with enhanced entropy analyzer"""
        logger.info("🚀 Starting DAWN Enhanced Entropy System...")
        
        # Initialize components
        if not self.initialize_components():
            logger.error("❌ Component initialization failed")
            return False
        
        self.running = True
        
        # Start background systems
        self.start_entropy_monitoring()
        self.start_system_simulation()
        
        # Start tick engine if available
        if self.tick_engine:
            self.tick_engine.start()
            logger.info("🔄 Tick engine started")
        
        # Display system status
        print("\n" + "="*70)
        print("🧠 DAWN Enhanced Entropy Analyzer System ONLINE")
        print("="*70)
        print(f"🧬 Enhanced Entropy Analyzer: {'✅ Active' if self.enhanced_entropy_analyzer else '❌ Not Available'}")
        print(f"🔥 Pulse Controller: {'✅ Connected' if self.pulse_controller else '❌ Not Available'}")
        print(f"🔮 Sigil Engine: {'✅ Connected' if self.sigil_engine else '❌ Not Available'}")
        print(f"⚙️ Tick Engine: {'✅ Running' if self.tick_engine else '❌ Not Available'}")
        print("\n🎯 Features Active:")
        print("   • Real-time entropy shift detection")
        print("   • Autonomous threshold-based alerting")
        print("   • Thermal correlation analysis")
        print("   • Cognitive load integration")
        print("   • GUI visualization with live updates")
        print("\n🖥️ Starting GUI interface...")
        print("="*70)
        
        # Start GUI (this will block until window is closed)
        self.start_gui()
        
        return True
    
    def stop(self):
        """Stop the DAWN system"""
        logger.info("🛑 Stopping DAWN Enhanced Entropy System...")
        
        self.running = False
        
        # Stop tick engine
        if self.tick_engine:
            self.tick_engine.stop()
            logger.info("⚙️ Tick engine stopped")
        
        # Stop sigil engine
        if self.sigil_engine and self.sigil_engine.is_running:
            self.sigil_engine.stop()
            logger.info("🔮 Sigil engine stopped")
        
        logger.info("✅ DAWN Enhanced Entropy System shutdown complete")


def main():
    """Main launcher function"""
    try:
        print("🌅 DAWN Enhanced Entropy Analyzer GUI Launcher")
        print("=" * 60)
        print("Initializing DAWN with enhanced entropy detection...")
        print()
        
        # Create and start system
        dawn_system = EnhancedEntropyDAWNSystem()
        
        if dawn_system.start():
            logger.info("DAWN system completed successfully")
        else:
            logger.error("DAWN system failed to start")
            return False
            
    except KeyboardInterrupt:
        print("\n🛑 DAWN Enhanced Entropy System interrupted by user")
        return True
    except Exception as e:
        logger.error(f"❌ Launcher error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 