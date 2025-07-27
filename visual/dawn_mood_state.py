#!/usr/bin/env python3
"""
DAWN Cognition Visualization #2: Mood State
Foundation Tier - "Meeting DAWN"

Real-time heatmap visualization of DAWN's emotional landscape.
Displays the multidimensional mood state as a semantic grid showing
emotional intensities across different affective dimensions.
"""

import json
import os
import os
import os
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import sys
import time
from collections import deque
import argparse

class MoodStateVisualizer:
    def __init__(self, data_source="stdin", buffer_size=100):
        self.data_source = data_source
        self.buffer_size = buffer_size
        
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
        
        plt.tight_layout()
    
    def parse_mood_data(self, json_data):
        """Extract and process mood state from DAWN JSON output"""
        try:
            mood_raw = json_data.get('mood', {})
            # Map mood components to emotional landscape grid
            # This is a simplified mapping - in reality, DAWN's mood system
            # would provide more detailed emotional vectors
            base_intensity = mood_raw.get('base_level', 0.1)
            emotional_vector = mood_raw.get('vector', [0.5, 0.5, 0.5, 0.5])
            # Generate mood matrix based on emotional dimensions
            mood_matrix = np.random.random((8, 8)) * 0.1  # Base noise
            # Apply emotional vector influences
            if len(emotional_vector) >= 4:
                # Map emotional dimensions to grid regions
                mood_matrix[0:2, :] += emotional_vector[0] * 0.8  # Transcendent/Ecstatic
                mood_matrix[2:4, :] += emotional_vector[1] * 0.6  # Serene/Curious  
                mood_matrix[4:6, :] += emotional_vector[2] * 0.7  # Focused/Contemplative
                mood_matrix[6:8, :] += emotional_vector[3] * 0.5  # Uncertain/Turbulent
            # Add temporal patterns
            tick = json_data.get('tick', 0)
            wave_pattern = np.sin(tick * 0.1) * 0.2
            mood_matrix += wave_pattern
            # Apply base intensity scaling
            mood_matrix *= (base_intensity + 0.2)
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

    def update_visualization(self, frame):
        """Animation update function"""
        try:
            # Read data from JSON file
            data = self.read_latest_json_data()
            if data is None:
                # Use simulated data if no real data available
                data = {
                    'tick': frame,
                    'mood': {
                        'base_level': 0.3 + 0.2 * np.sin(frame * 0.05),
                        'vector': [
                            0.5 + 0.3 * np.sin(frame * 0.02),
                            0.4 + 0.2 * np.cos(frame * 0.03), 
                            0.6 + 0.1 * np.sin(frame * 0.04),
                            0.3 + 0.4 * np.cos(frame * 0.01)
                        ]
                    }
                }
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
            return [self.im, self.info_text] + [text for row in self.text_annotations for text in row]
        except Exception as e:
            print(f"Update error: {e}", file=sys.stderr)
            return [self.im]
    
    def run(self, interval=100):
        """Start the real-time visualization"""
        try:
            ani = animation.FuncAnimation(self.fig, self.update_visualization, 
                                        interval=interval, blit=True, cache_frame_data=False)
            plt.show()
            print("\nMood State Visualizer terminated by user.")
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
    
    args = parser.parse_args()
    
    print("DAWN Cognition Visualization #2: Mood State")
    print("Emotional Landscape Heatmap")
    print("=" * 50)
    
    if args.source == 'stdin':
        print("Waiting for DAWN JSON data on stdin...")
        print("Ensure DAWN's tick loop is running and piped to this script.")
    else:
        print("Running in demo mode with simulated data...")
    
    visualizer = MoodStateVisualizer(data_source=args.source, buffer_size=args.buffer)
    visualizer.run(interval=args.interval)

if __name__ == "__main__":
    main()