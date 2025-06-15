"""
Process Timeline Visualizer
Visualizes the timeline of different processes and their states
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Optional, List
from .base_visualizer import BaseVisualizer

class ProcessTimelineVisualizer(BaseVisualizer):
    def __init__(self):
        super().__init__()
        self.fig = None
        self.ax = None
        self.data_buffer: List[Dict] = []
        self.max_samples = 100
        self.process_colors = {
            'neural': 'blue',
            'consciousness': 'green',
            'memory': 'red',
            'attention': 'purple',
            'learning': 'orange'
        }
        
    def start(self):
        """Initialize the visualization"""
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.ax.set_title('Process Timeline')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Process State')
        self.ax.grid(True, alpha=0.3)
        
    def update(self, data: Dict):
        """Update the visualization with new data"""
        if 'process_states' not in data:
            return
            
        process_states = data['process_states']
        self.data_buffer.append(process_states)
        
        # Keep buffer size limited
        if len(self.data_buffer) > self.max_samples:
            self.data_buffer = self.data_buffer[-self.max_samples:]
            
        # Update timeline
        if self.ax is not None:
            self.ax.clear()
            
            # Plot each process
            for process_name, color in self.process_colors.items():
                if process_name in process_states:
                    values = [state.get(process_name, 0) for state in self.data_buffer]
                    times = np.arange(len(values))
                    self.ax.plot(times, values, color=color, label=process_name, alpha=0.7)
                    
            # Add legend and labels
            self.ax.legend(loc='upper right')
            self.ax.set_title('Process Timeline')
            self.ax.set_xlabel('Time')
            self.ax.set_ylabel('Process State')
            self.ax.grid(True, alpha=0.3)
            
            # Set y-axis limits
            self.ax.set_ylim(-0.1, 1.1)
            
            self.fig.tight_layout()
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            
    def render(self) -> Optional[Dict]:
        """Return the current state of the visualization"""
        if not self.data_buffer:
            return None
            
        return {
            'type': 'process_timeline',
            'data': {
                'current_states': self.data_buffer[-1],
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