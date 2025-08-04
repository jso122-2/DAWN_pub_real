#!/usr/bin/env python3
"""
DAWN Backend Bloom Genealogy Network Visualizer
Backend-compatible version for analytics and API integration.
"""

import numpy as np
from datetime import datetime
from typing import Dict, Any, List
import logging
from collections import deque
import signal
import atexit
import sys

# Import GIF saver

    from ...gif_saver import setup_gif_saver
    from gif_saver import setup_gif_saver
import signal
import atexit

# Import GIF saver

    from ...gif_saver import setup_gif_saver
    from gif_saver import setup_gif_saver

logger = logging.getLogger(__name__)

# Bloom type definitions (copied from visualizer)
BLOOM_TYPES = {
    'sensory': {'color': (79, 195, 247), 'generation_rate': 0.8},
    'conceptual': {'color': (129, 199, 132), 'generation_rate': 0.6},
    'emotional': {'color': (255, 138, 101), 'generation_rate': 0.7},
    'procedural': {'color': (186, 104, 200), 'generation_rate': 0.5},
    'meta': {'color': (255, 183, 77), 'generation_rate': 0.4},
    'creative': {'color': (240, 98, 146), 'generation_rate': 0.3},
}

class BloomGenealogyNetworkBackend:
    """Backend analytics for the Bloom Genealogy Network visualizer"""
    def __init__(self, max_blooms=200, max_processes=12):
        self.max_blooms = max_blooms
        self.max_processes = max_processes
        self.blooms = []  # List of bloom dicts
        self.family_lines = {}
        self.generation_layers = {}
        self.current_tick = 0
        self.analytics_history = deque(maxlen=100)
        self._active = True
        self._init_demo_state()
        
        # Setup GIF saver
        self.gif_saver = setup_gif_saver("bloomgenealogynetworkbackend")
        
        # Setup signal handlers for GIF saving
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        atexit.register(self.cleanup)
        
        logger.info("BloomGenealogyNetworkBackend initialized")

    def save_animation_gif(self):
        """Save the animation as GIF"""

            if hasattr(self, 'animation') and self.animation is not None:
                gif_path = self.gif_saver.save_animation_as_gif(self.animation, fps=5, dpi=100)
                if gif_path:
                    print(f"\nAnimation GIF saved: {gif_path}", file=sys.stderr)
                else:
                    print("\nFailed to save animation GIF", file=sys.stderr)
            else:
                print("\nNo animation to save", file=sys.stderr)
            print(f"\nError saving animation GIF: {e}", file=sys.stderr)

    def cleanup(self):
        """Cleanup function to save GIF"""
        self.save_animation_gif()

    def signal_handler(self, signum, frame):
        """Signal handler to save GIF on termination"""
        print(f"\nReceived signal {signum}, saving GIF...", file=sys.stderr)
        self.save_animation_gif()
        sys.exit(0)

    def _init_demo_state(self):
        # Start with a few demo blooms
        self.blooms = []
        self.family_lines = {}
        self.generation_layers = {}
        for i in range(6):
            self._add_bloom(bloom_type=list(BLOOM_TYPES.keys())[i], generation=0)

    def _add_bloom(self, bloom_type, generation=0, parent_ids=None):
        bloom_id = len(self.blooms)
        bloom = {
            'id': bloom_id,
            'bloom_type': bloom_type,
            'generation': generation,
            'parents': parent_ids or [],
            'children': [],
            'family_line': bloom_id if generation == 0 else None,
            'activation_level': np.random.uniform(0.3, 1.0),
            'age': 0,
        }
        self.blooms.append(bloom)
        if generation not in self.generation_layers:
            self.generation_layers[generation] = []
        self.generation_layers[generation].append(bloom_id)
        if bloom['family_line'] is not None:
            self.family_lines[bloom['family_line']] = [bloom_id]
        return bloom_id

    def simulate_tick(self):
        # Simulate bloom creation and activation
        self.current_tick += 1
        if len(self.blooms) < self.max_blooms:
            # Randomly create new blooms
            if np.random.rand() < 0.3:
                parent = np.random.choice(self.blooms) if self.blooms else None
                bloom_type = np.random.choice(list(BLOOM_TYPES.keys()))
                parent_ids = [parent['id']] if parent else []
                gen = parent['generation'] + 1 if parent else 0
                new_id = self._add_bloom(bloom_type, generation=gen, parent_ids=parent_ids)
                if parent:
                    parent['children'].append(new_id)
        # Age and activate blooms
        for bloom in self.blooms:
            bloom['age'] += 1
            if np.random.rand() < 0.1:
                bloom['activation_level'] = min(1.0, bloom['activation_level'] + np.random.uniform(0.1, 0.3))
            else:
                bloom['activation_level'] *= 0.98
        # Prune old blooms
        if len(self.blooms) > self.max_blooms:
            self.blooms = self.blooms[-self.max_blooms:]
        # Update analytics
        self.analytics_history.append(self.get_analytics())

    def get_analytics(self) -> Dict[str, Any]:
        if not self.blooms:
            return {
                'total_blooms': 0,
                'family_lines': 0,
                'average_generation': 0,
                'max_generation': 0,
                'orphaned_blooms': 0,
                'active_families': 0
            }
        generations = [b['generation'] for b in self.blooms]
        orphans = sum(1 for b in self.blooms if not b['parents'])
        active_families = len(set(b['family_line'] for b in self.blooms if b['activation_level'] > 0.1 and b['family_line'] is not None))
        return {
            'total_blooms': len(self.blooms),
            'family_lines': len(self.family_lines),
            'average_generation': float(np.mean(generations)),
            'max_generation': int(np.max(generations)),
            'orphaned_blooms': orphans,
            'active_families': active_families
        }

    def get_visualization_data(self) -> Dict[str, Any]:
        return {
            'tick': self.current_tick,
            'analytics': self.get_analytics(),
            'blooms': [
                {
                    'id': b['id'],
                    'bloom_type': b['bloom_type'],
                    'generation': b['generation'],
                    'parents': b['parents'],
                    'children': b['children'],
                    'family_line': b['family_line'],
                    'activation_level': b['activation_level'],
                    'age': b['age']
                } for b in self.blooms[-50:]  # Only last 50 for brevity
            ],
            'timestamp': datetime.now().isoformat()
        }

    def is_active(self):
        return self._active

    def start_animation(self):
        self._active = True
        logger.info("BloomGenealogyNetworkBackend animation started")

    def stop_animation(self):
        self._active = False
        logger.info("BloomGenealogyNetworkBackend animation stopped")

    async def tick(self, *args, **kwargs):
        self.simulate_tick()

    def update_all_processes(self, all_process_data=None, tick=None):
        self.simulate_tick()

    def close(self):
        self._active = False
        logger.info("BloomGenealogyNetworkBackend closed")

    async def shutdown(self):
        self.close()

# Singleton accessor
_bloom_genealogy_network = None

def get_bloom_genealogy_network():
    global _bloom_genealogy_network
    if _bloom_genealogy_network is None:
        _bloom_genealogy_network = BloomGenealogyNetworkBackend()
    return _bloom_genealogy_network