"""
KAN Topology Manager

Manages the network structure and connections for the KAN-Cairrn system.
"""

import numpy as np
import networkx as nx
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging

from ..models import KANTopology, SplineNeuron, KANConfig


class KANTopologyManager:
    """Manager for KAN network topology and connections"""
    
    def __init__(self, config: KANConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.topology: Optional[KANTopology] = None
    
    def create_topology(self, initial_neurons: Dict[str, SplineNeuron] = None) -> KANTopology:
        """Create a new KAN topology"""
        
        # Initialize connection graph
        connection_graph = nx.DiGraph()
        
        # Add initial neurons to graph
        if initial_neurons:
            for neuron_id in initial_neurons.keys():
                connection_graph.add_node(neuron_id)
        
        # Create thread routing matrix
        total_neurons = len(initial_neurons) if initial_neurons else sum(self.config.neurons_per_layer)
        thread_routing_matrix = self._create_routing_matrix(total_neurons)
        
        # Create topology
        self.topology = KANTopology(
            spline_neurons=initial_neurons or {},
            connection_graph=connection_graph,
            thread_routing_matrix=thread_routing_matrix,
            global_entropy=0.5,
            entropy_threshold=self.config.sparse_threshold
        )
        
        self.logger.info(f"Created KAN topology with {len(self.topology.spline_neurons)} neurons")
        return self.topology
    
    def _create_routing_matrix(self, size: int) -> np.ndarray:
        """Create thread routing matrix for spline connections"""
        
        # Initialize with small random weights
        matrix = np.random.normal(0, 0.1, (size, size))
        
        # Apply sparsity threshold
        mask = np.abs(matrix) < self.config.sparse_threshold
        matrix[mask] = 0
        
        # Normalize rows
        row_sums = np.sum(np.abs(matrix), axis=1, keepdims=True)
        matrix = np.divide(matrix, row_sums, out=np.zeros_like(matrix), where=(row_sums != 0))
        
        return matrix
    
    def add_neuron(self, neuron_id: str, neuron: SplineNeuron) -> bool:
        """Add a neuron to the topology"""
        
        if not self.topology:
            self.logger.error("Topology not initialized")
            return False
        
        if neuron_id in self.topology.spline_neurons:
            self.logger.warning(f"Neuron {neuron_id} already exists")
            return False
        
        # Add to neurons dict
        self.topology.spline_neurons[neuron_id] = neuron
        
        # Add to connection graph
        self.topology.connection_graph.add_node(neuron_id)
        
        # Expand routing matrix if needed
        current_size = self.topology.thread_routing_matrix.shape[0]
        new_size = len(self.topology.spline_neurons)
        
        if new_size > current_size:
            self._expand_routing_matrix(new_size)
        
        self.logger.info(f"Added neuron {neuron_id} to topology")
        return True
    
    def remove_neuron(self, neuron_id: str) -> bool:
        """Remove a neuron from the topology"""
        
        if not self.topology or neuron_id not in self.topology.spline_neurons:
            return False
        
        # Remove from neurons dict
        del self.topology.spline_neurons[neuron_id]
        
        # Remove from connection graph
        self.topology.connection_graph.remove_node(neuron_id)
        
        self.logger.info(f"Removed neuron {neuron_id} from topology")
        return True
    
    def add_connection(self, source_id: str, target_id: str, weight: float = 0.5) -> bool:
        """Add a connection between neurons"""
        
        if not self.topology:
            return False
        
        if source_id not in self.topology.spline_neurons or target_id not in self.topology.spline_neurons:
            self.logger.error(f"Cannot connect {source_id} -> {target_id}: neurons not found")
            return False
        
        # Add edge to connection graph
        self.topology.connection_graph.add_edge(source_id, target_id, weight=weight)
        
        self.logger.debug(f"Added connection {source_id} -> {target_id} (weight: {weight})")
        return True
    
    def _expand_routing_matrix(self, new_size: int):
        """Expand the routing matrix to accommodate new neurons"""
        
        current_matrix = self.topology.thread_routing_matrix
        current_size = current_matrix.shape[0]
        
        if new_size <= current_size:
            return
        
        # Create new larger matrix
        new_matrix = np.zeros((new_size, new_size))
        
        # Copy existing values
        new_matrix[:current_size, :current_size] = current_matrix
        
        # Fill new entries with small random values
        new_entries = np.random.normal(0, 0.01, (new_size, new_size))
        new_matrix[current_size:, :] = new_entries[current_size:, :]
        new_matrix[:, current_size:] = new_entries[:, current_size:]
        
        # Apply sparsity
        mask = np.abs(new_matrix) < self.config.sparse_threshold
        new_matrix[mask] = 0
        
        self.topology.thread_routing_matrix = new_matrix
    
    def get_neuron_connections(self, neuron_id: str) -> Dict[str, float]:
        """Get all connections for a specific neuron"""
        
        if not self.topology or neuron_id not in self.topology.spline_neurons:
            return {}
        
        connections = {}
        
        # Outgoing connections
        for target, edge_data in self.topology.connection_graph[neuron_id].items():
            connections[target] = edge_data.get('weight', 0.0)
        
        return connections
    
    def get_topology_stats(self) -> Dict[str, Any]:
        """Get statistics about the current topology"""
        
        if not self.topology:
            return {"error": "Topology not initialized"}
        
        graph = self.topology.connection_graph
        
        stats = {
            "total_neurons": len(self.topology.spline_neurons),
            "total_connections": graph.number_of_edges(),
            "global_entropy": self.topology.global_entropy,
            "matrix_size": self.topology.thread_routing_matrix.shape,
            "connectivity_density": graph.number_of_edges() / max(1, graph.number_of_nodes() ** 2),
            "average_degree": sum(dict(graph.degree()).values()) / max(1, graph.number_of_nodes()),
            "last_updated": self.topology.last_updated.isoformat()
        }
        
        # Network analysis
        if graph.number_of_nodes() > 0:
            try:
                # Convert to undirected for some metrics
                undirected = graph.to_undirected()
                
                if nx.is_connected(undirected):
                    stats["average_path_length"] = nx.average_shortest_path_length(undirected)
                    stats["diameter"] = nx.diameter(undirected)
                
                stats["clustering_coefficient"] = nx.average_clustering(undirected)
                
            except Exception as e:
                self.logger.debug(f"Network analysis failed: {e}")
        
        return stats
    
    def optimize_connections(self, pruning_threshold: float = 0.01) -> int:
        """Optimize connections by removing weak edges"""
        
        if not self.topology:
            return 0
        
        edges_to_remove = []
        
        # Find weak connections
        for source, target, data in self.topology.connection_graph.edges(data=True):
            weight = data.get('weight', 0.0)
            if abs(weight) < pruning_threshold:
                edges_to_remove.append((source, target))
        
        # Remove weak connections
        for source, target in edges_to_remove:
            self.topology.connection_graph.remove_edge(source, target)
        
        self.logger.info(f"Optimized topology: removed {len(edges_to_remove)} weak connections")
        return len(edges_to_remove)
    
    def visualize_topology(self) -> Dict[str, Any]:
        """Generate visualization data for the topology"""
        
        if not self.topology:
            return {"error": "Topology not initialized"}
        
        graph = self.topology.connection_graph
        
        # Node data
        nodes = []
        for node_id in graph.nodes():
            neuron = self.topology.spline_neurons.get(node_id)
            
            node_data = {
                "id": node_id,
                "entropy": neuron.entropy_level if neuron else 0.5,
                "access_count": neuron.access_count if neuron else 0,
                "features": neuron.input_features if neuron else []
            }
            nodes.append(node_data)
        
        # Edge data
        edges = []
        for source, target, data in graph.edges(data=True):
            edge_data = {
                "source": source,
                "target": target,
                "weight": data.get('weight', 0.0)
            }
            edges.append(edge_data)
        
        return {
            "nodes": nodes,
            "edges": edges,
            "stats": self.get_topology_stats(),
            "timestamp": datetime.now().isoformat()
        } 