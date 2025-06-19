import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import threading
import time
from collections import deque, defaultdict
import signal
import atexit

# Import GIF saver
try:
    from .gif_saver import setup_gif_saver
except ImportError:
    from gif_saver import setup_gif_saver

DRIFT_STATES = {
    'contemplative': {
        'color': '#4a90e2', 'position': (0, 1), 'description': 'Deep reflection and analysis'
    },
    'exploratory': {
        'color': '#7ed321', 'position': (1, 0.5), 'description': 'Active discovery and search'
    },
    'integrative': {
        'color': '#f5a623', 'position': (0, 0), 'description': 'Synthesis and consolidation'
    },
    'creative': {
        'color': '#d0021b', 'position': (-1, 0.5), 'description': 'Generative and novel thinking'
    },
    'analytical': {
        'color': '#9013fe', 'position': (0.5, -1), 'description': 'Logical processing and reasoning'
    },
    'intuitive': {
        'color': '#50e3c2', 'position': (-0.5, -1), 'description': 'Pattern sensing and insight'
    },
    'dormant': {
        'color': '#4a4a4a', 'position': (0, -0.5), 'description': 'Low activity and rest'
    },
    'emergent': {
        'color': '#ff6b6b', 'position': (0, 0.5), 'description': 'Novel pattern emergence'
    }
}

DRIFT_STATE_LIST = list(DRIFT_STATES.keys())
STATE_INDEX = {s: i for i, s in enumerate(DRIFT_STATE_LIST)}

class DriftStateTransitionsVisualizer:
    def __init__(self, history_length=100):
        self.current_state = 'dormant'
        self.previous_state = 'dormant'
        self.state_history = deque(maxlen=history_length)
        self.transition_counts = defaultdict(int)
        self.dwell_times = defaultdict(list)
        self.current_dwell_start = time.time()
        self.transition_matrix = np.zeros((len(DRIFT_STATES), len(DRIFT_STATES)))
        self.graph = nx.DiGraph()
        self.node_positions = {s: DRIFT_STATES[s]['position'] for s in DRIFT_STATES}
        self.lock = threading.Lock()
        self.visualization_data = {}
        self.running = False
        self._animation_thread = None
        self._setup_graph()

    def _setup_graph(self):
        for state, props in DRIFT_STATES.items():
            self.graph.add_node(state, color=props['color'], description=props['description'])
        for src in DRIFT_STATES:
            for dst in DRIFT_STATES:
                if src != dst:
                    self.graph.add_edge(src, dst, weight=0)

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

    def detect_drift_state(self, mood, entropy, heat, scup_data):
        """Analyze DAWN's cognitive metrics to determine current drift state"""
        
        # Extract SCUP components - use real data if available, fallback to defaults
        coherence = scup_data.get('coherence', 0.5)
        schema_pressure = scup_data.get('schema_pressure', 0.5)
        utility = scup_data.get('utility', 0.5)
        pressure = scup_data.get('pressure', 0.5)
        
        # Normalize heat to 0-1 range
        heat_norm = min(heat / 100.0, 1.0) if isinstance(heat, (int, float)) else 0.5
        
        # State detection heuristics based on cognitive metrics
        if entropy > 0.7 and mood > 0.6:
            return 'exploratory', 0.8
        elif coherence > 0.8 and entropy < 0.4:
            return 'contemplative', 0.9
        elif heat_norm > 0.8 and schema_pressure > 0.7:
            return 'creative', 0.7
        elif schema_pressure > 0.8 and coherence > 0.7:
            return 'analytical', 0.8
        elif mood > 0.7 and entropy > 0.5:
            return 'integrative', 0.6
        elif heat_norm < 0.3 and entropy < 0.3:
            return 'dormant', 0.9
        elif utility > 0.8 and pressure < 0.4:
            return 'intuitive', 0.7
        elif pressure > 0.8 and heat_norm > 0.6:
            return 'emergent', 0.6
        else:
            # Default to contemplative if no clear pattern
            return 'contemplative', 0.5

    def update_visualization(self, mood, entropy, heat, scup_data):
        """Update with real cognitive metrics"""
        drift_state, confidence = self.detect_drift_state(mood, entropy, heat, scup_data)
        with self.lock:
            now = time.time()
            if drift_state != self.current_state:
                # Record dwell time
                dwell = now - self.current_dwell_start
                self.dwell_times[self.current_state].append(dwell)
                self.current_dwell_start = now
                # Update transition counts
                self.transition_counts[(self.current_state, drift_state)] += 1
                self.state_history.append((self.current_state, drift_state, now))
                self.previous_state = self.current_state
                self.current_state = drift_state
            self._update_transition_matrix()
            self._update_visualization_data(confidence)

    def _update_transition_matrix(self):
        mat = np.zeros((len(DRIFT_STATES), len(DRIFT_STATES)))
        for (src, dst), count in self.transition_counts.items():
            i, j = STATE_INDEX[src], STATE_INDEX[dst]
            mat[i, j] = count
        # Normalize rows to get probabilities
        row_sums = mat.sum(axis=1, keepdims=True)
        with np.errstate(divide='ignore', invalid='ignore'):
            probs = np.divide(mat, row_sums, out=np.zeros_like(mat), where=row_sums!=0)
        self.transition_matrix = probs

    def _update_visualization_data(self, confidence):
        # Node data
        node_data = {}
        for state in DRIFT_STATES:
            node_data[state] = {
                'color': DRIFT_STATES[state]['color'],
                'description': DRIFT_STATES[state]['description'],
                'size': 300 + 700 * (np.mean(self.dwell_times[state]) if self.dwell_times[state] else 0.1),
                'is_current': (state == self.current_state),
                'is_previous': (state == self.previous_state)
            }
        # Edge data
        edge_data = {}
        for (src, dst), count in self.transition_counts.items():
            edge_data[(src, dst)] = {
                'weight': count,
                'probability': float(self.transition_matrix[STATE_INDEX[src], STATE_INDEX[dst]])
            }
        # Recent path
        recent_path = list(self.state_history)[-10:]
        # Stats
        dwell = time.time() - self.current_dwell_start
        likely_next = self._get_most_likely_next_states(self.current_state)
        self.visualization_data = {
            'nodes': node_data,
            'edges': edge_data,
            'current_state': self.current_state,
            'previous_state': self.previous_state,
            'recent_path': recent_path,
            'dwell_time': dwell,
            'likely_next': likely_next,
            'confidence': confidence,
            'transition_matrix': self.transition_matrix.tolist(),
            'timestamp': time.time()
        }

    def _get_most_likely_next_states(self, state, topn=3):
        idx = STATE_INDEX[state]
        probs = self.transition_matrix[idx]
        sorted_indices = np.argsort(probs)[::-1]
        return [DRIFT_STATE_LIST[i] for i in sorted_indices[:topn] if probs[i] > 0]

    def get_visualization_data(self):
        with self.lock:
            return dict(self.visualization_data)

    def _background_update_loop(self):
        # No simulation - this will be called from external updates
        while self.running:
            time.sleep(1)  # Just keep the thread alive

    def simulate_dawn_data(self):
        # Remove simulation - this should not be called
        pass

# Factory function for backend integration
def get_drift_state_transitions_visualizer():
    return DriftStateTransitionsVisualizer(history_length=100)