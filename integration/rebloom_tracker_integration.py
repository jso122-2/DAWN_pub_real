#!/usr/bin/env python3
"""
rebloom_tracker_integration.py - Integration Layer for RebloomTracker
Connects the rebloom tracker with existing DAWN bloom management systems
"""

import os
import sys
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

# Add project root to path
if hasattr(sys, '_getframe'):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from rebloom_tracker import RebloomTracker, RebloomEvent, BloomNode

# Import existing DAWN systems
try:
    from schema.bloom import BloomGarden, BloomType, BloomStage
    SCHEMA_BLOOM_AVAILABLE = True
except ImportError:
    SCHEMA_BLOOM_AVAILABLE = False

try:
    from core.bloom_manager import BloomManager
    BLOOM_MANAGER_AVAILABLE = True
except ImportError:
    BLOOM_MANAGER_AVAILABLE = False

try:
    from bloom.unified_bloom_engine import BloomEngine
    UNIFIED_ENGINE_AVAILABLE = True
except ImportError:
    UNIFIED_ENGINE_AVAILABLE = False

try:
    from integration.vault.vault_manager import DawnVaultManager
    VAULT_MANAGER_AVAILABLE = True
except ImportError:
    VAULT_MANAGER_AVAILABLE = False


class IntegratedRebloomSystem:
    """
    Integrated rebloom system that connects RebloomTracker with existing DAWN components
    """
    
    def __init__(self, vault_path: str = ".", tracker_save_path: str = "memories/rebloom_tracker.json"):
        """Initialize the integrated rebloom system"""
        # Core tracker
        self.tracker = RebloomTracker()
        self.tracker_save_path = tracker_save_path
        
        # Integration with existing systems
        self.bloom_garden = None
        self.bloom_manager = None
        self.bloom_engine = None
        self.vault_manager = None
        
        # Initialize available systems
        self._initialize_systems(vault_path)
        
        # Load existing tracker state if available
        self._load_tracker_state()
        
        # Statistics
        self.integration_stats = {
            'blooms_tracked': 0,
            'reblooms_processed': 0,
            'genealogy_events': 0,
            'vault_syncs': 0
        }
        
        print(f"[RebloomIntegration] Initialized with systems: "
              f"Garden={self.bloom_garden is not None}, "
              f"Manager={self.bloom_manager is not None}, "
              f"Engine={self.bloom_engine is not None}, "
              f"Vault={self.vault_manager is not None}")
    
    def _initialize_systems(self, vault_path: str):
        """Initialize available DAWN systems"""
        if SCHEMA_BLOOM_AVAILABLE:
            try:
                self.bloom_garden = BloomGarden()
                print("[RebloomIntegration] ✅ Connected to BloomGarden")
            except Exception as e:
                print(f"[RebloomIntegration] ⚠️ BloomGarden init failed: {e}")
        
        if BLOOM_MANAGER_AVAILABLE:
            try:
                self.bloom_manager = BloomManager()
                print("[RebloomIntegration] ✅ Connected to BloomManager")
            except Exception as e:
                print(f"[RebloomIntegration] ⚠️ BloomManager init failed: {e}")
        
        if UNIFIED_ENGINE_AVAILABLE:
            try:
                self.bloom_engine = BloomEngine()
                print("[RebloomIntegration] ✅ Connected to BloomEngine")
            except Exception as e:
                print(f"[RebloomIntegration] ⚠️ BloomEngine init failed: {e}")
        
        if VAULT_MANAGER_AVAILABLE:
            try:
                self.vault_manager = DawnVaultManager(vault_path)
                print("[RebloomIntegration] ✅ Connected to VaultManager")
            except Exception as e:
                print(f"[RebloomIntegration] ⚠️ VaultManager init failed: {e}")
    
    def _load_tracker_state(self):
        """Load existing tracker state if available"""
        if os.path.exists(self.tracker_save_path):
            try:
                self.tracker.load_from_file(self.tracker_save_path)
                print(f"[RebloomIntegration] 📂 Loaded tracker state from {self.tracker_save_path}")
            except Exception as e:
                print(f"[RebloomIntegration] ⚠️ Failed to load tracker state: {e}")
    
    def _save_tracker_state(self):
        """Save tracker state"""
        try:
            os.makedirs(os.path.dirname(self.tracker_save_path), exist_ok=True)
            self.tracker.save_to_file(self.tracker_save_path)
            print(f"[RebloomIntegration] 💾 Saved tracker state to {self.tracker_save_path}")
        except Exception as e:
            print(f"[RebloomIntegration] ⚠️ Failed to save tracker state: {e}")
    
    def log_bloom_creation(self, bloom_id: str, parent_id: Optional[str] = None, 
                          entropy_diff: float = 0.0, metadata: Optional[Dict] = None) -> bool:
        """
        Log a new bloom creation or rebloom event
        
        Args:
            bloom_id: ID of the new bloom
            parent_id: ID of parent bloom (None for root blooms)
            entropy_diff: Entropy change from parent to child
            metadata: Additional metadata
            
        Returns:
            True if successfully logged
        """
        if parent_id is None:
            # Root bloom - just add to tracker without parent relationship
            if bloom_id not in self.tracker.nodes:
                root_node = BloomNode(bloom_id=bloom_id, depth=0)
                self.tracker.nodes[bloom_id] = root_node
                self.tracker.roots.add(bloom_id)
                self.tracker.depth_index[0].append(bloom_id)
                self.tracker.lineage_graph.add_node(bloom_id, depth=0)
                
                print(f"[RebloomIntegration] 🌱 Root bloom registered: {bloom_id}")
                self.integration_stats['blooms_tracked'] += 1
                return True
            return False
        else:
            # Rebloom - log the parent-child relationship
            success = self.tracker.log_rebloom(parent_id, bloom_id, entropy_diff, metadata)
            if success:
                print(f"[RebloomIntegration] 🌸 Rebloom tracked: {parent_id} → {bloom_id} (Δentropy: {entropy_diff:+.3f})")
                self.integration_stats['reblooms_processed'] += 1
                self.integration_stats['genealogy_events'] += 1
                
                # Auto-save tracker state after significant events
                if self.integration_stats['genealogy_events'] % 10 == 0:
                    self._save_tracker_state()
                
                return True
            return False
    
    def process_bloom_engine_event(self, bloom_data: Dict) -> bool:
        """
        Process a bloom event from the BloomEngine
        
        Args:
            bloom_data: Bloom data from engine
            
        Returns:
            True if successfully processed
        """
        if not self.bloom_engine:
            return False
        
        bloom_id = bloom_data.get('bloom_id')
        parent_id = bloom_data.get('parent_bloom')
        entropy_score = bloom_data.get('entropy_score', 0.5)
        
        if not bloom_id:
            return False
        
        # Calculate entropy diff if we have parent
        entropy_diff = 0.0
        if parent_id and parent_id in self.tracker.nodes:
            parent_entropy = self.tracker.nodes[parent_id].total_entropy_drift
            entropy_diff = entropy_score - parent_entropy
        
        # Extract metadata
        metadata = {
            'source': 'bloom_engine',
            'bloom_type': bloom_data.get('bloom_type', 'unknown'),
            'trigger_type': bloom_data.get('trigger_type', 'manual'),
            'mood': bloom_data.get('mood', 'neutral'),
            'lineage_depth': bloom_data.get('lineage_depth', 0)
        }
        
        return self.log_bloom_creation(bloom_id, parent_id, entropy_diff, metadata)
    
    def process_vault_rebloom(self, original_bloom_id: str, rebloom_id: str, 
                             evolution_data: Dict) -> bool:
        """
        Process a rebloom event from the VaultManager
        
        Args:
            original_bloom_id: ID of original bloom
            rebloom_id: ID of new rebloom
            evolution_data: Evolution metadata
            
        Returns:
            True if successfully processed
        """
        if not self.vault_manager:
            return False
        
        # Calculate entropy diff based on evolution
        entropy_diff = evolution_data.get('entropy_score', 0.1)
        
        metadata = {
            'source': 'vault_manager',
            'evolution_notes': evolution_data.get('evolution_notes'),
            'rebloom_generation': evolution_data.get('rebloom_generation', 1),
            'semantic_drift': evolution_data.get('semantic_drift', 0.0)
        }
        
        success = self.log_bloom_creation(rebloom_id, original_bloom_id, entropy_diff, metadata)
        
        if success:
            self.integration_stats['vault_syncs'] += 1
        
        return success
    
    def get_bloom_genealogy(self, bloom_id: str) -> Dict[str, Any]:
        """
        Get comprehensive genealogy information for a bloom
        
        Args:
            bloom_id: ID of the bloom
            
        Returns:
            Dictionary with genealogy information
        """
        if bloom_id not in self.tracker.nodes:
            return {'error': 'Bloom not found'}
        
        return {
            'bloom_id': bloom_id,
            'depth': self.tracker.get_depth(bloom_id),
            'ancestry_chain': self.tracker.get_ancestry_chain(bloom_id),
            'descendants': self.tracker.get_descendants(bloom_id),
            'siblings': self.tracker.get_siblings(bloom_id),
            'entropy_evolution': self.tracker.get_entropy_evolution(bloom_id),
            'node_info': {
                'creation_time': self.tracker.nodes[bloom_id].creation_time.isoformat(),
                'total_entropy_drift': self.tracker.nodes[bloom_id].total_entropy_drift,
                'children_count': len(self.tracker.nodes[bloom_id].children)
            }
        }
    
    def get_family_statistics(self, root_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get family tree statistics
        
        Args:
            root_id: Specific root to analyze (None for global stats)
            
        Returns:
            Dictionary with statistics
        """
        stats = self.tracker.get_lineage_statistics(root_id)
        
        # Add integration statistics
        stats['integration_stats'] = self.integration_stats.copy()
        
        # Add system availability
        stats['connected_systems'] = {
            'bloom_garden': self.bloom_garden is not None,
            'bloom_manager': self.bloom_manager is not None,
            'bloom_engine': self.bloom_engine is not None,
            'vault_manager': self.vault_manager is not None
        }
        
        return stats
    
    def get_rebloom_patterns(self, window_size: int = 20) -> Dict[str, Any]:
        """
        Get rebloom pattern analysis
        
        Args:
            window_size: Number of recent events to analyze
            
        Returns:
            Dictionary with pattern analysis
        """
        patterns = self.tracker.get_rebloom_patterns(window_size)
        
        # Add integration-specific patterns
        recent_events = self.tracker.rebloom_events[-window_size:] if self.tracker.rebloom_events else []
        
        source_distribution = {}
        for event in recent_events:
            source = event.metadata.get('source', 'unknown')
            source_distribution[source] = source_distribution.get(source, 0) + 1
        
        patterns['source_distribution'] = source_distribution
        patterns['integration_health'] = self._assess_integration_health()
        
        return patterns
    
    def _assess_integration_health(self) -> Dict[str, Any]:
        """Assess the health of system integrations"""
        total_events = sum(self.integration_stats.values())
        
        health = {
            'total_events': total_events,
            'tracking_active': total_events > 0,
            'genealogy_depth': self.tracker.max_depth_observed,
            'family_trees': len(self.tracker.roots),
            'last_activity': datetime.now().isoformat()
        }
        
        # Health score based on activity and connectivity
        connected_systems = sum([
            self.bloom_garden is not None,
            self.bloom_manager is not None, 
            self.bloom_engine is not None,
            self.vault_manager is not None
        ])
        
        health['connectivity_score'] = connected_systems / 4.0
        health['activity_score'] = min(total_events / 100.0, 1.0)
        health['overall_health'] = (health['connectivity_score'] + health['activity_score']) / 2.0
        
        return health
    
    def visualize_lineage_network(self, root_id: Optional[str] = None, 
                                format: str = 'dict') -> Dict[str, Any]:
        """
        Get visualization data for the lineage network
        
        Args:
            root_id: Specific root to visualize (None for all)
            format: Output format ('dict', 'networkx', 'graphviz')
            
        Returns:
            Visualization data in requested format
        """
        viz_data = self.tracker.visualize_lineage_graph(root_id)
        
        if format == 'dict':
            return viz_data
        elif format == 'networkx':
            # Return the NetworkX graph directly
            if root_id:
                descendants = self.tracker.get_descendants(root_id)
                nodes_to_include = [root_id] + descendants
                return self.tracker.lineage_graph.subgraph(nodes_to_include)
            else:
                return self.tracker.lineage_graph
        elif format == 'graphviz':
            # Generate Graphviz DOT format
            return self._generate_graphviz_output(viz_data)
        else:
            return viz_data
    
    def _generate_graphviz_output(self, viz_data: Dict) -> str:
        """Generate Graphviz DOT format for visualization"""
        dot_lines = ['digraph RebloomLineage {']
        dot_lines.append('  rankdir=TB;')
        dot_lines.append('  node [shape=circle, style=filled];')
        
        # Add nodes
        for node in viz_data['nodes']:
            node_id = node['id']
            depth = node['depth']
            entropy = node['entropy_drift']
            color = self._get_node_color(depth, entropy)
            
            dot_lines.append(f'  "{node_id}" [fillcolor="{color}", label="{node_id}\\nD:{depth}\\nE:{entropy:.2f}"];')
        
        # Add edges
        for edge in viz_data['edges']:
            source = edge['source']
            target = edge['target']
            entropy_diff = edge['entropy_diff']
            edge_color = 'green' if entropy_diff > 0 else 'red'
            
            dot_lines.append(f'  "{source}" -> "{target}" [color="{edge_color}", label="{entropy_diff:+.2f}"];')
        
        dot_lines.append('}')
        return '\n'.join(dot_lines)
    
    def _get_node_color(self, depth: int, entropy: float) -> str:
        """Get color for node based on depth and entropy"""
        if depth == 0:
            return 'lightblue'  # Root nodes
        elif entropy > 0.5:
            return 'orange'     # High entropy
        elif entropy < -0.5:
            return 'lightgreen' # Low entropy
        else:
            return 'lightyellow' # Neutral
    
    def sync_with_vault(self) -> int:
        """
        Sync rebloom tracker with vault manager blooms
        
        Returns:
            Number of blooms synchronized
        """
        if not self.vault_manager:
            return 0
        
        synced_count = 0
        
        try:
            # This would scan existing blooms in the vault and add them to tracker
            # Implementation would depend on vault structure
            print("[RebloomIntegration] 🔄 Vault sync not yet implemented")
            
        except Exception as e:
            print(f"[RebloomIntegration] ⚠️ Vault sync error: {e}")
        
        return synced_count
    
    def shutdown(self):
        """Shutdown the integration system and save state"""
        print("[RebloomIntegration] 🔄 Shutting down...")
        self._save_tracker_state()
        
        final_stats = self.get_family_statistics()
        print(f"[RebloomIntegration] 📊 Final stats: {final_stats['total_blooms']} blooms, "
              f"{final_stats['total_roots']} families, max depth {final_stats['max_depth']}")
        
        print("[RebloomIntegration] ✅ Shutdown complete")


# Convenience functions for external use
def create_integrated_rebloom_system(vault_path: str = ".") -> IntegratedRebloomSystem:
    """Create and return an integrated rebloom system"""
    return IntegratedRebloomSystem(vault_path)

def log_rebloom_event(system: IntegratedRebloomSystem, parent_id: str, child_id: str, 
                     entropy_diff: float, **metadata) -> bool:
    """Convenience function to log a rebloom event"""
    return system.log_bloom_creation(child_id, parent_id, entropy_diff, metadata)

def get_bloom_family_tree(system: IntegratedRebloomSystem, bloom_id: str) -> Dict:
    """Convenience function to get a bloom's family tree"""
    return system.get_bloom_genealogy(bloom_id)


if __name__ == "__main__":
    # Demo integration
    print("=== Integrated Rebloom System Demo ===\n")
    
    # Create system
    system = IntegratedRebloomSystem()
    
    # Simulate some bloom events
    print("📝 Simulating bloom events...")
    
    # Create root bloom
    system.log_bloom_creation("root_bloom_001", None, 0.0, {'source': 'test', 'type': 'root'})
    
    # Create child blooms
    system.log_bloom_creation("child_001", "root_bloom_001", 0.1, {'source': 'test', 'trigger': 'curiosity'})
    system.log_bloom_creation("child_002", "root_bloom_001", -0.05, {'source': 'test', 'trigger': 'memory'})
    
    # Create grandchildren
    system.log_bloom_creation("grand_001", "child_001", 0.15, {'source': 'test', 'trigger': 'synthesis'})
    system.log_bloom_creation("grand_002", "child_002", 0.08, {'source': 'test', 'trigger': 'evolution'})
    
    # Show results
    print("\n📊 Family Statistics:")
    stats = system.get_family_statistics()
    for key, value in stats.items():
        if key != 'integration_stats':
            print(f"  {key}: {value}")
    
    print("\n🌳 Genealogy for grand_001:")
    genealogy = system.get_bloom_genealogy("grand_001")
    for key, value in genealogy.items():
        if key != 'node_info':
            print(f"  {key}: {value}")
    
    print("\n🔍 Rebloom Patterns:")
    patterns = system.get_rebloom_patterns()
    for key, value in patterns.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {key}: {value}")
    
    # Clean shutdown
    system.shutdown() 