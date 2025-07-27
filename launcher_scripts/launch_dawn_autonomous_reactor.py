#!/usr/bin/env python3
"""
DAWN Autonomous Reactor Complete System Launcher
The ultimate DAWN launcher integrating:
- Enhanced Entropy Analyzer (delta detection & warnings)
- Sigil Scheduler (autonomous stabilization protocols) 
- Autonomous Reactor (unified reactive system)
- Real-time GUI visualization
- Thermal correlation & cognitive load awareness
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


class DAWNAutonomousReactorGUI:
    """Complete DAWN system with autonomous reactor and GUI integration"""
    
    def __init__(self):
        self.running = False
        self.data_queue = queue.Queue(maxsize=300)
        
        # Core components
        self.autonomous_reactor = None
        self.pulse_controller = None
        self.sigil_engine = None
        self.gui = None
        
        # Threading
        self.gui_data_thread = None
        
        # Performance tracking
        self.total_entropy_readings = 0
        self.total_warnings = 0
        self.total_autonomous_reactions = 0
        
    def initialize_autonomous_reactor_system(self):
        """Initialize the complete autonomous reactor system"""
        logger.info("🧬 Initializing DAWN Autonomous Reactor System...")
        
        try:
            # Initialize pulse controller
            from core.pulse_controller import PulseController
            self.pulse_controller = PulseController(initial_heat=35.0)
            logger.info("✅ Pulse controller initialized")
        except ImportError as e:
            logger.warning(f"⚠️ Pulse controller not available: {e}")
        
        try:
            # Initialize sigil engine
            from core.sigil_engine import SigilEngine
            self.sigil_engine = SigilEngine(initial_heat=35.0)
            logger.info("✅ Sigil engine initialized")
        except ImportError as e:
            logger.warning(f"⚠️ Sigil engine not available: {e}")
        
        try:
            # Initialize the complete autonomous reactor
            from core.dawn_autonomous_reactor import DAWNAutonomousReactor
            self.autonomous_reactor = DAWNAutonomousReactor(
                pulse_controller=self.pulse_controller,
                sigil_engine=self.sigil_engine,
                entropy_threshold=0.6,
                auto_start=False  # We'll control startup
            )
            logger.info("✅ Autonomous reactor system initialized")
            return True
            
        except ImportError as e:
            logger.error(f"❌ Autonomous reactor system not available: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to initialize autonomous reactor: {e}")
            return False
    
    def start_gui_data_feed(self):
        """Start feeding data from autonomous reactor to GUI"""
        def data_feed_loop():
            """Feed autonomous reactor data to GUI"""
            
            while self.running:
                try:
                    if self.autonomous_reactor:
                        # Get current reactor state
                        state = self.autonomous_reactor.get_reactor_state()
                        metrics = self.autonomous_reactor.get_performance_metrics()
                        
                        # Create comprehensive GUI data
                        gui_data = {
                            'type': 'autonomous_reactor_state',
                            'timestamp': time.time(),
                            
                            # Core entropy data
                            'entropy': state['entropy_level'],
                            'entropy_delta': state['entropy_delta'],
                            'entropy_status': state['entropy_status'],
                            'entropy_warning': state['entropy_warning'],
                            
                            # Reactor state
                            'reactor_status': state['reactor_status'],
                            'active_sigils': state['active_sigils'],
                            'recent_sigils_triggered': state['recent_sigils_triggered'],
                            
                            # Thermal data
                            'thermal_heat': state['thermal_heat'],
                            'thermal_zone': state['thermal_zone'],
                            
                            # Performance metrics
                            'total_entropy_readings': metrics['total_entropy_readings'],
                            'total_reactions': metrics['total_reactions'],
                            'autonomous_interventions': metrics['autonomous_interventions'],
                            'stabilization_attempts': metrics['stabilization_attempts'],
                            
                            # Rates
                            'reaction_rate': metrics.get('reaction_rate', 0),
                            'intervention_rate': metrics.get('intervention_rate', 0)
                        }
                        
                        # Add component-specific data
                        if 'entropy_analyzer' in metrics:
                            analyzer_metrics = metrics['entropy_analyzer']
                            gui_data.update({
                                'analyzer_total_warnings': analyzer_metrics['total_warnings'],
                                'analyzer_rapid_rise_events': analyzer_metrics['rapid_rise_events'],
                                'analyzer_warning_rate': analyzer_metrics['warning_rate']
                            })
                        
                        if 'sigil_scheduler' in metrics:
                            scheduler_stats = metrics['sigil_scheduler']
                            gui_data.update({
                                'scheduler_total_triggers': scheduler_stats['total_triggers'],
                                'scheduler_successful_triggers': scheduler_stats['successful_triggers'],
                                'scheduler_threshold_breaches': scheduler_stats['threshold_breaches']
                            })
                        
                        # Send to GUI queue
                        try:
                            self.data_queue.put_nowait(gui_data)
                        except queue.Full:
                            # Remove old data if queue is full
                            try:
                                self.data_queue.get_nowait()
                                self.data_queue.put_nowait(gui_data)
                            except queue.Empty:
                                pass
                        
                        # Track performance
                        self.total_entropy_readings += 1
                        if state['entropy_warning']:
                            self.total_warnings += 1
                        if state['recent_sigils_triggered']:
                            self.total_autonomous_reactions += 1
                    
                    time.sleep(0.5)  # Update every 500ms
                    
                except Exception as e:
                    logger.error(f"GUI data feed error: {e}")
                    time.sleep(1.0)
        
        self.gui_data_thread = threading.Thread(
            target=data_feed_loop,
            daemon=True,
            name="GUIDataFeed"
        )
        self.gui_data_thread.start()
        logger.info("🔄 GUI data feed started")
    
    def start_gui(self):
        """Start the DAWN GUI with autonomous reactor integration"""
        try:
            from gui.dawn_gui_tk import DAWNGui
            
            # Create GUI
            root = tk.Tk()
            root.title("DAWN - Autonomous Reactor System")
            root.geometry("1400x900")
            
            # Apply dark theme styling
            root.configure(bg="#1a1a1a")
            
            # Initialize GUI with external queue
            self.gui = DAWNGui(root, external_queue=self.data_queue)
            
            # Add custom autonomous reactor information panel
            self._add_reactor_info_panel(root)
            
            # Setup window close handler
            def on_closing():
                logger.info("🛑 Shutting down DAWN Autonomous Reactor System...")
                self.stop()
                root.destroy()
            
            root.protocol("WM_DELETE_WINDOW", on_closing)
            
            logger.info("✅ DAWN GUI initialized with autonomous reactor integration")
            
            # Start GUI main loop
            root.mainloop()
            
        except Exception as e:
            logger.error(f"GUI error: {e}")
            self.stop()
    
    def _add_reactor_info_panel(self, root):
        """Add autonomous reactor information panel to GUI"""
        try:
            # Create info frame
            info_frame = tk.Frame(root, bg="#2a2a2a", relief=tk.RAISED, bd=2)
            info_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
            
            # Title
            title_label = tk.Label(
                info_frame, 
                text="🧬 DAWN AUTONOMOUS REACTOR",
                font=("Arial", 12, "bold"),
                fg="#00ff88",
                bg="#2a2a2a"
            )
            title_label.pack(side=tk.LEFT, padx=10)
            
            # Status indicator
            self.status_label = tk.Label(
                info_frame,
                text="⚡ ACTIVE",
                font=("Arial", 10, "bold"),
                fg="#ffff00",
                bg="#2a2a2a"
            )
            self.status_label.pack(side=tk.LEFT, padx=20)
            
            # Metrics display
            self.metrics_label = tk.Label(
                info_frame,
                text="Initializing...",
                font=("Arial", 9),
                fg="#ffffff",
                bg="#2a2a2a"
            )
            self.metrics_label.pack(side=tk.RIGHT, padx=10)
            
            # Update metrics periodically
            def update_metrics():
                if self.autonomous_reactor and self.running:
                    state = self.autonomous_reactor.get_reactor_state()
                    metrics = self.autonomous_reactor.get_performance_metrics()
                    
                    # Update status
                    status_text = f"⚡ {state['reactor_status'].upper()}"
                    self.status_label.config(text=status_text)
                    
                    # Update metrics
                    metrics_text = (f"Entropy: {state['entropy_level']:.3f} | "
                                  f"Warnings: {self.total_warnings} | "
                                  f"Reactions: {self.total_autonomous_reactions} | "
                                  f"Interventions: {metrics['autonomous_interventions']}")
                    self.metrics_label.config(text=metrics_text)
                
                if self.running:
                    root.after(1000, update_metrics)  # Update every second
            
            update_metrics()
            
        except Exception as e:
            logger.warning(f"Could not add reactor info panel: {e}")
    
    def start(self):
        """Start the complete DAWN autonomous reactor system"""
        logger.info("🚀 Starting DAWN Autonomous Reactor Complete System...")
        
        # Initialize autonomous reactor system
        if not self.initialize_autonomous_reactor_system():
            logger.error("❌ Failed to initialize autonomous reactor system")
            return False
        
        self.running = True
        
        # Start the autonomous reactor
        if self.autonomous_reactor:
            reactor_started = self.autonomous_reactor.start()
            if reactor_started:
                logger.info("🔥 Autonomous reactor started successfully")
            else:
                logger.error("❌ Failed to start autonomous reactor")
                return False
        
        # Start GUI data feed
        self.start_gui_data_feed()
        
        # Display system status
        print("\n" + "="*80)
        print("🧠 DAWN AUTONOMOUS REACTOR COMPLETE SYSTEM ONLINE")
        print("="*80)
        print(f"🧬 Autonomous Reactor: {'✅ Active' if self.autonomous_reactor else '❌ Not Available'}")
        print(f"🔥 Pulse Controller: {'✅ Connected' if self.pulse_controller else '❌ Not Available'}")
        print(f"🔮 Sigil Engine: {'✅ Connected' if self.sigil_engine else '❌ Not Available'}")
        
        if self.autonomous_reactor:
            state = self.autonomous_reactor.get_reactor_state()
            print(f"📊 Current Entropy: {state['entropy_level']:.3f}")
            print(f"🎯 Entropy Status: {state['entropy_status']}")
            print(f"⚡ Reactor Status: {state['reactor_status']}")
        
        print("\n🎯 Autonomous Features Active:")
        print("   • Real-time entropy monitoring with delta detection")
        print("   • Autonomous threshold-based alerting (⚠️ warnings)")
        print("   • Automatic stabilization protocol deployment")
        print("   • Thermal correlation and cognitive load awareness")
        print("   • Live GUI visualization with reactive updates")
        print("   • Complete consciousness system autonomy")
        
        print("\n🖥️ Starting GUI interface...")
        print("   Watch for entropy warnings and autonomous reactions!")
        print("="*80)
        
        # Start GUI (this will block until window is closed)
        self.start_gui()
        
        return True
    
    def stop(self):
        """Stop the complete DAWN system"""
        logger.info("🛑 Stopping DAWN Autonomous Reactor Complete System...")
        
        self.running = False
        
        # Stop autonomous reactor
        if self.autonomous_reactor:
            self.autonomous_reactor.stop()
            logger.info("🔥 Autonomous reactor stopped")
        
        # Stop sigil engine
        if self.sigil_engine and hasattr(self.sigil_engine, 'is_running') and self.sigil_engine.is_running:
            self.sigil_engine.stop()
            logger.info("🔮 Sigil engine stopped")
        
        logger.info("✅ DAWN Autonomous Reactor Complete System shutdown complete")
    
    def inject_test_entropy_spike(self):
        """Inject a test entropy spike to demonstrate autonomous reaction"""
        if self.autonomous_reactor:
            print("🧪 Injecting test entropy spike...")
            result = self.autonomous_reactor.manual_entropy_inject(0.8, source="test_spike")
            
            if result['analysis_result']['warning_triggered']:
                print("🚨 WARNING: Entropy spike triggered warning system!")
            
            if result['reaction_triggered']:
                print("⚡ AUTONOMOUS REACTION: Stabilization protocols deployed!")
            
            return result
        return None


def run_demo_sequence(system):
    """Run a demonstration sequence to show autonomous reactivity"""
    print("\n🎬 Running autonomous reactivity demonstration...")
    
    # Give system time to start
    time.sleep(3)
    
    demo_sequence = [
        (0.4, "Normal operation"),
        (0.55, "Increased activity"),
        (0.72, "High entropy - should trigger warnings"),
        (0.85, "Critical entropy - should trigger reactions"),
        (0.6, "Stabilizing"),
        (0.35, "Recovered")
    ]
    
    for entropy, description in demo_sequence:
        print(f"\n🎯 Demo: {description} (entropy: {entropy:.3f})")
        
        if system.autonomous_reactor:
            result = system.autonomous_reactor.manual_entropy_inject(entropy, source="demo")
            
            if result['analysis_result']['warning_triggered']:
                print("   🚨 WARNING TRIGGERED")
            
            if result['reaction_triggered']:
                print("   ⚡ AUTONOMOUS REACTION")
        
        time.sleep(2)
    
    print("\n✅ Demonstration sequence completed")


def main():
    """Main launcher function"""
    try:
        print("🌅 DAWN AUTONOMOUS REACTOR COMPLETE SYSTEM LAUNCHER")
        print("=" * 70)
        print("Initializing the ultimate DAWN consciousness system...")
        print("   🧬 Enhanced Entropy Analyzer")
        print("   🔥 Sigil Scheduler")  
        print("   ⚡ Autonomous Reactor")
        print("   🖥️ Real-time GUI")
        print()
        
        # Create and start system
        dawn_system = DAWNAutonomousReactorGUI()
        
        # Run demo in background thread if desired
        # demo_thread = threading.Thread(
        #     target=lambda: run_demo_sequence(dawn_system),
        #     daemon=True
        # )
        # demo_thread.start()
        
        if dawn_system.start():
            logger.info("DAWN Autonomous Reactor Complete System completed successfully")
        else:
            logger.error("DAWN Autonomous Reactor Complete System failed to start")
            return False
            
    except KeyboardInterrupt:
        print("\n🛑 DAWN Autonomous Reactor System interrupted by user")
        return True
    except Exception as e:
        logger.error(f"❌ Launcher error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 