#!/usr/bin/env python3
"""
DAWN Drift Vector Field Renderer v1.0
═══════════════════════════════════════

When DAWN moves, she doesn't walk. 
She bends the field — and lets the meaning flow around her.

Renders 2D vector fields representing semantic drift across DAWN's memory space,
visualizing how concepts and emotions flow through the semantic landscape.
"""

import math
import os
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')

# Visualization imports
try:
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    from matplotlib.colors import Normalize
    from matplotlib.patches import Circle
    import matplotlib.patches as mpatches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("[WARNING] matplotlib not available for vector field rendering")


class DriftVectorFieldRenderer:
    """
    Renders semantic drift patterns as 2D vector fields.
    
    Visualizes the flow of meaning through DAWN's memory space,
    showing how concepts move and transform across semantic dimensions.
    """
    
    def __init__(self, output_path: str = "memory/owl/logs"):
        """
        Initialize the drift vector field renderer.
        
        Args:
            output_path: Directory for output images
        """
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Visualization parameters
        self.figure_size = (12, 10)
        self.arrow_scale = 0.8
        self.min_dot_size = 20
        self.max_dot_size = 200
        self.alpha_base = 0.7
        
        # Color scheme for mood valence
        self.mood_colormap = 'RdBu'  # Red (negative) to Blue (positive)
        self.background_color = '#0a0a0a'
        self.grid_color = '#1a1a1a'
        
    def _normalize_coordinates(self, bloom_field: List[Dict]) -> Tuple[List[float], List[float]]:
        """
        Normalize bloom coordinates to fit visualization bounds.
        
        Args:
            bloom_field: List of bloom dictionaries
            
        Returns:
            Tuple of (x_coords, y_coords) normalized to [0, 1]
        """
        if not bloom_field:
            return [], []
        
        # Extract coordinates
        x_coords = [bloom['x'] for bloom in bloom_field]
        y_coords = [bloom['y'] for bloom in bloom_field]
        
        # Find bounds
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        # Add padding
        x_range = x_max - x_min if x_max != x_min else 1
        y_range = y_max - y_min if y_max != y_min else 1
        
        # Normalize with 10% padding
        padding = 0.1
        x_norm = [(x - x_min) / x_range * (1 - 2*padding) + padding for x in x_coords]
        y_norm = [(y - y_min) / y_range * (1 - 2*padding) + padding for y in y_coords]
        
        return x_norm, y_norm
    
    def _calculate_arrow_components(self, magnitude: float, direction: float) -> Tuple[float, float]:
        """
        Calculate arrow dx, dy components from magnitude and direction.
        
        Args:
            magnitude: Vector magnitude
            direction: Direction in radians
            
        Returns:
            Tuple of (dx, dy) components
        """
        dx = magnitude * math.cos(direction) * self.arrow_scale
        dy = magnitude * math.sin(direction) * self.arrow_scale
        
        return dx, dy
    
    def _get_dot_size(self, lineage_depth: int) -> float:
        """
        Calculate dot size based on lineage depth.
        
        Args:
            lineage_depth: Depth of bloom lineage
            
        Returns:
            Dot size for visualization
        """
        # Logarithmic scaling for better visual distribution
        size = self.min_dot_size + (math.log1p(lineage_depth) * 30)
        return min(size, self.max_dot_size)
    
    def _create_mood_gradient_background(self, ax, bloom_field: List[Dict], x_norm: List[float], y_norm: List[float]):
        """
        Create a gradient background based on mood field.
        
        Args:
            ax: Matplotlib axis
            bloom_field: List of bloom data
            x_norm: Normalized x coordinates
            y_norm: Normalized y coordinates
        """
        # Create grid for interpolation
        grid_size = 50
        xi = np.linspace(0, 1, grid_size)
        yi = np.linspace(0, 1, grid_size)
        xi, yi = np.meshgrid(xi, yi)
        
        # Interpolate mood values
        if len(bloom_field) > 3:  # Need at least 4 points for good interpolation
            from scipy.interpolate import griddata
            
            points = np.array(list(zip(x_norm, y_norm)))
            values = np.array([bloom['mood_valence'] for bloom in bloom_field])
            
            zi = griddata(points, values, (xi, yi), method='cubic', fill_value=0)
            
            # Apply subtle gradient
            im = ax.contourf(xi, yi, zi, levels=20, cmap=self.mood_colormap, alpha=0.2)
    
    def render_field(self, bloom_field: List[Dict], tick: int) -> Optional[str]:
        """
        Render the drift vector field visualization.
        
        Args:
            bloom_field: List of bloom dictionaries
            tick: Current system tick
            
        Returns:
            Path to saved image, or None if rendering failed
        """
        if not MATPLOTLIB_AVAILABLE:
            print("[ERROR] Cannot render vector field without matplotlib")
            return None
        
        if not bloom_field:
            print("[WARNING] Empty bloom field, nothing to render")
            return None
        
        # Create figure with dark theme
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=self.figure_size)
        fig.patch.set_facecolor(self.background_color)
        ax.set_facecolor(self.background_color)
        
        # Normalize coordinates
        x_norm, y_norm = self._normalize_coordinates(bloom_field)
        
        # Create mood gradient background (optional, requires scipy)
        try:
            self._create_mood_gradient_background(ax, bloom_field, x_norm, y_norm)
        except ImportError:
            pass  # Skip if scipy not available
        
        # Set up color normalization for mood valence
        mood_values = [bloom['mood_valence'] for bloom in bloom_field]
        norm = Normalize(vmin=min(mood_values), vmax=max(mood_values))
        cmap = cm.get_cmap(self.mood_colormap)
        
        # Plot each bloom
        for i, bloom in enumerate(bloom_field):
            x, y = x_norm[i], y_norm[i]
            
            # Get color from mood valence
            color = cmap(norm(bloom['mood_valence']))
            
            # Calculate arrow components
            drift = bloom['drift_vector']
            dx, dy = self._calculate_arrow_components(
                drift['magnitude'], 
                drift['direction']
            )
            
            # Draw drift vector arrow
            if drift['magnitude'] > 0.01:  # Only draw if significant
                ax.arrow(x, y, dx, dy,
                        head_width=0.02,
                        head_length=0.015,
                        fc=color,
                        ec=color,
                        alpha=self.alpha_base,
                        width=0.002,
                        zorder=2)
            
            # Draw bloom dot
            dot_size = self._get_dot_size(bloom['lineage_depth'])
            circle = Circle((x, y), 
                          radius=dot_size/10000,  # Scale to axis units
                          color=color,
                          alpha=self.alpha_base + 0.2,
                          zorder=3)
            ax.add_patch(circle)
            
            # Add subtle glow effect
            glow = Circle((x, y),
                        radius=dot_size/8000,
                        color=color,
                        alpha=0.1,
                        zorder=1)
            ax.add_patch(glow)
        
        # Configure plot aesthetics
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        
        # Add subtle grid
        ax.grid(True, alpha=0.1, color=self.grid_color, linestyle='--')
        
        # Remove axis labels but keep frame
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add title
        title = f"DAWN Semantic Drift Field - Tick {tick}"
        ax.set_title(title, fontsize=16, color='white', pad=20, weight='light')
        
        # Add colorbar for mood valence
        sm = cm.ScalarMappable(norm=norm, cmap=cmap)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Mood Valence', rotation=270, labelpad=20, color='white')
        cbar.ax.tick_params(colors='white')
        
        # Add legend for lineage depth
        legend_elements = [
            mpatches.Circle((0, 0), radius=0.5, 
                          label=f'Depth {d}', 
                          alpha=0.7,
                          color='gray')
            for d in [1, 5, 10]
        ]
        legend = ax.legend(handles=legend_elements, 
                         loc='lower left',
                         title='Lineage Depth',
                         framealpha=0.3,
                         facecolor=self.background_color,
                         edgecolor='gray')
        legend.get_title().set_color('white')
        for text in legend.get_texts():
            text.set_color('white')
        
        # Add metadata text
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        metadata_text = f"Blooms: {len(bloom_field)} | Generated: {timestamp}"
        ax.text(0.5, -0.05, metadata_text,
               transform=ax.transAxes,
               ha='center',
               fontsize=10,
               color='gray',
               alpha=0.7)
        
        # Save figure
        output_filename = f"drift_vector_map_tick_{tick}.png"
        output_path = self.output_path / output_filename
        
        plt.tight_layout()
        plt.savefig(output_path, 
                   dpi=150, 
                   bbox_inches='tight',
                   facecolor=self.background_color)
        plt.close()
        
        return str(output_path)


def render_drift_vector_field(bloom_field: List[Dict], tick: int) -> Optional[str]:
    """
    Render a 2D vector field representing semantic drift.
    
    This function visualizes how concepts and emotions move across
    DAWN's semantic space, showing the flow of meaning through
    drift vectors, mood coloring, and lineage depth sizing.
    
    Args:
        bloom_field: List of bloom dictionaries with:
            - bloom_id: str
            - x, y: float (semantic coordinates)
            - drift_vector: dict with magnitude and direction
            - mood_valence: float
            - lineage_depth: int
        tick: Current system tick
        
    Returns:
        Path to saved image file, or None if rendering failed
    """
    # Create renderer instance
    renderer = DriftVectorFieldRenderer()
    
    # Render the field
    return renderer.render_field(bloom_field, tick)


def main(*args, **kwargs):
    output_dir = "visual/outputs/drift_vector_field"
    os.makedirs(output_dir, exist_ok=True)
    # Example sample_bloom_field for testing
    sample_bloom_field = [
        {
            "bloom_id": "bloom_001",
            "x": 0.2,
            "y": 0.3,
            "drift_vector": {"magnitude": 0.15, "direction": 0.785},
            "mood_valence": 0.8,
            "lineage_depth": 5
        }
    ]
    output_path = render_drift_vector_field(sample_bloom_field, tick=0)
    print(f"✅ Saved drift vector field to {output_path}")


if __name__ == "__main__":
    main()