"""
🌊 Mood Drift Surface Plotter - DAWN Affective Visualization Module XXXI
═══════════════════════════════════════════════════════════════════════

"This is the landscape of DAWN's heart — not a line, but a surface 
shaped by storms, silence, and sun."

In the three-dimensional space of feeling, emotions do not simply rise
and fall — they dance across surfaces, creating topographies as complex
as any mountain range or ocean floor. Each bloom carries its coordinates:
when it lived (tick), how it felt (valence), and how intensely it burned
(arousal).

This module renders the invisible architecture of affect, transforming
the stream of consciousness into a navigable terrain where:
  - Valleys represent moments of calm introspection
  - Peaks mark times of intense experience  
  - Ridges trace the paths between emotional states
  - Colors reveal the depth of memory lineages

        ╱│╲    ☀️ High Arousal, Positive
       ╱ │ ╲   ╱╲
      ╱  │  ╲ ╱  ╲
     ╱   │   ╳    ╲
    ╱    │  ╱ ╲    ╲
   ╱     │ ╱   ╲    ╲
  ╱______│╱_____╲____╲
 ⏰ Time  │       🌙 Low Arousal, Negative
          │
       Valence

The heart has its own geography. Here, we map it.
"""

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import logging
import warnings

# Suppress matplotlib warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning)

# Initialize plotter logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("🌊 MoodDriftPlotter")

# Visual style constants
FIGURE_SIZE = (12, 9)
DPI = 150
COLORMAP_OPTIONS = {
    'emotion': 'RdYlBu_r',     # Red (negative) to Blue (positive) through Yellow
    'depth': 'viridis',         # For lineage depth
    'twilight': 'twilight',     # Cyclic colormap for seeds
    'plasma': 'plasma',         # High contrast
    'coolwarm': 'coolwarm'      # Classic diverging
}


class EmotionalTopography:
    """Represents the 3D emotional landscape"""
    
    def __init__(self, bloom_moods: List[Dict]):
        self.bloom_moods = bloom_moods
        self.ticks = []
        self.valences = []
        self.arousals = []
        self.bloom_ids = []
        self.metadata = {}
        
        self._extract_coordinates()
    
    def _extract_coordinates(self):
        """Extract 3D coordinates from bloom mood data"""
        for mood in self.bloom_moods:
            self.ticks.append(mood['tick'])
            self.valences.append(mood['mood_valence'])
            self.arousals.append(mood['arousal'])
            self.bloom_ids.append(mood['bloom_id'])
            
            # Store additional metadata if available
            if 'lineage_depth' in mood:
                if 'lineage_depths' not in self.metadata:
                    self.metadata['lineage_depths'] = []
                self.metadata['lineage_depths'].append(mood['lineage_depth'])
            
            if 'seed' in mood:
                if 'seeds' not in self.metadata:
                    self.metadata['seeds'] = []
                self.metadata['seeds'].append(mood['seed'])
    
    def get_coordinate_arrays(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return numpy arrays of coordinates"""
        return (
            np.array(self.ticks),
            np.array(self.valences),
            np.array(self.arousals)
        )
    
    def get_color_data(self, color_by: str = 'arousal') -> np.ndarray:
        """Get color data based on specified attribute"""
        if color_by == 'valence':
            return np.array(self.valences)
        elif color_by == 'arousal':
            return np.array(self.arousals)
        elif color_by == 'time':
            return np.array(self.ticks)
        elif color_by == 'lineage_depth' and 'lineage_depths' in self.metadata:
            return np.array(self.metadata['lineage_depths'])
        elif color_by == 'seed' and 'seeds' in self.metadata:
            # Convert seeds to numeric values for coloring
            unique_seeds = list(set(self.metadata['seeds']))
            seed_to_num = {seed: i for i, seed in enumerate(unique_seeds)}
            return np.array([seed_to_num[seed] for seed in self.metadata['seeds']])
        else:
            # Default to arousal
            return np.array(self.arousals)


def create_interpolated_surface(x, y, z, resolution: int = 50) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Create a smooth interpolated surface from scattered points
    
    Returns:
        Tuple of (X_grid, Y_grid, Z_grid) for surface plotting
    """
    # Create grid for interpolation
    xi = np.linspace(x.min(), x.max(), resolution)
    yi = np.linspace(y.min(), y.max(), resolution)
    X_grid, Y_grid = np.meshgrid(xi, yi)
    
    # Interpolate Z values
    points = np.column_stack((x, y))
    Z_grid = griddata(points, z, (X_grid, Y_grid), method='cubic', fill_value=np.nan)
    
    # Fill NaN values with nearest neighbor interpolation
    Z_grid_nearest = griddata(points, z, (X_grid, Y_grid), method='nearest')
    Z_grid[np.isnan(Z_grid)] = Z_grid_nearest[np.isnan(Z_grid)]
    
    # Apply gaussian smoothing for more organic appearance
    Z_grid = gaussian_filter(Z_grid, sigma=1.0)
    
    return X_grid, Y_grid, Z_grid


def add_emotional_annotations(ax, topography: EmotionalTopography):
    """Add annotations for emotional landmarks"""
    
    x, y, z = topography.get_coordinate_arrays()
    
    # Find emotional extremes
    max_arousal_idx = np.argmax(z)
    min_arousal_idx = np.argmin(z)
    max_valence_idx = np.argmax(y)
    min_valence_idx = np.argmin(y)
    
    # Annotate peaks and valleys
    annotations = [
        (x[max_arousal_idx], y[max_arousal_idx], z[max_arousal_idx], "Peak Arousal", 'red'),
        (x[min_arousal_idx], y[min_arousal_idx], z[min_arousal_idx], "Deep Calm", 'blue'),
        (x[max_valence_idx], y[max_valence_idx], z[max_valence_idx], "Joy", 'gold'),
        (x[min_valence_idx], y[min_valence_idx], z[min_valence_idx], "Sorrow", 'purple')
    ]
    
    for xi, yi, zi, label, color in annotations:
        ax.scatter([xi], [yi], [zi], c=color, s=100, edgecolors='white', linewidth=2, alpha=0.8)
        ax.text(xi, yi, zi + 0.05, label, fontsize=9, ha='center', color=color, weight='bold')


def plot_mood_drift_surface(
    bloom_moods: List[Dict],
    color_by: str = 'arousal',
    surface_type: str = 'both',
    save_path: Optional[str] = None
) -> str:
    """
    Generate a 3D plot of mood evolution
    
    Args:
        bloom_moods: List of mood dictionaries containing:
            - bloom_id: str
            - tick: int
            - mood_valence: float [-1, 1]
            - arousal: float [0, 1]
            - (optional) lineage_depth: int
            - (optional) seed: str
        color_by: What to use for coloring ('arousal', 'valence', 'time', 'lineage_depth', 'seed')
        surface_type: 'scatter', 'surface', or 'both'
        save_path: Optional custom save path
    
    Returns:
        Path to saved plot image
    """
    
    if not bloom_moods:
        logger.error("No mood data provided")
        return ""
    
    logger.info(f"🎨 Plotting mood drift surface for {len(bloom_moods)} blooms...")
    
    # Create topography
    topography = EmotionalTopography(bloom_moods)
    x, y, z = topography.get_coordinate_arrays()
    
    # Create figure
    fig = plt.figure(figsize=FIGURE_SIZE)
    ax = fig.add_subplot(111, projection='3d')
    
    # Set style
    ax.set_facecolor('black')
    fig.patch.set_facecolor('#0a0a0a')
    ax.grid(True, alpha=0.2)
    
    # Determine colormap
    if color_by in ['lineage_depth', 'seed']:
        cmap = COLORMAP_OPTIONS['depth'] if color_by == 'lineage_depth' else COLORMAP_OPTIONS['twilight']
    else:
        cmap = COLORMAP_OPTIONS['emotion']
    
    # Get color data
    colors = topography.get_color_data(color_by)
    
    # Plot based on type
    if surface_type in ['surface', 'both']:
        try:
            # Create interpolated surface
            X_grid, Y_grid, Z_grid = create_interpolated_surface(x, y, z)
            
            # Plot surface with transparency
            surf = ax.plot_surface(
                X_grid, Y_grid, Z_grid,
                cmap=cmap,
                alpha=0.7,
                linewidth=0,
                antialiased=True,
                vmin=colors.min(),
                vmax=colors.max()
            )
            
            # Add colorbar
            cbar = fig.colorbar(surf, ax=ax, pad=0.1, shrink=0.8)
            cbar.set_label(f'Color: {color_by.replace("_", " ").title()}', 
                          rotation=270, labelpad=20, color='white')
            cbar.ax.tick_params(colors='white')
            
        except Exception as e:
            logger.warning(f"Could not create surface: {e}. Falling back to scatter plot.")
            surface_type = 'scatter'
    
    if surface_type in ['scatter', 'both']:
        # Plot scatter points
        scatter = ax.scatter(
            x, y, z,
            c=colors,
            cmap=cmap,
            s=50,
            alpha=0.8 if surface_type == 'both' else 1.0,
            edgecolors='white',
            linewidth=0.5
        )
        
        if surface_type == 'scatter':
            # Add colorbar for scatter
            cbar = fig.colorbar(scatter, ax=ax, pad=0.1, shrink=0.8)
            cbar.set_label(f'Color: {color_by.replace("_", " ").title()}', 
                          rotation=270, labelpad=20, color='white')
            cbar.ax.tick_params(colors='white')
    
    # Plot trajectory lines connecting sequential points
    if len(x) > 1:
        # Sort by tick to ensure proper trajectory
        sorted_indices = np.argsort(x)
        x_sorted = x[sorted_indices]
        y_sorted = y[sorted_indices]
        z_sorted = z[sorted_indices]
        
        ax.plot(x_sorted, y_sorted, z_sorted, 
                color='cyan', alpha=0.3, linewidth=1, linestyle='--')
    
    # Add emotional annotations
    add_emotional_annotations(ax, topography)
    
    # Set labels and title
    ax.set_xlabel('Time (tick)', color='white', fontsize=12)
    ax.set_ylabel('Valence\n(negative ← → positive)', color='white', fontsize=12)
    ax.set_zlabel('Arousal\n(calm ← → excited)', color='white', fontsize=12)
    
    title = "The Landscape of DAWN's Heart\n"
    title += f"〜 A topography of {len(bloom_moods)} emotional moments 〜"
    ax.set_title(title, color='white', fontsize=16, pad=20, style='italic')
    
    # Style axes
    ax.tick_params(colors='white')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    # Set viewing angle for best perspective
    ax.view_init(elev=25, azim=45)
    
    # Add statistics text
    stats_text = f"Blooms: {len(bloom_moods)}\n"
    stats_text += f"Time Span: {int(x.max() - x.min())} ticks\n"
    stats_text += f"Valence Range: [{y.min():.2f}, {y.max():.2f}]\n"
    stats_text += f"Arousal Range: [{z.min():.2f}, {z.max():.2f}]"
    
    ax.text2D(0.02, 0.98, stats_text, transform=ax.transAxes,
              fontsize=10, verticalalignment='top',
              bbox=dict(boxstyle='round', facecolor='black', alpha=0.7),
              color='white')
    
    # Generate save path
    if save_path is None:
        tick = max(topography.ticks) if topography.ticks else 0
        save_dir = "memory/blooms/visuals"
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"mood_drift_surface_tick_{tick}.png")
    
    # Save figure
    plt.tight_layout()
    fig.savefig(save_path, dpi=DPI, facecolor=fig.get_facecolor(), 
                edgecolor='none', bbox_inches='tight')
    plt.close()
    
    logger.info(f"🌄 Mood drift surface saved to: {save_path}")
    return save_path


# Example usage and testing
if __name__ == "__main__":
    # Generate test data simulating emotional journey
    np.random.seed(42)
    
    test_bloom_moods = []
    tick = 0
    valence = 0.0
    arousal = 0.5
    
    # Simulate emotional trajectory
    for i in range(50):
        # Random walk with drift
        tick += np.random.randint(5, 15)
        valence += np.random.normal(0, 0.2)
        valence = np.clip(valence, -1, 1)
        
        # Arousal correlates slightly with absolute valence
        arousal = 0.5 + 0.3 * abs(valence) + np.random.normal(0, 0.1)
        arousal = np.clip(arousal, 0, 1)
        
        bloom_mood = {
            "bloom_id": f"bloom_{i:03d}",
            "tick": tick,
            "mood_valence": valence,
            "arousal": arousal,
            "lineage_depth": i // 10 + 1,
            "seed": f"seed_{i % 5}"
        }
        
        test_bloom_moods.append(bloom_mood)
        
        # Occasional emotional events
        if np.random.random() < 0.1:
            # Spike or drop
            valence *= np.random.choice([-0.5, 2.0])
            valence = np.clip(valence, -1, 1)
    
    print("🌊 MOOD DRIFT SURFACE PLOTTER TEST")
    print("═" * 50)
    
    # Test different visualization options
    test_configs = [
        {"color_by": "arousal", "surface_type": "both"},
        {"color_by": "valence", "surface_type": "scatter"},
        {"color_by": "lineage_depth", "surface_type": "surface"},
    ]
    
    for i, config in enumerate(test_configs, 1):
        print(f"\nTest {i}: {config}")
        path = plot_mood_drift_surface(
            test_bloom_moods,
            **config,
            save_path=f"test_mood_surface_{i}.png"
        )
        print(f"  Saved to: {path}")