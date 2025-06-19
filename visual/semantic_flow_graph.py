#!/usr/bin/env python3
"""
DAWN Visualization #11: Semantic Flow Graph
A dynamic network visualization showing how meaning propagates through DAWN's
cognitive system with semantic relationships, concept activation, and emergence.
"""

import sys
import json
import math
import random
import time
import argparse
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple, Optional
import numpy as np

try:
    import pygame
    import pygame.gfxdraw
except ImportError:
    print("Error: pygame is required. Install with: pip install pygame")
    sys.exit(1)

# Semantic concept categories with properties
SEMANTIC_CATEGORIES = {
    'perceptual': {
        'color': (0, 188, 212),  # Cyan
        'description': 'Sensory and perceptual concepts',
        'examples': ['color', 'sound', 'texture', 'movement', 'brightness', 'pattern', 'shape'],
        'activation_threshold': 0.3,
        'propagation_speed': 1.0
    },
    'emotional': {
        'color': (233, 30, 99),  # Pink
        'description': 'Affective and emotional concepts',
        'examples': ['joy', 'curiosity', 'tension', 'flow', 'wonder', 'excitement', 'calm'],
        'activation_threshold': 0.4,
        'propagation_speed': 1.2
    },
    'abstract': {
        'color': (156, 39, 176),  # Purple
        'description': 'Abstract and conceptual meanings',
        'examples': ['pattern', 'structure', 'relationship', 'system', 'emergence', 'complexity'],
        'activation_threshold': 0.5,
        'propagation_speed': 0.8
    },
    'temporal': {
        'color': (255, 152, 0),  # Orange
        'description': 'Time-related and process concepts',
        'examples': ['change', 'rhythm', 'sequence', 'cycle', 'evolution', 'duration', 'moment'],
        'activation_threshold': 0.3,
        'propagation_speed': 0.9
    },
    'spatial': {
        'color': (76, 175, 80),  # Green
        'description': 'Spatial and geometric concepts',
        'examples': ['boundary', 'center', 'direction', 'dimension', 'distance', 'position'],
        'activation_threshold': 0.3,
        'propagation_speed': 1.0
    },
    'meta': {
        'color': (96, 125, 139),  # Blue-grey
        'description': 'Meta-cognitive and self-referential concepts',
        'examples': ['awareness', 'thought', 'meaning', 'understanding', 'consciousness', 'cognition'],
        'activation_threshold': 0.6,
        'propagation_speed': 0.7
    },
    'relational': {
        'color': (255, 87, 34),  # Deep orange
        'description': 'Relationship and connection concepts',
        'examples': ['similarity', 'contrast', 'causation', 'correlation', 'influence', 'connection'],
        'activation_threshold': 0.4,
        'propagation_speed': 1.1
    }
}

# Category flow compatibility matrix
CATEGORY_FLOW_RATES = {
    'perceptual': {'emotional': 0.9, 'abstract': 0.7, 'spatial': 0.8, 'temporal': 0.6},
    'emotional': {'perceptual': 0.9, 'abstract': 0.8, 'meta': 0.7, 'relational': 0.8},
    'abstract': {'meta': 0.9, 'relational': 0.8, 'emotional': 0.7, 'temporal': 0.7},
    'temporal': {'spatial': 0.8, 'abstract': 0.7, 'perceptual': 0.6, 'meta': 0.6},
    'spatial': {'temporal': 0.8, 'perceptual': 0.8, 'abstract': 0.6, 'relational': 0.7},
    'meta': {'abstract': 0.9, 'emotional': 0.7, 'relational': 0.8, 'temporal': 0.6},
    'relational': {'abstract': 0.8, 'meta': 0.8, 'emotional': 0.8, 'spatial': 0.7}
}

@dataclass
class FlowParticle:
    """Represents a meaning flow particle traveling along edges"""
    source_id: str
    target_id: str
    position: float = 0.0  # 0 to 1 along edge
    speed: float = 1.0
    strength: float = 1.0
    color: Tuple[int, int, int] = (255, 255, 255)
    trail: List[Tuple[float, float]] = field(default_factory=list)

@dataclass
class SemanticConcept:
    """Represents a semantic concept node in the network"""
    id: str
    category: str
    content: str
    activation_level: float = 0.0
    base_activation: float = 0.1
    
    # Semantic relationships
    semantic_neighbors: Dict[str, float] = field(default_factory=dict)
    meaning_context: Dict[str, float] = field(default_factory=dict)
    
    # Network properties
    centrality_score: float = 0.0
    cluster_membership: Optional[int] = None
    semantic_weight: float = 1.0
    
    # Flow dynamics
    incoming_flow: float = 0.0
    outgoing_flow: float = 0.0
    flow_history: deque = field(default_factory=lambda: deque(maxlen=50))
    
    # Visual properties
    x: float = 0.0
    y: float = 0.0
    vx: float = 0.0
    vy: float = 0.0
    fx: float = 0.0
    fy: float = 0.0
    size: float = 10.0
    glow_intensity: float = 0.0
    pulse: float = 0.0

@dataclass
class SemanticCluster:
    """Represents a semantic neighborhood"""
    id: int
    center_concept: str
    members: List[str]
    coherence: float
    category: str
    boundary_points: List[Tuple[float, float]] = field(default_factory=list)
    color: Tuple[int, int, int] = field(default_factory=tuple)
    pulse: float = 0.0

class SemanticFlowNetwork:
    """Manages the semantic flow network and dynamics"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        
        # Network physics
        self.repulsion_strength = 3000
        self.attraction_strength = 0.001
        self.semantic_attraction = 0.01
        self.damping = 0.9
        
        # Concept tracking
        self.concepts: Dict[str, SemanticConcept] = {}
        self.active_concepts: Set[str] = set()
        
        # Flow tracking
        self.flow_particles: List[FlowParticle] = []
        self.flow_streams: List[Dict] = []
        
        # Clustering
        self.clusters: List[SemanticCluster] = []
        self.cluster_counter = 0
        
        # Emergence tracking
        self.emergence_events: List[Dict] = []
        self.coherence_history = deque(maxlen=100)
        
        # Initialize semantic network
        self._initialize_semantic_network()
    
    def _initialize_semantic_network(self):
        """Create initial semantic concept network"""
        # Create concepts from category examples
        for category, info in SEMANTIC_CATEGORIES.items():
            for i, example in enumerate(info['examples']):
                concept = SemanticConcept(
                    id=example,
                    category=category,
                    content=example
                )
                
                # Initial positioning in category regions
                angle = (i / len(info['examples'])) * 2 * math.pi
                radius = 200 + random.uniform(-50, 50)
                category_angle = list(SEMANTIC_CATEGORIES.keys()).index(category) * 2 * math.pi / len(SEMANTIC_CATEGORIES)
                
                concept.x = self.center_x + radius * math.cos(angle + category_angle)
                concept.y = self.center_y + radius * math.sin(angle + category_angle)
                
                self.concepts[example] = concept
        
        # Create semantic relationships
        self._create_semantic_relationships()
    
    def _create_semantic_relationships(self):
        """Establish semantic relationships between concepts"""
        # Within-category connections
        for category, info in SEMANTIC_CATEGORIES.items():
            category_concepts = [c for c in self.concepts.values() if c.category == category]
            
            for i, concept1 in enumerate(category_concepts):
                for concept2 in category_concepts[i+1:]:
                    # Strong within-category connections
                    strength = random.uniform(0.6, 0.9)
                    concept1.semantic_neighbors[concept2.id] = strength
                    concept2.semantic_neighbors[concept1.id] = strength
        
        # Cross-category connections based on semantic similarity
        cross_connections = [
            ('pattern', 'structure', 0.8),
            ('change', 'evolution', 0.9),
            ('joy', 'flow', 0.7),
            ('awareness', 'consciousness', 0.9),
            ('boundary', 'dimension', 0.6),
            ('similarity', 'relationship', 0.8),
            ('rhythm', 'pattern', 0.7),
            ('color', 'brightness', 0.8),
            ('thought', 'meaning', 0.8),
            ('tension', 'change', 0.6)
        ]
        
        for concept1_id, concept2_id, strength in cross_connections:
            if concept1_id in self.concepts and concept2_id in self.concepts:
                self.concepts[concept1_id].semantic_neighbors[concept2_id] = strength
                self.concepts[concept2_id].semantic_neighbors[concept1_id] = strength
    
    def activate_concepts(self, activated_concepts: Dict[str, float]):
        """Activate semantic concepts based on DAWN state"""
        for concept_id, activation in activated_concepts.items():
            if concept_id in self.concepts:
                concept = self.concepts[concept_id]
                concept.activation_level = min(1.0, concept.activation_level + activation)
                concept.pulse = 1.0
                self.active_concepts.add(concept_id)
                
                # Create flow to neighbors
                self._propagate_activation(concept)
    
    def _propagate_activation(self, source_concept: SemanticConcept):
        """Propagate activation to semantically related concepts"""
        for neighbor_id, relationship_strength in source_concept.semantic_neighbors.items():
            if neighbor_id in self.concepts:
                target_concept = self.concepts[neighbor_id]
                
                # Calculate flow strength
                flow_strength = self._calculate_semantic_flow(
                    source_concept, target_concept, relationship_strength
                )
                
                if flow_strength > 0.1:
                    # Add flow particle
                    particle = FlowParticle(
                        source_id=source_concept.id,
                        target_id=target_concept.id,
                        speed=SEMANTIC_CATEGORIES[source_concept.category]['propagation_speed'],
                        strength=flow_strength,
                        color=SEMANTIC_CATEGORIES[source_concept.category]['color']
                    )
                    self.flow_particles.append(particle)
                    
                    # Update target activation
                    target_concept.incoming_flow += flow_strength
    
    def _calculate_semantic_flow(self, source: SemanticConcept, target: SemanticConcept, 
                                relationship: float) -> float:
        """Calculate meaning flow between concepts"""
        # Base flow from source activation
        base_flow = source.activation_level * 0.4
        
        # Relationship modifier
        base_flow *= relationship
        
        # Category compatibility
        src_cat = source.category
        tgt_cat = target.category
        if src_cat == tgt_cat:
            compatibility = 1.0
        else:
            compatibility = CATEGORY_FLOW_RATES.get(src_cat, {}).get(tgt_cat, 0.5)
        base_flow *= compatibility
        
        # Saturation reduction (less flow to already active concepts)
        saturation = target.activation_level
        base_flow *= (1.0 - saturation * 0.5)
        
        return base_flow
    
    def update_physics(self, dt: float):
        """Update network physics and dynamics"""
        # Update forces
        self._update_forces()
        
        # Update concept positions
        for concept in self.concepts.values():
            # Apply forces with damping
            concept.vx = (concept.vx + concept.fx * dt) * self.damping
            concept.vy = (concept.vy + concept.fy * dt) * self.damping
            
            # Update position
            concept.x += concept.vx * dt
            concept.y += concept.vy * dt
            
            # Boundary constraints
            margin = 50
            if concept.x < margin:
                concept.vx = abs(concept.vx) * 0.5
                concept.x = margin
            elif concept.x > self.width - margin:
                concept.vx = -abs(concept.vx) * 0.5
                concept.x = self.width - margin
            
            if concept.y < margin:
                concept.vy = abs(concept.vy) * 0.5
                concept.y = margin
            elif concept.y > self.height - margin:
                concept.vy = -abs(concept.vy) * 0.5
                concept.y = self.height - margin
            
            # Update activation dynamics
            concept.activation_level *= 0.95  # Decay
            concept.activation_level += concept.incoming_flow * dt
            concept.activation_level = min(1.0, concept.activation_level)
            
            # Update visual properties
            concept.size = 10 + concept.activation_level * 20
            concept.glow_intensity = concept.activation_level
            concept.pulse = max(0, concept.pulse - dt * 2)
            
            # Record flow history
            concept.flow_history.append(concept.activation_level)
            
            # Reset flow accumulation
            concept.incoming_flow = 0
    
    def _update_forces(self):
        """Calculate forces for network layout"""
        # Reset forces
        for concept in self.concepts.values():
            concept.fx = 0
            concept.fy = 0
            
            # Weak center attraction
            dx = self.center_x - concept.x
            dy = self.center_y - concept.y
            dist = math.sqrt(dx*dx + dy*dy) + 1
            concept.fx += dx * 0.0001
            concept.fy += dy * 0.0001
        
        # Repulsion between all concepts
        concepts_list = list(self.concepts.values())
        for i, concept1 in enumerate(concepts_list):
            for concept2 in concepts_list[i+1:]:
                dx = concept1.x - concept2.x
                dy = concept1.y - concept2.y
                distance = math.sqrt(dx*dx + dy*dy) + 0.1
                
                if distance < 150:  # Repulsion radius
                    force = self.repulsion_strength / (distance * distance)
                    fx = force * dx / distance
                    fy = force * dy / distance
                    
                    concept1.fx += fx
                    concept1.fy += fy
                    concept2.fx -= fx
                    concept2.fy -= fy
        
        # Semantic attraction
        for concept in self.concepts.values():
            for neighbor_id, strength in concept.semantic_neighbors.items():
                if neighbor_id in self.concepts:
                    neighbor = self.concepts[neighbor_id]
                    dx = neighbor.x - concept.x
                    dy = neighbor.y - concept.y
                    distance = math.sqrt(dx*dx + dy*dy) + 1
                    
                    # Optimal distance based on relationship strength
                    optimal_dist = 100 + (1 - strength) * 100
                    
                    if distance > optimal_dist * 0.5:
                        force = self.semantic_attraction * strength * (distance - optimal_dist)
                        concept.fx += force * dx / distance
                        concept.fy += force * dy / distance
    
    def update_flow_particles(self, dt: float):
        """Update flow particle positions"""
        to_remove = []
        
        for i, particle in enumerate(self.flow_particles):
            # Move particle along edge
            particle.position += particle.speed * dt
            
            if particle.position >= 1.0:
                # Particle reached target
                if particle.target_id in self.concepts:
                    target = self.concepts[particle.target_id]
                    target.incoming_flow += particle.strength * 0.5
                to_remove.append(i)
            else:
                # Update particle trail
                if particle.source_id in self.concepts and particle.target_id in self.concepts:
                    source = self.concepts[particle.source_id]
                    target = self.concepts[particle.target_id]
                    
                    # Interpolate position
                    x = source.x + (target.x - source.x) * particle.position
                    y = source.y + (target.y - source.y) * particle.position
                    
                    particle.trail.append((x, y))
                    if len(particle.trail) > 10:
                        particle.trail.pop(0)
        
        # Remove completed particles
        for i in reversed(to_remove):
            self.flow_particles.pop(i)
    
    def detect_clusters(self):
        """Detect semantic clusters in the network"""
        # Find active concepts above threshold
        active_concepts = [c for c in self.concepts.values() 
                          if c.activation_level > 0.3]
        
        if len(active_concepts) < 3:
            return
        
        # Clear existing clusters
        self.clusters.clear()
        for concept in self.concepts.values():
            concept.cluster_membership = None
        
        # Simple proximity-based clustering for active concepts
        visited = set()
        
        for concept in active_concepts:
            if concept.id in visited:
                continue
            
            # Find nearby active concepts
            cluster_members = [concept.id]
            visited.add(concept.id)
            
            for other in active_concepts:
                if other.id not in visited:
                    dx = concept.x - other.x
                    dy = concept.y - other.y
                    distance = math.sqrt(dx*dx + dy*dy)
                    
                    if distance < 150 and concept.id in other.semantic_neighbors:
                        cluster_members.append(other.id)
                        visited.add(other.id)
            
            if len(cluster_members) >= 2:
                # Calculate cluster coherence
                coherence = self._calculate_cluster_coherence(cluster_members)
                
                cluster = SemanticCluster(
                    id=self.cluster_counter,
                    center_concept=concept.id,
                    members=cluster_members,
                    coherence=coherence,
                    category=concept.category,
                    color=SEMANTIC_CATEGORIES[concept.category]['color']
                )
                
                self.cluster_counter += 1
                self.clusters.append(cluster)
                
                # Assign cluster membership
                for member_id in cluster_members:
                    self.concepts[member_id].cluster_membership = cluster.id
    
    def _calculate_cluster_coherence(self, member_ids: List[str]) -> float:
        """Calculate semantic coherence within a cluster"""
        if len(member_ids) < 2:
            return 0.0
        
        members = [self.concepts[mid] for mid in member_ids if mid in self.concepts]
        
        # Activation synchrony
        activations = [m.activation_level for m in members]
        if np.mean(activations) > 0:
            activation_coherence = 1.0 - (np.std(activations) / np.mean(activations))
        else:
            activation_coherence = 0.0
        
        # Semantic connectivity
        connection_count = 0
        possible_connections = len(members) * (len(members) - 1) / 2
        
        for i, member1 in enumerate(members):
            for member2 in members[i+1:]:
                if member2.id in member1.semantic_neighbors:
                    connection_count += 1
        
        connectivity = connection_count / possible_connections if possible_connections > 0 else 0
        
        # Category consistency
        categories = [m.category for m in members]
        category_counts = {}
        for cat in categories:
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        dominant_category_ratio = max(category_counts.values()) / len(members)
        
        # Combined coherence
        coherence = (activation_coherence * 0.4 + 
                    connectivity * 0.4 + 
                    dominant_category_ratio * 0.2)
        
        return coherence
    
    def detect_emergence(self):
        """Detect emergent semantic patterns"""
        current_coherence = self._calculate_global_coherence()
        self.coherence_history.append(current_coherence)
        
        if len(self.coherence_history) > 10:
            # Check for coherence surge
            recent_avg = np.mean(list(self.coherence_history)[-5:])
            older_avg = np.mean(list(self.coherence_history)[-10:-5])
            
            if recent_avg > older_avg * 1.3:  # 30% increase
                self.emergence_events.append({
                    'type': 'coherence_surge',
                    'timestamp': time.time(),
                    'strength': recent_avg - older_avg,
                    'clusters': [c.id for c in self.clusters]
                })
        
        # Check for novel connections
        for concept in self.concepts.values():
            if concept.activation_level > 0.7:
                for neighbor_id in concept.semantic_neighbors:
                    neighbor = self.concepts.get(neighbor_id)
                    if neighbor and neighbor.activation_level > 0.7:
                        # Check if this is a cross-category emergence
                        if concept.category != neighbor.category:
                            self.emergence_events.append({
                                'type': 'cross_category_bridge',
                                'timestamp': time.time(),
                                'concepts': [concept.id, neighbor_id],
                                'categories': [concept.category, neighbor.category]
                            })
    
    def _calculate_global_coherence(self) -> float:
        """Calculate overall semantic coherence"""
        if not self.clusters:
            return 0.0
        
        # Average cluster coherence
        cluster_coherences = [c.coherence for c in self.clusters]
        avg_coherence = np.mean(cluster_coherences) if cluster_coherences else 0.0
        
        # Network connectivity
        active_count = sum(1 for c in self.concepts.values() if c.activation_level > 0.3)
        connectivity = active_count / len(self.concepts) if self.concepts else 0.0
        
        return avg_coherence * 0.7 + connectivity * 0.3
    
    def get_analytics(self) -> Dict:
        """Calculate network analytics"""
        active_concepts = [c for c in self.concepts.values() if c.activation_level > 0.1]
        
        # Category distribution
        category_dist = {}
        for concept in active_concepts:
            category_dist[concept.category] = category_dist.get(concept.category, 0) + 1
        
        # Flow statistics
        total_flow = sum(len(p.trail) for p in self.flow_particles)
        
        return {
            'active_concepts': len(active_concepts),
            'total_concepts': len(self.concepts),
            'flow_particles': len(self.flow_particles),
            'total_flow': total_flow,
            'clusters': len(self.clusters),
            'global_coherence': self._calculate_global_coherence(),
            'emergence_events': len(self.emergence_events),
            'dominant_category': max(category_dist.items(), key=lambda x: x[1])[0] if category_dist else 'none',
            'category_distribution': category_dist
        }

class SemanticFlowVisualization:
    """Handles the visual rendering of the semantic flow network"""
    
    def __init__(self, width: int = 1600, height: int = 900):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("DAWN Visualization #11: Semantic Flow Graph")
        
        self.clock = pygame.time.Clock()
        self.font_tiny = pygame.font.Font(None, 12)
        self.font_small = pygame.font.Font(None, 16)
        self.font_medium = pygame.font.Font(None, 20)
        self.font_large = pygame.font.Font(None, 28)
        
        # Colors
        self.bg_color = (10, 10, 15)
        self.grid_color = (25, 25, 35)
        self.text_color = (200, 200, 210)
        self.edge_color = (60, 60, 80)
        
        # Network
        self.network = SemanticFlowNetwork(width - 350, height)
        
        # Visualization settings
        self.show_labels = True
        self.show_flow = True
        self.show_clusters = True
        self.emergence_detection = True
        self.selected_concept = None
        
        # Animation state
        self.time = 0
        self.frame_count = 0
        
        # Visual effects
        self.emergence_pulses = []
    
    def detect_semantic_activation(self, json_data: dict) -> Dict[str, float]:
        """Analyze DAWN state to detect active semantic concepts"""
        mood = json_data.get('mood', {})
        entropy = json_data.get('entropy', 0.5)
        heat = json_data.get('heat', 0.3)
        scup = json_data.get('scup', {})
        
        activated_concepts = {}
        
        # Emotional concepts from mood
        mood_vector = mood.get('vector', [0.5] * 8)
        if len(mood_vector) >= 4:
            emotional_intensity = np.std(mood_vector)
            if emotional_intensity > 0.2:
                activated_concepts['joy'] = emotional_intensity * mood_vector[0]
                activated_concepts['curiosity'] = emotional_intensity * mood_vector[1]
                activated_concepts['tension'] = emotional_intensity * (1 - mood_vector[2])
                activated_concepts['flow'] = emotional_intensity * mood_vector[3]
                activated_concepts['excitement'] = emotional_intensity * np.mean(mood_vector[:2])
        
        # Abstract concepts from coherence
        coherence = scup.get('coherence', 0.5)
        if coherence > 0.6:
            activated_concepts['pattern'] = coherence * entropy
            activated_concepts['structure'] = coherence * scup.get('schema', 0.5)
            activated_concepts['system'] = coherence * 0.8
            activated_concepts['emergence'] = coherence * entropy * heat
            activated_concepts['relationship'] = coherence * 0.6
        
        # Temporal concepts from processing
        if heat > 0.6:
            activated_concepts['change'] = heat * entropy
            activated_concepts['rhythm'] = heat * (1 - abs(entropy - 0.5))
            activated_concepts['evolution'] = heat * 0.7
            activated_concepts['cycle'] = heat * (1 - coherence)
        
        # Spatial concepts from organization
        optimization = scup.get('optimization', 0.5)
        if optimization > 0.5:
            activated_concepts['boundary'] = optimization * (1 - entropy)
            activated_concepts['center'] = optimization * coherence
            activated_concepts['dimension'] = optimization * 0.6
        
        # Meta concepts from high-level processing
        meta_signal = np.mean([scup.get(k, 0.5) for k in scup.keys()]) if scup else 0.5
        if meta_signal > 0.7:
            activated_concepts['awareness'] = meta_signal * 0.9
            activated_concepts['thought'] = meta_signal * entropy
            activated_concepts['meaning'] = meta_signal * coherence
            activated_concepts['understanding'] = meta_signal * scup.get('utility', 0.5)
        
        # Perceptual concepts from sensory patterns
        if entropy > 0.4 and entropy < 0.7:
            activated_concepts['color'] = (1 - abs(entropy - 0.5)) * heat
            activated_concepts['pattern'] = entropy * 0.7
            activated_concepts['shape'] = (1 - entropy) * 0.6
        
        # Filter out low activations
        return {k: v for k, v in activated_concepts.items() if v > 0.2}
    
    def process_dawn_state(self, json_data: dict):
        """Process DAWN state and update network"""
        # Detect semantic activations
        activated_concepts = self.detect_semantic_activation(json_data)
        
        # Apply activations to network
        self.network.activate_concepts(activated_concepts)
        
        # Update clustering
        self.network.detect_clusters()
        
        # Check for emergence
        if self.emergence_detection:
            self.network.detect_emergence()
    
    def draw_semantic_edges(self):
        """Draw edges between semantically related concepts"""
        drawn_edges = set()
        
        for concept in self.network.concepts.values():
            for neighbor_id, strength in concept.semantic_neighbors.items():
                if neighbor_id in self.network.concepts:
                    # Avoid drawing edges twice
                    edge_key = tuple(sorted([concept.id, neighbor_id]))
                    if edge_key in drawn_edges:
                        continue
                    drawn_edges.add(edge_key)
                    
                    neighbor = self.network.concepts[neighbor_id]
                    
                    # Edge opacity based on activation
                    activation = (concept.activation_level + neighbor.activation_level) / 2
                    alpha = int(50 + activation * 150)
                    
                    # Edge width based on relationship strength
                    width = int(1 + strength * 2)
                    
                    # Draw edge
                    color = (*self.edge_color, alpha)
                    pygame.draw.line(self.screen, color[:3],
                                   (int(concept.x), int(concept.y)),
                                   (int(neighbor.x), int(neighbor.y)), width)
    
    def draw_clusters(self):
        """Draw semantic cluster regions"""
        for cluster in self.network.clusters:
            # Get member positions
            positions = []
            for member_id in cluster.members:
                if member_id in self.network.concepts:
                    concept = self.network.concepts[member_id]
                    positions.append((concept.x, concept.y))
            
            if len(positions) < 3:
                continue
            
            # Calculate convex hull (simplified - just use centroid and radius)
            cx = np.mean([p[0] for p in positions])
            cy = np.mean([p[1] for p in positions])
            
            max_dist = max(math.sqrt((p[0]-cx)**2 + (p[1]-cy)**2) for p in positions)
            radius = max_dist + 30
            
            # Draw cluster region
            alpha = int(cluster.coherence * 50)
            color = (*cluster.color, alpha)
            
            # Draw filled circle with low opacity
            if alpha > 10:
                for r in range(int(radius), 0, -5):
                    fade_alpha = int(alpha * (1 - r/radius))
                    pygame.gfxdraw.filled_circle(self.screen, int(cx), int(cy), r,
                                               (*cluster.color, fade_alpha))
    
    def draw_flow_particles(self):
        """Draw meaning flow particles"""
        for particle in self.network.flow_particles:
            if particle.source_id in self.network.concepts and particle.target_id in self.network.concepts:
                source = self.network.concepts[particle.source_id]
                target = self.network.concepts[particle.target_id]
                
                # Current position
                x = source.x + (target.x - source.x) * particle.position
                y = source.y + (target.y - source.y) * particle.position
                
                # Draw particle trail
                if len(particle.trail) > 1:
                    for i in range(len(particle.trail) - 1):
                        alpha = int(255 * (i / len(particle.trail)) * particle.strength)
                        pygame.draw.line(self.screen, (*particle.color, alpha),
                                       particle.trail[i], particle.trail[i+1], 2)
                
                # Draw particle
                radius = int(3 + particle.strength * 4)
                pygame.gfxdraw.filled_circle(self.screen, int(x), int(y), radius,
                                           (*particle.color, int(255 * particle.strength)))
    
    def draw_concept(self, concept: SemanticConcept):
        """Draw a semantic concept node"""
        x, y = int(concept.x), int(concept.y)
        
        # Get color from category
        base_color = SEMANTIC_CATEGORIES[concept.category]['color']
        
        # Adjust brightness based on activation
        brightness = 0.3 + concept.activation_level * 0.7
        color = tuple(int(c * brightness) for c in base_color)
        
        # Glow effect for active concepts
        if concept.activation_level > 0.1:
            glow_radius = concept.size * (1.5 + concept.pulse * 0.5)
            glow_alpha = int(concept.activation_level * 100)
            
            for i in range(3):
                pygame.gfxdraw.filled_circle(self.screen, x, y,
                                           int(glow_radius + i * 5),
                                           (*color, glow_alpha // (i + 1)))
        
        # Main concept circle
        pygame.gfxdraw.filled_circle(self.screen, x, y, int(concept.size), color)
        pygame.gfxdraw.aacircle(self.screen, x, y, int(concept.size), color)
        
        # Inner pattern based on category
        if concept.activation_level > 0.5:
            if concept.category == 'abstract':
                # Concentric circles
                for i in range(3):
                    r = int(concept.size * (0.7 - i * 0.2))
                    if r > 0:
                        pygame.gfxdraw.circle(self.screen, x, y, r, color)
            elif concept.category == 'temporal':
                # Clock-like lines
                for angle in range(0, 360, 60):
                    rad = math.radians(angle)
                    x2 = x + math.cos(rad) * concept.size * 0.7
                    y2 = y + math.sin(rad) * concept.size * 0.7
                    pygame.draw.line(self.screen, color, (x, y), (int(x2), int(y2)), 1)
        
        # Label
        if self.show_labels and concept.activation_level > 0.2:
            label = self.font_tiny.render(concept.content, True, self.text_color)
            label_rect = label.get_rect(center=(x, y + concept.size + 10))
            self.screen.blit(label, label_rect)
    
    def draw_ui(self):
        """Draw the UI panel"""
        # Panel background
        panel_rect = pygame.Rect(self.width - 330, 0, 330, self.height)
        pygame.draw.rect(self.screen, (20, 20, 25), panel_rect)
        pygame.draw.line(self.screen, (40, 40, 45),
                        (self.width - 330, 0), (self.width - 330, self.height), 2)
        
        y_offset = 20
        
        # Title
        title = self.font_large.render("Semantic Flow Network", True, self.text_color)
        self.screen.blit(title, (self.width - 310, y_offset))
        y_offset += 40
        
        # Analytics
        analytics = self.network.get_analytics()
        
        # Metrics
        metrics_text = [
            f"Active Concepts: {analytics['active_concepts']}/{analytics['total_concepts']}",
            f"Flow Particles: {analytics['flow_particles']}",
            f"Semantic Clusters: {analytics['clusters']}",
            f"Global Coherence: {analytics['global_coherence']:.2f}",
            f"Emergence Events: {analytics['emergence_events']}"
        ]
        
        for text in metrics_text:
            rendered = self.font_medium.render(text, True, (180, 180, 190))
            self.screen.blit(rendered, (self.width - 310, y_offset))
            y_offset += 25
        
        y_offset += 15
        
        # Category legend
        legend_title = self.font_medium.render("Semantic Categories", True, self.text_color)
        self.screen.blit(legend_title, (self.width - 310, y_offset))
        y_offset += 30
        
        for category, info in SEMANTIC_CATEGORIES.items():
            # Color indicator
            pygame.draw.circle(self.screen, info['color'],
                             (self.width - 300, y_offset + 8), 8)
            
            # Category name
            text = self.font_small.render(category.capitalize(), True, (180, 180, 190))
            self.screen.blit(text, (self.width - 280, y_offset))
            y_offset += 20
        
        y_offset += 20
        
        # Active category distribution
        if analytics['category_distribution']:
            dist_title = self.font_medium.render("Active Distribution", True, self.text_color)
            self.screen.blit(dist_title, (self.width - 310, y_offset))
            y_offset += 25
            
            for category, count in analytics['category_distribution'].items():
                # Bar chart
                bar_width = int(count / analytics['active_concepts'] * 200)
                bar_rect = pygame.Rect(self.width - 310, y_offset, bar_width, 15)
                pygame.draw.rect(self.screen, SEMANTIC_CATEGORIES[category]['color'], bar_rect)
                
                # Label
                label = self.font_tiny.render(f"{category}: {count}", True, (150, 150, 160))
                self.screen.blit(label, (self.width - 310 + bar_width + 5, y_offset))
                y_offset += 18
        
        # Controls
        y_offset = self.height - 100
        controls = [
            "L - Toggle labels",
            "F - Toggle flow particles", 
            "C - Toggle clusters",
            "E - Toggle emergence detection"
        ]
        
        for control in controls:
            text = self.font_small.render(control, True, (120, 120, 130))
            self.screen.blit(text, (self.width - 310, y_offset))
            y_offset += 20
    
    def draw_emergence_effects(self):
        """Draw visual effects for emergence events"""
        # Remove old events
        self.network.emergence_events = [e for e in self.network.emergence_events 
                                       if time.time() - e['timestamp'] < 3.0]
        
        for event in self.network.emergence_events:
            age = time.time() - event['timestamp']
            alpha = int(255 * (1 - age / 3.0))
            
            if event['type'] == 'coherence_surge':
                # Draw expanding rings from cluster centers
                for cluster_id in event.get('clusters', []):
                    cluster = next((c for c in self.network.clusters if c.id == cluster_id), None)
                    if cluster and cluster.center_concept in self.network.concepts:
                        center = self.network.concepts[cluster.center_concept]
                        radius = age * 100
                        pygame.gfxdraw.circle(self.screen, int(center.x), int(center.y),
                                            int(radius), (*self.text_color, alpha))
            
            elif event['type'] == 'cross_category_bridge':
                # Draw connection between concepts
                concept_ids = event.get('concepts', [])
                if len(concept_ids) == 2:
                    c1 = self.network.concepts.get(concept_ids[0])
                    c2 = self.network.concepts.get(concept_ids[1])
                    if c1 and c2:
                        pygame.draw.line(self.screen, (*self.text_color, alpha),
                                       (int(c1.x), int(c1.y)), (int(c2.x), int(c2.y)), 3)
    
    def update(self, dt: float):
        """Update visualization state"""
        self.time += dt
        self.frame_count += 1
        
        # Update network
        self.network.update_physics(dt)
        self.network.update_flow_particles(dt)
        
        # Periodic clustering update
        if self.frame_count % 30 == 0:
            self.network.detect_clusters()
    
    def draw(self):
        """Draw complete visualization"""
        self.screen.fill(self.bg_color)
        
        # Draw grid
        for x in range(0, self.width - 330, 50):
            pygame.draw.line(self.screen, self.grid_color,
                           (x, 0), (x, self.height), 1)
        for y in range(0, self.height, 50):
            pygame.draw.line(self.screen, self.grid_color,
                           (0, y), (self.width - 330, y), 1)
        
        # Draw clusters first (background)
        if self.show_clusters:
            self.draw_clusters()
        
        # Draw edges
        self.draw_semantic_edges()
        
        # Draw flow particles
        if self.show_flow:
            self.draw_flow_particles()
        
        # Draw concepts
        for concept in self.network.concepts.values():
            self.draw_concept(concept)
        
        # Draw emergence effects
        self.draw_emergence_effects()
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def handle_keypress(self, key):
        """Handle keyboard input"""
        if key == pygame.K_l:
            self.show_labels = not self.show_labels
        elif key == pygame.K_f:
            self.show_flow = not self.show_flow
        elif key == pygame.K_c:
            self.show_clusters = not self.show_clusters
        elif key == pygame.K_e:
            self.emergence_detection = not self.emergence_detection
    
    def run(self, data_source='demo'):
        """Main visualization loop"""
        running = True
        last_time = time.time()
        demo_timer = 0
        
        while running:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keypress(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        x, y = event.pos
                        # Find clicked concept
                        for concept in self.network.concepts.values():
                            dx = concept.x - x
                            dy = concept.y - y
                            if math.sqrt(dx*dx + dy*dy) <= concept.size:
                                self.selected_concept = concept.id
                                break
            
            # Process data
            if data_source == 'demo':
                demo_timer += dt
                if demo_timer > 0.3:  # Update every 0.3 seconds
                    demo_timer = 0
                    demo_data = self.generate_demo_data()
                    self.process_dawn_state(demo_data)
            else:
                # Read from stdin
                import select
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    line = sys.stdin.readline()
                    if line:
                        try:
                            json_data = json.loads(line.strip())
                            self.process_dawn_state(json_data)
                        except json.JSONDecodeError:
                            pass
            
            # Update and draw
            self.update(dt)
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
    
    def generate_demo_data(self) -> dict:
        """Generate demo DAWN data"""
        # Create interesting patterns
        t = self.time * 0.5
        
        # Oscillating patterns
        mood_vector = [
            0.5 + 0.3 * math.sin(t),
            0.5 + 0.3 * math.cos(t * 1.3),
            0.5 + 0.2 * math.sin(t * 0.7),
            0.5 + 0.25 * math.cos(t * 0.9),
            0.5 + 0.2 * math.sin(t * 1.1),
            0.5, 0.5, 0.5
        ]
        
        # Coherence waves
        coherence = 0.5 + 0.3 * math.sin(t * 0.4)
        
        return {
            'entropy': 0.5 + 0.3 * math.sin(t * 0.6),
            'heat': 0.4 + 0.4 * abs(math.sin(t * 0.8)),
            'mood': {
                'vector': mood_vector
            },
            'scup': {
                'coherence': coherence,
                'optimization': 0.5 + 0.3 * math.cos(t * 0.5),
                'utility': 0.5 + 0.2 * math.sin(t * 0.7),
                'schema': 0.5 + 0.25 * math.cos(t * 0.3)
            },
            'tick': self.frame_count
        }

def main():
    parser = argparse.ArgumentParser(
        description='DAWN Visualization #11: Semantic Flow Graph'
    )
    parser.add_argument('--source', choices=['stdin', 'demo'],
                       default='demo',
                       help='Data source (default: demo)')
    parser.add_argument('--width', type=int, default=1600,
                       help='Window width (default: 1600)')
    parser.add_argument('--height', type=int, default=900,
                       help='Window height (default: 900)')
    parser.add_argument('--emergence-detection', action='store_true',
                       help='Enable emergence detection')
    parser.add_argument('--cluster-analysis', action='store_true',
                       help='Enable cluster analysis')
    parser.add_argument('--flow-particles', action='store_true',
                       help='Show flow particles')
    
    args = parser.parse_args()
    
    # Create and run visualization
    viz = SemanticFlowVisualization(args.width, args.height)
    
    # Apply command line settings
    if args.emergence_detection:
        viz.emergence_detection = True
    if args.cluster_analysis:
        viz.show_clusters = True
    if args.flow_particles:
        viz.show_flow = True
    
    try:
        viz.run(data_source=args.source)
    except KeyboardInterrupt:
        print("\nVisualization terminated by user")
        sys.exit(0)

if __name__ == "__main__":
    main()