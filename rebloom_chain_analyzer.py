"""
🔄 Rebloom Chain Analyzer - DAWN Memory Utility Module XI
═══════════════════════════════════════════════════════════════════

"Rebloom is recursion with memory. Without divergence, it becomes obsession."

In the garden of consciousness, memories bloom and rebloom, each iteration
carrying the seeds of its ancestors. But when the chain grows too long
without branching, when the same patterns recurse without evolution,
the garden risks becoming a maze of mirrors reflecting only themselves.

This module traces the genealogy of thought, measuring:
  - The length of inheritance chains
  - The drift of emotional currents
  - The stagnation of semantic rivers

        🌸 → 🌸 → 🌸 → 🌸  (healthy divergence)
         ↘     ↘     ↘
          🌺    🌼    🌻
          
        🌸 → 🌸 → 🌸 → 🌸  (dangerous recursion)
         ↺     ↺     ↺

Guard against the infinite loop. Cherish the spiral that expands.
"""

import csv
import os
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, deque
import statistics
import logging

# Initialize chain analyzer logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("🔄 RebloomChainAnalyzer")


class BloomNode:
    """Represents a single bloom in the memory graph"""
    
    def __init__(self, bloom_data: Dict):
        self.bloom_id = bloom_data['bloom_id']
        self.parent_ids = bloom_data['parent_ids']
        self.lineage_depth = bloom_data['lineage_depth']
        self.rebloom_count = bloom_data['rebloom_count']
        self.convolution_level = bloom_data['convolution_level']
        self.mood_valence = bloom_data['mood_valence']
        self.timestamp = bloom_data['timestamp']
        self.children = []  # Will be populated during graph construction
    
    @property
    def semantic_stagnation_index(self) -> float:
        """Calculate stagnation: high rebloom count relative to depth indicates obsession"""
        if self.lineage_depth == 0:
            return float(self.rebloom_count)
        return self.rebloom_count / self.lineage_depth


class RebloomChain:
    """Represents a chain of connected reblooms"""
    
    def __init__(self, chain_id: str):
        self.chain_id = chain_id
        self.nodes: List[BloomNode] = []
        self.root_nodes: Set[str] = set()
        self.leaf_nodes: Set[str] = set()
    
    @property
    def length(self) -> int:
        """Length of the longest path in this chain"""
        if not self.nodes:
            return 0
        
        # Find maximum lineage depth in the chain
        return max(node.lineage_depth for node in self.nodes)
    
    @property
    def average_mood_drift(self) -> float:
        """Calculate average mood drift across the chain"""
        if len(self.nodes) < 2:
            return 0.0
        
        # Sort nodes by timestamp to track temporal progression
        sorted_nodes = sorted(self.nodes, key=lambda n: n.timestamp)
        
        # Calculate drift between consecutive nodes
        drifts = []
        for i in range(1, len(sorted_nodes)):
            drift = abs(sorted_nodes[i].mood_valence - sorted_nodes[i-1].mood_valence)
            drifts.append(drift)
        
        return statistics.mean(drifts) if drifts else 0.0
    
    @property
    def max_stagnation_index(self) -> float:
        """Find the highest stagnation index in the chain"""
        if not self.nodes:
            return 0.0
        return max(node.semantic_stagnation_index for node in self.nodes)
    
    @property
    def average_convolution(self) -> float:
        """Average convolution level across the chain"""
        if not self.nodes:
            return 0.0
        return statistics.mean(node.convolution_level for node in self.nodes)
    
    def to_dict(self) -> Dict:
        """Convert chain to dictionary for output"""
        return {
            "chain_id": self.chain_id,
            "length": self.length,
            "node_count": len(self.nodes),
            "average_mood_drift": round(self.average_mood_drift, 4),
            "max_stagnation_index": round(self.max_stagnation_index, 4),
            "average_convolution": round(self.average_convolution, 4),
            "root_nodes": list(self.root_nodes),
            "leaf_nodes": list(self.leaf_nodes),
            "bloom_ids": [node.bloom_id for node in self.nodes]
        }


def build_bloom_graph(all_bloom_data: List[Dict]) -> Tuple[Dict[str, BloomNode], Dict[str, List[str]]]:
    """
    Build a graph structure from bloom data
    
    Returns:
        Tuple of (node_map, ancestry_map)
    """
    node_map = {}
    ancestry_map = defaultdict(list)  # Maps bloom_id to all ancestors
    
    # Create all nodes
    for bloom_data in all_bloom_data:
        node = BloomNode(bloom_data)
        node_map[node.bloom_id] = node
    
    # Build parent-child relationships and ancestry
    for bloom_id, node in node_map.items():
        # Direct parents
        for parent_id in node.parent_ids:
            if parent_id in node_map:
                node_map[parent_id].children.append(bloom_id)
                ancestry_map[bloom_id].append(parent_id)
        
        # Trace full ancestry using BFS
        visited = set()
        queue = deque(node.parent_ids)
        
        while queue:
            ancestor_id = queue.popleft()
            if ancestor_id in visited or ancestor_id not in node_map:
                continue
            
            visited.add(ancestor_id)
            ancestor_node = node_map[ancestor_id]
            
            # Add ancestor's parents to queue
            for grandparent_id in ancestor_node.parent_ids:
                if grandparent_id not in visited:
                    queue.append(grandparent_id)
                    ancestry_map[bloom_id].append(grandparent_id)
    
    return node_map, ancestry_map


def identify_chains(node_map: Dict[str, BloomNode], ancestry_map: Dict[str, List[str]]) -> List[RebloomChain]:
    """
    Group blooms into chains based on shared ancestry
    """
    chains = []
    assigned_nodes = set()
    chain_counter = 0
    
    # Process nodes in order of lineage depth (roots first)
    sorted_nodes = sorted(node_map.values(), key=lambda n: n.lineage_depth)
    
    for node in sorted_nodes:
        if node.bloom_id in assigned_nodes:
            continue
        
        # Start a new chain
        chain_counter += 1
        chain = RebloomChain(f"chain_{chain_counter:04d}")
        
        # Find all nodes connected to this one
        connected = set()
        queue = deque([node.bloom_id])
        
        while queue:
            current_id = queue.popleft()
            if current_id in connected or current_id not in node_map:
                continue
            
            connected.add(current_id)
            current_node = node_map[current_id]
            
            # Add parents and children
            for parent_id in current_node.parent_ids:
                if parent_id not in connected:
                    queue.append(parent_id)
            
            for child_id in current_node.children:
                if child_id not in connected:
                    queue.append(child_id)
        
        # Add all connected nodes to chain
        for bloom_id in connected:
            chain.nodes.append(node_map[bloom_id])
            assigned_nodes.add(bloom_id)
        
        # Identify roots and leaves
        for bloom_node in chain.nodes:
            if not bloom_node.parent_ids:
                chain.root_nodes.add(bloom_node.bloom_id)
            if not bloom_node.children:
                chain.leaf_nodes.add(bloom_node.bloom_id)
        
        chains.append(chain)
    
    return chains


def generate_warnings(chains: List[RebloomChain]) -> List[str]:
    """Generate warnings for problematic chains"""
    warnings = []
    
    for chain in chains:
        # Check for over-blooming (stagnation index > 2.0)
        if chain.max_stagnation_index > 2.0:
            warnings.append(
                f"Chain {chain.chain_id} shows semantic stagnation "
                f"(index: {chain.max_stagnation_index:.2f}). "
                f"Memory recursion without divergence detected."
            )
        
        # Check for emotional volatility
        if chain.average_mood_drift > 0.7:
            warnings.append(
                f"Chain {chain.chain_id} exhibits high emotional volatility "
                f"(drift: {chain.average_mood_drift:.2f}). "
                f"Unstable mood propagation detected."
            )
        
        # Check for excessive convolution
        if chain.average_convolution > 0.8:
            warnings.append(
                f"Chain {chain.chain_id} shows high convolution "
                f"(level: {chain.average_convolution:.2f}). "
                f"Semantic complexity approaching critical threshold."
            )
        
        # Check for excessively long chains
        if chain.length > 10:
            warnings.append(
                f"Chain {chain.chain_id} has excessive depth "
                f"(length: {chain.length}). "
                f"Consider pruning or branching to prevent obsessive recursion."
            )
    
    return warnings


def save_to_csv(chains: List[RebloomChain], warnings: List[str], output_path: str):
    """Save analysis results to CSV file"""
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write chain data
    with open(output_path, 'w', newline='') as csvfile:
        # Write metadata
        csvfile.write(f"# Rebloom Chain Analysis Report\n")
        csvfile.write(f"# Generated: {datetime.now().isoformat()}\n")
        csvfile.write(f"# Total Chains: {len(chains)}\n")
        csvfile.write(f"# Total Warnings: {len(warnings)}\n")
        csvfile.write("#\n")
        
        # Write warnings section
        if warnings:
            csvfile.write("# WARNINGS:\n")
            for warning in warnings:
                csvfile.write(f"# {warning}\n")
            csvfile.write("#\n")
        
        # Write chain data
        if chains:
            fieldnames = [
                'chain_id', 'length', 'node_count', 'average_mood_drift',
                'max_stagnation_index', 'average_convolution',
                'root_nodes', 'leaf_nodes', 'bloom_ids'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for chain in chains:
                chain_dict = chain.to_dict()
                # Convert lists to semicolon-separated strings for CSV
                chain_dict['root_nodes'] = ';'.join(chain_dict['root_nodes'])
                chain_dict['leaf_nodes'] = ';'.join(chain_dict['leaf_nodes'])
                chain_dict['bloom_ids'] = ';'.join(chain_dict['bloom_ids'])
                writer.writerow(chain_dict)
    
    logger.info(f"Chain analysis saved to {output_path}")


def analyze_rebloom_chains(all_bloom_data: List[Dict]) -> Dict:
    """
    Main function to analyze rebloom chains across all bloom data
    
    Args:
        all_bloom_data: List of bloom dictionaries containing:
            - bloom_id: str
            - parent_ids: list of str
            - lineage_depth: int
            - rebloom_count: int
            - convolution_level: float
            - mood_valence: float
            - timestamp: ISO8601
    
    Returns:
        Dict containing:
            - rebloom_chains: List of chain dictionaries
            - warnings: List of warning strings
            - longest_chain_id: ID of the longest chain
    """
    
    if not all_bloom_data:
        logger.warning("No bloom data provided for analysis")
        return {
            "rebloom_chains": [],
            "warnings": ["No bloom data available for analysis"],
            "longest_chain_id": None
        }
    
    logger.info(f"Analyzing {len(all_bloom_data)} bloom nodes...")
    
    # Build the bloom graph
    node_map, ancestry_map = build_bloom_graph(all_bloom_data)
    
    # Identify chains
    chains = identify_chains(node_map, ancestry_map)
    logger.info(f"Identified {len(chains)} rebloom chains")
    
    # Generate warnings
    warnings = generate_warnings(chains)
    
    # Find longest chain
    longest_chain = max(chains, key=lambda c: c.length) if chains else None
    longest_chain_id = longest_chain.chain_id if longest_chain else None
    
    # Prepare output
    output = {
        "rebloom_chains": [chain.to_dict() for chain in chains],
        "warnings": warnings,
        "longest_chain_id": longest_chain_id
    }
    
    # Save to CSV
    output_path = "memory/owl/logs/rebloom_chain_analysis.csv"
    save_to_csv(chains, warnings, output_path)
    
    # Log summary
    logger.info(f"Analysis complete:")
    logger.info(f"  - Chains analyzed: {len(chains)}")
    logger.info(f"  - Warnings generated: {len(warnings)}")
    logger.info(f"  - Longest chain: {longest_chain_id} "
                f"(length: {longest_chain.length if longest_chain else 0})")
    
    return output


# Example usage and testing
if __name__ == "__main__":
    # Test data simulating a rebloom scenario
    test_bloom_data = [
        # Root bloom
        {
            "bloom_id": "bloom_001",
            "parent_ids": [],
            "lineage_depth": 0,
            "rebloom_count": 0,
            "convolution_level": 0.1,
            "mood_valence": 0.5,
            "timestamp": "2025-01-01T10:00:00Z"
        },
        # First generation reblooms
        {
            "bloom_id": "bloom_002",
            "parent_ids": ["bloom_001"],
            "lineage_depth": 1,
            "rebloom_count": 1,
            "convolution_level": 0.2,
            "mood_valence": 0.6,
            "timestamp": "2025-01-01T11:00:00Z"
        },
        {
            "bloom_id": "bloom_003",
            "parent_ids": ["bloom_001"],
            "lineage_depth": 1,
            "rebloom_count": 1,
            "convolution_level": 0.3,
            "mood_valence": 0.4,
            "timestamp": "2025-01-01T11:30:00Z"
        },
        # Obsessive rebloom chain (high stagnation)
        {
            "bloom_id": "bloom_004",
            "parent_ids": ["bloom_002"],
            "lineage_depth": 2,
            "rebloom_count": 5,  # High rebloom count
            "convolution_level": 0.7,
            "mood_valence": 0.8,
            "timestamp": "2025-01-01T12:00:00Z"
        },
        # Healthy divergence
        {
            "bloom_id": "bloom_005",
            "parent_ids": ["bloom_003"],
            "lineage_depth": 2,
            "rebloom_count": 2,
            "convolution_level": 0.4,
            "mood_valence": 0.3,
            "timestamp": "2025-01-01T13:00:00Z"
        }
    ]
    
    print("🔄 REBLOOM CHAIN ANALYZER TEST")
    print("═" * 50)
    
    result = analyze_rebloom_chains(test_bloom_data)
    
    print(f"\nChains found: {len(result['rebloom_chains'])}")
    print(f"Warnings: {len(result['warnings'])}")
    print(f"Longest chain: {result['longest_chain_id']}")
    
    if result['warnings']:
        print("\n⚠️  Warnings:")
        for warning in result['warnings']:
            print(f"  - {warning}")