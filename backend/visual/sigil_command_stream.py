#!/usr/bin/env python3
"""
DAWN Visualization #8: Sigil Command Stream
A real-time timeline visualization showing DAWN's internal symbolic commands 
and triggers (sigils) that orchestrate cognitive processes.
"""

# Configure matplotlib for headless operation
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import json
import os
import sys
import argparse
import time
from collections import deque
import random

class SigilCommandStream:
    """Sigil Command Stream Visualization"""
    
    def __init__(self, data_source='stdin', save_frames=False, output_dir="./visual_output"):
        self.save_frames = save_frames
        self.output_dir = output_dir
        self.frame_count = 0
        
        # Create output directory if saving
        if self.save_frames:
            os.makedirs(self.output_dir, exist_ok=True)
        
        self.data_source = data_source
        
        # Sigil categories
        self.categories = {
            'attention': {'color': '#ff6b6b', 'y': 5},
            'memory': {'color': '#4ecdc4', 'y': 4},
            'reasoning': {'color': '#45b7d1', 'y': 3},
            'creativity': {'color': '#96ceb4', 'y': 2},
            'action': {'color': '#feca57', 'y': 1},
            'meta': {'color': '#54a0ff', 'y': 0}
        }
        
        # Active sigils
        self.active_sigils = []
        self.sigil_history = deque(maxlen=100)
        
        # Setup visualization
        self.setup_visualization()
        
    def setup_visualization(self):
        """Initialize matplotlib figure and components"""
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(1, 1, figsize=(16, 8), facecolor='#0a0a0a')
        
        # Configure axes
        self.ax.set_xlim(0, 20)
        self.ax.set_ylim(-0.5, 5.5)
        self.ax.set_facecolor('#0a0a0a')
        
        # Draw category lanes
        for category, props in self.categories.items():
            y = props['y']
            self.ax.axhline(y, color=props['color'], alpha=0.3, linewidth=2)
            self.ax.text(-1, y, category.title(), color=props['color'], 
                        fontweight='bold', va='center')
        
        # Styling
        self.ax.set_xlabel('Time Flow →', color='white', fontsize=12)
        self.ax.set_title('DAWN Sigil Command Stream', color='white', 
                         fontsize=16, fontweight='bold', pad=20)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Remove spines
        for spine in self.ax.spines.values():
            spine.set_visible(False)
    
    def parse_sigil_data(self, json_data):
        """Extract sigil triggers from DAWN JSON output"""
        sigils = []
        
        # Extract data
        thermal_state = json_data.get('thermal_state', {})
        heat = thermal_state.get('heat_level', 0.0)
        entropy_data = json_data.get('entropy', {})
        entropy = entropy_data.get('total_entropy', 0.5) if isinstance(entropy_data, dict) else 0.5
        scup = json_data.get('scup', {})
        mood = json_data.get('mood', {})
        
        # Generate sigils based on cognitive state
        if heat > 0.6:
            sigils.append('attention')
        
        coherence = scup.get('coherence', 0.5)
        if coherence > 0.5:
            sigils.append('memory')
        
        schema = scup.get('schema', 0.5) 
        if schema > 0.6:
            sigils.append('reasoning')
        
        if entropy > 0.7:
            sigils.append('creativity')
        
        pressure = scup.get('pressure', 0.5)
        if pressure > 0.6:
            sigils.append('action')
        
        # Meta sigil occasionally
        if self.frame_count % 20 == 0:
            sigils.append('meta')
        
        return sigils
    
    def add_sigil(self, category):
        """Add new sigil to the stream"""
        if category not in self.categories:
            return
        
        props = self.categories[category]
        sigil = {
            'category': category,
            'x': 19,  # Start at right edge
            'y': props['y'],
            'color': props['color'],
            'age': 0,
            'size': 100 + random.randint(0, 50)
        }
        
        self.active_sigils.append(sigil)
        self.sigil_history.append(sigil.copy())
    
    def update_sigils(self):
        """Update sigil positions"""
        # Move sigils left
        for sigil in self.active_sigils:
            sigil['x'] -= 0.2
            sigil['age'] += 1
        
        # Remove expired sigils
        self.active_sigils = [s for s in self.active_sigils if s['x'] > -1]
    
    def draw_sigils(self):
        """Draw all active sigils"""
        self.ax.clear()
        
        # Redraw lanes
        for category, props in self.categories.items():
            y = props['y']
            self.ax.axhline(y, color=props['color'], alpha=0.3, linewidth=2)
            self.ax.text(-1, y, category.title(), color=props['color'], 
                        fontweight='bold', va='center')
        
        # Draw sigils
        for sigil in self.active_sigils:
            alpha = max(0.2, 1.0 - sigil['age'] / 100)
            self.ax.scatter(sigil['x'], sigil['y'], 
                           c=sigil['color'], s=sigil['size'], 
                           alpha=alpha, marker='o')
        
        # Styling
        self.ax.set_xlim(0, 20)
        self.ax.set_ylim(-0.5, 5.5)
        self.ax.set_facecolor('#0a0a0a')
        self.ax.set_xlabel('Time Flow →', color='white', fontsize=12)
        self.ax.set_title('DAWN Sigil Command Stream', color='white', 
                         fontsize=16, fontweight='bold', pad=20)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        for spine in self.ax.spines.values():
            spine.set_visible(False)
    
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
            # Get data
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
            
            # Parse and add sigils
            sigils = self.parse_sigil_data(data)
            for sigil_type in sigils:
                self.add_sigil(sigil_type)
            
            # Update existing sigils
            self.update_sigils()
            
            # Redraw
            self.draw_sigils()
            
            # Save frame if requested
            if self.save_frames and self.frame_count % 10 == 0:
                filename = f"{self.output_dir}/sigil_command_stream_frame_{self.frame_count:06d}.png"
                self.fig.savefig(filename, dpi=100, bbox_inches='tight',
                               facecolor='#0a0a0a', edgecolor='none')
            
            self.frame_count += 1
            
            return []
            
        except Exception as e:
            print(f"Update error: {e}", file=sys.stderr)
            return []

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
            print(f"Sigil Command Stream saved {frame_count} frames to: {self.output_dir}")
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
    parser = argparse.ArgumentParser(description='DAWN Sigil Command Stream')
    parser.add_argument('--source', choices=['stdin', 'demo'], default='stdin',
                       help='Data source (default: stdin)')
    parser.add_argument('--save', action='store_true',
                       help='Save visualization frames as PNG files')
    parser.add_argument('--output-dir', default='./visual_output/sigil_command_stream',
                       help='Directory to save output frames')
    
    args = parser.parse_args()
    
    viz = SigilCommandStream(
        data_source=args.source,
        save_frames=args.save,
        output_dir=args.output_dir
    )
    
    viz.run()

if __name__ == '__main__':
    main() 