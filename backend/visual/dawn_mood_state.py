#!/usr/bin/env python3
"""
DAWN Cognition Visualization #2: Mood State
Foundation Tier - "Meeting DAWN"

Real-time heatmap visualization of DAWN's emotional landscape.
Displays the multidimensional mood state as a semantic grid showing
emotional intensities across different affective dimensions.
"""

# Configure matplotlib for headless operation
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import json
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import sys
import time
from collections import deque
import argparse
import signal
import atexit
import threading
import queue

# Import GIF saver
try:
    from .gif_saver import setup_gif_saver
except ImportError:
    from gif_saver import setup_gif_saver

class MoodStateVisualizer:
    def __init__(self, data_source="stdin", buffer_size=100, save_frames=False, output_dir="./visual_output/dawn_mood_state"):
        self.data_source = data_source
        self.buffer_size = buffer_size
        self.save_frames = save_frames
        self.output_dir = output_dir
        self.frame_count = 0
        
        # Create output directory if saving
        if self.save_frames:
            os.makedirs(self.output_dir, exist_ok=True)
        
        # Mood state buffer for temporal smoothing
        self.mood_history = deque(maxlen=buffer_size)
        
        # Define emotional landscape dimensions (8x8 grid)
        self.mood_dimensions = [
            ['Transcendent', 'Luminous', 'Expansive', 'Crystalline', 'Ethereal', 'Radiant', 'Sublime', 'Infinite'],
            ['Ecstatic', 'Euphoric', 'Jubilant', 'Vivacious', 'Exuberant', 'Buoyant', 'Elated', 'Rapturous'],
            ['Serene', 'Peaceful', 'Harmonious', 'Balanced', 'Centered', 'Tranquil', 'Calm', 'Composed'],
            ['Curious', 'Inquisitive', 'Wonder', 'Fascinated', 'Intrigued', 'Exploratory', 'Seeking', 'Questioning'],
            ['Focused', 'Attentive', 'Concentrated', 'Sharp', 'Alert', 'Vigilant', 'Acute', 'Precise'],
            ['Contemplative', 'Reflective', 'Meditative', 'Pensive', 'Introspective', 'Thoughtful', 'Deep', 'Brooding'],
            ['Uncertain', 'Hesitant', 'Ambiguous', 'Doubtful', 'Questioning', 'Unsure', 'Wavering', 'Conflicted'],
            ['Turbulent', 'Chaotic', 'Fragmented', 'Unstable', 'Volatile', 'Scattered', 'Dissonant', 'Entropic']
        ]
        
        # Initialize mood state matrix
        self.mood_matrix = np.zeros((8, 8))
        self.mood_smoothed = np.zeros((8, 8))
        
        # Create custom colormap for emotional landscape
        colors = ['#0a0a0a', '#1a1a2e', '#16213e', '#0f3460', '#533483', 
                 '#7209b7', '#a663cc', '#4cc9f0', '#7209b7', '#f72585']
        self.mood_cmap = LinearSegmentedColormap.from_list('mood', colors, N=256)
        
        # Setup matplotlib
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        self.fig.patch.set_facecolor('#0a0a0a')
        
        # Initialize heatmap
        self.im = self.ax.imshow(self.mood_matrix, cmap=self.mood_cmap, 
                                aspect='equal', vmin=0, vmax=1, animated=True)
        
        # Setup axis labels with emotional dimensions
        self.ax.set_xticks(range(8))
        self.ax.set_yticks(range(8))
        self.ax.set_xticklabels([row[0][:8] for row in self.mood_dimensions], 
                               rotation=45, ha='right', fontsize=9, color='#cccccc')
        self.ax.set_yticklabels([f"{i+1}" for i in range(8)], 
                               fontsize=9, color='#cccccc')
        
        # Add detailed labels for each cell
        self.text_annotations = []
        for i in range(8):
            row_annotations = []
            for j in range(8):
                text = self.ax.text(j, i, self.mood_dimensions[i][j][:6], 
                                   ha='center', va='center', fontsize=7, 
                                   color='white', weight='bold')
                row_annotations.append(text)
            self.text_annotations.append(row_annotations)
        
        # Styling
        self.ax.set_title('DAWN Emotional Landscape\nMood State Heatmap', 
                         fontsize=16, color='#ffffff', pad=20, weight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(self.im, ax=self.ax, shrink=0.8)
        cbar.set_label('Affective Intensity', rotation=270, labelpad=20, 
                      color='#cccccc', fontsize=12)
        cbar.ax.tick_params(colors='#cccccc')
        
        # Add info text
        self.info_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes, 
                                     fontsize=10, color='#00ff88', verticalalignment='top',
                                     fontfamily='monospace')
        
        # Setup GIF saver
        self.gif_saver = setup_gif_saver("dawnmoodstate")
        
        # Setup signal handlers for GIF saving
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        atexit.register(self.cleanup)
        
        plt.tight_layout()
    
    def save_animation_gif(self):
        """Save the animation as GIF"""
        try:
            if hasattr(self, 'animation'):
                gif_path = self.gif_saver.save_animation_as_gif(self.animation, fps=5, dpi=100)
                if gif_path:
                    print(f"\nAnimation GIF saved: {gif_path}", file=sys.stderr)
                else:
                    print("\nFailed to save animation GIF", file=sys.stderr)
            else:
                print("\nNo animation to save", file=sys.stderr)
        except Exception as e:
            print(f"\nError saving animation GIF: {e}", file=sys.stderr)

    def cleanup(self):
        """Cleanup function to save GIF"""
        self.save_animation_gif()

    def signal_handler(self, signum, frame):
        """Signal handler to save GIF on termination"""
        print(f"\nReceived signal {signum}, saving GIF...", file=sys.stderr)
        self.save_animation_gif()
        sys.exit(0)
    
    def parse_mood_data(self, json_data):
        """Extract and process mood state from DAWN JSON output"""
        try:
            mood_raw = json_data.get('mood', {})
            thermal = json_data.get('thermal', {})
            heat = thermal.get('heat', 0.0)
            entropy = json_data.get('entropy', 0.5)
            scup = json_data.get('scup', {})
            
            # Extract mood data
            base_intensity = mood_raw.get('base_level', 0.3)
            
            # Generate realistic mood matrix based on actual DAWN data
            mood_matrix = np.zeros((8, 8))
            
            # Map heat to emotional intensity (transcendent/ecstatic regions)
            if heat > 0.5:
                mood_matrix[0:2, :] = heat * 0.8
            
            # Map entropy to curiosity/exploration
            mood_matrix[2:4, :] = entropy * 0.6
            
            # Map SCUP coherence to focus/contemplation
            coherence = scup.get('coherence', 0.5)
            mood_matrix[4:6, :] = coherence * 0.7
            
            # Map SCUP pressure to uncertainty/turbulence
            pressure = scup.get('pressure', 0.5)
            mood_matrix[6:8, :] = pressure * 0.6
            
            # Add cross-dimensional influences
            schema = scup.get('schema', 0.5)
            utility = scup.get('utility', 0.5)
            
            # Create patterns across the grid
            for i in range(8):
                for j in range(8):
                    # Add some variance based on position
                    position_factor = (i + j) / 14.0
                    mood_matrix[i, j] += schema * position_factor * 0.3
                    mood_matrix[i, j] += utility * (1 - position_factor) * 0.3
            
            # Add temporal wave patterns
            tick = json_data.get('tick_count', 0)
            if tick > 0:
                wave_x = np.sin(tick * 0.01) * 0.2
                wave_y = np.cos(tick * 0.007) * 0.2
                for i in range(8):
                    for j in range(8):
                        mood_matrix[i, j] += wave_x * np.sin(i * 0.5) + wave_y * np.cos(j * 0.5)
            
            # Apply base intensity scaling
            mood_matrix = mood_matrix * (base_intensity + 0.3)
            
            # Add some controlled randomness for dynamic feel
            noise = np.random.random((8, 8)) * 0.1
            mood_matrix += noise
            
            # Clamp values
            mood_matrix = np.clip(mood_matrix, 0, 1)
            
            return mood_matrix
            
        except Exception as e:
            print(f"Error parsing mood data: {e}", file=sys.stderr)
            return self.mood_matrix
    
    def smooth_mood_transition(self, new_mood, alpha=0.3):
        """Apply temporal smoothing to mood transitions"""
        self.mood_smoothed = alpha * new_mood + (1 - alpha) * self.mood_smoothed
        return self.mood_smoothed
    
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
        """Generate demonstration data"""
        t = frame * 0.02
        return {
            'thermal': {'heat': 0.5 + 0.3 * np.sin(t)},
            'entropy': 0.5 + 0.3 * np.cos(t * 0.7),
            'tick_count': 20000 + frame,
            'scup': {
                'schema': 0.5 + 0.25 * np.sin(t * 1.3),
                'coherence': 0.5 + 0.25 * np.cos(t * 1.7),
                'utility': 0.5 + 0.2 * np.sin(t * 0.9),
                'pressure': 0.3 + 0.4 * abs(np.sin(t * 0.5))
            },
            'mood': {'base_level': 0.6 + 0.2 * np.sin(t * 0.3)}
        }

    def update_visualization(self, frame):
        """Animation update function"""
        try:
            # Get data from stdin
            if self.data_source == 'stdin':
                try:
                    line = sys.stdin.readline().strip()
                    if line:
                        data = json.loads(line)
                    else:
                        data = self.generate_demo_data(frame)
                except:
                    data = self.generate_demo_data(frame)
            else:
                data = self.generate_demo_data(frame)
            
            # Update mood state
            new_mood = self.parse_mood_data(data)
            self.mood_matrix = self.smooth_mood_transition(new_mood)
            
            # Store in history
            self.mood_history.append(self.mood_matrix.copy())
            
            # Update heatmap
            self.im.set_array(self.mood_matrix)
            
            # Update info display
            tick = data.get('tick', frame)
            mood_info = data.get('mood', {})
            base_level = mood_info.get('base_level', 0)
            
            info_text = f"Tick: {tick:06d}\nBase Affect: {base_level:.3f}\nEmotional Flux: {np.std(self.mood_matrix):.3f}"
            self.info_text.set_text(info_text)
            
            # Update text annotations with intensity-based opacity
            for i in range(8):
                for j in range(8):
                    intensity = self.mood_matrix[i, j]
                    alpha = 0.4 + 0.6 * intensity  # Scale opacity with intensity
                    self.text_annotations[i][j].set_alpha(alpha)
            
            # Save frame if requested
            if self.save_frames and self.frame_count % 10 == 0:
                filename = f"{self.output_dir}/dawn_mood_state_frame_{self.frame_count:06d}.png"
                self.fig.savefig(filename, dpi=100, bbox_inches='tight',
                               facecolor='#0a0a0a', edgecolor='none')
            
            self.frame_count += 1
            
            return [self.im, self.info_text] + [text for row in self.text_annotations for text in row]
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}", file=sys.stderr)
            return [self.im]
        except Exception as e:
            print(f"Update error: {e}", file=sys.stderr)
            return [self.im]
    
    def run(self, interval=200):
        if self.save_frames:
            # Headless mode: process stdin and save frames
            frame_count = 0
            try:
                for line in sys.stdin:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        self.update_visualization(frame_count)
                        frame_count += 1
                        if frame_count % 50 == 0:
                            print(f"Processed frame {frame_count}", file=sys.stderr)
                        if frame_count >= 1000:
                            break
                    except json.JSONDecodeError:
                        continue
            except KeyboardInterrupt:
                pass
            print(f"Dawn Mood State saved {frame_count} frames to: {self.output_dir}")
        else:
            # Interactive mode
            try:
                self.animation = animation.FuncAnimation(
                    self.fig,
                    self.update_visualization,
                    frames=1000,
                    interval=interval,
                    blit=False,
                    cache_frame_data=False
                )
                plt.show()
            except Exception as e:
                print(f"Runtime error: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description='DAWN Mood State Visualizer')
    parser.add_argument('--source', choices=['stdin', 'demo'], default='stdin',
                       help='Data source: stdin for live DAWN data, demo for testing')
    parser.add_argument('--interval', type=int, default=100,
                       help='Animation update interval in milliseconds')
    parser.add_argument('--buffer', type=int, default=100,
                       help='Mood history buffer size')
    parser.add_argument('--save', action='store_true',
                       help='Save visualization frames as PNG files')
    parser.add_argument('--output-dir', default='./visual_output/dawn_mood_state',
                       help='Directory to save output frames')
    
    args = parser.parse_args()
    
    print("DAWN Cognition Visualization #2: Mood State")
    print("Emotional Landscape Heatmap")
    print("=" * 50)
    
    if args.source == 'stdin':
        print("Waiting for DAWN JSON data on stdin...")
        print("Ensure DAWN's tick loop is running and piped to this script.")
    else:
        print("Running in demo mode with simulated data...")
    
    visualizer = MoodStateVisualizer(data_source=args.source, buffer_size=args.buffer,
                                   save_frames=args.save, output_dir=args.output_dir)
    visualizer.run(interval=args.interval)

if __name__ == "__main__":
    main()