#!/usr/bin/env python3
"""
Bloom Manager - Fractal Memory System for DAWN Juliet Architecture
Manages rebloom chains, lineage tracking, and entropy evolution in cognitive blooms.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple, Any
from datetime import datetime, timedelta
import json
import uuid
import numpy as np
from collections import defaultdict, deque
import math


@dataclass
class Bloom:
    """
    Core bloom data structure representing a memory unit in the fractal system.
    Each bloom can spawn children with evolved entropy and semantic mutations.
    """
    id: str
    seed: str  # Semantic content/memory
    mood: Dict[str, float]  # Mood state at creation
    entropy: float  # Entropy level (0.0-1.0)
    parent_id: Optional[str] = None
    depth: int = 0
    children: List[str] = field(default_factory=list)
    
    # Semantic and state attributes
    semantic_vector: List[float] = field(default_factory=lambda: [0.0] * 64)
    tags: Set[str] = field(default_factory=set)
    resonance: float = 1.0  # Memory strength (decays over time)
    heat: float = 0.5  # Processing intensity when created
    coherence: float = 0.7  # Internal consistency
    
    # Temporal tracking
    creation_time: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    
    # Fractal properties
    complexity: float = 0.5  # Structural complexity
    semantic_drift: float = 0.0  # Cumulative drift from root
    total_entropy_drift: float = 0.0  # Cumulative entropy change from root
    
    # State management
    is_active: bool = True
    dormancy_level: float = 0.0  # 0.0 = fully active, 1.0 = dormant
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert bloom to dictionary for serialization"""
        return {
            'id': self.id,
            'seed': self.seed,
            'mood': self.mood,
            'entropy': self.entropy,
            'parent_id': self.parent_id,
            'depth': self.depth,
            'children': self.children,
            'semantic_vector': self.semantic_vector,
            'tags': list(self.tags),
            'resonance': self.resonance,
            'heat': self.heat,
            'coherence': self.coherence,
            'creation_time': self.creation_time.isoformat(),
            'last_accessed': self.last_accessed.isoformat(),
            'access_count': self.access_count,
            'complexity': self.complexity,
            'semantic_drift': self.semantic_drift,
            'total_entropy_drift': self.total_entropy_drift,
            'is_active': self.is_active,
            'dormancy_level': self.dormancy_level
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Bloom':
        """Create bloom from dictionary"""
        bloom = cls(
            id=data['id'],
            seed=data['seed'],
            mood=data['mood'],
            entropy=data['entropy'],
            parent_id=data.get('parent_id'),
            depth=data.get('depth', 0),
            children=data.get('children', []),
            semantic_vector=data.get('semantic_vector', [0.0] * 64),
            resonance=data.get('resonance', 1.0),
            heat=data.get('heat', 0.5),
            coherence=data.get('coherence', 0.7),
            complexity=data.get('complexity', 0.5),
            semantic_drift=data.get('semantic_drift', 0.0),
            total_entropy_drift=data.get('total_entropy_drift', 0.0),
            is_active=data.get('is_active', True),
            dormancy_level=data.get('dormancy_level', 0.0),
            access_count=data.get('access_count', 0)
        )
        
        bloom.tags = set(data.get('tags', []))
        
        # Parse timestamps
        if 'creation_time' in data:
            bloom.creation_time = datetime.fromisoformat(data['creation_time'])
        if 'last_accessed' in data:
            bloom.last_accessed = datetime.fromisoformat(data['last_accessed'])
            
        return bloom


@dataclass
class RebloomEvent:
    """Records a rebloom event for lineage tracking"""
    parent_id: str
    child_id: str
    entropy_diff: float
    semantic_mutation: float
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'parent_id': self.parent_id,
            'child_id': self.child_id,
            'entropy_diff': self.entropy_diff,
            'semantic_mutation': self.semantic_mutation,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }


class BloomManager:
    """
    Manages the fractal memory system with lineage tracking and entropy evolution.
    
    Features:
    - Create root blooms and spawn children through reblooming
    - Track lineage and ancestry chains
    - Manage entropy evolution across generations
    - Handle semantic mutations and drift
    - Maintain resonance and memory decay
    - Provide search and visualization capabilities
    """
    
    def __init__(self, 
                 entropy_decay: float = 0.9,
                 resonance_decay: float = 0.05,
                 max_capacity: int = 10000,
                 semantic_mutation_rate: float = 0.1):
        """
        Initialize the bloom manager.
        
        Args:
            entropy_decay: Factor for entropy inheritance (0.0-1.0)
            resonance_decay: Daily resonance decay rate
            max_capacity: Maximum number of blooms before pruning
            semantic_mutation_rate: Rate of semantic evolution during rebloom
        """
        # Core storage
        self.blooms: Dict[str, Bloom] = {}
        self.rebloom_events: List[RebloomEvent] = []
        
        # Indexes for efficient queries
        self.roots: Set[str] = set()  # Blooms with no parent
        self.depth_index: Dict[int, List[str]] = defaultdict(list)
        self.tag_index: Dict[str, Set[str]] = defaultdict(set)
        self.parent_to_children: Dict[str, List[str]] = defaultdict(list)
        
        # Configuration
        self.entropy_decay = entropy_decay
        self.resonance_decay = resonance_decay
        self.max_capacity = max_capacity
        self.semantic_mutation_rate = semantic_mutation_rate
        
        # Statistics
        self.stats = {
            'total_blooms_created': 0,
            'total_reblooms': 0,
            'max_depth_observed': 0,
            'active_bloom_count': 0,
            'dormant_bloom_count': 0,
            'average_lineage_length': 0.0,
            'entropy_variance': 0.0
        }
        
        # Time tracking for decay calculations
        self.last_decay_update = datetime.now()
    
    def create_bloom(self, 
                    seed: str, 
                    mood: Dict[str, float], 
                    entropy: float,
                    tags: Optional[Set[str]] = None,
                    heat: float = 0.5,
                    coherence: float = 0.7) -> Bloom:
        """
        Create a new root bloom with no parent.
        
        Args:
            seed: Semantic content of the bloom
            mood: Mood state dictionary
            entropy: Initial entropy level (0.0-1.0)
            tags: Optional semantic tags
            heat: Processing intensity
            coherence: Internal consistency
            
        Returns:
            Created Bloom object
        """
        bloom_id = str(uuid.uuid4())
        
        # Generate semantic vector from seed
        semantic_vector = self._generate_semantic_vector(seed)
        
        # Create bloom
        bloom = Bloom(
            id=bloom_id,
            seed=seed,
            mood=mood.copy(),
            entropy=max(0.0, min(1.0, entropy)),
            depth=0,
            semantic_vector=semantic_vector,
            tags=tags or set(),
            heat=heat,
            coherence=coherence
        )
        
        # Store and index
        self.blooms[bloom_id] = bloom
        self.roots.add(bloom_id)
        self.depth_index[0].append(bloom_id)
        
        # Update tag index
        for tag in bloom.tags:
            self.tag_index[tag].add(bloom_id)
        
        # Update statistics
        self.stats['total_blooms_created'] += 1
        self.stats['active_bloom_count'] += 1
        
        # Check capacity and prune if needed
        self._check_capacity()
        
        return bloom
    
    def rebloom(self, 
               parent_bloom_id: str, 
               delta_entropy: float,
               seed_mutation: Optional[str] = None,
               mood_shift: Optional[Dict[str, float]] = None) -> Optional[Bloom]:
        """
        Spawn a child bloom from a parent with entropy evolution.
        
        Args:
            parent_bloom_id: ID of the parent bloom
            delta_entropy: Entropy change for the child
            seed_mutation: Optional new semantic content (mutates from parent if None)
            mood_shift: Optional mood changes from parent
            
        Returns:
            Created child Bloom object or None if parent not found
        """
        if parent_bloom_id not in self.blooms:
            return None
        
        parent = self.blooms[parent_bloom_id]
        
        # Calculate child properties
        child_id = str(uuid.uuid4())
        child_depth = parent.depth + 1
        
        # Entropy evolution with decay
        child_entropy = (parent.entropy * self.entropy_decay) + delta_entropy
        child_entropy = max(0.0, min(1.0, child_entropy))
        
        # Semantic mutation
        if seed_mutation is None:
            child_seed = self._mutate_seed(parent.seed, self.semantic_mutation_rate)
            semantic_mutation = self.semantic_mutation_rate
        else:
            child_seed = seed_mutation
            semantic_mutation = self._calculate_semantic_distance(parent.seed, child_seed)
        
        # Mood evolution
        child_mood = parent.mood.copy()
        if mood_shift:
            for key, shift in mood_shift.items():
                child_mood[key] = child_mood.get(key, 0.0) + shift
                child_mood[key] = max(0.0, min(1.0, child_mood[key]))
        
        # Semantic drift calculation
        total_semantic_drift = parent.semantic_drift + semantic_mutation
        total_entropy_drift = parent.total_entropy_drift + delta_entropy
        
        # Generate child semantic vector
        child_semantic_vector = self._evolve_semantic_vector(
            parent.semantic_vector, semantic_mutation
        )
        
        # Inherit and evolve tags
        child_tags = parent.tags.copy()
        if len(child_tags) > 0 and np.random.random() < 0.3:
            # 30% chance to add a mutation tag
            child_tags.add(f"gen{child_depth}")
        
        # Create child bloom
        child = Bloom(
            id=child_id,
            seed=child_seed,
            mood=child_mood,
            entropy=child_entropy,
            parent_id=parent_bloom_id,
            depth=child_depth,
            semantic_vector=child_semantic_vector,
            tags=child_tags,
            heat=parent.heat * 0.95,  # Slight heat decay
            coherence=parent.coherence * 0.98,  # Slight coherence decay
            complexity=parent.complexity + semantic_mutation * 0.5,
            semantic_drift=total_semantic_drift,
            total_entropy_drift=total_entropy_drift
        )
        
        # Update parent-child relationships
        parent.children.append(child_id)
        
        # Store and index child
        self.blooms[child_id] = child
        self.depth_index[child_depth].append(child_id)
        self.parent_to_children[parent_bloom_id].append(child_id)
        
        # Update tag index
        for tag in child.tags:
            self.tag_index[tag].add(child_id)
        
        # Log rebloom event
        event = RebloomEvent(
            parent_id=parent_bloom_id,
            child_id=child_id,
            entropy_diff=delta_entropy,
            semantic_mutation=semantic_mutation,
            metadata={
                'child_depth': child_depth,
                'total_entropy_drift': total_entropy_drift,
                'semantic_drift': total_semantic_drift
            }
        )
        self.rebloom_events.append(event)
        
        # Update statistics
        self.stats['total_reblooms'] += 1
        self.stats['total_blooms_created'] += 1
        self.stats['active_bloom_count'] += 1
        self.stats['max_depth_observed'] = max(self.stats['max_depth_observed'], child_depth)
        
        # Access parent (reinforces memory)
        self._access_bloom(parent_bloom_id)
        
        # Check capacity
        self._check_capacity()
        
        return child
    
    def get_lineage(self, bloom_id: str) -> List[Bloom]:
        """
        Get the full ancestry chain from root to the specified bloom.
        
        Args:
            bloom_id: ID of the bloom
            
        Returns:
            List of Bloom objects from root to target (inclusive)
        """
        if bloom_id not in self.blooms:
            return []
        
        lineage = []
        current_id = bloom_id
        
        # Traverse up to root
        while current_id is not None:
            if current_id not in self.blooms:
                break
            
            bloom = self.blooms[current_id]
            lineage.insert(0, bloom)  # Insert at beginning for root-to-target order
            current_id = bloom.parent_id
        
        # Access all blooms in lineage (reinforces memory path)
        for bloom in lineage:
            self._access_bloom(bloom.id)
        
        return lineage
    
    def get_entropy_trend(self, bloom_id: str) -> List[Tuple[int, float]]:
        """
        Get entropy evolution across generations for a bloom's lineage.
        
        Args:
            bloom_id: ID of the bloom
            
        Returns:
            List of (depth, entropy) tuples from root to target
        """
        lineage = self.get_lineage(bloom_id)
        return [(bloom.depth, bloom.entropy) for bloom in lineage]
    
    def get_bloom_tree(self, root_id: str, max_depth: Optional[int] = None) -> Dict[str, Any]:
        """
        Get hierarchical tree structure starting from a root bloom.
        
        Args:
            root_id: ID of the root bloom
            max_depth: Optional maximum depth to traverse
            
        Returns:
            Nested dictionary representing the bloom tree
        """
        if root_id not in self.blooms:
            return {}
        
        def build_tree(bloom_id: str, current_depth: int = 0) -> Dict[str, Any]:
            if max_depth is not None and current_depth > max_depth:
                return {}
            
            bloom = self.blooms[bloom_id]
            tree_node = {
                'bloom': bloom.to_dict(),
                'children': {}
            }
            
            for child_id in bloom.children:
                if child_id in self.blooms:
                    tree_node['children'][child_id] = build_tree(child_id, current_depth + 1)
            
            return tree_node
        
        return build_tree(root_id)
    
    def find_resonant_blooms(self, 
                            query_seed: str, 
                            threshold: float = 0.7,
                            include_dormant: bool = False) -> List[Tuple[Bloom, float]]:
        """
        Find blooms with semantic similarity to a query.
        
        Args:
            query_seed: Semantic content to search for
            threshold: Minimum similarity threshold (0.0-1.0)
            include_dormant: Whether to include dormant blooms
            
        Returns:
            List of (Bloom, similarity_score) tuples sorted by similarity
        """
        query_vector = self._generate_semantic_vector(query_seed)
        results = []
        
        for bloom in self.blooms.values():
            if not include_dormant and not bloom.is_active:
                continue
            
            similarity = self._calculate_vector_similarity(query_vector, bloom.semantic_vector)
            if similarity >= threshold:
                results.append((bloom, similarity))
                # Access bloom (reinforces memory)
                self._access_bloom(bloom.id)
        
        # Sort by similarity (highest first)
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def prune_dormant_blooms(self, dormancy_threshold: float = 0.8) -> int:
        """
        Remove blooms that have become too dormant.
        
        Args:
            dormancy_threshold: Minimum dormancy level for pruning
            
        Returns:
            Number of blooms pruned
        """
        to_prune = []
        
        for bloom_id, bloom in self.blooms.items():
            if bloom.dormancy_level >= dormancy_threshold and bloom_id not in self.roots:
                to_prune.append(bloom_id)
        
        pruned_count = 0
        for bloom_id in to_prune:
            if self._remove_bloom(bloom_id):
                pruned_count += 1
        
        return pruned_count
    
    def update_resonance_decay(self) -> None:
        """Update resonance decay for all blooms based on time passage"""
        now = datetime.now()
        time_delta = now - self.last_decay_update
        decay_factor = self.resonance_decay * time_delta.total_seconds() / 86400  # Daily decay rate
        
        for bloom in self.blooms.values():
            # Decay resonance
            bloom.resonance = max(0.1, bloom.resonance - decay_factor)
            
            # Update dormancy based on resonance and last access
            days_since_access = (now - bloom.last_accessed).total_seconds() / 86400
            bloom.dormancy_level = min(1.0, days_since_access * 0.1 + (1.0 - bloom.resonance))
            
            # Mark as inactive if too dormant
            if bloom.dormancy_level > 0.9:
                bloom.is_active = False
                self.stats['active_bloom_count'] -= 1
                self.stats['dormant_bloom_count'] += 1
        
        self.last_decay_update = now
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the bloom system"""
        # Update dynamic statistics
        self._update_statistics()
        return self.stats.copy()
    
    def export_bloom_data(self, file_path: str) -> bool:
        """Export all bloom data to JSON file"""
        try:
            export_data = {
                'blooms': {bid: bloom.to_dict() for bid, bloom in self.blooms.items()},
                'rebloom_events': [event.to_dict() for event in self.rebloom_events],
                'roots': list(self.roots),
                'stats': self.stats,
                'config': {
                    'entropy_decay': self.entropy_decay,
                    'resonance_decay': self.resonance_decay,
                    'max_capacity': self.max_capacity,
                    'semantic_mutation_rate': self.semantic_mutation_rate
                },
                'export_timestamp': datetime.now().isoformat()
            }
            
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False
    
    def import_bloom_data(self, file_path: str) -> bool:
        """Import bloom data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                import_data = json.load(f)
            
            # Clear existing data
            self.blooms.clear()
            self.rebloom_events.clear()
            self.roots.clear()
            self._clear_indexes()
            
            # Import blooms
            for bloom_id, bloom_data in import_data['blooms'].items():
                bloom = Bloom.from_dict(bloom_data)
                self.blooms[bloom_id] = bloom
                
                if bloom.parent_id is None:
                    self.roots.add(bloom_id)
                
                # Rebuild indexes
                self.depth_index[bloom.depth].append(bloom_id)
                for tag in bloom.tags:
                    self.tag_index[tag].add(bloom_id)
                if bloom.parent_id:
                    self.parent_to_children[bloom.parent_id].append(bloom_id)
            
            # Import events
            for event_data in import_data['rebloom_events']:
                event = RebloomEvent(
                    parent_id=event_data['parent_id'],
                    child_id=event_data['child_id'],
                    entropy_diff=event_data['entropy_diff'],
                    semantic_mutation=event_data['semantic_mutation'],
                    metadata=event_data['metadata']
                )
                event.timestamp = datetime.fromisoformat(event_data['timestamp'])
                self.rebloom_events.append(event)
            
            # Import config if available
            if 'config' in import_data:
                config = import_data['config']
                self.entropy_decay = config.get('entropy_decay', self.entropy_decay)
                self.resonance_decay = config.get('resonance_decay', self.resonance_decay)
                self.max_capacity = config.get('max_capacity', self.max_capacity)
                self.semantic_mutation_rate = config.get('semantic_mutation_rate', self.semantic_mutation_rate)
            
            # Update statistics
            self._update_statistics()
            
            return True
        except Exception as e:
            print(f"Import failed: {e}")
            return False
    
    # Private helper methods
    
    def _generate_semantic_vector(self, seed: str) -> List[float]:
        """Generate a semantic vector from seed text (simple hash-based approach)"""
        # Simple hash-based semantic vector generation
        # In production, this could use proper embeddings (BERT, etc.)
        import hashlib
        
        # Create multiple hash values for vector components
        vector = []
        for i in range(64):
            hash_input = f"{seed}_{i}".encode()
            hash_value = int(hashlib.md5(hash_input).hexdigest()[:8], 16)
            # Normalize to [-1, 1] range
            vector.append((hash_value / 0xFFFFFFFF) * 2 - 1)
        
        return vector
    
    def _evolve_semantic_vector(self, parent_vector: List[float], mutation_rate: float) -> List[float]:
        """Evolve semantic vector with mutations"""
        child_vector = parent_vector.copy()
        
        for i in range(len(child_vector)):
            if np.random.random() < mutation_rate:
                # Add random mutation
                mutation = np.random.normal(0, 0.1)
                child_vector[i] = max(-1, min(1, child_vector[i] + mutation))
        
        return child_vector
    
    def _calculate_vector_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between vectors"""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(a * a for a in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def _mutate_seed(self, parent_seed: str, mutation_rate: float) -> str:
        """Apply semantic mutations to seed text"""
        if np.random.random() > mutation_rate:
            return parent_seed
        
        # Simple mutation: add variation prefix/suffix
        mutations = [
            f"evolved_{parent_seed}",
            f"{parent_seed}_variant",
            f"mutated_{parent_seed}",
            f"{parent_seed}_drift"
        ]
        
        return np.random.choice(mutations)
    
    def _calculate_semantic_distance(self, seed1: str, seed2: str) -> float:
        """Calculate semantic distance between two seeds"""
        if seed1 == seed2:
            return 0.0
        
        # Simple Levenshtein distance approximation
        len1, len2 = len(seed1), len(seed2)
        if len1 == 0 or len2 == 0:
            return 1.0
        
        # Normalize by length
        common_chars = sum(1 for c1, c2 in zip(seed1, seed2) if c1 == c2)
        return 1.0 - (common_chars / max(len1, len2))
    
    def _access_bloom(self, bloom_id: str) -> None:
        """Mark bloom as accessed (reinforces memory)"""
        if bloom_id in self.blooms:
            bloom = self.blooms[bloom_id]
            bloom.last_accessed = datetime.now()
            bloom.access_count += 1
            # Boost resonance slightly
            bloom.resonance = min(1.0, bloom.resonance + 0.01)
            # Reduce dormancy
            bloom.dormancy_level = max(0.0, bloom.dormancy_level - 0.1)
            if not bloom.is_active and bloom.dormancy_level < 0.5:
                bloom.is_active = True
                self.stats['active_bloom_count'] += 1
                self.stats['dormant_bloom_count'] -= 1
    
    def _remove_bloom(self, bloom_id: str) -> bool:
        """Remove a bloom and update all references"""
        if bloom_id not in self.blooms:
            return False
        
        bloom = self.blooms[bloom_id]
        
        # Remove from parent's children list
        if bloom.parent_id and bloom.parent_id in self.blooms:
            parent = self.blooms[bloom.parent_id]
            if bloom_id in parent.children:
                parent.children.remove(bloom_id)
        
        # Update children to be orphaned (or remove them too)
        for child_id in bloom.children:
            if child_id in self.blooms:
                self.blooms[child_id].parent_id = None
                self.roots.add(child_id)
        
        # Remove from indexes
        self.depth_index[bloom.depth].remove(bloom_id)
        for tag in bloom.tags:
            self.tag_index[tag].discard(bloom_id)
        if bloom.parent_id in self.parent_to_children:
            if bloom_id in self.parent_to_children[bloom.parent_id]:
                self.parent_to_children[bloom.parent_id].remove(bloom_id)
        
        # Remove from roots if applicable
        self.roots.discard(bloom_id)
        
        # Remove the bloom
        del self.blooms[bloom_id]
        
        # Update statistics
        if bloom.is_active:
            self.stats['active_bloom_count'] -= 1
        else:
            self.stats['dormant_bloom_count'] -= 1
        
        return True
    
    def _check_capacity(self) -> None:
        """Check if capacity limit is exceeded and prune if necessary"""
        if len(self.blooms) > self.max_capacity:
            # Prune dormant blooms first
            pruned = self.prune_dormant_blooms(0.5)
            
            # If still over capacity, prune least resonant active blooms
            if len(self.blooms) > self.max_capacity:
                active_blooms = [b for b in self.blooms.values() if b.is_active]
                active_blooms.sort(key=lambda x: x.resonance)
                
                to_remove = len(self.blooms) - self.max_capacity
                for i in range(min(to_remove, len(active_blooms) // 2)):
                    self._remove_bloom(active_blooms[i].id)
    
    def _clear_indexes(self) -> None:
        """Clear all indexes"""
        self.depth_index.clear()
        self.tag_index.clear()
        self.parent_to_children.clear()
    
    def _update_statistics(self) -> None:
        """Update dynamic statistics"""
        active_count = sum(1 for b in self.blooms.values() if b.is_active)
        dormant_count = len(self.blooms) - active_count
        
        self.stats.update({
            'active_bloom_count': active_count,
            'dormant_bloom_count': dormant_count,
            'total_bloom_count': len(self.blooms),
            'root_count': len(self.roots)
        })
        
        # Calculate average lineage length
        if self.blooms:
            lineage_lengths = []
            for root_id in self.roots:
                max_depth = self._get_max_depth_from_root(root_id)
                lineage_lengths.append(max_depth + 1)
            
            self.stats['average_lineage_length'] = np.mean(lineage_lengths) if lineage_lengths else 0.0
        
        # Calculate entropy variance
        entropies = [b.entropy for b in self.blooms.values()]
        self.stats['entropy_variance'] = np.var(entropies) if entropies else 0.0
    
    def _get_max_depth_from_root(self, root_id: str) -> int:
        """Get maximum depth reachable from a root bloom"""
        if root_id not in self.blooms:
            return 0
        
        max_depth = 0
        queue = [(root_id, 0)]
        
        while queue:
            bloom_id, depth = queue.pop(0)
            max_depth = max(max_depth, depth)
            
            if bloom_id in self.blooms:
                for child_id in self.blooms[bloom_id].children:
                    queue.append((child_id, depth + 1))
        
        return max_depth


# Integration with DAWN Codex Engine
def integrate_with_codex(bloom_manager: BloomManager, bloom_id: str) -> Optional[str]:
    """
    Integrate bloom data with DAWN Codex Engine for symbolic analysis.
    
    Args:
        bloom_manager: BloomManager instance
        bloom_id: ID of bloom to analyze
        
    Returns:
        Symbolic analysis string or None if bloom not found
    """
    try:
        from codex import summarize_bloom
        
        if bloom_id not in bloom_manager.blooms:
            return None
        
        bloom = bloom_manager.blooms[bloom_id]
        
        # Create bloom dict for codex analysis
        bloom_dict = {
            'depth': bloom.depth,
            'entropy': bloom.entropy,
            'lineage': [b.id for b in bloom_manager.get_lineage(bloom_id)],
            'semantic_drift': bloom.semantic_drift,
            'rebloom_status': 'active' if bloom.is_active else 'dormant',
            'complexity': bloom.complexity
        }
        
        return summarize_bloom(bloom_dict)
        
    except ImportError:
        if bloom_id not in bloom_manager.blooms:
            return f"Bloom {bloom_id}: Not found"
        bloom = bloom_manager.blooms[bloom_id]
        return f"Bloom {bloom_id}: Depth-{bloom.depth} | E:{bloom.entropy:.2f} | {'Active' if bloom.is_active else 'Dormant'}"


# Factory function for easy initialization
def create_bloom_manager(**kwargs) -> BloomManager:
    """Create and return a configured BloomManager instance"""
    return BloomManager(**kwargs)


# Example usage and testing
if __name__ == "__main__":
    # Create manager
    manager = BloomManager(entropy_decay=0.9, semantic_mutation_rate=0.1)
    
    # Create root bloom
    root = manager.create_bloom(
        seed="exploring consciousness",
        mood={'base_level': 0.6, 'volatility': 0.3},
        entropy=0.5,
        tags={'consciousness', 'exploration'}
    )
    
    print(f"Created root bloom: {root.id}")
    print(f"Root seed: {root.seed}")
    
    # Create some child blooms
    child1 = manager.rebloom(root.id, delta_entropy=0.1)
    child2 = manager.rebloom(root.id, delta_entropy=-0.2)
    grandchild = manager.rebloom(child1.id, delta_entropy=0.05)
    
    print(f"\nCreated children: {child1.id}, {child2.id}")
    print(f"Created grandchild: {grandchild.id}")
    
    # Show lineage
    lineage = manager.get_lineage(grandchild.id)
    print(f"\nLineage for {grandchild.id}:")
    for bloom in lineage:
        print(f"  Depth {bloom.depth}: {bloom.seed} (entropy: {bloom.entropy:.3f})")
    
    # Show entropy trend
    entropy_trend = manager.get_entropy_trend(grandchild.id)
    print(f"\nEntropy evolution:")
    for depth, entropy in entropy_trend:
        print(f"  Generation {depth}: {entropy:.3f}")
    
    # Test search
    results = manager.find_resonant_blooms("consciousness exploration", threshold=0.5)
    print(f"\nFound {len(results)} resonant blooms")
    
    # Show statistics
    stats = manager.get_statistics()
    print(f"\nBloom system statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test codex integration
    if grandchild:
        codex_analysis = integrate_with_codex(manager, grandchild.id)
        print(f"\nCodex analysis: {codex_analysis}") 