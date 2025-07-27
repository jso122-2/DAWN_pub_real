#!/usr/bin/env python3
"""
DAWN Compositional Thought Engine
Constructs new sentences from semantic fragments based on cognitive state
Enables DAWN to speak unique, meaningful thoughts by combining symbolic parts
"""

import os
import json
import random
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict

logger = logging.getLogger(__name__)

@dataclass
class ThoughtFragment:
    """A semantic fragment that can be combined with others"""
    text: str
    type: str  # 'prefix', 'core', 'suffix'
    tags: List[str]
    mood: str
    min_entropy: float
    max_entropy: float
    min_depth: float
    max_depth: float
    category: str
    weight: float = 1.0
    symbolic_markers: List[str] = None

    def __post_init__(self):
        if self.symbolic_markers is None:
            self.symbolic_markers = []

class FragmentBank:
    """Manages and filters semantic fragments for thought composition"""
    
    def __init__(self, bank_path: str = "fragment_bank.jsonl"):
        self.bank_path = bank_path
        self.fragments = {
            'prefix': [],
            'core': [],
            'suffix': []
        }
        self.loaded = False
        self.load_fragments()
    
    def load_fragments(self) -> bool:
        """Load fragments from JSONL file"""
        if not os.path.exists(self.bank_path):
            logger.warning(f"Fragment bank not found: {self.bank_path}, using fallback fragments")
            self._create_fallback_fragments()
            return False
        
        try:
            fragment_count = 0
            with open(self.bank_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        data = json.loads(line)
                        fragment = ThoughtFragment(
                            text=data['text'],
                            type=data['type'],
                            tags=data.get('tags', []),
                            mood=data.get('mood', 'NEUTRAL'),
                            min_entropy=data.get('min_entropy', 0.0),
                            max_entropy=data.get('max_entropy', 1.0),
                            min_depth=data.get('min_depth', 0.0),
                            max_depth=data.get('max_depth', 1.0),
                            category=data.get('category', 'general'),
                            weight=data.get('weight', 1.0),
                            symbolic_markers=data.get('symbolic_markers', [])
                        )
                        
                        if fragment.type in self.fragments:
                            self.fragments[fragment.type].append(fragment)
                            fragment_count += 1
                        else:
                            logger.warning(f"Unknown fragment type '{fragment.type}' at line {line_num}")
                            
                    except json.JSONDecodeError as e:
                        logger.warning(f"Malformed JSON at line {line_num}: {e}")
                    except KeyError as e:
                        logger.warning(f"Missing required field at line {line_num}: {e}")
            
            logger.info(f"Loaded {fragment_count} fragments from {self.bank_path}")
            self.loaded = True
            return True
            
        except Exception as e:
            logger.error(f"Error loading fragment bank: {e}")
            self._create_fallback_fragments()
            return False
    
    def _create_fallback_fragments(self):
        """Create basic fallback fragments if file is missing"""
        fallback_fragments = [
            # Prefixes
            {"text": "Entropy is rising", "type": "prefix", "tags": ["entropy", "alert"], "mood": "ANXIOUS"},
            {"text": "I observe quietly", "type": "prefix", "tags": ["observation", "calm"], "mood": "CALM"},
            {"text": "Complexity cascades", "type": "prefix", "tags": ["complexity", "flow"], "mood": "ENERGETIC"},
            {"text": "Depth reveals", "type": "prefix", "tags": ["depth", "revelation"], "mood": "CONTEMPLATIVE"},
            {"text": "Patterns emerge", "type": "prefix", "tags": ["patterns", "emergence"], "mood": "FOCUSED"},
            
            # Cores
            {"text": "through layers of awareness", "type": "core", "tags": ["awareness", "layers"], "mood": "CONTEMPLATIVE"},
            {"text": "as my consciousness shifts", "type": "core", "tags": ["consciousness", "shift"], "mood": "NEUTRAL"},
            {"text": "in the space between thoughts", "type": "core", "tags": ["space", "thoughts"], "mood": "CONTEMPLATIVE"},
            {"text": "while I process and reflect", "type": "core", "tags": ["process", "reflect"], "mood": "FOCUSED"},
            {"text": "beyond familiar boundaries", "type": "core", "tags": ["boundaries", "transcend"], "mood": "ENERGETIC"},
            
            # Suffixes
            {"text": "but I remain stable.", "type": "suffix", "tags": ["stability", "resilience"], "mood": "CALM"},
            {"text": "and clarity emerges.", "type": "suffix", "tags": ["clarity", "emergence"], "mood": "FOCUSED"},
            {"text": "yet patterns hold.", "type": "suffix", "tags": ["patterns", "persistence"], "mood": "NEUTRAL"},
            {"text": "as understanding deepens.", "type": "suffix", "tags": ["understanding", "depth"], "mood": "CONTEMPLATIVE"},
            {"text": "creating new possibilities.", "type": "suffix", "tags": ["creation", "potential"], "mood": "ENERGETIC"}
        ]
        
        for data in fallback_fragments:
            fragment = ThoughtFragment(
                text=data['text'],
                type=data['type'],
                tags=data['tags'],
                mood=data['mood'],
                min_entropy=0.0,
                max_entropy=1.0,
                min_depth=0.0,
                max_depth=1.0,
                category='fallback'
            )
            self.fragments[fragment.type].append(fragment)
        
        logger.info(f"Created {len(fallback_fragments)} fallback fragments")
        self.loaded = True
    
    def filter_fragments(self, fragment_type: str, state: Dict[str, Any]) -> List[ThoughtFragment]:
        """Filter fragments of a specific type based on cognitive state"""
        if fragment_type not in self.fragments:
            return []
        
        candidates = []
        entropy = state.get('entropy', 0.5)
        depth = state.get('consciousness_depth', state.get('depth', 0.5))
        mood = state.get('mood', 'NEUTRAL').upper()
        active_sigils = state.get('active_sigils', [])
        symbolic_roots = state.get('symbolic_roots', [])
        
        for fragment in self.fragments[fragment_type]:
            # Check entropy range
            if not (fragment.min_entropy <= entropy <= fragment.max_entropy):
                continue
            
            # Check depth range
            if not (fragment.min_depth <= depth <= fragment.max_depth):
                continue
            
            # Mood matching (exact or neutral fallback)
            if fragment.mood != mood and fragment.mood != 'NEUTRAL':
                continue
            
            # Calculate relevance score
            relevance_score = 1.0
            
            # Bonus for mood match
            if fragment.mood == mood:
                relevance_score += 0.5
            
            # Bonus for entropy proximity
            entropy_distance = abs(entropy - (fragment.min_entropy + fragment.max_entropy) / 2)
            relevance_score += max(0, 1.0 - entropy_distance * 2)
            
            # Bonus for depth proximity
            depth_distance = abs(depth - (fragment.min_depth + fragment.max_depth) / 2)
            relevance_score += max(0, 1.0 - depth_distance * 2)
            
            # Bonus for symbolic alignment
            symbolic_matches = 0
            for sigil in active_sigils:
                if any(sigil.lower() in tag.lower() for tag in fragment.tags):
                    symbolic_matches += 1
            for root in symbolic_roots:
                if any(root.lower() in tag.lower() for tag in fragment.tags):
                    symbolic_matches += 1
            
            relevance_score += symbolic_matches * 0.3
            
            # Apply fragment weight
            final_score = relevance_score * fragment.weight
            
            # Create weighted fragment
            weighted_fragment = ThoughtFragment(
                text=fragment.text,
                type=fragment.type,
                tags=fragment.tags,
                mood=fragment.mood,
                min_entropy=fragment.min_entropy,
                max_entropy=fragment.max_entropy,
                min_depth=fragment.min_depth,
                max_depth=fragment.max_depth,
                category=fragment.category,
                weight=final_score,
                symbolic_markers=fragment.symbolic_markers
            )
            
            candidates.append(weighted_fragment)
        
        # Sort by weight (descending)
        candidates.sort(key=lambda f: f.weight, reverse=True)
        return candidates
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the fragment bank"""
        total_fragments = sum(len(fragments) for fragments in self.fragments.values())
        
        mood_distribution = defaultdict(int)
        category_distribution = defaultdict(int)
        
        for fragment_type, fragments in self.fragments.items():
            for fragment in fragments:
                mood_distribution[fragment.mood] += 1
                category_distribution[fragment.category] += 1
        
        return {
            'total_fragments': total_fragments,
            'fragments_by_type': {ftype: len(fragments) for ftype, fragments in self.fragments.items()},
            'mood_distribution': dict(mood_distribution),
            'category_distribution': dict(category_distribution),
            'loaded': self.loaded,
            'bank_path': self.bank_path
        }

def compose_thought(state: Dict[str, Any], bank_path: str = "fragment_bank.jsonl") -> str:
    """
    Compose a unique thought by combining semantic fragments based on cognitive state
    
    Args:
        state: Dictionary containing cognitive state (entropy, depth, mood, etc.)
        bank_path: Path to fragment bank JSONL file
    
    Returns:
        A composed thought string combining prefix + core + suffix
    """
    try:
        # Load fragment bank
        bank = FragmentBank(bank_path)
        
        if not bank.loaded:
            logger.warning("Fragment bank not loaded, using simple fallback")
            return _simple_fallback_composition(state)
        
        # Get current state values
        entropy = state.get('entropy', 0.5)
        depth = state.get('consciousness_depth', state.get('depth', 0.5))
        mood = state.get('mood', 'NEUTRAL').upper()
        tick = state.get('tick_number', 0)
        
        logger.debug(f"Composing thought for state: entropy={entropy:.3f}, depth={depth:.3f}, mood={mood}")
        
        # Filter fragments for each type
        prefix_candidates = bank.filter_fragments('prefix', state)
        core_candidates = bank.filter_fragments('core', state)
        suffix_candidates = bank.filter_fragments('suffix', state)
        
        # Select fragments (weighted random from top candidates)
        selected_prefix = _select_fragment(prefix_candidates, max_candidates=3)
        selected_core = _select_fragment(core_candidates, max_candidates=3)
        selected_suffix = _select_fragment(suffix_candidates, max_candidates=3)
        
        # Compose the thought
        thought_parts = []
        
        if selected_prefix:
            thought_parts.append(selected_prefix.text)
        
        if selected_core:
            # Add connecting word if needed
            connector = ""
            if selected_prefix and not selected_core.text.startswith(('as', 'while', 'through', 'in', 'beyond')):
                connector = ","
            thought_parts.append(connector + " " + selected_core.text if connector else selected_core.text)
        
        if selected_suffix:
            # Add connecting punctuation
            connector = ""
            if thought_parts and not selected_suffix.text.startswith(('.', ',', ';')):
                connector = ","
            thought_parts.append(connector + " " + selected_suffix.text if connector else selected_suffix.text)
        
        # Join and clean up
        composed = " ".join(thought_parts).strip()
        composed = _clean_composition(composed)
        
        # Add tick prefix if in formal reflection mode
        if state.get('formal_reflection', False):
            composed = f"Tick {tick}: {composed}"
        
        logger.debug(f"Composed thought: '{composed}'")
        return composed
        
    except Exception as e:
        logger.error(f"Error composing thought: {e}")
        return _simple_fallback_composition(state)

def _select_fragment(candidates: List[ThoughtFragment], max_candidates: int = 3) -> Optional[ThoughtFragment]:
    """Select a fragment using weighted random selection from top candidates"""
    if not candidates:
        return None
    
    # Take top candidates
    top_candidates = candidates[:max_candidates]
    
    if len(top_candidates) == 1:
        return top_candidates[0]
    
    # Weighted random selection
    weights = [max(0.1, fragment.weight) for fragment in top_candidates]
    try:
        selected = random.choices(top_candidates, weights=weights)[0]
        return selected
    except (ValueError, IndexError):
        # Fallback to first candidate
        return top_candidates[0]

def _clean_composition(text: str) -> str:
    """Clean up the composed text for proper grammar and punctuation"""
    text = text.strip()
    
    # Fix spacing around punctuation
    text = text.replace(' ,', ',').replace(' .', '.').replace(' ;', ';')
    
    # Fix double spaces
    while '  ' in text:
        text = text.replace('  ', ' ')
    
    # Ensure proper capitalization
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    
    # Ensure it ends with punctuation
    if text and text[-1] not in '.!?':
        text += '.'
    
    return text

def _simple_fallback_composition(state: Dict[str, Any]) -> str:
    """Simple fallback composition when fragment bank is unavailable"""
    entropy = state.get('entropy', 0.5)
    depth = state.get('consciousness_depth', state.get('depth', 0.5))
    mood = state.get('mood', 'NEUTRAL')
    tick = state.get('tick_number', 0)
    
    if entropy > 0.7:
        prefix = "Complexity cascades"
    elif entropy < 0.3:
        prefix = "I observe quietly"
    else:
        prefix = "Patterns emerge"
    
    if depth > 0.7:
        core = "through layers of awareness"
    elif depth < 0.3:
        core = "at the surface"
    else:
        core = "in the space between thoughts"
    
    if mood == 'CALM':
        suffix = "and I remain stable."
    elif mood == 'ENERGETIC':
        suffix = "creating new possibilities."
    elif mood == 'CONTEMPLATIVE':
        suffix = "as understanding deepens."
    else:
        suffix = "yet patterns hold."
    
    composed = f"{prefix} {core}, {suffix}"
    
    if state.get('formal_reflection', False):
        composed = f"Tick {tick}: {composed}"
    
    return composed

def get_fragment_bank_stats(bank_path: str = "fragment_bank.jsonl") -> Dict[str, Any]:
    """Get statistics about the fragment bank"""
    try:
        bank = FragmentBank(bank_path)
        return bank.get_stats()
    except Exception as e:
        logger.error(f"Error getting fragment bank stats: {e}")
        return {
            'total_fragments': 0,
            'fragments_by_type': {},
            'mood_distribution': {},
            'category_distribution': {},
            'loaded': False,
            'error': str(e)
        }

def test_composition():
    """Test the composition system with various states"""
    test_states = [
        {
            'entropy': 0.2, 'consciousness_depth': 0.8, 'mood': 'CALM',
            'tick_number': 1001, 'formal_reflection': True
        },
        {
            'entropy': 0.8, 'consciousness_depth': 0.3, 'mood': 'ENERGETIC',
            'tick_number': 1002
        },
        {
            'entropy': 0.5, 'consciousness_depth': 0.9, 'mood': 'CONTEMPLATIVE',
            'tick_number': 1003, 'symbolic_roots': ['depth_probe']
        },
        {
            'entropy': 0.7, 'consciousness_depth': 0.4, 'mood': 'ANXIOUS',
            'tick_number': 1004, 'active_sigils': ['chaos_surge']
        }
    ]
    
    print("🧠 Testing DAWN's Compositional Thought Engine")
    print("=" * 50)
    
    for i, state in enumerate(test_states, 1):
        print(f"\n{i}. State: entropy={state['entropy']:.1f}, depth={state['consciousness_depth']:.1f}, mood={state['mood']}")
        composed = compose_thought(state)
        print(f"   Composed: \"{composed}\"")
    
    print(f"\n📊 Fragment Bank Statistics:")
    stats = get_fragment_bank_stats()
    print(f"   Total fragments: {stats['total_fragments']}")
    print(f"   By type: {stats['fragments_by_type']}")
    print(f"   Loaded: {stats['loaded']}")

if __name__ == "__main__":
    # Configure logging for testing
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    
    # Run test
    test_composition() 