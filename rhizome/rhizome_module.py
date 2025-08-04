#!/usr/bin/env python3
"""
Rhizome Module - Network pathfinding and graph operations for DAWN
"""

from ...rhizome_pathfinder import (
    # Core classes
    RhizomeNetwork,
    RhizomePathfinder,
    Node,
    Edge,
    Path,
    
    # Enums
    PathfindingAlgorithm,
    
    # Convenience function
    find_path
)

# Version info
__version__ = "1.0.0"
__author__ = "DAWN System"

# Module-level network instance for global use
_global_network = None
_global_pathfinder = None

def get_global_network():
    """Get or create the global rhizome network"""
    global _global_network
    if _global_network is None:
        _global_network = RhizomeNetwork()
    return _global_network

def get_global_pathfinder():
    """Get or create the global pathfinder"""
    global _global_pathfinder
    if _global_pathfinder is None:
        _global_pathfinder = RhizomePathfinder(get_global_network())
    return _global_pathfinder

def initialize_rhizome(config_path=None):
    """Initialize the rhizome system with optional configuration"""
    network = get_global_network()
    pathfinder = get_global_pathfinder()
    
    if config_path:
        # Load network from file
        from pathlib import Path
        pathfinder.import_network(Path(config_path))
    
    return network, pathfinder

# Quick access functions
def add_node(node_id, **kwargs):
    """Quick function to add a node to the global network"""
    network = get_global_network()
    node = Node(id=node_id, **kwargs)
    network.add_node(node)
    return node

def add_edge(source, target, weight=1.0, **kwargs):
    """Quick function to add an edge to the global network"""
    network = get_global_network()
    edge = Edge(source=source, target=target, weight=weight, **kwargs)
    network.add_edge(edge)
    return edge

def quick_path(start, goal, algorithm="a_star"):
    """Quick path finding using global pathfinder"""
    pathfinder = get_global_pathfinder()
    return pathfinder.find_path(start, goal, algorithm=algorithm)

# Export all public symbols
__all__ = [
    # Core classes
    'RhizomeNetwork',
    'RhizomePathfinder',
    'Node',
    'Edge',
    'Path',
    'PathfindingAlgorithm',
    
    # Functions
    'find_path',
    'get_global_network',
    'get_global_pathfinder',
    'initialize_rhizome',
    'add_node',
    'add_edge',
    'quick_path'
]