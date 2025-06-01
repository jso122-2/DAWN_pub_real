import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import random
from bloom.bloom_emitter_handler import handle_bloom_emitted

class Bloom:
    def __init__(self, bloom_id, seed, mood, bloom_factor, lineage_depth, entropy_score):
        self.bloom_id = bloom_id
        self.seed = seed
        self.mood = mood
        self.bloom_factor = bloom_factor
        self.lineage_depth = lineage_depth
        self.entropy_score = entropy_score

# Emit 3 test blooms
for i in range(3):
    bloom = Bloom(
        bloom_id=f"whale-00{i}_test",
        seed=f"whale-00{i}",
        mood=random.choice(["anxious", "calm", "excited"]),
        bloom_factor=round(random.uniform(0.3, 0.9), 3),
        lineage_depth=random.randint(0, 5),
        entropy_score=round(random.uniform(0.1, 1.0), 3)
    )
    handle_bloom_emitted(bloom)
