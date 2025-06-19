import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyBboxPatch
from matplotlib.collections import LineCollection
import numpy as np
import threading
import time
from collections import deque, defaultdict
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

class SigilCommandStreamVisualizer:
    """Backend-integrated Sigil Command Stream Visualization"""
    
    def __init__(self, timeline_width=100):
        # Timeline parameters
        self.timeline_width = timeline_width
        self.flow_speed = 0.5
        self.lane_height = 0.8
        self.num_lanes = len(SIGIL_CATEGORIES)
        
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
        
        # Threading
        self.lock = threading.Lock()
        self.visualization_data = {}
        self.running = False
        self._animation_thread = None
        
        # Initialize visualization
        self._init_visualization()
        
    def _init_visualization(self):
        """Initialize matplotlib components"""
        self.fig, self.ax = plt.subplots(figsize=(12, 8), facecolor='#0a0a0a')
        self.ax.set_xlim(0, self.timeline_width)
        self.ax.set_ylim(-0.5, self.num_lanes - 0.5)
        
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
            self.ax.add_patch(rect)
            
            # Lane label
            self.ax.text(-2, lane, category.capitalize(), 
                         ha='right', va='center',
                         fontsize=11, fontweight='bold',
                         color=props['color'])
        
        # Configure axes
        self.ax.set_xlabel('Time →', fontsize=12, color='white')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        
        # Time markers
        for i in range(0, self.timeline_width + 1, 10):
            self.ax.axvline(i, color='gray', alpha=0.2, linestyle='--')
        
        self.ax.set_title('DAWN Sigil Command Stream', fontsize=16, color='white', pad=20)

    def start_animation(self):
        if not self.running:
            self.running = True
            self._animation_thread = threading.Thread(target=self._background_update_loop, daemon=True)
            self._animation_thread.start()

    def stop_animation(self):
        self.running = False
        if self._animation_thread:
            self._animation_thread.join(timeout=1)

    def is_active(self):
        return self.running

    def update_visualization(self, mood, entropy, heat, scup_data):
        """Update with real cognitive metrics"""
        with self.lock:
            # Parse sigil data from cognitive metrics
            sigils = self._parse_sigil_data(mood, entropy, heat, scup_data)
            
            # Add new sigils
            for sigil in sigils:
                self._add_sigil(sigil['category'], sigil['symbol'],
                               sigil['intensity'], sigil['trigger'])
            
            # Update sigil positions
            self._update_sigils()
            
            # Update visualization data
            self._update_visualization_data()

    def _parse_sigil_data(self, mood, entropy, heat, scup_data):
        """Extract sigil triggers from cognitive metrics"""
        active_sigils = []
        
        # Normalize heat to 0-1 range
        heat_norm = min(heat / 100.0, 1.0) if isinstance(heat, (int, float)) else 0.5
        
        # Extract SCUP components
        coherence = scup_data.get('coherence', 0.5)
        schema_pressure = scup_data.get('schema_pressure', 0.5)
        utility = scup_data.get('utility', 0.5)
        pressure = scup_data.get('pressure', 0.5)
        
        # Attention sigils (based on heat/focus)
        if heat_norm > 0.7:
            active_sigils.append({
                'category': 'attention',
                'symbol': '◉',
                'intensity': heat_norm,
                'trigger': 'high_focus'
            })
        elif heat_norm < 0.3 and random.random() < 0.3:
            active_sigils.append({
                'category': 'attention',
                'symbol': '○',
                'intensity': 0.3,
                'trigger': 'attention_drift'
            })
        
        # Memory sigils (based on coherence)
        if coherence > 0.6:
            active_sigils.append({
                'category': 'memory',
                'symbol': '◆',
                'intensity': coherence,
                'trigger': 'memory_access'
            })
        
        # Reasoning sigils (based on schema)
        if schema_pressure > 0.6 and random.random() < 0.4:
            active_sigils.append({
                'category': 'reasoning',
                'symbol': '▲',
                'intensity': schema_pressure,
                'trigger': 'logical_processing'
            })
        
        # Creativity sigils (based on entropy + mood)
        creative_signal = entropy * mood
        if creative_signal > 0.5 and random.random() < 0.3:
            active_sigils.append({
                'category': 'creativity',
                'symbol': '✦',
                'intensity': creative_signal,
                'trigger': 'creative_spark'
            })
        
        # Integration sigils (based on utility)
        if utility > 0.5 and len(active_sigils) > 1:
            active_sigils.append({
                'category': 'integration',
                'symbol': '⬢',
                'intensity': utility,
                'trigger': 'integration_process'
            })
        
        # Action sigils (based on pressure)
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

    def _add_sigil(self, category, symbol, intensity, trigger):
        """Add new sigil to the command stream"""
        sigil = {
            'category': category,
            'symbol': symbol,
            'intensity': intensity,
            'trigger': trigger,
            'timestamp': time.time(),
            'x_position': self.timeline_width - 5,
            'y_position': SIGIL_CATEGORIES[category]['lane'],
            'age': 0,
            'sequence_id': None,
            'connections': []
        }
        
        self.active_sigils.append(sigil)
        self.sigil_history.append(sigil)
        
        # Update metrics
        self.metrics['sigil_counts'][category] += 1
        
        # Check for sequence patterns
        self._detect_command_sequences()
        
        # Check for interactions
        self._check_sigil_interactions(sigil)

    def _detect_command_sequences(self):
        """Identify patterns of related sigil activations"""
        if len(self.sigil_history) < 3:
            return
        
        # Get recent sigils
        recent_sigils = list(self.sigil_history)[-10:]
        recent_categories = [s['category'] for s in recent_sigils]
        
        # Check for known sequences
        for seq_name, pattern in COMMAND_SEQUENCES.items():
            if self._matches_pattern(recent_categories, pattern):
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

    def _matches_pattern(self, categories, pattern):
        """Check if categories list contains the pattern"""
        pattern_index = 0
        for cat in categories:
            if pattern_index < len(pattern) and cat == pattern[pattern_index]:
                pattern_index += 1
            if pattern_index == len(pattern):
                return True
        return False

    def _check_sigil_interactions(self, new_sigil):
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

    def _update_sigils(self):
        """Update sigil positions and states"""
        # Process pending interactions
        if hasattr(self, 'pending_interactions'):
            current_time = time.time()
            ready_interactions = [i for i in self.pending_interactions 
                                if i['trigger_time'] <= current_time]
            
            for interaction in ready_interactions:
                symbol = random.choice(SIGIL_CATEGORIES[interaction['category']]['symbols'])
                self._add_sigil(interaction['category'], symbol, 0.4, 'interaction')
                self.pending_interactions.remove(interaction)
        
        # Update active sigils
        expired_sigils = []
        for sigil in self.active_sigils:
            # Move sigil left
            sigil['x_position'] -= self.flow_speed
            sigil['age'] += 1
            
            # Check if expired
            if sigil['x_position'] < 0:
                expired_sigils.append(sigil)
        
        # Remove expired sigils
        for sigil in expired_sigils:
            self.active_sigils.remove(sigil)

    def _update_visualization_data(self):
        """Update visualization data for API"""
        # Calculate recent rate
        if len(self.sigil_history) > 1:
            recent = list(self.sigil_history)[-20:]
            time_span = recent[-1]['timestamp'] - recent[0]['timestamp']
            if time_span > 0:
                self.metrics['recent_rate'] = len(recent) / time_span
        
        # Prepare sigil data
        active_sigil_data = []
        for sigil in self.active_sigils:
            active_sigil_data.append({
                'category': sigil['category'],
                'symbol': sigil['symbol'],
                'intensity': sigil['intensity'],
                'trigger': sigil['trigger'],
                'x_position': sigil['x_position'],
                'y_position': sigil['y_position'],
                'age': sigil['age'],
                'color': SIGIL_CATEGORIES[sigil['category']]['color']
            })
        
        # Prepare sequence data
        recent_sequences = []
        for seq in self.command_sequences[-5:]:
            recent_sequences.append({
                'name': seq['name'],
                'timestamp': seq['timestamp'],
                'sigil_count': len(seq['sigils'])
            })
        
        self.visualization_data = {
            'active_sigils': active_sigil_data,
            'recent_sequences': recent_sequences,
            'metrics': dict(self.metrics),
            'sigil_categories': SIGIL_CATEGORIES,
            'command_sequences': COMMAND_SEQUENCES,
            'sigil_interactions': SIGIL_INTERACTIONS,
            'timestamp': time.time()
        }

    def get_visualization_data(self):
        with self.lock:
            return dict(self.visualization_data)

    def _background_update_loop(self):
        """Background update loop"""
        while self.running:
            self.frame_count += 1
            time.sleep(0.1)  # Update every 100ms

# Factory function for backend integration
def get_sigil_command_stream_visualizer():
    return SigilCommandStreamVisualizer(timeline_width=100) 