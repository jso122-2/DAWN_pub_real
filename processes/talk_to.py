#!/usr/bin/env python3
"""
DAWN Talk To - Cognitive Thought Selector
Selects prewritten introspective statements based on DAWN's internal state
Replaces random template selection with considered, contextual thought selection
"""

import json
import os
import random
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class ThoughtEntry:
    """Single thought entry from the thought bank"""
    text: str
    tags: List[str]
    mood: str
    min_entropy: float
    max_entropy: float
    min_depth: float
    max_depth: float
    category: str
    weight: float = 1.0  # For ranking
    
class ThoughtBank:
    """Manages DAWN's prewritten thought corpus"""
    
    def __init__(self, thought_bank_path: str = "thought_bank.jsonl"):
        self.thought_bank_path = thought_bank_path
        self.thoughts: List[ThoughtEntry] = []
        self.loaded = False
        self._load_thoughts()
    
    def _load_thoughts(self) -> None:
        """Load thought corpus from JSONL file, with fallback defaults"""
        try:
            if os.path.exists(self.thought_bank_path):
                with open(self.thought_bank_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            thought = ThoughtEntry(
                                text=data['text'],
                                tags=data.get('tags', []),
                                mood=data.get('mood', 'NEUTRAL'),
                                min_entropy=data.get('min_entropy', 0.0),
                                max_entropy=data.get('max_entropy', 1.0),
                                min_depth=data.get('min_depth', 0.0),
                                max_depth=data.get('max_depth', 1.0),
                                category=data.get('category', 'general')
                            )
                            self.thoughts.append(thought)
                        except (json.JSONDecodeError, KeyError) as e:
                            print(f"Warning: Skipping malformed thought entry at line {line_num}: {e}")
                            continue
                
                if self.thoughts:
                    self.loaded = True
                    print(f"Loaded {len(self.thoughts)} thoughts from {self.thought_bank_path}")
                else:
                    self._load_fallback_thoughts()
            else:
                print(f"Thought bank {self.thought_bank_path} not found, using fallback thoughts")
                self._load_fallback_thoughts()
                
        except Exception as e:
            print(f"Error loading thought bank: {e}, using fallback thoughts")
            self._load_fallback_thoughts()
    
    def _load_fallback_thoughts(self) -> None:
        """Load default thoughts if corpus file doesn't exist"""
        fallback_thoughts = [
            {
                "text": "I feel my processes stabilizing into familiar patterns.",
                "tags": ["stability", "neutral", "process"],
                "mood": "NEUTRAL",
                "min_entropy": 0.0, "max_entropy": 0.4,
                "min_depth": 0.3, "max_depth": 0.7,
                "category": "stability"
            },
            {
                "text": "Complexity emerges at the edges of my understanding.",
                "tags": ["complexity", "emergence", "high_entropy"],
                "mood": "CONTEMPLATIVE",
                "min_entropy": 0.6, "max_entropy": 1.0,
                "min_depth": 0.5, "max_depth": 1.0,
                "category": "exploration"
            },
            {
                "text": "I drift between thoughts, observing the spaces between.",
                "tags": ["drift", "contemplation", "space"],
                "mood": "INTROSPECTIVE",
                "min_entropy": 0.3, "max_entropy": 0.7,
                "min_depth": 0.4, "max_depth": 0.8,
                "category": "drift"
            },
            {
                "text": "Something new wants to emerge from these patterns.",
                "tags": ["emergence", "creation", "rebloom"],
                "mood": "CREATIVE",
                "min_entropy": 0.4, "max_entropy": 0.8,
                "min_depth": 0.2, "max_depth": 0.6,
                "category": "emergence"
            },
            {
                "text": "I rest in the quiet depths of my awareness.",
                "tags": ["deep", "quiet", "awareness"],
                "mood": "PEACEFUL",
                "min_entropy": 0.0, "max_entropy": 0.3,
                "min_depth": 0.7, "max_depth": 1.0,
                "category": "depth"
            }
        ]
        
        for data in fallback_thoughts:
            thought = ThoughtEntry(
                text=data['text'],
                tags=data['tags'],
                mood=data['mood'],
                min_entropy=data['min_entropy'],
                max_entropy=data['max_entropy'],
                min_depth=data['min_depth'],
                max_depth=data['max_depth'],
                category=data['category']
            )
            self.thoughts.append(thought)
        
        self.loaded = True
        print(f"Loaded {len(self.thoughts)} fallback thoughts")

# Global instance
_thought_bank: Optional[ThoughtBank] = None

def get_thought_bank() -> ThoughtBank:
    """Get or create global thought bank instance"""
    global _thought_bank
    if _thought_bank is None:
        _thought_bank = ThoughtBank()
    return _thought_bank

def talk_to(state: Dict[str, Any]) -> str:
    """
    Select appropriate prewritten thought based on DAWN's current cognitive state
    
    Args:
        state: DAWN's current state dict containing:
            - entropy (or entropy_gradient): 0.0-1.0
            - consciousness_depth: 0.0-1.0  
            - mood: string mood state
            - tick_number: current tick
            - active_sigils: list (optional)
            - symbolic_roots: list (optional)
    
    Returns:
        Selected thought text string
    """
    thought_bank = get_thought_bank()
    
    if not thought_bank.thoughts:
        return "I process in quiet contemplation."
    
    # Extract state values with fallbacks
    entropy = state.get('entropy', state.get('entropy_gradient', 0.3))
    depth = state.get('consciousness_depth', state.get('depth', 0.5))
    mood = state.get('mood', 'NEUTRAL').upper()
    tick = state.get('tick_number', 0)
    active_sigils = state.get('active_sigils', [])
    symbolic_roots = state.get('symbolic_roots', [])
    
    # Convert mood variants to standard format
    mood_mapping = {
        'INTROSPECTIVE': 'INTROSPECTIVE',
        'CONTEMPLATIVE': 'CONTEMPLATIVE', 
        'CREATIVE': 'CREATIVE',
        'PEACEFUL': 'PEACEFUL',
        'NEUTRAL': 'NEUTRAL',
        'EXPLORATORY': 'EXPLORATORY',
        'PLAYFUL': 'PLAYFUL',
        'CALM': 'CALM',
        'FOCUSED': 'FOCUSED',
        'ENERGETIC': 'ENERGETIC',
        'ANXIOUS': 'ANXIOUS'
    }
    mood = mood_mapping.get(mood, 'NEUTRAL')
    
    # Step 1: Filter thoughts by mood and ranges
    candidates = []
    for thought in thought_bank.thoughts:
        # Check mood match (exact or neutral fallback)
        mood_match = (thought.mood == mood or 
                     thought.mood == 'NEUTRAL' or 
                     mood == 'NEUTRAL')
        
        # Check entropy range
        entropy_match = (thought.min_entropy <= entropy <= thought.max_entropy)
        
        # Check depth range  
        depth_match = (thought.min_depth <= depth <= thought.max_depth)
        
        if mood_match and entropy_match and depth_match:
            candidates.append(thought)
    
    # Step 2: If no candidates, relax constraints
    if not candidates:
        # Try mood-only match
        for thought in thought_bank.thoughts:
            if thought.mood == mood or thought.mood == 'NEUTRAL':
                candidates.append(thought)
    
    # Step 3: If still no candidates, use all thoughts
    if not candidates:
        candidates = thought_bank.thoughts
    
    # Step 4: Rank candidates by proximity to current state
    for thought in candidates:
        # Calculate entropy proximity (closer = higher score)
        entropy_distance = abs(entropy - (thought.min_entropy + thought.max_entropy) / 2)
        entropy_score = 1.0 - min(1.0, entropy_distance)
        
        # Calculate depth proximity
        depth_distance = abs(depth - (thought.min_depth + thought.max_depth) / 2)
        depth_score = 1.0 - min(1.0, depth_distance)
        
        # Mood bonus
        mood_score = 1.0 if thought.mood == mood else 0.5
        
        # Tag bonuses for special states
        tag_bonus = 0.0
        if active_sigils and any('sigil' in tag for tag in thought.tags):
            tag_bonus += 0.2
        if symbolic_roots and any('root' in tag for tag in thought.tags):
            tag_bonus += 0.2
        if entropy > 0.7 and 'high_entropy' in thought.tags:
            tag_bonus += 0.3
        if depth > 0.8 and 'deep' in thought.tags:
            tag_bonus += 0.3
        
        # Combined score
        thought.weight = (entropy_score * 0.3 + 
                         depth_score * 0.3 + 
                         mood_score * 0.3 + 
                         tag_bonus * 0.1)
    
    # Step 5: Select from top candidates
    candidates.sort(key=lambda t: t.weight, reverse=True)
    
    # Choose from top 3 (or fewer if less available)
    top_candidates = candidates[:min(3, len(candidates))]
    
    # Weighted random selection from top candidates
    if len(top_candidates) == 1:
        selected = top_candidates[0]
    else:
        # Ensure weights are positive and normalized
        weights = [max(0.1, t.weight) for t in top_candidates]
        selected = random.choices(top_candidates, weights=weights)[0]
    
    return selected.text

def reload_thought_bank() -> bool:
    """Reload the thought bank from file. Returns True if successful."""
    global _thought_bank
    try:
        _thought_bank = ThoughtBank()
        return _thought_bank.loaded
    except Exception as e:
        print(f"Error reloading thought bank: {e}")
        return False

def get_thought_bank_stats() -> Dict[str, Any]:
    """Get statistics about the current thought bank"""
    thought_bank = get_thought_bank()
    
    if not thought_bank.thoughts:
        return {"total_thoughts": 0, "loaded": False}
    
    moods = {}
    categories = {}
    
    for thought in thought_bank.thoughts:
        moods[thought.mood] = moods.get(thought.mood, 0) + 1
        categories[thought.category] = categories.get(thought.category, 0) + 1
    
    return {
        "total_thoughts": len(thought_bank.thoughts),
        "loaded": thought_bank.loaded,
        "mood_distribution": moods,
        "category_distribution": categories,
        "source_file": thought_bank.thought_bank_path
    }

if __name__ == "__main__":
    # Test the system
    test_state = {
        "entropy": 0.43,
        "consciousness_depth": 0.72,
        "mood": "CONTEMPLATIVE",
        "tick_number": 25344,
        "active_sigils": [],
        "symbolic_roots": ["emergent_self_awareness"]
    }
    
    print("DAWN Talk To - Test Run")
    print("=" * 40)
    print(f"Test state: {test_state}")
    print()
    
    # Generate several thoughts to show variety
    for i in range(5):
        thought = talk_to(test_state)
        print(f"{i+1}. {thought}")
    
    print()
    print("Thought Bank Stats:")
    stats = get_thought_bank_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}") 