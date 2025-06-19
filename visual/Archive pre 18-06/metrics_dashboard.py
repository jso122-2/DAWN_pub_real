"""
Metrics Dashboard - Visual display of system metrics
"""

import logging
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
import time
import json
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MetricState:
    """Current state of metrics visualization"""
    scup_values: List[float] = None
    drift_values: List[float] = None
    mood_values: List[float] = None
    timestamps: List[float] = None
    last_update: float = 0.0
    
    def __post_init__(self):
        if self.scup_values is None:
            self.scup_values = []
        if self.drift_values is None:
            self.drift_values = []
        if self.mood_values is None:
            self.mood_values = []
        if self.timestamps is None:
            self.timestamps = []

class MetricsDashboard:
    """Visual dashboard for system metrics"""
    
    def __init__(self, window_size: int = 100):
        """Initialize metrics dashboard"""
        self._state = MetricState()
        self._window_size = window_size
        self._fig = None
        self._ax = None
        self._ani = None
        self._initialize()
        logger.info("Initialized MetricsDashboard")
        
    def _initialize(self) -> None:
        """Initialize visualization components"""
        try:
            # Create figure and axis
            self._fig, self._ax = plt.subplots(figsize=(12, 6))
            self._fig.suptitle("DAWN System Metrics", fontsize=16)
            
            # Initialize with non-zero values
            self._state.scup_values = [0.5] * self._window_size
            self._state.drift_values = [0.1] * self._window_size
            self._state.mood_values = [0.5] * self._window_size
            self._state.timestamps = list(range(self._window_size))
            
        except Exception as e:
            logger.error(f"Error initializing dashboard: {e}")
            
    def display_tick(self, data: Dict[str, float]) -> None:
        """Update and display metrics for current tick"""
        try:
            # Update state
            self._state.scup_values.append(data.get('scup', 0.5))
            self._state.drift_values.append(data.get('drift', 0.1))
            self._state.mood_values.append(data.get('mood', 0.5))
            self._state.timestamps.append(time.time())
            
            # Trim to window size
            if len(self._state.scup_values) > self._window_size:
                self._state.scup_values = self._state.scup_values[-self._window_size:]
                self._state.drift_values = self._state.drift_values[-self._window_size:]
                self._state.mood_values = self._state.mood_values[-self._window_size:]
                self._state.timestamps = self._state.timestamps[-self._window_size:]
                
            # Update plot
            self._update_plot()
            
        except Exception as e:
            logger.error(f"Error displaying tick: {e}")
            
    def _update_plot(self) -> None:
        """Update the metrics plot"""
        try:
            self._ax.clear()
            
            # Plot metrics
            self._ax.plot(self._state.timestamps, self._state.scup_values, 
                         label='SCUP', color='blue')
            self._ax.plot(self._state.timestamps, self._state.drift_values, 
                         label='Alignment Drift', color='red')
            self._ax.plot(self._state.timestamps, self._state.mood_values, 
                         label='Schema Mood', color='green')
            
            # Configure plot
            self._ax.set_ylim(0, 1)
            self._ax.set_xlabel('Time')
            self._ax.set_ylabel('Value')
            self._ax.legend()
            self._ax.grid(True)
            
            # Add current values as text
            self._ax.text(0.02, 0.98, 
                         f"SCUP: {self._state.scup_values[-1]:.3f}\n"
                         f"Drift: {self._state.drift_values[-1]:.3f}\n"
                         f"Mood: {self._state.mood_values[-1]:.3f}",
                         transform=self._ax.transAxes,
                         verticalalignment='top',
                         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            plt.draw()
            plt.pause(0.001)
            
        except Exception as e:
            logger.error(f"Error updating plot: {e}")
            
    def start_animation(self, interval: int = 1000) -> None:
        """Start animated display"""
        try:
            def update(frame):
                self._update_plot()
                return self._ax.lines
                
            self._ani = FuncAnimation(self._fig, update, interval=interval)
            plt.show()
            
        except Exception as e:
            logger.error(f"Error starting animation: {e}")
            
    def stop_animation(self) -> None:
        """Stop animated display"""
        try:
            if self._ani:
                self._ani.event_source.stop()
                plt.close(self._fig)
        except Exception as e:
            logger.error(f"Error stopping animation: {e}")

# Global instance
_metrics_dashboard = MetricsDashboard()

def display_tick(data: Dict[str, float]) -> None:
    """Display metrics for current tick on global dashboard"""
    _metrics_dashboard.display_tick(data)
    
def start_dashboard(interval: int = 1000) -> None:
    """Start metrics dashboard animation"""
    _metrics_dashboard.start_animation(interval)
    
def stop_dashboard() -> None:
    """Stop metrics dashboard animation"""
    _metrics_dashboard.stop_animation()

# Export key functions
__all__ = [
    'MetricsDashboard',
    'MetricState',
    'display_tick',
    'start_dashboard',
    'stop_dashboard'
] 