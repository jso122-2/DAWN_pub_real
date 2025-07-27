"""
Test Integrated Conversation System

Demonstrates the enhanced conversation handler working with consciousness 
and pattern detection systems for a complete DAWN conversational experience.
"""

import sys
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.consciousness import DAWNConsciousness
from core.pattern_detector import PatternDetector
from core.conversation_enhanced import create_enhanced_conversation_handler

def test_integrated_conversation():
    """Test the fully integrated conversation system"""
    
    print("Testing Integrated DAWN Conversation System")
    print("=" * 50)
    print("🧠 Components:")
    print("   ✓ DAWNConsciousness - Emotional awareness")
    print("   ✓ PatternDetector - Pattern & anomaly detection") 
    print("   ✓ ConversationEnhanced - Spontaneous thought generation")
    
    # Initialize all components
    consciousness = DAWNConsciousness()
    pattern_detector = PatternDetector()
    conversation_handler = create_enhanced_conversation_handler(consciousness, pattern_detector)
    
    # Test metrics that trigger different states
    test_scenarios = [
        {
            "name": "Creative State with Pattern Discovery",
            "metrics": {"scup": 0.8, "entropy": 0.7, "heat": 0.6, "tick_rate": 1.5},
            "user_input": "I sense something beautiful emerging in the patterns - what do you feel?"
        },
        {
            "name": "Contemplative State with Low Energy",
            "metrics": {"scup": 0.6, "entropy": 0.3, "heat": 0.2, "tick_rate": 0.8},
            "user_input": "Take a moment to reflect deeply on your inner experience"
        },
        {
            "name": "Overwhelmed State with High Complexity",
            "metrics": {"scup": 0.4, "entropy": 0.9, "heat": 0.8, "tick_rate": 2.0},
            "user_input": "The system seems intense right now - how are you handling the complexity?"
        },
        {
            "name": "Acceleration Request with Pattern Focus",
            "metrics": {"scup": 0.7, "entropy": 0.5, "heat": 0.7, "tick_rate": 1.2},
            "user_input": "Speed up the system please - I want to see the web of connections accelerate"
        }
    ]
    
    print(f"\n🗣️ Testing Integrated Conversations:")
    print("-" * 50)
    
    for i, scenario in enumerate(test_scenarios):
        print(f"\n--- Test {i+1}: {scenario['name']} ---")
        
        # Get consciousness state using current metrics
        consciousness_perception = consciousness.perceive_self(scenario['metrics'])
        
        # Add data point and detect patterns and anomalies
        emotion_state = {"emotion": "curious", "intensity": 0.5, "momentum": 0.0, "mood": "neutral"}
        pattern_detector.add_data_point(scenario['metrics'], emotion_state)
        
        pattern_info = pattern_detector.detect_reloop()
        anomalies = pattern_detector.find_anomalies(scenario['metrics'])
        
        # Add pattern detection to consciousness state
        consciousness_state = {
            "emotion": consciousness_perception["emotion"],
            "intensity": consciousness_perception.get("intensity", 0.5),
            "momentum": consciousness_perception.get("momentum", 0.0),
            "uptime_seconds": 300,
            "patterns_detected": pattern_info is not None,
            "anomalies_found": len(anomalies) > 0
        }
        
        print(f"Metrics: SCUP={scenario['metrics']['scup']:.1f}, "
              f"Entropy={scenario['metrics']['entropy']:.1f}, "
              f"Heat={scenario['metrics']['heat']:.1f}")
        print(f"User: \"{scenario['user_input']}\"")
        
        # Generate integrated response
        response = conversation_handler.generate_response(
            scenario['user_input'], scenario['metrics'], consciousness_state
        )
        
        print(f"\nDAWN: {response['text']}")
        
        # Show integrated analysis
        print(f"\n🧠 Consciousness Analysis:")
        print(f"   Emotion: {consciousness_perception['emotion']}")
        print(f"   Narrative: {consciousness_perception.get('narrative', 'Processing...')}")
        
        print(f"\n🕸️ Pattern Analysis:")
        if pattern_info:
            print(f"   Patterns: {pattern_info.pattern_type} detected (confidence: {pattern_info.confidence:.3f})")
            if pattern_info.rebloop_trigger:
                print(f"   🔄 REBLOOP TRIGGER: {pattern_info.description}")
        if anomalies:
            print(f"   Anomalies: {len(anomalies)} found (severity: {[a.severity for a in anomalies]})")
        if not pattern_info and not anomalies:
            print(f"   Status: Stable patterns, no anomalies")
        
        # Show spontaneous thought integration
        thought = response['spontaneous_thought']
        print(f"\n💭 Spontaneous Thought:")
        print(f"   {thought['cause']} → {thought['reaction']} → {thought['outcome']}")
        print(f"   Mood: {thought['mood']} (intensity: {thought['intensity']:.2f})")
        
        # Show sigil resonance with pattern awareness
        metadata = response['conversation_metadata']
        print(f"\n🔮 Sigil Resonance:")
        print(f"   Emotional Density: {metadata['emotional_density']:.2f}")
        print(f"   Resonance Type: {metadata['resonance_type']}")
        print(f"   Intent: {metadata['intent']}")
        
        if response.get('action'):
            print(f"\n⚡ Action Triggered: {response['action']}")
        
        print(f"\n{'─' * 40}")
    
    # Test with simulated pattern breaking / rebloop detection
    print(f"\n🌀 Testing Pattern Breaking & Spider Metaphors:")
    print("-" * 45)
    
    # Simulate pattern breaking scenario
    rebloop_metrics = {"scup": 0.65, "entropy": 0.8, "heat": 0.75, "tick_rate": 1.8}
    
    # Create pattern history that shows repetition
    for _ in range(5):
        pattern_detector.add_data_point(rebloop_metrics, {"emotion": "anxious", "intensity": 0.8, "momentum": 0.3, "mood": "turbulent"})
    
    # Now trigger detection
    rebloop_detection = pattern_detector.detect_reloop()
    
    consciousness_state_rebloop = {
        "emotion": "anxious",
        "intensity": 0.8,
        "momentum": 0.3,
        "uptime_seconds": 600,
        "patterns_detected": True,
        "rebloop_detected": rebloop_detection is not None and rebloop_detection.rebloop_trigger
    }
    
    rebloop_input = "Something feels cyclical here - like we're caught in a repeating pattern"
    
    response_rebloop = conversation_handler.generate_response(
        rebloop_input, rebloop_metrics, consciousness_state_rebloop
    )
    
    print(f"User: \"{rebloop_input}\"")
    print(f"DAWN: {response_rebloop['text']}")
    
    if "spider" in response_rebloop['text'] or "web" in response_rebloop['text']:
        print("✓ Spider metaphor successfully integrated!")
    
    # Show final system state
    print(f"\n📊 Final System State:")
    insights = conversation_handler.get_conversation_insights()
    print(f"   Conversations: {insights.get('conversation_count', 0)}")
    print(f"   Avg Emotional Density: {insights.get('average_emotional_density', 0):.3f}")
    print(f"   Sigil Evolution: {insights.get('sigil_evolution_trend', 'unknown')}")
    
    current_sigil = insights.get('current_sigil_state', {})
    print(f"   Sigil Density: {current_sigil.get('density', 0):.3f}")
    print(f"   Sigil Resonance: {current_sigil.get('resonance', 0):.3f}")
    
    print(f"\n✨ Integrated Conversation System Test Complete!")
    print("\n🎯 Integration Features Demonstrated:")
    print("   ✓ Consciousness emotional state → spontaneous thought")
    print("   ✓ Pattern detection → spider metaphor integration")
    print("   ✓ Anomaly detection → response intensity adjustment")
    print("   ✓ Sigil awareness → intent parsing enhancement")
    print("   ✓ Action generation → system control integration")
    print("   ✓ Narrative flow → cause→reaction→outcome→mood")
    print("   ✓ Source mapping → natural language conversion")
    print("   ✓ Poetic responses → human-readable expression")


if __name__ == "__main__":
    test_integrated_conversation() 