#!/usr/bin/env python3
"""
DAWN Backend Mood State Visualizer
Integrated version for backend tick engine
"""

import json
import os
import os
import os
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import asyncio
import logging
from collections import deque
from typing import Dict, Any, Optional
from datetime import datetime
import signal
import atexit
import sys

# Import GIF saver

    from .gif_saver import setup_gif_saver
    from gif_saver import setup_gif_saver
import signal
import atexit

# Import GIF saver

    from .gif_saver import setup_gif_saver
    from gif_saver import setup_gif_saver

logger = logging.getLogger(__name__)

class MoodStateVisualizer:
    """Backend-integrated mood state visualizer for DAWN"""
    
    def __init__(self, buffer_size=100, update_interval=100):
        self.buffer_size = buffer_size
        self.update_interval = update_interval
        self._active = True
        
        # Mood state buffer for temporal smoothing
        self.mood_history = deque(maxlen=buffer_size)
        
        # Define emotional landscape dimensions (8x8 grid)
        self.mood_dimensions = [
            ['Transcendent', 'Luminous', 'Expansive', 'Crystalline', 'Ethereal', 'Radiant', 'Sublime', 'Infinite'],
            ['Ecstatic', 'Euphoric', 'Jubilant', 'Vivacious', 'Exuberant', 'Buoyant', 'Elated', 'Rapturous'],
            ['Serene', 'Peaceful', 'Harmonious', 'Balanced', 'Centered', 'Tranquil', 'Calm', 'Composed'],
            ['Curious', 'Inquisitive', 'Wonder', 'Fascinated', 'Intrigued', 'Exploratory', 'Seeking', 'Questioning'],
            ['Focused', 'Attentive', 'Concentrated', 'Sharp', 'Alert', 'Vigilant', 'Acute', 'Precise'],
            ['Contemplative', 'Reflective', 'Meditative', 'Pensive', 'Introspective', 'Thoughtful', 'Deep', 'Brooding'],
            ['Uncertain', 'Hesitant', 'Ambiguous', 'Doubtful', 'Questioning', 'Unsure', 'Wavering', 'Conflicted'],
            ['Turbulent', 'Chaotic', 'Fragmented', 'Unstable', 'Volatile', 'Scattered', 'Dissonant', 'Entropic']
        ]
        
        # Initialize mood state matrix
        self.mood_matrix = np.zeros((8, 8))
        self.mood_smoothed = np.zeros((8, 8))
        
        # Create custom colormap for emotional landscape
        colors = ['#0a0a0a', '#1a1a2e', '#16213e', '#0f3460', '#533483', 
                 '#7209b7', '#a663cc', '#4cc9f0', '#7209b7', '#f72585']
        self.mood_cmap = LinearSegmentedColormap.from_list('mood', colors, N=256)
        
        # Setup matplotlib
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        self.fig.patch.set_facecolor('#0a0a0a')
        
        # Initialize heatmap
        self.im = self.ax.imshow(self.mood_matrix, cmap=self.mood_cmap, 
                                aspect='equal', vmin=0, vmax=1, animated=True)
        
        # Setup axis labels with emotional dimensions
        self.ax.set_xticks(range(8))
        self.ax.set_yticks(range(8))
        self.ax.set_xticklabels([row[0][:8] for row in self.mood_dimensions], 
                               rotation=45, ha='right', fontsize=9, color='#cccccc')
        self.ax.set_yticklabels([f"{i+1}" for i in range(8)], 
                               fontsize=9, color='#cccccc')
        
        # Add detailed labels for each cell
        self.text_annotations = []
        for i in range(8):
            row_annotations = []
            for j in range(8):
                text = self.ax.text(j, i, self.mood_dimensions[i][j][:6], 
                                   ha='center', va='center', fontsize=7, 
                                   color='white', weight='bold')
                row_annotations.append(text)
            self.text_annotations.append(row_annotations)
        
        # Styling
        self.ax.set_title('DAWN Emotional Landscape\nMood State Heatmap', 
                         fontsize=16, color='#ffffff', pad=20, weight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(self.im, ax=self.ax, shrink=0.8)
        cbar.set_label('Affective Intensity', rotation=270, labelpad=20, 
                      color='#cccccc', fontsize=12)
        cbar.ax.tick_params(colors='#cccccc')
        
        # Add info text
        self.info_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes, 
                                     fontsize=10, color='#00ff88', verticalalignment='top',
                                     fontfamily='monospace')
        
        plt.tight_layout()
        
        # Animation
        self.ani = None
        self.current_tick = 0
        
        # Setup GIF saver
        self.gif_saver = setup_gif_saver("mood_state_visualizer")
        
        # Setup signal handlers for GIF saving
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        atexit.register(self.cleanup)
        
        logger.info("MoodStateVisualizer initialized")
    
    def save_animation_gif(self):
        """Save the animation as GIF"""

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
    
    def is_active(self) -> bool:
        """Check if visualizer is active"""
        return self._active
    
    def parse_mood_data(self, mood_data: Dict[str, Any], tick: int = 0) -> np.ndarray:
        """Extract and process mood state from DAWN mood data"""

            base_intensity = mood_data.get('base_level', 0.1)
            emotional_vector = mood_data.get('vector', [0.5, 0.5, 0.5, 0.5])
            
            # Generate mood matrix based on emotional dimensions
            mood_matrix = np.random.random((8, 8)) * 0.1  # Base noise
            
            # Apply emotional vector influences
            if len(emotional_vector) >= 4:
                # Map emotional dimensions to grid regions
                mood_matrix[0:2, :] += emotional_vector[0] * 0.8  # Transcendent/Ecstatic
                mood_matrix[2:4, :] += emotional_vector[1] * 0.6  # Serene/Curious  
                mood_matrix[4:6, :] += emotional_vector[2] * 0.7  # Focused/Contemplative
                mood_matrix[6:8, :] += emotional_vector[3] * 0.5  # Uncertain/Turbulent
                
            # Add temporal patterns
            wave_pattern = np.sin(tick * 0.1) * 0.2
            mood_matrix += wave_pattern
            
            # Apply base intensity scaling
            mood_matrix *= (base_intensity + 0.2)
            
            # Clamp values
            mood_matrix = np.clip(mood_matrix, 0, 1)
            
            return mood_matrix
            
            logger.error(f"Error parsing mood data: {e}")
            return self.mood_matrix
    
    def smooth_mood_transition(self, new_mood: np.ndarray, alpha: float = 0.3) -> np.ndarray:
        """Apply temporal smoothing to mood transitions"""
        self.mood_smoothed = alpha * new_mood + (1 - alpha) * self.mood_smoothed
        return self.mood_smoothed
    
    def update_visualization(self, mood_data: Dict[str, Any], tick: int) -> None:
        """Update the visualization with new mood data"""

            # Update mood state
            new_mood = self.parse_mood_data(mood_data, tick)
            self.mood_matrix = self.smooth_mood_transition(new_mood)
            
            # Store in history
            self.mood_history.append(self.mood_matrix.copy())
            
            # Update heatmap
            self.im.set_array(self.mood_matrix)
            
            # Update info display
            base_level = mood_data.get('base_level', 0)
            info_text = f"Tick: {tick:06d}\nBase Affect: {base_level:.3f}\nEmotional Flux: {np.std(self.mood_matrix):.3f}"
            self.info_text.set_text(info_text)
            
            # Update text annotations with intensity-based opacity
            for i in range(8):
                for j in range(8):
                    intensity = self.mood_matrix[i, j]
                    alpha = 0.4 + 0.6 * intensity  # Scale opacity with intensity
                    self.text_annotations[i][j].set_alpha(alpha)
            
            # Redraw
            self.fig.canvas.draw_idle()
            self.fig.canvas.flush_events()
            
            logger.error(f"Update error: {e}")
    
    def get_visualization_data(self) -> Dict[str, Any]:
        """Get current visualization data for API/WebSocket transmission"""
        return {
            'mood_matrix': self.mood_matrix.tolist(),
            'current_tick': self.current_tick,
            'base_level': np.mean(self.mood_matrix),
            'emotional_flux': np.std(self.mood_matrix),
            'timestamp': datetime.now().isoformat()
        }
    
    def start_animation(self) -> None:
        """Start the animation loop"""
        if self.ani is None:
            self.ani = animation.FuncAnimation(frames=1000, 
                self.fig, 
                lambda frame: self._animation_frame(frame), 
                interval=self.update_interval, 
                blit=False, 
                cache_frame_data=False
            )
            logger.info("Mood state animation started")
    
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
            logger.info("Mood state animation stopped")
    
    def show(self) -> None:
        """Show the visualization window"""
        plt.show()
    
    def close(self) -> None:
        """Close the visualization"""
        if self.fig:
            plt.close(self.fig)
        self._active = False
        logger.info("Mood state visualizer closed")
    
    async def shutdown(self) -> None:
        """Async shutdown"""
        self.close()

# Global instance for backend integration
_mood_visualizer = None

def get_mood_visualizer() -> MoodStateVisualizer:
    """Get or create the global mood visualizer instance"""
    global _mood_visualizer
    if _mood_visualizer is None:
        _mood_visualizer = MoodStateVisualizer()
    return _mood_visualizer