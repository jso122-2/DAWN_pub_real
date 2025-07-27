#!/usr/bin/env python3
"""
DAWN Cognition Visualization #3: Heat Monitor
Foundation Tier - "Meeting DAWN"

Real-time radial gauge visualization of DAWN's cognitive intensity.
Displays processing heat as a dynamic speedometer showing the engine's
cognitive load, processing speed, and mental effort across time.
"""

import json
import os
import os
import os
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for headless mode
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Wedge, Circle
import sys
import time
from collections import deque
import argparse
import math

class HeatMonitorVisualizer:
    def __init__(self, data_source="stdin", buffer_size=50, save_frames=False, output_dir="./visual_output"):
        self.data_source = data_source
        self.buffer_size = buffer_size
        self.save_frames = save_frames
        self.output_dir = output_dir
        self.frame_count = 0
        
        # Create output directory if saving
        if self.save_frames:
            os.makedirs(self.output_dir, exist_ok=True)
        
        # Heat state buffers
        self.heat_history = deque(maxlen=buffer_size)
        self.heat_current = 0.0
        self.heat_smoothed = 0.0
        self.heat_peak = 0.0
        self.heat_average = 0.0
        
        # Gauge parameters
        self.gauge_radius = 1.0
        self.gauge_center = (0, 0)
        self.gauge_start_angle = 225  # Bottom left
        self.gauge_end_angle = 315    # Bottom right (150 degree arc)
        self.gauge_range = self.gauge_end_angle - self.gauge_start_angle
        
        # Heat zones and colors
        self.heat_zones = [
            (0.0, 0.2, '#0066cc', 'Dormant'),      # Deep blue
            (0.2, 0.4, '#00aaff', 'Warming'),     # Light blue  
            (0.4, 0.6, '#00ff88', 'Active'),      # Green
            (0.6, 0.8, '#ffaa00', 'Intense'),     # Orange
            (0.8, 1.0, '#ff3300', 'Critical')     # Red
        ]
        
        # Setup matplotlib
        plt.style.use('dark_background')
        self.fig, (self.ax_gauge, self.ax_history) = plt.subplots(1, 2, figsize=(16, 8))
        self.fig.patch.set_facecolor('#0a0a0a')
        
        # Initialize gauge display
        self.setup_gauge()
        
        # Initialize history plot
        self.setup_history_plot()
        
        plt.tight_layout()
    
    def setup_gauge(self):
        """Initialize the radial gauge display"""
        self.ax_gauge.set_xlim(-1.5, 1.5)
        self.ax_gauge.set_ylim(-1.5, 1.5)
        self.ax_gauge.set_aspect('equal')
        self.ax_gauge.axis('off')
        
        # Create gauge background rings
        self.gauge_bg = Circle(self.gauge_center, self.gauge_radius, 
                              fill=False, edgecolor='#333333', linewidth=8)
        self.ax_gauge.add_patch(self.gauge_bg)
        
        # Create heat zone arcs
        self.zone_wedges = []
        zone_width = self.gauge_range / len(self.heat_zones)
        
        for i, (min_val, max_val, color, label) in enumerate(self.heat_zones):
            start_angle = self.gauge_start_angle + i * zone_width
            end_angle = start_angle + zone_width
            
            wedge = Wedge(self.gauge_center, self.gauge_radius, 
                         start_angle, end_angle, width=0.15,
                         facecolor=color, alpha=0.3, edgecolor=color, linewidth=2)
            self.ax_gauge.add_patch(wedge)
            self.zone_wedges.append(wedge)
            
            # Add zone labels
            mid_angle = math.radians((start_angle + end_angle) / 2)
            label_radius = self.gauge_radius + 0.3
            label_x = label_radius * math.cos(mid_angle)
            label_y = label_radius * math.sin(mid_angle)
            
            self.ax_gauge.text(label_x, label_y, label, 
                              ha='center', va='center', fontsize=10, 
                              color=color, weight='bold')
        
        # Create needle
        self.needle_angle = self.gauge_start_angle
        needle_length = self.gauge_radius * 0.8
        needle_x = needle_length * math.cos(math.radians(self.needle_angle))
        needle_y = needle_length * math.sin(math.radians(self.needle_angle))
        
        self.needle, = self.ax_gauge.plot([0, needle_x], [0, needle_y], 
                                         'w-', linewidth=4, solid_capstyle='round')
        
        # Add center hub
        self.hub = Circle(self.gauge_center, 0.05, facecolor='white', edgecolor='#cccccc')
        self.ax_gauge.add_patch(self.hub)
        
        # Add gauge markings
        for i in range(6):  # 5 major ticks
            angle = self.gauge_start_angle + i * (self.gauge_range / 5)
            angle_rad = math.radians(angle)
            
            # Major tick marks
            inner_radius = self.gauge_radius * 0.85
            outer_radius = self.gauge_radius * 0.95
            
            inner_x = inner_radius * math.cos(angle_rad)
            inner_y = inner_radius * math.sin(angle_rad)
            outer_x = outer_radius * math.cos(angle_rad)
            outer_y = outer_radius * math.sin(angle_rad)
            
            self.ax_gauge.plot([inner_x, outer_x], [inner_y, outer_y], 
                              'w-', linewidth=2, alpha=0.7)
            
            # Value labels
            value = i * 0.2  # 0.0 to 1.0
            label_radius = self.gauge_radius * 1.1
            label_x = label_radius * math.cos(angle_rad)
            label_y = label_radius * math.sin(angle_rad)
            
            self.ax_gauge.text(label_x, label_y, f'{value:.1f}', 
                              ha='center', va='center', fontsize=9, 
                              color='#cccccc')
        
        # Title and info display
        self.ax_gauge.text(0, 1.3, 'DAWN Cognitive Heat Monitor', 
                          ha='center', va='center', fontsize=16, 
                          color='white', weight='bold')
        
        # Digital readout
        self.readout_text = self.ax_gauge.text(0, -0.5, '', 
                                              ha='center', va='center', 
                                              fontsize=14, color='#00ff88', 
                                              fontfamily='monospace', weight='bold')
        
        # Status indicators
        self.status_text = self.ax_gauge.text(0, -0.7, '', 
                                             ha='center', va='center', 
                                             fontsize=10, color='#cccccc')
    
    def setup_history_plot(self):
        """Initialize the heat history timeline"""
        self.ax_history.set_xlim(0, self.buffer_size)
        self.ax_history.set_ylim(0, 1.0)
        self.ax_history.set_facecolor('#0a0a0a')
        
        # History line plot
        self.history_line, = self.ax_history.plot([], [], 'g-', linewidth=2, alpha=0.8)
        self.average_line, = self.ax_history.plot([], [], 'y--', linewidth=1, alpha=0.6)
        self.peak_line, = self.ax_history.plot([], [], 'r:', linewidth=1, alpha=0.8)
        
        # Fill area under curve
        self.history_fill = self.ax_history.fill_between([], [], alpha=0.2, color='green')
        
        # Add heat zone backgrounds
        for min_val, max_val, color, label in self.heat_zones:
            self.ax_history.axhspan(min_val, max_val, alpha=0.1, color=color)
        
        # Styling
        self.ax_history.set_xlabel('Time (Recent → Past)', color='#cccccc', fontsize=12)
        self.ax_history.set_ylabel('Cognitive Heat', color='#cccccc', fontsize=12)
        self.ax_history.set_title('Processing Intensity Timeline', 
                                 color='white', fontsize=14, weight='bold')
        
        self.ax_history.tick_params(colors='#cccccc')
        self.ax_history.grid(True, alpha=0.2, color='#444444')
        
        # Legend
        self.ax_history.legend(['Current Heat', 'Average', 'Peak'], 
                              loc='upper right', facecolor='#1a1a1a', 
                              edgecolor='#444444', labelcolor='#cccccc')
    
    def parse_heat_data(self, json_data):
        """Extract and process heat/intensity from DAWN JSON output"""
        try:
            # Direct heat value - handle both old and new format
            heat_raw = json_data.get('heat', 0.3)
            if 'thermal' in json_data and isinstance(json_data['thermal'], dict):
                heat_raw = json_data['thermal'].get('heat', heat_raw)
            
            # Calculate derived heat from other cognitive metrics
            mood = json_data.get('mood', {})
            entropy = json_data.get('entropy', 0.5)
            scup = json_data.get('scup', {})
            # Combine multiple heat sources
            base_heat = float(heat_raw) if isinstance(heat_raw, (int, float)) else 0.3
            # Mood contribution (emotional intensity)
            mood_intensity = 0.0
            if isinstance(mood, dict):
                mood_vector = mood.get('vector', [0.5, 0.5, 0.5, 0.5])
                if isinstance(mood_vector, list):
                    mood_intensity = np.mean([abs(x - 0.5) for x in mood_vector[:4]]) * 2
            # Entropy contribution (information processing load)
            entropy_heat = float(entropy) if isinstance(entropy, (int, float)) else 0.5
            # SCUP pressure contribution
            scup_pressure = 0.0
            if isinstance(scup, dict):
                pressures = [scup.get(k, 0.5) for k in ['schema', 'coherence', 'utility', 'pressure']]
                scup_pressure = np.mean([abs(p - 0.5) for p in pressures if isinstance(p, (int, float))]) * 2
            # Combine heat sources with weights
            combined_heat = (
                base_heat * 0.4 +           # Primary heat signal
                mood_intensity * 0.2 +      # Emotional intensity
                entropy_heat * 0.2 +        # Information processing
                scup_pressure * 0.2         # Cognitive pressure
            )
            # Add temporal variation
            tick = json_data.get('tick', 0)
            if 'tick_count' in json_data:
                tick = json_data['tick_count']
            if isinstance(tick, (int, float)):
                temporal_noise = np.sin(tick * 0.001) * 0.05  # Adjust frequency for larger tick counts
                combined_heat += temporal_noise
            # Clamp to valid range
            return max(0.0, min(1.0, combined_heat))
        except Exception as e:
            print(f"Error parsing heat data: {e}", file=sys.stderr)
            return 0.3
    
    def smooth_heat_transition(self, new_heat, alpha=0.2):
        """Apply temporal smoothing to heat transitions"""
        self.heat_smoothed = alpha * new_heat + (1 - alpha) * self.heat_smoothed
        return self.heat_smoothed
    
    def get_heat_zone(self, heat_value):
        """Determine which heat zone the current value falls into"""
        for min_val, max_val, color, label in self.heat_zones:
            if min_val <= heat_value < max_val:
                return color, label
        return self.heat_zones[-1][2], self.heat_zones[-1][3]  # Default to highest zone
    
    def read_latest_json_data(self):
        """Read data from stdin or JSON file depending on source"""
        if self.data_source == 'stdin':
            try:
                # Read from stdin
                line = sys.stdin.readline()
                if line.strip():
                    return json.loads(line.strip())
            except Exception as e:
                print(f"Error reading JSON: {e}", file=sys.stderr)
            return None
        else:
            # Read from JSON file for demo mode
            json_file = "/tmp/dawn_tick_data.json"
            if os.path.exists(json_file):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
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
            self.frame_count = frame
            # Read data from stdin or file
            data = self.read_latest_json_data()
            if data is None:
                # Use simulated data if no real data available
                data = {
                    'tick': frame,
                    'heat': 0.4 + 0.3 * np.sin(frame * 0.03) + 0.1 * np.sin(frame * 0.1),
                    'mood': {
                        'vector': [
                            0.5 + 0.2 * np.sin(frame * 0.02),
                            0.5 + 0.2 * np.cos(frame * 0.025)
                        ]
                    },
                    'entropy': 0.5 + 0.2 * np.sin(frame * 0.04),
                    'scup': {
                        'schema': 0.5 + 0.1 * np.sin(frame * 0.015),
                        'coherence': 0.5 + 0.1 * np.cos(frame * 0.02),
                        'utility': 0.5 + 0.1 * np.sin(frame * 0.025),
                        'pressure': 0.4 + 0.2 * np.cos(frame * 0.01)
                    }
                }
            # Update heat state
            raw_heat = self.parse_heat_data(data)
            self.heat_current = self.smooth_heat_transition(raw_heat)
            # Store in history
            self.heat_history.append(self.heat_current)
            # Update statistics
            if len(self.heat_history) > 1:
                self.heat_average = np.mean(list(self.heat_history))
                self.heat_peak = np.max(list(self.heat_history))
            # Update needle position
            heat_fraction = self.heat_current
            self.needle_angle = self.gauge_start_angle + heat_fraction * self.gauge_range
            needle_length = self.gauge_radius * 0.8
            needle_x = needle_length * math.cos(math.radians(self.needle_angle))
            needle_y = needle_length * math.sin(math.radians(self.needle_angle))
            self.needle.set_data([0, needle_x], [0, needle_y])
            # Update needle color based on heat zone
            zone_color, zone_label = self.get_heat_zone(self.heat_current)
            self.needle.set_color(zone_color)
            # Update digital readout
            tick = data.get('tick', frame)
            if 'tick_count' in data:
                tick = data['tick_count']
            readout = f"HEAT: {self.heat_current:.3f}\nTICK: {tick:06d}"
            self.readout_text.set_text(readout)
            self.readout_text.set_color(zone_color)
            # Update status
            status = f"Zone: {zone_label} | Avg: {self.heat_average:.3f} | Peak: {self.heat_peak:.3f}"
            self.status_text.set_text(status)
            # Update history plot
            if len(self.heat_history) > 1:
                x_data = list(range(len(self.heat_history)))
                y_data = list(self.heat_history)
                self.history_line.set_data(x_data, y_data)
                # Update average and peak lines
                avg_data = [self.heat_average] * len(x_data)
                peak_data = [self.heat_peak] * len(x_data)
                self.average_line.set_data(x_data, avg_data)
                self.peak_line.set_data(x_data, peak_data)
                # Update fill
                if hasattr(self, 'history_fill') and self.history_fill:
                    self.history_fill.remove()
                self.history_fill = self.ax_history.fill_between(x_data, y_data, alpha=0.2, color=zone_color)
            
            # Save frame if requested
            if self.save_frames and self.frame_count % 10 == 0:  # Save every 10th frame
                filename = f"{self.output_dir}/heat_monitor_frame_{self.frame_count:06d}.png"
                self.fig.savefig(filename, dpi=100, bbox_inches='tight', 
                               facecolor='#0a0a0a', edgecolor='none')
            
            return [self.needle, self.readout_text, self.status_text, 
                   self.history_line, self.average_line, self.peak_line]
        except Exception as e:
            print(f"Update error: {e}", file=sys.stderr)
            return []
    
    def run(self, interval=50):
        """Start the real-time visualization"""
        try:
            if self.save_frames:
                # For saving mode, run a limited number of frames
                for frame in range(1000):  # Process up to 1000 frames
                    self.update_visualization(frame)
                    if frame % 50 == 0:  # Print progress every 50 frames
                        print(f"Processed frame {frame}", file=sys.stderr)
                    # Check if there's more data to read
                    try:
                        import select
                        if not select.select([sys.stdin], [], [], 0)[0]:
                            break  # No more data available
                    except:
                        pass
                print(f"Heat Monitor saved frames to: {self.output_dir}")
            else:
                # Interactive mode
                ani = animation.FuncAnimation(self.fig, self.update_visualization, 
                                            interval=interval, blit=False, cache_frame_data=False)
                plt.show()
                print("\nHeat Monitor terminated by user.")
        except Exception as e:
            print(f"Runtime error: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description='DAWN Heat Monitor')
    parser.add_argument('--source', choices=['stdin', 'demo'], default='stdin',
                       help='Data source: stdin for live DAWN data, demo for testing')
    parser.add_argument('--interval', type=int, default=50,
                       help='Animation update interval in milliseconds')
    parser.add_argument('--buffer', type=int, default=50,
                       help='Heat history buffer size')
    parser.add_argument('--save', action='store_true',
                       help='Save visualization frames as PNG files')
    parser.add_argument('--output-dir', default='./visual_output/heat_monitor',
                       help='Directory to save output frames')
    
    args = parser.parse_args()
    
    print("DAWN Cognition Visualization #3: Heat Monitor")
    print("Cognitive Intensity Gauge")
    print("=" * 50)
    
    if args.source == 'stdin':
        print("Waiting for DAWN JSON data on stdin...")
        print("Monitoring cognitive heat and processing intensity...")
    else:
        print("Running in demo mode with simulated heat data...")
    
    if args.save:
        print(f"Saving frames to: {args.output_dir}")
    
    visualizer = HeatMonitorVisualizer(data_source=args.source, buffer_size=args.buffer,
                                     save_frames=args.save, output_dir=args.output_dir)
    visualizer.run(interval=args.interval)

if __name__ == "__main__":
    main()