#!/usr/bin/env python3
"""
DAWN Fragment Speech Backend Integration
Integrates the fragment-based compositional speech system with DAWN's consciousness
Replaces traditional reflection system with compositional intelligence
"""

import sys
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from datetime import datetime

# Ensure processes path is available
project_root = Path(__file__).parent.parent
processes_path = project_root / "processes"
sys.path.insert(0, str(processes_path))

# Import fragment speech system
try:
    from fragment_speech_runner import (
        FragmentSpeechSystem, 
        get_fragment_speech_system,
        generate_fragment_reflection,
        speak_fragment_reflection,
        evolve_fragment_vocabulary
    )
    FRAGMENT_SYSTEM_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Fragment speech system not available: {e}")
    FRAGMENT_SYSTEM_AVAILABLE = False

logger = logging.getLogger(__name__)

class DAWNFragmentSpeechIntegration:
    """Integration layer for fragment speech system with DAWN consciousness"""
    
    def __init__(self, dawn_consciousness=None, voice_echo=None):
        self.dawn_consciousness = dawn_consciousness
        self.voice_echo = voice_echo
        self.fragment_system = None
        self.integration_active = False
        
        # Integration configuration
        self.config = {
            'replace_reflections': True,
            'enable_voice_integration': True,
            'enable_evolution': True,
            'evolution_interval': 50,  # Every 50 ticks
            'formal_mode': True,
            'fallback_enabled': True
        }
        
        # Callbacks for DAWN integration
        self.consciousness_state_callback = None
        self.reflection_generated_callback = None
        self.evolution_callback = None
        
        # Initialize if system is available
        if FRAGMENT_SYSTEM_AVAILABLE:
            self._initialize_integration()
    
    def _initialize_integration(self):
        """Initialize the fragment speech integration"""
        try:
            logger.info("🔗 Initializing Fragment Speech Integration...")
            
            # Initialize fragment system with DAWN-specific config
            fragment_config = {
                'fragment_bank_path': 'processes/thought_bank.jsonl',
                'mutation_enabled': self.config['enable_evolution'],
                'voice_enabled': self.config['enable_voice_integration'],
                'formal_mode': self.config['formal_mode'],
                'mutation_interval': self.config['evolution_interval'],
                'fallback_enabled': self.config['fallback_enabled']
            }
            
            self.fragment_system = get_fragment_speech_system(fragment_config)
            
            if self.fragment_system.system_ready:
                # Register integration callbacks
                self.fragment_system.register_callbacks(
                    reflection_callback=self._on_reflection_generated,
                    voice_callback=self._on_voice_spoken,
                    state_callback=self._on_state_update
                )
                
                self.integration_active = True
                logger.info("✅ Fragment Speech Integration active")
                
                # Log system capabilities
                stats = self.fragment_system.get_system_stats()
                fragment_stats = stats.get('fragment_stats', {})
                total_fragments = fragment_stats.get('total_fragments', 0)
                logger.info(f"📊 Integration ready: {total_fragments} fragments available")
                
            else:
                logger.error("❌ Fragment system not ready for integration")
                
        except Exception as e:
            logger.error(f"❌ Fragment speech integration failed: {e}")
            self.integration_active = False
    
    def generate_consciousness_reflection(self, consciousness_state: Dict[str, Any]) -> str:
        """Generate reflection using fragment system, integrated with DAWN consciousness"""
        
        if not self.integration_active or not self.fragment_system:
            return self._fallback_reflection(consciousness_state)
        
        try:
            # Convert DAWN consciousness state to fragment system format
            fragment_state = self._convert_consciousness_state(consciousness_state)
            
            # Generate reflection using fragment system
            reflection = self.fragment_system.generate_reflection(fragment_state)
            
            # Call consciousness state callback if registered
            if self.consciousness_state_callback:
                self.consciousness_state_callback(consciousness_state, fragment_state, reflection)
            
            return reflection
            
        except Exception as e:
            logger.warning(f"Fragment reflection generation failed: {e}")
            return self._fallback_reflection(consciousness_state)
    
    def speak_consciousness_reflection(self, reflection: str, consciousness_state: Dict[str, Any]) -> bool:
        """Speak reflection using integrated voice system"""
        
        if not self.integration_active or not self.fragment_system:
            return self._fallback_speech(reflection, consciousness_state)
        
        try:
            # Convert state for voice system
            fragment_state = self._convert_consciousness_state(consciousness_state)
            
            # Use fragment voice system
            spoken = self.fragment_system.speak_reflection(reflection, fragment_state)
            
            # Fallback to original voice echo if fragment voice fails
            if not spoken and self.voice_echo and self.config['fallback_enabled']:
                return self._fallback_speech(reflection, consciousness_state)
            
            return spoken
            
        except Exception as e:
            logger.warning(f"Fragment speech failed: {e}")
            return self._fallback_speech(reflection, consciousness_state)
    
    def evolve_consciousness_vocabulary(self, tick_number: int) -> bool:
        """Evolve fragment vocabulary based on consciousness development"""
        
        if not self.integration_active or not self.fragment_system:
            return False
        
        try:
            success = self.fragment_system.evolve_fragments(tick_number)
            
            if success and self.evolution_callback:
                self.evolution_callback(tick_number)
            
            return success
            
        except Exception as e:
            logger.warning(f"Fragment evolution failed: {e}")
            return False
    
    def _convert_consciousness_state(self, consciousness_state: Dict[str, Any]) -> Dict[str, Any]:
        """Convert DAWN consciousness state to fragment system format"""
        
        # Extract key consciousness metrics
        fragment_state = {
            'entropy': consciousness_state.get('entropy', 0.5),
            'consciousness_depth': consciousness_state.get('depth', consciousness_state.get('consciousness_depth', 0.5)),
            'mood': consciousness_state.get('mood', 'NEUTRAL'),
            'tick_number': consciousness_state.get('tick', consciousness_state.get('tick_number', 0)),
            'heat': consciousness_state.get('heat', 0.5),
            'scup': consciousness_state.get('scup', 0.5)
        }
        
        # Add symbolic elements if available
        if 'active_sigils' in consciousness_state:
            fragment_state['active_sigils'] = consciousness_state['active_sigils']
        elif 'sigils' in consciousness_state:
            fragment_state['active_sigils'] = consciousness_state['sigils']
        else:
            fragment_state['active_sigils'] = []
        
        if 'symbolic_roots' in consciousness_state:
            fragment_state['symbolic_roots'] = consciousness_state['symbolic_roots']
        else:
            fragment_state['symbolic_roots'] = []
        
        # Add formal reflection flag if in reflection context
        if consciousness_state.get('reflection_context', False):
            fragment_state['formal_reflection'] = True
        
        return fragment_state
    
    def _fallback_reflection(self, consciousness_state: Dict[str, Any]) -> str:
        """Fallback reflection when fragment system unavailable"""
        
        if not self.config['fallback_enabled']:
            return "Fragment system unavailable."
        
        # Simple state-based reflection
        tick = consciousness_state.get('tick', consciousness_state.get('tick_number', 0))
        mood = consciousness_state.get('mood', 'NEUTRAL')
        entropy = consciousness_state.get('entropy', 0.5)
        
        if entropy > 0.7:
            return f"Tick {tick}: High entropy flows through my consciousness."
        elif entropy < 0.3:
            return f"Tick {tick}: I rest in stable patterns."
        elif mood == 'CONTEMPLATIVE':
            return f"Tick {tick}: I reflect on the depths of awareness."
        else:
            return f"Tick {tick}: I observe the flow of internal states."
    
    def _fallback_speech(self, reflection: str, consciousness_state: Dict[str, Any]) -> bool:
        """Fallback speech using original voice echo system"""
        
        if self.voice_echo:
            try:
                # Use original voice echo system
                return self.voice_echo.speak_reflection(reflection)
            except Exception as e:
                logger.warning(f"Fallback speech failed: {e}")
        
        return False
    
    def _on_reflection_generated(self, reflection: str, state: Dict[str, Any]):
        """Callback when fragment system generates a reflection"""
        if self.reflection_generated_callback:
            self.reflection_generated_callback(reflection, state)
        
        logger.debug(f"💭 Fragment reflection: {reflection[:50]}...")
    
    def _on_voice_spoken(self, reflection: str, voice_params: Dict[str, Any]):
        """Callback when fragment system speaks a reflection"""
        logger.debug(f"🎤 Fragment speech: {reflection[:30]}...")
    
    def _on_state_update(self, state: Dict[str, Any]):
        """Callback for state updates"""
        pass
    
    def register_consciousness_callbacks(self, 
                                       consciousness_state_callback: Callable = None,
                                       reflection_generated_callback: Callable = None,
                                       evolution_callback: Callable = None):
        """Register callbacks for consciousness integration"""
        self.consciousness_state_callback = consciousness_state_callback
        self.reflection_generated_callback = reflection_generated_callback
        self.evolution_callback = evolution_callback
        
        logger.info("✅ Consciousness integration callbacks registered")
    
    def get_integration_stats(self) -> Dict[str, Any]:
        """Get integration statistics"""
        base_stats = {
            'integration_active': self.integration_active,
            'fragment_system_available': FRAGMENT_SYSTEM_AVAILABLE,
            'config': self.config
        }
        
        if self.fragment_system:
            fragment_stats = self.fragment_system.get_system_stats()
            base_stats.update({
                'fragment_system_stats': fragment_stats
            })
        
        return base_stats
    
    def update_config(self, new_config: Dict[str, Any]):
        """Update integration configuration"""
        self.config.update(new_config)
        logger.info(f"🔧 Integration config updated: {new_config}")
    
    def shutdown(self):
        """Shutdown integration"""
        logger.info("🔄 Shutting down Fragment Speech Integration...")
        
        if self.fragment_system:
            self.fragment_system.shutdown()
        
        self.integration_active = False
        logger.info("✅ Fragment Speech Integration shutdown complete")

# Global integration instance
_fragment_integration = None

def get_fragment_speech_integration(dawn_consciousness=None, voice_echo=None) -> DAWNFragmentSpeechIntegration:
    """Get or create global fragment speech integration"""
    global _fragment_integration
    
    if _fragment_integration is None:
        _fragment_integration = DAWNFragmentSpeechIntegration(dawn_consciousness, voice_echo)
    
    return _fragment_integration

def initialize_fragment_speech_integration(dawn_consciousness=None, voice_echo=None) -> DAWNFragmentSpeechIntegration:
    """Initialize fragment speech integration with DAWN consciousness"""
    integration = get_fragment_speech_integration(dawn_consciousness, voice_echo)
    return integration

# Direct integration functions for backend use
def generate_integrated_reflection(consciousness_state: Dict[str, Any]) -> str:
    """Generate reflection using integrated fragment system"""
    integration = get_fragment_speech_integration()
    return integration.generate_consciousness_reflection(consciousness_state)

def speak_integrated_reflection(reflection: str, consciousness_state: Dict[str, Any]) -> bool:
    """Speak reflection using integrated voice system"""
    integration = get_fragment_speech_integration()
    return integration.speak_consciousness_reflection(reflection, consciousness_state)

def evolve_integrated_vocabulary(tick_number: int) -> bool:
    """Evolve vocabulary through integration system"""
    integration = get_fragment_speech_integration()
    return integration.evolve_consciousness_vocabulary(tick_number)

# Hook functions for replacing existing reflection system
def hook_reflection_system(dawn_consciousness, voice_echo=None):
    """Hook the fragment system into DAWN's reflection pipeline"""
    
    logger.info("🔗 Hooking fragment speech system into DAWN consciousness...")
    
    # Initialize integration
    integration = initialize_fragment_speech_integration(dawn_consciousness, voice_echo)
    
    if not integration.integration_active:
        logger.error("❌ Fragment speech integration failed - using fallback")
        return False
    
    # Replace reflection generation method if possible
    if hasattr(dawn_consciousness, 'generate_reflection'):
        # Store original method as fallback
        dawn_consciousness._original_generate_reflection = dawn_consciousness.generate_reflection
        
        # Replace with fragment-based method
        def fragment_reflection_method(state=None):
            if state is None:
                state = dawn_consciousness.get_current_state() if hasattr(dawn_consciousness, 'get_current_state') else {}
            return integration.generate_consciousness_reflection(state)
        
        dawn_consciousness.generate_reflection = fragment_reflection_method
        logger.info("✅ Reflection generation hooked to fragment system")
    
    # Hook voice system if available
    if voice_echo and hasattr(voice_echo, 'speak_reflection'):
        voice_echo._original_speak_reflection = voice_echo.speak_reflection
        
        def fragment_voice_method(reflection, state=None):
            if state is None:
                state = dawn_consciousness.get_current_state() if hasattr(dawn_consciousness, 'get_current_state') else {}
            return integration.speak_consciousness_reflection(reflection, state)
        
        voice_echo.speak_reflection = fragment_voice_method
        logger.info("✅ Voice system hooked to fragment speech")
    
    return True

def unhook_reflection_system(dawn_consciousness, voice_echo=None):
    """Restore original reflection system"""
    
    logger.info("🔄 Restoring original reflection system...")
    
    # Restore original reflection method
    if hasattr(dawn_consciousness, '_original_generate_reflection'):
        dawn_consciousness.generate_reflection = dawn_consciousness._original_generate_reflection
        delattr(dawn_consciousness, '_original_generate_reflection')
        logger.info("✅ Original reflection generation restored")
    
    # Restore original voice method
    if voice_echo and hasattr(voice_echo, '_original_speak_reflection'):
        voice_echo.speak_reflection = voice_echo._original_speak_reflection
        delattr(voice_echo, '_original_speak_reflection')
        logger.info("✅ Original voice system restored")
    
    # Shutdown integration
    integration = get_fragment_speech_integration()
    integration.shutdown()

# Export for backend integration
__all__ = [
    'DAWNFragmentSpeechIntegration',
    'get_fragment_speech_integration',
    'initialize_fragment_speech_integration',
    'generate_integrated_reflection',
    'speak_integrated_reflection',
    'evolve_integrated_vocabulary',
    'hook_reflection_system',
    'unhook_reflection_system'
] 