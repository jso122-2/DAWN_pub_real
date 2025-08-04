# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
DAWN GUI Visualization Bridge
Adapts existing DAWN visualization scripts for real-time GUI integration
"""

import os
import sys
import json
import time
import base64
import asyncio
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable
import logging
from io import BytesIO
import queue

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend for GUI
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    logger.warning("matplotlib not available - visualizations disabled")

class VisualizationBridge:
    """
    Bridge between DAWN visualization scripts and GUI interface
    Converts matplotlib figures to base64 images for web display
    """
    
    def __init__(self, output_dir: str = "runtime/gui_visualizations"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.active_visualizations = {}
        self.update_queue = queue.Queue()
        self.running = False
        self.update_thread = None
        
        logger.info("VisualizationBridge initialized")
    
    def figure_to_base64(self, fig) -> str:
        """Convert matplotlib figure to base64 string for web display"""
        if not MATPLOTLIB_AVAILABLE:
            return ""
        
        try:
            buffer = BytesIO()
            fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight', 
                       facecolor='#0a0a0a', edgecolor='none')
            buffer.seek(0)
            image_data = buffer.getvalue()
            buffer.close()
            
            # Convert to base64
            base64_data = base64.b64encode(image_data).decode('utf-8')
            return f"data:image/png;base64,{base64_data}"
        except Exception as e:
            logger.error(f"Error converting figure to base64: {e}")
            return ""
    
    def save_figure_for_gui(self, fig, name: str) -> str:
        """Save figure as PNG file for GUI access"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = self.output_dir / filename
            
            fig.savefig(filepath, dpi=100, bbox_inches='tight',
                       facecolor='#0a0a0a', edgecolor='none')
            
            logger.info(f"Saved GUI visualization: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error saving figure: {e}")
            return ""

class EmotionalLandscapeBridge:
    """
    Bridge for the emotional landscape visualization (dawn_mood_state.py)
    """
    
    def __init__(self, bridge: VisualizationBridge):
        self.bridge = bridge
        self.last_update = time.time()
        self.mood_matrix = np.zeros((8, 8))
        
        # Emotional dimensions
        self.mood_dimensions = [
            ['Transcendent', 'Luminous', 'Expansive', 'Crystalline', 'Ethereal', 'Radiant', 'Sublime', 'Infinite'],
            ['Ecstatic', 'Euphoric', 'Jubilant', 'Vivacious', 'Exuberant', 'Buoyant', 'Elated', 'Rapturous'],
            ['Serene', 'Peaceful', 'Harmonious', 'Balanced', 'Centered', 'Tranquil', 'Calm', 'Composed'],
            ['Curious', 'Inquisitive', 'Wonder', 'Fascinated', 'Intrigued', 'Exploratory', 'Seeking', 'Questioning'],
            ['Focused', 'Attentive', 'Concentrated', 'Sharp', 'Alert', 'Vigilant', 'Acute', 'Precise'],
            ['Contemplative', 'Reflective', 'Meditative', 'Pensive', 'Introspective', 'Thoughtful', 'Deep', 'Brooding'],
            ['Uncertain', 'Hesitant', 'Ambiguous', 'Doubtful', 'Questioning', 'Unsure', 'Wavering', 'Conflicted'],
            ['Turbulent', 'Chaotic', 'Fragmented', 'Unstable', 'Volatile', 'Scattered', 'Dissonant', 'Entropic']
        ]
    
    def update_from_tick_data(self, tick_data: Dict[str, Any]) -> str:
        """Update emotional landscape from DAWN tick data"""
        if not MATPLOTLIB_AVAILABLE:
            return ""
        
        try:
            # Extract mood data
            mood_raw = tick_data.get('mood', 'NEUTRAL')
            entropy = tick_data.get('entropy', 0.5)
            scup = tick_data.get('scup', 0.5)
            tick = tick_data.get('tick', 0)
            
            # Generate mood matrix
            mood_matrix = np.random.random((8, 8)) * 0.1  # Base noise
            
            # Map consciousness state to emotional dimensions
            if mood_raw == 'CONTEMPLATIVE':
                mood_matrix[5:7, :] += 0.6  # Contemplative/Reflective region
            elif mood_raw == 'ACTIVE':
                mood_matrix[1:3, :] += 0.7  # Ecstatic/Euphoric region
            elif mood_raw == 'CRITICAL':
                mood_matrix[7:8, :] += 0.8  # Turbulent region
            else:  # NEUTRAL
                mood_matrix[2:4, :] += 0.5  # Serene/Curious region
            
            # Apply entropy influence
            mood_matrix += entropy * 0.3
            
            # Apply SCUP influence
            mood_matrix[4:6, :] += scup * 0.4  # Focused region
            
            # Add temporal wave
            wave = np.sin(tick * 0.1) * 0.1
            mood_matrix += wave
            
            # Clamp values
            mood_matrix = np.clip(mood_matrix, 0, 1)
            
            # Create visualization
            fig, ax = plt.subplots(figsize=(10, 8))
            fig.patch.set_facecolor('#0a0a0a')
            
            # Create heatmap
            from matplotlib.colors import LinearSegmentedColormap
            colors = ['#0a0a0a', '#1a1a2e', '#16213e', '#0f3460', '#533483', 
                     '#7209b7', '#a663cc', '#4cc9f0', '#7209b7', '#f72585']
            mood_cmap = LinearSegmentedColormap.from_list('mood', colors, N=256)
            
            im = ax.imshow(mood_matrix, cmap=mood_cmap, aspect='equal', vmin=0, vmax=1)
            
            # Add labels
            ax.set_xticks(range(8))
            ax.set_yticks(range(8))
            ax.set_xticklabels([row[0][:8] for row in self.mood_dimensions], 
                              rotation=45, ha='right', fontsize=8, color='#cccccc')
            ax.set_yticklabels([f"{i+1}" for i in range(8)], 
                              fontsize=8, color='#cccccc')
            
            # Add text annotations
            for i in range(8):
                for j in range(8):
                    intensity = mood_matrix[i, j]
                    alpha = 0.4 + 0.6 * intensity
                    ax.text(j, i, self.mood_dimensions[i][j][:6], 
                           ha='center', va='center', fontsize=6, 
                           color='white', weight='bold', alpha=alpha)
            
            ax.set_title(f'DAWN Emotional Landscape - Tick {tick}\n{mood_raw} State', 
                        fontsize=14, color='#ffffff', pad=20, weight='bold')
            
            # Add colorbar
            cbar = plt.colorbar(im, ax=ax, shrink=0.8)
            cbar.set_label('Affective Intensity', rotation=270, labelpad=15, 
                          color='#cccccc', fontsize=10)
            cbar.ax.tick_params(colors='#cccccc')
            
            plt.tight_layout()
            
            # Convert to base64 for GUI
            base64_image = self.bridge.figure_to_base64(fig)
            plt.close(fig)
            
            self.last_update = time.time()
            return base64_image
            
        except Exception as e:
            logger.error(f"Error updating emotional landscape: {e}")
            return ""

class CognitivePulseBridge:
    """
    Bridge for the cognitive pulse visualization (tick_pulse_visualizer.py)
    """
    
    def __init__(self, bridge: VisualizationBridge, buffer_size: int = 100):
        self.bridge = bridge
        self.buffer_size = buffer_size
        self.tick_history = []
        self.pulse_history = []
        self.time_history = []
        
    def update_from_tick_data(self, tick_data: Dict[str, Any]) -> str:
        """Update cognitive pulse from DAWN tick data"""
        if not MATPLOTLIB_AVAILABLE:
            return ""
        
        try:
            tick = tick_data.get('tick', 0)
            entropy = tick_data.get('entropy', 0.5)
            scup = tick_data.get('scup', 0.5)
            heat = tick_data.get('heat', 0.5)
            current_time = time.time()
            
            # Calculate pulse intensity
            pulse_intensity = np.sin(tick * 0.2) + 0.5 * entropy + 0.3 * scup
            
            # Update history
            self.tick_history.append(tick)
            self.pulse_history.append(pulse_intensity)
            self.time_history.append(current_time)
            
            # Trim history
            if len(self.tick_history) > self.buffer_size:
                self.tick_history.pop(0)
                self.pulse_history.pop(0)
                self.time_history.pop(0)
            
            # Create visualization
            fig, (ax_main, ax_rhythm) = plt.subplots(2, 1, figsize=(12, 8))
            fig.patch.set_facecolor('#0a0a0a')
            
            # Main pulse display
            ax_main.set_facecolor('#0a0a0a')
            if len(self.pulse_history) > 1:
                x_range = range(len(self.pulse_history))
                ax_main.plot(x_range, self.pulse_history, 'g-', linewidth=3, alpha=0.9)
                ax_main.fill_between(x_range, self.pulse_history, alpha=0.3, color='green')
                
                # Current pulse indicator
                current_pulse = self.pulse_history[-1]
                ax_main.scatter([len(self.pulse_history)-1], [current_pulse], 
                               s=200, c='#00ff88', alpha=0.8, zorder=10)
            
            ax_main.set_title(f'DAWN Cognitive Heartbeat - Tick {tick}', 
                             fontsize=14, color='white', weight='bold')
            ax_main.set_xlabel('Time Steps', color='#cccccc')
            ax_main.set_ylabel('Pulse Amplitude', color='#cccccc')
            ax_main.grid(True, alpha=0.3)
            ax_main.tick_params(colors='#cccccc')
            
            # Rhythm analysis
            ax_rhythm.set_facecolor('#0a0a0a')
            if len(self.pulse_history) > 10:
                # Calculate rhythm frequency
                pulse_array = np.array(self.pulse_history)
                fft = np.fft.fft(pulse_array)
                freqs = np.fft.fftfreq(len(pulse_array))
                
                ax_rhythm.plot(freqs[:len(freqs)//2], np.abs(fft[:len(fft)//2]), 
                              'c-', linewidth=2, alpha=0.8)
                ax_rhythm.fill_between(freqs[:len(freqs)//2], np.abs(fft[:len(fft)//2]), 
                                      alpha=0.3, color='cyan')
            
            ax_rhythm.set_title('Cognitive Rhythm Spectrum', fontsize=12, color='#cccccc')
            ax_rhythm.set_xlabel('Frequency', color='#cccccc')
            ax_rhythm.set_ylabel('Amplitude', color='#cccccc')
            ax_rhythm.grid(True, alpha=0.3)
            ax_rhythm.tick_params(colors='#cccccc')
            
            plt.tight_layout()
            
            # Convert to base64 for GUI
            base64_image = self.bridge.figure_to_base64(fig)
            plt.close(fig)
            
            return base64_image
            
        except Exception as e:
            logger.error(f"Error updating cognitive pulse: {e}")
            return ""

class NetworkFlowBridge:
    """
    Bridge for network flow visualization (simplified version)
    """
    
    def __init__(self, bridge: VisualizationBridge):
        self.bridge = bridge
        self.nodes = {}
        self.connections = []
        
    def update_from_tick_data(self, tick_data: Dict[str, Any]) -> str:
        """Update network visualization from DAWN tick data"""
        if not MATPLOTLIB_AVAILABLE:
            return ""
        
        try:
            import networkx as nx
            
            tick = tick_data.get('tick', 0)
            entropy = tick_data.get('entropy', 0.5)
            scup = tick_data.get('scup', 0.5)
            mood = tick_data.get('mood', 'NEUTRAL')
            
            # Create simple network graph
            G = nx.Graph()
            
            # Add consciousness nodes
            nodes = {
                'Entropy': entropy,
                'SCUP': scup,
                'Mood': hash(mood) % 100 / 100.0,
                'Tick': (tick % 100) / 100.0,
                'Heat': tick_data.get('heat', 0.5)
            }
            
            for node, value in nodes.items():
                G.add_node(node, value=value)
            
            # Add edges based on relationships
            edges = [
                ('Entropy', 'SCUP', entropy * scup),
                ('Entropy', 'Heat', entropy * 0.8),
                ('SCUP', 'Mood', scup * 0.6),
                ('Mood', 'Tick', 0.4),
                ('Heat', 'Tick', 0.5)
            ]
            
            for source, target, weight in edges:
                G.add_edge(source, target, weight=weight)
            
            # Create visualization
            fig, ax = plt.subplots(figsize=(10, 8))
            fig.patch.set_facecolor('#0a0a0a')
            ax.set_facecolor('#0a0a0a')
            
            # Position nodes
            pos = nx.spring_layout(G, k=2, iterations=50)
            
            # Draw edges
            edge_colors = [G[u][v]['weight'] for u, v in G.edges()]
            nx.draw_networkx_edges(G, pos, edge_color=edge_colors, 
                                  edge_cmap=plt.cm.viridis, alpha=0.6, width=3)
            
            # Draw nodes
            node_colors = [nodes[node] for node in G.nodes()]
            node_sizes = [nodes[node] * 1000 + 200 for node in G.nodes()]
            
            nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                                  node_size=node_sizes, cmap=plt.cm.plasma, alpha=0.8)
            
            # Draw labels
            nx.draw_networkx_labels(G, pos, font_color='white', font_weight='bold')
            
            ax.set_title(f'DAWN Consciousness Network - Tick {tick}', 
                        fontsize=14, color='white', weight='bold')
            ax.axis('off')
            
            plt.tight_layout()
            
            # Convert to base64 for GUI
            base64_image = self.bridge.figure_to_base64(fig)
            plt.close(fig)
            
            return base64_image
            
        except ImportError:
            logger.warning("networkx not available for network visualization")
            return ""
        except Exception as e:
            logger.error(f"Error updating network flow: {e}")
            return ""

class GUIVisualizationManager:
    """
    Main manager for all GUI visualizations
    """
    
    def __init__(self):
        self.bridge = VisualizationBridge()
        
        # Initialize visualization bridges
        self.emotional_landscape = EmotionalLandscapeBridge(self.bridge)
        self.cognitive_pulse = CognitivePulseBridge(self.bridge)
        self.network_flow = NetworkFlowBridge(self.bridge)
        
        logger.info("GUIVisualizationManager initialized with 3 visualizations")
    
    def update_all_visualizations(self, tick_data: Dict[str, Any]) -> Dict[str, str]:
        """Update all visualizations and return base64 images"""
        results = {}
        
        try:
            # Update emotional landscape
            emotional_image = self.emotional_landscape.update_from_tick_data(tick_data)
            if emotional_image:
                results['emotional_landscape'] = emotional_image
            
            # Update cognitive pulse
            pulse_image = self.cognitive_pulse.update_from_tick_data(tick_data)
            if pulse_image:
                results['cognitive_pulse'] = pulse_image
            
            # Update network flow
            network_image = self.network_flow.update_from_tick_data(tick_data)
            if network_image:
                results['network_flow'] = network_image
            
            logger.info(f"Updated {len(results)} visualizations for tick {tick_data.get('tick', 0)}")
            
        except Exception as e:
            logger.error(f"Error updating visualizations: {e}")
        
        return results

def main():
    """CLI interface for testing the visualization bridge"""
    import argparse
    
    parser = argparse.ArgumentParser(description='DAWN GUI Visualization Bridge')
    parser.add_argument('--test', action='store_true', help='Run test with simulated data')
    parser.add_argument('--tick-data', help='JSON file with tick data')
    
    args = parser.parse_args()
    
    # Initialize manager
    manager = GUIVisualizationManager()
    
    if args.test:
        # Test with simulated data
        print("Testing GUI visualizations with simulated data...")
        
        test_data = {
            'tick': 42,
            'entropy': 0.7,
            'scup': 0.3,
            'heat': 0.5,
            'mood': 'CONTEMPLATIVE',
            'zone': 'CRITICAL',
            'reblooms': 2,
            'sigils': 1
        }
        
        results = manager.update_all_visualizations(test_data)
        
        print(f"Generated {len(results)} visualizations:")
        for name, image_data in results.items():
            data_size = len(image_data) if image_data else 0
            print(f"  - {name}: {data_size:,} bytes")
    
    elif args.tick_data:
        # Load data from file
        try:
            with open(args.tick_data, 'r') as f:
                tick_data = json.load(f)
            
            results = manager.update_all_visualizations(tick_data)
            print(f"Generated {len(results)} visualizations from {args.tick_data}")
            
        except Exception as e:
            print(f"Error loading tick data: {e}")
    
    else:
        print("Use --test for testing or --tick-data <file> to process real data")

if __name__ == "__main__":
    main() 