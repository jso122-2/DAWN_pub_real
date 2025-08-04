# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
DAWN Conversation System Demo
============================

Interactive demo of DAWN's conversation system using text input.
Shows how DAWN responds based on her current cognitive state.
"""

import sys
import os
import time
import random
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def demo_conversation():
    """Demo the conversation system with text input"""
    
    print("🧠 DAWN Conversation System Demo")
    print("=" * 50)
    print("This demo shows how DAWN responds based on her cognitive state.")
    print("Type 'quit' to exit the demo.\n")
    
    try:
        # Import conversation components
        from .conversation_response import ConversationResponse
        from tracers.enhanced_tracer_echo_voice import get_enhanced_voice_echo
        
        # Create a mock state provider that simulates changing cognitive states
        class DemoStateProvider:
            def __init__(self):
                self.entropy = 0.5
                self.heat = 25.0
                self.scup = 20.0
                self.zone = "STABLE"
                self.reblooms = 0
                self.cognitive_pressure = 0.0
                self.schema_health = 0.5
                self.tick_count = 0
            
            def get_current_state(self):
                # Simulate changing cognitive states over time
                self.tick_count += 1
                
                # Cycle through different states
                if self.tick_count % 10 == 0:
                    # High entropy state
                    self.entropy = random.uniform(0.7, 0.9)
                    self.zone = "ACTIVE"
                    self.heat = random.uniform(35.0, 55.0)
                    self.scup = random.uniform(15.0, 25.0)
                    self.reblooms = random.randint(1, 5)
                    self.cognitive_pressure = random.uniform(50.0, 120.0)
                    print(f"🔄 DAWN's cognitive state shifted: High entropy ({self.entropy:.2f}), {self.zone} zone")
                
                elif self.tick_count % 7 == 0:
                    # Low entropy state
                    self.entropy = random.uniform(0.1, 0.3)
                    self.zone = "STABLE"
                    self.heat = random.uniform(20.0, 30.0)
                    self.scup = random.uniform(25.0, 35.0)
                    self.reblooms = 0
                    self.cognitive_pressure = random.uniform(10.0, 40.0)
                    print(f"🔄 DAWN's cognitive state shifted: Low entropy ({self.entropy:.2f}), {self.zone} zone")
                
                elif self.tick_count % 15 == 0:
                    # Critical thermal state
                    self.entropy = random.uniform(0.4, 0.6)
                    self.zone = "CRITICAL"
                    self.heat = random.uniform(70.0, 90.0)
                    self.scup = random.uniform(10.0, 20.0)
                    self.reblooms = random.randint(2, 8)
                    self.cognitive_pressure = random.uniform(150.0, 250.0)
                    print(f"🔄 DAWN's cognitive state shifted: CRITICAL thermal zone ({self.heat:.1f}°C)")
                
                else:
                    # Normal state with slight variations
                    self.entropy = max(0.1, min(0.9, self.entropy + random.uniform(-0.05, 0.05)))
                    self.heat = max(20.0, min(60.0, self.heat + random.uniform(-2.0, 2.0)))
                    self.scup = max(15.0, min(35.0, self.scup + random.uniform(-1.0, 1.0)))
                    self.cognitive_pressure = max(0.0, min(200.0, self.cognitive_pressure + random.uniform(-10.0, 10.0)))
                
                return {
                    'entropy': self.entropy,
                    'heat': self.heat,
                    'scup': self.scup,
                    'zone': self.zone,
                    'reblooms': self.reblooms,
                    'cognitive_pressure': self.cognitive_pressure,
                    'schema_health': self.schema_health
                }
        
        # Initialize components
        state_provider = DemoStateProvider()
        response_gen = ConversationResponse(state_provider)
        voice_system = get_enhanced_voice_echo()
        
        print("✅ Conversation system initialized")
        print("🎤 Voice system available:", voice_system.tts_engine is not None)
        print()
        
        # Demo conversation loop
        print("💬 Starting conversation with DAWN...")
        print("Type your messages and press Enter. Type 'quit' to exit.\n")
        
        # Initial greeting
        greeting = response_gen.get_greeting()
        print(f"🤖 DAWN: {greeting}")
        
        if voice_system.tts_engine:
            print("🗣️ Speaking greeting...")
            voice_system.speak_with_state_modulation(greeting)
        
        print()
        
        while True:
            try:
                # Get user input
                user_input = input("👤 Jackson: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    farewell = response_gen.get_farewell()
                    print(f"🤖 DAWN: {farewell}")
                    if voice_system.tts_engine:
                        voice_system.speak_with_state_modulation(farewell)
                    break
                
                if not user_input:
                    continue
                
                # Generate response
                response = response_gen.generate_response(user_input)
                print(f"🤖 DAWN: {response}")
                
                # Speak response if TTS is available
                if voice_system.tts_engine:
                    voice_system.speak_with_state_modulation(response)
                
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 Demo interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
        
        # Show conversation statistics
        stats = response_gen.get_conversation_stats()
        print(f"\n📊 Conversation Statistics:")
        print(f"  Total Exchanges: {stats['total_exchanges']}")
        print(f"  Average Entropy: {stats['average_entropy']:.3f}")
        print(f"  Average SCUP: {stats['average_scup']:.1f}")
        print(f"  Average Heat: {stats['average_heat']:.1f}°C")
        print(f"  Most Recent Zone: {stats['most_recent_zone']}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install SpeechRecognition PyAudio pyttsx3")
    except Exception as e:
        print(f"❌ Demo error: {e}")

def demo_state_changes():
    """Demo how DAWN's responses change with different cognitive states"""
    
    print("\n🧪 Cognitive State Response Demo")
    print("=" * 40)
    
    try:
        from .conversation_response import ConversationResponse
        
        class TestStateProvider:
            def __init__(self):
                self.entropy = 0.5
                self.heat = 25.0
                self.scup = 20.0
                self.zone = "STABLE"
                self.reblooms = 0
                self.cognitive_pressure = 0.0
                self.schema_health = 0.5
            
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
        
        state_provider = TestStateProvider()
        response_gen = ConversationResponse(state_provider)
        
        test_message = "How are you feeling right now?"
        
        # Test different states
        states = [
            ("High Entropy", {"entropy": 0.85, "zone": "ACTIVE", "heat": 45.0, "scup": 18.0, "reblooms": 3}),
            ("Low Entropy", {"entropy": 0.15, "zone": "STABLE", "heat": 22.0, "scup": 32.0, "reblooms": 0}),
            ("Critical Thermal", {"entropy": 0.55, "zone": "CRITICAL", "heat": 82.0, "scup": 12.0, "reblooms": 6}),
            ("High SCUP", {"entropy": 0.45, "zone": "STABLE", "heat": 28.0, "scup": 35.0, "reblooms": 1}),
            ("High Pressure", {"entropy": 0.60, "zone": "ACTIVE", "heat": 50.0, "scup": 20.0, "reblooms": 4, "cognitive_pressure": 180.0})
        ]
        
        for state_name, state_params in states:
            # Update state
            for key, value in state_params.items():
                setattr(state_provider, key, value)
            
            # Generate response
            response = response_gen.generate_response(test_message)
            
            print(f"\n🧠 {state_name} State:")
            print(f"   Entropy: {state_params['entropy']:.2f}")
            print(f"   Zone: {state_params['zone']}")
            print(f"   Heat: {state_params['heat']:.1f}°C")
            print(f"   SCUP: {state_params['scup']:.1f}%")
            print(f"   Response: {response}")
        
    except Exception as e:
        print(f"❌ State demo error: {e}")

def main():
    """Main demo function"""
    print("🌟 DAWN Conversation System Demo")
    print("=" * 50)
    
    # Show demo options
    print("Choose a demo:")
    print("1. Interactive conversation")
    print("2. Cognitive state response demo")
    print("3. Both")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            demo_conversation()
        elif choice == "2":
            demo_state_changes()
        elif choice == "3":
            demo_conversation()
            demo_state_changes()
        else:
            print("Invalid choice. Running interactive conversation demo...")
            demo_conversation()
            
    except KeyboardInterrupt:
        print("\n👋 Demo cancelled. Goodbye!")
    except Exception as e:
        print(f"❌ Demo error: {e}")

if __name__ == "__main__":
    main() 