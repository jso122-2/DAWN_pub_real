#!/usr/bin/env python3
"""
DAWN Autonomous Reactor Integration
Complete integration of Enhanced Entropy Analyzer + Sigil Scheduler + Autonomous Reactor
"""

import sys
import os
import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def integrate_autonomous_reactor_system():
    """
    Integrate the complete DAWN autonomous reactor system.
    
    Returns:
        Tuple of (success, reactor, components_status)
    """
    logger.info("🧬 Starting DAWN Autonomous Reactor System Integration")
    
    components_status = {
        'enhanced_entropy_analyzer': False,
        'sigil_scheduler': False,
        'autonomous_reactor': False,
        'pulse_controller': False,
        'sigil_engine': False,
        'system_integration': False
    }
    
    try:
        # Import core components
        print("📦 Importing DAWN autonomous reactor components...")
        
        # Enhanced Entropy Analyzer
        try:
            from core.dawn_entropy_analyzer import EnhancedEntropyAnalyzer
            components_status['enhanced_entropy_analyzer'] = True
            print("✅ Enhanced Entropy Analyzer imported")
        except ImportError as e:
            print(f"❌ Enhanced Entropy Analyzer failed: {e}")
            return False, None, components_status
        
        # Sigil Scheduler
        try:
            from core.dawn_sigil_scheduler import DAWNSigilScheduler
            components_status['sigil_scheduler'] = True
            print("✅ DAWN Sigil Scheduler imported")
        except ImportError as e:
            print(f"❌ DAWN Sigil Scheduler failed: {e}")
            return False, None, components_status
        
        # Autonomous Reactor
        try:
            from core.dawn_autonomous_reactor import DAWNAutonomousReactor
            components_status['autonomous_reactor'] = True
            print("✅ DAWN Autonomous Reactor imported")
        except ImportError as e:
            print(f"❌ DAWN Autonomous Reactor failed: {e}")
            return False, None, components_status
        
        # Try to initialize supporting components
        pulse_controller = None
        try:
            from core.pulse_controller import PulseController
            pulse_controller = PulseController(initial_heat=30.0)
            components_status['pulse_controller'] = True
            print("✅ Pulse Controller initialized")
        except ImportError:
            print("⚠️ Pulse Controller not available (will use simulation mode)")
        
        sigil_engine = None
        try:
            from core.sigil_engine import SigilEngine
            sigil_engine = SigilEngine(initial_heat=30.0)
            components_status['sigil_engine'] = True
            print("✅ Sigil Engine initialized")
        except ImportError:
            print("⚠️ Sigil Engine not available (will use simulation mode)")
        
        # Create the complete autonomous reactor system
        print("\n🚀 Creating DAWN Autonomous Reactor System...")
        
        reactor = DAWNAutonomousReactor(
            pulse_controller=pulse_controller,
            sigil_engine=sigil_engine,
            entropy_threshold=0.6,
            auto_start=False  # We'll start it manually after setup
        )
        
        components_status['system_integration'] = True
        print("✅ Autonomous Reactor System created successfully")
        
        # Test the system
        print("\n🧪 Testing autonomous reactor system...")
        
        # Enable debug mode for testing
        reactor.enable_debug_mode(True)
        
        # Run comprehensive test
        test_result = reactor.test_reactor([0.3, 0.5, 0.65, 0.8, 0.45])
        
        if test_result['summary']['warnings_triggered'] > 0:
            print("✅ Entropy warning system functional")
        
        if test_result['summary']['reactions_triggered'] > 0:
            print("✅ Autonomous reaction system functional")
        
        # Get system metrics
        metrics = reactor.get_performance_metrics()
        state = reactor.get_reactor_state()
        
        print("\n📊 Autonomous Reactor System Status:")
        print(f"  Reactor Status: {state['reactor_status']}")
        print(f"  Current Entropy: {state['entropy_level']:.3f}")
        print(f"  Entropy Status: {state['entropy_status']}")
        print(f"  Active Sigils: {state['active_sigils']}")
        
        if pulse_controller:
            print(f"  Thermal Heat: {state['thermal_heat']:.1f}°C")
            print(f"  Thermal Zone: {state['thermal_zone']}")
        
        print("\n🎯 Performance Metrics:")
        print(f"  Total Entropy Readings: {metrics['total_entropy_readings']}")
        print(f"  Total Reactions: {metrics['total_reactions']}")
        print(f"  Autonomous Interventions: {metrics['autonomous_interventions']}")
        print(f"  Stabilization Attempts: {metrics['stabilization_attempts']}")
        
        # Component-specific metrics
        if 'entropy_analyzer' in metrics:
            analyzer_metrics = metrics['entropy_analyzer']
            print(f"\n🔍 Entropy Analyzer Metrics:")
            print(f"  Total Warnings: {analyzer_metrics['total_warnings']}")
            print(f"  Rapid Rise Events: {analyzer_metrics['rapid_rise_events']}")
            print(f"  Warning Rate: {analyzer_metrics['warning_rate']:.3f}")
        
        if 'sigil_scheduler' in metrics:
            scheduler_stats = metrics['sigil_scheduler']
            print(f"\n🔥 Sigil Scheduler Metrics:")
            print(f"  Total Triggers: {scheduler_stats['total_triggers']}")
            print(f"  Successful Triggers: {scheduler_stats['successful_triggers']}")
            print(f"  Threshold Breaches: {scheduler_stats['threshold_breaches']}")
        
        print("\n🎉 DAWN Autonomous Reactor System integration completed successfully!")
        
        return True, reactor, components_status
        
    except Exception as e:
        logger.error(f"❌ Autonomous reactor system integration failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None, components_status


def demonstrate_autonomous_reactivity(reactor):
    """
    Demonstrate the autonomous reactivity system in action.
    
    Args:
        reactor: The DAWNAutonomousReactor instance
    """
    print("\n" + "="*70)
    print("🧠 DAWN AUTONOMOUS REACTIVITY DEMONSTRATION")
    print("="*70)
    
    # Start the reactor for live demonstration
    print("🚀 Starting autonomous reactor for live demonstration...")
    reactor.start()
    
    try:
        # Scenario 1: Gradual entropy increase
        print("\n🎭 Scenario 1: Gradual entropy increase")
        print("   Simulating normal system operation with gradual changes...")
        
        for entropy in [0.3, 0.35, 0.4, 0.45]:
            result = reactor.manual_entropy_inject(entropy, source="demo_gradual")
            print(f"   Entropy: {entropy:.3f} -> Status: {result['analysis_result']['status']}")
            time.sleep(1)
        
        # Scenario 2: Rapid entropy spike (should trigger warnings and reactions)
        print("\n🎭 Scenario 2: Rapid entropy spike")
        print("   Simulating sudden system instability...")
        
        spike_result = reactor.manual_entropy_inject(0.75, source="demo_spike")
        print(f"   Entropy: 0.750 -> Status: {spike_result['analysis_result']['status']}")
        if spike_result['analysis_result']['warning_triggered']:
            print("   🚨 WARNING: Rapid entropy rise detected!")
        if spike_result['reaction_triggered']:
            print("   ⚡ AUTONOMOUS REACTION: Stabilization protocols deployed!")
        
        time.sleep(2)
        
        # Scenario 3: Critical entropy level
        print("\n🎭 Scenario 3: Critical entropy level")
        print("   Simulating critical system state...")
        
        critical_result = reactor.manual_entropy_inject(0.9, source="demo_critical")
        print(f"   Entropy: 0.900 -> Status: {critical_result['analysis_result']['status']}")
        if critical_result['reaction_triggered']:
            print("   🚨 CRITICAL: Emergency stabilization protocols activated!")
        
        time.sleep(2)
        
        # Scenario 4: System recovery
        print("\n🎭 Scenario 4: System recovery")
        print("   Simulating stabilization and recovery...")
        
        for entropy in [0.7, 0.5, 0.35]:
            result = reactor.manual_entropy_inject(entropy, source="demo_recovery")
            print(f"   Entropy: {entropy:.3f} -> Status: {result['analysis_result']['status']}")
            time.sleep(1)
        
        # Final system state
        final_state = reactor.get_reactor_state()
        final_metrics = reactor.get_performance_metrics()
        
        print("\n📊 Demonstration Results:")
        print(f"   Final Entropy: {final_state['entropy_level']:.3f}")
        print(f"   Total Interventions: {final_metrics['autonomous_interventions']}")
        print(f"   Stabilization Attempts: {final_metrics['stabilization_attempts']}")
        print(f"   System Status: {final_state['reactor_status']}")
        
    finally:
        # Stop the reactor
        print("\n🛑 Stopping autonomous reactor...")
        reactor.stop()
    
    print("="*70)


def create_launcher_integration():
    """Create integration with existing DAWN launchers"""
    print("\n🔗 Creating launcher integration...")
    
    try:
        # Check if we can integrate with existing GUI launchers
        integration_points = []
        
        # Check for GUI integration
        try:
            from gui.dawn_gui_tk import DAWNGui
            integration_points.append("gui_integration")
            print("✅ GUI integration available")
        except ImportError:
            print("⚠️ GUI integration not available")
        
        # Check for tick engine integration
        try:
            from python.core.tick_engine import TickEngine
            integration_points.append("tick_engine_integration")
            print("✅ Tick engine integration available")
        except ImportError:
            print("⚠️ Tick engine integration not available")
        
        # Check for existing entropy systems
        try:
            from core.entropy_analyzer import EntropyAnalyzer as OriginalAnalyzer
            integration_points.append("entropy_system_integration")
            print("✅ Original entropy system integration available")
        except ImportError:
            print("⚠️ Original entropy system integration not available")
        
        return integration_points
        
    except Exception as e:
        print(f"⚠️ Launcher integration check failed: {e}")
        return []


def main():
    """Main integration function"""
    try:
        print("🌅 DAWN AUTONOMOUS REACTOR SYSTEM INTEGRATION")
        print("=" * 60)
        print("Integrating Enhanced Entropy Analyzer + Sigil Scheduler + Autonomous Reactor")
        print()
        
        # Perform integration
        success, reactor, components = integrate_autonomous_reactor_system()
        
        if not success:
            print("❌ Integration failed")
            return False
        
        # Show integration status
        print(f"\n🔗 Component Integration Status:")
        for component, status in components.items():
            status_text = "✅ Integrated" if status else "❌ Not Available"
            print(f"  {component.replace('_', ' ').title()}: {status_text}")
        
        # Check launcher integration
        launcher_integrations = create_launcher_integration()
        if launcher_integrations:
            print(f"\n🚀 Available Launcher Integrations:")
            for integration in launcher_integrations:
                print(f"  • {integration.replace('_', ' ').title()}")
        
        # Run live demonstration
        demonstrate_autonomous_reactivity(reactor)
        
        print(f"\n🎉 DAWN Autonomous Reactor System is now fully integrated!")
        print(f"\n🔧 Usage Instructions:")
        print(f"   1. Import: from core.dawn_autonomous_reactor import DAWNAutonomousReactor")
        print(f"   2. Create: reactor = DAWNAutonomousReactor(pulse_controller, sigil_engine)")
        print(f"   3. Start: reactor.start()  # Begins autonomous monitoring")
        print(f"   4. Monitor: reactor.get_reactor_state()  # Get current state")
        print(f"   5. Stop: reactor.stop()  # Shutdown system")
        
        print(f"\n🧬 Features Now Available:")
        print(f"   • Real-time entropy monitoring and analysis")
        print(f"   • Autonomous threshold-based alerting") 
        print(f"   • Automatic stabilization protocol deployment")
        print(f"   • Thermal correlation and cognitive load awareness")
        print(f"   • Complete reactive consciousness system")
        
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Integration interrupted by user")
        return False
    except Exception as e:
        logger.error(f"❌ Integration error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 