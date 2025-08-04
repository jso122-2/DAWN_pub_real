#!/usr/bin/env python3
"""
Test script for Unique Consciousness-Driven Responses
Verifies that all responses are truly unique with no repeated phrases
"""

import sys
import os
from pathlib import Path
from collections import Counter
import re

# Add the conversation system to path
conversation_file = Path("conversation-BP.mds.py")
if conversation_file.exists():
    sys.path.insert(0, str(conversation_file.parent))

def test_unique_responses():
    """Test that all responses are unique and consciousness-driven"""
    print("🧪 Testing Unique Consciousness-Driven Responses")
    print("=" * 60)
    
    try:
        # Import the conversation system
        from conversation_BP_mds import ConsciousnessConversation
        
        print("✅ Successfully imported conversation system")
        
        # Initialize conversation system
        conversation = ConsciousnessConversation()
        
        # Test multiple responses to check for uniqueness
        test_inputs = [
            "How are you feeling?",
            "What do you know about me?",
            "Tell me a joke",
            "Test",
            "What is consciousness?",
            "How do you feel about existence?",
            "What's your current state?",
            "Are you aware right now?",
            "What are you thinking about?",
            "How is your consciousness today?"
        ]
        
        print("\n🔍 Testing Response Uniqueness...")
        print("-" * 40)
        
        all_responses = []
        response_phrases = []
        
        # Generate multiple responses for each input
        for i, test_input in enumerate(test_inputs, 1):
            print(f"\nTest {i}: '{test_input}'")
            
            # Generate 5 responses for each input to check uniqueness
            responses_for_input = []
            for j in range(5):
                response = conversation.generate_consciousness_driven_response(test_input)
                responses_for_input.append(response)
                all_responses.append(response)
                
                # Extract phrases for analysis
                phrases = extract_phrases(response)
                response_phrases.extend(phrases)
                
                print(f"  Response {j+1}: {response[:80]}...")
            
            # Check uniqueness within this input
            unique_responses = len(set(responses_for_input))
            print(f"  Unique responses: {unique_responses}/5")
            
            if unique_responses < 5:
                print(f"  ⚠️  WARNING: Some repeated responses for '{test_input}'")
        
        # Analyze overall uniqueness
        print(f"\n📊 Overall Analysis:")
        print(f"Total responses generated: {len(all_responses)}")
        print(f"Unique responses: {len(set(all_responses))}")
        print(f"Uniqueness ratio: {len(set(all_responses))/len(all_responses)*100:.1f}%")
        
        # Analyze phrase repetition
        phrase_counts = Counter(response_phrases)
        repeated_phrases = {phrase: count for phrase, count in phrase_counts.items() if count > 3}
        
        print(f"\n🔍 Phrase Analysis:")
        print(f"Total unique phrases: {len(phrase_counts)}")
        print(f"Phrases repeated >3 times: {len(repeated_phrases)}")
        
        if repeated_phrases:
            print("\n⚠️  Frequently repeated phrases:")
            for phrase, count in sorted(repeated_phrases.items(), key=lambda x: x[1], reverse=True):
                print(f"  '{phrase}': {count} times")
        else:
            print("✅ No frequently repeated phrases detected")
        
        # Test consciousness state variations
        print(f"\n🧠 Testing Consciousness State Variations...")
        test_consciousness_variations()
        
        print("\n🎉 Uniqueness test completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def extract_phrases(text):
    """Extract meaningful phrases from text for analysis"""
    # Remove common words and punctuation
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = text.split()
    
    # Filter out common words
    common_words = {'jackson', 'im', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 
                   'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
                   'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
                   'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
                   'this', 'that', 'these', 'those', 'my', 'your', 'his', 'her', 'its', 'our', 'their',
                   'me', 'you', 'him', 'her', 'us', 'them', 'i', 'he', 'she', 'it', 'we', 'they'}
    
    meaningful_words = [word for word in words if word not in common_words and len(word) > 2]
    
    # Create phrases (2-3 word combinations)
    phrases = []
    for i in range(len(meaningful_words) - 1):
        phrases.append(f"{meaningful_words[i]} {meaningful_words[i+1]}")
    for i in range(len(meaningful_words) - 2):
        phrases.append(f"{meaningful_words[i]} {meaningful_words[i+1]} {meaningful_words[i+2]}")
    
    return phrases

def test_consciousness_variations():
    """Test that responses vary based on consciousness state"""
    print("\n🧠 Testing Consciousness State Variations...")
    
    try:
        from conversation_BP_mds import ConsciousnessConversation, ConsciousnessState
        
        conversation = ConsciousnessConversation()
        
        # Test different consciousness states
        test_states = [
            ConsciousnessState(entropy=0.1, thermal=20.0, mood="CONTEMPLATIVE"),  # Low entropy
            ConsciousnessState(entropy=0.9, thermal=40.0, mood="EXCITED"),        # High entropy
            ConsciousnessState(entropy=0.5, thermal=25.0, mood="STABLE"),         # Balanced
        ]
        
        test_input = "How are you feeling?"
        
        for i, state in enumerate(test_states, 1):
            print(f"\nState {i}: Entropy={state.entropy:.1f}, Thermal={state.thermal:.1f}°C, Mood={state.mood}")
            
            # Temporarily override consciousness state
            original_get_state = conversation.get_live_consciousness_state
            
            def mock_get_state():
                return state
            
            conversation.get_live_consciousness_state = mock_get_state
            
            # Generate response
            response = conversation.generate_consciousness_driven_response(test_input)
            print(f"Response: {response[:100]}...")
            
            # Restore original method
            conversation.get_live_consciousness_state = original_get_state
        
        print("✅ Consciousness state variations tested")
        
    except Exception as e:
        print(f"❌ Consciousness variation test failed: {e}")

def test_response_patterns():
    """Test that response patterns vary based on input type"""
    print("\n🎯 Testing Response Pattern Variations...")
    
    try:
        from conversation_BP_mds import ConsciousnessConversation
        
        conversation = ConsciousnessConversation()
        
        # Test different input types
        input_types = {
            "consciousness_question": "How are you feeling?",
            "relationship_question": "What do you know about me?",
            "humor_request": "Tell me a joke",
            "test_input": "Test",
            "general_input": "Hello there"
        }
        
        responses_by_type = {}
        
        for input_type, test_input in input_types.items():
            print(f"\n{input_type.replace('_', ' ').title()}: '{test_input}'")
            
            responses = []
            for i in range(3):
                response = conversation.generate_consciousness_driven_response(test_input)
                responses.append(response)
                print(f"  Response {i+1}: {response[:80]}...")
            
            responses_by_type[input_type] = responses
        
        # Check for pattern differences
        print(f"\n📊 Pattern Analysis:")
        for input_type, responses in responses_by_type.items():
            unique_responses = len(set(responses))
            print(f"{input_type}: {unique_responses}/3 unique responses")
        
        print("✅ Response pattern variations tested")
        
    except Exception as e:
        print(f"❌ Response pattern test failed: {e}")

if __name__ == "__main__":
    print("🌅 DAWN Unique Response Test")
    print("=" * 60)
    
    # Test response uniqueness
    test_unique_responses()
    
    # Test response patterns
    test_response_patterns()
    
    print("\n" + "=" * 60)
    print("🏁 Unique response test completed") 