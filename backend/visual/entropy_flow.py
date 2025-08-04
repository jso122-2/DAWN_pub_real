#!/usr/bin/env python3
"""
DAWN Cognition Visualization #4: Entropy Flow
Foundation Tier - "Meeting DAWN"

Real-time vector field visualization of DAWN's information streams.
Displays entropy flow as animated arrows showing the direction and
intensity of information processing across cognitive space.
"""

# Configure matplotlib for headless operation
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import json
import os
import os
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyArrowPatch
import sys
import time
from collections import deque
import argparse
import math
import signal
import atexit
import threading
import queue

# Import GIF saver
try:
    from ...gif_saver import setup_gif_saver
except ImportError:
    from gif_saver import setup_gif_saver

class EntropyFlowVisualizer:
    def __init__(self, data_source="stdin", buffer_size=30):
        self.data_source = data_source
        self.buffer_size = buffer_size
        
        # Flow field parameters
        self.grid_size = 12
        self.field_bounds = (-6, 6, -6, 6)  # x_min, x_max, y_min, y_max
        
        # Create coordinate grids
        self.x = np.linspace(self.field_bounds[0], self.field_bounds[1], self.grid_size)
        self.y = np.linspace(self.field_bounds[2], self.field_bounds[3], self.grid_size)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        
        # Flow vectors (u, v components)
        self.U = np.zeros_like(self.X)
        self.V = np.zeros_like(self.Y)
        self.magnitude = np.zeros_like(self.X)
        
        # Entropy state tracking
        self.entropy_history = deque(maxlen=buffer_size)
        self.entropy_current = 0.5
        self.flow_phase = 0.0
        self.information_density = np.zeros((self.grid_size, self.grid_size))
        
        # Information stream types
        self.stream_types = {
            'sensory': {'color': '#00aaff', 'weight': 1.0},      # Input streams
            'memory': {'color': '#aa00ff', 'weight': 0.8},       # Memory recall
            'cognitive': {'color': '#00ff88', 'weight': 1.2},    # Active thinking
            'creative': {'color': '#ffaa00', 'weight': 0.9},     # Creative synthesis
            'output': {'color': '#ff4444', 'weight': 1.1}        # Decision/action
        }
        
        # Setup matplotlib
        plt.style.use('dark_background')
        self.fig, (self.ax_main, self.ax_metrics) = plt.subplots(1, 2, figsize=(16, 8))
        self.fig.patch.set_facecolor('#0a0a0a')
        
        # Initialize main flow field
        self.setup_flow_field()
        
        # Initialize metrics panel
        self.setup_metrics_panel()
        
        plt.tight_layout()
        
        # Data queue and background thread for stdin
        self.data_queue = queue.Queue()
        self.stdin_thread = None
        self.stop_event = threading.Event()
        if True:  # Always read from JSON file
            self.stdin_thread = threading.Thread(target=self.read_json_data, daemon=True)
            self.stdin_thread.start()
        
        # Setup GIF saver
        self.gif_saver = setup_gif_saver("entropyflowvisualizer")

        # Register cleanup function
        atexit.register(self.cleanup)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def setup_flow_field(self):
        """Initialize the vector field display"""
        self.ax_main.set_xlim(self.field_bounds[0], self.field_bounds[1])
        self.ax_main.set_ylim(self.field_bounds[2], self.field_bounds[3])
        self.ax_main.set_aspect('equal')
        self.ax_main.set_facecolor('#0a0a0a')
        
        # Create vector field quiver plot
        self.quiver = self.ax_main.quiver(self.X, self.Y, self.U, self.V,
                                         self.magnitude, scale=20, scale_units='xy',
                                         angles='xy', width=0.003, alpha=0.8,
                                         cmap='plasma')
        
        # Add information density contours
        self.contour = self.ax_main.contour(self.X, self.Y, self.information_density,
                                           levels=8, colors='white', alpha=0.2, linewidths=0.5)
        
        # Add cognitive region labels
        regions = [
            (-4, 4, 'Perception\nInput', '#00aaff'),
            (0, 4, 'Active\nCognition', '#00ff88'),
            (4, 4, 'Decision\nOutput', '#ff4444'),
            (-4, 0, 'Memory\nRecall', '#aa00ff'),
            (0, 0, 'Integration\nHub', '#ffffff'),
            (4, 0, 'Creative\nSynthesis', '#ffaa00'),
            (-4, -4, 'Subconscious\nProcessing', '#666666'),
            (0, -4, 'Pattern\nRecognition', '#888888'),
            (4, -4, 'Habit\nAutomation', '#444444')
        ]
        
        for x, y, label, color in regions:
            self.ax_main.text(x, y, label, ha='center', va='center',
                             fontsize=9, color=color, weight='bold',
                             bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
        
        # Title and styling
        self.ax_main.set_title('DAWN Information Entropy Flow\nCognitive Vector Field',
                              fontsize=14, color='white', weight='bold', pad=20)
        
        self.ax_main.set_xlabel('Cognitive Space X', color='#cccccc', fontsize=12)
        self.ax_main.set_ylabel('Cognitive Space Y', color='#cccccc', fontsize=12)
        
        # Add grid
        self.ax_main.grid(True, alpha=0.1, color='#444444')
        
        # Flow magnitude indicator
        self.flow_text = self.ax_main.text(0.02, 0.98, '', transform=self.ax_main.transAxes,
                                          fontsize=10, color='#00ff88', verticalalignment='top',
                                          fontfamily='monospace')
    
    def setup_metrics_panel(self):
        """Initialize the entropy metrics display"""
        self.ax_metrics.set_xlim(0, self.buffer_size)
        self.ax_metrics.set_ylim(0, 1.0)
        self.ax_metrics.set_facecolor('#0a0a0a')
        
        # Entropy timeline
        self.entropy_line, = self.ax_metrics.plot([], [], 'g-', linewidth=2, label='Entropy')
        self.flow_magnitude_line, = self.ax_metrics.plot([], [], 'c-', linewidth=2, label='Flow Magnitude')
        self.coherence_line, = self.ax_metrics.plot([], [], 'y-', linewidth=2, label='Information Coherence')
        
        # Stream type indicators
        self.stream_indicators = {}
        for i, (stream_type, props) in enumerate(self.stream_types.items()):
            y_pos = 0.85 - i * 0.15
            indicator = self.ax_metrics.text(0.02, y_pos, f"{stream_type.title()}: 0.000",
                                           transform=self.ax_metrics.transAxes,
                                           fontsize=10, color=props['color'],
                                           fontfamily='monospace')
            self.stream_indicators[stream_type] = indicator
        
        # Styling
        self.ax_metrics.set_title('Entropy Metrics & Stream Analysis',
                                 color='white', fontsize=14, weight='bold')
        self.ax_metrics.set_xlabel('Time Steps', color='#cccccc', fontsize=12)
        self.ax_metrics.set_ylabel('Flow Intensity', color='#cccccc', fontsize=12)
        
        self.ax_metrics.tick_params(colors='#cccccc')
        self.ax_metrics.grid(True, alpha=0.2, color='#444444')
        self.ax_metrics.legend(loc='upper right', facecolor='#1a1a1a',
                              edgecolor='#444444', labelcolor='#cccccc')
    
    def parse_entropy_data(self, json_data):
        """Extract and process entropy flow from DAWN JSON output"""
        try:
            # Main entropy value
            entropy_raw = json_data.get('entropy', 0.5)
            entropy_val = float(entropy_raw) if isinstance(entropy_raw, (int, float)) else 0.5
            
            # Get additional cognitive metrics
            mood = json_data.get('mood', {})
            scup = json_data.get('scup', {})
            heat = json_data.get('heat', 0.3)
            tick = json_data.get('tick', 0)
            
            # Calculate flow components from cognitive state
            mood_vector = mood.get('vector', [0.5, 0.5, 0.5, 0.5])
            if not isinstance(mood_vector, list):
                mood_vector = [0.5, 0.5, 0.5, 0.5]
            
            # Generate flow field based on entropy and cognitive state
            flow_data = {
                'entropy': entropy_val,
                'tick': tick,
                'heat': float(heat) if isinstance(heat, (int, float)) else 0.3,
                'mood_influence': np.mean(mood_vector[:4]) if len(mood_vector) >= 4 else 0.5,
                'scup_pressure': np.mean([
                    scup.get('schema', 0.5),
                    scup.get('coherence', 0.5),
                    scup.get('utility', 0.5),
                    scup.get('pressure', 0.5)
                ]) if isinstance(scup, dict) else 0.5
            }
            
            return flow_data
        except Exception as e:
            print(f"Error parsing entropy data: {e}", file=sys.stderr)
            return {'entropy': 0.5, 'tick': 0, 'heat': 0.3, 'mood_influence': 0.5, 'scup_pressure': 0.5}
    
    def calculate_flow_field(self, flow_data):
        """Generate vector field from entropy and cognitive state"""
        entropy = flow_data['entropy']
        tick = flow_data['tick']
        heat = flow_data['heat']
        mood_influence = flow_data['mood_influence']
        scup_pressure = flow_data['scup_pressure']
        
        # Update flow phase for temporal dynamics
        self.flow_phase += 0.1 * entropy
        
        # Create base flow patterns
        # Radial flow from center (information integration)
        center_x, center_y = 0, 0
        radial_u = (self.X - center_x) * entropy * 0.5
        radial_v = (self.Y - center_y) * entropy * 0.5
        
        # Circular flow (cognitive circulation)
        circular_u = -(self.Y - center_y) * mood_influence * 0.3
        circular_v = (self.X - center_x) * mood_influence * 0.3
        
        # Wave patterns (oscillatory thinking)
        wave_u = np.sin(self.X * 0.5 + self.flow_phase) * scup_pressure * 0.4
        wave_v = np.cos(self.Y * 0.5 + self.flow_phase) * scup_pressure * 0.4
        
        # Heat-driven turbulence
        noise_u = np.random.normal(0, heat * 0.2, self.X.shape)
        noise_v = np.random.normal(0, heat * 0.2, self.Y.shape)
        
        # Combine flow components
        self.U = radial_u + circular_u + wave_u + noise_u
        self.V = radial_v + circular_v + wave_v + noise_v
        
        # Calculate flow magnitude
        self.magnitude = np.sqrt(self.U**2 + self.V**2)
        
        # Update information density (areas of high processing)
        density_centers = [
            (0, 0, entropy),           # Central integration
            (-3, 3, mood_influence),   # Perception input
            (3, 3, scup_pressure),     # Decision output
            (0, -3, heat)              # Subconscious processing
        ]
        
        self.information_density.fill(0)
        for cx, cy, intensity in density_centers:
            # Gaussian density peaks
            distances = np.sqrt((self.X - cx)**2 + (self.Y - cy)**2)
            self.information_density += intensity * np.exp(-distances**2 / 4)
        
        # Calculate stream intensities
        stream_intensities = {
            'sensory': mood_influence * (1 + 0.3 * np.sin(tick * 0.02)),
            'memory': entropy * (1 + 0.2 * np.cos(tick * 0.015)),
            'cognitive': heat * (1 + 0.4 * np.sin(tick * 0.03)),
            'creative': scup_pressure * (1 + 0.3 * np.cos(tick * 0.025)),
            'output': np.mean([entropy, heat, mood_influence]) * (1 + 0.2 * np.sin(tick * 0.04))
        }
        
        return stream_intensities
    
    def read_json_data(self):
        """Background thread to read data from JSON file"""
        json_file = "/tmp/dawn_tick_data.json"
        last_position = 0
        
        while not self.stop_event.is_set():
            try:
                if not os.path.exists(json_file):
                    time.sleep(0.1)
                    continue
                
                with open(json_file, 'r') as f:
                    f.seek(last_position)
                    lines = f.readlines()
                    last_position = f.tell()
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            self.data_queue.put(data)
                        except json.JSONDecodeError as e:
                            print(f"Error parsing JSON: {e}", file=sys.stderr)
                            continue
                
                time.sleep(0.1)  # Small delay to avoid excessive CPU usage
                
            except Exception as e:
                print(f"Error reading JSON file: {e}", file=sys.stderr)
                time.sleep(1.0)  # Longer delay on error
    
    def read_latest_json_data(self):
        """Read the latest data from JSON file"""
        json_file = "/tmp/dawn_tick_data.json"
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        if last_line:
                            return json.loads(last_line)
            except Exception as e:
                print(f"Error reading JSON: {e}", file=sys.stderr)
        return None

    def generate_demo_data(self, frame):
        """Generate demo data for testing"""
        t = frame * 0.03
        return {
            'entropy': 0.5 + 0.3 * np.sin(t),
            'heat': 0.4 + 0.3 * np.cos(t * 0.7),
            'tick': frame,
            'mood': {'vector': [0.5 + 0.2 * np.sin(t * 0.5)] * 4},
            'scup': {
                'schema': 0.5 + 0.3 * np.sin(t * 0.3),
                'coherence': 0.5 + 0.25 * np.cos(t * 0.4),
                'utility': 0.5 + 0.2 * np.sin(t * 0.6),
                'pressure': 0.3 + 0.4 * abs(np.sin(t * 0.2))
            }
        }

    def update_visualization(self, frame):
        """Animation update function"""
        try:
            data = None
            if self.data_source == 'stdin':
                if not self.data_queue.empty():
                    data = self.data_queue.get_nowait()
            else:
                data = self.read_latest_json_data()
            
            if data is None:
                data = self.generate_demo_data(frame)
            
            if data is None:
                return [self.entropy_line, self.flow_magnitude_line]
            
            # Parse and process data
            flow_data = self.parse_entropy_data(data)
            stream_intensities = self.calculate_flow_field(flow_data)
            
            # Store entropy history
            self.entropy_current = flow_data['entropy']
            self.entropy_history.append(self.entropy_current)
            
            # Update vector field
            self.quiver.set_UVC(self.U, self.V, self.magnitude)
            
            # Update contours
            if hasattr(self, 'contour') and hasattr(self.contour, 'collections'):
                for coll in self.contour.collections:
                    coll.remove()
            self.contour = self.ax_main.contour(self.X, self.Y, self.information_density,
                                               levels=8, colors='white', alpha=0.2, linewidths=0.5)
            
            # Update flow information display
            tick = flow_data['tick']
            avg_magnitude = np.mean(self.magnitude)
            max_magnitude = np.max(self.magnitude)
            
            flow_info = (f"Tick: {tick:06d}\n"
                        f"Entropy: {self.entropy_current:.3f}\n"
                        f"Avg Flow: {avg_magnitude:.3f}\n"
                        f"Max Flow: {max_magnitude:.3f}")
            self.flow_text.set_text(flow_info)
            
            # Update metrics panel
            if len(self.entropy_history) > 1:
                x_data = list(range(len(self.entropy_history)))
                entropy_data = list(self.entropy_history)
                magnitude_data = [np.mean(self.magnitude)] * len(x_data)
                coherence_data = [1.0 - flow_data['entropy']] * len(x_data)  # Inverse of entropy
                
                self.entropy_line.set_data(x_data, entropy_data)
                self.flow_magnitude_line.set_data(x_data, magnitude_data)
                self.coherence_line.set_data(x_data, coherence_data)
            
            # Update stream indicators
            for stream_type, intensity in stream_intensities.items():
                if stream_type in self.stream_indicators:
                    self.stream_indicators[stream_type].set_text(f"{stream_type.title()}: {intensity:.3f}")
            
            return [self.quiver]
            
        except Exception as e:
            print(f"Error in update_visualization: {e}", file=sys.stderr)
            return [self.entropy_line, self.flow_magnitude_line]
    
    def run(self, interval=200):
        """Start the visualization"""
        try:
            import matplotlib
            if matplotlib.get_backend() == 'Agg':
                self.animation = animation.FuncAnimation(
                    self.fig,
                    self.update_visualization,
                    interval=interval,
                    blit=False,
                    cache_frame_data=False,
                    repeat=False,
                    frames=20
                )
                for i in range(20):
                    self.update_visualization(i)
                print(f"DEBUG: Generated 20 frames, saving GIF...", file=sys.stderr)
                self.save_animation_gif()
                print(f"DEBUG: GIF save completed", file=sys.stderr)
                return
            else:
                self.animation = animation.FuncAnimation(
                    self.fig,
                    self.update_visualization,
                    interval=interval,
                    blit=False,
                    cache_frame_data=False
                )
                plt.show()
        except Exception as e:
            print(f"Runtime error: {e}", file=sys.stderr)
            self.save_animation_gif()

    def cleanup(self):
        """Cleanup function for compatibility."""
        pass

    def signal_handler(self, signum, frame):
        print(f"Received signal {signum}, exiting gracefully.")
        self.cleanup()
        sys.exit(0)

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
        except Exception as e:
            print(f'\nError saving animation GIF: {e}', file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description='DAWN Entropy Flow Visualizer')
    parser.add_argument('--source', choices=['stdin', 'demo'], default='stdin',
                       help='Data source: stdin for live DAWN data, demo for testing')
    parser.add_argument('--interval', type=int, default=100,
                       help='Animation update interval in milliseconds')
    parser.add_argument('--buffer', type=int, default=30,
                       help='Entropy history buffer size')
    
    args = parser.parse_args()
    
    print("DAWN Cognition Visualization #4: Entropy Flow")
    print("Information Vector Field Visualization")
    print("=" * 50)
    
    if args.source == 'stdin':
        print("Waiting for DAWN JSON data on stdin...")
        print("Visualizing information entropy flows and cognitive vector fields...")
    else:
        print("Running in demo mode with simulated entropy data...")
    
    visualizer = EntropyFlowVisualizer(data_source=args.source, buffer_size=args.buffer)
    visualizer.run(interval=args.interval)

if __name__ == "__main__":
    main()