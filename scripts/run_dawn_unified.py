#!/usr/bin/env python3
"""
DAWN Unified System Launcher
Complete DAWN consciousness architecture with all integrated components

🧬 Unified launcher for the complete DAWN ecosystem:
- Pulse Controller (Thermal regulation)
- Sigil Engine (Cognitive command processing) 
- Entropy Analyzer (Chaos prediction & stabilization)
- GUI Interface (Real-time monitoring)
"""

import sys
import time
import random
import logging
import argparse
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(message)s'
)

def check_dawn_components():
    """Check availability of all DAWN components"""
    components = {
        'pulse_controller': False,
        'entropy_analyzer': False,
        'sigil_engine': False,
        'gui_interface': False,
        'reflex_system': False
    }
    
    print("🔍 Checking DAWN Component Availability...")
    print("=" * 50)
    
    # Test Pulse Controller
    try:
        from core.pulse_controller import PulseController
        components['pulse_controller'] = True
        print("✅ Pulse Controller: Available")
    except ImportError as e:
        print(f"❌ Pulse Controller: Missing - {e}")
    
    # Test Entropy Analyzer
    try:
        from core.dawn_entropy_analyzer import EnhancedEntropyAnalyzer
        components['entropy_analyzer'] = True
        print("✅ Entropy Analyzer: Available")
    except ImportError as e:
        print(f"❌ Entropy Analyzer: Missing - {e}")
    
    # Test Sigil Engine
    try:
        from core.sigil_engine import SigilEngine
        components['sigil_engine'] = True
        print("✅ Sigil Engine: Available")
    except ImportError as e:
        print(f"❌ Sigil Engine: Missing - {e}")
    
    # Test GUI Interface
    try:
        from gui.dawn_gui_enhanced import EnhancedDawnGUI
        components['gui_interface'] = True
        print("✅ GUI Interface: Available")
    except ImportError as e:
        print(f"❌ GUI Interface: Missing - {e}")
    
    # Test Reflex System
    try:
        from reflex.reflex_executor import ReflexExecutor
        components['reflex_system'] = True
        print("✅ Reflex System: Available")
    except ImportError as e:
        print(f"❌ Reflex System: Missing - {e}")
    
    # Test Cognitive Pressure Engine
    try:
        from core.cognitive_pressure import CognitivePressureEngine
        components['cognitive_pressure'] = True
        print("✅ Cognitive Pressure Engine: Available")
    except ImportError as e:
        print(f"❌ Cognitive Pressure Engine: Missing - {e}")
    
    # Test Conversation System
    try:
        from core.dawn_conversation import DAWNConversationEngine
        components['conversation_system'] = True
        print("✅ DAWN Conversation System: Available")
    except ImportError as e:
        print(f"❌ DAWN Conversation System: Missing - {e}")
    
    return components


class DAWNUnifiedSystem:
    """Unified DAWN consciousness system"""
    
    def __init__(self):
        """Initialize the unified DAWN system"""
        self.pulse_controller = None
        self.entropy_analyzer = None
        self.sigil_engine = None
        self.gui_interface = None
        self.reflex_executor = None
        self.cognitive_pressure_engine = None
        self.conversation_engine = None
        self.is_running = False
        self.tick_count = 0
        
        # System state
        self.system_state = {
            'pulse_zone': 'CALM',
            'entropy_level': 0.0,
            'heat_level': 0.0,
            'active_sigils': 0,
            'reflex_triggers': [],
            'cognitive_pressure': 0.0,
            'pressure_level': 'minimal',
            'pressure_alerts': [],
            'conversation_active': False,
            'conversation_id': '',
            'conversation_turns': 0
        }
        
        logging.info("DAWN Unified System initialized")
    
    def initialize_components(self):
        """Initialize all DAWN components"""
        print("\n🧬 Initializing DAWN Components...")
        print("=" * 40)
        
        # Initialize Pulse Controller
        try:
            from core.pulse_controller import PulseController
            self.pulse_controller = PulseController()
            print("✅ Pulse Controller initialized")
        except Exception as e:
            print(f"❌ Pulse Controller initialization failed: {e}")
            return False
        
        # Initialize Entropy Analyzer
        try:
            from core.dawn_entropy_analyzer import EnhancedEntropyAnalyzer
            self.entropy_analyzer = EnhancedEntropyAnalyzer()
            print("✅ Entropy Analyzer initialized")
        except Exception as e:
            print(f"❌ Entropy Analyzer initialization failed: {e}")
            return False
        
        # Initialize Sigil Engine
        try:
            from core.sigil_engine import SigilEngine
            self.sigil_engine = SigilEngine()
            print("✅ Sigil Engine initialized")
        except Exception as e:
            print(f"⚠️  Sigil Engine initialization failed: {e}")
            # Continue without sigil engine for now
        
        # Initialize Reflex Executor
        try:
            from reflex.reflex_executor import ReflexExecutor
            self.reflex_executor = ReflexExecutor()
            print("✅ Reflex Executor initialized")
        except Exception as e:
            print(f"⚠️  Reflex Executor initialization failed: {e}")
        
        # Initialize Cognitive Pressure Engine
        try:
            from core.cognitive_pressure import CognitivePressureEngine, initialize_pressure_engine
            self.cognitive_pressure_engine = initialize_pressure_engine(
                pulse_controller=self.pulse_controller,
                sigil_engine=self.sigil_engine,
                entropy_analyzer=self.entropy_analyzer
            )
            print("✅ Cognitive Pressure Engine initialized with component integration")
        except Exception as e:
            print(f"⚠️  Cognitive Pressure Engine initialization failed: {e}")
        
        # Initialize Enhanced Voice System
        try:
            from tracers.enhanced_tracer_echo_voice import get_enhanced_voice_echo
            self.voice_system = get_enhanced_voice_echo()
            print("✅ Enhanced Voice System initialized")
        except Exception as e:
            print(f"⚠️  Enhanced Voice System initialization failed: {e}")
        
        # Initialize Conversation Engine
        try:
            from core.dawn_conversation import DAWNConversationEngine, initialize_conversation_engine
            self.conversation_engine = initialize_conversation_engine(
                pulse_controller=self.pulse_controller,
                entropy_analyzer=self.entropy_analyzer,
                cognitive_pressure_engine=self.cognitive_pressure_engine
            )
            print("✅ DAWN Conversation Engine initialized with consciousness integration")
        except Exception as e:
            print(f"⚠️  DAWN Conversation Engine initialization failed: {e}")
        
        # Initialize GUI Interface (optional)
        try:
            from gui.dawn_gui_enhanced import EnhancedDawnGUI
            self.gui_interface = EnhancedDawnGUI()
            print("✅ GUI Interface initialized")
        except Exception as e:
            print(f"⚠️  GUI Interface initialization failed: {e}")
        
        return True
    
    def run_system_tick(self):
        """Execute one system tick"""
        self.tick_count += 1
        
        # Update pulse controller
        if self.pulse_controller:
            # Generate a simulated heat value for demonstration
            import random
            simulated_heat = random.uniform(20.0, 60.0)
            pulse_state = self.pulse_controller.update_heat(simulated_heat)
            self.system_state['pulse_zone'] = pulse_state.get('zone', 'STABLE')
            self.system_state['heat_level'] = pulse_state.get('current_heat', 25.0)
        
        # Update entropy analyzer
        if self.entropy_analyzer:
            # Generate sample entropy reading
            entropy_reading = random.uniform(0.1, 0.9)
            entropy_analysis = self.entropy_analyzer.analyze(entropy_reading)
            self.system_state['entropy_level'] = entropy_reading
        
        # Update sigil engine
        if self.sigil_engine:
            active_sigils = self.sigil_engine.get_active_count()
            self.system_state['active_sigils'] = active_sigils
        
        # Update cognitive pressure
        if self.cognitive_pressure_engine:
            try:
                pressure_snapshot = self.cognitive_pressure_engine.calculate_cognitive_pressure()
                self.system_state['cognitive_pressure'] = pressure_snapshot.cognitive_pressure
                self.system_state['pressure_level'] = pressure_snapshot.pressure_level.value
                self.system_state['pressure_alerts'] = [alert.value for alert in pressure_snapshot.active_alerts]
            except Exception as e:
                logging.warning(f"Cognitive pressure calculation error: {e}")
        
        # Update voice system state
        if hasattr(self, 'voice_system') and self.voice_system:
            try:
                # Update voice system with current cognitive state
                self.voice_system.entropy = self.system_state['entropy_level']
                self.voice_system.heat = self.system_state['heat_level']
                self.voice_system.zone = self.system_state['pulse_zone']
                self.voice_system.cognitive_pressure = self.system_state['cognitive_pressure']
                
                # Get conversation status
                conv_status = self.voice_system.get_conversation_status()
                self.system_state['conversation_active'] = conv_status['conversation_mode']
                self.system_state['voice_enabled'] = conv_status['voice_enabled']
            except Exception as e:
                logging.warning(f"Voice system state update error: {e}")
        
        # Update conversation state (legacy)
        if self.conversation_engine:
            try:
                conv_status = self.conversation_engine.get_conversation_status()
                self.system_state['conversation_active'] = conv_status['is_active']
                self.system_state['conversation_id'] = conv_status['conversation_id']
                self.system_state['conversation_turns'] = conv_status['turns_in_session']
            except Exception as e:
                logging.warning(f"Conversation status error: {e}")
        
        # Execute reflexes
        if self.reflex_executor:
            reflex_triggers = self.reflex_executor.evaluate_triggers(self.system_state)
            self.system_state['reflex_triggers'] = reflex_triggers
        
        # Update GUI
        if self.gui_interface:
            self.gui_interface.update_state(self.system_state)
    
    def run(self, duration_seconds: Optional[int] = None):
        """Run the unified DAWN system"""
        print(f"\n🌟 Starting DAWN Unified System")
        print("=" * 40)
        
        if not self.initialize_components():
            print("❌ Component initialization failed - aborting")
            return False
        
        self.is_running = True
        start_time = time.time()
        
        try:
            while self.is_running:
                # Execute system tick
                self.run_system_tick()
                
                # Display status every 10 ticks
                if self.tick_count % 10 == 0:
                    self.display_status()
                
                # Check duration limit
                if duration_seconds and (time.time() - start_time) > duration_seconds:
                    print(f"\n⏰ Duration limit reached ({duration_seconds}s)")
                    break
                
                # Sleep to control tick rate (10 FPS)
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n⏹️  Shutdown requested by user")
        except Exception as e:
            print(f"\n❌ System error: {e}")
            logging.exception("System error")
        finally:
            self.shutdown()
        
        return True
    
    def display_status(self):
        """Display current system status"""
        status = self.system_state
        print(f"\n📊 DAWN Status [Tick {self.tick_count}]")
        print(f"   Pulse Zone: {status['pulse_zone']}")
        print(f"   Heat Level: {status['heat_level']:.3f}")
        print(f"   Entropy: {status['entropy_level']:.3f}")
        print(f"   Active Sigils: {status['active_sigils']}")
        print(f"   🧠 Cognitive Pressure: {status['cognitive_pressure']:.2f} ({status['pressure_level']})")
        if status['pressure_alerts']:
            print(f"   🚨 Pressure Alerts: {', '.join(status['pressure_alerts'])}")
        
        # Voice and conversation status
        voice_status = "🔊" if status.get('voice_enabled', False) else "🔇"
        if status['conversation_active']:
            print(f"   💬 Conversation: Active {voice_status} (ID: {status.get('conversation_id', 'N/A')}, Turns: {status.get('conversation_turns', 0)})")
        else:
            print(f"   💬 Conversation: Inactive {voice_status}")
        
        if status['reflex_triggers']:
            print(f"   Reflex Triggers: {', '.join(status['reflex_triggers'])}")
    
    def shutdown(self):
        """Shutdown the DAWN system"""
        print("\n🔄 Shutting down DAWN Unified System...")
        
        self.is_running = False
        
        # Shutdown components gracefully
        if self.gui_interface:
            try:
                self.gui_interface.shutdown()
                print("✅ GUI Interface shutdown")
            except Exception as e:
                print(f"⚠️  GUI shutdown error: {e}")
        
        if self.pulse_controller:
            try:
                self.pulse_controller.shutdown()
                print("✅ Pulse Controller shutdown")
            except Exception as e:
                print(f"⚠️  Pulse Controller shutdown error: {e}")
        
        print("🌙 DAWN Unified System shutdown complete")
    
    def handle_console_command(self, command: str):
        """Handle console commands for system interaction"""
        parts = command.strip().split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        
        if cmd == "status":
            self.display_status()
        
        elif cmd == "pressure":
            self.display_pressure_status()
        
        elif cmd == "cognitive":
            self.display_cognitive_breakdown()
        
        elif cmd == "thermal":
            self.display_thermal_status()
        
        elif cmd == "entropy":
            self.display_entropy_status()
        
        elif cmd == "talk":
            self.start_conversation_mode()
        
        elif cmd == "stop_talk" or cmd == "end_talk":
            self.stop_conversation_mode()
        
        elif cmd == "say" and len(parts) > 1:
            # Handle text input to DAWN in conversation mode
            message = " ".join(parts[1:])
            self.process_conversation_input(message)
        
        elif cmd == "conversation" or cmd == "conv":
            self.display_conversation_status()
        
        elif cmd.startswith("voice"):
            if len(parts) > 1:
                if parts[1] == "on":
                    if hasattr(self, 'voice_system') and self.voice_system:
                        self.voice_system.toggle_voice_output(True)
                        print("🔊 Voice output enabled")
                    else:
                        print("❌ Voice system not available")
                elif parts[1] == "off":
                    if hasattr(self, 'voice_system') and self.voice_system:
                        self.voice_system.toggle_voice_output(False)
                        print("🔇 Voice output disabled")
                    else:
                        print("❌ Voice system not available")
                else:
                    print("❌ Usage: voice [on/off]")
            else:
                # Toggle voice output
                if hasattr(self, 'voice_system') and self.voice_system:
                    self.voice_system.toggle_voice_output()
                    status = "enabled" if self.voice_system.voice_enabled else "disabled"
                    print(f"🔊 Voice output {status}")
                else:
                    print("❌ Voice system not available")
        
        elif cmd == "help":
            self.display_help()
        
        else:
            print(f"❌ Unknown command: {cmd}. Type 'help' for available commands.")
    
    def display_pressure_status(self):
        """Display current cognitive pressure status"""
        if not self.cognitive_pressure_engine:
            print("❌ Cognitive Pressure Engine not available")
            return
        
        state = self.cognitive_pressure_engine.get_current_state()
        print(f"\n🧠 Cognitive Pressure Status")
        print("=" * 40)
        print(f"Current Pressure (P): {state['cognitive_pressure']:.2f}")
        print(f"Pressure Level: {state['pressure_level']}")
        print(f"Last Update: {time.ctime(state['last_update'])}")
        print(f"Calculation Count: {state['calculation_count']}")
        print(f"Alert Count: {state['alert_count']}")
        print(f"Avg Calculation Time: {state['average_calculation_time']:.4f}s")
        
        # Component status
        print(f"\n🔧 Component Integration:")
        components = state['component_status']
        print(f"  Pulse Controller: {'✅' if components['pulse_controller'] else '❌'}")
        print(f"  Sigil Engine: {'✅' if components['sigil_engine'] else '❌'}")
        print(f"  Entropy Analyzer: {'✅' if components['entropy_analyzer'] else '❌'}")
        
        # Integration flags
        flags = state['integration_flags']
        print(f"\n⚙️  Integration Settings:")
        print(f"  Thermal Coupling: {'✅' if flags['thermal_coupling'] else '❌'}")
        print(f"  Entropy Feedback: {'✅' if flags['entropy_feedback'] else '❌'}")
        print(f"  Alert System: {'✅' if flags['alert_system'] else '❌'}")
    
    def display_cognitive_breakdown(self):
        """Display detailed cognitive pressure breakdown"""
        if not self.cognitive_pressure_engine:
            print("❌ Cognitive Pressure Engine not available")
            return
        
        breakdown = self.cognitive_pressure_engine.get_pressure_breakdown()
        if 'error' in breakdown:
            print(f"❌ {breakdown['error']}")
            return
        
        print(f"\n🧠 Cognitive Pressure Breakdown (P = Bσ²)")
        print("=" * 50)
        
        # Bloom Mass (B) breakdown
        bloom = breakdown['bloom_mass_breakdown']
        print(f"\n🌸 Bloom Mass (B): {bloom['total']:.2f}")
        print(f"  Sigil Queue Size: {bloom['sigil_queue_size']:.2f}")
        print(f"  Sigil Execution Load: {bloom['sigil_execution_load']:.2f}")
        print(f"  Entropy Activity: {bloom['entropy_activity']:.2f}")
        print(f"  Thermal Contribution: {bloom['thermal_contribution']:.2f}")
        print(f"  Memory Load: {bloom['memory_load']:.2f}")
        
        # Sigil Velocity (σ) breakdown
        velocity = breakdown['sigil_velocity_breakdown']
        print(f"\n⚡ Sigil Velocity (σ): {velocity['total']:.2f}")
        print(f"  Recent Executions: {velocity['recent_executions']:.2f}")
        print(f"  Processing Speed: {velocity['processing_speed']:.2f}")
        print(f"  Entropy Change Rate: {velocity['entropy_change_rate']:.2f}")
        print(f"  Thermal Momentum: {velocity['thermal_momentum']:.2f}")
        print(f"  Cognitive Acceleration: {velocity['cognitive_acceleration']:.2f}")
        
        # Pressure calculation
        calc = breakdown['pressure_calculation']
        print(f"\n🧮 Pressure Calculation:")
        print(f"  B (Bloom Mass): {calc['bloom_mass_B']:.2f}")
        print(f"  σ (Sigil Velocity): {calc['sigil_velocity_sigma']:.2f}")
        print(f"  σ² (Velocity Squared): {calc['velocity_squared']:.2f}")
        print(f"  P = B × σ²: {calc['cognitive_pressure_P']:.2f}")
        print(f"  Pressure Level: {calc['pressure_level']}")
        
        # System integration
        integration = breakdown['system_integration']
        print(f"\n🔗 System Integration:")
        print(f"  Thermal Coupling: {integration['thermal_coupling']:.3f}")
        print(f"  Pulse Zone Influence: {integration['pulse_zone_influence']}")
        print(f"  Entropy Feedback: {integration['entropy_feedback']:.3f}")
        print(f"  System Health: {integration['system_health']}")
        
        # Alerts and recommendations
        if breakdown['alerts']:
            print(f"\n🚨 Active Alerts:")
            for alert in breakdown['alerts']:
                print(f"  • {alert}")
        
        if breakdown['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in breakdown['recommendations']:
                print(f"  • {rec}")
    
    def display_thermal_status(self):
        """Display thermal system status"""
        if not self.pulse_controller:
            print("❌ Pulse Controller not available")
            return
        
        print(f"\n🌡️  Thermal System Status")
        print("=" * 30)
        print(f"Current Heat: {self.system_state['heat_level']:.3f}")
        print(f"Pulse Zone: {self.system_state['pulse_zone']}")
        
        # If pulse controller has additional methods, call them
        if hasattr(self.pulse_controller, 'get_thermal_state'):
            try:
                thermal_state = self.pulse_controller.get_thermal_state()
                for key, value in thermal_state.items():
                    print(f"{key}: {value}")
            except Exception as e:
                print(f"Error getting thermal details: {e}")
    
    def display_entropy_status(self):
        """Display entropy system status"""
        if not self.entropy_analyzer:
            print("❌ Entropy Analyzer not available")
            return
        
        print(f"\n📊 Entropy System Status")
        print("=" * 30)
        print(f"Current Entropy: {self.system_state['entropy_level']:.3f}")
        
        # If entropy analyzer has additional methods, call them
        if hasattr(self.entropy_analyzer, 'get_analysis_state'):
            try:
                entropy_state = self.entropy_analyzer.get_analysis_state()
                for key, value in entropy_state.items():
                    print(f"{key}: {value}")
            except Exception as e:
                print(f"Error getting entropy details: {e}")
    
    def start_conversation_mode(self):
        """Start conversation mode with DAWN"""
        if not hasattr(self, 'voice_system') or not self.voice_system:
            print("❌ Voice system not available")
            return
        
        success = self.voice_system.enter_conversation_mode()
        if success:
            print("💬 Conversation mode started!")
            print("🎤 DAWN is listening for speech input (if microphone available)")
            print("💭 Type 'say <message>' to send text to DAWN")
            print("🔊 Type 'voice on/off' to toggle voice output")
            print("🛑 Type 'stop_talk' to end conversation")
        else:
            print("❌ Failed to start conversation")
    
    def stop_conversation_mode(self):
        """Stop conversation mode"""
        if not hasattr(self, 'voice_system') or not self.voice_system:
            print("❌ Voice system not available")
            return
        
        self.voice_system.exit_conversation_mode()
        print("💬 Conversation mode ended")
    
    def process_conversation_input(self, message: str):
        """Process text input to DAWN during conversation"""
        if not hasattr(self, 'voice_system') or not self.voice_system:
            print("❌ Voice system not available")
            return
        
        conv_status = self.voice_system.get_conversation_status()
        if not conv_status['conversation_mode']:
            print("❌ Conversation not active. Type 'talk' to start.")
            return
        
        print(f"👤 Jackson: {message}")
        
        # Generate response using conversation response generator
        if hasattr(self.voice_system, 'conversation_response') and self.voice_system.conversation_response:
            response = self.voice_system.conversation_response.generate_response(message)
            print(f"🤖 DAWN: {response}")
            
            # Speak the response if voice is enabled
            if self.voice_system.voice_enabled:
                self.voice_system.speak_with_state_modulation(response)
        else:
            print("❌ Conversation response generator not available")
    
    def display_conversation_status(self):
        """Display conversation system status"""
        if not hasattr(self, 'voice_system') or not self.voice_system:
            print("❌ Voice system not available")
            return
        
        status = self.voice_system.get_conversation_status()
        
        print(f"\n💬 DAWN Conversation Status")
        print("=" * 40)
        print(f"Conversation Available: {'✅' if status['conversation_available'] else '❌'}")
        print(f"Conversation Active: {'✅' if status['conversation_mode'] else '❌'}")
        print(f"Voice Output: {'✅' if status['voice_enabled'] else '❌'}")
        
        if status['conversation_mode']:
            print(f"Listening: {'✅' if status['listening'] else '❌'}")
            print(f"Queue Size: {status['queue_size']}")
        
        # Show conversation statistics if available
        if 'conversation_stats' in status:
            stats = status['conversation_stats']
            print(f"\n📊 Conversation Statistics:")
            print(f"  Total Exchanges: {stats['total_exchanges']}")
            print(f"  Average Entropy: {stats['average_entropy']:.3f}")
            print(f"  Average SCUP: {stats['average_scup']:.1f}")
            print(f"  Average Heat: {stats['average_heat']:.1f}°C")
        
        print(f"\n💭 Use 'say <message>' to talk to DAWN")
        print(f"🔊 Use 'voice on/off' to toggle voice output")
        print(f"🛑 Use 'stop_talk' to end conversation")

    def display_help(self):
        """Display available console commands"""
        print(f"\n📖 DAWN Console Commands")
        print("=" * 30)
        print("  status       - Display overall system status")
        print("  pressure     - Show cognitive pressure (P = Bσ²) status")
        print("  cognitive    - Detailed cognitive pressure breakdown")
        print("  thermal      - Display thermal system status")
        print("  entropy      - Display entropy analyzer status")
        print("  talk         - Start conversation mode with DAWN")
        print("  stop_talk    - End conversation mode")
        print("  say <msg>    - Send text message to DAWN (in conversation)")
        print("  voice [on/off] - Toggle voice output")
        print("  conversation - Display conversation system status")
        print("  help         - Show this help message")
        print("\n💬 Conversation Commands:")
        print("  talk                    - Start voice/text conversation")
        print("  say Hello DAWN!         - Send text to DAWN")
        print("  voice on/off            - Toggle voice output")
        print("  stop_talk               - End conversation")
        print("\nType any command and press Enter")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='DAWN Unified System Launcher')
    parser.add_argument('--check-only', action='store_true',
                       help='Only check component availability')
    parser.add_argument('--duration', type=int, default=None,
                       help='Run duration in seconds (default: unlimited)')
    parser.add_argument('--no-gui', action='store_true',
                       help='Run without GUI interface')
    
    args = parser.parse_args()
    
    print("🧬 DAWN Unified System Launcher")
    print("=" * 50)
    
    # Check component availability
    components = check_dawn_components()
    
    # Count available components
    available_count = sum(components.values())
    total_count = len(components)
    
    print(f"\n📋 Component Summary: {available_count}/{total_count} available")
    
    if args.check_only:
        return
    
    # Require minimum components to run
    required_components = ['pulse_controller', 'entropy_analyzer']
    missing_required = [comp for comp in required_components if not components[comp]]
    
    if missing_required:
        print(f"\n❌ Missing required components: {', '.join(missing_required)}")
        print("Cannot start DAWN system without core components")
        sys.exit(1)
    
    # Initialize and run the system
    dawn_system = DAWNUnifiedSystem()
    
    try:
        success = dawn_system.run(duration_seconds=args.duration)
        if success:
            print("\n🎉 DAWN Unified System completed successfully")
        else:
            print("\n❌ DAWN Unified System failed to start")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        logging.exception("Unexpected error")
        sys.exit(1)


if __name__ == "__main__":
    main() 