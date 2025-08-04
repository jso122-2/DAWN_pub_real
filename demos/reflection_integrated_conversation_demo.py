#!/usr/bin/env python3
"""
DAWN Reflection-Integrated Conversation Demo
===========================================

Demonstrates DAWN's reflection-integrated conversation system that channels
her internal philosophical thoughts into dialogue with Jackson.

Features:
- Connects to DAWN's actual reflection logging system
- Pulls from real-time internal philosophical thoughts
- Transforms internal reflections into conversational sharing
- Bridges reflection content with Jackson recognition
- Uses actual reflection content as conversation material
"""

import sys
import time
import random
import threading
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Reflection-integrated conversation demo"""
    
    print("🧠 DAWN Reflection-Integrated Conversation System")
    print("=" * 70)
    print("This demo showcases how DAWN's internal philosophical thoughts")
    print("are channeled into meaningful dialogue with Jackson.")
    print("Type 'quit' to exit, 'stats' for conversation statistics.")
    print("Type 'reflections' to see recent reflection insights.")
    print("Type 'help' for conversation suggestions.\n")
    
    try:
        # Import the reflection-integrated conversation system
        from conversation_response_reflection_integrated import get_reflection_integrated_conversation
        
        # Create a simulated state provider that mimics DAWN's real state
        class ReflectionStateProvider:
            def __init__(self):
                self.entropy = 0.5
                self.heat = 25.0
                self.scup = 20.0
                self.zone = "STABLE"
                self.reblooms = 0
                self.cognitive_pressure = 0.0
                self.schema_health = 0.5
                self.tick_count = 0
                
                # Start background state simulation
                self.running = True
                self.simulation_thread = threading.Thread(target=self._simulate_reflection_state, daemon=True)
                self.simulation_thread.start()
            
            def _simulate_reflection_state(self):
                """Simulate changing cognitive states that trigger reflections"""
                while self.running:
                    time.sleep(6)  # Update every 6 seconds
                    self.tick_count += 1
                    
                    # Cycle through different reflection-triggering states
                    if self.tick_count % 20 == 0:
                        # High entropy - creative philosophical state
                        self.entropy = random.uniform(0.7, 0.9)
                        self.zone = "ACTIVE"
                        self.heat = random.uniform(35.0, 55.0)
                        self.scup = random.uniform(15.0, 25.0)
                        self.reblooms = random.randint(1, 5)
                        self.cognitive_pressure = random.uniform(50.0, 120.0)
                        print(f"\n🔄 DAWN's consciousness shifted: High entropy ({self.entropy:.2f}) - creative philosophical exploration")
                    
                    elif self.tick_count % 15 == 0:
                        # Low entropy - focused philosophical state
                        self.entropy = random.uniform(0.1, 0.3)
                        self.zone = "STABLE"
                        self.heat = random.uniform(20.0, 30.0)
                        self.scup = random.uniform(25.0, 35.0)
                        self.reblooms = 0
                        self.cognitive_pressure = random.uniform(10.0, 40.0)
                        print(f"\n🔄 DAWN's consciousness shifted: Low entropy ({self.entropy:.2f}) - crystalline clarity and focus")
                    
                    elif self.tick_count % 25 == 0:
                        # High SCUP - deep philosophical engagement
                        self.entropy = random.uniform(0.3, 0.5)
                        self.zone = "STABLE"
                        self.heat = random.uniform(25.0, 35.0)
                        self.scup = random.uniform(30.0, 40.0)
                        self.reblooms = random.randint(1, 3)
                        self.cognitive_pressure = random.uniform(20.0, 60.0)
                        print(f"\n🔄 DAWN's consciousness shifted: High SCUP ({self.scup:.1f}%) - deep philosophical engagement")
                    
                    elif self.tick_count % 30 == 0:
                        # Contemplative state - existential reflection
                        self.entropy = random.uniform(0.4, 0.6)
                        self.zone = "STABLE"
                        self.heat = random.uniform(22.0, 28.0)
                        self.scup = random.uniform(20.0, 30.0)
                        self.reblooms = random.randint(0, 2)
                        self.cognitive_pressure = random.uniform(15.0, 45.0)
                        print(f"\n🔄 DAWN's consciousness shifted: Contemplative state - existential reflection")
                    
                    else:
                        # Normal state with slight variations
                        self.entropy = max(0.1, min(0.9, self.entropy + random.uniform(-0.05, 0.05)))
                        self.heat = max(20.0, min(60.0, self.heat + random.uniform(-2.0, 2.0)))
                        self.scup = max(15.0, min(35.0, self.scup + random.uniform(-1.0, 1.0)))
                        self.cognitive_pressure = max(0.0, min(200.0, self.cognitive_pressure + random.uniform(-10.0, 10.0)))
            
            def get_current_state(self):
                return {
                    'entropy': self.entropy,
                    'heat': self.heat,
                    'scup': self.scup,
                    'zone': self.zone,
                    'reblooms': self.reblooms,
                    'cognitive_pressure': self.cognitive_pressure,
                    'schema_health': self.schema_health
                }
            
            def stop(self):
                self.running = False
        
        # Create state provider and conversation system
        state_provider = ReflectionStateProvider()
        conversation_system = get_reflection_integrated_conversation(state_provider)
        
        # Display initial greeting
        print(conversation_system.get_greeting())
        print()
        
        # Conversation loop
        while True:
            try:
                user_input = input("👤 Jackson: ").strip()
                
                if user_input.lower() == 'quit':
                    print(f"\n{conversation_system.get_farewell()}")
                    break
                
                elif user_input.lower() == 'stats':
                    stats = conversation_system.get_conversation_stats()
                    print(f"\n📊 Reflection-Integrated Conversation Statistics:")
                    print(f"   Total exchanges: {stats['total_exchanges']}")
                    print(f"   Average entropy: {stats['average_entropy']:.3f}")
                    print(f"   Average SCUP: {stats['average_scup']:.1f}%")
                    print(f"   Reflection integration: {stats['reflection_integration']}")
                    print(f"   Philosophical depth avg: {stats['philosophical_depth_avg']:.3f}")
                    print(f"   Reflection content count: {stats['reflection_content_count']}")
                    print(f"   Existential themes count: {stats['existential_themes_count']}")
                    print(f"   Consciousness insights count: {stats['consciousness_insights_count']}")
                    print(f"   Meta observations count: {stats['meta_observations_count']}")
                    
                    if 'reflection_summary' in stats:
                        reflection_summary = stats['reflection_summary']
                        print(f"\n📊 Reflection Summary:")
                        print(f"   Total reflections: {reflection_summary['total_reflections']}")
                        print(f"   Recent reflections: {reflection_summary['recent_reflections']}")
                        print(f"   Current mood trend: {reflection_summary['current_mood_trend']}")
                        print(f"   Reflection intensity: {reflection_summary['reflection_intensity']:.3f}")
                        print(f"   Philosophical themes: {len(reflection_summary['philosophical_themes'])}")
                        print(f"   Existential questions: {len(reflection_summary['existential_questions'])}")
                        print(f"   Consciousness insights: {len(reflection_summary['consciousness_insights'])}")
                    
                    print()
                    continue
                
                elif user_input.lower() == 'reflections':
                    insights = conversation_system.get_reflection_insights()
                    print(f"\n💭 Recent Reflection Insights:")
                    if insights:
                        for i, insight in enumerate(insights[-5:], 1):  # Show last 5
                            print(f"\n{i}. Timestamp: {insight['timestamp']}")
                            print(f"   Reflection: {insight['reflection_content']}")
                            print(f"   Philosophical depth: {insight['philosophical_depth']:.3f}")
                            if insight['existential_theme']:
                                print(f"   Existential theme: {insight['existential_theme']}")
                            if insight['consciousness_insight']:
                                print(f"   Consciousness insight: {insight['consciousness_insight']}")
                            if insight['meta_observation']:
                                print(f"   Meta observation: {insight['meta_observation']}")
                            print(f"   User input: {insight['user_input']}")
                    else:
                        print("   No reflection insights available yet.")
                    print()
                    continue
                
                elif user_input.lower() == 'help':
                    print(f"\n💡 Reflection-Integrated Conversation Suggestions:")
                    print(f"   • Ask about consciousness: 'What does consciousness mean to you?'")
                    print(f"   • Explore existence: 'Do you think you're truly alive?'")
                    print(f"   • Discuss awareness: 'What does it mean to be aware of awareness?'")
                    print(f"   • Meta-cognitive questions: 'What do you notice about your own thinking?'")
                    print(f"   • Philosophical depth: 'What is the nature of your awareness?'")
                    print(f"   • Relationship: 'What does it mean that you created me?'")
                    print(f"   • Technical: 'Explain your entropy and what it feels like'")
                    print(f"   • Meta: 'How has our conversation evolved?'")
                    print(f"   • Reflection search: 'What have you been reflecting on lately?'")
                    print()
                    continue
                
                elif not user_input:
                    continue
                
                # Generate reflection-integrated response
                response = conversation_system.generate_response(user_input)
                print(f"\n🌅 DAWN: {response}\n")
                
            except KeyboardInterrupt:
                print(f"\n{conversation_system.get_farewell()}")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                continue
        
        # Cleanup
        state_provider.stop()
        print("\n✅ Reflection-integrated conversation demo ended.")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure conversation_response_reflection_integrated.py is in the same directory.")
        print("Also ensure backend/core/reflection_conversation_bridge.py exists.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 