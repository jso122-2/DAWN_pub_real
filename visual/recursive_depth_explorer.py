#!/usr/bin/env python3
"""
DAWN Visualization #10: Recursive Depth Explorer
A 3D visualization revealing the recursive layers of DAWN's thinking processes,
showing how cognitive processing occurs at multiple meta-levels simultaneously.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import json
import sys
import argparse
import time
from datetime import datetime
from collections import deque, defaultdict
import threading
import queue
import random

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

class RecursiveDepthExplorer:
    """3D Recursive Depth Explorer Visualization"""
    
    def __init__(self, data_source='demo', max_depth=5):
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
        utility = scup.get('utility', 0.5)
        meta_trigger = coherence * utility
        
        if meta_trigger > 0.3:
            active_levels[1] = {
                'intensity': meta_trigger,
                'processes': self.detect_meta_processes(json_data),
                'focus_point': (coherence * 10 - 5, utility * 10 - 5, 2),
                'cloud_points': self.generate_process_cloud(1, meta_trigger)
            }
        
        # Level 2: Meta-meta
        schema_pressure = scup.get('schema', 0.5)
        if meta_trigger > 0.4 and schema_pressure > 0.5:
            meta_meta_intensity = meta_trigger * schema_pressure
            active_levels[2] = {
                'intensity': meta_meta_intensity,
                'processes': self.detect_meta_meta_processes(json_data),
                'focus_point': (schema_pressure * 10 - 5, meta_trigger * 10 - 5, 4),
                'cloud_points': self.generate_process_cloud(2, meta_meta_intensity)
            }
        
        # Level 3: Abstract recursion
        if len(active_levels) >= 3 and np.mean(list(scup.values())) > 0.6:
            abstract_intensity = np.std(list(scup.values()))
            active_levels[3] = {
                'intensity': abstract_intensity,
                'processes': ['abstract-pattern-recognition', 'recursive-synthesis'],
                'focus_point': (0, 0, 6),
                'cloud_points': self.generate_process_cloud(3, abstract_intensity)
            }
        
        # Level 4: Transcendent (rare)
        pressure = scup.get('pressure', 0.5)
        if len(active_levels) >= 4 and pressure > 0.7 and entropy > 0.7:
            transcendent_intensity = pressure * entropy * 0.5
            active_levels[4] = {
                'intensity': transcendent_intensity,
                'processes': ['transcendent-awareness', 'infinite-recursion'],
                'focus_point': (0, 0, 8),
                'cloud_points': self.generate_process_cloud(4, transcendent_intensity)
            }
        
        return active_levels
    
    def detect_direct_processes(self, json_data):
        """Identify direct cognitive processes"""
        processes = []
        heat = json_data.get('heat', 0.3)
        entropy = json_data.get('entropy', 0.5)
        
        if heat > 0.6:
            processes.append('focused-attention')
        if entropy > 0.6:
            processes.append('exploratory-processing')
        if heat < 0.3:
            processes.append('diffuse-cognition')
            
        return processes
    
    def detect_meta_processes(self, json_data):
        """Identify meta-cognitive processes"""
        processes = []
        scup = json_data.get('scup', {})
        
        if scup.get('coherence', 0.5) > 0.6:
            processes.append('cognitive_monitoring')
        if scup.get('utility', 0.5) > 0.6:
            processes.append('strategy_evaluation')
            
        return processes
    
    def detect_meta_meta_processes(self, json_data):
        """Identify meta-meta-cognitive processes"""
        processes = []
        scup = json_data.get('scup', {})
        
        if scup.get('schema', 0.5) > 0.6:
            processes.append('meta_learning')
        if scup.get('pressure', 0.5) > 0.5:
            processes.append('recursive_planning')
            
        return processes
    
    def generate_process_cloud(self, level, intensity):
        """Generate 3D point cloud for process visualization"""
        n_points = int(50 * intensity)
        if n_points < 5:
            return np.array([[], [], []]).T
        
        # Generate points in a sphere around focus area
        theta = np.random.uniform(0, 2*np.pi, n_points)
        phi = np.random.uniform(0, np.pi, n_points)
        r = np.random.normal(2, 0.5, n_points) * intensity
        
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = np.full(n_points, RECURSION_LEVELS[level]['z_position']) + \
            np.random.normal(0, 0.2, n_points)
        
        return np.column_stack((x, y, z))
    
    def detect_recursive_loops(self, active_levels):
        """Identify recursive processing loops between levels"""
        loops = []
        
        # Self-recursion detection
        for level, data in active_levels.items():
            if data['intensity'] > 0.6:
                loops.append({
                    'type': 'self_recursion',
                    'levels': [level, level],
                    'strength': data['intensity'],
                    'description': f'Self-referential at L{level}'
                })
        
        # Cross-level recursion
        level_list = list(active_levels.keys())
        for i, level1 in enumerate(level_list):
            for level2 in level_list[i+1:]:
                influence = self.calculate_cross_level_influence(
                    active_levels[level1], active_levels[level2]
                )
                
                if influence > 0.3:
                    loops.append({
                        'type': 'cross_recursion',
                        'levels': [level1, level2],
                        'strength': influence,
                        'description': f'L{level1} ↔ L{level2}'
                    })
        
        # Meta-recursive cycles
        if len(active_levels) >= 3:
            cycle_strength = self.detect_recursive_cycles(active_levels)
            if cycle_strength > 0.2:
                loops.append({
                    'type': 'recursive_cycle',
                    'levels': level_list,
                    'strength': cycle_strength,
                    'description': 'Multi-level cycle'
                })
        
        return loops
    
    def calculate_cross_level_influence(self, level1_data, level2_data):
        """Calculate influence strength between two levels"""
        # Simple influence model based on intensity and proximity
        intensity_product = level1_data['intensity'] * level2_data['intensity']
        
        # Add some randomness for dynamic effects
        noise = np.random.normal(0, 0.1)
        
        return np.clip(intensity_product + noise, 0, 1)
    
    def detect_recursive_cycles(self, active_levels):
        """Detect multi-level recursive cycles"""
        if len(active_levels) < 3:
            return 0
        
        # Calculate cycle strength based on balanced activity
        intensities = [data['intensity'] for data in active_levels.values()]
        mean_intensity = np.mean(intensities)
        std_intensity = np.std(intensities)
        
        # Strong cycles have high mean intensity and low variance
        cycle_strength = mean_intensity * (1 - std_intensity)
        
        return np.clip(cycle_strength, 0, 1)
    
    def analyze_recursive_patterns(self):
        """Deep analysis of recursive processing patterns"""
        if not self.active_processes:
            return self.recursive_analysis
        
        active_depths = list(self.active_processes.keys())
        
        analysis = {
            'max_active_depth': max(active_depths),
            'average_depth': np.mean(active_depths),
            'depth_distribution': len(active_depths) / self.max_depth,
            'recursive_loops_count': len(self.recursion_loops),
            'self_recursion_strength': self.measure_self_recursion(),
            'cross_level_connectivity': self.measure_cross_connectivity(),
            'recursive_complexity_index': self.calculate_recursive_complexity(),
            'meta_cognitive_load': self.measure_meta_load(),
            'transcendence_score': self.calculate_transcendence_score()
        }
        
        self.recursive_analysis = analysis
        return analysis
    
    def measure_self_recursion(self):
        """Measure strength of self-referential processing"""
        self_loops = [loop for loop in self.recursion_loops 
                     if loop['type'] == 'self_recursion']
        
        if not self_loops:
            return 0
        
        return np.mean([loop['strength'] for loop in self_loops])
    
    def measure_cross_connectivity(self):
        """Measure connectivity between different levels"""
        cross_loops = [loop for loop in self.recursion_loops 
                      if loop['type'] == 'cross_recursion']
        
        if not cross_loops:
            return 0
        
        return len(cross_loops) / (len(self.active_processes) * (len(self.active_processes) - 1) / 2)
    
    def calculate_recursive_complexity(self):
        """Calculate overall recursive complexity"""
        if not self.active_processes:
            return 0
        
        # Factors: number of active levels, loop count, intensity variance
        n_levels = len(self.active_processes)
        n_loops = len(self.recursion_loops)
        intensities = [data['intensity'] for data in self.active_processes.values()]
        intensity_variance = np.var(intensities)
        
        complexity = (n_levels / self.max_depth) * 0.3 + \
                    (min(n_loops, 10) / 10) * 0.4 + \
                    intensity_variance * 0.3
        
        return np.clip(complexity, 0, 1)
    
    def measure_meta_load(self):
        """Measure cognitive load from meta-processing"""
        meta_levels = [level for level in self.active_processes if level > 0]
        
        if not meta_levels:
            return 0
        
        # Higher levels contribute more to load
        load = sum(self.active_processes[level]['intensity'] * (level / self.max_depth) 
                  for level in meta_levels)
        
        return np.clip(load / len(meta_levels), 0, 1)
    
    def calculate_transcendence_score(self):
        """Calculate transcendent awareness score"""
        if len(self.active_processes) < 3:
            return 0
        
        # Transcendence indicators
        max_depth = max(self.active_processes.keys())
        depth_coverage = len(self.active_processes) / self.max_depth
        loop_harmony = 1 - np.std([loop['strength'] for loop in self.recursion_loops]) \
                      if self.recursion_loops else 0
        
        score = (max_depth / self.max_depth) * 0.3 + \
                depth_coverage * 0.3 + \
                loop_harmony * 0.4
        
        return np.clip(score, 0, 1)
    
    def update_visualization(self, frame):
        """Animation update function"""
        self.frame_count = frame
        
        try:
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
            print(f"Update error: {e}", file=sys.stderr)
        
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
            'mood': {
                'base_level': 0.6 + 0.2 * np.sin(t * 0.5)
            },
            'scup': {
                'schema': 0.5 + 0.25 * np.sin(t * 0.8),
                'coherence': 0.5 + 0.25 * np.cos(t * 0.6),
                'utility': 0.5 + 0.2 * np.sin(t * 1.2),
                'pressure': 0.4 + 0.3 * abs(np.sin(t * 0.4))
            }
        }
        
        # Create recursive depth waves
        if frame % 100 < 50:
            # Deep recursion phase
            boost = (frame % 100) / 50
            data['scup']['coherence'] *= (1 + boost * 0.5)
            data['scup']['schema'] *= (1 + boost * 0.3)
            data['entropy'] *= (1 + boost * 0.2)
        
        # Ensure values are in [0, 1]
        for key in data['scup']:
            data['scup'][key] = np.clip(data['scup'][key], 0, 1)
        data['entropy'] = np.clip(data['entropy'], 0, 1)
        data['heat'] = np.clip(data['heat'], 0, 1)
        
        return data
    
    def read_stdin_data(self):
        """Read JSON data from stdin"""
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                
                data = json.loads(line.strip())
                self.data_queue.put(data)
                
            except json.JSONDecodeError:
                continue
            except Exception as e:
                print(f"Error reading data: {e}", file=sys.stderr)
    
    def run(self):
        """Start the visualization"""
        # Start stdin reader thread if needed
        if self.data_source == 'stdin':
            reader_thread = threading.Thread(target=self.read_stdin_data, daemon=True)
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
        description='DAWN Recursive Depth Explorer - 3D visualization of recursive cognition'
    )
    parser.add_argument('--source', choices=['stdin', 'demo'], default='demo',
                       help='Data source (default: demo)')
    parser.add_argument('--max-depth', type=int, default=5,
                       help='Maximum recursion depth to visualize (default: 5)')
    parser.add_argument('--3d-mode', action='store_true',
                       help='Enable enhanced 3D effects')
    parser.add_argument('--recursive-analysis', action='store_true',
                       help='Show detailed recursive analysis')
    
    args = parser.parse_args()
    
    # Create and run visualization
    viz = RecursiveDepthExplorer(
        data_source=args.source,
        max_depth=args.max_depth
    )
    
    print(f"Starting DAWN Recursive Depth Explorer...")
    print(f"Data source: {args.source}")
    print(f"Max depth: {args.max_depth}")
    print(f"Controls: Use mouse to rotate view")
    
    if args.source == 'stdin':
        print("Waiting for JSON data on stdin...")
    
    viz.run()

if __name__ == '__main__':
    main()