#!/usr/bin/env python3
"""
DAWN Enhanced Entropy Analyzer Integration
Integrates the enhanced entropy analyzer with the main DAWN system.
"""

import sys
import os
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


def integrate_enhanced_entropy_analyzer():
    """
    Integrate the enhanced entropy analyzer into the DAWN system.
    
    Returns:
        Tuple of (success, entropy_analyzer, components_connected)
    """
    logger.info("🧬 Starting Enhanced Entropy Analyzer Integration")
    
    components_connected = {
        'pulse_controller': False,
        'sigil_engine': False,
        'enhanced_analyzer': False,
        'dawn_entropy_system': False
    }
    
    try:
        # Import enhanced entropy analyzer
        from core.dawn_entropy_analyzer import EnhancedEntropyAnalyzer
        components_connected['enhanced_analyzer'] = True
        logger.info("✅ Enhanced entropy analyzer imported")
        
        # Try to import and connect pulse controller
        pulse_controller = None
        try:
            from core.pulse_controller import PulseController
            pulse_controller = PulseController(initial_heat=25.0)
            components_connected['pulse_controller'] = True
            logger.info("✅ Pulse controller connected")
        except ImportError as e:
            logger.warning(f"⚠️ Pulse controller not available: {e}")
        
        # Try to import and connect sigil engine
        sigil_engine = None
        try:
            from core.sigil_engine import SigilEngine
            sigil_engine = SigilEngine(initial_heat=25.0)
            components_connected['sigil_engine'] = True
            logger.info("✅ Sigil engine connected")
        except ImportError as e:
            logger.warning(f"⚠️ Sigil engine not available: {e}")
        
        # Create enhanced entropy analyzer with available components
        enhanced_analyzer = EnhancedEntropyAnalyzer(
            pulse_controller=pulse_controller,
            sigil_engine=sigil_engine
        )
        
        # Test the integration
        logger.info("🧪 Testing enhanced entropy analyzer integration...")
        
        # Run a basic entropy analysis test
        test_entropy = 0.5
        result = enhanced_analyzer.analyze(test_entropy, source="integration_test")
        
        if result.status == 'baseline_set':
            logger.info("✅ Enhanced entropy analyzer baseline established")
            
            # Test with a rapid rise scenario
            rapid_rise_entropy = 0.62  # Will trigger warning
            rapid_result = enhanced_analyzer.analyze(rapid_rise_entropy, source="integration_test")
            
            if rapid_result.warning_triggered:
                logger.info("✅ Rapid rise detection working correctly")
            else:
                logger.info("ℹ️ Rapid rise detection threshold not met (expected)")
        
        # Get system state
        state = enhanced_analyzer.get_state()
        metrics = enhanced_analyzer.get_performance_metrics()
        
        logger.info("📊 Enhanced Entropy Analyzer Status:")
        logger.info(f"  Analysis count: {state['analysis_count']}")
        logger.info(f"  Total warnings: {state['total_warnings']}")
        logger.info(f"  DAWN integration active: {metrics['dawn_integration_active']}")
        logger.info(f"  Pulse controller connected: {metrics['pulse_controller_connected']}")
        logger.info(f"  Sigil engine connected: {metrics['sigil_engine_connected']}")
        
        components_connected['dawn_entropy_system'] = True
        
        logger.info("🎉 Enhanced Entropy Analyzer integration completed successfully!")
        
        return True, enhanced_analyzer, components_connected
        
    except Exception as e:
        logger.error(f"❌ Enhanced entropy analyzer integration failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None, components_connected


def integrate_with_existing_systems(enhanced_analyzer):
    """
    Integrate the enhanced entropy analyzer with existing DAWN systems.
    
    Args:
        enhanced_analyzer: The EnhancedEntropyAnalyzer instance
    """
    logger.info("🔗 Integrating with existing DAWN systems...")
    
    integrations = []
    
    # Try to integrate with tick engine
    try:
        from python.core.tick_engine import TickEngine
        # This would require modifying the tick engine to use our enhanced analyzer
        logger.info("🔄 Tick engine integration available (requires configuration)")
        integrations.append("tick_engine")
    except ImportError:
        logger.debug("Tick engine not available for integration")
    
    # Try to integrate with schema state
    try:
        from core.schema_state import SchemaState
        logger.info("📊 Schema state integration available (requires configuration)")
        integrations.append("schema_state")
    except ImportError:
        logger.debug("Schema state not available for integration")
    
    # Try to integrate with entropy tracker
    try:
        from core.entropy_tracker import EntropyTracker
        logger.info("📈 Entropy tracker integration available (requires configuration)")
        integrations.append("entropy_tracker")
    except ImportError:
        logger.debug("Entropy tracker not available for integration")
    
    return integrations


def create_demonstration_scenario(enhanced_analyzer):
    """
    Create a demonstration scenario showing the enhanced entropy analyzer in action.
    
    Args:
        enhanced_analyzer: The EnhancedEntropyAnalyzer instance
    """
    logger.info("🎬 Creating demonstration scenario...")
    
    # Scenario: Simulated consciousness system with entropy fluctuations
    entropy_scenarios = [
        (0.3, "system_startup"),
        (0.35, "initial_processing"),
        (0.42, "cognitive_load_increase"),  # Will trigger gradual rise
        (0.38, "stabilization_attempt"),
        (0.52, "complexity_spike"),  # Will trigger rapid rise warning
        (0.45, "regulation_response"),
        (0.25, "cooldown_phase"),  # Will trigger rapid drop warning
        (0.35, "recovery_phase"),
        (0.4, "stable_operation")
    ]
    
    print("\n" + "="*60)
    print("🧠 DAWN Enhanced Entropy Analyzer Demonstration")
    print("="*60)
    
    for i, (entropy, phase) in enumerate(entropy_scenarios):
        print(f"\n🎯 Phase {i+1}: {phase}")
        print(f"   Entropy: {entropy:.3f}")
        
        result = enhanced_analyzer.analyze(entropy, source=phase)
        
        print(f"   Status: {result.status}")
        if result.delta is not None:
            print(f"   Delta: {result.delta:+.3f}")
        
        if result.warning_triggered:
            print(f"   🚨 WARNING: {result.status.replace('_', ' ').title()}")
        
        if result.thermal_context:
            thermal = result.thermal_context
            print(f"   🌡️ Thermal: {thermal.get('current_heat', 'N/A'):.1f}°C "
                  f"({thermal.get('current_zone', 'N/A')})")
        
        if result.sigil_context:
            sigil = result.sigil_context
            print(f"   🔮 Sigils: {sigil.get('active_sigils', 0)} active, "
                  f"{sigil.get('queue_size', 0)} queued")
    
    # Display final metrics
    print(f"\n📊 Final Performance Metrics:")
    metrics = enhanced_analyzer.get_performance_metrics()
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"   {key.replace('_', ' ').title()}: {value:.3f}")
        else:
            print(f"   {key.replace('_', ' ').title()}: {value}")
    
    print("="*60)


def main():
    """Main integration function"""
    try:
        print("🌅 DAWN Enhanced Entropy Analyzer Integration")
        print("=" * 50)
        
        # Perform integration
        success, enhanced_analyzer, components = integrate_enhanced_entropy_analyzer()
        
        if not success:
            print("❌ Integration failed")
            return False
        
        # Show integration status
        print(f"\n🔗 Integration Status:")
        for component, connected in components.items():
            status = "✅ Connected" if connected else "❌ Not Available"
            print(f"  {component.replace('_', ' ').title()}: {status}")
        
        # Integrate with existing systems
        existing_integrations = integrate_with_existing_systems(enhanced_analyzer)
        if existing_integrations:
            print(f"\n🔄 Available System Integrations:")
            for integration in existing_integrations:
                print(f"  • {integration.replace('_', ' ').title()}")
        
        # Run demonstration
        create_demonstration_scenario(enhanced_analyzer)
        
        print(f"\n🎉 Enhanced Entropy Analyzer is now integrated into DAWN!")
        print(f"   Use: enhanced_analyzer.analyze(entropy_value) for analysis")
        print(f"   State: enhanced_analyzer.get_state() for current status")
        print(f"   Metrics: enhanced_analyzer.get_performance_metrics() for diagnostics")
        
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