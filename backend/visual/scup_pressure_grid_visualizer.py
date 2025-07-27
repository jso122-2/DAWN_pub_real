#!/usr/bin/env python3
"""
DAWN Backend SCUP Pressure Grid Visualizer
Integrated version for backend tick engine with multi-process support
"""

import logging
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
from collections import deque
from typing import Dict, Any, List
from datetime import datetime
import time
import signal
import atexit
import sys

# Import GIF saver
try:
    from .gif_saver import setup_gif_saver
except ImportError:
    try:
        from gif_saver import setup_gif_saver
    except ImportError:
        def setup_gif_saver(name):
            class DummyGifSaver:
                def save_animation_as_gif(self, animation, fps=5, dpi=100):
                    return None
            return DummyGifSaver()

logger = logging.getLogger(__name__)

class SCUPPressureGridVisualizer:
    """Backend-integrated SCUP pressure grid for DAWN with multi-process support"""
    
    def __init__(self, smoothing=0.15, interaction_model='reinforcing', 
                 history_size=50, max_processes=12):
        # Core dimensions
        self.dimensions = ['Schema', 'Coherence', 'Utility', 'Pressure']
        self.short_dims = ['S', 'C', 'U', 'P']
        
        # Interaction labels for off-diagonal cells
        self.interaction_labels = {
            (0, 1): 'Structure↔Meaning',
            (0, 2): 'Pattern↔Goal',
            (0, 3): 'Structure↔Urgency',
            (1, 0): 'Meaning↔Structure',
            (1, 2): 'Meaning↔Goal',
            (1, 3): 'Meaning↔Urgency',
            (2, 0): 'Goal↔Pattern',
            (2, 1): 'Goal↔Meaning',
            (2, 3): 'Goal↔Urgency',
            (3, 0): 'Urgency↔Structure',
            (3, 1): 'Urgency↔Meaning',
            (3, 2): 'Urgency↔Goal'
        }
        
        # Self-pressure labels for diagonal cells
        self.self_labels = {
            0: 'Pattern\nRigidity',
            1: 'Meaning\nIntegration',
            2: 'Goal\nOptimization',
            3: 'Urgency\nAmplification'
        }
        
        # Interaction calculation models
        self.interaction_models = {
            'reinforcing': lambda a, b: a * b,
            'competing': lambda a, b: abs(a - b),
            'averaging': lambda a, b: (a + b) / 2,
            'tension': lambda a, b: min(a, b) * abs(a - b),
            'synergistic': lambda a, b: (a * b) ** 0.5
        }
        
        # Parameters
        self.smoothing = smoothing
        self.interaction_model_name = interaction_model
        self.interaction_fn = self.interaction_models[interaction_model]
        self.history_size = history_size
        self.max_processes = max_processes
        self._active = True
        
        # State variables for each process
        self.pressure_matrix = {i: np.zeros((4, 4)) for i in range(max_processes)}
        self.pressure_history = {i: deque(maxlen=history_size) for i in range(max_processes)}
        self.scup_history = {i: {dim: deque(maxlen=history_size) for dim in self.dimensions} for i in range(max_processes)}
        self.time_stamps = {i: deque(maxlen=history_size) for i in range(max_processes)}
        
        # Wave propagation state for each process
        self.wave_sources = {i: [] for i in range(max_processes)}  # [(row, col, intensity, time)]
        self.wave_decay = 0.85
        
        # Critical state detection
        self.critical_threshold = 0.8
        self.critical_cells = {i: set() for i in range(max_processes)}
        
        # Setup visualization
        self.setup_visualization()
        
        # Animation
        self.ani = None
        self.current_tick = 0
        
        # Setup GIF saver
        self.gif_saver = setup_gif_saver("scup_pressure_grid_visualizer")
        
        # Setup signal handlers for GIF saving
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        atexit.register(self.cleanup)
        
        logger.info(f"SCUPPressureGridVisualizer initialized for {max_processes} processes")
    
    def save_animation_gif(self):
        """Save the animation as GIF"""
        try:
            if hasattr(self, 'ani'):
                gif_path = self.gif_saver.save_animation_as_gif(self.ani, fps=5, dpi=100)
                if gif_path:
                    print(f"\nAnimation GIF saved: {gif_path}", file=sys.stderr)
                else:
                    print("\nFailed to save animation GIF", file=sys.stderr)
            else:
                print("\nNo animation to save", file=sys.stderr)
            print(f"\nError saving animation GIF: {e}", file=sys.stderr)

    def cleanup(self):
        """Cleanup function to save GIF"""
        self.save_animation_gif()

    def signal_handler(self, signum, frame):
        """Signal handler to save GIF on termination"""
        print(f"\nReceived signal {signum}, saving GIF...", file=sys.stderr)
        self.save_animation_gif()
        sys.exit(0)
    
    def setup_visualization(self):
        """Initialize matplotlib figure and components"""
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(20, 16), facecolor='#0a0a0a')
        
        # Create custom colormap (blue → yellow → red)
        colors = ['#001f3f', '#0074D9', '#39CCCC', '#3D9970', 
                  '#FFDC00', '#FF851B', '#FF4136', '#85144b']
        n_bins = 100
        self.cmap = LinearSegmentedColormap.from_list('pressure', colors, N=n_bins)
        
        # Calculate grid layout for multiple processes
        cols = min(4, self.max_processes)  # Max 4 columns
        rows = (self.max_processes + cols - 1) // cols  # Calculate needed rows
        
        # Create subplots for each process
        self.axes = []
        self.ims = []
        self.cell_texts = {i: [] for i in range(self.max_processes)}
        
        for i in range(self.max_processes):
            row = i // cols
            col = i % cols
            
            if i == 0:
                # Main grid (process 0) gets more space
                ax = plt.subplot2grid((rows, cols), (row, col), colspan=2, rowspan=2)
            else:
                ax = plt.subplot2grid((rows, cols), (row, col))
            
            self.axes.append(ax)
            self.setup_process_grid(ax, i)
        
        plt.tight_layout()
    
    def setup_process_grid(self, ax, process_id):
        """Initialize a SCUP pressure grid for a specific process"""
        ax.set_facecolor('#0a0a0a')
        
        # Initialize heatmap
        im = ax.imshow(self.pressure_matrix[process_id], cmap=self.cmap,
                       vmin=0, vmax=1, aspect='equal')
        self.ims.append(im)
        
        # Configure heatmap
        title = f'Process {process_id} SCUP Grid' if process_id > 0 else 'DAWN SCUP Pressure Grid'
        ax.set_title(title, fontsize=12 if process_id == 0 else 8, 
                    fontweight='bold', pad=10, color='white')
        
        # Set ticks and labels
        ax.set_xticks(range(4))
        ax.set_yticks(range(4))
        ax.set_xticklabels(self.short_dims, fontsize=10 if process_id == 0 else 6, fontweight='bold')
        ax.set_yticklabels(self.short_dims, fontsize=10 if process_id == 0 else 6, fontweight='bold')
        
        # Add grid lines
        for i in range(5):
            ax.axhline(i - 0.5, color='white', linewidth=1, alpha=0.3)
            ax.axvline(i - 0.5, color='white', linewidth=1, alpha=0.3)
        
        # Cell annotations
        row_texts = []
        for i in range(4):
            col_texts = []
            for j in range(4):
                if i == j:
                    # Diagonal cell - self pressure
                    text = ax.text(j, i, self.self_labels[i],
                                  ha='center', va='center',
                                  fontsize=8 if process_id == 0 else 6, fontweight='bold',
                                  color='white', alpha=0.8)
                else:
                    # Off-diagonal - interaction (only show for main process to avoid clutter)
                    if process_id == 0:
                        label = self.interaction_labels.get((i, j), '')
                        text = ax.text(j, i, label,
                                      ha='center', va='center',
                                      fontsize=6, color='white',
                                      alpha=0.7, rotation=0)
                    else:
                        text = ax.text(j, i, '',
                                      ha='center', va='center',
                                      fontsize=6, color='white',
                                      alpha=0.7)
                col_texts.append(text)
            row_texts.append(col_texts)
        self.cell_texts[process_id] = row_texts
        
        # Add metadata text
        metadata_text = ax.text(0.02, 0.02, '', fontsize=6 if process_id > 0 else 8,
                               color='gray', alpha=0.8, transform=ax.transAxes)
        ax.metadata_text = metadata_text
        
        # Critical state indicator
        critical_text = ax.text(0.5, 0.95, '', fontsize=8 if process_id == 0 else 6,
                               ha='center', color='#FF4136',
                               fontweight='bold', alpha=0, transform=ax.transAxes)
        ax.critical_text = critical_text
    
    def is_active(self) -> bool:
        """Check if visualizer is active"""
        return self._active
    
    def calculate_pressure_matrix(self, scup_values: Dict[str, Any], process_id: int = 0):
        """Calculate 4x4 pressure interaction matrix for a specific process"""
        # Extract individual dimension values
        dims = [scup_values.get(dim.lower(), 0.5) for dim in self.dimensions]
        
        # Apply temporal smoothing
        if len(self.pressure_history[process_id]) > 0:
            prev_matrix = self.pressure_history[process_id][-1]
            smooth_factor = self.smoothing
        else:
            prev_matrix = np.zeros((4, 4))
            smooth_factor = 0
        
        # Calculate new pressure matrix
        new_matrix = np.zeros((4, 4))
        
        for i in range(4):
            for j in range(4):
                if i == j:
                    # Self-pressure (diagonal)
                    # Higher values indicate more internal pressure
                    new_matrix[i, j] = dims[i] ** 1.5  # Amplify high values
                else:
                    # Interaction pressure (off-diagonal)
                    new_matrix[i, j] = self.interaction_fn(dims[i], dims[j])
        
        # Apply wave propagation effects
        wave_matrix = self.calculate_wave_effects(process_id)
        new_matrix = new_matrix * 0.8 + wave_matrix * 0.2
        
        # Apply temporal smoothing
        self.pressure_matrix[process_id] = (1 - smooth_factor) * new_matrix + smooth_factor * prev_matrix
        
        # Detect critical states
        self.detect_critical_states(process_id)
        
        # Update history
        self.pressure_history[process_id].append(self.pressure_matrix[process_id].copy())
        self.time_stamps[process_id].append(time.time())
        
        # Update dimension histories
        for i, dim in enumerate(self.dimensions):
            self.scup_history[process_id][dim].append(dims[i])
    
    def calculate_wave_effects(self, process_id: int) -> np.ndarray:
        """Calculate pressure wave propagation effects for a specific process"""
        wave_matrix = np.zeros((4, 4))
        
        # Process active waves
        current_time = time.time()
        active_waves = []
        
        for row, col, intensity, start_time in self.wave_sources[process_id]:
            age = current_time - start_time
            if age < 2.0:  # Wave lifetime
                # Calculate wave spread
                decay = self.wave_decay ** age
                radius = age * 2  # Wave speed
                
                # Apply wave to nearby cells
                for i in range(4):
                    for j in range(4):
                        distance = np.sqrt((i - row)**2 + (j - col)**2)
                        if distance <= radius:
                            wave_intensity = intensity * decay * (1 - distance/radius)
                            wave_matrix[i, j] = max(wave_matrix[i, j], wave_intensity)
                active_waves.append((row, col, intensity, start_time))
        
        self.wave_sources[process_id] = active_waves
        return wave_matrix
    
    def detect_critical_states(self, process_id: int):
        """Detect critical pressure states for a specific process"""
        self.critical_cells[process_id].clear()
        
        for i in range(4):
            for j in range(4):
                if self.pressure_matrix[process_id][i, j] > self.critical_threshold:
                    self.critical_cells[process_id].add((i, j))
                    
                    # Trigger wave if new critical state
                    if len(self.wave_sources[process_id]) < 3:  # Limit concurrent waves
                        self.wave_sources[process_id].append((i, j, 0.8, time.time()))
    
    def update_visualization(self, process_data: Dict[str, Any], process_id: int = 0, tick: int = 0) -> None:
        """Update visualization for a specific process"""
        try:
            # Extract SCUP data
            scup_data = process_data.get('scup', {})
            scup_values = {
                'schema': scup_data.get('schema', 0.5),
                'coherence': scup_data.get('coherence', 0.5),
                'utility': scup_data.get('utility', 0.5),
                'pressure': scup_data.get('pressure', 0.5)
            }
            
            # Calculate pressure matrix
            self.calculate_pressure_matrix(scup_values, process_id)
            
            # Update heatmap
            if process_id < len(self.ims):
                self.ims[process_id].set_array(self.pressure_matrix[process_id])
                
                # Update cell colors based on intensity
                for i in range(4):
                    for j in range(4):
                        intensity = self.pressure_matrix[process_id][i, j]
                        text = self.cell_texts[process_id][i][j]
                        
                        # Adjust text color for readability
                        if intensity > 0.6:
                            text.set_color('black')
                        else:
                            text.set_color('white')
                        
                        # Highlight critical cells
                        if (i, j) in self.critical_cells[process_id]:
                            text.set_fontweight('bold')
                            text.set_fontsize(10 if i == j else 8)
                        else:
                            text.set_fontweight('normal')
                            text.set_fontsize(8 if i == j else 6)
            
            self.current_tick = tick
            
            logger.error(f"Error updating visualization for process {process_id}: {e}")
    
    def update_all_processes(self, all_process_data: Dict[int, Dict[str, Any]], tick: int) -> None:
        """Update visualization for all processes"""
        for process_id, process_data in all_process_data.items():
            if process_id < self.max_processes:
                self.update_visualization(process_data, process_id, tick)
    
    def get_visualization_data(self) -> Dict[str, Any]:
        """Get current visualization data"""
        return {
            'pressure_matrices': {pid: matrix.tolist() for pid, matrix in self.pressure_matrix.items()},
            'critical_cells': {pid: list(cells) for pid, cells in self.critical_cells.items()},
            'current_tick': self.current_tick,
            'interaction_model': self.interaction_model_name,
            'smoothing': self.smoothing
        }
    
    def start_animation(self) -> None:
        """Start the animation"""
        if self.ani is None:
            self.ani = animation.FuncAnimation(frames=1000, 
                self.fig, self._animation_frame,
                interval=100,  # 10 FPS
                blit=False,
                cache_frame_data=False
            )
    
    def _animation_frame(self, frame) -> None:
        """Animation frame update function"""
        # This can be overridden for custom animation logic
        pass
    
    def stop_animation(self) -> None:
        """Stop the animation"""
        if self.ani:
            self.ani.event_source.stop()
            self.ani = None
    
    def show(self) -> None:
        """Show the visualization"""
        plt.show()
    
    def close(self) -> None:
        """Close the visualization"""
        self.stop_animation()
        plt.close(self.fig)
        self._active = False
    
    async def shutdown(self) -> None:
        """Async shutdown method"""
        self.close()
        logger.info("SCUPPressureGridVisualizer shutdown complete")

def get_scup_pressure_grid() -> SCUPPressureGridVisualizer:
    return SCUPPressureGridVisualizer()