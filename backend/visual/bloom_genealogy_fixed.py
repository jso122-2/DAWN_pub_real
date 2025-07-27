#!/usr/bin/env python3
"""
DAWN Visualization #9: Bloom Genealogy Network - Fixed
A dynamic network showing DAWN's memory system as connected bloom nodes
with genealogical relationships. Pure matplotlib implementation.
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
import math

class BloomGenealogyNetwork:
    """Bloom Genealogy Network Visualization"""
    
    def __init__(self, data_source='stdin', save_frames=False, output_dir="./visual_output"):
        self.save_frames = save_frames
        self.output_dir = output_dir
        self.frame_count = 0
        
        # Create output directory if saving
        if self.save_frames:
            os.makedirs(self.output_dir, exist_ok=True)
        
        self.data_source = data_source
        
        # Bloom types and colors
        self.bloom_types = {
            'sensory': {'color': '#4fc3f7', 'size': 50},
            'conceptual': {'color': '#81c784', 'size': 70},
            'emotional': {'color': '#ff8a65', 'size': 60},
            'procedural': {'color': '#ba68c8', 'size': 55},
            'meta': {'color': '#ffd54f', 'size': 80},
            'creative': {'color': '#f06292', 'size': 75}
        }
        
        # Active blooms
        self.blooms = []
        self.connections = []
        self.bloom_id_counter = 0
        
        # Setup visualization
        self.setup_visualization()
        
    def setup_visualization(self):
        """Initialize matplotlib figure and components"""
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(1, 1, figsize=(16, 10), facecolor='#0a0a0a')
        
        # Configure axes
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-8, 8)
        self.ax.set_facecolor('#0a0a0a')
        self.ax.set_aspect('equal')
        
        # Styling
        self.ax.set_title('DAWN Bloom Genealogy Network', color='white', 
                         fontsize=16, fontweight='bold', pad=20)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Remove spines
        for spine in self.ax.spines.values():
            spine.set_visible(False)
            
        # Add grid
        self.ax.grid(True, alpha=0.1, color='gray')
    
    def parse_bloom_data(self, json_data):
        """Extract bloom triggers from DAWN JSON output"""
        new_blooms = []
        
        # Extract data
        thermal = json_data.get('thermal', {})
        heat = thermal.get('heat', 0.0)
        entropy = json_data.get('entropy', 0.5)
        scup = json_data.get('scup', {})
        mood = json_data.get('mood', {})
        
        # Generate blooms based on cognitive state
        if heat > 0.7:
            new_blooms.append({
                'type': 'sensory',
                'strength': heat,
                'trigger': 'high_heat'
            })
        
        coherence = scup.get('coherence', 0.5)
        if coherence > 0.6:
            new_blooms.append({
                'type': 'conceptual', 
                'strength': coherence,
                'trigger': 'coherent_thought'
            })
        
        base_level = mood.get('base_level', 0.5)
        if abs(base_level - 0.5) > 0.3:
            new_blooms.append({
                'type': 'emotional',
                'strength': abs(base_level - 0.5) * 2,
                'trigger': 'emotional_shift'
            })
        
        schema = scup.get('schema', 0.5)
        if schema > 0.7:
            new_blooms.append({
                'type': 'procedural',
                'strength': schema,
                'trigger': 'schema_activation'
            })
        
        if entropy > 0.8:
            new_blooms.append({
                'type': 'creative',
                'strength': entropy,
                'trigger': 'high_entropy'
            })
        
        # Meta bloom occasionally
        if self.frame_count % 30 == 0 and coherence > 0.5:
            new_blooms.append({
                'type': 'meta',
                'strength': coherence,
                'trigger': 'meta_cognition'
            })
        
        return new_blooms
    
    def create_bloom(self, bloom_type, strength, trigger):
        """Create a new bloom in the network"""
        bloom = {
            'id': self.bloom_id_counter,
            'type': bloom_type,
            'strength': strength,
            'trigger': trigger,
            'x': random.uniform(-8, 8),
            'y': random.uniform(-6, 6),
            'vx': random.uniform(-0.1, 0.1),
            'vy': random.uniform(-0.1, 0.1),
            'age': 0,
            'activation': 1.0,
            'parents': [],
            'children': []
        }
        
        # Find potential parents
        parents = self.find_parents(bloom)
        bloom['parents'] = parents
        
        # Update parent-child relationships
        for parent_id in parents:
            parent_bloom = next((b for b in self.blooms if b['id'] == parent_id), None)
            if parent_bloom:
                parent_bloom['children'].append(bloom['id'])
        
        self.blooms.append(bloom)
        self.bloom_id_counter += 1
        
        # Create connections to parents
        for parent_id in parents:
            self.connections.append({
                'from': parent_id,
                'to': bloom['id'],
                'strength': 0.5
            })
        
        return bloom
    
    def find_parents(self, new_bloom):
        """Find potential parent blooms"""
        if len(self.blooms) < 2:
            return []
        
        # Find compatible blooms
        candidates = []
        for bloom in self.blooms[-10:]:  # Only consider recent blooms
            if bloom['activation'] > 0.3 and bloom['age'] < 100:
                distance = math.sqrt(
                    (bloom['x'] - new_bloom['x'])**2 + 
                    (bloom['y'] - new_bloom['y'])**2
                )
                if distance < 5.0:  # Close enough to be related
                    candidates.append(bloom['id'])
        
        # Return up to 2 parents
        return random.sample(candidates, min(2, len(candidates)))
    
    def update_blooms(self):
        """Update bloom positions and states"""
        # Update physics
        for bloom in self.blooms:
            # Age the bloom
            bloom['age'] += 1
            bloom['activation'] *= 0.995  # Slow decay
            
            # Simple physics
            bloom['x'] += bloom['vx']
            bloom['y'] += bloom['vy']
            
            # Boundary conditions
            if abs(bloom['x']) > 9:
                bloom['vx'] *= -0.5
            if abs(bloom['y']) > 7:
                bloom['vy'] *= -0.5
            
            # Add small random motion
            bloom['vx'] += random.uniform(-0.01, 0.01)
            bloom['vy'] += random.uniform(-0.01, 0.01)
            
            # Damping
            bloom['vx'] *= 0.98
            bloom['vy'] *= 0.98
        
        # Remove old, inactive blooms
        self.blooms = [b for b in self.blooms if b['age'] < 500 or b['activation'] > 0.1]
        
        # Remove orphaned connections
        bloom_ids = {b['id'] for b in self.blooms}
        self.connections = [c for c in self.connections 
                          if c['from'] in bloom_ids and c['to'] in bloom_ids]
    
    def draw_network(self):
        """Draw the bloom network"""
        self.ax.clear()
        
        # Redraw setup
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-8, 8)
        self.ax.set_facecolor('#0a0a0a')
        self.ax.set_aspect('equal')
        self.ax.set_title('DAWN Bloom Genealogy Network', color='white', 
                         fontsize=16, fontweight='bold', pad=20)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        self.ax.grid(True, alpha=0.1, color='gray')
        
        # Draw connections
        for conn in self.connections:
            from_bloom = next((b for b in self.blooms if b['id'] == conn['from']), None)
            to_bloom = next((b for b in self.blooms if b['id'] == conn['to']), None)
            
            if from_bloom and to_bloom:
                alpha = min(from_bloom['activation'], to_bloom['activation']) * 0.5
                self.ax.plot([from_bloom['x'], to_bloom['x']], 
                           [from_bloom['y'], to_bloom['y']], 
                           'white', alpha=alpha, linewidth=1)
        
        # Draw blooms
        for bloom in self.blooms:
            bloom_info = self.bloom_types[bloom['type']]
            color = bloom_info['color']
            base_size = bloom_info['size']
            
            # Size based on strength and activation
            size = base_size * bloom['strength'] * (0.5 + bloom['activation'] * 0.5)
            alpha = 0.3 + bloom['activation'] * 0.7
            
            # Draw bloom
            circle = Circle((bloom['x'], bloom['y']), 
                          radius=size/500, 
                          color=color, alpha=alpha,
                          zorder=10)
            self.ax.add_patch(circle)
            
            # Add generation indicator for children
            if bloom['children']:
                self.ax.scatter(bloom['x'], bloom['y'], 
                              s=10, c='white', alpha=0.8, zorder=15)
        
        # Add type legend
        legend_x = -9.5
        legend_y = 7
        for i, (bloom_type, info) in enumerate(self.bloom_types.items()):
            y_pos = legend_y - i * 0.8
            self.ax.scatter(legend_x, y_pos, s=50, c=info['color'], alpha=0.8)
            self.ax.text(legend_x + 0.5, y_pos, bloom_type.title(), 
                        color='white', fontsize=10, va='center')
        
        # Add statistics
        stats_text = f"Blooms: {len(self.blooms)} | Connections: {len(self.connections)}"
        self.ax.text(0, -7.5, stats_text, color='white', fontsize=12, 
                    ha='center', bbox=dict(boxstyle="round,pad=0.3", 
                                         facecolor='black', alpha=0.7))
    
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
            
            # Parse and create new blooms
            new_blooms = self.parse_bloom_data(data)
            for bloom_data in new_blooms:
                if random.random() < 0.3:  # Random chance to create
                    self.create_bloom(bloom_data['type'], 
                                    bloom_data['strength'], 
                                    bloom_data['trigger'])
            
            # Update existing blooms
            self.update_blooms()
            
            # Redraw network
            self.draw_network()
            
            # Save frame if requested
            if self.save_frames and self.frame_count % 10 == 0:
                filename = f"{self.output_dir}/bloom_genealogy_frame_{self.frame_count:06d}.png"
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
            print(f"Bloom Genealogy Network saved {frame_count} frames to: {self.output_dir}")
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
    parser = argparse.ArgumentParser(description='DAWN Bloom Genealogy Network - Fixed')
    parser.add_argument('--source', choices=['stdin', 'demo'], default='stdin',
                       help='Data source (default: stdin)')
    parser.add_argument('--save', action='store_true',
                       help='Save visualization frames as PNG files')
    parser.add_argument('--output-dir', default='./visual_output/bloom_genealogy',
                       help='Directory to save output frames')
    
    args = parser.parse_args()
    
    viz = BloomGenealogyNetwork(
        data_source=args.source,
        save_frames=args.save,
        output_dir=args.output_dir
    )
    
    viz.run()

if __name__ == '__main__':
    main() 