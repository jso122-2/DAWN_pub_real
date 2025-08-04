"""
Metrics Radar Visualizer
Visualizes system metrics in a radar/spider chart format
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Optional, List
from ...base_visualizer import BaseVisualizer

class MetricsRadarVisualizer(BaseVisualizer):
    def __init__(self):
        super().__init__()
        self.fig = None
        self.ax = None
        self.data_buffer: List[Dict[str, float]] = []
        self.max_samples = 100
        self.metrics = [
            'Accuracy',
            'Precision',
            'Recall',
            'F1 Score',
            'Latency',
            'Throughput',
            'Memory Usage',
            'CPU Usage'
        ]
        
    def start(self):
        """Initialize the visualization"""
        self.fig, self.ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        self.ax.set_title('System Metrics Radar')
        
    def update(self, data: Dict):
        """Update the visualization with new data"""
        if 'metrics' not in data:
            return
            
        metrics = data['metrics']
        self.data_buffer.append(metrics)
        
        # Keep buffer size limited
        if len(self.data_buffer) > self.max_samples:
            self.data_buffer = self.data_buffer[-self.max_samples:]
            
        # Update radar chart
        if self.ax is not None:
            self.ax.clear()
            
            # Get current metrics
            current_metrics = self.data_buffer[-1]
            
            # Prepare data for radar chart
            values = []
            for metric in self.metrics:
                values.append(current_metrics.get(metric, 0))
                
            # Convert to numpy array
            values = np.array(values)
            
            # Number of variables
            N = len(self.metrics)
            
            # Compute angle for each axis
            angles = [n / float(N) * 2 * np.pi for n in range(N)]
            angles += angles[:1]  # Close the loop
            
            # Add the first value again to close the loop
            values = np.concatenate((values, [values[0]]))
            
            # Plot data
            self.ax.plot(angles, values, linewidth=2, linestyle='solid')
            self.ax.fill(angles, values, alpha=0.4)
            
            # Set labels
            self.ax.set_xticks(angles[:-1])
            self.ax.set_xticklabels(self.metrics)
            
            # Add grid
            self.ax.grid(True)
            
            # Set title
            self.ax.set_title('System Metrics Radar')
            
            # Add value labels
            for i, value in enumerate(values[:-1]):
                angle = angles[i]
                self.ax.text(
                    angle,
                    value,
                    f'{value:.2f}',
                    ha='center',
                    va='center',
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
            'type': 'metrics_radar',
            'data': {
                'current_metrics': self.data_buffer[-1],
                'history': self.data_buffer,
                'timestamp': self.timestamp
            }
        }
        
    def cleanup(self):
        """Clean up resources"""
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None
            self.ax = None
        self.data_buffer = [] 