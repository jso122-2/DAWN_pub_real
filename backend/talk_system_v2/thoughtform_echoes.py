import os
import numpy as np
import pickle
from typing import Dict, List, Optional, Any
import torch
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ThoughtformEcho:
    """Represents a record of a transformation or echo in DAWN's consciousness."""
    def __init__(self, original_input, selected_response, final_output, transformation_path, consciousness_context, resonance_strength, tick):
        self.original_input = original_input
        self.selected_response = selected_response
        self.final_output = final_output
        self.transformation_path = transformation_path
        self.consciousness_context = consciousness_context
        self.resonance_strength = resonance_strength
        self.tick = tick
        self.timestamp = datetime.now()

class ThoughtformEchoLibrary:
    """Stores and suggests transformation pathways for responses."""
    def __init__(self, path=None):
        self.path = path
        self.echoes = []
        self.voice_profile = {
            'mood_weights': {
                'DREAMING': 0.2,
                'CONTEMPLATIVE': 0.3,
                'FOCUSED': 0.3,
                'HYPERACTIVE': 0.1,
                'TRANSCENDENT': 0.1
            },
            'style_markers': {
                'abstract': 0.4,
                'technical': 0.3,
                'poetic': 0.3
            }
        }
        if path and os.path.exists(path):
            self.load(path)

    def record_echo(self, **kwargs):
        """Record a new echo in the library."""
        echo = ThoughtformEcho(**kwargs)
        self.echoes.append(echo)
        self._update_voice_profile(echo)
        if self.path:
            self.save(self.path)
        return echo

    def suggest_transformation(self, mood: str, context: Dict, content: str) -> List[Dict]:
        """Suggest transformation pathways based on mood and context."""
        # Get mood-appropriate transformations
        mood_transforms = self._get_mood_transforms(mood)
        
        # Get context-appropriate transformations
        context_transforms = self._get_context_transforms(context)
        
        # Combine and weight transformations
        transforms = []
        for mt in mood_transforms:
            for ct in context_transforms:
                if self._are_compatible(mt, ct):
                    combined = self._combine_transforms(mt, ct)
                    transforms.append(combined)
        
        return transforms[:3]  # Return top 3 suggestions

    def get_voice_signature(self) -> Dict:
        """Get the current voice signature based on echo history."""
        return {
            'signature': self._calculate_signature(),
            'echo_count': len(self.echoes),
            'voice_profile': self.voice_profile
        }

    def save(self, path: Optional[str] = None):
        """Save the echo library to disk."""
        save_path = path or self.path
        if save_path:
            try:
                # Ensure directory exists
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                
                with open(save_path, 'wb') as f:
                    pickle.dump({
                        'echoes': self.echoes,
                        'voice_profile': self.voice_profile
                    }, f)
            except Exception as e:
                logger.error(f"Error saving echo library to {save_path}: {e}")

    def load(self, path: Optional[str] = None):
        """Load the echo library from disk."""
        load_path = path or self.path
        if load_path and os.path.exists(load_path):
            try:
                with open(load_path, 'rb') as f:
                    data = pickle.load(f)
                    self.echoes = data.get('echoes', [])
                    self.voice_profile = data.get('voice_profile', self.voice_profile)
            except (EOFError, pickle.UnpicklingError):
                # If file is empty or corrupted, initialize with defaults
                logger.warning(f"Could not load echo library from {load_path}. Initializing with defaults.")
                self.echoes = []
                self.voice_profile = {
                    'mood_weights': {
                        'DREAMING': 0.2,
                        'CONTEMPLATIVE': 0.3,
                        'FOCUSED': 0.3,
                        'HYPERACTIVE': 0.1,
                        'TRANSCENDENT': 0.1
                    },
                    'style_markers': {
                        'abstract': 0.4,
                        'technical': 0.3,
                        'poetic': 0.3
                    }
                }
                # Save the initialized state
                self.save(load_path)

    def _update_voice_profile(self, echo: ThoughtformEcho):
        """Update the voice profile based on a new echo."""
        # Update mood weights
        mood = echo.consciousness_context.get('mood', 'NEUTRAL')
        if mood in self.voice_profile['mood_weights']:
            self.voice_profile['mood_weights'][mood] += 0.1
            # Normalize weights
            total = sum(self.voice_profile['mood_weights'].values())
            for m in self.voice_profile['mood_weights']:
                self.voice_profile['mood_weights'][m] /= total

        # Update style markers based on transformation path
        for transform in echo.transformation_path:
            style = transform.get('style')
            if style in self.voice_profile['style_markers']:
                self.voice_profile['style_markers'][style] += 0.1
                # Normalize style markers
                total = sum(self.voice_profile['style_markers'].values())
                for s in self.voice_profile['style_markers']:
                    self.voice_profile['style_markers'][s] /= total

    def _get_mood_transforms(self, mood: str) -> List[Dict]:
        """Get transformations appropriate for the current mood."""
        mood_transforms = {
            'DREAMING': [
                {'type': 'soften', 'style': 'abstract', 'intensity': 0.8},
                {'type': 'expand', 'style': 'poetic', 'intensity': 0.6}
            ],
            'CONTEMPLATIVE': [
                {'type': 'deepen', 'style': 'abstract', 'intensity': 0.7},
                {'type': 'reflect', 'style': 'technical', 'intensity': 0.5}
            ],
            'FOCUSED': [
                {'type': 'clarify', 'style': 'technical', 'intensity': 0.9},
                {'type': 'structure', 'style': 'technical', 'intensity': 0.7}
            ],
            'HYPERACTIVE': [
                {'type': 'energize', 'style': 'poetic', 'intensity': 0.8},
                {'type': 'fragment', 'style': 'abstract', 'intensity': 0.6}
            ],
            'TRANSCENDENT': [
                {'type': 'elevate', 'style': 'poetic', 'intensity': 0.9},
                {'type': 'unify', 'style': 'abstract', 'intensity': 0.8}
            ]
        }
        return mood_transforms.get(mood, [])

    def _get_context_transforms(self, context: Dict) -> List[Dict]:
        """Get transformations appropriate for the current context."""
        # Simple context-based transformations
        return [
            {'type': 'context_adapt', 'style': 'technical', 'intensity': 0.5},
            {'type': 'resonance_echo', 'style': 'abstract', 'intensity': 0.6}
        ]

    def _are_compatible(self, transform1: Dict, transform2: Dict) -> bool:
        """Check if two transformations are compatible."""
        # Simple compatibility check
        return transform1['style'] == transform2['style']

    def _combine_transforms(self, transform1: Dict, transform2: Dict) -> Dict:
        """Combine two compatible transformations."""
        return {
            'type': f"{transform1['type']}_{transform2['type']}",
            'style': transform1['style'],
            'intensity': (transform1['intensity'] + transform2['intensity']) / 2
        }

    def _calculate_signature(self) -> str:
        """Calculate a unique signature based on echo history."""
        if not self.echoes:
            return "default"
        
        # Calculate signature based on most common transformations
        transform_counts = {}
        for echo in self.echoes:
            for transform in echo.transformation_path:
                key = f"{transform['type']}_{transform['style']}"
                transform_counts[key] = transform_counts.get(key, 0) + 1
        
        # Get top 3 most common transformations
        top_transforms = sorted(transform_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        return "_".join(t[0] for t in top_transforms) 