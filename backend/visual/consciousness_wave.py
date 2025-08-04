"""
Consciousness Wave Visualizer
Visualizes the wave-like patterns of consciousness states
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Optional
from ...base_visualizer import BaseVisualizer
import time

class ConsciousnessWaveVisualizer(BaseVisualizer):
    def __init__(self, frequency: float = 1.0, amplitude: float = 1.0, wave_type: str = 'sine'):
        super().__init__()
        self.fig = None
        self.ax = None
        self.line = None
        self.data_buffer = []
        self.max_points = 1000
        
        # Wave parameters
        self.frequency = frequency
        self.amplitude = amplitude
        self.wave_type = wave_type
        self.phase = 0.0
        
        # Live stream parameters
        self._stream_active = False
        self._data_source = None
        
    def start(self):
        """Initialize the visualization"""
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_title('Consciousness Wave Pattern')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Amplitude')
        self.ax.grid(True)
        self.line, = self.ax.plot([], [], 'b-', alpha=0.7)
        plt.ion()  # Enable interactive mode
        
    def update(self, data: Dict):
        """Update the visualization with new data"""
        if 'consciousness_state' not in data:
            return
            
        state = data['consciousness_state']
        self.data_buffer.append(state)
        
        # Keep buffer size limited
        if len(self.data_buffer) > self.max_points:
            self.data_buffer = self.data_buffer[-self.max_points:]
            
        # Update plot
        if self.line is not None:
            x = np.arange(len(self.data_buffer))
            self.line.set_data(x, self.data_buffer)
            self.ax.relim()
            self.ax.autoscale_view()
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            
    def render(self) -> Optional[Dict]:
        """Return the current state of the visualization"""
        if not self.data_buffer:
            return None
            
        return {
            'type': 'consciousness_wave',
            'data': {
                'values': self.data_buffer,
                'timestamp': self.timestamp
            }
        }
        
    def cleanup(self):
        """Clean up resources"""
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None
            self.ax = None
            self.line = None
        self.data_buffer = []

    def generate(self, data: Dict) -> Optional[Dict]:
        """Generate visualization data from input data.
        
        Args:
            data: Dictionary containing visualization input data
            
        Returns:
            Dictionary containing generated visualization data or None if no data
        """
        if 'consciousness_state' not in data:
            return None
            
        state = data['consciousness_state']
        self.data_buffer.append(state)
        
        # Keep buffer size limited
        if len(self.data_buffer) > self.max_points:
            self.data_buffer = self.data_buffer[-self.max_points:]
            
        return {
            'type': 'consciousness_wave',
            'data': {
                'values': self.data_buffer,
                'timestamp': time.time()
            }
        }

    def start_live_stream(self, data_source=None):
        """Start live streaming of consciousness wave data.
        
        Args:
            data_source: Optional callable that returns wave parameters dict
                        Expected format: {'frequency': float, 'amplitude': float, 'phase': float}
        """
        if self._stream_active:
            return
            
        self._stream_active = True
        self._data_source = data_source
        
        # Initialize visualization
        self.start()
        
        # Start update loop
        def update_loop():
            while self._stream_active:

                    # Get current parameters from data source if provided
                    if self._data_source:
                        params = self._data_source()
                        if isinstance(params, dict):
                            self.frequency = params.get('frequency', self.frequency)
                            self.amplitude = params.get('amplitude', self.amplitude)
                            self.phase = params.get('phase', self.phase)
                    
                    # Generate and update wave data
                    t = np.linspace(0, 2*np.pi, 100)
                    wave = self.amplitude * np.sin(self.frequency * t + self.phase)
                    
                    # Update visualization
                    if self.line is not None:
                        self.line.set_data(t, wave)
                        self.ax.relim()
                        self.ax.autoscale_view()
                        self.fig.canvas.draw()
                        self.fig.canvas.flush_events()
                    
                    time.sleep(0.1)  # Update every 100ms
                    
                    print(f"Error in consciousness wave update: {e}")
                    time.sleep(1)  # Wait before retrying
        
        # Start update thread
        import threading
        self._update_thread = threading.Thread(target=update_loop, daemon=True)
        self._update_thread.start()
        
    def stop_live_stream(self):
        """Stop the live streaming of consciousness wave data."""
        self._stream_active = False
        if hasattr(self, '_update_thread'):
            self._update_thread.join(timeout=1.0)
        self.cleanup() 