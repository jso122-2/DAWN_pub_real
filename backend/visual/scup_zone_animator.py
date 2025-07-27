#!/usr/bin/env python3
"""
DAWN SCUP Zone Animator - Simple Working Version
Real-time SCUP zone visualization
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

class SCUPZoneAnimator:
    """Simple SCUP Zone Animator"""
    
    def __init__(self, data_source='stdin', save_frames=False, output_dir="./visual_output/scup_zone_animator"):
        self.data_source = data_source
        self.save_frames = save_frames
        self.output_dir = output_dir
        self.frame_count = 0
        
        # Create output directory if saving
        if self.save_frames:
            os.makedirs(self.output_dir, exist_ok=True)
        
        # Setup visualization
        self.setup_visualization()
        
    def setup_visualization(self):
        """Initialize the visualization"""
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(1, 1, figsize=(12, 8), facecolor='#0a0a0a')
        
        # SCUP data
        self.scup_data = {'schema': 0.5, 'coherence': 0.5, 'utility': 0.5, 'pressure': 0.5}
        
        # Bar chart
        self.bars = self.ax.bar(['Schema', 'Coherence', 'Utility', 'Pressure'], 
                               [0.5, 0.5, 0.5, 0.5],
                               color=['#2196f3', '#4caf50', '#ff9800', '#f44336'])
        
        self.ax.set_ylim(0, 1)
        self.ax.set_title('DAWN SCUP Zone Animator', fontsize=16, color='white')
        self.ax.set_ylabel('SCUP Values', color='white')
        
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
            
            # Update SCUP values
            scup = data.get('scup', {})
            self.scup_data['schema'] = scup.get('schema', 0.5)
            self.scup_data['coherence'] = scup.get('coherence', 0.5)
            self.scup_data['utility'] = scup.get('utility', 0.5)
            self.scup_data['pressure'] = scup.get('pressure', 0.5)
            
            # Update bars
            values = list(self.scup_data.values())
            for bar, value in zip(self.bars, values):
                bar.set_height(value)
            
            # Save frame if requested
            if self.save_frames and self.frame_count % 10 == 0:
                filename = f"{self.output_dir}/scup_zone_animator_frame_{self.frame_count:06d}.png"
                self.fig.savefig(filename, dpi=100, bbox_inches='tight',
                               facecolor='#0a0a0a', edgecolor='none')
            
            self.frame_count += 1
            
            return self.bars
            
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
            print(f"SCUP Zone Animator saved {frame_count} frames to: {self.output_dir}")
        else:
            # Interactive mode
            self.animation = animation.FuncAnimation(
                self.fig, self.update_visualization,
                interval=100, blit=False, cache_frame_data=False
            )
            plt.show()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='DAWN SCUP Zone Animator')
    parser.add_argument('--source', choices=['stdin', 'demo'], default='stdin',
                       help='Data source (default: stdin)')
    parser.add_argument('--save', action='store_true',
                       help='Save visualization frames as PNG files')
    parser.add_argument('--output-dir', default='./visual_output/scup_zone_animator',
                       help='Directory to save output frames')
    
    args = parser.parse_args()
    
    viz = SCUPZoneAnimator(
        data_source=args.source,
        save_frames=args.save,
        output_dir=args.output_dir
    )
    
    viz.run()

if __name__ == '__main__':
    main() 