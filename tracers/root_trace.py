#!/usr/bin/env python3
"""
DAWN Symbolic Root Emergence Logger
===================================

Logs symbolic root events detected by rhizome_map.py and other
symbolic pattern detection systems.

Called from cognition_runtime.py when detect_symbolic_root() 
returns significant results.
"""

import json
import os
import time
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime

# Ensure log directory exists
ROOT_TRACE_LOG = Path("runtime/logs/root_trace.log")
ROOT_TRACE_LOG.parent.mkdir(parents=True, exist_ok=True)

def log_root_event(root: Dict[str, Any]) -> None:
    """
    Log a symbolic root emergence event.
    
    Args:
        root: Dictionary containing root event data
    """
    # Add timestamp if not present
    if 'timestamp' not in root:
        root['timestamp'] = time.time()
    
    if 'datetime' not in root:
        root['datetime'] = datetime.now().isoformat()
    
    try:
        with open(ROOT_TRACE_LOG, "a", encoding='utf-8') as f:
            f.write(json.dumps(root) + "\n")
        
        print(f"🌿 Root traced: {root.get('symbolic_root', 'unknown')} at tick {root.get('tick', '?')}")
        
    except Exception as e:
        print(f"⚠️ Error logging root event: {e}")

def log_mycelium_expansion(root_count: int, network_density: float, tick: int) -> None:
    """Log mycelium network expansion as a root event"""
    root_event = {
        "tick": tick,
        "type": "MYCELIUM_EXPANSION",
        "root_count": root_count,
        "network_density": network_density,
        "symbolic_root": f"network_expansion_{root_count}",
        "branch": ["mycelium", "growth", "connectivity"],
        "depth": 1,
        "significance": min(1.0, network_density * 2)
    }
    
    log_root_event(root_event)

def log_rhizome_cluster(cluster_nodes: List[str], cluster_size: int, tick: int) -> None:
    """Log rhizome cluster formation as a root event"""
    root_event = {
        "tick": tick,
        "type": "RHIZOME_CLUSTER", 
        "origin": cluster_nodes[0] if cluster_nodes else "unknown",
        "cluster_nodes": cluster_nodes[:5],  # Top 5 nodes
        "cluster_size": cluster_size,
        "symbolic_root": f"emergent_cluster_{cluster_size}",
        "branch": ["rhizome", "clustering", "emergence"],
        "depth": len(cluster_nodes),
        "significance": min(1.0, cluster_size / 10.0)
    }
    
    log_root_event(root_event)

def log_lineage_milestone(depth: int, deepest_chunk: str, tick: int) -> None:
    """Log memory lineage depth milestone as a root event"""
    root_event = {
        "tick": tick,
        "type": "LINEAGE_MILESTONE",
        "origin": deepest_chunk,
        "lineage_depth": depth,
        "symbolic_root": f"deep_ancestry_{depth}",
        "branch": ["memory", "lineage", "ancestry"],
        "depth": depth,
        "significance": min(1.0, depth / 15.0)
    }
    
    log_root_event(root_event)

def log_cognitive_emergence(pattern_type: str, data: Dict[str, Any], tick: int) -> None:
    """Log general cognitive emergence patterns"""
    root_event = {
        "tick": tick,
        "type": "COGNITIVE_EMERGENCE",
        "pattern_type": pattern_type,
        "data": data,
        "symbolic_root": f"cognitive_{pattern_type}",
        "branch": ["cognition", "emergence", pattern_type],
        "depth": data.get('complexity', 1),
        "significance": data.get('significance', 0.5)
    }
    
    log_root_event(root_event)

def get_recent_roots(limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent symbolic root events"""
    if not ROOT_TRACE_LOG.exists():
        return []
    
    roots = []
    try:
        with open(ROOT_TRACE_LOG, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    root = json.loads(line.strip())
                    roots.append(root)
        
        # Return most recent
        return roots[-limit:]
        
    except Exception as e:
        print(f"⚠️ Error reading root trace: {e}")
        return []

def analyze_root_patterns() -> Dict[str, Any]:
    """Analyze patterns in symbolic root emergence"""
    roots = get_recent_roots(50)
    
    if not roots:
        return {"total_roots": 0, "patterns": {}}
    
    # Pattern analysis
    root_types = {}
    significance_levels = []
    branch_patterns = {}
    
    for root in roots:
        # Count types
        root_type = root.get('type', 'unknown')
        root_types[root_type] = root_types.get(root_type, 0) + 1
        
        # Track significance
        significance = root.get('significance', 0.5)
        significance_levels.append(significance)
        
        # Track branch patterns
        branches = root.get('branch', [])
        for branch in branches:
            branch_patterns[branch] = branch_patterns.get(branch, 0) + 1
    
    avg_significance = sum(significance_levels) / len(significance_levels)
    
    return {
        "total_roots": len(roots),
        "root_types": root_types,
        "avg_significance": avg_significance,
        "top_branches": sorted(branch_patterns.items(), key=lambda x: x[1], reverse=True)[:5],
        "recent_activity": len([r for r in roots if time.time() - r.get('timestamp', 0) < 300])  # Last 5 minutes
    }

# Sample usage and testing
if __name__ == "__main__":
    print("🌿 Testing Symbolic Root Logging")
    print("=" * 40)
    
    # Test different types of root events
    log_mycelium_expansion(15, 0.73, 1001)
    log_rhizome_cluster(["node_a", "node_b", "node_c"], 4, 1002)
    log_lineage_milestone(12, "memory_deep_001", 1003)
    log_cognitive_emergence("meta_reflection", {"complexity": 3, "significance": 0.8}, 1004)
    
    # Analyze patterns
    print("\nAnalyzing root patterns...")
    patterns = analyze_root_patterns()
    print(f"Total roots: {patterns['total_roots']}")
    print(f"Average significance: {patterns['avg_significance']:.2f}")
    print(f"Top branches: {patterns['top_branches']}")
    
    print(f"\n✅ Root trace log: {ROOT_TRACE_LOG}") 