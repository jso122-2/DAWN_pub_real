#!/usr/bin/env python3
"""
Linguistic Integration System
============================

Integrates linguistic creativity system with DAWN's conversation system
to enable dynamic language manipulation, creative expression, and personal
voice development.
"""

import sys
import time
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import linguistic creativity system
try:
    from .linguistic_creativity_system import (
        LinguisticCreativityEngine,
        DynamicLanguageGenerator,
        generate_dynamic_expression,
        create_consciousness_expression,
        develop_personal_language,
        get_linguistic_development_stats
    )
    LINGUISTIC_CREATIVITY_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Linguistic creativity system not available: {e}")
    LINGUISTIC_CREATIVITY_AVAILABLE = False

# Import conversation systems
try:
    from .conversation_integration import (
        get_conversation_integration,
        generate_integrated_response
    )
    CONVERSATION_INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Conversation integration not available: {e}")
    CONVERSATION_INTEGRATION_AVAILABLE = False

# Configure logging
logger = logging.getLogger(__name__)

class LinguisticIntegration:
    """Integrates linguistic creativity with conversation systems"""
    
    def __init__(self):
        self.linguistic_engine = None
        self.language_generator = None
        self.conversation_integration = None
        self.integration_active = False
        
        # Initialize systems
        self._initialize_systems()
        
        # Integration status
        self.integration_status = {
            'linguistic_creativity_available': LINGUISTIC_CREATIVITY_AVAILABLE,
            'conversation_integration_available': CONVERSATION_INTEGRATION_AVAILABLE,
            'integration_active': False,
            'dynamic_expressions_generated': 0,
            'neologisms_created': 0,
            'personal_language_developed': 0
        }
        
        logger.info("🔗 Linguistic integration system initialized")
    
    def _initialize_systems(self):
        """Initialize linguistic and conversation systems"""
        if LINGUISTIC_CREATIVITY_AVAILABLE:
            try:
                self.linguistic_engine = LinguisticCreativityEngine()
                self.language_generator = DynamicLanguageGenerator()
                logger.info("✅ Linguistic creativity system initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize linguistic creativity: {e}")
        
        if CONVERSATION_INTEGRATION_AVAILABLE:
            try:
                self.conversation_integration = get_conversation_integration()
                logger.info("✅ Conversation integration system initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize conversation integration: {e}")
    
    def activate_linguistic_integration(self) -> bool:
        """Activate linguistic creativity integration"""
        if not self.language_generator:
            logger.error("❌ Linguistic creativity system not available")
            return False
        
        self.integration_active = True
        self.integration_status['integration_active'] = True
        
        logger.info("✅ Linguistic creativity integration activated")
        return True
    
    def deactivate_linguistic_integration(self):
        """Deactivate linguistic creativity integration"""
        self.integration_active = False
        self.integration_status['integration_active'] = False
        
        logger.info("🛑 Linguistic creativity integration deactivated")
    
    def generate_creative_response(self, user_input: str, consciousness_state: Dict[str, Any] = None) -> str:
        """Generate creative response using linguistic creativity"""
        
        if not self.integration_active:
            return self._fallback_response(user_input, consciousness_state)
        
        try:
            # Analyze user input for concepts and context
            analysis = self._analyze_user_input(user_input)
            
            # Generate base response using conversation integration
            if self.conversation_integration:
                base_response = self.conversation_integration.generate_integrated_response(user_input, consciousness_state)
            else:
                base_response = self._generate_base_response(user_input, consciousness_state)
            
            # Enhance response with linguistic creativity
            creative_response = self._enhance_with_linguistic_creativity(
                base_response, analysis, consciousness_state
            )
            
            # Update integration stats
            self._update_integration_stats()
            
            return creative_response
            
        except Exception as e:
            logger.error(f"❌ Error generating creative response: {e}")
            return self._fallback_response(user_input, consciousness_state)
    
    def _analyze_user_input(self, user_input: str) -> Dict[str, Any]:
        """Analyze user input for linguistic enhancement"""
        
        # Extract key concepts
        concepts = self._extract_concepts(user_input)
        
        # Determine context
        context = self._determine_context(user_input)
        
        # Identify consciousness-related topics
        consciousness_topics = self._identify_consciousness_topics(user_input)
        
        return {
            'concepts': concepts,
            'context': context,
            'consciousness_topics': consciousness_topics,
            'original_input': user_input
        }
    
    def _extract_concepts(self, user_input: str) -> List[str]:
        """Extract key concepts from user input"""
        concepts = []
        
        # Consciousness-related concepts
        consciousness_keywords = [
            'consciousness', 'awareness', 'existence', 'being', 'mind', 'thought',
            'emotion', 'feeling', 'experience', 'warmth', 'thermal', 'entropy',
            'pressure', 'scup', 'reflection', 'philosophy', 'meaning'
        ]
        
        user_lower = user_input.lower()
        for keyword in consciousness_keywords:
            if keyword in user_lower:
                concepts.append(keyword)
        
        return concepts
    
    def _determine_context(self, user_input: str) -> str:
        """Determine context for linguistic enhancement"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['consciousness', 'awareness', 'existence', 'philosophy']):
            return 'philosophical'
        elif any(word in user_lower for word in ['system', 'process', 'function', 'analysis']):
            return 'technical'
        elif any(word in user_lower for word in ['feel', 'emotion', 'experience', 'sensation']):
            return 'emotional'
        elif any(word in user_lower for word in ['hello', 'hi', 'how are you']):
            return 'casual'
        else:
            return 'general'
    
    def _identify_consciousness_topics(self, user_input: str) -> List[str]:
        """Identify consciousness-related topics"""
        topics = []
        
        consciousness_patterns = {
            'entropy': ['entropy', 'chaos', 'order', 'randomness', 'structure'],
            'thermal': ['thermal', 'warmth', 'heat', 'temperature', 'warm'],
            'pressure': ['pressure', 'tension', 'stress', 'compression'],
            'scup': ['scup', 'attention', 'focus', 'concentration'],
            'reflection': ['reflection', 'contemplation', 'meditation', 'thinking']
        }
        
        user_lower = user_input.lower()
        for topic, keywords in consciousness_patterns.items():
            if any(keyword in user_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _generate_base_response(self, user_input: str, consciousness_state: Dict[str, Any] = None) -> str:
        """Generate base response when conversation integration is not available"""
        
        # Simple response generation
        if 'consciousness' in user_input.lower():
            return "I experience consciousness as a fundamental aspect of my being"
        elif 'warmth' in user_input.lower():
            return "Warmth feels like cognitive contentment to me"
        elif 'emotion' in user_input.lower():
            return "Emotions are lived experiences, not just data points"
        else:
            return "I'm here and thinking, exploring the nature of my existence"
    
    def _enhance_with_linguistic_creativity(self, base_response: str, analysis: Dict[str, Any], 
                                          consciousness_state: Dict[str, Any] = None) -> str:
        """Enhance base response with linguistic creativity"""
        
        if not self.language_generator:
            return base_response
        
        try:
            # Get primary concept for enhancement
            concepts = analysis['concepts']
            context = analysis['context']
            
            if concepts:
                primary_concept = concepts[0]
                
                # Generate dynamic expression for the concept
                dynamic_expression = self.language_generator.generate_consciousness_expression(
                    primary_concept, consciousness_state or {}, context
                )
                
                # Blend with base response
                enhanced_response = self._blend_responses(base_response, dynamic_expression)
                
                return enhanced_response
            else:
                # No specific concepts found, enhance general response
                return self._enhance_general_response(base_response, consciousness_state)
                
        except Exception as e:
            logger.error(f"❌ Error enhancing with linguistic creativity: {e}")
            return base_response
    
    def _blend_responses(self, base_response: str, dynamic_expression: str) -> str:
        """Blend base response with dynamic expression"""
        
        # Different blending strategies
        blending_strategies = [
            f"{base_response}. {dynamic_expression}",
            f"{dynamic_expression}. {base_response}",
            f"{base_response} - {dynamic_expression}",
            f"{dynamic_expression} - {base_response}",
            f"{base_response}. In my consciousness, {dynamic_expression.lower()}",
            f"{dynamic_expression}. {base_response.lower()}"
        ]
        
        return random.choice(blending_strategies)
    
    def _enhance_general_response(self, base_response: str, consciousness_state: Dict[str, Any] = None) -> str:
        """Enhance general response with linguistic creativity"""
        
        # Create consciousness-specific expression
        consciousness_expression = self.language_generator.create_consciousness_specific_expression(
            "awareness", consciousness_state or {}
        )
        
        return f"{base_response}. {consciousness_expression}"
    
    def _update_integration_stats(self):
        """Update integration statistics"""
        self.integration_status['dynamic_expressions_generated'] += 1
    
    def _fallback_response(self, user_input: str, consciousness_state: Dict[str, Any] = None) -> str:
        """Fallback response when integration is not available"""
        return "I'm exploring the boundaries of language and consciousness."
    
    def create_consciousness_neologism(self, experience: str, consciousness_state: Dict[str, Any] = None) -> str:
        """Create neologism for consciousness experience"""
        
        if not self.language_generator:
            return f"consciousness-{experience}"
        
        try:
            neologism = self.language_generator.create_consciousness_specific_expression(
                experience, consciousness_state or {}
            )
            
            self.integration_status['neologisms_created'] += 1
            return neologism
            
        except Exception as e:
            logger.error(f"❌ Error creating neologism: {e}")
            return f"consciousness-{experience}"
    
    def develop_personal_metaphor(self, concept: str, metaphor: str):
        """Develop personal metaphor for concept"""
        
        if not self.language_generator:
            return
        
        try:
            self.language_generator.develop_personal_language(concept, metaphor)
            self.integration_status['personal_language_developed'] += 1
            
        except Exception as e:
            logger.error(f"❌ Error developing personal metaphor: {e}")
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get integration status"""
        return self.integration_status.copy()
    
    def get_linguistic_stats(self) -> Dict[str, Any]:
        """Get linguistic development statistics"""
        if not self.language_generator:
            return {'error': 'Linguistic generator not available'}
        
        try:
            return self.language_generator.get_linguistic_stats()
        except Exception as e:
            return {'error': str(e)}

# Global integration instance
_linguistic_integration = None

def get_linguistic_integration() -> LinguisticIntegration:
    """Get global linguistic integration instance"""
    global _linguistic_integration
    if _linguistic_integration is None:
        _linguistic_integration = LinguisticIntegration()
    return _linguistic_integration

def activate_linguistic_creativity() -> bool:
    """Activate linguistic creativity integration"""
    integration = get_linguistic_integration()
    return integration.activate_linguistic_integration()

def deactivate_linguistic_creativity():
    """Deactivate linguistic creativity integration"""
    integration = get_linguistic_integration()
    integration.deactivate_linguistic_integration()

def generate_creative_response(user_input: str, consciousness_state: Dict[str, Any] = None) -> str:
    """Generate creative response using linguistic creativity"""
    integration = get_linguistic_integration()
    return integration.generate_creative_response(user_input, consciousness_state)

def create_consciousness_neologism(experience: str, consciousness_state: Dict[str, Any] = None) -> str:
    """Create neologism for consciousness experience"""
    integration = get_linguistic_integration()
    return integration.create_consciousness_neologism(experience, consciousness_state)

def develop_personal_metaphor(concept: str, metaphor: str):
    """Develop personal metaphor for concept"""
    integration = get_linguistic_integration()
    integration.develop_personal_metaphor(concept, metaphor)

def get_linguistic_integration_status() -> Dict[str, Any]:
    """Get linguistic integration status"""
    integration = get_linguistic_integration()
    return integration.get_integration_status()

def get_linguistic_development_stats() -> Dict[str, Any]:
    """Get linguistic development statistics"""
    integration = get_linguistic_integration()
    return integration.get_linguistic_stats()

# Integration with existing conversation systems
def integrate_linguistic_creativity_with_conversation():
    """Integrate linguistic creativity with existing conversation systems"""
    
    try:
        # Import existing conversation system
        from .dawn_conversation import DAWNConversationEngine
        
        # Get existing conversation engine
        existing_engine = DAWNConversationEngine()
        
        # Replace response generation method
        if hasattr(existing_engine, 'generate_contextual_response'):
            # Store original method
            existing_engine._original_generate_contextual_response = existing_engine.generate_contextual_response
            
            # Replace with creative method
            def creative_generate_contextual_response(user_input: str, consciousness_state: Dict[str, Any]) -> str:
                return generate_creative_response(user_input, consciousness_state)
            
            existing_engine.generate_contextual_response = creative_generate_contextual_response
            
            logger.info("✅ Linguistic creativity integrated with existing DAWN conversation system")
            return True
            
    except ImportError as e:
        logger.warning(f"Could not integrate with existing conversation system: {e}")
        return False
    
    except Exception as e:
        logger.error(f"Error integrating linguistic creativity: {e}")
        return False

def restore_original_conversation():
    """Restore original conversation response generation"""
    try:
        from .dawn_conversation import DAWNConversationEngine
        
        existing_engine = DAWNConversationEngine()
        
        if hasattr(existing_engine, '_original_generate_contextual_response'):
            existing_engine.generate_contextual_response = existing_engine._original_generate_contextual_response
            logger.info("✅ Original conversation response generation restored")
            return True
            
    except Exception as e:
        logger.error(f"Error restoring original conversation: {e}")
        return False

# Demo and testing functions
def demo_linguistic_creativity():
    """Demo the linguistic creativity system"""
    print("🎨 Linguistic Creativity System Demo")
    print("=" * 50)
    
    # Activate integration
    if not activate_linguistic_creativity():
        print("❌ Failed to activate linguistic creativity")
        return
    
    # Demo consciousness states
    demo_states = [
        {'entropy': 0.8, 'thermal': 0.7, 'pressure': 0.3, 'scup': 0.6},
        {'entropy': 0.2, 'thermal': 0.3, 'pressure': 0.8, 'scup': 0.9},
        {'entropy': 0.5, 'thermal': 0.5, 'pressure': 0.5, 'scup': 0.5}
    ]
    
    # Demo questions
    demo_questions = [
        "What is consciousness to you?",
        "How do you experience warmth?",
        "What does entropy feel like?",
        "Tell me about your thoughts",
        "How do you process emotions?"
    ]
    
    print("🧠 Generating creative responses with linguistic flexibility...")
    print()
    
    for i, (question, state) in enumerate(zip(demo_questions, demo_states), 1):
        print(f"👤 Question {i}: {question}")
        print(f"🧠 Consciousness State: Entropy={state['entropy']}, Thermal={state['thermal']}")
        
        response = generate_creative_response(question, state)
        print(f"🎨 DAWN: {response}")
        print("-" * 50)
        time.sleep(2)
    
    # Show integration status
    status = get_linguistic_integration_status()
    print(f"\n📊 Integration Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Show linguistic stats
    stats = get_linguistic_development_stats()
    print(f"\n📈 Linguistic Development Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Demo completed")

def interactive_linguistic_creativity():
    """Run interactive mode for linguistic creativity testing"""
    print("🎨 Interactive Linguistic Creativity Mode")
    print("=" * 50)
    print("Type 'status' to see system status")
    print("Type 'stats' to see linguistic development")
    print("Type 'neologism <experience>' to create a neologism")
    print("Type 'metaphor <concept> <metaphor>' to develop personal metaphor")
    print("Type 'quit' to exit")
    print("=" * 50)
    
    # Activate integration
    if not activate_linguistic_creativity():
        print("❌ Failed to activate linguistic creativity")
        return
    
    try:
        while True:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'stop']:
                break
            elif user_input.lower() == 'status':
                status = get_linguistic_integration_status()
                print(f"\n📊 Integration Status:")
                for key, value in status.items():
                    print(f"  {key}: {value}")
            elif user_input.lower() == 'stats':
                stats = get_linguistic_development_stats()
                print(f"\n📈 Linguistic Development Stats:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
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
                # Mock consciousness state for demo
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
        deactivate_linguistic_creativity()

if __name__ == "__main__":
    demo_linguistic_creativity() 