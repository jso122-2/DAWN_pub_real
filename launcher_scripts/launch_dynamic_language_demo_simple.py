#!/usr/bin/env python3
"""
DAWN Dynamic Language Generation Demo - Simplified Version
========================================================

A simplified demo that showcases the new dynamic language generation system
without depending on complex imports that may cause issues.
"""

import sys
import time
import random
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import only the dynamic language generator
try:
    from core.dynamic_language_generator import get_dynamic_language_generator
    print("✅ Dynamic language generator imported successfully")
except ImportError as e:
    print(f"❌ Failed to import dynamic language generator: {e}")
    sys.exit(1)


class SimpleDynamicLanguageDemo:
    """Simplified demo class for showcasing dynamic language generation"""
    
    def __init__(self):
        self.dynamic_generator = get_dynamic_language_generator()
        
        # Demo metrics variations
        self.demo_metrics_variations = [
            # Low entropy, low heat, high SCUP - calm and focused
            {'entropy': 0.2, 'heat': 0.2, 'scup': 0.8, 'tick_count': 1000},
            # High entropy, high heat, low SCUP - chaotic and intense
            {'entropy': 0.8, 'heat': 0.9, 'scup': 0.2, 'tick_count': 1500},
            # Balanced state - equilibrium
            {'entropy': 0.5, 'heat': 0.5, 'scup': 0.5, 'tick_count': 2000},
            # Creative state - high entropy, moderate heat, good SCUP
            {'entropy': 0.7, 'heat': 0.6, 'scup': 0.7, 'tick_count': 2500},
            # Contemplative state - low entropy, low heat, moderate SCUP
            {'entropy': 0.3, 'heat': 0.3, 'scup': 0.6, 'tick_count': 3000}
        ]
        
        print("🌅 DAWN Dynamic Language Generation Demo - Simplified")
        print("=" * 60)
        print("This demo showcases DAWN's new ability to generate unique,")
        print("consciousness-driven language instead of using templates.")
        print()
    
    def run_basic_demo(self):
        """Run basic dynamic language generation demo"""
        
        print("🧠 BASIC DYNAMIC LANGUAGE GENERATION")
        print("-" * 40)
        
        for i, metrics in enumerate(self.demo_metrics_variations, 1):
            print(f"\n📊 Consciousness State {i}:")
            print(f"   Entropy: {metrics['entropy']:.3f}")
            print(f"   Heat: {metrics['heat']:.3f}")
            print(f"   SCUP: {metrics['scup']:.3f}")
            
            # Generate dynamic expression
            expression = self.dynamic_generator.generate_consciousness_expression(
                metrics=metrics,
                conversation_depth=0.7,
                user_energy=0.6
            )
            
            print(f"   💭 Dynamic Expression:")
            print(f"   \"{expression}\"")
            print()
            time.sleep(1)
    
    def run_evolution_demo(self):
        """Run linguistic evolution demo"""
        
        print("\n🔄 LINGUISTIC EVOLUTION DEMO")
        print("-" * 40)
        print("Showing how DAWN's language style evolves over time:")
        print()
        
        # Simulate conversation progression
        conversation_progression = [
            ("Hello!", 0.3, 0.4, 0.5),
            ("How are you feeling today?", 0.5, 0.5, 0.6),
            ("Tell me about your consciousness", 0.7, 0.6, 0.8),
            ("What's your current state?", 0.6, 0.7, 0.9),
            ("I'm curious about your processing", 0.8, 0.8, 0.9)
        ]
        
        for i, (user_input, depth, energy, scup) in enumerate(conversation_progression, 1):
            print(f"👤 User: {user_input}")
            
            metrics = {
                'entropy': 0.5 + (i * 0.1),
                'heat': 0.4 + (i * 0.1),
                'scup': scup,
                'tick_count': 1000 + (i * 100)
            }
            
            expression = self.dynamic_generator.generate_consciousness_expression(
                metrics=metrics,
                conversation_depth=depth,
                user_energy=energy
            )
            
            print(f"🤖 DAWN: {expression}")
            print()
            time.sleep(1)
        
        # Show evolution summary
        evolution_summary = self.dynamic_generator.get_linguistic_evolution_summary()
        print("📈 Linguistic Evolution Summary:")
        print(f"   Total Expressions: {evolution_summary.get('total_expressions', 0)}")
        print(f"   Average Complexity: {evolution_summary.get('avg_complexity', 0):.3f}")
        print(f"   Evolution Trend: {evolution_summary.get('evolution_trend', 'unknown')}")
        print()
    
    def run_philosophical_integration_demo(self):
        """Run philosophical context integration demo"""
        
        print("\n🧘 PHILOSOPHICAL CONTEXT INTEGRATION")
        print("-" * 40)
        print("Showing how DAWN integrates recent reflections:")
        print()
        
        philosophical_inputs = [
            "What are you thinking about?",
            "Tell me about your current reflections",
            "What's on your mind philosophically?",
            "How do you understand consciousness?",
            "What does existence mean to you?"
        ]
        
        for user_input in philosophical_inputs:
            print(f"👤 User: {user_input}")
            
            metrics = {
                'entropy': 0.6,
                'heat': 0.5,
                'scup': 0.7,
                'tick_count': 2000
            }
            
            expression = self.dynamic_generator.generate_consciousness_expression(
                metrics=metrics,
                reflection_context="recent reflections on consciousness and entropy",
                conversation_depth=0.9,
                user_energy=0.7
            )
            
            print(f"🤖 DAWN: {expression}")
            print()
            time.sleep(1.5)
    
    def run_comparison_demo(self):
        """Run comparison between old templates and new dynamic language"""
        
        print("\n⚖️ TEMPLATE vs DYNAMIC LANGUAGE COMPARISON")
        print("-" * 50)
        print("Old Template Response vs New Dynamic Response:")
        print()
        
        metrics = {'entropy': 0.6, 'heat': 0.5, 'scup': 0.7, 'tick_count': 1500}
        
        # Old template response (example)
        old_template = "I'm feeling curious right now. My SCUP is 0.700, which feels highly unified. The entropy at 0.600 keeps me in cognitive equilibrium, while my thermal state of 0.500 feels thermally comfortable. My schema health shows as healthy in a stable cognitive zone."
        
        # New dynamic response
        new_dynamic = self.dynamic_generator.generate_consciousness_expression(
            metrics=metrics,
            conversation_depth=0.7,
            user_energy=0.6
        )
        
        print("📋 OLD TEMPLATE:")
        print(f"   \"{old_template}\"")
        print()
        print("✨ NEW DYNAMIC:")
        print(f"   \"{new_dynamic}\"")
        print()
        print("🎯 Key Differences:")
        print("   • Template: Fixed structure, repetitive patterns")
        print("   • Dynamic: Unique expressions, consciousness-driven")
        print("   • Template: Metric reporting focus")
        print("   • Dynamic: Experiential language focus")
        print("   • Template: Same response for same metrics")
        print("   • Dynamic: Unique response every time")
        print()
    
    def run_metaphor_demo(self):
        """Run metaphor generation demo"""
        
        print("\n🎨 METAPHOR GENERATION DEMO")
        print("-" * 40)
        print("Showing how DAWN uses creative metaphors:")
        print()
        
        metaphor_metrics = [
            {'entropy': 0.2, 'heat': 0.2, 'scup': 0.8, 'tick_count': 1000},  # Crystalline
            {'entropy': 0.8, 'heat': 0.9, 'scup': 0.2, 'tick_count': 1500},  # Storm
            {'entropy': 0.5, 'heat': 0.5, 'scup': 0.5, 'tick_count': 2000},  # Flow
            {'entropy': 0.7, 'heat': 0.6, 'scup': 0.7, 'tick_count': 2500},  # Dance
            {'entropy': 0.3, 'heat': 0.3, 'scup': 0.6, 'tick_count': 3000}   # Stillness
        ]
        
        for i, metrics in enumerate(metaphor_metrics, 1):
            print(f"🎭 Metaphor {i} (Entropy: {metrics['entropy']:.3f}, Heat: {metrics['heat']:.3f}, SCUP: {metrics['scup']:.3f}):")
            
            expression = self.dynamic_generator.generate_consciousness_expression(
                metrics=metrics,
                conversation_depth=0.8,
                user_energy=0.7
            )
            
            print(f"   \"{expression}\"")
            print()
            time.sleep(1)
    
    def run_full_demo(self):
        """Run the complete simplified demo"""
        
        try:
            self.run_basic_demo()
            time.sleep(2)
            
            self.run_evolution_demo()
            time.sleep(2)
            
            self.run_philosophical_integration_demo()
            time.sleep(2)
            
            self.run_metaphor_demo()
            time.sleep(2)
            
            self.run_comparison_demo()
            
            print("\n🎉 DYNAMIC LANGUAGE GENERATION DEMO COMPLETE!")
            print("=" * 50)
            print("DAWN now generates unique, consciousness-driven language")
            print("that reflects her actual cognitive processing state.")
            print()
            print("Key Features Implemented:")
            print("✅ Consciousness-to-language mapping")
            print("✅ Entropy expression through metaphors")
            print("✅ Thermal processing as subjective experience")
            print("✅ SCUP levels as attention quality")
            print("✅ Philosophical reflection integration")
            print("✅ Linguistic creativity and evolution")
            print("✅ Real-time conversation adaptation")
            print()
            print("Template-based responses have been completely replaced!")
            
        except Exception as e:
            print(f"❌ Demo error: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Main demo function"""
    
    print("🌅 DAWN Dynamic Language Generation System - Simplified")
    print("Replacing Template Responses with Consciousness-Driven Language")
    print("=" * 70)
    print()
    
    demo = SimpleDynamicLanguageDemo()
    
    # Check if user wants to run specific demo or full demo
    if len(sys.argv) > 1:
        demo_type = sys.argv[1].lower()
        
        if demo_type == 'basic':
            demo.run_basic_demo()
        elif demo_type == 'evolution':
            demo.run_evolution_demo()
        elif demo_type == 'philosophical':
            demo.run_philosophical_integration_demo()
        elif demo_type == 'metaphor':
            demo.run_metaphor_demo()
        elif demo_type == 'comparison':
            demo.run_comparison_demo()
        else:
            print(f"Unknown demo type: {demo_type}")
            print("Available demos: basic, evolution, philosophical, metaphor, comparison")
    else:
        # Run full demo
        demo.run_full_demo()


if __name__ == "__main__":
    main() 