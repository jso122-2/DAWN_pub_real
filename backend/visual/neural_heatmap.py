"""
Neural Heatmap Visualizer
Visualizes neural network activation patterns as a heatmap
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Optional, List
from ...base_visualizer import BaseVisualizer

class NeuralHeatmapVisualizer(BaseVisualizer):
    def __init__(self):
        super().__init__()
        self.fig = None
        self.ax = None
        self.im = None
        self.data_buffer: List[np.ndarray] = []
        self.max_samples = 100
        self.grid_size = (32, 32)  # Default grid size
        
    def start(self):
        """Initialize the visualization"""
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.ax.set_title('Neural Activation Heatmap')
        
    def update(self, data: Dict):
        """Update the visualization with new data"""
        if 'neural_activations' not in data:
            return
            
        activations = data['neural_activations']
        
        # Convert to numpy array if not already
        if not isinstance(activations, np.ndarray):
            activations = np.array(activations)
            
        # Reshape if needed
        if activations.ndim == 1:
            activations = activations.reshape(self.grid_size)
            
        self.data_buffer.append(activations)
        
        # Keep buffer size limited
        if len(self.data_buffer) > self.max_samples:
            self.data_buffer = self.data_buffer[-self.max_samples:]
            
        # Update heatmap
        if self.ax is not None:
            self.ax.clear()
            
            # Use the most recent activation pattern
            current_activation = self.data_buffer[-1]
            
            # Create heatmap
            self.im = self.ax.imshow(
                current_activation,
                cmap='viridis',
                interpolation='nearest',
                aspect='auto'
            )
            
            # Add colorbar
            plt.colorbar(self.im, ax=self.ax, label='Activation Strength')
            
            # Add title and remove axes
            self.ax.set_title('Neural Activation Heatmap')
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            
            # Add activation statistics
            mean_act = np.mean(current_activation)
            max_act = np.max(current_activation)
            self.ax.text(
                0.02, 0.98,
                f'Mean: {mean_act:.3f}\nMax: {max_act:.3f}',
                transform=self.ax.transAxes,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
            )
            
            self.fig.tight_layout()
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            
    def render(self) -> Optional[Dict]:
        """Return the current state of the visualization"""
        if not self.data_buffer:
            return None
            
        return {
            'type': 'neural_heatmap',
            'data': {
                'current_activation': self.data_buffer[-1].tolist(),
                'mean_activation': float(np.mean(self.data_buffer[-1])),
                'max_activation': float(np.max(self.data_buffer[-1])),
                'timestamp': self.timestamp
            }
        }
        
    def cleanup(self):
        """Clean up resources"""
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None
            self.ax = None
            self.im = None
        self.data_buffer = [] 