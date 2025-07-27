"""
Unified Bloom Visualization System
Handles all visualization, animation, and graphical analysis for the DAWN bloom system
"""

import os
import json
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

# Ensure output directories exist
VISUAL_OUTPUT_DIR = "juliet_flowers/cluster_report"
ANIMATION_OUTPUT_DIR = "visuals"
for dir_path in [VISUAL_OUTPUT_DIR, ANIMATION_OUTPUT_DIR]:
    os.makedirs(dir_path, exist_ok=True)


class RebloomTreeVisualizer:
    """Visualizes rebloom lineage as tree structures with animations"""
    
    def __init__(self, lineage_path: str = "juliet_flowers/cluster_report/rebloom_lineage.json"):
        self.lineage_path = lineage_path
        self.output_dir = VISUAL_OUTPUT_DIR
        self.cognition_log = []
        self.G = nx.DiGraph()
        
    def load_lineage_data(self) -> List[Dict]:
        """Load rebloom lineage data from JSON"""
        try:
            with open(self.lineage_path, 'r') as f:
                lineage = json.load(f)
            # Sort by tick for temporal ordering
            lineage.sort(key=lambda x: x.get("tick", 0))
            return lineage
        except FileNotFoundError:
            print(f"[Visualizer] ❌ Lineage file not found: {self.lineage_path}")
            return []
            
    def build_graph(self, lineage: List[Dict]) -> nx.DiGraph:
        """Build NetworkX graph from lineage data"""
        G = nx.DiGraph()
        
        for bloom in lineage:
            # VAL cognition trace
            self.cognition_log.append(
                f"VAL sees: bloom_id={bloom['bloom_id']} | "
                f"mood={bloom.get('mood', 'unknown')} | "
                f"entropy={bloom.get('entropy', 0):.3f} | "
                f"depth={bloom.get('depth', 0)}"
            )
            
            node_id = bloom["bloom_id"]
            parent_id = bloom.get("parent_id")
            
            # Add node with attributes
            G.add_node(
                node_id,
                mood=bloom.get("mood", "unknown"),
                entropy=bloom.get("entropy", 0),
                depth=bloom.get("depth", 0),
                tick=bloom.get("tick", 0)
            )
            
            # Add edge if parent exists
            if parent_id and parent_id in G:
                G.add_edge(parent_id, node_id)
                
        return G
        
    def analyze_tree_health(self, G: nx.DiGraph) -> Dict:
        """Analyze tree structure health metrics"""
        if G.number_of_nodes() == 0:
            return {"status": "empty", "broken_chains": 0, "penalty": 0}
            
        # Find leaves and broken chains
        leaves = [n for n in G.nodes if G.out_degree(n) == 0]
        broken_roots = sum(1 for n in G.nodes 
                          if G.in_degree(n) == 0 and G.nodes[n].get('depth', 0) > 0)
        
        # Calculate metrics
        max_depth = max(nx.get_node_attributes(G, 'depth').values(), default=0)
        avg_entropy = sum(nx.get_node_attributes(G, 'entropy').values()) / G.number_of_nodes()
        
        # Calculate broken chain penalty
        penalty_ratio = broken_roots / G.number_of_nodes()
        penalty = round(min(0.2, penalty_ratio * 0.5), 4)
        
        print(f"[Owl] 🪶 Tree Analysis:")
        print(f"  Leaves: {len(leaves)}")
        print(f"  Max Depth: {max_depth}")
        print(f"  Avg Entropy: {avg_entropy:.3f}")
        print(f"  Broken Roots: {broken_roots}")
        print(f"[SHI] 📊 Broken chain penalty = {penalty} "
              f"({broken_roots}/{G.number_of_nodes()} nodes)")
        
        # Save to SHI file
        self._update_schema_health(penalty)
        
        return {
            "leaves": len(leaves),
            "max_depth": max_depth,
            "avg_entropy": avg_entropy,
            "broken_roots": broken_roots,
            "penalty": penalty,
            "total_nodes": G.number_of_nodes()
        }
        
    def _update_schema_health(self, penalty: float):
        """Update schema health index with broken chain penalty"""
        shi_path = os.path.join(self.output_dir, "schema_health_curve.csv")
        
        # Try to inject into live SCUP/SHI
        try:
            from schema.schema_health_index import update_schema_health
            update_schema_health(1.0 - penalty)
        except Exception as e:
            print(f"[SHI] ⚠️ Failed to inject penalty into SCUP: {e}")
        
        # Save to file
        with open(shi_path, "a") as f:
            f.write(f"BROKEN_CHAIN,{penalty}\n")
            
    def create_static_visualization(self, G: nx.DiGraph, save_path: Optional[str] = None):
        """Create static tree visualization"""
        if save_path is None:
            save_path = os.path.join(self.output_dir, "rebloom_tree.png")
            
        # Layout
        pos = nx.spring_layout(G, seed=42, k=2, iterations=50)
        
        # Node colors based on mood
        moods = nx.get_node_attributes(G, 'mood')
        mood_colors = {
            'curious': '#FFD700',
            'anxious': '#FF6B6B',
            'reflective': '#4ECDC4',
            'focused': '#95E1D3',
            'joyful': '#FFF89E',
            'sad': '#A8DADC',
            'overload': '#FF006E'
        }
        colors = [mood_colors.get(moods.get(n, 'unknown'), '#C0C0C0') for n in G.nodes]
        
        # Node sizes based on entropy
        entropies = nx.get_node_attributes(G, 'entropy')
        sizes = [300 + entropies.get(n, 0.5) * 600 for n in G.nodes]
        
        # Create figure
        plt.figure(figsize=(14, 10))
        
        # Draw network
        nx.draw(G, pos, 
                node_color=colors,
                node_size=sizes,
                with_labels=True,
                font_size=8,
                font_weight='bold',
                arrows=True,
                edge_color='gray',
                alpha=0.8)
        
        plt.title("🧬 Rebloom Ancestry Tree", fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"[Tree] 🌿 Static tree saved to: {save_path}")
        
    def create_animated_visualization(self, lineage: List[Dict], save_path: Optional[str] = None):
        """Create animated tree growth visualization"""
        if save_path is None:
            save_path = os.path.join(self.output_dir, "rebloom_tree_animation.gif")
            
        # Get unique ticks
        ticks = sorted(set(entry.get("tick", 0) for entry in lineage))
        if not ticks:
            ticks = [0]
            
        fig, ax = plt.subplots(figsize=(12, 8))
        
        def update(frame_tick):
            ax.clear()
            
            # Build graph up to current tick
            current_nodes = [b for b in lineage if b.get("tick", 0) <= frame_tick]
            G_current = nx.DiGraph()
            
            for bloom in current_nodes:
                node_id = bloom["bloom_id"]
                parent_id = bloom.get("parent_id")
                
                G_current.add_node(
                    node_id,
                    mood=bloom.get("mood", "unknown"),
                    entropy=bloom.get("entropy", 0)
                )
                
                if parent_id and parent_id in G_current:
                    G_current.add_edge(parent_id, node_id)
            
            if G_current.number_of_nodes() == 0:
                ax.text(0.5, 0.5, "No blooms yet...", 
                       ha='center', va='center', transform=ax.transAxes)
                ax.set_title(f"🧬 Rebloom Tree — Tick {frame_tick}")
                return
            
            # Layout and colors
            pos = nx.spring_layout(G_current, seed=42)
            moods = nx.get_node_attributes(G_current, 'mood')
            colors = [plt.cm.tab10(hash(moods.get(n, 'unknown')) % 10) for n in G_current.nodes]
            
            # Sizes based on entropy
            entropies = nx.get_node_attributes(G_current, 'entropy')
            sizes = [300 + entropies.get(n, 0.5) * 600 for n in G_current.nodes]
            
            # Draw
            nx.draw(G_current, pos,
                   node_color=colors,
                   node_size=sizes,
                   with_labels=True,
                   ax=ax,
                   font_size=6,
                   arrows=True)
            
            ax.set_title(f"🧬 Rebloom Tree — Tick {frame_tick}")
            
        # Create animation
        ani = FuncAnimation(fig, update, frames=ticks, interval=1000, repeat=True)
        
        # Save
        ani.save(save_path, writer="pillow", fps=1)
        plt.close()
        
        print(f"[Tree] 🎬 Animation saved to: {save_path}")
        
    def visualize_complete(self):
        """Run complete visualization pipeline"""
        # Load data
        lineage = self.load_lineage_data()
        if not lineage:
            return
            
        # Build graph
        self.G = self.build_graph(lineage)
        
        # Analyze health
        health_metrics = self.analyze_tree_health(self.G)
        
        # Create visualizations
        self.create_static_visualization(self.G)
        self.create_animated_visualization(lineage)
        
        # Print cognition log samples
        print("\n[VAL] 🧠 Recent cognition traces:")
        for entry in self.cognition_log[-5:]:
            print(f"  {entry}")
            
        return health_metrics


class DriftAnimator:
    """Animates drift score evolution over time"""
    
    def __init__(self, log_dir: str = "juliet_flowers/cluster_report"):
        self.log_dir = log_dir
        
    def load_drift_sequence(self) -> List[float]:
        """Load drift scores from log files"""
        scores = []
        
        try:
            # Look for drift log files
            for fname in sorted(os.listdir(self.log_dir)):
                if fname.startswith("vector_drift_") and fname.endswith(".log"):
                    with open(os.path.join(self.log_dir, fname), encoding="utf-8") as f:
                        for line in f:
                            if "Drift Score" in line:
                                score = float(line.strip().split(": ")[-1])
                                scores.append(score)
        except Exception as e:
            print(f"[DriftAnimator] ⚠️ Error loading drift scores: {e}")
            
        return scores
        
    def animate_drift(self, scores: List[float], save_path: Optional[str] = None):
        """Create animated drift score visualization"""
        if not scores:
            print("[DriftAnimator] ❌ No drift scores to animate")
            return
            
        if save_path is None:
            save_path = os.path.join(self.log_dir, "drift_by_tick.gif")
            
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title("Semantic Drift Score Evolution", fontsize=14, fontweight='bold')
        ax.set_xlabel("Tick")
        ax.set_ylabel("Drift Score")
        ax.set_xlim(0, len(scores))
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)
        
        line, = ax.plot([], [], "bo-", markersize=4)
        
        def update(frame):
            x = list(range(frame + 1))
            y = scores[:frame + 1]
            line.set_data(x, y)
            
            # Color based on drift level
            if frame > 0:
                current_drift = scores[frame]
                if current_drift > 0.7:
                    line.set_color('red')
                elif current_drift > 0.4:
                    line.set_color('orange')
                else:
                    line.set_color('green')
                    
            return line,
            
        ani = FuncAnimation(fig, update, frames=len(scores), 
                           interval=300, repeat=False, blit=True)
        
        # Save animation
        ani.save(save_path, writer="pillow")
        plt.close()
        
        print(f"[Animation] 🎞️ Drift animation saved: {save_path}")
        
    def create_drift_analysis_plot(self, scores: List[float], save_path: Optional[str] = None):
        """Create static drift analysis plot"""
        if not scores:
            return
            
        if save_path is None:
            save_path = os.path.join(self.log_dir, "drift_analysis.png")
            
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Time series plot
        ax1.plot(scores, 'b-', linewidth=2)
        ax1.fill_between(range(len(scores)), scores, alpha=0.3)
        ax1.set_title("Drift Score Time Series", fontsize=12)
        ax1.set_xlabel("Tick")
        ax1.set_ylabel("Drift Score")
        ax1.grid(True, alpha=0.3)
        
        # Add danger zones
        ax1.axhline(y=0.7, color='r', linestyle='--', alpha=0.5, label='Danger Zone')
        ax1.axhline(y=0.4, color='orange', linestyle='--', alpha=0.5, label='Warning Zone')
        ax1.legend()
        
        # Distribution plot
        ax2.hist(scores, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
        ax2.set_title("Drift Score Distribution", fontsize=12)
        ax2.set_xlabel("Drift Score")
        ax2.set_ylabel("Frequency")
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add statistics
        mean_drift = np.mean(scores)
        std_drift = np.std(scores)
        ax2.axvline(mean_drift, color='red', linestyle='--', 
                   label=f'Mean: {mean_drift:.3f}')
        ax2.axvline(mean_drift + std_drift, color='orange', linestyle=':', 
                   label=f'Std: ±{std_drift:.3f}')
        ax2.axvline(mean_drift - std_drift, color='orange', linestyle=':')
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"[Analysis] 📊 Drift analysis saved: {save_path}")
        
    def run_complete_analysis(self):
        """Run complete drift analysis pipeline"""
        scores = self.load_drift_sequence()
        
        if scores:
            self.animate_drift(scores)
            self.create_drift_analysis_plot(scores)
            
            # Print summary statistics
            print(f"\n[Drift] 📊 Summary Statistics:")
            print(f"  Total ticks: {len(scores)}")
            print(f"  Mean drift: {np.mean(scores):.3f}")
            print(f"  Max drift: {max(scores):.3f}")
            print(f"  Min drift: {min(scores):.3f}")
            print(f"  Current drift: {scores[-1]:.3f}")
        else:
            print("[Drift] ❌ No drift data found")


class LineageAnimator:
    """Creates rebloom lineage animations from CSV logs"""
    
    def __init__(self, log_path: str = "logs/rebloom_summary_log.csv"):
        self.log_path = log_path
        self.output_dir = ANIMATION_OUTPUT_DIR
        
    def animate_rebloom_lineage(self, save_path: Optional[str] = None):
        """Create animated lineage network from CSV"""
        if save_path is None:
            save_path = os.path.join(self.output_dir, "rebloom_lineage_animation.gif")
            
        try:
            df = pd.read_csv(self.log_path)
        except FileNotFoundError:
            print(f"[LineageAnimator] ❌ Log file not found: {self.log_path}")
            return
            
        G = nx.DiGraph()
        ticks = sorted(df["tick_id"].astype(str).unique())
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        def update(tick):
            ax.clear()
            
            # Get data up to current tick
            partial = df[df["tick_id"] <= int(tick)]
            G.clear()
            
            # Build graph
            for _, row in partial.iterrows():
                seed = row["seed_id"]
                ancestry = row.get("ancestry_tag", "untagged")
                
                G.add_node(seed)
                if ancestry != "untagged" and ancestry in G:
                    G.add_edge(ancestry, seed)
                    
            if G.number_of_nodes() == 0:
                ax.text(0.5, 0.5, "No reblooms yet...", 
                       ha='center', va='center', transform=ax.transAxes)
            else:
                pos = nx.spring_layout(G, seed=42)
                nx.draw(G, pos, 
                       with_labels=True,
                       node_color="lightgreen",
                       edge_color="gray",
                       arrows=True,
                       ax=ax,
                       node_size=500,
                       font_size=8)
                       
            ax.set_title(f"🕸️ Rebloom Lineage Overlay — Tick {tick}")
            
        # Create animation
        ani = animation.FuncAnimation(fig, update, frames=ticks, 
                                     repeat=False, interval=500)
        
        # Save
        os.makedirs(self.output_dir, exist_ok=True)
        ani.save(save_path, writer="pillow")
        plt.close()
        
        print(f"[LineageAnimator] 🎬 Animation saved: {save_path}")


# ============== Unified Visualization Runner ==============

def run_all_visualizations():
    """Run all visualization pipelines"""
    print("🎨 Starting Unified Visualization System")
    print("=" * 50)
    
    # Rebloom tree visualization
    print("\n1. Rebloom Tree Visualization...")
    tree_viz = RebloomTreeVisualizer()
    tree_health = tree_viz.visualize_complete()
    
    # Drift animation
    print("\n2. Drift Score Animation...")
    drift_animator = DriftAnimator()
    drift_animator.run_complete_analysis()
    
    # Lineage animation
    print("\n3. Lineage Network Animation...")
    lineage_animator = LineageAnimator()
    lineage_animator.animate_rebloom_lineage()
    
    print("\n✅ All visualizations complete!")
    
    return {
        "tree_health": tree_health,
        "outputs": {
            "static_tree": os.path.join(VISUAL_OUTPUT_DIR, "rebloom_tree.png"),
            "tree_animation": os.path.join(VISUAL_OUTPUT_DIR, "rebloom_tree_animation.gif"),
            "drift_animation": os.path.join(VISUAL_OUTPUT_DIR, "drift_by_tick.gif"),
            "drift_analysis": os.path.join(VISUAL_OUTPUT_DIR, "drift_analysis.png"),
            "lineage_animation": os.path.join(ANIMATION_OUTPUT_DIR, "rebloom_lineage_animation.gif")
        }
    }


if __name__ == "__main__":
    results = run_all_visualizations()
    
    print("\n📊 Visualization Summary:")
    print(json.dumps(results, indent=2))