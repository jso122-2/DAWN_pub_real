# sigil_memory_ring.py

class SigilMemoryRing:
    def __init__(self):
        # Priority rings: core (0 = highest), inner (1), mid (2), outer (3 = lowest)
        self.rings = {0: [], 1: [], 2: [], 3: []}

    def add_sigil(self, sigil_id, temp, house, priority):
        entry = {
            "id": sigil_id,
            "temp": temp,
            "house": house,
            "priority": priority
        }
        ring = min(max(priority, 0), 3)  # Clamp priority to 0–3
        self.rings[ring].append(entry)

    def decay_ring(self, temp_threshold=20):
        for ring_level in self.rings:
            self.rings[ring_level] = [s for s in self.rings[ring_level] if s["temp"] >= temp_threshold]

    def get_active_sigils(self):
        active = []
        for ring_level in sorted(self.rings):  # From core outward
            active.extend(self.rings[ring_level])
        return active

    def heat_sort(self):
        sigils = self.get_active_sigils()
        return sorted(sigils, key=lambda s: s["temp"], reverse=True)

    def __str__(self):
        lines = []
        for level in sorted(self.rings):
            sigils = self.rings[level]
            lines.append(f"Ring {level} ({len(sigils)} sigils):")
            for s in sigils:
                lines.append(f"  - {s['id']} | {s['house']} | Temp: {s['temp']} | Priority: {s['priority']}")
        return "\n".join(lines)
