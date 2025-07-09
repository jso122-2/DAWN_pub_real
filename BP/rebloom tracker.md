#!/usr/bin/env python3
"""
rebloom_tracker.py - Rebloom Chain Tracking for DAWN
Tracks genealogy, entropy evolution, and rebloom patterns in the cognitive system.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime
import json
import networkx as nx
import numpy as np
from collections import defaultdict, deque


@dataclass
class RebloomEvent:
    """Represents a single rebloom event"""
    parent_id: str
    child_id: str
    entropy_diff: float
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'parent_id': self.parent_id,
            'child_id': self.child_id,
            'entropy_diff': self.entropy_diff,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }


@dataclass 
class BloomNode:
    """Lightweight node for tracking bloom relationships"""
    bloom_id: str
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    depth: int = 0
    entropy_delta_from_parent: float = 0.0
    creation_time: datetime = field(default_factory=datetime.now)
    total_entropy_drift: float = 0.0  # Cumulative entropy change from root
    
    
class RebloomTracker:
    """
    Tracks rebloom chains and genealogy in DAWN's cognitive system.
    Maintains parent-child relationships and entropy evolution metadata.
    """
    
    def __init__(self):
        """Initialize the rebloom tracker"""
        # Core tracking structures
        self.nodes: Dict[str, BloomNode] = {}  # bloom_id -> BloomNode
        self.rebloom_events: List[RebloomEvent] = []  # Chronological log
        self.roots: Set[str] = set()  # Bloom IDs with no parent
        
        # Indexes for efficient queries
        self.parent_to_children: Dict[str, List[str]] = defaultdict(list)
        self.depth_index: Dict[int, List[str]] = defaultdict(list)  # depth -> bloom_ids
        
        # NetworkX graph for advanced analysis
        self.lineage_graph = nx.DiGraph()
        
        # Statistics
        self.max_depth_observed = 0
        self.total_reblooms = 0
        self.entropy_stats = {
            'max_positive_drift': 0.0,
            'max_negative_drift': 0.0,
            'average_drift': 0.0
        }
        
    def log_rebloom(self, parent_id: str, child_id: str, entropy_diff: float,
                    metadata: Optional[Dict] = None) -> bool:
        """
        Log a rebloom event linking parent to child with entropy difference.
        
        Args:
            parent_id: ID of the parent bloom
            child_id: ID of the child bloom
            entropy_diff: Entropy change from parent to child
            metadata: Optional additional metadata
            
        Returns:
            True if successfully logged, False if validation failed
        """
        # Validation
        if child_id == parent_id:
            return False  # Can't be own parent
        
        if child_id in self.nodes and self.nodes[child_id].parent_id is not None:
            return False  # Child already has a parent
        
        # Create or update parent node
        if parent_id not in self.nodes:
            # Parent must be a root if we haven't seen it before
            parent_node = BloomNode(bloom_id=parent_id, depth=0)
            self.nodes[parent_id] = parent_node
            self.roots.add(parent_id)
            self.depth_index[0].append(parent_id)
            self.lineage_graph.add_node(parent_id, depth=0)
        else:
            parent_node = self.nodes[parent_id]
        
        # Calculate child depth
        child_depth = parent_node.depth + 1
        
        # Calculate total entropy drift from root
        total_drift = parent_node.total_entropy_drift + entropy_diff
        
        # Create child node
        child_node = BloomNode(
            bloom_id=child_id,
            parent_id=parent_id,
            depth=child_depth,
            entropy_delta_from_parent=entropy_diff,
            total_entropy_drift=total_drift
        )
        
        # Update structures
        self.nodes[child_id] = child_node
        parent_node.children.append(child_id)
        self.parent_to_children[parent_id].append(child_id)
        self.depth_index[child_depth].append(child_id)
        
        # Update graph
        self.lineage_graph.add_node(child_id, depth=child_depth, 
                                   entropy_drift=total_drift)
        self.lineage_graph.add_edge(parent_id, child_id, 
                                   entropy_diff=entropy_diff)
        
        # Log event
        event = RebloomEvent(
            parent_id=parent_id,
            child_id=child_id,
            entropy_diff=entropy_diff,
            metadata=metadata or {}
        )
        self.rebloom_events.append(event)
        
        # Update statistics
        self.total_reblooms += 1
        self.max_depth_observed = max(self.max_depth_observed, child_depth)
        
        # Update entropy statistics
        if entropy_diff > self.entropy_stats['max_positive_drift']:
            self.entropy_stats['max_positive_drift'] = entropy_diff
        if entropy_diff < self.entropy_stats['max_negative_drift']:
            self.entropy_stats['max_negative_drift'] = entropy_diff
        
        # Recalculate average drift
        all_drifts = [e.entropy_diff for e in self.rebloom_events]
        if all_drifts:
            self.entropy_stats['average_drift'] = np.mean(all_drifts)
        
        return True
    
    def get_depth(self, bloom_id: str) -> int:
        """
        Get the generation depth of a bloom from its root ancestor.
        
        Args:
            bloom_id: ID of the bloom
            
        Returns:
            Depth from root (0 for roots, -1 if bloom not found)
        """
        if bloom_id not in self.nodes:
            return -1
        
        return self.nodes[bloom_id].depth
    
    def get_ancestry_chain(self, bloom_id: str) -> List[str]:
        """
        Get the ancestry chain from root to the specified bloom.
        
        Args:
            bloom_id: ID of the bloom
            
        Returns:
            List of bloom IDs from root ancestor to target bloom
        """
        if bloom_id not in self.nodes:
            return []
        
        chain = []
        current_id = bloom_id
        
        # Build chain from bloom to root
        while current_id is not None:
            chain.append(current_id)
            node = self.nodes[current_id]
            current_id = node.parent_id
        
        # Reverse to get root-to-bloom order
        chain.reverse()
        
        return chain
    
    def get_rebloom_map(self) -> Dict[str, List[str]]:
        """
        Get mapping of all parent to children relationships.
        
        Returns:
            Dictionary mapping parent IDs to lists of child IDs
        """
        # Return a copy to prevent external modification
        return {
            parent: children.copy() 
            for parent, children in self.parent_to_children.items()
            if children  # Only include parents that have children
        }
    
    def get_entropy_evolution(self, bloom_id: str) -> List[Tuple[str, float]]:
        """
        Get entropy evolution along the ancestry chain.
        
        Args:
            bloom_id: ID of the bloom
            
        Returns:
            List of (bloom_id, total_entropy_drift) tuples
        """
        chain = self.get_ancestry_chain(bloom_id)
        
        evolution = []
        for bid in chain:
            node = self.nodes[bid]
            evolution.append((bid, node.total_entropy_drift))
        
        return evolution
    
    def get_descendants(self, bloom_id: str, max_depth: Optional[int] = None) -> List[str]:
        """
        Get all descendants of a bloom.
        
        Args:
            bloom_id: ID of the bloom
            max_depth: Maximum depth to traverse (None for all)
            
        Returns:
            List of descendant bloom IDs
        """
        if bloom_id not in self.nodes:
            return []
        
        descendants = []
        to_visit = deque([(bloom_id, 0)])
        
        while to_visit:
            current_id, current_depth = to_visit.popleft()
            
            # Add children if within depth limit
            if max_depth is None or current_depth < max_depth:
                for child_id in self.nodes[current_id].children:
                    descendants.append(child_id)
                    to_visit.append((child_id, current_depth + 1))
        
        return descendants
    
    def get_siblings(self, bloom_id: str) -> List[str]:
        """
        Get sibling blooms (same parent).
        
        Args:
            bloom_id: ID of the bloom
            
        Returns:
            List of sibling bloom IDs (excluding self)
        """
        if bloom_id not in self.nodes:
            return []
        
        node = self.nodes[bloom_id]
        if node.parent_id is None:
            return []  # Root nodes have no siblings
        
        parent_node = self.nodes[node.parent_id]
        siblings = [
            child_id for child_id in parent_node.children 
            if child_id != bloom_id
        ]
        
        return siblings
    
    def find_common_ancestor(self, bloom_id1: str, bloom_id2: str) -> Optional[str]:
        """
        Find the most recent common ancestor of two blooms.
        
        Args:
            bloom_id1: First bloom ID
            bloom_id2: Second bloom ID
            
        Returns:
            Common ancestor bloom ID or None
        """
        chain1 = self.get_ancestry_chain(bloom_id1)
        chain2 = self.get_ancestry_chain(bloom_id2)
        
        if not chain1 or not chain2:
            return None
        
        # Find where chains diverge
        common_ancestor = None
        for b1, b2 in zip(chain1, chain2):
            if b1 == b2:
                common_ancestor = b1
            else:
                break
        
        return common_ancestor
    
    def get_lineage_statistics(self, root_id: Optional[str] = None) -> Dict:
        """
        Get statistics about lineage structure.
        
        Args:
            root_id: Specific root to analyze (None for all)
            
        Returns:
            Dictionary of lineage statistics
        """
        if root_id:
            # Stats for specific lineage
            descendants = self.get_descendants(root_id)
            lineage_nodes = [root_id] + descendants
            
            depths = [self.nodes[bid].depth for bid in lineage_nodes]
            entropy_drifts = [self.nodes[bid].total_entropy_drift 
                            for bid in lineage_nodes]
            
            return {
                'root_id': root_id,
                'total_nodes': len(lineage_nodes),
                'max_depth': max(depths) if depths else 0,
                'average_depth': np.mean(depths) if depths else 0,
                'entropy_range': (min(entropy_drifts), max(entropy_drifts)) 
                                if entropy_drifts else (0, 0),
                'branching_factor': self._calculate_branching_factor(lineage_nodes)
            }
        else:
            # Global statistics
            all_depths = [node.depth for node in self.nodes.values()]
            all_drifts = [node.total_entropy_drift for node in self.nodes.values()]
            
            return {
                'total_blooms': len(self.nodes),
                'total_roots': len(self.roots),
                'total_reblooms': self.total_reblooms,
                'max_depth': self.max_depth_observed,
                'average_depth': np.mean(all_depths) if all_depths else 0,
                'entropy_stats': self.entropy_stats.copy(),
                'depth_distribution': self._get_depth_distribution(),
                'largest_family_size': self._find_largest_family()
            }
    
    def get_rebloom_patterns(self, window_size: int = 10) -> Dict:
        """
        Analyze rebloom patterns over time.
        
        Args:
            window_size: Number of recent events to analyze
            
        Returns:
            Dictionary of pattern analysis
        """
        recent_events = self.rebloom_events[-window_size:] if self.rebloom_events else []
        
        if not recent_events:
            return {'patterns': [], 'frequency': 0}
        
        # Analyze entropy diff patterns
        entropy_diffs = [e.entropy_diff for e in recent_events]
        
        patterns = {
            'increasing_entropy': sum(1 for d in entropy_diffs if d > 0),
            'decreasing_entropy': sum(1 for d in entropy_diffs if d < 0),
            'stable_entropy': sum(1 for d in entropy_diffs if abs(d) < 0.1),
            'high_volatility': sum(1 for d in entropy_diffs if abs(d) > 0.5),
            'average_diff': np.mean(entropy_diffs),
            'entropy_trend': 'increasing' if np.mean(entropy_diffs) > 0 else 'decreasing'
        }
        
        # Time-based patterns
        if len(recent_events) > 1:
            time_deltas = []
            for i in range(1, len(recent_events)):
                delta = (recent_events[i].timestamp - recent_events[i-1].timestamp).total_seconds()
                time_deltas.append(delta)
            
            patterns['average_rebloom_interval'] = np.mean(time_deltas)
            patterns['rebloom_acceleration'] = time_deltas[-1] < patterns['average_rebloom_interval']
        
        return patterns
    
    def visualize_lineage_graph(self, root_id: Optional[str] = None) -> Dict:
        """
        Get graph visualization data for lineage.
        
        Args:
            root_id: Specific root to visualize (None for all)
            
        Returns:
            Dictionary with nodes and edges for visualization
        """
        if root_id:
            # Get subgraph for specific lineage
            descendants = self.get_descendants(root_id)
            nodes_to_include = [root_id] + descendants
            subgraph = self.lineage_graph.subgraph(nodes_to_include)
        else:
            subgraph = self.lineage_graph
        
        # Prepare visualization data
        nodes = []
        for node_id in subgraph.nodes():
            node_data = self.nodes[node_id]
            nodes.append({
                'id': node_id,
                'depth': node_data.depth,
                'entropy_drift': node_data.total_entropy_drift,
                'is_root': node_id in self.roots,
                'children_count': len(node_data.children)
            })
        
        edges = []
        for parent, child in subgraph.edges():
            edge_data = subgraph.edges[parent, child]
            edges.append({
                'source': parent,
                'target': child,
                'entropy_diff': edge_data.get('entropy_diff', 0)
            })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'stats': {
                'total_nodes': len(nodes),
                'total_edges': len(edges),
                'max_depth': max(n['depth'] for n in nodes) if nodes else 0
            }
        }
    
    def _calculate_branching_factor(self, node_ids: List[str]) -> float:
        """Calculate average branching factor for a set of nodes"""
        parent_nodes = [nid for nid in node_ids 
                       if self.nodes[nid].children]
        
        if not parent_nodes:
            return 0.0
        
        total_children = sum(len(self.nodes[nid].children) 
                           for nid in parent_nodes)
        
        return total_children / len(parent_nodes)
    
    def _get_depth_distribution(self) -> Dict[int, int]:
        """Get distribution of nodes by depth"""
        return {
            depth: len(nodes) 
            for depth, nodes in self.depth_index.items()
        }
    
    def _find_largest_family(self) -> int:
        """Find the size of the largest family tree"""
        if not self.roots:
            return 0
        
        max_size = 0
        for root in self.roots:
            family_size = 1 + len(self.get_descendants(root))
            max_size = max(max_size, family_size)
        
        return max_size
    
    def save_to_file(self, filepath: str):
        """Save tracker state to JSON file"""
        data = {
            'nodes': {
                bid: {
                    'bloom_id': node.bloom_id,
                    'parent_id': node.parent_id,
                    'children': node.children,
                    'depth': node.depth,
                    'entropy_delta_from_parent': node.entropy_delta_from_parent,
                    'total_entropy_drift': node.total_entropy_drift,
                    'creation_time': node.creation_time.isoformat()
                }
                for bid, node in self.nodes.items()
            },
            'events': [event.to_dict() for event in self.rebloom_events],
            'statistics': {
                'max_depth_observed': self.max_depth_observed,
                'total_reblooms': self.total_reblooms,
                'entropy_stats': self.entropy_stats
            },
            'metadata': {
                'saved_at': datetime.now().isoformat(),
                'total_nodes': len(self.nodes),
                'total_roots': len(self.roots)
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filepath: str):
        """Load tracker state from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Clear current state
        self.__init__()
        
        # Rebuild nodes
        for bid, node_data in data['nodes'].items():
            node = BloomNode(
                bloom_id=node_data['bloom_id'],
                parent_id=node_data['parent_id'],
                children=node_data['children'],
                depth=node_data['depth'],
                entropy_delta_from_parent=node_data['entropy_delta_from_parent'],
                total_entropy_drift=node_data['total_entropy_drift'],
                creation_time=datetime.fromisoformat(node_data['creation_time'])
            )
            self.nodes[bid] = node
            
            # Rebuild indexes
            if node.parent_id is None:
                self.roots.add(bid)
            
            self.depth_index[node.depth].append(bid)
            
            if node.children:
                self.parent_to_children[bid] = node.children.copy()
            
            # Rebuild graph
            self.lineage_graph.add_node(bid, depth=node.depth,
                                      entropy_drift=node.total_entropy_drift)
            if node.parent_id:
                self.lineage_graph.add_edge(node.parent_id, bid,
                                          entropy_diff=node.entropy_delta_from_parent)
        
        # Rebuild events
        for event_data in data['events']:
            event = RebloomEvent(
                parent_id=event_data['parent_id'],
                child_id=event_data['child_id'],
                entropy_diff=event_data['entropy_diff'],
                timestamp=datetime.fromisoformat(event_data['timestamp']),
                metadata=event_data.get('metadata', {})
            )
            self.rebloom_events.append(event)
        
        # Restore statistics
        stats = data['statistics']
        self.max_depth_observed = stats['max_depth_observed']
        self.total_reblooms = stats['total_reblooms']
        self.entropy_stats = stats['entropy_stats']


# Example usage and testing
if __name__ == "__main__":
    # Create tracker
    tracker = RebloomTracker()
    
    # Create a root bloom
    root_id = "bloom_root_001"
    
    # Create first generation
    tracker.log_rebloom(root_id, "bloom_child_001", entropy_diff=0.1)
    tracker.log_rebloom(root_id, "bloom_child_002", entropy_diff=-0.2)
    tracker.log_rebloom(root_id, "bloom_child_003", entropy_diff=0.15)
    
    # Create second generation
    tracker.log_rebloom("bloom_child_001", "bloom_grand_001", entropy_diff=0.05)
    tracker.log_rebloom("bloom_child_001", "bloom_grand_002", entropy_diff=-0.1)
    tracker.log_rebloom("bloom_child_002", "bloom_grand_003", entropy_diff=0.3)
    
    # Create third generation
    tracker.log_rebloom("bloom_grand_001", "bloom_great_001", entropy_diff=0.2)
    
    # Test methods
    print("=== Rebloom Tracker Test ===\n")
    
    # Get depth
    print(f"Depth of bloom_great_001: {tracker.get_depth('bloom_great_001')}")
    print(f"Depth of root: {tracker.get_depth(root_id)}")
    
    # Get ancestry chain
    print(f"\nAncestry of bloom_great_001: {tracker.get_ancestry_chain('bloom_great_001')}")
    
    # Get rebloom map
    print("\nRebloom Map:")
    rebloom_map = tracker.get_rebloom_map()
    for parent, children in rebloom_map.items():
        print(f"  {parent} -> {children}")
    
    # Get entropy evolution
    print("\nEntropy Evolution for bloom_great_001:")
    evolution = tracker.get_entropy_evolution('bloom_great_001')
    for bloom_id, drift in evolution:
        print(f"  {bloom_id}: {drift:+.3f}")
    
    # Get siblings
    print(f"\nSiblings of bloom_child_001: {tracker.get_siblings('bloom_child_001')}")
    
    # Find common ancestor
    common = tracker.find_common_ancestor('bloom_grand_001', 'bloom_grand_003')
    print(f"\nCommon ancestor of bloom_grand_001 and bloom_grand_003: {common}")
    
    # Get statistics
    print("\nGlobal Statistics:")
    stats = tracker.get_lineage_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Get patterns
    print("\nRebloom Patterns:")
    patterns = tracker.get_rebloom_patterns()
    for key, value in patterns.items():
        print(f"  {key}: {value}")
    
    # Visualize
    print("\nLineage Visualization Data:")
    viz_data = tracker.visualize_lineage_graph(root_id)
    print(f"  Nodes: {len(viz_data['nodes'])}")
    print(f"  Edges: {len(viz_data['edges'])}")
    print(f"  Max Depth: {viz_data['stats']['max_depth']}")