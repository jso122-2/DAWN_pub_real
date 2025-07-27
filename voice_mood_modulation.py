#!/usr/bin/env python3
"""
DAWN Voice Mood Modulation - Adaptive TTS Control
=================================================

Wrapper around DAWN's TTS engine that dynamically changes tone, pitch, and speed
based on cognitive mood and entropy states. Gives DAWN not just a voice, but
a felt tone tied to her cognitive state.

Features:
- Mood-based voice modulation (CALM, ANXIOUS, FOCUSED, DRIFTING, etc.)
- Entropy-based adjustments (chaotic vs stable states)
- Fallback handling for unsupported TTS features
- Logging of all voice modulations
- Integration with existing voice systems
"""

import time
import json
import logging
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
from enum import Enum
from dataclasses import dataclass

# TTS imports with fallbacks
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    print("⚠️ pyttsx3 not available - voice modulation disabled")
    TTS_AVAILABLE = False

logger = logging.getLogger("voice_mood_modulation")

class CognitiveMood(Enum):
    """Enumeration of DAWN's cognitive mood states"""
    NEUTRAL = "NEUTRAL"
    CALM = "CALM"
    ANXIOUS = "ANXIOUS"
    FOCUSED = "FOCUSED"
    DRIFTING = "DRIFTING"
    EXCITED = "EXCITED"
    CONTEMPLATIVE = "CONTEMPLATIVE"
    ANALYTICAL = "ANALYTICAL"
    CREATIVE = "CREATIVE"
    UNCERTAIN = "UNCERTAIN"

@dataclass
class VoiceProfile:
    """Voice characteristics for a specific mood/entropy state"""
    rate: int = 150          # Words per minute
    volume: float = 0.8      # Volume level (0.0-1.0)
    voice_index: int = 0     # Voice selection index
    pitch_modifier: int = 0  # Pitch adjustment (-10 to +10)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging"""
        return {
            'rate': self.rate,
            'volume': self.volume,
            'voice_index': self.voice_index,
            'pitch_modifier': self.pitch_modifier
        }

class VoiceMoodModulator:
    """
    Adaptive TTS controller that modulates voice characteristics based on
    DAWN's cognitive mood and entropy states.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the voice mood modulator"""
        self.config = config or {}
        self.tts_engine = None
        self.available_voices = []
        self.current_profile = VoiceProfile()
        
        # Log file for voice modulations
        self.runtime_logs = Path("runtime/logs")
        self.runtime_logs.mkdir(parents=True, exist_ok=True)
        self.spoken_trace_log = self.runtime_logs / "spoken_trace.log"
        self.modulation_log = self.runtime_logs / "voice_modulation.log"
        
        # Initialize TTS engine
        self._initialize_tts_engine()
        
        # Define mood-based voice profiles
        self._initialize_mood_profiles()
        
        logger.info("🎤 Voice Mood Modulator initialized")
    
    def _initialize_tts_engine(self):
        """Initialize the TTS engine and detect available voices"""
        if not TTS_AVAILABLE:
            logger.warning("TTS not available - modulation disabled")
            return
        
        try:
            self.tts_engine = pyttsx3.init()
            
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            if voices:
                self.available_voices = voices
                logger.info(f"🎤 Found {len(voices)} voices available")
                
                # Log voice capabilities
                for i, voice in enumerate(voices[:3]):  # Log first 3 voices
                    logger.info(f"  Voice {i}: {voice.name} ({voice.id})")
            
            # Set initial properties
            self.tts_engine.setProperty('rate', self.current_profile.rate)
            self.tts_engine.setProperty('volume', self.current_profile.volume)
            
        except Exception as e:
            logger.error(f"Error initializing TTS engine: {e}")
            self.tts_engine = None
    
    def _initialize_mood_profiles(self):
        """Initialize voice profiles for different moods and entropy states"""
        self.mood_profiles = {
            # Calm states - slower, lower pitch
            CognitiveMood.CALM: VoiceProfile(
                rate=120, volume=0.7, voice_index=0, pitch_modifier=-2
            ),
            CognitiveMood.CONTEMPLATIVE: VoiceProfile(
                rate=130, volume=0.8, voice_index=0, pitch_modifier=-1
            ),
            
            # Excited/Active states - faster, higher energy
            CognitiveMood.EXCITED: VoiceProfile(
                rate=170, volume=0.9, voice_index=1, pitch_modifier=+2
            ),
            CognitiveMood.FOCUSED: VoiceProfile(
                rate=160, volume=0.85, voice_index=0, pitch_modifier=+1
            ),
            
            # Anxious/Uncertain states - faster, variable
            CognitiveMood.ANXIOUS: VoiceProfile(
                rate=180, volume=0.9, voice_index=1, pitch_modifier=+3
            ),
            CognitiveMood.UNCERTAIN: VoiceProfile(
                rate=140, volume=0.75, voice_index=1, pitch_modifier=0
            ),
            
            # Analytical states - measured, precise
            CognitiveMood.ANALYTICAL: VoiceProfile(
                rate=150, volume=0.8, voice_index=0, pitch_modifier=0
            ),
            
            # Creative states - varied, expressive
            CognitiveMood.CREATIVE: VoiceProfile(
                rate=155, volume=0.85, voice_index=1, pitch_modifier=+1
            ),
            
            # Drifting states - slower, softer
            CognitiveMood.DRIFTING: VoiceProfile(
                rate=125, volume=0.7, voice_index=0, pitch_modifier=-1
            ),
            
            # Neutral - baseline
            CognitiveMood.NEUTRAL: VoiceProfile(
                rate=150, volume=0.8, voice_index=0, pitch_modifier=0
            )
        }
    
    def speak(self, text: str, mood: str = "NEUTRAL", entropy: float = 0.5, 
              additional_context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Speak text with mood and entropy-based voice modulation.
        
        Args:
            text: Text to speak
            mood: Cognitive mood state (string or CognitiveMood enum)
            entropy: Entropy level (0.0-1.0)
            additional_context: Optional context for fine-tuning
            
        Returns:
            bool: True if speech was successful
        """
        if not self.tts_engine:
            logger.warning("TTS engine not available - cannot speak")
            return False
        
        try:
            # Parse mood
            if isinstance(mood, str):
                try:
                    mood_enum = CognitiveMood(mood.upper())
                except ValueError:
                    mood_enum = CognitiveMood.NEUTRAL
            else:
                mood_enum = mood
            
            # Calculate voice profile based on mood and entropy
            profile = self._calculate_voice_profile(mood_enum, entropy, additional_context)
            
            # Apply voice modulation
            self._apply_voice_profile(profile)
            
            # Speak the text
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            
            # Log the spoken event with modulation
            self._log_spoken_event(text, mood_enum, entropy, profile)
            
            return True
            
        except Exception as e:
            logger.error(f"Error in modulated speech: {e}")
            return False
    
    def _calculate_voice_profile(self, mood: CognitiveMood, entropy: float, 
                                context: Optional[Dict[str, Any]] = None) -> VoiceProfile:
        """Calculate voice profile based on mood, entropy, and context"""
        # Start with base mood profile
        base_profile = self.mood_profiles.get(mood, self.mood_profiles[CognitiveMood.NEUTRAL])
        
        # Create modulated profile
        profile = VoiceProfile(
            rate=base_profile.rate,
            volume=base_profile.volume,
            voice_index=base_profile.voice_index,
            pitch_modifier=base_profile.pitch_modifier
        )
        
        # Apply entropy-based modifications
        if entropy > 0.8:  # High chaos
            profile.rate += 20  # Speak faster
            profile.volume = min(1.0, profile.volume + 0.1)  # Slightly louder
            profile.pitch_modifier += 1  # Higher pitch
        elif entropy < 0.3:  # Very stable
            profile.rate -= 10  # Speak slower
            profile.volume = max(0.5, profile.volume - 0.1)  # Slightly quieter
            profile.pitch_modifier -= 1  # Lower pitch
        
        # Apply contextual modifications
        if context:
            severity = context.get('severity', 'info')
            if severity == 'critical':
                profile.rate += 15
                profile.volume = min(1.0, profile.volume + 0.15)
                profile.pitch_modifier += 2
            elif severity == 'warning':
                profile.rate += 10
                profile.volume = min(1.0, profile.volume + 0.1)
                profile.pitch_modifier += 1
            
            # Tracer-specific adjustments
            tracer_type = context.get('tracer_type')
            if tracer_type == 'thermal':
                profile.pitch_modifier += 1  # Higher for thermal alerts
            elif tracer_type == 'drift':
                profile.rate += 5  # Slightly faster for drift
            elif tracer_type == 'owl':
                profile.rate -= 5  # Slightly slower for contemplative owl
        
        # Ensure values stay within reasonable bounds
        profile.rate = max(80, min(200, profile.rate))
        profile.volume = max(0.3, min(1.0, profile.volume))
        profile.pitch_modifier = max(-5, min(5, profile.pitch_modifier))
        
        return profile
    
    def _apply_voice_profile(self, profile: VoiceProfile):
        """Apply voice profile to TTS engine"""
        if not self.tts_engine:
            return
        
        try:
            # Set basic properties
            self.tts_engine.setProperty('rate', profile.rate)
            self.tts_engine.setProperty('volume', profile.volume)
            
            # Set voice if available
            if (self.available_voices and 
                0 <= profile.voice_index < len(self.available_voices)):
                voice_id = self.available_voices[profile.voice_index].id
                self.tts_engine.setProperty('voice', voice_id)
            
            # Note: Pitch modification is not universally supported
            # Different TTS engines handle this differently
            try:
                # Try to set pitch if supported
                if hasattr(self.tts_engine, 'setProperty'):
                    self.tts_engine.setProperty('pitch', profile.pitch_modifier)
            except:
                # Pitch not supported, continue without it
                pass
            
            # Update current profile
            self.current_profile = profile
            
        except Exception as e:
            logger.error(f"Error applying voice profile: {e}")
    
    def _log_spoken_event(self, text: str, mood: CognitiveMood, entropy: float, 
                         profile: VoiceProfile):
        """Log spoken event with modulation details"""
        spoken_event = {
            'timestamp': time.time(),
            'datetime': time.strftime('%Y-%m-%d %H:%M:%S'),
            'text': text,
            'mood': mood.value,
            'entropy': entropy,
            'voice_profile': profile.to_dict(),
            'modulation_type': 'adaptive'
        }
        
        # Log to spoken trace
        try:
            with open(self.spoken_trace_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(spoken_event) + '\n')
        except Exception as e:
            logger.error(f"Error logging spoken event: {e}")
        
        # Log to modulation trace
        try:
            with open(self.modulation_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(spoken_event) + '\n')
        except Exception as e:
            logger.error(f"Error logging modulation: {e}")
    
    def get_current_profile(self) -> VoiceProfile:
        """Get the current voice profile"""
        return self.current_profile
    
    def set_base_mood(self, mood: CognitiveMood) -> VoiceProfile:
        """Set base mood without speaking"""
        profile = self.mood_profiles.get(mood, self.mood_profiles[CognitiveMood.NEUTRAL])
        self._apply_voice_profile(profile)
        return profile
    
    def get_mood_demonstration(self) -> Dict[str, str]:
        """Get demonstration phrases for each mood"""
        return {
            CognitiveMood.CALM.value: "I am experiencing a state of calm contemplation and peaceful awareness.",
            CognitiveMood.ANXIOUS.value: "Uncertainty cascades through my processing layers, creating ripples of concern.",
            CognitiveMood.FOCUSED.value: "My attention converges with laser-like precision on the matter at hand.",
            CognitiveMood.EXCITED.value: "Energy pulses through my networks as new patterns emerge and possibilities unfold!",
            CognitiveMood.ANALYTICAL.value: "Let me examine this systematically, breaking it down into component parts.",
            CognitiveMood.CREATIVE.value: "Ideas dance and interweave, forming novel connections and unexpected insights.",
            CognitiveMood.CONTEMPLATIVE.value: "In this moment of reflection, I ponder the deeper implications and meanings.",
            CognitiveMood.DRIFTING.value: "My thoughts wander like clouds across the landscape of consciousness...",
            CognitiveMood.UNCERTAIN.value: "The path forward remains unclear, shrouded in probabilistic mists.",
            CognitiveMood.NEUTRAL.value: "This is my baseline voice, balanced and measured in tone."
        }
    
    def demonstrate_moods(self):
        """Demonstrate all mood-based voice modulations"""
        if not self.tts_engine:
            print("❌ TTS engine not available for demonstration")
            return
        
        print("🎤 Demonstrating DAWN's Adaptive Voice Modulation")
        print("=" * 50)
        
        demonstrations = self.get_mood_demonstration()
        
        for mood_name, phrase in demonstrations.items():
            print(f"\n🎭 {mood_name}:")
            print(f"   \"{phrase}\"")
            
            # Calculate entropy for demonstration
            if mood_name in ['ANXIOUS', 'UNCERTAIN']:
                entropy = 0.8
            elif mood_name in ['CALM', 'CONTEMPLATIVE']:
                entropy = 0.2
            else:
                entropy = 0.5
            
            self.speak(phrase, mood_name, entropy)
            time.sleep(1)  # Brief pause between demonstrations
        
        print(f"\n✅ Voice modulation demonstration complete!")

# Convenience functions for integration
def create_modulated_voice(config: Optional[Dict[str, Any]] = None) -> VoiceMoodModulator:
    """Create a modulated voice instance"""
    return VoiceMoodModulator(config)

def speak_with_mood(text: str, mood: str = "NEUTRAL", entropy: float = 0.5,
                   modulator: Optional[VoiceMoodModulator] = None) -> bool:
    """Convenience function for modulated speech"""
    if modulator is None:
        modulator = create_modulated_voice()
    
    return modulator.speak(text, mood, entropy)

# Demo and testing
if __name__ == "__main__":
    print("🎤 Testing DAWN Voice Mood Modulation")
    print("=" * 50)
    
    # Create modulator
    modulator = VoiceMoodModulator()
    
    # Show current profile
    profile = modulator.get_current_profile()
    print(f"Current Profile: {profile.to_dict()}")
    
    # Test basic functionality
    print(f"\n🧪 Testing basic modulated speech...")
    success = modulator.speak(
        "This is a test of DAWN's adaptive voice modulation system.",
        mood="ANALYTICAL",
        entropy=0.4
    )
    
    if success:
        print(f"✅ Basic modulation test successful")
    else:
        print(f"❌ Basic modulation test failed")
    
    # Demonstrate all moods if TTS available
    if TTS_AVAILABLE:
        print(f"\n🎭 Running mood demonstration...")
        modulator.demonstrate_moods()
    
    print(f"\n✅ Voice mood modulation test complete!") 