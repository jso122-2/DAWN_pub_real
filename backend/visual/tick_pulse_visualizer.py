"""
Backend Tick Pulse Visualizer for DAWN
Real-time cognitive heartbeat visualization integrated with the backend system.
"""

import json
import os
import os
import os
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import time
from collections import deque
from typing import Dict, Any, Optional, List
import logging

from ...base_visualizer import BaseVisualizer

logger = logging.getLogger(__name__)

class TickPulseVisualizer(BaseVisualizer):
    """Backend-compatible Tick Pulse Visualizer for DAWN's cognitive heartbeat"""
    
    def __init__(self, buffer_size: int = 200):
        super().__init__(name="TickPulseVisualizer")
        self.buffer_size = buffer_size
        
        # Tick tracking
        self.tick_history = deque(maxlen=buffer_size)
        self.time_history = deque(maxlen=buffer_size)
        self.pulse_intensity = deque(maxlen=buffer_size)
        
        # Cognitive rhythm analysis
        self.rhythm_amplitude = deque(maxlen=buffer_size)
        self.rhythm_frequency = 0.0
        self.rhythm_phase = 0.0
        
        # Current state
        self.current_tick = 0
        self.tick_rate = 0.0
        self.pulse_strength = 0.0
        self.heartbeat_phase = 0.0
        
        # Rhythm detection
        self.last_tick_time = time.time()
        self.tick_intervals = deque(maxlen=50)
        
        # Setup matplotlib
        plt.style.use('dark_background')
        self.fig, (self.ax_main, self.ax_rhythm) = plt.subplots(2, 1, figsize=(16, 10))
        self.fig.patch.set_facecolor('#0a0a0a')
        
        # Initialize displays
        self.setup_pulse_display()
        self.setup_rhythm_display()
        
        plt.tight_layout()
        
        # Animation objects
        self.animation = None
        self.pulse_line = None
        self.tick_line = None
        self.heartbeat_markers = None
        self.pulse_fill = None
        self.current_pulse_indicator = None
        self.rhythm_line = None
        self.rhythm_bands = []
        self.metrics_text = None
        
        logger.info("TickPulseVisualizer initialized")
    
    def setup_pulse_display(self):
        """Initialize the main cognitive pulse visualization"""
        self.ax_main.set_facecolor('#0a0a0a')
        self.ax_main.set_xlim(0, self.buffer_size)
        self.ax_main.set_ylim(-1.5, 1.5)
        
        # Main pulse line
        self.pulse_line, = self.ax_main.plot([], [], 'g-', linewidth=3, alpha=0.9, label='Cognitive Pulse')
        
        # Tick progression line
        self.tick_line, = self.ax_main.plot([], [], 'c-', linewidth=2, alpha=0.7, label='Tick Progression')
        
        # Heartbeat markers
        self.heartbeat_markers = self.ax_main.scatter([], [], s=[], c=[], 
                                                     cmap='plasma', alpha=0.8, label='Heartbeat Events')
        
        # Current pulse indicator (large circle)
        self.current_pulse_indicator = Circle((0, 0), 0.1, color='#00ff88', alpha=0.0)
        self.ax_main.add_patch(self.current_pulse_indicator)
        
        # Styling
        self.ax_main.set_title('DAWN Cognitive Heartbeat\nTick Pulse Monitor', 
                              fontsize=16, color='white', weight='bold', pad=20)
        self.ax_main.set_xlabel('Time Steps', color='#cccccc', fontsize=12)
        self.ax_main.set_ylabel('Cognitive Pulse Amplitude', color='#cccccc', fontsize=12)
        
        self.ax_main.grid(True, alpha=0.2, color='#444444')
        self.ax_main.legend(loc='upper right', facecolor='#1a1a1a', 
                           edgecolor='#444444', labelcolor='#cccccc')
        
        # Real-time metrics display
        self.metrics_text = self.ax_main.text(0.02, 0.98, '', transform=self.ax_main.transAxes,
                                             fontsize=11, color='#00ff88', verticalalignment='top',
                                             fontfamily='monospace', weight='bold')
    
    def setup_rhythm_display(self):
        """Initialize the rhythm analysis visualization"""
        self.ax_rhythm.set_facecolor('#0a0a0a')
        self.ax_rhythm.set_xlim(0, self.buffer_size)
        self.ax_rhythm.set_ylim(0, 2.0)
        
        # Rhythm amplitude
        self.rhythm_line, = self.ax_rhythm.plot([], [], 'orange', linewidth=2, 
                                               alpha=0.8, label='Rhythm Amplitude')
        
        # Frequency bands
        self.rhythm_bands = []
        band_colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57']
        band_labels = ['Ultra-Fast', 'Fast', 'Medium', 'Slow', 'Ultra-Slow']
        
        for i, (color, label) in enumerate(zip(band_colors, band_labels)):
            line, = self.ax_rhythm.plot([], [], color=color, linewidth=1.5, 
                                       alpha=0.6, label=f'{label} Rhythm')
            self.rhythm_bands.append(line)
        
        # Average rhythm indicator
        self.avg_rhythm_line = self.ax_rhythm.axhline(y=1.0, color='white', 
                                                     linestyle='--', alpha=0.5)
        
        # Styling
        self.ax_rhythm.set_title('Cognitive Rhythm Analysis', 
                                fontsize=14, color='white', weight='bold')
        self.ax_rhythm.set_xlabel('Time Steps', color='#cccccc', fontsize=12)
        self.ax_rhythm.set_ylabel('Rhythm Intensity', color='#cccccc', fontsize=12)
        
        self.ax_rhythm.grid(True, alpha=0.2, color='#444444')
        self.ax_rhythm.legend(loc='upper right', facecolor='#1a1a1a', 
                             edgecolor='#444444', labelcolor='#cccccc', fontsize=9)
    
    def parse_tick_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and process tick information from DAWN data"""

            # Extract tick count
            tick = data.get('tick', 0)
            
            # Calculate tick progression and timing
            current_time = time.time()
            if self.current_tick > 0:
                tick_interval = current_time - self.last_tick_time
                self.tick_intervals.append(tick_interval)
                
                # Calculate tick rate (ticks per second)
                if len(self.tick_intervals) > 1:
                    self.tick_rate = 1.0 / np.mean(list(self.tick_intervals))
            
            self.last_tick_time = current_time
            self.current_tick = tick
            
            # Extract cognitive state for pulse calculation
            mood = data.get('mood', {})
            entropy = data.get('entropy', 0.5)
            heat = data.get('heat', 0.3)
            scup = data.get('scup', {})
            
            # Calculate cognitive pulse intensity
            pulse_components = {
                'mood_component': self.calculate_mood_pulse(mood),
                'entropy_component': entropy * 0.5,
                'heat_component': heat * 0.3,
                'scup_component': self.calculate_scup_pulse(scup),
                'temporal_component': self.calculate_temporal_pulse(tick)
            }
            
            # Combine components into unified pulse
            base_pulse = sum(pulse_components.values()) / len(pulse_components)
            
            # Add heartbeat rhythm (sinusoidal with tick-based phase)
            self.heartbeat_phase += 0.1
            heartbeat_rhythm = 0.3 * np.sin(self.heartbeat_phase)
            
            # Final pulse intensity
            self.pulse_strength = base_pulse + heartbeat_rhythm
            
            return {
                'tick': tick,
                'pulse_intensity': self.pulse_strength,
                'tick_rate': self.tick_rate,
                'pulse_components': pulse_components,
                'heartbeat_phase': self.heartbeat_phase
            }
            
            logger.error(f"Error parsing tick data: {e}")
            return {
                'tick': self.current_tick,
                'pulse_intensity': 0.0,
                'tick_rate': 0.0,
                'pulse_components': {},
                'heartbeat_phase': 0.0
            }
    
    def calculate_mood_pulse(self, mood_data: Dict[str, Any]) -> float:
        """Calculate pulse component from mood state"""
        if not isinstance(mood_data, dict):
            return 0.3
        
        mood_vector = mood_data.get('vector', [0.5, 0.5, 0.5, 0.5])
        if not isinstance(mood_vector, list) or len(mood_vector) == 0:
            return 0.3
        
        # Mood intensity as deviation from neutral (0.5)
        mood_intensity = np.mean([abs(x - 0.5) for x in mood_vector[:4]]) * 2
        return mood_intensity
    
    def calculate_scup_pulse(self, scup_data: Dict[str, Any]) -> float:
        """Calculate pulse component from SCUP pressure"""
        if not isinstance(scup_data, dict):
            return 0.3
        
        scup_values = [
            scup_data.get('schema', 0.5),
            scup_data.get('coherence', 0.5),
            scup_data.get('utility', 0.5),
            scup_data.get('pressure', 0.5)
        ]
        
        # SCUP pulse as average pressure
        return np.mean(scup_values)
    
    def calculate_temporal_pulse(self, tick: int) -> float:
        """Calculate pulse component from temporal patterns"""
        # Create multiple rhythm frequencies
        fast_rhythm = 0.1 * np.sin(tick * 0.1)      # High frequency
        medium_rhythm = 0.2 * np.sin(tick * 0.05)   # Medium frequency  
        slow_rhythm = 0.3 * np.sin(tick * 0.01)     # Low frequency
        
        return 0.5 + fast_rhythm + medium_rhythm + slow_rhythm
    
    def analyze_cognitive_rhythm(self) -> Dict[str, Any]:
        """Analyze rhythm patterns in the pulse data"""
        if len(self.pulse_intensity) < 20:
            return {}
        
        pulse_array = np.array(list(self.pulse_intensity))
        
        # FFT analysis for frequency detection
        fft = np.fft.fft(pulse_array)
        frequencies = np.fft.fftfreq(len(pulse_array))
        
        # Find dominant frequency
        dominant_freq_idx = np.argmax(np.abs(fft[1:len(fft)//2])) + 1
        self.rhythm_frequency = abs(frequencies[dominant_freq_idx])
        
        # Calculate rhythm amplitude in different frequency bands
        rhythm_analysis = {
            'dominant_frequency': self.rhythm_frequency,
            'rhythm_strength': np.std(pulse_array),
            'rhythm_regularity': 1.0 / (np.std(np.diff(pulse_array)) + 0.01),
            'frequency_bands': self.analyze_frequency_bands(fft, frequencies)
        }
        
        return rhythm_analysis
    
    def analyze_frequency_bands(self, fft: np.ndarray, frequencies: np.ndarray) -> Dict[str, float]:
        """Analyze rhythm intensity in different frequency bands"""
        bands = {
            'ultra_fast': (0.3, 0.5),    # Very rapid cognitive changes
            'fast': (0.1, 0.3),          # Fast cognitive rhythms  
            'medium': (0.05, 0.1),       # Medium cognitive cycles
            'slow': (0.01, 0.05),        # Slow cognitive phases
            'ultra_slow': (0.001, 0.01)  # Very slow trends
        }
        
        band_intensities = {}
        
        for band_name, (min_freq, max_freq) in bands.items():
            # Find frequencies in this band
            band_mask = (np.abs(frequencies) >= min_freq) & (np.abs(frequencies) < max_freq)
            band_power = np.sum(np.abs(fft[band_mask])**2)
            band_intensities[band_name] = band_power
        
        # Normalize band intensities
        total_power = sum(band_intensities.values())
        if total_power > 0:
            band_intensities = {k: v/total_power for k, v in band_intensities.items()}
        
        return band_intensities
    
    def detect_pulse_peaks(self, pulse_data: List[float], min_prominence: float = 0.1) -> List[int]:
        """Detect heartbeat peaks in pulse data"""
        if len(pulse_data) < 5:
            return []
        
        peaks = []
        for i in range(2, len(pulse_data) - 2):
            # Simple peak detection: local maximum above threshold
            if (pulse_data[i] > pulse_data[i-1] and 
                pulse_data[i] > pulse_data[i+1] and
                pulse_data[i] > min_prominence):
                peaks.append(i)
        
        return peaks
    
    def format_metrics_display(self, tick_data: Dict[str, Any], rhythm_analysis: Dict[str, Any]) -> str:
        """Format real-time metrics for display"""
        tick = tick_data['tick']
        pulse = tick_data['pulse_intensity']
        tick_rate = tick_data['tick_rate']
        
        rhythm_freq = rhythm_analysis.get('dominant_frequency', 0.0)
        rhythm_strength = rhythm_analysis.get('rhythm_strength', 0.0)
        rhythm_regularity = rhythm_analysis.get('rhythm_regularity', 0.0)
        
        metrics = f"""COGNITIVE HEARTBEAT MONITOR
╭─────────────────────────────╮
│ Tick: {tick:08d}            │
│ Rate: {tick_rate:6.2f} Hz           │
│ Pulse: {pulse:6.3f}              │
├─────────────────────────────┤
│ Rhythm Freq: {rhythm_freq:6.3f}      │  
│ Rhythm Strength: {rhythm_strength:6.3f}   │
│ Regularity: {rhythm_regularity:6.3f}      │
╰─────────────────────────────╯"""
        
        return metrics
    
    def update(self, data: Dict[str, Any]) -> None:
        """Update the visualization with new data"""

            # Process tick data
            tick_data = self.parse_tick_data(data)
            
            # Update history buffers
            self.tick_history.append(tick_data['tick'])
            self.time_history.append(len(self.tick_history))
            self.pulse_intensity.append(tick_data['pulse_intensity'])
            
            # Analyze cognitive rhythm
            rhythm_analysis = self.analyze_cognitive_rhythm()
            
            # Update rhythm amplitude
            current_rhythm_amp = rhythm_analysis.get('rhythm_strength', 0.5)
            self.rhythm_amplitude.append(current_rhythm_amp)
            
            # Update main pulse display
            if len(self.pulse_intensity) > 1:
                x_data = list(range(len(self.pulse_intensity)))
                pulse_data = list(self.pulse_intensity)
                
                # Normalize tick progression for display
                if len(self.tick_history) > 1:
                    tick_normalized = np.array(list(self.tick_history)) / max(self.tick_history)
                    tick_normalized = (tick_normalized - 0.5) * 2  # Scale to [-1, 1]
                    self.tick_line.set_data(x_data, tick_normalized)
                
                self.pulse_line.set_data(x_data, pulse_data)
                
                # Update pulse fill
                if self.pulse_fill:
                    self.pulse_fill.remove()
                self.pulse_fill = self.ax_main.fill_between(x_data, 0, pulse_data, 
                                                           alpha=0.2, color='green')
                
                # Update heartbeat markers (peaks in pulse)
                peaks = self.detect_pulse_peaks(pulse_data)
                if peaks:
                    peak_x = [x_data[i] for i in peaks]
                    peak_y = [pulse_data[i] for i in peaks]
                    peak_sizes = [100 + 50 * abs(pulse_data[i]) for i in peaks]
                    peak_colors = [pulse_data[i] for i in peaks]
                    
                    self.heartbeat_markers.set_offsets(list(zip(peak_x, peak_y)))
                    self.heartbeat_markers.set_sizes(peak_sizes)
                    self.heartbeat_markers.set_array(np.array(peak_colors))
            
            # Update current pulse indicator
            current_x = len(self.pulse_intensity) - 1
            current_y = tick_data['pulse_intensity']
            
            self.current_pulse_indicator.center = (current_x, current_y)
            self.current_pulse_indicator.radius = 0.1 + 0.05 * abs(current_y)
            self.current_pulse_indicator.set_alpha(0.6 + 0.4 * abs(current_y))
            
            # Update rhythm analysis display
            if len(self.rhythm_amplitude) > 1:
                rhythm_x = list(range(len(self.rhythm_amplitude)))
                rhythm_y = list(self.rhythm_amplitude)
                
                self.rhythm_line.set_data(rhythm_x, rhythm_y)
                
                # Update frequency band lines
                if rhythm_analysis and 'frequency_bands' in rhythm_analysis:
                    bands = rhythm_analysis['frequency_bands']
                    band_names = ['ultra_fast', 'fast', 'medium', 'slow', 'ultra_slow']
                    
                    for i, (band_name, line) in enumerate(zip(band_names, self.rhythm_bands)):
                        if band_name in bands:
                            band_intensity = bands[band_name]
                            band_y = [band_intensity] * len(rhythm_x)
                            line.set_data(rhythm_x, band_y)
            
            # Update metrics display
            metrics_text = self.format_metrics_display(tick_data, rhythm_analysis)
            self.metrics_text.set_text(metrics_text)
            
            # Update axis limits for scrolling
            if len(self.pulse_intensity) > self.buffer_size * 0.8:
                self.ax_main.set_xlim(len(self.pulse_intensity) - self.buffer_size, 
                                     len(self.pulse_intensity))
                self.ax_rhythm.set_xlim(len(self.rhythm_amplitude) - self.buffer_size, 
                                       len(self.rhythm_amplitude))
            
            logger.error(f"Error updating tick pulse visualization: {e}")
    
    def render(self) -> None:
        """Render the current visualization state"""

            if self.fig:
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
            logger.error(f"Error rendering tick pulse visualization: {e}")
    
    def get_visualization_data(self) -> Dict[str, Any]:
        """Get current visualization data for API responses"""

            return {
                'tick': self.current_tick,
                'pulse_intensity': self.pulse_strength,
                'tick_rate': self.tick_rate,
                'rhythm_frequency': self.rhythm_frequency,
                'rhythm_strength': np.std(list(self.pulse_intensity)) if self.pulse_intensity else 0.0,
                'heartbeat_phase': self.heartbeat_phase,
                'buffer_size': len(self.pulse_intensity),
                'timestamp': time.time()
            }
            logger.error(f"Error getting visualization data: {e}")
            return {}
    
    def start_animation(self) -> None:
        """Start the animation loop"""

            if not self.animation:
                self.animation = animation.FuncAnimation(frames=1000, 
                    self.fig, 
                    lambda frame: self.render(), 
                    interval=100, 
                    blit=False, 
                    cache_frame_data=False
                )
            self.is_active = True
            logger.info("TickPulseVisualizer animation started")
            logger.error(f"Error starting animation: {e}")
    
    def stop_animation(self) -> None:
        """Stop the animation loop"""

            if self.animation:
                self.animation.event_source.stop()
                self.animation = None
            self.is_active = False
            logger.info("TickPulseVisualizer animation stopped")
            logger.error(f"Error stopping animation: {e}")
    
    def cleanup(self) -> None:
        """Clean up resources"""

            self.stop_animation()
            if self.fig:
                plt.close(self.fig)
            logger.info("TickPulseVisualizer cleaned up")
            logger.error(f"Error cleaning up: {e}")

def get_tick_pulse_visualizer() -> TickPulseVisualizer:
    """Factory function to create and return a TickPulseVisualizer instance"""
    return TickPulseVisualizer() 