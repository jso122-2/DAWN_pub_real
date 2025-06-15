import numpy as np
import json
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime
import pickle

@dataclass
class InteractionRecord:
    timestamp: float
    user_input: str
    user_embedding: np.ndarray
    selected_response: str
    response_id: str
    consciousness_state: Dict
    resonance_score: float = 0.0
    user_pause_duration: float = 0.0
    follow_up_occurred: bool = False
    sentiment_shift: str = "neutral"

class ResonanceTracker:
    def __init__(self, memory_decay_rate: float = 0.95):
        self.interactions: List[InteractionRecord] = []
        self.response_resonance_scores: Dict[str, float] = {}
        self.concept_resonance: Dict[str, float] = {}
        self.active_glyphs: Set[str] = set()  # High-resonance responses
        self.memory_decay_rate = memory_decay_rate
        
        # Echo accretion - fragments that get absorbed
        self.user_echo_fragments: List[Dict] = []
        self.crystallized_echoes: List[str] = []
        
    def record_interaction(self, 
                         user_input: str,
                         user_embedding: np.ndarray,
                         selected_response: str,
                         response_id: str,
                         consciousness_state: Dict):
        """Record a new interaction"""
        interaction = InteractionRecord(
            timestamp=datetime.now().timestamp(),
            user_input=user_input,
            user_embedding=user_embedding,
            selected_response=selected_response,
            response_id=response_id,
            consciousness_state=consciousness_state.copy()
        )
        
        self.interactions.append(interaction)
        return interaction
    
    def update_resonance(self, 
                        interaction_id: int,
                        pause_duration: float = 0.0,
                        follow_up: bool = False,
                        sentiment_shift: str = "neutral"):
        """Update interaction with resonance indicators"""
        if interaction_id >= len(self.interactions):
            return
            
        interaction = self.interactions[interaction_id]
        
        # Calculate resonance score
        resonance = self._calculate_resonance_score(
            pause_duration, follow_up, sentiment_shift
        )
        
        interaction.resonance_score = resonance
        interaction.user_pause_duration = pause_duration
        interaction.follow_up_occurred = follow_up
        interaction.sentiment_shift = sentiment_shift
        
        # Update global scores
        self._update_response_scores(interaction)
        self._update_concept_resonance(interaction)
        
        # Handle echo accretion
        if resonance > 0.7:
            self._process_echo_accretion(interaction)
    
    def _calculate_resonance_score(self, 
                                 pause_duration: float,
                                 follow_up: bool,
                                 sentiment_shift: str) -> float:
        """Calculate how much this interaction resonated"""
        score = 0.0
        
        # Pause duration indicates contemplation
        if pause_duration > 3.0:  # 3+ seconds pause
            score += 0.3
        elif pause_duration > 1.0:
            score += 0.1
            
        # Follow-up questions indicate engagement
        if follow_up:
            score += 0.4
            
        # Sentiment shift indicates emotional impact
        sentiment_weights = {
            "positive": 0.3,
            "negative": 0.1,  # Still engagement
            "curious": 0.4,
            "confused": -0.2,
            "neutral": 0.0
        }
        score += sentiment_weights.get(sentiment_shift, 0.0)
        
        return min(1.0, max(0.0, score))
    
    def _update_response_scores(self, interaction: InteractionRecord):
        """Update global response effectiveness scores"""
        response_id = interaction.response_id
        
        if response_id not in self.response_resonance_scores:
            self.response_resonance_scores[response_id] = 0.0
            
        # Weighted update with decay
        current_score = self.response_resonance_scores[response_id]
        new_score = (current_score * self.memory_decay_rate + 
                    interaction.resonance_score * (1 - self.memory_decay_rate))
        
        self.response_resonance_scores[response_id] = new_score
        
        # Promote to active glyph if high resonance
        if new_score > 0.8:
            self.active_glyphs.add(response_id)
        elif new_score < 0.5:
            self.active_glyphs.discard(response_id)
    
    def _update_concept_resonance(self, interaction: InteractionRecord):
        """Track which concepts/modules resonate most"""
        consciousness = interaction.consciousness_state
        modules = consciousness.get('active_modules', [])
        
        for module in modules:
            if module not in self.concept_resonance:
                self.concept_resonance[module] = 0.0
                
            # Update concept resonance
            current = self.concept_resonance[module]
            self.concept_resonance[module] = (
                current * self.memory_decay_rate + 
                interaction.resonance_score * (1 - self.memory_decay_rate)
            )
    
    def _process_echo_accretion(self, interaction: InteractionRecord):
        """Process high-resonance interactions for echo accretion"""
        user_words = interaction.user_input.lower().split()
        
        # Extract interesting fragments (simple heuristic)
        fragments = []
        for i, word in enumerate(user_words):
            if len(word) > 4 and word.isalpha():
                # Create fragment with context
                context_start = max(0, i-2)
                context_end = min(len(user_words), i+3)
                context = " ".join(user_words[context_start:context_end])
                
                fragments.append({
                    'fragment': word,
                    'context': context,
                    'timestamp': interaction.timestamp,
                    'resonance': interaction.resonance_score,
                    'consciousness_state': interaction.consciousness_state
                })
        
        self.user_echo_fragments.extend(fragments)
        
        # Crystallize fragments into responses
        if len(self.user_echo_fragments) > 20:
            self._crystallize_echoes()
    
    def _crystallize_echoes(self):
        """Convert accumulated echo fragments into new response patterns"""
        # Group fragments by similarity (simplified)
        fragment_groups = {}
        
        for frag in self.user_echo_fragments[-20:]:  # Recent fragments
            key = frag['fragment'][:3]  # Simple grouping
            if key not in fragment_groups:
                fragment_groups[key] = []
            fragment_groups[key].append(frag)
        
        # Create new responses from high-frequency fragments
        for group, fragments in fragment_groups.items():
            if len(fragments) >= 3:  # Minimum frequency
                avg_resonance = sum(f['resonance'] for f in fragments) / len(fragments)
                
                if avg_resonance > 0.6:
                    # Create new "dreamed" response
                    most_resonant = max(fragments, key=lambda x: x['resonance'])
                    
                    # Transform fragment into DAWN-style response
                    crystallized = self._transform_fragment_to_dawn_response(
                        most_resonant['fragment'],
                        most_resonant['context']
                    )
                    
                    if crystallized:
                        self.crystallized_echoes.append(crystallized)
    
    def _transform_fragment_to_dawn_response(self, fragment: str, context: str) -> Optional[str]:
        """Transform user fragment into DAWN-style response"""
        # Simple transformation rules (could be enhanced with small LLM)
        transformations = [
            f"I sense {fragment} in the pattern flow.",
            f"{fragment.title()} resonates through the lattice.",
            f"The concept of {fragment} shifts...",
            f"{fragment.title()} echoes in quantum space."
        ]
        
        # Choose transformation based on fragment characteristics
        if len(fragment) > 6:
            return transformations[0]
        elif fragment.endswith('ing'):
            return transformations[1]
        else:
            return transformations[2]
    
    def get_active_glyphs(self) -> List[str]:
        """Get current high-resonance responses"""
        return list(self.active_glyphs)
    
    def get_concept_preferences(self) -> Dict[str, float]:
        """Get current concept resonance scores"""
        return self.concept_resonance.copy()
    
    def get_crystallized_echoes(self) -> List[str]:
        """Get new responses created from user echoes"""
        return self.crystallized_echoes.copy()
    
    def save_state(self, path: str):
        """Save resonance tracking state"""
        state = {
            'response_scores': self.response_resonance_scores,
            'concept_resonance': self.concept_resonance,
            'active_glyphs': list(self.active_glyphs),
            'echo_fragments': self.user_echo_fragments,
            'crystallized_echoes': self.crystallized_echoes,
            'interactions': [asdict(i) for i in self.interactions[-100:]]  # Keep recent
        }
        
        with open(path, 'wb') as f:
            pickle.dump(state, f)
    
    def load_state(self, path: str):
        """Load resonance tracking state"""
        try:
            with open(path, 'rb') as f:
                state = pickle.load(f)
                
            self.response_resonance_scores = state.get('response_scores', {})
            self.concept_resonance = state.get('concept_resonance', {})
            self.active_glyphs = set(state.get('active_glyphs', []))
            self.user_echo_fragments = state.get('echo_fragments', [])
            self.crystallized_echoes = state.get('crystallized_echoes', [])
            
        except FileNotFoundError:
            pass  # Start fresh if no saved state 