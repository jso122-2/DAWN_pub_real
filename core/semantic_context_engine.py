import math
from collections import defaultdict

class semantic_context_engine:
    def __init__(self, decay_rate=0.95, pressure_alpha=1.2, recurrence_threshold=3):
        self.constellations = []
        self.recurrence_map = defaultdict(float)
        self.pressure_map = defaultdict(float)
        self.last_pressure = {}
        self.decay_rate = decay_rate
        self.pressure_alpha = pressure_alpha
        self.recurrence_threshold = recurrence_threshold
        self.tick = 0
        self.semantic_clusters = defaultdict(set)  # seed_id -> cluster of neighbors

    def observe(self, seed_id, signal_strength, mood_heat, urgency=1.0):
        """Ingests new signal, updates recurrence and pressure maps."""
        self.tick += 1
        self.recurrence_map[seed_id] += 1

        # Weighted pressure with urgency
        composite_pressure = (mood_heat * signal_strength) ** self.pressure_alpha * urgency
        self.pressure_map[seed_id] += composite_pressure

        # Track last pressure for drift detection
        self.last_pressure[seed_id] = composite_pressure

    def decay_maps(self):
        """Applies decay to keep memory dynamic."""
        for seed in list(self.recurrence_map.keys()):
            self.recurrence_map[seed] *= self.decay_rate
            if self.recurrence_map[seed] < 0.01:
                del self.recurrence_map[seed]

        for seed in list(self.pressure_map.keys()):
            self.pressure_map[seed] *= self.decay_rate
            if self.pressure_map[seed] < 0.01:
                del self.pressure_map[seed]

    def register_cluster(self, seed_id, neighbors):
        """Optional: define seed neighborhood for contextual spreading."""
        self.semantic_clusters[seed_id] = set(neighbors)

    def get_pressure_drift(self, seed_id):
        """Returns delta pressure since last tick."""
        current = self.pressure_map.get(seed_id, 0)
        last = self.last_pressure.get(seed_id, 0)
        return current - last

    def infer_context(self):
        """Derives current semantic core + high-pressure zones."""
        high_recurrence = [k for k, v in self.recurrence_map.items() if v >= self.recurrence_threshold]
        high_pressure_sorted = sorted(self.pressure_map.items(), key=lambda x: x[1], reverse=True)

        # Expand core_context by neighbors for a field effect
        expanded_context = set(high_recurrence)
        for seed in high_recurrence:
            expanded_context.update(self.semantic_clusters.get(seed, set()))

        return {
            "tick": self.tick,
            "core_context": list(expanded_context),
            "high_pressure_zone": [k for k, _ in high_pressure_sorted[:5]],
            "drift_vectors": {
                k: self.get_pressure_drift(k) for k in expanded_context
            }
        }

    def on_tick(self):
        """To be called every tick for decay and snapshot updates."""
        self.decay_maps()
