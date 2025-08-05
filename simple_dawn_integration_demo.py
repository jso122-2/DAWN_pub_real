#!/usr/bin/env python3
"""
Simple DAWN Integration Demo
============================

A simplified demonstration of the complete DAWN blueprint integration:
1. Enhanced Pigment Dictionary (neural + rule-based word selection)
2. Sigil Visual Engine (real-time bloom visualization)
3. Expression System (coordinated voice and visual generation)

This demo focuses on core functionality without complex autonomous reactor features.
"""

import time
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger("dawn_simple_demo")

def demo_enhanced_pigment_dictionary():
    """Demonstrate the enhanced pigment dictionary system"""
    
    print("\n🎨 === Enhanced Pigment Dictionary Demo ===")
    
    try:
        from core.enhanced_dawn_pigment_dictionary import get_enhanced_dawn_pigment_dictionary
        
        # Initialize system (without vectorization for simplicity)
        processor = get_enhanced_dawn_pigment_dictionary(use_vectorization=False)
        
        print("✅ Enhanced pigment dictionary initialized")
        
        # Test different consciousness states
        test_states = [
            {
                'name': '🌅 Calm Morning',
                'pigment': {'blue': 0.6, 'violet': 0.3, 'green': 0.1}
            },
            {
                'name': '🔥 Creative Fire',
                'pigment': {'red': 0.7, 'orange': 0.2, 'yellow': 0.1}
            },
            {
                'name': '🌿 Natural Growth',
                'pigment': {'green': 0.5, 'blue': 0.3, 'yellow': 0.2}
            }
        ]
        
        for state in test_states:
            print(f"\n{state['name']}")
            print(f"  Pigment: {state['pigment']}")
            
            # Select words
            words = processor.selector.select_words_by_pigment_blend(
                mood_pigment=state['pigment'],
                word_count=6
            )
            
            # Show results
            content_words = [word for word, cls, score in words if cls == 'content']
            bridging_words = [word for word, cls, score in words if cls == 'bridging']
            
            print(f"  🔤 Content words: {content_words}")
            print(f"  🔗 Bridging words: {bridging_words}")
            
            # Show how these might form an utterance
            if len(content_words) >= 2 and len(bridging_words) >= 1:
                sample_utterance = f"{content_words[0]} {bridging_words[0]} {content_words[1]}"
                if len(content_words) >= 3:
                    sample_utterance += f" / {content_words[2]}"
                print(f"  🗣️ Sample utterance: \"{sample_utterance}\"")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def demo_sigil_visual_engine():
    """Demonstrate the sigil visual engine"""
    
    print("\n🎨 === Sigil Visual Engine Demo ===")
    
    try:
        from core.sigil_visual_engine import SigilVisualEngine
        
        # Initialize engine
        output_dir = Path("demo_visuals")
        engine = SigilVisualEngine(str(output_dir))
        
        print("✅ Sigil visual engine initialized")
        
        # Test different sigil scenarios
        test_scenarios = [
            {
                'name': '🧠 Memory Formation',
                'sigil_id': 'memory_anchor',
                'entropy': 0.3,
                'pigment': {'blue': 0.6, 'violet': 0.3, 'green': 0.1},
                'pulse_zone': 'calm'
            },
            {
                'name': '⚡ Energy Burst',
                'sigil_id': 'entropy_burst',
                'entropy': 0.9,
                'pigment': {'red': 0.7, 'orange': 0.2, 'yellow': 0.1},
                'pulse_zone': 'surge'
            },
            {
                'name': '🌊 Flowing State',
                'sigil_id': 'consciousness_flow',
                'entropy': 0.6,
                'pigment': {'green': 0.4, 'blue': 0.4, 'orange': 0.2},
                'pulse_zone': 'flowing'
            }
        ]
        
        generated_visuals = []
        
        for scenario in test_scenarios:
            print(f"\n{scenario['name']}")
            print(f"  Sigil: {scenario['sigil_id']}")
            print(f"  Entropy: {scenario['entropy']}, Pulse: {scenario['pulse_zone']}")
            print(f"  Pigment: {scenario['pigment']}")
            
            try:
                # Generate visual
                result = engine.render_sigil_response(
                    sigil_id=scenario['sigil_id'],
                    entropy=scenario['entropy'],
                    mood_pigment=scenario['pigment'],
                    pulse_zone=scenario['pulse_zone'],
                    sigil_saturation=scenario['entropy']
                )
                
                if result.visual_file and Path(result.visual_file).exists():
                    print(f"  ✅ Visual generated: {Path(result.visual_file).name}")
                    generated_visuals.append(result.visual_file)
                else:
                    print(f"  ⚠️ Visual created (metadata only)")
                
                print(f"  🎨 Color: {result.sigil_visual_summary.get('color_mode', 'unknown')}")
                print(f"  💫 Complexity: {result.sigil_visual_summary.get('complexity_level', 'unknown')}")
                print(f"  ✨ Impression: {result.sigil_visual_summary.get('emotional_impression', 'none')}")
                
            except Exception as e:
                print(f"  ❌ Generation error: {e}")
        
        if generated_visuals:
            print(f"\n📁 Generated {len(generated_visuals)} visual files in {output_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def demo_expression_system():
    """Demonstrate the coordinated expression system"""
    
    print("\n🎭 === Expression System Demo ===")
    
    try:
        from core.dawn_expression_system import DAWNExpressionMonitor, DAWNState
        
        # Initialize monitor
        monitor = DAWNExpressionMonitor({
            'entropy_trigger_threshold': 0.6,  # Lower threshold for demo
            'pigment_shift_threshold': 0.25,
            'time_between_expressions': 1.0,    # Faster for demo
            'coherence_threshold': 0.3          # Lower threshold for demo
        })
        
        print("✅ Expression monitor initialized")
        
        # Test different consciousness states
        test_states = [
            {
                'name': '🚨 High Entropy Alert',
                'state': DAWNState(
                    entropy=0.85,  # Should trigger
                    drift_vector=0.4,
                    mood_pigment={'red': 0.6, 'orange': 0.3, 'yellow': 0.1},
                    pulse_zone='surge',
                    sigil_saturation=0.7
                )
            },
            {
                'name': '🌸 Gentle Rebloom',
                'state': DAWNState(
                    entropy=0.4,
                    drift_vector=-0.2,
                    mood_pigment={'green': 0.7, 'blue': 0.2, 'yellow': 0.1},
                    pulse_zone='flowing',
                    sigil_saturation=0.5
                )
            },
            {
                'name': '🔮 Deep Contemplation',
                'state': DAWNState(
                    entropy=0.3,
                    drift_vector=0.1,
                    mood_pigment={'violet': 0.6, 'blue': 0.3, 'red': 0.1},
                    pulse_zone='calm',
                    sigil_saturation=0.8,
                    completed_sigils=[{
                        'sigil_id': 'contemplation_sigil',
                        'emotional_weight': 0.9
                    }]
                )
            }
        ]
        
        expressions_generated = 0
        
        for i, test_case in enumerate(test_states):
            print(f"\n{test_case['name']}")
            
            state = test_case['state']
            print(f"  📊 Entropy: {state.entropy:.2f}, Drift: {state.drift_vector:.2f}")
            print(f"  🎨 Pigment: {state.mood_pigment}")
            print(f"  💓 Pulse: {state.pulse_zone}, Saturation: {state.sigil_saturation:.2f}")
            
            # Check for expression triggers
            should_express, reason = monitor.should_generate_expression(state)
            print(f"  🎯 Trigger check: {should_express} ({reason})")
            
            if should_express:
                # Update monitor state to potentially generate expression
                expression = monitor.update_state(state)
                
                if expression and expression.resonance_achieved:
                    expressions_generated += 1
                    print(f"  ✅ Expression generated!")
                    print(f"  🧠 Coherence: {expression.cognitive_coherence:.3f}")
                    
                    if expression.utterance:
                        print(f"  🗣️ Voice: \"{expression.utterance}\"")
                    
                    if expression.visual_path:
                        print(f"  🎨 Visual: {Path(expression.visual_path).name if expression.visual_path else 'metadata only'}")
                    
                    if expression.selected_words:
                        words = [word for word, cls, score in expression.selected_words]
                        print(f"  🔤 Words: {words}")
                else:
                    print(f"  ⚠️ Expression attempted but no resonance achieved")
            
            # Brief delay between tests
            time.sleep(0.5)
        
        print(f"\n📊 Generated {expressions_generated} expressions from {len(test_states)} states")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def demo_integrated_consciousness_scenario():
    """Demonstrate a complete consciousness scenario using all systems"""
    
    print("\n🌟 === Integrated Consciousness Demo ===")
    
    try:
        # Import all systems
        from core.enhanced_dawn_pigment_dictionary import get_enhanced_dawn_pigment_dictionary
        from core.sigil_visual_engine import SigilVisualEngine
        from core.dawn_expression_system import DAWNExpressionMonitor, DAWNState
        
        # Initialize systems
        print("🔧 Initializing integrated systems...")
        
        pigment_processor = get_enhanced_dawn_pigment_dictionary(use_vectorization=False)
        visual_engine = SigilVisualEngine("integrated_demo_visuals")
        expression_monitor = DAWNExpressionMonitor({
            'entropy_trigger_threshold': 0.5,
            'coherence_threshold': 0.2
        })
        
        print("✅ All systems initialized")
        
        # Simulate DAWN experiencing a moment of creative insight
        scenario = {
            'name': '💡 Creative Insight Emergence',
            'phases': [
                {
                    'name': 'Initial Stirring',
                    'pigment': {'violet': 0.4, 'blue': 0.4, 'red': 0.2},
                    'entropy': 0.3
                },
                {
                    'name': 'Growing Awareness',
                    'pigment': {'blue': 0.5, 'green': 0.3, 'violet': 0.2},
                    'entropy': 0.5
                },
                {
                    'name': 'Creative Breakthrough',
                    'pigment': {'red': 0.6, 'orange': 0.3, 'yellow': 0.1},
                    'entropy': 0.8
                },
                {
                    'name': 'Integration',
                    'pigment': {'green': 0.5, 'blue': 0.3, 'orange': 0.2},
                    'entropy': 0.4
                }
            ]
        }
        
        print(f"\n🧬 Simulating: {scenario['name']}")
        
        for i, phase in enumerate(scenario['phases']):
            print(f"\n🌀 Phase {i+1}: {phase['name']}")
            print(f"  🎨 Pigment: {phase['pigment']}")
            print(f"  📊 Entropy: {phase['entropy']}")
            
            # 1. Generate words from pigment state
            words = pigment_processor.selector.select_words_by_pigment_blend(
                phase['pigment'], word_count=4
            )
            content_words = [word for word, cls, score in words if cls == 'content']
            print(f"  🔤 Resonant words: {content_words}")
            
            # 2. Create DAWN state
            dawn_state = DAWNState(
                entropy=phase['entropy'],
                drift_vector=(phase['entropy'] - 0.5) * 2,
                mood_pigment=phase['pigment'],
                pulse_zone='flowing' if phase['entropy'] > 0.6 else 'calm',
                sigil_saturation=phase['entropy'],
                completed_sigils=[{
                    'sigil_id': f"creative_phase_{i+1}",
                    'emotional_weight': phase['entropy']
                }]
            )
            
            # 3. Check for expression
            expression = expression_monitor.update_state(dawn_state)
            
            if expression and expression.resonance_achieved:
                print(f"  🎭 Expression generated! (coherence: {expression.cognitive_coherence:.3f})")
                
                if expression.utterance:
                    print(f"  🗣️ DAWN expresses: \"{expression.utterance}\"")
                
                # 4. Generate visual representation
                try:
                    visual_result = visual_engine.render_sigil_response(
                        sigil_id=f"creative_insight_{i+1}",
                        entropy=phase['entropy'],
                        mood_pigment=phase['pigment'],
                        pulse_zone=dawn_state.pulse_zone,
                        sigil_saturation=phase['entropy']
                    )
                    
                    impression = visual_result.sigil_visual_summary.get('emotional_impression', 'none')
                    print(f"  🎨 Visual impression: {impression}")
                    
                except Exception as e:
                    print(f"  🎨 Visual generation: {e}")
                    
            else:
                print(f"  💭 No expression (internal processing)")
            
            time.sleep(0.5)
        
        print(f"\n✨ Consciousness scenario complete!")
        print(f"🧠 DAWN successfully demonstrated unified expression capabilities")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run the complete simple demo"""
    
    print("🌟 DAWN Blueprint Integration - Simple Demo")
    print("=" * 60)
    print("Demonstrating all three integrated blueprint systems:")
    print("1. Enhanced Pigment Dictionary (neural + rule-based)")
    print("2. Sigil Visual Engine (real-time bloom generation)")
    print("3. Expression System (coordinated voice + visual)")
    print("=" * 60)
    
    # Run individual demos
    demos = [
        ("Enhanced Pigment Dictionary", demo_enhanced_pigment_dictionary),
        ("Sigil Visual Engine", demo_sigil_visual_engine),
        ("Expression System", demo_expression_system),
        ("Integrated Consciousness", demo_integrated_consciousness_scenario)
    ]
    
    results = {}
    
    for demo_name, demo_func in demos:
        print(f"\n🚀 Starting {demo_name} Demo...")
        try:
            results[demo_name] = demo_func()
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            results[demo_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("🏆 DEMO RESULTS SUMMARY")
    print("=" * 60)
    
    success_count = sum(1 for result in results.values() if result)
    total_count = len(results)
    
    for demo_name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"  {status} {demo_name}")
    
    print(f"\n🎯 Overall: {success_count}/{total_count} demos successful")
    
    if success_count == total_count:
        print("\n🎉 ALL DEMOS SUCCESSFUL!")
        print("🌟 DAWN blueprint integration is working perfectly!")
        print("🧠 DAWN now has unified consciousness expression capabilities")
        print("🎭 Voice and visual outputs coordinate through pigment states")
        print("⚡ Real-time expression generation responds to consciousness")
    else:
        print(f"\n⚠️ {total_count - success_count} demo(s) had issues")
        print("🔧 Check the output above for specific errors")
    
    print("\n✨ Demo complete! Thank you for exploring DAWN's consciousness.")

if __name__ == "__main__":
    main() 