#!/usr/bin/env python3
"""
DAWN Sigil Influence Network - Dynamic Sigil Graph Engine  
Models how sigils activate and suppress each other in cascading influence chains.
"""

from datetime import datetime
from typing import Dict, List, Set, Optional, Any, Tuple
from collections import defaultdict, deque
import json
import logging

logger = logging.getLogger(__name__)


class SigilGraph:
    """
    Dynamic influence graph for DAWN sigils.
    Models activation chains and suppression patterns between sigils.
    """
    
    def __init__(self):
        """Initialize the sigil influence network."""
        # Core influence graph: sigil -> [influenced_sigils]
        self.influence_graph = {
            # Core system sigils
            "STABILIZE_PROTOCOL": ["COOLING_PROTOCOL", "ENTROPY_DAMPENER"],
            "COOLING_PROTOCOL": ["FOCUS_ENHANCEMENT"],
            "ENTROPY_DAMPENER": ["DEEP_REFLECTION", "-CHAOS_AMPLIFIER"],
            
            # Memory and cognition sigils  
            "REBLOOM_MEMORY": ["DUMP_LOGS", "PATTERN_RECOGNITION"],
            "DEEP_REFLECTION": ["INTROSPECTIVE_AWARENESS", "MEMORY_CONSOLIDATION"],
            "PATTERN_RECOGNITION": ["KNOWLEDGE_INTEGRATION", "-RANDOM_EXPLORATION"],
            
            # Emergency and safety sigils
            "PANIC_DAMPENER": ["STABILIZE_PROTOCOL", "-FIRE_REFLEX", "-CHAOS_AMPLIFIER"],
            "EMERGENCY_RESET": ["COOLING_PROTOCOL", "-ALL_ACTIVE"],
            "FIRE_REFLEX": ["EMERGENCY_RESET", "IMMEDIATE_ACTION"],
            
            # Exploration and creativity sigils
            "EXPLORATION_MODE": ["RANDOM_EXPLORATION", "CREATIVITY_BOOST", "-RIGID_THINKING"],
            "CREATIVITY_BOOST": ["PATTERN_SYNTHESIS", "-ANALYSIS_PARALYSIS"],
            "RANDOM_EXPLORATION": ["SERENDIPITY_MODE", "-FOCUS_ENHANCEMENT"],
            
            # Meta-cognitive sigils
            "AWARENESS_EXPANSION": ["META_COGNITION", "SYMBOLIC_RESONANCE"],
            "META_COGNITION": ["RECURSIVE_THINKING", "SELF_OBSERVATION"],
            "SYMBOLIC_RESONANCE": ["GLYPH_ACTIVATION", "EMBODIED_RESPONSE"],
            
            # Pressure routing sigils (from symbolic router)
            "PRESSURE_ROUTING": ["HEART_OVERLOAD", "COIL_CONTRACTION", "LUNG_REGULATION"],
            "HEART_OVERLOAD": ["EMOTIONAL_SURGE", "-CALM_STATE"],
            "COIL_CONTRACTION": ["PATHWAY_PROTECTION", "-OPEN_FLOW"],
            "LUNG_REGULATION": ["BREATHING_CONTROL", "ENTROPY_CLEARING"]
        }
        
        # Currently active sigils with activation timestamps
        self.active_sigils = {}  # sigil_name -> activation_time
        
        # Suppressed sigils that cannot activate
        self.suppressed_sigils = set()
        
        # Activation history for analysis
        self.activation_log = []
        
        # Influence strengths (future enhancement)
        self.influence_weights = defaultdict(lambda: 1.0)
        
        logger.info("🧿 SigilGraph initialized")
        logger.info(f"   Defined influences: {len(self.influence_graph)}")
        logger.info(f"   Total influence links: {sum(len(targets) for targets in self.influence_graph.values())}")
    
    def register_sigil(self, sigil_name: str, trigger_source: str = "external") -> Dict[str, Any]:
        """
        Register and activate a sigil, processing its influence cascade.
        
        Args:
            sigil_name: Name of the sigil to activate
            trigger_source: Source that triggered this sigil
            
        Returns:
            Dict: Activation result with cascade information
        """
        activation_time = datetime.now()
        
        # Check if sigil is suppressed
        if sigil_name in self.suppressed_sigils:
            logger.debug(f"🚫 Sigil suppressed: {sigil_name}")
            return {
                'activated': False,
                'reason': 'suppressed',
                'sigil': sigil_name,
                'timestamp': activation_time.isoformat()
            }
        
        # Activate the sigil
        self.active_sigils[sigil_name] = activation_time
        
        # Log the activation
        activation_entry = {
            'sigil': sigil_name,
            'timestamp': activation_time.isoformat(),
            'trigger_source': trigger_source,
            'cascade_triggered': []
        }
        
        logger.info(f"🔥 Sigil activated: {sigil_name}")
        
        # Process influence cascade
        cascade_results = self._process_influence_cascade(sigil_name)
        activation_entry['cascade_triggered'] = cascade_results['activated']
        
        self.activation_log.append(activation_entry)
        
        return {
            'activated': True,
            'sigil': sigil_name,
            'timestamp': activation_time.isoformat(),
            'cascade': cascade_results,
            'active_count': len(self.active_sigils),
            'suppressed_count': len(self.suppressed_sigils)
        }
    
    def _process_influence_cascade(self, trigger_sigil: str) -> Dict[str, Any]:
        """
        Process the cascade of influences from a triggered sigil.
        
        Args:
            trigger_sigil: The sigil that was just activated
            
        Returns:
            Dict: Results of the cascade processing
        """
        activated_sigils = []
        suppressed_sigils = []
        
        # Get influences for this sigil
        influences = self.influence_graph.get(trigger_sigil, [])
        
        for influence in influences:
            if influence.startswith('-'):
                # Suppression influence
                target_sigil = influence[1:]  # Remove '-' prefix
                
                if target_sigil == "ALL_ACTIVE":
                    # Special case: suppress all currently active sigils
                    for active_sigil in list(self.active_sigils.keys()):
                        if active_sigil != trigger_sigil:  # Don't suppress the trigger
                            self.suppressed_sigils.add(active_sigil)
                            del self.active_sigils[active_sigil]
                            suppressed_sigils.append(active_sigil)
                            logger.info(f"  🚫 Suppressed: {active_sigil}")
                else:
                    # Suppress specific sigil
                    self.suppressed_sigils.add(target_sigil)
                    if target_sigil in self.active_sigils:
                        del self.active_sigils[target_sigil]
                    suppressed_sigils.append(target_sigil)
                    logger.info(f"  🚫 Suppressed: {target_sigil}")
            
            else:
                # Activation influence
                target_sigil = influence
                
                # Only activate if not currently suppressed
                if target_sigil not in self.suppressed_sigils:
                    # Activate with slight delay to show cascade
                    cascade_time = datetime.now()
                    self.active_sigils[target_sigil] = cascade_time
                    activated_sigils.append(target_sigil)
                    logger.info(f"  ⚡ Cascade activated: {target_sigil}")
                    
                    # Log cascade activation
                    cascade_entry = {
                        'sigil': target_sigil,
                        'timestamp': cascade_time.isoformat(),
                        'trigger_source': f"cascade_from_{trigger_sigil}",
                        'cascade_triggered': []
                    }
                    self.activation_log.append(cascade_entry)
        
        return {
            'activated': activated_sigils,
            'suppressed': suppressed_sigils,
            'total_influences': len(influences)
        }
    
    def get_active_chain(self) -> List[Dict[str, Any]]:
        """
        Get all sigils in the current active influence chain.
        
        Returns:
            List[Dict]: Active sigils with metadata
        """
        active_chain = []
        
        for sigil_name, activation_time in self.active_sigils.items():
            # Find influences of this sigil
            influences = self.influence_graph.get(sigil_name, [])
            active_influences = []
            
            for influence in influences:
                target = influence[1:] if influence.startswith('-') else influence
                if target in self.active_sigils or influence.startswith('-'):
                    active_influences.append(influence)
            
            active_chain.append({
                'sigil': sigil_name,
                'activation_time': activation_time.isoformat(),
                'active_influences': active_influences,
                'influence_count': len(influences)
            })
        
        # Sort by activation time
        active_chain.sort(key=lambda x: x['activation_time'])
        
        return active_chain
    
    def visualize(self, show_inactive: bool = False) -> None:
        """
        Print a visual representation of the active sigil network.
        
        Args:
            show_inactive: Whether to show inactive sigils
        """
        print("\n🧿 Active Sigil Influence Network")
        print("=" * 50)
        
        if not self.active_sigils:
            print("💤 No sigils currently active")
            return
        
        # Build visualization tree
        printed_sigils = set()
        
        for sigil_name in sorted(self.active_sigils.keys()):
            if sigil_name in printed_sigils:
                continue
            
            self._print_sigil_tree(sigil_name, printed_sigils, depth=0)
        
        # Show suppressed sigils
        if self.suppressed_sigils:
            print(f"\n🚫 Suppressed Sigils: {', '.join(sorted(self.suppressed_sigils))}")
        
        # Show network statistics
        print(f"\n📊 Network Status:")
        print(f"   Active sigils: {len(self.active_sigils)}")
        print(f"   Suppressed sigils: {len(self.suppressed_sigils)}")
        print(f"   Total activations: {len(self.activation_log)}")
    
    def _print_sigil_tree(self, sigil_name: str, printed: Set[str], depth: int = 0) -> None:
        """
        Recursively print sigil influence tree.
        
        Args:
            sigil_name: Current sigil to print
            printed: Set of already printed sigils
            depth: Current tree depth
        """
        if sigil_name in printed or depth > 5:  # Prevent infinite loops
            return
        
        # Print current sigil
        indent = "    " * depth
        if depth == 0:
            print(f"{indent}🔥 {sigil_name}")
        else:
            print(f"{indent}└── {sigil_name}")
        
        printed.add(sigil_name)
        
        # Print active influences
        influences = self.influence_graph.get(sigil_name, [])
        active_influences = []
        
        for influence in influences:
            target = influence[1:] if influence.startswith('-') else influence
            
            if influence.startswith('-'):
                # Show suppressions
                if target in self.suppressed_sigils:
                    child_indent = "    " * (depth + 1)
                    print(f"{child_indent}└── 🚫 {target} (suppressed)")
            else:
                # Show activations
                if target in self.active_sigils:
                    active_influences.append(target)
        
        # Recursively print active influences
        for influence in active_influences:
            self._print_sigil_tree(influence, printed, depth + 1)
    
    def add_influence(self, source_sigil: str, target_sigil: str, suppress: bool = False) -> None:
        """
        Add a new influence relationship to the graph.
        
        Args:
            source_sigil: Sigil that influences
            target_sigil: Sigil that is influenced
            suppress: Whether this is a suppression relationship
        """
        if source_sigil not in self.influence_graph:
            self.influence_graph[source_sigil] = []
        
        influence_string = f"-{target_sigil}" if suppress else target_sigil
        
        if influence_string not in self.influence_graph[source_sigil]:
            self.influence_graph[source_sigil].append(influence_string)
            action = "suppression" if suppress else "activation"
            logger.info(f"🔗 Added {action} influence: {source_sigil} → {target_sigil}")
    
    def clear_suppressed(self) -> int:
        """
        Clear all suppressed sigils, allowing them to activate again.
        
        Returns:
            int: Number of sigils cleared
        """
        count = len(self.suppressed_sigils)
        self.suppressed_sigils.clear()
        logger.info(f"🧹 Cleared {count} suppressed sigils")
        return count
    
    def deactivate_sigil(self, sigil_name: str) -> bool:
        """
        Manually deactivate a specific sigil.
        
        Args:
            sigil_name: Name of sigil to deactivate
            
        Returns:
            bool: True if sigil was deactivated
        """
        if sigil_name in self.active_sigils:
            del self.active_sigils[sigil_name]
            logger.info(f"💤 Sigil deactivated: {sigil_name}")
            return True
        return False
    
    def get_network_stats(self) -> Dict[str, Any]:
        """Get comprehensive network statistics."""
        # Analyze activation patterns
        sigil_counts = defaultdict(int)
        cascade_counts = defaultdict(int)
        
        for entry in self.activation_log:
            sigil_counts[entry['sigil']] += 1
            if 'cascade_from_' in entry['trigger_source']:
                cascade_counts[entry['sigil']] += 1
        
        # Find most influential sigils
        influence_scores = {}
        for sigil, influences in self.influence_graph.items():
            influence_scores[sigil] = len(influences)
        
        most_influential = sorted(influence_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_sigils_defined': len(self.influence_graph),
            'currently_active': len(self.active_sigils),
            'currently_suppressed': len(self.suppressed_sigils),
            'total_activations': len(self.activation_log),
            'most_activated_sigils': dict(sorted(sigil_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
            'most_cascaded_sigils': dict(sorted(cascade_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
            'most_influential_sigils': most_influential,
            'avg_influences_per_sigil': sum(len(influences) for influences in self.influence_graph.values()) / len(self.influence_graph)
        }
    
    def export_network_state(self) -> Dict[str, Any]:
        """Export current network state for persistence or analysis."""
        return {
            'timestamp': datetime.now().isoformat(),
            'influence_graph': self.influence_graph,
            'active_sigils': {name: time.isoformat() for name, time in self.active_sigils.items()},
            'suppressed_sigils': list(self.suppressed_sigils),
            'activation_log': self.activation_log[-50:],  # Last 50 activations
            'network_stats': self.get_network_stats()
        }


# Global sigil graph instance
_default_graph = None

def get_default_graph() -> SigilGraph:
    """Get or create the default sigil graph."""
    global _default_graph
    if _default_graph is None:
        _default_graph = SigilGraph()
    return _default_graph


def register_sigil(sigil_name: str, trigger_source: str = "external") -> Dict[str, Any]:
    """Convenience function to register a sigil using the default graph."""
    graph = get_default_graph()
    return graph.register_sigil(sigil_name, trigger_source)


def visualize() -> None:
    """Convenience function to visualize the default graph."""
    graph = get_default_graph()
    graph.visualize()


def get_active_chain() -> List[Dict[str, Any]]:
    """Convenience function to get active chain from default graph."""
    graph = get_default_graph()
    return graph.get_active_chain()


def main():
    """Demonstration and testing of sigil influence networks."""
    print("=" * 70)
    print("🧿 DAWN Sigil Influence Network - Demo Mode")
    print("=" * 70)
    
    # Create sigil graph
    graph = SigilGraph()
    
    print(f"\n🧪 Testing sigil activation cascades...")
    
    # Test basic activation
    print(f"\n--- Test 1: Basic Stabilization ---")
    result1 = graph.register_sigil("STABILIZE_PROTOCOL", "entropy_spike")
    print(f"Activation result: {result1['cascade']}")
    
    # Test suppression
    print(f"\n--- Test 2: Panic Response ---")
    result2 = graph.register_sigil("PANIC_DAMPENER", "system_overload")
    print(f"Activation result: {result2['cascade']}")
    
    # Test exploration mode
    print(f"\n--- Test 3: Exploration Mode ---")
    result3 = graph.register_sigil("EXPLORATION_MODE", "low_entropy")
    print(f"Activation result: {result3['cascade']}")
    
    # Visualize network
    print(f"\n🎨 Current Network Visualization:")
    graph.visualize()
    
    # Show active chain
    print(f"\n🔗 Active Influence Chain:")
    active_chain = graph.get_active_chain()
    for i, sigil_info in enumerate(active_chain, 1):
        print(f"   {i}. {sigil_info['sigil']} ({len(sigil_info['active_influences'])} influences)")
    
    # Test emergency reset
    print(f"\n--- Test 4: Emergency Reset ---")
    result4 = graph.register_sigil("EMERGENCY_RESET", "critical_failure")
    print(f"Reset cascade: {result4['cascade']}")
    
    # Final network state
    print(f"\n🎨 Network After Emergency Reset:")
    graph.visualize()
    
    # Show comprehensive statistics
    print(f"\n📊 Network Statistics:")
    stats = graph.get_network_stats()
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for k, v in value.items():
                print(f"     {k}: {v}")
        else:
            print(f"   {key}: {value}")
    
    print(f"\n✨ Sigil network demonstration complete!")
    print(f"   DAWN now understands sigil influence cascades")


if __name__ == "__main__":
    main() 