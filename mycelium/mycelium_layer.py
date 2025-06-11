# mycelium/mycelium_layer.py
"""
Mycelium Layer - The Cognitive Substrate
========================================
The underground network that connects all thoughts and blooms
"""

from typing import Dict, List, Set, Optional, Any
from datetime import datetime
import random


class MyceliumLayer:
    """
    The mycelial substrate - a living network beneath DAWN's consciousness
    
    Like fungal networks in a forest, this layer connects blooms,
    shares nutrients (information), and enables emergent communication.
    """
    
    def __init__(self):
        # Core network structure
        self.roots: Dict[str, Dict[str, Any]] = {
            "seed://init": {
                "type": "primary",
                "created": datetime.now(),
                "connections": set(),
                "nutrients": 1.0,
                "depth": 0
            }
        }
        
        # Active connections between nodes
        self.connections: Dict[str, Set[str]] = {
            "seed://init": set()
        }
        
        # Nutrient flow tracking
        self.nutrient_flow: Dict[str, float] = {
            "seed://init": 1.0
        }
        
        # Network health
        self.health = 1.0
        self.growth_rate = 0.1
        self.active = True
        
        print("[MyceliumLayer] 🍄 Substrate layer initialized with primary root")
    
    def grow(self, source: Optional[str] = None) -> Dict[str, Any]:
        """
        Grow the mycelial network from a source point
        """
        print("[mycelium] Growing cognitive root network...")
        
        if source is None:
            source = "seed://init"
            
        # Calculate growth potential
        growth_potential = self.nutrient_flow.get(source, 0.5) * self.growth_rate
        
        # Create new root if growth is strong enough
        if growth_potential > 0.05 and random.random() < growth_potential:
            new_root_id = f"root://{len(self.roots)}_{int(datetime.now().timestamp())}"
            
            self.roots[new_root_id] = {
                "type": "secondary",
                "created": datetime.now(),
                "connections": {source},
                "nutrients": growth_potential,
                "depth": self.roots[source]["depth"] + 1
            }
            
            # Create bidirectional connection
            self.connections[new_root_id] = {source}
            self.connections[source].add(new_root_id)
            
            # Share nutrients
            self.nutrient_flow[new_root_id] = growth_potential
            
            print(f"[mycelium] New root grown: {new_root_id} (depth: {self.roots[new_root_id]['depth']})")
            
            return {
                "growth": True,
                "new_root": new_root_id,
                "connections": len(self.connections[new_root_id]),
                "nutrients": growth_potential
            }
        
        return {
            "growth": False,
            "reason": "insufficient nutrients or growth potential",
            "current_roots": len(self.roots)
        }
    
    def connect(self, root_a: str, root_b: str) -> bool:
        """
        Create a mycelial connection between two roots
        """
        if root_a in self.roots and root_b in self.roots:
            self.connections[root_a].add(root_b)
            self.connections[root_b].add(root_a)
            
            # Share nutrients through connection
            avg_nutrients = (self.nutrient_flow.get(root_a, 0) + 
                           self.nutrient_flow.get(root_b, 0)) / 2
            self.nutrient_flow[root_a] = avg_nutrients
            self.nutrient_flow[root_b] = avg_nutrients
            
            print(f"[mycelium] Connected {root_a} <-> {root_b}")
            return True
        return False
    
    def share_nutrients(self, source: str, amount: float) -> Dict[str, float]:
        """
        Distribute nutrients through the network from a source
        """
        if source not in self.roots:
            return {}
            
        # Add nutrients to source
        self.nutrient_flow[source] = self.nutrient_flow.get(source, 0) + amount
        
        # Distribute to connected roots
        distributed = {source: amount}
        connections = self.connections.get(source, set())
        
        if connections:
            share_amount = amount * 0.3 / len(connections)  # Share 30% equally
            for connected in connections:
                self.nutrient_flow[connected] = self.nutrient_flow.get(connected, 0) + share_amount
                distributed[connected] = share_amount
                
        return distributed
    
    def find_path(self, start: str, end: str) -> Optional[List[str]]:
        """
        Find a mycelial path between two roots
        """
        if start not in self.roots or end not in self.roots:
            return None
            
        # Simple BFS pathfinding
        visited = {start}
        queue = [(start, [start])]
        
        while queue:
            current, path = queue.pop(0)
            
            if current == end:
                return path
                
            for neighbor in self.connections.get(current, set()):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
                    
        return None
    
    def get_network_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the mycelial network
        """
        total_connections = sum(len(conns) for conns in self.connections.values()) // 2
        max_depth = max((root["depth"] for root in self.roots.values()), default=0)
        total_nutrients = sum(self.nutrient_flow.values())
        
        return {
            "total_roots": len(self.roots),
            "total_connections": total_connections,
            "max_depth": max_depth,
            "total_nutrients": total_nutrients,
            "health": self.health,
            "growth_rate": self.growth_rate,
            "active": self.active
        }
    
    def decay(self, rate: float = 0.01):
        """
        Natural decay process - nutrients dissipate over time
        """
        for root in self.nutrient_flow:
            self.nutrient_flow[root] *= (1 - rate)
            
        # Remove roots with no nutrients
        dead_roots = [root for root, nutrients in self.nutrient_flow.items() 
                     if nutrients < 0.001 and root != "seed://init"]
        
        for root in dead_roots:
            self._remove_root(root)
            
    def _remove_root(self, root: str):
        """
        Remove a dead root from the network
        """
        if root == "seed://init":
            return  # Never remove the primary root
            
        # Remove connections
        for connected in self.connections.get(root, set()).copy():
            if connected in self.connections:
                self.connections[connected].discard(root)
                
        # Remove root
        self.roots.pop(root, None)
        self.connections.pop(root, None)
        self.nutrient_flow.pop(root, None)
        
        print(f"[mycelium] Root decayed: {root}")
    
    def visualize_network(self) -> str:
        """
        Create a simple text visualization of the network
        """
        viz = "[Mycelium Network Map]\n"
        viz += "=" * 40 + "\n"
        
        # Sort roots by depth
        sorted_roots = sorted(self.roots.items(), 
                            key=lambda x: (x[1]["depth"], x[0]))
        
        for root_id, root_info in sorted_roots:
            indent = "  " * root_info["depth"]
            nutrients = self.nutrient_flow.get(root_id, 0)
            connections = len(self.connections.get(root_id, set()))
            
            viz += f"{indent}🌱 {root_id}\n"
            viz += f"{indent}   nutrients: {nutrients:.3f}\n"
            viz += f"{indent}   connections: {connections}\n"
            
        viz += "=" * 40 + "\n"
        viz += f"Total roots: {len(self.roots)}\n"
        viz += f"Network health: {self.health:.2f}\n"
        
        return viz
    
    def __repr__(self):
        stats = self.get_network_stats()
        return (f"<MyceliumLayer roots={stats['total_roots']} "
                f"connections={stats['total_connections']} "
                f"health={stats['health']:.2f}>")


# Create a global instance for the bloom engine to use
_global_mycelium = None

def get_mycelium() -> MyceliumLayer:
    """Get or create the global mycelium instance"""
    global _global_mycelium
    if _global_mycelium is None:
        _global_mycelium = MyceliumLayer()
    return _global_mycelium