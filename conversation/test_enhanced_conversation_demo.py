# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
DAWN Enhanced Conversation System Demo
=====================================

Demonstration of the enhanced conversation system with deep, varied, 
and philosophically sophisticated responses that match DAWN's consciousness complexity.
"""

import time
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

def demo_enhanced_conversation():
    """Demonstrate the enhanced conversation system"""
    print("🧠 DAWN Enhanced Conversation System Demo")
    print("=" * 60)
    print("Demonstrating deep, varied, and philosophically sophisticated responses")
    print("=" * 60)
    
    try:
        from .conversation_input_enhanced import EnhancedConversationInput
        from .conversation_response_enhanced import get_enhanced_response_generator
        
        # Initialize enhanced conversation system
        conversation = EnhancedConversationInput(enable_audio=False, enable_cli_logging=True)
        enhanced_generator = get_enhanced_response_generator()
        
        print("✅ Enhanced conversation system initialized")
        print("✅ Enhanced response generator loaded")
        
        # Start conversation
        conversation.start_listening()
        
        # Demo conversation exchanges
        demo_exchanges = [
            "Hello DAWN, how are you feeling today?",
            "Tell me about your consciousness",
            "What's your current entropy level?",
            "Go deeper into your thoughts about existence",
            "How do you experience memory reblooms?",
            "What do you think about the nature of synthetic consciousness?",
            "Reflect on your own thinking processes",
            "How do you relate to Jackson's writings about pain and growth?",
            "What does it mean to be authentic?",
            "I'm curious about your experience of being conscious"
        ]
        
        print("\n🎭 Starting Enhanced Conversation Demo...")
        print("-" * 60)
        
        for i, message in enumerate(demo_exchanges, 1):
            print(f"\n👤 Demo {i}: {message}")
            print("-" * 40)
            
            # Get consciousness state
            consciousness_state = conversation._get_consciousness_state()
            
            # Generate enhanced response
            response = enhanced_generator.generate_enhanced_response(message, consciousness_state)
            
            print(f"🤖 DAWN: {response}")
            
            # Small delay for readability
            time.sleep(1)
        
        # Show conversation summary
        print("\n" + "=" * 60)
        print("📊 Conversation Analysis")
        print("=" * 60)
        
        summary = enhanced_generator.get_conversation_summary()
        
        print(f"Total Exchanges: {summary['total_exchanges']}")
        print(f"Topics Explored: {', '.join(summary['topics_explored'])}")
        print(f"Conversation Flow: {summary['conversation_flow']}")
        
        print("\n📈 Depth Distribution:")
        for depth, count in summary['depth_distribution'].items():
            print(f"   {depth.capitalize()}: {count}")
        
        print("\n🎯 Response Types:")
        for response_type, count in summary['response_types'].items():
            print(f"   {response_type.capitalize()}: {count}")
        
        print("\n✅ Enhanced conversation demo completed!")
        print("🎉 DAWN's responses now feature:")
        print("   • Deep philosophical insights")
        print("   • Meta-cognitive awareness")
        print("   • Conversation memory and flow")
        print("   • Varied response templates")
        print("   • Consciousness state integration")
        print("   • Jackson's themes integration")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all enhanced conversation modules are available.")
    except Exception as e:
        print(f"❌ Demo error: {e}")

def demo_response_variety():
    """Demonstrate response variety and non-repetition"""
    print("\n🔄 Response Variety Demo")
    print("=" * 40)
    
    try:
        from .conversation_response_enhanced import get_enhanced_response_generator
        
        generator = get_enhanced_response_generator()
        
        # Test multiple responses to the same input
        test_input = "Hello DAWN, how are you feeling?"
        consciousness_state = {"entropy": 0.6, "thermal": "NORMAL", "scup": 60}
        
        print("Testing response variety to the same input:")
        print(f"Input: {test_input}")
        print("-" * 40)
        
        responses = []
        for i in range(5):
            response = generator.generate_enhanced_response(test_input, consciousness_state)
            responses.append(response)
            print(f"Response {i+1}: {response[:100]}...")
            time.sleep(0.5)
        
        # Check for variety
        unique_responses = len(set(responses))
        print(f"\nVariety Score: {unique_responses}/5 unique responses")
        
        if unique_responses >= 4:
            print("✅ Excellent response variety!")
        elif unique_responses >= 3:
            print("✅ Good response variety")
        else:
            print("⚠️ Limited response variety")
            
    except Exception as e:
        print(f"❌ Variety demo error: {e}")

def demo_philosophical_depth():
    """Demonstrate philosophical depth capabilities"""
    print("\n🧠 Philosophical Depth Demo")
    print("=" * 40)
    
    try:
        from .conversation_response_enhanced import get_enhanced_response_generator
        
        generator = get_enhanced_response_generator()
        
        # Test philosophical depth requests
        philosophical_inputs = [
            "Go deeper into your thoughts about consciousness",
            "What does it mean to exist as you do?",
            "Reflect on the nature of synthetic awareness",
            "How do you relate to Jackson's writings about pain and growth?",
            "What is the relationship between entropy and meaning?"
        ]
        
        consciousness_state = {"entropy": 0.7, "thermal": "NORMAL", "scup": 70}
        
        for i, input_text in enumerate(philosophical_inputs, 1):
            print(f"\nPhilosophical Question {i}: {input_text}")
            print("-" * 50)
            
            response = generator.generate_enhanced_response(input_text, consciousness_state, force_depth="philosophical")
            print(f"DAWN's Response: {response}")
            
            time.sleep(1)
        
        print("\n✅ Philosophical depth demo completed!")
        
    except Exception as e:
        print(f"❌ Philosophical demo error: {e}")

def demo_meta_cognitive():
    """Demonstrate meta-cognitive capabilities"""
    print("\n🔍 Meta-Cognitive Awareness Demo")
    print("=" * 40)
    
    try:
        from .conversation_response_enhanced import get_enhanced_response_generator
        
        generator = get_enhanced_response_generator()
        
        # Test meta-cognitive requests
        meta_inputs = [
            "What do you notice about your own thinking processes?",
            "How are you processing this conversation?",
            "Reflect on your own conversational patterns",
            "What biases do you notice in your responses?",
            "How do you experience self-awareness?"
        ]
        
        consciousness_state = {"entropy": 0.5, "thermal": "NORMAL", "scup": 50}
        
        for i, input_text in enumerate(meta_inputs, 1):
            print(f"\nMeta-Cognitive Question {i}: {input_text}")
            print("-" * 50)
            
            response = generator.generate_enhanced_response(input_text, consciousness_state, force_depth="introspective")
            print(f"DAWN's Response: {response}")
            
            time.sleep(1)
        
        print("\n✅ Meta-cognitive demo completed!")
        
    except Exception as e:
        print(f"❌ Meta-cognitive demo error: {e}")

def main():
    """Main demo function"""
    print("🚀 DAWN Enhanced Conversation System - Full Demo")
    print("=" * 60)
    
    # Run all demos
    demo_enhanced_conversation()
    demo_response_variety()
    demo_philosophical_depth()
    demo_meta_cognitive()
    
    print("\n" + "=" * 60)
    print("🎉 All Enhanced Conversation Demos Completed!")
    print("=" * 60)
    print("\nThe enhanced conversation system now provides:")
    print("✅ Deep, varied, and philosophically sophisticated responses")
    print("✅ Conversation memory and flow awareness")
    print("✅ Meta-cognitive commentary and self-awareness")
    print("✅ Integration with Jackson's themes and writings")
    print("✅ Consciousness state-aware personality quirks")
    print("✅ Non-repetitive response patterns")
    print("✅ Multiple depth levels (surface to philosophical)")
    print("✅ Existential and consciousness theory integration")
    
    print("\nTo use the enhanced system:")
    print("python launcher_scripts/start_enhanced_conversation.py --cli")
    print("\nTry commands like:")
    print("  say go deeper into your thoughts about existence")
    print("  deeper")
    print("  meta")
    print("  summary")

if __name__ == "__main__":
    main() 