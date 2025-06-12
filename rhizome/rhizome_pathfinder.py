#!/usr/bin/env python3
"""
Rhizome Pathfinder - Graph-based pathfinding for DAWN's interconnected systems
Implements various pathfinding algorithms for navigating the rhizome network
"""

import heapq
import math
from typing import Dict, List, Tuple, Optional, Set, Any, Callable, Union
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum
import json
import time
import numpy as np
from pathlib import Path

class PathfindingAlgorithm(Enum):
    """Available pathfinding algorithms"""
    DIJKSTRA = "dijkstra"
    A_STAR = "a_star"
    BFS = "breadth_first"
    DFS = "depth_first"
    BEAM_SEARCH = "beam_search"
    BIDIRECTIONAL = "bidirectional"
    QUANTUM = "quantum"  # For consciousness-aware pathfinding

@dataclass
class Node:
    """Represents a node in the rhizome network"""
    id: str
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)  # 3D position
    data: Dict[str, Any] = field(default_factory=dict)
    connections: Set[str] = field(default_factory=set)
    weight: float = 1.0
    tags: Set[str] = field(default_factory=set)
    
    def distance_to(self, other: 'Node') -> float:
        """Calculate Euclidean distance to another node"""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(self.position, other.position)))

@dataclass
class Edge:
    """Represents an edge in the rhizome network"""
    source: str
    target: str
    weight: float = 1.0
    data: Dict[str, Any] = field(default_factory=dict)
    bidirectional: bool = True
    tags: Set[str] = field(default_factory=set)

@dataclass
class Path:
    """Represents a path through the rhizome"""
    nodes: List[str]
    edges: List[Edge]
    total_cost: float
    algorithm: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __len__(self) -> int:
        return len(self.nodes)
    
    def is_valid(self) -> bool:
        """Check if path is valid (has at least start and end)"""
        return len(self.nodes) >= 2

class RhizomeNetwork:
    """The rhizome network structure"""
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[Tuple[str, str], Edge] = {}
        self.adjacency: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.reverse_adjacency: Dict[str, Dict[str, float]] = defaultdict(dict)
        
    def add_node(self, node: Node) -> None:
        """Add a node to the network"""
        self.nodes[node.id] = node
        
    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the network"""
        # Add nodes if they don't exist
        if edge.source not in self.nodes:
            self.nodes[edge.source] = Node(id=edge.source)
        if edge.target not in self.nodes:
            self.nodes[edge.target] = Node(id=edge.target)
            
        # Add edge
        self.edges[(edge.source, edge.target)] = edge
        self.adjacency[edge.source][edge.target] = edge.weight
        self.reverse_adjacency[edge.target][edge.source] = edge.weight
        
        # Add reverse edge if bidirectional
        if edge.bidirectional:
            reverse_edge = Edge(
                source=edge.target,
                target=edge.source,
                weight=edge.weight,
                data=edge.data,
                bidirectional=False
            )
            self.edges[(edge.target, edge.source)] = reverse_edge
            self.adjacency[edge.target][edge.source] = edge.weight
            self.reverse_adjacency[edge.source][edge.target] = edge.weight
            
        # Update node connections
        self.nodes[edge.source].connections.add(edge.target)
        if edge.bidirectional:
            self.nodes[edge.target].connections.add(edge.source)
    
    def get_neighbors(self, node_id: str) -> List[Tuple[str, float]]:
        """Get neighboring nodes and edge weights"""
        return [(target, weight) for target, weight in self.adjacency.get(node_id, {}).items()]
    
    def get_edge(self, source: str, target: str) -> Optional[Edge]:
        """Get edge between two nodes"""
        return self.edges.get((source, target))
    
    def remove_node(self, node_id: str) -> None:
        """Remove a node and all its edges"""
        if node_id not in self.nodes:
            return
            
        # Remove edges
        for neighbor in list(self.adjacency.get(node_id, {}).keys()):
            self.remove_edge(node_id, neighbor)
        for neighbor in list(self.reverse_adjacency.get(node_id, {}).keys()):
            self.remove_edge(neighbor, node_id)
            
        # Remove node
        del self.nodes[node_id]
    
    def remove_edge(self, source: str, target: str) -> None:
        """Remove an edge"""
        if (source, target) in self.edges:
            del self.edges[(source, target)]
        if target in self.adjacency.get(source, {}):
            del self.adjacency[source][target]
        if source in self.reverse_adjacency.get(target, {}):
            del self.reverse_adjacency[target][source]
            
        # Update node connections
        if source in self.nodes and target in self.nodes[source].connections:
            self.nodes[source].connections.remove(target)

class RhizomePathfinder:
    """Pathfinding algorithms for the rhizome network"""
    
    def __init__(self, network: Optional[RhizomeNetwork] = None):
        self.network = network or RhizomeNetwork()
        self.path_cache: Dict[Tuple[str, str, str], Path] = {}
        self.heuristic_cache: Dict[Tuple[str, str], float] = {}
        
    def find_path(self,
                  start: Union[str, Node],
                  goal: Union[str, Node],
                  algorithm: Union[str, PathfindingAlgorithm] = PathfindingAlgorithm.A_STAR,
                  constraints: Optional[Dict[str, Any]] = None,
                  heuristic: Optional[Callable[[str, str], float]] = None) -> Optional[Path]:
        """
        Find a path from start to goal using specified algorithm
        
        Args:
            start: Starting node or node ID
            goal: Goal node or node ID
            algorithm: Pathfinding algorithm to use
            constraints: Optional constraints (max_cost, avoid_nodes, required_tags, etc.)
            heuristic: Optional custom heuristic function for A*
            
        Returns:
            Path object if found, None otherwise
        """
        # Convert to node IDs
        start_id = start.id if isinstance(start, Node) else start
        goal_id = goal.id if isinstance(goal, Node) else goal
        
        # Validate nodes exist
        if start_id not in self.network.nodes or goal_id not in self.network.nodes:
            return None
            
        # Check cache
        cache_key = (start_id, goal_id, str(algorithm))
        if cache_key in self.path_cache and not constraints:
            return self.path_cache[cache_key]
        
        # Convert algorithm string to enum
        if isinstance(algorithm, str):
            algorithm = PathfindingAlgorithm(algorithm)
            
        # Apply constraints
        if constraints:
            network = self._apply_constraints(constraints)
        else:
            network = self.network
            
        # Run appropriate algorithm
        path = None
        start_time = time.time()
        
        if algorithm == PathfindingAlgorithm.DIJKSTRA:
            path = self._dijkstra(start_id, goal_id, network)
        elif algorithm == PathfindingAlgorithm.A_STAR:
            path = self._a_star(start_id, goal_id, network, heuristic)
        elif algorithm == PathfindingAlgorithm.BFS:
            path = self._bfs(start_id, goal_id, network)
        elif algorithm == PathfindingAlgorithm.DFS:
            path = self._dfs(start_id, goal_id, network)
        elif algorithm == PathfindingAlgorithm.BEAM_SEARCH:
            path = self._beam_search(start_id, goal_id, network, beam_width=constraints.get('beam_width', 3) if constraints else 3)
        elif algorithm == PathfindingAlgorithm.BIDIRECTIONAL:
            path = self._bidirectional_search(start_id, goal_id, network)
        elif algorithm == PathfindingAlgorithm.QUANTUM:
            path = self._quantum_pathfinding(start_id, goal_id, network, constraints)
        
        if path:
            path.metadata['computation_time'] = time.time() - start_time
            # Cache the result
            if not constraints:
                self.path_cache[cache_key] = path
                
        return path
    
    def _dijkstra(self, start: str, goal: str, network: RhizomeNetwork) -> Optional[Path]:
        """Dijkstra's shortest path algorithm"""
        distances = {node: float('inf') for node in network.nodes}
        distances[start] = 0
        previous = {}
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
                
            visited.add(current)
            
            if current == goal:
                # Reconstruct path
                path_nodes = []
                path_edges = []
                node = goal
                
                while node in previous:
                    path_nodes.append(node)
                    prev_node = previous[node]
                    edge = network.get_edge(prev_node, node)
                    if edge:
                        path_edges.append(edge)
                    node = prev_node
                    
                path_nodes.append(start)
                path_nodes.reverse()
                path_edges.reverse()
                
                return Path(
                    nodes=path_nodes,
                    edges=path_edges,
                    total_cost=distances[goal],
                    algorithm="dijkstra"
                )
            
            for neighbor, weight in network.get_neighbors(current):
                if neighbor in visited:
                    continue
                    
                distance = current_dist + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))
        
        return None
    
    def _a_star(self, start: str, goal: str, network: RhizomeNetwork, heuristic: Optional[Callable] = None) -> Optional[Path]:
        """A* pathfinding algorithm"""
        if heuristic is None:
            heuristic = self._default_heuristic
            
        open_set = [(0, start)]
        g_score = {node: float('inf') for node in network.nodes}
        g_score[start] = 0
        f_score = {node: float('inf') for node in network.nodes}
        f_score[start] = heuristic(start, goal)
        previous = {}
        open_set_hash = {start}
        
        while open_set:
            current_f, current = heapq.heappop(open_set)
            open_set_hash.remove(current)
            
            if current == goal:
                # Reconstruct path
                path_nodes = []
                path_edges = []
                node = goal
                
                while node in previous:
                    path_nodes.append(node)
                    prev_node = previous[node]
                    edge = network.get_edge(prev_node, node)
                    if edge:
                        path_edges.append(edge)
                    node = prev_node
                    
                path_nodes.append(start)
                path_nodes.reverse()
                path_edges.reverse()
                
                return Path(
                    nodes=path_nodes,
                    edges=path_edges,
                    total_cost=g_score[goal],
                    algorithm="a_star",
                    metadata={'heuristic_calls': len(self.heuristic_cache)}
                )
            
            for neighbor, weight in network.get_neighbors(current):
                tentative_g_score = g_score[current] + weight
                
                if tentative_g_score < g_score[neighbor]:
                    previous[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                    
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)
        
        return None
    
    def _bfs(self, start: str, goal: str, network: RhizomeNetwork) -> Optional[Path]:
        """Breadth-first search"""
        queue = deque([(start, [start], [])])
        visited = {start}
        
        while queue:
            current, path_nodes, path_edges = queue.popleft()
            
            if current == goal:
                total_cost = sum(edge.weight for edge in path_edges)
                return Path(
                    nodes=path_nodes,
                    edges=path_edges,
                    total_cost=total_cost,
                    algorithm="bfs"
                )
            
            for neighbor, weight in network.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    edge = network.get_edge(current, neighbor)
                    new_path_nodes = path_nodes + [neighbor]
                    new_path_edges = path_edges + [edge] if edge else path_edges
                    queue.append((neighbor, new_path_nodes, new_path_edges))
        
        return None
    
    def _dfs(self, start: str, goal: str, network: RhizomeNetwork) -> Optional[Path]:
        """Depth-first search"""
        stack = [(start, [start], [])]
        visited = set()
        
        while stack:
            current, path_nodes, path_edges = stack.pop()
            
            if current in visited:
                continue
                
            visited.add(current)
            
            if current == goal:
                total_cost = sum(edge.weight for edge in path_edges)
                return Path(
                    nodes=path_nodes,
                    edges=path_edges,
                    total_cost=total_cost,
                    algorithm="dfs"
                )
            
            for neighbor, weight in network.get_neighbors(current):
                if neighbor not in visited:
                    edge = network.get_edge(current, neighbor)
                    new_path_nodes = path_nodes + [neighbor]
                    new_path_edges = path_edges + [edge] if edge else path_edges
                    stack.append((neighbor, new_path_nodes, new_path_edges))
        
        return None
    
    def _beam_search(self, start: str, goal: str, network: RhizomeNetwork, beam_width: int = 3) -> Optional[Path]:
        """Beam search algorithm"""
        beam = [(0, start, [start], [])]
        
        while beam:
            next_beam = []
            
            for cost, current, path_nodes, path_edges in beam:
                if current == goal:
                    return Path(
                        nodes=path_nodes,
                        edges=path_edges,
                        total_cost=cost,
                        algorithm="beam_search",
                        metadata={'beam_width': beam_width}
                    )
                
                for neighbor, weight in network.get_neighbors(current):
                    if neighbor not in path_nodes:  # Avoid cycles
                        edge = network.get_edge(current, neighbor)
                        new_cost = cost + weight
                        new_path_nodes = path_nodes + [neighbor]
                        new_path_edges = path_edges + [edge] if edge else path_edges
                        
                        # Heuristic score for beam selection
                        h_score = self._default_heuristic(neighbor, goal)
                        priority = new_cost + h_score
                        
                        next_beam.append((priority, new_cost, neighbor, new_path_nodes, new_path_edges))
            
            # Keep only top beam_width candidates
            next_beam.sort(key=lambda x: x[0])
            beam = [(cost, node, path, edges) for _, cost, node, path, edges in next_beam[:beam_width]]
        
        return None
    
    def _bidirectional_search(self, start: str, goal: str, network: RhizomeNetwork) -> Optional[Path]:
        """Bidirectional search algorithm"""
        # Forward search
        forward_queue = deque([(start, [start], [])])
        forward_visited = {start: ([start], [])}
        
        # Backward search
        backward_queue = deque([(goal, [goal], [])])
        backward_visited = {goal: ([goal], [])}
        
        while forward_queue and backward_queue:
            # Forward step
            if forward_queue:
                current, path_nodes, path_edges = forward_queue.popleft()
                
                if current in backward_visited:
                    # Path found - merge forward and backward paths
                    back_nodes, back_edges = backward_visited[current]
                    
                    # Merge paths
                    merged_nodes = path_nodes[:-1] + back_nodes[::-1]
                    
                    # Calculate total cost
                    total_cost = sum(e.weight for e in path_edges)
                    total_cost += sum(e.weight for e in back_edges)
                    
                    return Path(
                        nodes=merged_nodes,
                        edges=path_edges + back_edges[::-1],
                        total_cost=total_cost,
                        algorithm="bidirectional"
                    )
                
                for neighbor, weight in network.get_neighbors(current):
                    if neighbor not in forward_visited:
                        edge = network.get_edge(current, neighbor)
                        new_path_nodes = path_nodes + [neighbor]
                        new_path_edges = path_edges + [edge] if edge else path_edges
                        forward_visited[neighbor] = (new_path_nodes, new_path_edges)
                        forward_queue.append((neighbor, new_path_nodes, new_path_edges))
            
            # Backward step
            if backward_queue:
                current, path_nodes, path_edges = backward_queue.popleft()
                
                if current in forward_visited:
                    # Path found - merge forward and backward paths
                    fwd_nodes, fwd_edges = forward_visited[current]
                    
                    # Merge paths
                    merged_nodes = fwd_nodes[:-1] + path_nodes[::-1]
                    
                    # Calculate total cost
                    total_cost = sum(e.weight for e in fwd_edges)
                    total_cost += sum(e.weight for e in path_edges)
                    
                    return Path(
                        nodes=merged_nodes,
                        edges=fwd_edges + path_edges[::-1],
                        total_cost=total_cost,
                        algorithm="bidirectional"
                    )
                
                # Use reverse adjacency for backward search
                for neighbor in network.reverse_adjacency.get(current, {}):
                    if neighbor not in backward_visited:
                        edge = network.get_edge(neighbor, current)
                        new_path_nodes = path_nodes + [neighbor]
                        new_path_edges = path_edges + [edge] if edge else path_edges
                        backward_visited[neighbor] = (new_path_nodes, new_path_edges)
                        backward_queue.append((neighbor, new_path_nodes, new_path_edges))
        
        return None
    
    def _quantum_pathfinding(self, start: str, goal: str, network: RhizomeNetwork, constraints: Optional[Dict] = None) -> Optional[Path]:
        """
        Quantum-inspired pathfinding that considers consciousness dimensions
        Uses superposition and entanglement concepts for path exploration
        """
        # Initialize quantum states
        psi = {}  # Wave function for nodes
        entanglement = defaultdict(list)  # Entangled paths
        
        # Initialize all nodes with superposition probability
        for node in network.nodes:
            distance = self._default_heuristic(node, goal)
            # Probability amplitude based on distance to goal
            psi[node] = 1.0 / (1.0 + distance)
        
        # Normalize wave function
        total_prob = sum(p ** 2 for p in psi.values())
        norm_factor = 1.0 / math.sqrt(total_prob)
        psi = {node: prob * norm_factor for node, prob in psi.items()}
        
        # Quantum walk parameters
        iterations = constraints.get('quantum_iterations', 100) if constraints else 100
        coherence = constraints.get('coherence', 0.8) if constraints else 0.8
        
        # Best path tracking
        best_path = None
        best_cost = float('inf')
        
        # Quantum walk
        current_states = {start: ([start], [], 0.0)}  # node: (path_nodes, path_edges, cost)
        
        for iteration in range(iterations):
            next_states = {}
            
            for node, (path_nodes, path_edges, cost) in current_states.items():
                if node == goal:
                    if cost < best_cost:
                        best_cost = cost
                        best_path = Path(
                            nodes=path_nodes,
                            edges=path_edges,
                            total_cost=cost,
                            algorithm="quantum",
                            metadata={
                                'iterations': iteration,
                                'coherence': coherence,
                                'final_probability': psi[goal] ** 2
                            }
                        )
                    continue
                
                # Quantum superposition - explore multiple paths simultaneously
                neighbors = network.get_neighbors(node)
                if not neighbors:
                    continue
                
                # Calculate transition probabilities
                transition_probs = []
                for neighbor, weight in neighbors:
                    if neighbor not in path_nodes:  # Avoid loops
                        # Quantum amplitude influenced by edge weight and goal distance
                        amplitude = psi[neighbor] / (1.0 + weight)
                        transition_probs.append((neighbor, weight, amplitude))
                
                # Normalize transition probabilities
                total_amp = sum(amp ** 2 for _, _, amp in transition_probs)
                if total_amp > 0:
                    norm_factor = 1.0 / math.sqrt(total_amp)
                    
                    # Apply quantum transitions
                    for neighbor, weight, amplitude in transition_probs:
                        normalized_amp = amplitude * norm_factor
                        
                        # Decoherence factor
                        if np.random.random() < coherence * normalized_amp ** 2:
                            edge = network.get_edge(node, neighbor)
                            new_path_nodes = path_nodes + [neighbor]
                            new_path_edges = path_edges + [edge] if edge else path_edges
                            new_cost = cost + weight
                            
                            # Quantum interference - combine with existing states
                            if neighbor in next_states:
                                existing_cost = next_states[neighbor][2]
                                if new_cost < existing_cost:
                                    next_states[neighbor] = (new_path_nodes, new_path_edges, new_cost)
                            else:
                                next_states[neighbor] = (new_path_nodes, new_path_edges, new_cost)
            
            current_states = next_states
            
            # Early termination if goal reached with good probability
            if goal in current_states and psi[goal] ** 2 > 0.9:
                break
        
        # Final check for goal in current states
        if goal in current_states:
            path_nodes, path_edges, cost = current_states[goal]
            if cost < best_cost:
                best_path = Path(
                    nodes=path_nodes,
                    edges=path_edges,
                    total_cost=cost,
                    algorithm="quantum",
                    metadata={
                        'iterations': iterations,
                        'coherence': coherence,
                        'final_probability': psi[goal] ** 2
                    }
                )
        
        return best_path
    
    def _default_heuristic(self, node1: str, node2: str) -> float:
        """Default heuristic function using Euclidean distance"""
        cache_key = (node1, node2)
        if cache_key in self.heuristic_cache:
            return self.heuristic_cache[cache_key]
            
        n1 = self.network.nodes.get(node1)
        n2 = self.network.nodes.get(node2)
        
        if n1 and n2:
            distance = n1.distance_to(n2)
        else:
            # Fallback: return large value if nodes don't have positions
            distance = 100.0
            
        self.heuristic_cache[cache_key] = distance
        return distance
    
    def _apply_constraints(self, constraints: Dict[str, Any]) -> RhizomeNetwork:
        """Apply constraints to create a filtered network view"""
        filtered = RhizomeNetwork()
        
        avoid_nodes = set(constraints.get('avoid_nodes', []))
        avoid_edges = set(constraints.get('avoid_edges', []))
        required_tags = set(constraints.get('required_tags', []))
        max_weight = constraints.get('max_edge_weight', float('inf'))
        
        # Copy nodes that meet constraints
        for node_id, node in self.network.nodes.items():
            if node_id in avoid_nodes:
                continue
            if required_tags and not required_tags.intersection(node.tags):
                continue
            filtered.add_node(node)
        
        # Copy edges that meet constraints
        for (source, target), edge in self.network.edges.items():
            if (source, target) in avoid_edges:
                continue
            if source in avoid_nodes or target in avoid_nodes:
                continue
            if edge.weight > max_weight:
                continue
            if required_tags and not required_tags.intersection(edge.tags):
                continue
            filtered.add_edge(edge)
            
        return filtered
    
    def find_all_paths(self,
                      start: str,
                      goal: str,
                      max_paths: int = 10,
                      max_length: Optional[int] = None) -> List[Path]:
        """Find multiple paths from start to goal"""
        paths = []
        
        def dfs_all_paths(current: str, target: str, visited: Set[str], path_nodes: List[str], path_edges: List[Edge], cost: float):
            if len(paths) >= max_paths:
                return
                
            if max_length and len(path_nodes) > max_length:
                return
                
            if current == target:
                paths.append(Path(
                    nodes=path_nodes.copy(),
                    edges=path_edges.copy(),
                    total_cost=cost,
                    algorithm="all_paths"
                ))
                return
            
            for neighbor, weight in self.network.get_neighbors(current):
                if neighbor not in visited:
                    edge = self.network.get_edge(current, neighbor)
                    visited.add(neighbor)
                    path_nodes.append(neighbor)
                    if edge:
                        path_edges.append(edge)
                    
                    dfs_all_paths(neighbor, target, visited, path_nodes, path_edges, cost + weight)
                    
                    # Backtrack
                    visited.remove(neighbor)
                    path_nodes.pop()
                    if edge:
                        path_edges.pop()
        
        dfs_all_paths(start, goal, {start}, [start], [], 0.0)
        
        # Sort by cost
        paths.sort(key=lambda p: p.total_cost)
        
        return paths[:max_paths]
    
    def find_shortest_path(self, start: str, goal: str) -> Optional[Path]:
        """Convenience method to find shortest path using Dijkstra"""
        return self.find_path(start, goal, algorithm=PathfindingAlgorithm.DIJKSTRA)
    
    def find_path_through_nodes(self, nodes: List[str], algorithm: PathfindingAlgorithm = PathfindingAlgorithm.A_STAR) -> Optional[Path]:
        """Find a path that passes through a sequence of nodes"""
        if len(nodes) < 2:
            return None
            
        total_path = Path(nodes=[], edges=[], total_cost=0.0, algorithm=str(algorithm))
        
        # Find path between each consecutive pair
        for i in range(len(nodes) - 1):
            segment = self.find_path(nodes[i], nodes[i + 1], algorithm=algorithm)
            if not segment:
                return None  # No path exists
                
            # Merge segments
            if i == 0:
                total_path.nodes.extend(segment.nodes)
            else:
                total_path.nodes.extend(segment.nodes[1:])  # Skip duplicate node
                
            total_path.edges.extend(segment.edges)
            total_path.total_cost += segment.total_cost
        
        return total_path
    
    def analyze_connectivity(self) -> Dict[str, Any]:
        """Analyze network connectivity properties"""
        analysis = {
            'node_count': len(self.network.nodes),
            'edge_count': len(self.network.edges),
            'average_degree': 0.0,
            'connected_components': 0,
            'diameter': 0,
            'clustering_coefficient': 0.0,
            'isolated_nodes': []
        }
        
        # Calculate average degree
        total_degree = sum(len(node.connections) for node in self.network.nodes.values())
        analysis['average_degree'] = total_degree / len(self.network.nodes) if self.network.nodes else 0
        
        # Find isolated nodes
        for node_id, node in self.network.nodes.items():
            if not node.connections:
                analysis['isolated_nodes'].append(node_id)
        
        # Find connected components using BFS
        visited = set()
        components = []
        
        for start_node in self.network.nodes:
            if start_node not in visited:
                component = set()
                queue = deque([start_node])
                
                while queue:
                    node = queue.popleft()
                    if node in visited:
                        continue
                        
                    visited.add(node)
                    component.add(node)
                    
                    for neighbor, _ in self.network.get_neighbors(node):
                        if neighbor not in visited:
                            queue.append(neighbor)
                
                components.append(component)
        
        analysis['connected_components'] = len(components)
        
        # Calculate diameter (longest shortest path) for largest component
        if components:
            largest_component = max(components, key=len)
            max_distance = 0
            
            for node1 in largest_component:
                for node2 in largest_component:
                    if node1 != node2:
                        path = self.find_shortest_path(node1, node2)
                        if path:
                            max_distance = max(max_distance, len(path) - 1)
            
            analysis['diameter'] = max_distance
        
        return analysis
    
    def export_network(self, filepath: Path) -> None:
        """Export network to JSON file"""
        data = {
            'nodes': [
                {
                    'id': node.id,
                    'position': node.position,
                    'data': node.data,
                    'weight': node.weight,
                    'tags': list(node.tags)
                }
                for node in self.network.nodes.values()
            ],
            'edges': [
                {
                    'source': edge.source,
                    'target': edge.target,
                    'weight': edge.weight,
                    'data': edge.data,
                    'bidirectional': edge.bidirectional,
                    'tags': list(edge.tags)
                }
                for edge in self.network.edges.values()
                if edge.bidirectional or (edge.target, edge.source) not in self.network.edges
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def import_network(self, filepath: Path) -> None:
        """Import network from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        self.network = RhizomeNetwork()
        
        # Import nodes
        for node_data in data.get('nodes', []):
            node = Node(
                id=node_data['id'],
                position=tuple(node_data.get('position', [0, 0, 0])),
                data=node_data.get('data', {}),
                weight=node_data.get('weight', 1.0),
                tags=set(node_data.get('tags', []))
            )
            self.network.add_node(node)
        
        # Import edges
        for edge_data in data.get('edges', []):
            edge = Edge(
                source=edge_data['source'],
                target=edge_data['target'],
                weight=edge_data.get('weight', 1.0),
                data=edge_data.get('data', {}),
                bidirectional=edge_data.get('bidirectional', True),
                tags=set(edge_data.get('tags', []))
            )
            self.network.add_edge(edge)

# Convenience function for direct import
def find_path(start: Union[str, Node],
              goal: Union[str, Node],
              network: Optional[RhizomeNetwork] = None,
              algorithm: str = "a_star",
              **kwargs) -> Optional[Path]:
    """
    Convenience function for finding paths
    
    Args:
        start: Starting node or ID
        goal: Goal node or ID
        network: Optional network (creates empty one if not provided)
        algorithm: Algorithm to use
        **kwargs: Additional arguments passed to pathfinder
        
    Returns:
        Path if found, None otherwise
    """
    pathfinder = RhizomePathfinder(network)
    return pathfinder.find_path(start, goal, algorithm=algorithm, **kwargs)