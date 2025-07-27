#!/usr/bin/env python3
"""
DAWN Rebloom Lineage Tracker - Memory Ancestry & Lineage System
==============================================================

Tracks the ancestry and lineage of rebloomed memory chunks, creating
a semantic family tree of memory evolution and connection patterns.

This system enables ancestry-aware forecasting and deep memory analysis
by maintaining a graph of how memories evolve, split, and recombine.
"""

import json
import time
import logging
from typing import Dict, Any, List, Optional, Union, Tuple
from pathlib import Path
from datetime import datetime
from collections import defaultdict, deque

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rebloom_lineage")

class MemoryChunk:
    """Simple memory chunk representation for lineage tracking"""
    
    def __init__(self, chunk_id: str, content: str = "", metadata: Dict[str, Any] = None):
        self.id = chunk_id
        self.content = content
        self.metadata = metadata or {}
        self.created_at = time.time()
        self.last_accessed = time.time()
    
    def __str__(self):
        return f"MemoryChunk({self.id})"
    
    def __repr__(self):
        return self.__str__()

class LineageEntry:
    """Represents a single entry in the memory lineage tree"""
    
    def __init__(self, child_id: str, parent_id: str, method: str, 
                 depth: int = 0, significance: float = 0.5):
        self.child_id = child_id
        self.parent_id = parent_id
        self.method = method  # 'semantic_retrieval', 'sigil_triggered', 'manual', etc.
        self.depth = depth
        self.significance = significance
        self.timestamp = time.time()
        self.datetime = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'child_id': self.child_id,
            'parent_id': self.parent_id,
            'method': self.method,
            'depth': self.depth,
            'significance': self.significance,
            'timestamp': self.timestamp,
            'datetime': self.datetime
        }

class ReblooooomLineageTracker:
    """
    Tracks memory lineage and ancestry patterns for DAWN's cognitive system.
    
    Maintains a graph of how memory chunks evolve, enabling:
    - Ancestry-aware forecasting
    - Deep memory pattern analysis
    - Semantic family tree visualization
    - Lineage-based significance scoring
    """
    
    def __init__(self, lineage_file: Optional[str] = None):
        """Initialize the lineage tracker"""
        self.lineage_file = Path(lineage_file) if lineage_file else Path("runtime/memory/lineage_log.jsonl")
        self.lineage_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Core data structures
        self.lineage_cache: Dict[str, LineageEntry] = {}  # child_id -> lineage_entry
        self.parent_to_children: Dict[str, List[str]] = defaultdict(list)  # parent_id -> [child_ids]
        self.depth_cache: Dict[str, int] = {}  # chunk_id -> max_depth
        self.significance_cache: Dict[str, float] = {}  # chunk_id -> accumulated_significance
        
        # Statistics tracking
        self.total_lineage_entries = 0
        self.deepest_ancestry_depth = 0
        self.deepest_ancestry_chunk = None
        self.method_counts = defaultdict(int)
        
        # Load existing lineage data
        self._load_lineage_data()
        
        logger.info(f"🌳 ReblooooomLineageTracker initialized with {len(self.lineage_cache)} entries")
    
    def track_lineage(self, parent_chunk: Union[MemoryChunk, str], 
                     rebloomed_chunk: Union[MemoryChunk, str],
                     method: str = "semantic_retrieval",
                     significance: float = 0.5) -> str:
        """
        Track a new lineage relationship between parent and rebloomed chunk.
        
        Args:
            parent_chunk: The parent memory chunk or ID
            rebloomed_chunk: The newly rebloomed memory chunk or ID
            method: How the rebloom occurred ('semantic_retrieval', 'sigil_triggered', etc.)
            significance: Significance score of this lineage connection (0.0-1.0)
        
        Returns:
            lineage_id: Unique identifier for this lineage entry
        """
        # Extract IDs
        parent_id = parent_chunk.id if hasattr(parent_chunk, 'id') else str(parent_chunk)
        child_id = rebloomed_chunk.id if hasattr(rebloomed_chunk, 'id') else str(rebloomed_chunk)
        
        # Calculate depth
        parent_depth = self.get_ancestry_depth(parent_id)
        child_depth = parent_depth + 1
        
        # Create lineage entry
        lineage_entry = LineageEntry(
            child_id=child_id,
            parent_id=parent_id,
            method=method,
            depth=child_depth,
            significance=significance
        )
        
        # Update caches
        self.lineage_cache[child_id] = lineage_entry
        self.parent_to_children[parent_id].append(child_id)
        self.depth_cache[child_id] = child_depth
        self.significance_cache[child_id] = significance
        
        # Update statistics
        self.total_lineage_entries += 1
        self.method_counts[method] += 1
        
        if child_depth > self.deepest_ancestry_depth:
            self.deepest_ancestry_depth = child_depth
            self.deepest_ancestry_chunk = child_id
        
        # Log to file
        self._log_lineage_entry(lineage_entry)
        
        lineage_id = f"lineage_{child_id}_{int(time.time())}"
        
        logger.info(f"🌿 Tracked lineage: {parent_id} -> {child_id} via {method} (depth: {child_depth})")
        
        return lineage_id
    
    def get_ancestry(self, chunk_id: str, max_depth: int = 50) -> List[Dict[str, Any]]:
        """
        Get the ancestry lineage for a memory chunk.
        
        Args:
            chunk_id: The memory chunk ID to trace
            max_depth: Maximum ancestry depth to traverse
        
        Returns:
            List of ancestry entries from oldest to newest
        """
        ancestry = []
        current_id = chunk_id
        depth = 0
        
        while current_id in self.lineage_cache and depth < max_depth:
            lineage_entry = self.lineage_cache[current_id]
            ancestry.append(lineage_entry.to_dict())
            current_id = lineage_entry.parent_id
            depth += 1
        
        # Return in chronological order (oldest first)
        return list(reversed(ancestry))
    
    def get_ancestry_depth(self, chunk_id: str) -> int:
        """Get the ancestry depth for a memory chunk"""
        if chunk_id in self.depth_cache:
            return self.depth_cache[chunk_id]
        
        # Calculate depth by traversing ancestry
        depth = 0
        current_id = chunk_id
        visited = set()
        
        while current_id in self.lineage_cache and current_id not in visited:
            visited.add(current_id)
            lineage_entry = self.lineage_cache[current_id]
            current_id = lineage_entry.parent_id
            depth += 1
            
            # Prevent infinite loops
            if depth > 100:
                break
        
        # Cache the result
        self.depth_cache[chunk_id] = depth
        return depth
    
    def get_children(self, parent_id: str) -> List[str]:
        """Get all direct children of a memory chunk"""
        return self.parent_to_children.get(parent_id, [])
    
    def get_descendants(self, ancestor_id: str, max_depth: int = 10) -> List[str]:
        """Get all descendants of a memory chunk up to max_depth"""
        descendants = []
        to_visit = deque([(ancestor_id, 0)])
        visited = set()
        
        while to_visit:
            current_id, depth = to_visit.popleft()
            
            if current_id in visited or depth >= max_depth:
                continue
            
            visited.add(current_id)
            children = self.get_children(current_id)
            
            for child_id in children:
                descendants.append(child_id)
                to_visit.append((child_id, depth + 1))
        
        return descendants
    
    def find_common_ancestor(self, chunk_id_a: str, chunk_id_b: str) -> Optional[str]:
        """Find the most recent common ancestor of two memory chunks"""
        ancestry_a = set(entry['parent_id'] for entry in self.get_ancestry(chunk_id_a))
        ancestry_b = set(entry['parent_id'] for entry in self.get_ancestry(chunk_id_b))
        
        # Find intersection
        common_ancestors = ancestry_a.intersection(ancestry_b)
        
        if not common_ancestors:
            return None
        
        # Return the one with the greatest depth (most recent)
        best_ancestor = None
        best_depth = -1
        
        for ancestor_id in common_ancestors:
            depth = self.get_ancestry_depth(ancestor_id)
            if depth > best_depth:
                best_depth = depth
                best_ancestor = ancestor_id
        
        return best_ancestor
    
    def get_lineage_stats_for_chunk(self, chunk_id: str) -> Dict[str, Any]:
        """Get detailed lineage statistics for a specific chunk"""
        ancestry = self.get_ancestry(chunk_id)
        children = self.get_children(chunk_id)
        descendants = self.get_descendants(chunk_id)
        
        return {
            'chunk_id': chunk_id,
            'ancestry_depth': len(ancestry),
            'direct_children': len(children),
            'total_descendants': len(descendants),
            'lineage_methods': [entry['method'] for entry in ancestry],
            'significance_scores': [entry['significance'] for entry in ancestry],
            'avg_significance': sum(entry['significance'] for entry in ancestry) / len(ancestry) if ancestry else 0.0,
            'creation_path': [entry['parent_id'] for entry in ancestry] + [chunk_id]
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get overall lineage tracker statistics"""
        return {
            'total_lineage_entries': self.total_lineage_entries,
            'unique_chunks_tracked': len(self.lineage_cache),
            'deepest_ancestry_depth': self.deepest_ancestry_depth,
            'deepest_ancestry_chunk': self.deepest_ancestry_chunk,
            'method_distribution': dict(self.method_counts),
            'avg_significance': sum(self.significance_cache.values()) / len(self.significance_cache) if self.significance_cache else 0.0,
            'lineage_file_size': self.lineage_file.stat().st_size if self.lineage_file.exists() else 0
        }
    
    def export_lineage_graph(self) -> Dict[str, Any]:
        """Export lineage data as a graph structure for visualization"""
        nodes = []
        edges = []
        
        # Create nodes
        all_chunks = set(self.lineage_cache.keys())
        for parent_id in self.parent_to_children.keys():
            all_chunks.add(parent_id)
        
        for chunk_id in all_chunks:
            depth = self.get_ancestry_depth(chunk_id)
            significance = self.significance_cache.get(chunk_id, 0.5)
            
            nodes.append({
                'id': chunk_id,
                'depth': depth,
                'significance': significance,
                'children_count': len(self.get_children(chunk_id))
            })
        
        # Create edges
        for child_id, lineage_entry in self.lineage_cache.items():
            edges.append({
                'from': lineage_entry.parent_id,
                'to': child_id,
                'method': lineage_entry.method,
                'significance': lineage_entry.significance,
                'depth': lineage_entry.depth
            })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'metadata': {
                'total_nodes': len(nodes),
                'total_edges': len(edges),
                'max_depth': self.deepest_ancestry_depth,
                'export_time': datetime.now().isoformat()
            }
        }
    
    def _load_lineage_data(self):
        """Load existing lineage data from file"""
        if not self.lineage_file.exists():
            return
        
        try:
            with open(self.lineage_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            entry_data = json.loads(line.strip())
                            self._process_loaded_entry(entry_data)
                        except json.JSONDecodeError:
                            continue
            
            logger.info(f"📂 Loaded {len(self.lineage_cache)} lineage entries from {self.lineage_file}")
            
        except Exception as e:
            logger.error(f"Error loading lineage data: {e}")
    
    def _process_loaded_entry(self, entry_data: Dict[str, Any]):
        """Process a loaded lineage entry and update caches"""
        lineage_entry = LineageEntry(
            child_id=entry_data['child_id'],
            parent_id=entry_data['parent_id'],
            method=entry_data['method'],
            depth=entry_data.get('depth', 0),
            significance=entry_data.get('significance', 0.5)
        )
        lineage_entry.timestamp = entry_data.get('timestamp', time.time())
        lineage_entry.datetime = entry_data.get('datetime', datetime.now().isoformat())
        
        # Update caches
        child_id = lineage_entry.child_id
        parent_id = lineage_entry.parent_id
        
        self.lineage_cache[child_id] = lineage_entry
        self.parent_to_children[parent_id].append(child_id)
        self.depth_cache[child_id] = lineage_entry.depth
        self.significance_cache[child_id] = lineage_entry.significance
        
        # Update statistics
        self.total_lineage_entries += 1
        self.method_counts[lineage_entry.method] += 1
        
        if lineage_entry.depth > self.deepest_ancestry_depth:
            self.deepest_ancestry_depth = lineage_entry.depth
            self.deepest_ancestry_chunk = child_id
    
    def _log_lineage_entry(self, lineage_entry: LineageEntry):
        """Log a lineage entry to the persistent file"""
        try:
            with open(self.lineage_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(lineage_entry.to_dict()) + '\n')
        except Exception as e:
            logger.error(f"Error logging lineage entry: {e}")

# Global instance for easy access
_default_tracker = None

def get_default_tracker() -> ReblooooomLineageTracker:
    """Get or create the default lineage tracker instance"""
    global _default_tracker
    if _default_tracker is None:
        _default_tracker = ReblooooomLineageTracker()
    return _default_tracker

def track_rebloom_lineage(parent_chunk: Union[MemoryChunk, str], 
                         rebloomed_chunk: Union[MemoryChunk, str],
                         method: str = "semantic_retrieval") -> str:
    """Convenience function to track lineage using the default tracker"""
    tracker = get_default_tracker()
    return tracker.track_lineage(parent_chunk, rebloomed_chunk, method)

def get_chunk_ancestry(chunk_id: str) -> List[Dict[str, Any]]:
    """Convenience function to get ancestry using the default tracker"""
    tracker = get_default_tracker()
    return tracker.get_ancestry(chunk_id)

def get_lineage_statistics() -> Dict[str, Any]:
    """Convenience function to get statistics using the default tracker"""
    tracker = get_default_tracker()
    return tracker.get_statistics()

# Demo and testing
if __name__ == "__main__":
    print("🌳 Testing DAWN Rebloom Lineage Tracker")
    print("=" * 50)
    
    # Create test tracker
    tracker = ReblooooomLineageTracker("test_lineage.jsonl")
    
    # Create some test lineage
    test_chunks = [
        ("root_memory", "child_1", "semantic_retrieval"),
        ("child_1", "child_2", "sigil_triggered"),
        ("child_2", "child_3", "semantic_retrieval"),
        ("child_1", "sibling_1", "manual"),
        ("sibling_1", "grandchild_1", "semantic_retrieval")
    ]
    
    for parent, child, method in test_chunks:
        tracker.track_lineage(parent, child, method, significance=0.7)
    
    # Test ancestry retrieval
    print(f"\nAncestry of 'grandchild_1':")
    ancestry = tracker.get_ancestry("grandchild_1")
    for entry in ancestry:
        print(f"  {entry['parent_id']} -> {entry['child_id']} via {entry['method']}")
    
    # Test statistics
    print(f"\nLineage Statistics:")
    stats = tracker.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test common ancestor
    common = tracker.find_common_ancestor("child_3", "grandchild_1")
    print(f"\nCommon ancestor of child_3 and grandchild_1: {common}")
    
    # Export graph
    graph = tracker.export_lineage_graph()
    print(f"\nLineage graph: {graph['metadata']['total_nodes']} nodes, {graph['metadata']['total_edges']} edges")
    
    print(f"\n✅ Rebloom lineage tracker test complete!") 