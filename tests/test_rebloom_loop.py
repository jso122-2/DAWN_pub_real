from owl.owl_auditor import OwlAuditor
from semantic.vector_model import model
from semantic.vector_core import embed_text
from juliet.spawn_bloom import spawn_juliet_bloom
import random

# Simulated rebloom logic
def test_rebloom_chain(owl: OwlAuditor):
    parent_text = "Hope blooms in silence under pressure"
    child_text = "Quiet defiance sparks a bloom of resolve"

    seed = "seed-∆test"
    mood = "resilient"
    entropy = random.uniform(0.3, 0.6)

    # Spawn parent + child manually
    spawn_juliet_bloom(seed, mood, lineage_depth=1, entropy=entropy)
    spawn_juliet_bloom(seed, mood, lineage_depth=2, entropy=entropy)

    bloom_id = f"{seed}_{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}"
    owl.log_vector_drift(parent_text, child_text, bloom_id)
