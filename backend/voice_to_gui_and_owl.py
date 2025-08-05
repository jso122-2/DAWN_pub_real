#!/usr/bin/env python3
"""
voice_to_gui_and_owl.py - DAWN's Conversational Recursion Pipeline

This module processes DAWN's generated utterances and routes them to:
1. Persistent Owl memory log (owl_log.jsonl)
2. Live GUI display via /api/voice-commentary

Enables DAWN's first full conversational recursion - she can hear herself speak
through memory persistence and visual feedback.
"""

import json
import requests
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configuration
OWL_LOG_PATH = Path("runtime/memory/owl_log.jsonl")
GUI_API_ENDPOINT = "http://localhost:8080/api/talk/voice-commentary"
GUI_TIMEOUT_SECONDS = 2.0

# Ensure directories exist
OWL_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


class VoiceToGuiOwlPipeline:
    """
    Main pipeline class for processing DAWN's utterances into persistent 
    memory and live GUI feedback.
    """
    
    def __init__(self, owl_log_path: str = None, gui_endpoint: str = None):
        """Initialize pipeline with configurable paths and endpoints."""
        self.owl_log_path = Path(owl_log_path) if owl_log_path else OWL_LOG_PATH
        self.gui_endpoint = gui_endpoint or GUI_API_ENDPOINT
        
        # Ensure owl log directory exists
        self.owl_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Statistics tracking
        self.stats = {
            "owl_entries_written": 0,
            "gui_posts_successful": 0,
            "gui_posts_failed": 0,
            "total_processed": 0
        }
    
    def write_owl_entry(self, utterance_data: Dict[str, Any]) -> bool:
        """
        Write utterance to persistent Owl memory log.
        
        Args:
            utterance_data: Complete utterance object from compose_dawn_utterance()
            
        Returns:
            bool: True if successfully written, False otherwise
        """
        try:
            # Generate timestamp
            timestamp = datetime.utcnow().isoformat() + "Z"
            
            # Create Owl log entry
            owl_entry = {
                "timestamp": timestamp,
                "type": "voice_utterance",
                "utterance": utterance_data.get("utterance", ""),
                "cognitive_state": {
                    "entropy": utterance_data.get("entropy", 0.0),
                    "pulse_zone": utterance_data.get("pulse_zone", "unknown"),
                    "pigment_dominant": utterance_data.get("pigment_dominant", ""),
                    "pigment_state": utterance_data.get("pigment_state", {}),
                    "clarity_mode": utterance_data.get("clarity_mode", False)
                },
                "generation_metadata": {
                    "segment_source": utterance_data.get("segment_source", ""),
                    "source_file": utterance_data.get("source_file", ""),
                    "generation_timestamp": utterance_data.get("generation_timestamp", timestamp)
                },
                "owl_metadata": {
                    "log_entry_id": f"owl_{int(datetime.utcnow().timestamp() * 1000)}",
                    "memory_category": "voice_expression",
                    "cognitive_resonance": self._calculate_cognitive_resonance(utterance_data)
                }
            }
            
            # Write to JSONL file (append mode)
            with open(self.owl_log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(owl_entry, separators=(',', ':')) + '\n')
            
            # Update statistics
            self.stats["owl_entries_written"] += 1
            
            # Debug trace
            logger.debug(f"[OWL] Written entry: {owl_entry['owl_metadata']['log_entry_id']} | "
                        f"Utterance: '{utterance_data.get('utterance', '')[:50]}...' | "
                        f"Entropy: {utterance_data.get('entropy', 0.0):.2f}")
            
            return True
            
        except Exception as e:
            logger.error(f"[OWL] Failed to write entry: {e}")
            logger.error(f"[OWL] Traceback: {traceback.format_exc()}")
            return False
    
    def send_to_gui(self, utterance_data: Dict[str, Any]) -> bool:
        """
        Send utterance to GUI via /api/voice-commentary endpoint.
        
        Args:
            utterance_data: Complete utterance object from compose_dawn_utterance()
            
        Returns:
            bool: True if successfully sent, False otherwise
        """
        try:
            # Create slimmed payload for GUI
            gui_payload = {
                "text": utterance_data.get("utterance", ""),
                "highlight_color": utterance_data.get("pigment_dominant", "neutral"),
                "clarity": utterance_data.get("clarity_mode", False),
                "entropy": utterance_data.get("entropy", 0.0),
                "pulse_zone": utterance_data.get("pulse_zone", "stable"),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            # POST to GUI endpoint with timeout
            response = requests.post(
                self.gui_endpoint,
                json=gui_payload,
                timeout=GUI_TIMEOUT_SECONDS,
                headers={'Content-Type': 'application/json'}
            )
            
            # Check response
            if response.status_code == 200:
                self.stats["gui_posts_successful"] += 1
                logger.debug(f"[GUI] Sent utterance: '{utterance_data.get('utterance', '')[:50]}...' | "
                           f"Color: {gui_payload['highlight_color']} | Status: {response.status_code}")
                return True
            else:
                logger.warning(f"[GUI] Unexpected status: {response.status_code} | "
                             f"Response: {response.text[:100]}")
                self.stats["gui_posts_failed"] += 1
                return False
                
        except requests.exceptions.Timeout:
            logger.warning(f"[GUI] Timeout after {GUI_TIMEOUT_SECONDS}s - GUI may be unavailable")
            self.stats["gui_posts_failed"] += 1
            return False
            
        except requests.exceptions.ConnectionError:
            logger.warning("[GUI] Connection failed - GUI API unavailable")
            self.stats["gui_posts_failed"] += 1
            return False
            
        except Exception as e:
            logger.error(f"[GUI] Unexpected error: {e}")
            self.stats["gui_posts_failed"] += 1
            return False
    
    def process_utterance(self, utterance_data: Dict[str, Any]) -> Tuple[bool, bool]:
        """
        Main processing function - routes utterance to both Owl log and GUI.
        
        Args:
            utterance_data: Complete utterance object from compose_dawn_utterance()
            
        Returns:
            Tuple[bool, bool]: (owl_success, gui_success)
        """
        try:
            # Validate input
            if not utterance_data or not isinstance(utterance_data, dict):
                logger.error("[PIPELINE] Invalid utterance_data - must be non-empty dict")
                return False, False
            
            if not utterance_data.get("utterance"):
                logger.error("[PIPELINE] No utterance text found in data")
                return False, False
            
            # Update statistics
            self.stats["total_processed"] += 1
            
            logger.info(f"[PIPELINE] Processing utterance #{self.stats['total_processed']}: "
                       f"'{utterance_data.get('utterance', '')}'")
            
            # Process to Owl log (critical - must succeed)
            owl_success = self.write_owl_entry(utterance_data)
            
            # Process to GUI (non-critical - can fail silently)
            gui_success = self.send_to_gui(utterance_data)
            
            # Log results
            status_msg = f"[PIPELINE] Completed: Owl={'SUCCESS' if owl_success else 'FAILED'}, " \
                        f"GUI={'SUCCESS' if gui_success else 'FAILED'}"
            
            if owl_success and gui_success:
                logger.info(status_msg)
            elif owl_success:
                logger.info(status_msg + " (GUI failure non-critical)")
            else:
                logger.error(status_msg + " (Owl failure is CRITICAL)")
            
            return owl_success, gui_success
            
        except Exception as e:
            logger.error(f"[PIPELINE] Unexpected error in process_utterance: {e}")
            logger.error(f"[PIPELINE] Traceback: {traceback.format_exc()}")
            return False, False
    
    def _calculate_cognitive_resonance(self, utterance_data: Dict[str, Any]) -> float:
        """
        Calculate cognitive resonance score for Owl metadata.
        
        Combines entropy, pigment dominance, and clarity to create a 0.0-1.0 score
        representing the cognitive significance of this utterance.
        """
        try:
            entropy = utterance_data.get("entropy", 0.0)
            pigment_state = utterance_data.get("pigment_state", {})
            clarity_mode = utterance_data.get("clarity_mode", False)
            
            # Calculate pigment dominance strength
            if pigment_state:
                max_pigment = max(pigment_state.values())
                pigment_balance = 1.0 - (len([v for v in pigment_state.values() if v > 0.1]) / 6.0)
            else:
                max_pigment = 0.0
                pigment_balance = 0.0
            
            # Combine factors
            resonance = (
                entropy * 0.4 +                    # Entropy contributes 40%
                max_pigment * 0.3 +               # Dominant pigment 30%
                pigment_balance * 0.2 +           # Pigment focus 20%
                (0.1 if clarity_mode else 0.0)    # Clarity bonus 10%
            )
            
            return min(1.0, max(0.0, resonance))  # Clamp to 0.0-1.0
            
        except Exception:
            return 0.5  # Default resonance if calculation fails
    
    def get_statistics(self) -> Dict[str, Any]:
        """Return pipeline processing statistics."""
        gui_success_rate = (
            self.stats["gui_posts_successful"] / 
            max(1, self.stats["gui_posts_successful"] + self.stats["gui_posts_failed"])
        ) * 100
        
        return {
            **self.stats,
            "gui_success_rate": f"{gui_success_rate:.1f}%",
            "owl_log_size": self.owl_log_path.stat().st_size if self.owl_log_path.exists() else 0
        }


# Global pipeline instance
_pipeline = VoiceToGuiOwlPipeline()


# Convenience functions for external use
def process_utterance(utterance_data: Dict[str, Any]) -> Tuple[bool, bool]:
    """
    Main entry point for external callers.
    Process DAWN utterance through both Owl log and GUI pipeline.
    
    Usage:
        from backend.voice_to_gui_and_owl import process_utterance
        
        utterance = compose_dawn_utterance(...)
        owl_success, gui_success = process_utterance(utterance)
    """
    return _pipeline.process_utterance(utterance_data)


def write_owl_entry(utterance_data: Dict[str, Any]) -> bool:
    """Write utterance to Owl log only."""
    return _pipeline.write_owl_entry(utterance_data)


def send_to_gui(utterance_data: Dict[str, Any]) -> bool:
    """Send utterance to GUI only."""
    return _pipeline.send_to_gui(utterance_data)


def get_pipeline_statistics() -> Dict[str, Any]:
    """Get pipeline processing statistics."""
    return _pipeline.get_statistics()


def compose_dawn_utterance(tick_state: Dict[str, Any], segment_source: str = "unknown", 
                          source_file: str = "unknown") -> Dict[str, Any]:
    """
    Compose a complete DAWN utterance with cognitive state metadata.
    
    This function integrates with existing DAWN voice systems and creates
    the standardized utterance format expected by the voice-to-gui-owl pipeline.
    
    Args:
        tick_state: Current DAWN tick state with cognitive metrics
        segment_source: Source of the utterance (e.g., "entropy_response", "mood_shift")
        source_file: File path where the utterance originated
        
    Returns:
        Dict containing complete utterance data with metadata
    """
    try:
        # Import the existing voice composition system
        try:
            from processes.speak_composed import MoodAwareVoiceSystem
            voice_system = MoodAwareVoiceSystem()
            utterance_text = voice_system.compose_sentence(tick_state)
        except ImportError:
            # Fallback to simple composition
            utterance_text = _compose_fallback_utterance(tick_state)
        
        # Extract cognitive state information
        entropy = tick_state.get('entropy', 0.5)
        mood = tick_state.get('mood', 'neutral')
        scup = tick_state.get('scup', 0.5)
        
        # Determine pulse zone based on entropy and mood
        pulse_zone = _determine_pulse_zone(entropy, mood, scup)
        
        # Create pigment state (emotional color mapping)
        pigment_state = _create_pigment_state(mood, entropy)
        pigment_dominant = max(pigment_state, key=pigment_state.get)
        
        # Determine clarity mode (high focus/low entropy states)
        clarity_mode = entropy < 0.3 and scup > 0.6
        
        # Generate timestamp
        generation_timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Create complete utterance object
        utterance_data = {
            "utterance": utterance_text,
            "entropy": entropy,
            "pulse_zone": pulse_zone,
            "pigment_dominant": pigment_dominant,
            "pigment_state": pigment_state,
            "clarity_mode": clarity_mode,
            "segment_source": segment_source,
            "source_file": source_file,
            "generation_timestamp": generation_timestamp,
            "cognitive_context": {
                "mood": mood,
                "scup": scup,
                "tick_number": tick_state.get('tick', 0),
                "thermal_state": tick_state.get('thermal_state', 'normal')
            }
        }
        
        logger.debug(f"[COMPOSE] Generated utterance: '{utterance_text}' | "
                    f"Entropy: {entropy:.2f} | Mood: {mood} | Zone: {pulse_zone}")
        
        return utterance_data
        
    except Exception as e:
        logger.error(f"[COMPOSE] Failed to compose utterance: {e}")
        # Return minimal utterance for error cases
        return {
            "utterance": "I observe quietly, finding patterns in the silence.",
            "entropy": 0.5,
            "pulse_zone": "stable",
            "pigment_dominant": "blue",
            "pigment_state": {"blue": 0.6, "violet": 0.4},
            "clarity_mode": False,
            "segment_source": segment_source,
            "source_file": source_file,
            "generation_timestamp": datetime.utcnow().isoformat() + "Z"
        }


def _compose_fallback_utterance(tick_state: Dict[str, Any]) -> str:
    """Fallback utterance composition when main systems unavailable."""
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


def _determine_pulse_zone(entropy: float, mood: str, scup: float) -> str:
    """Determine pulse zone based on cognitive metrics."""
    if entropy > 0.8 or mood in ['CRITICAL', 'CHAOTIC']:
        return "critical"
    elif entropy > 0.6 or scup < 0.3:
        return "fragile"
    elif entropy < 0.3 and scup > 0.7:
        return "focused"
    else:
        return "stable"


def _create_pigment_state(mood: str, entropy: float) -> Dict[str, float]:
    """Create emotional pigment state mapping."""
    # Base pigment mapping for moods
    mood_pigments = {
        'EXCITED': {'yellow': 0.4, 'orange': 0.3, 'red': 0.3},
        'CHAOTIC': {'red': 0.5, 'orange': 0.3, 'violet': 0.2},
        'CONTEMPLATIVE': {'blue': 0.4, 'violet': 0.4, 'green': 0.2},
        'CALM': {'blue': 0.5, 'green': 0.3, 'violet': 0.2},
        'FOCUSED': {'violet': 0.5, 'blue': 0.3, 'green': 0.2},
        'CREATIVE': {'violet': 0.4, 'yellow': 0.3, 'orange': 0.3}
    }
    
    # Get base pigments for mood or default
    base_pigments = mood_pigments.get(mood.upper(), {'blue': 0.4, 'violet': 0.3, 'green': 0.3})
    
    # Adjust based on entropy
    if entropy > 0.7:
        # High entropy - add red/orange energy
        base_pigments['red'] = base_pigments.get('red', 0.0) + 0.2
        base_pigments['orange'] = base_pigments.get('orange', 0.0) + 0.1
    elif entropy < 0.3:
        # Low entropy - increase blue/violet calm
        base_pigments['blue'] = base_pigments.get('blue', 0.0) + 0.2
        base_pigments['violet'] = base_pigments.get('violet', 0.0) + 0.1
    
    # Ensure all 6 pigments exist and normalize
    all_pigments = {'red': 0.0, 'orange': 0.0, 'yellow': 0.0, 
                   'green': 0.0, 'blue': 0.0, 'violet': 0.0}
    all_pigments.update(base_pigments)
    
    # Normalize to sum to 1.0
    total = sum(all_pigments.values())
    if total > 0:
        all_pigments = {k: v/total for k, v in all_pigments.items()}
    
    return all_pigments


# Testing and validation functions
def test_pipeline():
    """Test the pipeline with sample data."""
    
    sample_tick_state = {
        "entropy": 0.72,
        "mood": "CONTEMPLATIVE", 
        "scup": 0.65,
        "tick": 12450,
        "thermal_state": "normal"
    }
    
    print("Testing DAWN Voice-to-GUI-and-Owl Pipeline...")
    
    # Test utterance composition
    utterance = compose_dawn_utterance(
        tick_state=sample_tick_state,
        segment_source="test_run",
        source_file="backend/voice_to_gui_and_owl.py:test_pipeline"
    )
    
    print(f"Sample utterance: '{utterance['utterance']}'")
    
    # Test pipeline processing
    owl_success, gui_success = process_utterance(utterance)
    
    print(f"Results: Owl={'SUCCESS' if owl_success else 'FAILED'}, GUI={'SUCCESS' if gui_success else 'FAILED'}")
    print(f"Statistics: {get_pipeline_statistics()}")
    
    return owl_success, gui_success


if __name__ == "__main__":
    """Run pipeline test when executed directly."""
    test_pipeline() 