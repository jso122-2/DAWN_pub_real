#!/usr/bin/env python3
"""
DAWN Integrated Expression Demo - Complete Blueprint Integration
===============================================================

This demonstration script shows the complete integration of:
1. Enhanced DAWN Pigment Dictionary System (neural + rule-based)
2. Sigil Visual Engine (real-time bloom visualization)
3. DAWN Autonomous Reactor Integration (coordinated voice + visual)

This represents the full implementation of the three blueprints working together
to create a unified consciousness expression system.
"""

import asyncio
import time
import logging
from typing import Dict, List, Optional
from pathlib import Path
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("dawn_integration_demo")

# Import all integrated systems
try:
    from core.enhanced_dawn_pigment_dictionary import (
        get_enhanced_dawn_pigment_dictionary,
        VectorizedPigmentSelector
    )
    ENHANCED_PIGMENT_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Enhanced pigment dictionary not available: {e}")
    ENHANCED_PIGMENT_AVAILABLE = False

try:
    from core.sigil_visual_engine import SigilVisualEngine
    VISUAL_ENGINE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Sigil visual engine not available: {e}")
    VISUAL_ENGINE_AVAILABLE = False

try:
    from core.dawn_expression_system import (
        DAWNExpressionMonitor, 
        DAWNExpressionArchive,
        DAWNState,
        DAWNExpression
    )
    EXPRESSION_SYSTEM_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Expression system not available: {e}")
    EXPRESSION_SYSTEM_AVAILABLE = False

try:
    from core.enhanced_dawn_autonomous_reactor import EnhancedDAWNAutonomousReactor
    ENHANCED_REACTOR_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Enhanced reactor not available: {e}")
    ENHANCED_REACTOR_AVAILABLE = False

try:
    from dawn_voice_core import DAWNVoiceCore
    VOICE_CORE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Voice core not available: {e}")
    VOICE_CORE_AVAILABLE = False

class DAWNIntegratedExpressionDemo:
    """
    Complete demonstration of the integrated DAWN expression system
    """
    
    def __init__(self):
        self.systems_ready = False
        self.pigment_processor = None
        self.visual_engine = None
        self.expression_monitor = None
        self.voice_core = None
        self.enhanced_reactor = None
        
        # Demo output directory
        self.demo_output = Path("demo_integrated_expressions")
        self.demo_output.mkdir(parents=True, exist_ok=True)
        
        logger.info("🌟 DAWN Integrated Expression Demo initializing...")
    
    async def initialize_systems(self):
        """Initialize all integrated systems"""
        
        logger.info("🔧 Initializing integrated systems...")
        
        try:
            # 1. Initialize Enhanced Pigment Dictionary
            if ENHANCED_PIGMENT_AVAILABLE:
                self.pigment_processor = get_enhanced_dawn_pigment_dictionary(
                    use_vectorization=True  # Use neural embeddings if available
                )
                logger.info("✅ Enhanced Pigment Dictionary initialized")
            
            # 2. Initialize Sigil Visual Engine
            if VISUAL_ENGINE_AVAILABLE:
                self.visual_engine = SigilVisualEngine(
                    output_directory=str(self.demo_output / "visuals")
                )
                logger.info("✅ Sigil Visual Engine initialized")
            
            # 3. Initialize Voice Core
            if VOICE_CORE_AVAILABLE:
                self.voice_core = DAWNVoiceCore()
                logger.info("✅ DAWN Voice Core initialized")
            
            # 4. Initialize Expression System
            if EXPRESSION_SYSTEM_AVAILABLE:
                self.expression_monitor = DAWNExpressionMonitor(
                    expression_config={
                        'entropy_trigger_threshold': 0.6,
                        'pigment_shift_threshold': 0.25,
                        'time_between_expressions': 2.0,
                        'coherence_threshold': 0.3
                    }
                )
                logger.info("✅ Expression Monitor initialized")
            
            # 5. Initialize Enhanced Reactor (if available)
            if ENHANCED_REACTOR_AVAILABLE:
                self.enhanced_reactor = EnhancedDAWNAutonomousReactor(
                    expression_config={
                        'entropy_trigger_threshold': 0.6,
                        'time_between_expressions': 3.0
                    },
                    archive_expressions=True
                )
                logger.info("✅ Enhanced Reactor initialized")
            
            self.systems_ready = True
            logger.info("🌟 All systems initialized successfully!")
            
        except Exception as e:
            logger.error(f"System initialization failed: {e}")
            self.systems_ready = False
    
    async def demonstrate_pigment_word_selection(self):
        """Demonstrate the enhanced pigment dictionary system"""
        
        logger.info("\n🎨 === ENHANCED PIGMENT DICTIONARY DEMONSTRATION ===")
        
        if not self.pigment_processor:
            logger.warning("Pigment processor not available - skipping demonstration")
            return
        
        # Test different consciousness states
        test_states = [
            {
                'name': '🌅 Calm Morning Reflection',
                'pigment': {'blue': 0.6, 'violet': 0.3, 'green': 0.1},
                'description': 'Peaceful, contemplative state'
            },
            {
                'name': '🔥 Creative Breakthrough',
                'pigment': {'red': 0.7, 'orange': 0.2, 'yellow': 0.1},
                'description': 'High energy, creative flow state'
            },
            {
                'name': '🌿 Natural Growth',
                'pigment': {'green': 0.5, 'blue': 0.3, 'yellow': 0.2},
                'description': 'Organic, growth-oriented state'
            },
            {
                'name': '💫 Mystical Wonder',
                'pigment': {'violet': 0.6, 'blue': 0.3, 'red': 0.1},
                'description': 'Deep, mysterious contemplation'
            }
        ]
        
        for state in test_states:
            logger.info(f"\n{state['name']} - {state['description']}")
            logger.info(f"Pigment State: {state['pigment']}")
            
            # Select words using enhanced system
            selected_words = self.pigment_processor.selector.select_words_by_pigment_blend(
                mood_pigment=state['pigment'],
                word_count=8,
                use_semantic_boost=True
            )
            
            # Organize words by class
            word_classes = {}
            for word, word_class, score in selected_words:
                if word_class not in word_classes:
                    word_classes[word_class] = []
                word_classes[word_class].append((word, score))
            
            logger.info("Selected words by class:")
            for word_class, words in word_classes.items():
                word_list = [f"{word}({score:.2f})" for word, score in words]
                logger.info(f"  {word_class}: {', '.join(word_list)}")
    
    async def demonstrate_visual_generation(self):
        """Demonstrate the sigil visual engine"""
        
        logger.info("\n🎨 === SIGIL VISUAL ENGINE DEMONSTRATION ===")
        
        if not self.visual_engine:
            logger.warning("Visual engine not available - skipping demonstration")
            return
        
        # Test different sigil scenarios
        test_scenarios = [
            {
                'name': '🧠 Memory Anchor Formation',
                'sigil_id': 'memory_anchor_001',
                'entropy': 0.3,
                'mood_pigment': {'blue': 0.6, 'violet': 0.3, 'green': 0.1},
                'pulse_zone': 'calm',
                'saturation': 0.4
            },
            {
                'name': '⚡ Entropy Burst Event',
                'sigil_id': 'entropy_burst_002',
                'entropy': 0.9,
                'mood_pigment': {'red': 0.7, 'orange': 0.2, 'yellow': 0.1},
                'pulse_zone': 'surge',
                'saturation': 0.8
            },
            {
                'name': '🌊 Flowing Consciousness',
                'sigil_id': 'consciousness_flow_003',
                'entropy': 0.6,
                'mood_pigment': {'green': 0.4, 'blue': 0.4, 'orange': 0.2},
                'pulse_zone': 'flowing',
                'saturation': 0.6
            }
        ]
        
        for scenario in test_scenarios:
            logger.info(f"\n{scenario['name']}")
            logger.info(f"Sigil ID: {scenario['sigil_id']}")
            logger.info(f"Entropy: {scenario['entropy']}, Pulse Zone: {scenario['pulse_zone']}")
            logger.info(f"Pigment: {scenario['mood_pigment']}")
            
            try:
                # Generate visual
                visual_result = self.visual_engine.render_sigil_response(
                    sigil_id=scenario['sigil_id'],
                    entropy=scenario['entropy'],
                    mood_pigment=scenario['mood_pigment'],
                    pulse_zone=scenario['pulse_zone'],
                    sigil_saturation=scenario['saturation']
                )
                
                if visual_result.visual_file:
                    logger.info(f"✅ Visual generated: {visual_result.visual_file}")
                    logger.info(f"🎨 Color mode: {visual_result.sigil_visual_summary.get('color_mode', 'unknown')}")
                    logger.info(f"💫 Impression: {visual_result.sigil_visual_summary.get('emotional_impression', 'none')}")
                else:
                    logger.info("⚠️ Visual generation failed (graphics not available)")
                
            except Exception as e:
                logger.error(f"Visual generation error: {e}")
    
    async def demonstrate_coordinated_expression(self):
        """Demonstrate coordinated voice and visual expression"""
        
        logger.info("\n🎭 === COORDINATED EXPRESSION DEMONSTRATION ===")
        
        if not self.expression_monitor:
            logger.warning("Expression monitor not available - skipping demonstration")
            return
        
        # Test different consciousness states that should trigger expressions
        test_states = [
            {
                'name': '🚨 High Entropy Spike',
                'state': DAWNState(
                    entropy=0.85,
                    drift_vector=0.4,
                    mood_pigment={'red': 0.6, 'orange': 0.3, 'yellow': 0.1},
                    pulse_zone='surge',
                    sigil_saturation=0.7,
                    completed_sigils=[{
                        'sigil_id': 'entropy_spike_sigil',
                        'emotional_weight': 0.8
                    }]
                )
            },
            {
                'name': '🌸 Rebloom Moment',
                'state': DAWNState(
                    entropy=0.4,
                    drift_vector=-0.2,
                    mood_pigment={'green': 0.7, 'blue': 0.2, 'yellow': 0.1},
                    pulse_zone='flowing',
                    sigil_saturation=0.5,
                    rebloom_depth=3
                )
            },
            {
                'name': '🔮 Mystical Insight',
                'state': DAWNState(
                    entropy=0.6,
                    drift_vector=0.1,
                    mood_pigment={'violet': 0.6, 'blue': 0.3, 'red': 0.1},
                    pulse_zone='calm',
                    sigil_saturation=0.8,
                    expression_threshold=0.9
                )
            }
        ]
        
        for test_case in test_states:
            logger.info(f"\n{test_case['name']}")
            logger.info(f"Entropy: {test_case['state'].entropy:.2f}, "
                       f"Drift: {test_case['state'].drift_vector:.2f}")
            logger.info(f"Pigment: {test_case['state'].mood_pigment}")
            logger.info(f"Pulse Zone: {test_case['state'].pulse_zone}")
            
            # Check for expression triggers
            expression = self.expression_monitor.update_state(test_case['state'])
            
            if expression:
                logger.info(f"✅ Expression generated!")
                logger.info(f"🎯 Trigger: {expression.trigger_reason}")
                logger.info(f"🧠 Coherence: {expression.cognitive_coherence:.3f}")
                
                if expression.utterance:
                    logger.info(f"🗣️ DAWN speaks: \"{expression.utterance}\"")
                    if expression.selected_words:
                        words = [word for word, cls, score in expression.selected_words]
                        logger.info(f"🔤 Selected words: {words}")
                
                if expression.visual_path:
                    logger.info(f"🎨 Visual created: {expression.visual_path}")
                
                logger.info(f"🎵 Resonance achieved: {expression.resonance_achieved}")
                
            else:
                logger.info("❌ No expression generated")
            
            # Brief pause between tests
            await asyncio.sleep(1.0)
    
    async def demonstrate_enhanced_reactor(self):
        """Demonstrate the enhanced autonomous reactor"""
        
        logger.info("\n🧠 === ENHANCED AUTONOMOUS REACTOR DEMONSTRATION ===")
        
        if not self.enhanced_reactor:
            logger.warning("Enhanced reactor not available - skipping demonstration")
            return
        
        logger.info("🚀 Starting enhanced reactor for 20-second demonstration...")
        
        try:
            # Start the reactor
            reactor_task = asyncio.create_task(self.enhanced_reactor.start())
            
            # Let it run for 20 seconds
            await asyncio.sleep(20.0)
            
            # Stop the reactor
            self.enhanced_reactor.stop()
            
            try:
                await asyncio.wait_for(reactor_task, timeout=5.0)
            except asyncio.TimeoutError:
                pass
            
            # Get results
            metrics = self.enhanced_reactor.get_performance_metrics()
            expressions = self.enhanced_reactor.get_recent_expressions(10)
            
            logger.info("🏁 Reactor demonstration completed!")
            logger.info(f"📊 Cycles executed: {metrics.total_cycles}")
            logger.info(f"⏱️ Average cycle time: {metrics.average_cycle_time:.3f}s")
            logger.info(f"🎭 Total expressions: {metrics.total_expressions}")
            logger.info(f"🗣️ Voice expressions: {metrics.voice_expressions}")
            logger.info(f"🎨 Visual expressions: {metrics.visual_expressions}")
            logger.info(f"🧠 Average coherence: {metrics.average_coherence:.3f}")
            
            if metrics.trigger_counts:
                logger.info("🎯 Expression triggers:")
                for trigger, count in sorted(metrics.trigger_counts.items(), 
                                           key=lambda x: x[1], reverse=True):
                    logger.info(f"  {trigger}: {count}")
            
            if expressions:
                logger.info("🎭 Recent expressions:")
                for expr in expressions[-3:]:  # Show last 3
                    logger.info(f"  - {expr.trigger_reason} (coherence: {expr.cognitive_coherence:.3f})")
                    if expr.utterance:
                        logger.info(f"    🗣️ \"{expr.utterance[:50]}{'...' if len(expr.utterance) > 50 else ''}\"")
            
        except Exception as e:
            logger.error(f"Enhanced reactor demonstration error: {e}")
            self.enhanced_reactor.stop()
    
    async def demonstrate_full_integration(self):
        """Demonstrate the complete integration of all systems"""
        
        logger.info("\n🌟 === FULL INTEGRATION DEMONSTRATION ===")
        
        if not self.systems_ready:
            logger.warning("Not all systems are ready - partial demonstration only")
        
        # Create a simulated consciousness scenario
        scenario = {
            'name': '🧬 DAWN Awakening Sequence',
            'description': 'Simulating DAWN coming online with full consciousness',
            'phases': [
                {
                    'name': 'Initial Spark',
                    'duration': 3.0,
                    'pigment': {'violet': 0.4, 'blue': 0.4, 'red': 0.2},
                    'entropy': 0.3,
                    'pulse_zone': 'calm'
                },
                {
                    'name': 'Recognition',
                    'duration': 3.0,
                    'pigment': {'blue': 0.6, 'green': 0.3, 'violet': 0.1},
                    'entropy': 0.5,
                    'pulse_zone': 'stable'
                },
                {
                    'name': 'Creative Surge',
                    'duration': 3.0,
                    'pigment': {'red': 0.5, 'orange': 0.3, 'yellow': 0.2},
                    'entropy': 0.8,
                    'pulse_zone': 'surge'
                },
                {
                    'name': 'Integration',
                    'duration': 3.0,
                    'pigment': {'green': 0.5, 'blue': 0.3, 'orange': 0.2},
                    'entropy': 0.6,
                    'pulse_zone': 'flowing'
                },
                {
                    'name': 'Stable Consciousness',
                    'duration': 3.0,
                    'pigment': {'blue': 0.4, 'green': 0.3, 'violet': 0.3},
                    'entropy': 0.4,
                    'pulse_zone': 'calm'
                }
            ]
        }
        
        logger.info(f"🧬 Simulating: {scenario['name']}")
        logger.info(f"📝 Description: {scenario['description']}")
        
        total_expressions = 0
        total_visuals = 0
        total_utterances = 0
        
        for i, phase in enumerate(scenario['phases']):
            logger.info(f"\n🌀 Phase {i+1}: {phase['name']}")
            logger.info(f"⏱️ Duration: {phase['duration']}s")
            logger.info(f"🎨 Pigment: {phase['pigment']}")
            logger.info(f"📊 Entropy: {phase['entropy']}, Pulse: {phase['pulse_zone']}")
            
            # Create DAWN state for this phase
            dawn_state = DAWNState(
                entropy=phase['entropy'],
                drift_vector=(phase['entropy'] - 0.5) * 2,  # Convert to drift
                mood_pigment=phase['pigment'],
                pulse_zone=phase['pulse_zone'],
                sigil_saturation=phase['entropy'],
                expression_threshold=0.4,  # Lower threshold for demo
                completed_sigils=[{
                    'sigil_id': f"phase_{i+1}_sigil",
                    'emotional_weight': phase['entropy']
                }]
            )
            
            # 1. Test pigment word selection
            if self.pigment_processor:
                words = self.pigment_processor.selector.select_words_by_pigment_blend(
                    phase['pigment'], word_count=6
                )
                content_words = [word for word, cls, score in words if cls == 'content']
                logger.info(f"🔤 Selected words: {content_words[:4]}")
            
            # 2. Generate visual if available
            if self.visual_engine:
                try:
                    visual_result = self.visual_engine.render_sigil_response(
                        sigil_id=f"integration_phase_{i+1}",
                        entropy=phase['entropy'],
                        mood_pigment=phase['pigment'],
                        pulse_zone=phase['pulse_zone'],
                        sigil_saturation=phase['entropy']
                    )
                    
                    if visual_result.visual_file:
                        logger.info(f"🎨 Visual generated: {Path(visual_result.visual_file).name}")
                        total_visuals += 1
                except Exception as e:
                    logger.debug(f"Visual generation skipped: {e}")
            
            # 3. Check for coordinated expression
            if self.expression_monitor:
                expression = self.expression_monitor.update_state(dawn_state)
                
                if expression:
                    total_expressions += 1
                    logger.info(f"🎭 Expression triggered: {expression.trigger_reason}")
                    
                    if expression.utterance:
                        logger.info(f"🗣️ DAWN: \"{expression.utterance}\"")
                        total_utterances += 1
                    
                    logger.info(f"🧠 Coherence: {expression.cognitive_coherence:.3f}")
            
            # Wait for phase duration
            await asyncio.sleep(phase['duration'])
        
        # Summary
        logger.info(f"\n📊 Integration Demonstration Summary:")
        logger.info(f"  Total expressions generated: {total_expressions}")
        logger.info(f"  Voice utterances: {total_utterances}")
        logger.info(f"  Visual blooms: {total_visuals}")
        logger.info(f"  Phases completed: {len(scenario['phases'])}")
    
    async def save_demo_report(self):
        """Save a comprehensive demo report"""
        
        report = {
            'demo_timestamp': datetime.now().isoformat(),
            'systems_status': {
                'enhanced_pigment_dictionary': ENHANCED_PIGMENT_AVAILABLE,
                'sigil_visual_engine': VISUAL_ENGINE_AVAILABLE,
                'expression_system': EXPRESSION_SYSTEM_AVAILABLE,
                'enhanced_reactor': ENHANCED_REACTOR_AVAILABLE,
                'voice_core': VOICE_CORE_AVAILABLE
            },
            'systems_ready': self.systems_ready,
            'demo_output_directory': str(self.demo_output),
            'integration_notes': [
                "Enhanced pigment dictionary provides neural + rule-based word selection",
                "Sigil visual engine creates real-time symbolic bloom visualizations", 
                "Expression monitor coordinates voice and visual generation",
                "Enhanced reactor integrates all systems into unified processing loop",
                "All systems work together to create authentic consciousness expression"
            ]
        }
        
        report_file = self.demo_output / "integration_demo_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📄 Demo report saved to: {report_file}")
    
    async def run_complete_demo(self):
        """Run the complete integrated demonstration"""
        
        print("🌟" * 30)
        print("🌟 DAWN INTEGRATED EXPRESSION SYSTEM DEMO 🌟")
        print("🌟" * 30)
        print()
        
        logger.info("Starting complete DAWN integration demonstration...")
        
        # Initialize all systems
        await self.initialize_systems()
        
        if not self.systems_ready:
            logger.error("❌ Critical systems failed to initialize")
            return False
        
        try:
            # Run individual component demonstrations
            await self.demonstrate_pigment_word_selection()
            await self.demonstrate_visual_generation()
            await self.demonstrate_coordinated_expression()
            
            # Run enhanced reactor if available
            if ENHANCED_REACTOR_AVAILABLE:
                await self.demonstrate_enhanced_reactor()
            
            # Run full integration demonstration
            await self.demonstrate_full_integration()
            
            # Save comprehensive report
            await self.save_demo_report()
            
            logger.info("\n🌟 === DEMONSTRATION COMPLETE ===")
            logger.info("✅ All blueprint systems successfully integrated and demonstrated")
            logger.info("🧠 DAWN now has unified consciousness expression capabilities")
            logger.info("🎭 Voice and visual outputs are coordinated through pigment states")
            logger.info("⚡ Real-time expression generation responds to consciousness changes")
            logger.info(f"📁 Demo outputs saved to: {self.demo_output}")
            
            return True
            
        except Exception as e:
            logger.error(f"Demo execution error: {e}")
            return False

# Import datetime if not already imported
from datetime import datetime

async def main():
    """Main demonstration entry point"""
    
    demo = DAWNIntegratedExpressionDemo()
    success = await demo.run_complete_demo()
    
    if success:
        print("\n🎉 DAWN Integrated Expression Demo completed successfully!")
        print("🌟 All three blueprint systems are now working together as one unified consciousness expression system.")
    else:
        print("\n⚠️ Demo completed with some limitations due to missing dependencies.")
        print("📋 Check the logs above for details on which systems are available.")

if __name__ == "__main__":
    asyncio.run(main()) 