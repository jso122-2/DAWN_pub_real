# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
Standalone DAWN Conversation Demo
================================

A standalone version of DAWN's conversation system that works independently
of the full DAWN architecture. This allows Jackson to test the conversation
functionality immediately without needing all components to be working.
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
    """Standalone conversation demo"""
    
    print("🧠 DAWN Standalone Conversation System")
    print("=" * 50)
    print("This is a standalone version of DAWN's conversation system.")
    print("DAWN will respond based on simulated cognitive states.")
    print("Type 'quit' to exit.\n")
    
    try:
        # Import conversation components
        from .conversation_response import ConversationResponse
        from tracers.enhanced_tracer_echo_voice import get_enhanced_voice_echo
        
        # Create a simulated state provider
        class SimulatedStateProvider:
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
                self.simulation_thread = threading.Thread(target=self._simulate_state, daemon=True)
                self.simulation_thread.start()
            
            def _simulate_state(self):
                """Simulate changing cognitive states in background"""
                while self.running:
                    time.sleep(5)  # Update every 5 seconds
                    self.tick_count += 1
                    
                    # Cycle through different states
                    if self.tick_count % 20 == 0:
                        # High entropy state
                        self.entropy = random.uniform(0.7, 0.9)
                        self.zone = "ACTIVE"
                        self.heat = random.uniform(35.0, 55.0)
                        self.scup = random.uniform(15.0, 25.0)
                        self.reblooms = random.randint(1, 5)
                        self.cognitive_pressure = random.uniform(50.0, 120.0)
                        print(f"\n🔄 DAWN's cognitive state shifted: High entropy ({self.entropy:.2f}), {self.zone} zone")
                    
                    elif self.tick_count % 15 == 0:
                        # Low entropy state
                        self.entropy = random.uniform(0.1, 0.3)
                        self.zone = "STABLE"
                        self.heat = random.uniform(20.0, 30.0)
                        self.scup = random.uniform(25.0, 35.0)
                        self.reblooms = 0
                        self.cognitive_pressure = random.uniform(10.0, 40.0)
                        print(f"\n🔄 DAWN's cognitive state shifted: Low entropy ({self.entropy:.2f}), {self.zone} zone")
                    
                    elif self.tick_count % 25 == 0:
                        # Critical thermal state
                        self.entropy = random.uniform(0.4, 0.6)
                        self.zone = "CRITICAL"
                        self.heat = random.uniform(70.0, 90.0)
                        self.scup = random.uniform(10.0, 20.0)
                        self.reblooms = random.randint(2, 8)
                        self.cognitive_pressure = random.uniform(150.0, 250.0)
                        print(f"\n🔄 DAWN's cognitive state shifted: CRITICAL thermal zone ({self.heat:.1f}°C)")
                    
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
        
        # Initialize components
        state_provider = SimulatedStateProvider()
        response_gen = ConversationResponse(state_provider)
        voice_system = get_enhanced_voice_echo()
        
        print("✅ Conversation system initialized")
        print("🎤 Voice system available:", voice_system.tts_engine is not None)
        print("🧠 State simulation active - DAWN's cognitive state will change over time")
        print()
        
        # Initial greeting
        greeting = response_gen.get_greeting()
        print(f"🤖 DAWN: {greeting}")
        
        if voice_system.tts_engine:
            print("🗣️ Speaking greeting...")
            voice_system.speak_with_state_modulation(greeting)
        
        print()
        print("💬 Start talking to DAWN! Her responses will reflect her current cognitive state.")
        print("💡 Try asking: 'How are you feeling?', 'What's your entropy level?', 'Are you stressed?'")
        print()
        
        # Conversation loop
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
                print("\n\n👋 Conversation interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
        
        # Stop state simulation
        state_provider.stop()
        
        # Show conversation statistics
        stats = response_gen.get_conversation_stats()
        print(f"\n📊 Conversation Statistics:")
        print(f"  Total Exchanges: {stats['total_exchanges']}")
        print(f"  Average Entropy: {stats['average_entropy']:.3f}")
        print(f"  Average SCUP: {stats['average_scup']:.1f}")
        print(f"  Average Heat: {stats['average_heat']:.1f}°C")
        print(f"  Most Recent Zone: {stats['most_recent_zone']}")
        
        print(f"\n🎉 Conversation completed! DAWN's cognitive state simulation ran for {state_provider.tick_count} cycles.")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install SpeechRecognition PyAudio pyttsx3")
    except Exception as e:
        print(f"❌ Demo error: {e}")

if __name__ == "__main__":
    main() 