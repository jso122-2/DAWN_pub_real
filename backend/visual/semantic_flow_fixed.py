#!/usr/bin/env python3
"""
DAWN Semantic Flow Graph Visualizer - Fixed
Real-time visualization of semantic flow patterns with pure matplotlib
"""

# Configure matplotlib for headless operation
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, FancyBboxPatch
import json
import os
import sys
import argparse
import time
from collections import deque
import random
import math
from typing import Dict, List

class SemanticFlowGraph:
    """Semantic Flow Graph Visualization"""
    
    def __init__(self, data_source='stdin', save_frames=False, output_dir="./visual_output"):
        self.save_frames = save_frames
        self.output_dir = output_dir
        self.frame_count = 0
        
        # Create output directory if saving
        if self.save_frames:
            os.makedirs(self.output_dir, exist_ok=True)
        
        self.data_source = data_source
        
        # Semantic concept categories
        self.categories = {
            'perceptual': {'color': '#00bcd4', 'concepts': ['color', 'sound', 'texture', 'pattern']},
            'emotional': {'color': '#e91e63', 'concepts': ['joy', 'curiosity', 'tension', 'calm']},
            'abstract': {'color': '#9c27b0', 'concepts': ['pattern', 'structure', 'system', 'complexity']},
            'temporal': {'color': '#ff9800', 'concepts': ['change', 'rhythm', 'sequence', 'moment']},
            'spatial': {'color': '#4caf50', 'concepts': ['boundary', 'center', 'direction', 'position']},
            'meta': {'color': '#607d8b', 'concepts': ['awareness', 'thought', 'meaning', 'understanding']}
        }
        
        # Initialize concepts and network
        self.concepts = {}
        self.flows = []
        self.active_concepts = set()
        
        self._initialize_concepts()
        self.setup_visualization()
        
    def _initialize_concepts(self):
        """Initialize semantic concepts with positions"""
        concept_id = 0
        for category, info in self.categories.items():
            for i, concept_name in enumerate(info['concepts']):
                # Position concepts in category clusters
                angle = (i / len(info['concepts'])) * 2 * np.pi
                category_angle = list(self.categories.keys()).index(category) * np.pi / 3
                
                radius = 3 + random.uniform(-0.5, 0.5)
                x = radius * np.cos(angle + category_angle)
                y = radius * np.sin(angle + category_angle)
                
                self.concepts[concept_name] = {
                    'id': concept_id,
                    'category': category,
                    'x': x,
                    'y': y,
                    'activation': 0.0,
                    'size': 50,
                    'glow': 0.0,
                    'neighbors': []
                }
                concept_id += 1
        
        # Create semantic connections
        self._create_connections()
    
    def _create_connections(self):
        """Create semantic connections between concepts"""
        # Within-category connections
        for category, info in self.categories.items():
            concepts = info['concepts']
            for i, concept1 in enumerate(concepts):
                for concept2 in concepts[i+1:]:
                    if concept1 in self.concepts and concept2 in self.concepts:
                        self.concepts[concept1]['neighbors'].append(concept2)
                        self.concepts[concept2]['neighbors'].append(concept1)
        
        # Cross-category connections
        cross_connections = [
            ('pattern', 'structure'), ('change', 'rhythm'), ('joy', 'color'),
            ('awareness', 'meaning'), ('boundary', 'position'), ('texture', 'pattern'),
            ('curiosity', 'understanding'), ('system', 'structure')
        ]
        
        for concept1, concept2 in cross_connections:
            if concept1 in self.concepts and concept2 in self.concepts:
                self.concepts[concept1]['neighbors'].append(concept2)
                self.concepts[concept2]['neighbors'].append(concept1)
    
    def setup_visualization(self):
        """Initialize matplotlib visualization"""
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(1, 1, figsize=(16, 10), facecolor='#0a0a0a')
        
        # Configure axes
        self.ax.set_xlim(-8, 8)
        self.ax.set_ylim(-6, 6)
        self.ax.set_facecolor('#0a0a0a')
        self.ax.set_aspect('equal')
        
        # Styling
        self.ax.set_title('DAWN Semantic Flow Graph', color='white', 
                         fontsize=16, fontweight='bold', pad=20)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Remove spines
        for spine in self.ax.spines.values():
            spine.set_visible(False)
            
        # Add subtle grid
        self.ax.grid(True, alpha=0.1, color='gray')
    
    def parse_semantic_data(self, json_data):
        """Extract semantic activations from DAWN JSON output"""
        activations = {}
        
        # Extract various cognitive states
        thermal = json_data.get('thermal', {})
        heat = thermal.get('heat', 0.0)
        entropy = json_data.get('entropy', 0.5)
        scup = json_data.get('scup', {})
        mood = json_data.get('mood', {})
        
        # Map cognitive states to semantic concepts
        if heat > 0.6:
            activations['pattern'] = heat
            activations['structure'] = heat * 0.8
        
        if entropy > 0.7:
            activations['change'] = entropy
            activations['curiosity'] = entropy * 0.9
        
        coherence = scup.get('coherence', 0.5)
        if coherence > 0.6:
            activations['understanding'] = coherence
            activations['meaning'] = coherence * 0.8
        
        schema = scup.get('schema', 0.5)
        if schema > 0.5:
            activations['system'] = schema
            activations['complexity'] = schema * 0.7
        
        # Emotional mappings
        base_level = mood.get('base_level', 0.5)
        if base_level > 0.6:
            activations['joy'] = base_level - 0.5
        elif base_level < 0.4:
            activations['tension'] = 0.5 - base_level
        
        # Perceptual activations based on entropy patterns
        if entropy > 0.8:
            activations['color'] = min(1.0, entropy)
            activations['texture'] = min(1.0, entropy * 0.8)
        
        # Temporal activations
        if abs(heat - 0.5) > 0.3:
            activations['moment'] = abs(heat - 0.5) * 2
            activations['rhythm'] = min(1.0, abs(heat - 0.5) * 1.5)
        
        # Meta-cognitive activations
        if coherence > 0.7 and schema > 0.6:
            activations['awareness'] = min(1.0, (coherence + schema) / 2)
            activations['thought'] = min(1.0, coherence * 0.9)
        
        return activations
    
    def create_flow(self, source, target, strength):
        """Create a flow between two concepts"""
        if source in self.concepts and target in self.concepts:
            flow = {
                'source': source,
                'target': target,
                'strength': strength,
                'progress': 0.0,
                'speed': 0.02,
                'color': self.categories[self.concepts[source]['category']]['color']
            }
            self.flows.append(flow)
    
    def update_flows(self):
        """Update flow animations"""
        completed_flows = []
        
        for i, flow in enumerate(self.flows):
            flow['progress'] += flow['speed']
            
            if flow['progress'] >= 1.0:
                # Flow completed - activate target
                target = flow['target']
                if target in self.concepts:
                    self.concepts[target]['activation'] = min(1.0, 
                        self.concepts[target]['activation'] + flow['strength'] * 0.3)
                    self.concepts[target]['glow'] = 1.0
                completed_flows.append(i)
        
        # Remove completed flows
        for i in reversed(completed_flows):
            self.flows.pop(i)
    
    def update_concepts(self):
        """Update concept states"""
        for concept in self.concepts.values():
            # Decay activation
            concept['activation'] *= 0.95
            concept['glow'] *= 0.9
            
            # Update visual properties
            base_size = 50
            concept['size'] = base_size + concept['activation'] * 100
    
    def draw_connections(self):
        """Draw semantic connections"""
        drawn_connections = set()
        
        for concept_name, concept in self.concepts.items():
            for neighbor in concept['neighbors']:
                # Avoid drawing duplicate connections
                connection = tuple(sorted([concept_name, neighbor]))
                if connection in drawn_connections:
                    continue
                drawn_connections.add(connection)
                
                if neighbor in self.concepts:
                    neighbor_concept = self.concepts[neighbor]
                    
                    # Line strength based on activation
                    strength = (concept['activation'] + neighbor_concept['activation']) / 2
                    alpha = 0.2 + strength * 0.5
                    
                    self.ax.plot([concept['x'], neighbor_concept['x']], 
                               [concept['y'], neighbor_concept['y']], 
                               'white', alpha=alpha, linewidth=1)
    
    def draw_flows(self):
        """Draw active semantic flows"""
        for flow in self.flows:
            source = self.concepts[flow['source']]
            target = self.concepts[flow['target']]
            
            # Interpolate position along connection
            progress = flow['progress']
            x = source['x'] + (target['x'] - source['x']) * progress
            y = source['y'] + (target['y'] - source['y']) * progress
            
            # Draw flow particle
            size = 20 + flow['strength'] * 30
            alpha = 0.7 + 0.3 * np.sin(self.frame_count * 0.3)
            
            self.ax.scatter(x, y, s=size, c=flow['color'], alpha=alpha, 
                           edgecolors='white', linewidths=1, zorder=20)
    
    def draw_concepts(self):
        """Draw semantic concepts"""
        for concept_name, concept in self.concepts.items():
            category = concept['category']
            color = self.categories[category]['color']
            
            # Base circle
            size = concept['size']
            alpha = 0.6 + concept['activation'] * 0.4
            
            self.ax.scatter(concept['x'], concept['y'], s=size, c=color, 
                           alpha=alpha, edgecolors='white', linewidths=2, zorder=10)
            
            # Glow effect for active concepts
            if concept['glow'] > 0.1:
                glow_size = size * (1 + concept['glow'])
                glow_alpha = concept['glow'] * 0.3
                self.ax.scatter(concept['x'], concept['y'], s=glow_size, 
                               c=color, alpha=glow_alpha, zorder=5)
            
            # Label for highly active concepts
            if concept['activation'] > 0.3:
                self.ax.text(concept['x'], concept['y'] - 0.5, concept_name,
                            color='white', fontsize=8, ha='center', va='top',
                            alpha=concept['activation'])
    
    def draw_legend(self):
        """Draw category legend"""
        legend_x = -7.5
        legend_y = 5.5
        
        self.ax.text(legend_x, legend_y, 'Semantic Categories', 
                    color='white', fontsize=12, fontweight='bold')
        
        for i, (category, info) in enumerate(self.categories.items()):
            y_pos = legend_y - 0.6 - i * 0.4
            
            # Color indicator
            self.ax.scatter(legend_x, y_pos, s=30, c=info['color'], alpha=0.8)
            
            # Category name
            self.ax.text(legend_x + 0.3, y_pos, category.title(), 
                        color='white', fontsize=9, va='center')
    
    def draw_statistics(self):
        """Draw network statistics"""
        active_count = sum(1 for c in self.concepts.values() if c['activation'] > 0.1)
        flow_count = len(self.flows)
        
        stats_text = f"Active Concepts: {active_count} | Flows: {flow_count}"
        self.ax.text(0, -5.5, stats_text, color='white', fontsize=12, 
                    ha='center', bbox=dict(boxstyle="round,pad=0.3", 
                                         facecolor='black', alpha=0.7))
    
    def generate_demo_data(self, frame):
        """Generate demonstration data"""
        t = frame * 0.02
        return {
            'thermal': {'heat': 0.5 + 0.3 * np.sin(t)},
            'entropy': 0.5 + 0.3 * np.cos(t * 0.7),
            'tick_count': 20000 + frame,
            'scup': {
                'schema': 0.5 + 0.25 * np.sin(t * 1.3),
                'coherence': 0.5 + 0.25 * np.cos(t * 1.7),
                'utility': 0.5 + 0.2 * np.sin(t * 0.9),
                'pressure': 0.3 + 0.4 * abs(np.sin(t * 0.5))
            },
            'mood': {'base_level': 0.6 + 0.2 * np.sin(t * 0.3)}
        }

    def update_visualization(self, frame):
        """Animation update function"""
        try:
            # Get data
            if self.data_source == 'stdin':
                try:
                    line = sys.stdin.readline().strip()
                    if line:
                        data = json.loads(line)
                    else:
                        data = self.generate_demo_data(frame)
                except:
                    data = self.generate_demo_data(frame)
            else:
                data = self.generate_demo_data(frame)
            
            # Parse semantic activations
            activations = self.parse_semantic_data(data)
            
            # Activate concepts and create flows
            for concept_name, activation in activations.items():
                if concept_name in self.concepts:
                    concept = self.concepts[concept_name]
                    concept['activation'] = min(1.0, concept['activation'] + activation)
                    concept['glow'] = 1.0
                    self.active_concepts.add(concept_name)
                    
                    # Create flows to neighbors
                    for neighbor in concept['neighbors']:
                        if random.random() < activation * 0.3:  # Random flow chance
                            self.create_flow(concept_name, neighbor, activation)
            
            # Update system
            self.update_flows()
            self.update_concepts()
            
            # Clear and redraw
            self.ax.clear()
            
            # Reset visualization
            self.ax.set_xlim(-8, 8)
            self.ax.set_ylim(-6, 6)
            self.ax.set_facecolor('#0a0a0a')
            self.ax.set_aspect('equal')
            self.ax.set_title('DAWN Semantic Flow Graph', color='white', 
                             fontsize=16, fontweight='bold', pad=20)
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            for spine in self.ax.spines.values():
                spine.set_visible(False)
            self.ax.grid(True, alpha=0.1, color='gray')
            
            # Draw components
            self.draw_connections()
            self.draw_flows()
            self.draw_concepts()
            self.draw_legend()
            self.draw_statistics()
            
            # Save frame if requested
            if self.save_frames and self.frame_count % 10 == 0:
                filename = f"{self.output_dir}/semantic_flow_frame_{self.frame_count:06d}.png"
                self.fig.savefig(filename, dpi=100, bbox_inches='tight',
                               facecolor='#0a0a0a', edgecolor='none')
            
            self.frame_count += 1
            
            return []
            
        except Exception as e:
            print(f"Update error: {e}", file=sys.stderr)
            return []

    def run(self, interval=100):
        if self.save_frames:
            # Headless mode: process stdin and save frames
            frame_count = 0
            try:
                for line in sys.stdin:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        self.update_visualization(frame_count)
                        frame_count += 1
                        if frame_count % 50 == 0:
                            print(f"Processed frame {frame_count}", file=sys.stderr)
                        if frame_count >= 1000:
                            break
                    except json.JSONDecodeError:
                        continue
            except KeyboardInterrupt:
                pass
            print(f"Semantic Flow Graph saved {frame_count} frames to: {self.output_dir}")
        else:
            # Interactive mode
            try:
                self.animation = animation.FuncAnimation(
                    self.fig,
                    self.update_visualization,
                    frames=1000,
                    interval=interval,
                    blit=False,
                    cache_frame_data=False
                )
                plt.show()
            except Exception as e:
                print(f"Runtime error: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description='DAWN Semantic Flow Graph - Fixed')
    parser.add_argument('--source', choices=['stdin', 'demo'], default='stdin',
                       help='Data source (default: stdin)')
    parser.add_argument('--save', action='store_true',
                       help='Save visualization frames as PNG files')
    parser.add_argument('--output-dir', default='./visual_output/semantic_flow',
                       help='Directory to save output frames')
    
    args = parser.parse_args()
    
    viz = SemanticFlowGraph(
        data_source=args.source,
        save_frames=args.save,
        output_dir=args.output_dir
    )
    
    viz.run()

if __name__ == '__main__':
    main() 