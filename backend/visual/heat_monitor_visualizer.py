#!/usr/bin/env python3
"""
DAWN Backend Heat Monitor Visualizer
Integrated version for backend tick engine with multi-process support
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Wedge, Circle
import asyncio
import logging
from collections import deque
from typing import Dict, Any, Optional, List
from datetime import datetime
import math
import signal
import atexit
import sys

# Import GIF saver
try:
    from .gif_saver import setup_gif_saver
except ImportError:
    from gif_saver import setup_gif_saver

logger = logging.getLogger(__name__)

class HeatMonitorVisualizer:
    """Backend-integrated heat monitor for DAWN with multi-process support"""
    
    def __init__(self, buffer_size=50, update_interval=50, max_processes=12):
        self.buffer_size = buffer_size
        self.update_interval = update_interval
        self.max_processes = max_processes
        self._active = True
        
        # Heat state buffers for multiple processes
        self.heat_history = {i: deque(maxlen=buffer_size) for i in range(max_processes)}
        self.heat_current = {i: 0.0 for i in range(max_processes)}
        self.heat_smoothed = {i: 0.0 for i in range(max_processes)}
        self.heat_peak = {i: 0.0 for i in range(max_processes)}
        self.heat_average = {i: 0.0 for i in range(max_processes)}
        
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
        
        # Setup matplotlib with subplots for multiple processes
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(20, 12))
        self.fig.patch.set_facecolor('#0a0a0a')
        
        # Animation
        self.ani = None
        self.current_tick = 0
        
        # Setup GIF saver
        self.gif_saver = setup_gif_saver("heat_monitor_visualizer")
        
        # Setup signal handlers for GIF saving
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        atexit.register(self.cleanup)
        
        # Create grid layout for multiple gauges
        self.setup_multi_gauge_layout()
        
        logger.info(f"HeatMonitorVisualizer initialized for {max_processes} processes")
    
    def save_animation_gif(self):
        """Save the animation as GIF"""
        try:
            if hasattr(self, 'ani'):
                gif_path = self.gif_saver.save_animation_as_gif(self.ani, fps=10, dpi=100)
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
    
    def setup_multi_gauge_layout(self):
        """Setup layout for multiple process gauges"""
        # Calculate grid dimensions
        cols = min(4, self.max_processes)  # Max 4 columns
        rows = (self.max_processes + cols - 1) // cols  # Calculate needed rows
        
        # Create subplots
        self.axes = []
        for i in range(self.max_processes):
            row = i // cols
            col = i % cols
            
            if i == 0:
                # Main gauge (process 0) gets more space
                ax = plt.subplot2grid((rows, cols), (row, col), colspan=2, rowspan=2)
            else:
                ax = plt.subplot2grid((rows, cols), (row, col))
            
            self.axes.append(ax)
            self.setup_gauge(ax, i)
        
        plt.tight_layout()
    
    def setup_gauge(self, ax, process_id):
        """Initialize a radial gauge display for a specific process"""
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Create gauge background rings
        gauge_bg = Circle(self.gauge_center, self.gauge_radius, 
                         fill=False, edgecolor='#333333', linewidth=8)
        ax.add_patch(gauge_bg)
        
        # Create heat zone arcs
        zone_wedges = []
        zone_width = self.gauge_range / len(self.heat_zones)
        
        for i, (min_val, max_val, color, label) in enumerate(self.heat_zones):
            start_angle = self.gauge_start_angle + i * zone_width
            end_angle = start_angle + zone_width
            
            wedge = Wedge(self.gauge_center, self.gauge_radius, 
                         start_angle, end_angle, width=0.15,
                         facecolor=color, alpha=0.3, edgecolor=color, linewidth=2)
            ax.add_patch(wedge)
            zone_wedges.append(wedge)
            
            # Add zone labels (only for main gauge to avoid clutter)
            if process_id == 0:
                mid_angle = math.radians((start_angle + end_angle) / 2)
                label_radius = self.gauge_radius + 0.3
                label_x = label_radius * math.cos(mid_angle)
                label_y = label_radius * math.sin(mid_angle)
                
                ax.text(label_x, label_y, label, 
                       ha='center', va='center', fontsize=10, 
                       color=color, weight='bold')
        
        # Create needle
        needle_angle = self.gauge_start_angle
        needle_length = self.gauge_radius * 0.8
        needle_x = needle_length * math.cos(math.radians(needle_angle))
        needle_y = needle_length * math.sin(math.radians(needle_angle))
        
        needle, = ax.plot([0, needle_x], [0, needle_y], 
                         'w-', linewidth=4, solid_capstyle='round')
        
        # Add center hub
        hub = Circle(self.gauge_center, 0.05, facecolor='white', edgecolor='#cccccc')
        ax.add_patch(hub)
        
        # Add gauge markings (only for main gauge)
        if process_id == 0:
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
                
                ax.plot([inner_x, outer_x], [inner_y, outer_y], 
                       'w-', linewidth=2, alpha=0.7)
                
                # Value labels
                value = i * 0.2  # 0.0 to 1.0
                label_radius = self.gauge_radius * 1.1
                label_x = label_radius * math.cos(angle_rad)
                label_y = label_radius * math.sin(angle_rad)
                
                ax.text(label_x, label_y, f'{value:.1f}', 
                       ha='center', va='center', fontsize=9, 
                       color='#cccccc')
        
        # Title and info display
        title = f'Process {process_id}' if process_id > 0 else 'DAWN Cognitive Heat Monitor'
        ax.text(0, 1.3, title, 
               ha='center', va='center', fontsize=12 if process_id == 0 else 8, 
               color='white', weight='bold')
        
        # Digital readout
        readout_text = ax.text(0, -0.5, '', 
                              ha='center', va='center', 
                              fontsize=10 if process_id == 0 else 8, color='#00ff88', 
                              fontfamily='monospace', weight='bold')
        
        # Status indicators
        status_text = ax.text(0, -0.7, '', 
                             ha='center', va='center', 
                             fontsize=8 if process_id == 0 else 6, color='#cccccc')
        
        # Store references
        if not hasattr(self, 'gauge_components'):
            self.gauge_components = {}
        
        self.gauge_components[process_id] = {
            'needle': needle,
            'readout_text': readout_text,
            'status_text': status_text,
            'zone_wedges': zone_wedges
        }
    
    def is_active(self) -> bool:
        """Check if visualizer is active"""
        return self._active
    
    def parse_heat_data(self, process_data: Dict[str, Any], process_id: int = 0) -> float:
        """Extract and process heat/intensity from DAWN process data"""
        try:
            # Direct heat value
            heat_raw = process_data.get('heat', 0.3)
            
            # Calculate derived heat from other cognitive metrics
            mood = process_data.get('mood', {})
            entropy = process_data.get('entropy', 0.5)
            scup = process_data.get('scup', {})
            
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
            tick = process_data.get('tick', 0)
            if isinstance(tick, (int, float)):
                temporal_noise = np.sin(tick * 0.1 + process_id * 0.5) * 0.05
                combined_heat += temporal_noise
            
            # Clamp to valid range
            return max(0.0, min(1.0, combined_heat))
            
        except Exception as e:
            logger.error(f"Error parsing heat data for process {process_id}: {e}")
            return 0.3
    
    def smooth_heat_transition(self, new_heat: float, process_id: int, alpha: float = 0.2) -> float:
        """Apply temporal smoothing to heat transitions"""
        self.heat_smoothed[process_id] = alpha * new_heat + (1 - alpha) * self.heat_smoothed[process_id]
        return self.heat_smoothed[process_id]
    
    def get_heat_zone(self, heat_value: float) -> tuple:
        """Determine which heat zone the current value falls into"""
        for min_val, max_val, color, label in self.heat_zones:
            if min_val <= heat_value < max_val:
                return color, label
        return self.heat_zones[-1][2], self.heat_zones[-1][3]  # Default to highest zone
    
    def update_visualization(self, process_data: Dict[str, Any], process_id: int = 0, tick: int = 0) -> None:
        """Update the visualization with new process data"""
        try:
            # Update heat state
            raw_heat = self.parse_heat_data(process_data, process_id)
            self.heat_current[process_id] = self.smooth_heat_transition(raw_heat, process_id)
            
            # Store in history
            self.heat_history[process_id].append(self.heat_current[process_id])
            
            # Update statistics
            if len(self.heat_history[process_id]) > 1:
                self.heat_average[process_id] = np.mean(list(self.heat_history[process_id]))
                self.heat_peak[process_id] = np.max(list(self.heat_history[process_id]))
            
            # Update needle position
            heat_fraction = self.heat_current[process_id]
            needle_angle = self.gauge_start_angle + heat_fraction * self.gauge_range
            
            needle_length = self.gauge_radius * 0.8
            needle_x = needle_length * math.cos(math.radians(needle_angle))
            needle_y = needle_length * math.sin(math.radians(needle_angle))
            
            components = self.gauge_components[process_id]
            components['needle'].set_data([0, needle_x], [0, needle_y])
            
            # Update needle color based on heat zone
            zone_color, zone_label = self.get_heat_zone(self.heat_current[process_id])
            components['needle'].set_color(zone_color)
            
            # Update digital readout
            readout = f"HEAT: {self.heat_current[process_id]:.3f}\nTICK: {tick:06d}"
            components['readout_text'].set_text(readout)
            components['readout_text'].set_color(zone_color)
            
            # Update status
            status = f"Zone: {zone_label} | Avg: {self.heat_average[process_id]:.3f}"
            components['status_text'].set_text(status)
            
        except Exception as e:
            logger.error(f"Update error for process {process_id}: {e}")
    
    def update_all_processes(self, all_process_data: Dict[int, Dict[str, Any]], tick: int) -> None:
        """Update visualization for all processes"""
        for process_id in range(self.max_processes):
            if process_id in all_process_data:
                self.update_visualization(all_process_data[process_id], process_id, tick)
            else:
                # Use default data for inactive processes
                default_data = {
                    'tick': tick,
                    'heat': 0.1,
                    'mood': {'vector': [0.5, 0.5, 0.5, 0.5]},
                    'entropy': 0.3,
                    'scup': {'schema': 0.3, 'coherence': 0.3, 'utility': 0.3, 'pressure': 0.3}
                }
                self.update_visualization(default_data, process_id, tick)
        
        # Redraw
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()
    
    def get_visualization_data(self) -> Dict[str, Any]:
        """Get current visualization data for API/WebSocket transmission"""
        return {
            'heat_data': {
                process_id: {
                    'current': self.heat_current[process_id],
                    'average': self.heat_average[process_id],
                    'peak': self.heat_peak[process_id],
                    'history': list(self.heat_history[process_id])
                } for process_id in range(self.max_processes)
            },
            'current_tick': self.current_tick,
            'timestamp': datetime.now().isoformat()
        }
    
    def start_animation(self) -> None:
        """Start the animation loop"""
        if self.ani is None:
            self.ani = animation.FuncAnimation(
                self.fig, 
                lambda frame: self._animation_frame(frame), 
                interval=self.update_interval, 
                blit=False, 
                cache_frame_data=False
            )
            logger.info("Heat monitor animation started")
    
    def _animation_frame(self, frame) -> None:
        """Animation frame update (called by matplotlib)"""
        # This will be called by matplotlib animation
        # The actual updates are handled by update_visualization()
        pass
    
    def stop_animation(self) -> None:
        """Stop the animation"""
        if self.ani is not None:
            self.ani.event_source.stop()
            self.ani = None
            logger.info("Heat monitor animation stopped")
    
    def show(self) -> None:
        """Show the visualization window"""
        plt.show()
    
    def close(self) -> None:
        """Close the visualization"""
        if self.fig:
            plt.close(self.fig)
        self._active = False
        logger.info("Heat monitor visualizer closed")
    
    async def shutdown(self) -> None:
        """Async shutdown"""
        self.close()

# Global instance for backend integration
_heat_monitor = None

def get_heat_monitor() -> HeatMonitorVisualizer:
    """Get or create the global heat monitor instance"""
    global _heat_monitor
    if _heat_monitor is None:
        _heat_monitor = HeatMonitorVisualizer()
    return _heat_monitor 