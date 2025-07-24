#!/usr/bin/env python3
"""
rebloom_tracker.py - Rebloom Chain Tracking for DAWN
Tracks genealogy, entropy evolution, and rebloom patterns in the cognitive system.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime, timedelta
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
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'RebloomEvent':
        """Create from dictionary"""
        return cls(
            parent_id=data['parent_id'],
            child_id=data['child_id'],
            entropy_diff=data['entropy_diff'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            metadata=data.get('metadata', {})
        )


@dataclass
class BloomGenealogy:
    """Tracks the genealogical tree of bloom reblooms"""
    bloom_id: str
    parent_ids: List[str] = field(default_factory=list)
    child_ids: List[str] = field(default_factory=list)
    generation: int = 0
    branch_depth: int = 0
    entropy_evolution: List[float] = field(default_factory=list)
    rebloom_count: int = 0
    
    def add_child(self, child_id: str, entropy_diff: float):
        """Add a child bloom to this genealogy"""
        self.child_ids.append(child_id)
        self.rebloom_count += 1
        self.entropy_evolution.append(entropy_diff)
    
    def get_entropy_trend(self) -> str:
        """Determine if entropy is increasing, decreasing, or stable"""
        if len(self.entropy_evolution) < 2:
            return "insufficient_data"
        
        recent_changes = self.entropy_evolution[-3:]
        avg_change = sum(recent_changes) / len(recent_changes)
        
        if avg_change > 0.1:
            return "increasing"
        elif avg_change < -0.1:
            return "decreasing"
        else:
            return "stable"


class RebloomTracker:
    """Advanced rebloom chain tracking and analysis system"""
    
    def __init__(self):
        """Initialize the rebloom tracker"""
        self.events: List[RebloomEvent] = []
        self.genealogies: Dict[str, BloomGenealogy] = {}
        self.rebloom_graph = nx.DiGraph()
        self.entropy_thresholds = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.8
        }
        
        # Analysis cache
        self._analysis_cache = {}
        self._cache_timestamp = datetime.now()
    
    def record_rebloom(self, parent_id: str, child_id: str, entropy_diff: float, 
                      metadata: Optional[Dict] = None) -> RebloomEvent:
        """Record a new rebloom event"""
        event = RebloomEvent(
            parent_id=parent_id,
            child_id=child_id,
            entropy_diff=entropy_diff,
            metadata=metadata or {}
        )
        
        self.events.append(event)
        
        # Update genealogies
        self._update_genealogy(parent_id, child_id, entropy_diff)
        
        # Update graph
        self.rebloom_graph.add_edge(parent_id, child_id, 
                                  entropy_diff=entropy_diff,
                                  timestamp=event.timestamp)
        
        # Clear analysis cache
        self._analysis_cache.clear()
        
        return event
    
    def _update_genealogy(self, parent_id: str, child_id: str, entropy_diff: float):
        """Update genealogical tracking"""
        # Update parent genealogy
        if parent_id not in self.genealogies:
            self.genealogies[parent_id] = BloomGenealogy(bloom_id=parent_id)
        
        parent_genealogy = self.genealogies[parent_id]
        parent_genealogy.add_child(child_id, entropy_diff)
        
        # Create child genealogy
        if child_id not in self.genealogies:
            self.genealogies[child_id] = BloomGenealogy(
                bloom_id=child_id,
                parent_ids=[parent_id],
                generation=parent_genealogy.generation + 1,
                branch_depth=parent_genealogy.branch_depth + 1
            )
    
    def get_rebloom_chains(self, min_length: int = 3) -> List[List[str]]:
        """Find rebloom chains of specified minimum length"""
        chains = []
        
        # Find all paths in the graph
        for source in self.rebloom_graph.nodes():
            if self.rebloom_graph.in_degree(source) == 0:  # Root node
                for target in self.rebloom_graph.nodes():
                    if self.rebloom_graph.out_degree(target) == 0:  # Leaf node
                        try:
                            paths = list(nx.all_simple_paths(
                                self.rebloom_graph, source, target, cutoff=10))
                            chains.extend([path for path in paths if len(path) >= min_length])
                        except nx.NetworkXNoPath:
                            continue
        
        return chains
    
    def analyze_entropy_evolution(self, bloom_id: str) -> Dict:
        """Analyze entropy evolution for a specific bloom"""
        if bloom_id not in self.genealogies:
            return {"error": "Bloom not found"}
        
        genealogy = self.genealogies[bloom_id]
        entropy_evolution = genealogy.entropy_evolution
        
        if not entropy_evolution:
            return {"status": "no_data"}
        
        analysis = {
            "bloom_id": bloom_id,
            "rebloom_count": len(entropy_evolution),
            "entropy_trend": genealogy.get_entropy_trend(),
            "avg_entropy_change": sum(entropy_evolution) / len(entropy_evolution),
            "entropy_variance": np.var(entropy_evolution) if len(entropy_evolution) > 1 else 0,
            "generation": genealogy.generation,
            "branch_depth": genealogy.branch_depth
        }
        
        # Classify entropy behavior
        avg_change = analysis["avg_entropy_change"]
        variance = analysis["entropy_variance"]
        
        if avg_change > 0.2 and variance > 0.1:
            analysis["pattern"] = "chaotic_growth"
        elif avg_change > 0.1:
            analysis["pattern"] = "steady_growth"
        elif avg_change < -0.1:
            analysis["pattern"] = "entropy_decay"
        elif variance < 0.05:
            analysis["pattern"] = "stable"
        else:
            analysis["pattern"] = "oscillating"
        
        return analysis
    
    def find_rebloom_hotspots(self, time_window_hours: int = 24) -> List[Dict]:
        """Find blooms with high rebloom activity in recent time window"""
        cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
        
        recent_events = [event for event in self.events 
                        if event.timestamp > cutoff_time]
        
        # Count reblooms per parent
        parent_counts = defaultdict(int)
        for event in recent_events:
            parent_counts[event.parent_id] += 1
        
        # Find hotspots (top 20% by activity)
        if not parent_counts:
            return []
        
        sorted_parents = sorted(parent_counts.items(), key=lambda x: x[1], reverse=True)
        hotspot_threshold = max(1, int(len(sorted_parents) * 0.2))
        
        hotspots = []
        for bloom_id, count in sorted_parents[:hotspot_threshold]:
            hotspot_data = {
                "bloom_id": bloom_id,
                "rebloom_count": count,
                "time_window_hours": time_window_hours
            }
            
            # Add genealogy data if available
            if bloom_id in self.genealogies:
                genealogy = self.genealogies[bloom_id]
                hotspot_data.update({
                    "generation": genealogy.generation,
                    "total_children": len(genealogy.child_ids),
                    "entropy_trend": genealogy.get_entropy_trend()
                })
            
            hotspots.append(hotspot_data)
        
        return hotspots
    
    def get_rebloom_network_stats(self) -> Dict:
        """Get comprehensive statistics about the rebloom network"""
        if not self.rebloom_graph.nodes():
            return {"error": "No rebloom data"}
        
        stats = {
            "total_blooms": len(self.rebloom_graph.nodes()),
            "total_reblooms": len(self.rebloom_graph.edges()),
            "network_density": nx.density(self.rebloom_graph),
            "average_rebloom_rate": len(self.rebloom_graph.edges()) / len(self.rebloom_graph.nodes()),
            "max_generation": max(g.generation for g in self.genealogies.values()) if self.genealogies else 0,
            "deepest_branch": max(g.branch_depth for g in self.genealogies.values()) if self.genealogies else 0
        }
        
        # Find most prolific bloomers
        out_degrees = dict(self.rebloom_graph.out_degree())
        if out_degrees:
            stats["most_prolific_bloom"] = max(out_degrees, key=out_degrees.get)
            stats["max_children"] = max(out_degrees.values())
        
        # Entropy distribution analysis
        entropy_diffs = [data['entropy_diff'] for _, _, data in self.rebloom_graph.edges(data=True)]
        if entropy_diffs:
            stats["entropy_stats"] = {
                "mean": np.mean(entropy_diffs),
                "std": np.std(entropy_diffs),
                "min": min(entropy_diffs),
                "max": max(entropy_diffs)
            }
        
        return stats
    
    def export_rebloom_data(self, filepath: str):
        """Export rebloom data to JSON file"""
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "events": [event.to_dict() for event in self.events],
            "genealogies": {
                bloom_id: {
                    "bloom_id": genealogy.bloom_id,
                    "parent_ids": genealogy.parent_ids,
                    "child_ids": genealogy.child_ids,
                    "generation": genealogy.generation,
                    "branch_depth": genealogy.branch_depth,
                    "entropy_evolution": genealogy.entropy_evolution,
                    "rebloom_count": genealogy.rebloom_count
                }
                for bloom_id, genealogy in self.genealogies.items()
            },
            "network_stats": self.get_rebloom_network_stats()
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
    
    def import_rebloom_data(self, filepath: str):
        """Import rebloom data from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Clear existing data
        self.events.clear()
        self.genealogies.clear()
        self.rebloom_graph.clear()
        
        # Import events
        for event_data in data.get('events', []):
            event = RebloomEvent.from_dict(event_data)
            self.events.append(event)
            
            # Rebuild graph
            self.rebloom_graph.add_edge(
                event.parent_id, event.child_id,
                entropy_diff=event.entropy_diff,
                timestamp=event.timestamp
            )
        
        # Import genealogies
        for bloom_id, genealogy_data in data.get('genealogies', {}).items():
            genealogy = BloomGenealogy(
                bloom_id=genealogy_data['bloom_id'],
                parent_ids=genealogy_data['parent_ids'],
                child_ids=genealogy_data['child_ids'],
                generation=genealogy_data['generation'],
                branch_depth=genealogy_data['branch_depth'],
                entropy_evolution=genealogy_data['entropy_evolution'],
                rebloom_count=genealogy_data['rebloom_count']
            )
            self.genealogies[bloom_id] = genealogy


# Example usage and testing
if __name__ == "__main__":
    print("🌸 DAWN Rebloom Tracker - Advanced Genealogy System")
    print("=" * 60)
    
    # Create tracker
    tracker = RebloomTracker()
    
    # Simulate some rebloom events
    print("\n🧪 Simulating rebloom events...")
    
    # Create a branching rebloom pattern
    tracker.record_rebloom("bloom_alpha", "bloom_beta", 0.15, {"trigger": "entropy_spike"})
    tracker.record_rebloom("bloom_alpha", "bloom_gamma", 0.08, {"trigger": "thermal_flux"})
    tracker.record_rebloom("bloom_beta", "bloom_delta", 0.22, {"trigger": "resonance"})
    tracker.record_rebloom("bloom_beta", "bloom_epsilon", -0.05, {"trigger": "decay"})
    tracker.record_rebloom("bloom_gamma", "bloom_zeta", 0.18, {"trigger": "cascade"})
    tracker.record_rebloom("bloom_delta", "bloom_eta", 0.12, {"trigger": "amplification"})
    
    # Analyze the network
    print("\n📊 Network Analysis:")
    stats = tracker.get_rebloom_network_stats()
    for key, value in stats.items():
        if key != "entropy_stats":
            print(f"  {key}: {value}")
    
    if "entropy_stats" in stats:
        print("  Entropy Statistics:")
        for key, value in stats["entropy_stats"].items():
            print(f"    {key}: {value:.4f}")
    
    # Find rebloom chains
    print("\n🔗 Rebloom Chains:")
    chains = tracker.get_rebloom_chains(min_length=3)
    for i, chain in enumerate(chains, 1):
        print(f"  Chain {i}: {' → '.join(chain)}")
    
    # Analyze specific bloom evolution
    print("\n🧬 Bloom Evolution Analysis:")
    for bloom_id in ["bloom_alpha", "bloom_beta", "bloom_delta"]:
        analysis = tracker.analyze_entropy_evolution(bloom_id)
        if "error" not in analysis:
            print(f"  {bloom_id}:")
            print(f"    Pattern: {analysis['pattern']}")
            print(f"    Trend: {analysis['entropy_trend']}")
            print(f"    Generation: {analysis['generation']}")
    
    print("\n🎉 Rebloom tracking demonstration complete!") 