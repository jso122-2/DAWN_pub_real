"""
Drift Vector Field Visualizer for DAWN
"""

from .base_visualizer import BaseVisualizer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import logging

logger = logging.getLogger(__name__)

class DriftVectorFieldRenderer(BaseVisualizer):
    def __init__(self):
        super().__init__(name="DriftVectorFieldRenderer")
        self.fig = None
        self.ax = None
        self.quiver = None
        self.grid_size = 20
        self.field_data = None
        
    def update(self, data: dict) -> None:
        """Update the vector field with new data"""
        if not self.is_active:
            return
            
        try:
            # Extract drift vectors from data
            if 'drift_vectors' in data:
                self.field_data = data['drift_vectors']
            elif 'vector_field' in data:
                self.field_data = data['vector_field']
            else:
                # Generate synthetic data if none provided
                x = np.linspace(-2, 2, self.grid_size)
                y = np.linspace(-2, 2, self.grid_size)
                X, Y = np.meshgrid(x, y)
                U = -Y  # Example: circular flow
                V = X
                self.field_data = {'X': X, 'Y': Y, 'U': U, 'V': V}
            
            self.render()
            
        except Exception as e:
            logger.error(f"Error updating drift vector field: {e}")
    
    def render(self) -> None:
        """Render the current vector field state"""
        if not self.is_active or self.field_data is None:
            return
            
        try:
            if self.fig is None:
                self.fig, self.ax = plt.subplots(figsize=(8, 8))
                self.ax.set_title("DAWN Drift Vector Field")
                self.ax.set_xlabel("X")
                self.ax.set_ylabel("Y")
            
            # Clear previous quiver plot
            if self.quiver is not None:
                self.quiver.remove()
            
            # Create new quiver plot
            self.quiver = self.ax.quiver(
                self.field_data['X'],
                self.field_data['Y'],
                self.field_data['U'],
                self.field_data['V'],
                scale=50,
                color='cyan',
                alpha=0.6
            )
            
            plt.draw()
            plt.pause(0.001)
            
        except Exception as e:
            logger.error(f"Error rendering drift vector field: {e}")
    
    def cleanup(self) -> None:
        """Clean up resources"""
        if self.fig is not None:
            plt.close(self.fig)
        super().cleanup() 