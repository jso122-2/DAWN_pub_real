"""
DAWN Unified Visualization System - FIXED VERSION
Combines all visualization scripts into one comprehensive process
"""

import os
import sys
import json
import csv
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pathlib import Path
from datetime import datetime
from matplotlib.patches import PathPatch, Circle, Wedge, Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.patheffects as path_effects
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.cm as cm
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d
import pandas as pd
import networkx as nx
from collections import defaultdict

class DawnUnifiedVisualizer:
    """Unified visualization system for all DAWN visual outputs"""
    
    def __init__(self, base_path=None):
        self.base_path = Path(base_path or os.getcwd())
        self.visual_output = self.base_path / "visual_output"
        self.setup_directories()
        self.setup_data()
        
    def setup_directories(self):
        """Create all necessary output directories"""
        dirs = [
            "visual_output",
            "visual_output/drift",
            "visual_output/entropy",
            "visual_output/bloom",
            "visual_output/belief",
            "visual_output/decay",
            "visual_output/coherence",
            "visual_output/mood",
            "visual_output/pulse",
            "visual_output/animations",
            "juliet_flowers/bloom_metadata",
            "juliet_flowers/cluster_report",
            "logs",
            "owl/logs",
            "codex"
        ]
        for d in dirs:
            (self.base_path / d).mkdir(parents=True, exist_ok=True)
    
    def setup_data(self):
        """Create dummy data files if they don't exist"""
        # Drift compass log
        drift_log = self.base_path / "juliet_flowers/cluster_report/drift_compass_log.csv"
        if not drift_log.exists():
            with open(drift_log, 'w', encoding='utf-8') as f:
                f.write("tick,angle,magnitude,entropy\n")  # Added header
                for i in range(100):
                    tick = 1000 + i
                    angle = (i * 0.1) % (2 * np.pi)
                    mag = 0.5 + 0.3 * np.sin(i * 0.05)
                    entropy = 0.3 + 0.2 * np.sin(i * 0.08)
                    f.write(f"{tick},{angle},{mag},{entropy}\n")
        
        # Bloom metadata
        bloom_dir = self.base_path / "juliet_flowers/bloom_metadata"
        if not list(bloom_dir.glob("*.json")):
            for i in range(10):
                bloom_data = {
                    "seed_id": f"BLOOM_{i:03d}",
                    "lineage_depth": i % 4,
                    "entropy_score": 0.1 + (i * 0.08) % 0.8,
                    "mood": ["joyful", "focused", "reflective", "anxious"][i % 4],
                    "belief_resonance": {
                        "belief": ["growth", "decay", "synthesis"][i % 3],
                        "distance": 0.2 + (i * 0.05),
                        "rgb": [100 + i*10, 150 - i*5, 200 - i*10]
                    }
                }
                with open(bloom_dir / f"bloom_{i}.json", 'w') as f:
                    json.dump(bloom_data, f, indent=2)
        
        # Zone overlay log
        zone_log = self.base_path / "juliet_flowers/cluster_report/zone_overlay_log.csv"
        if not zone_log.exists():
            with open(zone_log, 'w', encoding='utf-8') as f:
                f.write("tick,zone,heat\n")
                for i in range(100):
                    tick = 1000 + i
                    zone = ["calm", "active", "surge"][i % 3]
                    heat = 0.3 + (i % 10) * 0.05
                    f.write(f"{tick},{zone},{heat:.3f}\n")
        
        # Decay loss log - FIXED
        decay_log = self.base_path / "logs/decay_loss_log.csv"
        if not decay_log.exists():
            with open(decay_log, 'w', encoding='utf-8') as f:
                f.write("tick_id,from,to,total_decay\n")
                for i in range(50):
                    tick = f"{1000 + i}"
                    from_node = f"NODE_{i % 5}"
                    to_node = f"NODE_{(i + 1) % 5}"
                    decay = 0.1 + (i % 10) * 0.02
                    f.write(f"{tick},{from_node},{to_node},{decay}\n")
        
        # Synthesis bloom log - FIXED
        synthesis_log = self.base_path / "logs/synthesis_bloom_log.csv"
        if not synthesis_log.exists():
            with open(synthesis_log, 'w', encoding='utf-8') as f:
                f.write("tick_id,seed_id,path\n")
                for i in range(30):
                    tick = 1000 + i * 2
                    seed = f"SYNTH_{i}"
                    path = f"A{i%3}→B{i%4}→C{i%5}"
                    f.write(f"{tick},{seed},{path}\n")
        
        # Rebloom tick log for pulse visualizations
        rebloom_log = self.base_path / "juliet_flowers/cluster_report/rebloom_tick_log.csv"
        if not rebloom_log.exists():
            with open(rebloom_log, 'w', encoding='utf-8') as f:
                f.write("tick,bloom_count,heat,zone,scup\n")
                for i in range(100):
                    tick = 1000 + i
                    bloom_ct = i % 5
                    heat = 0.3 + (i % 10) * 0.05
                    zone = ["calm", "active", "surge"][i % 3]
                    scup = 0.7 - (i % 20) * 0.02
                    f.write(f"{tick},{bloom_ct},{heat},{zone},{scup}\n")
        
        # Crow stall log
        stall_log = self.base_path / "owl/logs/crow_stall_log.json"
        if not stall_log.exists():
            stall_data = {
                f"{chr(65+i%5)}{j}": np.random.randint(1, 10) 
                for i in range(5) for j in range(5)
            }
            with open(stall_log, 'w') as f:
                json.dump(stall_data, f)
    
    def polar_to_xy(self, angle_rad, magnitude):
        """Convert polar to cartesian coordinates"""
        return magnitude * np.cos(angle_rad), magnitude * np.sin(angle_rad)
    
    # === DRIFT VISUALIZATIONS ===
    
    def create_drift_compass(self):
        """Create drift compass visualization"""
        print("Creating drift compass...")
        
        csv_path = self.base_path / "juliet_flowers/cluster_report/drift_compass_log.csv"
        ticks, angles, mags = [], [], []
        
        try:
            df = pd.read_csv(csv_path)
            ticks = df['tick'].tolist()
            angles = df['angle'].tolist()
            mags = df['magnitude'].tolist()
        except Exception as e:
            print(f"Warning: Could not read drift data: {e}")
            # Use dummy data
            ticks = list(range(1000, 1100))
            angles = [(i * 0.1) % (2 * np.pi) for i in range(100)]
            mags = [0.5 + 0.3 * np.sin(i * 0.05) for i in range(100)]
        
        X = np.array(ticks)
        Y = np.zeros_like(X)
        U, V = [], []
        
        for a, m in zip(angles, mags):
            dx, dy = self.polar_to_xy(a, m)
            U.append(dx)
            V.append(dy)
        
        plt.figure(figsize=(12, 4))
        plt.quiver(X, Y, U, V, angles, scale=1, scale_units='xy', angles='xy', cmap="hsv")
        plt.yticks([])
        plt.xlabel("Tick")
        plt.title("Semantic Drift Compass")
        plt.tight_layout()
        
        output_path = self.visual_output / "drift" / "drift_compass.png"
        plt.savefig(output_path)
        plt.close()
        print(f"✅ Saved: {output_path}")
    
    def create_drift_entropy_overlay(self):
        """Create drift and entropy overlay visualization"""
        print("Creating drift-entropy overlay...")
        
        csv_path = self.base_path / "juliet_flowers/cluster_report/drift_compass_log.csv"
        
        try:
            df = pd.read_csv(csv_path)
            ticks = df['tick'].tolist()
            angles = df['angle'].tolist()
            mags = df['magnitude'].tolist()
            entropy_vals = df['entropy'].tolist()
        except Exception as e:
            print(f"Warning: Could not read drift data: {e}")
            # Use dummy data
            ticks = list(range(1000, 1100))
            angles = [(i * 0.1) % (2 * np.pi) for i in range(100)]
            mags = [0.5 + 0.3 * np.sin(i * 0.05) for i in range(100)]
            entropy_vals = [0.3 + 0.2 * np.sin(i * 0.08) for i in range(100)]
        
        X = np.array(ticks)
        Y = np.zeros_like(X)
        U, V = [], []
        
        for a, m in zip(angles, mags):
            dx, dy = self.polar_to_xy(a, m)
            U.append(dx)
            V.append(dy)
        
        fig, ax1 = plt.subplots(figsize=(14, 5))
        
        # Drift Vectors
        quiv = ax1.quiver(X, Y, U, V, angles, scale=1, scale_units='xy', angles='xy', cmap="twilight_shifted")
        ax1.set_ylabel("Drift Direction (vector)")
        ax1.set_yticks([])
        ax1.set_xlabel("Tick")
        ax1.set_title("Drift & Entropy Stormmap")
        
        # Entropy Overlay
        ax2 = ax1.twinx()
        ax2.plot(ticks, entropy_vals, color="black", alpha=0.5, linewidth=2, linestyle="--", label="Entropy")
        ax2.set_ylabel("Entropy", color="black")
        ax2.tick_params(axis='y', labelcolor="black")
        
        plt.grid(True, axis='x')
        plt.tight_layout()
        
        output_path = self.visual_output / "drift" / "drift_entropy_overlay.png"
        plt.savefig(output_path)
        plt.close()
        print(f"✅ Saved: {output_path}")
    
    def create_drift_lattice(self):
        """Create drift lattice from bloom metadata"""
        print("Creating drift lattice...")
        
        bloom_dir = self.base_path / "juliet_flowers/bloom_metadata"
        
        plt.figure(figsize=(10, 6))
        for fname in bloom_dir.glob("*.json"):
            try:
                with open(fname, "r") as f:
                    bloom = json.load(f)
                    x = bloom.get("lineage_depth", 0)
                    y = int(bloom["seed_id"][-2:]) if bloom["seed_id"][-2:].isdigit() else 0
                    entropy = bloom.get("entropy_score", 0.0)
                    plt.scatter(x, y, s=150, c=[[1-entropy, 0.2, entropy]], edgecolors='black')
                    plt.text(x + 0.1, y, bloom["seed_id"], fontsize=7)
            except Exception as e:
                print(f"Warning: Could not process bloom file {fname}: {e}")
                continue
        
        plt.title("Semantic Drift Lattice")
        plt.xlabel("Lineage Depth")
        plt.ylabel("Semantic Y")
        plt.grid(True)
        plt.tight_layout()
        
        output_path = self.visual_output / "drift" / "drift_lattice.png"
        plt.savefig(output_path)
        plt.close()
        print(f"✅ Saved: {output_path}")
    
    # === ENTROPY VISUALIZATIONS ===
    
    def create_entropy_clusters(self):
        """Create entropy clustering visualization"""
        print("Creating entropy clusters...")
        
        bloom_dir = self.base_path / "juliet_flowers/bloom_metadata"
        clusters = {"low": [], "medium": [], "high": []}
        
        for fname in bloom_dir.glob("*.json"):
            try:
                with open(fname, "r") as f:
                    bloom = json.load(f)
                    e = bloom.get("entropy_score", 0.0)
                    if e < 0.3:
                        clusters["low"].append(bloom)
                    elif e < 0.7:
                        clusters["medium"].append(bloom)
                    else:
                        clusters["high"].append(bloom)
            except Exception as e:
                print(f"Warning: Could not process bloom file {fname}: {e}")
                continue
        
        counts = [len(clusters["low"]), len(clusters["medium"]), len(clusters["high"])]
        labels = ["Low (0–0.3)", "Medium (0.3–0.7)", "High (0.7–1.0)"]
        
        plt.figure(figsize=(8, 5))
        plt.bar(labels, counts, color=["blue", "orange", "red"])
        plt.title("Entropy Clustering by Variance")
        plt.ylabel("Bloom Count")
        plt.tight_layout()
        
        output_path = self.visual_output / "entropy" / "entropy_clusters.png"
        plt.savefig(output_path)
        plt.close()
        print(f"✅ Saved: {output_path}")
    
    # === BELIEF VISUALIZATIONS ===
    
    def create_belief_resonance_scatter(self):
        """Create belief resonance scatter plot"""
        print("Creating belief resonance scatter...")
        
        bloom_dir = self.base_path / "juliet_flowers/bloom_metadata"
        x, y, colors, labels = [], [], [], []
        
        for file in bloom_dir.glob("*.json"):
            try:
                with open(file) as f:
                    data = json.load(f)
                    belief_data = data.get("belief_resonance", {})
                    if belief_data:
                        x.append(data.get("lineage_depth", 0))
                        y.append(belief_data.get("distance", 0.0))
                        colors.append(belief_data.get("rgb", [128, 128, 128]))
                        labels.append(belief_data.get("belief", "unknown"))
            except Exception as e:
                print(f"Warning: Could not process bloom file {file}: {e}")
                continue
        
        if x:
            plt.figure(figsize=(10, 6))
            for i in range(len(x)):
                plt.scatter(x[i], y[i], color=[c/255 for c in colors[i]], 
                           label=labels[i] if labels[i] not in labels[:i] else "", s=80)
            
            plt.xlabel("Lineage Depth")
            plt.ylabel("Belief Resonance (RGB Distance)")
            plt.title("Bloom Belief Resonance Scatter")
            plt.grid(True)
            if labels:
                plt.legend(loc="upper right")
            
            output_path = self.visual_output / "belief" / "belief_resonance_scatter.png"
            plt.savefig(output_path)
            plt.close()
            print(f"✅ Saved: {output_path}")
    
    # === BLOOM VISUALIZATIONS ===
    
    def create_bloom_lineage_radar(self):
        """Create bloom lineage radar visualization"""
        print("Creating bloom lineage radar...")
        
        # Use example data
        bloom_data = [
            {"juliet_id": "ROOT_001", "parent_id": None, "mood": 0.0, 
             "urgency": 0.5, "generation": 0},
            {"juliet_id": "BLOOM_A1", "parent_id": "ROOT_001", "mood": 0.3, 
             "urgency": 0.7, "generation": 1, "semantic_drift": 0.2},
            {"juliet_id": "BLOOM_A2", "parent_id": "ROOT_001", "mood": -0.2, 
             "urgency": 0.4, "generation": 1, "semantic_drift": -0.1},
            {"juliet_id": "BLOOM_B1", "parent_id": "BLOOM_A1", "mood": 0.6, 
             "urgency": 0.8, "generation": 2, "semantic_drift": 0.3},
        ]
        
        self._render_bloom_lineage_radar(bloom_data, 1)
    
    def _render_bloom_lineage_radar(self, bloom_data, tick):
        """Render bloom lineage radar visualization"""
        fig, ax = plt.subplots(figsize=(16, 16), facecolor='black')
        ax.set_facecolor('black')
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Build tree structure
        nodes = {}
        root = None
        
        for bloom in bloom_data:
            node = {
                'juliet_id': bloom['juliet_id'],
                'parent_id': bloom.get('parent_id'),
                'mood': bloom['mood'],
                'urgency': bloom['urgency'],
                'generation': bloom['generation'],
                'semantic_drift': bloom.get('semantic_drift', 0.0),
                'children': [],
                'angle': 0.0
            }
            nodes[node['juliet_id']] = node
            
            if node['parent_id'] is None:
                root = node
        
        # Link parent-child relationships
        for node in nodes.values():
            if node['parent_id'] and node['parent_id'] in nodes:
                nodes[node['parent_id']]['children'].append(node)
        
        # Assign angles recursively
        if root:
            self._assign_angles_recursive(root, 0, 2 * np.pi)
            
            # Draw connections
            self._draw_connections_recursive(ax, root, nodes)
            
            # Draw nodes
            self._draw_nodes_recursive(ax, root, nodes)
        
        # Add title
        title = ax.text(0, 0.95, f'DAWN Bloom Lineage | Tick {tick}', 
                       color='white', fontsize=20, ha='center',
                       fontfamily='monospace', weight='bold')
        title.set_path_effects([path_effects.withStroke(linewidth=3, foreground='purple')])
        
        # Save
        output_path = self.visual_output / "bloom" / f"bloom_lineage_radar_tick_{tick:04d}.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                   facecolor='black', edgecolor='none')
        plt.close()
        
        print(f"✅ Saved: {output_path}")
    
    def _assign_angles_recursive(self, node, start_angle, angle_range):
        """Assign angles to nodes for radial layout"""
        if not node['children']:
            return
        
        angle_step = angle_range / len(node['children'])
        current_angle = start_angle
        
        for child in node['children']:
            child['angle'] = current_angle + angle_step / 2
            self._assign_angles_recursive(child, current_angle, angle_step * 0.8)
            current_angle += angle_step
    
    def _draw_connections_recursive(self, ax, node, all_nodes, parent_pos=None):
        """Draw connections between nodes"""
        # Calculate position
        if node['generation'] == 0:
            x, y = 0, 0
        else:
            radius = 0.15 + (node['generation'] * 0.12)
            x = radius * np.cos(node['angle'])
            y = radius * np.sin(node['angle'])
        
        node_pos = (x, y)
        
        # Draw connection to parent
        if parent_pos:
            # Create curved connection
            color = self._get_mood_color(node['mood'])
            ax.plot([parent_pos[0], x], [parent_pos[1], y], 
                   color=color, linewidth=2, alpha=0.6)
        
        # Recursive for children
        for child in node['children']:
            self._draw_connections_recursive(ax, child, all_nodes, node_pos)
    
    def _draw_nodes_recursive(self, ax, node, all_nodes):
        """Draw nodes recursively"""
        # Calculate position
        if node['generation'] == 0:
            x, y = 0, 0
        else:
            radius = 0.15 + (node['generation'] * 0.12)
            x = radius * np.cos(node['angle'])
            y = radius * np.sin(node['angle'])
        
        # Node appearance
        size = 0.02 + (node['urgency'] * 0.03)
        color = self._get_mood_color(node['mood'])
        
        # Draw node with glow
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
        
        # Add label for significant nodes
        if node['urgency'] > 0.7 or node['generation'] < 3:
            label = ax.text(x, y - size - 0.02, node['juliet_id'][:8], 
                          color='white', fontsize=8, ha='center',
                          alpha=0.7, fontfamily='monospace')
            label.set_path_effects([path_effects.withStroke(linewidth=2, foreground='black')])
        
        # Recursive for children
        for child in node['children']:
            self._draw_nodes_recursive(ax, child, all_nodes)
    
    def _get_mood_color(self, mood):
        """Get color for mood value"""
        mood_colors = {
            -1.0: '#1a0033',
            -0.5: '#4d0099',
            0.0: '#9933ff',
            0.5: '#cc99ff',
            1.0: '#ffffff'
        }
        
        # Find closest mood value
        mood_vals = sorted(mood_colors.keys())
        for i in range(len(mood_vals) - 1):
            if mood_vals[i] <= mood <= mood_vals[i + 1]:
                return mood_colors[mood_vals[i]]
        
        return mood_colors[0.0]
    
    def create_cognition_pressure_map(self):
        """Create cognition pressure map"""
        print("Creating cognition pressure map...")
        
        bloom_dir = self.base_path / "juliet_flowers/bloom_metadata"
        pressure_grid = {}
        
        for fname in bloom_dir.glob("*.json"):
            try:
                with open(fname, "r") as f:
                    bloom = json.load(f)
                    x = bloom.get("lineage_depth", 0)
                    y = int(bloom["seed_id"][-2:]) if bloom["seed_id"][-2:].isdigit() else 0
                    pressure = bloom.get("entropy_score", 0.0)
                    key = (x, y)
                    pressure_grid[key] = pressure_grid.get(key, 0) + pressure
            except Exception as e:
                print(f"Warning: Could not process bloom file {fname}: {e}")
                continue
        
        if pressure_grid:
            xs, ys, weights = zip(*[(k[0], k[1], v) for k, v in pressure_grid.items()])
            plt.figure(figsize=(10, 6))
            plt.scatter(xs, ys, c=weights, cmap="plasma", s=180, edgecolors='black')
            plt.colorbar(label="Cognitive Pressure")
            plt.title("Cognition Pressure Map")
            plt.xlabel("Lineage Depth")
            plt.ylabel("Semantic Y")
            plt.grid(True)
            plt.tight_layout()
            
            output_path = self.visual_output / "bloom" / "cognition_pressure_map.png"
            plt.savefig(output_path)
            plt.close()
            print(f"✅ Saved: {output_path}")
    
    # === DECAY VISUALIZATIONS ===
    
    def create_decay_trails_frame(self):
        """Create a single frame of decay trails"""
        print("Creating decay trails frame...")
        
        log_path = self.base_path / "logs/decay_loss_log.csv"
        if not log_path.exists():
            print("No decay log found, skipping...")
            return
        
        try:
            df = pd.read_csv(log_path)
            df["tick_id"] = df["tick_id"].astype(str)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            nodes = set(df["from"]) | set(df["to"])
            pos = {node: (i, 0) for i, node in enumerate(sorted(nodes))}
            
            # Show first tick if available
            if len(df) > 0:
                tick = sorted(df["tick_id"].unique())[0]
                current = df[df["tick_id"] == tick]
                
                for _, row in current.iterrows():
                    x1, y1 = pos[row["from"]]
                    x2, y2 = pos[row["to"]]
                    width = row["total_decay"] * 5
                    ax.plot([x1, x2], [y1, y2], color="red", linewidth=width, alpha=0.6)
                    ax.text(x1, y1 + 0.1, row["from"], ha="center", fontsize=8)
                    ax.text(x2, y2 + 0.1, row["to"], ha="center", fontsize=8)
                
                ax.set_title(f"Decay Trails at Tick {tick}")
            else:
                ax.set_title("Decay Trails (No Data)")
            
            ax.set_ylim(-1, 2)
            ax.set_xticks([])
            ax.set_yticks([])
            
            output_path = self.visual_output / "decay" / "decay_trails_frame.png"
            plt.savefig(output_path)
            plt.close()
            print(f"✅ Saved: {output_path}")
            
        except Exception as e:
            print(f"Error creating decay trails: {e}")
    
    def create_synthesis_trails_frame(self):
        """Create synthesis trails visualization"""
        print("Creating synthesis trails...")
        
        path = self.base_path / "logs/synthesis_bloom_log.csv"
        if not path.exists():
            print("No synthesis log found, skipping...")
            return
        
        try:
            df = pd.read_csv(path)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if len(df) > 0:
                tick = sorted(df["tick_id"].unique())[0]
                current = df[df["tick_id"] == tick]
                ax.set_title(f"Synthesis Trails – Tick {tick}")
                
                for _, row in current.iterrows():
                    path_nodes = row["path"].split("→")
                    for i in range(len(path_nodes) - 1):
                        ax.plot([i, i+1], [5, 5], color="magenta", linewidth=2, alpha=0.6)
                        ax.text(i, 5.2, path_nodes[i], fontsize=8, ha="center")
                    if path_nodes:
                        ax.text(len(path_nodes)-1, 5.2, path_nodes[-1], fontsize=8, ha="center", color="purple")
            else:
                ax.set_title("Synthesis Trails (No Data)")
            
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            
            output_path = self.visual_output / "decay" / "synthesis_trails_frame.png"
            plt.savefig(output_path)
            plt.close()
            print(f"✅ Saved: {output_path}")
            
        except Exception as e:
            print(f"Error creating synthesis trails: {e}")
    
    # === MOOD VISUALIZATIONS ===
    
    def create_mood_distribution(self):
        """Create mood distribution histogram"""
        print("Creating mood distribution...")
        
        bloom_dir = self.base_path / "juliet_flowers/bloom_metadata"
        moods = []
        
        for fname in bloom_dir.glob("*.json"):
            try:
                with open(fname, "r") as f:
                    bloom = json.load(f)
                    moods.append(bloom.get("mood", "undefined"))
            except Exception as e:
                print(f"Warning: Could not process bloom file {fname}: {e}")
                continue
        
        # Count mood frequencies
        mood_counts = {}
        for mood in moods:
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        if mood_counts:
            plt.figure(figsize=(10, 5))
            plt.bar(mood_counts.keys(), mood_counts.values(), color='skyblue', edgecolor='black')
            plt.title("Mood Distribution Across Blooms")
            plt.ylabel("Bloom Count")
            plt.xlabel("Mood")
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            output_path = self.visual_output / "mood" / "mood_distribution.png"
            plt.savefig(output_path)
            plt.close()
            print(f"✅ Saved: {output_path}")
    
    # === PULSE VISUALIZATIONS ===
    
    def create_pulse_field_evolution(self):
        """Create pulse field evolution visualization"""
        print("Creating pulse field evolution...")
        
        log_path = self.base_path / "juliet_flowers/cluster_report/zone_overlay_log.csv"
        
        try:
            df = pd.read_csv(log_path)
            
            plt.figure(figsize=(10, 6))
            
            # Plot heat/entropy over ticks colored by zone
            zone_colors = {"calm": "green", "active": "gold", "surge": "red"}
            
            for zone in zone_colors:
                zone_data = df[df['zone'] == zone]
                if not zone_data.empty:
                    plt.scatter(zone_data['tick'], zone_data['heat'], 
                               color=zone_colors[zone], label=zone, alpha=0.7, s=50)
            
            plt.plot(df['tick'], df['heat'], 'purple', linewidth=1, alpha=0.5, label='Heat Trend')
            
            plt.xlabel("Tick")
            plt.ylabel("Heat/Entropy Level")
            plt.title("Pulse Field Evolution")
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            output_path = self.visual_output / "pulse" / "pulse_field_evolution.png"
            plt.savefig(output_path)
            plt.close()
            print(f"✅ Saved: {output_path}")
            
        except Exception as e:
            print(f"Error creating pulse field evolution: {e}")
    
    def create_interval_animation_frame(self):
        """Create pulse heat & SCUP overlay visualization"""
        print("Creating interval animation frame...")
        
        csv_path = self.base_path / "juliet_flowers/cluster_report/rebloom_tick_log.csv"
        
        try:
            df = pd.read_csv(csv_path)
            
            if len(df) == 0:
                print("No data to visualize")
                return
            
            ticks = df['tick'].tolist()
            heat_vals = df['heat'].tolist()
            zones = df['zone'].tolist()
            scup_vals = df['scup'].tolist()
            
            fig, ax1 = plt.subplots(figsize=(12, 6))
            zone_colors = {"calm": "green", "active": "gold", "surge": "red"}
            zone_plot = [zone_colors.get(z, "gray") for z in zones]
            
            scatter = ax1.scatter(ticks, heat_vals, c=zone_plot, label="Pulse Heat", s=50)
            ax1.plot(ticks, heat_vals, alpha=0.3, linewidth=1)
            ax1.set_xlabel("Tick")
            ax1.set_ylabel("Pulse Heat")
            ax1.grid(True)
            
            # SCUP on twin y-axis
            ax2 = ax1.twinx()
            ax2.plot(ticks, scup_vals, color="blue", linewidth=2, linestyle="--", label="SCUP")
            ax2.set_ylabel("SCUP", color="blue")
            ax2.tick_params(axis='y', labelcolor="blue")
            
            plt.title("Pulse Heat & SCUP Overlay Over Time")
            fig.tight_layout()
            
            output_path = self.visual_output / "pulse" / "interval_animation_frame.png"
            output_path.parent.mkdir(exist_ok=True)
            plt.savefig(output_path)
            plt.close()
            print(f"✅ Saved: {output_path}")
            
        except Exception as e:
            print(f"Error creating interval animation: {e}")
    
    # === OTHER VISUALIZATIONS ===
    
    def create_crow_stall_heatmap(self):
        """Create crow stall heatmap"""
        print("Creating crow stall heatmap...")
        
        stall_log = self.base_path / "owl/logs/crow_stall_log.json"
        if not stall_log.exists():
            print("No stall log found, skipping...")
            return
        
        try:
            with open(stall_log, "r") as f:
                stall_data = json.load(f)
            
            def to_coords(zone):
                return ord(zone[0]) - ord("A"), int(zone[1])
            
            heatmap = defaultdict(int)
            for zone, count in stall_data.items():
                x, y = to_coords(zone)
                heatmap[(x, y)] += count
            
            if heatmap:
                xs, ys, values = zip(*[(x, y, heatmap[(x, y)]) for (x, y) in heatmap])
                
                plt.figure(figsize=(6, 6))
                plt.scatter(xs, ys, s=[v * 40 for v in values], c=values, cmap="Reds", alpha=0.7)
                plt.grid(True)
                plt.xticks(range(5), ["A", "B", "C", "D", "E"])
                plt.yticks(range(5))
                plt.title("Crow Stall Heatmap (by Node)")
                plt.colorbar(label="Stall Count")
                
                output_path = self.visual_output / "crow_stall_heatmap.png"
                plt.savefig(output_path)
                plt.close()
                print(f"✅ Saved: {output_path}")
                
        except Exception as e:
            print(f"Error creating crow stall heatmap: {e}")
    
    def create_coherence_field_frame(self):
        """Create a single coherence field frame"""
        print("Creating coherence field frame...")
        
        # Simulated data
        tick = 1000
        ticks = list(range(tick - 50, tick + 1))
        scup_values = [0.5 + 0.3 * np.sin(t * 0.1) + np.random.normal(0, 0.05) for t in ticks]
        entropy_values = [0.3 + 0.4 * np.sin(t * 0.07) + np.random.normal(0, 0.1) for t in ticks]
        
        fig, (ax_field, ax_metrics) = plt.subplots(
            2, 1, figsize=(16, 10),
            gridspec_kw={'height_ratios': [3, 1]},
            facecolor='#0a0a0a'
        )
        
        # Create field visualization
        ax_field.set_facecolor('#0a0a0a')
        
        # Simple field representation
        field = np.zeros((50, len(ticks)))
        for i, (s, e) in enumerate(zip(scup_values, entropy_values)):
            wave = np.exp(-((np.linspace(0, 1, 50) - s) ** 2) / 0.1)
            field[:, i] = wave * (1 + e * 0.5)
        
        im = ax_field.imshow(
            field, aspect='auto', cmap='viridis',
            extent=[ticks[0], ticks[-1], 0, 1],
            alpha=0.9
        )
        
        ax_field.plot(ticks, scup_values, color='#00ffff', linewidth=2, alpha=0.8, label='SCUP')
        ax_field.plot(ticks, entropy_values, color='#ff00ff', linewidth=2, alpha=0.8, label='Entropy')
        
        ax_field.set_ylim(0, 1)
        ax_field.set_ylabel('Coherence State', color='white', fontsize=12)
        ax_field.set_title(f'DAWN Coherence Field | Tick {tick}', color='white', fontsize=16)
        ax_field.tick_params(colors='white')
        ax_field.legend(loc='upper right', facecolor='black', edgecolor='white')
        
        # Metrics panel
        ax_metrics.set_facecolor('#0a0a0a')
        ax_metrics.plot(ticks, scup_values, color='#ffaa00', linewidth=1.5, label='SCUP')
        ax_metrics.plot(ticks, entropy_values, color='#00ff00', linewidth=1.5, label='Entropy')
        ax_metrics.set_ylim(0, 1)
        ax_metrics.set_xlabel('Tick', color='white')
        ax_metrics.set_ylabel('Values', color='white')
        ax_metrics.tick_params(colors='white')
        ax_metrics.legend(loc='upper right', facecolor='black', edgecolor='white')
        ax_metrics.grid(True, alpha=0.2, color='white')
        
        plt.tight_layout()
        
        output_path = self.visual_output / "coherence" / "coherence_field_frame.png"
        plt.savefig(output_path, dpi=150, facecolor='#0a0a0a')
        plt.close()
        print(f"✅ Saved: {output_path}")
    
    def create_all_visualizations(self):
        """Create all visualizations in one batch"""
        print("\n" + "="*60)
        print("DAWN UNIFIED VISUALIZATION SYSTEM")
        print("="*60)
        print(f"Output directory: {self.visual_output}")
        print(f"Starting visualization generation...\n")
        
        start_time = time.time()
        
        # Create visualizations with proper error handling
        visualizations = [
            ("drift compass", self.create_drift_compass),
            ("drift entropy overlay", self.create_drift_entropy_overlay),
            ("drift lattice", self.create_drift_lattice),
            ("entropy clusters", self.create_entropy_clusters),
            ("belief resonance scatter", self.create_belief_resonance_scatter),
            ("bloom lineage radar", self.create_bloom_lineage_radar),
            ("cognition pressure map", self.create_cognition_pressure_map),
            ("decay trails frame", self.create_decay_trails_frame),
            ("synthesis trails frame", self.create_synthesis_trails_frame),
            ("mood distribution", self.create_mood_distribution),
            ("pulse field evolution", self.create_pulse_field_evolution),
            ("interval animation frame", self.create_interval_animation_frame),
            ("crow stall heatmap", self.create_crow_stall_heatmap),
            ("coherence field frame", self.create_coherence_field_frame),
        ]
        
        for name, func in visualizations:
            try:
                func()
            except Exception as e:
                print(f"❌ Error in {name}: {e}")
        
        elapsed = time.time() - start_time
        
        print("\n" + "="*60)
        print(f"✅ VISUALIZATION GENERATION COMPLETE")
        print(f"⏱️ Total time: {elapsed:.2f} seconds")
        print(f"📁 All outputs saved to: {self.visual_output}")
        print("="*60)
        
        # Create index of generated files
        self.create_output_index()
    
    def create_output_index(self):
        """Create an HTML index of all generated visualizations"""
        print("\n📄 Creating output index...")
        
        # FIXED: Proper HTML template escaping
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>DAWN Unified Visualization Output</title>
    <style>
        body {{ 
            font-family: 'Courier New', monospace; 
            margin: 20px; 
            background: #0a0a0a; 
            color: #00ffaa;
        }}
        h1 {{ 
            color: #ff00ff; 
            text-shadow: 0 0 10px #ff00ff;
        }}
        h2 {{ 
            color: #00ffff; 
            margin-top: 30px;
        }}
        .gallery {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); 
            gap: 20px; 
            margin-top: 20px;
        }}
        .image-card {{ 
            background: #1a1a1a; 
            padding: 10px; 
            border-radius: 8px; 
            border: 1px solid #00ffaa;
            transition: transform 0.2s;
        }}
        .image-card:hover {{
            transform: scale(1.05);
            border-color: #ff00ff;
            box-shadow: 0 0 20px #ff00ff;
        }}
        img {{ 
            width: 100%; 
            height: auto; 
            border-radius: 4px; 
        }}
        .title {{ 
            color: #00ffaa; 
            margin-top: 10px; 
            font-size: 14px;
        }}
        .timestamp {{
            color: #666;
            font-size: 12px;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <h1>DAWN Unified Visualization Output</h1>
    <div class="timestamp">Generated: {timestamp}</div>
"""
        
        # Organize by category
        categories = {
            "Drift Dynamics": "drift",
            "Entropy Analysis": "entropy", 
            "Bloom Evolution": "bloom",
            "Belief Systems": "belief",
            "Decay Patterns": "decay",
            "Coherence Fields": "coherence",
            "Mood Dynamics": "mood",
            "Pulse Patterns": "pulse"
        }
        
        for category_name, folder in categories.items():
            folder_path = self.visual_output / folder
            if folder_path.exists():
                images = list(folder_path.glob("*.png")) + list(folder_path.glob("*.gif"))
                if images:
                    html_content += f'<h2>{category_name}</h2><div class="gallery">'
                    for img in images:
                        rel_path = img.relative_to(self.visual_output)
                        html_content += f'''
                        <div class="image-card">
                            <img src="{rel_path.as_posix()}" alt="{img.name}">
                            <div class="title">{img.stem.replace("_", " ").title()}</div>
                        </div>
                        '''
                    html_content += '</div>'
        
        # Also check root output directory
        root_images = list(self.visual_output.glob("*.png"))
        if root_images:
            html_content += '<h2>Other Visualizations</h2><div class="gallery">'
            for img in root_images:
                rel_path = img.relative_to(self.visual_output)
                html_content += f'''
                <div class="image-card">
                    <img src="{rel_path.as_posix()}" alt="{img.name}">
                    <div class="title">{img.stem.replace("_", " ").title()}</div>
                </div>
                '''
            html_content += '</div>'
        
        html_content += """
</body>
</html>
"""
        
        try:
            index_path = self.visual_output / "index.html"
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(html_content.format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            print(f"✅ Created index: {index_path}")
            print(f"   Open this file in your browser to view all visualizations")
        except Exception as e:
            print(f"❌ Error creating index: {e}")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='DAWN Unified Visualization System')
    parser.add_argument('--path', type=str, help='Base path for DAWN system')
    parser.add_argument('--quick', action='store_true', help='Run only core visualizations')
    
    args = parser.parse_args()
    
    # Create visualizer
    visualizer = DawnUnifiedVisualizer(base_path=args.path)
    
    if args.quick:
        print("🚀 Quick mode - creating core visualizations only...")
        try:
            visualizer.create_drift_compass()
            visualizer.create_entropy_clusters()
            visualizer.create_bloom_lineage_radar()
            visualizer.create_mood_distribution()
            visualizer.create_pulse_field_evolution()
        except Exception as e:
            print(f"Error: {e}")
    else:
        # Create all visualizations
        visualizer.create_all_visualizations()
    
    print("\n✨ Done! Check the visual_output directory for results.")
    print("📄 Open visual_output/index.html to browse all visualizations.")

if __name__ == "__main__":
    main()