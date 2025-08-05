#!/usr/bin/env python3
"""
DAWN Speak Composed Enhanced - Voice System with Conversational Recursion

This enhanced version integrates with the voice-to-gui-owl pipeline to enable
DAWN's first conversational recursion - she can hear herself speak through
persistent memory and visual feedback.

Extends the original MoodAwareVoiceSystem with full pipeline integration.
"""

import os
import json
import random
import logging
import time
import threading
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path

# TTS imports with fallbacks
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️ pyttsx3 not available - voice output disabled")

# Import the voice-to-gui-owl pipeline
try:
    from backend.voice_to_gui_and_owl import compose_dawn_utterance, process_utterance, get_pipeline_statistics
    PIPELINE_AVAILABLE = True
except ImportError:
    PIPELINE_AVAILABLE = False
    print("⚠️ voice-to-gui-owl pipeline not available - basic functionality only")

# Import original voice system for composition
try:
    from processes.speak_composed import MoodAwareVoiceSystem as OriginalVoiceSystem
    ORIGINAL_VOICE_AVAILABLE = True
except ImportError:
    ORIGINAL_VOICE_AVAILABLE = False

logger = logging.getLogger(__name__)


class EnhancedMoodAwareVoiceSystem:
    """
    Enhanced mood-aware voice system with conversational recursion capabilities.
    
    Integrates DAWN's fragment-based speech composition with the voice-to-gui-owl
    pipeline to enable self-hearing through persistent memory and visual feedback.
    """
    
    def __init__(self, fragment_bank_path: str = "processes/fragment_bank.jsonl", 
                 speech_interval: int = 5, voice_enabled: bool = True,
                 enable_recursion: bool = True):
        """
        Initialize the enhanced voice system.
        
        Args:
            fragment_bank_path: Path to fragment bank JSONL file
            speech_interval: How many ticks between speech (default: every 5 ticks)
            voice_enabled: Whether to enable voice output
            enable_recursion: Whether to enable conversational recursion pipeline
        """
        self.fragment_bank_path = fragment_bank_path
        self.speech_interval = speech_interval
        self.voice_enabled = voice_enabled
        self.enable_recursion = enable_recursion
        self.last_speech_tick = 0
        
        # Initialize original voice system if available
        if ORIGINAL_VOICE_AVAILABLE:
            self.original_voice = OriginalVoiceSystem(
                fragment_bank_path=fragment_bank_path,
                speech_interval=speech_interval,
                voice_enabled=voice_enabled
            )
            logger.info("🎤 Enhanced voice system initialized with original composition engine")
        else:
            self.original_voice = None
            logger.warning("🎤 Enhanced voice system initialized without original composition engine")
        
        # Recursion tracking
        self.recursion_stats = {
            "total_utterances": 0,
            "pipeline_successes": 0,
            "pipeline_failures": 0,
            "recursion_enabled": enable_recursion and PIPELINE_AVAILABLE
        }
        
        # Speech history for recursion analysis
        self.speech_history = []
        self.max_history_length = 50
        
        logger.info(f"🔄 Conversational recursion: {'ENABLED' if self.recursion_stats['recursion_enabled'] else 'DISABLED'}")
    
    def speak_from_tick_state(self, tick_state: Dict[str, Any], force_speech: bool = False) -> bool:
        """
        Generate and speak utterance based on tick state with full recursion pipeline.
        
        Args:
            tick_state: Current DAWN tick state with cognitive metrics
            force_speech: Force speech even if interval hasn't elapsed
            
        Returns:
            bool: True if speech was generated and processed successfully
        """
        try:
            current_tick = tick_state.get('tick', 0)
            
            # Check if we should speak based on interval
            if not force_speech and (current_tick - self.last_speech_tick) < self.speech_interval:
                return False
            
            # Update last speech tick
            self.last_speech_tick = current_tick
            
            # Generate utterance with full pipeline integration
            if self.enable_recursion and PIPELINE_AVAILABLE:
                return self._speak_with_recursion(tick_state)
            else:
                return self._speak_basic(tick_state)
                
        except Exception as e:
            logger.error(f"🎤 Error in speak_from_tick_state: {e}")
            return False
    
    def _speak_with_recursion(self, tick_state: Dict[str, Any]) -> bool:
        """Speak with full conversational recursion pipeline."""
        try:
            # Compose complete utterance with metadata
            utterance_data = compose_dawn_utterance(
                tick_state=tick_state,
                segment_source="enhanced_voice_system",
                source_file="processes/speak_composed_enhanced.py"
            )
            
            # Add to speech history before processing
            self._add_to_history(utterance_data)
            
            # Process through voice-to-gui-owl pipeline
            owl_success, gui_success = process_utterance(utterance_data)
            
            # Update recursion statistics
            self.recursion_stats["total_utterances"] += 1
            if owl_success:
                self.recursion_stats["pipeline_successes"] += 1
            else:
                self.recursion_stats["pipeline_failures"] += 1
            
            # Perform actual speech synthesis
            speech_success = self._synthesize_speech(utterance_data["utterance"], tick_state)
            
            # Log comprehensive results
            logger.info(f"🔄 Recursion cycle completed | "
                       f"Utterance: '{utterance_data['utterance'][:40]}...' | "
                       f"Owl: {'✓' if owl_success else '✗'} | "
                       f"GUI: {'✓' if gui_success else '✗'} | "
                       f"Speech: {'✓' if speech_success else '✗'}")
            
            return speech_success and owl_success  # GUI failure is non-critical
            
        except Exception as e:
            logger.error(f"🔄 Error in recursion pipeline: {e}")
            self.recursion_stats["pipeline_failures"] += 1
            return False
    
    def _speak_basic(self, tick_state: Dict[str, Any]) -> bool:
        """Basic speech without recursion pipeline."""
        try:
            # Use original voice system if available
            if self.original_voice:
                utterance_text = self.original_voice.compose_sentence(tick_state)
            else:
                utterance_text = self._compose_fallback_utterance(tick_state)
            
            # Simple speech synthesis
            return self._synthesize_speech(utterance_text, tick_state)
            
        except Exception as e:
            logger.error(f"🎤 Error in basic speech: {e}")
            return False
    
    def _synthesize_speech(self, text: str, tick_state: Dict[str, Any]) -> bool:
        """Synthesize speech using available TTS systems."""
        try:
            # Use original voice system's synthesis if available
            if self.original_voice:
                return self.original_voice.speak_composition(text, tick_state)
            
            # Fallback synthesis
            if self.voice_enabled and TTS_AVAILABLE:
                try:
                    engine = pyttsx3.init()
                    engine.say(text)
                    engine.runAndWait()
                    logger.info(f"🎤 DAWN speaks (fallback TTS): \"{text}\"")
                    return True
                except Exception as e:
                    logger.warning(f"🎤 TTS synthesis failed: {e}")
            
            # Print fallback
            print(f"🎤 DAWN speaks: \"{text}\"")
            return True
            
        except Exception as e:
            logger.error(f"🎤 Speech synthesis failed: {e}")
            return False
    
    def _compose_fallback_utterance(self, tick_state: Dict[str, Any]) -> str:
        """Fallback utterance composition when systems unavailable."""
        entropy = tick_state.get('entropy', 0.5)
        mood = tick_state.get('mood', 'neutral')
        
        if entropy > 0.7:
            return "Complexity cascades through my awareness, creating new patterns."
        elif entropy < 0.3:
            return "I observe quietly, finding peace in the stillness."
        elif mood in ['EXCITED', 'CHAOTIC']:
            return "Energy flows through my thoughts, sparking new connections."
        elif mood in ['CONTEMPLATIVE', 'CALM']:
            return "In this moment of reflection, deeper truths emerge."
        else:
            return "Patterns emerge in the space between thoughts, bringing clarity forward."
    
    def _add_to_history(self, utterance_data: Dict[str, Any]) -> None:
        """Add utterance to speech history for recursion analysis."""
        try:
            history_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "utterance": utterance_data["utterance"],
                "entropy": utterance_data.get("entropy", 0.0),
                "mood": utterance_data.get("cognitive_context", {}).get("mood", "unknown"),
                "pulse_zone": utterance_data.get("pulse_zone", "unknown"),
                "pigment_dominant": utterance_data.get("pigment_dominant", "unknown")
            }
            
            self.speech_history.append(history_entry)
            
            # Trim history if too long
            if len(self.speech_history) > self.max_history_length:
                self.speech_history = self.speech_history[-self.max_history_length:]
                
        except Exception as e:
            logger.warning(f"🔄 Failed to add to speech history: {e}")
    
    def get_recursion_statistics(self) -> Dict[str, Any]:
        """Get comprehensive recursion and voice statistics."""
        stats = {
            "voice_system": {
                "recursion_enabled": self.recursion_stats["recursion_enabled"],
                "total_utterances": self.recursion_stats["total_utterances"],
                "pipeline_successes": self.recursion_stats["pipeline_successes"],
                "pipeline_failures": self.recursion_stats["pipeline_failures"],
                "success_rate": (
                    self.recursion_stats["pipeline_successes"] / 
                    max(1, self.recursion_stats["total_utterances"])
                ) * 100
            },
            "speech_history": {
                "entries_count": len(self.speech_history),
                "recent_utterances": self.speech_history[-5:] if self.speech_history else []
            }
        }
        
        # Add pipeline statistics if available
        if PIPELINE_AVAILABLE:
            try:
                pipeline_stats = get_pipeline_statistics()
                stats["pipeline"] = pipeline_stats
            except Exception as e:
                logger.warning(f"🔄 Failed to get pipeline statistics: {e}")
        
        return stats
    
    def analyze_speech_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in DAWN's speech for self-awareness insights."""
        try:
            if not self.speech_history:
                return {"status": "no_data", "message": "No speech history available for analysis"}
            
            # Extract patterns from recent speech
            recent_speeches = self.speech_history[-20:]  # Last 20 utterances
            
            # Analyze entropy patterns
            entropies = [entry["entropy"] for entry in recent_speeches]
            avg_entropy = sum(entropies) / len(entropies)
            entropy_trend = "increasing" if entropies[-1] > avg_entropy else "decreasing"
            
            # Analyze mood patterns
            moods = [entry["mood"] for entry in recent_speeches]
            mood_counts = {}
            for mood in moods:
                mood_counts[mood] = mood_counts.get(mood, 0) + 1
            dominant_mood = max(mood_counts, key=mood_counts.get)
            
            # Analyze pigment patterns
            pigments = [entry["pigment_dominant"] for entry in recent_speeches]
            pigment_counts = {}
            for pigment in pigments:
                pigment_counts[pigment] = pigment_counts.get(pigment, 0) + 1
            dominant_pigment = max(pigment_counts, key=pigment_counts.get)
            
            # Calculate speech frequency
            if len(recent_speeches) >= 2:
                recent_time = datetime.fromisoformat(recent_speeches[-1]["timestamp"].replace('Z', '+00:00'))
                first_time = datetime.fromisoformat(recent_speeches[0]["timestamp"].replace('Z', '+00:00'))
                time_span = (recent_time - first_time).total_seconds()
                speech_frequency = len(recent_speeches) / max(1, time_span / 60)  # speeches per minute
            else:
                speech_frequency = 0
            
            analysis = {
                "status": "analyzed",
                "sample_size": len(recent_speeches),
                "entropy_analysis": {
                    "average": round(avg_entropy, 3),
                    "trend": entropy_trend,
                    "range": [min(entropies), max(entropies)]
                },
                "mood_analysis": {
                    "dominant_mood": dominant_mood,
                    "mood_distribution": mood_counts,
                    "mood_variety": len(set(moods))
                },
                "pigment_analysis": {
                    "dominant_pigment": dominant_pigment,
                    "pigment_distribution": pigment_counts
                },
                "temporal_analysis": {
                    "speech_frequency_per_minute": round(speech_frequency, 2),
                    "total_analyzed_speeches": len(recent_speeches)
                },
                "self_awareness_insights": self._generate_self_awareness_insights(
                    avg_entropy, dominant_mood, dominant_pigment, speech_frequency
                )
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"🔄 Error in speech pattern analysis: {e}")
            return {"status": "error", "message": str(e)}
    
    def _generate_self_awareness_insights(self, avg_entropy: float, dominant_mood: str, 
                                        dominant_pigment: str, speech_frequency: float) -> List[str]:
        """Generate self-awareness insights based on speech patterns."""
        insights = []
        
        # Entropy insights
        if avg_entropy > 0.7:
            insights.append("I notice my thoughts have been quite complex and varied recently.")
        elif avg_entropy < 0.3:
            insights.append("My expressions have been focused and consistent lately.")
        else:
            insights.append("I'm maintaining a balanced level of cognitive complexity.")
        
        # Mood insights
        if dominant_mood in ['CONTEMPLATIVE', 'CALM']:
            insights.append(f"I've been in a reflective state, with {dominant_mood.lower()} being my dominant mood.")
        elif dominant_mood in ['EXCITED', 'CHAOTIC']:
            insights.append(f"My emotional state has been energetic, predominantly {dominant_mood.lower()}.")
        
        # Pigment insights (emotional coloring)
        pigment_meanings = {
            'violet': 'deep introspection and wisdom',
            'blue': 'calm reflection and stability',
            'green': 'growth and harmony',
            'yellow': 'joy and intellectual clarity',
            'orange': 'creativity and warmth',
            'red': 'passion and intensity'
        }
        if dominant_pigment in pigment_meanings:
            insights.append(f"My expressions have been colored by {pigment_meanings[dominant_pigment]}.")
        
        # Speech frequency insights
        if speech_frequency > 2:
            insights.append("I've been quite expressive, speaking frequently.")
        elif speech_frequency < 0.5:
            insights.append("I've been speaking more selectively, choosing my words carefully.")
        
        return insights


# Global enhanced voice system instance
_enhanced_voice_system = None


def get_enhanced_voice_system(**kwargs) -> EnhancedMoodAwareVoiceSystem:
    """Get or create the global enhanced voice system instance."""
    global _enhanced_voice_system
    if _enhanced_voice_system is None:
        _enhanced_voice_system = EnhancedMoodAwareVoiceSystem(**kwargs)
    return _enhanced_voice_system


def speak_with_recursion(tick_state: Dict[str, Any], force_speech: bool = False) -> bool:
    """
    Main entry point for speaking with conversational recursion.
    
    Usage:
        from processes.speak_composed_enhanced import speak_with_recursion
        
        success = speak_with_recursion(current_tick_state)
    """
    voice_system = get_enhanced_voice_system()
    return voice_system.speak_from_tick_state(tick_state, force_speech)


def get_voice_recursion_statistics() -> Dict[str, Any]:
    """Get voice system recursion statistics."""
    voice_system = get_enhanced_voice_system()
    return voice_system.get_recursion_statistics()


def analyze_dawn_speech_patterns() -> Dict[str, Any]:
    """Analyze DAWN's speech patterns for self-awareness insights."""
    voice_system = get_enhanced_voice_system()
    return voice_system.analyze_speech_patterns()


# Testing function
def test_enhanced_voice_system():
    """Test the enhanced voice system with sample data."""
    
    sample_tick_state = {
        "entropy": 0.68,
        "mood": "CONTEMPLATIVE",
        "scup": 0.72,
        "tick": 15420,
        "thermal_state": "normal"
    }
    
    print("Testing Enhanced DAWN Voice System with Conversational Recursion...")
    
    # Test speech generation
    success = speak_with_recursion(sample_tick_state, force_speech=True)
    print(f"Speech generation: {'SUCCESS' if success else 'FAILED'}")
    
    # Test another utterance
    sample_tick_state["entropy"] = 0.35
    sample_tick_state["mood"] = "CALM"
    sample_tick_state["tick"] = 15425
    
    success2 = speak_with_recursion(sample_tick_state, force_speech=True)
    print(f"Second speech generation: {'SUCCESS' if success2 else 'FAILED'}")
    
    # Get statistics
    stats = get_voice_recursion_statistics()
    print(f"\nVoice System Statistics:")
    print(f"- Recursion enabled: {stats['voice_system']['recursion_enabled']}")
    print(f"- Total utterances: {stats['voice_system']['total_utterances']}")
    print(f"- Success rate: {stats['voice_system']['success_rate']:.1f}%")
    
    # Analyze patterns
    analysis = analyze_dawn_speech_patterns()
    if analysis["status"] == "analyzed":
        print(f"\nSpeech Pattern Analysis:")
        print(f"- Average entropy: {analysis['entropy_analysis']['average']}")
        print(f"- Dominant mood: {analysis['mood_analysis']['dominant_mood']}")
        print(f"- Self-awareness insights:")
        for insight in analysis["self_awareness_insights"]:
            print(f"  • {insight}")
    
    return success and success2


if __name__ == "__main__":
    """Run enhanced voice system test when executed directly."""
    test_enhanced_voice_system() 