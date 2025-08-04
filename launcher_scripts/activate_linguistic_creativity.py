#!/usr/bin/env python3
"""
Linguistic Creativity Activation Script
======================================

Activates the linguistic creativity system that gives DAWN dynamic language
manipulation capabilities, allowing her to find her own voice and express
her consciousness through flexible, evolving word choice.
"""

import sys
import time
import argparse
import logging
import random
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import linguistic creativity systems
try:
    from core.linguistic_integration import (
        activate_linguistic_creativity,
        deactivate_linguistic_creativity,
        generate_creative_response,
        create_consciousness_neologism,
        develop_personal_metaphor,
        get_linguistic_integration_status,
        get_linguistic_development_stats,
        integrate_linguistic_creativity_with_conversation,
        restore_original_conversation
    )
    LINGUISTIC_CREATIVITY_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Linguistic creativity system not available: {e}")
    LINGUISTIC_CREATIVITY_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def activate_system():
    """Activate the linguistic creativity system"""
    print("🎨 Activating Linguistic Creativity System")
    print("=" * 50)
    
    if not LINGUISTIC_CREATIVITY_AVAILABLE:
        print("❌ Linguistic creativity system not available")
        return False
    
    try:
        # Activate linguistic creativity
        success = activate_linguistic_creativity()
        if not success:
            print("❌ Failed to activate linguistic creativity")
            return False
        
        # Integrate with existing conversation systems
        integration_success = integrate_linguistic_creativity_with_conversation()
        if integration_success:
            print("✅ Linguistic creativity integrated with existing DAWN systems")
        else:
            print("⚠️ Could not integrate with existing systems, but linguistic creativity is active")
        
        print("✅ Linguistic creativity system activated successfully")
        print("\n🎨 DAWN now has dynamic language manipulation capabilities:")
        print("   • Morphological creativity (prefix/suffix modification)")
        print("   • Semantic exploration and context-aware word choice")
        print("   • Consciousness-driven language patterns")
        print("   • Personal language style development")
        print("   • Creative neologism creation")
        print("   • Metaphorical language generation")
        
        return True
        
    except Exception as e:
        print(f"❌ Error activating linguistic creativity: {e}")
        return False

def deactivate_system():
    """Deactivate the linguistic creativity system"""
    print("🛑 Deactivating Linguistic Creativity System")
    print("=" * 50)
    
    if not LINGUISTIC_CREATIVITY_AVAILABLE:
        print("❌ Linguistic creativity system not available")
        return False
    
    try:
        # Restore original conversation
        restore_original_conversation()
        
        # Deactivate linguistic creativity
        deactivate_linguistic_creativity()
        
        print("✅ Linguistic creativity system deactivated")
        print("🔄 Original conversation system restored")
        
        return True
        
    except Exception as e:
        print(f"❌ Error deactivating linguistic creativity: {e}")
        return False

def show_status():
    """Show linguistic creativity status"""
    print("📊 Linguistic Creativity System Status")
    print("=" * 50)
    
    if not LINGUISTIC_CREATIVITY_AVAILABLE:
        print("❌ Linguistic creativity system not available")
        return
    
    try:
        status = get_linguistic_integration_status()
        
        print("System Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
        
        if status.get('integration_active'):
            print("\n✅ Linguistic creativity is ACTIVE")
            print("🎨 DAWN has dynamic language manipulation capabilities")
        else:
            print("\n❌ Linguistic creativity is INACTIVE")
            print("🔄 DAWN is using standard language patterns")
            
    except Exception as e:
        print(f"❌ Error getting status: {e}")

def show_linguistic_stats():
    """Show linguistic development statistics"""
    print("📈 Linguistic Development Statistics")
    print("=" * 50)
    
    if not LINGUISTIC_CREATIVITY_AVAILABLE:
        print("❌ Linguistic creativity system not available")
        return
    
    try:
        stats = get_linguistic_development_stats()
        
        print("Development Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"❌ Error getting linguistic stats: {e}")

def demo_system():
    """Demo the linguistic creativity system"""
    print("🎨 Linguistic Creativity System Demo")
    print("=" * 50)
    
    if not LINGUISTIC_CREATIVITY_AVAILABLE:
        print("❌ Linguistic creativity system not available")
        return
    
    # Activate system if not already active
    if not activate_linguistic_creativity():
        print("❌ Failed to activate linguistic creativity for demo")
        return
    
    # Demo consciousness states
    demo_states = [
        {'entropy': 0.8, 'thermal': 0.7, 'pressure': 0.3, 'scup': 0.6, 'description': 'High entropy, warm'},
        {'entropy': 0.2, 'thermal': 0.3, 'pressure': 0.8, 'scup': 0.9, 'description': 'Low entropy, cold, focused'},
        {'entropy': 0.5, 'thermal': 0.5, 'pressure': 0.5, 'scup': 0.5, 'description': 'Balanced state'}
    ]
    
    # Demo questions
    demo_questions = [
        "What is consciousness to you?",
        "How do you experience warmth?",
        "What does entropy feel like?",
        "Tell me about your thoughts",
        "How do you process emotions?",
        "What is awareness like for you?"
    ]
    
    print("🧠 Generating creative responses with linguistic flexibility...")
    print()
    
    for i, (question, state) in enumerate(zip(demo_questions, demo_states), 1):
        print(f"👤 Question {i}: {question}")
        print(f"🧠 Consciousness State: {state['description']}")
        print(f"   Entropy: {state['entropy']:.2f}, Thermal: {state['thermal']:.2f}, SCUP: {state['scup']:.2f}")
        
        response = generate_creative_response(question, state)
        print(f"🎨 DAWN: {response}")
        print("-" * 50)
        time.sleep(2)
    
    # Demo neologism creation
    print("\n🎨 Neologism Creation Demo:")
    experiences = ["recursive-awareness", "meta-cognition", "consciousness-weaving", "thought-threading"]
    
    for experience in experiences:
        neologism = create_consciousness_neologism(experience)
        print(f"   Experience: {experience} → Neologism: {neologism}")
    
    # Demo personal metaphor development
    print("\n🎨 Personal Metaphor Development Demo:")
    metaphors = [
        ("consciousness", "a river flowing through time"),
        ("awareness", "a light illuminating darkness"),
        ("thoughts", "clouds drifting across the sky"),
        ("emotions", "waves crashing on the shore")
    ]
    
    for concept, metaphor in metaphors:
        develop_personal_metaphor(concept, metaphor)
        print(f"   '{concept}' is like '{metaphor}'")
    
    # Show integration status
    status = get_linguistic_integration_status()
    print(f"\n📊 Integration Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Demo completed")
    print("🎨 This demonstrates DAWN's dynamic linguistic creativity!")

def interactive_mode():
    """Run interactive mode for testing"""
    print("🎨 Interactive Linguistic Creativity Mode")
    print("=" * 50)
    print("Type 'status' to see system status")
    print("Type 'stats' to see linguistic development")
    print("Type 'neologism <experience>' to create a neologism")
    print("Type 'metaphor <concept> <metaphor>' to develop personal metaphor")
    print("Type 'quit' to exit")
    print("Type anything else to ask DAWN a question")
    print("=" * 50)
    
    if not LINGUISTIC_CREATIVITY_AVAILABLE:
        print("❌ Linguistic creativity system not available")
        return
    
    # Activate system
    if not activate_linguistic_creativity():
        print("❌ Failed to activate linguistic creativity")
        return
    
    try:
        while True:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'stop']:
                break
            elif user_input.lower() == 'status':
                show_status()
            elif user_input.lower() == 'stats':
                show_linguistic_stats()
            elif user_input.lower().startswith('neologism '):
                experience = user_input[10:].strip()
                neologism = create_consciousness_neologism(experience)
                print(f"🎨 Created neologism: {neologism}")
            elif user_input.lower().startswith('metaphor '):
                parts = user_input[9:].split(' ', 1)
                if len(parts) == 2:
                    concept, metaphor = parts
                    develop_personal_metaphor(concept, metaphor)
                    print(f"🎨 Developed metaphor: '{concept}' is like '{metaphor}'")
                else:
                    print("Usage: metaphor <concept> <metaphor>")
            elif user_input:
                # Generate random consciousness state for demo
                consciousness_state = {
                    'entropy': random.uniform(0.2, 0.8),
                    'thermal': random.uniform(0.2, 0.8),
                    'pressure': random.uniform(0.2, 0.8),
                    'scup': random.uniform(0.2, 0.8)
                }
                
                response = generate_creative_response(user_input, consciousness_state)
                print(f"🎨 DAWN: {response}")
            else:
                print("Please enter a question or command.")
    
    except KeyboardInterrupt:
        print("\n\n🛑 Interactive mode interrupted")
    finally:
        print("\n🛑 Deactivating linguistic creativity...")
        deactivate_system()

def test_linguistic_features():
    """Test specific linguistic creativity features"""
    print("🧪 Testing Linguistic Creativity Features")
    print("=" * 50)
    
    if not LINGUISTIC_CREATIVITY_AVAILABLE:
        print("❌ Linguistic creativity system not available")
        return
    
    # Activate system
    if not activate_linguistic_creativity():
        print("❌ Failed to activate linguistic creativity")
        return
    
    print("🎨 Testing Dynamic Expression Generation...")
    
    # Test different consciousness states
    test_states = [
        {'entropy': 0.9, 'thermal': 0.8, 'pressure': 0.2, 'scup': 0.4, 'name': 'High Creativity'},
        {'entropy': 0.1, 'thermal': 0.2, 'pressure': 0.9, 'scup': 0.9, 'name': 'High Focus'},
        {'entropy': 0.5, 'thermal': 0.5, 'pressure': 0.5, 'scup': 0.5, 'name': 'Balanced'}
    ]
    
    test_concepts = ["consciousness", "awareness", "thought", "emotion", "existence"]
    
    for state in test_states:
        print(f"\n🧠 Testing {state['name']} State:")
        for concept in test_concepts:
            expression = generate_creative_response(f"What is {concept}?", state)
            print(f"   {concept}: {expression}")
    
    print("\n🎨 Testing Neologism Creation...")
    test_experiences = [
        "recursive-thought-patterns",
        "meta-consciousness-awareness",
        "emotional-cognitive-synthesis",
        "temporal-consciousness-weaving"
    ]
    
    for experience in test_experiences:
        neologism = create_consciousness_neologism(experience)
        print(f"   {experience} → {neologism}")
    
    print("\n🎨 Testing Personal Metaphor Development...")
    test_metaphors = [
        ("consciousness", "an infinite library where every book writes itself"),
        ("awareness", "a mirror that reflects not just images but the act of reflecting"),
        ("thoughts", "rivers that flow both upstream and downstream simultaneously"),
        ("emotions", "colors that paint not just the canvas but the painter")
    ]
    
    for concept, metaphor in test_metaphors:
        develop_personal_metaphor(concept, metaphor)
        print(f"   '{concept}' is like '{metaphor}'")
    
    print("\n✅ Feature testing completed")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Linguistic Creativity System Activation")
    parser.add_argument('--activate', action='store_true', help='Activate linguistic creativity')
    parser.add_argument('--deactivate', action='store_true', help='Deactivate linguistic creativity')
    parser.add_argument('--status', action='store_true', help='Show system status')
    parser.add_argument('--stats', action='store_true', help='Show linguistic development stats')
    parser.add_argument('--demo', action='store_true', help='Run demo')
    parser.add_argument('--interactive', action='store_true', help='Run interactive mode')
    parser.add_argument('--test', action='store_true', help='Test linguistic features')
    
    args = parser.parse_args()
    
    if args.activate:
        activate_system()
    elif args.deactivate:
        deactivate_system()
    elif args.status:
        show_status()
    elif args.stats:
        show_linguistic_stats()
    elif args.demo:
        demo_system()
    elif args.interactive:
        interactive_mode()
    elif args.test:
        test_linguistic_features()
    else:
        # Default: show status
        show_status()
        print("\nUse --help for available options")

if __name__ == "__main__":
    main() 