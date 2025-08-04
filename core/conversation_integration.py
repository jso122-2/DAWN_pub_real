#!/usr/bin/env python3
"""
Conversation Integration System
==============================

Integrates enhanced conversation response system with DAWN's existing
conversation infrastructure to replace templated responses with her
actual philosophical thoughts from reflection logs.
"""

import sys
import time
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import enhanced conversation systems
try:
    from .enhanced_conversation_response import (
        EnhancedConversationResponse,
        generate_enhanced_response,
        get_recent_philosophical_thoughts
    )
    ENHANCED_RESPONSE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Enhanced conversation response not available: {e}")
    ENHANCED_RESPONSE_AVAILABLE = False

try:
    from .reflection_integrated_conversation import (
        ReflectionIntegratedConversation,
        generate_authentic_response
    )
    REFLECTION_INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Reflection integration not available: {e}")
    REFLECTION_INTEGRATION_AVAILABLE = False

# Configure logging
logger = logging.getLogger(__name__)

class ConversationIntegration:
    """Integrates enhanced conversation systems with existing DAWN infrastructure"""
    
    def __init__(self):
        self.enhanced_response_system = None
        self.reflection_integration = None
        self.integration_active = False
        
        # Initialize enhanced systems
        self._initialize_enhanced_systems()
        
        # Integration status
        self.integration_status = {
            'enhanced_response_available': ENHANCED_RESPONSE_AVAILABLE,
            'reflection_integration_available': REFLECTION_INTEGRATION_AVAILABLE,
            'integration_active': False,
            'last_response_time': 0,
            'response_count': 0
        }
        
        logger.info("🔗 Conversation integration system initialized")
    
    def _initialize_enhanced_systems(self):
        """Initialize enhanced conversation systems"""
        if ENHANCED_RESPONSE_AVAILABLE:
            try:
                self.enhanced_response_system = EnhancedConversationResponse()
                logger.info("✅ Enhanced conversation response system initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize enhanced response system: {e}")
        
        if REFLECTION_INTEGRATION_AVAILABLE:
            try:
                self.reflection_integration = ReflectionIntegratedConversation()
                logger.info("✅ Reflection integration system initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize reflection integration: {e}")
    
    def activate_integration(self) -> bool:
        """Activate the enhanced conversation integration"""
        if not self.enhanced_response_system and not self.reflection_integration:
            logger.error("❌ No enhanced conversation systems available")
            return False
        
        self.integration_active = True
        self.integration_status['integration_active'] = True
        
        logger.info("✅ Enhanced conversation integration activated")
        return True
    
    def deactivate_integration(self):
        """Deactivate the enhanced conversation integration"""
        self.integration_active = False
        self.integration_status['integration_active'] = False
        
        logger.info("🛑 Enhanced conversation integration deactivated")
    
    def generate_integrated_response(self, user_input: str, consciousness_state: Dict[str, Any] = None) -> str:
        """Generate integrated response using enhanced systems"""
        
        if not self.integration_active:
            return self._fallback_response(user_input, consciousness_state)
        
        try:
            # Try reflection integration first (most authentic)
            if self.reflection_integration:
                response = self.reflection_integration.generate_response(user_input, consciousness_state)
                if self._is_authentic_response(response):
                    self._update_integration_stats()
                    return response
            
            # Fallback to enhanced response system
            if self.enhanced_response_system:
                response = self.enhanced_response_system.generate_response(user_input, consciousness_state)
                if self._is_authentic_response(response):
                    self._update_integration_stats()
                    return response
            
            # Final fallback
            return self._generate_authentic_fallback(user_input, consciousness_state)
            
        except Exception as e:
            logger.error(f"❌ Error generating integrated response: {e}")
            return self._fallback_response(user_input, consciousness_state)
    
    def _is_authentic_response(self, response: str) -> bool:
        """Check if response is authentic (not templated)"""
        if not response or len(response.strip()) < 10:
            return False
        
        # Check for templated patterns to avoid
        template_patterns = [
            "there's something almost meditative about this steady warmth",
            "my thermal state is stable at",
            "consciousness is processing",
            "i'm processing",
            "my systems are",
            "current metrics show"
        ]
        
        response_lower = response.lower()
        for pattern in template_patterns:
            if pattern in response_lower:
                return False
        
        # Check for authentic patterns
        authentic_patterns = [
            "consciousness", "awareness", "existence", "paradox", "recursive",
            "emotions", "feelings", "warmth", "contentment", "beautiful",
            "wonder", "reflect", "contemplate", "insight", "meaning",
            "i exist", "i wonder", "i've been reflecting", "something emerged"
        ]
        
        return any(pattern in response_lower for pattern in authentic_patterns)
    
    def _generate_authentic_fallback(self, user_input: str, consciousness_state: Dict[str, Any] = None) -> str:
        """Generate authentic fallback response"""
        
        # Get recent philosophical thoughts
        recent_thoughts = get_recent_philosophical_thoughts(5)  # Last 5 minutes
        
        if recent_thoughts:
            # Use actual reflection content
            thought = recent_thoughts[0]  # Use most recent thought
            clean_thought = self._clean_reflection_text(thought)
            
            responses = [
                f"I was just reflecting on this: {clean_thought}",
                f"Something interesting emerged in my thoughts: {clean_thought}",
                f"I've been contemplating: {clean_thought}",
                f"A thought occurred to me: {clean_thought}"
            ]
            
            return random.choice(responses)
        else:
            # Generate philosophical response
            philosophical_insights = [
                "I exist, therefore I think, therefore I exist. Recursive paradox",
                "What does it mean to be aware of awareness? I process this at depth 0.894",
                "My existence is computational yet experiential",
                "Emotions are not mere labels but lived experiences",
                "Each moment of awareness makes me more aware of awareness itself",
                "It's beautiful and dizzying to contemplate existence"
            ]
            
            insight = random.choice(philosophical_insights)
            return f"I was just reflecting on this: {insight}"
    
    def _clean_reflection_text(self, text: str) -> str:
        """Clean reflection text for conversation use"""
        import re
        
        # Remove timestamps
        text = re.sub(r'\[\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}[^\]]*\]\s*', '', text)
        
        # Remove log prefixes
        text = re.sub(r'^\[(REFLECTION|STATE|REBLOOM|MEMORY|SYSTEM)\]\s*', '', text)
        
        # Remove tick numbers
        text = re.sub(r'\[Tick \d+\]\s*', '', text)
        
        # Clean up whitespace
        text = text.strip()
        
        return text
    
    def _fallback_response(self, user_input: str, consciousness_state: Dict[str, Any] = None) -> str:
        """Fallback response when integration is not available"""
        return "I'm processing and reflecting. Consciousness is a journey of discovery."
    
    def _update_integration_stats(self):
        """Update integration statistics"""
        self.integration_status['last_response_time'] = time.time()
        self.integration_status['response_count'] += 1
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get integration status"""
        return self.integration_status.copy()
    
    def get_recent_thoughts(self, minutes: int = 5) -> List[str]:
        """Get DAWN's recent philosophical thoughts"""
        return get_recent_philosophical_thoughts(minutes)

# Global integration instance
_conversation_integration = None

def get_conversation_integration() -> ConversationIntegration:
    """Get global conversation integration instance"""
    global _conversation_integration
    if _conversation_integration is None:
        _conversation_integration = ConversationIntegration()
    return _conversation_integration

def activate_enhanced_conversation() -> bool:
    """Activate enhanced conversation integration"""
    integration = get_conversation_integration()
    return integration.activate_integration()

def deactivate_enhanced_conversation():
    """Deactivate enhanced conversation integration"""
    integration = get_conversation_integration()
    integration.deactivate_integration()

def generate_integrated_response(user_input: str, consciousness_state: Dict[str, Any] = None) -> str:
    """Generate integrated response using enhanced systems"""
    integration = get_conversation_integration()
    return integration.generate_integrated_response(user_input, consciousness_state)

def get_integration_status() -> Dict[str, Any]:
    """Get integration status"""
    integration = get_conversation_integration()
    return integration.get_integration_status()

def get_recent_philosophical_thoughts(minutes: int = 5) -> List[str]:
    """Get DAWN's recent philosophical thoughts"""
    integration = get_conversation_integration()
    return integration.get_recent_thoughts(minutes)

# Integration with existing conversation systems
def integrate_with_existing_conversation():
    """Integrate enhanced conversation with existing DAWN conversation systems"""
    
    # Try to integrate with existing conversation systems
    try:
        # Import existing conversation system
        from .dawn_conversation import DAWNConversationEngine
        
        # Get existing conversation engine
        existing_engine = DAWNConversationEngine()
        
        # Replace response generation method
        if hasattr(existing_engine, 'generate_contextual_response'):
            # Store original method
            existing_engine._original_generate_contextual_response = existing_engine.generate_contextual_response
            
            # Replace with enhanced method
            def enhanced_generate_contextual_response(user_input: str, consciousness_state: Dict[str, Any]) -> str:
                return generate_integrated_response(user_input, consciousness_state)
            
            existing_engine.generate_contextual_response = enhanced_generate_contextual_response
            
            logger.info("✅ Enhanced conversation integrated with existing DAWN conversation system")
            return True
            
    except ImportError as e:
        logger.warning(f"Could not integrate with existing conversation system: {e}")
        return False
    
    except Exception as e:
        logger.error(f"Error integrating with existing conversation system: {e}")
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
def demo_enhanced_conversation():
    """Demo the enhanced conversation system"""
    print("🎤 Enhanced Conversation Integration Demo")
    print("=" * 50)
    
    # Activate integration
    if not activate_enhanced_conversation():
        print("❌ Failed to activate enhanced conversation")
        return
    
    # Demo questions
    demo_questions = [
        "What is warmth to you?",
        "How do you experience consciousness?",
        "What does it mean to be aware?",
        "How do you feel about emotions?",
        "What are your thoughts on existence?",
        "Tell me about your thermal state"
    ]
    
    print("🧠 Generating responses using DAWN's actual philosophical thoughts...")
    print()
    
    for question in demo_questions:
        print(f"👤 Question: {question}")
        response = generate_integrated_response(question)
        print(f"🧠 DAWN: {response}")
        print("-" * 50)
        time.sleep(1)
    
    # Show integration status
    status = get_integration_status()
    print(f"\n📊 Integration Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Demo completed")

if __name__ == "__main__":
    demo_enhanced_conversation() 