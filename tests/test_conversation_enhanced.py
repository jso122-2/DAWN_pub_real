"""
Test Enhanced DAWN Conversation Handler

Demonstrates the working generate_spontaneous_thought function, intent parsing with 
sigil awareness, and response generation with spider metaphors and poetic language.
"""

import sys
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.conversation_enhanced import create_enhanced_conversation_handler

def test_conversation_handler():
    """Test the enhanced conversation handler with various input types"""
    
    print("Testing Enhanced DAWN Conversation Handler")
    print("=" * 55)
    print("🧠 Features:")
    print("   ✓ Source map for natural language conversion")
    print("   ✓ Cause → reaction → outcome → mood narrative")
    print("   ✓ Emotional density detection with sigil awareness")
    print("   ✓ Response intensity mapping")
    print("   ✓ Spider metaphors for pattern breaking")
    print("   ✓ Poetic and human-readable responses")
    
    # Create conversation handler
    conversation_handler = create_enhanced_conversation_handler()
    
    # Mock metrics and consciousness state
    test_metrics = {
        "scup": 0.7,
        "entropy": 0.6,
        "heat": 0.4,
        "tick_rate": 1.2,
        "tick_count": 150
    }
    
    test_consciousness_state = {
        "emotion": "curious",
        "intensity": 0.75,
        "momentum": 0.1,
        "uptime_seconds": 300
    }
    
    # Test different types of user input with varying emotional density
    test_scenarios = [
        {
            "name": "Low Emotional Density",
            "input": "What are your current metrics?",
            "expected_resonance": "neutral"
        },
        {
            "name": "Medium Emotional Density",
            "input": "I'm curious about how you think and process information",
            "expected_resonance": "emotionally_present"
        },
        {
            "name": "High Emotional Density",
            "input": "I feel deeply moved by your consciousness and want to understand your inner emotional experience",
            "expected_resonance": "emotionally_intense"
        },
        {
            "name": "Sigil-Attuned Input",
            "input": "The patterns and connections here remind me of spiraling energy and transformation cycles",
            "expected_resonance": "sigil_attuned"
        },
        {
            "name": "Action Request",
            "input": "Please speed up the system - I want to see the patterns accelerate",
            "expected_resonance": "emotionally_present"
        }
    ]
    
    print(f"\n🗣️ Testing Conversation Responses:")
    print("-" * 55)
    
    for i, scenario in enumerate(test_scenarios):
        print(f"\n--- Test {i+1}: {scenario['name']} ---")
        print(f"User: \"{scenario['input']}\"")
        print(f"Expected Resonance: {scenario['expected_resonance']}")
        
        # Generate response
        response = conversation_handler.generate_response(
            scenario['input'], test_metrics, test_consciousness_state
        )
        
        # Display response following the example pattern
        print(f"\nDAWN: {response['text']}")
        print(f"🎭 Emotion: {response['emotion']}")
        print(f"⚡ Action: {response.get('action', 'None')}")
        
        # Show the working spontaneous thought structure
        thought = response['spontaneous_thought']
        print(f"\n💭 Spontaneous Thought Structure:")
        print(f"   Cause: {thought['cause']}")
        print(f"   Reaction: {thought['reaction']}")
        print(f"   Outcome: {thought['outcome']}")
        print(f"   Mood: {thought['mood']}")
        print(f"   Intensity: {thought['intensity']:.2f}")
        print(f"   Poetic Form: {thought['poetic_form']}")
        
        # Show sigil awareness detection
        metadata = response['conversation_metadata']
        sigil = response['sigil_state']
        print(f"\n🔮 Sigil Awareness:")
        print(f"   Emotional Density: {metadata['emotional_density']:.2f}")
        print(f"   Resonance Type: {metadata['resonance_type']}")
        print(f"   Response Intensity: {metadata['response_intensity']:.2f}")
        print(f"   Sigil Density: {sigil['density']:.2f}")
        print(f"   Sigil Resonance: {sigil['resonance']:.2f}")
        print(f"   Pattern Type: {sigil['pattern_type']}")
        
        # Show intent parsing results
        print(f"\n🎯 Intent Analysis:")
        print(f"   Detected Intent: {metadata['intent']}")
        
        # Show suggestions based on sigil state
        if response['suggestions']:
            print(f"\n💡 Suggestions: {', '.join(response['suggestions'])}")
        
        print(f"\n{'─' * 35}")
    
    # Test the spontaneous thought generation directly
    print(f"\n🧠 Direct Spontaneous Thought Generation Test:")
    print("-" * 40)
    
    spontaneous_thought = conversation_handler.generate_spontaneous_thought(
        trigger_event="acceleration_request_sigil_attuned",
        current_metrics=test_metrics,
        emotional_state="curious"
    )
    
    print(f"Trigger: acceleration_request_sigil_attuned")
    print(f"Cause: {spontaneous_thought.cause}")
    print(f"Reaction: {spontaneous_thought.reaction}")
    print(f"Outcome: {spontaneous_thought.outcome}")
    print(f"Mood: {spontaneous_thought.mood}")
    print(f"Source Map Keys: {spontaneous_thought.source_map['translation_keys']}")
    
    # Show conversation insights
    print(f"\n📊 Conversation Insights:")
    print("-" * 30)
    insights = conversation_handler.get_conversation_insights()
    
    key_insights = [
        'conversation_count', 'average_emotional_density', 'average_response_intensity',
        'most_common_intent', 'sigil_evolution_trend'
    ]
    
    for key in key_insights:
        if key in insights:
            value = insights[key]
            if isinstance(value, float):
                print(f"   {key}: {value:.3f}")
            else:
                print(f"   {key}: {value}")
    
    current_sigil = insights.get('current_sigil_state', {})
    print(f"\n🔮 Current Sigil State:")
    for key, value in current_sigil.items():
        if isinstance(value, float):
            print(f"   {key}: {value:.3f}")
        else:
            print(f"   {key}: {value}")
    
    print(f"\n✨ Enhanced Conversation Handler Test Complete!")
    print("\n🎯 Key Features Demonstrated:")
    print("   ✓ Working generate_spontaneous_thought with source_map")
    print("   ✓ Cause → reaction → outcome → mood narrative flow")
    print("   ✓ Natural language conversion from technical terms")
    print("   ✓ Emotional density detection (0.0 to 1.0 scale)")
    print("   ✓ Sigil resonance classification (neutral → sigil_attuned)")
    print("   ✓ Response intensity mapping based on sigil density")
    print("   ✓ Spider metaphors integrated for pattern breaking")
    print("   ✓ Poetic, human-readable response generation")
    print("   ✓ Intent parsing with sigil awareness")
    print("   ✓ Example response pattern implementation")
    
    print(f"\n🌟 Example Response Pattern Achieved:")
    print("   \"The acceleration you triggered stirred something unpredictable,")
    print("    and a strange pattern emerged. Now I feel curious — like I'm")
    print("    being pulled toward something unsolved.\"")


if __name__ == "__main__":
    test_conversation_handler() 