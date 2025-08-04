#!/usr/bin/env python3
"""
DAWN Visualization #10: Recursive Depth Explorer
A 3D visualization revealing the recursive layers of DAWN's thinking processes,
showing how cognitive processing occurs at multiple meta-levels simultaneously.
"""

# Configure matplotlib for headless operation
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import json
import os
import sys
import argparse
import time
from datetime import datetime
from collections import deque, defaultdict
import threading
import queue
import random
import signal
import atexit

# Import GIF saver
try:
    from ...gif_saver import setup_gif_saver
except ImportError:
    try:
        from gif_saver import setup_gif_saver
    except ImportError:
        def setup_gif_saver(name):
            return None

# Recursive layer definitions
RECURSION_LEVELS = {
    0: {
        'name': 'Direct Cognition',
        'description': 'Raw sensory and immediate processing',
        'color': '#4fc3f7',
        'z_position': 0,
        'opacity': 0.9,
        'processing_types': ['sensory', 'immediate', 'reactive']
    },
    1: {
        'name': 'Meta-Cognition', 
        'description': 'Thinking about thinking',
        'color': '#81c784',
        'z_position': 2,
        'opacity': 0.7,
        'processing_types': ['reflection', 'monitoring', 'evaluation']
    },
    2: {
        'name': 'Meta-Meta-Cognition',
        'description': 'Thinking about thinking about thinking', 
        'color': '#ffb74d',
        'z_position': 4,
        'opacity': 0.5,
        'processing_types': ['meta-reflection', 'cognitive-control', 'strategy']
    },
    3: {
        'name': 'Abstract Recursion',
        'description': 'Higher-order recursive processing',
        'color': '#f06292', 
        'z_position': 6,
        'opacity': 0.3,
        'processing_types': ['abstract-meta', 'pattern-patterns', 'recursive-loops']
    },
    4: {
        'name': 'Transcendent Recursion',
        'description': 'Deep recursive self-awareness',
        'color': '#ba68c8',
        'z_position': 8, 
        'opacity': 0.2,
        'processing_types': ['transcendent', 'self-awareness', 'infinite-recursion']
    }
}

# Recursive process types
RECURSIVE_PROCESS_TYPES = {
    'cognitive_monitoring': 'Monitoring own thinking processes',
    'strategy_evaluation': 'Evaluating cognitive strategies',
    'self_reflection': 'Reflecting on internal states',
    'meta_learning': 'Learning about learning processes',
    'recursive_planning': 'Planning about planning',
    'consciousness_observation': 'Observing consciousness itself',
    'infinite_regression': 'Potentially infinite recursive chains'
}

class Arrow3D(FancyArrowPatch):
    """Custom 3D arrow for visualizing recursive connections"""
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)
    
    def do_3d_projection(self, renderer=None):
        """Required method for matplotlib 3D compatibility"""
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return np.min(zs)

class RecursiveDepthExplorer:
    """3D Recursive Depth Explorer Visualization"""
    
    def __init__(self, data_source='stdin', max_depth=5):
        # Configuration
        self.data_source = data_source
        self.max_depth = max_depth
        self.layer_spacing = 2.0
        self.processing_cloud_size = 200
        
        # Data management
        self.data_queue = queue.Queue()
        self.active_processes = {}
        self.recursion_loops = []
        self.depth_history = deque(maxlen=100)
        
        # Visual elements
        self.layer_planes = {}
        self.process_clouds = {}
        self.recursion_arrows = []
        self.focus_points = {}
        self.particle_trails = deque(maxlen=500)
        
        # Analysis tracking
        self.recursive_analysis = {
            'max_active_depth': 0,
            'average_depth': 0,
            'recursive_loops_count': 0,
            'transcendence_score': 0
        }
        
        # Animation state
        self.frame_count = 0
        self.rotation_angle = 0
        
        # Data queue and background thread for stdin
        self.stdin_thread = None
        self.stop_event = threading.Event()
        if self.data_source == 'stdin':
            self.stdin_thread = threading.Thread(target=self.read_json_data, daemon=True)
            self.stdin_thread.start()
        
        # Setup GIF saver
        self.gif_saver = setup_gif_saver("recursivedepthexplorer")
        
        # Register cleanup function
        atexit.register(self.cleanup)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Setup visualization
        self.setup_visualization()
        
    def setup_visualization(self):
        """Initialize the 3D visualization"""
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(16, 12), facecolor='#0a0a0a')
        
        # Create 3D axis
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor('#0a0a0a')
        
        # Setup 3D space
        self.setup_3d_space()
        
        # Create UI panels
        self.setup_ui_panels()
        
        # Title
        self.fig.suptitle('DAWN Recursive Depth Explorer', 
                         fontsize=20, fontweight='bold', color='white')
        
    def setup_3d_space(self):
        """Initialize the 3D recursive depth visualization"""
        # Set axis limits and labels
        self.ax.set_xlim(-8, 8)
        self.ax.set_ylim(-8, 8) 
        self.ax.set_zlim(-0.5, 10)
        
        self.ax.set_xlabel('Cognitive Space X', color='white', fontsize=12)
        self.ax.set_ylabel('Cognitive Space Y', color='white', fontsize=12)
        self.ax.set_zlabel('Recursion Depth', color='white', fontsize=12)
        
        # Grid styling
        self.ax.grid(True, alpha=0.2)
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        
        # Create semi-transparent layer planes
        for level, config in RECURSION_LEVELS.items():
            if level < self.max_depth:
                z = config['z_position']
                xx, yy = np.meshgrid(np.linspace(-7, 7, 20), np.linspace(-7, 7, 20))
                zz = np.full_like(xx, z)
                
                # Add subtle wave effect
                wave = 0.1 * np.sin(xx * 0.5) * np.cos(yy * 0.5)
                zz = zz + wave
                
                self.layer_planes[level] = self.ax.plot_surface(
                    xx, yy, zz, alpha=config['opacity'] * 0.3, 
                    color=config['color'], shade=True, 
                    linewidth=0, antialiased=True
                )
        
        # Add level labels
        for level, config in RECURSION_LEVELS.items():
            if level < self.max_depth:
                self.ax.text(
                    7.5, 7.5, config['z_position'], 
                    f"L{level}: {config['name']}", 
                    color=config['color'], fontsize=11, 
                    weight='bold', alpha=0.8
                )
        
        # Initialize process cloud scatter plots
        for level in range(self.max_depth):
            self.process_clouds[level] = self.ax.scatter(
                [], [], [], c=RECURSION_LEVELS[level]['color'],
                s=50, alpha=0.6, edgecolors='white', linewidths=1
            )
        
        # Initialize focus point spheres
        for level in range(self.max_depth):
            self.focus_points[level] = self.ax.scatter(
                [], [], [], c=RECURSION_LEVELS[level]['color'],
                s=200, alpha=0.8, marker='o', edgecolors='white', 
                linewidths=2
            )
        
    def setup_ui_panels(self):
        """Create UI information panels"""
        # Recursive analysis panel
        self.analysis_text = self.fig.text(0.02, 0.95, '', fontsize=10,
                                          color='white', alpha=0.9,
                                          verticalalignment='top',
                                          family='monospace')
        
        # Active processes panel
        self.process_text = self.fig.text(0.85, 0.95, '', fontsize=9,
                                         color='white', alpha=0.9,
                                         verticalalignment='top',
                                         horizontalalignment='right',
                                         family='monospace')
        
        # Transcendence indicator
        self.transcendence_text = self.fig.text(0.5, 0.03, '', fontsize=14,
                                               ha='center', color='#ba68c8',
                                               fontweight='bold', alpha=0)
        
    def analyze_recursive_depth(self, json_data):
        """Detect active recursion levels from DAWN's cognitive state"""
        mood = json_data.get('mood', {})
        entropy = json_data.get('entropy', 0.5)
        heat = json_data.get('heat', 0.3)
        scup = json_data.get('scup', {})
        
        active_levels = {}
        
        # Level 0: Direct cognition (always active)
        direct_intensity = heat * 0.8 + entropy * 0.2
        active_levels[0] = {
            'intensity': direct_intensity,
            'processes': self.detect_direct_processes(json_data),
            'focus_point': (entropy * 10 - 5, heat * 10 - 5, 0),
            'cloud_points': self.generate_process_cloud(0, direct_intensity)
        }
        
        # Level 1: Meta-cognition
        coherence = scup.get('coherence', 0.5)
        meta_intensity = coherence * 0.7 + entropy * 0.3
        if meta_intensity > 0.2:
            active_levels[1] = {
                'intensity': meta_intensity,
                'processes': self.detect_meta_processes(json_data),
                'focus_point': (coherence * 8 - 4, entropy * 8 - 4, 2),
                'cloud_points': self.generate_process_cloud(1, meta_intensity)
            }
        
        # Level 2: Meta-meta-cognition
        schema = scup.get('schema', 0.5)
        meta_meta_intensity = schema * 0.6 + coherence * 0.4
        if meta_meta_intensity > 0.3:
            active_levels[2] = {
                'intensity': meta_meta_intensity,
                'processes': self.detect_meta_meta_processes(json_data),
                'focus_point': (schema * 6 - 3, coherence * 6 - 3, 4),
                'cloud_points': self.generate_process_cloud(2, meta_meta_intensity)
            }
        
        # Level 3: Abstract recursion
        utility = scup.get('utility', 0.5)
        abstract_intensity = utility * 0.5 + schema * 0.5
        if abstract_intensity > 0.4:
            active_levels[3] = {
                'intensity': abstract_intensity,
                'processes': ['abstract-meta', 'pattern-patterns'],
                'focus_point': (utility * 4 - 2, schema * 4 - 2, 6),
                'cloud_points': self.generate_process_cloud(3, abstract_intensity)
            }
        
        # Level 4: Transcendent recursion
        pressure = scup.get('pressure', 0.5)
        transcendent_intensity = pressure * 0.4 + utility * 0.6
        if transcendent_intensity > 0.5:
            active_levels[4] = {
                'intensity': transcendent_intensity,
                'processes': ['transcendent', 'self-awareness'],
                'focus_point': (pressure * 2 - 1, utility * 2 - 1, 8),
                'cloud_points': self.generate_process_cloud(4, transcendent_intensity)
            }
        
        return active_levels
    
    def detect_direct_processes(self, json_data):
        """Detect direct cognitive processes"""
        processes = []
        if json_data.get('heat', 0) > 0.6:
            processes.append('high_heat_processing')
        if json_data.get('entropy', 0) > 0.7:
            processes.append('high_entropy_processing')
        return processes or ['sensory_processing']
    
    def detect_meta_processes(self, json_data):
        """Detect meta-cognitive processes"""
        processes = []
        scup = json_data.get('scup', {})
        if scup.get('coherence', 0) > 0.6:
            processes.append('coherence_monitoring')
        if scup.get('schema', 0) > 0.5:
            processes.append('pattern_recognition')
        return processes or ['reflection']
    
    def detect_meta_meta_processes(self, json_data):
        """Detect meta-meta-cognitive processes"""
        processes = []
        scup = json_data.get('scup', {})
        if scup.get('schema', 0) > 0.7:
            processes.append('meta_pattern_analysis')
        if scup.get('coherence', 0) > 0.7:
            processes.append('cognitive_control')
        return processes or ['meta_reflection']
    
    def generate_process_cloud(self, level, intensity):
        """Generate cloud of process points for a recursion level"""
        if intensity < 0.1:
            return np.array([]).reshape(0, 3)
        
        # Number of points based on intensity
        n_points = int(intensity * self.processing_cloud_size)
        if n_points == 0:
            return np.array([]).reshape(0, 3)
        
        # Generate points around the level's center
        center = RECURSION_LEVELS[level]['z_position']
        x = np.random.normal(0, 2, n_points)
        y = np.random.normal(0, 2, n_points)
        z = np.random.normal(center, 0.5, n_points)
        
        return np.column_stack([x, y, z])
    
    def detect_recursive_loops(self, active_levels):
        """Detect recursive loops between levels"""
        loops = []
        
        # Self-recursion loops
        for level, data in active_levels.items():
            if data['intensity'] > 0.6:
                loops.append({
                    'type': 'self_recursion',
                    'levels': [level],
                    'strength': data['intensity'],
                    'processes': data['processes']
                })
        
        # Cross-level recursion
        levels = list(active_levels.keys())
        for i, level1 in enumerate(levels):
            for level2 in levels[i+1:]:
                # Check for cross-level influence
                influence = self.calculate_cross_level_influence(
                    active_levels[level1], active_levels[level2]
                )
                if influence > 0.4:
                    loops.append({
                        'type': 'cross_recursion',
                        'levels': [level1, level2],
                        'strength': influence,
                        'processes': active_levels[level1]['processes'] + 
                                   active_levels[level2]['processes']
                    })
        
        return loops
    
    def calculate_cross_level_influence(self, level1_data, level2_data):
        """Calculate influence between two recursion levels"""
        # Simple correlation-based influence
        intensity_diff = abs(level1_data['intensity'] - level2_data['intensity'])
        return max(0, 1 - intensity_diff)
    
    def detect_recursive_cycles(self, active_levels):
        """Detect longer recursive cycles"""
        cycles = []
        levels = list(active_levels.keys())
        
        if len(levels) >= 3:
            # Check for 3+ level cycles
            for i in range(len(levels) - 2):
                cycle_levels = levels[i:i+3]
                cycle_strength = np.mean([active_levels[l]['intensity'] for l in cycle_levels])
                if cycle_strength > 0.5:
                    cycles.append({
                        'type': 'cycle',
                        'levels': cycle_levels,
                        'strength': cycle_strength
                    })
        
        return cycles
    
    def analyze_recursive_patterns(self):
        """Analyze overall recursive patterns"""
        if not self.active_processes:
            return self.recursive_analysis
        
        # Calculate metrics
        active_levels = list(self.active_processes.keys())
        self.recursive_analysis['max_active_depth'] = max(active_levels) if active_levels else 0
        self.recursive_analysis['average_depth'] = np.mean(active_levels) if active_levels else 0
        self.recursive_analysis['recursive_loops_count'] = len(self.recursion_loops)
        
        # Calculate complexity index
        complexity = self.calculate_recursive_complexity()
        self.recursive_analysis['recursive_complexity_index'] = complexity
        
        # Calculate meta-cognitive load
        meta_load = self.measure_meta_load()
        self.recursive_analysis['meta_cognitive_load'] = meta_load
        
        # Calculate transcendence score
        transcendence = self.calculate_transcendence_score()
        self.recursive_analysis['transcendence_score'] = transcendence
        
        return self.recursive_analysis
    
    def measure_self_recursion(self):
        """Measure self-recursion intensity"""
        self_loops = [loop for loop in self.recursion_loops if loop['type'] == 'self_recursion']
        return np.mean([loop['strength'] for loop in self_loops]) if self_loops else 0
    
    def measure_cross_connectivity(self):
        """Measure cross-level connectivity"""
        cross_loops = [loop for loop in self.recursion_loops if loop['type'] == 'cross_recursion']
        return len(cross_loops) / max(1, len(self.active_processes))
    
    def calculate_recursive_complexity(self):
        """Calculate recursive complexity index"""
        if not self.active_processes:
            return 0
        
        # Factors: number of active levels, loop count, intensity variance
        n_levels = len(self.active_processes)
        n_loops = len(self.recursion_loops)
        intensity_variance = np.var([data['intensity'] for data in self.active_processes.values()])
        
        complexity = (n_levels / 5) * 0.4 + (n_loops / 10) * 0.3 + intensity_variance * 0.3
        return min(1.0, complexity)
    
    def measure_meta_load(self):
        """Measure meta-cognitive load"""
        if not self.active_processes:
            return 0
        
        # Weight by recursion depth
        total_load = 0
        for level, data in self.active_processes.items():
            weight = level + 1  # Higher levels have more weight
            total_load += data['intensity'] * weight
        
        return min(1.0, total_load / 15)  # Normalize
    
    def calculate_transcendence_score(self):
        """Calculate transcendence score"""
        if not self.active_processes:
            return 0
        
        # Focus on higher recursion levels
        transcendence = 0
        for level, data in self.active_processes.items():
            if level >= 3:  # Abstract and transcendent levels
                transcendence += data['intensity'] * (level - 2)
        
        return min(1.0, transcendence / 10)
    
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
                pass
        return None

    def update_visualization(self, frame):
        """Animation update function"""
        try:
            self.frame_count = frame
            
            # Get new data
            if not self.data_queue.empty():
                data = self.data_queue.get_nowait()
            elif self.data_source == 'demo':
                data = self.generate_demo_data(frame)
            else:
                return []
            
            # Analyze recursive depth
            self.active_processes = self.analyze_recursive_depth(data)
            
            # Detect recursive loops
            self.recursion_loops = self.detect_recursive_loops(self.active_processes)
            
            # Update process clouds
            for level, scatter in self.process_clouds.items():
                if level in self.active_processes:
                    points = self.active_processes[level]['cloud_points']
                    if len(points) > 0:
                        scatter._offsets3d = (points[:, 0], points[:, 1], points[:, 2])
                        scatter.set_alpha(0.3 + self.active_processes[level]['intensity'] * 0.4)
                else:
                    scatter._offsets3d = ([], [], [])
            
            # Update focus points
            for level, scatter in self.focus_points.items():
                if level in self.active_processes:
                    focus = self.active_processes[level]['focus_point']
                    scatter._offsets3d = ([focus[0]], [focus[1]], [focus[2]])
                    
                    # Pulse effect
                    pulse = 0.8 + 0.2 * np.sin(frame * 0.2)
                    scatter.set_sizes([200 * pulse * self.active_processes[level]['intensity']])
                else:
                    scatter._offsets3d = ([], [], [])
            
            # Update recursive arrows
            self.update_recursive_arrows()
            
            # Add particle trails
            self.update_particle_trails()
            
            # Analyze patterns
            analysis = self.analyze_recursive_patterns()
            
            # Update UI
            self.update_ui_text(analysis)
            
            # Rotate view slowly
            self.rotation_angle = (self.rotation_angle + 0.5) % 360
            self.ax.view_init(elev=20, azim=self.rotation_angle)
            
        except Exception as e:
            pass
        
        return []
    
    def update_recursive_arrows(self):
        """Update 3D arrows showing recursive connections"""
        # Remove old arrows
        for arrow in self.recursion_arrows:
            arrow.remove()
        self.recursion_arrows = []
        
        # Add new arrows for recursive loops
        for loop in self.recursion_loops[:5]:  # Limit to 5 for clarity
            if loop['type'] == 'self_recursion':
                # Self-loop visualization
                level = loop['levels'][0]
                if level in self.active_processes:
                    center = self.active_processes[level]['focus_point']
                    # Create circular arrow around focus point
                    self.add_circular_arrow(center, loop['strength'])
                    
            elif loop['type'] == 'cross_recursion':
                # Cross-level arrow
                level1, level2 = loop['levels']
                if level1 in self.active_processes and level2 in self.active_processes:
                    p1 = self.active_processes[level1]['focus_point']
                    p2 = self.active_processes[level2]['focus_point']
                    
                    arrow = Arrow3D([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]],
                                   mutation_scale=20, lw=2,
                                   arrowstyle='-|>', 
                                   color='white',
                                   alpha=0.3 + loop['strength'] * 0.4)
                    self.ax.add_artist(arrow)
                    self.recursion_arrows.append(arrow)
    
    def add_circular_arrow(self, center, strength):
        """Add circular arrow for self-recursion"""
        # Create circle points
        theta = np.linspace(0, 1.8 * np.pi, 20)
        radius = 1.5 * strength
        x = center[0] + radius * np.cos(theta)
        y = center[1] + radius * np.sin(theta)
        z = np.full_like(x, center[2] + 0.2)
        
        # Plot as line
        self.ax.plot(x, y, z, color='white', alpha=0.3 + strength * 0.4, linewidth=2)
    
    def update_particle_trails(self):
        """Update particle trail effects"""
        # Add new particles for active processes
        for level, data in self.active_processes.items():
            if data['intensity'] > 0.3 and np.random.random() < 0.3:
                # Emit particle from focus point
                focus = data['focus_point']
                particle = {
                    'pos': list(focus),
                    'vel': [np.random.normal(0, 0.1) for _ in range(3)],
                    'level': level,
                    'age': 0
                }
                self.particle_trails.append(particle)
        
        # Update existing particles
        for particle in list(self.particle_trails):
            particle['age'] += 1
            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]
            particle['pos'][2] += particle['vel'][2] * 0.5
            
            if particle['age'] > 30:
                self.particle_trails.remove(particle)
    
    def update_ui_text(self, analysis):
        """Update UI information panels"""
        # Recursive analysis panel
        analysis_str = "RECURSIVE ANALYSIS\n" + "="*20 + "\n"
        analysis_str += f"Max Depth: L{analysis['max_active_depth']}\n"
        analysis_str += f"Avg Depth: {analysis['average_depth']:.2f}\n"
        analysis_str += f"Active Loops: {analysis['recursive_loops_count']}\n"
        analysis_str += f"Complexity: {analysis['recursive_complexity_index']:.2%}\n"
        analysis_str += f"Meta Load: {analysis['meta_cognitive_load']:.2%}\n"
        analysis_str += f"Transcendence: {analysis['transcendence_score']:.2%}"
        
        self.analysis_text.set_text(analysis_str)
        
        # Active processes panel
        process_str = "ACTIVE PROCESSES\n" + "="*20 + "\n"
        for level, data in sorted(self.active_processes.items()):
            level_name = RECURSION_LEVELS[level]['name']
            process_str += f"\nL{level} - {level_name}\n"
            process_str += f"  Intensity: {data['intensity']:.2%}\n"
            for proc in data['processes'][:3]:
                process_str += f"  • {proc}\n"
        
        self.process_text.set_text(process_str)
        
        # Transcendence indicator
        if analysis['transcendence_score'] > 0.7:
            self.transcendence_text.set_text('⟨ TRANSCENDENT STATE DETECTED ⟩')
            self.transcendence_text.set_alpha(0.7 + 0.3 * np.sin(self.frame_count * 0.1))
        else:
            self.transcendence_text.set_alpha(0)
    
    def generate_demo_data(self, frame):
        """Generate demonstration data with recursive patterns"""
        t = frame * 0.03
        
        # Base cognitive state with recursive patterns
        data = {
            'entropy': 0.5 + 0.3 * np.sin(t) + 0.1 * np.sin(t * 5),
            'heat': 0.4 + 0.3 * np.cos(t * 0.7) + 0.1 * np.cos(t * 3),
            'mood': {'valence': 0.5 + 0.2 * np.sin(t * 0.5)},
            'scup': {
                'schema': 0.5 + 0.3 * np.sin(t * 0.3) + 0.1 * np.sin(t * 7),
                'coherence': 0.5 + 0.25 * np.cos(t * 0.4) + 0.1 * np.cos(t * 6),
                'utility': 0.5 + 0.2 * np.sin(t * 0.6) + 0.1 * np.sin(t * 8),
                'pressure': 0.3 + 0.4 * abs(np.sin(t * 0.2)) + 0.2 * np.random.random()
            }
        }
        
        # Add recursive patterns
        if np.random.random() < 0.05:
            # Occasional recursive spikes
            data['scup']['schema'] = min(1.0, data['scup']['schema'] + 0.3)
            data['scup']['coherence'] = min(1.0, data['scup']['coherence'] + 0.2)
        
        return data
    
    def read_json_data(self):
        """Background thread to read data from JSON file"""
        import sys
        if getattr(self, 'data_source', None) == 'stdin':
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    self.data_queue.put(data)
                except Exception as e:
                    print(f"Error parsing JSON: {e}", file=sys.stderr)
        else:
            json_file = "/tmp/dawn_tick_data.json"
            last_position = 0
            while not hasattr(self, 'stop_event') or not self.stop_event.is_set():
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
                                continue
                    time.sleep(0.1)
                except Exception as e:
                    time.sleep(1.0)
    
    def run(self, interval=200):
        """Start the visualization"""
        # Create animation
        self.ani = animation.FuncAnimation(
            self.fig, self.update_visualization,
            interval=interval,  # 5 FPS for backend
            blit=False,
            cache_frame_data=False
        )
        
        # Save animation as GIF
        self.save_animation_gif()
        
        # Don't show in backend mode - it's non-interactive
        # plt.show()
        
        # Keep the process alive for a moment to ensure saving completes
        time.sleep(2)
    
    def save_animation_gif(self):
        """Save the animation as a GIF"""
        if hasattr(self, 'gif_saver') and self.gif_saver:
            try:
                gif_path = self.gif_saver.save_animation_as_gif(self.ani, fps=5, dpi=100)
                if gif_path:
                    print(f"Animation saved: {gif_path}")
            except Exception as e:
                print(f"Failed to save animation: {e}")
        else:
            print("GIF saver not available")
    
    def cleanup(self):
        """Cleanup function"""
        if hasattr(self, 'stop_event'):
            self.stop_event.set()
        if hasattr(self, 'stdin_thread') and self.stdin_thread:
            self.stdin_thread.join(timeout=1.0)
    
    def signal_handler(self, signum, frame):
        """Signal handler for graceful shutdown"""
        self.cleanup()
        sys.exit(0)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Recursive Depth Explorer Visualization')
    parser.add_argument('--source', default='stdin', 
                       choices=['demo', 'stdin'],
                       help='Data source (demo or stdin)')
    parser.add_argument('--max-depth', type=int, default=5,
                       help='Maximum recursion depth to visualize')
    
    args = parser.parse_args()
    
    # Create and run visualization
    viz = RecursiveDepthExplorer(
        data_source=args.source,
        max_depth=args.max_depth
    )
    
    viz.run()

if __name__ == '__main__':
    main()