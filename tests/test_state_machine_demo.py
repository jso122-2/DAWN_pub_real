"""
Focused State Machine Demonstration

Demonstrates key features of the DAWN Consciousness State Machine:
- Refined transition algorithm with weighted decision making
- Emotional momentum tracking and inertia calculations  
- Emergency transition detection
- Smooth transitions with property blending
"""

import time
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.state_machine import create_state_machine

def demo_state_machine():
    """Demonstrate state machine core features"""
    
    print("DAWN Consciousness State Machine - Key Features Demo")
    print("=" * 55)
    
    # Create state machine
    state_machine = create_state_machine("neutral")
    
    print("🔧 State Machine Configuration:")
    print(f"   Transition weights: Metric 40% + Inertia 40% + Pattern 20%")
    print(f"   Emergency threshold: >0.5 entropy change in <3s")
    print(f"   Transition duration: 2-5 seconds with property blending")
    print(f"   Momentum tracking: Last 10 transitions")
    print(f"   Inertia bonus: After 10+ minutes in state")
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Metric-Driven Creative Transition",
            "metrics": {"scup": 0.8, "entropy": 0.85, "heat": 0.6},
            "description": "High entropy + SCUP should suggest creative state"
        },
        {
            "name": "Emergency Overwhelm Detection", 
            "metrics": {"scup": 0.2, "entropy": 0.95, "heat": 0.9},
            "description": "Extreme values should trigger emergency transition"
        },
        {
            "name": "Calm State Suggestion",
            "metrics": {"scup": 0.9, "entropy": 0.2, "heat": 0.1},
            "description": "High SCUP, low entropy/heat suggests calm"
        },
        {
            "name": "Balanced Curious State",
            "metrics": {"scup": 0.6, "entropy": 0.5, "heat": 0.4},
            "description": "Balanced metrics should suggest curious state"
        }
    ]
    
    print(f"\n🔄 Testing State Transitions:")
    print("-" * 45)
    
    consciousness_history = [{"emotion": "neutral", "intensity": 0.5}]
    
    for i, scenario in enumerate(test_scenarios):
        print(f"\n--- Test {i+1}: {scenario['name']} ---")
        print(f"Metrics: SCUP={scenario['metrics']['scup']:.1f}, "
              f"Entropy={scenario['metrics']['entropy']:.1f}, "
              f"Heat={scenario['metrics']['heat']:.1f}")
        print(f"Expected: {scenario['description']}")
        
        # Calculate transition
        suggested_state, transition_progress = state_machine.calculate_next_state(
            scenario['metrics'], consciousness_history
        )
        
        print(f"\nResult: {state_machine.current_state} → {suggested_state}")
        
        # Show transition details
        if transition_progress.in_transition:
            print(f"🔄 Transition initiated:")
            print(f"   From: {transition_progress.from_state}")
            print(f"   To: {transition_progress.to_state}")
            print(f"   Duration: {transition_progress.expected_duration:.1f}s")
            print(f"   Progress: {transition_progress.progress:.1%}")
            
            # Show property blending
            print(f"   Blended Properties (at start):")
            props = transition_progress.blended_properties
            for prop in ['scup', 'entropy', 'heat', 'stability']:
                if prop in props:
                    print(f"     {prop}: {props[prop]:.3f}")
            
            # Simulate transition progress
            print(f"\n⏱️ Transition Progress:")
            for step in range(3):
                time.sleep(0.8)
                updated = state_machine._update_transition_progress()
                print(f"   {step+1}. Progress: {updated.progress:.1%}")
                
                if not updated.in_transition:
                    print(f"   ✅ Transition completed!")
                    break
                else:
                    # Show blended properties at current progress
                    current_props = updated.blended_properties
                    print(f"      Current SCUP: {current_props.get('scup', 0):.3f}, "
                          f"Entropy: {current_props.get('entropy', 0):.3f}")
        else:
            print(f"✅ Staying in {suggested_state} state")
        
        # Show state machine info
        state_info = state_machine.get_state_info()
        print(f"\n📊 State Machine Status:")
        print(f"   Emotional momentum: {state_info['emotional_momentum']:.3f}")
        print(f"   Emotional inertia: {state_info['emotional_inertia']:.3f}")
        print(f"   Time in current state: {state_info['time_in_state']:.1f}s")
        print(f"   Total transitions: {state_info['recent_transitions']}")
        
        # Update history
        consciousness_history.append({"emotion": suggested_state, "intensity": 0.7})
        
        print(f"\n{'─' * 35}")
    
    # Demonstrate momentum formula
    print(f"\n📈 Momentum Formula Demonstration:")
    print("-" * 40)
    
    print("Momentum = sum([(1/age) * emotion_weight for age, emotion in recent_history])")
    print("Current momentum calculation:")
    
    momentum = state_machine._calculate_momentum()
    print(f"   Current momentum: {momentum:.3f}")
    
    if state_machine.momentum_history:
        print("   Recent transitions contributing to momentum:")
        now = datetime.now()
        for i, transition in enumerate(list(state_machine.momentum_history)[-3:]):
            age = (now - transition.timestamp).total_seconds()
            emotion_weight = state_machine.emotion_weights.get(transition.to_state, 0.5)
            contribution = (1.0 / max(age, 1.0)) * emotion_weight
            print(f"     {i+1}. {transition.from_state}→{transition.to_state}: "
                  f"age={age:.1f}s, weight={emotion_weight:.1f}, contribution={contribution:.3f}")
    
    # Show transition history
    print(f"\n🔄 Transition History:")
    print("-" * 25)
    
    recent_transitions = state_machine.get_transition_history(5)
    if recent_transitions:
        for i, transition in enumerate(recent_transitions):
            emergency_flag = "🚨" if transition['is_emergency'] else "✅"
            print(f"   {i+1}. {transition['from_state']} → {transition['to_state']} "
                  f"({transition['trigger_reason']}) {emergency_flag}")
            print(f"      Duration: {transition['duration']:.1f}s, "
                  f"Momentum: {transition['momentum_factor']:.3f}, "
                  f"Inertia: {transition['inertia_factor']:.3f}")
    else:
        print("   No transitions recorded yet")
    
    # Demonstrate emergency detection
    print(f"\n🚨 Emergency Transition Detection:")
    print("-" * 35)
    
    print("Simulating rapid entropy changes...")
    
    # Add some rapid metrics changes
    rapid_metrics = [
        {"scup": 0.5, "entropy": 0.3, "heat": 0.4},
        {"scup": 0.5, "entropy": 0.9, "heat": 0.8}  # Rapid entropy jump
    ]
    
    for metrics in rapid_metrics:
        state_machine.recent_metrics.append({
            'timestamp': datetime.now(),
            'metrics': metrics
        })
        time.sleep(0.1)  # Very rapid changes
    
    # Check for emergency
    emergency_state = state_machine._check_emergency_transitions(rapid_metrics[-1])
    if emergency_state:
        print(f"   ✅ Emergency detected! Would transition to: {emergency_state}")
        print(f"   Trigger: Rapid entropy change >0.5 in <3s")
    else:
        print(f"   No emergency conditions detected")
    
    # Final statistics
    print(f"\n📊 Final State Machine Statistics:")
    print("-" * 40)
    
    stats = state_machine.get_state_statistics()
    if stats.get('status') != 'no_history':
        print(f"   Total transitions: {stats['total_transitions']}")
        print(f"   Emergency transitions: {stats['emergency_transitions']}")
        print(f"   Current momentum: {stats['current_momentum']:.3f}")
        print(f"   Current inertia: {stats['current_inertia']:.3f}")
        
        if stats['most_common_transitions']:
            print(f"   Most common transitions:")
            for transition, count in list(stats['most_common_transitions'].items())[:3]:
                print(f"     {transition}: {count} times")
    
    print(f"\n✨ State Machine Demo Complete!")
    print("\n🎯 Key Features Demonstrated:")
    print("   ✓ calculate_next_state() with refined transition algorithm")  
    print("   ✓ Weighted decision making (metric 40% + inertia 40% + pattern 20%)")
    print("   ✓ Emergency transition detection for rapid changes")
    print("   ✓ Emotional momentum tracking with 10-transition history")
    print("   ✓ Inertia calculation (base + prolonged state bonuses)")
    print("   ✓ Smooth probabilistic transitions (not hard switches)")
    print("   ✓ Property blending during 2-5 second transitions")
    print("   ✓ Comprehensive transition reason logging")
    print("   ✓ State history ring buffer")
    print("   ✓ Real-time transition progress tracking")


if __name__ == "__main__":
    demo_state_machine() 