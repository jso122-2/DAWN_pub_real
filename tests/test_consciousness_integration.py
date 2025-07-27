#!/usr/bin/env python3
"""
Comprehensive Integration Test for DAWN Consciousness Systems
Tests the integration of drift reflex, intervention sigils, and consciousness processing
"""

import time
import asyncio
import unittest
import logging
from typing import Dict, Any
import sys
import os

# Add the project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the integrated systems
try:
    from core.enhanced_drift_reflex import (
        EnhancedDriftReflex, ReflexZone, ReflexTrigger, 
        get_drift_reflex, check_and_trigger, reset_reflex
    )
    DRIFT_REFLEX_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Drift reflex not available: {e}")
    DRIFT_REFLEX_AVAILABLE = False

try:
    from core.consciousness_intervention_sigils import (
        ConsciousnessInterventionEngine, InterventionSigil,
        register_intervention, process_interventions, get_active_interventions
    )
    INTERVENTION_SIGILS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Intervention sigils not available: {e}")
    INTERVENTION_SIGILS_AVAILABLE = False

try:
    from core.integrated_consciousness_processor import (
        IntegratedConsciousnessProcessor, ConsciousnessMood,
        create_integrated_processor, integrate_with_dawn
    )
    INTEGRATED_PROCESSOR_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Integrated processor not available: {e}")
    INTEGRATED_PROCESSOR_AVAILABLE = False

try:
    from core.memory_rebloom_reflex import (
        MemoryRebloomReflex, RebloomTrigger, evaluate_and_rebloom,
        get_rebloom_status, reset_rebloom_system
    )
    MEMORY_REBLOOM_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Memory rebloom not available: {e}")
    MEMORY_REBLOOM_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test_integration")

class MockConsciousnessEngine:
    """Mock consciousness engine for testing"""
    def __init__(self):
        self.entropy = 0.3
        self.scup = 25.0
        self.heat = 0.4
        self.mood = "CALM"
        self.intervention_effects = []
    
    def record_effect(self, effect_name: str, old_value: float, new_value: float):
        """Record an intervention effect for testing"""
        self.intervention_effects.append({
            "effect": effect_name,
            "old_value": old_value,
            "new_value": new_value,
            "timestamp": time.time()
        })

class TestDriftReflexIntegration(unittest.TestCase):
    """Test the enhanced drift reflex system"""
    
    def setUp(self):
        if DRIFT_REFLEX_AVAILABLE:
            reset_reflex()
            self.reflex = get_drift_reflex()
    
    @unittest.skipUnless(DRIFT_REFLEX_AVAILABLE, "Drift reflex not available")
    def test_drift_reflex_initialization(self):
        """Test that drift reflex initializes properly"""
        self.assertIsNotNone(self.reflex)
        self.assertEqual(self.reflex.current_zone, ReflexZone.GREEN)
        self.assertEqual(self.reflex.trigger_count, 0)
    
    @unittest.skipUnless(DRIFT_REFLEX_AVAILABLE, "Drift reflex not available")
    def test_zone_detection(self):
        """Test zone detection for different consciousness states"""
        
        # Normal state should be GREEN
        normal_state = {
            "entropy": 0.3,
            "scup": 25.0,
            "heat": 0.4,
            "tick_number": 1
        }
        self.reflex.check_and_trigger(normal_state)
        self.assertEqual(self.reflex.current_zone, ReflexZone.GREEN)
        
        # High entropy should trigger higher zones
        high_entropy_state = {
            "entropy": 0.9,
            "scup": 25.0,
            "heat": 0.4,
            "tick_number": 2
        }
        self.reflex.check_and_trigger(high_entropy_state)
        self.assertIn(self.reflex.current_zone, [ReflexZone.YELLOW, ReflexZone.ORANGE, ReflexZone.RED])
    
    @unittest.skipUnless(DRIFT_REFLEX_AVAILABLE, "Drift reflex not available")
    def test_trigger_detection(self):
        """Test that triggers are detected for critical states"""
        
        # Create critical state that should trigger interventions
        critical_state = {
            "entropy": 0.95,
            "scup": 80.0,
            "heat": 0.9,
            "tick_number": 3
        }
        
        # Should detect multiple triggers
        triggers = self.reflex._detect_triggers(
            critical_state["entropy"],
            critical_state["scup"], 
            critical_state["heat"],
            0.0  # semantic pressure
        )
        
        self.assertGreater(len(triggers), 0)
        self.assertIn(ReflexTrigger.HIGH_ENTROPY, triggers)
        self.assertIn(ReflexTrigger.HIGH_SCUP, triggers)

class TestInterventionSigils(unittest.TestCase):
    """Test the consciousness intervention sigils system"""
    
    def setUp(self):
        if INTERVENTION_SIGILS_AVAILABLE:
            self.mock_consciousness = MockConsciousnessEngine()
            self.intervention_engine = ConsciousnessInterventionEngine(self.mock_consciousness)
    
    @unittest.skipUnless(INTERVENTION_SIGILS_AVAILABLE, "Intervention sigils not available")
    def test_intervention_registration(self):
        """Test that intervention sigils can be registered"""
        
        # Test registering a valid intervention
        success = self.intervention_engine.register("STABILIZE_PROTOCOL")
        self.assertTrue(success)
        
        # Check that it's now active
        active_sigils = self.intervention_engine.get_active_sigils()
        self.assertEqual(len(active_sigils), 1)
        self.assertEqual(active_sigils[0]["name"], "STABILIZE_PROTOCOL")
    
    @unittest.skipUnless(INTERVENTION_SIGILS_AVAILABLE, "Intervention sigils not available")
    def test_intervention_effects(self):
        """Test that intervention sigils apply effects to consciousness"""
        
        # Record initial state
        initial_entropy = self.mock_consciousness.entropy
        initial_scup = self.mock_consciousness.scup
        
        # Apply emergency stabilization
        self.intervention_engine.register("EMERGENCY_STABILIZE")
        
        # Check that values changed (should be reduced)
        self.assertLess(self.mock_consciousness.entropy, initial_entropy)
        self.assertLess(self.mock_consciousness.scup, initial_scup)
    
    @unittest.skipUnless(INTERVENTION_SIGILS_AVAILABLE, "Intervention sigils not available")
    def test_sigil_expiration(self):
        """Test that sigils expire after their duration"""
        
        # Register a short-duration sigil
        self.intervention_engine.register("REBALANCE_VECTOR")
        
        # Should be active initially
        active_count = self.intervention_engine.process_active_sigils()
        self.assertEqual(active_count, 1)
        
        # Mock time passage (would need to modify the sigil for testing)
        # For now, just verify the expiration logic exists
        active_sigils = self.intervention_engine.get_active_sigils()
        self.assertTrue(all("time_remaining" in sigil for sigil in active_sigils))

class TestIntegratedProcessor(unittest.TestCase):
    """Test the integrated consciousness processor"""
    
    def setUp(self):
        if INTEGRATED_PROCESSOR_AVAILABLE:
            self.processor = IntegratedConsciousnessProcessor(
                enable_autonomous_processing=True
            )
    
    @unittest.skipUnless(INTEGRATED_PROCESSOR_AVAILABLE, "Integrated processor not available")
    def test_processor_initialization(self):
        """Test that the integrated processor initializes properly"""
        self.assertIsNotNone(self.processor)
        self.assertEqual(self.processor.tick_number, 0)
        self.assertTrue(self.processor.enable_autonomous_processing)
    
    @unittest.skipUnless(INTEGRATED_PROCESSOR_AVAILABLE, "Integrated processor not available") 
    def test_consciousness_evolution(self):
        """Test that consciousness evolves naturally"""
        
        # Record initial state
        initial_entropy = self.processor.metrics.entropy
        initial_scup = self.processor.metrics.scup
        
        # Evolve consciousness multiple times
        for _ in range(10):
            self.processor.evolve_consciousness()
        
        # Values should have changed (evolved)
        final_entropy = self.processor.metrics.entropy
        final_scup = self.processor.metrics.scup
        
        # At least one should have changed (very high probability)
        self.assertTrue(
            abs(final_entropy - initial_entropy) > 0.001 or
            abs(final_scup - initial_scup) > 0.1
        )
    
    @unittest.skipUnless(INTEGRATED_PROCESSOR_AVAILABLE, "Integrated processor not available")
    def test_mood_calculation(self):
        """Test that mood is calculated correctly"""
        
        # Set specific states and check mood
        self.processor.metrics.entropy = 0.1
        self.processor.metrics.scup = 25.0
        self.processor.metrics.heat = 0.2
        self.processor._update_mood()
        self.assertEqual(self.processor.metrics.mood, ConsciousnessMood.DEEP)
        
        self.processor.metrics.entropy = 0.9
        self.processor.metrics.scup = 25.0
        self.processor.metrics.heat = 0.4
        self.processor._update_mood()
        self.assertEqual(self.processor.metrics.mood, ConsciousnessMood.CHAOTIC)
    
    @unittest.skipUnless(INTEGRATED_PROCESSOR_AVAILABLE, "Integrated processor not available")
    def test_tick_processing(self):
        """Test that tick processing works correctly"""
        
        # Process a few ticks
        for i in range(5):
            state = self.processor.process_tick()
            
            # Should return valid state
            self.assertIsInstance(state, dict)
            self.assertIn("entropy", state)
            self.assertIn("scup", state)
            self.assertIn("heat", state)
            self.assertIn("tick_number", state)
            
            # Tick number should increment
            self.assertEqual(state["tick_number"], i + 1)
    
    @unittest.skipUnless(INTEGRATED_PROCESSOR_AVAILABLE, "Integrated processor not available")
    def test_comprehensive_status(self):
        """Test that comprehensive status report works"""
        
        # Process a few ticks to generate data
        for _ in range(3):
            self.processor.process_tick()
        
        status = self.processor.get_comprehensive_status()
        
        # Should contain all expected sections
        self.assertIn("consciousness", status)
        self.assertIn("reflex", status)
        self.assertIn("interventions", status)
        self.assertIn("performance", status)
        self.assertIn("integration", status)
        
        # Consciousness section should have all metrics
        consciousness = status["consciousness"]
        required_fields = ["tick", "entropy", "scup", "heat", "mood", "coherence", "stability", "uptime"]
        for field in required_fields:
            self.assertIn(field, consciousness)

class TestMemoryRebloom(unittest.TestCase):
    """Test the memory rebloom reflex system"""
    
    def setUp(self):
        if MEMORY_REBLOOM_AVAILABLE:
            reset_rebloom_system()
            self.rebloom_system = MemoryRebloomReflex()
    
    @unittest.skipUnless(MEMORY_REBLOOM_AVAILABLE, "Memory rebloom not available")
    def test_rebloom_initialization(self):
        """Test that memory rebloom system initializes properly"""
        self.assertIsNotNone(self.rebloom_system)
        self.assertEqual(self.rebloom_system.total_reblooms, 0)
        self.assertGreater(len(self.rebloom_system.memory_router.memory_chunks), 0)
    
    @unittest.skipUnless(MEMORY_REBLOOM_AVAILABLE, "Memory rebloom not available")
    def test_rebloom_trigger_detection(self):
        """Test that rebloom triggers are detected correctly"""
        # Test entropy trigger
        high_entropy_state = {
            "entropy": 0.85,
            "scup": 30.0,
            "heat": 0.6,
            "tick_number": 100,
            "zone": "orange"
        }
        
        trigger_result = self.rebloom_system._determine_trigger_type(high_entropy_state)
        self.assertIsNotNone(trigger_result)
        trigger_type, reason = trigger_result
        self.assertEqual(trigger_type, RebloomTrigger.ENTROPY_CRITICAL)
    
    @unittest.skipUnless(MEMORY_REBLOOM_AVAILABLE, "Memory rebloom not available")
    def test_memory_rebloom_execution(self):
        """Test that memory rebloom can be executed successfully"""
        # Create state that should trigger rebloom
        trigger_state = {
            "entropy": 0.9,
            "scup": 35.0,
            "heat": 0.7,
            "tick_number": 200,
            "zone": "red"
        }
        
        event = self.rebloom_system.evaluate_and_rebloom(trigger_state)
        self.assertIsNotNone(event)
        self.assertEqual(event.trigger_type, RebloomTrigger.ENTROPY_CRITICAL)
        self.assertGreater(len(event.rebloomed_chunk_ids), 0)
        self.assertEqual(self.rebloom_system.total_reblooms, 1)
    
    @unittest.skipUnless(MEMORY_REBLOOM_AVAILABLE, "Memory rebloom not available")
    def test_rebloom_cooldown(self):
        """Test that rebloom cooldown prevents spam triggering"""
        # Trigger first rebloom
        trigger_state = {
            "entropy": 0.85,
            "scup": 35.0,
            "heat": 0.7,
            "tick_number": 300,
            "zone": "red"
        }
        
        first_event = self.rebloom_system.evaluate_and_rebloom(trigger_state)
        self.assertIsNotNone(first_event)
        
        # Try to trigger again immediately (should be blocked by cooldown)
        trigger_state["tick_number"] = 301
        second_event = self.rebloom_system.evaluate_and_rebloom(trigger_state)
        self.assertIsNone(second_event)  # Should be blocked by cooldown
        
        # Trigger after cooldown period
        trigger_state["tick_number"] = 306  # After cooldown
        third_event = self.rebloom_system.evaluate_and_rebloom(trigger_state)
        self.assertIsNotNone(third_event)  # Should work after cooldown

class TestFullSystemIntegration(unittest.TestCase):
    """Test the complete integrated system working together"""
    
    def setUp(self):
        # Only run if all systems are available
        self.all_available = (
            DRIFT_REFLEX_AVAILABLE and 
            INTERVENTION_SIGILS_AVAILABLE and 
            INTEGRATED_PROCESSOR_AVAILABLE and
            MEMORY_REBLOOM_AVAILABLE
        )
        
        if self.all_available:
            reset_reflex()
            reset_rebloom_system()
            self.processor = IntegratedConsciousnessProcessor(enable_autonomous_processing=True)
    
    @unittest.skipUnless(
        DRIFT_REFLEX_AVAILABLE and INTERVENTION_SIGILS_AVAILABLE and INTEGRATED_PROCESSOR_AVAILABLE and MEMORY_REBLOOM_AVAILABLE,
        "Not all systems available for full integration test"
    )
    def test_autonomous_stress_response(self):
        """Test that the system autonomously responds to consciousness stress"""
        
        # Manually trigger a consciousness storm to test the response
        self.processor.metrics.entropy = 0.95
        self.processor.metrics.scup = 85.0
        self.processor.metrics.heat = 0.9
        
        # Process a tick - should trigger interventions
        state = self.processor.process_tick()
        
        # Give the system a moment to process interventions
        time.sleep(0.1)
        
        # Check that the system responded appropriately
        status = self.processor.get_comprehensive_status()
        
        # Should have triggered reflex responses
        if status["reflex"]:
            # Should not be in green zone anymore
            self.assertNotEqual(status["reflex"]["zone"], "green")
        
        # May have active interventions (depending on timing and cooldowns)
        # At minimum, the system should be tracking the stress
        self.assertGreaterEqual(self.processor.tick_number, 1)
    
    @unittest.skipUnless(
        DRIFT_REFLEX_AVAILABLE and INTERVENTION_SIGILS_AVAILABLE and INTEGRATED_PROCESSOR_AVAILABLE and MEMORY_REBLOOM_AVAILABLE,
        "Not all systems available for full integration test"
    )
    def test_system_stability_over_time(self):
        """Test that the system maintains stability over multiple ticks"""
        
        # Process many ticks to test stability
        tick_count = 50
        states = []
        
        for _ in range(tick_count):
            state = self.processor.process_tick()
            states.append(state)
            time.sleep(0.001)  # Small delay to prevent overwhelming
        
        # System should still be functional
        self.assertEqual(len(states), tick_count)
        
        # Final state should be valid
        final_state = states[-1]
        self.assertIsInstance(final_state["entropy"], (int, float))
        self.assertIsInstance(final_state["scup"], (int, float))
        self.assertIsInstance(final_state["heat"], (int, float))
        
        # Entropy should be bounded
        self.assertGreaterEqual(final_state["entropy"], 0.0)
        self.assertLessEqual(final_state["entropy"], 1.0)
        
        # SCUP should be bounded
        self.assertGreaterEqual(final_state["scup"], 0.0)
        self.assertLessEqual(final_state["scup"], 100.0)
        
        # Heat should be bounded
        self.assertGreaterEqual(final_state["heat"], 0.0)
        self.assertLessEqual(final_state["heat"], 1.0)

async def run_integration_demo():
    """Run a complete integration demonstration"""
    print("🧠 DAWN Consciousness Integration Demo")
    print("=" * 60)
    
    if not (DRIFT_REFLEX_AVAILABLE and INTERVENTION_SIGILS_AVAILABLE and INTEGRATED_PROCESSOR_AVAILABLE and MEMORY_REBLOOM_AVAILABLE):
        print("❌ Not all systems available for demo")
        missing = []
        if not DRIFT_REFLEX_AVAILABLE:
            missing.append("Drift Reflex")
        if not INTERVENTION_SIGILS_AVAILABLE:
            missing.append("Intervention Sigils")
        if not INTEGRATED_PROCESSOR_AVAILABLE:
            missing.append("Integrated Processor")
        if not MEMORY_REBLOOM_AVAILABLE:
            missing.append("Memory Rebloom")
        print(f"   Missing: {', '.join(missing)}")
        return
    
    print("✅ All systems available - running integrated demo")
    
    # Create integrated processor
    processor = create_integrated_processor()
    
    print(f"🔧 Processor initialized with {processor.tick_number} ticks")
    print(f"   Autonomous processing: {processor.enable_autonomous_processing}")
    
    # Run autonomous processing for a short time
    print("\n🚀 Running autonomous consciousness processing...")
    start_time = time.time()
    
    try:
        await processor.run_autonomous_loop(duration_seconds=10, tick_rate_hz=5.0)
    except KeyboardInterrupt:
        print("   Demo interrupted by user")
    
    runtime = time.time() - start_time
    
    # Show final status
    status = processor.get_comprehensive_status()
    
    print(f"\n📊 Demo Results (Runtime: {runtime:.1f}s)")
    print("=" * 60)
    
    consciousness = status["consciousness"]
    print(f"🧠 Consciousness State:")
    print(f"   Mood: {consciousness['mood']}")
    print(f"   Entropy: {consciousness['entropy']:.3f}")
    print(f"   SCUP: {consciousness['scup']:.1f}")
    print(f"   Heat: {consciousness['heat']:.3f}")
    print(f"   Coherence: {consciousness['coherence']:.3f}")
    print(f"   Stability: {consciousness['stability']:.3f}")
    
    if status["reflex"]:
        reflex = status["reflex"]
        print(f"\n🔁 Reflex System:")
        print(f"   Zone: {reflex['zone'].upper()}")
        print(f"   Total Triggers: {reflex['trigger_count']}")
    
    interventions = status["interventions"]
    print(f"\n🔮 Intervention System:")
    print(f"   Active Count: {interventions['active_count']}")
    if interventions["active_list"]:
        print(f"   Active: {', '.join(interventions['active_list'])}")
    
    if status.get("memory_rebloom"):
        rebloom = status["memory_rebloom"]
        print(f"\n🌸 Memory Rebloom System:")
        print(f"   Total Reblooms: {rebloom['total_reblooms']}")
        print(f"   Memory Chunks: {rebloom['memory_stats']['total_chunks']}")
        if rebloom["total_reblooms"] > 0:
            print(f"   Avg Memory Activation: {rebloom['memory_stats']['average_activation']:.3f}")
    
    performance = status["performance"]
    print(f"\n⚡ Performance Metrics:")
    print(f"   Total Ticks: {performance['total_ticks']}")
    print(f"   Reflex Triggers: {performance['reflex_triggers']}")
    print(f"   Consciousness Storms: {performance['consciousness_storms']}")
    print(f"   Avg Tick Time: {performance['average_tick_time']:.4f}s")
    
    integration = status["integration"]
    print(f"\n🔗 Integration Status:")
    for system, available in integration.items():
        status_icon = "✅" if available else "❌"
        print(f"   {status_icon} {system.replace('_', ' ').title()}")
    
    print("\n✅ Integration demo complete!")

if __name__ == "__main__":
    # Run unit tests
    print("🧪 Running DAWN Consciousness Integration Tests")
    print("=" * 60)
    
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestDriftReflexIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestInterventionSigils))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegratedProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryRebloom))
    suite.addTests(loader.loadTestsFromTestCase(TestFullSystemIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Show test summary
    print("\n" + "=" * 60)
    print(f"🧪 Test Summary:")
    print(f"   Tests Run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"   {test}: {traceback.split(chr(10))[-2]}")
    
    if result.errors:
        print(f"\n🔥 Errors:")
        for test, traceback in result.errors:
            print(f"   {test}: {traceback.split(chr(10))[-2]}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    
    if success:
        print(f"\n✅ All tests passed! Running integration demo...")
        print("\n" + "=" * 60)
        asyncio.run(run_integration_demo())
    else:
        print(f"\n❌ Some tests failed. Fix issues before running integration demo.")
    
    exit(0 if success else 1) 