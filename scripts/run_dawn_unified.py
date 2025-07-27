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
        self.is_running = False
        self.tick_count = 0
        
        # System state
        self.system_state = {
            'pulse_zone': 'CALM',
            'entropy_level': 0.0,
            'heat_level': 0.0,
            'active_sigils': 0,
            'reflex_triggers': []
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
            pulse_state = self.pulse_controller.tick()
            self.system_state['pulse_zone'] = pulse_state.get('zone', 'CALM')
            self.system_state['heat_level'] = pulse_state.get('heat', 0.0)
        
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