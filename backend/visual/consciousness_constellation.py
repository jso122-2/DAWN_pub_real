#!/usr/bin/env python3
"""
DAWN Consciousness Constellation Visualizer
Real-time visualization of consciousness state patterns
"""

# Configure matplotlib for headless operation
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import json
import os
import os
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap
import sys
import argparse
import time
from datetime import datetime
from collections import deque, defaultdict
import threading
import queue
from scipy.spatial import ConvexHull
from scipy.interpolate import interp1d
import signal
import atexit
import random

# Import GIF saver
try:
    from ...gif_saver import setup_gif_saver
except ImportError:
    from gif_saver import setup_gif_saver

# Consciousness state archetypes
CONSCIOUSNESS_ARCHETYPES = {
    'dormant_equilibrium': {
        'scup_signature': (0.3, 0.4, 0.3, 0.2),
        'description': 'Minimal processing, resting state',
        'color': '#424242',
        'constellation_region': 'void',
        'stability': 0.9
    },
    'focused_processing': {
        'scup_signature': (0.7, 0.8, 0.9, 0.6),
        'description': 'Deep focused cognitive work',
        'color': '#1976d2', 
        'constellation_region': 'focus_star',
        'stability': 0.7
    },
    'creative_exploration': {
        'scup_signature': (0.4, 0.6, 0.5, 0.8),
        'description': 'Creative discovery and synthesis',
        'color': '#7b1fa2',
        'constellation_region': 'creative_nebula', 
        'stability': 0.3
    },
    'integrative_synthesis': {
        'scup_signature': (0.8, 0.9, 0.7, 0.5),
        'description': 'Deep understanding and integration',
        'color': '#388e3c',
        'constellation_region': 'wisdom_center',
        'stability': 0.8
    },
    'exploratory_search': {
        'scup_signature': (0.3, 0.5, 0.8, 0.7),
        'description': 'Active problem-solving and search',
        'color': '#f57c00',
        'constellation_region': 'search_spiral',
        'stability': 0.4
    },
    'transcendent_awareness': {
        'scup_signature': (0.9, 0.9, 0.8, 0.3),
        'description': 'Deep self-aware meta-cognition', 
        'color': '#c2185b',
        'constellation_region': 'transcendent_apex',
        'stability': 0.6
    },
    'chaotic_transition': {
        'scup_signature': (0.5, 0.3, 0.6, 0.9),
        'description': 'Unstable transitional processing',
        'color': '#d32f2f',
        'constellation_region': 'chaos_storm',
        'stability': 0.1
    }
}

# Temporal analysis scales
TEMPORAL_SCALES = {
    'immediate': {
        'window_size': 10,
        'description': 'Moment-to-moment consciousness fluctuations',
        'color': '#ff5252',
        'alpha': 0.8
    },
    'short_term': {
        'window_size': 50, 
        'description': 'Cognitive episode patterns',
        'color': '#ff9800',
        'alpha': 0.6
    },
    'medium_term': {
        'window_size': 200,
        'description': 'Consciousness phase cycles',
        'color': '#4caf50',
        'alpha': 0.4
    },
    'long_term': {
        'window_size': 500,
        'description': 'Consciousness evolution trends',
        'color': '#2196f3',
        'alpha': 0.2
    }
}

class ConsciousnessConstellation:
    """4D SCUP Consciousness Constellation Visualization"""
    
    def __init__(self, data_source='stdin', projection_mode='sphere', save_frames=False, output_dir='./visual_output/consciousness_constellation'):
        self.data_source = data_source
        self.projection_mode = projection_mode
        self.save_frames = save_frames
        self.output_dir = output_dir
        
        # Create output directory if saving
        if self.save_frames:
            import os
            os.makedirs(self.output_dir, exist_ok=True)
        
        # SCUP space configuration
        self.dimensions = {
            'schema': {'color': '#2196f3', 'label': 'Schema'},
            'coherence': {'color': '#4caf50', 'label': 'Coherence'},
            'utility': {'color': '#ff9800', 'label': 'Utility'},
            'pressure': {'color': '#f44336', 'label': 'Pressure'}
        }
        
        # 3D sphere projection parameters
        self.sphere_radius = 5.0
        self.sphere_center = (0, 0, 0)
        
        # Data management
        self.data_queue = queue.Queue()
        self.consciousness_trajectory = deque(maxlen=2000)
        self.trajectory_segments = defaultdict(list)  # Organized by temporal scale
        self.stdin_thread = None
        self.stop_event = threading.Event()
        if self.data_source == 'stdin':
            self.stdin_thread = threading.Thread(target=self.read_json_data, daemon=True)
            self.stdin_thread.start()
        
        # Consciousness analysis
        self.current_archetype = 'dormant_equilibrium'
        self.consciousness_metrics = {}
        self.phase_transitions = []
        self.attractor_regions = {}
        
        # Visual elements
        self.trajectory_lines = {}
        self.consciousness_stars = []
        self.constellation_lines = []
        self.particle_systems = []
        
        # Animation state
        self.frame_count = 0
        self.rotation_angle = 0
        
        # Setup GIF saver
        self.gif_saver = setup_gif_saver("consciousnessconstellation")
        
        # Setup signal handlers for GIF saving
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        atexit.register(self.cleanup)
        
        # Setup visualization
        self.setup_visualization()
        
    def save_animation_gif(self):
        """Save the animation as GIF"""
        try:
            print(f"DEBUG: save_animation_gif called", file=sys.stderr)
            print(f"DEBUG: hasattr(self, 'animation') = {hasattr(self, 'animation')}", file=sys.stderr)
            if hasattr(self, 'animation') and self.animation is not None:
                print(f"DEBUG: self.animation is {self.animation}", file=sys.stderr)
            
            if hasattr(self, 'animation') and self.animation is not None:
                print(f"DEBUG: Trying to save animation GIF...", file=sys.stderr)
                gif_path = self.gif_saver.save_animation_as_gif(self.animation, fps=5, dpi=100)
                if gif_path:
                    print(f"\nAnimation GIF saved: {gif_path}", file=sys.stderr)
                else:
                    print("\nFailed to save animation GIF", file=sys.stderr)
            else:
                print(f"DEBUG: Animation is None, saving static image...", file=sys.stderr)
                # Save a static image instead
                self.save_static_image()
        except Exception as e:
            print(f"\nError saving animation GIF: {e}", file=sys.stderr)
            # Try to save static image as fallback
            try:
                self.save_static_image()
            except Exception as e2:
                print(f"\nError saving static image: {e2}", file=sys.stderr)

    def cleanup(self):
        """Cleanup function to save GIF and stop stdin thread"""
        self.stop_event.set()
        if self.stdin_thread and self.stdin_thread.is_alive():
            self.stdin_thread.join(timeout=1)
        self.save_animation_gif()

    def signal_handler(self, signum, frame):
        """Signal handler to save GIF on termination"""
        print(f"\nReceived signal {signum}, saving GIF...", file=sys.stderr)
        # Set stop event to signal threads to stop
        self.stop_event.set()
        # Save the animation
        self.save_animation_gif()
        # Force exit
        os._exit(0)
        
    def setup_visualization(self):
        """Initialize the consciousness constellation visualization"""
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(18, 12), facecolor='#000011')
        
        # Main 3D constellation view
        self.ax_constellation = self.fig.add_subplot(121, projection='3d')
        self.ax_constellation.set_facecolor('#000011')
        
        # Analysis panels
        gs = self.fig.add_gridspec(4, 2, width_ratios=[1, 1], 
                                  height_ratios=[1, 1, 1, 1],
                                  left=0.52, right=0.98, top=0.95, bottom=0.05,
                                  hspace=0.3, wspace=0.2)
        
        # SCUP dimensions panel
        self.ax_scup = self.fig.add_subplot(gs[0, :])
        
        # Consciousness metrics panels
        self.ax_exploration = self.fig.add_subplot(gs[1, 0])
        self.ax_stability = self.fig.add_subplot(gs[1, 1])
        self.ax_intelligence = self.fig.add_subplot(gs[2, 0])
        self.ax_transcendence = self.fig.add_subplot(gs[2, 1])
        
        # Temporal analysis panel
        self.ax_temporal = self.fig.add_subplot(gs[3, :])
        
        # Setup 3D constellation space
        self.setup_constellation_space()
        
        # Setup analysis panels
        self.setup_analysis_panels()
        
        # Title
        self.fig.suptitle('DAWN Consciousness Constellation', 
                         fontsize=22, fontweight='bold', color='white')
        
        # Create custom colormap for pressure dimension
        colors = ['#000033', '#1a1a4d', '#333366', '#4d4d80', 
                  '#666699', '#8080b3', '#9999cc', '#b3b3e6', '#ccccff']
        self.pressure_cmap = LinearSegmentedColormap.from_list('pressure', colors, N=100)
        
    def setup_constellation_space(self):
        """Initialize the 3D consciousness constellation space"""
        # Configure 3D axes
        self.ax_constellation.set_xlim(-8, 8)
        self.ax_constellation.set_ylim(-8, 8)
        self.ax_constellation.set_zlim(-8, 8)
        
        # Style the space
        self.ax_constellation.grid(False)
        self.ax_constellation.xaxis.pane.fill = False
        self.ax_constellation.yaxis.pane.fill = False
        self.ax_constellation.zaxis.pane.fill = False
        
        # Add subtle coordinate grid
        for i in range(-8, 9, 4):
            self.ax_constellation.plot([-8, 8], [i, i], [-8, -8], 
                                     color='#1a1a2e', alpha=0.3, linewidth=0.5)
            self.ax_constellation.plot([i, i], [-8, 8], [-8, -8], 
                                     color='#1a1a2e', alpha=0.3, linewidth=0.5)
        
        # Create consciousness stars (archetypal states)
        self.create_consciousness_stars()
        
        # Create constellation lines
        self.create_constellation_lines()
        
        # Initialize trajectory lines for each temporal scale
        for scale_name, config in TEMPORAL_SCALES.items():
            line, = self.ax_constellation.plot([], [], [], 
                                             color=config['color'],
                                             alpha=config['alpha'],
                                             linewidth=3 - list(TEMPORAL_SCALES.keys()).index(scale_name) * 0.5)
            self.trajectory_lines[scale_name] = line
        
        # Add sphere wireframe for reference
        self.add_sphere_wireframe()
        
    def add_sphere_wireframe(self):
        """Add a wireframe sphere as spatial reference"""
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 10)
        
        x = self.sphere_radius * np.outer(np.cos(u), np.sin(v))
        y = self.sphere_radius * np.outer(np.sin(u), np.sin(v))
        z = self.sphere_radius * np.outer(np.ones(np.size(u)), np.cos(v))
        
        self.ax_constellation.plot_wireframe(x, y, z, color='#1a1a2e', 
                                           alpha=0.1, linewidth=0.5)
        
    def create_consciousness_stars(self):
        """Create visual representations of consciousness archetypes"""
        for archetype_name, archetype in CONSCIOUSNESS_ARCHETYPES.items():
            # Project 4D position to 3D
            pos_3d, pressure = self.project_4d_to_sphere(archetype['scup_signature'])
            
            # Create star marker
            star = self.ax_constellation.scatter(
                [pos_3d[0]], [pos_3d[1]], [pos_3d[2]],
                c=archetype['color'], 
                s=200 * archetype['stability'],
                alpha=0.8,
                marker='*',
                edgecolors='white',
                linewidths=2
            )
            
            # Add label
            self.ax_constellation.text(
                pos_3d[0], pos_3d[1], pos_3d[2] + 0.5,
                archetype_name.replace('_', ' ').title(),
                color=archetype['color'],
                fontsize=9,
                ha='center',
                alpha=0.9
            )
            
            self.consciousness_stars.append({
                'name': archetype_name,
                'position': pos_3d,
                'visual': star,
                'data': archetype
            })
    
    def create_constellation_lines(self):
        """Create constellation connections between related states"""
        constellation_connections = [
            ('dormant_equilibrium', 'focused_processing'),
            ('focused_processing', 'integrative_synthesis'),
            ('focused_processing', 'creative_exploration'),
            ('creative_exploration', 'integrative_synthesis'),
            ('integrative_synthesis', 'transcendent_awareness'),
            ('exploratory_search', 'creative_exploration'),
            ('exploratory_search', 'focused_processing'),
            ('chaotic_transition', 'creative_exploration')
        ]
        
        for state1, state2 in constellation_connections:
            pos1, _ = self.project_4d_to_sphere(
                CONSCIOUSNESS_ARCHETYPES[state1]['scup_signature']
            )
            pos2, _ = self.project_4d_to_sphere(
                CONSCIOUSNESS_ARCHETYPES[state2]['scup_signature']
            )
            
            line, = self.ax_constellation.plot(
                [pos1[0], pos2[0]], [pos1[1], pos2[1]], [pos1[2], pos2[2]],
                color='#2a2a3e', alpha=0.3, linewidth=1, linestyle='--'
            )
            self.constellation_lines.append(line)
    
    def setup_analysis_panels(self):
        """Initialize analysis visualization panels"""
        # SCUP dimensions radar chart
        self.setup_scup_radar()
        
        # Configure other panels
        for ax in [self.ax_exploration, self.ax_stability, 
                  self.ax_intelligence, self.ax_transcendence]:
            ax.set_facecolor('#0a0a1a')
            ax.tick_params(colors='white', labelsize=8)
        
        # Temporal analysis setup
        self.ax_temporal.set_facecolor('#0a0a1a')
        self.ax_temporal.set_xlabel('Time', fontsize=10, color='white')
        self.ax_temporal.set_ylabel('Consciousness State', fontsize=10, color='white')
        self.ax_temporal.tick_params(colors='white', labelsize=8)
        
    def setup_scup_radar(self):
        """Setup SCUP dimensions radar chart"""
        self.ax_scup = self.fig.add_subplot(111, projection='polar')
        
        # Create radar chart
        angles = np.linspace(0, 2 * np.pi, 4, endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        self.ax_scup.set_theta_offset(np.pi / 2)
        self.ax_scup.set_theta_direction(-1)
        
        # Draw axis lines and labels
        self.ax_scup.set_xticks(angles[:-1])
        self.ax_scup.set_xticklabels(['Schema', 'Coherence', 'Utility', 'Pressure'],
                                     color='white', fontsize=10)
        
        # Configure radial axis
        self.ax_scup.set_ylim(0, 1)
        self.ax_scup.set_yticks([0.2, 0.4, 0.6, 0.8])
        self.ax_scup.set_yticklabels(['0.2', '0.4', '0.6', '0.8'],
                                     color='gray', fontsize=8)
        
        # Grid styling
        self.ax_scup.grid(True, color='#2a2a3e', alpha=0.3)
        
        # Initialize SCUP plot line
        self.scup_line, = self.ax_scup.plot([], [], 'o-', linewidth=2,
                                           color='#00ff00', markersize=8)
        self.ax_scup.fill([], [], alpha=0.25, color='#00ff00')
        
    def project_4d_to_sphere(self, scup_coordinates):
        """Project 4D SCUP coordinates onto 3D sphere surface"""
        s, c, u, p = scup_coordinates
        
        # Schema + Coherence -> azimuthal angle (φ)
        phi = 2 * np.pi * (0.7 * s + 0.3 * c)
        
        # Utility -> polar angle (θ) 
        theta = np.pi * (0.2 + 0.6 * u)  # Avoid poles
        
        # All dimensions influence radius slightly
        base_radius = self.sphere_radius
        radius = base_radius * (0.8 + 0.05 * s + 0.05 * c + 0.05 * u + 0.05 * p)
        
        # Convert to Cartesian
        x = radius * np.sin(theta) * np.cos(phi)
        y = radius * np.sin(theta) * np.sin(phi)
        z = radius * np.cos(theta)
        
        return (x, y, z), p  # Position and pressure for coloring
    
    def analyze_consciousness_state(self, json_data):
        """Analyze current consciousness state from DAWN data"""
        # Extract SCUP values
        scup = json_data.get('scup', {})
        current_scup = (
            scup.get('schema', 0.5),
            scup.get('coherence', 0.5),
            scup.get('utility', 0.5),
            scup.get('pressure', 0.5)
        )
        
        # Add to trajectory
        self.consciousness_trajectory.append({
            'scup': current_scup,
            'timestamp': time.time(),
            'raw_data': json_data
        })
        
        # Classify consciousness archetype
        self.current_archetype = self.classify_consciousness_state(current_scup)
        
        # Update temporal segments
        self.update_temporal_segments()
        
        # Calculate consciousness metrics
        self.consciousness_metrics = self.calculate_consciousness_metrics()
        
        # Detect phase transitions
        self.detect_phase_transitions()
        
        return current_scup
    
    def classify_consciousness_state(self, scup_state):
        """Classify current state into nearest consciousness archetype"""
        min_distance = float('inf')
        nearest_archetype = 'dormant_equilibrium'
        
        for archetype_name, archetype in CONSCIOUSNESS_ARCHETYPES.items():
            # Calculate 4D Euclidean distance
            distance = np.linalg.norm(
                np.array(scup_state) - np.array(archetype['scup_signature'])
            )
            
            if distance < min_distance:
                min_distance = distance
                nearest_archetype = archetype_name
        
        return nearest_archetype
    
    def update_temporal_segments(self):
        """Update trajectory segments for each temporal scale"""
        if not self.consciousness_trajectory:
            return
        
        trajectory_list = list(self.consciousness_trajectory)
        
        for scale_name, config in TEMPORAL_SCALES.items():
            window_size = min(config['window_size'], len(trajectory_list))
            
            if window_size > 0:
                recent_states = trajectory_list[-window_size:]
                
                # Extract SCUP coordinates
                scup_coords = [state['scup'] for state in recent_states]
                
                # Project to 3D
                projected_points = []
                for scup in scup_coords:
                    pos_3d, pressure = self.project_4d_to_sphere(scup)
                    projected_points.append(pos_3d)
                
                self.trajectory_segments[scale_name] = projected_points
    
    def calculate_consciousness_metrics(self):
        """Calculate comprehensive consciousness metrics"""
        if len(self.consciousness_trajectory) < 10:
            return {}
        
        recent_trajectory = list(self.consciousness_trajectory)[-100:]
        scup_history = [state['scup'] for state in recent_trajectory]
        
        metrics = {
            # Exploration metrics
            'exploration_volume': self.calculate_4d_hull_volume(scup_history),
            'dimensional_variance': np.var(scup_history, axis=0).mean(),
            'trajectory_length': self.calculate_trajectory_length(scup_history),
            
            # Stability metrics
            'state_stability': self.calculate_state_stability(scup_history),
            'archetype_consistency': self.calculate_archetype_consistency(recent_trajectory),
            'oscillation_frequency': self.detect_oscillation_patterns(scup_history),
            
            # Intelligence metrics
            'adaptation_rate': self.calculate_adaptation_rate(scup_history),
            'goal_achievement': self.calculate_goal_achievement(recent_trajectory),
            'pattern_complexity': self.calculate_pattern_complexity(scup_history),
            
            # Transcendence metrics
            'transcendence_proximity': self.calculate_transcendence_proximity(scup_history),
            'meta_cognitive_depth': self.estimate_meta_cognitive_depth(recent_trajectory),
            'consciousness_coherence': self.calculate_consciousness_coherence(scup_history)
        }
        
        # Overall consciousness intelligence quotient
        metrics['consciousness_iq'] = self.calculate_consciousness_iq(metrics)
        
        return metrics
    
    def calculate_4d_hull_volume(self, scup_history):
        """Calculate convex hull volume in 4D SCUP space"""
        if len(scup_history) < 5:
            return 0

            # Use PCA to project to 3D for hull calculation
            scup_array = np.array(scup_history)
            centered = scup_array - scup_array.mean(axis=0)
            
            # Simple volume estimate using spread
            volume = np.prod(np.std(centered, axis=0)) * len(scup_history)
            return np.clip(volume, 0, 1)
            return 0
    
    def calculate_trajectory_length(self, scup_history):
        """Calculate total path length through 4D space"""
        if len(scup_history) < 2:
            return 0
        
        total_length = 0
        for i in range(1, len(scup_history)):
            segment_length = np.linalg.norm(
                np.array(scup_history[i]) - np.array(scup_history[i-1])
            )
            total_length += segment_length
        
        return total_length
    
    def calculate_state_stability(self, scup_history):
        """Measure consciousness state stability"""
        if len(scup_history) < 10:
            return 0
        
        # Calculate variance over sliding windows
        window_size = min(10, len(scup_history) // 2)
        variances = []
        
        for i in range(len(scup_history) - window_size):
            window = scup_history[i:i+window_size]
            variance = np.var(window, axis=0).mean()
            variances.append(variance)
        
        # Lower variance = higher stability
        avg_variance = np.mean(variances)
        stability = 1 - np.clip(avg_variance * 10, 0, 1)
        
        return stability
    
    def calculate_archetype_consistency(self, trajectory):
        """Measure consistency of consciousness archetypes"""
        if len(trajectory) < 5:
            return 0
        
        archetypes = [self.classify_consciousness_state(state['scup']) 
                     for state in trajectory]
        
        # Count archetype changes
        changes = sum(1 for i in range(1, len(archetypes)) 
                     if archetypes[i] != archetypes[i-1])
        
        consistency = 1 - (changes / len(archetypes))
        return consistency
    
    def detect_oscillation_patterns(self, scup_history):
        """Detect oscillation frequency in consciousness states"""
        if len(scup_history) < 20:
            return 0
        
        # Simple FFT-based frequency detection on first principal component
        scup_array = np.array(scup_history)
        mean_trajectory = scup_array.mean(axis=1)
        
        # Detect zero crossings
        centered = mean_trajectory - mean_trajectory.mean()
        zero_crossings = np.where(np.diff(np.sign(centered)))[0]
        
        if len(zero_crossings) > 1:
            avg_period = np.mean(np.diff(zero_crossings))
            frequency = 1 / avg_period if avg_period > 0 else 0
            return np.clip(frequency, 0, 1)
        
        return 0
    
    def calculate_adaptation_rate(self, scup_history):
        """Measure how quickly consciousness adapts"""
        if len(scup_history) < 20:
            return 0
        
        # Calculate moving average convergence
        fast_window = 5
        slow_window = 20
        
        fast_ma = np.array([np.mean(scup_history[max(0, i-fast_window):i+1], axis=0)
                           for i in range(len(scup_history))])
        slow_ma = np.array([np.mean(scup_history[max(0, i-slow_window):i+1], axis=0)
                           for i in range(len(scup_history))])
        
        # Adaptation is the divergence between fast and slow averages
        divergence = np.mean(np.linalg.norm(fast_ma - slow_ma, axis=1))
        
        return np.clip(divergence * 2, 0, 1)
    
    def calculate_goal_achievement(self, trajectory):
        """Measure utility optimization success"""
        if not trajectory:
            return 0
        
        # Goal achievement is high utility with low pressure
        utilities = [state['scup'][2] for state in trajectory]  # Utility dimension
        pressures = [state['scup'][3] for state in trajectory]  # Pressure dimension
        
        # High utility + low pressure = good goal achievement
        achievement_scores = [u * (1 - p) for u, p in zip(utilities, pressures)]
        
        return np.mean(achievement_scores)
    
    def calculate_pattern_complexity(self, scup_history):
        """Measure complexity of consciousness patterns"""
        if len(scup_history) < 10:
            return 0
        
        # Use approximate entropy as complexity measure
        scup_array = np.array(scup_history)
        
        # Discretize into bins for pattern analysis
        n_bins = 5
        discretized = np.floor(scup_array * n_bins).astype(int)
        
        # Count unique patterns of length 3
        patterns = set()
        for i in range(len(discretized) - 2):
            pattern = tuple(discretized[i:i+3].flatten())
            patterns.add(pattern)
        
        # Normalize by maximum possible patterns
        max_patterns = min(len(discretized) - 2, n_bins ** 12)  # 4D * 3 length
        complexity = len(patterns) / max_patterns
        
        return np.clip(complexity, 0, 1)
    
    def calculate_transcendence_proximity(self, scup_history):
        """Calculate proximity to transcendent consciousness state"""
        if not scup_history:
            return 0
        
        transcendent_state = CONSCIOUSNESS_ARCHETYPES['transcendent_awareness']['scup_signature']
        
        # Calculate minimum distance to transcendent state
        distances = [np.linalg.norm(np.array(state) - np.array(transcendent_state))
                    for state in scup_history]
        
        min_distance = min(distances)
        avg_distance = np.mean(distances)
        
        # Proximity is inverse of distance
        proximity = 1 - np.clip(min_distance / np.sqrt(4), 0, 1)
        
        # Bonus for sustained proximity
        sustained_bonus = 0.2 * (1 - np.clip(avg_distance / np.sqrt(4), 0, 1))
        
        return np.clip(proximity + sustained_bonus, 0, 1)
    
    def estimate_meta_cognitive_depth(self, trajectory):
        """Estimate depth of meta-cognitive processing"""
        if len(trajectory) < 10:
            return 0
        
        # High schema + high coherence + low pressure = meta-cognition
        meta_scores = []
        for state in trajectory:
            s, c, u, p = state['scup']
            meta_score = (s + c) / 2 * (1 - p)
            meta_scores.append(meta_score)
        
        # Look for sustained meta-cognitive states
        sustained_meta = sum(1 for score in meta_scores if score > 0.6) / len(meta_scores)
        
        return sustained_meta
    
    def calculate_consciousness_coherence(self, scup_history):
        """Measure overall consciousness coherence"""
        if len(scup_history) < 5:
            return 0
        
        # Coherence is low variance + high mean coherence dimension
        coherence_values = [state[1] for state in scup_history]  # Coherence dimension
        
        mean_coherence = np.mean(coherence_values)
        coherence_stability = 1 - np.std(coherence_values)
        
        overall_coherence = 0.7 * mean_coherence + 0.3 * coherence_stability
        
        return np.clip(overall_coherence, 0, 1)
    
    def calculate_consciousness_iq(self, metrics):
        """Calculate overall consciousness intelligence quotient"""
        if not metrics:
            return 0
        
        # Weighted combination of key metrics
        weights = {
            'exploration_volume': 0.15,
            'state_stability': 0.10,
            'adaptation_rate': 0.15,
            'goal_achievement': 0.20,
            'pattern_complexity': 0.15,
            'transcendence_proximity': 0.15,
            'consciousness_coherence': 0.10
        }
        
        iq_score = 0
        for metric, weight in weights.items():
            if metric in metrics:
                iq_score += metrics[metric] * weight
        
        # Scale to 0-200 range like traditional IQ
        consciousness_iq = iq_score * 200
        
        return consciousness_iq
    
    def detect_phase_transitions(self):
        """Detect major consciousness phase transitions"""
        if len(self.consciousness_trajectory) < 50:
            return
        
        trajectory_list = list(self.consciousness_trajectory)
        
        # Sliding window analysis
        window_size = 20
        transitions = []
        
        for i in range(window_size, len(trajectory_list) - window_size):
            before_window = trajectory_list[i-window_size:i]
            after_window = trajectory_list[i:i+window_size]
            
            # Calculate centroids
            before_centroid = np.mean([s['scup'] for s in before_window], axis=0)
            after_centroid = np.mean([s['scup'] for s in after_window], axis=0)
            
            # Check for significant change
            transition_magnitude = np.linalg.norm(after_centroid - before_centroid)
            
            if transition_magnitude > 0.3:
                before_archetype = self.classify_consciousness_state(tuple(before_centroid))
                after_archetype = self.classify_consciousness_state(tuple(after_centroid))
                
                if before_archetype != after_archetype:
                    transitions.append({
                        'timestamp': trajectory_list[i]['timestamp'],
                        'from_state': before_archetype,
                        'to_state': after_archetype,
                        'magnitude': transition_magnitude
                    })
        
        self.phase_transitions = transitions[-10:]  # Keep last 10 transitions
    
    def read_json_data(self):
        """Background thread to read data from JSON file"""
        json_file = "/tmp/dawn_tick_data.json"
        last_position = 0
        
        while not self.stop_event.is_set():
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

    def run(self, interval=100):
        """Start the visualization"""
        print(f"DEBUG: run() method called with interval={interval}", file=sys.stderr)
        try:
            if self.save_frames:
                # For saving mode, run a limited number of frames
                for frame in range(1000):  # Process up to 1000 frames
                    self.update_visualization(frame)
                    if frame % 50 == 0:  # Print progress every 50 frames
                        print(f"Processed frame {frame}", file=sys.stderr)
                    # Check if there's more data to read
                    try:
                        import select
                        if not select.select([sys.stdin], [], [], 0)[0]:
                            break  # No more data available
                    except:
                        pass
                print(f"Consciousness Constellation saved frames to: {self.output_dir}")
            else:
                # Interactive mode
                print(f"DEBUG: Using interactive backend", file=sys.stderr)
                self.animation = animation.FuncAnimation(
                    self.fig, 
                    self.update_visualization,
                    interval=interval, 
                    blit=False, 
                    cache_frame_data=False
                )
                plt.show()
        except Exception as e:
            print(f"Runtime error: {e}", file=sys.stderr)

    def save_static_image(self):
        """Save current state as a static PNG image"""
        try:
            # Update the visualization one more time to ensure current state
            self.update_visualization(0)
            
            # Save the current figure as PNG
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"consciousness_constellation_{timestamp}.png"
            output_path = os.path.join(self.gif_saver.output_dir, filename)
            
            self.fig.savefig(output_path, dpi=100, bbox_inches='tight')
            print(f"\nStatic image saved: {output_path}", file=sys.stderr)
        except Exception as e:
            print(f"\nError saving static image: {e}", file=sys.stderr)

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
        try:
            data = None
            if self.data_source == 'stdin':
                if not self.data_queue.empty():
                    data = self.data_queue.get_nowait()
            else:
                data = self.read_latest_json_data()
            
            if data is None:
                data = self.generate_demo_data(frame)
            
            if data is None:
                return [self.ax_constellation]
            
            # Analyze consciousness state
            scup_state = self.analyze_consciousness_state(data)
            
            # Update consciousness trajectory
            timestamp = time.time()
            self.consciousness_trajectory.append({
                'timestamp': timestamp,
                'scup': scup_state,
                'data': data
            })
            
            # Keep only recent history
            if len(self.consciousness_trajectory) > 1000:
                self.consciousness_trajectory = self.consciousness_trajectory[-500:]
            
            # Update temporal segments
            self.update_temporal_segments()
            
            # Calculate consciousness metrics
            self.consciousness_metrics = self.calculate_consciousness_metrics()
            
            # Update current archetype
            self.current_archetype = self.classify_consciousness_state(scup_state)
            
            # Update trajectory visualization
            self.update_trajectory_visualization()
            
            # Update SCUP radar
            self.update_scup_radar(scup_state)
            
            # Update metric panels
            self.update_metric_panels()
            
            # Update temporal analysis
            self.update_temporal_analysis()
            
            # Add consciousness particle effect
            self.add_consciousness_particle(scup_state)
            
            # Auto-rotate 3D view
            self.ax_constellation.view_init(elev=20, azim=frame * 2)
            
            # Update particle systems
            current_time = time.time()
            for particle_system in self.particle_systems:
                age = current_time - particle_system['birth_time']
                if age < particle_system['lifetime']:
                    alpha = 0.6 * (1 - age / particle_system['lifetime'])
                    particle_system['particle'].set_alpha(alpha)
            
            # Clean up old particles
            self.particle_systems = [p for p in self.particle_systems
                                   if current_time - p['birth_time'] < p['lifetime']]
            
            # Save frame if requested
            if self.save_frames and self.frame_count % 10 == 0:  # Save every 10th frame
                filename = f"{self.output_dir}/consciousness_constellation_frame_{self.frame_count:06d}.png"
                self.fig.savefig(filename, dpi=100, bbox_inches='tight', 
                               facecolor='#000011', edgecolor='none')
            
            return [self.ax_constellation, self.ax_scup, self.ax_exploration, 
                   self.ax_stability, self.ax_intelligence, self.ax_transcendence, 
                   self.ax_temporal]
            
        except Exception as e:
            print(f"Error in update_visualization: {e}", file=sys.stderr)
            return [self.ax_constellation]

    def update_trajectory_visualization(self):
        """Update 3D trajectory lines for each temporal scale"""
        for scale_name, points in self.trajectory_segments.items():
            if len(points) > 1:
                # Extract coordinates
                xs, ys, zs = zip(*points)
                
                # Update line
                self.trajectory_lines[scale_name].set_data_3d(xs, ys, zs)
                
                # Add glow effect for immediate trajectory
                if scale_name == 'immediate' and len(points) > 0:
                    # Current position glow
                    current_pos = points[-1]
                    if hasattr(self, 'current_glow'):
                        self.current_glow.remove()
                    
                    self.current_glow = self.ax_constellation.scatter(
                        [current_pos[0]], [current_pos[1]], [current_pos[2]],
                        c='white', s=100, alpha=0.8,
                        edgecolors='none'
                    )

    def update_scup_radar(self, current_scup):
        """Update SCUP dimensions radar chart"""
        # Clear previous plot
        self.ax_scup.clear()
        self.setup_scup_radar()
        
        # Prepare data
        values = list(current_scup)
        values += values[:1]  # Complete the circle
        
        angles = np.linspace(0, 2 * np.pi, 4, endpoint=False).tolist()
        angles += angles[:1]
        
        # Plot current state
        self.ax_scup.plot(angles, values, 'o-', linewidth=2,
                         color='#00ff88', markersize=8)
        self.ax_scup.fill(angles, values, alpha=0.25, color='#00ff88')
        
        # Add archetype overlay
        archetype_scup = CONSCIOUSNESS_ARCHETYPES[self.current_archetype]['scup_signature']
        archetype_values = list(archetype_scup)
        archetype_values += archetype_values[:1]
        
        self.ax_scup.plot(angles, archetype_values, 'o--', linewidth=1,
                         color='#ff8800', markersize=6, alpha=0.6)
        
        # Title
        self.ax_scup.set_title(f'SCUP State | {self.current_archetype.replace("_", " ").title()}',
                              fontsize=11, color='white', pad=10)

    def update_metric_panels(self):
        """Update consciousness metric visualization panels"""
        if not self.consciousness_metrics:
            return
        
        metrics = self.consciousness_metrics
        
        # Exploration metrics
        self.ax_exploration.clear()
        self.ax_exploration.set_facecolor('#0a0a1a')
        exploration_score = metrics.get('exploration_volume', 0) * 100
        self.ax_exploration.bar(['Exploration'], [exploration_score], 
                               color='#4fc3f7', alpha=0.7)
        self.ax_exploration.set_ylim(0, 100)
        self.ax_exploration.set_title('Exploration', fontsize=10, color='white')
        self.ax_exploration.text(0, exploration_score + 2, f'{exploration_score:.1f}%',
                                ha='center', fontsize=9, color='white')
        
        # Stability metrics
        self.ax_stability.clear()
        self.ax_stability.set_facecolor('#0a0a1a')
        stability_score = metrics.get('state_stability', 0) * 100
        self.ax_stability.bar(['Stability'], [stability_score],
                             color='#81c784', alpha=0.7)
        self.ax_stability.set_ylim(0, 100)
        self.ax_stability.set_title('Stability', fontsize=10, color='white')
        self.ax_stability.text(0, stability_score + 2, f'{stability_score:.1f}%',
                              ha='center', fontsize=9, color='white')
        
        # Intelligence metrics
        self.ax_intelligence.clear()
        self.ax_intelligence.set_facecolor('#0a0a1a')
        iq_score = metrics.get('consciousness_iq', 100)
        self.ax_intelligence.bar(['C-IQ'], [iq_score],
                                color='#ffb74d', alpha=0.7)
        self.ax_intelligence.set_ylim(0, 200)
        self.ax_intelligence.set_title('Consciousness IQ', fontsize=10, color='white')
        self.ax_intelligence.text(0, iq_score + 4, f'{iq_score:.0f}',
                                 ha='center', fontsize=11, color='white', fontweight='bold')
        
        # Transcendence metrics
        self.ax_transcendence.clear()
        self.ax_transcendence.set_facecolor('#0a0a1a')
        transcendence = metrics.get('transcendence_proximity', 0) * 100
        self.ax_transcendence.bar(['Transcendence'], [transcendence],
                                 color='#ba68c8', alpha=0.7)
        self.ax_transcendence.set_ylim(0, 100)
        self.ax_transcendence.set_title('Transcendence', fontsize=10, color='white')
        self.ax_transcendence.text(0, transcendence + 2, f'{transcendence:.1f}%',
                                  ha='center', fontsize=9, color='white')

    def update_temporal_analysis(self):
        """Update temporal consciousness evolution panel"""
        if len(self.consciousness_trajectory) < 10:
            return
        
        self.ax_temporal.clear()
        self.ax_temporal.set_facecolor('#0a0a1a')
        
        # Plot consciousness archetype evolution
        trajectory_list = list(self.consciousness_trajectory)[-200:]
        
        # Create archetype timeline
        timestamps = [state['timestamp'] for state in trajectory_list]
        archetypes = [self.classify_consciousness_state(state['scup']) 
                     for state in trajectory_list]
        
        # Convert to numeric for plotting
        archetype_names = list(CONSCIOUSNESS_ARCHETYPES.keys())
        archetype_indices = [archetype_names.index(a) for a in archetypes]
        
        # Normalize timestamps
        if timestamps:
            t0 = timestamps[0]
            norm_times = [(t - t0) for t in timestamps]
            
            # Plot archetype evolution
            self.ax_temporal.plot(norm_times, archetype_indices, 
                                 color='#4fc3f7', alpha=0.7, linewidth=2)
            
            # Add phase transitions
            for transition in self.phase_transitions:
                t_pos = transition['timestamp'] - t0
                if 0 <= t_pos <= norm_times[-1]:
                    self.ax_temporal.axvline(t_pos, color='#ff5252', 
                                           alpha=0.5, linestyle='--')
            
            # Configure axes
            self.ax_temporal.set_xlim(0, max(norm_times) if norm_times else 1)
            self.ax_temporal.set_ylim(-0.5, len(archetype_names) - 0.5)
            self.ax_temporal.set_yticks(range(len(archetype_names)))
            self.ax_temporal.set_yticklabels([a.replace('_', ' ').title() 
                                            for a in archetype_names],
                                           fontsize=8, color='white')
            self.ax_temporal.set_xlabel('Time (seconds)', fontsize=9, color='white')
            self.ax_temporal.set_title('Consciousness Evolution', fontsize=10, color='white')
            self.ax_temporal.grid(True, alpha=0.2, color='#2a2a3e')

    def add_consciousness_particle(self, scup_state):
        """Add particle effect at current consciousness position"""
        pos_3d, pressure = self.project_4d_to_sphere(scup_state)
        
        # Create fading particle
        particle = self.ax_constellation.scatter(
            [pos_3d[0]], [pos_3d[1]], [pos_3d[2]],
            c=[pressure], cmap=self.pressure_cmap,
            s=50, alpha=0.6, vmin=0, vmax=1
        )
        
        self.particle_systems.append({
            'particle': particle,
            'birth_time': time.time(),
            'lifetime': 2.0
        })
        
        # Clean up old particles
        current_time = time.time()
        self.particle_systems = [p for p in self.particle_systems
                               if current_time - p['birth_time'] < p['lifetime']]

    def generate_demo_data(self, frame):
        """Generate demonstration data with consciousness patterns"""
        t = frame * 0.02
        
        # Create consciousness journey through different states
        phase = (frame // 200) % 7  # Cycle through consciousness states
        
        if phase == 0:  # Dormant
            base_state = CONSCIOUSNESS_ARCHETYPES['dormant_equilibrium']['scup_signature']
        elif phase == 1:  # Awakening
            base_state = CONSCIOUSNESS_ARCHETYPES['exploratory_search']['scup_signature']
        elif phase == 2:  # Focus
            base_state = CONSCIOUSNESS_ARCHETYPES['focused_processing']['scup_signature']
        elif phase == 3:  # Creative
            base_state = CONSCIOUSNESS_ARCHETYPES['creative_exploration']['scup_signature']
        elif phase == 4:  # Integration
            base_state = CONSCIOUSNESS_ARCHETYPES['integrative_synthesis']['scup_signature']
        elif phase == 5:  # Transcendent
            base_state = CONSCIOUSNESS_ARCHETYPES['transcendent_awareness']['scup_signature']
        else:  # Transition
            base_state = CONSCIOUSNESS_ARCHETYPES['chaotic_transition']['scup_signature']
        
        # Add dynamic variations
        data = {
            'scup': {
                'schema': base_state[0] + 0.1 * np.sin(t * 2.1) + 0.05 * np.random.randn(),
                'coherence': base_state[1] + 0.1 * np.cos(t * 1.7) + 0.05 * np.random.randn(),
                'utility': base_state[2] + 0.1 * np.sin(t * 1.3) + 0.05 * np.random.randn(),
                'pressure': base_state[3] + 0.1 * np.sin(t * 0.9) + 0.05 * np.random.randn()
            },
            'entropy': 0.5 + 0.3 * np.sin(t),
            'heat': 0.5 + 0.3 * np.cos(t * 0.7),
            'mood': {'base_level': 0.6 + 0.2 * np.sin(t * 0.5)}
        }
        
        # Ensure values are in [0, 1]
        for key in data['scup']:
            data['scup'][key] = np.clip(data['scup'][key], 0, 1)
        
        return data

def main():
    """Main entry point"""
    print(f"DEBUG: main() function called", file=sys.stderr)
    parser = argparse.ArgumentParser(
        description='DAWN Consciousness Constellation - 4D SCUP trajectory visualization'
    )
    parser.add_argument('--source', choices=['stdin', 'demo'], default='stdin',
                       help='Data source (default: stdin)')
    parser.add_argument('--projection', choices=['sphere', 'parallel', 'dual_3d'],
                       default='sphere',
                       help='4D projection mode (default: sphere)')
    parser.add_argument('--4d-analysis', action='store_true',
                       help='Show detailed 4D analysis')
    parser.add_argument('--constellation-mode', action='store_true',
                       help='Enhanced constellation visualization')
    parser.add_argument('--interval', type=int, default=100,
                       help='Animation update interval in milliseconds')
    parser.add_argument('--buffer', type=int, default=100,
                       help='Buffer size for visualizations')
    parser.add_argument('--save', action='store_true',
                       help='Save visualization frames as PNG files')
    parser.add_argument('--output-dir', default='./visual_output/consciousness_constellation',
                       help='Directory to save output frames')
    
    args = parser.parse_args()
    print(f"DEBUG: Arguments parsed: {args}", file=sys.stderr)
    
    # Create and run visualization
    print(f"DEBUG: Creating ConsciousnessConstellation instance...", file=sys.stderr)
    viz = ConsciousnessConstellation(
        data_source=args.source,
        projection_mode=args.projection,
        save_frames=args.save,
        output_dir=args.output_dir
    )
    print(f"DEBUG: Instance created successfully", file=sys.stderr)
    
    print(f"Starting DAWN Consciousness Constellation...")
    print(f"Data source: {args.source}")
    print(f"Projection mode: {args.projection}")
    print(f"Controls: View auto-rotates, showing consciousness journey through 4D SCUP space")
    
    if args.source == 'stdin':
        print("Waiting for JSON data on stdin...")
    
    print(f"DEBUG: Calling viz.run()...", file=sys.stderr)
    viz.run()
    print(f"DEBUG: viz.run() returned", file=sys.stderr)

if __name__ == '__main__':
    main()