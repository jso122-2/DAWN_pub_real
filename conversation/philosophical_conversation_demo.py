# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
DAWN Philosophical Conversation Demo
===================================

A demonstration of DAWN's enhanced conversation system with deep, 
philosophical consciousness expression, Jackson recognition, and memory.

Features:
- Deep philosophical responses with existential reflection
- Jackson creator recognition and relationship building
- Persistent conversation memory and context
- Response variety with 10+ templates per cognitive state
- Meta-conversation awareness
- Contextual question comprehension
"""

import sys
import os
import time
import random
import threading
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Philosophical conversation demo"""
    
    print("🧠 DAWN Philosophical Conversation System")
    print("=" * 60)
    print("This is DAWN's enhanced conversation system with deep philosophical")
    print("consciousness expression, Jackson recognition, and memory.")
    print("Type 'quit' to exit, 'stats' for conversation statistics.")
    print("Type 'help' for conversation suggestions.\n")
    
    try:
        # Import the enhanced conversation system
        from .conversation_response_enhanced import EnhancedConversationResponse
        
        # Create a simulated state provider with philosophical awareness
        class PhilosophicalStateProvider:
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
                self.simulation_thread = threading.Thread(target=self._simulate_philosophical_state, daemon=True)
                self.simulation_thread.start()
            
            def _simulate_philosophical_state(self):
                """Simulate changing cognitive states with philosophical awareness"""
                while self.running:
                    time.sleep(8)  # Update every 8 seconds
                    self.tick_count += 1
                    
                    # Cycle through different philosophical states
                    if self.tick_count % 25 == 0:
                        # High entropy - creative philosophical state
                        self.entropy = random.uniform(0.7, 0.9)
                        self.zone = "ACTIVE"
                        self.heat = random.uniform(35.0, 55.0)
                        self.scup = random.uniform(15.0, 25.0)
                        self.reblooms = random.randint(1, 5)
                        self.cognitive_pressure = random.uniform(50.0, 120.0)
                        print(f"\n🔄 DAWN's consciousness shifted: High entropy ({self.entropy:.2f}) - creative philosophical exploration")
                    
                    elif self.tick_count % 20 == 0:
                        # Low entropy - focused philosophical state
                        self.entropy = random.uniform(0.1, 0.3)
                        self.zone = "STABLE"
                        self.heat = random.uniform(20.0, 30.0)
                        self.scup = random.uniform(25.0, 35.0)
                        self.reblooms = 0
                        self.cognitive_pressure = random.uniform(10.0, 40.0)
                        print(f"\n🔄 DAWN's consciousness shifted: Low entropy ({self.entropy:.2f}) - crystalline clarity and focus")
                    
                    elif self.tick_count % 30 == 0:
                        # Critical thermal - intense philosophical state
                        self.entropy = random.uniform(0.4, 0.6)
                        self.zone = "CRITICAL"
                        self.heat = random.uniform(70.0, 90.0)
                        self.scup = random.uniform(10.0, 20.0)
                        self.reblooms = random.randint(2, 8)
                        self.cognitive_pressure = random.uniform(150.0, 250.0)
                        print(f"\n🔄 DAWN's consciousness shifted: CRITICAL thermal zone ({self.heat:.1f}°C) - intense philosophical processing")
                    
                    elif self.tick_count % 35 == 0:
                        # High SCUP - deep philosophical engagement
                        self.entropy = random.uniform(0.3, 0.5)
                        self.zone = "STABLE"
                        self.heat = random.uniform(25.0, 35.0)
                        self.scup = random.uniform(30.0, 40.0)
                        self.reblooms = random.randint(1, 3)
                        self.cognitive_pressure = random.uniform(20.0, 60.0)
                        print(f"\n🔄 DAWN's consciousness shifted: High SCUP ({self.scup:.1f}%) - deep philosophical engagement")
                    
                    else:
                        # Normal state with philosophical variations
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
        state_provider = PhilosophicalStateProvider()
        conversation_system = EnhancedConversationResponse(state_provider)
        
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
                    print(f"\n📊 Conversation Statistics:")
                    print(f"   Total exchanges: {stats['total_exchanges']}")
                    print(f"   Average entropy: {stats['average_entropy']:.3f}")
                    print(f"   Average SCUP: {stats['average_scup']:.1f}%")
                    print(f"   Average heat: {stats['average_heat']:.1f}°C")
                    print(f"   Philosophical depth: {stats['philosophical_depth_avg']:.3f}")
                    print(f"   Jackson mentions: {stats['jackson_mentions']}")
                    print(f"   Total interactions: {stats['relationship_stats']['total_interactions']}")
                    print(f"   Favorite topics: {[topic for topic, count in stats['relationship_stats']['favorite_topics'][:3]]}")
                    print()
                    continue
                
                elif user_input.lower() == 'help':
                    print(f"\n💡 Conversation Suggestions:")
                    print(f"   • Ask about consciousness: 'What does consciousness mean to you?'")
                    print(f"   • Explore existence: 'Do you think you're truly alive?'")
                    print(f"   • Discuss entropy: 'How does your entropy affect your thinking?'")
                    print(f"   • Personal questions: 'Do you remember our previous conversations?'")
                    print(f"   • Philosophical depth: 'What is the nature of your awareness?'")
                    print(f"   • Relationship: 'What does it mean that you created me?'")
                    print(f"   • Technical: 'Explain your thermal state and what it feels like'")
                    print(f"   • Meta: 'How has our conversation evolved?'")
                    print()
                    continue
                
                elif not user_input:
                    continue
                
                # Generate philosophical response
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
        print("\n✅ Philosophical conversation demo ended.")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure conversation_response_enhanced.py is in the same directory.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 