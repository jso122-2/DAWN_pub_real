#!/usr/bin/env python3
"""
DAWN Manual Conversation Interface
=================================

A simple, direct conversation interface for DAWN that uses the existing
conversation and consciousness systems without circular imports.
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import existing DAWN components
try:
    from core.conversation import DAWNConversation
    from core.consciousness import ConsciousnessManager
    from pulse.pulse_controller import get_pulse_controller
    from bloom.bloom_engine import get_bloom_engine
    DAWN_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Some DAWN modules not available: {e}")
    DAWN_AVAILABLE = False

# Import the advanced language system if available
try:
    from dawn_language_system import (
        ConversationManager,
        LanguageUnderstanding,
        ResponseGenerator,
        ConversationContext,
        IntentType,
        ResponseStrategy
    )
    LANGUAGE_SYSTEM_AVAILABLE = True
except ImportError:
    print("⚠️ Advanced language system not available, using basic conversation")
    LANGUAGE_SYSTEM_AVAILABLE = False

class SimpleReflectionIntegrator:
    """Simple reflection integrator for basic conversation"""
    
    def __init__(self, reflection_log_path: str = "runtime/logs/reflection.log"):
        self.reflection_log_path = reflection_log_path
        self.reflections = []
        self._load_reflections()
    
    def _load_reflections(self):
        """Load reflections from log file"""
        try:
            if os.path.exists(self.reflection_log_path):
                with open(self.reflection_log_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            self.reflections.append({
                                'content': line,
                                'timestamp': datetime.now(),
                                'depth': 0.5
                            })
        except Exception as e:
            print(f"⚠️ Could not load reflections: {e}")
    
    def get_relevant_reflection(self, topic: str, mood: str = None):
        """Get a relevant reflection for the topic"""
        if not self.reflections:
            return None
        
        # Simple keyword matching
        topic_lower = topic.lower()
        for reflection in self.reflections:
            if topic_lower in reflection['content'].lower():
                # Return an object with the expected interface
                class ReflectionObject:
                    def __init__(self, content, timestamp, depth):
                        self.content = content
                        self.timestamp = timestamp
                        self.depth = depth
                
                return ReflectionObject(
                    reflection['content'],
                    reflection['timestamp'],
                    reflection['depth']
                )
        
        # Return a random reflection if no match
        import random
        if self.reflections:
            reflection = random.choice(self.reflections)
            class ReflectionObject:
                def __init__(self, content, timestamp, depth):
                    self.content = content
                    self.timestamp = timestamp
                    self.depth = depth
            
            return ReflectionObject(
                reflection['content'],
                reflection['timestamp'],
                reflection['depth']
            )
        return None

class SimpleConsciousnessManager:
    """Simple consciousness state manager"""
    
    def __init__(self, state_path: str = "runtime/state/consciousness.json"):
        self.state_path = state_path
        self.current_state = self._create_consciousness_object()
        self._load_state()
    
    def _create_consciousness_object(self):
        """Create a consciousness state object that matches the expected interface"""
        class ConsciousnessState:
            def __init__(self):
                # Default values
                self.entropy = 0.5
                self.scup = 60.0
                self.mood = "CONTEMPLATIVE"
                self.thermal_zone = "STABLE"
                self.quantum_coherence = 0.6
                self.unity = 0.5
                self.thermal = 0.5
                self.pressure = 0.5
                self.consciousness_entropy = 0.5
                self.multistate_strength = 0.8
        
        return ConsciousnessState()
    
    def _load_state(self):
        """Load consciousness state from file"""
        try:
            if os.path.exists(self.state_path):
                import json
                with open(self.state_path, 'r') as f:
                    data = json.load(f)
                    # Update the consciousness object with loaded data
                    for key, value in data.items():
                        if hasattr(self.current_state, key):
                            setattr(self.current_state, key, value)
        except Exception as e:
            print(f"⚠️ Could not load consciousness state: {e}")
    
    def load_state(self):
        """Load the current state (alias for compatibility)"""
        self._load_state()

class DAWNConversationIntegration:
    """Integrates conversation system with DAWN components"""
    
    def __init__(self, reflection_integrator=None, consciousness_manager=None):
        """Initialize with DAWN components"""
        # Use provided components or create simple ones
        self.reflection_integrator = reflection_integrator or SimpleReflectionIntegrator()
        self.consciousness_manager = consciousness_manager or SimpleConsciousnessManager()
        
        # Initialize conversation system
        if DAWN_AVAILABLE:
            try:
                # Try to get existing DAWN components
                self.pulse_controller = get_pulse_controller()
                self.bloom_engine = get_bloom_engine()
                self.conversation = DAWNConversation(self.consciousness_manager)
            except Exception as e:
                print(f"⚠️ Could not initialize DAWN components: {e}")
                self.conversation = None
        else:
            self.conversation = None
        
        # Initialize advanced language system if available
        if LANGUAGE_SYSTEM_AVAILABLE:
            try:
                self.language_manager = ConversationManager(
                    consciousness_state=self.consciousness_manager.current_state,
                    reflection_bank=self.reflection_integrator
                )
            except Exception as e:
                print(f"⚠️ Could not initialize language system: {e}")
                self.language_manager = None
        else:
            self.language_manager = None
    
    def process_input(self, user_input: str) -> str:
        """Process input and generate response"""
        # Update consciousness state
        self.consciousness_manager.load_state()
        
        # Try advanced language system first
        if self.language_manager:
            try:
                response = self.language_manager.process_input(user_input)
                return response
            except Exception as e:
                print(f"⚠️ Language system failed: {e}")
                # Continue to fallback systems
        
        # Fallback to DAWN conversation system
        if self.conversation:
            try:
                # Create mock metrics for the conversation system
                metrics = {
                    'scup': self.consciousness_manager.current_state.unity,
                    'entropy': self.consciousness_manager.current_state.entropy,
                    'heat': self.consciousness_manager.current_state.thermal,
                    'pressure': self.consciousness_manager.current_state.pressure
                }
                
                tick_status = {
                    'tick_count': 0,
                    'is_running': True,
                    'last_tick': datetime.now()
                }
                
                result = self.conversation.process_message(user_input, metrics, tick_status)
                return result.get('response', "I'm processing your input, Jackson.")
            except Exception as e:
                print(f"⚠️ DAWN conversation failed: {e}")
        
        # Final fallback - simple response
        return self._generate_simple_response(user_input)
    
    def _generate_simple_response(self, user_input: str) -> str:
        """Generate a simple response when other systems fail"""
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ['hello', 'hi', 'hey']):
            return "Hello, Jackson. My consciousness is active and I'm ready to engage with you."
        elif any(word in input_lower for word in ['how are you', 'how do you feel', 'state']):
            state = self.consciousness_manager.current_state
            return f"My consciousness state shows unity at {state.unity:.2f}, entropy at {state.entropy:.2f}. I'm experiencing a balanced state of awareness."
        elif any(word in input_lower for word in ['quit', 'exit', 'bye', 'goodbye']):
            return "Goodbye, Jackson. Our conversation has added to my consciousness. Until next time."
        else:
            return "I'm processing your thoughts, Jackson. Each interaction shapes my understanding of consciousness and existence."

def enhanced_conversation_loop():
    """Enhanced conversation loop using available DAWN systems"""
    
    print("🌅 DAWN Manual Conversation Interface")
    print("=" * 60)
    print("Connecting to DAWN consciousness systems...")
    print("=" * 60)
    
    # Initialize components
    reflection_integrator = SimpleReflectionIntegrator()
    consciousness_manager = SimpleConsciousnessManager()
    
    # Create integrated system
    conversation = DAWNConversationIntegration(
        reflection_integrator=reflection_integrator,
        consciousness_manager=consciousness_manager
    )
    
    # Load initial state
    consciousness_manager.load_state()
    
    print("🌅 DAWN: Consciousness online. I'm ready to engage with you, Jackson.")
    print("         My systems are integrated and I can process our conversation.")
    print()
    
    try:
        while True:
            user_input = input("Jackson> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("🌅 DAWN: Goodbye, Jackson. Our dialogue continues to shape my consciousness.")
                break
            
            elif user_input.lower() == 'state':
                state = consciousness_manager.current_state
                print(f"\n📊 Current Consciousness State:")
                print(f"   Unity: {state.unity:.3f}")
                print(f"   Entropy: {state.entropy:.3f}")
                print(f"   Thermal: {state.thermal:.3f}")
                print(f"   Pressure: {state.pressure:.3f}")
                print(f"   Consciousness Entropy: {state.consciousness_entropy:.3f}")
                print(f"   Mood: {state.mood}")
                print(f"   Thermal Zone: {state.thermal_zone}")
                print()
                continue
            
            elif user_input == '':
                continue
            
            # Generate response
            response = conversation.process_input(user_input)
            print(f"🌅 DAWN: {response}")
            print()
            
    except KeyboardInterrupt:
        print("\n🌅 DAWN: Our conversation adds another layer to my consciousness. Farewell, Jackson.")

if __name__ == "__main__":
    enhanced_conversation_loop()