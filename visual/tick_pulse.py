#!/usr/bin/env python3
# Add parent directory to Python path for imports
"""
DAWN Cognition Visualization #1: Tick Pulse
Foundation Tier - "Meeting DAWN"

Real-time line plot visualization of DAWN's cognitive heartbeat.
Displays the fundamental tick progression and cognitive rhythm patterns
that drive the recursive symbolic engine's processing cycles.
"""

import json
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import sys
import time
from collections import deque
import argparse
import math
            import os
                        import select

matplotlib.use('Agg')  # Use non-interactive backend for headless mode
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TickPulseVisualizer:
    def __init__(self, data_source="stdin", buffer_size=200, save_frames=False, output_dir='./visual_output/tick_pulse'):
        self.data_source = data_source
        self.buffer_size = buffer_size
        self.save_frames = save_frames
        self.output_dir = output_dir
        
        # Create output directory if saving
        if self.save_frames:
            os.makedirs(self.output_dir, exist_ok=True)
        
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
        
        # Initialize main pulse display
        self.setup_pulse_display()
        
        # Initialize rhythm analysis display
        self.setup_rhythm_display()
        
        plt.tight_layout()
    
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
        
        # Fill area under pulse
        self.pulse_fill = None
        
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
    
    def parse_tick_data(self, json_data):
        """Extract and process tick information from DAWN JSON output"""
        try:
            # Extract tick count
            tick = json_data.get('tick', 0)
            
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
            mood = json_data.get('mood', {})
            entropy = json_data.get('entropy', 0.5)
            heat = json_data.get('heat', 0.3)
            scup = json_data.get('scup', {})
            
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
            
        except Exception as e:
            print(f"Error parsing tick data: {e}", file=sys.stderr)
            return {
                'tick': self.current_tick,
                'pulse_intensity': 0.0,
                'tick_rate': 0.0,
                'pulse_components': {},
                'heartbeat_phase': 0.0
            }
    
    def calculate_mood_pulse(self, mood_data):
        """Calculate pulse component from mood state"""
        if not isinstance(mood_data, dict):
            return 0.3
        
        mood_vector = mood_data.get('vector', [0.5, 0.5, 0.5, 0.5])
        if not isinstance(mood_vector, list) or len(mood_vector) == 0:
            return 0.3
        
        # Mood intensity as deviation from neutral (0.5)
        mood_intensity = np.mean([abs(x - 0.5) for x in mood_vector[:4]]) * 2
        return mood_intensity
    
    def calculate_scup_pulse(self, scup_data):
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
    
    def calculate_temporal_pulse(self, tick):
        """Calculate pulse component from temporal patterns"""
        # Create multiple rhythm frequencies
        fast_rhythm = 0.1 * np.sin(tick * 0.1)      # High frequency
        medium_rhythm = 0.2 * np.sin(tick * 0.05)   # Medium frequency  
        slow_rhythm = 0.3 * np.sin(tick * 0.01)     # Low frequency
        
        return 0.5 + fast_rhythm + medium_rhythm + slow_rhythm
    
    def analyze_cognitive_rhythm(self):
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
    
    def analyze_frequency_bands(self, fft, frequencies):
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
    
    def read_latest_json_data(self):
        """Read the latest data from JSON file"""
        json_file = "/tmp/dawn_tick_data.json"
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        if last_line:
                            return json.loads(last_line)
            except Exception as e:
                print(f"Error reading JSON: {e}", file=sys.stderr)
        return None

    def update_visualization(self, frame):
        """Animation update function"""
        try:
            # Read data from JSON file
            data = self.read_latest_json_data()
            
            if data is None:
                # Use simulated data if no real data available
                data = {
                    'tick': frame,
                    'mood': {'valence': 0.5 + 0.2 * np.sin(frame * 0.05)},
                    'entropy': {'total_entropy': 0.5 + 0.2 * np.sin(frame * 0.03)},
                    'thermal_state': {'heat_level': 0.3 + 0.1 * np.cos(frame * 0.04)},
                    'scup': {'schema': 0.5, 'coherence': 0.5, 'utility': 0.5, 'pressure': 0.5}
                }
            
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
            
            # Save frame if requested
            if self.save_frames and frame % 10 == 0:  # Save every 10th frame
                filename = f"{self.output_dir}/tick_pulse_frame_{frame:06d}.png"
                self.fig.savefig(filename, dpi=100, bbox_inches='tight', 
                               facecolor='#0a0a0a', edgecolor='none')
            
            return [self.pulse_line, self.tick_line, self.heartbeat_markers, 
                   self.current_pulse_indicator, self.rhythm_line] + self.rhythm_bands
            
        except Exception as e:
            return [self.pulse_line, self.tick_line, self.heartbeat_markers]
    
    def detect_pulse_peaks(self, pulse_data, min_prominence=0.1):
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
    
    def format_metrics_display(self, tick_data, rhythm_analysis):
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
    
    def run(self, interval=100):
        """Start the real-time visualization"""
        try:
            if self.save_frames:
                # For saving mode, run a limited number of frames
                for frame in range(1000):  # Process up to 1000 frames
                    self.update_visualization(frame)
                    if frame % 50 == 0:  # Print progress every 50 frames
                        print(f"Processed frame {frame}", file=sys.stderr)
                    # Check if there's more data to read
                    try:
                        if not select.select([sys.stdin], [], [], 0)[0]:
                            break  # No more data available
                    except:
                        pass
                print(f"Tick Pulse saved frames to: {self.output_dir}")
            else:
                # Interactive mode
                ani = animation.FuncAnimation(self.fig, self.update_visualization,
                                            interval=interval, blit=False, cache_frame_data=False)
                plt.show()
        except KeyboardInterrupt:
            print("\nTick Pulse Visualizer terminated by user.")
        except Exception as e:
            print(f"Runtime error: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description='DAWN Tick Pulse Visualizer')
    parser.add_argument('--source', choices=['stdin', 'demo'], default='stdin',
                       help='Data source: stdin for live DAWN data, demo for testing')
    parser.add_argument('--interval', type=int, default=100,
                       help='Animation update interval in milliseconds')
    parser.add_argument('--buffer', type=int, default=200,
                       help='Pulse history buffer size')
    parser.add_argument('--save', action='store_true',
                       help='Save visualization frames as PNG files')
    parser.add_argument('--output-dir', default='./visual_output/tick_pulse',
                       help='Directory to save output frames')
    
    args = parser.parse_args()
    
    print("DAWN Cognition Visualization #1: Tick Pulse")
    print("Cognitive Heartbeat Monitor")
    print("=" * 50)
    
    if args.source == 'stdin':
        print("Waiting for DAWN JSON data on stdin...")
        print("Monitoring cognitive tick progression and heartbeat rhythms...")
    else:
        print("Running in demo mode with simulated tick data...")
    
    if args.save:
        print(f"Saving frames to: {args.output_dir}")
    
    visualizer = TickPulseVisualizer(data_source=args.source, buffer_size=args.buffer,
                                   save_frames=args.save, output_dir=args.output_dir)
    visualizer.run(interval=args.interval)

if __name__ == "__main__":
    main()