"""
DAWN Pulse Waveform Renderer
Renders live waveform visualization of pulse heat with valence-based coloring
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection
from datetime import datetime
from typing import List, Dict, Tuple, Optional


class PulseWaveformRenderer:
    """Renders and saves pulse heat waveforms with valence-based coloring"""
    
    def __init__(self, 
                 output_dir: str = "visual_output/pulse_waveform",
                 window_size: int = 100,
                 save_interval: int = 20):
        """
        Initialize the pulse waveform renderer
        
        Args:
            output_dir: Directory to save output images
            window_size: Number of ticks to display in the waveform window
            save_interval: Save image every N ticks
        """
        self.output_dir = output_dir
        self.window_size = window_size
        self.save_interval = save_interval
        
        # Data storage
        self.ticks: List[int] = []
        self.heat_values: List[float] = []
        self.valence_values: List[float] = []  # -1 (calm/blue) to 1 (agitated/red)
        
        # Metadata storage
        self.metadata_index: List[Dict] = []
        self.current_tick = 0
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Setup figure
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.fig.patch.set_facecolor('#0a0a0a')
        self.ax.set_facecolor('#0a0a0a')
        
    def add_pulse_data(self, 
                      heat_value: float, 
                      valence: float = 0.0,
                      awareness_level: Optional[float] = None,
                      scup_data: Optional[Dict] = None):
        """
        Add a new pulse data point
        
        Args:
            heat_value: Thermal value (0-10)
            valence: Emotional valence (-1=calm/blue, 1=agitated/red)
            awareness_level: Optional awareness metric
            scup_data: Optional SCUP (Sensory Cortical Update Protocol) data
        """
        self.current_tick += 1
        self.ticks.append(self.current_tick)
        self.heat_values.append(np.clip(heat_value, 0, 10))
        self.valence_values.append(np.clip(valence, -1, 1))
        
        # Check if we should save
        if self.current_tick % self.save_interval == 0:
            self._save_waveform(awareness_level, scup_data)
    
    def _get_valence_color(self, valence: float) -> Tuple[float, float, float, float]:
        """Convert valence value to RGBA color"""
        # Normalize valence from [-1, 1] to [0, 1]
        normalized = (valence + 1) / 2
        
        # Interpolate between blue (calm) and red (agitated)
        # Blue: (0.2, 0.4, 0.8), Red: (0.8, 0.2, 0.2)
        r = 0.2 + (0.8 - 0.2) * normalized
        g = 0.4 - (0.4 - 0.2) * normalized
        b = 0.8 - (0.8 - 0.2) * normalized
        
        return (r, g, b, 0.8)
    
    def _create_gradient_line(self, x, y, valences):
        """Create a line with gradient coloring based on valence"""
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        # Create colors for each segment
        colors = [self._get_valence_color(v) for v in valences[:-1]]
        
        lc = LineCollection(segments, colors=colors, linewidth=2)
        return lc
    
    def _save_waveform(self, awareness_level: Optional[float], scup_data: Optional[Dict]):
        """Save the current waveform as PNG and update metadata"""
        self.ax.clear()
        
        # Determine display window
        start_idx = max(0, len(self.ticks) - self.window_size)
        display_ticks = self.ticks[start_idx:]
        display_heat = self.heat_values[start_idx:]
        display_valence = self.valence_values[start_idx:]
        
        if len(display_ticks) > 1:
            # Create gradient line
            line_collection = self._create_gradient_line(
                display_ticks, display_heat, display_valence
            )
            self.ax.add_collection(line_collection)
            
            # Add glow effect
            for i in range(3):
                alpha = 0.3 - i * 0.1
                width = 4 + i * 2
                glow_lc = self._create_gradient_line(
                    display_ticks, display_heat, display_valence
                )
                for line in glow_lc.get_segments():
                    self.ax.plot(line[:, 0], line[:, 1], 
                               color='white', alpha=alpha, linewidth=width)
        
        # Configure axes
        self.ax.set_xlim(display_ticks[0] if display_ticks else 0, 
                         display_ticks[-1] if display_ticks else 100)
        self.ax.set_ylim(-0.5, 10.5)
        
        # Styling
        self.ax.set_xlabel('Ticks', color='#cccccc', fontsize=12)
        self.ax.set_ylabel('Thermal Value', color='#cccccc', fontsize=12)
        self.ax.set_title(f'DAWN Pulse Heat - Tick {self.current_tick}', 
                         color='white', fontsize=16, pad=20)
        
        # Grid
        self.ax.grid(True, alpha=0.2, color='#444444')
        
        # Tick colors
        self.ax.tick_params(colors='#cccccc')
        for spine in self.ax.spines.values():
            spine.set_color('#444444')
        
        # Add legend
        calm_patch = mpatches.Patch(color=(0.2, 0.4, 0.8), label='Calm')
        agitated_patch = mpatches.Patch(color=(0.8, 0.2, 0.2), label='Agitated')
        self.ax.legend(handles=[calm_patch, agitated_patch], 
                      loc='upper right', facecolor='#1a1a1a', 
                      edgecolor='#444444', labelcolor='white')
        
        # Add current stats
        if display_heat:
            current_heat = display_heat[-1]
            current_valence = display_valence[-1]
            stats_text = f'Current: Heat={current_heat:.2f}, Valence={current_valence:.2f}'
            self.ax.text(0.02, 0.98, stats_text, transform=self.ax.transAxes,
                        color='white', fontsize=10, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='#1a1a1a', alpha=0.8))
        
        # Save image
        filename = f"tick_{self.current_tick:04d}.png"
        filepath = os.path.join(self.output_dir, filename)
        self.fig.savefig(filepath, dpi=150, bbox_inches='tight', 
                        facecolor=self.fig.get_facecolor())
        
        # Update metadata
        metadata_entry = {
            "tick": self.current_tick,
            "timestamp": datetime.now().isoformat(),
            "filename": filename,
            "heat_value": self.heat_values[-1] if self.heat_values else 0,
            "valence": self.valence_values[-1] if self.valence_values else 0,
            "awareness_level": awareness_level,
            "scup_data": scup_data or {},
            "stats": {
                "avg_heat": np.mean(display_heat) if display_heat else 0,
                "max_heat": np.max(display_heat) if display_heat else 0,
                "min_heat": np.min(display_heat) if display_heat else 0,
                "heat_variance": np.var(display_heat) if display_heat else 0
            }
        }
        self.metadata_index.append(metadata_entry)
        
        # Save metadata index
        index_path = os.path.join(self.output_dir, "metadata_index.json")
        with open(index_path, 'w') as f:
            json.dump(self.metadata_index, f, indent=2)
    
    def generate_pulse_sequence(self, 
                               duration: int = 200,
                               base_frequency: float = 0.1,
                               awareness_callback=None):
        """
        Generate a simulated pulse sequence for testing
        
        Args:
            duration: Number of ticks to generate
            base_frequency: Base frequency for the waveform
            awareness_callback: Optional function to calculate awareness
        """
        for i in range(duration):
            # Generate heat value with multiple frequency components
            t = i * 0.1
            heat = 5 + (
                2 * np.sin(base_frequency * t) +
                1 * np.sin(base_frequency * 3 * t) +
                0.5 * np.sin(base_frequency * 7 * t) +
                0.3 * np.random.randn()  # Add noise
            )
            
            # Generate valence based on heat rate of change
            if i > 0:
                heat_delta = heat - self.heat_values[-1]
                valence = np.tanh(heat_delta * 2)  # More change = more agitation
            else:
                valence = 0
            
            # Calculate awareness if callback provided
            awareness = None
            if awareness_callback:
                awareness = awareness_callback(i, heat, valence)
            
            # Example SCUP data
            scup_data = {
                "cortical_activity": np.random.rand(),
                "sensory_integration": np.random.rand(),
                "update_protocol": f"SCUP-{i:04d}"
            }
            
            self.add_pulse_data(heat, valence, awareness, scup_data)
    
    def close(self):
        """Close the renderer and save final state"""
        if self.current_tick % self.save_interval != 0:
            # Save final frame if needed
            self._save_waveform(None, None)
        plt.close(self.fig)


# Example usage
if __name__ == "__main__":
    # Create renderer
    renderer = PulseWaveformRenderer()
    
    # Example awareness calculation
    def calculate_awareness(tick, heat, valence):
        # Simple awareness model based on heat stability
        return 1.0 / (1.0 + abs(valence))
    
    # Generate example pulse sequence
    print("Generating pulse waveform sequence...")
    renderer.generate_pulse_sequence(
        duration=200,
        base_frequency=0.15,
        awareness_callback=calculate_awareness
    )
    
    # Close renderer
    renderer.close()
    print(f"Waveform images saved to: {renderer.output_dir}")
    print(f"Total frames generated: {renderer.current_tick // renderer.save_interval}")