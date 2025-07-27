"""
Semantic Distance Checker
Evaluates semantic relationships and distances between components for tracer routing.
Uses semantic field mapping and vector similarity to determine semantic proximity.
"""

import json
import os
from typing import Dict, List, Tuple, Optional, Set
import numpy as np
from collections import defaultdict
from datetime import datetime

class SemanticDistance:
    """Manages semantic distances between components in the system."""
    
    def __init__(self, field_map_path: str = "field_map.json", 
                 search_log_path: str = "semantic_searches.json"):
        self.field_map_path = field_map_path
        self.search_log_path = search_log_path
        self.field_map: Dict[str, Dict] = {}
        self.vector_cache: Dict[str, np.ndarray] = {}
        self.distance_cache: Dict[str, float] = {}
        self.cache_size = 1000
        self.search_log = []
        self.load_field_map()
        self.load_search_log()
        
    def load_field_map(self) -> None:
        """Load semantic field map from file."""
        try:
            if os.path.exists(self.field_map_path):
                with open(self.field_map_path, 'r') as f:
                    self.field_map = json.load(f)
                print(f"[SemanticDistance] Loaded field map with {len(self.field_map)} nodes")
            else:
                print("[SemanticDistance] No existing field map found, starting fresh")
                self.field_map = {}
        except Exception as e:
            print(f"[SemanticDistance] Error loading field map: {e}")
            self.field_map = {}
            
    def save_field_map(self) -> None:
        """Save semantic field map to file."""
        try:
            with open(self.field_map_path, 'w') as f:
                json.dump(self.field_map, f, indent=2)
            print(f"[SemanticDistance] Saved field map with {len(self.field_map)} nodes")
        except Exception as e:
            print(f"[SemanticDistance] Error saving field map: {e}")
            
    def load_search_log(self) -> None:
        """Load search log from file."""
        try:
            if os.path.exists(self.search_log_path):
                with open(self.search_log_path, 'r') as f:
                    self.search_log = json.load(f)
                print(f"[SemanticDistance] Loaded {len(self.search_log)} search logs")
            else:
                print("[SemanticDistance] No existing search log found, starting fresh")
                self.search_log = []
        except Exception as e:
            print(f"[SemanticDistance] Error loading search log: {e}")
            self.search_log = []
            
    def save_search_log(self) -> None:
        """Save search log to file."""
        try:
            with open(self.search_log_path, 'w') as f:
                json.dump(self.search_log, f, indent=2)
            print(f"[SemanticDistance] Saved {len(self.search_log)} search logs")
        except Exception as e:
            print(f"[SemanticDistance] Error saving search log: {e}")
            
    def log_search(self, source: str, target: str, distance: float, 
                  path: Optional[List[str]] = None) -> None:
        """Log a semantic search."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'target': target,
            'distance': distance,
            'path': path
        }
        self.search_log.append(log_entry)
        self.save_search_log()
            
    def get_component_vector(self, component: str) -> np.ndarray:
        """
        Get or compute semantic vector for a component.
        
        Args:
            component: Component identifier
            
        Returns:
            np.ndarray: Semantic vector
        """
        if component in self.vector_cache:
            return self.vector_cache[component]
            
        if component not in self.field_map:
            # Create new vector for unknown component
            vector = np.random.randn(100)  # 100-dimensional semantic space
            vector = vector / np.linalg.norm(vector)  # Normalize
            self.field_map[component] = {
                'vector': vector.tolist(),
                'created_at': datetime.now().isoformat(),
                'connections': []
            }
        else:
            vector = np.array(self.field_map[component]['vector'])
            
        # Update cache
        self.vector_cache[component] = vector
        if len(self.vector_cache) > self.cache_size:
            # Remove oldest entries
            oldest = next(iter(self.vector_cache))
            del self.vector_cache[oldest]
            
        return vector
        
    def calculate_semantic_distance(self, source: str, target: str) -> float:
        """
        Calculate semantic distance between two components.
        
        Args:
            source: Source component
            target: Target component
            
        Returns:
            float: Semantic distance [0-1]
        """
        cache_key = f"{source}→{target}"
        if cache_key in self.distance_cache:
            return self.distance_cache[cache_key]
            
        # Get component vectors
        source_vector = self.get_component_vector(source)
        target_vector = self.get_component_vector(target)
        
        # Calculate cosine similarity
        similarity = np.dot(source_vector, target_vector)
        
        # Convert to distance (1 - similarity)
        distance = 1.0 - similarity
        
        # Update cache
        self.distance_cache[cache_key] = distance
        if len(self.distance_cache) > self.cache_size:
            # Remove oldest entries
            oldest = next(iter(self.distance_cache))
            del self.distance_cache[oldest]
            
        # Log the search
        self.log_search(source, target, distance)
            
        return distance
        
    def update_component_vector(self, component: str, 
                              new_vector: np.ndarray,
                              decay: float = 0.1) -> None:
        """
        Update semantic vector for a component.
        
        Args:
            component: Component identifier
            new_vector: New semantic vector
            decay: Decay factor for old vector
        """
        if component not in self.field_map:
            self.field_map[component] = {
                'vector': new_vector.tolist(),
                'created_at': datetime.now().isoformat(),
                'connections': []
            }
        else:
            # Blend old and new vectors
            old_vector = np.array(self.field_map[component]['vector'])
            blended_vector = (1 - decay) * old_vector + decay * new_vector
            blended_vector = blended_vector / np.linalg.norm(blended_vector)
            
            self.field_map[component]['vector'] = blended_vector.tolist()
            self.field_map[component]['updated_at'] = datetime.now().isoformat()
            
        # Update cache
        self.vector_cache[component] = new_vector
        
    def add_semantic_connection(self, source: str, target: str, 
                              strength: float = 1.0) -> None:
        """
        Add semantic connection between components.
        
        Args:
            source: Source component
            target: Target component
            strength: Connection strength [0-1]
        """
        if source not in self.field_map:
            self.field_map[source] = {
                'vector': np.random.randn(100).tolist(),
                'created_at': datetime.now().isoformat(),
                'connections': []
            }
            
        connection = {
            'target': target,
            'strength': strength,
            'created_at': datetime.now().isoformat()
        }
        
        self.field_map[source]['connections'].append(connection)
        
    def get_semantic_neighbors(self, component: str, 
                             max_distance: float = 0.5) -> List[Tuple[str, float]]:
        """
        Get semantically similar components.
        
        Args:
            component: Component identifier
            max_distance: Maximum semantic distance
            
        Returns:
            List of (component, distance) tuples
        """
        neighbors = []
        component_vector = self.get_component_vector(component)
        
        for other in self.field_map:
            if other != component:
                distance = self.calculate_semantic_distance(component, other)
                if distance <= max_distance:
                    neighbors.append((other, distance))
                    
        return sorted(neighbors, key=lambda x: x[1])
        
    def get_semantic_path(self, source: str, target: str, 
                         max_distance: float = 0.7) -> Optional[List[str]]:
        """
        Find semantic path between components.
        
        Args:
            source: Source component
            target: Target component
            max_distance: Maximum semantic distance
            
        Returns:
            Optional[List[str]]: Path if found, None otherwise
        """
        # Use A* with semantic distance as heuristic
        open_set = {source}
        closed_set = set()
        came_from = {}
        g_score = {source: 0}
        f_score = {source: self.calculate_semantic_distance(source, target)}
        
        while open_set:
            current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
            
            if current == target:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(source)
                path.reverse()
                
                # Log the search with path
                self.log_search(source, target, 
                              self.calculate_semantic_distance(source, target),
                              path)
                return path
                
            open_set.remove(current)
            closed_set.add(current)
            
            for neighbor in self.get_semantic_neighbors(current, max_distance):
                if neighbor[0] in closed_set:
                    continue
                    
                tentative_g_score = g_score[current] + neighbor[1]
                
                if neighbor[0] not in open_set:
                    open_set.add(neighbor[0])
                elif tentative_g_score >= g_score.get(neighbor[0], float('inf')):
                    continue
                    
                came_from[neighbor[0]] = current
                g_score[neighbor[0]] = tentative_g_score
                f_score[neighbor[0]] = g_score[neighbor[0]] + \
                    self.calculate_semantic_distance(neighbor[0], target)
                    
        # Log failed search
        self.log_search(source, target, 
                       self.calculate_semantic_distance(source, target),
                       None)
        return None
        
    def get_semantic_cluster(self, component: str, 
                           max_distance: float = 0.3) -> Set[str]:
        """
        Get cluster of semantically related components.
        
        Args:
            component: Component identifier
            max_distance: Maximum semantic distance
            
        Returns:
            Set[str]: Set of related components
        """
        cluster = {component}
        to_process = {component}
        
        while to_process:
            current = to_process.pop()
            neighbors = self.get_semantic_neighbors(current, max_distance)
            
            for neighbor, distance in neighbors:
                if neighbor not in cluster:
                    cluster.add(neighbor)
                    to_process.add(neighbor)
                    
        return cluster 