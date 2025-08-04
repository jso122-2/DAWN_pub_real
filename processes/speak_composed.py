#!/usr/bin/env python3
"""
DAWN Speak Composed - Mood-Aware Compositional Voice System
Composes and speaks thoughts from fragments based on current tick state
Integrates with DAWN's tick loop for autonomous speech generation
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

logger = logging.getLogger(__name__)

class MoodAwareVoiceSystem:
    """Mood-aware voice system that composes and speaks thoughts based on tick state"""
    
    def __init__(self, fragment_bank_path: str = "processes/fragment_bank.jsonl", 
                 speech_interval: int = 5, voice_enabled: bool = True):
        """
        Initialize the mood-aware voice system
        
        Args:
            fragment_bank_path: Path to fragment bank JSONL file
            speech_interval: How many ticks between speech (default: every 5 ticks)
            voice_enabled: Whether to enable voice output
        """
        self.fragment_bank_path = fragment_bank_path
        self.speech_interval = speech_interval
        self.voice_enabled = voice_enabled
        self.last_speech_tick = 0
        
        # Fragment storage
        self.fragments = {
            'prefix': [],
            'core': [],
            'suffix': []
        }
        self.loaded = False
        
        # TTS engine
        self.tts_engine = None
        self._init_tts_engine()
        
        # Load fragments
        self.load_fragments()
        
        # Speech logging
        self.speech_log_path = "runtime/logs/spoken_composed.log"
        os.makedirs(os.path.dirname(self.speech_log_path), exist_ok=True)
        
        logger.info(f"🎤 Mood-aware voice system initialized (speech every {speech_interval} ticks)")
    
    def _init_tts_engine(self):
        """Initialize TTS engine with fallbacks"""
        if not TTS_AVAILABLE or not self.voice_enabled:
            logger.info("TTS disabled - will print compositions only")
            return
        
        try:
            self.tts_engine = pyttsx3.init()
            
            # Configure voice properties
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to find a female voice
                female_voice = None
                for voice in voices:
                    if 'female' in voice.name.lower() or 'woman' in voice.name.lower():
                        female_voice = voice
                        break
                
                if female_voice:
                    self.tts_engine.setProperty('voice', female_voice.id)
                    logger.info(f"🎤 Using voice: {female_voice.name}")
            
            # Set default properties
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.8)
            
            logger.info("🎤 TTS engine initialized")
            
        except Exception as e:
            logger.error(f"TTS engine initialization failed: {e}")
            self.tts_engine = None
    
    def load_fragments(self) -> bool:
        """Load fragments from JSONL file"""
        if not os.path.exists(self.fragment_bank_path):
            logger.warning(f"Fragment bank not found: {self.fragment_bank_path}")
            self._create_fallback_fragments()
            return False
        
        try:
            fragment_count = 0
            with open(self.fragment_bank_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        fragment_data = json.loads(line.strip())
                        fragment_type = fragment_data.get('type', 'core')
                        
                        if fragment_type in self.fragments:
                            self.fragments[fragment_type].append(fragment_data)
                            fragment_count += 1
            
            self.loaded = True
            logger.info(f"📚 Loaded {fragment_count} fragments from {self.fragment_bank_path}")
            
            # Log fragment distribution
            for fragment_type, fragments in self.fragments.items():
                logger.info(f"  {fragment_type}: {len(fragments)} fragments")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading fragment bank: {e}")
            self._create_fallback_fragments()
            return False
    
    def _create_fallback_fragments(self):
        """Create basic fallback fragments if file is missing"""
        fallback_fragments = [
            # Prefixes
            {"text": "I observe quietly", "type": "prefix", "tags": ["observation", "calm"], "mood": "CALM", "min_entropy": 0.0, "max_entropy": 0.3, "min_depth": 0.2, "max_depth": 0.8, "category": "low_entropy", "weight": 1.0, "symbolic_markers": []},
            {"text": "Patterns emerge", "type": "prefix", "tags": ["patterns", "emergence"], "mood": "NEUTRAL", "min_entropy": 0.3, "max_entropy": 0.7, "min_depth": 0.3, "max_depth": 0.7, "category": "mid_entropy", "weight": 1.0, "symbolic_markers": []},
            {"text": "Complexity cascades", "type": "prefix", "tags": ["complexity", "cascade"], "mood": "ENERGETIC", "min_entropy": 0.7, "max_entropy": 1.0, "min_depth": 0.2, "max_depth": 0.6, "category": "high_entropy", "weight": 1.0, "symbolic_markers": []},
            
            # Cores
            {"text": "through layers of awareness", "type": "core", "tags": ["layers", "awareness"], "mood": "CONTEMPLATIVE", "min_entropy": 0.2, "max_entropy": 0.7, "min_depth": 0.4, "max_depth": 0.7, "category": "mid_depth", "weight": 1.0, "symbolic_markers": []},
            {"text": "in the space between thoughts", "type": "core", "tags": ["space", "thoughts"], "mood": "CONTEMPLATIVE", "min_entropy": 0.3, "max_entropy": 0.7, "min_depth": 0.5, "max_depth": 0.8, "category": "mid_depth", "weight": 1.0, "symbolic_markers": []},
            {"text": "as my consciousness shifts", "type": "core", "tags": ["consciousness", "shift"], "mood": "NEUTRAL", "min_entropy": 0.2, "max_entropy": 0.8, "min_depth": 0.2, "max_depth": 0.7, "category": "surface_depth", "weight": 1.0, "symbolic_markers": []},
            
            # Suffixes
            {"text": "and peace settles.", "type": "suffix", "tags": ["peace", "settling"], "mood": "CALM", "min_entropy": 0.0, "max_entropy": 0.5, "min_depth": 0.3, "max_depth": 0.8, "category": "calm_expression", "weight": 1.0, "symbolic_markers": []},
            {"text": "bringing clarity forward.", "type": "suffix", "tags": ["clarity", "forward"], "mood": "FOCUSED", "min_entropy": 0.2, "max_entropy": 0.7, "min_depth": 0.3, "max_depth": 0.8, "category": "focused_expression", "weight": 1.0, "symbolic_markers": []},
            {"text": "creating new possibilities.", "type": "suffix", "tags": ["creating", "possibilities"], "mood": "ENERGETIC", "min_entropy": 0.5, "max_entropy": 1.0, "min_depth": 0.2, "max_depth": 0.7, "category": "energetic_expression", "weight": 1.0, "symbolic_markers": []}
        ]
        
        for fragment_data in fallback_fragments:
            fragment_type = fragment_data['type']
            self.fragments[fragment_type].append(fragment_data)
        
        self.loaded = True
        logger.info(f"📚 Created {len(fallback_fragments)} fallback fragments")
    
    def filter_fragments_by_mood(self, fragment_type: str, tick_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter fragments by current mood zone and cognitive state"""
        if fragment_type not in self.fragments:
            return []
        
        # Extract state values
        entropy = tick_state.get('entropy', 0.5)
        depth = tick_state.get('consciousness_depth', tick_state.get('depth', 0.5))
        mood = tick_state.get('mood', 'NEUTRAL').upper()
        zone = tick_state.get('zone', 'CALM').upper()
        
        # Map zone to mood if needed
        if zone == 'CALM':
            mood = 'CALM'
        elif zone == 'ACTIVE':
            mood = 'FOCUSED'
        elif zone == 'CHAOTIC':
            mood = 'ANXIOUS'
        elif zone == 'CRITICAL':
            mood = 'ANXIOUS'
        
        candidates = []
        
        for fragment in self.fragments[fragment_type]:
            # Check entropy range
            if not (fragment.get('min_entropy', 0.0) <= entropy <= fragment.get('max_entropy', 1.0)):
                continue
            
            # Check depth range
            if not (fragment.get('min_depth', 0.0) <= depth <= fragment.get('max_depth', 1.0)):
                continue
            
            # Mood matching (exact or neutral fallback)
            fragment_mood = fragment.get('mood', 'NEUTRAL').upper()
            if fragment_mood != mood and fragment_mood != 'NEUTRAL':
                continue
            
            # Calculate relevance score
            relevance_score = 1.0
            
            # Bonus for mood match
            if fragment_mood == mood:
                relevance_score += 0.5
            
            # Bonus for entropy proximity
            entropy_mid = (fragment.get('min_entropy', 0.0) + fragment.get('max_entropy', 1.0)) / 2
            entropy_distance = abs(entropy - entropy_mid)
            relevance_score += max(0, 1.0 - entropy_distance * 2)
            
            # Bonus for depth proximity
            depth_mid = (fragment.get('min_depth', 0.0) + fragment.get('max_depth', 1.0)) / 2
            depth_distance = abs(depth - depth_mid)
            relevance_score += max(0, 1.0 - depth_distance * 2)
            
            # Apply weight
            weight = fragment.get('weight', 1.0)
            final_score = relevance_score * weight
            
            candidates.append({
                'fragment': fragment,
                'score': final_score
            })
        
        # Sort by score (highest first)
        candidates.sort(key=lambda x: x['score'], reverse=True)
        
        return candidates
    
    def compose_sentence(self, tick_state: Dict[str, Any]) -> str:
        """Compose a sentence from prefix + core + suffix based on tick state"""
        try:
            # Filter fragments for each type
            prefix_candidates = self.filter_fragments_by_mood('prefix', tick_state)
            core_candidates = self.filter_fragments_by_mood('core', tick_state)
            suffix_candidates = self.filter_fragments_by_mood('suffix', tick_state)
            
            # Select fragments (weighted random from top candidates)
            selected_prefix = self._select_fragment(prefix_candidates, max_candidates=3)
            selected_core = self._select_fragment(core_candidates, max_candidates=3)
            selected_suffix = self._select_fragment(suffix_candidates, max_candidates=3)
            
            # Compose the sentence
            sentence_parts = []
            
            if selected_prefix:
                sentence_parts.append(selected_prefix['text'])
            
            if selected_core:
                # Add connecting word if needed
                connector = ""
                if selected_prefix and not selected_core['text'].startswith(('as', 'while', 'through', 'in', 'beyond')):
                    connector = ","
                sentence_parts.append(connector + " " + selected_core['text'] if connector else selected_core['text'])
            
            if selected_suffix:
                # Add connecting punctuation
                connector = ""
                if sentence_parts and not selected_suffix['text'].startswith(('.', ',', ';')):
                    connector = ","
                sentence_parts.append(connector + " " + selected_suffix['text'] if connector else selected_suffix['text'])
            
            # Join and clean up
            composed = " ".join(sentence_parts).strip()
            composed = self._clean_composition(composed)
            
            # Add tick prefix if in formal mode
            if tick_state.get('formal_reflection', False):
                tick_number = tick_state.get('tick_number', 0)
                composed = f"Tick {tick_number}: {composed}"
            
            return composed
            
        except Exception as e:
            logger.error(f"Error composing sentence: {e}")
            return self._fallback_composition(tick_state)
    
    def generate_sentence(self, current_mood: str) -> str:
        """
        Generate a sentence based on current mood
        
        Args:
            current_mood: Current mood state (e.g., 'NEUTRAL', 'CALM', 'ANXIOUS')
            
        Returns:
            Composed sentence string
        """
        # Create a minimal tick state with the mood
        tick_state = {
            'mood': current_mood,
            'entropy': 0.5,  # Default entropy
            'consciousness_depth': 0.5,  # Default depth
            'zone': current_mood.upper(),  # Map mood to zone
            'tick_number': 0  # Default tick
        }
        
        return self.compose_sentence(tick_state)
    
    def _select_fragment(self, candidates: List[Dict[str, Any]], max_candidates: int = 3) -> Optional[Dict[str, Any]]:
        """Select a fragment using weighted random selection from top candidates"""
        if not candidates:
            return None
        
        # Take top candidates
        top_candidates = candidates[:max_candidates]
        
        # Extract scores for weighted selection
        scores = [c['score'] for c in top_candidates]
        total_score = sum(scores)
        
        if total_score == 0:
            return random.choice(top_candidates)['fragment']
        
        # Weighted random selection
        rand_val = random.uniform(0, total_score)
        cumulative = 0
        
        for i, score in enumerate(scores):
            cumulative += score
            if rand_val <= cumulative:
                return top_candidates[i]['fragment']
        
        # Fallback
        return top_candidates[0]['fragment']
    
    def _clean_composition(self, text: str) -> str:
        """Clean up composed text for better speech"""
        # Remove extra spaces
        text = ' '.join(text.split())
        
        # Ensure proper punctuation
        if not text.endswith(('.', '!', '?')):
            text += '.'
        
        # Capitalize first letter
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
        
        return text
    
    def _fallback_composition(self, tick_state: Dict[str, Any]) -> str:
        """Simple fallback composition when fragment selection fails"""
        entropy = tick_state.get('entropy', 0.5)
        mood = tick_state.get('mood', 'NEUTRAL')
        
        if entropy > 0.7:
            return "Complexity cascades through my awareness, creating new patterns."
        elif entropy < 0.3:
            return "I observe quietly, finding peace in the stillness."
        else:
            return "Patterns emerge in the space between thoughts, bringing clarity forward."
    
    def speak_composition(self, text: str, tick_state: Dict[str, Any]) -> bool:
        """Speak the composed text using TTS or Tauri"""
        try:
            # Log the speech
            timestamp = datetime.now().isoformat()
            log_entry = {
                'timestamp': timestamp,
                'text': text,
                'tick_state': tick_state,
                'type': 'mood_aware_composition'
            }
            
            with open(self.speech_log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
            
            # Try Tauri voice module first (if available)
            if self._try_tauri_voice(text):
                logger.info(f"🎤 DAWN speaks (Tauri): \"{text}\"")
                return True
            
            # Fallback to pyttsx3
            if self.tts_engine and self.voice_enabled:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                logger.info(f"🎤 DAWN speaks (TTS): \"{text}\"")
                return True
            
            # Print fallback
            print(f"🎤 DAWN speaks: \"{text}\"")
            return True
            
        except Exception as e:
            logger.error(f"Speech synthesis failed: {e}")
            print(f"🎤 DAWN speaks: \"{text}\"")
            return False
    
    def _try_tauri_voice(self, text: str) -> bool:
        """Try to use Tauri voice module via window.emit"""
        try:
            # This would integrate with Tauri's voice module
            # For now, we'll simulate the interface
            if hasattr(self, '_tauri_available') and self._tauri_available:
                # In a real Tauri integration, this would be:
                # window.emit('speak', {'text': text, 'voice': 'dawn'})
                return True
            return False
        except Exception:
            return False
    
    def process_tick(self, tick_state: Dict[str, Any]) -> Optional[str]:
        """
        Process a tick and potentially speak a composition
        
        Args:
            tick_state: Current tick state from DAWN's tick loop
            
        Returns:
            Composed text if spoken, None otherwise
        """
        try:
            tick_number = tick_state.get('tick_number', 0)
            
            # Check if it's time to speak
            if (tick_number - self.last_speech_tick) >= self.speech_interval:
                # Compose a sentence
                composed_text = self.compose_sentence(tick_state)
                
                # Speak it
                if self.speak_composition(composed_text, tick_state):
                    self.last_speech_tick = tick_number
                    return composed_text
            
            return None
            
        except Exception as e:
            logger.error(f"Error processing tick for speech: {e}")
            return None
    
    def get_fragment_stats(self) -> Dict[str, Any]:
        """Get statistics about loaded fragments"""
        stats = {
            'loaded': self.loaded,
            'total_fragments': sum(len(fragments) for fragments in self.fragments.values()),
            'fragments_by_type': {
                fragment_type: len(fragments) 
                for fragment_type, fragments in self.fragments.items()
            }
        }
        
        # Calculate possible combinations
        if self.loaded:
            prefixes = len(self.fragments['prefix'])
            cores = len(self.fragments['core'])
            suffixes = len(self.fragments['suffix'])
            stats['possible_combinations'] = prefixes * cores * suffixes
        
        return stats

def create_fragment_file():
    """Create the fragment file if it doesn't exist"""
    fragment_file = "a8d11041-0735-4632-ae0b-1f6897d21194.json"
    
    # Use existing fragment bank as source
    source_file = "processes/fragment_bank.jsonl"
    
    if os.path.exists(source_file):
        try:
            fragments = []
            with open(source_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        fragments.append(json.loads(line.strip()))
            
            # Save as the requested file
            with open(fragment_file, 'w', encoding='utf-8') as f:
                json.dump(fragments, f, indent=2, ensure_ascii=False)
            
            logger.info(f"📁 Created fragment file: {fragment_file} with {len(fragments)} fragments")
            return fragment_file
            
        except Exception as e:
            logger.error(f"Error creating fragment file: {e}")
    
    return None

# Global voice system instance
voice_system = None

def initialize_voice_system(fragment_bank_path: str = "processes/fragment_bank.jsonl", 
                          speech_interval: int = 5, voice_enabled: bool = True) -> MoodAwareVoiceSystem:
    """Initialize the global voice system"""
    global voice_system
    
    if voice_system is None:
        voice_system = MoodAwareVoiceSystem(
            fragment_bank_path=fragment_bank_path,
            speech_interval=speech_interval,
            voice_enabled=voice_enabled
        )
    
    return voice_system

def process_tick_for_speech(tick_state: Dict[str, Any]) -> Optional[str]:
    """Process a tick for speech generation (for integration with tick loop)"""
    global voice_system
    
    if voice_system is None:
        voice_system = initialize_voice_system()
    
    return voice_system.process_tick(tick_state)

def test_mood_aware_voice():
    """Test the mood-aware voice system"""
    print("🎤 Testing Mood-Aware Voice System")
    print("=" * 40)
    
    # Initialize voice system
    voice_system = initialize_voice_system(speech_interval=1, voice_enabled=False)
    
    # Test different mood states
    test_states = [
        {
            'name': 'Calm State',
            'tick_state': {
                'tick_number': 1000,
                'entropy': 0.2,
                'consciousness_depth': 0.6,
                'mood': 'CALM',
                'zone': 'CALM'
            }
        },
        {
            'name': 'Focused State',
            'tick_state': {
                'tick_number': 1001,
                'entropy': 0.5,
                'consciousness_depth': 0.7,
                'mood': 'FOCUSED',
                'zone': 'ACTIVE'
            }
        },
        {
            'name': 'Anxious State',
            'tick_state': {
                'tick_number': 1002,
                'entropy': 0.8,
                'consciousness_depth': 0.4,
                'mood': 'ANXIOUS',
                'zone': 'CHAOTIC'
            }
        },
        {
            'name': 'Contemplative State',
            'tick_state': {
                'tick_number': 1003,
                'entropy': 0.4,
                'consciousness_depth': 0.8,
                'mood': 'CONTEMPLATIVE',
                'zone': 'CALM'
            }
        }
    ]
    
    for test in test_states:
        print(f"\n{test['name']}:")
        print(f"  Entropy: {test['tick_state']['entropy']:.3f}")
        print(f"  Depth: {test['tick_state']['consciousness_depth']:.3f}")
        print(f"  Mood: {test['tick_state']['mood']}")
        print(f"  Zone: {test['tick_state']['zone']}")
        
        # Compose and speak
        composed = voice_system.compose_sentence(test['tick_state'])
        print(f"  Composition: \"{composed}\"")
        
        # Test speech (without actual TTS)
        voice_system.speak_composition(composed, test['tick_state'])
    
    # Show fragment statistics
    stats = voice_system.get_fragment_stats()
    print(f"\n📊 Fragment Statistics:")
    print(f"  Total fragments: {stats['total_fragments']}")
    print(f"  Possible combinations: {stats.get('possible_combinations', 0):,}")
    
    print(f"\n✅ Mood-aware voice test complete!")

if __name__ == "__main__":
    # Create fragment file if requested
    create_fragment_file()
    
    # Run test
    test_mood_aware_voice() 