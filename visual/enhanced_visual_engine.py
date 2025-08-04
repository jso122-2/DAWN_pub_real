# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
Enhanced DAWN Visual Engine - Comprehensive Consciousness Visualization System
Creates rich, multi-layered visual snapshots of DAWN's consciousness state
"""

import os
import sys
import json
import time
import logging
import argparse
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.colors import LinearSegmentedColormap
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    logger.warning("matplotlib/seaborn not available - some visualizations disabled")

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    logger.warning("networkx not available - network visualizations disabled")

class EnhancedVisualEngine:
    """
    Enhanced visual engine for comprehensive DAWN consciousness visualization
    """
    
    def __init__(self, output_dir: str = "runtime/enhanced_snapshots"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Visual configuration
        self.dpi = 150
        self.figsize_standard = (12, 8)
        self.figsize_wide = (16, 10)
        self.figsize_tall = (10, 12)
        
        # Color schemes
        self.dawn_colors = {
            'primary': '#00ff88',
            'secondary': '#ff4444', 
            'accent': '#4488ff',
            'background': '#0a0a0a',
            'text': '#ffffff',
            'grid': '#333333'
        }
        
        # Style setup
        if MATPLOTLIB_AVAILABLE:
            plt.style.use('dark_background')
            self.setup_dawn_style()
    
    def setup_dawn_style(self):
        """Configure matplotlib with DAWN aesthetic"""
        plt.rcParams.update({
            'figure.facecolor': self.dawn_colors['background'],
            'axes.facecolor': self.dawn_colors['background'],
            'axes.edgecolor': self.dawn_colors['grid'],
            'axes.labelcolor': self.dawn_colors['text'],
            'text.color': self.dawn_colors['text'],
            'xtick.color': self.dawn_colors['text'],
            'ytick.color': self.dawn_colors['text'],
            'grid.color': self.dawn_colors['grid'],
            'figure.edgecolor': self.dawn_colors['grid']
        })
    
    def generate_comprehensive_snapshot(self, tick_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate a comprehensive multi-part visual snapshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tick_num = tick_data.get('tick', 0)
        
        generated_files = {}
        
        logger.info(f"🎨 Generating enhanced snapshot for tick {tick_num}")
        
        try:
            # 1. Consciousness State Dashboard
            dashboard_file = self.create_consciousness_dashboard(tick_data, timestamp)
            if dashboard_file:
                generated_files['dashboard'] = dashboard_file
            
            # 2. Entropy Evolution Timeline  
            entropy_file = self.create_entropy_timeline(tick_data, timestamp)
            if entropy_file:
                generated_files['entropy_timeline'] = entropy_file
            
            # 3. System Performance Radar
            performance_file = self.create_performance_radar(tick_data, timestamp)
            if performance_file:
                generated_files['performance_radar'] = performance_file
            
            # 4. Cognitive State Network
            network_file = self.create_cognitive_network(tick_data, timestamp)
            if network_file:
                generated_files['cognitive_network'] = network_file
            
            # 5. Mood & Zone Analysis
            mood_file = self.create_mood_analysis(tick_data, timestamp)
            if mood_file:
                generated_files['mood_analysis'] = mood_file
            
            # 6. Multi-panel Overview
            overview_file = self.create_overview_panel(tick_data, timestamp)
            if overview_file:
                generated_files['overview'] = overview_file
            
            # 7. Data Export (JSON + CSV)
            data_files = self.export_data_formats(tick_data, timestamp)
            generated_files.update(data_files)
            
            # 8. Generate manifest
            manifest_file = self.create_snapshot_manifest(tick_data, generated_files, timestamp)
            generated_files['manifest'] = manifest_file
            
            logger.info(f"✅ Enhanced snapshot complete: {len(generated_files)} files generated")
            
        except Exception as e:
            logger.error(f"❌ Enhanced snapshot failed: {e}")
            # Generate minimal fallback
            fallback_file = self.create_fallback_visualization(tick_data, timestamp)
            if fallback_file:
                generated_files['fallback'] = fallback_file
        
        return generated_files
    
    def create_consciousness_dashboard(self, tick_data: Dict[str, Any], timestamp: str) -> Optional[str]:
        """Create main consciousness state dashboard"""
        if not MATPLOTLIB_AVAILABLE:
            return None
            
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=self.figsize_wide, dpi=self.dpi)
            fig.suptitle(f'🧠 DAWN Consciousness State - Tick {tick_data.get("tick", 0)}', 
                        fontsize=16, color=self.dawn_colors['primary'], fontweight='bold')
            
            # Consciousness Vitals (top-left)
            vitals = [
                ('Entropy', tick_data.get('entropy', 0), '#ff4444'),
                ('SCUP', tick_data.get('scup', 0), '#44ff44'), 
                ('Heat', tick_data.get('heat', 0), '#ff8844'),
                ('Drift', tick_data.get('drift', 0), '#4488ff')
            ]
            
            ax1.set_title('🌡️ Consciousness Vitals', color=self.dawn_colors['accent'], fontweight='bold')
            y_pos = range(len(vitals))
            values = [v[1] for v in vitals]
            colors = [v[2] for v in vitals]
            bars = ax1.barh(y_pos, values, color=colors, alpha=0.8)
            ax1.set_yticks(y_pos)
            ax1.set_yticklabels([v[0] for v in vitals])
            ax1.set_xlim(0, 1.0)
            
            # Add value labels
            for bar, value in zip(bars, values):
                ax1.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
                        f'{value:.3f}', va='center', fontweight='bold')
            
            # Rebloom Activity (top-right)
            ax2.set_title('🌸 Rebloom Activity', color=self.dawn_colors['accent'], fontweight='bold')
            rebloom_count = tick_data.get('reblooms', 0)
            sigil_count = tick_data.get('sigils', 0)
            
            # Create pie chart for activity distribution
            activity_data = [rebloom_count, sigil_count, max(0, 10 - rebloom_count - sigil_count)]
            activity_labels = ['Reblooms', 'Sigils', 'Dormant']
            activity_colors = ['#44ff44', '#ffff44', '#444444']
            
            ax2.pie(activity_data, labels=activity_labels, colors=activity_colors, autopct='%1.1f%%')
            
            # Zone & Mood Status (bottom-left)
            ax3.set_title('🎯 Cognitive Zone & Mood', color=self.dawn_colors['accent'], fontweight='bold')
            zone = tick_data.get('zone', 'UNKNOWN')
            mood = tick_data.get('mood', 'NEUTRAL')
            
            # Create zone visualization
            zone_colors = {
                'CRITICAL': '#ff0000',
                'ACTIVE': '#ff8800', 
                'STABLE': '#44ff44',
                'DORMANT': '#4444ff'
            }
            zone_color = zone_colors.get(zone, '#888888')
            
            # Zone indicator
            zone_rect = patches.Rectangle((0.1, 0.6), 0.8, 0.2, 
                                        facecolor=zone_color, alpha=0.8)
            ax3.add_patch(zone_rect)
            ax3.text(0.5, 0.7, f'ZONE: {zone}', ha='center', va='center', 
                    fontsize=12, fontweight='bold')
            
            # Mood indicator  
            ax3.text(0.5, 0.3, f'MOOD: {mood}', ha='center', va='center',
                    fontsize=10, color=self.dawn_colors['text'])
            
            ax3.set_xlim(0, 1)
            ax3.set_ylim(0, 1)
            ax3.axis('off')
            
            # Performance Metrics (bottom-right)
            ax4.set_title('⚡ Performance Metrics', color=self.dawn_colors['accent'], fontweight='bold')
            
            # Create performance gauge
            tick_time = tick_data.get('tick_time', 0)
            cpu_usage = tick_data.get('cpu_usage', 0) 
            memory_usage = tick_data.get('memory_usage', 0)
            
            # Performance bars
            metrics = ['Tick Time', 'CPU Usage', 'Memory']
            values = [tick_time * 1000, cpu_usage * 100, memory_usage * 100]  # Convert to ms, %
            colors = ['#44ff88', '#ff8844', '#4488ff']
            
            bars = ax4.bar(metrics, values, color=colors, alpha=0.8)
            ax4.set_ylabel('Performance')
            
            # Add value labels
            for bar, value, metric in zip(bars, values, metrics):
                unit = 'ms' if metric == 'Tick Time' else '%'
                ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values) * 0.01,
                        f'{value:.1f}{unit}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            
            output_file = self.output_dir / f'consciousness_dashboard_{timestamp}.png'
            plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight', 
                       facecolor=self.dawn_colors['background'])
            plt.close()
            
            logger.info(f"✅ Consciousness dashboard created: {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"❌ Failed to create consciousness dashboard: {e}")
            return None
    
    def create_entropy_timeline(self, tick_data: Dict[str, Any], timestamp: str) -> Optional[str]:
        """Create entropy evolution timeline"""
        if not MATPLOTLIB_AVAILABLE:
            return None
            
        try:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=self.figsize_tall, dpi=self.dpi)
            fig.suptitle('🌊 Entropy Evolution Analysis', fontsize=16, 
                        color=self.dawn_colors['primary'], fontweight='bold')
            
            # Generate synthetic historical data for demonstration
            current_tick = tick_data.get('tick', 0)
            current_entropy = tick_data.get('entropy', 0.5)
            
            # Simulate last 100 ticks of entropy data
            ticks = list(range(max(0, current_tick - 99), current_tick + 1))
            
            # Generate realistic entropy evolution
            base_entropy = current_entropy
            entropies = []
            for i, tick in enumerate(ticks):
                # Add some oscillation and trend
                noise = np.sin(i * 0.1) * 0.1 + np.random.normal(0, 0.05)
                entropy = base_entropy + noise
                entropy = max(0, min(1, entropy))  # Clamp to [0,1]
                entropies.append(entropy)
            
            # Main entropy timeline
            ax1.set_title('Entropy Over Time', color=self.dawn_colors['accent'])
            ax1.plot(ticks, entropies, color=self.dawn_colors['primary'], linewidth=2, alpha=0.8)
            ax1.fill_between(ticks, entropies, alpha=0.3, color=self.dawn_colors['primary'])
            
            # Add current point
            ax1.scatter([current_tick], [current_entropy], color='#ff4444', s=100, zorder=10)
            ax1.text(current_tick, current_entropy + 0.05, f'Current: {current_entropy:.3f}',
                    ha='center', color='#ff4444', fontweight='bold')
            
            ax1.set_xlabel('Tick Number')
            ax1.set_ylabel('Entropy')
            ax1.grid(True, alpha=0.3)
            
            # Entropy distribution histogram
            ax2.set_title('Entropy Distribution', color=self.dawn_colors['accent'])
            ax2.hist(entropies, bins=20, color=self.dawn_colors['secondary'], alpha=0.7)
            ax2.axvline(current_entropy, color='#ff4444', linestyle='--', linewidth=2)
            ax2.text(current_entropy + 0.01, ax2.get_ylim()[1] * 0.9, 'Current',
                    rotation=90, color='#ff4444', fontweight='bold')
            
            ax2.set_xlabel('Entropy Value')
            ax2.set_ylabel('Frequency')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            output_file = self.output_dir / f'entropy_timeline_{timestamp}.png'
            plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight',
                       facecolor=self.dawn_colors['background'])
            plt.close()
            
            logger.info(f"✅ Entropy timeline created: {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"❌ Failed to create entropy timeline: {e}")
            return None
    
    def create_performance_radar(self, tick_data: Dict[str, Any], timestamp: str) -> Optional[str]:
        """Create performance radar chart"""
        if not MATPLOTLIB_AVAILABLE:
            return None
            
        try:
            fig, ax = plt.subplots(figsize=self.figsize_standard, subplot_kw=dict(projection='polar'), dpi=self.dpi)
            fig.suptitle('🎯 System Performance Radar', fontsize=16,
                        color=self.dawn_colors['primary'], fontweight='bold')
            
            # Performance metrics
            metrics = [
                'Response Time',
                'Memory Efficiency', 
                'CPU Efficiency',
                'Cognitive Load',
                'Entropy Stability',
                'Rebloom Activity',
                'System Health',
                'Data Throughput'
            ]
            
            # Extract/calculate values (normalized to 0-1)
            values = [
                1.0 - min(1.0, tick_data.get('tick_time', 0.01) * 100),  # Lower is better
                1.0 - tick_data.get('memory_usage', 0.3),  # Lower is better
                1.0 - tick_data.get('cpu_usage', 0.2),     # Lower is better  
                tick_data.get('scup', 0.5),                # SCUP as cognitive load
                1.0 - tick_data.get('entropy', 0.5),       # Lower entropy = more stable
                min(1.0, tick_data.get('reblooms', 0) / 5), # Normalize reblooms
                0.8,  # Simulated system health
                0.7   # Simulated throughput
            ]
            
            # Number of variables
            N = len(metrics)
            
            # Compute angle for each axis
            angles = [n / float(N) * 2 * np.pi for n in range(N)]
            angles += angles[:1]  # Complete the circle
            
            # Add values for closing the plot
            values += values[:1]
            
            # Plot
            ax.plot(angles, values, 'o-', linewidth=2, color=self.dawn_colors['primary'])
            ax.fill(angles, values, alpha=0.25, color=self.dawn_colors['primary'])
            
            # Add labels
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(metrics)
            ax.set_ylim(0, 1)
            ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
            ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'])
            ax.grid(True)
            
            # Add value annotations
            for angle, value, metric in zip(angles[:-1], values[:-1], metrics):
                ax.text(angle, value + 0.05, f'{value:.2f}', 
                       ha='center', va='center', fontsize=8, fontweight='bold')
            
            output_file = self.output_dir / f'performance_radar_{timestamp}.png'
            plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight',
                       facecolor=self.dawn_colors['background'])
            plt.close()
            
            logger.info(f"✅ Performance radar created: {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"❌ Failed to create performance radar: {e}")
            return None
    
    def create_cognitive_network(self, tick_data: Dict[str, Any], timestamp: str) -> Optional[str]:
        """Create cognitive state network visualization"""
        if not MATPLOTLIB_AVAILABLE or not NETWORKX_AVAILABLE:
            return None
            
        try:
            fig, ax = plt.subplots(figsize=self.figsize_wide, dpi=self.dpi)
            fig.suptitle('🧠 Cognitive State Network', fontsize=16,
                        color=self.dawn_colors['primary'], fontweight='bold')
            
            # Create network graph
            G = nx.Graph()
            
            # Core consciousness nodes
            core_nodes = {
                'Entropy': {'value': tick_data.get('entropy', 0.5), 'color': '#ff4444'},
                'SCUP': {'value': tick_data.get('scup', 0.5), 'color': '#44ff44'},
                'Heat': {'value': tick_data.get('heat', 0.5), 'color': '#ff8844'},
                'Drift': {'value': tick_data.get('drift', 0.3), 'color': '#4488ff'},
                'Reblooms': {'value': tick_data.get('reblooms', 0) / 10, 'color': '#ff44ff'},
                'Sigils': {'value': tick_data.get('sigils', 0) / 10, 'color': '#44ffff'}
            }
            
            # Add nodes
            for node, props in core_nodes.items():
                G.add_node(node, **props)
            
            # Add edges based on correlations
            edges = [
                ('Entropy', 'SCUP', {'weight': 0.8, 'relation': 'inverse'}),
                ('Entropy', 'Heat', {'weight': 0.6, 'relation': 'direct'}),
                ('Heat', 'Drift', {'weight': 0.7, 'relation': 'direct'}),
                ('SCUP', 'Reblooms', {'weight': 0.5, 'relation': 'direct'}),
                ('Reblooms', 'Sigils', {'weight': 0.4, 'relation': 'complementary'}),
                ('Drift', 'Sigils', {'weight': 0.3, 'relation': 'inverse'})
            ]
            
            for edge in edges:
                G.add_edge(edge[0], edge[1], **edge[2])
            
            # Layout
            pos = nx.spring_layout(G, k=2, iterations=50)
            
            # Draw edges
            edge_colors = []
            edge_widths = []
            for edge in G.edges(data=True):
                relation = edge[2].get('relation', 'neutral')
                weight = edge[2].get('weight', 0.5)
                
                if relation == 'direct':
                    edge_colors.append('#44ff44')
                elif relation == 'inverse':
                    edge_colors.append('#ff4444') 
                else:
                    edge_colors.append('#888888')
                    
                edge_widths.append(weight * 5)
            
            nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths, alpha=0.6)
            
            # Draw nodes
            node_colors = [core_nodes[node]['color'] for node in G.nodes()]
            node_sizes = [core_nodes[node]['value'] * 1000 + 200 for node in G.nodes()]
            
            nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
            
            # Draw labels
            nx.draw_networkx_labels(G, pos, font_color='white', font_weight='bold')
            
            # Add value annotations
            for node, (x, y) in pos.items():
                value = core_nodes[node]['value']
                ax.text(x, y-0.15, f'{value:.3f}', ha='center', va='center',
                       fontsize=8, color='white', fontweight='bold')
            
            ax.axis('off')
            
            output_file = self.output_dir / f'cognitive_network_{timestamp}.png'
            plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight',
                       facecolor=self.dawn_colors['background'])
            plt.close()
            
            logger.info(f"✅ Cognitive network created: {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"❌ Failed to create cognitive network: {e}")
            return None
    
    def create_mood_analysis(self, tick_data: Dict[str, Any], timestamp: str) -> Optional[str]:
        """Create mood and zone analysis"""
        if not MATPLOTLIB_AVAILABLE:
            return None
            
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=self.figsize_wide, dpi=self.dpi)
            fig.suptitle('🎭 Mood & Zone Analysis', fontsize=16,
                        color=self.dawn_colors['primary'], fontweight='bold')
            
            # Current mood state
            mood = tick_data.get('mood', 'NEUTRAL')
            zone = tick_data.get('zone', 'STABLE')
            
            # Mood history simulation
            ax1.set_title('Mood Evolution', color=self.dawn_colors['accent'])
            
            # Generate mood transition data
            mood_states = ['CONTEMPLATIVE', 'ACTIVE', 'FOCUSED', 'REFLECTIVE', 'EXCITED']
            mood_timeline = np.random.choice(mood_states, size=50)
            mood_counts = {state: list(mood_timeline).count(state) for state in mood_states}
            
            colors = ['#44ff88', '#ff8844', '#4488ff', '#ff44ff', '#ffff44']
            bars = ax1.bar(mood_counts.keys(), mood_counts.values(), color=colors, alpha=0.8)
            ax1.set_ylabel('Frequency')
            ax1.tick_params(axis='x', rotation=45)
            
            # Highlight current mood
            if mood in mood_counts:
                mood_idx = list(mood_counts.keys()).index(mood)
                bars[mood_idx].set_edgecolor('#ffffff')
                bars[mood_idx].set_linewidth(3)
            
            # Zone distribution
            ax2.set_title('Zone Distribution', color=self.dawn_colors['accent'])
            zone_data = {
                'CRITICAL': 15,
                'ACTIVE': 35, 
                'STABLE': 40,
                'DORMANT': 10
            }
            zone_colors = ['#ff0000', '#ff8800', '#44ff44', '#4444ff']
            
            wedges, texts, autotexts = ax2.pie(zone_data.values(), labels=zone_data.keys(), 
                                             colors=zone_colors, autopct='%1.1f%%')
            
            # Highlight current zone
            if zone in zone_data:
                zone_idx = list(zone_data.keys()).index(zone)
                wedges[zone_idx].set_edgecolor('#ffffff')
                wedges[zone_idx].set_linewidth(3)
            
            # Mood-Zone correlation matrix
            ax3.set_title('Mood-Zone Correlation', color=self.dawn_colors['accent'])
            
            # Generate correlation data
            correlation_data = np.random.rand(len(mood_states), len(zone_data))
            correlation_data = (correlation_data + correlation_data.T) / 2  # Make symmetric-ish
            
            im = ax3.imshow(correlation_data, cmap='RdYlBu_r', aspect='auto')
            ax3.set_xticks(range(len(zone_data)))
            ax3.set_xticklabels(zone_data.keys(), rotation=45)
            ax3.set_yticks(range(len(mood_states)))
            ax3.set_yticklabels(mood_states)
            
            # Add correlation values
            for i in range(len(mood_states)):
                for j in range(len(zone_data)):
                    ax3.text(j, i, f'{correlation_data[i, j]:.2f}',
                           ha='center', va='center', color='white', fontweight='bold')
            
            # Current state indicator
            ax4.set_title('Current State', color=self.dawn_colors['accent'])
            ax4.text(0.5, 0.7, f'MOOD: {mood}', ha='center', va='center',
                    fontsize=14, fontweight='bold', color=self.dawn_colors['primary'])
            ax4.text(0.5, 0.3, f'ZONE: {zone}', ha='center', va='center',
                    fontsize=14, fontweight='bold', color=self.dawn_colors['secondary'])
            
            # Add stability indicator
            stability = 1.0 - tick_data.get('entropy', 0.5)
            ax4.text(0.5, 0.1, f'Stability: {stability:.1%}', ha='center', va='center',
                    fontsize=12, color=self.dawn_colors['text'])
            
            ax4.set_xlim(0, 1)
            ax4.set_ylim(0, 1)
            ax4.axis('off')
            
            plt.tight_layout()
            
            output_file = self.output_dir / f'mood_analysis_{timestamp}.png'
            plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight',
                       facecolor=self.dawn_colors['background'])
            plt.close()
            
            logger.info(f"✅ Mood analysis created: {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"❌ Failed to create mood analysis: {e}")
            return None
    
    def create_overview_panel(self, tick_data: Dict[str, Any], timestamp: str) -> Optional[str]:
        """Create comprehensive overview panel"""
        if not MATPLOTLIB_AVAILABLE:
            return None
            
        try:
            fig = plt.figure(figsize=(20, 12), dpi=self.dpi)
            fig.suptitle(f'🌅 DAWN Consciousness Overview - Tick {tick_data.get("tick", 0)}',
                        fontsize=20, color=self.dawn_colors['primary'], fontweight='bold')
            
            # Create complex grid layout
            gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
            
            # Key metrics (top row)
            ax1 = fig.add_subplot(gs[0, 0])
            ax2 = fig.add_subplot(gs[0, 1])
            ax3 = fig.add_subplot(gs[0, 2])
            ax4 = fig.add_subplot(gs[0, 3])
            
            # Large visualization (middle)
            ax_main = fig.add_subplot(gs[1, :])
            
            # Bottom details
            ax5 = fig.add_subplot(gs[2, 0])
            ax6 = fig.add_subplot(gs[2, 1])
            ax7 = fig.add_subplot(gs[2, 2])
            ax8 = fig.add_subplot(gs[2, 3])
            
            # Top row - Key metrics as gauges
            metrics = [
                ('Entropy', tick_data.get('entropy', 0.5), '#ff4444'),
                ('SCUP', tick_data.get('scup', 0.5), '#44ff44'),
                ('Heat', tick_data.get('heat', 0.5), '#ff8844'),
                ('Drift', tick_data.get('drift', 0.3), '#4488ff')
            ]
            
            for ax, (name, value, color) in zip([ax1, ax2, ax3, ax4], metrics):
                # Create gauge visualization
                theta = np.linspace(0, np.pi, 100)
                r = np.ones_like(theta)
                
                ax.plot(theta, r, 'k-', linewidth=3)
                
                # Value indicator
                value_theta = value * np.pi
                ax.plot([value_theta, value_theta], [0, 1], color=color, linewidth=4)
                ax.fill_between([0, value_theta], [0, 0], [1, 1], alpha=0.3, color=color)
                
                # Labels
                ax.text(np.pi/2, 0.5, f'{value:.3f}', ha='center', va='center',
                       fontsize=14, fontweight='bold', color=color)
                ax.text(np.pi/2, -0.2, name, ha='center', va='center',
                       fontsize=12, fontweight='bold')
                
                ax.set_xlim(0, np.pi)
                ax.set_ylim(-0.3, 1.2)
                ax.axis('off')
            
            # Main visualization - Consciousness state over time
            ax_main.set_title('🧠 Consciousness State Evolution', fontsize=16, 
                            color=self.dawn_colors['accent'], pad=20)
            
            # Generate synthetic time series
            current_tick = tick_data.get('tick', 0)
            time_range = list(range(max(0, current_tick - 200), current_tick + 1))
            
            # Multiple consciousness metrics over time
            entropy_series = [tick_data.get('entropy', 0.5) + np.sin(i * 0.1) * 0.1 + np.random.normal(0, 0.02) for i in range(len(time_range))]
            scup_series = [tick_data.get('scup', 0.5) + np.cos(i * 0.08) * 0.15 + np.random.normal(0, 0.03) for i in range(len(time_range))]
            heat_series = [tick_data.get('heat', 0.5) + np.sin(i * 0.12) * 0.2 + np.random.normal(0, 0.025) for i in range(len(time_range))]
            
            # Clamp values
            entropy_series = np.clip(entropy_series, 0, 1)
            scup_series = np.clip(scup_series, 0, 1)
            heat_series = np.clip(heat_series, 0, 1)
            
            ax_main.plot(time_range, entropy_series, color='#ff4444', linewidth=2, label='Entropy', alpha=0.8)
            ax_main.plot(time_range, scup_series, color='#44ff44', linewidth=2, label='SCUP', alpha=0.8)
            ax_main.plot(time_range, heat_series, color='#ff8844', linewidth=2, label='Heat', alpha=0.8)
            
            # Fill areas
            ax_main.fill_between(time_range, entropy_series, alpha=0.2, color='#ff4444')
            ax_main.fill_between(time_range, scup_series, alpha=0.2, color='#44ff44')
            ax_main.fill_between(time_range, heat_series, alpha=0.2, color='#ff8844')
            
            # Current point indicators
            ax_main.scatter([current_tick], [tick_data.get('entropy', 0.5)], color='#ff4444', s=100, zorder=10)
            ax_main.scatter([current_tick], [tick_data.get('scup', 0.5)], color='#44ff44', s=100, zorder=10)
            ax_main.scatter([current_tick], [tick_data.get('heat', 0.5)], color='#ff8844', s=100, zorder=10)
            
            ax_main.set_xlabel('Tick Number')
            ax_main.set_ylabel('Value')
            ax_main.legend()
            ax_main.grid(True, alpha=0.3)
            
            # Bottom row - Additional details
            
            # System info
            ax5.set_title('System Info', color=self.dawn_colors['accent'])
            info_text = f"""Tick: {tick_data.get('tick', 0)}
Zone: {tick_data.get('zone', 'STABLE')}
Mood: {tick_data.get('mood', 'NEUTRAL')}
Reblooms: {tick_data.get('reblooms', 0)}
Sigils: {tick_data.get('sigils', 0)}"""
            ax5.text(0.1, 0.5, info_text, transform=ax5.transAxes, fontsize=10,
                    verticalalignment='center', color=self.dawn_colors['text'])
            ax5.axis('off')
            
            # Performance metrics
            ax6.set_title('Performance', color=self.dawn_colors['accent'])
            perf_metrics = ['Tick Time', 'CPU', 'Memory']
            perf_values = [
                tick_data.get('tick_time', 0.01) * 1000,  # Convert to ms
                tick_data.get('cpu_usage', 0.2) * 100,    # Convert to %
                tick_data.get('memory_usage', 0.3) * 100  # Convert to %
            ]
            perf_colors = ['#44ff88', '#ff8844', '#4488ff']
            
            bars = ax6.bar(perf_metrics, perf_values, color=perf_colors, alpha=0.8)
            ax6.set_ylabel('Value')
            
            for bar, value, metric in zip(bars, perf_values, perf_metrics):
                unit = 'ms' if metric == 'Tick Time' else '%'
                ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(perf_values) * 0.02,
                        f'{value:.1f}{unit}', ha='center', va='bottom', fontsize=8)
            
            # Activity indicators
            ax7.set_title('Activity Level', color=self.dawn_colors['accent'])
            activity_level = (tick_data.get('entropy', 0.5) + tick_data.get('scup', 0.5) + 
                            tick_data.get('reblooms', 0) / 10) / 3
            
            # Activity gauge
            theta = np.linspace(0, 2*np.pi, 100)
            r = np.ones_like(theta) * 0.8
            ax7.plot(theta, r, 'k-', linewidth=2)
            
            # Activity level indicator
            activity_theta = activity_level * 2 * np.pi
            ax7.plot([0, activity_theta], [0, 0.8], color=self.dawn_colors['primary'], linewidth=4)
            ax7.fill_between([0, activity_theta], [0, 0], [0.8, 0.8], alpha=0.3, color=self.dawn_colors['primary'])
            
            ax7.text(0, 0, f'{activity_level:.1%}', ha='center', va='center',
                    fontsize=12, fontweight='bold', color=self.dawn_colors['primary'])
            ax7.set_xlim(-1, 1)
            ax7.set_ylim(-1, 1)
            ax7.axis('off')
            
            # Timestamp and metadata
            ax8.set_title('Snapshot Info', color=self.dawn_colors['accent'])
            metadata_text = f"""Generated: {datetime.now().strftime('%H:%M:%S')}
Date: {datetime.now().strftime('%Y-%m-%d')}
Engine: Enhanced Visual v2.0
Quality: {self.dpi} DPI
Status: ACTIVE"""
            ax8.text(0.1, 0.5, metadata_text, transform=ax8.transAxes, fontsize=10,
                    verticalalignment='center', color=self.dawn_colors['text'])
            ax8.axis('off')
            
            output_file = self.output_dir / f'overview_panel_{timestamp}.png'
            plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight',
                       facecolor=self.dawn_colors['background'])
            plt.close()
            
            logger.info(f"✅ Overview panel created: {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"❌ Failed to create overview panel: {e}")
            return None
    
    def export_data_formats(self, tick_data: Dict[str, Any], timestamp: str) -> Dict[str, str]:
        """Export data in multiple formats"""
        exported_files = {}
        
        try:
            # Enhanced JSON export
            enhanced_data = {
                'metadata': {
                    'timestamp': timestamp,
                    'tick': tick_data.get('tick', 0),
                    'generated_by': 'Enhanced DAWN Visual Engine v2.0',
                    'snapshot_type': 'comprehensive'
                },
                'consciousness_state': tick_data,
                'computed_metrics': {
                    'stability_index': 1.0 - tick_data.get('entropy', 0.5),
                    'activity_level': (tick_data.get('entropy', 0.5) + tick_data.get('scup', 0.5)) / 2,
                    'cognitive_load': tick_data.get('scup', 0.5),
                    'system_efficiency': 1.0 - tick_data.get('tick_time', 0.01) * 100
                },
                'analysis': {
                    'mood': tick_data.get('mood', 'NEUTRAL'),
                    'zone': tick_data.get('zone', 'STABLE'),
                    'trend': 'stable',  # Could be computed from history
                    'alerts': []
                }
            }
            
            json_file = self.output_dir / f'snapshot_data_{timestamp}.json'
            with open(json_file, 'w') as f:
                json.dump(enhanced_data, f, indent=2)
            exported_files['json_data'] = str(json_file)
            
            # CSV export for analysis
            csv_file = self.output_dir / f'metrics_{timestamp}.csv'
            with open(csv_file, 'w') as f:
                f.write('metric,value,unit,category\n')
                metrics_data = [
                    ('tick', tick_data.get('tick', 0), 'count', 'system'),
                    ('entropy', tick_data.get('entropy', 0.5), 'ratio', 'consciousness'),
                    ('scup', tick_data.get('scup', 0.5), 'ratio', 'consciousness'),
                    ('heat', tick_data.get('heat', 0.5), 'ratio', 'consciousness'),
                    ('drift', tick_data.get('drift', 0.3), 'ratio', 'consciousness'),
                    ('reblooms', tick_data.get('reblooms', 0), 'count', 'activity'),
                    ('sigils', tick_data.get('sigils', 0), 'count', 'activity'),
                    ('tick_time', tick_data.get('tick_time', 0.01), 'seconds', 'performance'),
                    ('cpu_usage', tick_data.get('cpu_usage', 0.2), 'ratio', 'performance'),
                    ('memory_usage', tick_data.get('memory_usage', 0.3), 'ratio', 'performance')
                ]
                
                for metric, value, unit, category in metrics_data:
                    f.write(f'{metric},{value},{unit},{category}\n')
            
            exported_files['csv_data'] = str(csv_file)
            
            logger.info(f"✅ Data exported to {len(exported_files)} formats")
            
        except Exception as e:
            logger.error(f"❌ Failed to export data: {e}")
        
        return exported_files
    
    def create_snapshot_manifest(self, tick_data: Dict[str, Any], generated_files: Dict[str, str], timestamp: str) -> str:
        """Create manifest file for the snapshot"""
        manifest = {
            'snapshot_info': {
                'timestamp': timestamp,
                'tick': tick_data.get('tick', 0),
                'engine_version': 'Enhanced DAWN Visual Engine v2.0',
                'generation_time': datetime.now().isoformat()
            },
            'consciousness_state': {
                'entropy': tick_data.get('entropy', 0.5),
                'scup': tick_data.get('scup', 0.5),
                'heat': tick_data.get('heat', 0.5),
                'zone': tick_data.get('zone', 'STABLE'),
                'mood': tick_data.get('mood', 'NEUTRAL'),
                'reblooms': tick_data.get('reblooms', 0),
                'sigils': tick_data.get('sigils', 0)
            },
            'generated_files': generated_files,
            'file_count': len(generated_files),
            'visualization_types': list(generated_files.keys())
        }
        
        manifest_file = self.output_dir / f'snapshot_manifest_{timestamp}.json'
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"✅ Snapshot manifest created: {manifest_file}")
        return str(manifest_file)
    
    def create_fallback_visualization(self, tick_data: Dict[str, Any], timestamp: str) -> Optional[str]:
        """Create minimal fallback visualization if main generation fails"""
        try:
            if not MATPLOTLIB_AVAILABLE:
                return None
                
            fig, ax = plt.subplots(figsize=(10, 6), dpi=self.dpi)
            fig.suptitle(f'🧠 DAWN Consciousness Snapshot - Tick {tick_data.get("tick", 0)}',
                        fontsize=14, color=self.dawn_colors['primary'])
            
            # Simple bar chart of key metrics
            metrics = ['Entropy', 'SCUP', 'Heat', 'Reblooms']
            values = [
                tick_data.get('entropy', 0.5),
                tick_data.get('scup', 0.5), 
                tick_data.get('heat', 0.5),
                tick_data.get('reblooms', 0) / 10  # Normalize
            ]
            colors = ['#ff4444', '#44ff44', '#ff8844', '#44ffff']
            
            bars = ax.bar(metrics, values, color=colors, alpha=0.8)
            ax.set_ylabel('Value')
            ax.set_title('Consciousness Metrics')
            
            # Add value labels
            for bar, value in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                       f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            
            output_file = self.output_dir / f'fallback_snapshot_{timestamp}.png'
            plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight',
                       facecolor=self.dawn_colors['background'])
            plt.close()
            
            logger.info(f"✅ Fallback visualization created: {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"❌ Failed to create fallback visualization: {e}")
            return None

def main():
    """Main CLI interface for enhanced visual engine"""
    parser = argparse.ArgumentParser(description='Enhanced DAWN Visual Engine')
    parser.add_argument('--snapshot-now', action='store_true', help='Generate immediate snapshot')
    parser.add_argument('--simulate-data', action='store_true', help='Use simulated tick data')
    parser.add_argument('--output-dir', default='runtime/enhanced_snapshots', help='Output directory')
    parser.add_argument('--tick-data-file', help='Path to tick data JSON file')
    
    args = parser.parse_args()
    
    # Initialize engine
    engine = EnhancedVisualEngine(args.output_dir)
    
    if args.snapshot_now:
        # Get tick data
        if args.tick_data_file and os.path.exists(args.tick_data_file):
            with open(args.tick_data_file, 'r') as f:
                tick_data = json.load(f)
        elif args.simulate_data:
            # Generate realistic simulated data
            tick_data = {
                'tick': 1275,
                'entropy': 0.384,
                'scup': 0.090,
                'heat': 0.312,
                'drift': 0.156,
                'zone': 'CRITICAL',
                'mood': 'CONTEMPLATIVE',
                'reblooms': 2,
                'sigils': 1,
                'tick_time': 0.011,
                'cpu_usage': 0.377,
                'memory_usage': 0.654,
                'timestamp': datetime.now().isoformat()
            }
        else:
            # Try to read from environment
            tick_data = {}
            for key in ['tick', 'entropy', 'scup', 'heat', 'drift', 'zone', 'mood', 'reblooms', 'sigils']:
                env_key = f'DAWN_{key.upper()}'
                if env_key in os.environ:
                    try:
                        value = float(os.environ[env_key]) if key not in ['zone', 'mood'] else os.environ[env_key]
                        tick_data[key] = value
                    except ValueError:
                        tick_data[key] = os.environ[env_key]
        
        # Generate enhanced snapshot
        print("[Enhanced Visuals] Generating enhanced visual snapshot...")
        generated_files = engine.generate_comprehensive_snapshot(tick_data)
        
        if generated_files:
            print(f"✅ Enhanced snapshot complete!")
            print(f"📁 Output directory: {engine.output_dir}")
            print(f"📊 Generated {len(generated_files)} files:")
            for file_type, file_path in generated_files.items():
                file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
                print(f"   - {file_type}: {os.path.basename(file_path)} ({file_size:,} bytes)")
        else:
            print("❌ Enhanced snapshot failed")
            sys.exit(1)
    
    else:
        print("Enhanced DAWN Visual Engine v2.0")
        print("Use --snapshot-now to generate a comprehensive snapshot")
        print("Use --simulate-data for demo with simulated data")

if __name__ == "__main__":
    main() 