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
            house: House/category the sigil belongs to
            priority: Priority level (0-3, where 0 is highest priority)
        """
        entry = {
            "id": sigil_id,
            "temp": temp,
            "house": house,
            "priority": priority
        }
        
        # Clamp priority to valid range 0-3
        ring = min(max(priority, 0), 3)
        self.rings[ring].append(entry)
        
        logger.debug(f"Added sigil {sigil_id} to ring {ring} (temp={temp}, house={house})")

    def decay_ring(self, temp_threshold: float = 20) -> None:
        """
        Remove sigils below temperature threshold from all rings.
        
        Args:
            temp_threshold: Minimum temperature for sigil retention
        """
        removed_count = 0
        
        for ring_level in self.rings:
            original_count = len(self.rings[ring_level])
            self.rings[ring_level] = [
                s for s in self.rings[ring_level] 
                if s["temp"] >= temp_threshold
            ]
            removed_count += original_count - len(self.rings[ring_level])
            
        if removed_count > 0:
            logger.info(f"Decayed {removed_count} sigils below temperature {temp_threshold}")

    def get_active_sigils(self) -> List[Dict[str, Any]]:
        """
        Get all active sigils ordered by priority (core to outer).
        
        Returns:
            List of sigil dictionaries ordered by ring priority
        """
        active = []
        for ring_level in sorted(self.rings):  # From core (0) outward (3)
            active.extend(self.rings[ring_level])
        return active

    def heat_sort(self) -> List[Dict[str, Any]]:
        """
        Get all sigils sorted by temperature (hottest first).
        
        Returns:
            List of sigil dictionaries sorted by temperature descending
        """
        sigils = self.get_active_sigils()
        return sorted(sigils, key=lambda s: s["temp"], reverse=True)

    def prune_outer_rings(self, keep_core: bool = True) -> int:
        """
        Prune sigils from outer rings, optionally preserving core ring.
        
        Args:
            keep_core: Whether to preserve the core ring (priority 0)
            
        Returns:
            Number of sigils pruned
        """
        pruned_count = 0
        start_ring = 1 if keep_core else 0
        
        for ring_level in range(start_ring, 4):
            pruned_count += len(self.rings[ring_level])
            self.rings[ring_level] = []
            
        if pruned_count > 0:
            logger.info(f"Pruned {pruned_count} sigils from outer rings (core preserved: {keep_core})")
            
        return pruned_count

    def get_ring_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the ring system.
        
        Returns:
            Dictionary containing ring statistics
        """
        stats = {
            "total_sigils": sum(len(ring) for ring in self.rings.values()),
            "ring_counts": {f"ring_{level}": len(ring) for level, ring in self.rings.items()},
            "average_temps": {},
            "houses_per_ring": {}
        }
        
        # Calculate average temperatures and house distributions
        for level, ring in self.rings.items():
            if ring:
                stats["average_temps"][f"ring_{level}"] = sum(s["temp"] for s in ring) / len(ring)
                houses = {}
                for sigil in ring:
                    house = sigil["house"]
                    houses[house] = houses.get(house, 0) + 1
                stats["houses_per_ring"][f"ring_{level}"] = houses
            else:
                stats["average_temps"][f"ring_{level}"] = 0.0
                stats["houses_per_ring"][f"ring_{level}"] = {}
                
        return stats

    def find_sigils_by_house(self, house: str) -> List[Dict[str, Any]]:
        """
        Find all sigils belonging to a specific house.
        
        Args:
            house: House name to search for
            
        Returns:
            List of sigils belonging to the specified house
        """
        matching_sigils = []
        for ring in self.rings.values():
            matching_sigils.extend([s for s in ring if s["house"] == house])
        return matching_sigils

    def update_sigil_temp(self, sigil_id: str, new_temp: float) -> bool:
        """
        Update the temperature of a specific sigil.
        
        Args:
            sigil_id: ID of the sigil to update
            new_temp: New temperature value
            
        Returns:
            True if sigil was found and updated, False otherwise
        """
        for ring in self.rings.values():
            for sigil in ring:
                if sigil["id"] == sigil_id:
                    old_temp = sigil["temp"]
                    sigil["temp"] = new_temp
                    logger.debug(f"Updated sigil {sigil_id} temperature: {old_temp} -> {new_temp}")
                    return True
        return False

    def __str__(self) -> str:
        """
        String representation of the sigil memory ring system.
        
        Returns:
            Human-readable string showing ring contents
        """
        lines = []
        total_sigils = sum(len(ring) for ring in self.rings.values())
        lines.append(f"SigilMemoryRing (Total: {total_sigils} sigils)")
        lines.append("=" * 50)
        
        for level in sorted(self.rings):
            sigils = self.rings[level]
            ring_name = ["Core", "Inner", "Mid", "Outer"][level]
            lines.append(f"{ring_name} Ring {level} ({len(sigils)} sigils):")
            
            if not sigils:
                lines.append("  (empty)")
            else:
                for s in sigils:
                    lines.append(f"  - {s['id']} | {s['house']} | Temp: {s['temp']:.1f} | Priority: {s['priority']}")
                    
        return "\n".join(lines) 