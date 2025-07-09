import matplotlib
matplotlib.use('Agg')  # For headless environments
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from collections import deque
from matplotlib.colors import LinearSegmentedColormap
import threading
import time
import signal
import atexit
import sys

# Import GIF saver

    from .gif_saver import setup_gif_saver
    from gif_saver import setup_gif_saver
import signal
import atexit

# Import GIF saver

    from .gif_saver import setup_gif_saver
    from gif_saver import setup_gif_saver

class MoodEntropyPhaseSpace:
    def __init__(self, trail_length=50):
        self.mood_range = (0, 1)
        self.entropy_range = (0, 1)
        self.trail_length = trail_length
        self.mood_history = deque(maxlen=self.trail_length)
        self.entropy_history = deque(maxlen=self.trail_length)
        self.heat_history = deque(maxlen=self.trail_length)
        self.last_coords = (0.5, 0.5, 0.3)
        self.running = False
        self.lock = threading.Lock()
        self.visualization_data = {}
        self._init_colormap()
        self._init_plot()
        self._animation_thread = None
        # Setup GIF saver
        self.gif_saver = setup_gif_saver("mood_entropy_phase_visualizer")
        # Setup signal handlers for GIF saving
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        atexit.register(self.cleanup)

    def _init_colormap(self):
        self.heat_cmap = LinearSegmentedColormap.from_list(
            'dawn_heat',
            [(0, '#00bfff'), (0.33, '#00fff7'), (0.66, '#ffe066'), (1, '#ff3b3b')]
        )

    def _init_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.ax.set_facecolor('#0a0a0f')
        self.ax.set_xlim(self.entropy_range)
        self.ax.set_ylim(self.mood_range)
        self.ax.grid(color='#222228', linestyle='--', linewidth=0.5, alpha=0.7)
        self.add_quadrant_labels()
        self.scatter = None
        self.trail_line = None

    def add_quadrant_labels(self):
        self.ax.text(0.75, 0.85, 'Creative Flow', color='#ffb347', fontsize=16, ha='center', va='center', alpha=0.8)
        self.ax.text(0.25, 0.85, 'Peaceful Clarity', color='#7fffd4', fontsize=16, ha='center', va='center', alpha=0.8)
        self.ax.text(0.75, 0.15, 'Information Overload', color='#ff6666', fontsize=16, ha='center', va='center', alpha=0.8)
        self.ax.text(0.25, 0.15, 'Dormant State', color='#b0b0b0', fontsize=16, ha='center', va='center', alpha=0.8)
        self.ax.set_xlabel('Entropy (Information Flow)', fontsize=14, color='white')
        self.ax.set_ylabel('Mood (Emotional Intensity)', fontsize=14, color='white')
        self.ax.tick_params(colors='gray')
        self.ax.set_title('DAWN | Mood-Entropy Phase Space', fontsize=18, color='white', pad=20)

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

    def update_visualization(self, mood, entropy, heat=0.3):
        with self.lock:
            self.mood_history.append(mood)
            self.entropy_history.append(entropy)
            self.heat_history.append(heat)
            self.last_coords = (mood, entropy, heat)
            self._update_visualization_data()

    def _update_visualization_data(self):
        # Prepare data for API/JSON
        trail = [
            {
                'mood': float(m),
                'entropy': float(e),
                'heat': float(h),
                'color': self._heat_to_color(h),
                'size': 30 + 70 * (i / max(1, len(self.mood_history)-1))
            }
            for i, (m, e, h) in enumerate(zip(self.mood_history, self.entropy_history, self.heat_history))
        ]
        current = {
            'mood': float(self.last_coords[0]),
            'entropy': float(self.last_coords[1]),
            'heat': float(self.last_coords[2]),
            'color': self._heat_to_color(self.last_coords[2]),
            'quadrant': self.analyze_current_quadrant(self.last_coords[0], self.last_coords[1])
        }
        self.visualization_data = {
            'trail': trail,
            'current': current,
            'timestamp': time.time()
        }

    def _heat_to_color(self, heat):
        rgba = self.heat_cmap(heat)
        return '#%02x%02x%02x' % tuple(int(255*x) for x in rgba[:3])

    def get_visualization_data(self):
        with self.lock:
            return dict(self.visualization_data)

    def analyze_current_quadrant(self, mood, entropy):
        if mood > 0.5 and entropy > 0.5:
            return "Creative Flow"
        elif mood > 0.5 and entropy <= 0.5:
            return "Peaceful Clarity"
        elif mood <= 0.5 and entropy > 0.5:
            return "Information Overload"
        else:
            return "Dormant State"

    def _background_update_loop(self):
        # No simulation - this will be called from external updates
        while self.running:
            time.sleep(1)  # Just keep the thread alive

    def simulate_dawn_data(self):
        # Remove simulation - this should not be called
        pass

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

# Factory function for backend integration
def get_mood_entropy_phase_visualizer():
    return MoodEntropyPhaseSpace(trail_length=50)