import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
import matplotlib.cm as cm
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d
import os
import json
from datetime import datetime
from pathlib import Path

class CoherenceFieldMap:
    """
    OWL-VIZ Coherence Field Renderer for DAWN
    Maps SCUP + entropy dynamics into visual coherence fields
    """
    
    def __init__(self, dawn_interface_path=None):
        # Initialize paths
        self.base_path = Path("C:/Users/Admin/OneDrive/Desktop/DAWN/Tick_engine")
        self.visual_output = self.base_path / "visual_output" / "coherence_map"
        self.visual_output.mkdir(parents=True, exist_ok=True)
        
        # DAWN interface
        self.dawn_interface = dawn_interface_path or self.base_path / "core_metabolic_helix.json"
        
        # Visual parameters
        self.fig_width = 16
        self.fig_height = 10
        self.dpi = 150
        
        # Field parameters
        self.tick_window = 100  # Number of ticks to display
        self.field_resolution = 50  # Vertical resolution of field
        self.collapse_threshold = 0.85  # Entropy threshold for collapse detection
        
        # Color mapping
        self.cmap_harmonic = cm.Blues_r
        self.cmap_critical = cm.Reds
        self.cmap_neutral = cm.viridis
        
        # Initialize data buffers
        self.ticks = []
        self.scup_values = []
        self.entropy_values = []
        self.pulse_values = []
        self.alignment_values = []
        self.collapse_events = []
        
    def read_metabolic_state(self):
        """Read current state from DAWN's core metabolic helix"""
        try:
            if self.dawn_interface.exists():
                with open(self.dawn_interface, 'r') as f:
                    state = json.load(f)
                    return {
                        'tick': state.get('tick', len(self.ticks)),
                        'scup': state.get('scup', np.random.random()),
                        'entropy': state.get('entropy', np.random.random()),
                        'pulse': state.get('pulse_heat', np.random.random()),
                        'alignment': state.get('schema_health_index', 0.5)
                    }
        except:
            pass
        
        # Simulated data if no interface
        tick = len(self.ticks)
        base_scup = 0.5 + 0.3 * np.sin(tick * 0.1)
        noise = np.random.normal(0, 0.05)
        
        return {
            'tick': tick,
            'scup': np.clip(base_scup + noise, 0, 1),
            'entropy': np.clip(0.3 + 0.4 * np.sin(tick * 0.07) + np.random.normal(0, 0.1), 0, 1),
            'pulse': np.clip(0.6 + 0.2 * np.sin(tick * 0.15), 0, 1),
            'alignment': np.clip(0.5 + 0.3 * np.cos(tick * 0.08), 0, 1)
        }
    
    def detect_collapse(self, entropy, scup):
        """Detect collapse moments in the coherence field"""
        tension = entropy * (1 - scup)
        return tension > self.collapse_threshold
    
    def calculate_tension_state(self, scup, entropy, pulse, alignment):
        """Calculate tension state for color mapping"""
        # Harmonic: high SCUP, low entropy, good alignment
        harmonic_score = scup * (1 - entropy) * alignment
        
        # Critical: high entropy, low SCUP, pulse instability
        critical_score = entropy * (1 - scup) * abs(pulse - 0.5) * 2
        
        # Return normalized tension (-1 = harmonic, 0 = neutral, 1 = critical)
        return np.clip(critical_score - harmonic_score, -1, 1)
    
    def generate_coherence_field(self, ticks, scup, entropy, tension_states):
        """Generate the 2D coherence field"""
        if len(ticks) < 2:
            return np.zeros((self.field_resolution, self.tick_window))
        
        # Create interpolated functions
        tick_range = np.linspace(ticks[0], ticks[-1], self.tick_window)
        
        # Smooth interpolation for SCUP waves
        if len(ticks) > 3:
            f_scup = interp1d(ticks, scup, kind='cubic', fill_value='extrapolate')
            f_entropy = interp1d(ticks, entropy, kind='cubic', fill_value='extrapolate')
            f_tension = interp1d(ticks, tension_states, kind='cubic', fill_value='extrapolate')
        else:
            f_scup = interp1d(ticks, scup, kind='linear', fill_value='extrapolate')
            f_entropy = interp1d(ticks, entropy, kind='linear', fill_value='extrapolate')
            f_tension = interp1d(ticks, tension_states, kind='linear', fill_value='extrapolate')
        
        # Sample at display resolution
        scup_smooth = f_scup(tick_range)
        entropy_smooth = f_entropy(tick_range)
        tension_smooth = f_tension(tick_range)
        
        # Create 2D field
        field = np.zeros((self.field_resolution, self.tick_window))
        
        for i, (s, e, t) in enumerate(zip(scup_smooth, entropy_smooth, tension_smooth)):
            # SCUP creates primary wave
            scup_wave = np.exp(-((np.linspace(0, 1, self.field_resolution) - s) ** 2) / 0.1)
            
            # Entropy creates interference pattern
            entropy_wave = e * np.sin(np.linspace(0, 10*np.pi, self.field_resolution) * (1 + e))
            
            # Combine with tension modulation
            field[:, i] = scup_wave + 0.3 * entropy_wave
            field[:, i] *= (1 + 0.5 * t)  # Amplify by tension
        
        # Apply Gaussian smoothing for fluid appearance
        field = gaussian_filter1d(field, sigma=1.5, axis=0)
        field = gaussian_filter1d(field, sigma=0.5, axis=1)
        
        return field, tick_range
    
    def render_frame(self, tick_num):
        """Render a single frame of the coherence field"""
        # Read current state
        state = self.read_metabolic_state()
        
        # Update buffers
        self.ticks.append(state['tick'])
        self.scup_values.append(state['scup'])
        self.entropy_values.append(state['entropy'])
        self.pulse_values.append(state['pulse'])
        self.alignment_values.append(state['alignment'])
        
        # Detect collapse
        if self.detect_collapse(state['entropy'], state['scup']):
            self.collapse_events.append(state['tick'])
        
        # Keep only recent data
        if len(self.ticks) > self.tick_window * 2:
            self.ticks = self.ticks[-self.tick_window:]
            self.scup_values = self.scup_values[-self.tick_window:]
            self.entropy_values = self.entropy_values[-self.tick_window:]
            self.pulse_values = self.pulse_values[-self.tick_window:]
            self.alignment_values = self.alignment_values[-self.tick_window:]
            self.collapse_events = [c for c in self.collapse_events if c > self.ticks[0]]
        
        # Calculate tension states
        tension_states = [
            self.calculate_tension_state(s, e, p, a) 
            for s, e, p, a in zip(
                self.scup_values, self.entropy_values, 
                self.pulse_values, self.alignment_values
            )
        ]
        
        # Generate coherence field
        field, tick_range = self.generate_coherence_field(
            self.ticks, self.scup_values, self.entropy_values, tension_states
        )
        
        # Create figure
        fig, (ax_field, ax_metrics) = plt.subplots(
            2, 1, figsize=(self.fig_width, self.fig_height),
            gridspec_kw={'height_ratios': [3, 1]},
            facecolor='#0a0a0a'
        )
        
        # Render coherence field
        ax_field.set_facecolor('#0a0a0a')
        
        # Create custom colormap based on average tension
        avg_tension = np.mean(tension_states[-20:]) if len(tension_states) > 20 else 0
        if avg_tension < -0.3:
            cmap = self.cmap_harmonic
        elif avg_tension > 0.3:
            cmap = self.cmap_critical
        else:
            cmap = self.cmap_neutral
        
        im = ax_field.imshow(
            field, aspect='auto', cmap=cmap,
            extent=[tick_range[0], tick_range[-1], 0, 1],
            alpha=0.9, vmin=0, vmax=2
        )
        
        # Add collapse flares
        for collapse_tick in self.collapse_events:
            if tick_range[0] <= collapse_tick <= tick_range[-1]:
                ax_field.axvline(
                    x=collapse_tick, color='#ff4444', alpha=0.7,
                    linewidth=2, linestyle='--'
                )
                # Add flare effect
                flare_width = 2
                flare = Rectangle(
                    (collapse_tick - flare_width/2, 0), flare_width, 1,
                    facecolor='#ff4444', alpha=0.2
                )
                ax_field.add_patch(flare)
        
        # Overlay SCUP and entropy traces
        if len(self.ticks) > 1:
            ax_field.plot(
                self.ticks[-len(self.scup_values):], 
                self.scup_values, 
                color='#00ffff', linewidth=2, alpha=0.8, label='SCUP'
            )
            ax_field.plot(
                self.ticks[-len(self.entropy_values):], 
                self.entropy_values, 
                color='#ff00ff', linewidth=2, alpha=0.8, label='Entropy'
            )
        
        ax_field.set_ylim(0, 1)
        ax_field.set_xlim(tick_range[0], tick_range[-1])
        ax_field.set_ylabel('Coherence State', color='white', fontsize=12)
        ax_field.set_title(
            f'DAWN Coherence Field | Tick {state["tick"]}', 
            color='white', fontsize=16, pad=20
        )
        ax_field.tick_params(colors='white')
        ax_field.legend(loc='upper right', facecolor='black', edgecolor='white')
        
        # Render metrics panel
        ax_metrics.set_facecolor('#0a0a0a')
        ax_metrics.plot(
            self.ticks, self.pulse_values, 
            color='#ffaa00', linewidth=1.5, alpha=0.8, label='Pulse'
        )
        ax_metrics.plot(
            self.ticks, self.alignment_values, 
            color='#00ff00', linewidth=1.5, alpha=0.8, label='Alignment'
        )
        ax_metrics.fill_between(
            self.ticks, 0, self.pulse_values, 
            color='#ffaa00', alpha=0.2
        )
        
        ax_metrics.set_ylim(0, 1)
        ax_metrics.set_xlim(tick_range[0], tick_range[-1])
        ax_metrics.set_xlabel('Tick', color='white', fontsize=12)
        ax_metrics.set_ylabel('Metabolic State', color='white', fontsize=12)
        ax_metrics.tick_params(colors='white')
        ax_metrics.legend(loc='upper right', facecolor='black', edgecolor='white')
        ax_metrics.grid(True, alpha=0.2, color='white')
        
        # Add tension indicator
        tension_color = plt.cm.RdBu_r(0.5 - avg_tension * 0.5)
        ax_metrics.text(
            0.02, 0.95, f'Tension: {avg_tension:.2f}',
            transform=ax_metrics.transAxes, color=tension_color,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='black', alpha=0.7)
        )
        
        plt.tight_layout()
        
        # Save frame
        filename = f"tick_{str(state['tick']).zfill(4)}.png"
        filepath = self.visual_output / filename
        plt.savefig(filepath, dpi=self.dpi, facecolor='#0a0a0a')
        plt.close()
        
        return filepath
    
    def run_continuous(self, interval=1000):
        """Run continuous visualization"""
        print(f"OWL-VIZ Coherence Field Map initialized")
        print(f"Output directory: {self.visual_output}")
        print(f"Monitoring: {self.dawn_interface}")
        
        tick = 0
        try:
            while True:
                filepath = self.render_frame(tick)
                print(f"Rendered: {filepath}")
                tick += 1
                
                # Small delay to prevent overwhelming the system
                import time
                time.sleep(interval / 1000.0)
                
        except KeyboardInterrupt:
            print("\nCoherence field visualization stopped")


if __name__ == "__main__":
    # Initialize and run the coherence field mapper
    mapper = CoherenceFieldMap()
    
    # Generate a single frame for testing
    test_frame = mapper.render_frame(0)
    print(f"Test frame generated: {test_frame}")
    
    # Uncomment to run continuous visualization
    # mapper.run_continuous(interval=500)  # Update every 500ms