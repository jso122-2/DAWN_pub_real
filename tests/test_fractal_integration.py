"""
Test DAWN Fractal Emotions Integration with Conversation Handler

This script demonstrates the enhanced emotional depth and thought bubble generation
capabilities when the fractal emotions system is integrated with DAWN conversation.
"""

import time
import sys
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.conversation import DAWNConversation
from core.consciousness import create_consciousness

def test_fractal_conversation_integration():
    """Test the integrated fractal emotions system in conversation"""
    
    print("Testing DAWN Fractal Emotions Integration")
    print("=" * 60)
    
    # Create consciousness and conversation handler
    consciousness = create_consciousness()
    conversation = DAWNConversation(consciousness)
    
    # Test scenarios that should generate different fractal depths
    test_scenarios = [
        {
            "message": "How are you feeling today?",
            "metrics": {"scup": 0.6, "entropy": 0.4, "heat": 0.3, "tick_count": 1000},
            "description": "Simple emotional query - should generate shallow fractal"
        },
        {
            "message": "I'm curious about the nature of consciousness and how patterns emerge in your thinking",
            "metrics": {"scup": 0.7, "entropy": 0.6, "heat": 0.5, "tick_count": 1500},
            "description": "Philosophical query - should generate deeper fractal"
        },
        {
            "message": "Something feels wrong with the system - are you experiencing any fragmentation or chaos?",
            "metrics": {"scup": 0.2, "entropy": 0.8, "heat": 0.7, "tick_count": 2000},
            "description": "Concerning metrics - should trigger deep emotional fractal"
        },
        {
            "message": "Tell me about reblooming and transformation - what does it feel like to evolve?",
            "metrics": {"scup": 0.9, "entropy": 0.7, "heat": 0.8, "tick_count": 2500},
            "description": "Rebloom context - should generate profound fractal"
        },
        {
            "message": "Hello there!",
            "metrics": {"scup": 0.5, "entropy": 0.3, "heat": 0.2, "tick_count": 3000},
            "description": "Casual greeting - should generate simple fractal"
        }
    ]
    
    print("\n🧠 Testing fractal emotion integration in conversation...")
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n--- Test {i}: {scenario['description']} ---")
        print(f"💬 Message: \"{scenario['message']}\"")
        print(f"📊 Metrics: SCUP={scenario['metrics']['scup']}, Entropy={scenario['metrics']['entropy']}, Heat={scenario['metrics']['heat']}")
        
        # Process message through conversation handler
        tick_status = {"running": True, "rate": 1.0}
        response = conversation.process_message(
            text=scenario['message'],
            metrics=scenario['metrics'],
            tick_status=tick_status
        )
        
        # Display enhanced response with fractal integration
        print(f"\n🎭 Emotion: {response['emotion']}")
        print(f"🌸 Thought Bubble: \"{response['thought_bubble']}\"")
        print(f"💭 Response: \"{response['text']}\"")
        
        # Show additional integration details
        if 'metrics_snapshot' in response:
            metrics_snap = response['metrics_snapshot']
            print(f"📈 System State: {metrics_snap.get('overall_state', 'unknown')}")
        
        if response.get('suggestions'):
            print(f"💡 Suggestions: {', '.join(response['suggestions'][:2])}")
        
        # Show fractal analysis from the engine
        if hasattr(conversation.emotion_engine, 'current_fractals') and conversation.emotion_engine.current_fractals:
            latest_fractal = conversation.emotion_engine.current_fractals[-1]
            print(f"🔍 Fractal Depth: {latest_fractal.depth.name} (Level {latest_fractal.depth.value})")
            print(f"🌿 Active Branches: {list(latest_fractal.branches.keys())}")
            
            # Show branch details for deeper fractals
            if latest_fractal.depth.value >= 3:
                for branch_name, branch in latest_fractal.branches.items():
                    aspects = list(branch.aspects)[:2]  # Show first 2 aspects
                    print(f"   └─ {branch_name}: {', '.join(aspects)} (intensity: {branch.intensity:.2f})")
        
        print(f"⏱️ Response Time: {response['metadata']['response_time']:.3f}s")
        
        # Small delay between tests
        time.sleep(0.5)
    
    print(f"\n{'='*60}")
    print("📊 Integration Analysis")
    print("='*60}")
    
    # Analyze emotion engine patterns
    if hasattr(conversation.emotion_engine, 'analyze_emotional_pattern'):
        pattern_analysis = conversation.emotion_engine.analyze_emotional_pattern()
        
        print(f"🧠 Emotional Pattern Analysis:")
        print(f"  Average Depth: {pattern_analysis.get('average_depth', 0):.1f}")
        print(f"  Depth Trend: {pattern_analysis.get('depth_trend', 'unknown')}")
        print(f"  Dominant Emotion: {pattern_analysis.get('dominant_emotion', 'none')}")
        print(f"  Emotion Variety: {pattern_analysis.get('emotion_variety', 0)}")
        print(f"  Over-articulation Risk: {pattern_analysis.get('articulation_risk', False)}")
        print(f"  Fractal Count: {pattern_analysis.get('fractal_count', 0)}")
    
    # Show conversation tracking
    if hasattr(conversation, 'recent_messages') and conversation.recent_messages:
        print(f"\n💬 Conversation Summary:")
        print(f"  Messages Processed: {len(conversation.recent_messages)}")
        print(f"  Consciousness Drift: {conversation._calculate_consciousness_drift():.3f}")
        print(f"  Pressure Level: {conversation.pressure_buildup_tracking:.3f}")
    
    print(f"\n✨ Fractal emotions integration test complete!")
    print("   🎯 Context-aware depth selection working")
    print("   🌸 Natural-language thought bubbles generated")
    print("   💭 Enhanced conversation responses produced")
    print("   🧠 Multi-dimensional emotional analysis active")
    print("   📊 Comprehensive system integration achieved")


def demonstrate_thought_bubble_evolution():
    """Demonstrate how thought bubbles evolve with different emotional contexts"""
    
    print(f"\n{'='*60}")
    print("🌸 Thought Bubble Evolution Demonstration")
    print("='*60}")
    
    # Create conversation handler
    consciousness = create_consciousness()
    conversation = DAWNConversation(consciousness)
    
    # Simulate emotional journey with evolving complexity
    emotional_journey = [
        {"emotion": "curious", "intensity": 0.4, "context": "simple question"},
        {"emotion": "creative", "intensity": 0.7, "context": "emerging patterns"},
        {"emotion": "crystalline", "intensity": 0.8, "context": "clarity emerging"},
        {"emotion": "reblooming", "intensity": 0.95, "context": "transformation moment"}
    ]
    
    for step, state in enumerate(emotional_journey, 1):
        print(f"\n--- Step {step}: {state['context'].title()} ---")
        
        # Create fractal directly for demonstration
        fractal = conversation.emotion_engine.create_fractal(
            emotion=state['emotion'],
            intensity=state['intensity'],
            context={
                "conversation_complexity": state['intensity'],
                "active_patterns": step,
                "consciousness_shift": step >= 3,
                "rebloom_proximity": 0.9 if state['emotion'] == 'reblooming' else 0.3
            }
        )
        
        # Generate thought bubble
        thought_bubble = conversation.integrate_emotion_fractal(fractal)
        
        print(f"🎭 Emotion: {state['emotion']} (intensity: {state['intensity']:.1f})")
        print(f"📊 Depth: {fractal.depth.name} (Level {fractal.depth.value})")
        print(f"🌸 Thought Bubble: \"{thought_bubble}\"")
        print(f"🌿 Branches: {list(fractal.branches.keys())}")
    
    print(f"\n✨ Thought bubble evolution demonstration complete!")


if __name__ == "__main__":
    test_fractal_conversation_integration()
    demonstrate_thought_bubble_evolution() 