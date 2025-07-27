#!/usr/bin/env python3
"""
DAWN Mycelium Graph Export - Semantic Thread Router
===================================================

Exports visualizable JSON graph of memory chunk linkages and
semantic routing patterns detected by the mycelium layer.

Called from connect_chunks(...) with current rebloom semantic pairings.
Powers future GUIs like MyceliumOverlay.tsx or memory lineage graphs.
"""

import json
import os
import time
from typing import Dict, Any, List, Tuple, Set
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Ensure export directory exists
MYCELIUM_GRAPH_PATH = Path("runtime/memory/mycelium_graph.json")
MYCELIUM_GRAPH_PATH.parent.mkdir(parents=True, exist_ok=True)

SEMANTIC_ROUTING_LOG = Path("runtime/logs/semantic_routing.log")
SEMANTIC_ROUTING_LOG.parent.mkdir(parents=True, exist_ok=True)

class MyceliumGraphExporter:
    """
    Manages semantic thread routing and graph export for memory connections.
    
    Tracks mycelium layer connections and exports them as visualizable graphs
    for GUI components and analysis tools.
    """
    
    def __init__(self):
        self.connection_history = []
        self.semantic_clusters = {}
        self.routing_metrics = {
            'total_connections': 0,
            'unique_nodes': set(),
            'cluster_count': 0,
            'last_export': None
        }
    
    def export_mycelium_graph(self, connections: List[Tuple[str, str]], 
                             metadata: Dict[str, Any] = None) -> None:
        """
        Export mycelium connections as a visualizable JSON graph.
        
        Args:
            connections: List of (source, destination) connection tuples
            metadata: Optional metadata about the connections
        """
        if not connections:
            return
        
        # Extract nodes from connections
        all_nodes = set()
        for src, dst in connections:
            all_nodes.add(src)
            all_nodes.add(dst)
        
        # Build node data with metadata
        nodes = []
        for node_id in all_nodes:
            node_data = {
                "id": node_id,
                "label": node_id,
                "type": self._classify_node_type(node_id),
                "connections": len([c for c in connections if node_id in c]),
                "timestamp": time.time()
            }
            
            # Add semantic metadata if available
            if metadata and node_id in metadata:
                node_data.update(metadata[node_id])
            
            nodes.append(node_data)
        
        # Build edge data
        edges = []
        for i, (src, dst) in enumerate(connections):
            edge_data = {
                "id": f"edge_{i}",
                "from": src,
                "to": dst,
                "type": "semantic_link",
                "weight": 1.0,
                "timestamp": time.time()
            }
            
            # Add connection strength if available
            if metadata and 'edge_weights' in metadata:
                edge_weights = metadata['edge_weights']
                if i < len(edge_weights):
                    edge_data['weight'] = edge_weights[i]
            
            edges.append(edge_data)
        
        # Build complete graph
        graph = {
            "metadata": {
                "export_time": datetime.now().isoformat(),
                "timestamp": time.time(),
                "node_count": len(nodes),
                "edge_count": len(edges),
                "density": len(edges) / (len(nodes) * (len(nodes) - 1)) if len(nodes) > 1 else 0,
                "source": "mycelium_layer"
            },
            "nodes": nodes,
            "edges": edges,
            "clusters": self._detect_clusters(connections),
            "routing_paths": self._calculate_routing_paths(connections)
        }
        
        # Export to JSON
        try:
            with open(MYCELIUM_GRAPH_PATH, "w", encoding='utf-8') as f:
                json.dump(graph, f, indent=2)
            
            # Update metrics
            self.routing_metrics['total_connections'] += len(connections)
            self.routing_metrics['unique_nodes'].update(all_nodes)
            self.routing_metrics['cluster_count'] = len(graph['clusters'])
            self.routing_metrics['last_export'] = time.time()
            
            print(f"🧬 Mycelium graph exported: {len(nodes)} nodes, {len(edges)} edges")
            
            # Log the export event
            self._log_routing_event("GRAPH_EXPORT", {
                "node_count": len(nodes),
                "edge_count": len(edges),
                "cluster_count": len(graph['clusters']),
                "density": graph['metadata']['density']
            })
            
        except Exception as e:
            print(f"⚠️ Error exporting mycelium graph: {e}")
    
    def connect_chunks(self, chunk_pairs: List[Tuple[str, str]], 
                      connection_type: str = "rebloom") -> None:
        """
        Process chunk connections and update the semantic graph.
        
        Args:
            chunk_pairs: List of (chunk_id_a, chunk_id_b) semantic connections
            connection_type: Type of connection ('rebloom', 'semantic', 'temporal')
        """
        if not chunk_pairs:
            return
        
        # Store connection history
        connection_event = {
            'timestamp': time.time(),
            'type': connection_type,
            'connections': chunk_pairs,
            'count': len(chunk_pairs)
        }
        
        self.connection_history.append(connection_event)
        
        # Export updated graph
        self.export_mycelium_graph(chunk_pairs, {
            'connection_type': connection_type,
            'batch_size': len(chunk_pairs)
        })
        
        # Log the connection event
        self._log_routing_event("CHUNK_CONNECTION", {
            "connection_type": connection_type,
            "pair_count": len(chunk_pairs),
            "chunk_ids": [pair[0] for pair in chunk_pairs[:5]]  # Sample
        })
        
        print(f"🌿 Connected {len(chunk_pairs)} chunk pairs via {connection_type}")
    
    def _classify_node_type(self, node_id: str) -> str:
        """Classify node type based on ID pattern"""
        if node_id.startswith('memory_'):
            return 'memory_chunk'
        elif node_id.startswith('root://'):
            return 'mycelium_root'
        elif node_id.startswith('rebloom_'):
            return 'rebloom_node'
        elif 'consciousness' in node_id.lower():
            return 'consciousness_node'
        else:
            return 'generic_node'
    
    def _detect_clusters(self, connections: List[Tuple[str, str]]) -> List[Dict[str, Any]]:
        """Detect semantic clusters in the connection graph"""
        if not connections:
            return []
        
        # Build adjacency list
        adjacency = defaultdict(set)
        for src, dst in connections:
            adjacency[src].add(dst)
            adjacency[dst].add(src)
        
        # Simple clustering: find connected components
        visited = set()
        clusters = []
        
        def dfs_cluster(node, cluster):
            if node in visited:
                return
            visited.add(node)
            cluster.append(node)
            for neighbor in adjacency[node]:
                dfs_cluster(neighbor, cluster)
        
        for node in adjacency:
            if node not in visited:
                cluster = []
                dfs_cluster(node, cluster)
                if len(cluster) >= 2:  # Only clusters with 2+ nodes
                    clusters.append({
                        'id': f'cluster_{len(clusters)}',
                        'nodes': cluster,
                        'size': len(cluster),
                        'density': len([c for c in connections if c[0] in cluster and c[1] in cluster]) / (len(cluster) * (len(cluster) - 1)) if len(cluster) > 1 else 0
                    })
        
        return clusters
    
    def _calculate_routing_paths(self, connections: List[Tuple[str, str]]) -> List[Dict[str, Any]]:
        """Calculate important routing paths in the semantic network"""
        if not connections:
            return []
        
        # Build adjacency list
        adjacency = defaultdict(list)
        for src, dst in connections:
            adjacency[src].append(dst)
        
        # Find paths between high-degree nodes
        node_degrees = defaultdict(int)
        for src, dst in connections:
            node_degrees[src] += 1
            node_degrees[dst] += 1
        
        # Get top nodes by degree
        top_nodes = sorted(node_degrees.items(), key=lambda x: x[1], reverse=True)[:5]
        
        routing_paths = []
        for i, (node_a, _) in enumerate(top_nodes):
            for node_b, _ in top_nodes[i+1:]:
                path = self._find_shortest_path(adjacency, node_a, node_b)
                if path and len(path) > 1:
                    routing_paths.append({
                        'from': node_a,
                        'to': node_b,
                        'path': path,
                        'length': len(path) - 1,
                        'importance': (node_degrees[node_a] + node_degrees[node_b]) / 2
                    })
        
        return sorted(routing_paths, key=lambda x: x['importance'], reverse=True)[:10]
    
    def _find_shortest_path(self, adjacency: Dict, start: str, end: str, max_depth: int = 5) -> List[str]:
        """Find shortest path between two nodes using BFS"""
        if start == end:
            return [start]
        
        from collections import deque
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            node, path = queue.popleft()
            
            if len(path) > max_depth:
                continue
            
            for neighbor in adjacency[node]:
                if neighbor == end:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return []  # No path found
    
    def _log_routing_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log semantic routing events"""
        event = {
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat(),
            'type': event_type,
            'data': data
        }
        
        try:
            with open(SEMANTIC_ROUTING_LOG, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            print(f"⚠️ Error logging routing event: {e}")
    
    def get_routing_metrics(self) -> Dict[str, Any]:
        """Get current routing metrics"""
        return {
            'total_connections': self.routing_metrics['total_connections'],
            'unique_nodes': len(self.routing_metrics['unique_nodes']),
            'cluster_count': self.routing_metrics['cluster_count'],
            'last_export': self.routing_metrics['last_export'],
            'connection_history_size': len(self.connection_history),
            'graph_file_exists': MYCELIUM_GRAPH_PATH.exists(),
            'graph_file_size': MYCELIUM_GRAPH_PATH.stat().st_size if MYCELIUM_GRAPH_PATH.exists() else 0
        }
    
    def export_routing_summary(self) -> Dict[str, Any]:
        """Export comprehensive routing summary"""
        summary = {
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat(),
            'metrics': self.get_routing_metrics(),
            'recent_connections': self.connection_history[-10:] if self.connection_history else [],
            'semantic_clusters': len(self.semantic_clusters),
            'routing_health': 'healthy' if self.routing_metrics['total_connections'] > 0 else 'inactive'
        }
        
        # Export summary
        summary_path = Path("runtime/memory/routing_summary.json")
        try:
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error exporting routing summary: {e}")
        
        return summary

# Global exporter instance
_mycelium_exporter = None

def get_mycelium_exporter() -> MyceliumGraphExporter:
    """Get or create the global mycelium exporter"""
    global _mycelium_exporter
    if _mycelium_exporter is None:
        _mycelium_exporter = MyceliumGraphExporter()
    return _mycelium_exporter

def export_mycelium_graph(connections: List[Tuple[str, str]], metadata: Dict[str, Any] = None) -> None:
    """Convenience function to export mycelium graph"""
    exporter = get_mycelium_exporter()
    exporter.export_mycelium_graph(connections, metadata)

def connect_chunks(chunk_pairs: List[Tuple[str, str]], connection_type: str = "rebloom") -> None:
    """Convenience function to connect chunks"""
    exporter = get_mycelium_exporter()
    exporter.connect_chunks(chunk_pairs, connection_type)

# Sample usage and testing
if __name__ == "__main__":
    print("🧬 Testing Mycelium Graph Export")
    print("=" * 40)
    
    # Create sample connections
    sample_connections = [
        ("memory_001", "memory_002"),
        ("memory_002", "memory_003"),
        ("memory_003", "memory_004"),
        ("memory_001", "memory_004"),
        ("root://myc_001", "memory_002"),
        ("consciousness_core", "memory_001")
    ]
    
    # Test export
    exporter = MyceliumGraphExporter()
    exporter.export_mycelium_graph(sample_connections)
    
    # Test chunk connections
    chunk_pairs = [
        ("chunk_a", "chunk_b"),
        ("chunk_b", "chunk_c")
    ]
    exporter.connect_chunks(chunk_pairs, "semantic")
    
    # Show metrics
    metrics = exporter.get_routing_metrics()
    print(f"\nRouting Metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    # Export summary
    summary = exporter.export_routing_summary()
    print(f"\n✅ Routing summary exported")
    print(f"✅ Graph file: {MYCELIUM_GRAPH_PATH}")
    print(f"✅ Routing log: {SEMANTIC_ROUTING_LOG}") 