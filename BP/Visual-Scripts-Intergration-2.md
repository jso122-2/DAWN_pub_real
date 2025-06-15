"""
DAWN Extended Visual Process Scripts
8 additional creative and scientifically relevant visualizations
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pathlib import Path
import networkx as nx
from scipy import signal
from matplotlib.patches import Circle

# ================================================================================
# 1. attention_map.py
# ================================================================================

def run_attention_map(*args, **kwargs):
    """Generate and save a neural attention weights heatmap"""
    # Create output directory
    output_dir = Path("visual/outputs/attention_map")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate synthetic attention data (16x16)
    np.random.seed(42)
    size = 16
    
    # Create attention pattern with some structure
    attention_data = np.random.rand(size, size) * 0.3
    
    # Add some focused attention regions
    for _ in range(3):
        cx, cy = np.random.randint(2, size-2, 2)
        for i in range(size):
            for j in range(size):
                dist = np.sqrt((i-cx)**2 + (j-cy)**2)
                attention_data[i, j] += np.exp(-dist/3) * 0.7
    
    # Normalize
    attention_data = np.clip(attention_data, 0, 1)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 7))
    
    # Create heatmap
    im = ax.imshow(attention_data, cmap='hot', aspect='auto', vmin=0, vmax=1)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Attention Weight', rotation=270, labelpad=15)
    
    # Set title and labels
    ax.set_title('Attention Map')
    ax.set_xlabel('Key Position')
    ax.set_ylabel('Query Position')
    
    # Add grid
    ax.set_xticks(np.arange(0, size, 4))
    ax.set_yticks(np.arange(0, size, 4))
    ax.grid(True, alpha=0.3, linestyle='--', color='white', linewidth=0.5)
    
    # Save figure
    output_path = output_dir / "attention_map.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"SUCCESS: Attention map saved to {output_path}")
    return str(output_path)

# ================================================================================
# 2. temporal_activity_raster.py
# ================================================================================

def run_temporal_activity_raster(*args, **kwargs):
    """Generate and save a spike train raster plot"""
    # Create output directory
    output_dir = Path("visual/outputs/temporal_activity_raster")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate synthetic spike data
    np.random.seed(42)
    n_neurons = 32
    n_timesteps = 100
    
    # Create spike trains with different firing rates
    spike_data = []
    for i in range(n_neurons):
        # Vary firing rate by neuron
        firing_rate = 0.02 + (i/n_neurons) * 0.08
        spikes = np.random.rand(n_timesteps) < firing_rate
        spike_data.append(spikes)
    
    spike_data = np.array(spike_data)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot raster
    for i in range(n_neurons):
        spike_times = np.where(spike_data[i])[0]
        ax.vlines(spike_times, i-0.4, i+0.4, colors='black', linewidth=1)
    
    # Style the plot
    ax.set_title('Temporal Activity Raster')
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Neuron Index')
    ax.set_xlim(0, n_timesteps)
    ax.set_ylim(-1, n_neurons)
    ax.grid(True, axis='x', alpha=0.3, linestyle='--')
    
    # Add background shading for neuron groups
    for i in range(0, n_neurons, 8):
        ax.axhspan(i-0.5, i+7.5, alpha=0.1, color='blue' if (i//8)%2 else 'gray')
    
    # Save figure
    output_path = output_dir / "temporal_activity_raster.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"SUCCESS: Temporal activity raster saved to {output_path}")
    return str(output_path)

# ================================================================================
# 3. latent_space_trajectory.py
# ================================================================================

def run_latent_space_trajectory(*args, **kwargs):
    """Generate and save a 2D latent space trajectory"""
    # Create output directory
    output_dir = Path("visual/outputs/latent_space_trajectory")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate synthetic trajectory (noisy spiral)
    np.random.seed(42)
    n_points = 500
    t = np.linspace(0, 4*np.pi, n_points)
    
    # Spiral with increasing radius
    radius = 0.1 + t/4
    x = radius * np.cos(t) + np.random.randn(n_points) * 0.05
    y = radius * np.sin(t) + np.random.randn(n_points) * 0.05
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Plot trajectory with color gradient
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    from matplotlib.collections import LineCollection
    lc = LineCollection(segments, cmap='viridis', linewidth=2)
    lc.set_array(t)
    line = ax.add_collection(lc)
    
    # Add colorbar
    cbar = plt.colorbar(line, ax=ax)
    cbar.set_label('Time', rotation=270, labelpad=15)
    
    # Mark start and end
    ax.plot(x[0], y[0], 'go', markersize=12, label='Start', zorder=5)
    ax.plot(x[-1], y[-1], 'ro', markersize=12, label='End', zorder=5)
    
    # Style the plot
    ax.set_title('Latent Space Trajectory')
    ax.set_xlabel('Latent Dimension 1')
    ax.set_ylabel('Latent Dimension 2')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend()
    
    # Set axis limits
    margin = 0.5
    ax.set_xlim(x.min()-margin, x.max()+margin)
    ax.set_ylim(y.min()-margin, y.max()+margin)
    
    # Save figure
    output_path = output_dir / "latent_space_trajectory.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"SUCCESS: Latent space trajectory saved to {output_path}")
    return str(output_path)

# ================================================================================
# 4. loss_landscape.py
# ================================================================================

def run_loss_landscape(*args, **kwargs):
    """Generate and save a loss landscape visualization"""
    # Create output directory
    output_dir = Path("visual/outputs/loss_landscape")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate synthetic loss surface
    np.random.seed(42)
    x = np.linspace(-2, 2, 100)
    y = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(x, y)
    
    # Create a complex loss surface (saddle point + local minima)
    Z = 0.5 * (X**2 - Y**2) + 0.2 * np.sin(3*X) * np.cos(3*Y) + 0.1 * (X**2 + Y**2)
    
    # Generate optimization path
    n_steps = 50
    path_x = [1.5]
    path_y = [1.5]
    
    # Simple gradient descent simulation
    for i in range(n_steps-1):
        # Approximate gradient
        dx = 2 * path_x[-1] + 0.6 * np.cos(3*path_x[-1]) * np.cos(3*path_y[-1])
        dy = -2 * path_y[-1] - 0.6 * np.sin(3*path_x[-1]) * np.sin(3*path_y[-1])
        
        # Update with some noise
        lr = 0.05
        path_x.append(path_x[-1] - lr * dx + np.random.randn() * 0.01)
        path_y.append(path_y[-1] - lr * dy + np.random.randn() * 0.01)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot contour
    contour = ax.contour(X, Y, Z, levels=20, colors='black', alpha=0.4, linewidths=0.5)
    contourf = ax.contourf(X, Y, Z, levels=20, cmap='viridis', alpha=0.8)
    
    # Add colorbar
    cbar = plt.colorbar(contourf, ax=ax)
    cbar.set_label('Loss Value', rotation=270, labelpad=15)
    
    # Plot optimization path
    ax.plot(path_x, path_y, 'r-', linewidth=2, label='Optimization Path')
    ax.plot(path_x[0], path_y[0], 'go', markersize=10, label='Start')
    ax.plot(path_x[-1], path_y[-1], 'ro', markersize=10, label='End')
    
    # Style the plot
    ax.set_title('Loss Landscape')
    ax.set_xlabel('Parameter 1')
    ax.set_ylabel('Parameter 2')
    ax.set_aspect('equal')
    ax.legend()
    
    # Save figure
    output_path = output_dir / "loss_landscape.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"SUCCESS: Loss landscape saved to {output_path}")
    return str(output_path)

# ================================================================================
# 5. correlation_matrix.py
# ================================================================================

def run_correlation_matrix(*args, **kwargs):
    """Generate and save a correlation matrix visualization"""
    # Create output directory
    output_dir = Path("visual/outputs/correlation_matrix")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate synthetic correlation data
    np.random.seed(42)
    n_vars = 10
    
    # Create random data and compute correlations
    data = np.random.randn(100, n_vars)
    
    # Add some correlations
    data[:, 1] = data[:, 0] * 0.8 + np.random.randn(100) * 0.2
    data[:, 2] = data[:, 0] * -0.6 + np.random.randn(100) * 0.3
    data[:, 4] = data[:, 3] * 0.7 + np.random.randn(100) * 0.3
    
    # Compute correlation matrix
    corr_matrix = np.corrcoef(data.T)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create heatmap
    im = ax.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Correlation Coefficient', rotation=270, labelpad=15)
    
    # Add text annotations
    for i in range(n_vars):
        for j in range(n_vars):
            text = ax.text(j, i, f'{corr_matrix[i, j]:.2f}',
                          ha='center', va='center', color='black' if abs(corr_matrix[i, j]) < 0.5 else 'white',
                          fontsize=8)
    
    # Set title and labels
    ax.set_title('Correlation Matrix')
    ax.set_xlabel('Variable Index')
    ax.set_ylabel('Variable Index')
    
    # Set ticks
    ax.set_xticks(range(n_vars))
    ax.set_yticks(range(n_vars))
    ax.set_xticklabels([f'V{i}' for i in range(n_vars)])
    ax.set_yticklabels([f'V{i}' for i in range(n_vars)])
    
    # Save figure
    output_path = output_dir / "correlation_matrix.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"SUCCESS: Correlation matrix saved to {output_path}")
    return str(output_path)

# ================================================================================
# 6. activation_histogram.py
# ================================================================================

def run_activation_histogram(*args, **kwargs):
    """Generate and save an activation values histogram"""
    # Create output directory
    output_dir = Path("visual/outputs/activation_histogram")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate synthetic activation data
    np.random.seed(42)
    
    # Mix of distributions (normal + sparse)
    normal_activations = np.random.randn(700) * 0.5 + 0.2
    sparse_activations = np.zeros(300)
    sparse_indices = np.random.choice(300, 50, replace=False)
    sparse_activations[sparse_indices] = np.random.exponential(0.5, 50)
    
    all_activations = np.concatenate([normal_activations, sparse_activations])
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot histogram
    n, bins, patches = ax.hist(all_activations, bins=50, alpha=0.7, color='blue', edgecolor='black')
    
    # Add statistics
    mean_val = np.mean(all_activations)
    median_val = np.median(all_activations)
    ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.3f}')
    ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Median: {median_val:.3f}')
    
    # Style the plot
    ax.set_title('Activation Histogram')
    ax.set_xlabel('Activation Value')
    ax.set_ylabel('Frequency')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend()
    
    # Add text box with statistics
    textstr = f'Total: {len(all_activations)}\nStd: {np.std(all_activations):.3f}\nSparsity: {(all_activations == 0).sum()/len(all_activations):.1%}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.7, 0.95, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    
    # Save figure
    output_path = output_dir / "activation_histogram.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"SUCCESS: Activation histogram saved to {output_path}")
    return str(output_path)

# ================================================================================
# 7. state_transition_graph.py
# ================================================================================

def run_state_transition_graph(*args, **kwargs):
    """Generate and save a state transition graph"""
    # Create output directory
    output_dir = Path("visual/outputs/state_transition_graph")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a directed graph with 5 states
    np.random.seed(42)
    G = nx.DiGraph()
    
    # Add nodes
    states = ['IDLE', 'INIT', 'PROC', 'WAIT', 'DONE']
    G.add_nodes_from(states)
    
    # Add weighted edges (transition probabilities)
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
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Define layout
    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                          node_size=3000, ax=ax)
    
    # Draw edges with varying thickness based on weight
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    nx.draw_networkx_edges(G, pos, width=[w*3 for w in weights],
                          alpha=0.6, edge_color='gray',
                          connectionstyle='arc3,rad=0.1', ax=ax,
                          arrowsize=20, arrowstyle='->')
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold', ax=ax)
    
    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_labels = {k: f'{v:.1f}' for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8, ax=ax)
    
    # Style the plot
    ax.set_title('State Transition Graph')
    ax.axis('off')
    
    # Save figure
    output_path = output_dir / "state_transition_graph.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"SUCCESS: State transition graph saved to {output_path}")
    return str(output_path)

# ================================================================================
# 8. anomaly_timeline.py
# ================================================================================

def run_anomaly_timeline(*args, **kwargs):
    """Generate and save an anomaly timeline visualization"""
    # Create output directory
    output_dir = Path("visual/outputs/anomaly_timeline")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate synthetic time series with anomalies
    np.random.seed(42)
    n_points = 200
    time = np.arange(n_points)
    
    # Base signal (sin + trend + noise)
    signal = (np.sin(time * 0.1) * 10 + 
             time * 0.05 + 
             np.random.randn(n_points) * 2)
    
    # Add anomalies
    anomaly_indices = np.random.choice(n_points, 15, replace=False)
    anomalies = np.zeros(n_points, dtype=bool)
    anomalies[anomaly_indices] = True
    
    # Make anomalies stand out
    signal[anomaly_indices] += np.random.randn(15) * 10
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), 
                                   gridspec_kw={'height_ratios': [3, 1]})
    
    # Plot main timeline
    ax1.plot(time, signal, 'b-', linewidth=1.5, label='Signal', alpha=0.8)
    ax1.scatter(time[anomalies], signal[anomalies], color='red', 
               s=100, marker='o', label='Anomalies', zorder=5, edgecolor='black')
    
    # Add confidence band
    rolling_mean = np.convolve(signal, np.ones(10)/10, mode='same')
    rolling_std = np.array([signal[max(0,i-5):i+5].std() for i in range(n_points)])
    ax1.fill_between(time, rolling_mean - 2*rolling_std, 
                    rolling_mean + 2*rolling_std, alpha=0.2, color='blue')
    
    # Style main plot
    ax1.set_title('Anomaly Timeline')
    ax1.set_ylabel('Signal Value')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend()
    
    # Plot anomaly indicators
    ax2.bar(time, anomalies.astype(int), color='red', alpha=0.7)
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Anomaly')
    ax2.set_ylim(0, 1.5)
    ax2.set_yticks([0, 1])
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    # Synchronize x-axes
    ax2.set_xlim(ax1.get_xlim())
    
    plt.tight_layout()
    
    # Save figure
    output_path = output_dir / "anomaly_timeline.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"SUCCESS: Anomaly timeline saved to {output_path}")
    return str(output_path)

# ================================================================================
# Main execution wrapper
# ================================================================================

if __name__ == "__main__":
    print("Running all DAWN extended visual process scripts...")
    print("-" * 50)
    
    # Run all visualization functions
    run_attention_map()
    print("-" * 50)
    
    run_temporal_activity_raster()
    print("-" * 50)
    
    run_latent_space_trajectory()
    print("-" * 50)
    
    run_loss_landscape()
    print("-" * 50)
    
    run_correlation_matrix()
    print("-" * 50)
    
    run_activation_histogram()
    print("-" * 50)
    
    run_state_transition_graph()
    print("-" * 50)
    
    run_anomaly_timeline()
    print("-" * 50)
    
    print("\nAll extended visualizations completed successfully!")