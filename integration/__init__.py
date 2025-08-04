#!/usr/bin/env python3
"""
DAWN Conversation Integration Package
====================================

This package provides a unified interface for consciousness-aware conversations
with real-time cognitive pressure monitoring, tracer activation, and voice synthesis.

Main Components:
- Cognitive Pressure Bridge
- Tracer Activation System
- Voice Integration System
- Main Integration Orchestrator
"""

# Import main integration components
try:
    from .dawn_conversation_integration import (
        get_dawn_conversation_integration,
        DAWNConversationIntegration,
        ConversationTurn
    )
    from .cognitive_pressure_bridge import (
        get_cognitive_pressure_bridge,
        CognitivePressureBridge,
        EnhancedConsciousnessState
    )
    from .tracer_activation_system import (
        get_tracer_activation_system,
        TracerActivationSystem,
        TracerActivationContext
    )
    from .voice_integration_system import (
        get_voice_integration_system,
        VoiceIntegrationSystem,
        VoiceParameters
    )
    
    # Main integration function
    def get_integration_system():
        """Get the main DAWN conversation integration system"""
        return get_dawn_conversation_integration()
    
    # Quick start function
    def process_conversation(user_input: str, context: dict = None) -> dict:
        """
        Quick function to process a conversation turn
        
        Args:
            user_input: User's input text
            context: Optional additional context
            
        Returns:
            Complete response with all integration data
        """
        integration = get_dawn_conversation_integration()
        return integration.process_user_input(user_input, context)
    
    __all__ = [
        # Main integration
        'get_dawn_conversation_integration',
        'DAWNConversationIntegration',
        'ConversationTurn',
        'get_integration_system',
        'process_conversation',
        
        # Cognitive pressure bridge
        'get_cognitive_pressure_bridge',
        'CognitivePressureBridge',
        'EnhancedConsciousnessState',
        
        # Tracer activation system
        'get_tracer_activation_system',
        'TracerActivationSystem',
        'TracerActivationContext',
        
        # Voice integration system
        'get_voice_integration_system',
        'VoiceIntegrationSystem',
        'VoiceParameters'
    ]
    
except ImportError as e:
    # If components are not available, provide fallback
    print(f"Warning: Some DAWN integration components are not available: {e}")
    
    def get_integration_system():
        """Fallback integration system when components are unavailable"""
        print("Warning: DAWN integration components are not available")
        return None
    
    def process_conversation(user_input: str, context: dict = None) -> dict:
        """Fallback conversation processing"""
        return {
            'response': f"I'm experiencing some cognitive turbulence. Could you repeat that? (Components unavailable: {e})",
            'consciousness_state': {'scup': 50.0, 'entropy': 0.5, 'mood': 'NEUTRAL'},
            'activated_tracers': [],
            'voice_success': False,
            'processing_time': 0.0,
            'response_strategy': 'FALLBACK',
            'metadata': {'error': 'Components unavailable'}
        }
    
    __all__ = ['get_integration_system', 'process_conversation']

# Package metadata
__version__ = "1.0.0"
__author__ = "DAWN Development Team"
__description__ = "DAWN Conversation Integration System - Consciousness-aware conversations with real-time cognitive monitoring"

# Package info
def get_package_info():
    """Get package information and component status"""
    try:
        integration = get_dawn_conversation_integration()
        if integration:
            status = integration.get_system_status()
            return {
                'version': __version__,
                'description': __description__,
                'components_available': status.get('components_available', False),
                'conversation_systems_available': status.get('conversation_systems_available', False),
                'integration_enabled': status.get('integration_enabled', False),
                'status': 'operational' if status.get('integration_enabled') else 'limited'
            }
        else:
            return {
                'version': __version__,
                'description': __description__,
                'components_available': False,
                'conversation_systems_available': False,
                'integration_enabled': False,
                'status': 'unavailable'
            }
    except Exception as e:
        return {
            'version': __version__,
            'description': __description__,
            'components_available': False,
            'conversation_systems_available': False,
            'integration_enabled': False,
            'status': f'error: {e}'
        }

# Quick status check
def check_system_status():
    """Quick check of system status"""
    info = get_package_info()
    print(f"🧠 DAWN Integration System v{info['version']}")
    print(f"Status: {info['status']}")
    print(f"Components available: {info['components_available']}")
    print(f"Conversation systems: {info['conversation_systems_available']}")
    return info

if __name__ == "__main__":
    # Run status check when package is executed directly
    check_system_status() 