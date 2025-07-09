#!/usr/bin/env python3
"""
Connect Owl Bloom Log and Sigil Stream
======================================
Integration script that connects DAWN's Owl bloom monitoring system
with the Sigil command stream for real-time cognitive processing.

This script:
1. Initializes the Owl-Sigil Bridge
2. Connects to existing DAWN backend systems
3. Integrates with GUI components
4. Provides real-time monitoring and logging
"""

import sys
import os
import time
import threading
import argparse
import logging
from typing import Dict, Any

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import DAWN components
try:
    from core.owl_sigil_bridge import OwlSigilBridge, get_owl_sigil_bridge, initialize_bridge_with_systems
    from core.sigil_engine import SigilEngine
    from backend.visual.sigil_command_stream_visualizer import get_sigil_command_stream_visualizer
    from gui.dawn_gui_integration import DAWNGuiIntegration
    from run_dawn_unified import create_dawn_unified_system
    COMPONENTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Some DAWN components not available: {e}")
    COMPONENTS_AVAILABLE = False


class OwlSigilConnectionManager:
    """Manages the connection between Owl and Sigil systems"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.running = False
        
        # Core systems
        self.bridge = None
        self.sigil_engine = None
        self.sigil_visualizer = None
        self.dawn_system = None
        self.gui_integration = None
        
        # Connection status
        self.connections = {
            'bridge': False,
            'sigil_engine': False,
            'visualizer': False,
            'dawn_system': False,
            'gui': False
        }
        
        # Performance tracking
        self.metrics = {
            'start_time': time.time(),
            'bloom_events': 0,
            'sigil_commands': 0,
            'reflections': 0,
            'connection_uptime': 0
        }
        
        self.logger.info("🔗 Owl-Sigil Connection Manager initialized")
    
    def initialize_systems(self):
        """Initialize all required systems and connections"""
        try:
            print("🚀 Initializing Owl-Sigil Stream Connection...")
            
            # 1. Initialize bridge
            self._initialize_bridge()
            
            # 2. Connect to DAWN unified system
            self._connect_dawn_system()
            
            # 3. Initialize sigil engine
            self._initialize_sigil_engine()
            
            # 4. Connect sigil visualizer
            self._connect_sigil_visualizer()
            
            # 5. Setup GUI integration
            self._setup_gui_integration()
            
            # 6. Configure monitoring callbacks
            self._setup_monitoring_callbacks()
            
            print("✅ All systems initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"System initialization failed: {e}")
            print(f"❌ System initialization failed: {e}")
            return False
    
    def _initialize_bridge(self):
        """Initialize the Owl-Sigil bridge"""
        self.bridge = get_owl_sigil_bridge()
        
        # Configure bridge settings
        self.bridge.config.update({
            'bloom_scan_interval': 1.5,  # Faster scanning
            'enable_auto_reflection': True,
            'log_all_events': True,
            'entropy_alert_threshold': 0.65
        })
        
        self.connections['bridge'] = True
        print("🦉🔮 Owl-Sigil Bridge initialized")
    
    def _connect_dawn_system(self):
        """Connect to DAWN unified system"""
        try:
            if COMPONENTS_AVAILABLE:
                self.dawn_system = create_dawn_unified_system()
                if self.dawn_system.get('status') == 'ready':
                    self.connections['dawn_system'] = True
                    print("🌅 Connected to DAWN unified system")
                else:
                    print("⚠️ DAWN system not ready")
            else:
                print("⚠️ DAWN unified system not available")
                
        except Exception as e:
            self.logger.error(f"DAWN system connection failed: {e}")
            print(f"⚠️ DAWN system connection failed: {e}")
    
    def _initialize_sigil_engine(self):
        """Initialize sigil engine for command execution"""
        try:
            # Use existing engine from DAWN system or create new one
            if self.dawn_system and 'sigil_engine' in self.dawn_system:
                self.sigil_engine = self.dawn_system['sigil_engine']
                print("🔮 Using existing DAWN sigil engine")
            else:
                self.sigil_engine = SigilEngine(initial_heat=30.0)
                print("🔮 Created new sigil engine")
            
            # Connect to bridge
            self.bridge.connect_sigil_engine(self.sigil_engine)
            self.connections['sigil_engine'] = True
            
        except Exception as e:
            self.logger.error(f"Sigil engine initialization failed: {e}")
            print(f"⚠️ Sigil engine initialization failed: {e}")
    
    def _connect_sigil_visualizer(self):
        """Connect sigil command stream visualizer"""
        try:
            self.sigil_visualizer = get_sigil_command_stream_visualizer()
            
            # Connect to bridge
            self.bridge.connect_sigil_visualizer(self.sigil_visualizer)
            self.connections['visualizer'] = True
            
            # Start visualization
            self.sigil_visualizer.start_animation()
            
            print("🎨 Sigil command stream visualizer connected and started")
            
        except Exception as e:
            self.logger.error(f"Sigil visualizer connection failed: {e}")
            print(f"⚠️ Sigil visualizer connection failed: {e}")
    
    def _setup_gui_integration(self):
        """Setup GUI integration for real-time monitoring"""
        try:
            if COMPONENTS_AVAILABLE:
                self.gui_integration = DAWNGuiIntegration()
                
                # Configure GUI to display owl-sigil bridge data
                self.gui_integration.enable_owl_sigil_monitoring = True
                
                self.connections['gui'] = True
                print("🖥️ GUI integration configured")
            else:
                print("⚠️ GUI integration not available")
                
        except Exception as e:
            self.logger.error(f"GUI integration setup failed: {e}")
            print(f"⚠️ GUI integration setup failed: {e}")
    
    def _setup_monitoring_callbacks(self):
        """Setup monitoring callbacks for logging and metrics"""
        
        def on_bloom_detected(bloom_data):
            """Handle bloom detection"""
            self.metrics['bloom_events'] += 1
            bloom_id = bloom_data.get('seed_id', 'unknown')
            entropy = bloom_data.get('entropy', 0.0)
            
            print(f"🌸 Bloom detected: {bloom_id} (entropy: {entropy:.3f})")
            
            # Log to DAWN system if available
            if self.dawn_system and 'pulse_controller' in self.dawn_system:
                pulse = self.dawn_system['pulse_controller']
                # Potential heat adjustment based on bloom activity
                if entropy > 0.7:
                    pulse.update_heat(pulse.current_heat + 5)
        
        def on_sigil_triggered(sigil, urgency):
            """Handle sigil trigger"""
            self.metrics['sigil_commands'] += 1
            print(f"🔮 Sigil activated: {sigil} (urgency: {urgency:.2f})")
        
        def on_reflection_generated(reflection, bloom_data):
            """Handle reflection generation"""
            self.metrics['reflections'] += 1
            print(f"💭 Owl reflection: {reflection}")
            
            # Feed reflection to GUI if available
            if self.gui_integration:
                try:
                    self.gui_integration.update_owl_reflection(reflection)
                except Exception as e:
                    self.logger.error(f"GUI reflection update failed: {e}")
        
        # Register callbacks with bridge
        self.bridge.on_bloom_detected(on_bloom_detected)
        self.bridge.on_reflection_generated(on_reflection_generated)
        
        print("📊 Monitoring callbacks configured")
    
    def start_monitoring(self):
        """Start the complete monitoring system"""
        if not self.bridge:
            print("❌ Bridge not initialized")
            return False
        
        try:
            # Start bridge monitoring
            self.bridge.start_monitoring()
            
            # Start performance monitoring
            self._start_performance_monitoring()
            
            self.running = True
            print("🚀 Owl-Sigil stream monitoring started")
            
            # Display connection status
            self._display_connection_status()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start monitoring: {e}")
            print(f"❌ Failed to start monitoring: {e}")
            return False
    
    def stop_monitoring(self):
        """Stop the monitoring system"""
        self.running = False
        
        if self.bridge:
            self.bridge.stop_monitoring()
        
        if self.sigil_visualizer:
            self.sigil_visualizer.stop_animation()
        
        print("🛑 Owl-Sigil monitoring stopped")
    
    def _start_performance_monitoring(self):
        """Start performance metrics monitoring"""
        def performance_monitor():
            while self.running:
                try:
                    time.sleep(10)  # Update every 10 seconds
                    self._update_performance_metrics()
                    self._log_system_status()
                except Exception as e:
                    self.logger.error(f"Performance monitoring error: {e}")
        
        monitor_thread = threading.Thread(target=performance_monitor, daemon=True)
        monitor_thread.start()
    
    def _update_performance_metrics(self):
        """Update performance metrics"""
        self.metrics['connection_uptime'] = time.time() - self.metrics['start_time']
        
        # Get bridge metrics
        if self.bridge:
            bridge_status = self.bridge.get_bridge_status()
            bridge_metrics = bridge_status.get('performance_metrics', {})
            
            # Update with bridge data
            self.metrics.update({
                'bridge_events': bridge_metrics.get('events_processed', 0),
                'bridge_sigils': bridge_metrics.get('sigils_triggered', 0),
                'bridge_reflections': bridge_metrics.get('reflections_generated', 0),
                'active_blooms': bridge_status.get('active_blooms', 0),
                'queued_events': bridge_status.get('queued_events', 0)
            })
    
    def _log_system_status(self):
        """Log current system status"""
        status_msg = (
            f"[Status] Uptime: {self.metrics['connection_uptime']:.0f}s | "
            f"Blooms: {self.metrics.get('active_blooms', 0)} | "
            f"Events: {self.metrics.get('bridge_events', 0)} | "
            f"Sigils: {self.metrics.get('bridge_sigils', 0)} | "
            f"Queue: {self.metrics.get('queued_events', 0)}"
        )
        self.logger.info(status_msg)
    
    def _display_connection_status(self):
        """Display current connection status"""
        print("\n📡 Connection Status:")
        for system, connected in self.connections.items():
            status = "✅ Connected" if connected else "❌ Disconnected"
            print(f"  {system.capitalize()}: {status}")
        print()
    
    def inject_test_sigil(self, sigil: str = "◉", urgency: float = 0.6):
        """Inject a test sigil for demonstration"""
        if self.bridge:
            self.bridge.inject_external_sigil(sigil, "test", urgency)
            print(f"🧪 Test sigil {sigil} injected")
        else:
            print("❌ Bridge not available for test injection")
    
    def get_status_report(self) -> Dict[str, Any]:
        """Get comprehensive status report"""
        self._update_performance_metrics()
        
        report = {
            'connections': self.connections.copy(),
            'metrics': self.metrics.copy(),
            'running': self.running,
            'bridge_status': self.bridge.get_bridge_status() if self.bridge else None,
            'recent_activity': self.bridge.get_recent_activity(5) if self.bridge else []
        }
        
        return report
    
    def run_interactive_mode(self):
        """Run in interactive mode with user commands"""
        print("\n🎛️ Interactive Mode Commands:")
        print("  'status' - Show system status")
        print("  'inject <sigil>' - Inject test sigil")
        print("  'metrics' - Show performance metrics")
        print("  'quit' - Exit")
        print()
        
        while self.running:
            try:
                command = input("owl-sigil> ").strip().lower()
                
                if command == 'quit':
                    break
                elif command == 'status':
                    self._display_connection_status()
                    if self.bridge:
                        bridge_status = self.bridge.get_bridge_status()
                        print(f"Bridge: {bridge_status}")
                elif command == 'metrics':
                    print(f"Performance Metrics: {self.metrics}")
                elif command.startswith('inject'):
                    parts = command.split()
                    sigil = parts[1] if len(parts) > 1 else "◉"
                    self.inject_test_sigil(sigil)
                elif command == 'help':
                    print("Available commands: status, inject <sigil>, metrics, quit")
                else:
                    print("Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Command error: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Connect Owl Bloom Log and Sigil Stream")
    parser.add_argument('--mode', choices=['auto', 'interactive', 'demo'], 
                       default='auto', help='Running mode')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--no-gui', action='store_true',
                       help='Disable GUI integration')
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🦉🔮 DAWN Owl-Sigil Stream Connection")
    print("=" * 50)
    
    # Initialize connection manager
    manager = OwlSigilConnectionManager()
    
    # Disable GUI if requested
    if args.no_gui:
        manager.connections['gui'] = 'disabled'
    
    # Initialize systems
    if not manager.initialize_systems():
        print("❌ Failed to initialize systems")
        return 1
    
    # Start monitoring
    if not manager.start_monitoring():
        print("❌ Failed to start monitoring")
        return 1
    
    try:
        if args.mode == 'demo':
            print("\n🎮 Demo Mode - Injecting test sigils...")
            time.sleep(2)
            
            # Inject some demo sigils
            test_sigils = ["◉", "◆", "▲", "✦", "⬢", "⚡"]
            for i, sigil in enumerate(test_sigils):
                time.sleep(3)
                urgency = 0.3 + (i * 0.1)
                manager.inject_test_sigil(sigil, urgency)
                print(f"Demo sigil {i+1}/{len(test_sigils)}: {sigil}")
            
            print("\n📊 Demo completed. System continues monitoring...")
            
        if args.mode == 'interactive':
            manager.run_interactive_mode()
        else:
            # Auto mode - just run and display status
            print("🔄 Auto monitoring mode - Press Ctrl+C to stop")
            while True:
                time.sleep(30)
                report = manager.get_status_report()
                print(f"📊 Active blooms: {report['metrics'].get('active_blooms', 0)} | "
                      f"Events processed: {report['metrics'].get('bridge_events', 0)} | "
                      f"Uptime: {report['metrics']['connection_uptime']:.0f}s")
    
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down...")
    
    finally:
        manager.stop_monitoring()
        print("✅ Owl-Sigil connection terminated")
    
    return 0


if __name__ == "__main__":
    exit(main()) 