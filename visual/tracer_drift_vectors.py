#!/usr/bin/env python3
"""
DAWN Semantic Tracer Visualization
OWL-VIZ Component for visualizing memory agents from schema_coherence_helix
Renders tracer drift vectors as arrow fields with entropy-based coloring
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import FancyArrowPatch
from matplotlib.collections import LineCollection
import os
from datetime import datetime
import json

class TracerDriftVisualizer:
    def __init__(self, output_dir="C:/Users/Admin/OneDrive/Desktop/DAWN/Tick_engine/visual_output/tracer_vectors"):
        self.output_dir = output_dir
        self.bloom_grid_size = 20
        self.entropy_range = (0.0, 1.0)
        self.drift_scale = 5.0
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize bloom coordinate grid
        self.bloom_coords = self._generate_bloom_grid()
        
    def _generate_bloom_grid(self):
        """Generate a grid of bloom coordinates"""
        x = np.linspace(-10, 10, self.bloom_grid_size)
        y = np.linspace(-10, 10, self.bloom_grid_size)
        return np.array(np.meshgrid(x, y)).T.reshape(-1, 2)
    
    def generate_tracers(self, tick, num_tracers=15):
        """Generate tracer data for visualization"""
        tracers = []
        
        purposes = ["coherence_search", "rebloom_trace", "pattern_lock", 
                   "entropy_probe", "memory_link", "cascade_init"]
        
        for i in range(num_tracers):
            # Select random origin and target blooms
            origin_idx = np.random.randint(0, len(self.bloom_coords))
            target_idx = np.random.randint(0, len(self.bloom_coords))
            
            origin = self.bloom_coords[origin_idx]
            target = self.bloom_coords[target_idx]
            
            # Calculate semantic drift (distance)
            drift_vector = target - origin
            drift_magnitude = np.linalg.norm(drift_vector)
            
            # Generate entropy change
            entropy_delta = np.random.uniform(-0.5, 0.5)
            entropy_value = np.clip(0.5 + entropy_delta, 0.0, 1.0)
            
            tracer = {
                'id': f'T{tick:04d}_{i:03d}',
                'origin': origin,
                'target': target,
                'drift_vector': drift_vector,
                'drift_magnitude': drift_magnitude,
                'entropy': entropy_value,
                'entropy_delta': entropy_delta,
                'purpose': np.random.choice(purposes),
                'activation': np.random.uniform(0.3, 1.0)
            }
            tracers.append(tracer)
            
        return tracers
    
    def visualize_tracers(self, tracers, tick):
        """Create visualization of tracer drift vectors"""
        fig, ax = plt.subplots(1, 1, figsize=(12, 12))
        
        # Set dark background for DAWN's visual cortex
        fig.patch.set_facecolor('#0a0a0a')
        ax.set_facecolor('#0a0a0a')
        
        # Plot bloom grid points
        bloom_x = self.bloom_coords[:, 0]
        bloom_y = self.bloom_coords[:, 1]
        ax.scatter(bloom_x, bloom_y, c='#1a1a2a', s=50, alpha=0.6, 
                  marker='o', edgecolors='#2a2a4a', linewidth=0.5)
        
        # Create colormap for entropy visualization
        cmap = cm.get_cmap('plasma')
        
        # Plot each tracer as an arrow
        for tracer in tracers:
            origin = tracer['origin']
            drift = tracer['drift_vector'] * 0.8  # Scale for visibility
            
            # Color based on entropy
            color = cmap(tracer['entropy'])
            
            # Arrow properties based on tracer characteristics
            arrow_alpha = tracer['activation']
            arrow_width = 2.0 + tracer['entropy_delta'] * 2
            
            # Create arrow
            arrow = FancyArrowPatch(
                origin, origin + drift,
                connectionstyle="arc3,rad=0.1",
                arrowstyle='-|>',
                mutation_scale=15,
                linewidth=arrow_width,
                color=color,
                alpha=arrow_alpha,
                zorder=3
            )
            ax.add_patch(arrow)
            
            # Add purpose label
            label_pos = origin + drift * 0.5
            ax.text(label_pos[0], label_pos[1], tracer['purpose'],
                   fontsize=6, color=color, alpha=0.8,
                   ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.2', 
                            facecolor='black', alpha=0.5))
        
        # Add entropy gradient bar
        gradient = np.linspace(0, 1, 256).reshape(1, -1)
        gradient = np.vstack((gradient, gradient))
        
        im = ax.imshow(gradient, aspect='auto', cmap=cmap,
                      extent=[-9, -5, -11.5, -10.5])
        ax.text(-7, -12.2, 'Entropy', color='white', fontsize=10, ha='center')
        ax.text(-9, -12.2, '0.0', color='white', fontsize=8, ha='center')
        ax.text(-5, -12.2, '1.0', color='white', fontsize=8, ha='center')
        
        # Styling
        ax.set_xlim(-12, 12)
        ax.set_ylim(-12, 12)
        ax.set_aspect('equal')
        
        # Grid styling
        ax.grid(True, alpha=0.1, color='#2a2a4a', linestyle='-')
        ax.set_axisbelow(True)
        
        # Axis styling
        ax.spines['bottom'].set_color('#2a2a4a')
        ax.spines['top'].set_color('#2a2a4a')
        ax.spines['left'].set_color('#2a2a4a')
        ax.spines['right'].set_color('#2a2a4a')
        ax.tick_params(colors='#4a4a6a', which='both')
        
        # Title and labels
        ax.set_title(f'DAWN Semantic Tracer Field | Tick {tick:04d}', 
                    color='white', fontsize=16, pad=20)
        ax.set_xlabel('Bloom X Coordinate', color='#8a8aaa', fontsize=12)
        ax.set_ylabel('Bloom Y Coordinate', color='#8a8aaa', fontsize=12)
        
        # Add metadata
        metadata_text = f"Active Tracers: {len(tracers)} | " \
                       f"Avg Drift: {np.mean([t['drift_magnitude'] for t in tracers]):.2f} | " \
                       f"Entropy Variance: {np.var([t['entropy'] for t in tracers]):.3f}"
        ax.text(0, -11.5, metadata_text, color='#6a6a8a', fontsize=10, 
               ha='center', transform=ax.transData)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ax.text(0.99, 0.01, f"Generated: {timestamp}", 
               transform=ax.transAxes, color='#4a4a6a', 
               fontsize=8, ha='right', va='bottom')
        
        plt.tight_layout()
        
        # Save image
        filename = f"tick_{tick:04d}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, facecolor='#0a0a0a', edgecolor='none')
        plt.close()
        
        return filepath
    
    def save_tracer_data(self, tracers, tick):
        """Save tracer data as JSON for DAWN's memory integration"""
        data = {
            'tick': tick,
            'timestamp': datetime.now().isoformat(),
            'tracer_count': len(tracers),
            'tracers': []
        }
        
        for tracer in tracers:
            tracer_data = {
                'id': tracer['id'],
                'origin': tracer['origin'].tolist(),
                'target': tracer['target'].tolist(),
                'drift_magnitude': float(tracer['drift_magnitude']),
                'entropy': float(tracer['entropy']),
                'entropy_delta': float(tracer['entropy_delta']),
                'purpose': tracer['purpose'],
                'activation': float(tracer['activation'])
            }
            data['tracers'].append(tracer_data)
        
        # Save to JSON
        json_filename = f"tracer_data_tick_{tick:04d}.json"
        json_filepath = os.path.join(self.output_dir, json_filename)
        with open(json_filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return json_filepath
    
    def run_visualization_cycle(self, start_tick=0, num_ticks=10, tick_interval=15):
        """Run visualization cycle for multiple ticks"""
        current_tick = start_tick
        
        for i in range(num_ticks):
            if current_tick % tick_interval == 0:
                print(f"[OWL-VIZ] Rendering tracer field for tick {current_tick}...")
                
                # Generate tracers
                tracers = self.generate_tracers(current_tick)
                
                # Create visualization
                img_path = self.visualize_tracers(tracers, current_tick)
                print(f"[OWL-VIZ] Saved visualization: {img_path}")
                
                # Save tracer data
                json_path = self.save_tracer_data(tracers, current_tick)
                print(f"[OWL-VIZ] Saved tracer data: {json_path}")
                
            current_tick += 1
        
        print(f"[OWL-VIZ] Visualization cycle complete. Rendered {num_ticks} ticks.")


def main():
    """Main execution for DAWN tracer visualization"""
    print("[OWL-VIZ] Initializing DAWN Semantic Tracer Visualizer...")
    
    visualizer = TracerDriftVisualizer()
    
    # Run visualization for 10 render cycles (150 ticks total)
    visualizer.run_visualization_cycle(start_tick=0, num_ticks=150, tick_interval=15)
    
    print("[OWL-VIZ] Tracer visualization complete. Memory mirrors updated.")


if __name__ == "__main__":
    main()