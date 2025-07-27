"""
DAWN Visual Process Scripts
Four minimal, robust Python scripts for scientific visualization
"""

# ================================================================================
# 1. mood_heatmap.py
# ================================================================================

import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

def run_mood_heatmap(*args, **kwargs):
    """Generate and save a mood intensity heatmap"""
    # Create output directory
    output_dir = Path("visual/outputs/mood_heatmap")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate synthetic mood data (10x10 grid)
    np.random.seed(42)  # For reproducibility
    mood_data = np.random.rand(10, 10)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create heatmap
    im = ax.imshow(mood_data, cmap='RdYlBu_r', aspect='auto', vmin=0, vmax=1)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Mood Intensity', rotation=270, labelpad=15)
    
    # Set title and labels
    ax.set_title('Mood Heatmap')
    ax.set_xlabel('X Dimension')
    ax.set_ylabel('Y Dimension')
    
    # Add grid
    ax.set_xticks(np.arange(10))
    ax.set_yticks(np.arange(10))
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Save figure
    output_path = output_dir / "mood_heatmap.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"SUCCESS: Mood heatmap saved to {output_path}")
    return str(output_path)

# ================================================================================
# 2. scup_zone_animator.py
# ================================================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pathlib import Path

def run_scup_zone_animator(*args, **kwargs):
    """Generate and save an animated SCUP values plot with zone overlay"""
    # Create output directory
    output_dir = Path("visual/outputs/scup_zone_animator")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate synthetic SCUP data (random walk)
    np.random.seed(42)
    n_frames = 100
    time_points = 50
    
    # Initialize SCUP values
    scup_data = []
    current_value = 0.5
    
    for frame in range(n_frames):
        # Generate time series for this frame
        frame_data = []
        for t in range(time_points):
            # Random walk
            current_value += np.random.randn() * 0.02
            current_value = np.clip(current_value, 0, 1)
            frame_data.append(current_value)
        scup_data.append(frame_data)
    
    scup_data = np.array(scup_data)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Initialize plot elements
    x = np.arange(time_points)
    line, = ax.plot([], [], 'b-', linewidth=2)
    
    # Set up axes
    ax.set_xlim(0, time_points-1)
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlabel('Time')
    ax.set_ylabel('SCUP Value')
    ax.grid(True, alpha=0.3)
    
    # Define zones
    def get_zone(value):
        if value < 0.33:
            return 'calm', '#E8F4F8'
        elif value < 0.66:
            return 'active', '#FFF4E6'
        else:
            return 'surge', '#FFE6E6'
    
    # Animation function
    def animate(frame):
        data = scup_data[frame]
        line.set_data(x, data)
        
        # Determine zone based on average value
        avg_value = np.mean(data)
        zone, color = get_zone(avg_value)
        
        # Update background
        ax.set_facecolor(color)
        
        # Update title
        ax.set_title(f'SCUP + Zone Overlay - Frame {frame} [{zone}]')
        
        return line,
    
    # Create animation
    anim = animation.FuncAnimation(
        fig, animate, frames=n_frames, 
        interval=50, blit=True
    )
    
    # Save as GIF
    output_path = output_dir / "scup_zone_animation.gif"
    anim.save(output_path, writer='pillow', fps=20)
    plt.close()
    
    print(f"SUCCESS: SCUP zone animation saved to {output_path}")
    return str(output_path)

# ================================================================================
# 3. sigil_trace_visualizer.py
# ================================================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def run_sigil_trace_visualizer(*args, **kwargs):
    """Generate and save a 2D sigil trace visualization"""
    # Create output directory
    output_dir = Path("visual/outputs/sigil_trace_visualizer")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate synthetic parametric curve (noisy circle)
    np.random.seed(42)
    n_points = 1000
    t = np.linspace(0, 2*np.pi, n_points)
    
    # Base circle
    radius = 1.0
    noise_amplitude = 0.1
    
    # Add multiple frequency components for interesting patterns
    x = radius * np.cos(t) + noise_amplitude * np.sin(5*t) * np.cos(3*t)
    y = radius * np.sin(t) + noise_amplitude * np.cos(7*t) * np.sin(2*t)
    
    # Add some random noise
    x += np.random.randn(n_points) * 0.02
    y += np.random.randn(n_points) * 0.02
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Plot sigil trace
    ax.plot(x, y, 'b-', linewidth=1.5, alpha=0.8)
    
    # Add starting point marker
    ax.plot(x[0], y[0], 'go', markersize=10, label='Start')
    
    # Add ending point marker
    ax.plot(x[-1], y[-1], 'ro', markersize=10, label='End')
    
    # Style the plot
    ax.set_title('Sigil Trace Visualization')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend()
    
    # Set axis limits with some padding
    margin = 0.2
    ax.set_xlim(-radius-margin-noise_amplitude, radius+margin+noise_amplitude)
    ax.set_ylim(-radius-margin-noise_amplitude, radius+margin+noise_amplitude)
    
    # Save figure
    output_path = output_dir / "sigil_trace.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"SUCCESS: Sigil trace visualization saved to {output_path}")
    return str(output_path)

# ================================================================================
# 4. drift_vector_field.py
# ================================================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def run_drift_vector_field(*args, **kwargs):
    """Generate and save a 2D drift vector field visualization"""
    # Create output directory
    output_dir = Path("visual/outputs/drift_vector_field")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create meshgrid
    x = np.linspace(-2, 2, 20)
    y = np.linspace(-2, 2, 20)
    X, Y = np.meshgrid(x, y)
    
    # Define vector field (circular flow with drift)
    # u = -y, v = x creates circular flow
    # Add drift component
    drift_x = 0.2
    drift_y = 0.1
    
    U = -Y + drift_x
    V = X + drift_y
    
    # Add some noise for realism
    np.random.seed(42)
    noise_scale = 0.1
    U += np.random.randn(*U.shape) * noise_scale
    V += np.random.randn(*V.shape) * noise_scale
    
    # Calculate magnitude for coloring
    magnitude = np.sqrt(U**2 + V**2)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create quiver plot
    q = ax.quiver(X, Y, U, V, magnitude, 
                  scale_units='xy', scale=1, 
                  cmap='viridis', alpha=0.8)
    
    # Add colorbar
    cbar = plt.colorbar(q, ax=ax)
    cbar.set_label('Vector Magnitude', rotation=270, labelpad=15)
    
    # Add streamlines for better visualization
    ax.streamplot(X, Y, U, V, color='gray', 
                  density=0.5, linewidth=0.5, alpha=0.5)
    
    # Style the plot
    ax.set_title('Drift Vector Field')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Save figure
    output_path = output_dir / "drift_vector_field.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"SUCCESS: Drift vector field saved to {output_path}")
    return str(output_path)

# ================================================================================
# 5. attention_map.py
# ================================================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def run_attention_map(*args, **kwargs):
    """Generate and save a synthetic attention map heatmap"""
    output_dir = Path("visual/outputs/attention_map")
    output_dir.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    attention = np.random.rand(16, 16)
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(attention, cmap='viridis', vmin=0, vmax=1)
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Attention Weight', rotation=270, labelpad=15)
    ax.set_title('Attention Map')
    ax.set_xlabel('Key Index')
    ax.set_ylabel('Query Index')
    ax.set_xticks(np.arange(16))
    ax.set_yticks(np.arange(16))
    ax.grid(True, alpha=0.2, linestyle='--')
    output_path = output_dir / "attention_map.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Attention map saved to {output_path}")
    return str(output_path)

# ================================================================================
# 6. temporal_activity_raster.py
# ================================================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def run_temporal_activity_raster(*args, **kwargs):
    """Generate and save a temporal activity raster plot"""
    output_dir = Path("visual/outputs/temporal_activity_raster")
    output_dir.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    n_neurons = 32
    n_time = 100
    spikes = np.random.rand(n_neurons, n_time) < 0.05  # 5% chance of spike
    fig, ax = plt.subplots(figsize=(12, 6))
    for i in range(n_neurons):
        spike_times = np.where(spikes[i])[0]
        ax.vlines(spike_times, i + 0.5, i + 1.5, color='black', linewidth=1)
    ax.set_ylim(0.5, n_neurons + 0.5)
    ax.set_xlim(0, n_time)
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Neuron Index')
    ax.set_title('Temporal Activity Raster')
    ax.grid(True, axis='x', alpha=0.2, linestyle='--')
    output_path = output_dir / "temporal_activity_raster.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Temporal activity raster saved to {output_path}")
    return str(output_path)

# ================================================================================
# 7. latent_space_trajectory.py
# ================================================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def run_latent_space_trajectory(*args, **kwargs):
    """Generate and save a 2D latent space trajectory plot"""
    output_dir = Path("visual/outputs/latent_space_trajectory")
    output_dir.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    n_points = 200
    t = np.linspace(0, 4 * np.pi, n_points)
    x = np.cos(t) * (1 + 0.2 * np.random.randn(n_points)) + 0.1 * t
    y = np.sin(t) * (1 + 0.2 * np.random.randn(n_points)) + 0.1 * t
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.plot(x, y, 'b-', linewidth=2, alpha=0.8, label='Trajectory')
    ax.scatter(x[0], y[0], color='green', s=60, label='Start')
    ax.scatter(x[-1], y[-1], color='red', s=60, label='End')
    ax.set_title('Latent Space Trajectory')
    ax.set_xlabel('Latent Dim 1')
    ax.set_ylabel('Latent Dim 2')
    ax.legend()
    ax.grid(True, alpha=0.3, linestyle='--')
    output_path = output_dir / "latent_space_trajectory.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Latent space trajectory saved to {output_path}")
    return str(output_path)

# ================================================================================
# 8. loss_landscape.py
# ================================================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def run_loss_landscape(*args, **kwargs):
    """Generate and save a synthetic loss landscape with optimization path"""
    output_dir = Path("visual/outputs/loss_landscape")
    output_dir.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = (X ** 2 + Y ** 2) + 2 * np.sin(X) * np.cos(Y)  # Bowl + ripples
    # Simulate optimization path
    n_steps = 20
    path_x = np.linspace(2.5, -2.5, n_steps) + 0.2 * np.random.randn(n_steps)
    path_y = np.linspace(2.5, -2.5, n_steps) + 0.2 * np.random.randn(n_steps)
    path_z = (path_x ** 2 + path_y ** 2) + 2 * np.sin(path_x) * np.cos(path_y)
    fig, ax = plt.subplots(figsize=(10, 8))
    contour = ax.contourf(X, Y, Z, levels=30, cmap='plasma', alpha=0.85)
    cbar = plt.colorbar(contour, ax=ax)
    cbar.set_label('Loss Value', rotation=270, labelpad=15)
    ax.plot(path_x, path_y, 'w-o', linewidth=2, markersize=6, label='Optimization Path')
    ax.set_title('Loss Landscape')
    ax.set_xlabel('Parameter 1')
    ax.set_ylabel('Parameter 2')
    ax.legend()
    ax.grid(True, alpha=0.2, linestyle='--')
    output_path = output_dir / "loss_landscape.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Loss landscape saved to {output_path}")
    return str(output_path)

# ================================================================================
# Main execution wrapper (for testing all scripts)
# ================================================================================

if __name__ == "__main__":
    print("Running all DAWN visual process scripts...")
    print("-" * 50)
    
    # Run all visualization functions
    run_mood_heatmap()
    print("-" * 50)
    
    run_scup_zone_animator()
    print("-" * 50)
    
    run_sigil_trace_visualizer()
    print("-" * 50)
    
    run_drift_vector_field()
    print("-" * 50)
    
    run_attention_map()
    print("-" * 50)
    
    run_temporal_activity_raster()
    print("-" * 50)
    
    run_latent_space_trajectory()
    print("-" * 50)
    
    run_loss_landscape()
    print("-" * 50)
    
    print("\nAll visualizations completed successfully!")