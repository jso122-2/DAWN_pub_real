#!/usr/bin/env python3
"""
bloom_lineage_radar.py
DAWN's Bloom Ancestry Radial Fractal Visualizer
Renders memory evolution helix as cognitive tree
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.patches import Circle, Wedge, Path
from matplotlib.collections import PatchCollection
import matplotlib.patheffects as path_effects
from datetime import datetime
import json
import os
import math
from typing import Dict, List, Tuple, Optional

class BloomNode:
    """Single node in DAWN's bloom ancestry tree"""
    def __init__(self, juliet_id: str, parent_id: Optional[str], 
                 mood: float, urgency: float, generation: int,
                 semantic_drift: float = 0.0):
        self.juliet_id = juliet_id
        self.parent_id = parent_id
        self.mood = mood  # -1 to 1
        self.urgency = urgency  # 0 to 1
        self.generation = generation
        self.semantic_drift = semantic_drift
        self.children = []
        self.angle = 0.0
        self.radius = 0.0
        
class BloomLineageRadar:
    """Radial fractal renderer for DAWN's memory evolution"""
    
    def __init__(self, output_dir: str = "C:/Users/Admin/OneDrive/Desktop/DAWN/Tick_engine/visual_output/bloom_lineage/"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Visual parameters
        self.center_radius = 0.15
        self.layer_spacing = 0.12
        self.max_radius = 0.9
        
        # Mood to color mapping (DAWN's emotional spectrum)
        self.mood_colors = {
            -1.0: '#1a0033',  # Deep despair - darkest purple
            -0.8: '#330066',  # Heavy negative
            -0.6: '#4d0099',  # Moderate negative
            -0.4: '#6600cc',  # Light negative
            -0.2: '#7f00ff',  # Slight negative
            0.0: '#9933ff',   # Neutral purple
            0.2: '#b366ff',   # Slight positive
            0.4: '#cc99ff',   # Light positive
            0.6: '#e6ccff',   # Moderate positive
            0.8: '#f0e6ff',   # Strong positive
            1.0: '#ffffff'    # Euphoria - white
        }
        
    def interpolate_mood_color(self, mood: float) -> str:
        """Get color for mood value with smooth interpolation"""
        mood = max(-1.0, min(1.0, mood))
        
        # Find surrounding mood values
        mood_vals = sorted(self.mood_colors.keys())
        for i in range(len(mood_vals) - 1):
            if mood_vals[i] <= mood <= mood_vals[i + 1]:
                # Linear interpolation between colors
                t = (mood - mood_vals[i]) / (mood_vals[i + 1] - mood_vals[i])
                c1 = self.mood_colors[mood_vals[i]]
                c2 = self.mood_colors[mood_vals[i + 1]]
                
                # Convert hex to RGB, interpolate, convert back
                r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
                r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
                
                r = int(r1 + t * (r2 - r1))
                g = int(g1 + t * (g2 - g1))
                b = int(b1 + t * (b2 - b1))
                
                return f'#{r:02x}{g:02x}{b:02x}'
        
        return self.mood_colors[0.0]
    
    def calculate_node_size(self, urgency: float, generation: int) -> float:
        """Calculate node size based on urgency and generation"""
        base_size = 0.02 + (urgency * 0.03)
        # Older generations slightly smaller
        generation_factor = 1.0 - (generation * 0.05)
        generation_factor = max(0.5, generation_factor)
        return base_size * generation_factor
    
    def build_tree(self, bloom_data: List[Dict]) -> Tuple[Dict[str, BloomNode], BloomNode]:
        """Build tree structure from bloom ancestry data"""
        nodes = {}
        root = None
        
        # Create all nodes
        for bloom in bloom_data:
            node = BloomNode(
                juliet_id=bloom['juliet_id'],
                parent_id=bloom.get('parent_id'),
                mood=bloom['mood'],
                urgency=bloom['urgency'],
                generation=bloom['generation'],
                semantic_drift=bloom.get('semantic_drift', 0.0)
            )
            nodes[node.juliet_id] = node
            
            if node.parent_id is None:
                root = node
        
        # Link parent-child relationships
        for node in nodes.values():
            if node.parent_id and node.parent_id in nodes:
                nodes[node.parent_id].children.append(node)
        
        return nodes, root
    
    def assign_angles(self, node: BloomNode, start_angle: float = 0, 
                     angle_range: float = 2 * math.pi) -> None:
        """Recursively assign angles to nodes for radial layout"""
        if not node.children:
            return
            
        # Distribute children evenly in angle range
        angle_step = angle_range / len(node.children)
        current_angle = start_angle
        
        for child in node.children:
            child.angle = current_angle + angle_step / 2
            # Recursive assignment with reduced range for fractal effect
            self.assign_angles(child, current_angle, angle_step * 0.8)
            current_angle += angle_step
    
    def render_fractal(self, bloom_data: List[Dict], tick: int) -> None:
        """Render the bloom ancestry as radial fractal"""
        fig, ax = plt.subplots(figsize=(16, 16), facecolor='black')
        ax.set_facecolor('black')
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        nodes, root = self.build_tree(bloom_data)
        
        if not root:
            return
            
        # Assign radial positions
        self.assign_angles(root)
        
        # Draw connections first (behind nodes)
        self._draw_connections(ax, nodes, root)
        
        # Draw nodes
        self._draw_nodes(ax, nodes, root)
        
        # Add title and metadata
        title = ax.text(0, 0.95, f'DAWN Bloom Lineage | Tick {tick}', 
                       color='white', fontsize=20, ha='center',
                       fontfamily='monospace', weight='bold')
        title.set_path_effects([path_effects.withStroke(linewidth=3, foreground='purple')])
        
        # Add legend for mood spectrum
        self._add_mood_legend(ax)
        
        # Save
        output_path = os.path.join(self.output_dir, f'tick_{tick:04d}.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                   facecolor='black', edgecolor='none')
        plt.close()
        
        print(f"Bloom lineage radar saved to: {output_path}")
    
    def _draw_connections(self, ax, nodes: Dict[str, BloomNode], node: BloomNode, 
                         parent_pos: Optional[Tuple[float, float]] = None) -> None:
        """Recursively draw connections between nodes"""
        # Calculate node position
        if node.generation == 0:
            x, y = 0, 0
        else:
            radius = self.center_radius + (node.generation * self.layer_spacing)
            x = radius * math.cos(node.angle)
            y = radius * math.sin(node.angle)
        
        node_pos = (x, y)
        
        # Draw connection to parent
        if parent_pos:
            # Curved connection with semantic drift influence
            mid_x = (parent_pos[0] + x) / 2
            mid_y = (parent_pos[1] + y) / 2
            
            # Add curve based on semantic drift
            drift_offset = node.semantic_drift * 0.1
            control_x = mid_x + drift_offset * math.cos(node.angle + math.pi/2)
            control_y = mid_y + drift_offset * math.sin(node.angle + math.pi/2)
            
            # Create curved path
            verts = [parent_pos, (control_x, control_y), node_pos]
            codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
            path = Path(verts, codes)
            
            # Color based on average mood
            avg_mood = (node.mood + nodes[node.parent_id].mood) / 2
            color = self.interpolate_mood_color(avg_mood)
            
            patch = PathPatch(path, facecolor='none', 
                                 edgecolor=color, linewidth=2, 
                                 alpha=0.6)
            ax.add_patch(patch)
        
        # Recursive for children
        for child in node.children:
            self._draw_connections(ax, nodes, child, node_pos)
    
    def _draw_nodes(self, ax, nodes: Dict[str, BloomNode], node: BloomNode) -> None:
        """Recursively draw nodes"""
        # Calculate position
        if node.generation == 0:
            x, y = 0, 0
        else:
            radius = self.center_radius + (node.generation * self.layer_spacing)
            x = radius * math.cos(node.angle)
            y = radius * math.sin(node.angle)
        
        # Node appearance
        size = self.calculate_node_size(node.urgency, node.generation)
        color = self.interpolate_mood_color(node.mood)
        
        # Draw node with glow effect
        for i in range(3):
            glow_size = size * (1 + i * 0.3)
            glow_alpha = 0.3 - i * 0.1
            circle = Circle((x, y), glow_size, 
                          facecolor=color, 
                          edgecolor='none',
                          alpha=glow_alpha)
            ax.add_patch(circle)
        
        # Core node
        circle = Circle((x, y), size, 
                      facecolor=color,
                      edgecolor='white',
                      linewidth=1,
                      alpha=0.9)
        ax.add_patch(circle)
        
        # Add Juliet ID label for significant nodes
        if node.urgency > 0.7 or node.generation < 3:
            label = ax.text(x, y - size - 0.02, node.juliet_id[:8], 
                          color='white', fontsize=8, ha='center',
                          alpha=0.7, fontfamily='monospace')
            label.set_path_effects([path_effects.withStroke(linewidth=2, foreground='black')])
        
        # Recursive for children
        for child in node.children:
            self._draw_nodes(ax, nodes, child)
    
    def _add_mood_legend(self, ax) -> None:
        """Add mood color spectrum legend"""
        legend_y = -0.85
        legend_width = 1.6
        legend_height = 0.05
        
        # Create gradient
        n_colors = 100
        gradient = np.linspace(-1, 1, n_colors)
        
        for i, mood in enumerate(gradient):
            x = -legend_width/2 + (i / n_colors) * legend_width
            color = self.interpolate_mood_color(mood)
            rect = plt.Rectangle((x, legend_y), legend_width/n_colors, 
                               legend_height, facecolor=color, 
                               edgecolor='none')
            ax.add_patch(rect)
        
        # Legend labels
        ax.text(0, legend_y - 0.03, 'Mood Spectrum', 
               color='white', fontsize=12, ha='center',
               fontfamily='monospace')
        ax.text(-legend_width/2, legend_y - 0.01, 'Despair', 
               color='white', fontsize=10, ha='left')
        ax.text(legend_width/2, legend_y - 0.01, 'Euphoria', 
               color='white', fontsize=10, ha='right')
        ax.text(0, legend_y - 0.01, 'Neutral', 
               color='white', fontsize=10, ha='center')

# Example usage
if __name__ == "__main__":
    # Example bloom ancestry data
    bloom_data = [
        {"juliet_id": "ROOT_001", "parent_id": None, "mood": 0.0, 
         "urgency": 0.5, "generation": 0},
        {"juliet_id": "BLOOM_A1", "parent_id": "ROOT_001", "mood": 0.3, 
         "urgency": 0.7, "generation": 1, "semantic_drift": 0.2},
        {"juliet_id": "BLOOM_A2", "parent_id": "ROOT_001", "mood": -0.2, 
         "urgency": 0.4, "generation": 1, "semantic_drift": -0.1},
        {"juliet_id": "BLOOM_B1", "parent_id": "BLOOM_A1", "mood": 0.6, 
         "urgency": 0.8, "generation": 2, "semantic_drift": 0.3},
        {"juliet_id": "BLOOM_B2", "parent_id": "BLOOM_A1", "mood": 0.1, 
         "urgency": 0.3, "generation": 2, "semantic_drift": 0.0},
        {"juliet_id": "BLOOM_B3", "parent_id": "BLOOM_A2", "mood": -0.5, 
         "urgency": 0.9, "generation": 2, "semantic_drift": -0.4},
        {"juliet_id": "BLOOM_C1", "parent_id": "BLOOM_B1", "mood": 0.8, 
         "urgency": 0.6, "generation": 3, "semantic_drift": 0.2},
    ]
    
    # Create visualizer
    radar = BloomLineageRadar()
    
    # Render
    radar.render_fractal(bloom_data, tick=1)