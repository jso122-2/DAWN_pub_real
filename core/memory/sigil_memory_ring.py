"""
SigilMemoryRing module for DAWN consciousness system.
Manages sigil memory with priority-based ring architecture.
"""

from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class SigilMemoryRing:
    """
    Priority-based sigil memory management system.
    Organizes sigils into concentric rings based on priority levels.
    """
    
    def __init__(self):
        """Initialize the sigil memory ring system."""
        # Priority rings: core (0 = highest), inner (1), mid (2), outer (3 = lowest)
        self.rings = {0: [], 1: [], 2: [], 3: []}
        logger.info("SigilMemoryRing initialized with 4 priority rings")

    def add_sigil(self, sigil_id: str, temp: float, house: str, priority: int) -> None:
        """
        Add a sigil to the appropriate priority ring.
        
        Args:
            sigil_id: Unique identifier for the sigil
            temp: Temperature/heat value of the sigil
            house: Cognitive house the sigil belongs to
            priority: Priority level (0-3, where 0 is highest priority)
        """
        # Validate priority level
        if priority not in self.rings:
            priority = 3  # Default to lowest priority if invalid
            
        sigil_data = {
            'id': sigil_id,
            'temp': temp,
            'house': house,
            'priority': priority
        }
        
        self.rings[priority].append(sigil_data)
        logger.debug(f"Added sigil {sigil_id} to priority ring {priority}")

    def get_ring_contents(self, priority: int) -> List[Dict[str, Any]]:
        """
        Get all sigils in a specific priority ring.
        
        Args:
            priority: Priority level (0-3)
            
        Returns:
            List of sigil data dictionaries
        """
        if priority not in self.rings:
            logger.warning(f"Invalid priority level: {priority}")
            return []
            
        return self.rings[priority].copy()

    def find_sigil(self, sigil_id: str) -> Dict[str, Any]:
        """
        Find a sigil by its ID across all rings.
        
        Args:
            sigil_id: The sigil ID to search for
            
        Returns:
            Sigil data dictionary if found, empty dict if not found
        """
        for priority, sigils in self.rings.items():
            for sigil in sigils:
                if sigil['id'] == sigil_id:
                    return sigil
                    
        logger.debug(f"Sigil {sigil_id} not found in any ring")
        return {}

    def remove_sigil(self, sigil_id: str) -> bool:
        """
        Remove a sigil from the ring system.
        
        Args:
            sigil_id: The sigil ID to remove
            
        Returns:
            True if sigil was found and removed, False otherwise
        """
        for priority, sigils in self.rings.items():
            for i, sigil in enumerate(sigils):
                if sigil['id'] == sigil_id:
                    removed_sigil = sigils.pop(i)
                    logger.info(f"Removed sigil {sigil_id} from priority ring {priority}")
                    return True
                    
        logger.warning(f"Attempted to remove non-existent sigil: {sigil_id}")
        return False

    def promote_sigil(self, sigil_id: str) -> bool:
        """
        Promote a sigil to a higher priority ring (lower number).
        
        Args:
            sigil_id: The sigil ID to promote
            
        Returns:
            True if promotion successful, False otherwise
        """
        # Find the sigil
        sigil_data = self.find_sigil(sigil_id)
        if not sigil_data:
            return False
            
        current_priority = sigil_data['priority']
        if current_priority == 0:
            logger.info(f"Sigil {sigil_id} already at highest priority")
            return False
            
        # Remove from current ring and add to higher priority ring
        if self.remove_sigil(sigil_id):
            new_priority = current_priority - 1
            sigil_data['priority'] = new_priority
            self.rings[new_priority].append(sigil_data)
            logger.info(f"Promoted sigil {sigil_id} from priority {current_priority} to {new_priority}")
            return True
            
        return False

    def demote_sigil(self, sigil_id: str) -> bool:
        """
        Demote a sigil to a lower priority ring (higher number).
        
        Args:
            sigil_id: The sigil ID to demote
            
        Returns:
            True if demotion successful, False otherwise
        """
        # Find the sigil
        sigil_data = self.find_sigil(sigil_id)
        if not sigil_data:
            return False
            
        current_priority = sigil_data['priority']
        if current_priority == 3:
            logger.info(f"Sigil {sigil_id} already at lowest priority")
            return False
            
        # Remove from current ring and add to lower priority ring
        if self.remove_sigil(sigil_id):
            new_priority = current_priority + 1
            sigil_data['priority'] = new_priority
            self.rings[new_priority].append(sigil_data)
            logger.info(f"Demoted sigil {sigil_id} from priority {current_priority} to {new_priority}")
            return True
            
        return False

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the ring system.
        
        Returns:
            Dictionary containing ring statistics
        """
        stats = {
            'total_sigils': sum(len(sigils) for sigils in self.rings.values()),
            'ring_counts': {priority: len(sigils) for priority, sigils in self.rings.items()}
        }
        
        # Calculate temperature statistics
        all_temps = []
        for sigils in self.rings.values():
            all_temps.extend([sigil['temp'] for sigil in sigils])
            
        if all_temps:
            stats['temperature_stats'] = {
                'avg': sum(all_temps) / len(all_temps),
                'min': min(all_temps),
                'max': max(all_temps)
            }
        else:
            stats['temperature_stats'] = {'avg': 0, 'min': 0, 'max': 0}
            
        return stats

    def clear_ring(self, priority: int) -> int:
        """
        Clear all sigils from a specific priority ring.
        
        Args:
            priority: Priority level (0-3)
            
        Returns:
            Number of sigils cleared
        """
        if priority not in self.rings:
            logger.warning(f"Invalid priority level: {priority}")
            return 0
            
        count = len(self.rings[priority])
        self.rings[priority].clear()
        logger.info(f"Cleared {count} sigils from priority ring {priority}")
        return count

    def clear_all_rings(self) -> int:
        """
        Clear all sigils from all rings.
        
        Returns:
            Total number of sigils cleared
        """
        total_cleared = 0
        for priority in self.rings:
            total_cleared += self.clear_ring(priority)
            
        logger.info(f"Cleared all rings, removed {total_cleared} sigils total")
        return total_cleared


# Testing and example usage
if __name__ == "__main__":
    print("🔮 SigilMemoryRing Test Suite")
    print("=" * 40)
    
    # Create a ring system
    ring_system = SigilMemoryRing()
    
    # Add some test sigils
    test_sigils = [
        ("sigil_alpha", 0.8, "cognitive", 0),
        ("sigil_beta", 0.6, "emotional", 1),
        ("sigil_gamma", 0.4, "memory", 2),
        ("sigil_delta", 0.2, "reflex", 3),
        ("sigil_epsilon", 0.9, "cognitive", 0)
    ]
    
    print("\n📥 Adding test sigils...")
    for sigil_id, temp, house, priority in test_sigils:
        ring_system.add_sigil(sigil_id, temp, house, priority)
        print(f"  Added {sigil_id} (temp: {temp}, house: {house}, priority: {priority})")
    
    # Display ring statistics
    print("\n📊 Ring Statistics:")
    stats = ring_system.get_stats()
    print(f"  Total sigils: {stats['total_sigils']}")
    print("  Ring distribution:")
    for priority, count in stats['ring_counts'].items():
        print(f"    Priority {priority}: {count} sigils")
    print(f"  Temperature stats: {stats['temperature_stats']}")
    
    # Test finding sigils
    print("\n🔍 Testing sigil lookup...")
    test_sigil = ring_system.find_sigil("sigil_gamma")
    if test_sigil:
        print(f"  Found: {test_sigil}")
    else:
        print("  Sigil not found")
    
    # Test promotion/demotion
    print("\n⬆️ Testing sigil promotion...")
    if ring_system.promote_sigil("sigil_gamma"):
        promoted_sigil = ring_system.find_sigil("sigil_gamma")
        print(f"  Promoted sigil_gamma to priority {promoted_sigil['priority']}")
    
    print("\n⬇️ Testing sigil demotion...")
    if ring_system.demote_sigil("sigil_alpha"):
        demoted_sigil = ring_system.find_sigil("sigil_alpha")
        print(f"  Demoted sigil_alpha to priority {demoted_sigil['priority']}")
    
    # Final statistics
    print("\n📊 Final Ring Statistics:")
    final_stats = ring_system.get_stats()
    for priority, count in final_stats['ring_counts'].items():
        print(f"  Priority {priority}: {count} sigils")
    
    print("\n🎉 SigilMemoryRing test completed!") 