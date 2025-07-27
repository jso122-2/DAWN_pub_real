#!/usr/bin/env python3
"""
DAWN Visualization #8: Sigil Command Stream
A real-time timeline visualization showing DAWN's internal symbolic commands 
and triggers (sigils) that orchestrate cognitive processes.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
from matplotlib.collections import LineCollection
import json
import os
import os
import os
import os
import sys
import argparse
import time
from datetime import datetime
from collections import deque, defaultdict
import threading
import queue
import random

# Sigil command categories and their properties
SIGIL_CATEGORIES = {
    'attention': {
        'lane': 0,
        'color': '#ff6b6b',
        'symbols': ['◉', '◎', '○', '●', '◐'],
        'description': 'Focus and attention control'
    },
    'memory': {
        'lane': 1, 
        'color': '#4ecdc4',
        'symbols': ['◆', '◇', '◈', '⬧', '⬨'],
        'description': 'Memory retrieval and storage'
    },
    'reasoning': {
        'lane': 2,
        'color': '#45b7d1', 
        'symbols': ['▲', '△', '▴', '▵', '⟁'],
        'description': 'Logical processing and inference'
    },
    'creativity': {
        'lane': 3,
        'color': '#96ceb4',
        'symbols': ['✦', '✧', '✪', '✫', '✬'],
        'description': 'Creative synthesis and generation'
    },
    'integration': {
        'lane': 4,
        'color': '#feca57',
        'symbols': ['⬢', '⬡', '⬠', '⬟', '⬞'],
        'description': 'Information integration and coherence'
    },
    'action': {
        'lane': 5,
        'color': '#ff9ff3',
        'symbols': ['➤', '➣', '➢', '➡', '⟶'],
        'description': 'Decision execution and output'
    },
    'meta': {
        'lane': 6,
        'color': '#54a0ff',
        'symbols': ['◊', '⟐', '⟡', '⟢', '⟣'],
        'description': 'Meta-cognitive monitoring'
    }
}

# Sigil interaction network
SIGIL_INTERACTIONS = {
    'attention': ['reasoning', 'memory'],
    'memory': ['integration', 'creativity'],
    'reasoning': ['action', 'meta'],
    'creativity': ['integration', 'action'],
    'integration': ['meta', 'action'],
    'meta': ['attention', 'reasoning'],
    'action': ['meta']
}

# Command sequences
COMMAND_SEQUENCES = {
    'attention_focus': ['attention', 'reasoning', 'integration'],
    'memory_recall': ['memory', 'integration', 'reasoning'],
    'creative_flow': ['creativity', 'memory', 'integration', 'action'],
    'problem_solving': ['attention', 'memory', 'reasoning', 'integration'],
    'meta_monitoring': ['meta', 'attention', 'integration'],
    'decision_making': ['reasoning', 'integration', 'action', 'meta']
}

class SigilCommandStream:
    """Sigil Command Stream Visualization"""
    
    def __init__(self, data_source='demo', flow_speed=0.5, timeline_width=100):
        # Timeline parameters
        self.timeline_width = timeline_width
        self.flow_speed = flow_speed
        self.lane_height = 0.8
        self.num_lanes = len(SIGIL_CATEGORIES)
        
        # Data source
        self.data_source = data_source
        self.data_queue = queue.Queue()
        
        # Thread control
        self.stop_event = threading.Event()
        
        # Active sigil tracking
        self.active_sigils = []
        self.sigil_history = deque(maxlen=1000)
        self.command_sequences = []
        self.sequence_connections = []
        
        # Animation state
        self.time_offset = 0
        self.frame_count = 0
        
        # Metrics tracking
        self.metrics = {
            'sigil_counts': defaultdict(int),
            'sequence_counts': defaultdict(int),
            'recent_rate': 0,
            'dominant_category': None
        }
        
        # Setup visualization
        self.setup_visualization()
        
    def setup_visualization(self):
        """Initialize matplotlib figure and components"""
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(16, 10), facecolor='#0a0a0a')
        
        # Layout
        gs = self.fig.add_gridspec(5, 4, height_ratios=[3, 0.5, 0.5, 0.5, 0.5],
                                   width_ratios=[3, 1, 1, 1],
                                   hspace=0.3, wspace=0.2)
        
        # Main timeline
        self.ax_timeline = self.fig.add_subplot(gs[0, :])
        
        # Metrics panels
        self.ax_metrics = []
        for i in range(4):
            for j in range(4):
                if i > 0 and j < 3:
                    ax = self.fig.add_subplot(gs[i, j])
                    self.ax_metrics.append(ax)
        
        # Configure timeline
        self.setup_timeline()
        
        # Initialize metrics displays
        self.setup_metrics_panels()
        
        # Title and metadata
        self.fig.suptitle('DAWN Sigil Command Stream', fontsize=18, 
                         fontweight='bold', color='white')
        
        self.metadata_text = self.fig.text(0.02, 0.02, '', fontsize=10,
                                          color='gray', alpha=0.8)
        
    def setup_timeline(self):
        """Configure the main timeline axis"""
        self.ax_timeline.set_xlim(0, self.timeline_width)
        self.ax_timeline.set_ylim(-0.5, self.num_lanes - 0.5)
        
        # Draw lane backgrounds
        for category, props in SIGIL_CATEGORIES.items():
            lane = props['lane']
            
            # Lane background
            rect = FancyBboxPatch((0, lane - self.lane_height/2), 
                                  self.timeline_width, self.lane_height,
                                  boxstyle="round,pad=0.02",
                                  facecolor=props['color'], 
                                  alpha=0.1,
                                  edgecolor=props['color'],
                                  linewidth=1)
            self.ax_timeline.add_patch(rect)
            
            # Lane label
            self.ax_timeline.text(-2, lane, category.capitalize(), 
                                 ha='right', va='center',
                                 fontsize=11, fontweight='bold',
                                 color=props['color'])
        
        # Configure axes
        self.ax_timeline.set_xlabel('Time →', fontsize=12, color='white')
        self.ax_timeline.set_xticks([])
        self.ax_timeline.set_yticks([])
        self.ax_timeline.spines['top'].set_visible(False)
        self.ax_timeline.spines['right'].set_visible(False)
        self.ax_timeline.spines['bottom'].set_visible(False)
        self.ax_timeline.spines['left'].set_visible(False)
        
        # Time markers
        for i in range(0, self.timeline_width + 1, 10):
            self.ax_timeline.axvline(i, color='gray', alpha=0.2, linestyle='--')
        
        # Initialize sigil text objects pool
        self.sigil_texts = []
        self.available_texts = []
        
        # Pre-create text objects for performance
        for _ in range(50):
            text = self.ax_timeline.text(0, 0, '', fontsize=20, 
                                       ha='center', va='center',
                                       alpha=0, fontweight='bold')
            self.sigil_texts.append(text)
            self.available_texts.append(text)
        
        # Connection lines collection
        self.connection_lines = LineCollection([], colors='white', 
                                              linewidths=2, alpha=0.3)
        self.ax_timeline.add_collection(self.connection_lines)
        
    def setup_metrics_panels(self):
        """Initialize metrics display panels"""
        # Panel configurations
        panel_configs = [
            ('Active Sequences', self.plot_active_sequences),
            ('Category Distribution', self.plot_category_distribution),
            ('Command Rate', self.plot_command_rate),
            ('Sequence Efficiency', self.plot_sequence_efficiency),
            ('Interaction Network', self.plot_interaction_network),
            ('Cognitive Rhythm', self.plot_cognitive_rhythm)
        ]
        
        for ax, (title, plot_fn) in zip(self.ax_metrics, panel_configs):
            ax.set_title(title, fontsize=10, color='white', pad=5)
            ax.set_facecolor('#0a0a0a')
            ax.tick_params(colors='white', labelsize=8)
            
            # Store plot function reference
            ax.plot_fn = plot_fn
            ax.plot_fn(ax)
    
    def parse_sigil_data(self, json_data):
        """Extract sigil triggers from DAWN JSON output"""
        active_sigils = []
        
        # Direct sigil data if available
        sigil_triggers = json_data.get('sigil_triggers', {})
        for category, triggers in sigil_triggers.items():
            if category in SIGIL_CATEGORIES:
                for trigger in triggers:
                    active_sigils.append({
                        'category': category,
                        'symbol': random.choice(SIGIL_CATEGORIES[category]['symbols']),
                        'intensity': trigger.get('intensity', 0.5),
                        'trigger': trigger.get('name', 'unknown')
                    })
        
        # Infer sigils from cognitive state
        mood = json_data.get('mood', {})
        entropy = json_data.get('entropy', 0.5)
        heat = json_data.get('heat', 0.3)
        scup = json_data.get('scup', {})
        
        # Attention sigils (based on heat/focus)
        if heat > 0.7:
            active_sigils.append({
                'category': 'attention',
                'symbol': '◉',
                'intensity': heat,
                'trigger': 'high_focus'
            })
        elif heat < 0.3 and random.random() < 0.3:
            active_sigils.append({
                'category': 'attention',
                'symbol': '○',
                'intensity': 0.3,
                'trigger': 'attention_drift'
            })
        
        # Memory sigils (based on coherence)
        coherence = scup.get('coherence', 0.5)
        if coherence > 0.6:
            active_sigils.append({
                'category': 'memory',
                'symbol': '◆',
                'intensity': coherence,
                'trigger': 'memory_access'
            })
        
        # Reasoning sigils (based on schema)
        schema = scup.get('schema', 0.5)
        if schema > 0.6 and random.random() < 0.4:
            active_sigils.append({
                'category': 'reasoning',
                'symbol': '▲',
                'intensity': schema,
                'trigger': 'logical_processing'
            })
        
        # Creativity sigils (based on entropy + mood)
        creative_signal = entropy * mood.get('base_level', 0.5)
        if creative_signal > 0.5 and random.random() < 0.3:
            active_sigils.append({
                'category': 'creativity',
                'symbol': '✦',
                'intensity': creative_signal,
                'trigger': 'creative_spark'
            })
        
        # Integration sigils (based on utility)
        utility = scup.get('utility', 0.5)
        if utility > 0.5 and len(active_sigils) > 1:
            active_sigils.append({
                'category': 'integration',
                'symbol': '⬢',
                'intensity': utility,
                'trigger': 'integration_process'
            })
        
        # Action sigils (based on pressure)
        pressure = scup.get('pressure', 0.5)
        if pressure > 0.6 and random.random() < 0.4:
            active_sigils.append({
                'category': 'action',
                'symbol': '➤',
                'intensity': pressure,
                'trigger': 'action_execution'
            })
        
        # Meta sigils (periodic monitoring)
        if self.frame_count % 30 == 0 and random.random() < 0.5:
            active_sigils.append({
                'category': 'meta',
                'symbol': '◊',
                'intensity': 0.4 + 0.2 * random.random(),
                'trigger': 'meta_monitoring'
            })
        
        return active_sigils
    
    def add_sigil(self, category, symbol, intensity, trigger):
        """Add new sigil to the command stream"""
        # Get available text object
        if not self.available_texts:
            return  # No available text objects
        
        text_obj = self.available_texts.pop()
        
        sigil = {
            'category': category,
            'symbol': symbol,
            'intensity': intensity,
            'trigger': trigger,
            'timestamp': time.time(),
            'x_position': self.timeline_width - 5,
            'y_position': SIGIL_CATEGORIES[category]['lane'],
            'age': 0,
            'text_obj': text_obj,
            'sequence_id': None,
            'connections': []
        }
        
        # Configure text object
        text_obj.set_text(symbol)
        text_obj.set_position((sigil['x_position'], sigil['y_position']))
        text_obj.set_color(SIGIL_CATEGORIES[category]['color'])
        text_obj.set_fontsize(10 + intensity * 20)
        text_obj.set_alpha(0.3 + intensity * 0.7)
        
        self.active_sigils.append(sigil)
        self.sigil_history.append(sigil)
        
        # Update metrics
        self.metrics['sigil_counts'][category] += 1
        
        # Check for sequence patterns
        self.detect_command_sequences()
        
        # Check for interactions
        self.check_sigil_interactions(sigil)
    
    def detect_command_sequences(self):
        """Identify patterns of related sigil activations"""
        if len(self.sigil_history) < 3:
            return
        
        # Get recent sigils
        recent_sigils = list(self.sigil_history)[-10:]
        recent_categories = [s['category'] for s in recent_sigils]
        
        # Check for known sequences
        for seq_name, pattern in COMMAND_SEQUENCES.items():
            if self.matches_pattern(recent_categories, pattern):
                # Create sequence connection
                sequence_sigils = []
                pattern_index = 0
                
                for sigil in reversed(recent_sigils):
                    if pattern_index < len(pattern) and sigil['category'] == pattern[pattern_index]:
                        sequence_sigils.append(sigil)
                        sigil['sequence_id'] = seq_name
                        pattern_index += 1
                
                if len(sequence_sigils) == len(pattern):
                    self.command_sequences.append({
                        'name': seq_name,
                        'sigils': sequence_sigils,
                        'timestamp': time.time()
                    })
                    self.metrics['sequence_counts'][seq_name] += 1
    
    def matches_pattern(self, categories, pattern):
        """Check if categories list contains the pattern"""
        pattern_index = 0
        for cat in categories:
            if pattern_index < len(pattern) and cat == pattern[pattern_index]:
                pattern_index += 1
            if pattern_index == len(pattern):
                return True
        return False
    
    def check_sigil_interactions(self, new_sigil):
        """Check for sigil interaction effects"""
        category = new_sigil['category']
        if category not in SIGIL_INTERACTIONS:
            return
        
        # Trigger related sigils with some probability
        for target_category in SIGIL_INTERACTIONS[category]:
            if random.random() < 0.3:  # 30% chance of triggering
                # Add interaction sigil after short delay
                self.pending_interactions = getattr(self, 'pending_interactions', [])
                self.pending_interactions.append({
                    'category': target_category,
                    'trigger_time': time.time() + 0.5,
                    'source_sigil': new_sigil
                })
    
    def update_sigils(self):
        """Update sigil positions and states"""
        # Process pending interactions
        if hasattr(self, 'pending_interactions'):
            current_time = time.time()
            ready_interactions = [i for i in self.pending_interactions 
                                if i['trigger_time'] <= current_time]
            
            for interaction in ready_interactions:
                symbol = random.choice(SIGIL_CATEGORIES[interaction['category']]['symbols'])
                self.add_sigil(interaction['category'], symbol, 0.4, 'interaction')
                self.pending_interactions.remove(interaction)
        
        # Update active sigils
        expired_sigils = []
        for sigil in self.active_sigils:
            # Move sigil left
            sigil['x_position'] -= self.flow_speed
            sigil['age'] += 1
            
            # Update visual properties
            if sigil['x_position'] < 0:
                expired_sigils.append(sigil)
            else:
                # Update position
                sigil['text_obj'].set_position((sigil['x_position'], sigil['y_position']))
                
                # Fade based on age
                base_alpha = 0.3 + sigil['intensity'] * 0.7
                fade_factor = max(0, 1 - (sigil['age'] / 200))
                sigil['text_obj'].set_alpha(base_alpha * fade_factor)
                
                # Pulse effect for recent sigils
                if sigil['age'] < 20:
                    pulse = 1 + 0.2 * np.sin(sigil['age'] * 0.5)
                    base_size = 10 + sigil['intensity'] * 20
                    sigil['text_obj'].set_fontsize(base_size * pulse)
        
        # Remove expired sigils
        for sigil in expired_sigils:
            self.active_sigils.remove(sigil)
            sigil['text_obj'].set_alpha(0)
            self.available_texts.append(sigil['text_obj'])
        
        # Update sequence connections
        self.update_sequence_connections()
    
    def update_sequence_connections(self):
        """Update visual connections between sequence sigils"""
        segments = []
        
        for sequence in self.command_sequences[-5:]:  # Show last 5 sequences
            sigils = sequence['sigils']
            if len(sigils) < 2:
                continue
            
            # Create line segments between sequence sigils
            for i in range(len(sigils) - 1):
                if sigils[i] in self.active_sigils and sigils[i+1] in self.active_sigils:
                    x1, y1 = sigils[i]['x_position'], sigils[i]['y_position']
                    x2, y2 = sigils[i+1]['x_position'], sigils[i+1]['y_position']
                    segments.append([(x1, y1), (x2, y2)])
        
        self.connection_lines.set_segments(segments)
    
    def plot_active_sequences(self, ax):
        """Plot currently active sequences"""
        ax.clear()
        sequences = list(self.metrics['sequence_counts'].keys())[-5:]
        counts = [self.metrics['sequence_counts'][s] for s in sequences]
        
        if sequences:
            bars = ax.barh(sequences, counts, color='#4ecdc4', alpha=0.7)
            ax.set_xlabel('Count', fontsize=8, color='white')
            for i, (seq, count) in enumerate(zip(sequences, counts)):
                ax.text(count + 0.1, i, str(count), va='center', 
                       fontsize=8, color='white')
        else:
            ax.text(0.5, 0.5, 'No sequences yet', ha='center', va='center',
                   transform=ax.transAxes, color='gray')
        
        ax.set_xlim(0, max(counts) + 1 if counts else 1)
    
    def plot_category_distribution(self, ax):
        """Plot sigil category distribution"""
        ax.clear()
        categories = list(SIGIL_CATEGORIES.keys())
        counts = [self.metrics['sigil_counts'][cat] for cat in categories]
        total = sum(counts)
        
        if total > 0:
            percentages = [c/total * 100 for c in counts]
            colors = [SIGIL_CATEGORIES[cat]['color'] for cat in categories]
            
            # Create pie chart
            wedges, texts, autotexts = ax.pie(percentages, labels=categories,
                                              colors=colors, autopct='%1.0f%%',
                                              startangle=90)
            
            for text in texts:
                text.set_fontsize(8)
                text.set_color('white')
            for autotext in autotexts:
                autotext.set_fontsize(7)
                autotext.set_color('black')
                autotext.set_fontweight('bold')
        else:
            ax.text(0.5, 0.5, 'No data yet', ha='center', va='center',
                   transform=ax.transAxes, color='gray')
    
    def plot_command_rate(self, ax):
        """Plot command rate over time"""
        ax.clear()
        
        # Calculate rate from recent history
        if len(self.sigil_history) > 1:
            recent = list(self.sigil_history)[-20:]
            time_span = recent[-1]['timestamp'] - recent[0]['timestamp']
            if time_span > 0:
                rate = len(recent) / time_span
                self.metrics['recent_rate'] = rate
                
                # Simple bar showing rate
                ax.barh(['Rate'], [rate], color='#ff6b6b', alpha=0.7)
                ax.set_xlim(0, 10)
                ax.text(rate + 0.1, 0, f'{rate:.1f}/s', va='center',
                       fontsize=10, color='white', fontweight='bold')
        
        ax.set_xlabel('Commands/sec', fontsize=8, color='white')
    
    def plot_sequence_efficiency(self, ax):
        """Plot sequence completion efficiency"""
        ax.clear()
        
        # Calculate efficiency metrics
        total_sequences = sum(self.metrics['sequence_counts'].values())
        if total_sequences > 0:
            efficiency = min(1.0, total_sequences / (len(self.sigil_history) / 5))
            
            # Circular progress indicator
            theta = np.linspace(0, 2 * np.pi * efficiency, 100)
            r = 0.8
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            
            ax.plot(x, y, color='#96ceb4', linewidth=4)
            ax.text(0, 0, f'{efficiency*100:.0f}%', ha='center', va='center',
                   fontsize=16, fontweight='bold', color='white')
            ax.set_xlim(-1, 1)
            ax.set_ylim(-1, 1)
            ax.set_aspect('equal')
            ax.axis('off')
        else:
            ax.text(0.5, 0.5, 'No sequences', ha='center', va='center',
                   transform=ax.transAxes, color='gray')
    
    def plot_interaction_network(self, ax):
        """Plot sigil interaction network"""
        ax.clear()
        
        # Simple network visualization
        categories = list(SIGIL_CATEGORIES.keys())[:5]  # Limit for clarity
        n = len(categories)
        
        # Position nodes in circle
        angles = np.linspace(0, 2*np.pi, n, endpoint=False)
        x = np.cos(angles)
        y = np.sin(angles)
        
        # Draw connections
        for i, cat1 in enumerate(categories):
            if cat1 in SIGIL_INTERACTIONS:
                for cat2 in SIGIL_INTERACTIONS[cat1]:
                    if cat2 in categories:
                        j = categories.index(cat2)
                        ax.plot([x[i], x[j]], [y[i], y[j]], 
                               color='gray', alpha=0.3, linewidth=1)
        
        # Draw nodes
        for i, cat in enumerate(categories):
            color = SIGIL_CATEGORIES[cat]['color']
            ax.scatter(x[i], y[i], s=300, c=color, edgecolor='white', 
                      linewidth=2, zorder=5)
            ax.text(x[i], y[i], cat[0].upper(), ha='center', va='center',
                   fontsize=10, fontweight='bold', color='black')
        
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
    
    def plot_cognitive_rhythm(self, ax):
        """Plot cognitive rhythm patterns"""
        ax.clear()
        
        # Extract timing patterns
        if len(self.sigil_history) > 10:
            timestamps = [s['timestamp'] for s in list(self.sigil_history)[-50:]]
            intervals = np.diff(timestamps)
            
            if len(intervals) > 0:
                # Plot interval distribution
                ax.hist(intervals, bins=20, color='#54a0ff', alpha=0.7, 
                       edgecolor='white')
                ax.set_xlabel('Interval (s)', fontsize=8, color='white')
                ax.set_ylabel('Count', fontsize=8, color='white')
                
                # Add average line
                avg_interval = np.mean(intervals)
                ax.axvline(avg_interval, color='#ff6b6b', linestyle='--',
                          linewidth=2, label=f'Avg: {avg_interval:.2f}s')
                ax.legend(fontsize=8, loc='upper right')
        else:
            ax.text(0.5, 0.5, 'Gathering rhythm data...', ha='center', va='center',
                   transform=ax.transAxes, color='gray')
    
    def read_latest_json_data(self):
        """Read the latest data from JSON file"""
        json_file = "/tmp/dawn_tick_data.json"
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        if last_line:
                            return json.loads(last_line)
            except Exception as e:
                print(f"Error reading JSON: {e}", file=sys.stderr)
        return None

    def update_visualization(self, frame):
        """Animation update function"""
        self.frame_count = frame
        
        try:
            # Read data from JSON file
            data = self.read_latest_json_data()
            
            if data is None:
                # Use simulated data if no real data available
                data = {
                    'tick': frame,
                    'mood': {'valence': 0.5 + 0.2 * np.sin(frame * 0.05)},
                    'entropy': {'total_entropy': 0.5 + 0.2 * np.sin(frame * 0.03)},
                    'thermal_state': {'heat_level': 0.3 + 0.1 * np.cos(frame * 0.04)},
                    'scup': {'schema': 0.5, 'coherence': 0.5, 'utility': 0.5, 'pressure': 0.5}
                }
            
            # Get new data
            if not self.data_queue.empty():
                data = self.data_queue.get_nowait()
                sigils = self.parse_sigil_data(data)
                for sigil in sigils:
                    self.add_sigil(sigil['category'], sigil['symbol'],
                                 sigil['intensity'], sigil['trigger'])
            
            elif self.data_source == 'demo':
                # Generate demo data
                data = self.generate_demo_data(frame)
                sigils = self.parse_sigil_data(data)
                for sigil in sigils:
                    self.add_sigil(sigil['category'], sigil['symbol'],
                                 sigil['intensity'], sigil['trigger'])
            
            # Update sigil positions
            self.update_sigils()
            
            # Update metrics panels periodically
            if frame % 10 == 0:
                for ax in self.ax_metrics:
                    if hasattr(ax, 'plot_fn'):
                        ax.plot_fn(ax)
            
            # Update metadata
            self.metadata_text.set_text(
                f'Active Sigils: {len(self.active_sigils)} | '
                f'Total Commands: {len(self.sigil_history)} | '
                f'Rate: {self.metrics["recent_rate"]:.1f}/s'
            )
            
        except Exception as e:
            print(f"Update error: {e}", file=sys.stderr)
        
        return [t for t in self.sigil_texts if t.get_alpha() > 0] + [self.connection_lines]
    
    def generate_demo_data(self, frame):
        """Generate demonstration data with interesting patterns"""
        t = frame * 0.05
        
        # Base cognitive state
        data = {
            'entropy': 0.5 + 0.2 * np.sin(t * 0.7),
            'heat': 0.4 + 0.3 * np.sin(t * 1.1),
            'mood': {
                'base_level': 0.6 + 0.2 * np.cos(t * 0.9)
            },
            'scup': {
                'schema': 0.5 + 0.25 * np.sin(t * 0.8),
                'coherence': 0.5 + 0.25 * np.cos(t * 0.6),
                'utility': 0.5 + 0.2 * np.sin(t * 1.2),
                'pressure': 0.4 + 0.3 * abs(np.sin(t * 0.4))
            }
        }
        
        # Add periodic bursts
        if frame % 60 == 0:
            data['heat'] = min(1.0, data['heat'] + 0.3)
        
        # Add sequence triggers
        if frame % 40 == 20:
            data['scup']['coherence'] = 0.8
        
        return data
    
    def read_json_data(self):
        """Background thread to read data from JSON file"""
        json_file = "/tmp/dawn_tick_data.json"
        last_position = 0
        
        while not getattr(self, 'stop_event', None) or not self.stop_event.is_set():
            try:
                if not os.path.exists(json_file):
                    time.sleep(0.1)
                    continue
                
                with open(json_file, 'r') as f:
                    f.seek(last_position)
                    lines = f.readlines()
                    last_position = f.tell()
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            self.data_queue.put(data)
                        except json.JSONDecodeError as e:
                            print(f"Error parsing JSON: {e}", file=sys.stderr)
                            continue
                
                time.sleep(0.1)  # Small delay to avoid excessive CPU usage
                
            except Exception as e:
                print(f"Error reading JSON file: {e}", file=sys.stderr)
                time.sleep(1.0)  # Longer delay on error

    def run(self):
        """Start the visualization"""
        # Start stdin reader thread if needed
        if self.data_source == 'stdin':
            reader_thread = threading.Thread(target=self.read_json_data, daemon=True)
            reader_thread.start()
        
        # Create animation
        self.ani = animation.FuncAnimation(
            self.fig, self.update_visualization,
            interval=50,  # 20 FPS
            blit=False,
            cache_frame_data=False
        )
        
        plt.tight_layout()
        plt.show()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='DAWN Sigil Command Stream - Visualize internal cognitive commands'
    )
    parser.add_argument('--source', choices=['stdin', 'demo'], default='demo',
                       help='Data source (default: demo)')
    parser.add_argument('--speed', type=float, default=0.5,
                       help='Flow speed (default: 0.5)')
    parser.add_argument('--timeline-width', type=int, default=100,
                       help='Timeline width in time units (default: 100)')
    
    args = parser.parse_args()
    
    # Create and run visualization
    viz = SigilCommandStream(
        data_source=args.source,
        flow_speed=args.speed,
        timeline_width=args.timeline_width
    )
    
    print(f"Starting DAWN Sigil Command Stream Visualization...")
    print(f"Data source: {args.source}")
    print(f"Flow speed: {args.speed}")
    print(f"Timeline width: {args.timeline_width}")
    
    if args.source == 'stdin':
        print("Waiting for JSON data on stdin...")
    
    viz.run()

if __name__ == '__main__':
    main()