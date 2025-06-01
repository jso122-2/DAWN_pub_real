import random
import math

GLOW_TRACE_THRESHOLD = 0.7
VOLATILITY_DECAY = 0.02  # simulated nutrient loss

class RhizomeEdge:
    def __init__(self, weight=1.0):
        self.weight = weight
        self.reinforcement_score = 0.0
        self.last_pulse_tick = 0
        self.glow_intensity = 0.0  # [0.0–1.0]

    def reinforce(self, amount):
        self.reinforcement_score += amount
        self.glow_intensity = min(1.0, self.glow_intensity + amount / 10)

    def decay(self):
        self.glow_intensity = max(0.0, self.glow_intensity - VOLATILITY_DECAY)

class RhizomeNode:
    def __init__(self, bloom):
        self.seed_id = bloom.seed_id
        self.edges = {}  # target_seed_id → RhizomeEdge
        self.semantic_vector = None
        self.nutrient_reservoir = {}
        self.activity_log = []

    def add_edge(self, target_seed, weight=1.0):
        self.edges[target_seed] = RhizomeEdge(weight=weight)
        self.activity_log.append(f"🔗 Edge added → {target_seed} (w={weight})")

    def decay_edges(self):
        for edge in self.edges.values():
            edge.decay()

# 🧠 Mood + rebloom stress as edge volatility
def scan_edge_volatility(bloom, edge_count=None):
    mood = bloom.mood
    instability = {
        "anxious": 0.8,
        "curious": 0.5,
        "reflective": 0.3,
        "joyful": 0.2,
        "calm": 0.1
    }
    noise = random.uniform(-0.1, 0.1)
    base = instability.get(mood, 0.4)

    # Factor in structure instability (more edges → less coherent)
    edge_factor = min(1.0, 0.3 + (1 / (edge_count + 1))) if edge_count else 0.0

    return min(1.0, max(0.0, base + noise + edge_factor))

# 🍄 Detect ephemeral glow-traces from rebloomed semantic trails
def detect_glow_trace(bloom):
    """
    Detects if this bloom's lineage and emotional tone trigger a traceable ephemeral shimmer.
    Often seen in high-stress reblooms or semantic entanglement points.
    """
    depth = getattr(bloom, "lineage_depth", 0)
    mood = getattr(bloom, "mood", "")
    entropy = getattr(bloom, "entropy_score", 0.0)

    glow_probability = 0.0
    if depth >= 4:
        if mood in ["anxious", "overload", "joyful"]:
            glow_probability += 0.3
        if entropy > 0.6:
            glow_probability += 0.4
        if getattr(bloom, "bloom_factor", 0.0) > 1.0:
            glow_probability += 0.3

    return glow_probability > GLOW_TRACE_THRESHOLD
