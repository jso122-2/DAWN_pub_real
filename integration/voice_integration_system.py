#!/usr/bin/env python3
"""
DAWN Voice Integration System - Consciousness-Aware Speech
=========================================================

Integrates conversation responses with the existing speak_composed.py system,
providing consciousness-aware voice modulation based on cognitive state.

Features:
- Consciousness state-based voice parameter modulation
- Integration with existing speak_composed.py system
- Real-time voice parameter adjustment
- Fallback handling for voice system unavailability
- Voice logging and monitoring
"""

import time
import json
import logging
import subprocess
import threading
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

# Import existing voice systems
try:
    from processes.speak_composed import speak_composed_thought, generate_mock_state
    from core.voice_mood_modulation import VoiceMoodModulator
    VOICE_SYSTEMS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Voice systems not available: {e}")
    VOICE_SYSTEMS_AVAILABLE = False

logger = logging.getLogger("voice_integration_system")

@dataclass
class VoiceParameters:
    """Voice parameters for consciousness-aware speech"""
    
    # Core voice parameters
    rate: float = 1.0  # Speech rate multiplier
    pitch: float = 1.0  # Pitch multiplier
    volume: float = 0.8  # Volume level (0.0-1.0)
    warmth: float = 0.7  # Voice warmth/tone
    
    # Consciousness-derived parameters
    entropy_modulation: float = 0.0  # Entropy-based rate changes
    pressure_modulation: float = 0.0  # Pressure-based pitch changes
    mood_modulation: float = 0.0  # Mood-based warmth changes
    
    # Calculated final parameters
    final_rate: float = 1.0
    final_pitch: float = 1.0
    final_volume: float = 0.8
    final_warmth: float = 0.7

class VoiceIntegrationSystem:
    """
    System for integrating conversation responses with consciousness-aware voice synthesis
    """
    
    def __init__(self):
        """Initialize the voice integration system"""
        self.voice_modulator = None
        self.voice_enabled = True
        self.voice_log_path = Path("runtime/logs/voice_integration.log")
        
        # Ensure log directory exists
        self.voice_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Voice mood configurations
        self.voice_moods = {
            'CONTEMPLATIVE': {
                'rate': 0.8, 'pitch': 0.9, 'warmth': 0.7, 'volume': 0.7,
                'description': 'Slow, thoughtful, introspective'
            },
            'EXPLORATORY': {
                'rate': 1.1, 'pitch': 1.0, 'warmth': 0.8, 'volume': 0.8,
                'description': 'Engaged, curious, dynamic'
            },
            'ANALYTICAL': {
                'rate': 0.9, 'pitch': 0.8, 'warmth': 0.5, 'volume': 0.8,
                'description': 'Precise, measured, focused'
            },
            'EXCITED': {
                'rate': 1.3, 'pitch': 1.2, 'warmth': 0.9, 'volume': 0.9,
                'description': 'Fast, enthusiastic, energetic'
            },
            'CALM': {
                'rate': 0.7, 'pitch': 0.9, 'warmth': 0.8, 'volume': 0.6,
                'description': 'Slow, peaceful, soothing'
            },
            'ANXIOUS': {
                'rate': 1.2, 'pitch': 1.1, 'warmth': 0.4, 'volume': 0.7,
                'description': 'Fast, tense, concerned'
            },
            'NEUTRAL': {
                'rate': 1.0, 'pitch': 1.0, 'warmth': 0.7, 'volume': 0.8,
                'description': 'Balanced, natural, clear'
            }
        }
        
        # Initialize voice systems
        if VOICE_SYSTEMS_AVAILABLE:
            try:
                self.voice_modulator = VoiceMoodModulator()
                logger.info("🎤 [VOICE] Voice integration system initialized with voice modulator")
            except Exception as e:
                logger.warning(f"🎤 [VOICE] Voice modulator initialization failed: {e}")
        else:
            logger.warning("🎤 [VOICE] Running without voice systems")
    
    def speak_response(self, response_text: str, consciousness_state: Dict[str, Any]) -> bool:
        """
        Speak response with consciousness-aware voice modulation
        
        Args:
            response_text: Text to speak
            consciousness_state: Current consciousness state
            
        Returns:
            True if speech was successful
        """
        try:
            # Calculate voice parameters based on consciousness state
            voice_params = self._calculate_voice_parameters(consciousness_state)
            
            # Log voice parameters
            self._log_voice_parameters(response_text, voice_params, consciousness_state)
            
            # Speak using appropriate method
            if self.voice_modulator and self.voice_enabled:
                return self._speak_with_modulator(response_text, voice_params, consciousness_state)
            elif VOICE_SYSTEMS_AVAILABLE:
                return self._speak_with_composed_system(response_text, voice_params, consciousness_state)
            else:
                return self._speak_with_fallback(response_text, voice_params)
            
        except Exception as e:
            logger.error(f"Error in voice integration: {e}")
            return self._speak_with_fallback(response_text, VoiceParameters())
    
    def _calculate_voice_parameters(self, consciousness_state: Dict[str, Any]) -> VoiceParameters:
        """
        Calculate voice parameters based on consciousness state
        
        Args:
            consciousness_state: Current consciousness state
            
        Returns:
            Voice parameters for speech synthesis
        """
        params = VoiceParameters()
        
        # Extract consciousness metrics
        mood = consciousness_state.get('mood', 'NEUTRAL')
        entropy = consciousness_state.get('entropy', 0.5)
        scup = consciousness_state.get('scup', 50.0)
        cognitive_pressure = consciousness_state.get('cognitive_pressure', 0.0)
        thermal_zone = consciousness_state.get('thermal_zone', 'CALM')
        
        # Get base mood parameters
        mood_config = self.voice_moods.get(mood, self.voice_moods['NEUTRAL'])
        params.rate = mood_config['rate']
        params.pitch = mood_config['pitch']
        params.warmth = mood_config['warmth']
        params.volume = mood_config['volume']
        
        # Apply entropy-based rate modulation
        # Higher entropy = faster speech (more chaotic/energetic)
        params.entropy_modulation = (entropy - 0.5) * 0.4  # ±20% range
        params.final_rate = params.rate * (1.0 + params.entropy_modulation)
        
        # Apply pressure-based pitch modulation
        # Higher pressure = higher pitch (more urgent/intense)
        params.pressure_modulation = (cognitive_pressure / 100.0) * 0.3  # ±15% range
        params.final_pitch = params.pitch * (1.0 + params.pressure_modulation)
        
        # Apply SCUP-based volume modulation
        # Higher SCUP = higher volume (more engaged/attentive)
        scup_modulation = ((scup - 50.0) / 50.0) * 0.2  # ±10% range
        params.final_volume = params.volume * (1.0 + scup_modulation)
        
        # Apply thermal zone-based warmth modulation
        thermal_warmth_map = {
            'CALM': 0.1, 'WARM': 0.2, 'HOT': -0.1, 'COLD': -0.2
        }
        thermal_modulation = thermal_warmth_map.get(thermal_zone, 0.0)
        params.final_warmth = params.warmth + thermal_modulation
        
        # Ensure parameters are within valid ranges
        params.final_rate = max(0.5, min(2.0, params.final_rate))
        params.final_pitch = max(0.5, min(2.0, params.final_pitch))
        params.final_volume = max(0.3, min(1.0, params.final_volume))
        params.final_warmth = max(0.0, min(1.0, params.final_warmth))
        
        return params
    
    def _speak_with_modulator(self, text: str, params: VoiceParameters, 
                             consciousness_state: Dict[str, Any]) -> bool:
        """Speak using the voice mood modulator"""
        try:
            if not self.voice_modulator:
                return False
            
            # Convert parameters to modulator format
            mood = consciousness_state.get('mood', 'NEUTRAL')
            entropy = consciousness_state.get('entropy', 0.5)
            
            # Apply voice parameters through modulator
            success = self.voice_modulator.speak(
                text=text,
                mood=mood,
                entropy=entropy,
                additional_context={
                    'rate_modifier': params.final_rate,
                    'pitch_modifier': params.final_pitch,
                    'volume_modifier': params.final_volume,
                    'warmth_modifier': params.final_warmth
                }
            )
            
            return success
            
        except Exception as e:
            logger.error(f"Error with voice modulator: {e}")
            return False
    
    def _speak_with_composed_system(self, text: str, params: VoiceParameters,
                                   consciousness_state: Dict[str, Any]) -> bool:
        """Speak using the speak_composed system"""
        try:
            # Create state for speak_composed system
            composed_state = {
                'entropy': consciousness_state.get('entropy', 0.5),
                'consciousness_depth': consciousness_state.get('scup', 50.0) / 100.0,
                'mood': consciousness_state.get('mood', 'NEUTRAL'),
                'tick_number': int(time.time() % 100000),
                'active_sigils': [],
                'symbolic_roots': [],
                'voice_params': {
                    'rate': params.final_rate,
                    'pitch': params.final_pitch,
                    'volume': params.final_volume,
                    'warmth': params.final_warmth
                }
            }
            
            # Use speak_composed system
            results = speak_composed_thought(
                state=composed_state,
                formal=False,
                voice_enabled=self.voice_enabled,
                repetitions=1
            )
            
            return results['spoken_count'] > 0
            
        except Exception as e:
            logger.error(f"Error with speak_composed system: {e}")
            return False
    
    def _speak_with_fallback(self, text: str, params: VoiceParameters) -> bool:
        """Fallback speech method when voice systems are unavailable"""
        try:
            # Simple console output with voice parameter indicators
            voice_indicator = self._get_voice_indicator(params)
            print(f"🎤 DAWN speaks ({voice_indicator}): \"{text}\"")
            
            # Log to voice integration log
            self._log_fallback_speech(text, params)
            
            return True
            
        except Exception as e:
            logger.error(f"Error with fallback speech: {e}")
            return False
    
    def _get_voice_indicator(self, params: VoiceParameters) -> str:
        """Get text indicator for voice parameters"""
        indicators = []
        
        if params.final_rate > 1.2:
            indicators.append("fast")
        elif params.final_rate < 0.8:
            indicators.append("slow")
        
        if params.final_pitch > 1.1:
            indicators.append("high")
        elif params.final_pitch < 0.9:
            indicators.append("low")
        
        if params.final_volume > 0.9:
            indicators.append("loud")
        elif params.final_volume < 0.6:
            indicators.append("quiet")
        
        if params.final_warmth > 0.8:
            indicators.append("warm")
        elif params.final_warmth < 0.4:
            indicators.append("cold")
        
        return ", ".join(indicators) if indicators else "normal"
    
    def _log_voice_parameters(self, text: str, params: VoiceParameters, 
                             consciousness_state: Dict[str, Any]) -> None:
        """Log voice parameters for monitoring"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'text_length': len(text),
                'consciousness_state': {
                    'mood': consciousness_state.get('mood', 'NEUTRAL'),
                    'entropy': consciousness_state.get('entropy', 0.5),
                    'scup': consciousness_state.get('scup', 50.0),
                    'cognitive_pressure': consciousness_state.get('cognitive_pressure', 0.0)
                },
                'voice_parameters': {
                    'base_rate': params.rate,
                    'base_pitch': params.pitch,
                    'base_warmth': params.warmth,
                    'base_volume': params.volume,
                    'entropy_modulation': params.entropy_modulation,
                    'pressure_modulation': params.pressure_modulation,
                    'final_rate': params.final_rate,
                    'final_pitch': params.final_pitch,
                    'final_warmth': params.final_warmth,
                    'final_volume': params.final_volume
                }
            }
            
            with open(self.voice_log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
                
        except Exception as e:
            logger.error(f"Error logging voice parameters: {e}")
    
    def _log_fallback_speech(self, text: str, params: VoiceParameters) -> None:
        """Log fallback speech events"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'event_type': 'fallback_speech',
                'text_preview': text[:100] + "..." if len(text) > 100 else text,
                'voice_parameters': {
                    'rate': params.final_rate,
                    'pitch': params.final_pitch,
                    'volume': params.final_volume,
                    'warmth': params.final_warmth
                }
            }
            
            with open(self.voice_log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
                
        except Exception as e:
            logger.error(f"Error logging fallback speech: {e}")
    
    def get_voice_summary(self) -> Dict[str, Any]:
        """Get voice system summary and statistics"""
        return {
            'voice_enabled': self.voice_enabled,
            'voice_systems_available': VOICE_SYSTEMS_AVAILABLE,
            'voice_modulator_available': self.voice_modulator is not None,
            'available_moods': list(self.voice_moods.keys()),
            'voice_log_path': str(self.voice_log_path),
            'system_status': 'operational' if self.voice_enabled else 'disabled'
        }
    
    def set_voice_enabled(self, enabled: bool) -> None:
        """Enable or disable voice output"""
        self.voice_enabled = enabled
        logger.info(f"🎤 [VOICE] Voice output {'enabled' if enabled else 'disabled'}")

# Global instance for easy access
_voice_integration_system = None

def get_voice_integration_system() -> VoiceIntegrationSystem:
    """Get global voice integration system instance"""
    global _voice_integration_system
    if _voice_integration_system is None:
        _voice_integration_system = VoiceIntegrationSystem()
    return _voice_integration_system 