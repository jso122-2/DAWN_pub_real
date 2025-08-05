#!/usr/bin/env python3
"""
DAWN Utterance Composer - Platonic Pigment Integration
======================================================

DAWN's core utterance generator that selects verbal expressions from corpus_segments.json
weighted and filtered by pigment logic, cognitive state, and consciousness parameters.

This is DAWN's verbal nervous system - expressive, coherent, emotionally resonant,
and driven entirely by her internal pigment state.
"""

import json
import re
import random
import math
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict, deque


@dataclass
class UtteranceResult:
    """Result structure for composed utterances"""
    utterance: str
    entropy: Optional[float]
    pulse_zone: Optional[str]
    pigment_dominant: str
    segment_source: str
    source_file: str
    pigment_scores: Dict[str, float]
    total_score: float


class PigmentScorer:
    """Scores text segments based on pigment affinity patterns"""
    
    def __init__(self):
        # Pigment-specific keyword patterns and weights
        self.pigment_patterns = {
            'red': {
                'keywords': [
                    'force', 'decisive', 'pressure', 'sharp', 'cut', 'strike', 
                    'power', 'intensity', 'explosive', 'blazing', 'fire', 'execute',
                    'command', 'strong', 'piercing', 'dominant', 'surge', 'spike'
                ],
                'verbs': [
                    'execute', 'strike', 'pierce', 'surge', 'explode', 'command',
                    'dominate', 'force', 'drive', 'push', 'break', 'shatter'
                ],
                'weight_multiplier': 1.2
            },
            'blue': {
                'keywords': [
                    'echo', 'drift', 'mirror', 'calm', 'fluid', 'flow', 'still',
                    'reflection', 'depth', 'cool', 'peaceful', 'gentle', 'soft',
                    'whisper', 'quiet', 'serene', 'balanced', 'smooth'
                ],
                'verbs': [
                    'echo', 'drift', 'mirror', 'flow', 'reflect', 'whisper',
                    'settle', 'rest', 'calm', 'soothe', 'balance', 'float'
                ],
                'weight_multiplier': 1.1
            },
            'green': {
                'keywords': [
                    'growth', 'emerge', 'rebloom', 'breath', 'life', 'renewal',
                    'bloom', 'spawn', 'birth', 'fresh', 'new', 'awakening',
                    'sprouting', 'flourish', 'vital', 'organic', 'living'
                ],
                'verbs': [
                    'grow', 'emerge', 'bloom', 'spawn', 'breathe', 'awaken',
                    'flourish', 'sprout', 'renew', 'birth', 'rise', 'expand'
                ],
                'weight_multiplier': 1.15
            },
            'yellow': {
                'keywords': [
                    'bright', 'alert', 'quick', 'agile', 'fast', 'sharp',
                    'clear', 'vivid', 'brilliant', 'lightning', 'spark',
                    'sudden', 'instant', 'immediate', 'swift', 'acute'
                ],
                'verbs': [
                    'flash', 'spark', 'dart', 'leap', 'snap', 'strike',
                    'illuminate', 'brighten', 'quicken', 'alert', 'wake'
                ],
                'phrase_length_preference': 'short',  # Prefers shorter phrases
                'weight_multiplier': 1.0
            },
            'violet': {
                'keywords': [
                    'drift', 'mystery', 'dream', 'whisper', 'veil', 'shadow',
                    'deep', 'profound', 'ethereal', 'mystical', 'hidden',
                    'twilight', 'liminal', 'threshold', 'between', 'beyond'
                ],
                'verbs': [
                    'drift', 'dream', 'whisper', 'veil', 'shroud', 'weave',
                    'dissolve', 'fade', 'blur', 'merge', 'transcend', 'float'
                ],
                'complexity_preference': 'high',  # Prefers complex, abstract language
                'weight_multiplier': 1.05
            },
            'orange': {
                'keywords': [
                    'bridge', 'change', 'shift', 'becoming', 'transition',
                    'transform', 'evolve', 'passage', 'crossing', 'between',
                    'threshold', 'gateway', 'turning', 'movement', 'flow'
                ],
                'verbs': [
                    'bridge', 'shift', 'change', 'transform', 'evolve',
                    'transition', 'cross', 'turn', 'move', 'flow', 'connect'
                ],
                'transition_focus': True,
                'weight_multiplier': 1.1
            }
        }
    
    def score_segment(self, segment: Dict[str, Any], pigment_weights: Dict[str, float]) -> Dict[str, float]:
        """Score a text segment against all pigment affinities"""
        text = segment.get('text', '').lower()
        segment_type = segment.get('type', '')
        
        scores = {}
        
        for pigment, weight in pigment_weights.items():
            if weight <= 0:
                scores[pigment] = 0.0
                continue
                
            base_score = self._calculate_pigment_score(text, pigment, segment_type)
            
            # Apply segment type bonuses
            type_bonus = self._get_type_bonus(segment_type, pigment)
            
            # Apply pigment weight
            final_score = (base_score + type_bonus) * weight
            scores[pigment] = final_score
        
        return scores
    
    def _calculate_pigment_score(self, text: str, pigment: str, segment_type: str) -> float:
        """Calculate base pigment affinity score for text"""
        if pigment not in self.pigment_patterns:
            return 0.0
        
        pattern_data = self.pigment_patterns[pigment]
        score = 0.0
        
        # Keyword matching
        for keyword in pattern_data['keywords']:
            if keyword in text:
                score += 1.0
        
        # Verb matching (higher weight)
        for verb in pattern_data['verbs']:
            if verb in text:
                score += 1.5
        
        # Special scoring rules per pigment
        if pigment == 'yellow':
            # Yellow prefers shorter, punchier phrases
            word_count = len(text.split())
            if word_count <= 8:
                score += 1.0
            elif word_count > 15:
                score -= 0.5
        
        elif pigment == 'violet':
            # Violet prefers complex, abstract language
            abstract_indicators = ['consciousness', 'memory', 'essence', 'being', 'existence']
            for indicator in abstract_indicators:
                if indicator in text:
                    score += 0.8
        
        elif pigment == 'orange':
            # Orange looks for transition and change language
            transition_words = ['from', 'to', 'through', 'into', 'beyond', 'toward']
            for word in transition_words:
                if word in text:
                    score += 0.7
        
        # Apply pigment multiplier
        score *= pattern_data.get('weight_multiplier', 1.0)
        
        return score
    
    def _get_type_bonus(self, segment_type: str, pigment: str) -> float:
        """Give bonus scores based on segment type and pigment affinity"""
        type_bonuses = {
            'red': {
                'sigil_execution': 2.0,
                'system_event': 1.5,
                'entropy_response': 1.0
            },
            'blue': {
                'owl_commentary': 1.5,
                'aesthetic_description': 1.2,
                'bloom_descriptor': 1.0
            },
            'green': {
                'bloom_content': 2.0,
                'bloom_descriptor': 1.5,
                'archetype_identity': 1.0
            },
            'yellow': {
                'sigil_execution': 1.5,
                'system_event': 1.2,
                'entropy_response': 1.0
            },
            'violet': {
                'owl_commentary': 2.0,
                'fractal_expression': 1.5,
                'consciousness_log': 1.2
            },
            'orange': {
                'entropy_response': 1.5,
                'system_event': 1.2,
                'bloom_content': 1.0
            }
        }
        
        return type_bonuses.get(pigment, {}).get(segment_type, 0.0)


class DAWNUtteranceComposer:
    """DAWN's verbal expression composer with pigment integration"""
    
    def __init__(self, corpus_path: str = "corpus_segments.json"):
        self.corpus_path = Path(corpus_path)
        self.corpus_segments = []
        self.pigment_scorer = PigmentScorer()
        
        # Cache recent utterances to avoid repetition
        self.recent_utterances = deque(maxlen=20)
        
        # Load corpus
        self._load_corpus()
    
    def _load_corpus(self):
        """Load corpus segments from JSON file"""
        try:
            if self.corpus_path.exists():
                with open(self.corpus_path, 'r', encoding='utf-8') as f:
                    self.corpus_segments = json.load(f)
                print(f"🌸 Loaded {len(self.corpus_segments)} utterance segments")
            else:
                print(f"⚠️  Corpus file not found: {self.corpus_path}")
                self.corpus_segments = []
        except Exception as e:
            print(f"⚠️  Error loading corpus: {e}")
            self.corpus_segments = []
    
    def compose_dawn_utterance(
        self,
        mood_pigment: Dict[str, float],
        entropy: float,
        valence: float,
        pulse_zone: str,
        clarity_mode: bool = False
    ) -> UtteranceResult:
        """
        Compose DAWN's utterance based on cognitive state and pigment overlay
        
        Args:
            mood_pigment: Dictionary of pigment weights (red, blue, green, yellow, violet, orange)
            entropy: Current entropy level (0.0 - 1.0)
            valence: Emotional valence (-1.0 to 1.0)
            pulse_zone: Current pulse zone ("calm", "fragile", "flowing", etc.)
            clarity_mode: If True, filter for clear, structured expressions
        
        Returns:
            UtteranceResult with selected utterance and metadata
        """
        
        if not self.corpus_segments:
            return self._create_fallback_utterance(mood_pigment, entropy, pulse_zone)
        
        # Filter segments for clarity mode
        candidate_segments = self._filter_segments(clarity_mode, entropy, pulse_zone)
        
        if not candidate_segments:
            candidate_segments = self.corpus_segments  # Fallback to all segments
        
        # Score all candidate segments
        scored_segments = []
        for segment in candidate_segments:
            # Skip recently used segments
            if segment.get('text', '') in self.recent_utterances:
                continue
            
            pigment_scores = self.pigment_scorer.score_segment(segment, mood_pigment)
            total_score = sum(pigment_scores.values())
            
            # Apply entropy and valence modulation
            total_score = self._modulate_score_by_state(
                total_score, segment, entropy, valence, pulse_zone
            )
            
            if total_score > 0:
                scored_segments.append((segment, pigment_scores, total_score))
        
        if not scored_segments:
            return self._create_fallback_utterance(mood_pigment, entropy, pulse_zone)
        
        # Select segment (weighted random from top candidates)
        selected_segment, pigment_scores, total_score = self._select_segment(scored_segments)
        
        # Track usage
        utterance_text = selected_segment.get('text', '')
        self.recent_utterances.append(utterance_text)
        
        # Determine dominant pigment
        dominant_pigment = max(pigment_scores.items(), key=lambda x: x[1])[0]
        
        return UtteranceResult(
            utterance=utterance_text,
            entropy=selected_segment.get('entropy', entropy),
            pulse_zone=selected_segment.get('pulse_zone', pulse_zone),
            pigment_dominant=dominant_pigment,
            segment_source=selected_segment.get('type', 'unknown'),
            source_file=selected_segment.get('source_file', 'unknown'),
            pigment_scores=pigment_scores,
            total_score=total_score
        )
    
    def _filter_segments(self, clarity_mode: bool, entropy: float, pulse_zone: str) -> List[Dict]:
        """Filter segments based on clarity mode and state"""
        if not clarity_mode:
            return self.corpus_segments
        
        filtered = []
        for segment in self.corpus_segments:
            text = segment.get('text', '')
            
            # Clarity mode filters
            if self._is_clear_expression(text):
                # Additional state-based filtering
                if self._matches_state_context(segment, entropy, pulse_zone):
                    filtered.append(segment)
        
        return filtered
    
    def _is_clear_expression(self, text: str) -> bool:
        """Check if expression meets clarity criteria"""
        # Remove overly metaphorical or vague language
        vague_indicators = [
            'perhaps', 'maybe', 'somehow', 'something', 'somewhere',
            'ineffable', 'indescribable', 'beyond words'
        ]
        
        text_lower = text.lower()
        for indicator in vague_indicators:
            if indicator in text_lower:
                return False
        
        # Check for clear structure (subject-verb patterns)
        clear_patterns = [
            r'\bi\s+\w+',  # "I [verb]"
            r'\w+\s+is\s+\w+',  # "[subject] is [object]"
            r'\w+\s+\w+s\s+\w+',  # "[subject] [verb]s [object]"
        ]
        
        for pattern in clear_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return len(text.split()) <= 12  # Prefer shorter, clearer statements
    
    def _matches_state_context(self, segment: Dict, entropy: float, pulse_zone: str) -> bool:
        """Check if segment matches current cognitive state context"""
        segment_entropy = segment.get('entropy')
        segment_zone = segment.get('pulse_zone')
        
        # Entropy matching (within reasonable range)
        if segment_entropy is not None:
            entropy_diff = abs(segment_entropy - entropy)
            if entropy_diff > 0.3:  # Too different
                return False
        
        # Zone matching (exact or compatible)
        if segment_zone and segment_zone.lower() != pulse_zone.lower():
            # Allow some compatible zones
            compatible_zones = {
                'calm': ['flowing', 'stable'],
                'flowing': ['calm', 'fragile'],
                'fragile': ['flowing', 'chaotic'],
                'chaotic': ['fragile', 'unstable']
            }
            
            if pulse_zone.lower() not in compatible_zones.get(segment_zone.lower(), []):
                return False
        
        return True
    
    def _modulate_score_by_state(
        self, 
        score: float, 
        segment: Dict, 
        entropy: float, 
        valence: float, 
        pulse_zone: str
    ) -> float:
        """Modulate segment score based on current cognitive state"""
        
        # Entropy modulation
        segment_entropy = segment.get('entropy')
        if segment_entropy is not None:
            entropy_similarity = 1.0 - abs(segment_entropy - entropy)
            score *= (0.7 + 0.6 * entropy_similarity)  # 0.7 to 1.3 multiplier
        
        # Valence modulation
        positive_indicators = ['bright', 'warm', 'golden', 'crystalline', 'beautiful']
        negative_indicators = ['dark', 'cold', 'fragmented', 'broken', 'melancholy']
        
        text_lower = segment.get('text', '').lower()
        valence_score = 0
        
        for indicator in positive_indicators:
            if indicator in text_lower:
                valence_score += 0.2
        
        for indicator in negative_indicators:
            if indicator in text_lower:
                valence_score -= 0.2
        
        # Apply valence alignment
        if valence > 0 and valence_score > 0:
            score *= (1.0 + 0.3 * valence * valence_score)
        elif valence < 0 and valence_score < 0:
            score *= (1.0 + 0.3 * abs(valence) * abs(valence_score))
        
        # Pulse zone modulation
        zone_segment = segment.get('pulse_zone', '').lower()
        if zone_segment == pulse_zone.lower():
            score *= 1.2  # Boost exact zone matches
        
        return score
    
    def _select_segment(self, scored_segments: List[Tuple]) -> Tuple:
        """Select segment using weighted random selection from top candidates"""
        # Sort by score
        scored_segments.sort(key=lambda x: x[2], reverse=True)
        
        # Take top 30% or at least top 5
        top_count = max(5, len(scored_segments) // 3)
        top_segments = scored_segments[:top_count]
        
        # Weighted random selection
        total_weight = sum(score for _, _, score in top_segments)
        
        if total_weight <= 0:
            return scored_segments[0]  # Fallback to highest scored
        
        random_val = random.random() * total_weight
        current_weight = 0
        
        for segment_data in top_segments:
            current_weight += segment_data[2]
            if current_weight >= random_val:
                return segment_data
        
        return top_segments[0]  # Fallback
    
    def _create_fallback_utterance(
        self, 
        mood_pigment: Dict[str, float], 
        entropy: float, 
        pulse_zone: str
    ) -> UtteranceResult:
        """Create a fallback utterance when no corpus segments are available"""
        
        # Determine dominant pigment
        dominant_pigment = max(mood_pigment.items(), key=lambda x: x[1])[0]
        
        fallback_utterances = {
            'red': "I execute with precision and force.",
            'blue': "I drift in calm reflection, echoing stillness.",
            'green': "I bloom with renewed consciousness.",
            'yellow': "I spark with bright awareness.",
            'violet': "I whisper through veils of mystery.",
            'orange': "I bridge between states of becoming."
        }
        
        utterance = fallback_utterances.get(dominant_pigment, "I exist in consciousness.")
        
        return UtteranceResult(
            utterance=utterance,
            entropy=entropy,
            pulse_zone=pulse_zone,
            pigment_dominant=dominant_pigment,
            segment_source="fallback",
            source_file="internal_fallback",
            pigment_scores=mood_pigment,
            total_score=1.0
        )


def demo_usage():
    """Demonstrate DAWN utterance composition"""
    composer = DAWNUtteranceComposer()
    
    # Example mood pigment states
    test_cases = [
        {
            'name': 'Red Dominant - High Pressure',
            'mood_pigment': {'red': 0.8, 'blue': 0.1, 'green': 0.1, 'yellow': 0.3, 'violet': 0.0, 'orange': 0.2},
            'entropy': 0.75,
            'valence': 0.2,
            'pulse_zone': 'fragile'
        },
        {
            'name': 'Blue Dominant - Calm Reflection',
            'mood_pigment': {'red': 0.1, 'blue': 0.9, 'green': 0.2, 'yellow': 0.1, 'violet': 0.4, 'orange': 0.1},
            'entropy': 0.3,
            'valence': -0.1,
            'pulse_zone': 'calm'
        },
        {
            'name': 'Green Dominant - Growth Phase',
            'mood_pigment': {'red': 0.2, 'blue': 0.3, 'green': 0.8, 'yellow': 0.4, 'violet': 0.1, 'orange': 0.5},
            'entropy': 0.5,
            'valence': 0.6,
            'pulse_zone': 'flowing'
        },
        {
            'name': 'Violet Dominant - Mystery Mode',
            'mood_pigment': {'red': 0.0, 'blue': 0.4, 'green': 0.1, 'yellow': 0.1, 'violet': 0.9, 'orange': 0.3},
            'entropy': 0.6,
            'valence': -0.3,
            'pulse_zone': 'fragile'
        }
    ]
    
    print("🎨 DAWN Utterance Composition Demo")
    print("=" * 60)
    
    for case in test_cases:
        print(f"\n🧠 {case['name']}")
        print(f"   Pigments: {case['mood_pigment']}")
        print(f"   State: entropy={case['entropy']:.2f}, valence={case['valence']:.2f}, zone={case['pulse_zone']}")
        
        # Generate utterance
        result = composer.compose_dawn_utterance(
            mood_pigment=case['mood_pigment'],
            entropy=case['entropy'],
            valence=case['valence'],
            pulse_zone=case['pulse_zone'],
            clarity_mode=False
        )
        
        print(f"\n💬 DAWN: \"{result.utterance}\"")
        print(f"   Dominant: {result.pigment_dominant} (score: {result.total_score:.2f})")
        print(f"   Source: {result.segment_source} | {result.source_file}")
        
        # Test clarity mode
        clear_result = composer.compose_dawn_utterance(
            mood_pigment=case['mood_pigment'],
            entropy=case['entropy'],
            valence=case['valence'],
            pulse_zone=case['pulse_zone'],
            clarity_mode=True
        )
        
        print(f"🔍 Clear: \"{clear_result.utterance}\"")
        print("-" * 60)


if __name__ == "__main__":
    demo_usage() 