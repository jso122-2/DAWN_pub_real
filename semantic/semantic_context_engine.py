import math
from collections import defaultdict

class semantic_context_engine:
    def __init__(self, decay_rate=0.95, pressure_alpha=1.2, recurrence_threshold=3):
        self.constellations = []  # Optional: seed-pattern clusters (to be defined later)
        self.recurrence_map = defaultdict(float)      # How often seeds are accessed
        self.pressure_map = defaultdict(float)        # Accumulated semantic pressure
        self.last_pressure = {}                       # For drift comparison
        self.semantic_clusters = defaultdict(set)     # Local neighbors for context expansion
        self.decay_rate = decay_rate                  # Decay for soft forgetting
        self.pressure_alpha = pressure_alpha          # Exponential scale of pressure
        self.recurrence_threshold = recurrence_threshold  # Core context inclusion bar
        self.tick = 0

    def observe(self, seed_id, signal_strength, mood_heat, urgency=1.0):
        """
        Ingest signal into semantic field and reinforce seed dynamics.
        """
        self.tick += 1
        self.recurrence_map[seed_id] += 1

        # Composite pressure accounts for mood × signal × urgency
        composite_pressure = (mood_heat * signal_strength) ** self.pressure_alpha * urgency
        self.pressure_map[seed_id] += composite_pressure

        # Track most recent pressure for delta analysis
        self.last_pressure[seed_id] = composite_pressure

    def decay_maps(self):
        """
        Applies decay to recurrence and pressure memory maps.
        """
        for seed in list(self.recurrence_map.keys()):
            self.recurrence_map[seed] *= self.decay_rate
            if self.recurrence_map[seed] < 0.01:
                del self.recurrence_map[seed]

        for seed in list(self.pressure_map.keys()):
            self.pressure_map[seed] *= self.decay_rate
            if self.pressure_map[seed] < 0.01:
                del self.pressure_map[seed]

    def register_cluster(self, seed_id, neighbors):
        """
        Register semantic neighbors for a seed — helps propagate meaning locally.
        """
        self.semantic_clusters[seed_id] = set(neighbors)

    def get_pressure_drift(self, seed_id):
        """
        Returns pressure delta since last observation.
        """
        current = self.pressure_map.get(seed_id, 0)
        last = self.last_pressure.get(seed_id, 0)
        return current - last

    def infer_context(self):
        """
        Return a snapshot of current semantic pressure state.
        - Core context: persistent/high recurrence
        - High-pressure zones: volatile/reactive seeds
        - Drift vectors: changes since last tick
        """
        # Determine core seeds (frequency-based memory)
        high_recurrence = [k for k, v in self.recurrence_map.items() if v >= self.recurrence_threshold]

        # Sort by pressure for zone heat
        high_pressure_sorted = sorted(self.pressure_map.items(), key=lambda x: x[1], reverse=True)

        # Field effect — extend context by semantic neighbors
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
        """
        Called every tick to advance memory state.
        """
        self.decay_maps()


class SemanticContextEngine:
    """Semantic Context Engine - Understanding and meaning"""
    
    def __init__(self):
        self.active = False
        self.contexts = {}
        
    def initialize(self, event_bus=None):
        self.event_bus = event_bus
        self.active = True
        
    def add_context(self, key, context):
        """Add semantic context"""
        self.contexts[key] = context
        
    def get_context(self, key):
        """Retrieve semantic context"""
        return self.contexts.get(key)
        
    def process_meaning(self, text):
        """Process text for meaning"""
        # Simple processing
        return {
            'text': text,
            'length': len(text),
            'words': text.split()
        }
        
    def shutdown(self):
        self.active = False
        
    def get_status(self):
        return {
            'active': self.active,
            'contexts': len(self.contexts)
        }
