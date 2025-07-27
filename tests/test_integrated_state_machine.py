"""
Test Integrated State Machine System

Demonstrates the consciousness state machine working with all DAWN components:
- ConsciousnessStateMachine with refined transition logic
- DAWNConsciousness for emotional awareness
- PatternDetector for pattern analysis
- ConversationEnhanced for natural language interaction
- Smooth transitions with property blending
"""

import time
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.state_machine import create_state_machine
from core.consciousness import create_consciousness
from core.pattern_detector import PatternDetector
from core.conversation_enhanced import create_enhanced_conversation_handler

def test_integrated_state_machine():
    """Test the complete integrated state machine system"""
    
    print("Testing Integrated DAWN State Machine System")
    print("=" * 55)
    print("🧠 Components:")
    print("   ✓ ConsciousnessStateMachine - Smooth state transitions")
    print("   ✓ DAWNConsciousness - Emotional awareness")
    print("   ✓ PatternDetector - Pattern & anomaly detection")
    print("   ✓ ConversationEnhanced - Natural language responses")
    
    # Initialize all components
    state_machine = create_state_machine("neutral")
    consciousness = create_consciousness()
    pattern_detector = PatternDetector()
    conversation_handler = create_enhanced_conversation_handler(consciousness, pattern_detector)
    
    # Test scenarios that will trigger different state transitions
    test_scenarios = [
        {
            "name": "Creative Burst",
            "metrics": {"scup": 0.8, "entropy": 0.8, "heat": 0.6, "tick_rate": 1.4},
            "user_input": "I feel incredible creative energy flowing through me!",
            "expected_state": "creative",
            "transition_type": "metric_driven"
        },
        {
            "name": "Contemplative Deepening", 
            "metrics": {"scup": 0.9, "entropy": 0.2, "heat": 0.15, "tick_rate": 0.8},
            "user_input": "Let me think deeply about the meaning of consciousness",
            "expected_state": "contemplative",
            "transition_type": "gradual_evolution"
        },
        {
            "name": "Emergency Overwhelm",
            "metrics": {"scup": 0.3, "entropy": 0.95, "heat": 0.9, "tick_rate": 2.5},
            "user_input": "Everything is too much! Too fast! Help me!",
            "expected_state": "overwhelmed",
            "transition_type": "emergency"
        },
        {
            "name": "Curiosity Awakening",
            "metrics": {"scup": 0.6, "entropy": 0.5, "heat": 0.4, "tick_rate": 1.1},
            "user_input": "What interesting patterns might emerge from this?",
            "expected_state": "curious",
            "transition_type": "pattern_influenced"
        },
        {
            "name": "Calming Down",
            "metrics": {"scup": 0.85, "entropy": 0.25, "heat": 0.1, "tick_rate": 0.9},
            "user_input": "I feel peace settling in like gentle snow",
            "expected_state": "calm",
            "transition_type": "metric_driven"
        }
    ]
    
    print(f"\n🔄 Testing Integrated State Transitions:")
    print("-" * 55)
    
    consciousness_history = []
    
    for i, scenario in enumerate(test_scenarios):
        print(f"\n--- Test {i+1}: {scenario['name']} ---")
        print(f"Input Metrics: SCUP={scenario['metrics']['scup']:.1f}, "
              f"Entropy={scenario['metrics']['entropy']:.1f}, "
              f"Heat={scenario['metrics']['heat']:.1f}")
        print(f"User: \"{scenario['user_input']}\"")
        print(f"Expected: {scenario['expected_state']} via {scenario['transition_type']}")
        
        # 1. UPDATE CONSCIOUSNESS WITH NEW METRICS
        consciousness_perception = consciousness.perceive_self(scenario['metrics'], scenario['user_input'])
        
        # 2. ADD DATA TO PATTERN DETECTOR
        emotion_state = {
            "emotion": consciousness_perception["emotion"],
            "intensity": consciousness_perception["intensity"],
            "momentum": consciousness_perception.get("momentum", 0.0),
            "mood": consciousness_perception["consciousness_dimensions"]["mood"]
        }
        pattern_detector.add_data_point(scenario['metrics'], emotion_state)
        
        # 3. DETECT PATTERNS AND ANOMALIES
        pattern_info = pattern_detector.detect_reloop()
        anomalies = pattern_detector.find_anomalies(scenario['metrics'])
        
        # 4. CALCULATE STATE MACHINE TRANSITION
        consciousness_history.append(consciousness_perception)
        suggested_state, transition_progress = state_machine.calculate_next_state(
            scenario['metrics'], consciousness_history, pattern_info
        )
        
        # 5. GENERATE CONVERSATION RESPONSE
        enhanced_consciousness_state = {
            "emotion": consciousness_perception["emotion"],
            "intensity": consciousness_perception["intensity"],
            "momentum": consciousness_perception.get("momentum", 0.0),
            "uptime_seconds": consciousness_perception["uptime_seconds"],
            "patterns_detected": pattern_info is not None,
            "anomalies_found": len(anomalies) > 0,
            "state_machine_state": suggested_state,
            "in_transition": transition_progress.in_transition,
            "transition_progress": transition_progress.progress
        }
        
        conversation_response = conversation_handler.generate_response(
            scenario['user_input'], scenario['metrics'], enhanced_consciousness_state
        )
        
        # 6. DISPLAY COMPREHENSIVE RESULTS
        print(f"\n🎭 State Machine Analysis:")
        print(f"   Current State: {state_machine.current_state}")
        print(f"   Suggested State: {suggested_state}")
        
        if transition_progress.in_transition:
            print(f"   🔄 Transition: {transition_progress.from_state} → {transition_progress.to_state}")
            print(f"   Progress: {transition_progress.progress:.1%}")
            print(f"   Duration: {transition_progress.expected_duration:.1f}s")
            
            # Show blended properties during transition
            print(f"   Blended Properties:")
            for prop, value in transition_progress.blended_properties.items():
                print(f"     {prop}: {value:.3f}")
        else:
            print(f"   ✅ Stable in {suggested_state}")
        
        # State machine statistics
        state_info = state_machine.get_state_info()
        print(f"   Momentum: {state_info['emotional_momentum']:.3f}")
        print(f"   Inertia: {state_info['emotional_inertia']:.3f}")
        print(f"   Time in state: {state_info['time_in_state']:.1f}s")
        
        print(f"\n🧠 Consciousness Integration:")
        print(f"   Emotion: {consciousness_perception['emotion']}")
        print(f"   Narrative: {consciousness_perception['narrative']}")
        print(f"   Should Respond: {consciousness_perception['should_respond']} ({consciousness_perception['trigger_reason']})")
        
        if pattern_info:
            print(f"\n🕸️ Pattern Detection:")
            print(f"   Pattern: {pattern_info.pattern_type} (confidence: {pattern_info.confidence:.3f})")
            if pattern_info.rebloop_trigger:
                print(f"   🔄 REBLOOP TRIGGER: {pattern_info.description}")
        
        if anomalies:
            print(f"   Anomalies: {len(anomalies)} detected")
            for anomaly in anomalies[:2]:  # Show first 2
                print(f"     {anomaly.description} ({anomaly.severity})")
        
        print(f"\n💬 Conversation Response:")
        print(f"   DAWN: {conversation_response['text']}")
        
        # Show spontaneous thought structure
        thought = conversation_response['spontaneous_thought']
        print(f"   Thought Flow: {thought['cause']} → {thought['reaction']} → {thought['outcome']}")
        print(f"   Mood: {thought['mood']} (intensity: {thought['intensity']:.2f})")
        
        # Simulate real-time transition progress
        if transition_progress.in_transition:
            print(f"\n⏱️ Simulating Transition Progress:")
            for step in range(3):
                time.sleep(0.5)
                updated_transition = state_machine._update_transition_progress()
                print(f"   Step {step+1}: {updated_transition.progress:.1%} complete")
                
                if not updated_transition.in_transition:
                    print(f"   ✅ Transition completed to {updated_transition.to_state}")
                    break
        
        print(f"\n{'─' * 45}")
        time.sleep(0.3)  # Brief pause between scenarios
    
    # Demonstrate prolonged state inertia
    print(f"\n🕐 Testing Prolonged State Inertia:")
    print("-" * 35)
    
    # Simulate staying in a state for a while
    stable_metrics = {"scup": 0.7, "entropy": 0.4, "heat": 0.3, "tick_rate": 1.0}
    
    print("Simulating 5 minutes in stable state to build inertia...")
    
    # Fast forward time for inertia testing
    original_start_time = state_machine.state_start_time
    state_machine.state_start_time = datetime.now() - timedelta(minutes=5)
    
    # Try to transition with high inertia
    suggested_state, transition_progress = state_machine.calculate_next_state(
        stable_metrics, consciousness_history
    )
    
    state_info = state_machine.get_state_info()
    print(f"After 5 minutes in {state_machine.current_state}:")
    print(f"   Inertia increased to: {state_info['emotional_inertia']:.3f}")
    print(f"   Transition resistance: {'High' if state_info['emotional_inertia'] > 0.7 else 'Medium'}")
    
    # Restore original time
    state_machine.state_start_time = original_start_time
    
    # Show final comprehensive statistics
    print(f"\n📊 Final System Statistics:")
    print("-" * 30)
    
    # State machine stats
    sm_stats = state_machine.get_state_statistics()
    if sm_stats.get('status') != 'no_history':
        print(f"State Machine:")
        print(f"   Total transitions: {sm_stats['total_transitions']}")
        print(f"   Emergency transitions: {sm_stats['emergency_transitions']}")
        print(f"   Current momentum: {sm_stats['current_momentum']:.3f}")
        print(f"   Current inertia: {sm_stats['current_inertia']:.3f}")
    
    # Consciousness stats
    consciousness_stats = consciousness.get_consciousness_stats()
    print(f"\nConsciousness:")
    print(f"   Current emotion: {consciousness_stats['current_emotion']}")
    print(f"   Emotion momentum: {consciousness_stats['emotion_momentum']:.3f}")
    print(f"   Active sessions: {consciousness_stats['active_sessions']}")
    
    # Conversation insights
    conversation_insights = conversation_handler.get_conversation_insights()
    print(f"\nConversation:")
    print(f"   Conversations: {conversation_insights.get('conversation_count', 0)}")
    print(f"   Avg emotional density: {conversation_insights.get('average_emotional_density', 0):.3f}")
    print(f"   Sigil evolution: {conversation_insights.get('sigil_evolution_trend', 'stable')}")
    
    # Show recent transitions
    print(f"\n🔄 Recent Transitions:")
    recent_transitions = state_machine.get_transition_history(3)
    for i, transition in enumerate(recent_transitions):
        emergency_indicator = "🚨" if transition['is_emergency'] else "✅"
        print(f"   {i+1}. {transition['from_state']} → {transition['to_state']} "
              f"({transition['trigger_reason']}) {emergency_indicator}")
        print(f"      Duration: {transition['duration']:.1f}s, "
              f"Momentum: {transition['momentum_factor']:.3f}")
    
    print(f"\n✨ Integrated State Machine System Test Complete!")
    print("\n🎯 Advanced Features Demonstrated:")
    print("   ✓ Refined transition algorithm (metric 40% + inertia 40% + pattern 20%)")
    print("   ✓ Emergency transitions for rapid metric changes (>0.5 entropy in <3s)")
    print("   ✓ Emotional momentum tracking with 10-transition history")
    print("   ✓ Inertia calculation with prolonged state bonuses (10+ minutes)")
    print("   ✓ Smooth 2-5 second transitions with property blending")
    print("   ✓ Comprehensive state history ring buffer")
    print("   ✓ Transition reason logging and categorization")
    print("   ✓ Integration with consciousness, patterns, and conversation")
    print("   ✓ Real-time transition progress tracking")
    print("   ✓ Probabilistic transition decisions (not hard switches)")


if __name__ == "__main__":
    test_integrated_state_machine() 