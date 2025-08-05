#!/usr/bin/env python3
# Add parent directory to Python path for imports
"""
DAWN Visualization #6: SCUP Pressure Grid
A real-time 4x4 heatmap showing dynamic interactions between DAWN's four core
cognitive pressure dimensions: Schema, Coherence, Utility, and Pressure.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import json
import os
import sys
import argparse
import time
from datetime import datetime
from collections import deque
import threading
import queue

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
class SCUPPressureGrid:
    """SCUP Pressure Grid Visualization"""
    
    def __init__(self, data_source='demo', smoothing=0.15, interaction_model='reinforcing',
                 history_size=50):
        # Core dimensions
        self.dimensions = ['Schema', 'Coherence', 'Utility', 'Pressure']
        self.short_dims = ['S', 'C', 'U', 'P']
        
        # Interaction labels for off-diagonal cells
        self.interaction_labels = {
            (0, 1): 'Structure↔Meaning',
            (0, 2): 'Pattern↔Goal',
            (0, 3): 'Structure↔Urgency',
            (1, 0): 'Meaning↔Structure',
            (1, 2): 'Meaning↔Goal',
            (1, 3): 'Meaning↔Urgency',
            (2, 0): 'Goal↔Pattern',
            (2, 1): 'Goal↔Meaning',
            (2, 3): 'Goal↔Urgency',
            (3, 0): 'Urgency↔Structure',
            (3, 1): 'Urgency↔Meaning',
            (3, 2): 'Urgency↔Goal'
        }
        
        # Self-pressure labels for diagonal cells
        self.self_labels = {
            0: 'Pattern\nRigidity',
            1: 'Meaning\nIntegration',
            2: 'Goal\nOptimization',
            3: 'Urgency\nAmplification'
        }
        
        # Interaction calculation models
        self.interaction_models = {
            'reinforcing': lambda a, b: a * b,
            'competing': lambda a, b: abs(a - b),
            'averaging': lambda a, b: (a + b) / 2,
            'tension': lambda a, b: min(a, b) * abs(a - b),
            'synergistic': lambda a, b: (a * b) ** 0.5
        }
        
        # Parameters
        self.data_source = data_source
        self.smoothing = smoothing
        self.interaction_model_name = interaction_model
        self.interaction_fn = self.interaction_models[interaction_model]
        self.history_size = history_size
        
        # State variables
        self.pressure_matrix = np.zeros((4, 4))
        self.pressure_history = deque(maxlen=history_size)
        self.scup_history = {dim: deque(maxlen=history_size) for dim in self.dimensions}
        self.time_stamps = deque(maxlen=history_size)
        self.data_queue = queue.Queue()
        
        # Wave propagation state
        self.wave_sources = []  # [(row, col, intensity, time)]
        self.wave_decay = 0.85
        
        # Critical state detection
        self.critical_threshold = 0.8
        self.critical_cells = set()
        
        # Setup visualization
        self.setup_visualization()
        
    def setup_visualization(self):
        """Initialize matplotlib figure and components"""
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(14, 10), facecolor='#0a0a0a')
        
        # Create custom colormap (blue → yellow → red)
        colors = ['#001f3f', '#0074D9', '#39CCCC', '#3D9970', 
                  '#FFDC00', '#FF851B', '#FF4136', '#85144b']
        n_bins = 100
        self.cmap = LinearSegmentedColormap.from_list('pressure', colors, N=n_bins)
        
        # Layout: Main heatmap + side panels
        gs = self.fig.add_gridspec(4, 6, width_ratios=[1, 1, 1, 1, 0.3, 1.5],
                                   height_ratios=[1, 1, 1, 1],
                                   hspace=0.3, wspace=0.3)
        
        # Main heatmap
        self.ax_heatmap = self.fig.add_subplot(gs[:, :4])
        
        # Individual pressure bars
        self.ax_bars = []
        for i in range(4):
            ax = self.fig.add_subplot(gs[i, 5])
            self.ax_bars.append(ax)
        
        # Initialize heatmap
        self.im = self.ax_heatmap.imshow(self.pressure_matrix, cmap=self.cmap,
                                          vmin=0, vmax=1, aspect='equal')
        
        # Add colorbar
        cbar_ax = self.fig.add_subplot(gs[:, 4])
        self.cbar = plt.colorbar(self.im, cax=cbar_ax)
        self.cbar.set_label('Pressure Intensity', fontsize=12, color='white')
        self.cbar.ax.tick_params(colors='white')
        
        # Configure heatmap
        self.ax_heatmap.set_title('DAWN SCUP Pressure Grid', fontsize=16, 
                                  fontweight='bold', pad=20, color='white')
        self.ax_heatmap.set_xticks(range(4))
        self.ax_heatmap.set_yticks(range(4))
        self.ax_heatmap.set_xticklabels(self.short_dims, fontsize=14, fontweight='bold')
        self.ax_heatmap.set_yticklabels(self.short_dims, fontsize=14, fontweight='bold')
        
        # Add grid lines
        for i in range(5):
            self.ax_heatmap.axhline(i - 0.5, color='white', linewidth=2, alpha=0.3)
            self.ax_heatmap.axvline(i - 0.5, color='white', linewidth=2, alpha=0.3)
        
        # Cell annotations
        self.cell_texts = []
        for i in range(4):
            row_texts = []
            for j in range(4):
                if i == j:
                    # Diagonal cell - self pressure
                    text = self.ax_heatmap.text(j, i, self.self_labels[i],
                                               ha='center', va='center',
                                               fontsize=10, fontweight='bold',
                                               color='white', alpha=0.8)
                else:
                    # Off-diagonal - interaction
                    label = self.interaction_labels.get((i, j), '')
                    text = self.ax_heatmap.text(j, i, label,
                                               ha='center', va='center',
                                               fontsize=8, color='white',
                                               alpha=0.7, rotation=0)
                row_texts.append(text)
            self.cell_texts.append(row_texts)
        
        # Initialize pressure history bars
        self.setup_pressure_bars()
        
        # Add metadata text
        self.metadata_text = self.fig.text(0.02, 0.02, '', fontsize=10,
                                          color='gray', alpha=0.8)
        
        # Critical state indicator
        self.critical_text = self.fig.text(0.5, 0.95, '', fontsize=14,
                                          ha='center', color='#FF4136',
                                          fontweight='bold', alpha=0)
        
    def setup_pressure_bars(self):
        """Initialize individual pressure dimension bars"""
        for i, (ax, dim) in enumerate(zip(self.ax_bars, self.dimensions)):
            ax.set_xlim(0, self.history_size)
            ax.set_ylim(0, 1)
            ax.set_title(dim, fontsize=12, color='white', pad=5)
            ax.set_ylabel('Pressure', fontsize=10, color='white')
            ax.grid(True, alpha=0.2)
            ax.set_facecolor('#0a0a0a')
            
            # Create line plot for history
            line, = ax.plot([], [], color=self.cmap(0.5), linewidth=2, alpha=0.8)
            ax.line = line
            
            # Current value text
            value_text = ax.text(0.95, 0.95, '', transform=ax.transAxes,
                               ha='right', va='top', fontsize=10,
                               color='white', fontweight='bold')
            ax.value_text = value_text
    
    def calculate_pressure_matrix(self, scup_values):
        """Calculate 4x4 pressure interaction matrix"""
        # Extract individual dimension values
        dims = [scup_values.get(dim.lower(), 0.5) for dim in self.dimensions]
        
        # Apply temporal smoothing
        if len(self.pressure_history) > 0:
            prev_matrix = self.pressure_history[-1]
            smooth_factor = self.smoothing
        else:
            prev_matrix = np.zeros((4, 4))
            smooth_factor = 0
        
        # Calculate new pressure matrix
        new_matrix = np.zeros((4, 4))
        
        for i in range(4):
            for j in range(4):
                if i == j:
                    # Self-pressure (diagonal)
                    # Higher values indicate more internal pressure
                    new_matrix[i, j] = dims[i] ** 1.5  # Amplify high values
                else:
                    # Interaction pressure (off-diagonal)
                    new_matrix[i, j] = self.interaction_fn(dims[i], dims[j])
        
        # Apply wave propagation effects
        wave_matrix = self.calculate_wave_effects()
        new_matrix = new_matrix * 0.8 + wave_matrix * 0.2
        
        # Apply temporal smoothing
        self.pressure_matrix = (1 - smooth_factor) * new_matrix + smooth_factor * prev_matrix
        
        # Detect critical states
        self.detect_critical_states()
        
        # Update history
        self.pressure_history.append(self.pressure_matrix.copy())
        self.time_stamps.append(time.time())
        
        # Update dimension histories
        for i, dim in enumerate(self.dimensions):
            self.scup_history[dim].append(dims[i])
    
    def calculate_wave_effects(self):
        """Calculate pressure wave propagation effects"""
        wave_matrix = np.zeros((4, 4))
        
        # Process active waves
        current_time = time.time()
        active_waves = []
        
        for row, col, intensity, start_time in self.wave_sources:
            age = current_time - start_time
            if age < 2.0:  # Wave lifetime
                # Calculate wave spread
                decay = self.wave_decay ** age
                radius = age * 2  # Wave speed
                
                # Apply wave to nearby cells
                for i in range(4):
                    for j in range(4):
                        distance = np.sqrt((i - row)**2 + (j - col)**2)
                        if distance <= radius:
                            wave_intensity = intensity * decay * (1 - distance/radius)
                            wave_matrix[i, j] = max(wave_matrix[i, j], wave_intensity)
                active_waves.append((row, col, intensity, start_time))
        
        self.wave_sources = active_waves
        return wave_matrix
    
    def detect_critical_states(self):
        """Detect critical pressure states"""
        self.critical_cells.clear()
        
        for i in range(4):
            for j in range(4):
                if self.pressure_matrix[i, j] > self.critical_threshold:
                    self.critical_cells.add((i, j))
                    
                    # Trigger wave if new critical state
                    if len(self.wave_sources) < 3:  # Limit concurrent waves
                        self.wave_sources.append((i, j, 0.8, time.time()))
    
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
            # Get latest data
            if not self.data_queue.empty():
                data = self.data_queue.get_nowait()
                self.calculate_pressure_matrix(data)
            elif self.data_source == 'demo':
                # Generate demo data
                data = self.generate_demo_data(frame)
                self.calculate_pressure_matrix(data)
            # Update heatmap
            self.im.set_array(self.pressure_matrix)
            # Update cell colors based on intensity
            for i in range(4):
                for j in range(4):
                    intensity = self.pressure_matrix[i, j]
                    text = self.cell_texts[i][j]
                    # Adjust text color for readability
                    if intensity > 0.6:
                        text.set_color('black')
                    else:
                        text.set_color('white')
                    # Highlight critical cells
                    if (i, j) in self.critical_cells:
                        text.set_fontweight('bold')
                        text.set_fontsize(12 if i == j else 10)
                    else:
                        text.set_fontweight('normal')
                        text.set_fontsize(10 if i == j else 8)
            # Update pressure history bars
            for i, (ax, dim) in enumerate(zip(self.ax_bars, self.dimensions)):
                history = list(self.scup_history[dim])
                if history:
                    x = range(len(history))
                    ax.line.set_data(x, history)
                    ax.set_xlim(0, max(len(history), 10))
                    # Update current value
                    current_val = history[-1] if history else 0
                    ax.value_text.set_text(f'{current_val:.3f}')
                    ax.value_text.set_color(self.cmap(current_val))
            # Update metadata
            if self.time_stamps:
                fps = len(self.time_stamps) / max(1, self.time_stamps[-1] - self.time_stamps[0])
                self.metadata_text.set_text(
                    f'Model: {self.interaction_model_name} | '
                    f'Smoothing: {self.smoothing:.2f} | '
                    f'FPS: {fps:.1f}'
                )
            # Update critical state indicator
            if self.critical_cells:
                self.critical_text.set_text('⚠ CRITICAL PRESSURE DETECTED ⚠')
                self.critical_text.set_alpha(0.8 + 0.2 * np.sin(frame * 0.5))
            else:
                self.critical_text.set_alpha(0)
        except Exception as e:
            print(f"Update error: {e}", file=sys.stderr)
        return [self.im] + [text for row in self.cell_texts for text in row]
    
    def generate_demo_data(self, frame):
        """Generate demonstration data with interesting patterns"""
        t = frame * 0.05
        
        # Create dynamic patterns
        data = {
            'schema': 0.5 + 0.3 * np.sin(t) + 0.1 * np.sin(t * 3.7),
            'coherence': 0.5 + 0.3 * np.cos(t * 0.7) + 0.1 * np.cos(t * 4.3),
            'utility': 0.5 + 0.25 * np.sin(t * 1.3) * np.cos(t * 0.3),
            'pressure': 0.3 + 0.4 * abs(np.sin(t * 0.5)) + 0.2 * np.random.random()
        }
        
        # Add occasional spikes
        if np.random.random() < 0.02:
            spike_dim = np.random.choice(list(data.keys()))
            data[spike_dim] = min(1.0, data[spike_dim] + 0.3)
        
        # Ensure values are in [0, 1]
        for key in data:
            data[key] = np.clip(data[key], 0, 1)
        
        return data
    
    def read_json_data(self):
        """Background thread to read data from JSON file"""
        json_file = "/tmp/dawn_tick_data.json"
        last_position = 0
        
        while not hasattr(self, 'stop_event') or not self.stop_event.is_set():
            try:
                if not os.path.exists(json_file):
                    time.sleep(0.1)
                    continue
                
                with open(json_file, 'r') as f:
                    f.seek(last_position)
                    lines = f.readlines()
                    last_position = f.tell()
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            self.data_queue.put(data)
                        except json.JSONDecodeError as e:
                            print(f"Error parsing JSON: {e}", file=sys.stderr)
                            continue
                
                time.sleep(0.1)  # Small delay to avoid excessive CPU usage
                
            except Exception as e:
                print(f"Error reading JSON file: {e}", file=sys.stderr)
                time.sleep(1.0)  # Longer delay on error
    
    def run(self):
        """Start the visualization"""
        # Start stdin reader thread if needed
        if self.data_source == 'stdin':
            self.stop_event = threading.Event()
            reader_thread = threading.Thread(target=self.read_json_data, daemon=True)
            reader_thread.start()
        
        # Create animation
        self.ani = animation.FuncAnimation(
            self.fig, self.update_visualization,
            interval=50,  # 20 FPS
            blit=False,
            cache_frame_data=False
        )
        
        plt.show()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='SCUP Pressure Grid Visualization')
    parser.add_argument('--data-source', default='demo', 
                       choices=['demo', 'stdin'],
                       help='Data source (demo or stdin)')
    parser.add_argument('--smoothing', type=float, default=0.15,
                       help='Temporal smoothing factor (0-1)')
    parser.add_argument('--interaction-model', default='reinforcing',
                       choices=['reinforcing', 'competing', 'averaging', 'tension', 'synergistic'],
                       help='Interaction calculation model')
    parser.add_argument('--history-size', type=int, default=50,
                       help='History buffer size')
    
    args = parser.parse_args()
    
    # Create and run visualization
    viz = SCUPPressureGrid(
        data_source=args.data_source,
        smoothing=args.smoothing,
        interaction_model=args.interaction_model,
        history_size=args.history_size
    )
    
    print(f"Starting DAWN SCUP Pressure Grid Visualization...")
    print(f"Data source: {args.data_source}")
    print(f"Interaction model: {args.interaction_model}")
    print(f"Smoothing: {args.smoothing}")
    
    if args.data_source == 'stdin':
        print("Waiting for JSON data on stdin...")
    
    viz.run()

if __name__ == '__main__':
    main()