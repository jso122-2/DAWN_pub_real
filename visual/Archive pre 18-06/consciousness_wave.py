#!/usr/bin/env python3
"""
consciousness_wave.py - Consciousness Wave Visualizer for DAWN

This module provides visualization capabilities for consciousness waves,
allowing real-time monitoring of consciousness patterns through various
waveform representations.

Place this file at: Tick_engine/visual/consciousness_wave.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import time
import threading
import queue
from typing import Optional, Tuple, Callable, Dict, Any
from dataclasses import dataclass
import warnings


@dataclass
class WaveParameters:
    """Container for wave parameters with validation."""
    frequency: float = 1.0  # Hz
    amplitude: float = 1.0  # Wave height
    phase: float = 0.0      # Phase shift in radians
    offset: float = 0.0     # Vertical offset
    
    def __post_init__(self):
        """Validate parameters after initialization."""
        if self.frequency <= 0:
            raise ValueError(f"Frequency must be positive, got {self.frequency}")
        if self.amplitude < 0:
            raise ValueError(f"Amplitude must be non-negative, got {self.amplitude}")


class ConsciousnessWaveVisualizer:
    """
    A class for visualizing consciousness waves with various waveform types.
    
    This visualizer can generate and display different types of waves that
    represent consciousness states, with support for real-time updates and
    multiple waveform combinations.
    
    Attributes:
        wave_params (WaveParameters): Current wave parameters
        wave_type (str): Type of waveform ('sine', 'square', 'triangle', 'sawtooth', 'composite')
        sample_rate (int): Samples per second for wave generation
        time_window (float): Time window to display in seconds
        
    Example:
        >>> visualizer = ConsciousnessWaveVisualizer(frequency=2.0, amplitude=0.8)
        >>> visualizer.plot_static()
        >>> visualizer.start_live_stream()
    """
    
    VALID_WAVE_TYPES = {'sine', 'square', 'triangle', 'sawtooth', 'composite'}
    
    def __init__(self, 
                 frequency: float = 1.0,
                 amplitude: float = 1.0,
                 phase: float = 0.0,
                 wave_type: str = 'sine',
                 sample_rate: int = 1000,
                 time_window: float = 5.0):
        """
        Initialize the ConsciousnessWaveVisualizer.
        
        Args:
            frequency: Wave frequency in Hz (default: 1.0)
            amplitude: Wave amplitude (default: 1.0)
            phase: Phase shift in radians (default: 0.0)
            wave_type: Type of waveform (default: 'sine')
            sample_rate: Samples per second (default: 1000)
            time_window: Time window to display in seconds (default: 5.0)
            
        Raises:
            ValueError: If wave_type is not valid or parameters are invalid
        """
        # Validate wave type
        if wave_type not in self.VALID_WAVE_TYPES:
            raise ValueError(f"Invalid wave_type: {wave_type}. Must be one of {self.VALID_WAVE_TYPES}")
        
        # Initialize wave parameters
        self.wave_params = WaveParameters(frequency=frequency, amplitude=amplitude, phase=phase)
        self.wave_type = wave_type
        self.sample_rate = sample_rate
        self.time_window = time_window
        
        # For real-time streaming
        self._stream_active = False
        self._data_queue = queue.Queue(maxsize=1000)
        self._external_data_source: Optional[Callable] = None
        
        # Matplotlib setup
        self.fig: Optional[Figure] = None
        self.ax: Optional[plt.Axes] = None
        self.line = None
        
        # Consciousness-specific parameters
        self.consciousness_modulation = {
            'chaos': 0.0,      # 0-1, adds randomness
            'harmony': 1.0,    # 0-1, smoothing factor
            'resonance': 0.0,  # 0-1, harmonic emphasis
        }
        
    def generate_wave(self, t: np.ndarray) -> np.ndarray:
        """
        Generate waveform data based on current parameters.
        
        This method implements the mathematical generation of different wave types.
        For consciousness visualization, we use these waves as base patterns that
        can be modulated by consciousness parameters.
        
        Args:
            t: Time array in seconds
            
        Returns:
            Wave amplitude values corresponding to time points
            
        Mathematical basis:
            - Sine: y = A * sin(2πft + φ)
            - Square: y = A * sign(sin(2πft + φ))
            - Triangle: y = A * (2/π) * arcsin(sin(2πft + φ))
            - Sawtooth: y = A * (2/π) * arctan(tan(πft + φ/2))
            - Composite: Combination of multiple harmonics
        """
        f = self.wave_params.frequency
        A = self.wave_params.amplitude
        φ = self.wave_params.phase
        offset = self.wave_params.offset
        
        # Base angular frequency (ω = 2πf)
        omega = 2 * np.pi * f
        
        if self.wave_type == 'sine':
            # Pure sine wave - represents smooth consciousness flow
            wave = A * np.sin(omega * t + φ)
            
        elif self.wave_type == 'square':
            # Square wave - represents binary consciousness states
            wave = A * np.sign(np.sin(omega * t + φ))
            
        elif self.wave_type == 'triangle':
            # Triangle wave - represents linear consciousness transitions
            # Using Fourier series approximation for better performance
            wave = A * (2/np.pi) * np.arcsin(np.sin(omega * t + φ))
            
        elif self.wave_type == 'sawtooth':
            # Sawtooth wave - represents consciousness building/release cycles
            wave = A * (2/np.pi) * np.arctan(np.tan(np.pi * f * t + φ/2))
            
        elif self.wave_type == 'composite':
            # Composite wave - represents complex consciousness patterns
            # Fundamental + harmonics (simulating consciousness complexity)
            wave = A * np.sin(omega * t + φ)  # Fundamental
            wave += (A/3) * np.sin(3 * omega * t + φ)  # 3rd harmonic
            wave += (A/5) * np.sin(5 * omega * t + φ)  # 5th harmonic
            wave += (A/7) * np.sin(7 * omega * t + φ)  # 7th harmonic
            
        # Apply consciousness modulation
        wave = self._apply_consciousness_modulation(wave, t)
        
        return wave + offset
    
    def _apply_consciousness_modulation(self, wave: np.ndarray, t: np.ndarray) -> np.ndarray:
        """
        Apply consciousness-specific modulations to the wave.
        
        This method adds characteristics that make the wave more representative
        of consciousness states rather than pure mathematical functions.
        
        Args:
            wave: Base waveform
            t: Time array
            
        Returns:
            Modulated waveform
        """
        # Apply chaos (adds controlled randomness)
        if self.consciousness_modulation['chaos'] > 0:
            noise = np.random.normal(0, self.consciousness_modulation['chaos'] * 0.1, wave.shape)
            wave += noise * self.wave_params.amplitude
        
        # Apply harmony (smoothing via moving average)
        if self.consciousness_modulation['harmony'] < 1:
            window_size = int((1 - self.consciousness_modulation['harmony']) * 10) + 1
            wave = np.convolve(wave, np.ones(window_size)/window_size, mode='same')
        
        # Apply resonance (emphasize certain frequencies)
        if self.consciousness_modulation['resonance'] > 0:
            resonance_freq = self.wave_params.frequency * 2  # Octave resonance
            resonance = self.consciousness_modulation['resonance'] * 0.3
            wave += resonance * self.wave_params.amplitude * np.sin(2 * np.pi * resonance_freq * t)
        
        return wave
    
    def plot_static(self, duration: float = 5.0, show: bool = True) -> Optional[Figure]:
        """
        Create a static plot of the consciousness wave.
        
        Args:
            duration: Duration of wave to plot in seconds
            show: Whether to display the plot immediately
            
        Returns:
            Matplotlib figure object if show=False, None otherwise
        """
        # Generate time points
        t = np.linspace(0, duration, int(duration * self.sample_rate))
        
        # Generate wave
        wave = self.generate_wave(t)
        
        # Create figure
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.ax.set_facecolor('#0a0a0a')
        self.fig.patch.set_facecolor('#0a0a0a')
        
        # Plot wave with consciousness-themed styling
        self.line, = self.ax.plot(t, wave, color='#00ff88', linewidth=2)
        
        # Styling
        self.ax.set_xlabel('Time (s)', color='#e0e0e0')
        self.ax.set_ylabel('Amplitude', color='#e0e0e0')
        self.ax.set_title(f'Consciousness Wave - {self.wave_type.capitalize()} @ {self.wave_params.frequency}Hz', 
                         color='#e0e0e0', fontsize=14)
        self.ax.grid(True, alpha=0.2, color='#2a2a2a')
        self.ax.tick_params(colors='#808080')
        
        # Set y-axis limits with some padding
        y_margin = self.wave_params.amplitude * 0.2
        self.ax.set_ylim(-self.wave_params.amplitude - y_margin - abs(self.wave_params.offset),
                          self.wave_params.amplitude + y_margin + abs(self.wave_params.offset))
        
        plt.tight_layout()
        
        if show:
            plt.show()
            return None
        return self.fig
    
    def start_live_stream(self, update_interval: float = 0.05, data_source: Optional[Callable] = None):
        """
        Start real-time visualization of consciousness waves.
        
        Args:
            update_interval: Time between updates in seconds
            data_source: Optional callable that returns wave parameters dict
                        Expected format: {'frequency': float, 'amplitude': float, 'phase': float}
        """
        if self._stream_active:
            warnings.warn("Stream already active. Stop current stream before starting a new one.")
            return
        
        self._stream_active = True
        self._external_data_source = data_source
        
        # Setup the figure for animation
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.ax.set_facecolor('#0a0a0a')
        self.fig.patch.set_facecolor('#0a0a0a')
        
        # Initialize plot
        self.x_data = []
        self.y_data = []
        self.line, = self.ax.plot([], [], color='#00ff88', linewidth=2)
        
        # Configure axes
        self.ax.set_xlim(0, self.time_window)
        y_margin = self.wave_params.amplitude * 0.2
        self.ax.set_ylim(-self.wave_params.amplitude - y_margin,
                          self.wave_params.amplitude + y_margin)
        
        self.ax.set_xlabel('Time (s)', color='#e0e0e0')
        self.ax.set_ylabel('Amplitude', color='#e0e0e0')
        self.ax.set_title('Live Consciousness Wave Stream', color='#e0e0e0', fontsize=14)
        self.ax.grid(True, alpha=0.2, color='#2a2a2a')
        self.ax.tick_params(colors='#808080')
        
        # Start animation
        self.start_time = time.time()
        ani = animation.FuncAnimation(self.fig, self._update_live_plot, 
                                    interval=update_interval*1000, blit=True)
        
        plt.show()
        
        # Cleanup
        self._stream_active = False
    
    def _update_live_plot(self, frame):
        """Update function for live animation."""
        current_time = time.time() - self.start_time
        
        # Update parameters from external source if provided
        if self._external_data_source:
            try:
                new_params = self._external_data_source()
                if isinstance(new_params, dict):
                    self.update_parameters(**new_params)
            except Exception as e:
                warnings.warn(f"Error reading from data source: {e}")
        
        # Generate new data point
        t = np.array([current_time])
        y = self.generate_wave(t)[0]
        
        # Update data buffers
        self.x_data.append(current_time)
        self.y_data.append(y)
        
        # Keep only data within time window
        while self.x_data and self.x_data[0] < current_time - self.time_window:
            self.x_data.pop(0)
            self.y_data.pop(0)
        
        # Update plot
        self.line.set_data(self.x_data, self.y_data)
        
        # Adjust x-axis to follow current time
        if current_time > self.time_window:
            self.ax.set_xlim(current_time - self.time_window, current_time)
        
        return self.line,
    
    def update_parameters(self, frequency: Optional[float] = None,
                         amplitude: Optional[float] = None,
                         phase: Optional[float] = None,
                         offset: Optional[float] = None):
        """
        Update wave parameters dynamically.
        
        Args:
            frequency: New frequency in Hz
            amplitude: New amplitude
            phase: New phase in radians
            offset: New vertical offset
        """
        if frequency is not None:
            if frequency <= 0:
                raise ValueError(f"Frequency must be positive, got {frequency}")
            self.wave_params.frequency = frequency
            
        if amplitude is not None:
            if amplitude < 0:
                raise ValueError(f"Amplitude must be non-negative, got {amplitude}")
            self.wave_params.amplitude = amplitude
            
        if phase is not None:
            self.wave_params.phase = phase
            
        if offset is not None:
            self.wave_params.offset = offset
    
    def set_consciousness_modulation(self, chaos: Optional[float] = None,
                                   harmony: Optional[float] = None,
                                   resonance: Optional[float] = None):
        """
        Set consciousness-specific modulation parameters.
        
        Args:
            chaos: Randomness factor (0-1)
            harmony: Smoothing factor (0-1)
            resonance: Harmonic emphasis (0-1)
        """
        if chaos is not None:
            self.consciousness_modulation['chaos'] = np.clip(chaos, 0, 1)
        if harmony is not None:
            self.consciousness_modulation['harmony'] = np.clip(harmony, 0, 1)
        if resonance is not None:
            self.consciousness_modulation['resonance'] = np.clip(resonance, 0, 1)
    
    def save_snapshot(self, filename: str, dpi: int = 300):
        """
        Save current wave visualization to file.
        
        Args:
            filename: Output filename (e.g., 'consciousness_wave.png')
            dpi: Resolution in dots per inch
        """
        if self.fig is None:
            self.plot_static(show=False)
        
        self.fig.savefig(filename, dpi=dpi, facecolor='#0a0a0a', edgecolor='none')
        print(f"Wave snapshot saved to {filename}")
    
    def generate_wave_data(self, duration: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate wave data without plotting.
        
        Args:
            duration: Duration in seconds
            
        Returns:
            Tuple of (time_array, wave_array)
        """
        t = np.linspace(0, duration, int(duration * self.sample_rate))
        wave = self.generate_wave(t)
        return t, wave


def example_usage():
    """Demonstrate various features of the ConsciousnessWaveVisualizer."""
    
    print("=== Consciousness Wave Visualizer Examples ===\n")
    
    # Example 1: Basic sine wave
    print("1. Creating basic consciousness sine wave...")
    visualizer = ConsciousnessWaveVisualizer(frequency=2.0, amplitude=0.8)
    visualizer.plot_static(duration=3.0, show=False)
    visualizer.save_snapshot('consciousness_sine.png')
    
    # Example 2: Complex composite wave with modulation
    print("\n2. Creating complex consciousness pattern...")
    visualizer2 = ConsciousnessWaveVisualizer(
        frequency=1.5,
        amplitude=1.0,
        phase=np.pi/4,
        wave_type='composite'
    )
    visualizer2.set_consciousness_modulation(chaos=0.2, harmony=0.8, resonance=0.5)
    visualizer2.plot_static(duration=5.0, show=False)
    visualizer2.save_snapshot('consciousness_complex.png')
    
    # Example 3: Generate data for external processing
    print("\n3. Generating wave data for analysis...")
    t, wave = visualizer.generate_wave_data(duration=10.0)
    print(f"Generated {len(wave)} samples over {t[-1]:.1f} seconds")
    print(f"Wave stats: mean={np.mean(wave):.3f}, std={np.std(wave):.3f}")
    
    # Example 4: Live stream with simulated consciousness changes
    print("\n4. Starting live consciousness stream (close window to stop)...")
    
    def consciousness_data_source():
        """Simulate varying consciousness parameters."""
        current_time = time.time()
        # Simulate consciousness fluctuations
        return {
            'frequency': 1.0 + 0.5 * np.sin(current_time * 0.1),  # Slowly varying frequency
            'amplitude': 0.8 + 0.2 * np.sin(current_time * 0.2),  # Amplitude modulation
            'phase': current_time * 0.05  # Continuous phase shift
        }
    
    visualizer3 = ConsciousnessWaveVisualizer(wave_type='sine')
    visualizer3.set_consciousness_modulation(chaos=0.1, harmony=0.9, resonance=0.3)
    
    # Uncomment to see live stream (will block until window is closed)
    # visualizer3.start_live_stream(update_interval=0.05, data_source=consciousness_data_source)
    
    print("\nExamples completed! Check generated PNG files.")


# Integration example for DAWN tick engine
def integrate_with_dawn_tick_engine():
    """
    Example of how to integrate with DAWN's tick engine.
    
    This would be called from your main consciousness engine loop.
    """
    
    # Initialize visualizer
    wave_viz = ConsciousnessWaveVisualizer(wave_type='composite')
    
    def get_consciousness_state():
        """
        This function would connect to your actual DAWN tick engine.
        Replace with actual data retrieval from your consciousness engine.
        """
        # Example: Reading from your tick engine
        # from your_tick_engine import get_current_state
        # state = get_current_state()
        # return {
        #     'frequency': state.neural_frequency,
        #     'amplitude': state.scup,
        #     'phase': state.phase_coherence
        # }
        
        # Placeholder simulation
        return {
            'frequency': np.random.uniform(0.5, 2.0),
            'amplitude': np.random.uniform(0.5, 1.0),
            'phase': np.random.uniform(0, 2*np.pi)
        }
    
    # Start live visualization connected to tick engine
    wave_viz.start_live_stream(data_source=get_consciousness_state)


if __name__ == "__main__":
    # Run examples when module is executed directly
    example_usage()
    
    # Uncomment to test integration
    # integrate_with_dawn_tick_engine()