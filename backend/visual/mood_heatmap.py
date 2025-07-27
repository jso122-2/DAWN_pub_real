"""
Mood Heatmap Visualizer
Visualizes the emotional state distribution as a heatmap
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Optional, List, Tuple
from .base_visualizer import BaseVisualizer

class MoodHeatmapVisualizer(BaseVisualizer):
    def __init__(self):
        super().__init__()
        self.fig = None
        self.ax = None
        self.im = None
        self.data_buffer: List[Dict[str, float]] = []
        self.max_samples = 100
        self.emotions = ['Joy', 'Sadness', 'Anger', 'Fear', 'Surprise', 'Disgust']
        self.activities = ['Processing', 'Learning', 'Memory', 'Attention', 'Creativity']
        
    def start(self):
        """Initialize the visualization"""
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.ax.set_title('Emotional State Heatmap')
        self.ax.set_xlabel('Emotion')
        self.ax.set_ylabel('Activity')
        
    def update(self, data: Dict):
        """Update the visualization with new data"""
        if 'mood_state' not in data:
            return
            
        mood_state = data['mood_state']
        self.data_buffer.append(mood_state)
        
        # Keep buffer size limited
        if len(self.data_buffer) > self.max_samples:
            self.data_buffer = self.data_buffer[-self.max_samples:]
            
        # Create heatmap data
        heatmap_data = np.zeros((len(self.activities), len(self.emotions)))
        for i, activity in enumerate(self.activities):
            for j, emotion in enumerate(self.emotions):
                if emotion in mood_state and activity in mood_state[emotion]:
                    heatmap_data[i, j] = mood_state[emotion][activity]
                    
        # Update heatmap
        if self.ax is not None:
            self.ax.clear()
            self.im = self.ax.imshow(heatmap_data, cmap='RdYlBu_r', aspect='auto')
            
            # Add colorbar
            plt.colorbar(self.im, ax=self.ax, label='Intensity')
            
            # Set labels
            self.ax.set_xticks(np.arange(len(self.emotions)))
            self.ax.set_yticks(np.arange(len(self.activities)))
            self.ax.set_xticklabels(self.emotions)
            self.ax.set_yticklabels(self.activities)
            
            # Rotate x-axis labels
            plt.setp(self.ax.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')
            
            # Add title and adjust layout
            self.ax.set_title('Emotional State Heatmap')
            self.fig.tight_layout()
            
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            
    def render(self) -> Optional[Dict]:
        """Return the current state of the visualization"""
        if not self.data_buffer:
            return None
            
        return {
            'type': 'mood_heatmap',
            'data': {
                'current_state': self.data_buffer[-1],
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
            self.im = None
        self.data_buffer = []

if __name__ == "__main__":
    visualizer = MoodHeatmapVisualizer()
    visualizer.run() 