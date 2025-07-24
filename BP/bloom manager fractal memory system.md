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
            return