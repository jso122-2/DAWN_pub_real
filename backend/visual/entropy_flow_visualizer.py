#!/usr/bin/env python3
"""
DAWN Backend Entropy Flow Visualizer
Integrated version for backend tick engine with multi-process support
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyArrowPatch
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

class EntropyFlowVisualizer:
    """Backend-integrated entropy flow visualizer for DAWN with multi-process support"""
    
    def __init__(self, buffer_size=30, update_interval=100, max_processes=12):
        self.buffer_size = buffer_size
        self.update_interval = update_interval
        self.max_processes = max_processes
        self._active = True
        
        # Flow field parameters
        self.grid_size = 12
        self.field_bounds = (-6, 6, -6, 6)  # x_min, x_max, y_min, y_max
        
        # Create coordinate grids
        self.x = np.linspace(self.field_bounds[0], self.field_bounds[1], self.grid_size)
        self.y = np.linspace(self.field_bounds[2], self.field_bounds[3], self.grid_size)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        
        # Flow vectors (u, v components) for each process
        self.U = {i: np.zeros_like(self.X) for i in range(max_processes)}
        self.V = {i: np.zeros_like(self.Y) for i in range(max_processes)}
        self.magnitude = {i: np.zeros_like(self.X) for i in range(max_processes)}
        
        # Entropy state tracking for each process
        self.entropy_history = {i: deque(maxlen=buffer_size) for i in range(max_processes)}
        self.entropy_current = {i: 0.5 for i in range(max_processes)}
        self.flow_phase = {i: 0.0 for i in range(max_processes)}
        self.information_density = {i: np.zeros((self.grid_size, self.grid_size)) for i in range(max_processes)}
        
        # Information stream types
        self.stream_types = {
            'sensory': {'color': '#00aaff', 'weight': 1.0},      # Input streams
            'memory': {'color': '#aa00ff', 'weight': 0.8},       # Memory recall
            'cognitive': {'color': '#00ff88', 'weight': 1.2},    # Active thinking
            'creative': {'color': '#ffaa00', 'weight': 0.9},     # Creative synthesis
            'output': {'color': '#ff4444', 'weight': 1.1}        # Decision/action
        }
        
        # Setup matplotlib with subplots for multiple processes
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(24, 16))
        self.fig.patch.set_facecolor('#0a0a0a')
        
        # Create grid layout for multiple flow fields
        self.setup_multi_flow_layout()
        
        # Animation
        self.ani = None
        self.current_tick = 0
        
        # Setup GIF saver
        self.gif_saver = setup_gif_saver("entropy_flow_visualizer")
        
        # Setup signal handlers for GIF saving
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        atexit.register(self.cleanup)
        
        logger.info(f"EntropyFlowVisualizer initialized for {max_processes} processes")
    
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
    
    def setup_multi_flow_layout(self):
        """Setup layout for multiple process flow fields"""
        # Calculate grid dimensions
        cols = min(4, self.max_processes)  # Max 4 columns
        rows = (self.max_processes + cols - 1) // cols  # Calculate needed rows
        
        # Create subplots
        self.axes = []
        for i in range(self.max_processes):
            row = i // cols
            col = i % cols
            
            if i == 0:
                # Main flow field (process 0) gets more space
                ax = plt.subplot2grid((rows, cols), (row, col), colspan=2, rowspan=2)
            else:
                ax = plt.subplot2grid((rows, cols), (row, col))
            
            self.axes.append(ax)
            self.setup_flow_field(ax, i)
        
        plt.tight_layout()
    
    def setup_flow_field(self, ax, process_id):
        """Initialize the vector field display for a specific process"""
        ax.set_xlim(self.field_bounds[0], self.field_bounds[1])
        ax.set_ylim(self.field_bounds[2], self.field_bounds[3])
        ax.set_aspect('equal')
        ax.set_facecolor('#0a0a0a')
        
        # Create vector field quiver plot
        quiver = ax.quiver(self.X, self.Y, self.U[process_id], self.V[process_id],
                          self.magnitude[process_id], scale=20, scale_units='xy',
                          angles='xy', width=0.003, alpha=0.8,
                          cmap='plasma')
        
        # Add information density contours
        contour = ax.contour(self.X, self.Y, self.information_density[process_id],
                            levels=8, colors='white', alpha=0.2, linewidths=0.5)
        
        # Add cognitive region labels (only for main process to avoid clutter)
        if process_id == 0:
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
                ax.text(x, y, label, ha='center', va='center',
                       fontsize=9, color=color, weight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
        
        # Title and styling
        title = f'Process {process_id} Entropy Flow' if process_id > 0 else 'DAWN Information Entropy Flow\nCognitive Vector Field'
        ax.set_title(title, fontsize=12 if process_id == 0 else 8, color='white', weight='bold', pad=10)
        
        if process_id == 0:
            ax.set_xlabel('Cognitive Space X', color='#cccccc', fontsize=10)
            ax.set_ylabel('Cognitive Space Y', color='#cccccc', fontsize=10)
        
        # Add grid
        ax.grid(True, alpha=0.1, color='#444444')
        
        # Flow magnitude indicator
        flow_text = ax.text(0.02, 0.98, '', transform=ax.transAxes,
                           fontsize=8 if process_id == 0 else 6, color='#00ff88', 
                           verticalalignment='top', fontfamily='monospace')
        
        # Store references
        if not hasattr(self, 'flow_components'):
            self.flow_components = {}
        
        self.flow_components[process_id] = {
            'quiver': quiver,
            'contour': contour,
            'flow_text': flow_text
        }
    
    def is_active(self) -> bool:
        """Check if visualizer is active"""
        return self._active
    
    def parse_entropy_data(self, process_data: Dict[str, Any], process_id: int = 0) -> Dict[str, Any]:
        """Extract and process entropy flow from DAWN process data"""
        try:
            # Main entropy value
            entropy_raw = process_data.get('entropy', 0.5)
            entropy_val = float(entropy_raw) if isinstance(entropy_raw, (int, float)) else 0.5
            
            # Get additional cognitive metrics
            mood = process_data.get('mood', {})
            scup = process_data.get('scup', {})
            heat = process_data.get('heat', 0.3)
            tick = process_data.get('tick', 0)
            
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
            logger.error(f"Error parsing entropy data for process {process_id}: {e}")
            return {'entropy': 0.5, 'tick': 0, 'heat': 0.3, 'mood_influence': 0.5, 'scup_pressure': 0.5}
    
    def calculate_flow_field(self, flow_data: Dict[str, Any], process_id: int) -> Dict[str, float]:
        """Generate vector field from entropy and cognitive state for a specific process"""
        entropy = flow_data['entropy']
        tick = flow_data['tick']
        heat = flow_data['heat']
        mood_influence = flow_data['mood_influence']
        scup_pressure = flow_data['scup_pressure']
        
        # Update flow phase for temporal dynamics
        self.flow_phase[process_id] += 0.1 * entropy
        
        # Create base flow patterns
        # Radial flow from center (information integration)
        center_x, center_y = 0, 0
        radial_u = (self.X - center_x) * entropy * 0.5
        radial_v = (self.Y - center_y) * entropy * 0.5
        
        # Circular flow (cognitive circulation)
        circular_u = -(self.Y - center_y) * mood_influence * 0.3
        circular_v = (self.X - center_x) * mood_influence * 0.3
        
        # Wave patterns (oscillatory thinking)
        wave_u = np.sin(self.X * 0.5 + self.flow_phase[process_id]) * scup_pressure * 0.4
        wave_v = np.cos(self.Y * 0.5 + self.flow_phase[process_id]) * scup_pressure * 0.4
        
        # Heat-driven turbulence
        noise_u = np.random.normal(0, heat * 0.2, self.X.shape)
        noise_v = np.random.normal(0, heat * 0.2, self.Y.shape)
        
        # Combine flow components
        self.U[process_id] = radial_u + circular_u + wave_u + noise_u
        self.V[process_id] = radial_v + circular_v + wave_v + noise_v
        
        # Calculate flow magnitude
        self.magnitude[process_id] = np.sqrt(self.U[process_id]**2 + self.V[process_id]**2)
        
        # Update information density (areas of high processing)
        density_centers = [
            (0, 0, entropy),           # Central integration
            (-3, 3, mood_influence),   # Perception input
            (3, 3, scup_pressure),     # Decision output
            (0, -3, heat)              # Subconscious processing
        ]
        
        self.information_density[process_id].fill(0)
        for cx, cy, intensity in density_centers:
            # Gaussian density peaks
            distances = np.sqrt((self.X - cx)**2 + (self.Y - cy)**2)
            self.information_density[process_id] += intensity * np.exp(-distances**2 / 4)
        
        # Calculate stream intensities
        stream_intensities = {
            'sensory': mood_influence * (1 + 0.3 * np.sin(tick * 0.02 + process_id * 0.1)),
            'memory': entropy * (1 + 0.2 * np.cos(tick * 0.015 + process_id * 0.15)),
            'cognitive': heat * (1 + 0.4 * np.sin(tick * 0.03 + process_id * 0.2)),
            'creative': scup_pressure * (1 + 0.3 * np.cos(tick * 0.025 + process_id * 0.25)),
            'output': np.mean([entropy, heat, mood_influence]) * (1 + 0.2 * np.sin(tick * 0.04 + process_id * 0.3))
        }
        
        return stream_intensities
    
    def update_visualization(self, process_data: Dict[str, Any], process_id: int = 0, tick: int = 0) -> None:
        """Update the visualization with new process data"""
        try:
            # Parse and process data
            flow_data = self.parse_entropy_data(process_data, process_id)
            stream_intensities = self.calculate_flow_field(flow_data, process_id)
            
            # Store entropy history
            self.entropy_current[process_id] = flow_data['entropy']
            self.entropy_history[process_id].append(self.entropy_current[process_id])
            
            # Update vector field
            components = self.flow_components[process_id]
            components['quiver'].set_UVC(self.U[process_id], self.V[process_id], self.magnitude[process_id])
            
            # Update contours
            for collection in components['contour'].collections:
                collection.remove()
            components['contour'] = self.flow_components[process_id]['quiver'].axes.contour(
                self.X, self.Y, self.information_density[process_id],
                levels=8, colors='white', alpha=0.2, linewidths=0.5
            )
            
            # Update flow information display
            avg_magnitude = np.mean(self.magnitude[process_id])
            max_magnitude = np.max(self.magnitude[process_id])
            
            flow_info = (f"Tick: {tick:06d}\n"
                        f"Entropy: {self.entropy_current[process_id]:.3f}\n"
                        f"Avg Flow: {avg_magnitude:.3f}")
            components['flow_text'].set_text(flow_info)
            
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
                    'entropy': 0.3 + 0.1 * np.sin(tick * 0.01 + process_id * 0.5),
                    'heat': 0.3 + 0.1 * np.cos(tick * 0.02 + process_id * 0.3),
                    'mood': {
                        'vector': [0.5, 0.5, 0.5, 0.5]
                    },
                    'scup': {
                        'schema': 0.5 + 0.1 * np.sin(tick * 0.015 + process_id * 0.2),
                        'coherence': 0.5 + 0.1 * np.cos(tick * 0.02 + process_id * 0.4),
                        'utility': 0.5 + 0.1 * np.sin(tick * 0.025 + process_id * 0.6),
                        'pressure': 0.4 + 0.2 * np.cos(tick * 0.008 + process_id * 0.8)
                    }
                }
                self.update_visualization(default_data, process_id, tick)
        
        # Redraw
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()
    
    def get_visualization_data(self) -> Dict[str, Any]:
        """Get current visualization data for API/WebSocket transmission"""
        return {
            'entropy_data': {
                process_id: {
                    'current_entropy': self.entropy_current[process_id],
                    'entropy_history': list(self.entropy_history[process_id]),
                    'flow_magnitude': np.mean(self.magnitude[process_id]).item(),
                    'max_flow': np.max(self.magnitude[process_id]).item(),
                    'information_density': self.information_density[process_id].tolist()
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
            logger.info("Entropy flow animation started")
    
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
            logger.info("Entropy flow animation stopped")
    
    def show(self) -> None:
        """Show the visualization window"""
        plt.show()
    
    def close(self) -> None:
        """Close the visualization"""
        if self.fig:
            plt.close(self.fig)
        self._active = False
        logger.info("Entropy flow visualizer closed")
    
    async def shutdown(self) -> None:
        """Async shutdown"""
        self.close()

# Global instance for backend integration
_entropy_flow = None

def get_entropy_flow() -> EntropyFlowVisualizer:
    """Get or create the global entropy flow instance"""
    global _entropy_flow
    if _entropy_flow is None:
        _entropy_flow = EntropyFlowVisualizer()
    return _entropy_flow 