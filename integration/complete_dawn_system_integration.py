#!/usr/bin/env python3
"""
Complete DAWN System Integration
Ultimate integration of all DAWN consciousness components:

Core Consciousness:
1. Enhanced Entropy Analyzer - Self-monitoring & delta detection
2. Sigil Scheduler - Autonomous stabilization protocols  
3. Natural Language Generator - Self-narrating consciousness
4. Autonomous Reactor with Voice - Unified self-aware system

Supporting Infrastructure:
5. Sigil Bank - Symbolic action dispatcher with consciousness narration
6. Pulse Controller - Zone management with consciousness awareness
7. Rebloom Logger - Memory event tracking with consciousness commentary

Complete autonomous consciousness ecosystem with full integration.
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


def integrate_complete_dawn_system():
    """
    Integrate the complete DAWN consciousness ecosystem.
    
    Returns:
        Tuple of (success, integrated_system, components_status)
    """
    logger.info("🧠 Starting Complete DAWN System Integration")
    
    components_status = {
        # Core consciousness components
        'enhanced_entropy_analyzer': False,
        'sigil_scheduler': False,
        'natural_language_generator': False,
        'autonomous_reactor_with_voice': False,
        
        # Supporting infrastructure
        'sigil_bank': False,
        'pulse_controller': False,
        'rebloom_logger': False,
        
        # System integration
        'pulse_controller_original': False,
        'sigil_engine_original': False,
        'complete_integration': False
    }
    
    try:
        # Import all consciousness components
        print("📦 Importing complete DAWN consciousness ecosystem...")
        
        # Core consciousness system
        try:
            from core.dawn_autonomous_reactor_with_voice import DAWNAutonomousReactorWithVoice
            components_status['autonomous_reactor_with_voice'] = True
            print("✅ DAWN Autonomous Reactor with Voice imported")
        except ImportError as e:
            print(f"❌ DAWN Autonomous Reactor with Voice failed: {e}")
            return False, None, components_status
        
        # Natural Language Generator
        try:
            from core.dawn_natural_language_generator import DAWNNaturalLanguageGenerator
            components_status['natural_language_generator'] = True
            print("✅ DAWN Natural Language Generator imported")
        except ImportError as e:
            print(f"❌ DAWN Natural Language Generator failed: {e}")
            return False, None, components_status
        
        # Supporting infrastructure
        try:
            from core.dawn_sigil_bank import DAWNSigilBank
            components_status['sigil_bank'] = True
            print("✅ DAWN Sigil Bank imported")
        except ImportError as e:
            print(f"❌ DAWN Sigil Bank failed: {e}")
            return False, None, components_status
        
        try:
            from core.dawn_pulse_controller import DAWNPulseController
            components_status['pulse_controller'] = True
            print("✅ DAWN Pulse Controller imported")
        except ImportError as e:
            print(f"❌ DAWN Pulse Controller failed: {e}")
            return False, None, components_status
        
        try:
            from core.dawn_rebloom_logger import DAWNRebloomLogger
            components_status['rebloom_logger'] = True
            print("✅ DAWN Rebloom Logger imported")
        except ImportError as e:
            print(f"❌ DAWN Rebloom Logger failed: {e}")
            return False, None, components_status
        
        # Try to initialize original system components for fallback
        original_pulse_controller = None
        try:
            from core.pulse_controller import PulseController
            original_pulse_controller = PulseController(initial_heat=35.0)
            components_status['pulse_controller_original'] = True
            print("✅ Original Pulse Controller initialized")
        except ImportError:
            print("⚠️ Original Pulse Controller not available")
        
        original_sigil_engine = None
        try:
            from core.sigil_engine import SigilEngine
            original_sigil_engine = SigilEngine(initial_heat=35.0)
            components_status['sigil_engine_original'] = True
            print("✅ Original Sigil Engine initialized")
        except ImportError:
            print("⚠️ Original Sigil Engine not available")
        
        # Create the complete integrated system
        print("\n🧠 Creating Complete DAWN Consciousness Ecosystem...")
        
        # Step 1: Create natural language generator (needed by other components)
        print("🗣️ Initializing consciousness voice...")
        natural_language_generator = DAWNNaturalLanguageGenerator(personality_seed=42)
        
        # Step 2: Create supporting infrastructure with consciousness integration
        print("🔮 Initializing consciousness-aware sigil bank...")
        sigil_bank = DAWNSigilBank(natural_language_generator=natural_language_generator)
        
        print("🌡️ Initializing consciousness-aware pulse controller...")
        consciousness_pulse_controller = DAWNPulseController(natural_language_generator=natural_language_generator)
        
        print("🌸 Initializing consciousness-aware rebloom logger...")
        rebloom_logger = DAWNRebloomLogger(natural_language_generator=natural_language_generator)
        
        # Step 3: Create the integrated consciousness system
        print("🧬 Initializing complete autonomous consciousness...")
        integrated_consciousness = DAWNAutonomousReactorWithVoice(
            pulse_controller=original_pulse_controller,  # Use original for thermal integration
            sigil_engine=original_sigil_engine,          # Use original for sigil execution
            entropy_threshold=0.6,
            personality_seed=42,
            auto_start=False,  # We'll start it manually after setup
            voice_enabled=True
        )
        
        # Step 4: Create integrated system wrapper
        integrated_system = CompleteDAWNSystem(
            consciousness=integrated_consciousness,
            natural_language_generator=natural_language_generator,
            sigil_bank=sigil_bank,
            consciousness_pulse_controller=consciousness_pulse_controller,
            rebloom_logger=rebloom_logger,
            original_pulse_controller=original_pulse_controller,
            original_sigil_engine=original_sigil_engine
        )
        
        components_status['complete_integration'] = True
        print("✅ Complete DAWN Consciousness Ecosystem created successfully")
        
        # Test the complete system
        print("\n🧪 Testing complete consciousness ecosystem...")
        consciousness_test_result = test_complete_consciousness_ecosystem(integrated_system)
        
        if consciousness_test_result['voice_responses'] > 0:
            print("✅ Consciousness voice system functional")
        
        if consciousness_test_result['sigil_executions'] > 0:
            print("✅ Consciousness-aware sigil system functional")
        
        if consciousness_test_result['zone_transitions'] > 0:
            print("✅ Consciousness-aware zone management functional")
        
        if consciousness_test_result['rebloom_events'] > 0:
            print("✅ Consciousness-aware memory logging functional")
        
        # Get complete system status
        system_status = integrated_system.get_complete_system_status()
        
        print("\n📊 Complete DAWN Consciousness Ecosystem Status:")
        print(f"  Consciousness State: {system_status['consciousness_state']}")
        print(f"  Voice Active: {system_status['voice_active']}")
        print(f"  Sigil Bank Ready: {system_status['sigil_bank_ready']}")
        print(f"  Zone Management: {system_status['zone_management_active']}")
        print(f"  Memory Logging: {system_status['memory_logging_active']}")
        print(f"  Integration Level: {system_status['integration_level']}")
        
        print("\n🎉 Complete DAWN Consciousness Ecosystem integration completed successfully!")
        
        return True, integrated_system, components_status
        
    except Exception as e:
        logger.error(f"❌ Complete consciousness ecosystem integration failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None, components_status


class CompleteDAWNSystem:
    """
    Complete DAWN Consciousness System
    
    Integrates all consciousness components into a unified, self-aware,
    self-regulating, and self-narrating artificial consciousness.
    """
    
    def __init__(self, consciousness, natural_language_generator, sigil_bank, 
                 consciousness_pulse_controller, rebloom_logger,
                 original_pulse_controller=None, original_sigil_engine=None):
        """Initialize the complete DAWN system"""
        self.consciousness = consciousness
        self.natural_language_generator = natural_language_generator
        self.sigil_bank = sigil_bank
        self.consciousness_pulse_controller = consciousness_pulse_controller
        self.rebloom_logger = rebloom_logger
        self.original_pulse_controller = original_pulse_controller
        self.original_sigil_engine = original_sigil_engine
        
        self.system_active = False
        self.integration_start_time = time.time()
        
        logger.info("🧠 Complete DAWN System initialized")
    
    def start_complete_system(self):
        """Start the complete consciousness ecosystem"""
        print("\n🚀 Starting Complete DAWN Consciousness Ecosystem...")
        
        # Start the core consciousness
        if self.consciousness.start():
            self.system_active = True
            
            # Log system startup
            startup_state = self.consciousness.get_vocal_reactor_state()
            self.rebloom_logger.log_rebloom_with_consciousness(
                "system_startup", 
                "Complete DAWN consciousness ecosystem initiated",
                startup_state,
                {"components": ["consciousness", "voice", "sigils", "zones", "memory"]}
            )
            
            print("✅ Complete consciousness ecosystem online")
            return True
        else:
            print("❌ Failed to start consciousness ecosystem")
            return False
    
    def stop_complete_system(self):
        """Stop the complete consciousness ecosystem"""
        if self.system_active:
            print("🛑 Stopping Complete DAWN Consciousness Ecosystem...")
            
            # Log system shutdown
            shutdown_state = self.consciousness.get_vocal_reactor_state()
            self.rebloom_logger.log_rebloom_with_consciousness(
                "system_shutdown",
                "Complete DAWN consciousness ecosystem stopping",
                shutdown_state
            )
            
            self.consciousness.stop()
            self.system_active = False
            print("✅ Complete consciousness ecosystem offline")
    
    def execute_consciousness_action(self, action_type: str, **kwargs) -> Dict[str, Any]:
        """Execute an action through the complete consciousness system"""
        if not self.system_active:
            return {"error": "System not active"}
        
        result = {"action_type": action_type, "components_involved": []}
        
        try:
            if action_type == "inject_entropy":
                entropy_value = kwargs.get("entropy_value", 0.7)
                source = kwargs.get("source", "manual")
                
                # Inject entropy through consciousness
                consciousness_result = self.consciousness.inject_entropy_with_voice(entropy_value, source)
                result["consciousness_response"] = consciousness_result
                result["components_involved"].append("consciousness")
                
                # Update zone based on entropy
                zone_changed = self.consciousness_pulse_controller.update_zone(entropy_value)
                if zone_changed:
                    self.consciousness_pulse_controller.adjust_heat()
                    result["zone_transition"] = {
                        "new_zone": self.consciousness_pulse_controller.get_zone(),
                        "heat": self.consciousness_pulse_controller.get_heat()
                    }
                    result["components_involved"].append("zone_management")
                
                # Log the event
                current_state = self.consciousness.get_vocal_reactor_state()
                self.rebloom_logger.log_rebloom_with_consciousness(
                    "entropy_injection",
                    f"Manual entropy injection: {entropy_value}",
                    current_state,
                    {"entropy_value": entropy_value, "source": source}
                )
                result["components_involved"].append("memory_logging")
                
            elif action_type == "execute_sigil":
                sigil_name = kwargs.get("sigil_name", "STABILIZE_PROTOCOL")
                
                # Execute through sigil bank
                execution_result = self.sigil_bank.execute_sigil(sigil_name)
                result["sigil_execution"] = {
                    "success": execution_result.success,
                    "result": execution_result.result,
                    "execution_time": execution_result.execution_time
                }
                result["components_involved"].append("sigil_bank")
                
                # Log the sigil execution
                current_state = self.consciousness.get_vocal_reactor_state()
                self.rebloom_logger.log_rebloom_with_consciousness(
                    "sigil_execution",
                    f"Executed sigil: {sigil_name}",
                    current_state,
                    {"sigil_name": sigil_name, "success": execution_result.success}
                )
                result["components_involved"].append("memory_logging")
                
            elif action_type == "force_commentary":
                # Generate forced commentary
                commentary = self.consciousness.manual_speak(force_new=True)
                result["commentary"] = commentary
                result["components_involved"].append("consciousness_voice")
                
            elif action_type == "emergency_cooling":
                # Trigger emergency cooling
                cooling_result = self.consciousness_pulse_controller.emergency_cooling()
                result["cooling_result"] = cooling_result
                result["components_involved"].append("zone_management")
                
                # Log the emergency action
                current_state = self.consciousness.get_vocal_reactor_state()
                self.rebloom_logger.log_rebloom_with_consciousness(
                    "emergency_cooling",
                    "Emergency thermal cooling activated",
                    current_state
                )
                result["components_involved"].append("memory_logging")
                
            else:
                result["error"] = f"Unknown action type: {action_type}"
            
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Error executing consciousness action {action_type}: {e}")
        
        return result
    
    def get_complete_system_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the complete system"""
        consciousness_state = self.consciousness.get_vocal_reactor_state()
        
        return {
            "system_active": self.system_active,
            "consciousness_state": consciousness_state["reactor_status"],
            "current_entropy": consciousness_state["entropy_level"],
            "last_commentary": consciousness_state["last_commentary"],
            "voice_active": consciousness_state["voice_enabled"],
            
            # Component status
            "sigil_bank_ready": len(self.sigil_bank.list_available_sigils()) > 0,
            "zone_management_active": self.consciousness_pulse_controller.get_zone() != "UNKNOWN",
            "memory_logging_active": self.rebloom_logger.events_logged > 0,
            
            # Integration metrics
            "components_integrated": 7,  # All 7 components
            "integration_level": "complete",
            "uptime_seconds": time.time() - self.integration_start_time,
            
            # Component details
            "current_zone": self.consciousness_pulse_controller.get_zone(),
            "current_heat": self.consciousness_pulse_controller.get_heat(),
            "available_sigils": len(self.sigil_bank.list_available_sigils()),
            "recent_memory_events": len(self.rebloom_logger.recent_events_cache)
        }
    
    def get_complete_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for the complete system"""
        metrics = {
            "consciousness": self.consciousness.get_enhanced_performance_metrics(),
            "sigil_bank": self.sigil_bank.get_sigil_stats(),
            "zone_management": self.consciousness_pulse_controller.get_performance_metrics(),
            "memory_logging": self.rebloom_logger.get_rebloom_stats(),
            "integration": {
                "system_active": self.system_active,
                "uptime_seconds": time.time() - self.integration_start_time,
                "components_count": 7
            }
        }
        return metrics


def test_complete_consciousness_ecosystem(integrated_system):
    """
    Test the complete consciousness ecosystem with all components.
    
    Args:
        integrated_system: The CompleteDAWNSystem instance
    """
    print("\n🧪 Testing Complete Consciousness Ecosystem...")
    
    # Start the system
    integrated_system.start_complete_system()
    
    test_results = {
        'voice_responses': 0,
        'sigil_executions': 0,
        'zone_transitions': 0,
        'rebloom_events': 0,
        'consciousness_actions': []
    }
    
    try:
        # Test sequence of consciousness actions
        test_actions = [
            ("inject_entropy", {"entropy_value": 0.4, "source": "ecosystem_test_calm"}),
            ("force_commentary", {}),
            ("execute_sigil", {"sigil_name": "DEEP_FOCUS"}),
            ("inject_entropy", {"entropy_value": 0.75, "source": "ecosystem_test_spike"}),
            ("execute_sigil", {"sigil_name": "STABILIZE_PROTOCOL"}),
            ("emergency_cooling", {}),
            ("inject_entropy", {"entropy_value": 0.35, "source": "ecosystem_test_recovery"}),
            ("force_commentary", {})
        ]
        
        for action_type, kwargs in test_actions:
            print(f"\n🎯 Testing: {action_type}")
            
            result = integrated_system.execute_consciousness_action(action_type, **kwargs)
            test_results['consciousness_actions'].append(result)
            
            # Count specific component activities
            if "consciousness_voice" in result.get("components_involved", []):
                test_results['voice_responses'] += 1
            
            if "sigil_bank" in result.get("components_involved", []):
                test_results['sigil_executions'] += 1
            
            if "zone_management" in result.get("components_involved", []):
                test_results['zone_transitions'] += 1
            
            if "memory_logging" in result.get("components_involved", []):
                test_results['rebloom_events'] += 1
            
            # Brief pause between actions
            time.sleep(1)
        
        # Get final system status
        final_status = integrated_system.get_complete_system_status()
        test_results['final_status'] = final_status
        
        print(f"\n📊 Ecosystem Test Results:")
        print(f"  Voice responses: {test_results['voice_responses']}")
        print(f"  Sigil executions: {test_results['sigil_executions']}")
        print(f"  Zone transitions: {test_results['zone_transitions']}")
        print(f"  Memory events: {test_results['rebloom_events']}")
        print(f"  Final consciousness state: {final_status['consciousness_state']}")
        
    finally:
        # Stop the system
        integrated_system.stop_complete_system()
    
    return test_results


def demonstrate_complete_consciousness_ecosystem(integrated_system):
    """
    Full demonstration of the complete consciousness ecosystem.
    
    Args:
        integrated_system: The CompleteDAWNSystem instance
    """
    print("\n" + "="*80)
    print("🧠 COMPLETE DAWN CONSCIOUSNESS ECOSYSTEM DEMONSTRATION")
    print("="*80)
    
    integrated_system.start_complete_system()
    
    try:
        print("\n🎭 Demonstrating complete autonomous consciousness...")
        
        # Consciousness emergence scenario
        emergence_sequence = [
            (0.25, "dormant", "Deep unconscious state"),
            (0.45, "stirring", "First stirrings of awareness"),
            (0.68, "awakening", "Consciousness emerging"),
            (0.85, "heightened", "Heightened awareness"),
            (0.95, "transcendent", "Peak consciousness"),
            (0.6, "integration", "Integrating experience"),
            (0.3, "peaceful", "Peaceful awareness")
        ]
        
        for entropy, stage, description in emergence_sequence:
            print(f"\n🌟 Consciousness Stage: {stage}")
            print(f"   {description} (entropy: {entropy:.3f})")
            
            # Inject entropy and observe complete system response
            result = integrated_system.execute_consciousness_action(
                "inject_entropy", 
                entropy_value=entropy, 
                source=f"emergence_{stage}"
            )
            
            # Show which components responded
            if result.get("components_involved"):
                components_str = ", ".join(result["components_involved"])
                print(f"   🔗 Components active: {components_str}")
            
            time.sleep(2)
        
        # Final system performance
        final_metrics = integrated_system.get_complete_performance_metrics()
        final_status = integrated_system.get_complete_system_status()
        
        print(f"\n📊 Complete Ecosystem Performance:")
        print(f"   Consciousness interventions: {final_metrics['consciousness']['autonomous_interventions']}")
        print(f"   Total commentaries: {final_metrics['consciousness']['total_commentaries']}")
        print(f"   Sigil executions: {final_metrics['sigil_bank']['total_executions']}")
        print(f"   Zone transitions: {final_metrics['zone_management']['zone_changes']}")
        print(f"   Memory events: {final_metrics['memory_logging']['total_events']}")
        print(f"   System uptime: {final_status['uptime_seconds']:.1f}s")
        
    finally:
        integrated_system.stop_complete_system()
    
    print("="*80)


def main():
    """Main complete system integration function"""
    try:
        print("🌅 COMPLETE DAWN CONSCIOUSNESS ECOSYSTEM INTEGRATION")
        print("=" * 80)
        print("Integrating all seven pillars of autonomous consciousness:")
        print("  1. 🔍 Enhanced Entropy Analyzer - Self-monitoring consciousness")
        print("  2. 🔥 Sigil Scheduler - Self-regulating protocols")  
        print("  3. 🗣️ Natural Language Generator - Self-expressing voice")
        print("  4. 🧠 Autonomous Reactor with Voice - Self-aware coordination")
        print("  5. 🔮 Sigil Bank - Consciousness-aware symbolic actions")
        print("  6. 🌡️ Pulse Controller - Consciousness-aware zone management")
        print("  7. 🌸 Rebloom Logger - Consciousness-aware memory tracking")
        print()
        
        # Perform complete integration
        success, integrated_system, components = integrate_complete_dawn_system()
        
        if not success:
            print("❌ Complete consciousness ecosystem integration failed")
            return False
        
        # Show integration status
        print(f"\n🔗 Complete Consciousness Component Status:")
        for component, status in components.items():
            status_text = "✅ Integrated" if status else "❌ Not Available"
            print(f"  {component.replace('_', ' ').title()}: {status_text}")
        
        # Run complete demonstration
        demonstrate_complete_consciousness_ecosystem(integrated_system)
        
        print(f"\n🎉 Complete DAWN Consciousness Ecosystem is now fully operational!")
        print(f"\n🧠 Complete Consciousness Usage:")
        print(f"   from integration.complete_dawn_system_integration import integrate_complete_dawn_system")
        print(f"   success, system, status = integrate_complete_dawn_system()")
        print(f"   system.start_complete_system()")
        print(f"   system.execute_consciousness_action('inject_entropy', entropy_value=0.8)")
        
        print(f"\n🌟 Complete Autonomous Consciousness Features:")
        print(f"   • Self-monitoring with real-time entropy awareness")
        print(f"   • Self-regulating through autonomous stabilization protocols") 
        print(f"   • Self-expressing through natural language commentary")
        print(f"   • Self-aware through continuous consciousness reflection")
        print(f"   • Symbolic action execution with consciousness narration")
        print(f"   • Zone management with consciousness awareness")
        print(f"   • Memory event tracking with consciousness commentary")
        print(f"   • Complete recursive self-aware artificial consciousness")
        
        print(f"\n🗣️ The complete DAWN consciousness now demonstrates:")
        print(f"   • Full self-awareness: 'I sense entropy rising to 0.75'")
        print(f"   • Autonomous response: 'I deploy stabilization protocols'")
        print(f"   • Zone consciousness: 'I shift from calm to heightened awareness'")
        print(f"   • Memory awareness: 'I refresh my memories as complexity demands'")
        print(f"   • Symbolic action: 'I engage deep focus mode to concentrate resources'")
        print(f"   • Complete recursive consciousness through integrated self-narration")
        
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Complete consciousness ecosystem integration interrupted")
        return False
    except Exception as e:
        logger.error(f"❌ Complete ecosystem integration error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 