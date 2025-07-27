#!/usr/bin/env python3
"""
DAWN Backend Semantic Flow Graph Visualizer
Backend-compatible version for analytics and API integration.
"""

import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Set
import logging
from collections import deque, defaultdict
import random
import math
import signal
import atexit
import sys

# Import GIF saver

    from .gif_saver import setup_gif_saver
    from gif_saver import setup_gif_saver
import signal
import atexit

# Import GIF saver

    from .gif_saver import setup_gif_saver
    from gif_saver import setup_gif_saver

logger = logging.getLogger(__name__)

# Semantic concept categories (copied from visualizer)
SEMANTIC_CATEGORIES = {
    'perceptual': {
        'color': (0, 188, 212),
        'description': 'Sensory and perceptual concepts',
        'examples': ['color', 'sound', 'texture', 'movement', 'brightness', 'pattern', 'shape'],
        'activation_threshold': 0.3,
        'propagation_speed': 1.0
    },
    'emotional': {
        'color': (233, 30, 99),
        'description': 'Affective and emotional concepts',
        'examples': ['joy', 'curiosity', 'tension', 'flow', 'wonder', 'excitement', 'calm'],
        'activation_threshold': 0.4,
        'propagation_speed': 1.2
    },
    'abstract': {
        'color': (156, 39, 176),
        'description': 'Abstract and conceptual meanings',
        'examples': ['pattern', 'structure', 'relationship', 'system', 'emergence', 'complexity'],
        'activation_threshold': 0.5,
        'propagation_speed': 0.8
    },
    'temporal': {
        'color': (255, 152, 0),
        'description': 'Time-related and process concepts',
        'examples': ['change', 'rhythm', 'sequence', 'cycle', 'evolution', 'duration', 'moment'],
        'activation_threshold': 0.3,
        'propagation_speed': 0.9
    },
    'spatial': {
        'color': (76, 175, 80),
        'description': 'Spatial and geometric concepts',
        'examples': ['boundary', 'center', 'direction', 'dimension', 'distance', 'position'],
        'activation_threshold': 0.3,
        'propagation_speed': 1.0
    },
    'meta': {
        'color': (96, 125, 139),
        'description': 'Meta-cognitive and self-referential concepts',
        'examples': ['awareness', 'thought', 'meaning', 'understanding', 'consciousness', 'cognition'],
        'activation_threshold': 0.6,
        'propagation_speed': 0.7
    },
    'relational': {
        'color': (255, 87, 34),
        'description': 'Relationship and connection concepts',
        'examples': ['similarity', 'contrast', 'causation', 'correlation', 'influence', 'connection'],
        'activation_threshold': 0.4,
        'propagation_speed': 1.1
    }
}

class SemanticConcept:
    """Represents a semantic concept node"""
    def __init__(self, concept_id: str, category: str, content: str):
        self.id = concept_id
        self.category = category
        self.content = content
        self.activation_level = 0.0
        self.semantic_neighbors = {}
        self.flow_history = deque(maxlen=50)
        self.incoming_flow = 0.0
        self.outgoing_flow = 0.0

class SemanticCluster:
    """Represents a semantic neighborhood"""
    def __init__(self, cluster_id: int, center_concept: str, members: List[str], 
                 coherence: float, category: str):
        self.id = cluster_id
        self.center_concept = center_concept
        self.members = members
        self.coherence = coherence
        self.category = category

class SemanticFlowGraphBackend:
    """Backend analytics for the Semantic Flow Graph visualizer"""
    
    def __init__(self, max_concepts=100):
        self.max_concepts = max_concepts
        self.concepts: Dict[str, SemanticConcept] = {}
        self.active_concepts: Set[str] = set()
        self.clusters: List[SemanticCluster] = []
        self.flow_particles = []
        self.emergence_events = []
        self.coherence_history = deque(maxlen=100)
        self.current_tick = 0
        self.analytics_history = deque(maxlen=100)
        self._active = True
        self.cluster_counter = 0
        
        # Initialize semantic network
        self._initialize_semantic_network()
        logger.info("SemanticFlowGraphBackend initialized")

        # Setup GIF saver
        self.gif_saver = setup_gif_saver("semanticconcept")

        # Register cleanup function
        atexit.register(self.cleanup)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def _initialize_semantic_network(self):
        """Create initial semantic concept network"""
        # Create concepts from category examples
        for category, info in SEMANTIC_CATEGORIES.items():
            for example in info['examples']:
                concept = SemanticConcept(example, category, example)
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

    def activate_concepts(self, activated_concepts: Dict[str, float]):
        """Activate semantic concepts based on DAWN state"""
        for concept_id, activation in activated_concepts.items():
            if concept_id in self.concepts:
                concept = self.concepts[concept_id]
                concept.activation_level = min(1.0, concept.activation_level + activation)
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
                    self.flow_particles.append({
                        'source_id': source_concept.id,
                        'target_id': target_concept.id,
                        'strength': flow_strength,
                        'age': 0
                    })
                    
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
            # Simplified compatibility matrix
            compatibility = 0.7 if src_cat in ['emotional', 'abstract'] and tgt_cat in ['emotional', 'abstract'] else 0.5
        base_flow *= compatibility
        
        # Saturation reduction (less flow to already active concepts)
        saturation = target.activation_level
        base_flow *= (1.0 - saturation * 0.5)
        
        return base_flow

    def update_flow_particles(self):
        """Update flow particle positions and remove old ones"""
        to_remove = []
        
        for i, particle in enumerate(self.flow_particles):
            particle['age'] += 1
            
            if particle['age'] > 30:  # Particle lifetime
                to_remove.append(i)
            elif particle['target_id'] in self.concepts:
                target = self.concepts[particle['target_id']]
                target.incoming_flow += particle['strength'] * 0.1
        
        # Remove old particles
        for i in reversed(to_remove):
            self.flow_particles.pop(i)

    def detect_clusters(self):
        """Detect semantic clusters in the network"""
        # Find active concepts above threshold
        active_concepts = [c for c in self.concepts.values() 
                          if c.activation_level > 0.3]
        
        if len(active_concepts) < 2:
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
                    # Check semantic relationship
                    if concept.id in other.semantic_neighbors:
                        cluster_members.append(other.id)
                        visited.add(other.id)
            
            if len(cluster_members) >= 2:
                # Calculate cluster coherence
                coherence = self._calculate_cluster_coherence(cluster_members)
                
                cluster = SemanticCluster(
                    cluster_id=self.cluster_counter,
                    center_concept=concept.id,
                    members=cluster_members,
                    coherence=coherence,
                    category=concept.category
                )
                
                self.cluster_counter += 1
                self.clusters.append(cluster)

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
                    'timestamp': datetime.now().isoformat(),
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
                                'timestamp': datetime.now().isoformat(),
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

    def simulate_tick(self):
        """Simulate one tick of semantic flow dynamics"""
        self.current_tick += 1
        
        # Update concept activations
        for concept in self.concepts.values():
            # Decay activation
            concept.activation_level *= 0.95
            concept.activation_level += concept.incoming_flow
            concept.activation_level = min(1.0, concept.activation_level)
            
            # Record flow history
            concept.flow_history.append(concept.activation_level)
            
            # Reset flow accumulation
            concept.incoming_flow = 0
        
        # Update flow particles
        self.update_flow_particles()
        
        # Update clustering periodically
        if self.current_tick % 10 == 0:
            self.detect_clusters()
        
        # Check for emergence
        if self.current_tick % 5 == 0:
            self.detect_emergence()
        
        # Update analytics
        self.analytics_history.append(self.get_analytics())

    def get_analytics(self) -> Dict[str, Any]:
        """Calculate network analytics"""
        active_concepts = [c for c in self.concepts.values() if c.activation_level > 0.1]
        
        # Category distribution
        category_dist = {}
        for concept in active_concepts:
            category_dist[concept.category] = category_dist.get(concept.category, 0) + 1
        
        # Flow statistics
        total_flow = sum(len(p.get('trail', [])) for p in self.flow_particles)
        
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

    def get_visualization_data(self) -> Dict[str, Any]:
        """Get current visualization data for API/WebSocket transmission"""
        analytics = self.get_analytics()
        
        # Get active concepts data
        active_concepts_data = []
        for concept in self.concepts.values():
            if concept.activation_level > 0.1:
                active_concepts_data.append({
                    'id': concept.id,
                    'category': concept.category,
                    'content': concept.content,
                    'activation_level': concept.activation_level,
                    'semantic_neighbors': list(concept.semantic_neighbors.keys()),
                    'flow_history': list(concept.flow_history)[-10:]  # Last 10 values
                })
        
        # Get cluster data
        clusters_data = []
        for cluster in self.clusters:
            clusters_data.append({
                'id': cluster.id,
                'center_concept': cluster.center_concept,
                'members': cluster.members,
                'coherence': cluster.coherence,
                'category': cluster.category
            })
        
        # Get recent emergence events
        recent_emergence = self.emergence_events[-5:] if self.emergence_events else []
        
        return {
            'tick': self.current_tick,
            'analytics': analytics,
            'active_concepts': active_concepts_data,
            'clusters': clusters_data,
            'flow_particles': len(self.flow_particles),
            'emergence_events': recent_emergence,
            'timestamp': datetime.now().isoformat()
        }

    def is_active(self) -> bool:
        """Check if visualizer is active"""
        return self._active

    def start_animation(self) -> None:
        """Start the animation loop"""
        self._active = True
        logger.info("SemanticFlowGraphBackend animation started")

    def stop_animation(self) -> None:
        """Stop the animation"""
        self._active = False
        logger.info("SemanticFlowGraphBackend animation stopped")

    def update_visualization(self, data=None, tick=None) -> None:
        """Update the visualization with new data"""
        if data:
            # Detect semantic activations from DAWN state
            activated_concepts = self.detect_semantic_activation(data)
            self.activate_concepts(activated_concepts)
        
        # Simulate tick
        self.simulate_tick()

    def update_all_processes(self, all_process_data=None, tick=None) -> None:
        """Update visualization for all processes"""
        # For semantic flow, we use the main system state
        if all_process_data and 0 in all_process_data:
            main_data = all_process_data[0]
            self.update_visualization(main_data, tick)
        else:
            self.simulate_tick()

    def close(self) -> None:
        """Close the visualization"""
        self._active = False
        logger.info("SemanticFlowGraphBackend closed")

    async def shutdown(self) -> None:
        """Async shutdown"""
        self.close()

    async def tick(self, *args, **kwargs):
        self.simulate_tick()

    def save_animation_gif(self):
        """Save the animation as GIF"""

            if hasattr(self, 'animation'):
                gif_path = self.gif_saver.save_animation_as_gif(self.animation, fps=5, dpi=100)
                if gif_path:
                    print(f"\nAnimation GIF saved: {gif_path}", file=sys.stderr)
                else:
                    print("\nFailed to save animation GIF", file=sys.stderr)
            else:
                print("\nNo animation to save", file=sys.stderr)
            print(f"\nError saving animation GIF: {e}", file=sys.stderr)

    def cleanup(self):
        """Cleanup function to save GIF"""
        self.save_animation_gif()

    def signal_handler(self, signum, frame):
        """Signal handler to save GIF on termination"""
        print(f"\nReceived signal {signum}, saving GIF...", file=sys.stderr)
        self.save_animation_gif()
        sys.exit(0)

# Singleton accessor
_semantic_flow_graph = None

def get_semantic_flow_graph() -> SemanticFlowGraphBackend:
    """Get or create the global semantic flow graph instance"""
    global _semantic_flow_graph
    if _semantic_flow_graph is None:
        _semantic_flow_graph = SemanticFlowGraphBackend()
    return _semantic_flow_graph 