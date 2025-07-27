#!/usr/bin/env python
"""
Unified DAWN Visual Process Runner
Run all or any of the 12 visual process scripts from a single CLI.
"""

import sys
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Optional imports
try:
    import networkx as nx
except ImportError:
    nx = None
try:
    from scipy import signal
except ImportError:
    signal = None
try:
    from matplotlib.patches import Circle
except ImportError:
    Circle = None
try:
    from matplotlib.collections import LineCollection
except ImportError:
    LineCollection = None

# 1. Drift Vector Field
def run_drift_vector_field(*args, **kwargs):
    output_dir = Path("visual/outputs/drift_vector_field")
    output_dir.mkdir(parents=True, exist_ok=True)
    x = np.linspace(-2, 2, 20)
    y = np.linspace(-2, 2, 20)
    X, Y = np.meshgrid(x, y)
    drift_x = 0.2
    drift_y = 0.1
    U = -Y + drift_x
    V = X + drift_y
    np.random.seed(42)
    noise_scale = 0.1
    U += np.random.randn(*U.shape) * noise_scale
    V += np.random.randn(*V.shape) * noise_scale
    magnitude = np.sqrt(U**2 + V**2)
    fig, ax = plt.subplots(figsize=(10, 8))
    q = ax.quiver(X, Y, U, V, magnitude, scale_units='xy', scale=1, cmap='viridis', alpha=0.8)
    cbar = plt.colorbar(q, ax=ax)
    cbar.set_label('Vector Magnitude', rotation=270, labelpad=15)
    ax.streamplot(X, Y, U, V, color='gray', density=0.5, linewidth=0.5, alpha=0.5)
    ax.set_title('Drift Vector Field')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, linestyle='--')
    output_path = output_dir / "drift_vector_field.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Drift vector field saved to {output_path}")
    return str(output_path)

# 2. Mood Heatmap
def run_mood_heatmap(*args, **kwargs):
    output_dir = Path("visual/outputs/mood_heatmap")
    output_dir.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    mood_data = np.random.rand(10, 10)
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(mood_data, cmap='RdYlBu_r', aspect='auto', vmin=0, vmax=1)
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Mood Intensity', rotation=270, labelpad=15)
    ax.set_title('Mood Heatmap')
    ax.set_xlabel('X Dimension')
    ax.set_ylabel('Y Dimension')
    ax.set_xticks(np.arange(10))
    ax.set_yticks(np.arange(10))
    ax.grid(True, alpha=0.3, linestyle='--')
    output_path = output_dir / "mood_heatmap.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Mood heatmap saved to {output_path}")
    return str(output_path)

# 3. Sigil Trace Visualizer
def run_sigil_trace_visualizer(*args, **kwargs):
    output_dir = Path("visual/outputs/sigil_trace_visualizer")
    output_dir.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    n_points = 1000
    t = np.linspace(0, 2*np.pi, n_points)
    radius = 1.0
    noise_amplitude = 0.1
    x = radius * np.cos(t) + noise_amplitude * np.sin(5*t) * np.cos(3*t)
    y = radius * np.sin(t) + noise_amplitude * np.cos(7*t) * np.sin(2*t)
    x += np.random.randn(n_points) * 0.02
    y += np.random.randn(n_points) * 0.02
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.plot(x, y, 'b-', linewidth=1.5, alpha=0.8)
    ax.plot(x[0], y[0], 'go', markersize=10, label='Start')
    ax.plot(x[-1], y[-1], 'ro', markersize=10, label='End')
    ax.set_title('Sigil Trace Visualization')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend()
    margin = 0.2
    ax.set_xlim(-radius-margin-noise_amplitude, radius+margin+noise_amplitude)
    ax.set_ylim(-radius-margin-noise_amplitude, radius+margin+noise_amplitude)
    output_path = output_dir / "sigil_trace.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Sigil trace visualization saved to {output_path}")
    return str(output_path)

# 4. SCUP Zone Animator
def run_scup_zone_animator(*args, **kwargs):
    output_dir = Path("visual/outputs/scup_zone_animator")
    output_dir.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    n_frames = 100
    time_points = 50
    scup_data = []
    current_value = 0.5
    for frame in range(n_frames):
        frame_data = []
        for t in range(time_points):
            current_value += np.random.randn() * 0.02
            current_value = np.clip(current_value, 0, 1)
            frame_data.append(current_value)
        scup_data.append(frame_data)
    scup_data = np.array(scup_data)
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(time_points)
    line, = ax.plot([], [], 'b-', linewidth=2)
    ax.set_xlim(0, time_points-1)
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlabel('Time')
    ax.set_ylabel('SCUP Value')
    ax.grid(True, alpha=0.3)
    def get_zone(value):
        if value < 0.33:
            return 'calm', '#E8F4F8'
        elif value < 0.66:
            return 'active', '#FFF4E6'
        else:
            return 'surge', '#FFE6E6'
    def animate(frame):
        data = scup_data[frame]
        line.set_data(x, data)
        avg_value = np.mean(data)
        zone, color = get_zone(avg_value)
        ax.set_facecolor(color)
        ax.set_title(f'SCUP + Zone Overlay - Frame {frame} [{zone}]')
        return line,
    anim = animation.FuncAnimation(fig, animate, frames=n_frames, interval=50, blit=True)
    output_path = output_dir / "scup_zone_animation.gif"
    anim.save(output_path, writer='pillow', fps=20)
    plt.close()
    print(f"SUCCESS: SCUP zone animation saved to {output_path}")
    return str(output_path)

# 5. Attention Map (extended version)
def run_attention_map(*args, **kwargs):
    output_dir = Path("visual/outputs/attention_map")
    output_dir.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    size = 16
    attention_data = np.random.rand(size, size) * 0.3
    for _ in range(3):
        cx, cy = np.random.randint(2, size-2, 2)
        for i in range(size):
            for j in range(size):
                dist = np.sqrt((i-cx)**2 + (j-cy)**2)
                attention_data[i, j] += np.exp(-dist/3) * 0.7
    attention_data = np.clip(attention_data, 0, 1)
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(attention_data, cmap='hot', aspect='auto', vmin=0, vmax=1)
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Attention Weight', rotation=270, labelpad=15)
    ax.set_title('Attention Map')
    ax.set_xlabel('Key Position')
    ax.set_ylabel('Query Position')
    ax.set_xticks(np.arange(0, size, 4))
    ax.set_yticks(np.arange(0, size, 4))
    ax.grid(True, alpha=0.3, linestyle='--', color='white', linewidth=0.5)
    output_path = output_dir / "attention_map.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Attention map saved to {output_path}")
    return str(output_path)

# 6. Temporal Activity Raster (extended version)
def run_temporal_activity_raster(*args, **kwargs):
    output_dir = Path("visual/outputs/temporal_activity_raster")
    output_dir.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    n_neurons = 32
    n_timesteps = 100
    spike_data = []
    for i in range(n_neurons):
        firing_rate = 0.02 + (i/n_neurons) * 0.08
        spikes = np.random.rand(n_timesteps) < firing_rate
        spike_data.append(spikes)
    spike_data = np.array(spike_data)
    fig, ax = plt.subplots(figsize=(12, 8))
    for i in range(n_neurons):
        spike_times = np.where(spike_data[i])[0]
        ax.vlines(spike_times, i-0.4, i+0.4, colors='black', linewidth=1)
    ax.set_title('Temporal Activity Raster')
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Neuron Index')
    ax.set_xlim(0, n_timesteps)
    ax.set_ylim(-1, n_neurons)
    ax.grid(True, axis='x', alpha=0.3, linestyle='--')
    for i in range(0, n_neurons, 8):
        ax.axhspan(i-0.5, i+7.5, alpha=0.1, color='blue' if (i//8)%2 else 'gray')
    output_path = output_dir / "temporal_activity_raster.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Temporal activity raster saved to {output_path}")
    return str(output_path)

# 7. Latent Space Trajectory (extended version)
def run_latent_space_trajectory(*args, **kwargs):
    output_dir = Path("visual/outputs/latent_space_trajectory")
    output_dir.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    n_points = 500
    t = np.linspace(0, 4*np.pi, n_points)
    radius = 0.1 + t/4
    x = radius * np.cos(t) + np.random.randn(n_points) * 0.05
    y = radius * np.sin(t) + np.random.randn(n_points) * 0.05
    if LineCollection is None:
        print("WARNING: matplotlib LineCollection not available, skipping color gradient.")
        return None
    fig, ax = plt.subplots(figsize=(8, 8))
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, cmap='viridis', linewidth=2)
    lc.set_array(t)
    line = ax.add_collection(lc)
    cbar = plt.colorbar(line, ax=ax)
    cbar.set_label('Time', rotation=270, labelpad=15)
    ax.plot(x[0], y[0], 'go', markersize=12, label='Start', zorder=5)
    ax.plot(x[-1], y[-1], 'ro', markersize=12, label='End', zorder=5)
    ax.set_title('Latent Space Trajectory')
    ax.set_xlabel('Latent Dimension 1')
    ax.set_ylabel('Latent Dimension 2')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend()
    margin = 0.5
    ax.set_xlim(x.min()-margin, x.max()+margin)
    ax.set_ylim(y.min()-margin, y.max()+margin)
    output_path = output_dir / "latent_space_trajectory.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Latent space trajectory saved to {output_path}")
    return str(output_path)

# 8. Loss Landscape (extended version)
def run_loss_landscape(*args, **kwargs):
    output_dir = Path("visual/outputs/loss_landscape")
    output_dir.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    x = np.linspace(-2, 2, 100)
    y = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(x, y)
    Z = 0.5 * (X**2 - Y**2) + 0.2 * np.sin(3*X) * np.cos(3*Y) + 0.1 * (X**2 + Y**2)
    n_steps = 50
    path_x = [1.5]
    path_y = [1.5]
    for i in range(n_steps-1):
        dx = 2 * path_x[-1] + 0.6 * np.cos(3*path_x[-1]) * np.cos(3*path_y[-1])
        dy = -2 * path_y[-1] - 0.6 * np.sin(3*path_x[-1]) * np.sin(3*path_y[-1])
        lr = 0.05
        path_x.append(path_x[-1] - lr * dx + np.random.randn() * 0.01)
        path_y.append(path_y[-1] - lr * dy + np.random.randn() * 0.01)
    fig, ax = plt.subplots(figsize=(10, 8))
    contour = ax.contour(X, Y, Z, levels=20, colors='black', alpha=0.4, linewidths=0.5)
    contourf = ax.contourf(X, Y, Z, levels=20, cmap='viridis', alpha=0.8)
    cbar = plt.colorbar(contourf, ax=ax)
    cbar.set_label('Loss Value', rotation=270, labelpad=15)
    ax.plot(path_x, path_y, 'r-', linewidth=2, label='Optimization Path')
    ax.plot(path_x[0], path_y[0], 'go', markersize=10, label='Start')
    ax.plot(path_x[-1], path_y[-1], 'ro', markersize=10, label='End')
    ax.set_title('Loss Landscape')
    ax.set_xlabel('Parameter 1')
    ax.set_ylabel('Parameter 2')
    ax.set_aspect('equal')
    ax.legend()
    output_path = output_dir / "loss_landscape.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Loss landscape saved to {output_path}")
    return str(output_path)

# 9. Correlation Matrix
def run_correlation_matrix(*args, **kwargs):
    output_dir = Path("visual/outputs/correlation_matrix")
    output_dir.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    n_vars = 10
    data = np.random.randn(100, n_vars)
    data[:, 1] = data[:, 0] * 0.8 + np.random.randn(100) * 0.2
    data[:, 2] = data[:, 0] * -0.6 + np.random.randn(100) * 0.3
    data[:, 4] = data[:, 3] * 0.7 + np.random.randn(100) * 0.3
    corr_matrix = np.corrcoef(data.T)
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Correlation Coefficient', rotation=270, labelpad=15)
    for i in range(n_vars):
        for j in range(n_vars):
            text = ax.text(j, i, f'{corr_matrix[i, j]:.2f}', ha='center', va='center', color='black' if abs(corr_matrix[i, j]) < 0.5 else 'white', fontsize=8)
    ax.set_title('Correlation Matrix')
    ax.set_xlabel('Variable Index')
    ax.set_ylabel('Variable Index')
    ax.set_xticks(range(n_vars))
    ax.set_yticks(range(n_vars))
    ax.set_xticklabels([f'V{i}' for i in range(n_vars)])
    ax.set_yticklabels([f'V{i}' for i in range(n_vars)])
    output_path = output_dir / "correlation_matrix.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Correlation matrix saved to {output_path}")
    return str(output_path)

# 10. Activation Histogram
def run_activation_histogram(*args, **kwargs):
    output_dir = Path("visual/outputs/activation_histogram")
    output_dir.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    normal_activations = np.random.randn(700) * 0.5 + 0.2
    sparse_activations = np.zeros(300)
    sparse_indices = np.random.choice(300, 50, replace=False)
    sparse_activations[sparse_indices] = np.random.exponential(0.5, 50)
    all_activations = np.concatenate([normal_activations, sparse_activations])
    fig, ax = plt.subplots(figsize=(10, 6))
    n, bins, patches = ax.hist(all_activations, bins=50, alpha=0.7, color='blue', edgecolor='black')
    mean_val = np.mean(all_activations)
    median_val = np.median(all_activations)
    ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.3f}')
    ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Median: {median_val:.3f}')
    ax.set_title('Activation Histogram')
    ax.set_xlabel('Activation Value')
    ax.set_ylabel('Frequency')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend()
    textstr = f'Total: {len(all_activations)}\nStd: {np.std(all_activations):.3f}\nSparsity: {(all_activations == 0).sum()/len(all_activations):.1%}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.7, 0.95, textstr, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=props)
    output_path = output_dir / "activation_histogram.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Activation histogram saved to {output_path}")
    return str(output_path)

# 11. State Transition Graph
def run_state_transition_graph(*args, **kwargs):
    if nx is None:
        print("WARNING: networkx not installed, skipping state transition graph.")
        return None
    output_dir = Path("visual/outputs/state_transition_graph")
    output_dir.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    G = nx.DiGraph()
    states = ['IDLE', 'INIT', 'PROC', 'WAIT', 'DONE']
    G.add_nodes_from(states)
    transitions = [
        ('IDLE', 'INIT', 0.8),
        ('IDLE', 'IDLE', 0.2),
        ('INIT', 'PROC', 0.9),
        ('INIT', 'IDLE', 0.1),
        ('PROC', 'WAIT', 0.6),
        ('PROC', 'DONE', 0.3),
        ('PROC', 'PROC', 0.1),
        ('WAIT', 'PROC', 0.7),
        ('WAIT', 'DONE', 0.3),
        ('DONE', 'IDLE', 1.0)
    ]
    for src, dst, weight in transitions:
        G.add_edge(src, dst, weight=weight)
    fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=3000, ax=ax)
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    nx.draw_networkx_edges(G, pos, width=[w*3 for w in weights], alpha=0.6, edge_color='gray', connectionstyle='arc3,rad=0.1', ax=ax, arrowsize=20, arrowstyle='->')
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold', ax=ax)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_labels = {k: f'{v:.1f}' for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8, ax=ax)
    ax.set_title('State Transition Graph')
    ax.axis('off')
    output_path = output_dir / "state_transition_graph.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: State transition graph saved to {output_path}")
    return str(output_path)

# 12. Anomaly Timeline
def run_anomaly_timeline(*args, **kwargs):
    output_dir = Path("visual/outputs/anomaly_timeline")
    output_dir.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    n_points = 200
    time = np.arange(n_points)
    signal_data = (np.sin(time * 0.1) * 10 + time * 0.05 + np.random.randn(n_points) * 2)
    anomaly_indices = np.random.choice(n_points, 15, replace=False)
    anomalies = np.zeros(n_points, dtype=bool)
    anomalies[anomaly_indices] = True
    signal_data[anomaly_indices] += np.random.randn(15) * 10
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})
    ax1.plot(time, signal_data, 'b-', linewidth=1.5, label='Signal', alpha=0.8)
    ax1.scatter(time[anomalies], signal_data[anomalies], color='red', s=100, marker='o', label='Anomalies', zorder=5, edgecolor='black')
    rolling_mean = np.convolve(signal_data, np.ones(10)/10, mode='same')
    rolling_std = np.array([signal_data[max(0,i-5):i+5].std() for i in range(n_points)])
    ax1.fill_between(time, rolling_mean - 2*rolling_std, rolling_mean + 2*rolling_std, alpha=0.2, color='blue')
    ax1.set_title('Anomaly Timeline')
    ax1.set_ylabel('Signal Value')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend()
    ax2.bar(time, anomalies.astype(int), color='red', alpha=0.7)
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Anomaly')
    ax2.set_ylim(0, 1.5)
    ax2.set_yticks([0, 1])
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_xlim(ax1.get_xlim())
    plt.tight_layout()
    output_path = output_dir / "anomaly_timeline.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Anomaly timeline saved to {output_path}")
    return str(output_path)

# --- CLI and main logic ---
visualizations = {
    "drift_vector_field": run_drift_vector_field,
    "mood_heatmap": run_mood_heatmap,
    "sigil_trace_visualizer": run_sigil_trace_visualizer,
    "scup_zone_animator": run_scup_zone_animator,
    "attention_map": run_attention_map,
    "temporal_activity_raster": run_temporal_activity_raster,
    "latent_space_trajectory": run_latent_space_trajectory,
    "loss_landscape": run_loss_landscape,
    "correlation_matrix": run_correlation_matrix,
    "activation_histogram": run_activation_histogram,
    "state_transition_graph": run_state_transition_graph,
    "anomaly_timeline": run_anomaly_timeline,
}

def main():
    if len(sys.argv) == 1:
        print("Running all 12 DAWN visual process scripts...")
        for name, func in visualizations.items():
            print("-" * 50)
            print(f"Running: {name}")
            try:
                func()
            except Exception as e:
                print(f"ERROR running {name}: {e}")
        print("\nAll visualizations completed.")
    elif len(sys.argv) == 2:
        arg = sys.argv[1].lower()
        if arg == "list":
            print("Available visualizations:")
            for name in visualizations:
                print(f"- {name}")
        elif arg in visualizations:
            print(f"Running: {arg}")
            try:
                visualizations[arg]()
            except Exception as e:
                print(f"ERROR running {arg}: {e}")
        else:
            print(f"Unknown visualization: {arg}")
            print("Use 'python run_all_visuals.py list' to see available options.")
    else:
        print("Usage:")
        print("  python run_all_visuals.py           # Run all visualizations")
        print("  python run_all_visuals.py <name>    # Run a specific visualization")
        print("  python run_all_visuals.py list      # List all visualizations")

if __name__ == "__main__":
    main() 