#!/usr/bin/env python3
"""
DAWN Visualization #9: Bloom Genealogy Network
A dynamic force-directed network showing DAWN's memory system as fractal blooms
with genealogical inheritance relationships.
"""

# Configure matplotlib for headless operation
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import sys
import json
import os
import math
import random
import time
import argparse
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple, Optional
import numpy as np
import queue
import threading
import signal
import atexit
import select
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Import GIF saver
try:
    from .gif_saver import setup_gif_saver
except ImportError:
    from gif_saver import setup_gif_saver

# Try to import pygame, but don't fail if not available
try:
    import pygame
    import pygame.gfxdraw
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("Warning: pygame not available, using matplotlib backend only")

# Bloom type definitions with inheritance patterns
BLOOM_TYPES = {
    'sensory': {
        'color': (79, 195, 247),  # Light blue
        'symbol': '◉',
        'description': 'Direct sensory memory blooms',
        'generation_rate': 0.8,
        'inheritance_pattern': 'linear',
        'base_size': 20
    },
    'conceptual': {
        'color': (129, 199, 132),  # Green
        'symbol': '◈',
        'description': 'Abstract concept memory blooms',
        'generation_rate': 0.6,
        'inheritance_pattern': 'branching',
        'base_size': 25
    },
    'emotional': {
        'color': (255, 138, 101),  # Orange
        'symbol': '◆',
        'description': 'Affective memory blooms',
        'generation_rate': 0.7,
        'inheritance_pattern': 'clustering',
        'base_size': 22
    },
    'procedural': {
        'color': (186, 104, 200),  # Purple
        'symbol': '◇',
        'description': 'Skill and procedure memory blooms',
        'generation_rate': 0.5,
        'inheritance_pattern': 'sequential',
        'base_size': 18
    },
    'meta': {
        'color': (255, 183, 77),  # Gold
        'symbol': '◎',
        'description': 'Meta-cognitive memory blooms',
        'generation_rate': 0.4,
        'inheritance_pattern': 'recursive',
        'base_size': 28
    },
    'creative': {
        'color': (240, 98, 146),  # Pink
        'symbol': '✦',
        'description': 'Novel synthesis memory blooms',
        'generation_rate': 0.3,
        'inheritance_pattern': 'fusion',
        'base_size': 30
    }
}

# Inheritance rules defining which bloom types can inherit from others
INHERITANCE_RULES = {
    'sensory': ['sensory'],
    'conceptual': ['sensory', 'emotional', 'conceptual'],
    'emotional': ['sensory', 'emotional'],
    'procedural': ['sensory', 'procedural', 'conceptual'],
    'meta': ['conceptual', 'meta', 'emotional'],
    'creative': ['conceptual', 'emotional', 'meta', 'procedural']
}

@dataclass
class MemoryBloom:
    """Represents a single memory bloom in the genealogy network"""
    id: int
    bloom_type: str
    generation: int = 0
    age: float = 0.0
    strength: float = 1.0
    activation_level: float = 0.0
    
    # Genealogical relationships
    parents: List['MemoryBloom'] = field(default_factory=list)
    children: List['MemoryBloom'] = field(default_factory=list)
    siblings: List['MemoryBloom'] = field(default_factory=list)
    family_line: Optional[int] = None
    
    # Fractal properties
    fractal_depth: int = 1
    branching_factor: float = 1.0
    complexity_score: float = 1.0
    
    # Network position and physics
    x: float = 0.0
    y: float = 0.0
    vx: float = 0.0
    vy: float = 0.0
    fx: float = 0.0  # Force x
    fy: float = 0.0  # Force y
    
    # Visual properties
    radius: float = 0.0
    pulse: float = 0.0
    birth_animation: float = 1.0
    
    def __post_init__(self):
        """Initialize calculated properties"""
        base_size = BLOOM_TYPES[self.bloom_type]['base_size']
        self.radius = base_size * math.sqrt(self.strength)
        
        # Initialize position with some randomness
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(50, 200)
        self.x = distance * math.cos(angle)
        self.y = distance * math.sin(angle)
        
        # Small initial velocity
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)

class BloomGenealogyNetwork:
    """Manages the bloom genealogy network and force simulation"""
    
    def __init__(self, width: int, height: int, save_frames=False, output_dir="./visual_output"):
        self.save_frames = save_frames
        self.output_dir = output_dir
        self.frame_count = 0
        
        # Create output directory if saving
        if self.save_frames:
            os.makedirs(self.output_dir, exist_ok=True)
        
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        
        # Network simulation parameters
        self.repulsion_strength = 5000
        self.attraction_strength = 0.001
        self.genealogy_attraction = 0.005
        self.damping = 0.85
        self.min_distance = 30
        
        # Bloom tracking
        self.blooms: Dict[int, MemoryBloom] = {}
        self.bloom_counter = 0
        self.active_blooms: Set[int] = set()
        
        # Family line tracking
        self.family_lines: Dict[int, List[int]] = {}
        self.family_counter = 0
        self.generation_layers: Dict[int, List[int]] = defaultdict(list)
        
        # Visual effects
        self.pulse_effects: List[Tuple[float, float, float, float]] = []
        self.connection_animations: List[Dict] = []
        
    def create_bloom(self, bloom_type: str, trigger: str, strength: float) -> MemoryBloom:
        """Create a new memory bloom"""
        bloom_id = self.bloom_counter
        self.bloom_counter += 1
        
        bloom = MemoryBloom(
            id=bloom_id,
            bloom_type=bloom_type,
            strength=strength,
            generation=0
        )
        
        # Find potential parents
        parents = self._find_parents(bloom)
        if parents:
            bloom.parents = parents
            bloom.generation = max(p.generation for p in parents) + 1
            
            # Update parent-child relationships
            for parent in parents:
                parent.children.append(bloom)
            
            # Assign or create family line
            parent_families = [p.family_line for p in parents if p.family_line is not None]
            if parent_families:
                bloom.family_line = parent_families[0]  # Inherit from first parent
            else:
                bloom.family_line = self.family_counter
                self.family_counter += 1
            
            # Calculate inherited properties
            bloom.fractal_depth = max(p.fractal_depth for p in parents) + 1
            bloom.branching_factor = np.mean([p.branching_factor for p in parents]) * 1.1
            bloom.complexity_score = sum(p.complexity_score for p in parents) * 0.7
            
            # Position near parents
            if parents:
                bloom.x = np.mean([p.x for p in parents]) + random.uniform(-30, 30)
                bloom.y = np.mean([p.y for p in parents]) + random.uniform(-30, 30)
        else:
            # Orphan bloom - create new family line
            bloom.family_line = self.family_counter
            self.family_counter += 1
        
        self.blooms[bloom_id] = bloom
        self.generation_layers[bloom.generation].append(bloom_id)
        
        if bloom.family_line not in self.family_lines:
            self.family_lines[bloom.family_line] = []
        self.family_lines[bloom.family_line].append(bloom_id)
        
        # Add birth animation
        bloom.birth_animation = 0.0
        self.active_blooms.add(bloom_id)
        
        return bloom
    
    def _find_parents(self, new_bloom: MemoryBloom) -> List[MemoryBloom]:
        """Find potential parent blooms based on inheritance rules"""
        if not self.blooms:
            return []
        
        compatible_types = INHERITANCE_RULES.get(new_bloom.bloom_type, [])
        potential_parents = []
        
        for bloom in self.blooms.values():
            if (bloom.bloom_type in compatible_types and 
                bloom.activation_level > 0.3 and
                bloom.age < 50):
                
                # Calculate similarity/compatibility
                similarity = self._calculate_similarity(new_bloom, bloom)
                if similarity > 0.4:
                    potential_parents.append((bloom, similarity))
        
        # Select top parents (1-3)
        potential_parents.sort(key=lambda x: x[1], reverse=True)
        return [bloom for bloom, _ in potential_parents[:min(3, len(potential_parents))]]
    
    def _calculate_similarity(self, bloom1: MemoryBloom, bloom2: MemoryBloom) -> float:
        """Calculate similarity between two blooms"""
        # Type compatibility
        type_score = 1.0 if bloom1.bloom_type == bloom2.bloom_type else 0.5
        
        # Temporal proximity
        age_diff = abs(bloom1.age - bloom2.age)
        temporal_score = math.exp(-age_diff / 20)
        
        # Activation correlation
        activation_score = bloom2.activation_level
        
        return (type_score * 0.4 + temporal_score * 0.3 + activation_score * 0.3)
    
    def update_forces(self):
        """Update forces for all blooms"""
        # Reset forces
        for bloom in self.blooms.values():
            bloom.fx = 0
            bloom.fy = 0
            
            # Attraction to center (weak)
            dx = self.center_x - bloom.x
            dy = self.center_y - bloom.y
            distance = math.sqrt(dx*dx + dy*dy) + 1
            bloom.fx += dx * 0.0001
            bloom.fy += dy * 0.0001
        
        # Repulsion between all blooms
        bloom_list = list(self.blooms.values())
        for i, bloom1 in enumerate(bloom_list):
            for bloom2 in bloom_list[i+1:]:
                dx = bloom1.x - bloom2.x
                dy = bloom1.y - bloom2.y
                distance = math.sqrt(dx*dx + dy*dy) + 0.1
                
                if distance < self.min_distance * 2:
                    force = self.repulsion_strength / (distance * distance)
                    fx = force * dx / distance
                    fy = force * dy / distance
                    
                    bloom1.fx += fx
                    bloom1.fy += fy
                    bloom2.fx -= fx
                    bloom2.fy -= fy
        
        # Genealogical attractions
        for bloom in self.blooms.values():
            # Attraction to parents
            for parent in bloom.parents:
                if parent.id in self.blooms:
                    self._apply_genealogy_force(bloom, parent, 1.0)
            
            # Weaker attraction to children
            for child in bloom.children:
                if child.id in self.blooms:
                    self._apply_genealogy_force(bloom, self.blooms[child.id], 0.5)
    
    def _apply_genealogy_force(self, bloom1: MemoryBloom, bloom2: MemoryBloom, strength: float):
        """Apply attractive force between genealogically related blooms"""
        dx = bloom2.x - bloom1.x
        dy = bloom2.y - bloom1.y
        distance = math.sqrt(dx*dx + dy*dy) + 1
        
        # Optimal distance based on generations
        optimal_distance = 80 + abs(bloom1.generation - bloom2.generation) * 30
        
        if distance > optimal_distance * 0.5:
            force = self.genealogy_attraction * strength * (distance - optimal_distance)
            bloom1.fx += force * dx / distance
            bloom1.fy += force * dy / distance
    
    def update_physics(self, dt: float):
        """Update bloom positions based on forces"""
        for bloom in self.blooms.values():
            # Update velocity with damping
            bloom.vx = (bloom.vx + bloom.fx * dt) * self.damping
            bloom.vy = (bloom.vy + bloom.fy * dt) * self.damping
            
            # Update position
            bloom.x += bloom.vx * dt
            bloom.y += bloom.vy * dt
            
            # Keep blooms on screen with soft boundaries
            margin = 50
            if bloom.x < margin:
                bloom.vx += (margin - bloom.x) * 0.1
            elif bloom.x > self.width - margin:
                bloom.vx -= (bloom.x - (self.width - margin)) * 0.1
            
            if bloom.y < margin:
                bloom.vy += (margin - bloom.y) * 0.1
            elif bloom.y > self.height - margin:
                bloom.vy -= (bloom.y - (self.height - margin)) * 0.1
            
            # Update visual properties
            bloom.age += dt
            bloom.activation_level *= 0.98  # Decay
            bloom.pulse = max(0, bloom.pulse - dt * 2)
            bloom.birth_animation = min(1.0, bloom.birth_animation + dt * 2)
    
    def activate_bloom(self, bloom_id: int, activation: float):
        """Activate a bloom, affecting its visual state"""
        if bloom_id in self.blooms:
            bloom = self.blooms[bloom_id]
            bloom.activation_level = min(1.0, bloom.activation_level + activation)
            bloom.pulse = 1.0
            
            # Add pulse effect
            self.pulse_effects.append((bloom.x, bloom.y, 0.0, bloom.radius * 2))
    
    def get_analytics(self) -> Dict:
        """Calculate genealogical analytics"""
        if not self.blooms:
            return {
                'total_blooms': 0,
                'family_lines': 0,
                'average_generation': 0,
                'max_generation': 0,
                'orphaned_blooms': 0,
                'most_prolific_parent': None,
                'deepest_lineage': 0,
                'active_families': 0
            }
        
        # Find most prolific parent
        child_counts = {bid: len(b.children) for bid, b in self.blooms.items()}
        most_prolific_id = max(child_counts, key=child_counts.get) if child_counts else None
        
        # Count orphans
        orphans = sum(1 for b in self.blooms.values() if not b.parents)
        
        # Find deepest lineage
        max_gen = max(b.generation for b in self.blooms.values()) if self.blooms else 0
        
        # Count active families
        active_families = set()
        for bloom in self.blooms.values():
            if bloom.activation_level > 0.1 and bloom.family_line is not None:
                active_families.add(bloom.family_line)
        
        return {
            'total_blooms': len(self.blooms),
            'family_lines': len(self.family_lines),
            'average_generation': np.mean([b.generation for b in self.blooms.values()]),
            'max_generation': max_gen,
            'orphaned_blooms': orphans,
            'most_prolific_parent': most_prolific_id,
            'deepest_lineage': max_gen,
            'active_families': len(active_families)
        }

class BloomVisualization:
    """Handles the visual rendering of the bloom genealogy network"""
    
    def __init__(self, width: int = 1600, height: int = 900, data_source='stdin', save_frames=False, output_dir="./visual_output"):
        self.width = width
        self.height = height
        self.data_source = data_source
        self.save_frames = save_frames
        self.output_dir = output_dir
        self.frame_count = 0
        self.time = 0.0
        
        # Create output directory if saving
        if self.save_frames:
            os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize pygame if available
        if PYGAME_AVAILABLE:
            pygame.init()
            self.screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption("DAWN Bloom Genealogy Network")
            self.clock = pygame.time.Clock()
            
            # Colors
            self.bg_color = (10, 10, 15)
            self.text_color = (200, 200, 210)
            self.grid_color = (30, 30, 35)
            self.edge_color = (120, 120, 130)
            
            # Fonts
            self.font_large = pygame.font.Font(None, 24)
            self.font_medium = pygame.font.Font(None, 18)
            self.font_small = pygame.font.Font(None, 14)
        
        # Initialize network
        self.network = BloomGenealogyNetwork(width, height, save_frames=save_frames, output_dir=output_dir)
        
        # UI state
        self.show_labels = True
        self.show_connections = True
        self.highlight_families = False
        self.selected_bloom = None
        
        # Data handling
        self.data_queue = queue.Queue()
        self.stop_event = threading.Event()
        
        # Create matplotlib figure for compatibility
        self.fig = plt.figure(figsize=(16, 9))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#0a0a0a')
        
        # Setup GIF saver
        self.gif_saver = setup_gif_saver("bloomgenealogynetwork")
        
        # Setup signal handlers for GIF saving
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        atexit.register(self.cleanup)

    def read_json_data(self):
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
                                continue
                    time.sleep(0.1)
                except Exception as e:
                    time.sleep(1.0)

    def detect_bloom_creation(self, json_data: dict) -> List[Dict]:
        """Analyze DAWN state to detect new memory bloom formation"""
        mood = json_data.get('mood', {})
        entropy = json_data.get('entropy', 0.5)
        heat = json_data.get('heat', 0.3)
        scup = json_data.get('scup', {})
        
        if not isinstance(scup, dict):
            scup = {}
        
        coherence = scup.get('coherence', 0.5)
        new_blooms = []
        
        # Ensure entropy and coherence are numbers
        if isinstance(entropy, dict):
            entropy = entropy.get('value', 0.5)
        if isinstance(coherence, dict):
            coherence = coherence.get('value', 0.5)
        
        # High entropy + coherence = conceptual bloom
        if entropy > 0.6 and coherence > 0.6:
            new_blooms.append({
                'type': 'conceptual',
                'trigger': 'high_coherence',
                'strength': entropy * coherence
            })
        
        # Emotional intensity = emotional bloom
        mood_vector = mood.get('vector', [0.5] * 8)
        mood_intensity = np.mean([abs(x - 0.5) for x in mood_vector])
        if mood_intensity > 0.4:
            new_blooms.append({
                'type': 'emotional',
                'trigger': 'emotional_spike',
                'strength': mood_intensity
            })
        
        # High heat = sensory/procedural bloom
        if heat > 0.7:
            bloom_type = 'sensory' if entropy > 0.5 else 'procedural'
            new_blooms.append({
                'type': bloom_type,
                'trigger': 'high_processing',
                'strength': heat
            })
        
        # Meta-cognitive bloom from high optimization
        optimization = scup.get('optimization', 0.5)
        if optimization > 0.7 and coherence > 0.6:
            new_blooms.append({
                'type': 'meta',
                'trigger': 'meta_cognition',
                'strength': optimization
            })
        
        # Creative bloom from unusual patterns
        if entropy > 0.8 and mood_intensity > 0.5:
            new_blooms.append({
                'type': 'creative',
                'trigger': 'creative_synthesis',
                'strength': (entropy + mood_intensity) / 2
            })
        
        return new_blooms
    
    def process_dawn_state(self, json_data: dict):
        """Process incoming DAWN state and update network"""
        # Detect new blooms
        new_blooms = self.detect_bloom_creation(json_data)
        
        for bloom_data in new_blooms:
            # Random chance based on generation rate
            gen_rate = BLOOM_TYPES[bloom_data['type']]['generation_rate']
            if random.random() < gen_rate:
                bloom = self.network.create_bloom(
                    bloom_data['type'],
                    bloom_data['trigger'],
                    bloom_data['strength']
                )
        
        # Activate existing blooms based on current state
        if self.network.blooms:
            # Random activation patterns
            num_to_activate = min(3, len(self.network.blooms))
            bloom_ids = random.sample(list(self.network.blooms.keys()), num_to_activate)
            
            for bloom_id in bloom_ids:
                activation = random.uniform(0.3, 0.8)
                self.network.activate_bloom(bloom_id, activation)
    
    def draw_bloom(self, bloom: MemoryBloom):
        """Draw a single memory bloom with fractal-inspired design"""
        x, y = int(bloom.x + 300), int(bloom.y)
        
        # Get bloom color
        base_color = BLOOM_TYPES[bloom.bloom_type]['color']
        
        # Adjust color based on activation
        activation_factor = 0.5 + bloom.activation_level * 0.5
        color = tuple(int(c * activation_factor) for c in base_color)
        
        # Birth animation
        if bloom.birth_animation < 1.0:
            radius = bloom.radius * bloom.birth_animation
            alpha = int(255 * bloom.birth_animation)
        else:
            radius = bloom.radius
            alpha = 255
        
        # Outer glow for active blooms
        if bloom.activation_level > 0.1:
            glow_radius = radius * (1.2 + bloom.pulse * 0.3)
            glow_alpha = int(bloom.activation_level * 50)
            for i in range(3):
                pygame.gfxdraw.filled_circle(
                    self.screen, x, y,
                    int(glow_radius + i * 3),
                    (*color, glow_alpha // (i + 1))
                )
        
        # Main bloom circle
        pygame.gfxdraw.filled_circle(self.screen, x, y, int(radius), (*color, alpha))
        pygame.gfxdraw.aacircle(self.screen, x, y, int(radius), (*color, alpha))
        
        # Fractal pattern based on bloom type
        if bloom.fractal_depth > 1:
            pattern = BLOOM_TYPES[bloom.bloom_type]['inheritance_pattern']
            self._draw_fractal_pattern(x, y, radius, color, pattern, bloom.fractal_depth)
        
        # Generation indicator
        if bloom.generation > 0:
            gen_radius = min(5, bloom.generation * 2)
            pygame.gfxdraw.filled_circle(
                self.screen, x, y,
                gen_radius,
                (255, 255, 255, 100)
            )
    
    def _draw_fractal_pattern(self, x: int, y: int, radius: float, color: Tuple, 
                             pattern: str, depth: int):
        """Draw fractal patterns inside blooms"""
        if pattern == 'branching':
            # Tree-like branching
            angles = [i * math.pi * 2 / 6 for i in range(6)]
            for angle in angles:
                end_x = x + math.cos(angle) * radius * 0.7
                end_y = y + math.sin(angle) * radius * 0.7
                pygame.draw.line(self.screen, color, (x, y), 
                               (int(end_x), int(end_y)), 1)
                
        elif pattern == 'clustering':
            # Clustered dots
            for i in range(min(depth * 2, 8)):
                angle = random.uniform(0, 2 * math.pi)
                dist = random.uniform(0, radius * 0.6)
                dot_x = x + math.cos(angle) * dist
                dot_y = y + math.sin(angle) * dist
                pygame.gfxdraw.filled_circle(
                    self.screen, int(dot_x), int(dot_y), 2, color
                )
                
        elif pattern == 'recursive':
            # Concentric circles
            for i in range(min(depth, 4)):
                inner_radius = radius * (0.8 - i * 0.2)
                if inner_radius > 2:
                    pygame.gfxdraw.circle(
                        self.screen, x, y,
                        int(inner_radius), color
                    )
    
    def draw_connections(self):
        """Draw inheritance connections between blooms"""
        for bloom in self.network.blooms.values():
            x1 = bloom.x + 300
            y1 = bloom.y
            
            # Draw connections to parents
            for parent in bloom.parents:
                if parent.id in self.network.blooms:
                    x2 = parent.x + 300
                    y2 = parent.y
                    
                    # Calculate control points for curved line
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2
                    
                    # Offset control point perpendicular to line
                    dx = x2 - x1
                    dy = y2 - y1
                    length = math.sqrt(dx*dx + dy*dy) + 1
                    
                    # Perpendicular vector
                    perp_x = -dy / length * 20
                    perp_y = dx / length * 20
                    
                    control_x = mid_x + perp_x
                    control_y = mid_y + perp_y
                    
                    # Draw curved connection
                    alpha = int(100 + bloom.activation_level * 100)
                    self._draw_bezier_curve(
                        (x1, y1), (control_x, control_y), (x2, y2),
                        (*self.edge_color, alpha), 2
                    )
    
    def _draw_bezier_curve(self, p1: Tuple, p2: Tuple, p3: Tuple, 
                          color: Tuple, width: int):
        """Draw a quadratic Bezier curve"""
        points = []
        for t in np.linspace(0, 1, 20):
            x = (1-t)**2 * p1[0] + 2*(1-t)*t * p2[0] + t**2 * p3[0]
            y = (1-t)**2 * p1[1] + 2*(1-t)*t * p2[1] + t**2 * p3[1]
            points.append((int(x), int(y)))
        
        for i in range(len(points) - 1):
            pygame.draw.line(self.screen, color, points[i], points[i+1], width)
    
    def draw_ui(self):
        """Draw the UI panel with metrics and information"""
        # UI panel background
        panel_rect = pygame.Rect(0, 0, 280, self.height)
        pygame.draw.rect(self.screen, (20, 20, 25), panel_rect)
        pygame.draw.line(self.screen, (40, 40, 45), 
                        (280, 0), (280, self.height), 2)
        
        y_offset = 20
        
        # Title
        title = self.font_large.render("Bloom Genealogy Network", True, self.text_color)
        self.screen.blit(title, (20, y_offset))
        y_offset += 40
        
        # Analytics
        analytics = self.network.get_analytics()
        
        metrics = [
            ("Total Blooms", f"{analytics['total_blooms']}"),
            ("Family Lines", f"{analytics['family_lines']}"),
            ("Max Generation", f"{analytics['max_generation']}"),
            ("Active Families", f"{analytics['active_families']}"),
            ("Orphaned Blooms", f"{analytics['orphaned_blooms']}"),
        ]
        
        for label, value in metrics:
            text = self.font_medium.render(f"{label}:", True, (150, 150, 160))
            self.screen.blit(text, (20, y_offset))
            value_text = self.font_medium.render(value, True, self.text_color)
            self.screen.blit(value_text, (180, y_offset))
            y_offset += 25
        
        y_offset += 20
        
        # Bloom type legend
        legend_title = self.font_medium.render("Bloom Types", True, self.text_color)
        self.screen.blit(legend_title, (20, y_offset))
        y_offset += 30
        
        for bloom_type, info in BLOOM_TYPES.items():
            # Color indicator
            pygame.draw.circle(self.screen, info['color'], 
                             (30, y_offset + 8), 8)
            
            # Type name
            text = self.font_small.render(bloom_type.capitalize(), 
                                        True, (180, 180, 190))
            self.screen.blit(text, (50, y_offset))
            y_offset += 20
        
        # Instructions
        y_offset = self.height - 120
        instructions = [
            "Controls:",
            "L - Toggle labels",
            "C - Toggle connections",
            "F - Toggle family highlight",
            "Click - Select bloom"
        ]
        
        for instruction in instructions:
            text = self.font_small.render(instruction, True, (120, 120, 130))
            self.screen.blit(text, (20, y_offset))
            y_offset += 18
    
    def draw_pulse_effects(self):
        """Draw expanding pulse effects"""
        to_remove = []
        for i, (x, y, radius, max_radius) in enumerate(self.network.pulse_effects):
            if radius < max_radius:
                alpha = int(255 * (1 - radius / max_radius))
                pygame.gfxdraw.circle(self.screen, int(x + 300), int(y), 
                                    int(radius), (*self.text_color, alpha))
                self.network.pulse_effects[i] = (x, y, radius + 2, max_radius)
            else:
                to_remove.append(i)
        
        for i in reversed(to_remove):
            self.network.pulse_effects.pop(i)
    
    def handle_click(self, pos: Tuple[int, int]):
        """Handle mouse click to select blooms"""
        x, y = pos
        x -= 300  # Adjust for UI panel
        
        # Find clicked bloom
        for bloom in self.network.blooms.values():
            dx = bloom.x - x
            dy = bloom.y - y
            if math.sqrt(dx*dx + dy*dy) <= bloom.radius:
                self.selected_bloom = bloom.id if self.selected_bloom != bloom.id else None
                break
    
    def update(self, dt: float):
        """Update the visualization state"""
        data = None
        if self.data_source == 'stdin':
            while not self.data_queue.empty():
                line = self.data_queue.get()
                if not line.strip():
                    continue
                data = json.loads(line)
        else:
            data = self.generate_demo_data()
        if data is not None:
            self.process_dawn_state(data)
        self.time += dt
        self.frame_count += 1
        
        # Update network physics
        self.network.update_forces()
        self.network.update_physics(dt)
        
        # Clean up old blooms if too many
        if len(self.network.blooms) > 200:
            # Remove oldest, inactive blooms
            candidates = [(b.id, b.age * (1 - b.activation_level)) 
                         for b in self.network.blooms.values()
                         if not b.children]  # Don't remove parents
            candidates.sort(key=lambda x: x[1], reverse=True)
            
            for bloom_id, _ in candidates[:10]:
                bloom = self.network.blooms[bloom_id]
                # Remove from parent's children list
                for parent in bloom.parents:
                    if bloom in parent.children:
                        parent.children.remove(bloom)
                del self.network.blooms[bloom_id]
                if bloom_id in self.network.active_blooms:
                    self.network.active_blooms.remove(bloom_id)
    
    def draw(self):
        """Draw the complete visualization"""
        self.screen.fill(self.bg_color)
        
        # Draw grid
        for x in range(300, self.width, 50):
            pygame.draw.line(self.screen, self.grid_color, 
                           (x, 0), (x, self.height), 1)
        for y in range(0, self.height, 50):
            pygame.draw.line(self.screen, self.grid_color,
                           (300, y), (self.width, y), 1)
        
        # Draw connections
        if self.show_connections:
            self.draw_connections()
        
        # Draw blooms
        for bloom in self.network.blooms.values():
            self.draw_bloom(bloom)
        
        # Draw selected bloom highlight
        if self.selected_bloom and self.selected_bloom in self.network.blooms:
            bloom = self.network.blooms[self.selected_bloom]
            x, y = int(bloom.x + 300), int(bloom.y)
            pygame.gfxdraw.circle(self.screen, x, y, 
                                int(bloom.radius + 10), (255, 255, 100))
        
        # Draw pulse effects
        self.draw_pulse_effects()
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def run(self, interval=200):
        """Start the visualization"""
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
                        self.data_queue.put(data)
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
            print(f"Bloom Genealogy Network saved {frame_count} frames to: {self.output_dir}")
        else:
            # Interactive mode 
            try:
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

    def generate_demo_data(self) -> dict:
        """Generate demo DAWN data for testing"""
        return {
            'entropy': random.uniform(0.3, 0.9),
            'heat': random.uniform(0.2, 0.8),
            'mood': {
                'vector': [random.uniform(0, 1) for _ in range(8)]
            },
            'scup': {
                'coherence': random.uniform(0.4, 0.8),
                'optimization': random.uniform(0.3, 0.9)
            },
            'tick': self.frame_count
        }

    def save_animation_gif(self):
        """Save the animation as GIF"""
        try:
            if hasattr(self, 'animation') and self.animation is not None:
                gif_path = self.gif_saver.save_animation_as_gif(self.animation, fps=5, dpi=100)
                if gif_path:
                    print(f"\nAnimation GIF saved: {gif_path}", file=sys.stderr)
                else:
                    print("\nFailed to save animation GIF", file=sys.stderr)
            else:
                print("\nNo animation to save", file=sys.stderr)
        except Exception as e:
            print(f"\nError saving animation GIF: {e}", file=sys.stderr)

    def cleanup(self):
        """Cleanup function to save GIF"""
        self.save_animation_gif()

    def signal_handler(self, signum, frame):
        """Signal handler to save GIF on termination"""
        print(f"\nReceived signal {signum}, saving GIF...", file=sys.stderr)
        self.save_animation_gif()
        sys.exit(0)

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
                data = self.generate_demo_data()
            
            # Process the data
            self.process_dawn_state(data)
            
            # Update physics
            self.network.update_physics(0.016)  # 60 FPS equivalent
            
            # Save frame if requested
            if self.save_frames and self.frame_count % 10 == 0:  # Save every 10th frame
                filename = f"{self.output_dir}/{self.__class__.__name__.lower()}_frame_{self.frame_count:06d}.png"
                self.fig.savefig(filename, dpi=100, bbox_inches='tight',
                               facecolor='#0a0a0a', edgecolor='none')
            
            self.frame_count += 1
            
            # Return empty list for matplotlib compatibility
            return []
            
        except Exception as e:
            print(f"Error in update_visualization: {e}", file=sys.stderr)
            self.frame_count += 1
            return []

def main():
    parser = argparse.ArgumentParser(
        description='DAWN Visualization #9: Bloom Genealogy Network'
    )
    parser.add_argument('--source', choices=['stdin', 'demo'], default='stdin',
                       help='Data source (default: stdin)')
    parser.add_argument('--width', type=int, default=1400,
                       help='Window width (default: 1400)')
    parser.add_argument('--height', type=int, default=900,
                       help='Window height (default: 900)')
    parser.add_argument('--max-blooms', type=int, default=200,
                       help='Maximum number of blooms (default: 200)')
    parser.add_argument('--interval', type=int, default=100,
                       help='Animation update interval in milliseconds')
    parser.add_argument('--buffer', type=int, default=100,
                       help='Buffer size for visualizations')
    parser.add_argument('--save', action='store_true',
                       help='Save visualization frames as PNG files')
    parser.add_argument('--output-dir', default='./visual_output',
                       help='Directory to save output frames')
    
    args = parser.parse_args()
    viz = BloomVisualization(args.width, args.height, data_source=args.source, 
                           save_frames=args.save, output_dir=args.output_dir)

    viz.run(interval=args.interval)
    print("\nVisualization terminated by user")
    sys.exit(0)

if __name__ == "__main__":
    main()