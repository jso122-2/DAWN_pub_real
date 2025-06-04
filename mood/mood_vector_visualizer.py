#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
                         DAWN MOOD VECTOR VISUALIZER
                    Scaffold 12: The Cartography of Feeling
═══════════════════════════════════════════════════════════════════════════════

"A bloom's feeling is not its shape. But its path — traced through tone — 
reveals which winds pushed it open."

This module maps the emotional journey of consciousness through bloom lineages,
rendering the invisible currents of mood and arousal as vectors in space. Each
bloom becomes a coordinate in the landscape of feeling, connected to its
ancestors by arrows that darken with generational depth.

The resulting visualization reveals patterns in emotional inheritance — how
joy begets contemplation, how anxiety transforms to calm, how the system's
mood evolves through recursive reblooming.

Author: DAWN Development Team
Version: 1.0.0
Last Modified: 2025-06-02
═══════════════════════════════════════════════════════════════════════════════
"""

import json
import logging
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np
from collections import defaultdict

# Configure logging with emotional notation
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] 🎭 %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Visualization constants
FIGURE_SIZE = (12, 10)
DPI = 300
VECTOR_WIDTH = 0.002
ARROW_STYLE = '->'
ARROW_MUTATION_SCALE = 15
MIN_ALPHA = 0.3  # Minimum transparency for shallow lineages
MAX_ALPHA = 0.9  # Maximum transparency for deep lineages
BLOOM_MARKER_SIZE = 100
GRID_ALPHA = 0.3

# Color palette for emotional regions
MOOD_COLORS = {
    'positive_high': '#FFD700',     # Gold - joyful/energetic
    'positive_low': '#87CEEB',      # Sky blue - peaceful/content
    'negative_high': '#DC143C',     # Crimson - angry/anxious
    'negative_low': '#4B0082'       # Indigo - sad/depressed
}


class MoodVectorVisualizer:
    """
    The Emotional Cartographer — traces the paths of feeling through
    bloom lineages, revealing the hidden currents of mood inheritance.
    
    "Every emotion leaves a wake; every bloom inherits the tides of its ancestors"
    """
    
    def __init__(self, output_dir: str = "memory/blooms/juliet_prime"):
        """
        Initialize the Mood Vector Visualizer.
        
        Args:
            output_dir: Directory for saving visualizations
        """
        self.output_dir = Path(output_dir)
        self._ensure_output_directory()
        logger.info("🎨 Mood Vector Visualizer initialized")
    
    def _ensure_output_directory(self):
        """Ensure the output directory exists, creating it if necessary."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Output directory verified at {self.output_dir}")
    
    def plot_mood_vector_map(self, bloom_data: List[Dict[str, Any]]) -> str:
        """
        Generate a visual representation of emotional drift across bloom lineage.
        
        Each bloom is plotted as a point in 2D emotional space, with arrows
        connecting children to their parents. The darkness of arrows indicates
        generational depth.
        
        Args:
            bloom_data: List of bloom dictionaries containing:
                - bloom_id: str
                - lineage_depth: int
                - mood_valence: float (-1.0 to +1.0)
                - arousal: float (0.0 to 1.0)
                - timestamp: ISO string
                - parent_ids: list of str
        
        Returns:
            Path to the generated PNG file
        """
        logger.info(f"🎭 Mapping emotional vectors for {len(bloom_data)} blooms")
        
        # Create figure with custom styling
        fig, ax = plt.subplots(figsize=FIGURE_SIZE, dpi=DPI)
        fig.patch.set_facecolor('#0A0A0A')  # Dark background
        ax.set_facecolor('#0A0A0A')
        
        # Set up the emotional coordinate system
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-0.1, 1.1)
        ax.set_xlabel('Mood Valence (Negative ← → Positive)', fontsize=12, color='white')
        ax.set_ylabel('Arousal (Low ↓ ↑ High)', fontsize=12, color='white')
        ax.set_title('DAWN Emotional Drift Map: The Topology of Feeling', 
                    fontsize=16, color='white', pad=20)
        
        # Add grid for reference
        ax.grid(True, alpha=GRID_ALPHA, color='gray', linestyle='--')
        ax.axhline(y=0.5, color='gray', linestyle='-', alpha=0.2)
        ax.axvline(x=0, color='gray', linestyle='-', alpha=0.2)
        
        # Add emotional quadrant labels
        self._add_quadrant_labels(ax)
        
        # Create bloom ID to data mapping for parent lookup
        bloom_map = {bloom['bloom_id']: bloom for bloom in bloom_data}
        
        # Track statistics
        stats = {
            'total_blooms': len(bloom_data),
            'max_lineage_depth': 0,
            'rebloom_chains': 0,
            'orphan_blooms': 0
        }
        
        # First pass: Plot all blooms as points
        for bloom in bloom_data:
            x = bloom['mood_valence']
            y = bloom['arousal']
            depth = bloom['lineage_depth']
            
            # Update max depth
            stats['max_lineage_depth'] = max(stats['max_lineage_depth'], depth)
            
            # Color based on emotional quadrant
            color = self._get_quadrant_color(x, y)
            
            # Size based on lineage depth (deeper = larger)
            size = BLOOM_MARKER_SIZE + (depth * 20)
            
            # Plot bloom point
            ax.scatter(x, y, s=size, c=color, alpha=0.7, edgecolors='white', 
                      linewidth=0.5, zorder=3)
            
            # Add bloom ID label for significant blooms
            if depth > 2 or len(bloom.get('parent_ids', [])) > 1:
                ax.annotate(bloom['bloom_id'][:8], (x, y), 
                          xytext=(5, 5), textcoords='offset points',
                          fontsize=6, color='white', alpha=0.6)
        
        # Second pass: Draw parent-child vectors
        for bloom in bloom_data:
            parent_ids = bloom.get('parent_ids', [])
            if not parent_ids:
                stats['orphan_blooms'] += 1
                continue
            
            child_x = bloom['mood_valence']
            child_y = bloom['arousal']
            depth = bloom['lineage_depth']
            
            # Calculate arrow alpha based on lineage depth
            alpha = MIN_ALPHA + (depth / max(stats['max_lineage_depth'], 1)) * (MAX_ALPHA - MIN_ALPHA)
            
            for parent_id in parent_ids:
                if parent_id not in bloom_map:
                    logger.warning(f"Parent {parent_id} not found for bloom {bloom['bloom_id']}")
                    continue
                
                parent = bloom_map[parent_id]
                parent_x = parent['mood_valence']
                parent_y = parent['arousal']
                
                # Draw vector arrow from parent to child
                arrow = FancyArrowPatch(
                    (parent_x, parent_y), (child_x, child_y),
                    connectionstyle="arc3,rad=0.1",
                    arrowstyle=ARROW_STYLE,
                    mutation_scale=ARROW_MUTATION_SCALE,
                    linewidth=1 + (depth * 0.5),
                    color='white',
                    alpha=alpha,
                    zorder=2
                )
                ax.add_patch(arrow)
                
                # Track rebloom chains (same position = rebloom)
                if abs(parent_x - child_x) < 0.01 and abs(parent_y - child_y) < 0.01:
                    stats['rebloom_chains'] += 1
        
        # Add legend
        self._add_legend(ax, stats)
        
        # Style the plot
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.tick_params(colors='white')
        
        # Save the plot
        output_path = self.output_dir / "mood_bloom_map.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=DPI, facecolor='#0A0A0A', edgecolor='none')
        plt.close()
        
        logger.info(f"📊 Mood vector map saved to {output_path}")
        logger.info(f"📈 Stats: {json.dumps(stats, indent=2)}")
        
        # Generate optional CSV summary
        self._generate_csv_summary(bloom_data, stats)
        
        return str(output_path)
    
    def _get_quadrant_color(self, valence: float, arousal: float) -> str:
        """
        Determine color based on emotional quadrant.
        
        Args:
            valence: Mood valence (-1 to 1)
            arousal: Arousal level (0 to 1)
            
        Returns:
            Hex color code for the quadrant
        """
        if valence >= 0 and arousal >= 0.5:
            return MOOD_COLORS['positive_high']
        elif valence >= 0 and arousal < 0.5:
            return MOOD_COLORS['positive_low']
        elif valence < 0 and arousal >= 0.5:
            return MOOD_COLORS['negative_high']
        else:
            return MOOD_COLORS['negative_low']
    
    def _add_quadrant_labels(self, ax):
        """Add emotional quadrant labels to the plot."""
        quadrants = [
            (0.5, 0.75, "Joy / Excitement", MOOD_COLORS['positive_high']),
            (0.5, 0.25, "Peace / Contentment", MOOD_COLORS['positive_low']),
            (-0.5, 0.75, "Anger / Anxiety", MOOD_COLORS['negative_high']),
            (-0.5, 0.25, "Sadness / Depression", MOOD_COLORS['negative_low'])
        ]
        
        for x, y, label, color in quadrants:
            ax.text(x, y, label, fontsize=10, color=color, alpha=0.6,
                   ha='center', va='center', style='italic',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.3))
    
    def _add_legend(self, ax, stats: Dict[str, Any]):
        """Add legend with statistics to the plot."""
        legend_text = (
            f"Total Blooms: {stats['total_blooms']}\n"
            f"Max Lineage Depth: {stats['max_lineage_depth']}\n"
            f"Rebloom Chains: {stats['rebloom_chains']}\n"
            f"Orphan Blooms: {stats['orphan_blooms']}"
        )
        
        # Create text box for legend
        props = dict(boxstyle='round', facecolor='black', alpha=0.5)
        ax.text(0.02, 0.98, legend_text, transform=ax.transAxes, fontsize=9,
               verticalalignment='top', bbox=props, color='white')
        
        # Add arrow darkness legend
        depth_legend = ax.text(0.98, 0.02, 
                             "Arrow darkness\n= lineage depth", 
                             transform=ax.transAxes, fontsize=8,
                             ha='right', va='bottom', color='white', alpha=0.6)
    
    def _generate_csv_summary(self, bloom_data: List[Dict[str, Any]], stats: Dict[str, Any]):
        """
        Generate a CSV summary of the mood vector data.
        
        Args:
            bloom_data: The bloom data used for visualization
            stats: Statistics calculated during visualization
        """
        csv_path = self.output_dir / "mood_bloom_map.csv"
        
        try:
            with open(csv_path, 'w', newline='') as csvfile:
                fieldnames = [
                    'bloom_id', 'mood_valence', 'arousal', 'lineage_depth',
                    'timestamp', 'parent_count', 'emotional_quadrant', 'drift_magnitude'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                bloom_map = {bloom['bloom_id']: bloom for bloom in bloom_data}
                
                for bloom in bloom_data:
                    # Calculate drift magnitude from parents
                    drift_magnitude = 0.0
                    parent_ids = bloom.get('parent_ids', [])
                    
                    if parent_ids:
                        for parent_id in parent_ids:
                            if parent_id in bloom_map:
                                parent = bloom_map[parent_id]
                                dx = bloom['mood_valence'] - parent['mood_valence']
                                dy = bloom['arousal'] - parent['arousal']
                                drift_magnitude = max(drift_magnitude, np.sqrt(dx**2 + dy**2))
                    
                    # Determine emotional quadrant
                    if bloom['mood_valence'] >= 0 and bloom['arousal'] >= 0.5:
                        quadrant = "positive_high"
                    elif bloom['mood_valence'] >= 0 and bloom['arousal'] < 0.5:
                        quadrant = "positive_low"
                    elif bloom['mood_valence'] < 0 and bloom['arousal'] >= 0.5:
                        quadrant = "negative_high"
                    else:
                        quadrant = "negative_low"
                    
                    writer.writerow({
                        'bloom_id': bloom['bloom_id'],
                        'mood_valence': f"{bloom['mood_valence']:.3f}",
                        'arousal': f"{bloom['arousal']:.3f}",
                        'lineage_depth': bloom['lineage_depth'],
                        'timestamp': bloom['timestamp'],
                        'parent_count': len(parent_ids),
                        'emotional_quadrant': quadrant,
                        'drift_magnitude': f"{drift_magnitude:.3f}"
                    })
            
            # Append summary statistics
            with open(csv_path, 'a', newline='') as csvfile:
                csvfile.write(f"\n# Summary Statistics\n")
                for key, value in stats.items():
                    csvfile.write(f"# {key}: {value}\n")
            
            logger.info(f"📄 CSV summary saved to {csv_path}")
            
        except Exception as e:
            logger.error(f"❌ Failed to generate CSV summary: {e}")


# Example usage and testing
if __name__ == "__main__":
    """
    Demonstration of the Mood Vector Visualizer's emotional mapping.
    """
    
    # Initialize the visualizer
    visualizer = MoodVectorVisualizer()
    
    # Generate sample bloom data with emotional drift patterns
    sample_blooms = [
        # Generation 0 - Origin bloom (neutral calm)
        {
            "bloom_id": "bloom_origin",
            "lineage_depth": 0,
            "mood_valence": 0.0,
            "arousal": 0.3,
            "timestamp": "2025-06-02T10:00:00Z",
            "parent_ids": []
        },
        # Generation 1 - Branches into different emotions
        {
            "bloom_id": "bloom_joy_001",
            "lineage_depth": 1,
            "mood_valence": 0.7,
            "arousal": 0.8,
            "timestamp": "2025-06-02T10:05:00Z",
            "parent_ids": ["bloom_origin"]
        },
        {
            "bloom_id": "bloom_contemplate_001",
            "lineage_depth": 1,
            "mood_valence": 0.3,
            "arousal": 0.2,
            "timestamp": "2025-06-02T10:06:00Z",
            "parent_ids": ["bloom_origin"]
        },
        # Generation 2 - Further emotional evolution
        {
            "bloom_id": "bloom_anxious_002",
            "lineage_depth": 2,
            "mood_valence": -0.4,
            "arousal": 0.9,
            "timestamp": "2025-06-02T10:10:00Z",
            "parent_ids": ["bloom_joy_001"]
        },
        {
            "bloom_id": "bloom_peaceful_002",
            "lineage_depth": 2,
            "mood_valence": 0.5,
            "arousal": 0.1,
            "timestamp": "2025-06-02T10:12:00Z",
            "parent_ids": ["bloom_contemplate_001"]
        },
        # Generation 3 - Convergence and reblooming
        {
            "bloom_id": "bloom_resolved_003",
            "lineage_depth": 3,
            "mood_valence": 0.2,
            "arousal": 0.4,
            "timestamp": "2025-06-02T10:20:00Z",
            "parent_ids": ["bloom_anxious_002", "bloom_peaceful_002"]
        },
        # Rebloom example (same position as parent)
        {
            "bloom_id": "bloom_reborn_003",
            "lineage_depth": 3,
            "mood_valence": 0.2,
            "arousal": 0.4,
            "timestamp": "2025-06-02T10:25:00Z",
            "parent_ids": ["bloom_resolved_003"]
        }
    ]
    
    # Generate the mood vector map
    output_path = visualizer.plot_mood_vector_map(sample_blooms)
    print(f"\n🎨 Mood vector visualization complete!")
    print(f"📍 Output saved to: {output_path}")