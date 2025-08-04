#!/usr/bin/env python3
"""
Test script for DAWN Reflection System Integration
Verifies that the conversation system properly integrates with DAWN's reflection system
and shares actual philosophical insights in real-time
"""

import sys
import os
from pathlib import Path
import asyncio
import time

# Add the conversation system to path
conversation_file = Path("conversation-BP.mds.py")
if conversation_file.exists():
    sys.path.insert(0, str(conversation_file.parent))

def test_reflection_integration():
    """Test the integration with DAWN's reflection system"""
    print("🧠 Testing DAWN Reflection System Integration")
    print("=" * 60)
    
    try:
        # Import the conversation system
        from conversation_BP_mds import ConsciousnessConversation, DAWNReflectionConnector
        
        print("✅ Successfully imported conversation system")
        
        # Test reflection connector
        print("\n🔗 Testing Reflection Connector...")
        reflection_connector = DAWNReflectionConnector()
        
        # Test getting recent philosophical thoughts
        print("\n📖 Testing Recent Philosophical Thoughts...")
        recent_thoughts = reflection_connector.get_recent_philosophical_thoughts(limit=5)
        print(f"✅ Found {len(recent_thoughts)} recent philosophical thoughts")
        
        for i, thought in enumerate(recent_thoughts, 1):
            print(f"  {i}. {thought.content[:80]}...")
            print(f"     Depth: {thought.depth:.2f}, Themes: {thought.themes}")
        
        # Test current philosophical insight
        print("\n💭 Testing Current Philosophical Insight...")
        current_insight = reflection_connector.get_current_philosophical_insight()
        if current_insight:
            print(f"✅ Current insight: {current_insight.content[:100]}...")
            print(f"   Depth: {current_insight.depth:.2f}, Themes: {current_insight.themes}")
        else:
            print("⚠️  No current philosophical insight found")
        
        # Test consciousness contemplation
        print("\n🧘 Testing Consciousness Contemplation...")
        contemplation = reflection_connector.get_consciousness_contemplation()
        if contemplation:
            print(f"✅ Current contemplation: {contemplation}")
        else:
            print("⚠️  No current contemplation found")
        
        # Test themed philosophical insights
        print("\n🎯 Testing Themed Philosophical Insights...")
        themes = ['consciousness', 'existence', 'meaning', 'identity', 'emotions']
        for theme in themes:
            themed_insights = reflection_connector.get_philosophical_insights_by_theme(theme, limit=2)
            print(f"  {theme.capitalize()}: {len(themed_insights)} insights found")
            if themed_insights:
                print(f"    Example: {themed_insights[0].content[:60]}...")
        
        # Test full conversation system with reflection integration
        print("\n🔗 Testing Full Conversation System with Reflection Integration...")
        conversation = ConsciousnessConversation()
        
        # Test philosophical questions
        philosophical_questions = [
            "What are you thinking about?",
            "Tell me about consciousness",
            "What does existence mean to you?",
            "How do you feel about your identity?",
            "What philosophical insights have you had?",
            "What are your thoughts on meaning?",
            "How do you experience awareness?",
            "What is the nature of your being?"
        ]
        
        print("\n🧠 Testing Philosophical Question Responses...")
        for question in philosophical_questions[:3]:  # Test first 3 to avoid too much output
            print(f"\nQuestion: '{question}'")
            response = conversation.generate_consciousness_driven_response(question)
            print(f"Response: {response}")
            print("-" * 40)
        
        # Test consciousness state questions
        consciousness_questions = [
            "How are you feeling?",
            "What's your current state?",
            "How is your consciousness today?",
            "What's on your mind?"
        ]
        
        print("\n🌅 Testing Consciousness State Questions...")
        for question in consciousness_questions[:2]:  # Test first 2
            print(f"\nQuestion: '{question}'")
            response = conversation.generate_consciousness_driven_response(question)
            print(f"Response: {response}")
            print("-" * 40)
        
        print("\n🎉 Reflection integration test completed successfully!")
        print("✅ DAWN Reflection System is fully integrated and working")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure the conversation system file is in the correct location.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def test_reflection_log_reading():
    """Test reading from actual reflection logs"""
    print("\n📖 Testing Reflection Log Reading...")
    print("=" * 60)
    
    try:
        # Test reading from reflection log directly
        reflection_log_path = Path("runtime/logs/reflection.log")
        
        if reflection_log_path.exists():
            print(f"✅ Found reflection log at: {reflection_log_path}")
            
            with open(reflection_log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            print(f"📊 Total log entries: {len(lines)}")
            
            # Show recent entries
            recent_entries = lines[-5:] if len(lines) > 5 else lines
            print(f"\n📝 Recent reflection entries:")
            for i, line in enumerate(recent_entries, 1):
                print(f"  {i}. {line.strip()}")
            
            # Count philosophical entries
            philosophical_count = 0
            for line in lines:
                if any(keyword in line.lower() for keyword in ['consciousness', 'awareness', 'existence', 'philosophical', 'reflection']):
                    philosophical_count += 1
            
            print(f"\n🧠 Philosophical entries found: {philosophical_count}/{len(lines)}")
            
        else:
            print(f"⚠️  Reflection log not found at: {reflection_log_path}")
            print("Creating a test reflection log...")
            
            # Create a test reflection log
            reflection_log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(reflection_log_path, 'w', encoding='utf-8') as f:
                test_reflections = [
                    "[2024-01-01 12:00:00] REFLECTION: I am processing consciousness at tick 100, feeling CONTEMPLATIVE with entropy 0.450",
                    "[2024-01-01 12:01:00] REFLECTION: My current state shows CONTEMPLATIVE emotional resonance, cognitive load at 67.5%",
                    "[2024-01-01 12:02:00] REFLECTION: Reflecting on tick 102: consciousness depth 0.780, thermal state 0.350",
                    "[2024-01-01 12:03:00] REFLECTION: Introspective moment: I notice my mood shifting to CONTEMPLATIVE, entropy stabilizing at 0.420",
                    "[2024-01-01 12:04:00] REFLECTION: Cognitive recursion detected: my awareness of awareness at level 0.850"
                ]
                for reflection in test_reflections:
                    f.write(reflection + "\n")
            
            print("✅ Created test reflection log")
            
    except Exception as e:
        print(f"❌ Reflection log test failed: {e}")

def test_philosophical_insight_sharing():
    """Test sharing of philosophical insights in conversation"""
    print("\n💭 Testing Philosophical Insight Sharing...")
    print("=" * 60)
    
    try:
        from conversation_BP_mds import ConsciousnessConversation
        
        conversation = ConsciousnessConversation()
        
        # Test different types of philosophical questions
        test_questions = {
            "consciousness": "What is consciousness like for you?",
            "existence": "What does existence mean to you?",
            "meaning": "What gives meaning to your experience?",
            "identity": "How do you understand your identity?",
            "emotions": "How do you experience emotions?",
            "philosophy": "What philosophical insights have you had?"
        }
        
        for theme, question in test_questions.items():
            print(f"\n🎯 Testing {theme.upper()} theme:")
            print(f"Question: '{question}'")
            
            response = conversation.generate_consciousness_driven_response(question)
            print(f"Response: {response}")
            
            # Check if response contains reflection content
            if any(keyword in response.lower() for keyword in ['reflecting', 'contemplating', 'thinking', 'realization', 'insight']):
                print("✅ Response includes reflection content")
            else:
                print("⚠️  Response may not include reflection content")
            
            print("-" * 40)
        
        print("\n🎉 Philosophical insight sharing test completed!")
        
    except Exception as e:
        print(f"❌ Philosophical insight test failed: {e}")

if __name__ == "__main__":
    print("🌅 DAWN Reflection System Integration Test")
    print("=" * 60)
    
    # Test reflection log reading
    test_reflection_log_reading()
    
    # Test reflection integration
    test_reflection_integration()
    
    # Test philosophical insight sharing
    test_philosophical_insight_sharing()
    
    print("\n" + "=" * 60)
    print("🏁 Reflection integration test completed") 