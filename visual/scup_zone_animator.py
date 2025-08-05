#!/usr/bin/env python3
# Add parent directory to Python path for imports
"""
Fixed DAWN SCUP Zone Animator
Real-time SCUP zone visualization with cognitive state mapping

Transforms the original static GIF generator into a live real-time
visualization that reads DAWN's JSON data and displays SCUP dynamics
with proper cognitive zone terminology.
"""

import json
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import sys
import time
from collections import deque
import argparse


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
class SCUPZoneAnimator:
    def __init__(self, data_source="stdin", buffer_size=100):
        self.data_source = data_source
        self.buffer_size = buffer_size
        
        # SCUP data tracking
        self.scup_history = deque(maxlen=buffer_size)
        self.zone_history = deque(maxlen=buffer_size)
        self.timestamp_history = deque(maxlen=buffer_size)
        
        # Current state
        self.current_scup = {'schema': 0.5, 'coherence': 0.5, 'utility': 0.5, 'pressure': 0.5}
        self.current_zone = 'dormant'
        self.current_heat = 0.3
        
        # Cognitive zone definitions (semantic terminology)
        self.cognitive_zones = {
            'dormant': {
                'color': '#424242',
                'alpha': 0.3,
                'description': 'Minimal cognitive activity',
                'scup_range': (0.0, 0.4)
            },
            'contemplative': {
                'color': '#2196f3', 
                'alpha': 0.4,
                'description': 'Reflective processing state',
                'scup_range': (0.4, 0.6)
            },
            'active': {
                'color': '#4caf50',
                'alpha': 0.5,
                'description': 'Engaged cognitive processing',
                'scup_range': (0.6, 0.8)
            },
            'intense': {
                'color': '#ff9800',
                'alpha': 0.6,
                'description': 'High-intensity cognitive work',
                'scup_range': (0.8, 0.9)
            },
            'transcendent': {
                'color': '#9c27b0',
                'alpha': 0.7,
                'description': 'Peak cognitive performance',
                'scup_range': (0.9, 1.0)
            }
        }
        
        # Setup matplotlib with proper backend
        plt.style.use('dark_background')
        self.fig, (self.ax_main, self.ax_zones) = plt.subplots(2, 1, figsize=(14, 10))
        self.fig.patch.set_facecolor('#0a0a0a')
        
        # Initialize displays
        self.setup_scup_display()
        self.setup_zone_display()
        
        plt.tight_layout()
    
    def setup_scup_display(self):
        """Initialize the SCUP timeline display"""
        self.ax_main.set_facecolor('#0a0a0a')
        self.ax_main.set_xlim(0, self.buffer_size)
        self.ax_main.set_ylim(0, 1.0)
        
        # SCUP component lines
        self.scup_lines = {}
        scup_colors = {
            'schema': '#2196f3',      # Blue
            'coherence': '#4caf50',   # Green  
            'utility': '#ff9800',     # Orange
            'pressure': '#f44336'     # Red
        }
        
        for component, color in scup_colors.items():
            line, = self.ax_main.plot([], [], color=color, linewidth=2.5, 
                                     alpha=0.8, label=f'{component.title()}')
            self.scup_lines[component] = line
        
        # Combined SCUP average line
        self.scup_avg_line, = self.ax_main.plot([], [], color='white', linewidth=3,
                                               alpha=0.9, label='SCUP Average')
        
        # Zone overlay background
        self.zone_overlay = None
        
        # Styling
        self.ax_main.set_title('DAWN SCUP Dynamics & Cognitive Zones', 
                              fontsize=16, color='white', weight='bold', pad=20)
        self.ax_main.set_xlabel('Time Steps', color='#cccccc', fontsize=12)
        self.ax_main.set_ylabel('SCUP Component Values', color='#cccccc', fontsize=12)
        
        self.ax_main.grid(True, alpha=0.2, color='#444444')
        self.ax_main.legend(loc='upper left', facecolor='#1a1a1a', 
                           edgecolor='#444444', labelcolor='#cccccc')
        
        # Real-time info display
        self.info_text = self.ax_main.text(0.02, 0.98, '', transform=self.ax_main.transAxes,
                                          fontsize=10, color='#00ff88', verticalalignment='top',
                                          fontfamily='monospace', weight='bold')
    
    def setup_zone_display(self):
        """Initialize the cognitive zone indicator display"""
        self.ax_zones.set_facecolor('#0a0a0a')
        self.ax_zones.set_xlim(0, self.buffer_size)
        self.ax_zones.set_ylim(-0.5, len(self.cognitive_zones) - 0.5)
        
        # Zone level indicators
        self.zone_rectangles = {}
        zone_names = list(self.cognitive_zones.keys())
        
        for i, (zone_name, zone_config) in enumerate(self.cognitive_zones.items()):
            # Background rectangle for each zone level
            rect = Rectangle((0, i-0.4), self.buffer_size, 0.8, 
                           facecolor=zone_config['color'], alpha=0.1,
                           edgecolor=zone_config['color'], linewidth=1)
            self.ax_zones.add_patch(rect)
            
            # Zone label
            self.ax_zones.text(-2, i, zone_name.title(), 
                             color=zone_config['color'], fontsize=11, 
                             weight='bold', ha='right', va='center')
        
        # Current zone indicator line
        self.current_zone_line, = self.ax_zones.plot([], [], 'white', linewidth=4, alpha=0.8)
        
        # Zone transition markers
        self.zone_markers = self.ax_zones.scatter([], [], s=[], c=[], 
                                                 cmap='plasma', alpha=0.8)
        
        # Styling
        self.ax_zones.set_title('Cognitive Zone Progression', 
                               fontsize=14, color='white', weight='bold')
        self.ax_zones.set_xlabel('Time Steps', color='#cccccc', fontsize=12)
        self.ax_zones.set_ylabel('Cognitive Zones', color='#cccccc', fontsize=12)
        
        self.ax_zones.set_yticks(range(len(self.cognitive_zones)))
        self.ax_zones.set_yticklabels([name.title() for name in self.cognitive_zones.keys()],
                                     color='#cccccc')
        self.ax_zones.grid(True, alpha=0.2, color='#444444')
    
    def parse_scup_data(self, json_data):
        """Extract SCUP data from DAWN JSON output"""
        try:
            # Extract SCUP components
            scup = json_data.get('scup', {})
            
            scup_data = {
                'schema': float(scup.get('schema', 0.5)),
                'coherence': float(scup.get('coherence', 0.5)),
                'utility': float(scup.get('utility', 0.5)), 
                'pressure': float(scup.get('pressure', 0.5))
            }
            
            # Calculate average SCUP
            scup_avg = np.mean(list(scup_data.values()))
            
            # Extract additional context
            heat = float(json_data.get('heat', 0.3))
            tick = json_data.get('tick', 0)
            
            return {
                'scup_components': scup_data,
                'scup_average': scup_avg,
                'heat': heat,
                'tick': tick
            }
        except Exception as e:
            print(f"Error parsing SCUP data: {e}", file=sys.stderr)
            return {
                'scup_components': self.current_scup,
                'scup_average': 0.5,
                'heat': 0.3,
                'tick': 0
            }
    
    def classify_cognitive_zone(self, scup_data):
        """Classify current cognitive state into a semantic zone"""
        scup_avg = scup_data['scup_average']
        heat = scup_data['heat']
        scup_components = scup_data['scup_components']
        
        # Enhanced zone classification using multiple factors
        
        # Base classification by SCUP average
        base_zone = 'dormant'
        for zone_name, zone_config in self.cognitive_zones.items():
            min_val, max_val = zone_config['scup_range']
            if min_val <= scup_avg < max_val:
                base_zone = zone_name
                break
        
        # Refinements based on specific SCUP patterns
        schema = scup_components['schema']
        coherence = scup_components['coherence']
        pressure = scup_components['pressure']
        
        # Transcendent state: high schema + coherence, low pressure
        if schema > 0.8 and coherence > 0.8 and pressure < 0.4:
            return 'transcendent'
        
        # Contemplative state: moderate coherence, low pressure, moderate schema
        elif 0.5 < coherence < 0.8 and pressure < 0.5 and 0.4 < schema < 0.7:
            return 'contemplative'
        
        # Intense state: high pressure regardless of other factors
        elif pressure > 0.8:
            return 'intense'
        
        return base_zone
    
    def read_latest_json_data(self):
        """Read the latest data from JSON file"""
        json_file = "/tmp/dawn_tick_data.json"
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    last_line = lines[-1].strip()
                    if last_line:
                        return json.loads(last_line)
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
                    'mood': {'valence': 0.5 + 0.2 * np.sin(frame * 0.05)},
                    'entropy': {'total_entropy': 0.5 + 0.2 * np.sin(frame * 0.03)},
                    'thermal_state': {'heat_level': 0.3 + 0.1 * np.cos(frame * 0.04)},
                    'scup': {'schema': 0.5, 'coherence': 0.5, 'utility': 0.5, 'pressure': 0.5}
                }
        except Exception as e:
            print(f"JSON decode error: {e}", file=sys.stderr)
            return []

        try:
            # Process SCUP data
            scup_data = self.parse_scup_data(data)
            cognitive_zone = self.classify_cognitive_zone(scup_data)
            
            # Update history
            self.scup_history.append(scup_data)
            self.zone_history.append(cognitive_zone)
            self.timestamp_history.append(len(self.scup_history))
            
            # Update current state
            self.current_scup = scup_data['scup_components']
            self.current_zone = cognitive_zone
            self.current_heat = scup_data['heat']
            
            # Update SCUP component lines
            if len(self.scup_history) > 1:
                x_data = list(self.timestamp_history)
                
                for component in ['schema', 'coherence', 'utility', 'pressure']:
                    y_data = [h['scup_components'][component] for h in self.scup_history]
                    self.scup_lines[component].set_data(x_data, y_data)
                
                # Update average SCUP line
                avg_data = [h['scup_average'] for h in self.scup_history]
                self.scup_avg_line.set_data(x_data, avg_data)
                
                # Update zone overlay
                if self.zone_overlay:
                    self.zone_overlay.remove()
                
                zone_config = self.cognitive_zones[cognitive_zone]
                x_start = max(0, len(x_data) - 10)  # Last 10 steps
                self.zone_overlay = self.ax_main.fill_between(
                    x_data[x_start:], 0, 1.0,
                    color=zone_config['color'], alpha=zone_config['alpha'],
                    label=f'Zone: {cognitive_zone.title()}'
                )
            
            # Update zone progression display
            if len(self.zone_history) > 1:
                x_data = list(self.timestamp_history)
                
                # Map zones to numeric levels for plotting
                zone_levels = []
                zone_names = list(self.cognitive_zones.keys())
                
                for zone in self.zone_history:
                    zone_level = zone_names.index(zone) if zone in zone_names else 0
                    zone_levels.append(zone_level)
                
                self.current_zone_line.set_data(x_data, zone_levels)
                
                # Update zone transition markers
                transitions = self.detect_zone_transitions()
                if transitions:
                    trans_x = [self.timestamp_history[i] for i in transitions]
                    trans_y = [zone_levels[i] for i in transitions]
                    trans_sizes = [100] * len(transitions)
                    trans_colors = [zone_levels[i] for i in transitions]
                    
                    self.zone_markers.set_offsets(list(zip(trans_x, trans_y)))
                    self.zone_markers.set_sizes(trans_sizes)
                    self.zone_markers.set_array(np.array(trans_colors))
            
            # Update info display
            tick = scup_data['tick']
            info_text = (f"Tick: {tick:06d} | Zone: {cognitive_zone.title()}\n"
                        f"SCUP Avg: {scup_data['scup_average']:.3f} | Heat: {scup_data['heat']:.3f}\n"
                        f"S:{self.current_scup['schema']:.2f} "
                        f"C:{self.current_scup['coherence']:.2f} "
                        f"U:{self.current_scup['utility']:.2f} "
                        f"P:{self.current_scup['pressure']:.2f}")
            
            self.info_text.set_text(info_text)
            
            # Update axis limits for scrolling
            if len(self.timestamp_history) > self.buffer_size * 0.8:
                x_min = len(self.timestamp_history) - self.buffer_size
                x_max = len(self.timestamp_history)
                
                self.ax_main.set_xlim(x_min, x_max)
                self.ax_zones.set_xlim(x_min, x_max)
            
            return (list(self.scup_lines.values()) + 
                   [self.scup_avg_line, self.current_zone_line, self.zone_markers])
        except Exception as e:
            print(f"Update error: {e}", file=sys.stderr)
            return []
    
    def detect_zone_transitions(self):
        """Detect when cognitive zone changes occur"""
        if len(self.zone_history) < 2:
            return []
        
        transitions = []
        zones = list(self.zone_history)
        
        for i in range(1, len(zones)):
            if zones[i] != zones[i-1]:
                transitions.append(i)
        
        return transitions
    
    def run(self, interval=200):
        """Start the real-time visualization"""
        try:
            ani = animation.FuncAnimation(self.fig, self.update_visualization,
                                        interval=interval, blit=False, cache_frame_data=False)
            plt.show()
            print("\nSCUP Zone Animator terminated by user.")
        except Exception as e:
            print(f"Runtime error: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description='Fixed DAWN SCUP Zone Animator')
    parser.add_argument('--source', choices=['stdin', 'demo'], default='stdin',
                       help='Data source: stdin for live DAWN data, demo for testing')
    parser.add_argument('--interval', type=int, default=200,
                       help='Animation update interval in milliseconds')
    parser.add_argument('--buffer', type=int, default=100,
                       help='SCUP history buffer size')
    
    args = parser.parse_args()
    
    print("Fixed DAWN SCUP Zone Animator")
    print("Real-time Cognitive Zone Visualization")
    print("=" * 50)
    
    if args.source == 'stdin':
        print("Waiting for DAWN JSON data on stdin...")
        print("Monitoring SCUP dynamics and cognitive zone transitions...")
    else:
        print("Running in demo mode with simulated SCUP data...")
    
    # Create output directory if it doesn't exist
    output_dir = "visual/outputs/scup_zone_animator"
    os.makedirs(output_dir, exist_ok=True)
    
    animator = SCUPZoneAnimator(data_source=args.source, buffer_size=args.buffer)
    animator.run(interval=args.interval)

if __name__ == "__main__":
    main()