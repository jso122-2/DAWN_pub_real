import threading
import time
import numpy as np
import signal
import atexit
import sys

# Import GIF saver
try:
    from .gif_saver import setup_gif_saver
except ImportError:
    try:
        from gif_saver import setup_gif_saver
    except ImportError:
        def setup_gif_saver(name):
            class DummyGifSaver:
                def save_animation_as_gif(self, animation, fps=5, dpi=100):
                    return None
            return DummyGifSaver()

RECURSION_LEVELS = {
    0: {'name': 'Direct Cognition', 'z_position': 0},
    1: {'name': 'Meta-Cognition', 'z_position': 2},
    2: {'name': 'Meta-Meta-Cognition', 'z_position': 4},
    3: {'name': 'Abstract Recursion', 'z_position': 6},
    4: {'name': 'Transcendent Recursion', 'z_position': 8},
}

class RecursiveDepthExplorerVisualizer:
    """Backend-integrated Recursive Depth Explorer Visualization"""
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.lock = threading.Lock()
        self.visualization_data = {}
        self.running = False
        self._animation_thread = None
        self.frame_count = 0

        # Setup GIF saver
        self.gif_saver = setup_gif_saver("recursivedepthexplorervisualizer")

        # Register cleanup function
        atexit.register(self.cleanup)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def start_animation(self):
        if not self.running:
            self.running = True
            self._animation_thread = threading.Thread(target=self._background_update_loop, daemon=True)
            self._animation_thread.start()

    def stop_animation(self):
        self.running = False
        if self._animation_thread:
            self._animation_thread.join(timeout=1)

    def is_active(self):
        return self.running

    def update_visualization(self, mood, entropy, heat, scup_data):
        with self.lock:
            # Analyze recursive depth using real data
            active_levels = self._analyze_recursive_depth(mood, entropy, heat, scup_data)
            recursion_loops = self._detect_recursive_loops(active_levels)
            analysis = self._analyze_recursive_patterns(active_levels, recursion_loops)
            self.visualization_data = {
                'active_levels': active_levels,
                'recursion_loops': recursion_loops,
                'analysis': analysis,
                'frame': self.frame_count,
                'timestamp': time.time()
            }

    def _analyze_recursive_depth(self, mood, entropy, heat, scup):
        # All values should be floats in [0,1]
        mood_val = mood if isinstance(mood, (int, float)) else mood.get('base_level', 0.5)
        entropy_val = float(entropy)
        heat_val = float(heat) / 100.0 if heat > 1 else float(heat)
        scup = scup or {}
        levels = {}
        # Level 0: Direct cognition
        direct_intensity = heat_val * 0.8 + entropy_val * 0.2
        levels[0] = {
            'intensity': direct_intensity,
            'z': RECURSION_LEVELS[0]['z_position'],
        }
        # Level 1: Meta-cognition
        coherence = scup.get('coherence', 0.5)
        utility = scup.get('utility', 0.5)
        meta_trigger = coherence * utility
        if meta_trigger > 0.3:
            levels[1] = {
                'intensity': meta_trigger,
                'z': RECURSION_LEVELS[1]['z_position'],
            }
        # Level 2: Meta-meta
        schema_pressure = scup.get('schema', 0.5)
        if meta_trigger > 0.4 and schema_pressure > 0.5:
            meta_meta_intensity = meta_trigger * schema_pressure
            levels[2] = {
                'intensity': meta_meta_intensity,
                'z': RECURSION_LEVELS[2]['z_position'],
            }
        # Level 3: Abstract recursion
        if len(levels) >= 3 and np.mean(list(scup.values())) > 0.6:
            abstract_intensity = np.std(list(scup.values()))
            levels[3] = {
                'intensity': abstract_intensity,
                'z': RECURSION_LEVELS[3]['z_position'],
            }
        # Level 4: Transcendent
        pressure = scup.get('pressure', 0.5)
        if len(levels) >= 4 and pressure > 0.7 and entropy_val > 0.7:
            transcendent_intensity = pressure * entropy_val * 0.5
            levels[4] = {
                'intensity': transcendent_intensity,
                'z': RECURSION_LEVELS[4]['z_position'],
            }
        return levels

    def _detect_recursive_loops(self, active_levels):
        loops = []
        # Self-recursion
        for level, data in active_levels.items():
            if data['intensity'] > 0.6:
                loops.append({'type': 'self_recursion', 'levels': [level, level], 'strength': data['intensity']})
        # Cross-level
        level_list = list(active_levels.keys())
        for i, l1 in enumerate(level_list):
            for l2 in level_list[i+1:]:
                influence = active_levels[l1]['intensity'] * active_levels[l2]['intensity']
                if influence > 0.3:
                    loops.append({'type': 'cross_recursion', 'levels': [l1, l2], 'strength': influence})
        return loops

    def _analyze_recursive_patterns(self, active_levels, recursion_loops):
        if not active_levels:
            return {}
        active_depths = list(active_levels.keys())
        n_levels = len(active_levels)
        n_loops = len(recursion_loops)
        intensities = [data['intensity'] for data in active_levels.values()]
        analysis = {
            'max_active_depth': max(active_depths),
            'average_depth': float(np.mean(active_depths)),
            'recursive_loops_count': n_loops,
            'complexity': (n_levels / self.max_depth) * 0.5 + (min(n_loops, 10) / 10) * 0.5,
            'meta_load': sum(intensities[1:]) / (n_levels-1) if n_levels > 1 else 0,
            'transcendence_score': intensities[-1] if len(intensities) == 5 else 0
        }
        return analysis

    def get_visualization_data(self):
        with self.lock:
            return dict(self.visualization_data)

    def _background_update_loop(self):
        while self.running:
            self.frame_count += 1
            time.sleep(0.1)

    def save_animation_gif(self):
        """Save the animation as GIF"""
        try:
            if hasattr(self, 'animation'):
                gif_path = self.gif_saver.save_animation_as_gif(self.animation, fps=5, dpi=100)
                if gif_path:
                    print(f'\nAnimation GIF saved: {gif_path}', file=sys.stderr)
                else:
                    print('\nFailed to save animation GIF', file=sys.stderr)
            else:
                print('\nNo animation to save', file=sys.stderr)
            print(f'\nError saving animation GIF: {e}', file=sys.stderr)
    def cleanup(self):
        """Cleanup function to save GIF"""
        self.save_animation_gif()

    def signal_handler(self, signum, frame):
        """Signal handler to save GIF on termination"""
        print(f'\nReceived signal {signum}, saving GIF...', file=sys.stderr)
        self.save_animation_gif()
        sys.exit(0)

def get_recursive_depth_explorer_visualizer():
    return RecursiveDepthExplorerVisualizer(max_depth=5)