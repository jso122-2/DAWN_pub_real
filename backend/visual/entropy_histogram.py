"""
Entropy Histogram Visualizer
Visualizes the distribution of entropy values in the system
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Optional
from ...base_visualizer import BaseVisualizer

class EntropyHistogramVisualizer(BaseVisualizer):
    def __init__(self):
        super().__init__()
        self.fig = None
        self.ax = None
        self.bars = None
        self.data_buffer = []
        self.max_samples = 1000
        self.num_bins = 20
        
    def start(self):
        """Initialize the visualization"""
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_title('Entropy Distribution')
        self.ax.set_xlabel('Entropy Value')
        self.ax.set_ylabel('Frequency')
        self.ax.grid(True, alpha=0.3)
        
    def update(self, data: Dict):
        """Update the visualization with new data"""
        if 'entropy' not in data:
            return
            
        entropy = data['entropy']
        self.data_buffer.append(entropy)
        
        # Keep buffer size limited
        if len(self.data_buffer) > self.max_samples:
            self.data_buffer = self.data_buffer[-self.max_samples:]
            
        # Update histogram
        if self.ax is not None:
            self.ax.clear()
            self.ax.hist(self.data_buffer, bins=self.num_bins, alpha=0.7, color='blue')
            self.ax.set_title('Entropy Distribution')
            self.ax.set_xlabel('Entropy Value')
            self.ax.set_ylabel('Frequency')
            self.ax.grid(True, alpha=0.3)
            
            # Add mean and std dev lines
            mean_val = np.mean(self.data_buffer)
            std_val = np.std(self.data_buffer)
            self.ax.axvline(mean_val, color='red', linestyle='--', alpha=0.7, label=f'Mean: {mean_val:.2f}')
            self.ax.axvline(mean_val + std_val, color='green', linestyle=':', alpha=0.7, label=f'±1σ: {std_val:.2f}')
            self.ax.axvline(mean_val - std_val, color='green', linestyle=':', alpha=0.7)
            self.ax.legend()
            
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            
    def render(self) -> Optional[Dict]:
        """Return the current state of the visualization"""
        if not self.data_buffer:
            return None
            
        return {
            'type': 'entropy_histogram',
            'data': {
                'values': self.data_buffer,
                'mean': float(np.mean(self.data_buffer)),
                'std': float(np.std(self.data_buffer)),
                'timestamp': self.timestamp
            }
        }
        
    def cleanup(self):
        """Clean up resources"""
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None
            self.ax = None
            self.bars = None
        self.data_buffer = [] 