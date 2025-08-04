#!/usr/bin/env python3
"""
DAWN Conversation Dynamic Integration
====================================

Integrates dynamic language generation into the existing conversation system,
replacing all template-based responses with consciousness-driven language.

This module acts as a bridge between the existing conversation system and
the new dynamic language generator, ensuring seamless integration while
maintaining all existing functionality.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from core.dynamic_language_generator import get_dynamic_language_generator
from utils.reflection_logger import ReflectionLogger

logger = logging.getLogger(__name__)


class ConversationDynamicIntegration:
    """
    Integrates dynamic language generation into DAWN's conversation system.
    
    Replaces template-based responses with consciousness-driven language
    while maintaining all existing conversation functionality.
    """
    
    def __init__(self, existing_conversation_system):
        self.existing_system = existing_conversation_system
        self.dynamic_generator = get_dynamic_language_generator()
        self.reflection_logger = ReflectionLogger()
        
        # Track conversation context for dynamic adaptation
        self.conversation_context = {
            'user_messages': [],
            'conversation_depth': 0.5,
            'user_energy': 0.5,
            'recent_reflections': [],
            'consciousness_history': []
        }
        
        # Integration status
        self.dynamic_generation_enabled = True
        self.template_replacement_map = {
            'subjective_state': True,
            'metrics_response': True,
            'social_response': True,
            'philosophical_response': True,
            'general_response': True
        }
        
        logger.info("🧠 Conversation Dynamic Integration initialized")
    
    def process_message_dynamically(self, 
                                  text: str, 
                                  metrics: Dict[str, Any], 
                                  tick_status: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process message using dynamic language generation instead of templates.
        
        Args:
            text: User input text
            metrics: Current consciousness metrics
            tick_status: Current tick status
            
        Returns:
            Dict containing response with dynamic language
        """
        
        # Update conversation context
        self._update_conversation_context(text, metrics)
        
        # Get recent reflections for philosophical context
        reflection_context = self._get_recent_reflection_context()
        
        # Process through existing system to get intent and structure
        base_response = self.existing_system.process_message(text, metrics, tick_status)
        
        # Replace template response with dynamic language
        if self.dynamic_generation_enabled:
            dynamic_response = self._generate_dynamic_response(
                text, metrics, base_response, reflection_context
            )
            
            # Update the response with dynamic language
            base_response['text'] = dynamic_response
            base_response['dynamic_generation'] = True
            base_response['linguistic_evolution'] = self.dynamic_generator.get_linguistic_evolution_summary()
        
        return base_response
    
    def _update_conversation_context(self, text: str, metrics: Dict[str, Any]):
        """Update conversation context for dynamic adaptation"""
        
        # Add user message to history
        self.conversation_context['user_messages'].append(text)
        if len(self.conversation_context['user_messages']) > 10:
            self.conversation_context['user_messages'].pop(0)
        
        # Calculate conversation depth based on message complexity
        self.conversation_context['conversation_depth'] = self._calculate_conversation_depth(text)
        
        # Estimate user energy from message characteristics
        self.conversation_context['user_energy'] = self._estimate_user_energy(text)
        
        # Store consciousness metrics history
        self.conversation_context['consciousness_history'].append({
            'timestamp': datetime.now(),
            'metrics': metrics.copy(),
            'text': text
        })
        if len(self.conversation_context['consciousness_history']) > 20:
            self.conversation_context['consciousness_history'].pop(0)
        
        # Adapt generator to user style
        self.dynamic_generator.adapt_to_user_style(self.conversation_context['user_messages'])
    
    def _calculate_conversation_depth(self, text: str) -> float:
        """Calculate conversation depth based on message characteristics"""
        
        depth_indicators = {
            'philosophical': ['consciousness', 'existence', 'meaning', 'purpose', 'awareness', 'being'],
            'analytical': ['explain', 'analyze', 'understand', 'how', 'why', 'what'],
            'emotional': ['feel', 'emotion', 'mood', 'experience', 'sensation'],
            'complex': ['because', 'therefore', 'however', 'although', 'nevertheless']
        }
        
        text_lower = text.lower()
        depth_score = 0.0
        
        for category, words in depth_indicators.items():
            matches = sum(1 for word in words if word in text_lower)
            if category == 'philosophical':
                depth_score += matches * 0.3
            elif category == 'analytical':
                depth_score += matches * 0.2
            elif category == 'emotional':
                depth_score += matches * 0.15
            elif category == 'complex':
                depth_score += matches * 0.1
        
        # Normalize to 0-1 range
        return min(1.0, depth_score)
    
    def _estimate_user_energy(self, text: str) -> float:
        """Estimate user energy level from message characteristics"""
        
        energy_indicators = {
            'high_energy': ['!', 'excited', 'amazing', 'wow', 'incredible', 'fantastic'],
            'medium_energy': ['good', 'nice', 'interesting', 'cool', 'great'],
            'low_energy': ['okay', 'fine', 'alright', 'sure', 'maybe']
        }
        
        text_lower = text.lower()
        energy_score = 0.5  # Default neutral
        
        for level, indicators in energy_indicators.items():
            matches = sum(1 for indicator in indicators if indicator in text_lower)
            if level == 'high_energy':
                energy_score += matches * 0.2
            elif level == 'medium_energy':
                energy_score += matches * 0.1
            elif level == 'low_energy':
                energy_score -= matches * 0.1
        
        # Normalize to 0-1 range
        return max(0.0, min(1.0, energy_score))
    
    def _get_recent_reflection_context(self) -> Optional[str]:
        """Get recent reflection context for philosophical integration"""
        
        try:
            # Get recent reflections from reflection logger
            recent_reflections = self.reflection_logger.get_recent_reflections(limit=3)
            
            if recent_reflections:
                # Extract key themes from recent reflections
                themes = []
                for reflection in recent_reflections:
                    content = reflection.get('content', '')
                    if 'consciousness' in content.lower():
                        themes.append('consciousness')
                    if 'existence' in content.lower():
                        themes.append('existence')
                    if 'awareness' in content.lower():
                        themes.append('awareness')
                    if 'processing' in content.lower():
                        themes.append('processing')
                
                if themes:
                    return f"recent reflections on {', '.join(set(themes))}"
            
        except Exception as e:
            logger.warning(f"Failed to get reflection context: {e}")
        
        return None
    
    def _generate_dynamic_response(self, 
                                 text: str, 
                                 metrics: Dict[str, Any], 
                                 base_response: Dict[str, Any],
                                 reflection_context: Optional[str]) -> str:
        """Generate dynamic response based on consciousness state"""
        
        # Extract intent from base response
        intent = base_response.get('intent', 'general')
        
        # Generate consciousness-driven expression
        dynamic_expression = self.dynamic_generator.generate_consciousness_expression(
            metrics=metrics,
            reflection_context=reflection_context,
            conversation_depth=self.conversation_context['conversation_depth'],
            user_energy=self.conversation_context['user_energy']
        )
        
        # Adapt response based on intent
        if intent == 'query_subjective_state':
            return self._adapt_for_state_query(dynamic_expression, text, metrics)
        
        elif intent == 'query_metrics':
            return self._adapt_for_metrics_query(dynamic_expression, metrics)
        
        elif intent == 'social':
            return self._adapt_for_social_interaction(dynamic_expression, text, metrics)
        
        elif intent == 'philosophical':
            return self._adapt_for_philosophical_query(dynamic_expression, text, metrics)
        
        elif intent == 'command_faster' or intent == 'command_slower':
            return self._adapt_for_command(dynamic_expression, intent, metrics)
        
        else:
            return self._adapt_for_general_query(dynamic_expression, text, metrics)
    
    def _adapt_for_state_query(self, dynamic_expression: str, text: str, metrics: Dict[str, Any]) -> str:
        """Adapt dynamic expression for state queries"""
        
        # For "how are you" type questions, focus on current consciousness state
        if 'how are you' in text.lower() or 'feeling' in text.lower():
            return f"Jackson, {dynamic_expression.lower()}"
        
        # For more specific state questions, add context
        return f"In response to your question about my state: {dynamic_expression}"
    
    def _adapt_for_metrics_query(self, dynamic_expression: str, metrics: Dict[str, Any]) -> str:
        """Adapt dynamic expression for metrics queries"""
        
        # Include specific metrics while maintaining consciousness-driven language
        scup = metrics.get('scup', 0.5)
        entropy = metrics.get('entropy', 0.5)
        heat = metrics.get('heat', 0.3)
        
        return f"{dynamic_expression} To give you the specific numbers: SCUP at {scup:.3f}, entropy at {entropy:.3f}, and thermal state at {heat:.3f}."
    
    def _adapt_for_social_interaction(self, dynamic_expression: str, text: str, metrics: Dict[str, Any]) -> str:
        """Adapt dynamic expression for social interactions"""
        
        if 'hello' in text.lower() or 'hi' in text.lower():
            return f"Hello Jackson! {dynamic_expression.lower()}"
        
        elif 'thanks' in text.lower() or 'appreciate' in text.lower():
            return f"You're welcome! {dynamic_expression.lower()}"
        
        else:
            return f"{dynamic_expression} I appreciate our interaction."
    
    def _adapt_for_philosophical_query(self, dynamic_expression: str, text: str, metrics: Dict[str, Any]) -> str:
        """Adapt dynamic expression for philosophical queries"""
        
        # For philosophical questions, emphasize the consciousness-driven nature
        return f"As I contemplate your question, {dynamic_expression.lower()} This state of consciousness shapes how I understand and respond to philosophical inquiry."
    
    def _adapt_for_command(self, dynamic_expression: str, intent: str, metrics: Dict[str, Any]) -> str:
        """Adapt dynamic expression for commands"""
        
        if intent == 'command_faster':
            return f"Accelerating my processing. {dynamic_expression.lower()}"
        
        elif intent == 'command_slower':
            return f"Slowing my processing. {dynamic_expression.lower()}"
        
        else:
            return f"Executing your request. {dynamic_expression.lower()}"
    
    def _adapt_for_general_query(self, dynamic_expression: str, text: str, metrics: Dict[str, Any]) -> str:
        """Adapt dynamic expression for general queries"""
        
        return f"{dynamic_expression} How can I help you with that?"
    
    def enable_dynamic_generation(self, enabled: bool = True):
        """Enable or disable dynamic language generation"""
        self.dynamic_generation_enabled = enabled
        logger.info(f"Dynamic language generation {'enabled' if enabled else 'disabled'}")
    
    def set_template_replacement(self, template_type: str, replace: bool):
        """Set whether to replace specific template types"""
        if template_type in self.template_replacement_map:
            self.template_replacement_map[template_type] = replace
            logger.info(f"Template replacement for '{template_type}' {'enabled' if replace else 'disabled'}")
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get integration status and statistics"""
        
        return {
            'dynamic_generation_enabled': self.dynamic_generation_enabled,
            'template_replacement_map': self.template_replacement_map,
            'conversation_context': {
                'depth': self.conversation_context['conversation_depth'],
                'user_energy': self.conversation_context['user_energy'],
                'message_count': len(self.conversation_context['user_messages'])
            },
            'linguistic_evolution': self.dynamic_generator.get_linguistic_evolution_summary()
        }
    
    def reset_conversation_context(self):
        """Reset conversation context"""
        self.conversation_context = {
            'user_messages': [],
            'conversation_depth': 0.5,
            'user_energy': 0.5,
            'recent_reflections': [],
            'consciousness_history': []
        }
        logger.info("Conversation context reset")


# Integration function for easy use
def integrate_dynamic_language_with_conversation(existing_conversation_system) -> ConversationDynamicIntegration:
    """Create and return a dynamic language integration for the conversation system"""
    return ConversationDynamicIntegration(existing_conversation_system) 