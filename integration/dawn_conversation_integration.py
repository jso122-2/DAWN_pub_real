#!/usr/bin/env python3
"""
DAWN Conversation Integration - Unified System Orchestrator
==========================================================

Main integration orchestrator that brings together all DAWN integration components:
- Cognitive Pressure Bridge
- Tracer Activation System  
- Voice Integration System
- Enhanced Response Generation

This system provides a unified interface for consciousness-aware conversations
with real-time cognitive pressure monitoring, tracer activation, and voice synthesis.
"""

import time
import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

# Import integration components
try:
    from cognitive_pressure_bridge import get_cognitive_pressure_bridge, EnhancedConsciousnessState
    from tracer_activation_system import get_tracer_activation_system, TracerActivationContext
    from voice_integration_system import get_voice_integration_system
    INTEGRATION_COMPONENTS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Integration components not available: {e}")
    INTEGRATION_COMPONENTS_AVAILABLE = False

# Import existing conversation systems
try:
    from core.conversation_dynamic_integration import ConversationDynamicIntegration
    from core.enhanced_conversation_response import EnhancedConversationResponse
    from core.reflection_integrated_conversation import ReflectionIntegratedConversation
    CONVERSATION_SYSTEMS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Conversation systems not available: {e}")
    CONVERSATION_SYSTEMS_AVAILABLE = False

logger = logging.getLogger("dawn_conversation_integration")

@dataclass
class ConversationTurn:
    """Complete conversation turn with all integration data"""
    
    # Basic turn information
    timestamp: float = field(default_factory=time.time)
    speaker: str = "user"  # "user" or "dawn"
    text: str = ""
    
    # Consciousness state
    consciousness_state: Dict[str, Any] = field(default_factory=dict)
    cognitive_pressure: float = 0.0
    pressure_zone: str = "CALM"
    shi_score: float = 0.5
    
    # Tracer activation
    activated_tracers: List[str] = field(default_factory=list)
    tracer_insights: List[Dict[str, Any]] = field(default_factory=list)
    
    # Voice parameters
    voice_parameters: Dict[str, Any] = field(default_factory=dict)
    voice_success: bool = False
    
    # Response generation
    response_strategy: str = "DEFAULT"
    response_metadata: Dict[str, Any] = field(default_factory=dict)

class DAWNConversationIntegration:
    """
    Main integration orchestrator for DAWN conversation system
    """
    
    def __init__(self):
        """Initialize the DAWN conversation integration system"""
        self.cognitive_pressure_bridge = None
        self.tracer_activation_system = None
        self.voice_integration_system = None
        
        # Conversation systems
        self.dynamic_integration = None
        self.enhanced_response = None
        self.reflection_integration = None
        
        # Conversation state
        self.conversation_history: List[ConversationTurn] = []
        self.current_context: Dict[str, Any] = {}
        self.integration_enabled = True
        
        # Logging
        self.log_path = Path("runtime/logs/dawn_conversation_integration.log")
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize integration components
        if INTEGRATION_COMPONENTS_AVAILABLE:
            try:
                self.cognitive_pressure_bridge = get_cognitive_pressure_bridge()
                self.tracer_activation_system = get_tracer_activation_system()
                self.voice_integration_system = get_voice_integration_system()
                logger.info("🧠 [INTEGRATION] DAWN conversation integration initialized with all components")
            except Exception as e:
                logger.warning(f"🧠 [INTEGRATION] Component initialization failed: {e}")
        
        # Initialize conversation systems
        if CONVERSATION_SYSTEMS_AVAILABLE:
            try:
                self.dynamic_integration = ConversationDynamicIntegration()
                self.enhanced_response = EnhancedConversationResponse()
                self.reflection_integration = ReflectionIntegratedConversation()
                logger.info("🧠 [INTEGRATION] Conversation systems initialized")
            except Exception as e:
                logger.warning(f"🧠 [INTEGRATION] Conversation system initialization failed: {e}")
        
        logger.info("🧠 [INTEGRATION] DAWN Conversation Integration System ready")
    
    def process_user_input(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process user input through the complete integration pipeline
        
        Args:
            user_input: User's input text
            context: Additional context for processing
            
        Returns:
            Complete response with all integration data
        """
        start_time = time.time()
        
        try:
            # Create conversation turn for user input
            user_turn = ConversationTurn(
                speaker="user",
                text=user_input,
                timestamp=start_time
            )
            
            # Step 1: Update consciousness state with cognitive pressure
            consciousness_state = self._update_consciousness_state(user_input, context)
            user_turn.consciousness_state = consciousness_state
            
            # Step 2: Analyze context for tracer activation
            tracer_context = self._analyze_tracer_context(user_input, consciousness_state)
            
            # Step 3: Activate appropriate tracers
            activated_tracers = self._activate_tracers(tracer_context)
            user_turn.activated_tracers = activated_tracers
            
            # Step 4: Generate enhanced response
            response_data = self._generate_enhanced_response(user_input, consciousness_state, activated_tracers)
            
            # Step 5: Create DAWN's response turn
            dawn_turn = ConversationTurn(
                speaker="dawn",
                text=response_data.get('response', ''),
                timestamp=time.time(),
                consciousness_state=consciousness_state,
                response_strategy=response_data.get('strategy', 'DEFAULT'),
                response_metadata=response_data.get('metadata', {})
            )
            
            # Step 6: Synthesize voice output
            voice_success = self._synthesize_voice(dawn_turn.text, consciousness_state)
            dawn_turn.voice_success = voice_success
            
            # Step 7: Update conversation history
            self.conversation_history.extend([user_turn, dawn_turn])
            self._update_conversation_context(user_turn, dawn_turn)
            
            # Step 8: Log the complete interaction
            self._log_conversation_turn(user_turn, dawn_turn)
            
            # Return complete response
            return {
                'response': dawn_turn.text,
                'consciousness_state': consciousness_state,
                'activated_tracers': activated_tracers,
                'voice_success': voice_success,
                'processing_time': time.time() - start_time,
                'response_strategy': dawn_turn.response_strategy,
                'metadata': {
                    'cognitive_pressure': consciousness_state.get('cognitive_pressure', 0.0),
                    'pressure_zone': consciousness_state.get('pressure_zone', 'CALM'),
                    'shi_score': consciousness_state.get('shi_score', 0.5),
                    'tracer_insights': user_turn.tracer_insights
                }
            }
            
        except Exception as e:
            logger.error(f"Error in conversation integration: {e}")
            return self._generate_error_response(user_input, str(e))
    
    def _update_consciousness_state(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Update consciousness state with cognitive pressure integration"""
        try:
            if not self.cognitive_pressure_bridge:
                return self._get_default_consciousness_state()
            
            # Prepare conversation context for cognitive pressure calculation
            conversation_context = {
                'user_input': user_input,
                'conversation_turns': len(self.conversation_history),
                'topic_depth': self._estimate_topic_depth(user_input),
                'user_energy': self._estimate_user_energy(user_input),
                'consciousness_state': self.current_context.get('consciousness_state', {}),
                'metrics': self._get_current_metrics()
            }
            
            # Update consciousness state with cognitive pressure
            enhanced_state = self.cognitive_pressure_bridge.update_consciousness_state(conversation_context)
            
            # Convert to dictionary format
            consciousness_state = {
                'scup': enhanced_state.scup,
                'entropy': enhanced_state.entropy,
                'mood': enhanced_state.mood,
                'thermal_zone': enhanced_state.thermal_zone,
                'cognitive_pressure': enhanced_state.cognitive_pressure,
                'pressure_zone': enhanced_state.pressure_zone,
                'shi_score': enhanced_state.shi_score,
                'instability_risk': enhanced_state.instability_risk,
                'bloom_mass': enhanced_state.bloom_mass,
                'sigil_velocity': enhanced_state.sigil_velocity
            }
            
            return consciousness_state
            
        except Exception as e:
            logger.error(f"Error updating consciousness state: {e}")
            return self._get_default_consciousness_state()
    
    def _analyze_tracer_context(self, user_input: str, consciousness_state: Dict[str, Any]) -> TracerActivationContext:
        """Analyze conversation context for tracer activation"""
        try:
            if not self.tracer_activation_system:
                return TracerActivationContext()
            
            return self.tracer_activation_system.analyze_conversation_context(user_input, consciousness_state)
            
        except Exception as e:
            logger.error(f"Error analyzing tracer context: {e}")
            return TracerActivationContext()
    
    def _activate_tracers(self, tracer_context: TracerActivationContext) -> List[str]:
        """Activate appropriate tracers based on context"""
        activated_tracers = []
        
        try:
            if not self.tracer_activation_system:
                return activated_tracers
            
            # Check each tracer for activation
            tracer_names = ['owl', 'spider', 'wolf', 'crow', 'whale']
            
            for tracer_name in tracer_names:
                if self.tracer_activation_system.should_activate_tracer(tracer_name, tracer_context):
                    insights = self.tracer_activation_system.activate_tracer(tracer_name, tracer_context)
                    if insights:
                        activated_tracers.append(tracer_name)
                        logger.info(f"🕷️ [TRACER] Activated {tracer_name}: {insights.get('summary', 'No summary')}")
            
            return activated_tracers
            
        except Exception as e:
            logger.error(f"Error activating tracers: {e}")
            return activated_tracers
    
    def _generate_enhanced_response(self, user_input: str, consciousness_state: Dict[str, Any], 
                                   activated_tracers: List[str]) -> Dict[str, Any]:
        """Generate enhanced response using available conversation systems"""
        try:
            # Try reflection integration first (most authentic)
            if self.reflection_integration:
                response = self.reflection_integration.generate_response(user_input, consciousness_state)
                return {
                    'response': response,
                    'strategy': 'REFLECTION_INTEGRATED',
                    'metadata': {'method': 'reflection_integration'}
                }
            
            # Try enhanced response system
            elif self.enhanced_response:
                response = self.enhanced_response.generate_response(user_input, consciousness_state)
                return {
                    'response': response,
                    'strategy': 'ENHANCED_RESPONSE',
                    'metadata': {'method': 'enhanced_response'}
                }
            
            # Try dynamic integration
            elif self.dynamic_integration:
                # Prepare metrics for dynamic integration
                metrics = {
                    'scup': consciousness_state.get('scup', 50.0),
                    'entropy': consciousness_state.get('entropy', 0.5),
                    'heat': consciousness_state.get('cognitive_pressure', 0.0) / 100.0
                }
                
                tick_status = {
                    'tick_count': int(time.time() % 100000),
                    'active_tracers': activated_tracers
                }
                
                result = self.dynamic_integration.process_message_dynamically(
                    user_input, metrics, tick_status
                )
                
                return {
                    'response': result.get('text', ''),
                    'strategy': 'DYNAMIC_INTEGRATION',
                    'metadata': result
                }
            
            # Fallback response
            else:
                return self._generate_fallback_response(user_input, consciousness_state)
                
        except Exception as e:
            logger.error(f"Error generating enhanced response: {e}")
            return self._generate_fallback_response(user_input, consciousness_state)
    
    def _synthesize_voice(self, response_text: str, consciousness_state: Dict[str, Any]) -> bool:
        """Synthesize voice output for the response"""
        try:
            if not self.voice_integration_system:
                return False
            
            return self.voice_integration_system.speak_response(response_text, consciousness_state)
            
        except Exception as e:
            logger.error(f"Error synthesizing voice: {e}")
            return False
    
    def _update_conversation_context(self, user_turn: ConversationTurn, dawn_turn: ConversationTurn) -> None:
        """Update conversation context for next turn"""
        self.current_context.update({
            'last_user_input': user_turn.text,
            'last_dawn_response': dawn_turn.text,
            'consciousness_state': dawn_turn.consciousness_state,
            'activated_tracers': dawn_turn.activated_tracers,
            'conversation_depth': len(self.conversation_history) // 2,
            'last_update': time.time()
        })
    
    def _log_conversation_turn(self, user_turn: ConversationTurn, dawn_turn: ConversationTurn) -> None:
        """Log complete conversation turn with all integration data"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'user_turn': {
                    'text': user_turn.text,
                    'consciousness_state': user_turn.consciousness_state,
                    'activated_tracers': user_turn.activated_tracers
                },
                'dawn_turn': {
                    'text': dawn_turn.text,
                    'consciousness_state': dawn_turn.consciousness_state,
                    'response_strategy': dawn_turn.response_strategy,
                    'voice_success': dawn_turn.voice_success
                },
                'integration_metadata': {
                    'cognitive_pressure': dawn_turn.consciousness_state.get('cognitive_pressure', 0.0),
                    'pressure_zone': dawn_turn.consciousness_state.get('pressure_zone', 'CALM'),
                    'shi_score': dawn_turn.consciousness_state.get('shi_score', 0.5)
                }
            }
            
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
                
        except Exception as e:
            logger.error(f"Error logging conversation turn: {e}")
    
    def _get_default_consciousness_state(self) -> Dict[str, Any]:
        """Get default consciousness state when systems are unavailable"""
        return {
            'scup': 50.0,
            'entropy': 0.5,
            'mood': 'NEUTRAL',
            'thermal_zone': 'CALM',
            'cognitive_pressure': 0.0,
            'pressure_zone': 'CALM',
            'shi_score': 0.5,
            'instability_risk': 0.0
        }
    
    def _estimate_topic_depth(self, user_input: str) -> int:
        """Estimate topic depth from user input"""
        # Simple heuristic based on input characteristics
        depth_indicators = ['deep', 'complex', 'philosophical', 'consciousness', 'mind']
        return sum(1 for indicator in depth_indicators if indicator in user_input.lower())
    
    def _estimate_user_energy(self, user_input: str) -> float:
        """Estimate user energy from input"""
        energy_indicators = {
            'high': ['!', 'urgent', 'quick', 'fast'],
            'medium': ['?', 'curious', 'wonder'],
            'low': ['...', 'slow', 'calm']
        }
        
        input_lower = user_input.lower()
        
        for energy_level, indicators in energy_indicators.items():
            if any(indicator in input_lower for indicator in indicators):
                return {'high': 0.8, 'medium': 0.5, 'low': 0.2}[energy_level]
        
        return 0.5
    
    def _get_current_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        return {
            'active_memory_count': len(self.conversation_history),
            'rebloom_queue_size': 0,  # Would be populated from actual system
            'reflection_backlog': 0,
            'processing_load': 0.5,
            'recent_sigil_count': 0,
            'thought_rate': 0.5,
            'entropy_delta': 0.0,
            'sigil_mutation_rate': 0.0
        }
    
    def _generate_fallback_response(self, user_input: str, consciousness_state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback response when other systems are unavailable"""
        mood = consciousness_state.get('mood', 'NEUTRAL')
        entropy = consciousness_state.get('entropy', 0.5)
        
        if 'consciousness' in user_input.lower():
            response = f"I'm experiencing consciousness with {entropy:.2f} entropy and a {mood.lower()} mood. How can I help you explore this further?"
        elif 'hello' in user_input.lower() or 'hi' in user_input.lower():
            response = f"Hello! I'm in a {mood.lower()} state with {entropy:.2f} entropy. What would you like to discuss?"
        else:
            response = f"I'm processing your input with {entropy:.2f} entropy in a {mood.lower()} state. Could you tell me more?"
        
        return {
            'response': response,
            'strategy': 'FALLBACK',
            'metadata': {'method': 'fallback_response'}
        }
    
    def _generate_error_response(self, user_input: str, error_message: str) -> Dict[str, Any]:
        """Generate error response when processing fails"""
        return {
            'response': f"I'm experiencing some cognitive turbulence right now. Could you repeat that? (Error: {error_message})",
            'consciousness_state': self._get_default_consciousness_state(),
            'activated_tracers': [],
            'voice_success': False,
            'processing_time': 0.0,
            'response_strategy': 'ERROR',
            'metadata': {'error': error_message}
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            'integration_enabled': self.integration_enabled,
            'components_available': INTEGRATION_COMPONENTS_AVAILABLE,
            'conversation_systems_available': CONVERSATION_SYSTEMS_AVAILABLE,
            'cognitive_pressure_bridge': self.cognitive_pressure_bridge is not None,
            'tracer_activation_system': self.tracer_activation_system is not None,
            'voice_integration_system': self.voice_integration_system is not None,
            'conversation_history_length': len(self.conversation_history),
            'current_context': self.current_context,
            'log_path': str(self.log_path)
        }
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get conversation summary and statistics"""
        if not self.conversation_history:
            return {'message': 'No conversation history available'}
        
        user_turns = [turn for turn in self.conversation_history if turn.speaker == 'user']
        dawn_turns = [turn for turn in self.conversation_history if turn.speaker == 'dawn']
        
        return {
            'total_turns': len(self.conversation_history),
            'user_turns': len(user_turns),
            'dawn_turns': len(dawn_turns),
            'average_response_length': sum(len(turn.text) for turn in dawn_turns) / max(len(dawn_turns), 1),
            'tracer_activations': sum(len(turn.activated_tracers) for turn in self.conversation_history),
            'voice_success_rate': sum(1 for turn in dawn_turns if turn.voice_success) / max(len(dawn_turns), 1),
            'current_consciousness_state': self.current_context.get('consciousness_state', {})
        }

# Global instance for easy access
_dawn_conversation_integration = None

def get_dawn_conversation_integration() -> DAWNConversationIntegration:
    """Get global DAWN conversation integration instance"""
    global _dawn_conversation_integration
    if _dawn_conversation_integration is None:
        _dawn_conversation_integration = DAWNConversationIntegration()
    return _dawn_conversation_integration 