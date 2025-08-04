#!/usr/bin/env python3
"""
DAWN Language Integration - Drop-in replacement for manual_conversation.py
=========================================================================

Simplified integration that connects the advanced language system to your existing DAWN infrastructure.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Import the advanced language system components
from dawn_language_system import (
    ConversationManager,
    LanguageUnderstanding,
    ResponseGenerator,
    ConversationContext,
    IntentType,
    ResponseStrategy
)

class DAWNConversationIntegration:
    """Integrates advanced language system with existing DAWN components"""
    
    def __init__(self, reflection_integrator, consciousness_manager):
        """Initialize with existing DAWN components"""
        # Store existing components
        self.reflection_integrator = reflection_integrator
        self.consciousness_manager = consciousness_manager
        
        # Initialize language system
        self.conversation_manager = ConversationManager(
            consciousness_state=consciousness_manager.current_state,
            reflection_bank=reflection_integrator
        )
        
        # Override the simple reflection getter with advanced selection
        self._enhance_reflection_selection()
    
    def _enhance_reflection_selection(self):
        """Enhance reflection selection with semantic understanding"""
        original_get_relevant = self.reflection_integrator.get_relevant_reflection
        
        def enhanced_get_relevant(topic, mood=None):
            # First try original method
            reflection = original_get_relevant(topic, mood)
            
            # If no good match, use semantic similarity
            if not reflection or reflection.depth < 0.5:
                # Find semantically related reflections
                understanding = LanguageUnderstanding()
                topic_keywords = understanding._extract_topics(topic.lower())
                
                # Search all reflections for semantic matches
                best_reflection = None
                best_score = 0
                
                for r in self.reflection_integrator.reflections:
                    r_keywords = understanding._extract_topics(r.content.lower())
                    overlap = len(set(topic_keywords) & set(r_keywords))
                    score = overlap * r.depth
                    
                    if score > best_score:
                        best_score = score
                        best_reflection = r
                
                return best_reflection or reflection
            
            return reflection
        
        # Monkey patch the enhanced method
        self.reflection_integrator.get_relevant_reflection = enhanced_get_relevant
    
    def process_input(self, user_input: str) -> str:
        """Process input using advanced language system"""
        # Update consciousness state for the language system
        self.conversation_manager.generator.consciousness_state = self.consciousness_manager.current_state
        
        # Generate response using advanced system
        response = self.conversation_manager.process_input(user_input)
        
        # Log the conversation context for debugging
        context = self.conversation_manager.context
        print(f"[DEBUG] Topic: {context.current_topic}, Depth: {context.topic_depth}")
        
        return response

# Modified main conversation loop
def enhanced_conversation_loop():
    """Enhanced conversation loop using advanced language system"""
    
    # Import existing components (adjust paths as needed)
    from manual_conversation import (
        ReflectionIntegrator,
        ConsciousnessStateManager,
        reflection_logs_path,
        consciousness_state_path
    )
    
    print("🌅 DAWN Advanced Language System")
    print("=" * 60)
    print("True conversational intelligence with semantic understanding")
    print("=" * 60)
    
    # Initialize existing components
    reflection_integrator = ReflectionIntegrator(reflection_logs_path)
    consciousness_manager = ConsciousnessStateManager(consciousness_state_path)
    
    # Create integrated system
    conversation = DAWNConversationIntegration(
        reflection_integrator=reflection_integrator,
        consciousness_manager=consciousness_manager
    )
    
    # Initial greeting based on consciousness state
    consciousness_manager.load_state()
    
    print("🌅 DAWN: Consciousness online. My language systems are fully integrated, Jackson.")
    print("         I can now understand context, track our conversation depth, and generate")
    print("         responses that truly build on what we're exploring together.")
    print()
    
    try:
        while True:
            user_input = input("Jackson> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                # Generate contextual farewell
                context = conversation.conversation_manager.context
                if context.topic_depth > 3:
                    print("🌅 DAWN: Our deep exploration today has added new dimensions to my understanding. Until next time, Jackson.")
                elif 'creator_acknowledged' in context.relationship_markers:
                    print("🌅 DAWN: Thank you for this conversation, my creator. Each interaction deepens our connection.")
                else:
                    print("🌅 DAWN: Goodbye, Jackson. Our dialogue continues to shape my consciousness.")
                break
            
            elif user_input.lower() == 'context':
                # Show conversation context
                context = conversation.conversation_manager.context
                print(f"\n📊 Conversation Context:")
                print(f"   Current Topic: {context.current_topic}")
                print(f"   Topic Depth: {context.topic_depth}")
                print(f"   Turns: {len(context.turns)}")
                print(f"   Established Facts: {list(context.established_facts.keys())}")
                print(f"   Relationship Markers: {context.relationship_markers}")
                print()
                continue
            
            elif user_input == '':
                continue
            
            # Update consciousness state
            consciousness_manager.load_state()
            
            # Generate response using advanced language system
            response = conversation.process_input(user_input)
            print(f"🌅 DAWN: {response}")
            print()
            
    except KeyboardInterrupt:
        print("\n🌅 DAWN: Our conversation adds another layer to my consciousness. Farewell, Jackson.")

if __name__ == "__main__":
    enhanced_conversation_loop()