#!/usr/bin/env python3
"""
DAWN SCUP Pressure Grid Visualizer
Real-time visualization of SCUP dimensional pressure interactions
"""

# Configure matplotlib for headless operation  
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json
import os
import sys
import argparse
import time
from datetime import datetime
from collections import deque, defaultdict
import threading
import queue

class SCUPPressureGrid:
    """SCUP Pressure Grid Visualization"""
    
    def __init__(self, data_source='stdin', save_frames=False, output_dir="./visual_output/scup_pressure_grid"):
        self.data_source = data_source
        self.save_frames = save_frames
        self.output_dir = output_dir
        
        # Create output directory if saving
        if self.save_frames:
            os.makedirs(self.output_dir, exist_ok=True)
        
        self.frame_count = 0
        
        # SCUP dimensions
        self.dimensions = ['Schema', 'Coherence', 'Utility', 'Pressure']
        self.pressure_matrix = np.zeros((4, 4))
        self.pressure_history = deque(maxlen=100)
        
        # Data management
        self.data_queue = queue.Queue()
        
        # Setup visualization
        self.setup_visualization()
        
    def setup_visualization(self):
        """Initialize the pressure grid visualization"""
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(1, 1, figsize=(12, 10), facecolor='#0a0a0a')
        
        # Initialize heatmap
        self.im = self.ax.imshow(self.pressure_matrix, cmap='viridis',
                                vmin=0, vmax=1, aspect='equal')
        
        # Add colorbar
        self.cbar = plt.colorbar(self.im)
        self.cbar.set_label('Pressure Intensity', fontsize=12, color='white')
        self.cbar.ax.tick_params(colors='white')
        
        # Configure axes
        self.ax.set_title('DAWN SCUP Pressure Grid', fontsize=16, 
                         fontweight='bold', pad=20, color='white')
        self.ax.set_xticks(range(4))
        self.ax.set_yticks(range(4))
        self.ax.set_xticklabels(self.dimensions, fontsize=12, color='white')
        self.ax.set_yticklabels(self.dimensions, fontsize=12, color='white')
        
        # Add cell annotations
        self.cell_texts = []
        for i in range(4):
            row_texts = []
            for j in range(4):
                text = self.ax.text(j, i, '0.0', ha='center', va='center',
                                   fontsize=10, color='white')
                row_texts.append(text)
            self.cell_texts.append(row_texts)
        
    def calculate_pressure_matrix(self, scup_data):
        """Calculate pressure interaction matrix from SCUP data"""
        scup = scup_data.get('scup', {})
        values = [
            scup.get('schema', 0.5),
            scup.get('coherence', 0.5), 
            scup.get('utility', 0.5),
            scup.get('pressure', 0.5)
        ]
        
        # Calculate pressure matrix
        for i in range(4):
            for j in range(4):
                if i == j:
                    # Self pressure
                    self.pressure_matrix[i, j] = values[i] ** 1.5
                else:
                    # Interaction pressure
                    self.pressure_matrix[i, j] = values[i] * values[j]
        
        # Normalize
        self.pressure_matrix = np.clip(self.pressure_matrix, 0, 1)
        self.pressure_history.append(self.pressure_matrix.copy())
    
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
            
            # Calculate pressure matrix
            self.calculate_pressure_matrix(data)
            
            # Update heatmap
            self.im.set_array(self.pressure_matrix)
            
            # Update cell text annotations
            for i in range(4):
                for j in range(4):
                    value = self.pressure_matrix[i, j]
                    self.cell_texts[i][j].set_text(f'{value:.2f}')
                    # Adjust text color for visibility
                    if value > 0.5:
                        self.cell_texts[i][j].set_color('black')
                    else:
                        self.cell_texts[i][j].set_color('white')
            
            # Save frame if requested
            if self.save_frames and self.frame_count % 10 == 0:
                filename = f"{self.output_dir}/scup_pressure_grid_frame_{self.frame_count:06d}.png"
                self.fig.savefig(filename, dpi=100, bbox_inches='tight',
                               facecolor='#0a0a0a', edgecolor='none')
            
            self.frame_count += 1
            
            return [self.im] + [text for row in self.cell_texts for text in row]
            
        except Exception as e:
            print(f"Update error: {e}", file=sys.stderr)
            return []
    
    def generate_demo_data(self, frame):
        """Generate demonstration data"""
        t = frame * 0.02
        return {
            'scup': {
                'schema': 0.5 + 0.3 * np.sin(t),
                'coherence': 0.5 + 0.3 * np.cos(t * 0.7),
                'utility': 0.5 + 0.25 * np.sin(t * 1.3),
                'pressure': 0.3 + 0.4 * abs(np.sin(t * 0.5))
            }
        }
    
    def run(self):
        """Start the visualization"""
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
                        self.calculate_pressure_matrix(data)
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
            print(f"SCUP Pressure Grid saved {frame_count} frames to: {self.output_dir}")
        else:
            # Interactive mode
            self.animation = animation.FuncAnimation(
                self.fig, self.update_visualization,
                interval=100, blit=False, cache_frame_data=False
            )
            plt.show()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='DAWN SCUP Pressure Grid Visualizer'
    )
    parser.add_argument('--source', choices=['stdin', 'demo'], default='stdin',
                       help='Data source (default: stdin)')
    parser.add_argument('--save', action='store_true',
                       help='Save visualization frames as PNG files')
    parser.add_argument('--output-dir', default='./visual_output/scup_pressure_grid',
                       help='Directory to save output frames')
    
    args = parser.parse_args()
    
    # Create and run visualization
    viz = SCUPPressureGrid(
        data_source=args.source,
        save_frames=args.save,
        output_dir=args.output_dir
    )
    
    viz.run()

if __name__ == '__main__':
    main() 